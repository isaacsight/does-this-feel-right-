# WORLD — paper collage, six colours and gold

Proven by a 5-image test, $0.20, 2026-08-05. Bands below re-measured across the
finished 76 frames, not the test — a band from five images is a hypothesis.

## Why this world

From Isaac's mood board: torn and cut paper layered on cream stock, taped down,
with matte gold leaf accents. It is the fifth distinct world in six films, which is
the catalogue rule doing its job.

**The medium is the argument, which is why it was chosen for THIS film.** A memory
is not a recording played back; it is fragments reassembled, and the join does not
show. Every frame is visibly fragments reassembled. When the narration says a
rebuilt memory arrives smooth with no label on the invented parts, the picture is
already saying it.

## The locked clause

> a PAPER COLLAGE: the entire image is built from torn and cut pieces of paper
> layered on a warm cream paper ground, and every shape has a visibly TORN OR
> DECKLED EDGE with the white core of the paper showing along the tear. Pieces
> overlap and cast faint hard-edged paper shadows, and a few are held down with
> short strips of pale masking tape. The palette is strictly limited to VERMILION
> RED, deep COBALT BLUE, soft BLUSH PINK, MUSTARD YELLOW, dark FOREST GREEN,
> near-BLACK and the cream paper itself, plus small accents of flat MATTE GOLD
> LEAF. Surfaces carry real paper texture: some pieces show coarse halftone dot
> printing, some thick dry brushed paint, some plain flat pulp. Flat matte finish
> throughout: NO gradients, NO soft airbrushed shading, NO glow, NO metallic sheen
> on the gold, NO photographic texture, and no shadows other than the hard paper
> offsets. There is NO text, NO lettering, NO numbers and NO writing of any kind.
> This is ONE SINGLE COHERENT SCENE assembled from paper, NOT a mood board, NOT a
> grid of samples, NOT a sheet of unrelated swatches. 16:9, edge to edge.

Colours in words, never hex — a hex comes back drawn into the frame as a string.

## What the test settled

**It composes SCENES, not mood boards.** This was the risk that could have killed
the world: the reference is a board of unrelated fragments, and a film needs a
character doing a specific thing. The clause forbids the board explicitly, and the
test frames came back as single coherent scenes.

**The character survives as cut paper — better than in riso.** Torn edges carry an
expression well; the alarm close-up is the most expressive frame made in any world
so far.

**Gold reads as flat matte leaf**, no gradient, no chrome. This was expected to
fail and did not.

## The plates, and two failures worth keeping

**The layout plate is DRAWN, not generated.** Asked for "cream paper and one torn
ground strip", the model twice returned a row of coloured scraps — in a collage
world, "a torn strip" reads as an invitation to compose. A plate is a prior on
everything it contains (PLAYBOOK 10.9), so those scraps would have been donated
into all eighty frames. It is now made in ImageMagick from the world's own sampled
cream, with a fixed seed. Same ruling as the stair treads and the riso panel.

**The castplate is a PROVEN FRAME, not a turnaround sheet.** Three generated
character sheets failed: the first gave an empty hood, because a cream head was
specified against a cream ground and simply vanished — a feature described without
regard to what it sits against. The next two gave long branched hairs, despite the
prompt explicitly forbidding antlers, antennae and rabbit ears.

The fix was not a fourth prompt. The world-test frames, generated with NO castplate
at all, already had the character right — a full-body three-view turnaround is what
invites the elaboration. `castplate.png` is now the test's close-up frame, which
teaches construction, palette, face and tape, all correct.

In this world the two hairs read as short torn scraps on the crown rather than
distinct strands. That is the medium adapting the character, the same way riso
needed them thick and kinked, and it is accepted.

## The gate needs THESE numbers

**Re-measured across all 80 finished frames with the gate's own corrected mask**
(unsaturated AND bright), which is the only measurement that means anything —
the first pass used a different mask from the check and the two disagreed by
construction:

    hue  32.0 – 60.0      sat  1.8 – 14.9      val  82.0 – 96.5

Paper share falls as low as 1.7% of frame on the densest compositions. Bands are
set a little outside the observed range at each end, because a band drawn exactly
on the extremes fails the next frame that is one step further out — `b49` measured
val 82.0 against a floor of 82.0 and was rejected for sitting on its own boundary.

The hue ceiling is 64 rather than the 55 the first measurement suggested, because
that measurement sampled only BRIGHT unsaturated pixels while the gate sampled all
of them, including the near-black paper. The gate was fixed to match — paper is
unsaturated AND bright — and the band then had to cover the genuinely mustard-lit
grounds it had been hiding.

```assertions
ground_hue: [28.0, 64.0]
ground_sat: [0.0, 22.0]
ground_val: [78.0, 99.0]
ground_min_paper: 0.01
letterbox_max_rows: 4
vertical_min_vcov: 0.95
vertical_min_dev: 4.0
accent_hue: [0.0, 20.0]
hue_census_max: 100.00
glyph_min_conf: 78.0
```

**`hue_census_max: 100.00` disables the census, deliberately.** This world is
POLYCHROME by design — six colours plus gold — so a large second chromatic bucket
is correct, not a fault. The census is meaningless here and a foreign colour must
be caught by eye at QC. Say that out loud rather than letting 80/80 passing imply
coverage the gate does not have.

`accent_hue` is set to the vermilion band only so the opt-in accent-region check
still means something on frames that declare it; there is no single accent in this
world in the sense the ledger had one.

The riso file was copied here by mistake and judged the first batch against sage
paper and pink ink. It cost one frame. **Never inherit a WORLD.md across worlds.**
