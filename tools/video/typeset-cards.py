#!/usr/bin/env python3
"""Composite typography onto finished frames — SHARED tool.

WHY THIS EXISTS AND WHY IT RUNS LAST. Generated lettering is forbidden in every
world: the model cannot spell, and a hex code once came back drawn into a frame
as a literal string. The frame gate's glyph check exists to catch exactly that.
So our OWN type has to arrive after the gate has already passed, or the check
stops meaning anything about generated text.

    ORDER:  generate -> gate -> typeset -> assemble

Pristine frames are copied to production/pristine/ before anything is drawn, so
the gate can always be re-run against untouched art. Re-running this tool is
idempotent: it always composites from pristine, never from an already-typeset
frame, so type never stacks.

RENDERING IS IMAGEMAGICK, NOT FFMPEG. This machine's ffmpeg is built without
libfreetype and without libass, so drawtext/subtitles/ass are all unavailable
(CAPTION-SPEC Finding 6). Same reason tools/shorts/cut-verticals.py renders
caption cards in ImageMagick and composites them.

Config lives in the film at production/cards.json:

    {
      "font": "/System/Library/Fonts/Supplemental/Futura.ttc",
      "title":  {"frame": "b01", "lines": ["NOBODY ROOTS", "FOR GOLIATH"],
                 "ink": "#2b2118", "size": 132, "tracking": 8},
      "sources": [
        {"frame": "b23", "lines": ["Vandello, Goldschmied & Richards",
                                   "Pers. Soc. Psychol. Bull. 33(12), 2007"]}
      ],
      "scoreboard": [ {"frame": "b42", "value": "1"}, ... ]
    }

Usage:  python3 tools/video/typeset-cards.py <film-dir> [--revert]
"""
import json, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# Source cards sit in the lower-left, small and quiet. They are a citation, not
# a caption: they must be readable if you look and ignorable if you do not.
SOURCE_SIZE, SOURCE_PAD = 34, 56
SCORE_SIZE = 150


def run(*a):
    p = subprocess.run(a, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr.strip()[-400:], file=sys.stderr)
        sys.exit(2)


def main(film: Path, revert: bool):
    cfg_path = film / "production" / "cards.json"
    if not cfg_path.exists():
        print(f"no {cfg_path}", file=sys.stderr); sys.exit(2)
    cfg = json.loads(cfg_path.read_text())
    frames = film / "public" / "images" / "frames"
    pristine = film / "production" / "pristine"
    pristine.mkdir(parents=True, exist_ok=True)
    font = cfg.get("font", "/System/Library/Fonts/Supplemental/Futura.ttc")

    def stash(fid):
        """Pristine is the SOURCE of every composite, so type never stacks."""
        src, keep = frames / f"{fid}-final.png", pristine / f"{fid}-final.png"
        if not src.exists():
            print(f"  {fid}: no frame, skipped"); return None
        if not keep.exists():
            shutil.copy(src, keep)
        return keep

    if revert:
        n = 0
        for p in pristine.glob("*-final.png"):
            shutil.copy(p, frames / p.name); n += 1
        print(f"reverted {n} frames to pristine"); return

    done = 0

    t = cfg.get("title")
    if t and (keep := stash(t["frame"])):
        # The title sits on a flat plate of the world's own ground colour so it
        # reads as a CARD, not as text lying on a scene.
        args = ["magick", str(keep), "-fill", t.get("plate", "#e8dcc8"),
                "-colorize", "88", "-font", font, "-fill", t.get("ink", "#2b2118"),
                "-pointsize", str(t.get("size", 132)), "-gravity", "center",
                "-kerning", str(t.get("tracking", 8))]
        n = len(t["lines"])
        for i, line in enumerate(t["lines"]):
            dy = int((i - (n - 1) / 2) * t.get("size", 132) * 1.18)
            args += ["-annotate", f"+0{dy:+d}", line]
        run(*args, str(frames / f"{t['frame']}-final.png")); done += 1

    for s in cfg.get("sources", []):
        keep = stash(s["frame"])
        if not keep:
            continue
        # A citation must be READABLE or it is decoration. The first version set
        # 34pt ivory with a 2px shadow over a busy painted crowd and vanished.
        # Type now sits on a solid bar sized to the text, which is also how the
        # world's own signage would carry a caption.
        n = len(s["lines"])
        pt = s.get("size", 40)
        lh = int(pt * 1.45)
        bar_h = lh * n + int(pt * 0.9)
        bar_w = int(max(len(l) for l in s["lines"]) * pt * 0.56) + int(pt * 1.6)
        args = ["magick", str(keep),
                "-fill", s.get("plate", "#2b2118dd"), "-draw",
                f"rectangle {SOURCE_PAD},{{H}}-{SOURCE_PAD + bar_w},{{H2}}"]
        # ImageMagick has no arithmetic in -draw, so compute against the frame.
        from PIL import Image as _I
        H = _I.open(keep).size[1]
        y1, y0 = H - SOURCE_PAD, H - SOURCE_PAD - bar_h
        args[args.index("-draw") + 1] = \
            f"rectangle {SOURCE_PAD},{y0} {SOURCE_PAD + bar_w},{y1}"
        args += ["-font", font, "-pointsize", str(pt), "-kerning", "1",
                 "-fill", s.get("ink", "#fdf6e8"), "-gravity", "northwest"]
        for i, line in enumerate(s["lines"]):
            args += ["-annotate", f"+{SOURCE_PAD + int(pt*0.8)}"
                                  f"+{y0 + int(pt*0.45) + i*lh}", line]
        run(*args, str(frames / f"{s['frame']}-final.png")); done += 1

    for sc in cfg.get("scoreboard", []):
        keep = stash(sc["frame"])
        if not keep:
            continue
        g = sc.get("gravity", "north")
        run("magick", str(keep), "-font", font, "-pointsize",
            str(sc.get("size", SCORE_SIZE)), "-gravity", g, "-kerning", "6",
            "-fill", sc.get("ink", "#2b2118"),
            "-annotate", sc.get("offset", "+0+90"), sc["value"],
            str(frames / f"{sc['frame']}-final.png")); done += 1

    print(f"typeset {done} frame(s); pristine kept in production/pristine/")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print(__doc__); sys.exit(2)
    main((REPO / sys.argv[1]).resolve(), "--revert" in sys.argv)
