#!/usr/bin/env python3
"""Audit generated frames for the two defects the generator reliably produces.

Neither check is sufficient alone, and finding that out cost two pilot rounds:

  TRIM BBOX   catches an INSET PANEL - a drawing sitting on a margin, often
              with its own printed border. Cheap and decisive when the panel
              has an ink edge.
              But on a flat-fill style it also fires on every frame whose
              drawing simply does not touch the canvas edge, which is most of
              them. On its own it is a false-positive machine - the rituals
              film had 71 of 86 frames flagged this way and almost all were
              fine.

  CORNERS     catches a BORDER or a differently-coloured margin: sample the
              four corners and require them to agree with each other and with
              the paper. Immune to the "drawing does not reach the edge"
              false positive.
              But it passes an inset panel whose surround happens to be the
              same paper colour - exactly what frame 045a did.

So: corners decide whether the edge is clean, and the bbox is reported
alongside as context for a human looking at a flagged frame. A frame fails
only on the corner test or on an ink-coloured corner.

Usage: python3 frame-audit.py <dir> [--paper F4E8C8] [--tolerance 12]
"""
import re
import subprocess
import sys
from pathlib import Path


def px(path, x, y):
    out = subprocess.run(
        ['magick', str(path), '-format', f'%[pixel:p{{{x},{y}}}]', 'info:'],
        capture_output=True, text=True).stdout
    m = re.search(r'\((\d+),\s*(\d+),\s*(\d+)', out)
    return tuple(int(g) for g in m.groups()) if m else None


def bbox(path):
    return subprocess.run(['magick', str(path), '-fuzz', '4%', '-format', '%@', 'info:'],
                          capture_output=True, text=True).stdout.strip()


def size(path):
    return subprocess.run(['magick', str(path), '-format', '%wx%h', 'info:'],
                          capture_output=True, text=True).stdout.strip()


def main(d, paper, tol):
    files = sorted(Path(d).glob('*-final.png'))
    if not files:
        sys.exit(f'no *-final.png in {d}')
    want = tuple(int(paper[i:i+2], 16) for i in (0, 2, 4))
    bad = []

    for f in files:
        w, h = (int(v) for v in size(f).split('x'))
        corners = [px(f, 0, 0), px(f, w-1, 0), px(f, 0, h-1), px(f, w-1, h-1)]
        spread = max(max(c[i] for c in corners) - min(c[i] for c in corners)
                     for i in range(3))
        off = max(abs(sum(c[i] for c in corners)//4 - want[i]) for i in range(3))
        # A dark corner means ink at the edge: a printed border, not paper.
        darkest = min(sum(c)//3 for c in corners)

        fail = []
        if spread > tol:
            fail.append(f'corners disagree by {spread}')
        if darkest < 140:
            fail.append(f'ink at corner (luma {darkest})')
        if off > 40:
            fail.append(f'paper off target by {off}')

        if fail:
            bad.append((f.name, '; '.join(fail), bbox(f)))

    print(f'{len(files)} frames · {len(files)-len(bad)} clean · {len(bad)} flagged')
    for name, why, bb in bad:
        print(f'  FLAG {name:<18} {why:<34} bbox {bb}')
    return 1 if bad else 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    g = lambda n, d: (sys.argv[sys.argv.index(f'--{n}')+1]
                      if f'--{n}' in sys.argv else d)
    sys.exit(main(args[0], g('paper', 'F4E8C8').lstrip('#'), int(g('tolerance', '12'))))
