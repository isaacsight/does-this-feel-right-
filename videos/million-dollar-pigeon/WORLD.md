# WORLD — The Million-Dollar Pigeon

Third episode in the recurring mid-century painted world. **Not re-tested from
scratch, and that is the point:** four episodes in four worlds is an anthology;
a recurring world is a show. What the six concept probes settled was not the
look but whether THIS SUBJECT stages in it. It does, on all six.

## The rule this episode is built on

> Every frame has a HUMAN side that means everything and a BIRD side that means
> nothing, and wherever possible both are in the same picture.

The auctioneer's eyes bulge while the hen preens. The fancier weeps at a sky
containing one dot that is thinking about its wife. The comedy is the gap, so
the staging must show both halves — never cut away to the reaction.

The one exception is the Cher Ami act, which is played entirely straight. The
probe proved the world can carry gravity: mud, smoke, cupped hands, no gag.
Three episodes of jokes had never tested that, and it is now the reason this
subject can hold eight acts.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted
> cel figures with confident tapering ink outlines and no interior shading, in
> a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE,
> cream and flat VERMILION RED, each scene keying its own dominant colour from
> that set. Expressions are BOLD, exaggerated and readable at a glance. Visible
> gouache texture, flat matte, NO gradients, NO airbrushed shading, NO
> photographic texture, NO three-dimensional rendering.

Plus the standing laws: no text of any kind, blank signs, no franchise designs
and no likeness of any real person, one coherent scene, 16:9.

## Three things the probes taught, before any batch money is spent

**1. Sign-shaped objects attract lettering.** The first auction probe put the
word "THE HEN" on the plinth, straight through a clause forbidding all text.
The fix was not a stronger prohibition — it was removing the plinth. A label,
a placard, a nameplate and a scoreboard are all invitations. Where the staging
wants one, use a bare cushion, a smooth paddle, a blank board.

**2. "Spiral" is a shape word and shapes come back decorative.** The first
liberation probe produced a tidy wreath of birds. Describing the FORCE and the
direction of travel instead — blasting out, climbing steeply, off the top edge,
nearest ones large and furthest tiny — produced the image the act needs.

**3. The cast clause loses, again.** The horse-lab probe asked for one official
and returned a lab packed with onlookers, despite "ONLY the people described
above appear in this image". A laboratory is a place that contains people, and
the model draws what a place contains. This is the fourth instance of the same
failure across two episodes, and text has never once won it.

**Therefore `production/cast.json` ships with the FIRST batch on this film,**
not after a rejected cut. `generate-frames.mjs` withholds the character sheet
from every frame whose scene names no character. Omission, not negation.

## The plates

`castplate.png` — the three characters on an empty cream field and NOTHING
else: no loft, no rooftop, no sky, no props. The fancier is drawn mid-
expression, eyes wide and mouth open, because a plate's expressions are a prior
too and a neutral plate produced eight minutes of neutral faces on the queue
episode.

`layout-plate.png` — generated locally with ImageMagick as a flat cream field
with a faint even grain, because the model would not return a picture of
nothing and a picture of nothing is exactly the requirement. A plate that
contains props donates them to a quarter of the film.

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

Inherited from the queue episode with `ground_hue` already at the widened
[25, 95] — the band that was corrected after it twice rejected a legitimate
sage-green frame, sage green being one of the world's own six colours. The
lesson carried forward rather than relearned: **a band must cover what the
world DECLARES, not what the first frames happened to contain.**

`vertical_max_width` stays at 4. This idiom is built from vertical rectangles —
loft slats, chimney stacks, lab shelving, club windows — and the house default
of 24 quarantines architecture.

**What the gate cannot see** and what QC by eye must: whether both halves of
the two-sided frame are present, whether the Cher Ami act stayed serious, and
whether the fancier is someone the audience wants to spend eight minutes with.
A green gate is not evidence the episode holds.
