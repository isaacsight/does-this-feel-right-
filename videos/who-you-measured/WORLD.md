# WORLD — risograph, two inks, no cast

Tested and locked 2026-08-04. **7 images, $0.28.** This is the validated world
clause; the Art Director ratifies it and owns the FRAME-BOOK, but does not need to
rediscover any of what is below.

## Why this world

The last four films are flat vector comic — three on cream, one on ledger paper.
Same medium, same mark, four films running. Risograph keeps what works (bold,
graphic, flat, cheap to hold consistent) and changes the one thing that never has:
**the surface**. Grain and misregistration instead of clean fills.

It also argues. Riso is a duplicator — a machine for many fast, slightly imperfect
copies. For a film about findings that got copied far past their evidence, the
medium is doing work.

**The inks are structural, not decorative.** The pop story of dopamine is hot and
about pleasure; the mechanism is cool and predictive. One ink is the myth, one is
the finding, and the violet where they overlap is exactly where the public
confusion lives.

## The locked clause

> a RISOGRAPH PRINT: the whole image is printed in exactly TWO inks on uncoated
> off-white paper with visible paper tooth, and the paper is the SAME warm
> off-white across the whole frame with no change of paper colour toward the
> foreground and no cool grey or pure white anywhere. The two inks are a bright
> FLUORESCENT PINK and a deep BLUE, and nothing else. Every filled area is a
> coarse visible halftone of round dots, never a smooth flat fill. The two ink
> layers are slightly MISREGISTERED so their edges do not line up and a narrow
> band of bare paper shows along one side of every shape. Where the two inks
> overlap they multiply into a single darker violet. The ink is semi-transparent
> with uneven roller coverage, patchy density and occasional light streaking. No
> gradients, no soft shading, no glow, no drop shadows, no photographic texture.
> Edges are slightly ragged from the screen. There is NO text, NO lettering, NO
> numbers and NO writing of any kind anywhere in the image.

Colours are named in words. **Never put a hex code in a prompt** — `#D9E2DA` came
back drawn into the frame as the string `D9EE13D` (PLAYBOOK 10.33).

## The three things tested, and what they cost

**1 · The medium passes, convincingly.** Paper tooth, coarse halftone,
semi-transparent uneven ink, ragged screen edges, and a real multiply in the
overlap. Two inks only — no third leaked in across seven images.

**2 · The halftone survives the render path.** Tested free, on the actual path:
downscaled to 1920x1080, pushed through `assemble.mjs`'s zoompan, and sampled at
the end of the move. **No moiré.** The dots read as texture with only the expected
softening. This was the risk most likely to kill the world and it is clear.

**3 · The misregistration will NOT hold a direction — and that is fine here.**
Measured pink-vs-blue offset across five frames: `-14,+14` · `+14,0` · `-12,+14` ·
`-2,-8` · `+8,0`. The signs disagree on both axes; the model cannot place it
consistently. The clause therefore **asks for misregistration but no longer
specifies a direction** — asking for something the model will not honour spends
prompt budget and invites artifacts.

This is deliberately a *different* ruling from the ledger's margin rule, which was
forbidden for exactly this inconsistency. The distinction is that the margin rule
was **one discrete object** whose placement varied visibly frame to frame, while
misregistration is a **whole-frame texture** — and real risograph genuinely varies
between pulls. An inconsistent object reads as sloppiness; an inconsistent texture
reads as print.

## THE FILM HAS NO CAST — this is a world decision, not a story one

**The character does not survive this surface.** In the first test the figure came
back an unreadable blob in the wide, and in the close-up the protagonist's two fine
hairs rendered as insect antennae with the whole head reading as a bug. Halftone
plus deliberate misregistration destroys precisely the small consistent details the
character is built from. There was also a stray ink rectangle behind the head that
nothing asked for.

So this film is **object-led**: no people, no figures, no hands, anywhere. The
subject makes that a gain rather than a compromise — measurement, distributions,
populations and samples all have object vocabulary. The second test proved it:
hundreds of identical circles with one outlier; two rooms in cross-section, one
full and one empty; a scatter cloud with a line through it; a curled card corner in
extreme close-up.

**This breaks the character-spine rule** (`cognitive-debt/WORLD.md`: the protagonist
carries across films as the narrator's voice does). One deliberately cast-free film
in a distinct medium reads as an edition rather than a drift, and Isaac approved the
trade on 2026-08-04. It is a decision to revisit per film, not a new default.

## The gate needs THESE numbers, not the ledger's

`tools/video/frame-gate.py` reads its assertions from this file. Measured across the
seven test images — the band is widened from the measurement for headroom, and the
target is **zero false positives on frames that are right** (PLAYBOOK 10.37).

Measured on the 7 test images, then **re-measured across all 78 finished frames**:
paper hue 31.2–60.0, sat 4.0–13.9, val 83.9–96.1 · pink hue 328.1–345.2.

`accent_hue` was widened from 345 to 360 after the re-measure. The 7-image band
stopped at 345; `b74`'s pink medians at 345.2 and its tail lands in the 345–360
census bucket, so the gate read the film's own ink as a second accent. A band
measured on seven frames is a hypothesis; the band measured on seventy-eight is
the world.

```assertions
letterbox_max_rows: 4
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
ground_hue: [30.0, 70.0]
ground_sat: [0.0, 18.0]
ground_val: [80.0, 98.0]
accent_hue: [315.0, 360.0]
hue_census_max: 40.00
glyph_min_conf: 78.0
```

**Read `hue_census_max: 40.00` before changing it.** This world has TWO inks by
definition, so a large second chromatic bucket is *correct*, not a fault — the
ledger's 3.00 would fire on every single frame. The census is effectively disabled
here and a third ink must be caught by eye at QC instead. Say so out loud rather
than letting a passing gate imply coverage it does not have.

`vertical_min_vcov` is kept strict because misregistration puts a narrow ink band
along one edge of every shape, and a tall object could otherwise read as a rule.

## Resolution — RESOLVED 2026-08-04

`nano-banana` text-to-image returns **1344x768 (1.750)**, below canvas. That is why
the world test and the plates are that size, and it does not matter for a plate:
`generate-frames.mjs` downscales every reference to 1024 wide before encoding it.

**Production is clean.** The first conditioned frame through `nano-banana/edit`
came back **1920x1080**, on the first attempt, passing the gate. The open question
is closed: nothing is upscaled into the canvas.

The layout plate must be scenically EMPTY (PLAYBOOK 10.9). With no cast there is no
castplate; the plate that matters here is the world plate — paper, ink pair,
halftone, ground line, nothing else.
