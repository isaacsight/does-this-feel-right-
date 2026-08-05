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
board = (FILM / 'STORYBOARD.md').read_text()
words = json.loads((FILM / 'audio' / 'words.json').read_text())

# This film's board is generated, so read board.json directly rather than parsing
# the markdown back out — the MOVE column has to survive to the cut, and a regex
# round-trip through a table is exactly where that kind of column gets lost.
frames = json.loads((FILM / 'production' / 'board.json').read_text())
for f in frames:
    f['board_dur'] = 0.0

want = [f'b{i:02d}' for i in range(1, len(frames) + 1)]
got = [f['id'] for f in frames]
if got != want:
    print(f'board rows {len(got)}, expected 88; missing {set(want)-set(got)}', file=sys.stderr)
    sys.exit(1)

norm = lambda s: re.sub(r'[^a-z0-9 ]', '', s.lower().replace('-', ' ')).split()
wtok = [norm(w['word']) for w in words]
flat = []                      # (token, word_index)
for i, toks in enumerate(wtok):
    for t in toks:
        flat.append((t, i))
seq = [t for t, _ in flat]

cursor = 0
unmatched = []
for f in frames:
    toks = norm(f['line'])
    if not toks:
        unmatched.append(f['id']); f['widx'] = None; continue
    # Search forward from the cursor: the board is in narration order, so a line can
    # never legitimately match earlier than the previous one. Try the longest prefix
    # that still resolves, so a line the narrator elided slightly still lands.
    hit = None
    for n in range(min(8, len(toks)), 2, -1):
        probe = toks[:n]
        for s in range(cursor, len(seq) - n + 1):
            if seq[s:s + n] == probe:
                hit = flat[s][1]; break
        if hit is not None:
            break
    if hit is None:
        unmatched.append(f['id']); f['widx'] = None
    else:
        f['widx'] = hit
        cursor = max(cursor, next(i for i, (_, wi) in enumerate(flat) if wi == hit) + 1)

# Any frame that failed to match is placed midway between its resolved neighbours,
# rather than dropped - a missing anchor must not shift every later frame.
for i, f in enumerate(frames):
    if f['widx'] is not None:
        continue
    prev = next((frames[j]['widx'] for j in range(i - 1, -1, -1) if frames[j]['widx'] is not None), 0)
    nxt = next((frames[j]['widx'] for j in range(i + 1, len(frames)) if frames[j]['widx'] is not None),
               len(words) - 1)
    f['widx'] = (prev + nxt) // 2

total = words[-1]['end']
shots = []
for i, f in enumerate(frames):
    start = words[f['widx']]['start']
    end = words[frames[i + 1]['widx']]['start'] if i + 1 < len(frames) else total
    shots.append({'id': f['id'], 'start': round(start, 3), 'end': round(end, 3),
                  'dur': round(max(0.7, end - start), 3),
                  'camera': f['camera'], 'move': f['move'],
                  'expression': f['expression'], 'line': f['line'][:70]})

(FILM / 'build').mkdir(exist_ok=True)
(FILM / 'build' / 'shots.json').write_text(json.dumps(shots, indent=1))

d = [s['dur'] for s in shots]
from collections import Counter
mv = Counter(s['move'] for s in shots)
print(f'{len(shots)} shots  total {total:.1f}s')
print(f'  hold  min {min(d):.2f}  mean {sum(d)/len(d):.2f}  max {max(d):.2f}')
print('  moves  ' + '  '.join(f'{k}={v}' for k, v in sorted(mv.items())))
if unmatched:
    print(f'  UNMATCHED (interpolated): {" ".join(unmatched)}')
