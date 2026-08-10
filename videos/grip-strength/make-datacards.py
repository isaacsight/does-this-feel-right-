#!/usr/bin/env python3
"""Deterministic data cards — type composited in post, motion built locally.

The no-text law bans GENERATED lettering; this is the sanctioned path: every
numeral is set in ImageMagick over the gated still (pristine copies kept), and
the two long-hold cards (b04 at ~15s, b20 at ~12s) become deterministic CLIPS
— progressive composites concatenated by ffmpeg — dropped into public/clips/
where the assembly seam picks them up exactly as it would a generated clip.
Data motion through the same door, zero generation, zero cost.

Numbers shown are the verified claims and nothing else:
  b04: 142,861 PEOPLE / 17 COUNTRIES / +16% risk per 5 kg lost   (PURE)
  b09: 645,000 CO-AUTHORS                                        (PURE+Biobank)
  b20: 1985 121 LB / 2016 101 LB                                 (Fain 2016)
"""
import subprocess, shutil, pathlib

FILM = pathlib.Path(__file__).resolve().parent
FR = FILM / 'public/images/frames'
CL = FILM / 'public/clips'
PR = FILM / 'production/pristine'
PR.mkdir(exist_ok=True)
FONT = '/System/Library/Fonts/Avenir Next Condensed.ttc'
BONE, ORANGE = '#EDE6D6', '#E8622C'
FPS = 30

def annotate(src, out, texts):
    cmd = ['magick', str(src)]
    for t, pt, colour, grav, geom in texts:
        cmd += ['-font', FONT, '-pointsize', str(pt), '-kerning', '4',
                '-fill', colour, '-gravity', grav, '-annotate', geom, t]
    cmd += [str(out)]
    subprocess.run(cmd, check=True)

def still_to_clip(frames_with_secs, out):
    """Concatenate held stills into one mp4 — deterministic 'motion'."""
    tmp = FILM / 'production' / '.dc'
    shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir()
    parts = []
    for i, (png, secs) in enumerate(frames_with_secs):
        p = tmp / f'{i}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', f'{secs:.2f}',
                        '-i', str(png), '-vf', f'scale=1920:1080,fps={FPS},setsar=1',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                        '-pix_fmt', 'yuv420p', str(p)], check=True)
        parts.append(p)
    lst = tmp / 'list.txt'
    lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
                    '-i', str(lst), '-c', 'copy', str(out)], check=True)
    shutil.rmtree(tmp)

# ---- b04: the PURE numbers step in over the ring row (three states) --------
src = FR / 'b04-final.png'
if not (PR / 'b04-final.png').exists(): shutil.copy(src, PR / 'b04-final.png')
s1 = FILM / 'production/.b04-1.png'; s2 = FILM / 'production/.b04-2.png'; s3 = FILM / 'production/.b04-3.png'
annotate(PR / 'b04-final.png', s1, [('142,861 PEOPLE', 96, BONE, 'north', '+0+180')])
annotate(s1, s2, [('17 COUNTRIES', 72, BONE, 'south', '+0+260')])
annotate(s2, s3, [('+16% RISK PER 5 KG LOST', 84, ORANGE, 'south', '+0+150')])
still_to_clip([(s1, 5.4), (s2, 4.6), (s3, 6.0)], CL / 'b04.mp4')
print('b04.mp4  (3 states, 16s)')

# ---- b20: the two eras label in, then the deficit lands --------------------
src = FR / 'b20-final.png'
if not (PR / 'b20-final.png').exists(): shutil.copy(src, PR / 'b20-final.png')
s1 = FILM / 'production/.b20-1.png'; s2 = FILM / 'production/.b20-2.png'
annotate(PR / 'b20-final.png', s1, [
    ('1985', 76, BONE, 'south', '-240+120'), ('2016', 76, BONE, 'south', '+240+120'),
    ('121 LB', 68, BONE, 'north', '-240+150')])
annotate(s1, s2, [('101 LB', 68, BONE, 'north', '+240+240'),
                  ('-20 LB', 84, ORANGE, 'north', '+0+60')])
still_to_clip([(s1, 5.5), (s2, 6.5)], CL / 'b20.mp4')
print('b20.mp4  (2 states, 12s)')

# ---- b09: one static composite (5s hold) -----------------------------------
src = FR / 'b09-final.png'
if not (PR / 'b09-final.png').exists(): shutil.copy(src, PR / 'b09-final.png')
annotate(PR / 'b09-final.png', src, [('645,000 CO-AUTHORS', 64, '#3A3F49', 'north', '+0+165')])
print('b09 composited in place (pristine kept)')
