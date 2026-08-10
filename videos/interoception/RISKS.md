# Generation risks — THE EXPLANATION ARRIVES SECOND

Ranked by expected cost. Risk 1 is the one that will actually bite.

---

## 1. The office is a text-generation trap — CRITICAL

**This is the highest risk in the episode and it comes from the brief itself.**

A detective office is, visually, a room made of writing: case files, labels,
a button marked "PROBABLY DANGER", an oversized stamp, papers, a noticeboard.
The previous film's single most expensive lesson was that **generated frames
render text when the scene concept implies a label**, and no amount of "no
lettering" in the style block prevents it. That film lost frames to SCREAM,
A/B, crash, WOBBLE, MENU, UP/DOWN, AHA!, *thud thud wobble* — and **CLATTER
survived into the final export.** The style block already carries a CRITICAL
no-lettering clause. It was not enough, twice.

The brief asks for a stamp, files, and a labelled button. Built literally, this
episode would fail on more frames than the last one did.

**The fix — a wordless evidence language.** Every piece of "information" in the
office is a shape, a colour, or a posture. Nothing is ever written:

| Brief says | Build instead |
|---|---|
| A button labelled "PROBABLY DANGER" | A single oversized red mushroom button. Unlabelled. The Detective's hand already on it |
| A stamp reading ROMANCE / DANGER / READY | The stamp leaves **a plain red blot**. The verdict is communicated by *cutting to the hero's face*, never by the mark |
| Case files, evidence documents | **Blank** red folders. One small **blank** red index card. Nothing written on anything |
| A noticeboard of clues | Removed. Empty walls. The emptiness is funnier and safer |
| The three conclusions | Carried entirely by the hero's expression in the cutaway, plus the room they're standing in |

This is not a compromise. Wordless is the stronger version: a Detective
delivering an absolute verdict off **one blank card** is a better joke than one
holding a card that explains itself, and it forces the comedy into posture,
which is where this show's comedy lives anyway.

**Enforcement:** every office frame gets validated at 100% zoom before the batch
continues, and any frame with a glyph in it is reshot with the text-bearing
object removed from the scene text — not with a stronger prohibition, which
does not work.

---

## 2. Anchor drift across the three rooms — HIGH

The film's central claim is *identical body, different room*. If the red heart
changes size, shape or position between i08, i09 and i10, the claim is silently
refuted on screen and the film stops working.

Reference-conditioning holds the *character* well; it does not reliably hold a
*prop deformation* like a heart distending fabric.

**Mitigation:** generate the three as one batch with near-identical scene text —
change only the room clause, keep the body clause byte-identical. Review the
three side by side at full size before generating anything else in Act II. If
one drifts, reshoot all three rather than patching one, so they stay a set.

---

## 3. The Detective must not look like the hero — MEDIUM-HIGH

Both are stick figures with round heads in the same universe, and the hero is
the reference image. The reference-conditioning that keeps the hero consistent
will actively push the Detective toward looking like him.

**Mitigation:** differentiate on silhouette, not face — the Detective is
consistently seated or coated, always in the beige office, never with the red
heart. Consider generating the Detective's establishing frame first and adding
it as a second reference image for subsequent office frames. Budget one
validation frame for this before committing to the office batch.

---

## 4. The office as a location will drift — MEDIUM

i20, i33, i35 and i52 must read as the same room across four points in the
film, including a wide peak and a dark reset. Rooms drift more than characters
do — the last film held one flat, one office and one café, and the office
wandered.

**Mitigation:** fix the room in a single reusable clause (wall colour, desk
shape, slot in the wall, camera height) and paste it verbatim into all four.
Never re-describe it in different words.

---

## 5. The peak frame is the hardest single image — MEDIUM

i33 asks for: the hero, the Detective, two clerks, a room that is
simultaneously an office and the hero's head, and a legible read at a glance.
That is a crowded composition, which the brief explicitly warns against.

**Mitigation:** budget two or three attempts and accept a simpler staging.
Fallback: drop the clerks from the peak frame, keep only hero + Detective +
one red card. If it still doesn't read, split into two frames — the film
survives that; an unreadable peak it does not.

---

## 6. Holds over the ceiling — MEDIUM, entirely preventable

The last film shipped v03 at 11.6s, v41 at 10.1s, w02 at 9.9s, and two at 8.0s,
because seven closing lines had no frame and the placement pass stretched
neighbours to cover the gap.

**Mitigation:** run the coverage audit *before* export, not after — every
narration line must have a matched frame, and any hold over 8.0s fails the
build. `place-v5.py` in the polyvagal directory already does the placement;
add the assertion.

---

## 7. Lower-probability items

- **The 1962 figures** (i36–i39) introduce two non-hero characters. Keep them
  as plain, low-detail figures and never show their faces in close-up.
- **Hands.** i31 asks for blurred multiple hands; generators handle hands badly
  and this frame asks for many. Accept whatever comes back if it reads as
  shaking; do not chase it.
- **The empty office** (i35) may come back with a figure in it anyway.
  Emptiness is a common generation failure. Budget a reshoot.
- **Cost.** The last film cost $18.72 across three builds. A single clean build
  of ~52 frames plus validation and reshoots should land near **$6–8**. No
  paid generation without explicit approval.
