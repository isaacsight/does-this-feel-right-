#!/usr/bin/env python3
"""The four data frames, built deterministically — the model never draws data."""
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

# b022 — one man's mood becomes 12,000 prescriptions in one year
cmd = base()
txt(cmd, '1889: THE EVIDENCE', 54, MUSTARD, -370, kerning=10)
txt(cmd, '1 MAN', 200, INK, -160)
txt(cmd, 'BY YEAR END', 54, MUSTARD, 90, kerning=10)
txt(cmd, '12,000 DOCTORS', 160, VERMILION, 260)
cmd += [str(OUT / 'b022-final.png')]
subprocess.run(cmd, check=True)

# b063 — the price of the possibility
cmd = base()
txt(cmd, 'PAID FOR A MOLECULE, APRIL 2008', 54, MUSTARD, -330, kerning=10)
txt(cmd, '$720,000,000', 230, INK, 20, kerning=2)
txt(cmd, 'THERE WAS NO MEDICINE YET', 54, VERMILION, 360, kerning=10)
cmd += [str(OUT / 'b063-final.png')]
subprocess.run(cmd, check=True)

# b100 — the honest ledger
cmd = base()
txt(cmd, 'THE BOOTH, 1889 - TODAY', 54, MUSTARD, -350, kerning=10)
txt(cmd, 'VERIFIED EXTRA YEARS', 76, INK, -150, kerning=8)
txt(cmd, '0', 420, VERMILION, 160)
cmd += [str(OUT / 'b100-final.png')]
subprocess.run(cmd, check=True)

# b103 — the boring free thing
cmd = base()
txt(cmd, 'MOST ACTIVE vs LEAST ACTIVE', 54, MUSTARD, -350, kerning=10)
txt(cmd, '25-40%', 300, INK, -60, kerning=2)
txt(cmd, 'LOWER RISK OF DYING, ALL CAUSES COUNTED', 54, INK, 220, kerning=8)
txt(cmd, 'PRICE: A WALK', 54, VERMILION, 400, kerning=10)
cmd += [str(OUT / 'b103-final.png')]
subprocess.run(cmd, check=True)

print('4 data cards written')
