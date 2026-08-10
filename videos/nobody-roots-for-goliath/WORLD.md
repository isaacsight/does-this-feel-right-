# WORLD — the mid-century animation idiom (Chuck Jones)

Proven by a 5-image test, $0.20, 2026-08-07, after the Masereel woodcut cut was
rejected. Three world tests total on this film ($1.36) — the two earlier rounds
are recorded below because what they ruled OUT is the reason this one is right.

## Why this world, and what the woodcut got wrong

The woodcut film was rejected in three words: **creepy, humourless, and it
loses continuity.** All three were measurable, and all three were mine:

| fault | measurement |
|---|---|
| loses continuity | character in frame **26%** — against 44–56% in the three films that shipped |
| scenes don't match narration | **13%** of frames were abstract objects (scales, coins, masks, mirrors); the board illustrated the MECHANISM instead of the story |
| no through-line | black-and-white removed the vermilion jersey, so the character had no colour anchor and stopped being recognisable frame to frame |
| creepy | the medium. Masereel is German expressionist dread; dense masses of identical carved faces read as a tribunal, not a crowd |

The root cause was register purity. I argued this film's voice was
reveal-a-mechanism rather than litigate-a-rule, and then **banned comedy in
code** — the woodcut board carries a literal `BANNED` regex rejecting ABSURD
and COLOSSAL as "the comedian's instrument". Isaac's favourite film and the
channel's fastest-starting short both came from that instrument. Never
engineer out the thing that is working on a theory about voice.

**Why the Jones idiom is structurally right, not just warmer.** Wile E. Coyote
IS Goliath — better equipped, better funded, technically superior, universally
resented, while the small fast one is loved for nothing but being small and
fast. Jones animated this exact asymmetry for twenty years. And the idiom
solves the two demands the woodcut strained at:

- **The look to camera** is native. The deadpan glance at the audience is the
  best implicate-the-viewer device in animation, and the k4 probe — a
  dignified champion holding your eye while the crowd cheers for somebody
  else behind him — is the whole film in one image, funny and sad at once.
- **The take.** Jones's craft is the smallest movement carrying the biggest
  read, so a crowd turning sour lands as comedy rather than menace.

Rejected worlds, with reasons, across all three rounds: **attic vase** cannot
hold an expression (silhouette gave a magnificent Zeus where the film needs a
tired man); **stained glass** sanctifies everyone including the crowd;
**ukiyo-e** reads as a festival and carried red seal-marks; **ISOTYPE** cannot
carry emotion (its champion is a featureless blob) but donated a device;
**woodcut** won round 2 on the register probes and lost on screen; **1950s
sports litho** was the round-1 winner and is the near-miss this world
supersedes — same era, but flat cel animation draws a funnier character than a
poster does.

Ninth distinct world in nine films.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted background shapes with stylised
> ANGULAR GEOMETRY and exaggerated theatrical perspective, characters painted
> as flat cels with confident tapering ink outlines and no interior shading.
> The palette is warm and graphic: dusty ORANGE and terracotta, INK BLUE,
> mustard GOLD, sage GREEN, cream and flat VERMILION RED accents. Crowds are
> painted as ranked rows of simplified flat graphic shapes rather than rendered
> faces. Visible painted gouache texture and slight brush grain in the
> background washes. Expressions are BOLD and readable at a glance. Flat matte
> throughout: NO gradients, NO airbrushed shading, NO photographic texture, NO
> three-dimensional rendering, NO modern digital gloss. This is an ORIGINAL
> character and an original scene in a general mid-century cartoon idiom: NO
> existing cartoon characters, NO studio logos, NO trade dress, NO recognisable
> franchise designs of any kind. There is NO text, NO lettering, NO numbers, NO
> signage copy and NO writing of any kind anywhere in the image; any sign or
> board that appears is completely BLANK. This is ONE SINGLE COHERENT SCENE,
> NOT a grid, NOT a model sheet, NOT a sheet of studies. 16:9, edge to edge,
> one scene, one camera.

**Both guardrails held on all five probes** — no franchise designs, and no
lettering anywhere including on the blank sign, which was this idiom's main
risk (its reflex is to letter everything).

## The champion needs one correction

He drifted toward a generic square-jawed superhero. The register wanted is
Wile E.: **meticulous, wry, over-prepared, faintly vain** — dignity from
precision, not from heroic build. Boards state that at point of use.

## TYPOGRAPHY — the first film to carry any

Generated lettering stays forbidden forever; the model cannot spell and a hex
code once came back drawn into a frame as a string. But COMPOSITED type, added
by us after the gate, is new here and deliberate:

1. **A title card** in the world's idiom (Futura, flat terracotta).
2. **Source cards** naming the two studies as they are cited — the provenance
   discipline made visible, and something the pause-and-screenshot viewer can
   actually use.
3. **The scoreboard runner** — his numbers climbing while the crowd's
   enthusiasm falls, same composition each time. This is the comedy ladder and
   it REQUIRES numerals: the generated frame keeps a blank board and we paint
   the numbers on.

Ruled out: burned-in captions, kicker words, chapter titles, emphasis text.
Those convert a fable into an explainer.

**ORDER IS LOAD-BEARING: generate -> gate -> typeset -> assemble.** The gate
must never see our own type, or the glyph check stops meaning anything about
GENERATED text. `tools/video/typeset-cards.py` stashes pristine frames in
`production/pristine/` before compositing, so the gate can always be re-run
against the untouched art.

## The gate needs THESE numbers

This world is POLYCHROME and heavily saturated — chroma runs 62 to 78 percent
of frame, and the worst 15-degree bucket reaches 55 percent. The census is
therefore DISABLED here (`hue_census_max: 100.00`), which is the opposite of
the woodcut world where it was the primary check. The census follows the
world's claim, not a house default.

The paper here is warm cream and terracotta, more saturated than any paper
world, so the mask needs its override: measured s 11.8–25.0, v 61–96, hue
38–82 with sage-green background elements pushing p95 to 110.

```assertions
mask_sat_max: 28.0
mask_val_min: 58.0
ground_hue: [28.0, 120.0]
ground_sat: [5.0, 34.0]
ground_val: [55.0, 100.0]
ground_min_paper: 0.005
letterbox_max_rows: 4
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
accent_hue: [0.0, 20.0]
hue_census_max: 100.00
glyph_min_conf: 78.0
```

`ground_min_paper` is 0.005 because k3 dropped to 1% bare ground — a packed
arena legitimately leaves almost none.

**What the gate cannot see, stated out loud:** whether the character is
recognisably the same person, whether the crowd is looking the right way, and
whether anything is funny. Those are the board's quotas and QC by eye. A green
gate on 104 frames is not coverage of any of them — the woodcut film passed
104/104 and was still rejected.

**Never inherit a WORLD.md across worlds.** Written fresh for this film.
