# WORLD — Quitting (episode 7 of the stills catalog)

Seventh episode in the recurring mid-century painted world. 12-probe bake-off
(2026-08-11, $0.47) locked DEADPAN with two accents.

## The direction (locked 2026-08-11): DEADPAN

> The joke is the stillness. The rule holds everyone perfectly still while
> their situation is plainly absurd.

Butler-formal symmetry: compositions squared to the camera, generous still
space, flat even light, and characters HOLDING PERFECTLY STILL mid-absurdity
with completely composed faces — posing for a formal portrait while snow
drives sideways through them. Nothing dramatic in the light; the drama is
the refusal to react.

Accents:

- **CLUB** for the setpieces only (the donkey act, the verdict beats): a dark
  room, ONE hard spotlight circle, the surround ALWAYS populated with rows of
  individuated silhouettes (the paid theatre lesson — empty black fails), ONE
  deep warm brick-red back wall. The point of the frame stands lit; all else
  keeps politely to the dark.
- **TWIST is a rationed STAGING LAW** for designated sunk-cost frames only:
  ONE quietly wrong detail, never central, never pointed at, sized small —
  something in the frame is always already broken (a clock with one hand, a
  chair with three legs painted matter-of-factly). Cap ~6 designated frames;
  the board tags them.

**NAMED FAILURE:** the club probe drew the Man smug. The Man is NEVER smug —
his face does hope, dread, effort, relief. Gate it.

## The rule this episode is built on

> The grip is priced, never mocked. The people who can't put things down are
> us; the wall is the antagonist, and the wall is just paint.

Every act stages the HOLDING: closed hands, gripped objects (keys, ticket,
lease, schedule). The ending inverts to OPEN HANDS — the board stages the
hands as the film's true subject. The straight act (Langer & Rodin, the two
floors) is played with full Pullman gravity: no deadpan gags, no club light,
no twist details — plain warm daylight, composed elderly faces with dignity,
the plant treated as precious.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted
> cel figures with confident tapering ink outlines and no interior shading, in
> a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE,
> cream and flat VERMILION RED, each scene keying its own dominant colour from
> that set. Expressions are BOLD, exaggerated and readable at a glance. Visible
> gouache texture, flat matte, NO gradients, NO airbrushed shading, NO
> photographic texture, NO three-dimensional rendering.

Plus the standing laws: no text of any kind, blank signs/plaques/tickets/
banners, no franchise designs, no likeness of any real person, one coherent
scene, 16:9. **LIKENESS LAW sharpened:** the gym-wall author is NEVER drawn —
the wall's plaque is BLANK; the leaping-athlete idea is staged as ONE bronze
statue of a generic leaping figure on a BLANK plinth if needed. No frame may
resemble Michael Jordan or Jimmy Carr.

## ALL standing lessons enforced (the 20-law playbook), plus this film's new gate

**THE FLAT-RUN GATE (Isaac's law, first code enforcement):** no more than TWO
consecutive rows that are BOTH castless (expression '-') AND same setting.
The board rejects on any run of 3+. Abstract sentences get concrete distinct
images with a human where the act allows.

Also biting hardest here: label-invitation law (never name a document type or
proper noun in scene text — "ticket" is allowed as the standing exception
ONLY with "completely BLANK" in the same row); named lighting colours; counts
at point of use; omission-not-negation; retake-to-temp; never truncate a
gate's output; data rows excluded from prompts.json.

## The plates

`castplate.png` — the Man (winning two-hair phrasing) holding ONE blank
ticket with both closed hands, mid-dread, and THE WALL-KEEPER (this film's
counterpart: a broad gym coach type in a sage tracksuit with ONE whistle on
ONE lanyard, arms folded, monumentally still) on empty cream. `layout-plate`
— copy from tipping.

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

Inherited unchanged. Watch-items: club frames are dark-heavy (ground check
must find its bright region in the spotlight circle or brick wall — value
language "a step and a half darker", never "black"); snowstorm frames may
trip the vertical gate on driving snow streaks (eyeball before respending —
sat-floor rule applies). Calibrate on a 5-frame round before the batch.

**What the gate cannot see** and eye-QC must: the stillness actually reading
as deadpan (composed faces mid-absurdity, not blank faces), the Man never
smug, the straight act clean of all three grammars, the twist details small
and off-center, and closed-hands vs open-hands staging tracking the film's
arc. A green gate is not evidence the episode holds.
