#!/usr/bin/env python3
"""Inset finished frames onto a printed-paper panel, identically, every time.

Riso frames came back with a band of bare paper around the inked area, like a panel
on a printed page. It looks right and Isaac wanted it kept — but asked for in the
prompt the model gave one wide panel and one nearly square, and an inconsistent
structural border across a film reads as sloppiness, not design. That is exactly why
the ledger world forbade its margin rule.

So the model draws full bleed and this adds the panel: same inset, same paper, same
result on every frame. Idempotent-safe only in the sense that you should run it on
raw frames once — it does not detect an existing panel.

Usage: panel.py <film-dir> [--inset 0.055] [--paper auto|#RRGGBB]
"""
import sys, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

argv = sys.argv[1:]
if not argv or argv[0].startswith('--'):
    print(__doc__); sys.exit(1)
FILM = Path(argv[0]).resolve()
def arg(n, d):
    return argv[argv.index('--'+n)+1] if '--'+n in argv else d
INSET = float(arg('inset', 0.055))          # fraction of width, per side
PAPER = arg('paper', 'auto')

frames = sorted((FILM/'public'/'images'/'frames').glob('*-final.png'))
if not frames:
    print('no frames'); sys.exit(1)

if PAPER == 'auto':
    # Sample the paper from the frames themselves: the modal near-neutral bright
    # pixel across a handful of images. Hard-coding it would drift from the world.
    sam = []
    for f in frames[:8]:
        a = np.array(Image.open(f).convert('RGB')).astype(int)
        mx, mn = a.max(2), a.min(2)
        m = (mx > 200) & ((mx - mn) < 30)
        if m.sum() > 1000:
            sam.append(np.median(a[m], axis=0))
    r, g, b = (int(round(v)) for v in np.median(np.array(sam), axis=0))
else:
    r, g, b = (int(PAPER[i:i+2], 16) for i in (1, 3, 5))
paper = f'rgb({r},{g},{b})'
print(f'paper {paper} | inset {INSET:.3f} | {len(frames)} frames')

W, H = 1920, 1080
iw = int(round(W * (1 - 2 * INSET)))
ih = int(round(iw * H / W))
x, y = (W - iw) // 2, (H - ih) // 2
for f in frames:
    subprocess.run(['magick', '-size', f'{W}x{H}', f'xc:{paper}',
                    '(', str(f), '-resize', f'{iw}x{ih}!', ')',
                    '-geometry', f'+{x}+{y}', '-composite', str(f)], check=True)
print(f'panelled {len(frames)} frames -> inner {iw}x{ih} at +{x}+{y}')
