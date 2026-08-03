# Brief for Antigravity — generate a GALLEY film's frames with your built-in image generator

You are producing the **frame set** for a kernel.chat film in the repo
`~/blog design`. Everything else in the pipeline already exists and works. Your
job replaces exactly one step: the frames, which are normally generated against
fal.ai by `videos/<film>/production/generate-frames.mjs`, are instead generated
by **your own built-in image generator**.

Do not run `generate-frames.mjs`. Do not call fal, WaveSpeed, or any paid API.
Do not touch narration, assembly, rendering, or publishing — those chairs are
downstream of you and are not yours.

---

## The pipeline, so you know where you sit

```
script.txt
  → build-beats.py          syllable-timed beat map
  → STORYBOARD.md           one image per beat, tagged to its narration line
  → build-prompts.py        storyboard → production/prompts.json     ← YOU START HERE
  → [frames]                                                        ← YOUR JOB
  → colour-field.py         per-act tint
  → narrate.mjs             ElevenLabs, writes audio/words.json
  → conform-beats.py        beats conformed to measured audio
  → build-composition.mjs   HyperFrames composition
  → render → shorts → publish
```

You read `production/prompts.json` and you write PNGs into
`videos/<film>/public/images/frames/<id>.png`. One file per key in prompts.json,
named exactly by its key. That is the whole contract.

---

## What prompts.json gives you

A flat object: `{ "<frame-id>": "<full prompt string>", ... }`. Each value is
already a complete prompt — scene description first, then the house style block.
**Use it verbatim.** It was built by `tools/video/build-prompts.py` and encodes
fixes that cost real money to learn. Do not paraphrase, shorten, or "improve" it.

If you believe a prompt is wrong, fix it in `build-prompts.py` and regenerate
prompts.json. Never hand-edit a single prompt in isolation — the next run will
silently revert it.

---

## Reference conditioning — read this before your first image

**If your image generator accepts reference/input images, use both plates:**

- `production/refs/castplate.png` — the character sheet. Teaches construction
  and palette.
- A **layout plate** — teaches geometry only.

**A reference image is a prior on EVERYTHING it contains.** This is the single
most expensive lesson in this project and it has been relearned three times:

1. A previous film's frame showing a corridor of framed portraits was used as a
   "neutral" layout reference. It put its corridor into an unrelated frame.
2. A frame that *looked* plain was actually a dial, a stepladder and a cyan
   robot. Conditioning on it dropped gratuitous dials and ladders into a quarter
   of the film — including beats that never mention either. **37 frames, $1.44,
   regenerated.**
3. Conditioning on the character sheet alone made the model draw boxed panels on
   a cream field, because that is what a character sheet looks like.

So the layout plate must be **scenically empty**, not merely plain: flat cream to
all four edges, one horizon line, one small figure, nothing else. If the film has
no such plate, **build one first** and generate nothing until it exists.

**If your generator does NOT accept reference images**, say so before you start.
Text-only conditioning drifts much harder — the character will not hold across
120 frames on description alone. In that case the canonical description at point
of use (below) is doing all the work, and the contact-sheet check at the end is
mandatory rather than advisory.

---

## The five rules that produce usable frames

**1. Describe the character at the point of use, and state counts.**
A reference sheet is not sufficient. Wherever the board names the character, the
full canonical description must be expanded inline, and every countable feature
must carry its number. From `build-prompts.py`:

> the person in the red jacket — a short round-headed adult, completely bald
> except for **EXACTLY TWO** short thin hairs sticking straight up from the crown
> of the head, small dot eyes with simple straight eyebrows, wearing a red zip
> jacket over a cream shirt, black trousers and cream shoes

"A few hairs" gives you a different head every frame. "Exactly two" holds.

**2. The style block may only contain what is true of EVERY frame.**
A previous run put the red jacket in the style block, and all 133 frames came
back with every researcher, parent and bystander dressed as the protagonist. If
it is not true of every frame, it belongs in the scene description.

**3. No text, ever, anywhere.** The style block says so at length. Image models
garble type; all lettering in a GALLEY film is set by the Editor. Watch for
ALL-CAPS motif names leaking through from the storyboard — the model reads them
as labels to draw. `build-prompts.py` already down-cases them; if you see
lettering in output, that is a bug to fix upstream, not to paint over.

**4. Every recurring object needs its own canonical plate.** A motif described
only in words drifts across frames — one film's dial was drawn eight different
ways. If the board names an object that appears in more than about three frames,
generate one canonical version of it first, approve it, and condition the rest on
it.

**5. You cannot patch a generated frame.** Generative editors redraw the whole
image and hand back a different one, often at lower resolution. There is no
"fix the hand, keep everything else". If a frame is wrong, regenerate it whole,
from the same prompt, with the same references.

---

## Resolution — measure the artifact, not the preview

Gemini-class generators show a downscaled image in-page (~1024px) while the
actual downloadable file is much larger (2752px was measured). A previous session
measured the preview, concluded the film had to drop to 720p, and was wrong.

**Measure the file on disk**, e.g. `magick identify -format '%wx%h' <file>`.

Also audit the frame edge: generated 16:9 images often contain a smaller painted
panel inside a larger canvas, with dead margin around it. Check with
`magick <file> -format '%@' info:` (the trim bounding box) before assembly, and
normalise toward the painted panel rather than the full canvas.

---

## How to work

1. **Read** `videos/<film>/STORYBOARD.md` and `production/prompts.json`.
   Report the frame count back before generating anything.
2. **Confirm the plates exist** and are correct. Build the empty layout plate if
   it does not exist.
3. **Generate three frames first** — one dialogue, one wide, one detail. Stop.
   Show them. Do not proceed on your own judgement.
4. **Then generate in batches**, writing each PNG as you go so a crash loses
   nothing. Re-running must skip files that already exist.
5. **Contact-sheet the whole film before declaring done:**
   ```
   magick montage 'videos/<film>/public/images/frames/*.png' \
     -tile 8x -geometry 200x113+2+2 /tmp/contact.png
   ```
   Look at it. Character drift, stray lettering, donated props and boxed panels
   are all obvious on a contact sheet and all invisible frame by frame.
6. **Report**: frames generated, frames skipped, anything you could not do, and
   your honest read of the contact sheet.

---

## Hard limits

- **No paid API calls.** Not fal, not WaveSpeed, not ElevenLabs. If you think you
  need one, stop and say so.
- **Do not publish anything.** Publishing is gated behind Isaac's approval and a
  cadence guard (`tools/publish/cadence.mjs`); it is not part of this job.
- **No emoji, in code or in any user-visible copy.**
- **Magazine vocabulary** in filenames and copy — issue, feature, spread, folio,
  colophon. Never dashboard, panel, card, widget, modal.
- If a rule here conflicts with something you find in the repo, the repo's
  `docs/video/PRODUCTION-PLAYBOOK.md` wins — it is the long-form record and this
  brief is a summary of it.

## Where the full reasoning lives

- `docs/video/PRODUCTION-PLAYBOOK.md` — sections 10.x are the hard-won rules,
  each written up with what it cost.
- `docs/design-language.md` — house palette and type.
- `.claude/agents/galley/` — the chairs and what each one owns.
