#!/usr/bin/env python3
"""Build a kernel.chat episode thumbnail to the LOCKED series template.

WHY THIS EXISTS. Five episodes have shipped with five different thumbnail
treatments: two with no overlay at all, one with white text along the bottom
over a dark crowd, one with ink-and-tomato text on the left over cream. Viewed
as a channel grid — which is how a subscriber actually meets the catalogue —
they do not read as one show. A recurring world makes a series; a recurring
FRAME makes a series legible at 120 pixels wide in a sidebar.

THE TEMPLATE, and the reasoning behind each number:

  1280x720, always. YouTube's own spec.

  A CREAM PANEL on the left, 46% of the width. This is the load-bearing
  decision. Overlaying type directly on the picture means legibility depends
  on whatever the frame happens to contain, which is why the goliath thumbnail
  needed white text and the queue one needed black — the template stopped
  being a template. A panel makes contrast a constant, and the panel colour is
  the house cream that half these frames already sit on, so it reads as part
  of the picture rather than as a sticker.

  TWO LINES MAX, Avenir Next Condensed Heavy, all caps. Line one INK, line two
  TOMATO. The two-tone is the series signature — it is the only thing a viewer
  needs to recognise across a grid — and putting the payload on line two means
  the eye lands on the number or the noun, not on the setup.

  AUTO-FIT, never a fixed point size. Type is measured against the panel and
  stepped down until it fits, because a long line silently overflowing is how
  you get a thumbnail that works in the editor and not in the sidebar.

  A TOMATO BAR bottom-left, 8px. Small, constant, and the cheapest possible
  series mark — no logo, no wordmark, nothing that eats space.

  CHECKED AT 320px. The tool writes a 320px proof next to the output because
  that is roughly a sidebar impression, and a thumbnail that fails there fails
  everywhere that matters.

Usage:
  python3 tools/video/thumbnail.py <frame.png> <out.png> "LINE ONE" "LINE TWO"
  ... [--panel left|right] [--no-proof]
"""
import subprocess
import sys
from pathlib import Path

W, H = 1280, 720
PANEL_FRAC = 0.46
MARGIN = 46
GUTTER = 26
BAR_H = 8
INK = '#1F1E1D'
TOMATO = '#E24E1B'
CREAM = '#FAF9F6'
FONT = '/System/Library/Fonts/Avenir Next Condensed.ttc'
PT_MAX, PT_MIN, PT_STEP = 148, 62, 4


def text_width(s, pt):
    """Measured, not estimated. ImageMagick reports the real advance width."""
    out = subprocess.run(
        ['magick', '-font', FONT, '-pointsize', str(pt), '-kerning', '2',
         f'label:{s}', '-format', '%w', 'info:'],
        capture_output=True, text=True, check=True)
    return int(out.stdout.strip())


def fit(lines, box_w):
    pt = PT_MAX
    while pt > PT_MIN and max(text_width(l, pt) for l in lines) > box_w:
        pt -= PT_STEP
    return pt


def main():
    argv = sys.argv[1:]
    side = 'left'
    if '--panel' in argv:
        i = argv.index('--panel')
        # consume BOTH the flag and its value, or the value falls through into
        # the text lines and gets rendered as a caption reading "RIGHT"
        side = argv[i + 1] if i + 1 < len(argv) else 'left'
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith('--')]
    if len(args) < 3:
        print(__doc__)
        sys.exit(1)
    frame, out, *lines = args
    lines = [l.upper() for l in lines[:2]]
    if side not in ('left', 'right'):
        side = 'left'

    panel_w = int(W * PANEL_FRAC)
    box_w = panel_w - MARGIN * 2
    pt = fit(lines, box_w)

    # The subject is scaled to fill and then anchored AWAY from the panel, so
    # the face never lands underneath the type.
    anchor = 'east' if side == 'left' else 'west'
    px = 0 if side == 'left' else W - panel_w

    cmd = ['magick', frame, '-resize', f'{W}x{H}^', '-gravity', anchor,
           '-extent', f'{W}x{H}',
           '-fill', CREAM, '-draw', f'rectangle {px},0 {px + panel_w},{H}']

    y = -(pt // 2) - 6 if len(lines) > 1 else 0
    grav = 'west' if side == 'left' else 'east'
    for i, line in enumerate(lines):
        cmd += ['-font', FONT, '-pointsize', str(pt), '-kerning', '2',
                '-fill', TOMATO if i else INK, '-gravity', grav,
                '-annotate', f'{MARGIN if side == "left" else MARGIN:+d}{y:+d}', line]
        y += pt + GUTTER - 10

    cmd += ['-fill', TOMATO, '-draw',
            f'rectangle {px + MARGIN},{H - MARGIN} {px + MARGIN + 96},{H - MARGIN + BAR_H}',
            out]
    subprocess.run(cmd, check=True)

    if '--no-proof' not in sys.argv:
        proof = Path(out).with_suffix('.320.png')
        subprocess.run(['magick', out, '-resize', '320x', str(proof)], check=True)
        print(f'{out}  ({pt}pt)  proof: {proof}')
    else:
        print(f'{out}  ({pt}pt)')


if __name__ == '__main__':
    main()
