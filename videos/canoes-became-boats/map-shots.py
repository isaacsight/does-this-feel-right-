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

want = [f'b{i:02d}' for i in range(1, len(frames) + 1)]
got = [f['id'] for f in frames]
if got != want:
    print(f'board rows {len(got)}; missing {set(want)-set(got)}', file=sys.stderr)
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

d = [s['dur'] for s in shots]

print(f'{len(shots)} shots  total {total:.1f}s')
print(f'  hold  min {min(d):.2f}  mean {sum(d)/len(d):.2f}  max {max(d):.2f}')

if unmatched_sents:
    print(f'  sentences unmatched, interpolated: {unmatched_sents}')
