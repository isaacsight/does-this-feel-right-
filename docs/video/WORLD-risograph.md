# WORLD — risograph two-ink print

Drafted 2026-08-04 for the film after *Cognitive Debt*. **Not yet tested** — the
clause below is a proposal, and nothing is locked until it has survived a world
test (the ledger world took 21 images and ~$0.82 to lock; see PLAYBOOK 10.33).

## Why this world

The last four films are flat vector comic — three on cream, one on ledger paper.
Same medium, same mark. Risograph keeps what works (bold, graphic, flat, cheap to
keep consistent) and changes the thing that has never changed: **the surface**.
Grain and misregistration instead of clean fills.

It is also honest about what the films are. Riso is a duplicator — a machine for
producing many copies of something quickly and slightly imperfectly. For a
publication that argues about machine-made work, the medium is the argument.

## The proposed clause

> a RISOGRAPH PRINT world: the whole image is printed in exactly TWO inks on
> uncoated off-white paper with visible paper tooth. Every filled area is a coarse
> visible halftone of round dots, never a smooth flat fill. The two ink layers are
> slightly MISREGISTERED — each layer offset a few millimetres down and to the
> right of the other in the SAME direction everywhere in the frame — so their
> edges do not line up and a narrow band of bare paper shows along one side of
> every shape. Where the two inks overlap they multiply into a single darker third
> colour. The ink is semi-transparent with uneven roller coverage, patchy density
> and occasional light streaking. No gradients, no soft shading, no glow, no
> drop shadows. Edges are slightly ragged from the screen.

Ink pair to be chosen with the topic — the two candidates are **fluorescent pink
+ blue** (the most recognisably riso, reads contemporary and slightly loud) and
**blue + fluorescent orange** (cooler, more editorial). Named in words, never as
a hex code: a hex in a prompt comes back *drawn into the frame* as a string
(PLAYBOOK 10.33).

## What has to be tested before this locks

1. **Does the misregistration hold its direction?** If the offset wanders frame to
   frame it reads as sloppiness rather than as print, which is exactly how the
   ledger world lost its margin rule — a good effect the model could not place
   consistently is worse than no effect.
2. **Does the halftone survive at 1920x1080?** Coarse dots that look right in the
   source may alias into moiré when the frame is downscaled, and worse when the
   push in `assemble.mjs` resamples it. Test a frame through the actual render
   path, not just as a still.
3. **Does the character survive the medium?** This is the real risk and the reason
   this film should probably be **cast-free and object-led**. The ledger WORLD.md
   states that flat fills and even outlines are the tuned surface the protagonist's
   consistency depends on; changing the surface fights that lock directly. A film
   of objects, diagrams and spaces has no consistency problem and lets the render
   go as far as it likes.

## The gate needs new numbers for this world

`tools/video/frame-gate.py` reads its assertions from the film's `WORLD.md`, and
almost every one of them assumes the ledger:

| check | why it breaks here |
|---|---|
| `ground_hue/sat/val` | paper is off-white, not pale sage — the whole band moves |
| `hue_census_max` | this world has **two** inks by definition, so a second chromatic bucket is correct, not a fault. The census has to allow the second ink and still catch a *third* |
| `vertical_min_vcov` | misregistration puts a narrow ink band along one edge of every shape; a full-height object could read as a margin rule |
| `letterbox_max_rows` | unchanged, still valid |
| `glyph` | unchanged, still valid |

Do not copy the ledger assertions across. Measure them from the world test, the
way the ledger's were measured from its 88 frames, and tune for **zero false
positives on frames that are actually right** (PLAYBOOK 10.37).

## Traps carried forward

- **No hex codes in prompts.** Colours in words.
- **Never name a glyph, even to forbid it** (PLAYBOOK 10.38).
- **No pure white** unless the paper itself is the white — state which.
- The layout plate must be scenically EMPTY, and the world test must include at
  least one close-up: the ledger's ground drifted warm on close-ups while wides
  held, and only the doubled phrasing caught it.
