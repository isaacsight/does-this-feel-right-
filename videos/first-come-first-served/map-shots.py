#!/usr/bin/env python3
"""Build the cut from the board's frame-to-line mapping, not from an even spread.

The first assembly allocated 88 frames across 94 sentences proportional to word
count, because the board's table looked unparseable. It is parseable - the rows
are `| **b01** | *"line"* | dur | motion |` and the earlier grep looked for
backticks. The result was every picture landing near its line instead of on it,
which is the one thing the storyboard chair exists to prevent.

Each frame's start is the start of the first word of its own narration line,
located in audio/words.json by matching the line's token sequence. A frame holds
until the next frame's line begins.
"""
import re, json, sys
from pathlib import Path

FILM = Path(__file__).resolve().parent
words = json.loads((FILM / 'audio' / 'words.json').read_text())

# The sentences come from the script itself. The original derived them by parsing
# the storyboard's markdown table; this board is generated and has no such table,
# and board.json's `line` field is the sentence text rather than its index.
sents = [s.strip()
         for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text()) if a.strip()
         for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

frames = json.loads((FILM / 'production' / 'board.json').read_text())

# A sentence may carry several frames, so ids are the SENTENCE number plus a
# letter suffix for the extras (b18, b18b, b18c) rather than a running count.
# The invariants that still matter: every sentence has at least one frame, no
# duplicate ids, and the rows never run backwards through the script.
got = [f['id'] for f in frames]
covered = {f['line_no'] for f in frames}
problems = []
if len(set(got)) != len(got):
    problems.append('duplicate frame ids')
if sorted(covered) != list(range(1, len(sents) + 1)):
    problems.append(f'sentences with no frame: '
                    f'{sorted(set(range(1, len(sents) + 1)) - covered)[:12]}')
if [f['line_no'] for f in frames] != sorted(f['line_no'] for f in frames):
    problems.append('board rows run backwards through the script')
if problems:
    for p_ in problems:
        print(p_, file=sys.stderr)
    sys.exit(1)

norm = lambda s: re.sub(r'[^a-z0-9 ]', '', s.lower().replace('-', ' ')).split()
wtok = [norm(w['word']) for w in words]
flat = []                      # (token, word_index)
for i, toks in enumerate(wtok):
    for tk in toks:
        flat.append((tk, i))
seq = [tk for tk, _ in flat]

# Match each SENTENCE once, not each frame. Frames may share a sentence now, and
# two frames carrying the same line have identical text — a per-frame scan that
# advances a cursor finds the first and then can never find the second, which
# left 72 of 89 frames unmatched and produced a 195-second hold.
cursor = 0
sent_idx = {}
unmatched_sents = []
for n, sent in enumerate(sents, 1):
    toks = norm(sent)
    hit = None
    for ln in range(min(8, len(toks)), 2, -1):
        probe = toks[:ln]
        for s in range(cursor, len(seq) - ln + 1):
            if seq[s:s + ln] == probe:
                hit = flat[s][1]
                break
        if hit is not None:
            break
    if hit is None:
        unmatched_sents.append(n)
        sent_idx[n] = None
    else:
        sent_idx[n] = hit
        cursor = max(cursor, next(i for i, (_, wi) in enumerate(flat) if wi == hit) + 1)

# A sentence that failed to match sits midway between its resolved neighbours, so
# one miss cannot shift every later frame.
for n in range(1, len(sents) + 1):
    if sent_idx[n] is None:
        prev = next((sent_idx[m] for m in range(n - 1, 0, -1) if sent_idx[m] is not None), 0)
        nxt = next((sent_idx[m] for m in range(n + 1, len(sents) + 1) if sent_idx[m] is not None),
                   len(words) - 1)
        sent_idx[n] = (prev + nxt) // 2

for f in frames:
    f['widx'] = sent_idx[f['line_no']]

total = words[-1]['end']

# Group frames by the sentence they sit under, in order.
from itertools import groupby
groups = [(k, list(g)) for k, g in groupby(frames, key=lambda f: f.get('line_no'))]
anchors = []
for gi, (line_no, grp) in enumerate(groups):
    s = words[grp[0]['widx']]['start']
    e = (words[groups[gi + 1][1][0]['widx']]['start']
         if gi + 1 < len(groups) else total)
    step = (e - s) / len(grp)
    for k, f in enumerate(grp):
        f['_start'] = s + step * k
        f['_end'] = s + step * (k + 1)

shots = []
for i, f in enumerate(frames):
    start = f['_start']
    end = f['_end']
    shots.append({'id': f['id'], 'start': round(start, 3), 'end': round(end, 3),
                  'dur': round(max(0.7, end - start), 3),
                  'camera': f['camera'], 'expression': f['expression'],
                  'line': f['line'][:70]})

(FILM / 'build').mkdir(exist_ok=True)
(FILM / 'build' / 'shots.json').write_text(json.dumps(shots, indent=1))

# SENTENCE spans, for captions and for cutting verticals.
#
# Captions must follow the SCRIPT, not the frame book. Now that a sentence can
# carry four frames, a caption built from shots.json would repeat the same words
# four times over — and shots.json truncates `line` to 70 characters for the
# console, so it is not even the full sentence. Both are reasons to write the
# spans from the same matcher that produced the shots, once, here.
beats = []
for n, sent in enumerate(sents, 1):
    s = words[sent_idx[n]]['start']
    e = words[sent_idx[n + 1]]['start'] if n < len(sents) else total
    beats.append({'n': n, 'start': round(s, 3), 'duration': round(max(0.3, e - s), 3),
                  'line': sent})
(FILM / 'production' / 'beats-conformed.json').write_text(
    json.dumps({'beats': beats}, indent=1))

d = [s['dur'] for s in shots]

print(f'{len(shots)} shots  total {total:.1f}s')
print(f'  hold  min {min(d):.2f}  mean {sum(d)/len(d):.2f}  max {max(d):.2f}')

if unmatched_sents:
    print(f'  sentences unmatched, interpolated: {unmatched_sents}')
