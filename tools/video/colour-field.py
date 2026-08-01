#!/usr/bin/env python3
"""Apply a per-act colour field to generated frames.

Why this is an assembly step and not a prompt: the 2026-07-31 pilot asked for
five paper colours by hex and got cream back four times out of six, because the
layout reference is a cream frame and a reference image is a prior on
everything it contains - its background colour included. Instruction does not
beat reference. Tinting here is deterministic, free, and cannot drift across a
hundred frames.

METHOD. Not multiply, and not a flat colour-replace of the paper.

A fuzzy colour-replace would leave the character's cream shirt, shoes and face
at the old paper colour while the wall behind them moved - that reads as a
compositing error, not a change of light.

Multiply was tried first and is worse than it looks. It is a VALUE operation,
result = a*b/255, so it can only darken and can never move a pixel away from
the source hue. Dragging a warm cream toward a cool slate produced muddy brown
at every strength above 40.

What this does instead is a SIGNED PER-CHANNEL OFFSET. It samples the frame's
own corner to find the paper it actually has, computes the delta to the target
paper, and applies that delta to the whole image scaled by strength. At
strength 100 the paper lands exactly on target by construction, and everything
else - ink, jacket, faces - shifts by the same amount, which is what a real
change of room light does to a scene.

STRENGTH is the one dial. 0 is untouched, 100 puts the paper exactly on target.

Usage:
  python3 colour-field.py <frames-dir> <out-dir> <meta.json> [--strength 40]
  python3 colour-field.py --strip <frame.png> <hex> <out.png>   # test strip
"""
import json
import re
import subprocess
import sys
from pathlib import Path

STRENGTH = 55           # percent; chosen off the test strip


def corner_paper(src):
    """The frame's own paper, read from a corner. Generated frames land a few
    points off the nominal cream and vary between batches; measuring beats
    assuming."""
    out = subprocess.run(['magick', str(src), '-format', '%[pixel:p{4,4}]', 'info:'],
                         capture_output=True, text=True).stdout
    m = re.search(r'\((\d+),\s*(\d+),\s*(\d+)', out)
    return tuple(int(g) for g in m.groups()) if m else (250, 234, 211)


def tint(src, dest, hex_colour, strength):
    src_paper = corner_paper(src)
    tgt = tuple(int(hex_colour.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    delta = [(t - s) * strength / 100.0 for t, s in zip(tgt, src_paper)]

    if strength <= 0 or all(abs(d) < 0.5 for d in delta):
        subprocess.run(['magick', str(src), str(dest)], check=True)
        return

    cmd = ['magick', str(src)]
    for ch, d in zip(('R', 'G', 'B'), delta):
        pct = abs(d) / 255.0 * 100.0
        cmd += ['-channel', ch,
                '-evaluate', 'subtract' if d < 0 else 'add', f'{pct:.3f}%']
    cmd += ['+channel', str(dest)]
    subprocess.run(cmd, check=True)


def strip(src, hex_colour, dest):
    """Render one frame at five strengths side by side so the value is chosen
    by looking rather than by guessing."""
    parts = []
    for s in (0, 25, 40, 55, 70):
        p = f'/tmp/.cf-{s}.png'
        tint(src, p, hex_colour, s)
        subprocess.run(['magick', p, '-resize', '480x', p], check=True)
        parts.append(p)
    subprocess.run(['magick', *parts, '+append', dest], check=True)
    print(f'{dest}  (0 / 25 / 40 / 55 / 70)')


if __name__ == '__main__':
    if '--strip' in sys.argv:
        i = sys.argv.index('--strip')
        strip(sys.argv[i+1], sys.argv[i+2], sys.argv[i+3])
        sys.exit(0)

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 3:
        sys.exit(__doc__)
    src_dir, out_dir, meta_path = Path(args[0]), Path(args[1]), args[2]
    if '--strength' in sys.argv:
        STRENGTH = int(sys.argv[sys.argv.index('--strength') + 1])

    paper = {f['id']: f['paper'] for f in json.load(open(meta_path))}
    out_dir.mkdir(parents=True, exist_ok=True)

    done = 0
    for f in sorted(src_dir.glob('*-final.png')):
        fid = f.name.replace('-final.png', '')
        if fid not in paper:
            print(f'  skip {fid} - not in meta')
            continue
        tint(f, out_dir / f.name, paper[fid], STRENGTH)
        done += 1
    print(f'{done} frames tinted at strength {STRENGTH} -> {out_dir}')
