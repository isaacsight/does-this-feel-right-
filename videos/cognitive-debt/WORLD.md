# WORLD — the ledger

Tested and locked 2026-08-04, 21 images, ~$0.82. This is the validated world
clause; the Art Director ratifies it and owns the FRAME-BOOK, but it does not
need to rediscover any of what is below.

## Why this world

The last three films — *You Are Not Finished*, *You Happen to Life*, *You
Watched It Happen* — are the **same world**, and the last two have byte-identical
style blocks: flat mid-century comic, cream `#F4E8C8`, ink `#1F1E1D`. Three
consecutive films in one world is the catalogue risk the Art Director's chair
now guards against, arriving before the guard existed.

The ledger was chosen over three alternatives on the strength of the idea, not
just the break: *cognitive debt* is an accounting phrase, and ruled accounting
paper is the surface thinking used to happen on. In a film about essay-writing
and what gets outsourced, every frame sits on the thing being replaced.

The wide compositions are the argument for it. On a ruled ground, an empty
frame reads as **paper** rather than as void — emptiness gets structure for
free, which the cream world never gave us.

## The locked clause

> a LEDGER world: the whole background is pale sage-grey accounting paper, the
> SAME pale sage-grey across the whole frame with no warm or brown tint anywhere
> and no change of paper colour toward the foreground, with faint evenly spaced
> pale horizontal rules running edge to edge across the entire field, including
> behind and below every object. Near-black linework. One warm tomato-red accent.
> The rules are plain blank lines and carry NO writing, NO numbers and NO marks
> of any kind. There is NO vertical line anywhere in the image: no margin rule,
> no red vertical stripe, no vertical division of any kind. The rules are
> horizontal only.

Plus the house common block (flat fills, no gradients, no text, edge to edge,
one scene one camera, 16:9).

## The three things that had to be tested, and what they cost

**1. The ground drifts warm unless it is locked.** A close-up came back on warm
tan while wides on the identical world clause held sage-grey. The doubled
phrasing above — naming the colour, then forbidding the drift explicitly — held
sage across **all six** frames of the final test. Do not shorten it.

**2. The margin rule is FORBIDDEN, and this was not the obvious answer.** A thin
red vertical margin rule appeared *unbidden* in one frame of three. It is
genuinely handsome — it makes the frame read as a real ledger page rather than
generic ruled paper — so the test was specified-always versus forbidden-always,
three compositions each.

Specified put the rule in all three, and **could not place it consistently**:
full height in one, stopping at the horizon in another, terminating mid-frame in
the third. Across 120 frames an inconsistent structural line reads as sloppiness,
not as design. Forbidden came back clean in all three, every time.

A good accent the model cannot place reliably is worse than no accent. Losing it
is a real loss; keeping it was not on offer.

**3. Two-figure scenes are fine.** The first attempt returned "the model did not
generate the expected output for this prompt" with no image, which looked like a
limit and would have killed the world — most of this film has more than one
person in frame. Three retest variants all generated. **It was transient.** Two
unexplained refusals happened today across ~20 calls; treat a single refusal as
noise and retest before drawing a conclusion from it.

## Plates

- `production/refs/castplate.png` — single character, three views, ledger-native.
  **Single character on purpose**: the first world test used another film's CAST
  sheet and it donated its adjacent pair into a scene that asked for one person
  alone (PLAYBOOK 10.8, again).
- `production/refs/layout-plate.png` — the wide frame: ruled ground to all four
  edges, one horizon line, one small figure, nothing else to donate.

Both are gitignored, as all plates are. Regenerate from
`docs/video/PRODUCTION-PLAYBOOK.md` 10.28 if lost: repaint the castplate into the
world first, then condition everything on that.

## Two traps found while locking this

**Never put a hex code in a prompt.** `#D9E2DA` came back *drawn into the frame*
as the string `D9EE13D`. A hex is a label, and the model draws labels — the same
trap as naming a concrete example object in a style block. Colours are named in
words here for that reason.

**The character is spine; the world varies.** The protagonist carries across
films exactly as the narrator's voice does — it is what makes four films a body
of work rather than four uploads, and YouTube's own stated want is content where
"we know what channel it comes from." Supporting cast varies per film and is
governed per frame. Medium — flat fills, even outlines — does not vary: it is
the tuned surface the character consistency depends on.
