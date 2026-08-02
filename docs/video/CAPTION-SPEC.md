# Caption spec — house law

> Rewritten 2026-07-24 after building *The Last Thing That Happens*. The previous
> version of this file recommended `add_captions` with `wordPop`, Courier Prime
> at 64px, and `centerY: 0.70`. **Every one of those was wrong.** What follows
> is what actually shipped, and why each alternative failed.

## The settings

```
fontName   AvenirNextCondensed-Heavy   (PostScript name, exact)
fontSize   52                          (canvas POINTS — see below)
bold       true
color      #1F1E1D                     ink, and nothing else
fontCase   uppercase
tracking   -1
alignment  center
outline    disabled
shadow     disabled
transform  { centerX 0.5, centerY 0.63, width 0.94, height 0.15 }
animation  popIn                       whole-card, not per-word
```

Cards are built with **`add_texts` from the locked script** — never
`add_captions`. Target **~2 seconds per card, 2 lines maximum, ≤21 characters
per line.**

## Five things that cost this film an afternoon

### 1. `fontSize` is canvas points, not pixels

At `fontSize: 62` each glyph renders about **58px wide** on a 1080px canvas.
Every size chosen by pixel intuition came out enormous — 124 was overwhelming,
82 still forced three lines.

**Work backwards from the constraint instead.** A caption block must stay above
y=1436. At **52 points** you get roughly **21 characters per line**, and even a
three-line block clears both the picture above and the chrome below.

### 2. `maxWords` does not control how many cards you get

`add_captions` chunks on **speech pauses**, not word count. maxWords 3, 5, and
10 all produced **exactly 84 cards** on the same 52-second track — one card every
0.6 seconds. Unwatchably fast, and there is no parameter that fixes it.

### 3. Build cards from the locked script, not from ASR

`add_captions` derives text from ASR, which rendered "Kahneman's" as
**"Canneman's"** and "plus thirty more" as **"+30 more"** — and reproduced both
every time the group was regenerated.

`add_texts` at sentence timings from `get_transcript` gives text that is
**correct by construction**, chunking that is a deliberate choice rather than a
record of where the narrator breathed, and cards that land on the same
boundaries as the picture cuts. Get timings with
`get_transcript({granularity: 'segments'})`, then author the cards.

### 4. Word-by-word animations are not single-colour

`wordReveal` fades words in, so unspoken words sit at **mid-grey** — whole cards
render as a pale wash, and the first frames of a card are **completely blank**
because nothing has faded in yet.

`highlightPop` with a contrasting `highlightColor` is worse on a short: with 55%
of cards a single word, the accent becomes a full-screen colour strobe about
twice a second. Over 52 seconds that is genuinely fatiguing — it was described,
accurately, as giving a headache.

**One colour, whole-card `popIn`.** The research favouring word-by-word for
retention is real, but it assumes cards that hold long enough to read. At 0.6s
a card it inverts.

### 5. `update_text` re-fits the box unless you pass `transform`

Correcting a caption's `content` to longer text re-fits the box and **clips the
overflow** — "KAHNEMAN'S" shipped as "KAHNEMAN'". Always pass an explicit
`transform` alongside a content change to pin the box.

Note also that a content edit **clears that clip's word timings**, so any
per-word animation silently degrades to plain text on it. Another reason to
author cards correctly the first time.

## Safe zones

Full derivation in [`SHORTS-TEMPLATE.md`](SHORTS-TEMPLATE.md). Reserves are the
union across all three platforms: **top 130px, bottom 484px, left 60px, right
140px** — usable box **880 × 1306**.

`centerY: 0.63`. The old value of **0.70 left twelve pixels** of clearance under
a two-line caption and none at all under three.

## Verification — do all three

1. **Measure every card's width** against the frame before exporting. A script
   that renders each caption in the real font and compares to the safe width
   catches overflow that no amount of looking will.
2. **Contact-sheet the export** with the safe zones drawn over it — one frame per
   cut, all on one image. Every three-line overflow in this film was found this
   way and none were visible in the editor.
3. **Look at one full-resolution frame.** Thumbnail scaling hides the difference
   between "tight" and "clipped"; twice in this session a contact sheet led to
   the wrong diagnosis that a full-size frame corrected immediately.

## Checklist

- [ ] Cards authored with `add_texts` from the **locked script**
- [ ] ~2s per card, ≤2 lines, ≤21 characters per line
- [ ] AvenirNextCondensed-Heavy, 52pt, ink, uppercase
- [ ] One colour — no highlight, no per-word animation
- [ ] `centerY: 0.63`, explicit `transform` on every clip
- [ ] No orphan last lines (a single word alone on line 2)
- [ ] Widths measured programmatically — zero over the safe width
- [ ] Contact sheet checked with safe zones drawn

---

## Finding 6 — this machine's ffmpeg cannot render text at all

Discovered 2026-07-25 building the polyvagal verticals. Homebrew ffmpeg 8.0.1
on this Mac is built **without libass and without libfreetype**:

```bash
ffmpeg -hide_banner -filters | grep -iE "subtitles|^ .. ass|drawtext"   # returns nothing
```

So `subtitles=`, `ass=` and `drawtext=` all fail — `drawtext`/`subtitles` die
with a filter-parse error (misleading; it looks like an escaping problem and
you will waste a cycle escaping commas), and `ass=` dies honestly with
**"No such filter: 'ass'"**. Check for the filter before you debug the string.

**The working method: render caption cards with ImageMagick, composite with
ffmpeg `overlay`.** One transparent 1080×1920 PNG per cue, gated by `enable`:

```
[0:v]scale=1080:-2,pad=1080:1920:0:380:color=0x151312[bg];
[bg][1:v]overlay=0:0[v0];
[v0][2:v]overlay=0:0:enable='between(t,0.000,2.200)'[v1];
...
```

A single-frame PNG input holds under `overlay` (default `eof_action=repeat`),
so no `-loop 1` is needed. ~30 overlays in one chain is fine.

### The font

`magick -list font` returns **nothing** on this machine — no fonts are
registered. Pass the file path instead, and the TTC's default face is the one
we want:

```bash
# wrap on MEASURED width — caption: cannot overflow its -size box
magick -background none -fill '#FAF9F6' \
  -font "/System/Library/Fonts/Avenir Next Condensed.ttc" \
  -pointsize 76 -interline-spacing 12 -size 880x -gravity center \
  caption:"the whole line, unwrapped" block.png
magick -size 1080x1920 xc:none block.png \
  -gravity south -geometry -40+560 -composite card.png
```

**Never wrap by counting characters.** The first cut of these shorts did, with
a 21-char budget, and text ran off three cards. Two independent failures: a
character budget says nothing about rendered width on wide glyphs, and any
"rewrap to at most 2 lines" step merges a correct 3-line wrap back into ~28-char
lines that overflow by construction. `caption:` with a fixed `-size 880x` wraps
on measurement and cannot exceed the box. Step the pointsize down 76 → 54 in
6pt increments while the block is taller than ~300px (3 lines).

**The safe box is not centred on the canvas.** Left reserve 60, right reserve
140, so the usable centre sits at x=500 — every horizontal placement carries
`-40`. Centring on 540 pushes type into the right-hand action rail.

**Pointsize 76 here ≈ fontSize 52 in Palmier**, which is the locked look —
21 characters spans ~800px of the 880px safe width. The kicker is pointsize 38,
`-kerning 7`, `-fill '#E24E1B'`, `-gravity north -annotate +0+190`.

`-gravity south` bottom-anchors the block, so one- and two-line cards share a
bottom edge and the type doesn't jump between cards. Their optical centres land
at 0.685 and 0.66 — slightly below the template's 0.63 but well inside the
bottom reserve.

Reusable implementation: [`tools/shorts/cut-verticals.py`](../../tools/shorts/cut-verticals.py).

**Palmier is still the alternative** and produces identical typography via
`add_texts` — but it costs an import/export round-trip per revision, and the
media cache will refuse a re-import under the same filename (Finding 4). For
cutting verticals out of a finished master, the ImageMagick path is faster and
fully scriptable.
