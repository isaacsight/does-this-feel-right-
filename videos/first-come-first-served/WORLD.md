# WORLD — the painted world, v3

Rewritten 2026-08-07 after the second-medium world was abandoned. The previous
version of this file is in git history; the two probe scripts that built it are
still on disk (`world-test-2.mjs`, `world-test-3.mjs`) because the reasoning in
their headers is worth keeping even though the conclusion was wrong.

## What was abandoned, and why

Rounds 1–3 cost $0.98 and produced a world in which the queue stays calm flat
gouache and the man's interior arrives as a **second material** — raw scratched
ink and charcoal sitting on top of the paint, touching nothing. On five probes
it looked genuinely good. At 102 frames it failed, twice, for two different
reasons:

1. **Architecturally** — the mark language lived in the clause appended to every
   prompt and was switched off per frame with "no scratched marks anywhere". You
   cannot negate a concept you introduce in the same prompt. Fixed in v2 by
   splitting the clause. That fix worked.
2. **For a viewer** — and this is the one that killed it. The response to the
   assembled cut was *"i dont understand the squiggly lines."* The device was
   conceptually neat, it survived every gate, and it communicated nothing. No
   assertion in the gate could ever have caught that, because the gate can only
   measure whether the marks are THERE.

The world is now the painted half alone. No marks, no second material, no
mention of ink or charcoal anywhere in any prompt.

## The rule the episode is actually built on

> Paint what is SAID, as a physical event, pushed past realism, with a specific
> face doing a specific thing, somewhere new, with somebody else in the frame.

Exaggerated and literal *at the same time*. Temperature becomes a bursting
thermometer; arithmetic becomes a chalkboard of frantic sums hovering over his
head; "it has no police force" becomes a policeman asleep with his boots on the
desk. That is what lets a viewer connect the voice to the picture — and it is
the register of the two episodes that landed, which I had twice reasoned my way
out of (see the header of `board.py`).

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted cel
> figures with confident tapering ink outlines and no interior shading, in a warm
> graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, cream and
> flat VERMILION RED, each scene keying its own dominant colour from that set.
> Expressions are BOLD, exaggerated and readable at a glance, in the tradition of
> classic theatrical cartoon animation. Visible gouache texture, flat matte, NO
> gradients, NO airbrushed shading, NO photographic texture, NO three-dimensional
> rendering.

Plus the standing laws: no text of any kind, blank signs, no franchise designs,
one coherent scene, 16:9.

**"Everyone is calm, composed and perfectly ordinary" is deleted from the
clause.** It was there to make the scratched marks legible by contrast, and with
the marks gone it is simply an instruction to drain the faces — which is the
single largest cause of the rejected cut. It is replaced by the expression line
above.

## What the board enforces, and what each number is for

Measured on the rejected v2 board against v3:

| quota | v2 | v3 | why |
|---|---|---|---|
| frames naming a face action | **0** | 71 | the fault the viewer named first |
| close-ups (CU + XCU) | 32% | 42% | a face cannot carry a beat at full-body distance |
| scenes containing a queue | 77% | 30% | v2 circled one shop for eight minutes |
| scenes with a physical event | — | 93% | a state is not a picture |
| other characters in frame | — | 85% | "interaction with different characters" |
| scenes saying "standing" | 55 | 8 | the literal wording of the complaint |

Two of those checks exist because of specific near-misses:

- The face check runs **twice** — once on the declared expression, once on the
  scene text the model actually receives. A frame can declare "mortified" and
  ship a prompt with no face in it; that gap is exactly how v2 got to zero.
- `"standing"` was in **47** scenes on the first v3 run, and 39 of those were the
  HERO block: *"EXACTLY TWO hairs standing from the crown."* A shared clause
  poisons every count that reads the prompt. It now says "sticking up".

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

Unchanged from v2, and all of them still apply — they describe the painted half,
which is the half that survived. Two are worth restating:

`ground_sat` has a floor of **zero**. A floor of 4.0 drawn from the tinted-cream
majority rejected a frame whose ground was legitimately near-white paper.

`ground_hue` was widened from **[30, 62] to [25, 95]** after the v3 batch, and
the reason matters more than the number. The band rejected b99 twice — a frame
in which the man's neck glows red hot and steam pours off him, one of the best
in the episode — because its wall is **sage green**, hue 80. Sage green is named
in the locked clause as one of the world's six colours, and the clause tells
each scene to key its own dominant colour from that set. So the assertion was
forbidding something the world explicitly permits. That is the third time on
this film that a band drawn from an early sample has rejected a legitimate frame
(`ground_sat`, `vertical_max_width`, now `ground_hue`), and the pattern is always
the same: **the band must cover what the world DECLARES, not what the first few
frames happened to contain.** Widening only ever admits; it re-gated the 97
delivered frames with no change.

`vertical_max_width` is **4**, down from the house default of 24. The margin-rule
check exists to catch an accidental drawn rule or a letterbox line, but this idiom
is built out of vertical rectangles — building edges, lamp posts, doorframes,
escalator rails — and seven frames were quarantined for having architecture in
them. Exempting seven frames would have been the wrong instrument; the next twenty
would fail the same way.

**What the gate still cannot see:** whether the frame is FUNNY, whether the face
is doing anything, or whether the picture matches the sentence. Those live in the
board's quotas and in QC by eye. A green gate on 90 frames is not evidence the
episode holds — the second-medium world proved that at full length, twice.
