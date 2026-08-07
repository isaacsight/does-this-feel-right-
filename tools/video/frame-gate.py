#!/usr/bin/env python3
"""Per-frame acceptance gate. Blocks a frame from being written, at $0.039 a retry,
instead of reporting it after the batch at 50 frames a rebuild.

The checks here are not invented. Every one corresponds to a specific frame that
reached a finished film or a paid gate, and every threshold is the one QC measured
when it caught that frame — see videos/cognitive-debt/QC-gate2.md, which states an
explicit "fixed looks like" criterion for each. This file is that criterion made
executable and moved upstream of the spend.

    edges        b33  black bars painted into the pixels, panel 1920x861
    vertical     b13 b21 b87  the forbidden margin rule, vcov 1.00
    ground       the warm drift the doubled world clause exists to prevent
    hue          b31  brown at 10.75% of frame, more than the red at 8.18%
    glyph        the hex code #D9E2DA that came back drawn as "D9EE13D"
    accent       b85  a red sleeve 43% larger than the red tread beside it

What this gate does NOT check, and must not be read as covering: whether the frame
is the picture the board asked for. b08 and b72 pass every check here and are still
unanimatable, because "the boarded composition is absent" is a judgment. That stays
with the QC chair. A green gate means the frame is inside the world, not that it is
the right frame.

Global assertions come from the film's WORLD.md so the world clause has one home and
two audiences: prose for the model, an ASSERTIONS block for this scanner. Per-frame
expectations are optional and come from gate.json next to prompts.json.

Usage:
    frame-gate.py <film-dir> --frame b08          one frame, exit 1 on fail
    frame-gate.py <film-dir> --all                sweep, table + exit 1 if any fail
    frame-gate.py <film-dir> --all --json         machine-readable, for the generator
    frame-gate.py <film-dir> --all --calibrate    stats only, never fails - for tuning
"""
import sys, os, json, re, subprocess
from pathlib import Path

# A missing dependency must exit 2 (gate broken), never 1 (frame failed). Left as a
# bare import this file dies with a traceback and exit 1, and a caller that reads 1 as
# "the frame is bad" will regenerate a perfectly good frame until it runs out of money.
try:
    import numpy as np
    from PIL import Image
    from scipy import ndimage
except ImportError as _e:
    sys.stderr.write(
        f"GATE CANNOT RUN: {_e}\n  interpreter: {sys.executable}\n"
        "  This is a gate fault, not a frame fault. Exiting 2 so no caller reads it\n"
        "  as a verdict on the picture.\n")
    sys.exit(2)

# ---------------------------------------------------------------- world defaults
# Overridden per film by the ASSERTIONS block in WORLD.md. These are the cognitive-debt
# ledger values as measured by QC across the 87 frames that passed the paper lock.
DEFAULTS = {
    # Every value below was calibrated against the 88 cognitive-debt frames, where QC
    # had already established ground truth by hand. A gate that fails good frames is
    # worse than no gate, so the tuning target was zero false positives on the frames
    # QC passed - not maximum sensitivity.
    "letterbox_max_rows": 4,      # b33 had 110 top / 109 bottom; every other frame 0
    "letterbox_luma": 0.10,
    "vertical_min_vcov": 0.95,    # b13 1.00, b87 1.00 | b19's red hood edge 0.76 (FP)
    "vertical_min_dev": 4.0,
    "vertical_max_width": 24,     # wider than this is an object, and the board's call
    "ground_hue": [55.0, 80.0],   # measured band 64.6-70.0, widened for headroom
    "ground_sat": [0.0, 12.0],    # measured 5.2-5.6
    "ground_val": [82.0, 98.0],   # measured 90.2-91.4
    "accent_hue": [0.0, 20.0],    # tomato red
    # 1.20 rejected the best frame in the exaggeration pilot: a crowd of hundreds of
    # figures pushes the cast's own cream skin to 1.65% of frame in the same h30-45
    # bucket that brown drift lands in. Only magnitude separates them (b31's brown was
    # 17.2%), so the threshold moves to 3.0 and marginal second accents go to QC's eye.
    # A false positive here costs three regenerations AND can lose an irreplaceable
    # frame; a false negative costs a note in a report.
    "hue_census_max": 3.00,
    "hue_census_min_sat": 25.0,
    # A brightness floor on what counts as chromatic. load_world DROPS any key
    # that is not already in DEFAULTS, silently — so a new assertion is inert
    # until it is declared here. Default 0.0 keeps every world calibrated before
    # 2026-08-07 behaving exactly as it did.
    "hue_census_min_val": 0.0,
    "glyph_min_conf": 78.0,       # below this tesseract reads the ruled lines as type
    "glyph_min_chars": 3,
    # Fraction of frame that must be unsaturated for the ground check to run at
    # all. 0.15 assumes a world whose paper is visible in most frames. A film with
    # dense inked environments (a jungle laboratory) legitimately covers the sheet,
    # and demanding paper-dominance rejected three perfectly good frames in a row.
    "ground_min_paper": 0.15,
    "accent_share": [0.0, 100.0],
}

ASSERTION_RE = re.compile(r'^\s*([a-z_]+)\s*:\s*(.+?)\s*$')


def load_world(film: Path) -> dict:
    """Read the ASSERTIONS block out of WORLD.md. Absent block = house defaults,
    which is correct for a film that has not diverged from the ledger world."""
    cfg = dict(DEFAULTS)
    wm = film / "WORLD.md"
    if not wm.exists():
        return cfg
    text = wm.read_text()
    m = re.search(r'```assertions\n(.*?)```', text, re.S)
    if not m:
        return cfg
    for line in m.group(1).splitlines():
        am = ASSERTION_RE.match(line)
        if not am:
            continue
        k, v = am.group(1), am.group(2)
        if k not in cfg:
            continue
        cfg[k] = json.loads(v) if v.startswith('[') else float(v)
    return cfg


def hsv_planes(arr: np.ndarray):
    """Vectorised RGB->HSV. H in degrees, S and V in percent."""
    a = arr.astype(np.float32) / 255.0
    mx, mn = a.max(2), a.min(2)
    d = mx - mn
    h = np.zeros_like(mx)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    nz = d > 1e-6
    ir = nz & (mx == r); ig = nz & (mx == g); ib = nz & (mx == b)
    h[ir] = (60 * ((g - b)[ir] / d[ir])) % 360
    h[ig] = (60 * ((b - r)[ig] / d[ig]) + 120) % 360
    h[ib] = (60 * ((r - g)[ib] / d[ib]) + 240) % 360
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0) * 100
    return h, s, mx * 100


# ------------------------------------------------------------------- the checks
# Each returns (ok: bool, detail: str). Detail is always populated, pass or fail,
# so --calibrate can print the measurement for a frame the gate is letting through.

def check_edges(arr, cfg, exp):
    """Letterboxing painted into the pixels. Counts near-black bars inward from each
    edge rather than taking a strip mean: b33's bars are 110 and 109 rows deep and read
    0.000, while a legitimately dark object touching the edge only drags a strip mean
    down (b31 hit 0.704, b19 0.793). Depth separates them cleanly; a mean does not."""
    luma = (arr.astype(np.float32) @ [0.299, 0.587, 0.114]) / 255.0
    t = cfg["letterbox_luma"]
    depth = {
        "top":    next((i for i in range(200) if luma[i].max() >= t), 200),
        "bottom": next((i for i in range(200) if luma[-1 - i].max() >= t), 200),
        "left":   next((i for i in range(200) if luma[:, i].max() >= t), 200),
        "right":  next((i for i in range(200) if luma[:, -1 - i].max() >= t), 200),
    }
    bad = {k: v for k, v in depth.items() if v > cfg["letterbox_max_rows"]}
    if not bad:
        return True, "no bars"
    return False, "BLACK BARS: " + " ".join(f"{k}={v}px" for k, v in bad.items())


def check_vertical(arr, cfg, exp):
    """The forbidden margin rule. QC's scan: a thin column measurably redder than the
    paper baseline, covering most of the frame height. b13/b21/b87 read dev +12.5/+13.0
    at vcov 1.00. Nothing legitimate in this world is a thin full-height red column."""
    a = arr.astype(np.float32)
    redness = a[..., 0] - (a[..., 1] + a[..., 2]) / 2.0
    baseline = float(np.median(redness))
    dev = redness - baseline
    hot = dev > cfg["vertical_min_dev"]
    vcov = hot.mean(axis=0)                       # per-column fraction of rows that are red
    cand = np.where(vcov >= cfg["vertical_min_vcov"])[0]
    if cand.size == 0:
        return True, f"max vcov {vcov.max():.2f}"
    # Group adjacent columns into runs; only a THIN run is a rule. A wide one is an
    # object (a red wall, a figure) and is the board's business, not the world's.
    runs, start = [], cand[0]
    for i in range(1, len(cand)):
        if cand[i] != cand[i - 1] + 1:
            runs.append((start, cand[i - 1])); start = cand[i]
    runs.append((start, cand[-1]))
    thin = [(s, e) for s, e in runs if (e - s + 1) <= cfg["vertical_max_width"]]
    if not thin:
        return True, f"{len(runs)} wide column run(s), none thin"
    d = ", ".join(f"x{s}-{e} w{e-s+1} vcov{vcov[s:e+1].max():.2f}" for s, e in thin)
    return False, f"MARGIN RULE: {d}"


def check_ground(arr, cfg, exp):
    """The paper must be the locked colour. The world clause's whole reason for its
    doubled phrasing is that the ground drifts warm on close-ups unless pinned."""
    h, s, v = hsv_planes(arr)
    # Low saturation alone is NOT the paper: near-black and grey are unsaturated
    # too. In the ledger world everything dark was linework, so a bare `s < 15`
    # held. In a collage world with near-black paper elements it does not — eight
    # good frames reported a "ground" of val 15.7 to 22.0, which was the black
    # figure, not the sheet. Paper is UNSATURATED AND BRIGHT, and saying so is the
    # difference between measuring the ground and measuring the ink.
    # The mask thresholds are per-world, defaulting to the values every earlier
    # world was calibrated against. The gillray world's aged laid paper is a warm
    # TINT — sat 15-30 by construction — so `s < 15` finds no paper at all there
    # and every ground check silently becomes "too little paper to judge". A
    # world whose paper IS saturated overrides the MASK; it does not loosen the
    # colour band, which still has to hold on whatever the mask finds.
    paper = (s < cfg.get("mask_sat_max", 15.0)) & (v > cfg.get("mask_val_min", 60.0))
    if paper.sum() < arr.shape[0] * arr.shape[1] * cfg["ground_min_paper"]:
        return True, "too little bare paper to judge — colour unchecked"
    hh = float(np.median(h[paper])); ss = float(np.median(s[paper])); vv = float(np.median(v[paper]))
    okh = cfg["ground_hue"][0] <= hh <= cfg["ground_hue"][1]
    oks = cfg["ground_sat"][0] <= ss <= cfg["ground_sat"][1]
    okv = cfg["ground_val"][0] <= vv <= cfg["ground_val"][1]
    d = f"hue {hh:.1f} sat {ss:.1f} val {vv:.1f}"
    return (okh and oks and okv), d + ("" if (okh and oks and okv) else "  OUTSIDE LOCKED BAND")


def check_hue(arr, cfg, exp):
    """One accent, and only one. b31 came back with brown at 10.75% of frame - more of
    the frame than the red at 8.18%. A second chromatic accent is a different world."""
    h, s, v = hsv_planes(arr)
    # SATURATION ALONE IS NOT COLOUR. s = (max-min)/max, so in near-black ink a
    # two-point RGB difference reads as 40% saturation — pure quantisation noise
    # with a hue attached. In a heavily-inked black-and-white world that noise IS
    # most of the frame: the woodcut batch quarantined 13 frames for a "second
    # accent" whose chromatic pixels had a median brightness of 4 out of 100.
    # Every one of them was monochrome. A pixel that dark cannot be an accent.
    # Default 0.0 preserves every world calibrated before 2026-08-07.
    chroma = (s > cfg["hue_census_min_sat"]) & (v > cfg.get("hue_census_min_val", 0.0))
    total = arr.shape[0] * arr.shape[1]
    lo, hi = cfg["accent_hue"]
    offenders = []
    for b0 in range(0, 360, 15):
        if b0 < hi and (b0 + 15) > lo:            # the accent's own bucket
            continue
        share = float((chroma & (h >= b0) & (h < b0 + 15)).sum()) / total * 100
        if share > cfg["hue_census_max"]:
            offenders.append((b0, share))
    accent = float((chroma & (h >= lo) & (h < hi)).sum()) / total * 100
    if not offenders:
        return True, f"accent {accent:.2f}%"
    d = ", ".join(f"h{b}-{b+15} {sh:.2f}%" for b, sh in sorted(offenders, key=lambda x: -x[1])[:3])
    return False, f"SECOND ACCENT: {d} (accent {accent:.2f}%)"


def check_glyph(arr, cfg, exp):
    """No generated lettering. Catches the hex code that came back drawn as the string
    D9EE13D, and any number or label. It does NOT catch a non-text glyph - the heart on
    b04's fingertip is a shape, and no OCR pass will see it. That one stays with QC."""
    img = Image.fromarray(arr).convert("L").resize((arr.shape[1] // 2, arr.shape[0] // 2))
    p = subprocess.run(["tesseract", "stdin", "stdout", "--psm", "11", "tsv"],
                       input=_png_bytes(img), capture_output=True)
    hits = []
    for line in p.stdout.decode("utf8", "ignore").splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 12:
            continue
        try:
            conf = float(f[10])
        except ValueError:
            continue
        word = f[11].strip()
        # Confidence alone is not enough: tesseract returns high-confidence garbage on
        # outlines. Require a run of real alphanumerics too - the failure this exists
        # for is a hex string drawn into the frame, which is all alphanumeric.
        alnum = sum(c.isalnum() for c in word)
        if conf >= cfg["glyph_min_conf"] and alnum >= cfg["glyph_min_chars"] and alnum >= len(word) * 0.8:
            hits.append(f"{word}({conf:.0f})")
    if not hits:
        return True, "no type"
    return False, "TYPE FOUND: " + " ".join(hits[:6])


def _png_bytes(img):
    import io
    b = io.BytesIO(); img.save(b, "PNG"); return b.getvalue()


def check_accent(arr, cfg, exp):
    """The accent must be legible AS the accent. b85 passed its tread count and still
    failed: a red sleeve of 141,852px sat immediately against the red tread's 99,009px
    in the identical colour, so the one thing the frame existed to show did not read.
    A frame may declare how many separate accent regions it is allowed."""
    h, s, v = hsv_planes(arr)
    lo, hi = cfg["accent_hue"]
    mask = (s > cfg["hue_census_min_sat"]) & (h >= lo) & (h < hi)
    total = arr.shape[0] * arr.shape[1]
    share = float(mask.sum()) / total * 100
    smin, smax = exp.get("accent_share", cfg["accent_share"])
    lab, n = ndimage.label(mask)
    sizes = sorted((int(x) for x in ndimage.sum(mask, lab, range(1, n + 1)) if x > total * 0.002),
                   reverse=True)
    d = f"{share:.2f}% in {len(sizes)} region(s)" + (f" {sizes[:3]}" if sizes else "")
    if not (smin <= share <= smax):
        return False, d + f"  OUTSIDE {smin}-{smax}%"
    # OPT-IN, deliberately. Run as a default, "two comparable accent regions" fired on
    # 25 of 88 frames and only b85 was real - a jacket plus any second red object trips
    # it, and most frames legitimately have both. It is only meaningful where the board
    # says the accent IS the subject, so the board declares it:
    #     "b85": {"accent_regions": 1}
    # This is the gate's honest limit. b85's class of failure is caught only where
    # someone thought to declare it; everywhere else it belongs to QC's eye.
    maxr = exp.get("accent_regions")
    if maxr is not None and len(sizes) > maxr:
        return False, d + f"  MORE THAN THE {maxr} DECLARED REGION(S) - which is the subject?"
    return True, d


CHECKS = [("edges", check_edges), ("vertical", check_vertical), ("ground", check_ground),
          ("hue", check_hue), ("glyph", check_glyph), ("accent", check_accent)]


def gate_frame(path: Path, cfg: dict, exp: dict):
    arr = np.array(Image.open(path).convert("RGB"))
    out = {}
    for name, fn in CHECKS:
        if name in exp.get("skip", []):
            out[name] = (True, "skipped by board")
            continue
        try:
            out[name] = fn(arr, cfg, exp)
        except Exception as e:                    # a check that crashes must not pass a frame
            out[name] = (False, f"CHECK ERROR: {type(e).__name__}: {e}")
    return out


# Exit codes are load-bearing and callers depend on the distinction:
#   0  every frame passed
#   1  a frame FAILED a check - a real defect
#   2  the GATE ITSELF could not run - says nothing about the frame
# Conflating 1 and 2 is what turned this gate into a money burner on its first live
# run: it was invoked with an interpreter that had no numpy, crashed on import, exited
# non-zero, and the caller read that as 48 bad frames and regenerated all of them
# three times for $12.44. A broken gate must fail LOUD, never closed.
EXIT_PASS, EXIT_FRAME_FAILED, EXIT_GATE_BROKEN = 0, 1, 2


def selftest():
    """Verify the gate can actually run before anything spends money on its verdict."""
    problems = []
    for mod in ("numpy", "PIL", "scipy"):
        try:
            __import__(mod)
        except ImportError as e:
            problems.append(f"{mod}: {e}")
    try:
        r = subprocess.run(["tesseract", "--version"], capture_output=True)
        if r.returncode != 0:
            problems.append("tesseract present but not runnable")
    except FileNotFoundError:
        problems.append("tesseract not on PATH")
    if problems:
        print("GATE CANNOT RUN:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(f"  interpreter: {sys.executable}", file=sys.stderr)
        return EXIT_GATE_BROKEN
    print(f"gate ok ({sys.executable})")
    return EXIT_PASS


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print(__doc__); sys.exit(EXIT_GATE_BROKEN)
    film = Path(sys.argv[1]).resolve()
    args = sys.argv[2:]
    cfg = load_world(film)
    gate_cfg_path = film / "production" / "gate.json"
    per_frame = json.loads(gate_cfg_path.read_text()) if gate_cfg_path.exists() else {}

    frames_dir = film / "public" / "images" / "frames"
    if "--frame" in args:
        ids = [args[args.index("--frame") + 1]]
    else:
        ids = sorted(p.stem.replace("-final", "") for p in frames_dir.glob("*-final.png"))

    as_json = "--json" in args
    calibrate = "--calibrate" in args
    results, failed = {}, []
    for fid in ids:
        p = frames_dir / f"{fid}-final.png"
        if not p.exists():
            results[fid] = {"_missing": True}; failed.append(fid); continue
        r = gate_frame(p, cfg, per_frame.get(fid, {}))
        results[fid] = {k: {"ok": v[0], "detail": v[1]} for k, v in r.items()}
        bad = [k for k, v in r.items() if not v[0]]
        if bad:
            failed.append(fid)
        if not as_json:
            if bad and not calibrate:
                print(f"FAIL {fid}")
                for k in bad:
                    print(f"       {k:9} {r[k][1]}")
            elif calibrate:
                print(f"{'FAIL' if bad else 'ok  '} {fid}  " +
                      "  ".join(f"{k}[{r[k][1]}]" for k, _ in CHECKS))

    if as_json:
        print(json.dumps({"failed": failed, "results": results}, indent=1))
    elif not calibrate:
        print(f"\n{len(ids) - len(failed)}/{len(ids)} pass, {len(failed)} fail")
        if failed:
            print("failed: " + " ".join(failed))
    sys.exit(EXIT_FRAME_FAILED if (failed and not calibrate) else EXIT_PASS)


if __name__ == "__main__":
    main()
