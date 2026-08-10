# WORLD — The Lonely Chapter (episode 5 of the stills catalog)

Fifth episode in the recurring mid-century painted world. The 12-probe
direction bake-off (2026-08-10, $0.47) tested three grammars; EMBER was
locked with two accents.

## The direction (locked 2026-08-10): EMBER

> Light is membership. Every warm light in the frame belongs to a group the
> man is not in.

Golden lodge windows, lit bars, lamplit rooms full of company — painted flat
MUSTARD GOLD — while the man stands in cool flat INK BLUE dusk. The camera
sits at street level and frames him through or beside a threshold (a window
pane, a doorway, a fence): the warmth is always exactly one pane of glass
away. Both temperature fields are flat matte gouache, never gradients.

**THE WARM-MAN LAW.** The Man himself stays warm-palette inside any dusk:
the vermilion coat and warm skin tone hold. Two probe frames drew him cool
and blue; that is a named failure and the board states his warmth at point
of use in every dusk frame ("his red coat and warm face unchanged in the
blue evening").

Accents:

- **VACANCY** is a STAGING LAW, not a lighting mode — available in any frame
  under any light. The empty second place is drawn as carefully as a
  character: the vacant chair squared to the occupied one, the empty half of
  a booth given equal pictorial weight, the second soda with no hand for it.
- **PROCESSION** is the accent for the 1920s lodge act — full formal
  group-portrait pageantry, ranks of men in mustard collars, banners and
  candles — plus exactly ONE mirrored-empty modern frame (the same ceremonial
  composition drawn as bare floor). More than that and the device stops
  landing.

Connective frames use the series' plain flat daylight, as always.

## The rule this episode is built on

> Nobody in this film is pathetic. The silence is mutual, and both sides of
> it are staged.

Wherever the script pairs the man and the friend, the board pairs them too:
two living rooms, two phones, two men leaning and not reaching. The comedy is
logistics (the backward-walking goodbye, the eleven-word text); the ache is
architecture (the lit window one pane away). Never stage the man as broken —
the machinery did this, and the machinery is what gets drawn.

The one act played entirely straight: the mortality act (Holt-Lunstad +
Harvard). No gags, no jury, no comic faces — the same discipline as the
Pullman and Cher Ami acts. Vital-sign gravity.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted
> cel figures with confident tapering ink outlines and no interior shading, in
> a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE,
> cream and flat VERMILION RED, each scene keying its own dominant colour from
> that set. Expressions are BOLD, exaggerated and readable at a glance. Visible
> gouache texture, flat matte, NO gradients, NO airbrushed shading, NO
> photographic texture, NO three-dimensional rendering.

Plus the standing laws: no text of any kind, blank signs and banners and
screens, no franchise designs, no likeness of any real person, one coherent
scene, 16:9.

## Tipping lessons carried forward (all seven, enforced)

1. **Named lighting colours.** No lighting constant ever says "darker mix of
   the scene's colour" — Ember's fields are NAMED (mustard gold warm, ink
   blue cool). The teal drift is a solved problem only while this rule holds.
2. **Sat-floor eyeball rule.** If the frame gate quarantines on ground_hue
   with measured saturation under ~8, the hue is noise — eyeball before
   respending; promote by hand if the frame is right.
3. **Retake-to-temp.** Never delete a passing frame before its replacement
   exists.
4. **One splitter.** map-shots must use register-profile's `[.!?]+` split;
   copy the tipping map-shots, not the pigeon one.
5. **Counts at point of use**, never only in a reference sheet.
6. **Data rows never reach the generator** (excluded from prompts.json at the
   board).
7. **Sign-shaped objects stay blank and described positively** — the phone
   screen shows ONE glowing blank rounded rectangle; lodge banners are BLANK
   cloth; the portrait studio's photographs are BLANK grey plates.

## The plates

`castplate.png` — the Man (winning 2-hair phrasing from the tipping build:
"his head bald and smooth with bare scalp at the sides, bare above the ears,
and at the very top of his crown a single lonely PAIR of hairs: one thin hair
kinking left, one thin hair leaning right") and THE FRIEND on empty cream,
both mid-expression. `layout-plate.png` — the local ImageMagick empty cream
field, reused from tipping (same file works; copy it).

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

Inherited unchanged. WATCH-ITEM: Ember's dusk frames are dark-field-heavy —
the ground check must find its bright unsaturated region in the WARM window
areas (mustard, hue ~40-55) or the cream connective surfaces. If the first
five frames breach ground_val, the dusk field is painted too dark; fix the
value language ("a step and a half darker," never "night"), not the band.
Calibrate on a 5-frame round before the batch, as always.

**What the gate cannot see** and eye-QC must: the warm-man law (a blue-tinted
Man is a retake, not a mood), whether both sides of the silence are staged,
whether the straight act stayed straight, and whether the lit windows read as
membership rather than menace. A green gate is not evidence the episode
holds.
