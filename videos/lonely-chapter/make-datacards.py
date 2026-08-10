#!/usr/bin/env python3
"""The five data frames, built deterministically — the model never draws data.

Same card grammar as the tipping episode: the world's cream ground, one
condensed mid-century face, one fact per card, nothing invented. Every number
is a CLAIMS.md row.
"""
import subprocess
from pathlib import Path

FILM = Path(__file__).resolve().parent
OUT = FILM / 'public' / 'images' / 'frames'
OUT.mkdir(parents=True, exist_ok=True)

FONT = '/System/Library/Fonts/Avenir Next Condensed.ttc'
CREAM = '#F7EFDC'
INK = '#24425C'
VERMILION = '#C6431F'
MUSTARD = '#C99A2E'
GREY = '#9AA5AD'
W, H = 1920, 1080

def base():
    return ['magick', '-size', f'{W}x{H}', f'xc:{CREAM}',
            '-attenuate', '0.18', '+noise', 'Gaussian', '-colorspace', 'sRGB']

def txt(cmd, text, pt, fill, y, kerning=6, x=0):
    cmd += ['-font', FONT, '-pointsize', str(pt), '-kerning', str(kerning),
            '-fill', fill, '-gravity', 'center',
            '-annotate', f'+{x}+{y}', text]

# b024 — men with NO close friends, 1990 -> 2021
cmd = base()
txt(cmd, 'AMERICAN MEN WITH NO CLOSE FRIENDS', 54, MUSTARD, -330, kerning=10)
txt(cmd, '3%', 300, GREY, 30, x=-420)
txt(cmd, '15%', 300, VERMILION, 30, x=380)
txt(cmd, '1990', 54, INK, 330, x=-420, kerning=10)
txt(cmd, '2021', 54, INK, 330, x=380, kerning=10)
cmd += [str(OUT / 'b024-final.png')]
subprocess.run(cmd, check=True)

# b025 — men with ten or more close friends
cmd = base()
txt(cmd, 'MEN WITH TEN OR MORE CLOSE FRIENDS', 54, MUSTARD, -330, kerning=10)
txt(cmd, '40%', 300, INK, 30, x=-420)
txt(cmd, '15%', 300, GREY, 30, x=380)
txt(cmd, '1990', 54, INK, 330, x=-420, kerning=10)
txt(cmd, '2021', 54, INK, 330, x=380, kerning=10)
cmd += [str(OUT / 'b025-final.png')]
subprocess.run(cmd, check=True)

# b069 — bowling up ten percent
cmd = base()
txt(cmd, '1980 - 1993', 54, MUSTARD, -360, kerning=10)
txt(cmd, 'BOWLING', 110, INK, -180, kerning=8)
txt(cmd, '+10%', 340, INK, 120)
cmd += [str(OUT / 'b069-final.png')]
subprocess.run(cmd, check=True)

# b070 — league bowling down forty
cmd = base()
txt(cmd, 'THE SAME YEARS', 54, MUSTARD, -360, kerning=10)
txt(cmd, 'LEAGUE BOWLING', 110, INK, -180, kerning=8)
txt(cmd, '-40%', 340, VERMILION, 120)
cmd += [str(OUT / 'b070-final.png')]
subprocess.run(cmd, check=True)

# b090 — the posted price in hours
cmd = base()
txt(cmd, 'THE POSTED PRICE OF A FRIEND, IN HOURS', 54, MUSTARD, -370, kerning=10)
txt(cmd, '50', 230, GREY, -90, x=-520)
txt(cmd, '90', 230, INK, -90, x=0)
txt(cmd, '200+', 230, VERMILION, -90, x=520)
txt(cmd, 'CASUAL', 46, INK, 130, x=-520, kerning=10)
txt(cmd, 'REAL', 46, INK, 130, x=0, kerning=10)
txt(cmd, 'CLOSE', 46, INK, 130, x=520, kerning=10)
txt(cmd, 'THE HOURS WITH NO AGENDA COUNT MOST', 50, VERMILION, 400, kerning=8)
cmd += [str(OUT / 'b090-final.png')]
subprocess.run(cmd, check=True)

print('5 data cards written')
