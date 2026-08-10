# WORLD — Selling Immortality (episode 6 of the stills catalog)

Sixth episode in the recurring mid-century painted world. The 12-probe
direction bake-off (2026-08-10, $0.47) tested three grammars; MIDWAY locked
with two accents.

## The direction (locked 2026-08-10): MIDWAY

> Warmth as bait. The booth and its product glow like a lit window full of
> company, and the crowd leans toward the glow.

The booth and the amber product carry flat warm MUSTARD GOLD light — strings
of warm round bulbs, painted as flat discs, never rendered glows — while the
surrounding scene sits in cool flat INK BLUE evening. The camera stands IN
THE QUEUE at eye level, so the booth is always slightly above and ahead, the
way a stage is. The seduction must actually seduce: the booth is beautiful,
never obviously fake — the viewer should feel the pull that emptied 12,000
waiting rooms.

**THE BULB-BOOTH** is this episode's monument object (the catalog's third,
after the tipping slab and the six-hundred-pound phone): ONE wooden stall
lined with ONE row of warm round bulbs, the same recognizable cart re-dressed
in every era. **THE VIAL LAW:** the product is ONE small glass vial of softly
glowing warm amber, THE SAME AMBER IN EVERY ERA — vial, bottle, molecule
diagram, IV bag, pill: the amber never changes, because the promise never
does.

Accents:

- **APOTHECARY** (order as authority) for product/authority frames: walls of
  identical bottles in neat ranks, polished wood and brass, frontal shop-
  portrait symmetry, every label a completely BLANK paper rectangle. Light
  passes THROUGH the amber before it reaches any face.
- **PROSPECTUS** (paper as promise AND as executioner) for the institutional
  act only: the $720M deal, the halted trial, the one-page FDA statement.
  Dusty pale daylight in long beams, desk lamps, documents with wax seals and
  ribbons — all BLANK — handled like treasure; the camera slightly elevated,
  the auditor's angle.

Connective frames use the series' plain flat daylight.

**THE WARM-MAN LAW carries over from the lonely chapter:** in every evening
frame the Man keeps "his red coat and warm face unchanged in the blue
evening," stated at point of use.

## The rule this episode is built on

> The customer is never the joke, and the booth is never ugly.

Every buyer in every era behaves reasonably inside one false premise; the
staging shows the premise, not fools. The queue is drawn with dignity — the
same small want on every face. The Man appears in EVERY era's queue in his
unchanged red coat (the one-design-every-century trick, now the film's
argument).

The one act played entirely straight: the Byers act. No gags, no glow-
worship, no queue — the pharmacy shelf, the bottles, the man, and the
consequence, with the same discipline as the Pullman and Cher Ami acts. The
period's own black line is spoken by the narration; the pictures never wink.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted
> cel figures with confident tapering ink outlines and no interior shading, in
> a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE,
> cream and flat VERMILION RED, each scene keying its own dominant colour from
> that set. Expressions are BOLD, exaggerated and readable at a glance. Visible
> gouache texture, flat matte, NO gradients, NO airbrushed shading, NO
> photographic texture, NO three-dimensional rendering.

Plus the standing laws: no text of any kind, blank signs and labels and
documents and screens, no franchise designs, no likeness of any real person,
one coherent scene, 16:9.

**LIKENESS LAW, sharpened for this film:** Brown-Séquard, Voronoff, Byers,
Sinclair and Johnson are NEVER drawn as portraits of the real men. The board
stages period TYPES (a bearded lecturer, a proud surgeon, a believer at a
counter, a modern protocol-keeper) — no frame may be captioned as or resemble
a specific real person. The apothecary probe leaked lettering ("PHA...CY");
poster and label blankness is stated at point of use in every sign-bearing
frame.

## Standing lessons that bite hardest on THIS subject

1. **Named lighting colours** — the booth glow is MUSTARD GOLD, the evening
   INK BLUE, stated in the rows; never "warm light" alone.
2. **Flat objects need a camera that can see their surface** — the vial
   STANDS (safe); any flat document on a desk gets a slightly elevated
   camera stated in the row.
3. **Sign-shaped objects everywhere:** labels, posters, prospectuses,
   certificates, tickets, the FDA page — ALL described as completely BLANK
   at point of use, every time.
4. **Places draw their occupants:** empty-shelf or empty-clinic frames
   describe the emptiness positively ("the counter still and unattended").
5. **Counts at point of use:** ONE row of bulbs, ONE amber vial, TWELVE
   lecture-hall physicians, THREE ticket-holding rich men, ONE monkey on a
   fence, FOUR recliners, ~ONE HUNDRED pill bottles drawn as a wall (state
   "a wall of identical small bottles," never a countable claim).
6. **Retake-to-temp; sat-floor eyeball rule; data rows excluded from
   prompts; the register splitter in map-shots** — all inherited.

## The plates

`castplate.png` — the Man (winning two-hair phrasing) and THE BARKER (this
film's counterpart figure: a tall smiling salesman in a dusty ORANGE coat
and ONE straw boater, one arm presenting) on empty cream, both
mid-expression. `layout-plate.png` — the local ImageMagick empty cream field
(copy from tipping).

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

Inherited unchanged. WATCH-ITEMS: (1) night-street Midway frames are
dark-field-heavy — the ground check must find its bright unsaturated region
in the warm booth areas or cream surfaces; if the first five frames breach
ground_val, fix the value language ("a step and a half darker," never
"night"). (2) The amber glow at low saturation can read as near-neutral —
if ground_hue quarantines at sat < 8, eyeball before respending. Calibrate
on a 5-frame round before the batch, as always.

**What the gate cannot see** and eye-QC must: whether the booth actually
seduces, whether the Byers act stayed straight, whether any face drifts
toward a real person's likeness, whether the amber is the same amber in
every era, and whether the queue reads as dignity rather than mockery. A
green gate is not evidence the episode holds.
