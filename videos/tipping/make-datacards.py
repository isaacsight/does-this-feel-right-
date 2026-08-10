#!/usr/bin/env python3
"""The four data frames, built deterministically — the model never draws data.

Card grammar for the stills catalog: the painted world's cream ground and
palette, one condensed mid-century face, one fact per card, no chart junk.
Each card carries ONLY what its narration line says — the seven states, the
repeal, the number, the halving. Nothing invented.
"""
import subprocess
from pathlib import Path

FILM = Path(__file__).resolve().parent
OUT = FILM / 'public' / 'images' / 'frames'
OUT.mkdir(parents=True, exist_ok=True)

FONT = '/System/Library/Fonts/Avenir Next Condensed.ttc'
CREAM = '#FAF3E3'
INK = '#24425C'      # ink blue
VERMILION = '#C6431F'
MUSTARD = '#C99A2E'
W, H = 1920, 1080

def base():
    return ['magick', '-size', f'{W}x{H}', f'xc:{CREAM}',
            '-attenuate', '0.18', '+noise', 'Gaussian', '-colorspace', 'sRGB']

def txt(cmd, text, pt, fill, y, kerning=6, x=0):
    cmd += ['-font', FONT, '-pointsize', str(pt), '-kerning', str(kerning),
            '-fill', fill, '-gravity', 'center',
            '-annotate', f'+{x}+{y}', text]

STATES = ['WASHINGTON', 'MISSISSIPPI', 'ARKANSAS', 'IOWA', 'SOUTH CAROLINA',
          'TENNESSEE', 'GEORGIA']

# b033 — seven states ban tipping, 1909-1915
cmd = base()
txt(cmd, '1909 - 1915', 64, VERMILION, -400)
for i, s in enumerate(STATES):
    txt(cmd, s, 88, INK, -270 + i * 110)
txt(cmd, 'TIPPING PROHIBITED BY LAW', 54, MUSTARD, 470, kerning=10)
cmd += [str(OUT / 'b033-final.png')]
subprocess.run(cmd, check=True)

# b043 — every ban repealed by 1926: same list, struck through
cmd = base()
txt(cmd, 'BY 1926', 64, VERMILION, -400)
for i, s in enumerate(STATES):
    y = -270 + i * 110
    txt(cmd, s, 88, '#9AA5AD', y)
for i in range(len(STATES)):
    y = H // 2 - 270 + i * 110
    cmd += ['-stroke', VERMILION, '-strokewidth', '7',
            '-draw', f'line {W//2-340},{y} {W//2+340},{y}', '-stroke', 'none']
txt(cmd, 'ALL REPEALED', 54, MUSTARD, 470, kerning=10)
cmd += [str(OUT / 'b043-final.png')]
subprocess.run(cmd, check=True)

# b061 — the number
cmd = base()
txt(cmd, 'FEDERAL TIPPED MINIMUM WAGE', 54, MUSTARD, -330, kerning=10)
txt(cmd, '$2.13', 420, INK, 30, kerning=2)
txt(cmd, 'PER HOUR  ·  SET 1991', 54, VERMILION, 380, kerning=10)
cmd += [str(OUT / 'b061-final.png')]
subprocess.run(cmd, check=True)

# b063 — the real value halved: the same number, and its shadow at half height
cmd = base()
txt(cmd, 'THE NUMBER, 1991', 54, MUSTARD, -420, x=-420)
txt(cmd, 'WHAT IT BUYS TODAY', 54, MUSTARD, -420, x=430)
txt(cmd, '$2.13', 260, INK, 60, x=-420)
txt(cmd, '$2.13', 130, '#9AA5AD', 100, x=430)
txt(cmd, 'THE NUMBER STOOD STILL. THE VALUE ROUGHLY HALVED.', 50, VERMILION, 420, kerning=8)
cmd += [str(OUT / 'b063-final.png')]
subprocess.run(cmd, check=True)

print('4 data cards written')
