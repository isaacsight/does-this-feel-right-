#!/usr/bin/env python3
"""Cut captioned 9:16 verticals out of a finished 16:9 master.

Why this exists instead of Palmier: this machine's ffmpeg is built without
libass AND without libfreetype, so `subtitles=`, `ass=` and `drawtext=` are all
unavailable (see docs/video/CAPTION-SPEC.md Finding 6). Caption cards are
rendered with ImageMagick and composited with `overlay ... enable=between()`.

Usage:  python3 tools/shorts/cut-verticals.py <config.json>

Config shape — see videos/polyvagal/shorts.json for a worked example:
  { "master": "...mp4", "segments": "...segments.json", "out": "dir",
    "shorts": [ {"name": "...", "from": 1588, "to": 2824, "kicker": "..."} ] }
`from`/`to` are frame numbers in the segments file's own fps.
"""
import json, os, re, shutil, subprocess, sys

FONT = "/System/Library/Fonts/Avenir Next Condensed.ttc"  # default face IS Condensed Heavy

# 1080x1920 canvas. Safe zones are the union across TikTok/Reels/Shorts:
# top 130, bottom 484, left 60, right 140. The right reserve is bigger than the
# left, so the usable box is NOT centred on the canvas — its centre is at x=500,
# 40px left of 540. Every horizontal placement below carries that -40.
CANVAS_W, CANVAS_H = 1080, 1920
SAFE_W = 880                # 1080 - 60 - 140
SAFE_DX = -40               # centre of the safe box vs centre of the canvas
PICTURE_Y = 380             # top of the letterboxed 16:9 image (608px tall)
# A 3:2 source is 720px tall at 1080 wide, not 608, and at PICTURE_Y=380 its
# foot lands at 1100 — under a three-line caption, whose top edge sits at 1060.
# Override with "pictureY" in the config when the master is not 16:9.
CAPTION_UP = 560            # caption block bottom edge, measured up from frame bottom
CAPTION_PT = 76             # ≈ Palmier fontSize 52, the locked look
CAPTION_MIN_PT = 54         # floor when a long line needs shrinking
CAPTION_MAX_H = 300         # ~3 lines; past this, step the size down
KICKER_PT = 38
INK = '#FAF9F6'
TOMATO = '#E24E1B'
LETTERBOX = '0x151312'


def timecode(sec):
    sec = max(0.0, sec)     # a card straddling the in-point goes negative, and
                            # Python's floor-division renders that "-1:59:59,967"
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')


def srt(segs, fps, offset=0.0, duration=None):
    """Cues clamped to the clip. `sub` deliberately keeps cards that straddle
    the in- and out-points so the burned-in caption is never missing at a cut;
    the sidecar must still start at 0 and stop at the end of the clip."""
    out = []
    for i, (a, b, t) in enumerate(segs, 1):
        start = max(0.0, a / fps - offset)
        end = b / fps - offset
        if duration is not None:
            end = min(end, duration)
        if end <= start:
            continue
        out.append(f"{i}\n{timecode(start)} --> {timecode(end)}\n{t}\n")
    return "\n".join(out)


def card(text, path):
    """Render one transparent caption card.

    Uses ImageMagick `caption:` with a fixed -size width, which wraps on
    MEASURED width and therefore cannot overflow the box. Counting characters
    cannot do this: a 21-char budget silently overflows on wide glyphs, and any
    rewrap-to-N-lines step reintroduces long lines. Shrink only if the wrapped
    block grows past three lines.
    """
    for pt in range(CAPTION_PT, CAPTION_MIN_PT - 1, -6):
        tmp = path + '.txt.png'
        subprocess.run(['magick', '-background', 'none', '-fill', INK,
                        '-font', FONT, '-pointsize', str(pt),
                        '-interline-spacing', '12', '-size', f'{SAFE_W}x',
                        '-gravity', 'center', f'caption:{text}', tmp], check=True)
        h = int(subprocess.run(['magick', 'identify', '-format', '%h', tmp],
                               capture_output=True, text=True, check=True).stdout)
        w = int(subprocess.run(['magick', 'identify', '-format', '%w', tmp],
                               capture_output=True, text=True, check=True).stdout)
        if h <= CAPTION_MAX_H and w <= SAFE_W:
            break
    subprocess.run(['magick', '-size', f'{CANVAS_W}x{CANVAS_H}', 'xc:none', tmp,
                    '-gravity', 'south', '-geometry', f'{SAFE_DX:+d}+{CAPTION_UP}',
                    '-composite', path], check=True)
    os.remove(tmp)
    return pt, w, h


def kicker_plate(text, path):
    subprocess.run(['magick', '-size', f'{CANVAS_W}x{CANVAS_H}', 'xc:none',
                    '-font', FONT, '-pointsize', str(KICKER_PT), '-fill', TOMATO,
                    '-kerning', '7', '-gravity', 'north',
                    '-annotate', f'{SAFE_DX:+d}+190', text, path], check=True)


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    seg_doc = json.load(open(rel(cfg['segments'])))
    fps = float(seg_doc.get('fps', 30))
    SEG = [tuple(x) for x in seg_doc['segments']]
    master = rel(cfg['master'])
    outdir = rel(cfg['out']); os.makedirs(outdir, exist_ok=True)
    picture_y = int(cfg.get('pictureY', PICTURE_Y))

    for sh in cfg['shorts']:
        name, a, b = sh['name'], sh['from'], sh['to']
        t0, t1 = a / fps, b / fps
        dur = t1 - t0
        sub = [(s, e, t) for s, e, t in SEG if e > a and s < b]

        d = f'/tmp/cards-{name}'
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        kicker_plate(sh['kicker'], f'{d}/kick.png')

        shrunk = []
        ins = ['-i', master, '-i', f'{d}/kick.png']
        for i, (s, e, t) in enumerate(sub):
            p = f'{d}/{i:03d}.png'
            pt, w, h = card(t, p)
            if pt != CAPTION_PT:
                shrunk.append((pt, t))
            ins += ['-i', p]

        fc = [f"[0:v]scale={CANVAS_W}:-2,pad={CANVAS_W}:{CANVAS_H}:0:{picture_y}:color={LETTERBOX}[bg]",
              "[bg][1:v]overlay=0:0[v0]"]
        for i, (s, e, t) in enumerate(sub):
            st = max(0, s / fps - t0); en = min(dur, e / fps - t0)
            fc.append(f"[v{i}][{i+2}:v]overlay=0:0:"
                      f"enable='between(t,{st:.3f},{en:.3f})'[v{i+1}]")

        out = f'{outdir}/{name}.mp4'
        r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t0), '-to', str(t1),
                            *ins, '-filter_complex', ";".join(fc),
                            '-map', f'[v{len(sub)}]', '-map', '0:a',
                            '-c:v', 'libx264', '-crf', '19', '-preset', 'medium',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                            '-r', '30', '-t', str(dur), out],
                           capture_output=True, text=True)
        print(f"{name}  {dur:.1f}s  {len(sub)} cards  "
              f"{'OK' if r.returncode == 0 else r.stderr[-400:]}")
        for pt, t in shrunk:
            print(f"    shrunk to {pt}pt: {t}")
        open(f'{outdir}/{name}.srt', 'w').write(
            srt(sub, fps, offset=t0, duration=dur))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
