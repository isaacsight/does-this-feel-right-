# WORLD — the Gillray etching, hand-coloured

Proven by a 15-image three-world test (gillray / manual / theatre), $0.58,
2026-08-05. Bands below are measured across the FIVE test probes only — a band
from five images is a hypothesis. Re-measure across the finished batch before
trusting a rejection.

## Why this world

**The medium is the argument.** Ridicule killed the duel — Wellington's 1829
duel became cartoons, and the cartoons did in twenty-five years what law, God
and logic couldn't in two hundred. This film is drawn as the hand-coloured
satirical print that did the killing. When the narration says "it looked
ridiculous," the picture already is one.

It is also the register's native habitat: Gillray was the Larry David of 1800.
Every plate is an aggrieved man litigating an unwritten rule.

Sixth distinct world in seven films (ledger, riso, collage are the recent
three; nothing near hand-coloured etching in the catalogue).

## The locked clause

> a HAND-COLOURED REGENCY ETCHING in the manner of British satirical prints
> circa 1800: fine crosshatched copper-etched linework in warm sepia-black ink
> on aged cream laid paper, coloured with flat translucent watercolour washes
> in vermilion red, prussian blue, mustard yellow, sage green and rose pink
> that sit loosely inside the lines. Faces and bodies are CARICATURED: bulging
> eyes, ballooning coats, tiny legs, enormous indignant gestures. Visible
> plate tone and paper grain, slightly uneven wash edges, a faint plate-mark
> border. Flat matte, NO photographic texture, NO digital gradients. There is
> NO text, NO lettering, NO numbers, NO signatures and NO writing of any kind
> anywhere in the image. This is ONE SINGLE COHERENT SCENE, NOT a grid, NOT a
> sheet of studies. 16:9, edge to edge, one scene, one camera.

Colours in words, never hex.

**The stolen device:** the manual world's diagram grammar — DOTTED GUIDE
LINES, dashed arrows, pointing-hand manicules — is licensed INSIDE this world
for the rules sequences only (the code duello act, the honour-arithmetic act).
Etchings of the period genuinely used those conventions. It is a device, not
the world: a frame that is ONLY diagram belongs to the manual world and fails.

## What the test settled

**The aggrieved close-up is the best face any world has produced** — bulging
eyes, brows up, mid-complaint. The register survives the medium.

**The NO TEXT clause held on all five probes**, including the crowded ones.
(It also held on the manual world, which was that world's kill-risk.)

**Caricature does not break the cast** — both kinked hairs survived every
probe — but the medium AGES him: he comes back jowly and Regency-faced unless
pulled back toward canon. The castplate plus point-of-use description carry
that correction.

**Counts must be stated at point of use.** The pistol-case probe asked for
"two duelling pistols" loosely and got three. Every countable feature in a
board prompt states its count (PLAYBOOK; same lesson as the two hairs).

## The plates

**castplate.png = the test's k2 full-body frame** (proven-frame method, the
collage lesson — a generated turnaround sheet invites elaboration). It teaches
construction, palette, coat, legs and both hairs. Its face is older than
canon; boards must describe the round young face at point of use.

**layout-plate.png is DRAWN, not generated**: ImageMagick, the world's own
sampled cream (`#e5d7b9`, hue 41 sat 19 val 90) with the in-world plate-mark
border at 38px inset. Empty by law — a plate is a prior on everything it
contains.

## The gate needs THESE numbers

The gillray paper is a warm TINT — sat 15–30 by construction — so the gate's
default paper mask (`s<15 & v>60`) finds nothing here. This world overrides
the MASK (`mask_sat_max`, `mask_val_min`, added 2026-08-05, defaults preserve
every earlier world). The colour band still has to hold on what the mask
finds; a mask override is not a band loosening.

Measured across the five probes (margin sampling, p5–p95): hue 25–45,
sat 15–49, val 49–95 on the bright regions. Provisional bands sit a step
outside each end (the b49 lesson — a band drawn on the extremes fails the
next frame one step out):

```assertions
mask_sat_max: 34.0
mask_val_min: 55.0
ground_hue: [22.0, 50.0]
ground_sat: [12.0, 45.0]
ground_val: [55.0, 97.0]
ground_min_paper: 0.01
letterbox_max_rows: 4
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
accent_hue: [0.0, 20.0]
hue_census_max: 100.00
glyph_min_conf: 78.0
```

**`hue_census_max: 100.00` disables the census, deliberately** — five wash
colours make this world polychrome by design, so a large second chromatic
bucket is correct. A foreign colour must be caught by eye at QC; the gate
does not cover it, and 90/90 passing does not imply it does.

`accent_hue` is the vermilion band so opt-in accent regions still mean
something (his coat is the constant).

**Never inherit a WORLD.md across worlds** — this file was written fresh; the
collage file stays in its own film.
