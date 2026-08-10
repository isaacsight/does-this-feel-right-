# You Happen to Life — style block

Locked 2026-07-31. Carries the house look from *You Are Not Finished* so the
channel reads as one publication, with one deliberate change: **the paper
colour moves per act.**

## The style block

Copy verbatim into the tail of every image prompt, swapping only the paper hex:

> Flat mid-century comic line art. Clean black outlines of even weight. Flat
> solid colour fills only — no halftone dots, no stipple, no gradients, no
> texture. Plain cream `#F4E8C8` background. No text, no labels, no lettering,
> no numbers of any kind. Fill the entire canvas edge to edge with the
> background colour — no border, no frame, no white margin, no inset panel.
> ONE single continuous scene from ONE camera — never a split panel, never a
> diptych, never side-by-side comparison boxes.

The style block is composed into every prompt by
`tools/video/build-prompts.py`, which reads `STORYBOARD.md` as the single
source of truth. It also **downcases ALL-CAPS motif names** before prompting:
the pilot returned frame 047c with the words "THE STRANGER" lettered into it,
because the board wrote the motif name in caps and the generator read that as
a label to draw.

## Paper per act — applied at ASSEMBLY, not generated

The School of Life shorts study found their frames carry a colour field that
shifts by section while ours held one cream across 122 frames. This is that
fix, applied at **act** granularity rather than per beat — per beat would be
frantic, and the acts are the film's real sections.

**The paper hex is a tint applied in the composition. It is never prompted.**
The 2026-07-31 pilot asked for five different paper colours by hex and got
cream back four times out of six. The cause is the playbook's own rule
(§10.9) arriving from a new direction: the layout reference is a finished
cream frame from the last film, and **a reference image is a prior on
everything it contains — including its background colour.** Instruction does
not beat reference, and no amount of prompt emphasis was going to win.

Tinting at assembly is also the more faithful copy of what the reference
channel actually does: their colour field covers the whole frame, characters
included, rather than only the paper behind them. It is deterministic, free,
and cannot drift across 116 frames.

| Act | Paper | Hex | Why |
|---|---|---|---|
| 1 — The claim | cream | `#F4E8C8` | the house paper; the film opens where the channel lives |
| 2 — It is a real thing | pale blue-grey | `#DCE4E2` | the research turns cooler and more clinical |
| 3 — The practice claim | pale ochre | `#EFDDB8` | warmer; back in the room with the assertion |
| 4 — The numbers | pale olive | `#E2E3CC` | coldest reading in the first half; this act is a table |
| 5 — Which way does it point | rose-grey | `#EADDD6` | the turn; warmth returns but it is not comfortable |
| 6 — Where it turns cruel | dim slate | `#D6D8D6` | the film's lowest light |
| 7 — What survives | cream | `#F4E8C8` | returns home, deliberately, on the opening paper |

**Everything except the background stays fixed across the change** — same ink,
same red jacket, same line weight. The paper hex is the only variable, and it
is stated explicitly in every prompt so the generator does not treat a colour
change as licence to restyle.

## Palette

| Role | Hex |
|---|---|
| Ink | `#1F1E1D` |
| Jacket | red, as reference |
| Companion | cyan, as reference |
| Accent (assembly only) | tomato `#E24E1B` |

## Geometry

**1920x1080, full bleed.** Sources arrive around 2752x1536 and are downscaled;
nothing is ever upscaled.

## The one motif

**THE DIAL** — a single round dial with one pointer, mounted on a plain plate.
Two ends, marked only by a small filled circle at one end and a small open
circle at the other. **No lettering, no numerals, no tick labels.** It is
introduced in Act 2, read in Act 5, and turned to face a stranger in Act 6.
It appears in no frame where it is not doing work, and nothing else recurs.

The dial is the film's argument in one object: there is only one of them, and
where you set it for yourself is where you have set it for everyone.

## Cast

**THE PERSON** — the house character, carried from the last two films. Bald
with two hair tufts, red jacket over a cream shirt, black trousers, cream
shoes, a cream satchel on a shoulder strap.

**THE SPEAKER** — the figure on the stage in Act 1. **Deliberately generic:**
plain dark jacket, headset microphone, no distinguishing features, most often
shot from behind or in flat silhouette against stage light. This film argues
with a widely held belief, not with a person, and the art direction has to
hold that line as firmly as the script does. No caricature, no likeness, no
recognisable individual.

**THE COMPANION** — the cyan cube robot, carried over. Flat cyan cube head
sitting directly on two thin straight legs, two thin straight arms coming
straight out of the cube, no torso, no joints, no antenna, no rivets, no
mouth, two round black dot eyes. Appears as researcher and statistician.

**THE STRANGER** — Act 6 only. Another ordinary figure in the house style,
drawn with exactly the same care and line weight as the person. Never shabby,
never a caricature of poverty, never pitiable. The point of Act 6 fails
completely if the stranger is drawn as a type.

## Construction notes carried forward

**Always supply a full-body reference of every character.** The companion took
three failed attempts on the last film because the reference showed it cropped
at chest height and the generator filled the missing body from generic robot
priors. Reference conditioning beats instruction.

**A reference image is a prior on everything it contains** — its cast, its
captions, its layout. Supply a layout reference alongside the character sheet,
and make sure neither carries lettering.

## Two things the generator reliably ignores

Audit for both on every batch; do not trust the prompt.

1. **Lettering.** It labels things anyway. Any frame with text in it is
   regenerated — all type in this film is added at assembly. This film is at
   higher risk than the last one because Act 4 is full of numbers; the numbers
   are **assembly type**, never drawn.
2. **Full bleed.** Frames arrive as a painted panel inset on a margin often
   enough to matter. Measure with `magick <f> -fuzz 4% -format "%@" info:`
   before assembly and normalise toward the panel, never by upscaling.
