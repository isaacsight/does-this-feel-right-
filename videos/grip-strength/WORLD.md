# WORLD — The Instrument Room (motion strand pilot)

Written fresh 2026-08-09 (house rule: never inherit a WORLD.md). This is NOT
the mid-century painted world of the stills catalog — see FORMAT.md. It is a
motion-design world, authored in the layered grammar of the
`motion-prompt-language` skill, because every one of these frames will be
ASKED TO MOVE and the world has to be built from things that move well.

## Concept

**The instrument room.** The film's argument lives in instruments — a
dynamometer, a needle, a receipt printer, a fuel gauge — reading a human body
they cannot see. So the world is a dark, calm measurement space where luminous
instruments and warm human hands are the only living things. Every scene is
one instrument, one reading, or one hand. The tension of the piece — warm
flesh vs cold meter — IS the palette.

## Visual language

Flat graphic motion-design idiom in the register of Buck / Territory Studio /
DIA: bold simplified forms, engineered line work, generous negative space,
2D planes with shallow parallax implied by scale, no photorealism. One subject
per frame, oversized, centred or rule-of-thirds anchored — these frames are
i2v sources, and the model animates a single bold subject far better than an
ensemble.

## Palette (fixed — the LOCK clause needs something stable to hold)

- **Field:** deep INK-BLACK-BLUE (#101820 family) — every scene sits on it
- **Bone:** warm off-white for line work and instrument faces
- **Signal ORANGE:** one accent (#E24E1B family — kin to the house tomato,
  different world) — needles, readings, the moving thing. The mover is
  ALWAYS the orange thing where possible: it tells the i2v model what moves
- **Flesh:** a single warm muted skin tone for hands — the only organic colour
- **Steel grey:** instrument bodies

Fine even film grain, flat matte, NO gradients beyond a single soft vignette,
NO lens flares, NO photographic texture, NO 3D rendering.

## Camera

Locked off, always, in-model — the measured rule stands: never ask the clip
model for a camera move. Crops are keyframe-side (camera-as-crop grammar from
the stills pipeline: XCU/CU/MED/WIDE as crop instructions). Any camera feel
is added deterministically in assembly if ever wanted; default is none.

## Animation (the motion vocabulary — what things DO here)

One nameable motion per clip, orange wherever possible:
- a needle SWEEPS and settles
- a hand CLOSES around a handle, tendons rising
- a receipt FEEDS upward out of a printer, one line at a time
- a gauge needle SINKS
- a line DRAWS itself across a dark field
- keys DEPRESS under fingertips; a hay bale SWINGS up (the two-eras beat)
- dust MOTES drift in the instrument light (the ambient default)

Motion starts after the cut lands; every clip ends on a settle. BIG moves
(4-6 in the film, never adjacent) are reserved for: the first squeeze, the
needle-beats-the-cuff beat, the 1985/2016 comparison, the receipt reveal, and
the final squeeze. Everything else is ambient micro-motion.

## Typography

NO generated lettering, ever — the no-text law holds precisely BECAUSE type is
central to motion design: every number and word is composited in POST
(`typeset-cards.py` pattern; deterministic, correct, and animatable in
assembly), never asked of the image model. Any dial face, receipt or label in
a generated frame is BLANK; the type lands on it afterwards. Sign-shaped
objects attract lettering, so dial faces are drawn as marks-only (ticks, no
numerals) at the keyframe stage.

## Lighting

Single-source instrument glow: subjects lit as if by their own reading. Hands
warm-lit from the instrument side. The field stays dark and even — no
ambient wash, no sky.

## Texture

Fine grain, subtle paper-tooth on bone linework, clean steel on instruments.
Surfaces named clean (the measured rule: name the clean surfaces, because
there is no negative prompt).

## Timing

2:30 total, ~28-32 clips of 4-6s. Cuts land on sentence starts per
words.json, as in the stills pipeline. Inside a clip: still beat → motion →
settle. The film breathes on the settles.

## Data frames

The force curve and the 1985/2016 comparison are DATA. They are never given
subject motion (measured rule: the model redraws data wrong). They are built
as still keyframes with post-composited type, and any motion on them is
deterministic in assembly (a line revealed by crop, a bar grown by mask) —
never generated.

## The gate needs THESE numbers (CALIBRATED 2026-08-09 after the first batch — see below)

This is a DARK world; the stills catalog's bands do not transfer. These are
declared from the palette, and the probe round calibrates them before any
batch money moves (band must cover what the world DECLARES, not what the
first frames happen to contain):

```assertions
letterbox_max_rows: 4
letterbox_luma: 0.04
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
vertical_max_width: 24
ground_hue: [30.0, 80.0]
ground_sat: [0.0, 20.0]
ground_val: [75.0, 98.0]
ground_min_paper: 0.15
accent_hue: [8.0, 25.0]
hue_census_max: 100.00
glyph_min_conf: 78.0
```

**How the first calibration went wrong, so the next dark world skips this:**
the provisional bands were written from what the world LOOKS like; the gate
measures something else. `letterbox_luma 0.10` counted the ink-black field
itself as bars (the field sits at ~0.09 luma — the threshold now sits BELOW
the field at 0.04, so only true encode-black registers). And the "ground"
check does not measure the background — it measures the bright unsaturated
region, which in a dark world is the bone PAPER, hue 40-70. Banding it
[190, 240] for ink-blue rejected every frame containing what the world is
made of. Thirty frames went to quarantine against a wrong instrument before
any picture was actually judged. The rule from the stills catalog applies
with a twist: a band must cover what the world declares — AS THE INSTRUMENT
MEASURES IT, not as the author imagines it.

**What the gate cannot see:** whether the mover is the orange thing, whether a
clip settles, whether the film feels like one instrument room. That is the
drift gate plus QC by eye, per the plan.
