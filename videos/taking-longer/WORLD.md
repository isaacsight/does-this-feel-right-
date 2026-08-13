# WORLD — Why Everything Takes Longer Than You Think (episode 9)

Ninth episode in the recurring mid-century painted world. Direction locked
from the approved concept frame (2026-08-11, free AI Studio lane): the
plank mountain and the sufficient screwdriver.

## The direction: DEADPAN SCALE

> The gap between the plan and the thing is staged as SIZE.

Every act puts a small confident object against an enormous patient one:
ONE tiny screwdriver against a ceiling-high mountain of planks; ONE sheet
of paper against a half-built colossus; ONE folding table of committee
members against a corridor of archive boxes. Compositions squared and
formal, flat even light, the small thing held up brightly and the big
thing simply present. Faces composed mid-confidence — the planner's bright
morning face is this film's recurring expression, and it is never mocked.

**TIME PASSES WITHOUT NUMBERS** (no-text law makes clocks and calendars
impossible): the season out the window changes while the pose holds — the
same garage staging with snow, then blossom, then amber leaves through the
SAME window; the Man's beard question is settled as NO beard ever (canon);
instead ONE small potted plant on the workbench grows across frames
(sprout, then leggy, then spilling over the bench edge). The recurrence IS
the joke and the claim.

## The monument: THE PLANK MOUNTAIN

The ceiling-high stack of flat planks and closed boxes in the cream
garage, drawn the SAME on every return: planks in warm wood tones, boxes
plain and closed, ONE completely BLANK white instruction sheet on the
floor, ONE small brass screw beside it. It shrinks across the film only
in the final act.

## The locked clause

> a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation
> idiom of the late 1950s: flat gouache-painted backgrounds and flat painted
> cel figures with confident tapering ink outlines and no interior shading, in
> a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE,
> cream and flat VERMILION RED, each scene keying its own dominant colour from
> that set. Expressions are BOLD, exaggerated and readable at a glance. Visible
> gouache texture, flat matte, NO gradients, NO airbrushed shading, NO
> photographic texture, NO three-dimensional rendering.

Plus standing laws: no text of any kind, blank sheets/plans/banners, no
franchise designs, no likeness of any real person — **Kahneman is NAMED in
narration but NEVER drawn; no committee figure may resemble him. No
architect is drawn.** The white-sailed opera house on its harbour may be
staged as a BUILDING (half-built: bare concrete ribs and scaffolds) — it
is a place, not a person.

## Environments (10 — garage frames <=22%)

1. the garage (monument; window with seasons; workbench plant)
2. the kitchen table (the estimate made, one paper, one pencil-shaped... NO
   pencil lettering — one plain stick)
3. the thesis desk (the 1994 act: one lamp, one stack of pages BLANK)
4. the observers' room (peers at a glass pane, watching the desk)
5. the harbour construction (white-ribbed shell, scaffolds, tiny figures)
6. the committee room (folding table, seven committee members, ONE silent
   expert at the end seat with a face that knows)
7. the archive corridor (shelf after shelf of closed boxes — the never-used
   book's home; also the iron-law act's data staging)
8. the tunnel mouth / runway (iron law: one vast bore, one tiny lantern)
9. void (flat cream, connective + data cards)
10. the garage at dusk, finished shelf (the ending)

## FREE-LANE PRODUCTION NOTES (first full film on AI Studio)

- ONE reference (castplate) per frame; layout plate CANNOT be attached
  (two images crash the Lite model). Castless void frames therefore get an
  in-prompt geometry sentence instead ("a single flat cream field, one low
  horizon line") — watch them at eye-QC; the occupants prior is the risk.
- System-instructions experiment before the batch: style clause + laws in
  the system field, plate pasted once per chat, one chat per act; 3-frame
  drift test gates the approach.
- Downloads are 1376x768 JPEG → convert to <id>-final.png on ingest;
  frame-gate.py + quarantine loop unchanged.

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

Inherited. Calibrate on a 5-frame free-lane round before the batch; the
Lite model's rounder line may shift the glyph/vertical behaviour — measure,
don't assume. Watch-items: scaffold frames may trip the vertical gate
(eyeball before re-rolling); the harbour shell must NOT letter itself.

**What the gate cannot see** and eye-QC must: the bright-confidence face
reading as hope not smugness; the seasons-window recurrence holding its
staging; the plant's three growth stages consistent; the silent expert's
knowing face staying COMPOSED; the Lite model's style staying inside the
gouache idiom across 100+ frames.
