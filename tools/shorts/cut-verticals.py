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
from pathlib import Path

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


# ------------------------------------------------------------------ karaoke

_MEASURE_CACHE = {}


def measure(word, pt):
    """Width/height of one word at pt, measured — never estimated from chars."""
    key = (word, pt)
    if key not in _MEASURE_CACHE:
        out = subprocess.run(['magick', '-background', 'none', '-font', FONT,
                              '-pointsize', str(pt), f'label:{word}',
                              '-format', '%w %h', 'info:'],
                             capture_output=True, text=True, check=True).stdout
        _MEASURE_CACHE[key] = tuple(int(x) for x in out.split())
    return _MEASURE_CACHE[key]


def layout(tokens, pt):
    """Greedy wrap on MEASURED widths (the same law as card()); returns
    (lines, line_h) where lines are [[(idx, word, w), ...], ...], or None if a
    single word cannot fit the safe box at this size."""
    space = measure('n', pt)[0] // 2 + 2      # a space measures ~half an 'n'
    line_h = max(measure(w, pt)[1] for _, w in tokens) + 12
    lines, cur, cur_w = [], [], 0
    for idx, word in tokens:
        w, _ = measure(word, pt)
        if w > SAFE_W:
            return None
        add = w if not cur else cur_w + space + w
        if cur and add > SAFE_W:
            lines.append(cur); cur, cur_w = [], 0
            add = w
        cur.append((idx, word, w)); cur_w = add
    if cur:
        lines.append(cur)
    return (lines, line_h) if len(lines) * line_h <= CAPTION_MAX_H else None


def karaoke_cards(tokens, d, tag):
    """One card variant per word: word k in tomato, the rest in ivory.

    Why manual layout instead of `caption:`: highlighting one word needs its
    position, which auto-wrap does not expose, and this ImageMagick has no
    pango delegate for markup. So the wrap is done here on measured widths -
    which is also the only wrap that cannot overflow the box - and each
    variant is composed from per-word tiles. Tiles are rendered once per
    colour and reused across variants: a 6-word card costs 12 label renders
    and 6 composites, not 36 renders.
    """
    pt = next((p for p in range(CAPTION_PT, CAPTION_MIN_PT - 1, -6)
               if layout(tokens, p)), CAPTION_MIN_PT)
    lines, line_h = layout(tokens, pt) or layout(tokens, CAPTION_MIN_PT)
    space = measure('n', pt)[0] // 2 + 2
    block_h = len(lines) * line_h
    top = CANVAS_H - CAPTION_UP - block_h

    tiles = {}
    for li, line in enumerate(lines):
        for idx, word, w in line:
            for colour, fill in (('ink', INK), ('hot', TOMATO)):
                p = f'{d}/t-{tag}-{idx}-{colour}.png'
                subprocess.run(['magick', '-background', 'none', '-fill', fill,
                                '-font', FONT, '-pointsize', str(pt),
                                f'label:{word}', p], check=True)
                tiles[(idx, colour)] = p

    variants = []
    for k, _ in tokens:
        cmd = ['magick', '-size', f'{CANVAS_W}x{CANVAS_H}', 'xc:none']
        for li, line in enumerate(lines):
            x = (CANVAS_W // 2) + SAFE_DX - (sum(w for _, _, w in line)
                 + space * (len(line) - 1)) // 2
            y = top + li * line_h
            for idx, word, w in line:
                cmd += [tiles[(idx, 'hot' if idx == k else 'ink')],
                        '-geometry', f'+{x}+{y}', '-composite']
                x += w + space
        p = f'{d}/k-{tag}-{k}.png'
        subprocess.run(cmd + [p], check=True)
        variants.append((k, p))
    return variants


def align_words(words, wi, text):
    """Advance a word-list cursor through one card's text; returns the card's
    word objects or None if the card cannot be aligned (then it renders
    static). segments-from-words.py built the cards FROM this word list, so
    alignment is normally exact and sequential."""
    norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    toks = [t for t in text.split() if norm(t)]
    j = wi
    while j < len(words) and norm(words[j]['w']) != norm(toks[0]):
        j += 1
    if j >= len(words):
        return None, wi
    got = words[j:j + len(toks)]
    if len(got) != len(toks) or any(norm(a['w']) != norm(b) for a, b in zip(got, toks)):
        return None, wi
    return got, j + len(toks)


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

    # Karaoke: word-by-word highlight from the film's REAL word timings.
    # Opt-in per config ("karaoke": true); needs audio/words.json, which every
    # film has - recorded via /with-timestamps or retrofitted by
    # align-existing.mjs (PLAYBOOK 10.24).
    karaoke = bool(cfg.get('karaoke'))
    words = None
    if karaoke:
        wpath = rel(cfg.get('words', os.path.join(base, 'audio', 'words.json')))
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from words_io import load_words   # one reader, three shapes in this repo
    words = load_words(Path(wpath).parent.parent)

    for sh in cfg['shorts']:
        name, a, b = sh['name'], sh['from'], sh['to']
        t0, t1 = a / fps, b / fps
        dur = t1 - t0
        sub = [(s, e, t) for s, e, t in SEG if e > a and s < b]

        d = f'/tmp/cards-{name}'
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        kicker_plate(sh['kicker'], f'{d}/kick.png')

        shrunk, static_fallbacks = [], 0
        overlays = []                # (path, start, end) in clip time
        wi = 0
        for i, (s, e, t) in enumerate(sub):
            st = max(0, s / fps - t0); en = min(dur, e / fps - t0)
            got = None
            if karaoke:
                got, wi = align_words(words, wi, t)
            if got:
                toks = [x for x in enumerate(t.split())]
                variants = karaoke_cards(toks, d, f'{i:03d}')
                # Word k holds its highlight until word k+1 STARTS - the eye
                # reads a gap between words as a dropped highlight, so the card
                # never shows all-ivory mid-line. First variant starts with the
                # card, not with its word, for the same reason.
                for k, path in variants:
                    ws = st if k == 0 else max(st, got[k]['start'] - t0)
                    we = en if k == len(variants) - 1 else max(st, got[k + 1]['start'] - t0)
                    if we > ws:
                        overlays.append((path, ws, we))
            else:
                if karaoke:
                    static_fallbacks += 1
                p = f'{d}/{i:03d}.png'
                pt, w, h = card(t, p)
                if pt != CAPTION_PT:
                    shrunk.append((pt, t))
                overlays.append((p, st, en))

        ins = ['-i', master, '-i', f'{d}/kick.png']
        for p, _, _ in overlays:
            ins += ['-i', p]

        fc = [f"[0:v]scale={CANVAS_W}:-2,pad={CANVAS_W}:{CANVAS_H}:0:{picture_y}:color={LETTERBOX}[bg]",
              "[bg][1:v]overlay=0:0[v0]"]
        for i, (p, st, en) in enumerate(overlays):
            fc.append(f"[v{i}][{i+2}:v]overlay=0:0:"
                      f"enable='between(t,{st:.3f},{en:.3f})'[v{i+1}]")

        out = f'{outdir}/{name}.mp4'
        r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t0), '-to', str(t1),
                            *ins, '-filter_complex', ";".join(fc),
                            '-map', f'[v{len(overlays)}]', '-map', '0:a',
                            '-c:v', 'libx264', '-crf', '19', '-preset', 'medium',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                            '-r', '30', '-t', str(dur), out],
                           capture_output=True, text=True)
        mode = f"karaoke, {len(overlays)} overlays" if karaoke else f"{len(sub)} cards"
        print(f"{name}  {dur:.1f}s  {mode}  "
              f"{'OK' if r.returncode == 0 else r.stderr[-400:]}")
        if static_fallbacks:
            print(f"    {static_fallbacks} card(s) could not align to words.json — rendered static")
        for pt, t in shrunk:
            print(f"    shrunk to {pt}pt: {t}")
        open(f'{outdir}/{name}.srt', 'w').write(
            srt(sub, fps, offset=t0, duration=dur))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
