# WORLD — the Bayeux embroidery

Proven by a 15-image three-world test (bayeux / tin / litho), $0.58, 2026-08-05.
Bands below are measured across the FIVE test probes only — a hypothesis until
re-measured across the finished batch.

## Why this world

**The medium is the argument twice over.** Tapestry is how wars get
mythologized — and this film's thesis is that the trophy IS the myth: the
bucket was loot canonized after Zappolino, not the cause of it. Every frame
stitches a petty object with the reverence of a saint's relic, which is
exactly the joke and exactly the history.

The rejected worlds, for the record: **tin** came back photographic (glossy
enamel, lamplight bokeh) against the flat-matte law and collapsed into one
tabletop composition; **litho** could only make monuments, not scenes, and
overlapped the Gillray print world shipped the same week.

Seventh distinct world in eight films.

## The locked clause

> a MEDIEVAL EMBROIDERED TAPESTRY in the manner of the Bayeux Tapestry:
> figures and objects stitched in coloured wool thread on coarse natural
> LINEN cloth, with visible individual stitches, laid-and-couched work in the
> solid areas and stem-stitch outlines. The palette is wool colours only:
> VERMILION RED, deep INDIGO BLUE, MUSTARD OCHRE, sage GREEN, walnut BROWN
> and the bare linen ground, with small accents of couched GOLD THREAD.
> Figures are stylised and slightly stiff like Romanesque embroidery, with
> expressive oversized hands and faces. A narrow decorative embroidered
> border of small beasts runs along the top and bottom edges. The linen weave
> is visible everywhere. Flat matte, NO photographic depth, NO gradients, NO
> digital smoothness. There is NO text, NO lettering, NO numbers and NO
> writing of any kind anywhere in the image. This is ONE SINGLE COHERENT
> SCENE, NOT a grid, NOT a sheet of studies. 16:9, edge to edge, one scene,
> one camera.

Colours in words, never hex.

## What the test settled

**The relic gag lands in thread.** The k4 bucket — pedestal, candles, two
kneeling guards, stitched rays — is the film's thesis in one frame.

**Expression survives embroidery** (the risk that mattered): the k3 outrage
close-up reads instantly — O mouth, splayed oversized hands. Romanesque
stiffness AMPLIFIES indignation rather than muting it.

**The beast border is a constant**, top and bottom, every probe. It is the
world's own frame and the film keeps it.

**The character stitches correctly**: both kinked hairs came through in
couched thread on all five probes; tunic reads vermilion wool.

## The plates

**castplate.png = the test's k2 full-body frame** (proven-frame method). It
teaches stitch construction, palette, the tunic, and both hairs against clean
linen.

**layout-plate.png is DRAWN**: ImageMagick flat measured linen (`#c1b5a0`,
hue 38 sat 17 val 76), deliberately WITHOUT the beast border — a drawn solid
band would teach solid bands where the world wants beast friezes; the clause
carries the border, the plate carries only the cloth.

## The gate needs THESE numbers

The linen is darker and more saturated than any paper world (val ~62–84,
sat ~8–34), so this world needs the per-world MASK override added for
gillray. Measured mid-band (rows 30–70%, avoiding the borders): hue 29–46,
sat 8–34, val 61–90. Dense compositions (the relic, the council) drop linen
share to 8–10% of the mid-band, lower of full frame.

**The beast borders occupy the top and bottom ~12% of every frame** — exactly
where the letterbox check looks. They are busy embroidery, not uniform bars,
and passed on all five probes; if a future frame's border stitches too evenly
and trips `letterbox_max_rows`, that is a per-frame `gate.json` exemption
with this paragraph as its justification — never a band change discovered
mid-batch.

```assertions
mask_sat_max: 36.0
mask_val_min: 58.0
ground_hue: [26.0, 50.0]
ground_sat: [6.0, 36.0]
ground_val: [58.0, 92.0]
ground_min_paper: 0.01
letterbox_max_rows: 4
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
accent_hue: [0.0, 20.0]
hue_census_max: 100.00
glyph_min_conf: 78.0
```

**`hue_census_max: 100.00` disables the census, deliberately** — six wool
colours make the world polychrome by design. A foreign colour is caught by
eye at QC, and the gate passing does not imply otherwise.

`accent_hue` is the vermilion band — his tunic is the constant.

**Never inherit a WORLD.md across worlds.** Written fresh for this film.
