# Brief for Antigravity — generate a GALLEY film's frames with your built-in image generator

> ## VERDICT, retested 2026-08-13: this works. It is now the primary free frame lane.
>
> The 2026-08-02 verdict ("hard-locked to 1024×1024 square, cannot produce film
> frames") is **stale and wrong**. Antigravity's generator now takes an aspect
> ratio and returns **1376×768 true 16:9**.
>
> Measured on episode 9 (`taking-longer`), frame b001: correct house style,
> blank signage, no lettering, character on-model — and it **passed
> `frame-gate.py` on the first roll** (1/1 pass, exit 0).
>
> It beats every other free lane because it is *filesystem-native*: it writes
> straight into the film tree, so there is no download-and-ingest dance, it can
> read `production/prompts.json` itself, and it batches 5–8 frames per turn.
>
> Paid fal (`tools/video/generate-frames.mjs`, $0.039/frame) remains the
> fallback for unattended runs that need automatic retries and a spend ledger.

You are producing the **frame set** for a kernel.chat film in the repo
`~/blog design`. Everything else in the pipeline already exists and works. Your
job replaces exactly one step: the frames.

Do not touch narration, assembly, or publishing — those are downstream chairs
and are not yours. Do not call fal, WaveSpeed, or ElevenLabs.

---

## The pipeline, so you know where you sit

```
CLAIMS.md → script.txt (writers' room)
  → register-profile.py --gate    address bands: you/we, contractions, sentence weight
  → slop-lint.py --gate           the humanity gate (law 15)
  → board.py                      → production/prompts.json    ← YOU START HERE
  → [frames]                                                   ← YOUR JOB
  → frame-gate.py                 per-frame acceptance          ← YOU RUN THIS
  → make-datacards.py             deterministic number cards (never generated)
  → narrate-acts.mjs              ElevenLabs → audio/words.json
  → map-shots.py                  → build/shots.json
  → assemble-stills.mjs           → build/<film>-master.mp4
  → cut-verticals.py → publish
```

**The contract:** you read `production/prompts.json` and write one PNG per key
into `videos/<film>/public/images/frames/<id>-final.png`.

Note the **`-final` suffix**. It is not optional — every downstream tool globs
for `*-final.png`. A file named `b001.png` is invisible to the pipeline.

---

## What prompts.json gives you

A flat object: `{ "<frame-id>": "<full prompt string>" }`. Each value is already
a complete prompt — scene description first, then the house style block.

**Use it verbatim.** It was written by `videos/<film>/board.py`, which enforces
roughly twenty gates (counts at point of use, flat-run detection, label
invitation, self-reference, camera quota, likeness law). Every clause encodes a
fix that cost real money.

If you believe a prompt is wrong, fix it in `board.py` and re-run that script —
it regenerates prompts.json and re-checks every gate. **Never hand-edit a single
prompt**; the next board run silently reverts it.

Data cards are deliberately **absent** from prompts.json. Numbers are drawn
deterministically by `make-datacards.py`. A model never draws data.

---

## Reference conditioning — read this before your first image

**Find the plate before you assume a path**; it moves between films:

```
find "videos/<film>/" -iname '*ref*' -o -iname '*plate*' | grep -i png
```

Some films reuse an earlier film's plate (episode 9 uses
`videos/stop-and-chat/production/refs/castplate.png`, per its `CAST.md`).
If the search returns nothing and CAST.md names no plate, **stop and say so.**
Generating 100+ frames unconditioned is a different job, not a degraded one.

**Attach the plate on EVERY frame, and re-attach it every turn.** Do not assume
a reference carried over from a previous message — long agent runs drift, and
the character will not hold across 116 frames on description alone.

**ONE reference image is the proven configuration.** (Two pasted plates
reliably crashed a sibling lane with "an internal error has occurred." If you
try two and get an error, that is the known failure mode — drop back to one.)

**A reference image is a prior on EVERYTHING it contains.** The most expensive
lesson in this project, relearned three times:

1. A corridor of framed portraits used as a "neutral" layout reference put its
   corridor into an unrelated frame.
2. A frame that *looked* plain was actually a dial, a stepladder and a cyan
   robot. Conditioning on it dropped dials and ladders into a quarter of the
   film — beats that never mention either. **37 frames, $1.44, regenerated.**
3. Conditioning on a character sheet alone made the model draw boxed panels on
   a cream field, because that is what a character sheet looks like.

If a film's plate carries a character who is **not** in this film, the prompts
say so explicitly. Honour that — never stage a figure the prompt doesn't name.

---

## The five rules that produce usable frames

**1. Describe the character at the point of use, and state counts.** The board
already expands the canonical description inline wherever it names the
character, with every countable feature numbered ("a single lonely PAIR of
hairs: one kinking left, one leaning right"). "A few hairs" gives a different
head every frame. *Known residual fault:* the model still often draws three or
four crown hairs. It is invisible at video scale — **do not burn re-rolls on
it.**

**2. The style block may only contain what is true of EVERY frame.** A previous
run put the protagonist's red jacket in the style block and all 133 frames came
back with every bystander dressed as the protagonist.

**3. No text, ever, anywhere.** All lettering in a GALLEY film is set by the
Editor. If lettering appears in output, it is a bug to fix upstream in board.py,
not to paint over.

**4. Every recurring object needs its own canonical treatment.** A motif
described only in words drifts — one film's dial was drawn eight different ways.
The board handles this by wording recurrences identically; preserve that.

**5. You cannot patch a generated frame.** Generative editors redraw the whole
image and hand back a different one, often smaller. There is no "fix the hand,
keep everything else." Regenerate whole, same prompt, same reference.

---

## Output handling — two mechanical steps that matter

**Normalize the file.** Output arrives as JPEG data wearing a `.png` extension.
Convert before anything downstream reads it:

```
magick "<file>" -strip PNG24:"<file>"
```

**Measure the artifact, not the preview.** Previews are downscaled; measure on
disk:

```
magick identify -format '%wx%h\n' "<file>"
```

Expect **1376×768**. Also audit the frame edge — generated 16:9 images sometimes
contain a smaller painted panel inside a larger canvas. Check the trim box with
`magick <file> -format '%@' info:` and normalise toward the painted panel.

---

## How to work

1. **Read** `production/prompts.json`. Report the frame count before generating.
2. **Confirm the plate** exists (see above).
3. **Generate ONE frame**, normalize it, measure it, and **run the gate**:
   ```
   /usr/bin/python3 tools/video/frame-gate.py videos/<film> --frame <id>
   ```
   Show the result. Do not proceed on your own judgement.
4. **Then batches of 5–8**, in key order, writing each file as you go so a crash
   loses nothing. Re-running must skip ids whose file already exists.
5. **Gate each batch.** If a frame fails the gate, report the id and move on —
   do not attempt to fix it yourself. Failures are re-rolled deliberately, and
   the failing attempt is kept as evidence in `production/quarantine/`.
6. **Contact-sheet before declaring done:**
   ```
   magick montage 'videos/<film>/public/images/frames/*-final.png' \
     -tile 8x -geometry 200x113+2+2 /tmp/contact.png
   ```
   Character drift, stray lettering, donated props and boxed panels are obvious
   on a contact sheet and invisible frame by frame.
7. **Report**: frames generated, frames skipped, gate failures by id, anything
   you could not do, and your honest read of the contact sheet.

---

## Hard limits

- **No paid API calls.** Not fal, not WaveSpeed, not ElevenLabs.
- **Do not publish anything.** Publishing is gated behind Isaac's explicit
  approval and a cadence guard (`tools/publish/cadence.mjs`).
- **Do not edit** `script.txt`, `board.py` gates, or anything under
  `docs/video/` without being asked. The script is locked once it clears the
  register and humanity gates.
- **No emoji**, in code or user-visible copy.
- **Magazine vocabulary** in copy — issue, feature, spread, folio, colophon.
  Never dashboard, panel, card, widget, modal.
- If a rule here conflicts with the repo, `docs/video/PRODUCTION-PLAYBOOK.md`
  wins — it is the long-form record and this brief summarises it.

## Where the full reasoning lives

- `docs/video/PRODUCTION-PLAYBOOK.md` — the hard-won rules, each with its cost.
- `docs/video/HUMAN-VOICE.md` — the humanity gate and the corpus study.
- `docs/design-language.md` — house palette and type.
- `videos/<film>/WORLD.md` and `CAST.md` — this film's laws and counts.
