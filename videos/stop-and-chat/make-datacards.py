#!/usr/bin/env python3
"""The three data frames, built deterministically — the model never draws data.

Frame ids are wired to the board's data rows; re-check against board.py
before running (data rows are excluded from prompts.json by the board).
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
W, H = 1920, 1080

# ids of the board's data rows (board.json, verified)
CARD_PREDICTION = 'b021'
CARD_ENDINGS = 'b051'
CARD_RECOGNIZED = 'b066'
CARD_FACES = 'b067'

def base():
    return ['magick', '-size', f'{W}x{H}', f'xc:{CREAM}',
            '-attenuate', '0.18', '+noise', 'Gaussian', '-colorspace', 'sRGB']

def txt(cmd, text, pt, fill, y, kerning=6, x=0):
    cmd += ['-font', FONT, '-pointsize', str(pt), '-kerning', str(kerning),
            '-fill', fill, '-gravity', 'center',
            '-annotate', f'+{x}+{y}', text]

# card 1 — the prediction vs the measurement (Chicago, 2014)
cmd = base()
txt(cmd, 'CHICAGO, 2014 - 9 EXPERIMENTS, 800+ COMMUTERS', 54, MUSTARD, -370, kerning=10)
txt(cmd, 'PREDICTED BEST: SOLITUDE', 90, INK, -140, kerning=8)
txt(cmd, 'MEASURED BEST: TALKING', 110, VERMILION, 80, kerning=8)
txt(cmd, 'THE PEOPLE SPOKEN TO CAME OUT POSITIVE TOO', 54, INK, 330, kerning=10)
cmd += [str(OUT / f'{CARD_PREDICTION}-final.png')]
subprocess.run(cmd, check=True)

# card 2 — the broken exit (932 conversations, 2021)
cmd = base()
txt(cmd, '932 CONVERSATIONS, MEASURED 2021', 54, MUSTARD, -390, kerning=10)
txt(cmd, 'ENDED WHEN BOTH WANTED', 62, INK, -240, kerning=8)
txt(cmd, 'UNDER 2%', 250, VERMILION, -60)
txt(cmd, 'RAN TOO LONG: 48%', 76, INK, 220, kerning=8)
txt(cmd, 'ENDED TOO SOON: 34%', 76, INK, 350, kerning=8)
cmd += [str(OUT / f'{CARD_ENDINGS}-final.png')]
subprocess.run(cmd, check=True)

# card 3 — the photograph experiment (one platform, 1972)
cmd = base()
txt(cmd, 'ONE COMMUTER PLATFORM, 1972', 54, MUSTARD, -390, kerning=10)
txt(cmd, 'SHOWN PHOTOS OF THEIR OWN PLATFORM', 62, INK, -240, kerning=8)
txt(cmd, '89%', 340, VERMILION, -40)
txt(cmd, 'RECOGNIZED AT LEAST ONE FACE', 76, INK, 300, kerning=8)
cmd += [str(OUT / f'{CARD_RECOGNIZED}-final.png')]
subprocess.run(cmd, check=True)

# card 4 — the familiar strangers ratio
cmd = base()
txt(cmd, 'THE AVERAGE COMMUTER, SAME PLATFORM', 54, MUSTARD, -390, kerning=10)
txt(cmd, 'FACES KNOWN, NEVER SPOKEN TO', 62, INK, -240, kerning=8)
txt(cmd, '4.0', 340, VERMILION, -40)
txt(cmd, 'SPOKEN TO: 1.5', 90, INK, 300, kerning=8)
cmd += [str(OUT / f'{CARD_FACES}-final.png')]
subprocess.run(cmd, check=True)

print('4 data cards written')
