#!/usr/bin/env python3
"""The six data frames, built deterministically — the model never draws data.

Frame ids are the board's data rows (excluded from prompts.json at source):
  b019  the predicted number
  b021  the actual number
  b030  the worst case, beaten by reality
  b061  the opera house, 7M against 102M
  b069  the committee, 18-30 months against eight years
  b074b the iron law, nine of ten
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


def base():
    return ['magick', '-size', f'{W}x{H}', f'xc:{CREAM}',
            '-attenuate', '0.18', '+noise', 'Gaussian', '-colorspace', 'sRGB']


def txt(cmd, text, pt, fill, y, kerning=6, x=0):
    cmd += ['-font', FONT, '-pointsize', str(pt), '-kerning', str(kerning),
            '-fill', fill, '-gravity', 'center',
            '-annotate', f'+{x}+{y}', text]


def card(fid, rows):
    cmd = base()
    for args in rows:
        txt(cmd, *args)
    cmd += [str(OUT / f'{fid}-final.png')]
    subprocess.run(cmd, check=True)


# b019 — what they predicted
card('b019', [
    ('HONORS STUDENTS, 1994', 54, MUSTARD, -330, 10),
    ('THEY PREDICTED', 76, INK, -170, 8),
    ('33.9 DAYS', 250, INK, 40, 2),
    ('TO FINISH THE THESIS', 54, INK, 300, 10),
])

# b021 — what it took
card('b021', [
    ('THE SAME STUDENTS', 54, MUSTARD, -330, 10),
    ('IT ACTUALLY TOOK', 76, INK, -170, 8),
    ('55.5 DAYS', 250, VERMILION, 40, 2),
    ('THREE IN TEN FINISHED ON TIME', 54, INK, 300, 10),
])

# b030 — the worst case, beaten
card('b030', [
    ('ASKED FOR THEIR WORST CASE', 54, MUSTARD, -390, 10),
    ('IF EVERYTHING WENT AS BADLY AS IT POSSIBLY COULD', 48, INK, -280, 8),
    ('48.6 DAYS', 210, INK, -100, 2),
    ('REALITY', 62, VERMILION, 130, 8),
    ('55.5 DAYS', 210, VERMILION, 300, 2),
])

# b061 — the opera house
card('b061', [
    ('SYDNEY OPERA HOUSE', 54, MUSTARD, -390, 10),
    ('ESTIMATED 1957, DOORS OPEN JANUARY 1963', 48, INK, -290, 8),
    ('$7,000,000', 170, INK, -130, 2),
    ('OPENED OCTOBER 1973', 62, VERMILION, 90, 8),
    ('$102,000,000', 190, VERMILION, 280, 2),
])

# b069 — the committee
card('b069', [
    ('A CURRICULUM TEAM, 1976', 54, MUSTARD, -390, 10),
    ('THE ROOM ESTIMATED', 62, INK, -270, 8),
    ('18 TO 30 MONTHS', 150, INK, -120, 4),
    ('IT TOOK', 62, VERMILION, 90, 8),
    ('EIGHT YEARS', 190, VERMILION, 250, 4),
    ('THE BOOK WAS NEVER USED', 54, INK, 400, 10),
])

# b074b — the iron law
card('b074b', [
    ('LARGE PUBLIC WORKS, ~70 YEARS OF RECORDS', 54, MUSTARD, -390, 10),
    ('OVER BUDGET', 76, INK, -250, 8),
    ('9 OF 10', 260, VERMILION, -50, 4),
    ('CHANNEL TUNNEL: 80% OVER', 66, INK, 220, 8),
    ("DENVER'S AIRPORT: 200% OVER", 66, INK, 340, 8),
])

print('6 data cards written')
