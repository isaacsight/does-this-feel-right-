# STATUS — Batman effect

**Register: PROVEN.** 17 frames generated, 0 failures, $2.55. The peak-catastrophe
approach from `../memory-reconsolidation/COMEDY-REGISTER.md` works — accordion
commuter piles, the seat cartwheeling mid-air, the escalator queue erupting while
the tourist stands calmly. Isaac approved the look.

## Done
- `SCRIPT.md` — locked at **7:46**, source verified (npj Mental Health Research
  vol. 4, DOI 10.1038/s44184-025-00171-5). Do NOT trim to the old "4–5 min" header.
- `audio/narration.mp3` — 7:46, Chris @ 0.75, approved
- `frames.mjs` / `batch.mjs` — working, register block inline
- `frames-canonical/` — 17 frames (b01–b17), Scenes 1–4

## Blocking before publish: two IP frames

**b03 renders DC's Batman** — full cowl, ears, cape, as the character.
**b16 renders three Spider-Man costumes** — webbing, mask, eyes.

Both came from *describing appearance*. This is the naming trap in a third
variant: naming a labelled object produced letters; naming a character in the
style block populated an empty room; describing a costume's distinguishing
features produced the trademarked costume.

**Fix — describe function, never appearance:**

| Never write | Write instead |
|---|---|
| "pointed cowl", "cape", "bat" | "a tall still figure whose head-shape rises to two sharp points, in a long dark coat that reaches the floor" |
| "red-and-blue patterned bodysuit" | "three identical figures in matching plain gym clothes, arguing" |
| any hero's name or emblem | the shape's behaviour — what it is *doing*, not what it looks like |

Add to every prompt: *"No existing comic-book, film or franchise character. No
recognisable costume, emblem, mask design or logo of any kind."*

Reshoot b03 and b16 with that language before the remaining ~60 frames.

## Remaining
~60 frames for Scenes 5–6 and the ending (7:46 at 6s mean ≈ 78 total, ~$9 more).
Then audit at 100%, placement, assemble in Palmier, captions, shorts, delivery.

## Spend
$2.55 this film. **$14.10 across both films today.**
Server running at `FAL_DAILY_SPEND_LIMIT=25` — reset to 10 when done.

---

# SESSION END — 2026-07-26

## Running right now
`batch.mjs` is re-rendering all 76 frames with the **CLEAN** composition block.
Check: `tail -1 /tmp/bat10.log` and `ls frames-canonical | wc -l`.
Pre-CLEAN originals are safe in `frames-v1-backup/`.

**Server limit raised to $40** (`FAL_DAILY_SPEND_LIMIT=40`). **Reset it to 10
when the film is done.**

## The quality fix, and why it works

Isaac's note was "AI slop, loose continuity". Cause: his own template asked for
**one dominant gag plus one smaller callback** — two events. My scene text
routinely described five. The model rendered all five faithfully, which reads as
clutter no matter how well drawn.

`CLEAN` is now appended to every prompt: exactly two things happen, most of the
frame is empty, generous negative space, fewer objects larger. Proven on b43/b44/
b50 — dramatically cleaner.

**Partial fix.** The block constrains composition but the scene *text* still
names five elements in many frames. Full fix = rewrite each scene down to
gag + callback in `frames.mjs`. Do that next.

## Three bugs fixed this session, all silent failures

1. **Act filter** — frames authored later had no `act`; `undefined >= 1` is false,
   so 22 were dropped from the queue with **no error** and a plausible "done".
2. **Done-map counted failures** — error entries carry an `id` and no `url`;
   treating them as complete skipped 72 frames and reported success on an empty
   queue.
3. **Spend double-counting** — passing `SPENT_TODAY` on top of a log total that
   already includes today inflated the figure and throttled the run. The
   **server** is the only reliable spend guard; let it enforce and pass 0.

## Still outstanding

- **Narration fades 11.3 dB** across the runtime (−25.3 dB at 0s → −36.6 dB at
  315s). Cause: all 891 words in one ElevenLabs request. Fix: generate per scene,
  loudness-normalise each chunk, concatenate. No fal spend.
- **Simplify scene text** to gag + callback, then re-render.
- **Full-resolution audit** — only ~20 of 76 have ever been individually
  inspected. This gap is what produced the slop.
- Then: re-place with `place.py`, re-encode, Palmier master, captions, shorts.

## Assets
`narration-fast.mp3` (speed 1.0, 7:01) is the approved take — already copied to
`narration.mp3`. Also on disk: 0.75 (7:46) and 1.2 (4:40).
`renders/batman-effect-v3.mp4` is the current cut, pre-CLEAN frames.
