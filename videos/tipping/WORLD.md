# WORLD — Tipping (episode 4 of the stills catalog)

Fourth episode in the recurring mid-century painted world. The world is not
re-tested; the twelve direction probes (2026-08-09, $0.51) tested whether THIS
SUBJECT stages in it under three lighting grammars. It does, under all three;
one was chosen.

## The direction (locked 2026-08-09): TRIBUNAL

> One overhead shaft of judgment. Frontal, symmetric, formal.

The comic engine of this episode is a hearing that nobody convened, so the
light behaves like a courtroom fixture: a single soft-edged column falling from
directly above the person being judged, the surrounding field one and a half
values darker, the composition square to the camera the way evidence is square
to a bench. The shaft is PORTABLE — it falls on the man at the counter, on the
1912 crusader on his soapbox, on the $2.13 payroll ledger — because the
argument of the film is that the judgment travels.

Two accents, used sparingly:

- **THEATRE** (hard spotlight, black surround) for 1-2 setpieces where the
  performance-of-judgment thesis is stated outright — the screen-turn beat and
  the "public performance" act.
- **CUSTOMS** (dusty side window-light, long soft beams) for the history acts —
  the 1890s grand hotel, the 1912 Main Street rally, the capitol.

Everything else in the film sits in the shaft or in the plain flat daylight the
series has always used for connective frames. An accent that appears more than
twice stops being an accent.

## The rule this episode is built on

> Every judgment frame has a JUDGE side and a JUDGED side, and the judge side
> is always wrong about itself. The jury is rehearsing, not grading; the screen
> is a monument to a verdict that does not exist.

Stage both halves in one picture wherever possible: the man's hovering thumb
AND the five behind him studying the pastry case; the gloved palm AND the
averted eyes above it. The comedy is the gap. Never cut away to the reaction.

The one exception is the Pullman act, played entirely straight — the same
discipline as the pigeon episode's Cher Ami act, which proved the world can
carry gravity. Customs light, no gags, no jury, no shaft of judgment: the
porter is not on trial and must never be staged as if he is.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted
> cel figures with confident tapering ink outlines and no interior shading, in
> a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE,
> cream and flat VERMILION RED, each scene keying its own dominant colour from
> that set. Expressions are BOLD, exaggerated and readable at a glance. Visible
> gouache texture, flat matte, NO gradients, NO airbrushed shading, NO
> photographic texture, NO three-dimensional rendering.

Tribunal lighting is painted IN THIS IDIOM: the shaft is a flat lighter-value
gouache column with a hard painted edge, not a rendered volumetric beam. The
darker surround is a flat darker mix of the scene's key colour, not a vignette.

Plus the standing laws: no text of any kind, blank signs, no franchise designs
and no likeness of any real person, one coherent scene, 16:9.

## Standing lessons that bite hardest on THIS subject

**1. Sign-shaped objects attract lettering — and this film is MADE of them.**
The tablet, the buttons, the 1912 protest signs, the ledger, the diner menu
board, the split checks. The fix is never a stronger prohibition; it is the
pigeon lesson applied everywhere: the tablet shows THREE BLANK ROUNDED
RECTANGLES and one small blank rectangle below, the protest signs are BLANK
BOARDS held aloft, the ledger is RULED LINES with no figures, the checks are
blank slips. The $2.13 number exists only in narration and in the deterministic
data frames — never asked of the model.

**2. Counts are stated at point of use.** Three buttons (never "some buttons"),
five jurors plus ONE staring child, TWO points on the Grand Waiter's tailcoat,
ONE white glove, THREE buttons on the red coat, ONE pencil in the apron, eight
diners at the split-check table. A reference sheet is not sufficient; the count
appears in every frame prompt that stages the character.

**3. The cast clause loses; omission wins.** `production/cast.json` ships with
the FIRST batch. `generate-frames.mjs` withholds the character sheet from every
frame whose scene names no character. A cafe is a place that contains people;
describe the emptiness as a present thing ("the counter stands unattended, bare
cream wall behind it") rather than prohibiting occupants.

**4. The environment cap.** The cafe carries the spine but is capped at ≤20%
of frames (CAST.md law). Ten environments exist; the board budget spreads the
remaining 80% across the grand hotel, the liner, Main Street 1912, the
capitol, the diner, the payroll office, the taxi, the barbershop, the night
street.

## The plates

`castplate.png` — the recurring cast on an empty cream field and NOTHING else.
The man is drawn mid-wince (eyes wide, mouth a flat line of dread), the barista
mid-quarter-turn with a bailiff's neutral formality, because a plate's
expressions are a prior and a neutral plate produces a neutral film.

`layout-plate.png` — ImageMagick flat cream field with faint even grain,
locally built, EMPTY. A plate that contains props donates them to a quarter of
the film.

## The gate needs THESE numbers

```assertions
mask_sat_max: 28.0
mask_val_min: 58.0
ground_hue: [25.0, 95.0]
ground_sat: [0.0, 32.0]
ground_val: [62.0, 100.0]
ground_min_paper: 0.01
letterbox_max_rows: 4
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
vertical_max_width: 4
accent_hue: [0.0, 20.0]
hue_census_max: 100.00
glyph_min_conf: 78.0
```

Inherited from the pigeon episode unchanged — same painted world, same bands.
One watch-item the tribunal grammar adds: the darker surround of the shaft
lowers frame-mean value but the GROUND check reads the bright unsaturated
region (the shaft's floor, the cream wall), which stays inside ground_val
[62, 100]. If the first five frames breach ground_val, the shaft surround is
painted too dark — fix the prompt's value language ("one and a half values
darker", never "in darkness"), not the band. Calibrate on a 5-frame round
before the batch, per the grip-strength lesson.

**What the gate cannot see** and what QC by eye must: whether both halves of
the judge/judged frame are present, whether the Pullman act stayed straight
and shaft-free, whether the tablet reads as a monument rather than a gadget,
and whether the man is someone the audience wants to spend ten minutes with.
A green gate is not evidence the episode holds.
