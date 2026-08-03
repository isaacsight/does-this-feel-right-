# GALLEY production playbook

> Written 2026-07-24 after shipping *The Price of a Glance* — a 4:44 cited
> behavioural-science film, published at <https://youtu.be/0nOkJ6smSLg> for
> $37.70 of generation. Nearly everything below was learned by having work
> rejected. Read this before starting a film; it will save you three pivots.

---

## 0. The one-paragraph version

Record the narration first, because every timing downstream is measured from
it. Lock ONE canonical character image and reference-condition every frame off
it. Prompt the CAMERA, not the content. Never write "calm" in a style block.
Make each image a funny literal situation, not a symbol. Cut every 3–4 seconds
with uneven, comic rhythm. Nobody verifies their own claims. Validate on two
frames before you generate thirty.

---

## 1. The four pivots, and why they happened

This film was built four times. The failures are the most useful part.

| Version | What it was | Why it was rejected |
|---|---|---|
| v1 e-ink | Minimalist warm risograph, 30 abstract metaphor shots | "dull", "images don't make sense", "motion is off" |
| v2 motion reshoot | Same art, camera-motion prompts on kling | Better, but "not fun to watch", "they don't connect" |
| v3 whiteboard | After Skool line art, no character | Right medium, wrong energy |
| v4 **shipped** | Zenn-style stick figure, muted colour sets, comedy | — |

**The single root cause of all three failures was nine words in a style
block:** `calm, comforting, quiet, gentle, restrained, tasteful`. The model
obeyed them perfectly. Every complaint — dull, ambiguous, disconnected,
unfunny — traced back to explicitly commanding restraint and then being
surprised by restraint.

**Corollary:** when output feels flat, read your own prompt before you blame
the model or spend on a better one.

---

## 2. Art direction that works

### Banned words in any style block
`calm · comforting · quiet · serene · contemplative · gentle · restrained ·
elegant · tasteful`

### The comedy mandate (use verbatim)

> Crude, funny hand-drawn cartoon in the style of a comedic explainer channel.
> Thin stick-figure character with a round head and a BIG exaggerated
> expression — wide bulging eyes, dropped jaw, raised brows, or a flat deadpan
> stare, whichever the joke needs. Cartoon reaction conventions welcome: sweat
> drops, motion lines, squiggles, wobble lines, exaggerated posture. Muted flat
> colour set with confident black outlines — warm tans, muted yellows, soft
> greys. Exactly ONE flat tomato-red element as the accent. Comic, energetic,
> absurd situation played completely straight. Legible at a glance.
> 16:9. No lettering, no words, no numerals.

### Four rules for scene writing
1. **Situations, not symbols.** A funny thing HAPPENING beats a metaphor. The
   two frames that worked first time were a deadpan hero holding a potato and
   spectacles as evidence, and a thumb jerked back at a wall clock. The frames
   that failed were a red thread meaning "attention residue" and a branching
   fork meaning "600 million analyses".
2. **The hero must REACT.** Give a face and a posture every frame: smug,
   wrecked, hopeful, humiliated, dead-eyed. Neutral is what made v1 dull.
3. **Absurd played straight.** Nobody in frame acknowledges the ridiculous.
   The pigeon is a serious colleague. The potato is evidence.
4. **Escalate.** A recurring beat gets bigger and dumber each time. The phone
   gag ran sparkle-eyed grin → faceplant → tongue-out gremlin → same gremlin at
   night with a cobweb from elbow to knee. That escalation is what made it feel
   authored rather than assembled.

### The gate question
Not "is this on-style" but **"is this funny, and does it read in one second
without narration?"** A merely tasteful frame FAILS.

---

## 3. Character consistency — solved

**Text-only prompting cannot hold a character.** Across three text-generated
frames the hero grew ears, gained eyebrows, and changed body shape. Recognisably
the same brief, but three different people.

**The fix, proven across 83 frames with zero drift:**

1. Generate ONE canonical hero image. Keep it simple and distinctive.
2. Every subsequent frame uses `fal-ai/nano-banana-2/edit` with the hero passed
   as **`params.image_urls: ["<hero sourceUrl>"]`**.

> **CRITICAL:** the array must be nested inside `params`. At the top level the
> proxy silently drops it, fal receives `image_urls: []`, and the job is
> rejected *after* billing. This cost $0.24 to learn.

3. Prove it on two NEW scenes the hero was never drawn for. If it holds there,
   it holds anywhere.

### Frame-level traps
- **Never stage a prop on, over, or behind the hero's head.** A grey spike
  behind the scalp renders as a *mop of hair* no matter what the prompt says.
  Silhouette beats words. Move the prop to the floor.
- **Naming a prop by category invites that category's default features.** Ask
  for a "slot machine" and you get a big lit display — which became a second
  red accent AND re-read as a giant phone. Negate unwanted surfaces by name.
- **An edit model cannot be asked to remove its own reference subject.** A
  prompt saying the referenced hero should "walk out of frame" produced
  `no_media_generated` after nineteen minutes queued.
- **A `queued` job that outlives its batch siblings is a failure.** Read
  `pollError` immediately; don't wait it out. Spend is counted at submission,
  so a failed job still costs.

---

## 4. Motion — what actually works

### Camera over held subject
Prompting *content* motion ("the scene comes alive") gives the model room to
invent: it multiplied a single seed into three, sprouted a second teacup, grew
a new graph peak, curled a ribbon into a heart.

Prompting a **camera move over a locked subject** ("slow dolly-in, composition
unchanged, nothing else moves") removes that room. Five shots that failed
repeatedly on seedance came back clean on kling with camera prompting.

**The same change fixes dull motion AND elaboration defects.** They were one
problem.

### Model selection
| Model | Rate | Use |
|---|---|---|
| `seedance-lite` | $0.04/s | **Retired.** Caused every elaboration defect. |
| `kling-pro` | $0.07/s | Workhorse. Holds structure, takes camera prompts. |
| `veo-3-fast` | $0.40/s | Only for a shot the film turns on. Rarely justified. |

### The hard ceiling
**Palmier has no masks beyond a rectangular 4-side crop.** No shape, alpha, or
path masks. You therefore **cannot isolate a limb from a flat PNG** — character
part-motion from a single raster is impossible in this toolchain. The options
are pose-variant frames stepped as hard cuts (limited-anime style), or stills.

### Stills are a legitimate answer
This film ultimately shipped as **still images with hard cuts and zero motion**,
and it is better for it. If the art is strong and the timing is right, motion is
optional. Don't spend on animation to avoid an editing problem.

---

## 5. Timing — the whole craft of a stills film

With no motion, cut rhythm is the only expressive tool.

### Numbers
- **~3.5 s average hold.** v1 ran 9.1 s and read as a slideshow.
- **No hold over 8 s, ever.** A static image past 8 s dies.
- **~1 frame per 3.5 s of narration.** A 4:32 film needs ~75–83 frames.

### Comic timing is UNEVEN timing
| Beat | Hold |
|---|---|
| Quick run (list-y, escalating) | 1.5–2.5 s |
| Setup | 3–5 s |
| **Snap (punchline)** | 1.0–2.0 s |
| Breath (after a big beat, the turn) | 5–8 s |

Uniform 3-second cutting fixes the drag and still kills every joke.

### Rules
- Cut on the sentence, never mid-phrase. Image lands ~8 frames **before** its
  line, so the viewer reads the picture then hears the line land on it.
- Never three consecutive holds of the same length.
- Pace tracks the argument: fastest in the mechanism act, slowest at the turn.
- **The two best cuts in this film were both ~1 second and both landed on the
  film's honesty** — "That's close." and "the weakest thing I've shown you."

### The novelty finding
> **Length is not what makes a hold feel long. Novelty is.**

Every cut-back (reusing an earlier image) sat at the end of a beat on the
longest hold — quietly telling the viewer the beat was over. A 5.17 s hold on a
reused image dragged; the identical 5.17 s on a fresh image did not. **Never
reuse an image.** Generate a new one; frames are $0.08.

---

## 6. Sound

### Routes and real costs
| Purpose | Provider | Cost |
|---|---|---|
| Narration | `elevenlabs-v2` **direct** | **$0 fal** — subscription credits |
| Score | `elevenlabs-music` | $0.80 per *started* minute |
| Design | `elevenlabs-sfx` | $0.10 per generation |

- **Always pass `provider` explicitly.** The engine default is
  `elevenlabs-turbo`, which sounds worse AND is the only speech route that
  bills fal dollars.
- Music bills per *started* minute — a 61-second cue costs two minutes. Compose
  to the minute. Five 60 s act beds cost the same as one 300 s cue and retake
  for $0.80 instead of $4.00.
- **The Music API requires a paid ElevenLabs plan.** The estimate returns $0 and
  the failure only surfaces at submit with `402 paid_plan_required`.
- **The TTS character quota is per billing cycle** and will stop a record
  mid-film. Creator tier = 148,500 chars; a 4:30 film is ~4,000.

### Voice settings
- Defaults now `stability 0.35, style 0.0, similarity 0.75` — tuned for
  "sounds like a person".
- **`style > 0` pushes a voice toward its own characteristic delivery.** On a
  broadcast-register voice that adds *announcer*, not colour. Keep it at 0.
- **Stability moves pitch excursion, not pace.** Anyone reaching for it to slow
  a read should stop.
- **The response is not monotonic** — one act got worse at 0.55 before improving
  at 0.75. One setting is a sample, not a curve.

### Casting
- *The Price of a Glance* used **Eric** `cjVigY5qzO86Huf0OWal`.
- **NEXT FILM: Davis — `Z2fsAwk7IblvPhYzfslC`** ("Davis - Casual Deeper
  American Male", young/American/casual, `narrative_story`). Isaac's pick,
  2026-07-24. **Already added to the account** — callable like any other voice.
- **Adding a Voice Library voice via API is a TWO-step lookup.** `/v1/voices/{id}`
  returns `voice_not_found` for library voices until they are added, and
  `/v1/shared-voices` **cannot be filtered by voice_id** (2,500 voices paged
  blind, no hit). Instead search by NAME, read `public_owner_id` off the result,
  then `POST /v1/voices/add/{public_owner_id}/{voice_id}` with `{"new_name":...}`.
- Check WHICH account a key belongs to before debugging a missing voice — a
  voice added in the browser lands on whatever account that browser session is,
  which may not be the API key's account.

- Cast against the register line, not taste — and audition on real script text.
  Measured comparison beats description: the voice labelled "Steady Broadcaster"
  had the NARROWEST pitch range of three candidates, i.e. the least performed.
  Library labels describe a risk, not an outcome.

### Record narration FIRST
Every shot slot is measured from the actual read, not the script estimate.
**Word-count projections ran ~4× optimistic** on this cast: 18 added words were
projected at +7.8 s and delivered +2.0 s. Measure, never estimate.

---

## 7. Captions

**Build them from whisper's TIMINGS plus the locked script's TEXT.**

YouTube's ASR produced: "Schulz" (Schultz), "Day-Ann" (Dayan), "Furster"
(Ferster), "Amy Orban" (Orben), and — worst — **"a tension residue"** instead of
*attention residue*, the actual name of the phenomenon that beat is about.

On a film whose credibility rests on ten researcher names, auto-captions
actively undercut the argument. Correcting ASR text while keeping its word
timings is free and takes minutes.

`captions().insert` requires the **`youtube.force-ssl`** scope.
`youtube.upload` alone returns 403.

---

## 8. Publishing

### YouTube
- Upload via `tools/youtube-upload.py` (resumable, any file size).
- **YouTube Studio has no addressable file input** — browser automation cannot
  attach a file. The API is the only path.
- **Google permanently masks the OAuth client secret after creation.** If the
  download doesn't land, your only option is minting a second secret. Capture
  it at creation.
- Default to **unlisted**, watch on the platform, then `--publish`.

### TikTok and Instagram
Both **are** browser-automatable — each has a hidden `input[type=file]` behind
its drag-drop zone, which is exactly what the upload tool targets.

| | File input | Note |
|---|---|---|
| TikTok Studio | `accept="video/*"` | tiktok.com/tiktokstudio/upload |
| Instagram | `accept=...video/mp4` | Create → dialog. Business Suite needs separate login. |

- Browser upload caps at **10 MB** — encode upload copies. Not a quality
  compromise; both platforms re-encode everything anyway and flat line art
  compresses extremely well.
- Links are **not clickable** in TikTok or Instagram captions. Use a pinned
  first comment.
- Don't post all three shorts the same day; a burst reads as lower quality than
  a cadence.

---

## 9. Process rules that paid for themselves

1. **Nobody verifies their own claims.** The writers supply sources; the
   Director opens them. This caught a fabricated author pair ("Bos & Bos"), two
   experiments fused into one sentence, a disputed attribution, and a retracted
   group-size number. All written in complete confidence.
2. **Validate small before generating big.** Two frames ($0.16) proved the
   medium. Three frames ($0.24) exposed character drift. Five ($0.40) proved the
   fix. The 30-frame batch then landed 28/30 first pass.
3. **Prefer retracting your OWN evidence to conceding someone else's.** The
   film's strongest beat is where it withdraws a study it just spent 35 seconds
   building.
4. **Keep-the-better-take.** If a retake is worse than what it replaces, keep
   the original and say so. Never regress a good asset.
5. **Errors live between frames, not inside them.** Every frame can pass its own
   gate and the *sequence* still fail — repeated images, a phone that changes
   size, a room that gains a window. Review in sequence.
6. **A colophon cannot ship a number that isn't true.** "Seventy-five frames"
   became false when eight were added; "about eleven dollars" was never
   isolable. Set claims from the ledger or cut them.
7. **Chairs, not steps.** A step can be skipped; a chair has to sign. Each crew
   agent reads the previous one's filed artifact, not their reasoning — which is
   what lets them catch each other.

---

## 10. Costs actually observed

| Item | Rate |
|---|---|
| Keyframe / scene frame (`nano-banana-2`, `/edit`) | $0.08 |
| Clip, kling-pro 5 s | $0.35 |
| Clip, seedance-lite 5 s | $0.20 |
| Clip, veo-3-fast 5 s | $2.00 |
| Narration (`elevenlabs-v2` direct) | $0 fal |
| Score bed, 60 s | $0.80 |
| SFX cue | $0.10 |
| Palmier assembly, cut, export | $0 |

**A stills film is dramatically cheaper than a motion film and can be better.**
This one: 83 frames + narration ≈ **$12** of usable output. The other $25 was
spent learning what not to build.

---

## 11. Engine gotchas

- **The `production_submit` MCP wrapper has a quote/submit hash-mismatch bug.**
  Use the documented HTTP proxy directly: `/v1/images/estimate` →
  `/v1/images/fal` with the capability bearer.
- Quote tokens expire in five minutes. Re-estimate immediately before submit.
- `GET /health` reports `hasKey` for **`FAL_KEY` only** — it says nothing about
  the speech route. Don't infer ElevenLabs readiness from it.
- An env var set to the empty string reads as absent. "Present" in a process
  listing is not the same as "has a value".
- `curl -d @-` strips newlines and breaks the quote hash. Use `--data-binary`.

---

# 10. What the polyvagal film cost us to learn

Three full builds and $18.72 across one film ("THE THIRD THING", 4:35). Two of
the three builds were rejected by the viewer with the same complaint — *"I got
lost watching it."* Everything below is the diagnosis.

## 10.1 The failure was the script, not the edit

v1 (7:17) and v2 (5:06) both lost the viewer, and both times the instinct was
to fix the cut. It was never the cut. **The script had been written to be
read.** Compressed epigrams, each idea stated exactly once, clever lines that
need a second pass — and *a listener never gets a second pass*. Worse: every
tightening revision improved the page and worsened the ear. Tightening is the
wrong reflex on a VO script.

**What a script for the ear needs, all four, every time:**

| | |
|---|---|
| **Signposting** | "Here's the first. Here's the second. And here's the third." Number things out loud. |
| **Example before term** | Show the crying baby, *then* say "co-regulation". Never define first. |
| **Deliberate repetition** | State it, illustrate it, restate it. Saying a thing once is a page habit. |
| **No metaphor without a setup** | v2 had "stands on the brake" with no brake established. Orphaned metaphor = dead air. |

Check Flesch Reading Ease (house band 75–90; v5 scored 87.6) but do not trust
it — it measures prose, not concepts. v2 scored fine and was incomprehensible.

## 10.2 A lecture has no character. Give the narrator an opponent.

v1–v3 all had a passive protagonist — a demonstration dummy that things happen
to. No want, no conflict, no game, and so nothing to follow between facts.

The fix that worked, and it works with **one voice**: the narrator *anticipates
the viewer's objection and answers it.*

> "You'll call that composure. You went grey and stopped blinking."
> "And you're going to argue with that. From the floor. Where you are
> currently lying. Thinking."

This buys a character, a want (don't diagnose me), conflict, and escalation
without a second casting session. The hero's half of the argument is carried
entirely by the picture — he protests with his face while the image proves the
narrator right. It also makes every abstract beat a free reaction shot.

## 10.3 Images must explain, not pun

v2's images were visual puns on the *words* — funny, content-locked, and they
still explained nothing. The rule that fixed it:

> **Can the viewer be wrong about what they're seeing?**
> If yes, the frame must be **literal** — draw the sentence.
> Cartoon physics only where the narration has *already* made the point and
> the image cannot be misread.

Shipped mix: 64% literal · 14% object · 10% physics · 10% the chair anchor ·
2% absurd flourish. "A little bit of everything" is a real note — one style
applied everywhere flattens the film.

**Give the film one recurring shot.** Here it was the same person in the same
chair, three ways (warm / cold / grey; mug upright / spilled / on the floor).
A viewer who loses the thread can always re-enter on it. It is the single
highest-value frame in the film — protect it. (An empty chair in that slot
inverts the meaning; see the `v17` defect.)

## 10.4 Content-locking, and the two bugs in it

Never distribute frames evenly and never anchor only some of them. v1 anchored
15 and let 71 float — every image landed a beat early for seven minutes.

Match **each frame's line against the narration segments by text similarity**,
then re-time. Two bugs cost a cycle each:

- **The monotonic-cursor bug — hit twice.** Advancing a cursor through segments
  assumes the frame ids sort in narration order. They don't the moment you
  append fixes (`h01–h04`, `w01–w07`). *Match every frame independently against
  all segments, then sort by resulting start time.*
- **Stranded tails.** A hard cap on hold length strands the last frame at 18.9s.
  Use slack-bounded snapping: `slack = max(0, MAX - even_spacing)`.

Working bounds: min 1.8s, max 8.0s, drift tolerance 1.5s.

Then **audit the coverage before you export** — v5 shipped with seven closing
lines that had no frame at all, producing a 26.1s hold. A one-line check for
lines with no matched frame would have caught it.

## 10.5 Lettering contamination

Generated frames render text when the *concept* implies a label, and render
sound effects when the prompt describes *motion*. Casualties across this film:
"SCREAM", "A"/"B", "crash", "WOBBLE", "MENU", "UP/DOWN", "AHA!", "thud thud
wobble", and — surviving into the final export — **"CLATTER" twice in `w01`**.

Two fixes, both preventive:
- **Restage as aftermath.** Don't describe the crash; draw the wreckage.
- **Remove text-bearing objects** from the scene (menus, signs, labelled doors).
- Say it in the style block, and then *still* validate every frame.

**Never name a concrete example object inside a style block.** An opossum
mentioned once as an illustration was drawn into 7 of 10 reshoots. (Kept as a
running character — but that was luck, not design.)

## 10.6 Review the export frame by frame, and say what that can't catch

Extract the midpoint frame of every cut into a labelled contact sheet — frame
id, timecode, hold duration, and the narration line playing under it. 57 cuts
fit on three sheets. This catches mismatches, lettering, and out-of-band holds
in one pass.

It does **not** catch anything that only exists in motion. Say so every time.

## 10.7 Audit the frame edge before you audit the frame

A generator handed 1920x1080 canvases will not necessarily draw to the edge of
them. On *Why Humans Need Rituals*, 69 of 96 frames were a 1620x1080 panel
painted onto a cream field, 21 ran full-bleed, and 6 landed at margins of 198,
269, 270, 285 and 299px. Every file was 1920x1080, so nothing downstream
complained. The picture simply breathed in and out for the first ninety
seconds and then locked. Nobody chose it.

Measure it, don't eyeball it:

```bash
for f in *.png; do printf "%-24s %s\n" "$f" "$(magick "$f" -fuzz 4% -format "%@" info:)"; done
```

`%@` returns the bounding box of non-uniform-border content. A `+150+0` offset
means 150px of flat colour the model painted. 96 files in 8 seconds. Do this
before the first assembly, not after the master exists.

**Normalize toward the panel, not toward full-bleed.** Scaling a 3:2 panel up
to fill 16:9 costs 84px off the top and bottom in panel coordinates, and this
art keeps feet near the bottom edge — only 1 of 83 frames had the headroom to
survive it. Cropping everything *to* the common panel and padding back with
the paper colour is lossless for the majority and cost nothing but a verified
side-crop on the minority. Check the crop frame by frame anyway; the risk is
subjects near the left and right edges, not the centre.

The fix is pixels only. `build-literal-final.mjs` already sets
`background: #f4e8c8` on the root and every scene container, so corrected
images drop straight in with no HTML change and no re-derivation of the
clause-timed cue points. Back the originals up to a sibling directory first.

## 10.8 Generative editors cannot repair a frame. Do not try.

The same film had the companion drawn two ways — a flat box-robot in the
bookends, an articulated humanoid through the middle, 15 frames affected.
Gemini (Nano Banana, via the web UI, Pro account) was asked to swap the robot
and change nothing else, twice, with escalating precision about what to leave
alone.

Both attempts redrew the whole frame: the boy's face and head size, the basket
became a drum, the goat re-posed, the camera moved closer, the palette
saturated, the line thickened. The second attempt got the robot right and
drifted *further* from source, because it anchored on its own previous output
rather than the original. These models regenerate; they do not patch.

Second, independent blocker: output came back at **1024x682**. Correct 3:2, but
against a 1620x1080 panel that is a 1.58x upscale. Replaced frames would read
softer than their neighbours even if the style matched.

The trade is bad in both directions. One inconsistency inside a coherent world
beats 15 frames that are a different drawing *and* a different resolution. If a
character must be repaired after the fact, composite from the existing art —
the correct design already exists at full resolution in the frames that got it
right — and accept that this only works where the pose is generic and the
background behind the subject is flat.

The real lesson is upstream: lock the character reference before the first
batch. There is no cheap repair.

## 10.9 A reference image is a prior on everything it contains

*You Are Not Finished*, 2026-07-30. 87 frames generated through
fal-ai/nano-banana/edit, each conditioned on a character reference sheet.

The sheet fixed the drift that ruined the previous film outright — 87
independent generations, zero character drift, first time. Reference
conditioning is the single most effective control available.

But it conditions on **everything the reference shows**, and three separate
defects all traced to that:

| Defect | Cause | What fixed it |
|---|---|---|
| Robot appears in frames it doesn't belong in | Sheet shows two characters, so both are "what pictures contain" | Removed "cyan robot" from the global style block |
| "Front View", "Side View", "FUTURE SELF" printed into frames | Sheet is captioned | A sheet with the captions painted out |
| Scenes drawn as boxed panels floating on cream | The sheet **is** a grid of boxed panels | Adding a finished full-bleed frame as a second reference |

**Prohibition does not beat demonstration.** Every one of these survived an
explicit, capitalised ban in the prompt. Every one died the moment the
reference stopped demonstrating the unwanted thing. When output is wrong, the
first question is not "how do I word this better" but **"what is my reference
showing that I did not ask for?"**

**Use two references.** One for construction and palette (the character
sheet), one for layout (a finished frame you approve of). The layout reference
is what stops boxed panels.

**Make the clean reference mechanically.** Asking the model to remove the text
from its own sheet returned the sheet with every word intact — same
regenerate-don't-edit behaviour as 10.8. Painting flat cream over three label
bands with ImageMagick took one command and cost nothing.

**Costs, for planning:** 87 frames at $0.039 = $3.39 for a clean pass. Real
total with re-rolls was **$5.34** — budget roughly 1.6x the nominal count.
Drive fal directly rather than through the local engine: that wrapper caps
param strings at 2,000 chars (a reference data URI is ~96KB), reserves
image_url, sends singular image_url where /edit endpoints need image_urls as
an array, and refuses endpoints with no price metadata.

## 10.10 The layout reference must be scenically EMPTY, not merely plain

*Learned on* You Happen to Life, *2026-07-31, at a cost of 37 frames.*

10.9 says a reference image is a prior on everything it contains. That is
correct and it is not enough, because it does not say what to do about it. The
practical rule it implies is this:

> **A layout reference can only teach geometry if geometry is all it has.**

The sequence on this film, three failures deep:

1. The layout reference was the previous film's `01a` — a corridor of framed
   portraits. Frame 047c came back **set in that corridor**, in an act that has
   no corridor in it.
2. Repointed at this film's `015a`, which reads as "plain" to a human: one flat
   wall, lots of empty space. But it *is* a dial, a stepladder and the cyan
   robot. A quarter of the film came back with gratuitous dials and stepladders
   in beats that mention neither — including Act 6, where the robot has no
   business being.
3. Fixed by **generating a purpose-built plate**: flat paper to all four edges,
   one horizon line, one small figure seen from behind, and an explicit list of
   what must not be in it (no objects, no furniture, no walls, no dials, no
   machines, no second character, no props). Costs $0.04 and one prompt.

**"Plain to a human" is not the test.** The test is: *if the model copied every
object in this image, what would I be stuck with?* A frame with one distinctive
prop will donate that prop a hundred times.

**Make the plate before the batch, not after.** The defect is invisible frame
by frame — each individual image looks fine and on-model. It only becomes
obvious on a contact sheet of the whole film, by which point it is paid for.

**Corollary for the audit.** Neither automated edge check catches this, and
neither catches everything on its own:

| Check | Catches | Misses |
|---|---|---|
| trim bbox | inset panels, letterboxing | fires on any frame whose art does not touch the edge — most of them |
| corner sample | printed borders, wrong paper | passes an inset panel whose surround is the same paper |
| **contact sheet** | **content bleed, lettering, repetition** | nothing, but it needs eyes |

Run both automated checks to triage, then **look at the whole film on one
sheet before assembly**. Content bleed is a whole-film defect and is only
visible at whole-film scale.

## 10.11 Every recurring object needs its own reference plate

*Learned on* You Happen to Life *when Isaac watched the first cut and said some
of the images lost him and some lost the continuity.*

10.9 and 10.10 cover the character sheet and the layout plate. There is a third
reference nobody had thought to make, and its absence is what broke this film:

> **If an object recurs, it needs a reference image of its own. A text
> description is not a design.**

*You Happen to Life* turns on a single motif — a dial, mounted on a wall, one
needle, one end "internal" and one end "external". It appears in 22 frames. It
was specified in words on every one of them and never drawn once for reference,
so it came back as a grey square plate, a wall clock, a bright cyan disc with a
square in it, a speedometer with fine tick marks, a black plate, and a small
bronze ring. The film asks the viewer to track one object through an argument
and shows them eight.

The fix is one frame, $0.04: draw the object cleanly, on-model, full bleed, with
a figure beside it for scale, and pass it as the layout reference for every
frame that contains it. Continuity was restored in a single pass.

**State what the object is NOT.** The dial plate prompt had to say "no tick
marks, no numerals, no second hand, it is not a clock and not a speedometer" —
because every generic prior for "round thing with a needle on a wall" is a
clock. Naming the near-neighbours you are refusing does more work than any
amount of describing the thing you want.

## 10.12 A diagram of the idea is not an image of the idea

The other half of the same note. Where the script was abstract, the board was
abstract back:

| Line | What was boarded | What it read as |
|---|---|---|
| "the line is not only a mood" | a black bar floating in a room | nothing |
| "a claim that does not hold as hard as it sounds" | two bars sagging | nothing |
| "when it lands on the right person, it lifts them" | a bar raising someone | nothing |

An abstraction illustrated by an abstraction gives the viewer nothing to hold.
Worse, the bar became a *second* undeclared motif — and being an abstraction it
drifted too: black bars, a cyan rectangle, a black pillar, a slab on someone's
head. The board's own rule said "nothing else recurs" and the board broke it.

**The replacement rule: a person doing a specific thing in a specific place.**

| Line | Re-boarded as |
|---|---|
| "the line is not only a mood" | the person alone on the pavement afterwards, under one streetlight |
| "a claim that does not hold" | someone standing easily on a wooden crate — then the crate's side panel, quietly split |
| "it lifts them" / "it lands on somebody with no room" | one person reads a message and reaches for their coat; another reads the same message on the floor of a cramped room, and nothing in the room has changed |

Same argument, and now there is something to look at. **When a line is
abstract, that is exactly when the image must be concrete** — the narration is
already carrying the abstraction, and the picture's job is to give it a body.

## 10.13 Motion is the exception

All 108 clips of the first cut had a slow zoom. The note back was that the pans
and zooms need still frames between them, and that is right for a reason worth
writing down: **if everything moves, nothing reads as moving**, and the frames
that should land have no stillness to land into.

The rule now in `tools/video/build-composition.mjs`: a frame holds still unless
it earns a move, and it earns one only by being long (>= 3.4s). Two movers never
sit back to back. Frames carrying a claim — the evidence, the closing image —
are always still regardless of length. That lands at roughly a third in motion.

## 10.14 Never trim connective tissue to hit a runtime

*Isaac on the finished* You Happen to Life: *"a lot of this one jumps around
with no explanation or abruptly disconnects from the continuity of the ideas...
the narration has to feel like a conversation and the explanation and the
story."*

The script passed every register gate. The gates measure **sentences**; nothing
measured whether one paragraph follows from the last.

**The direct cause was the runtime trim.** The film came in at 6:57 against a
5-7 target, so four beats were cut. Three of the four were bridges:

| Cut | What it was doing |
|---|---|
| "So the line on the stage is not empty at all, and you should not dismiss it." | tying the research back to the opening claim |
| "That claim is testable too, because you can count your hours... and a great many researchers have done exactly that." | **the entire bridge into Act 4** |
| "Then they asked a very plain question." | the signpost before the evidence |

They were chosen because they carry no new information, which made them look
like the cheapest seconds in the script. **Carrying no information is what a
bridge is for.** It carries the argument's motion instead, and motion is the
thing the ear needs and the page does not show.

**Rule: when a script is over length, cut an example, a repetition, or a whole
beat — never the sentence that explains the move from one idea to the next.**
If an act must go, cut the act and its bridge together.

## 10.15 Write a story, not a stack of arguments

The deeper cause. *You Happen to Life* is seven acts that each state a claim and
evidence it. Nothing in Act 4 happens *because* of Act 3. That structure is
invisible while writing — each act is individually good — and it is exactly what
"jumps around" describes.

Two tests to run on the draft, before boarding:

**The skeleton test.** Read only the FIRST and LAST sentence of each paragraph,
in order, as one continuous passage. If that reduced text does not itself hold
together, the film will jump — the connective work is missing, not merely thin.

**The "so / but / which means" test.** Every section boundary should survive
having one of those words placed in front of it. If the honest connective is
"also" or "separately", the two sections are a list, not a story.

**Conversational register is a separate axis from reading level.** The gates
already force short words and plain sentences; they do not produce a person
talking. That comes from asking the viewer a question and then answering it,
naming the objection out loud before making it, admitting what is hard, and
letting a beat follow from the previous one instead of starting fresh.

## 10.16 Room tone: text-to-audio, not video-to-audio

Both films shipped as narration over **digital silence** - the gaps between acts
measured -90 dBFS, which is a hole, not a quiet moment. Fixed 2026-07-31 with
`tools/video/roomtone.mjs`. Three findings, total cost $0.39 to establish:

**A video-to-audio model cannot do this.** `wavespeed-ai/mmaudio-v2` is $0.001/s
and looks ideal. On our film it returned near-silence: 28 of 29 seconds at
-57 dBFS with a single blip. It infers sound from **visible physical events**,
and flat illustration with near-static frames gives it nothing to key off. It is
built for footage of things happening. This will be true of every GALLEY film.

**Bakeoff between the two text-to-audio candidates, identical prompt, 30s:**

| model | RMS | peak | per-second spread | $/s |
|---|---|---|---|---|
| `sonilo/v1/text-to-sfx` | -53 | -39 | **3 dB** | 0.002 |
| `mirelo-ai/sfx-1.6/text-to-audio` (ambience) | -25 | -4 | **13 dB** | 0.010 |

Mirelo has real *events* in it - a 13 dB spread and -4 dB peaks pull attention
off the narration. **A bed has to be boring.** Sonilo is steady and 5x cheaper.
Its very low output level is not a defect; a bed gets normalised into place.

**Normalise the bed, never gain it.** The model's absolute output level varies
between generations, so a fixed gain puts the bed somewhere different every
time. `loudnorm=I=-34` against a -16 LUFS programme is the shipped setting.

**Measured result on the film:** act gaps went from -90.3 dB to -36.8 dB, and
the level under narration moved by **+0.1 dB** - i.e. the bed fills the holes
and is inaudible under speech. That is the whole job.

Sonilo caps at 180s; longer films loop the tone rather than paying per second.

## 10.17 Real frame motion: LTX-2-fast, smoke-tested

The School of Life shorts study found their frames MOVE while ours are stills
with an assembly-level zoom. `lightricks/ltx-2-fast/image-to-video` closes that
gap and it survived a real test (2026-07-31, $0.48).

**Price.** $0.04/s, duration is an enum [6,8,10,12,14,16,18,20], so the floor is
**$0.24 per 6s clip**. Animating ~20 hero frames of a film is ~$5.
Compare Veo 3.1 lite at $0.08/s (1080p) - 2x the price for shots that do not
need Veo's composition control.

**It holds our style.** Two frames tested, one with two figures and one with a
crowd of roughly 200:

| | frame-to-frame delta | pixels changing >11% | RMSE vs source at 0.1s -> 6s |
|---|---|---|---|
| two figures | 1.05/255 | 0.95% | 0.183 -> 0.182 |
| crowd of ~200 | 2.02/255 | 1.54% | 0.204 -> 0.205 |

**The drift figure is the one that matters:** the difference from source is the
same at six seconds as at frame one. It does not accumulate, which is exactly
the melt/warble failure this style is vulnerable to.

**Two gotchas.**
1. Output is **25fps**. Our films are 30 - conform before assembly or the cut
   judders.
2. It applies a small reframe at frame one and then holds it. That is the ~0.18
   RMSE baseline, not quality loss. If a frame must match its neighbours
   exactly, budget for it or keep that frame still.

**Prompt discipline that produced these results:** name the camera as locked,
name the ONE thing allowed to move, state that nothing else moves at all, and
restate that the drawing style, line weight and colours stay exactly as in the
source. Asking for less motion is what keeps it on model.

### 10.17a Two hard limits, and the recipe that fixed the fixable one

**NEVER ASK LTX FOR A CAMERA MOVE.** Asked for a "very slow" dolly down an
archive, it travelled several metres: by 2s it was inside the drawers, by 4s it
had invented a symmetrical corridor that was not the source scene, with the
character and furniture gone. **"Slowly" is not a constraint it honours.**
Camera moves belong in the composition, where `build-composition.mjs` already
does them deterministically and to the frame. Every prompt should LOCK the
camera in explicit negatives - no dolly, no push, no zoom, no pan, no tilt.

**Subject motion is a treadmill.** A figure asked to walk across frame walks
IN PLACE while the background shifts. Do not fight it: board for motion in
place, or translate the finished clip in assembly.

**The recipe, A/B measured on one frame:**

| | v1: 1280px jpeg, "slowly" | v2: full PNG, camera locked, clean surfaces named |
|---|---|---|
| frame-to-frame delta | 1.50/255 | **1.29/255** |
| spurious pixel change | 1.25% | **0.94%** |
| RMSE drift over 6s | 0.145 -> 0.155 (drifting) | **0.145 -> 0.144 (holds)** |

Three levers, all of which paid:
1. **Send the full-resolution PNG, never a downscaled JPEG.** On flat line art
   the edges ARE the image; q88 at 1280px seeded visible floor debris and
   scratch artefacts from 4s onward.
2. **Lock the camera in five explicit negatives**, per the archive failure.
3. **Name the clean surfaces.** There is no `negative_prompt` field on this
   model, so "clean and empty, no marks, no debris" goes in the positive
   prompt. It works.

All three are baked into `tools/video/animate-frames.mjs`, which takes a
`motion.json` of `{frame-id: what moves}` and appends the lock clause itself -
they are not per-shot decisions.

### 10.17b Never animate a frame that carries data - and the metric that misses it

The five-bar chart is *You Happen to Life*'s central evidence: a collapse from
26% at games to under 1% at your job. Animated for six seconds it came back as
roughly **eight bars of near-equal height**. The model reads a chart as
decorative shapes and rearranges them. Shipping it would have put a picture on
screen that CONTRADICTS the narration.

**Charts, tables, diagrams and anything whose geometry IS the argument stay
still.** That is a correctness rule, not a quality setting.

**The metric that misses it.** Frame-to-frame delta - the warble detector in
10.17 - rated the failing clip as BETTER than the good one:

| | delta | spurious pixels | verdict |
|---|---|---|---|
| bar chart (destroyed its own data) | **1.18**/255 | **0.80%** | looked best |
| walking figure (fine) | 1.29/255 | 0.94% | looked worse |

Because **frame-to-frame delta measures melting, not meaning.** Content that
morphs slowly has low per-frame change and total semantic loss.

**What catches it is RMSE against the SOURCE, sampled early and late:**

| | at 0.2s | at 5.7s | drift |
|---|---|---|---|
| bar chart | 0.124 | 0.182 | **+0.057** |
| walking figure | 0.145 | 0.144 | -0.001 |

`tools/video/animate-frames.mjs` now runs this automatically after every clip
and **rejects anything drifting more than +0.02**, reporting the frame as one
that must stay still. Verified against both clips above: it rejects the chart
and passes the walk.

## 10.18 An intro's problem is usually rhythm, not footage

*Channel intro v15, approved 2026-07-31.*

The intro had good footage and a good mark and still felt flat. The diagnosis
was not the images: **everything moved at one speed.** Eight seconds of
constant-velocity corridor, a soft dissolve, a gentle draw-on. No acceleration,
no arrival, and - the real fault - nothing CAUSING anything. The corridor faded
out and, separately, the mark faded in.

**Build -> rush -> blow out -> resolve -> hold.** Three changes, no new
generation, no cost:

1. **Accelerate the move.** `zoompan` with a cubic ramp -
   `z='1+0.20*pow(on/240,3.2)'` - so it barely moves at the start and rushes at
   the end. A move that goes somewhere beats a move that merely continues.
2. **Cut the transition hard, on the peak of the acceleration.** A 0.65s
   `fade=t=out:color=<paper>` instead of a slow dissolve. It reads as the crash
   at the end of the rush.
3. **Make the destination CAUSE the mark.** The glyph now starts at scale 0.13 -
   roughly what the corridor's perspective gives its own vanishing point - and
   grows to full size while it draws. It does not appear after the corridor; it
   emerges from the exact point the camera was accelerating toward.

Point 3 is the general lesson. **The mark was always "the corridor reduced" and
the piece only ever said so in a code comment.** If a design idea is written in
your comments and not visible on screen, that is the improvement.

**One sound, not a soundtrack.** The core snap was the only hard arrival in the
picture and it landed silently. A single soft wooden knock on it ($0.004,
sonilo text-to-sfx, normalised down from a clipping 0 dBFS) completes the
rhythm. Everything else eases; one thing hits.

**Corollary:** when a hard transition is added, remove the soft one it replaced.
The title beat still dissolved a held still on top of the new blow-out, which
undid the handoff. Two transitions doing one job is worse than either alone.

## 10.19 Karaoke captions: take the word timings at record time

Requested for the film after *You Happen to Life*: captions that highlight
word by word as the narrator speaks.

**The enabler is free and already in the pipeline.** ElevenLabs'
`/v1/text-to-speech/{voice}/with-timestamps` returns character-level alignment
alongside the audio at no extra cost. `tools/video/narrate.mjs` now calls it and
folds the characters into per-word timings in `audio/words.json`, offset into
the final mix so each act's words sit at their true position after the act gaps.

Verified on a real line: 84 characters -> 18 words, durations from 0.02s ("a")
to 0.63s, inter-word gaps 0.023-0.337s. Those are real speech numbers, not
interpolation.

**Do NOT approximate word times.** Distributing a line's duration across its
characters is what `conform-beats.py` does for FRAME timing, where a few
hundred milliseconds is invisible against a ~3.8s hold. A caption highlight
reads as broken at 80ms. Take the alignment at record time or do not do the
feature.

**Render the highlight in HyperFrames, not ImageMagick.** This machine's ffmpeg
has neither libass nor libfreetype, which is why `cut-verticals.py` composites
caption cards as PNGs. Per-word highlighting that way means one PNG per
highlight state - thousands of files. In the composition the browser draws real
text and GSAP times the highlight off `words.json` directly.

## 10.20 A reference is necessary and not sufficient — describe the cast at point of use

*You Watched It Happen, 2026-07-31. Got this wrong in both directions in one hour.*

**Direction one: hardcoding the protagonist into the style block.** The block
carried "the recurring character wears a red jacket over a cream shirt..." and
`build-prompts.py` appended it to EVERY prompt. Fine on the previous film,
where he was in most frames. On a film with researchers, technicians and three
mothers it put him into all 133 frames whether the board asked for him or not —
so **every researcher came back as the protagonist**. The board said
"a researcher"; the prompt said "the recurring character wears a red jacket";
the model did as it was told.

**Direction two: removing the description entirely.** With the block fixed, the
only words left were the board's own phrase — "the person in the red jacket".
The cast sheet still showed him correctly. It was not enough: across 133 frames
his head drifted between **completely bald, one tuft, and a fringe**, and his
proportions between chunky-round and taller-adult. Isaac caught it: "the
character has 2 hairs sticking out... the heads need to be consistent."

**The rule.**

> A reference image is necessary and it is not sufficient. The WORDS have to
> carry the design as well — expanded at the point the board NAMES the
> character, and nowhere else.

`build-prompts.py` now holds a `CHARACTER` constant with the canonical
description ("completely bald except for EXACTLY TWO short thin hairs sticking
straight up from the crown...") and expands it at first mention per frame. On
this film that is 49 frames described in full and 84 with no protagonist forced
into them.

**Say the count.** "Two hairs" drifts to one or none; "EXACTLY TWO short thin
hairs sticking straight up from the crown" holds. Any countable feature of a
character — tufts, buttons, legs on a robot — needs its number stated, for the
same reason the camera plate had to say what it was NOT.

**Corollary for the style block:** it should carry only what is true of EVERY
frame. Anything true of some frames belongs to the board.

## 10.21 Build captions from real word timings, not from estimates

*You Watched It Happen, 2026-07-31. Isaac asked whether the captions were in
sync. They were not, by up to three seconds.*

The old chain estimated twice and the errors stacked:

1. `conform-beats.py` spreads an act's MEASURED duration across its beats in
   proportion to **syllables**.
2. `build-segments.py` then divides each beat into cards in proportion to
   **characters**.

Both are reasonable; both are approximations. Measured against the true word
timings on a 7-minute film:

| | old estimate chain | from `words.json` |
|---|---|---|
| mean drift | **+0.41s** | -0.001s |
| worst card | **3.3s early** | 0.017s |
| cards >0.5s out | **62%** | 0% |

0.017s is 30fps frame quantisation. There is no error left to remove.

**Use `tools/shorts/segments-from-words.py` wherever `audio/words.json` exists.**
Estimation was the only option before `narrate.mjs` recorded with
`/with-timestamps`; it is not any more. Keep `build-segments.py` only for old
projects with no word timings.

**Two rules that fell out of it.**

**Break cards on real pauses.** A gap of >=0.45s in the word stream is where the
speaker ended a thought. A card that runs across it reads as lagging even when
its timecode is right.

**The START must be exact; the END is free.** Reading time is not bounded by
speech. A card too short to read holds into the silence before the next card
rather than being merged or having its start nudged - moving a start is what
breaks sync, and nothing about holding an end does. That took 25 flashing cards
to zero without changing a single start time.

## 10.22 Never ask a sound model for a HUM

*Shipped a film with mains hum under it, 2026-07-31. Isaac heard it; the
measurements had not.*

The room-tone prompt in 10.16 said **"soft low air handling hum"**. The model
delivered exactly that: a harmonic series at 120 / 240 / 360 / 600 Hz with a
third of its energy below 200 Hz. That is not room tone, it is mains hum.

**Why the earlier checks missed it.** Every measurement taken was of LEVEL:
integrated LUFS, per-second RMS, and the delta under narration. All of them
passed, because the bed sat 18 dB down and moved the programme by +0.1 dB. Level
says nothing about CHARACTER. Under speech the hum was masked; in the act gaps
it added **48 dB** of low-frequency energy into what should have been silence,
and that is where a listener hears it.

**Three rules.**

1. **Ask for AIR, not for a tone.** "The faint airy hiss of a very quiet empty
   room, soft broadband air, no tone, no hum, no drone, no buzz, no motor."
   Naming the thing you are refusing does the work, exactly as with the camera
   plate in 10.11.
2. **High-pass any generated bed at 180 Hz regardless of what came back.** A room
   bed has no business carrying low end; that band belongs to the voice, and
   anything left in it reads as hum. `roomtone.mjs` now does this unconditionally.
3. **Measure the BAND, not just the level.** The test that finds this is
   band-limited energy (60-200 Hz) sampled IN THE GAPS between acts, compared
   against the same file without the bed. A 48 dB difference is not subtle once
   you look in the right place; it is invisible if you only look at LUFS.

**And a process note.** The bed was added, measured, declared good and published
inside one session, and the only thing that caught it was a human listening.
When a change is inaudible to the tools available, that is a reason to have
someone listen before it ships, not a reason to trust the tools.

---

## 10.23  Cut points come from the same file the captions do

`segments-from-words.py` fixed captions by reading `audio/words.json`. The IN
and OUT points of the shorts did not move with it — they were still coming from
`production/beats-conformed.json`, whose starts are *estimates*: an act's
measured duration spread across its beats in proportion to syllables. That is
accurate to a few hundred milliseconds, which is fine for holding a frame and
useless for a cut, because a few hundred milliseconds is a whole word.

Five of six shorts opened mid-sentence:

    "three researchers gathered every trial they could find"   (lost "In 1995,")
    "of us have said it to somebody"                           (lost "Most")
    "in. And what it is good at is the mother"                 (lost the clause)

On a vertical short the first second *is* the hook, so this is not cosmetic.

`tools/shorts/pick-spans.py` snaps every span to real sentence boundaries taken
from the word timings, and prefers the longest whole-sentence run that fits the
60s window over the first one that fits — the difference is usually one more
complete sentence, and a short that ends on a finished thought beats one that
ends because the clock ran out. Two of the six got materially better for free:
one became the film's actual cold open, another now ends on the film's last line.

**The rule.** Anything that needs to know when a word was said reads
`audio/words.json`. One source, every consumer. If a tool is deriving timing
from the beat map, it is deriving it from a model of the narration rather than
the narration.

## 10.24  A retrofit beats a re-record

*You Happen to Life* was recorded before `narrate.mjs` started requesting
`/with-timestamps`, so it had no word timings and its published captions were
up to **4.2 seconds** out — 123 of 185 cards more than half a second wrong.

ElevenLabs' `/v1/forced-alignment` takes audio you already have plus the text
you know was said and returns character-level timings for it.
`tools/video/align-existing.mjs` wraps it: worst drift went **−4.245s → +0.017s**
without re-recording a syllable, so the published audio is untouched and the
captions still match the film that shipped.

Any film in the catalogue can be given exact captions this way. There is no
reason to leave an old film with estimated ones.

## 10.25  Two Instagram bugs that looked like flakiness

Both presented as "some shorts upload, others fail in the same run", which reads
as rate limiting and is not.

**1. `clearOverlays` was closing the composer.** The sweep clicks anything
labelled Close or Dismiss to clear cookie and notification popups. Instagram's
*own* create-post dialog has an X labelled "Close", so the sweep shut the upload
and raised "Discard post?", which then sat on top of Next and blocked the rest
of the walk. Shorts that succeeded only won a race against that button
rendering inside the 800ms probe. `clearOverlays` is now composer-aware.

Detecting the composer by header text is not enough — the header changes every
step (Crop → Edit → New reel), so a text guard holds at step one and lapses at
step two. Detect the **dialog**; it is present the whole way through.

**2. The Next walk broke silently.** If Next was not visible it `break`ed and
fell through as if it had advanced. Instagram transcodes before it will let you
past Crop, and that scales with the file, so every short over ~55s blew the flat
20s budget. The error then surfaced 60 seconds later as "caption box never
appeared", three steps downstream of the cause. First Next now gets 180s, and
zero advances is a loud failure.

**The lesson, which is the same one as the hum.** Both bugs were invisible
because the adapter only screenshotted on a failure path neither took. A step
that can fail needs to capture what the page was showing when it did, or the
error names the symptom and buries the cause.

## 10.26  The TikTok adapter reported eight posts that did not exist

Worse than the Instagram bugs, because those failed loudly. This one succeeded
loudly and was wrong: all eight uploads on 2026-08-01 logged
`file attached / caption verified / posted`, and TikTok Studio's post list ended
at the previous day. Nothing had been published.

The cause was three lines that describe the check and then throw it away:

    // Confirm the composer actually closed - clicking is not proof of posting.
    await page.waitForURL(u => !u.includes('/upload'), { timeout: 90_000 })
      .catch(() => {})              // <- swallows the failure it just caught
    return { url: '...' }           // <- success regardless

**A verification you discard is worse than no verification**, because it reads
as evidence in the log. The comment above it was correct and the code under it
did the opposite.

The underlying block: TikTok runs a copyright / content check on upload, and if
it is still running when Post is clicked it raises a **"Continue to post?"**
dialog — *"The copyright check is incomplete. Posting your video now will stop
the check."* — with Cancel / **Post now**. Nothing answered it, so the post sat
there. It only started failing that day because the previous batch's checks had
finished before Post was clicked. The adapter now waits for the check to
finish, and confirms the dialog if it appears anyway.

### And a verification lesson, learned twice in one session

**Every social profile grid under-reports.** Instagram's reels grid returned 12
where there were 41. TikTok's profile grid returned 8 where Studio showed 32.
Both are virtualised; a fixed wait measures the viewport and a wheel-scroll loop
is not guaranteed to drive the container. I drew a wrong conclusion from each,
having just documented the trap for the other.

Use the **owner-side** list — TikTok Studio's Posts table, with its total count
in the header — and check the count moves by exactly the number you posted.
`tools/publish/tiktok-audit.mjs` exists for this. When a scraped count and a
displayed total disagree, the total is right and the scrape is truncated.

## 10.27  YPP is judged on the channel, so cadence is a production constraint

YouTube's 2026-08 clarification replaced "inauthentic content" with three named
buckets. Full reading in `docs/video/PLATFORM-POLICY.md`; the part that changes how
we work is this:

**Our exposure is not the imagery and not the synthetic voice.** YouTube is
explicit that it is "agnostic to what tools are used to create the content."
Our exposure is that YPP is assessed on the CHANNEL, and on 2026-08-01 we put
**fourteen verticals out in forty-eight hours** — same treatment, same caption
system, same structure. Each was a distinct argument with cited sources. The
upload history still read as "lots of videos really quickly that are very
similar", which is the policy's own wording for what it demonetises.

Good work in a bad pattern is still a bad pattern. So cadence is now enforced
rather than intended: `tools/publish/cadence.mjs`, on by default, two shorts per
rolling 24 hours **across all films** — per-channel, because a per-film limit
would let two queues drain on the same day and miss the point entirely. It
counts distinct shorts rather than jobs, since one short going to three
platforms is one video's worth of cadence.

Deliberately not blocked: finishing a short that is already part-published.
Leaving one live on TikTok and missing on YouTube is worse than either choice.

The other two buckets cost us nothing today and constrain the Director
permanently: **the narrator never becomes a character** (an "AI persona"
discussing health, medicine, law or finance is demonetised, and our films land
on medicine routinely — what exempts us is that we have narration, not a
presenter), and **on any such claim the authority is the citation, never the
narration**. "The research found X" is reporting. "You should do X" is advice
from a persona.

## 10.28  A world shift needs a world-native castplate

Tested 2026-08-02, six frames, $0.27. One scene (the character at a bus stop),
one castplate, four style blocks: house cream, night slate, riso duotone,
autumn field. The character held in all four — and the WORLD only fully
shifted in one. The night world kept a cream ground under a slate sky; the
riso world barely moved at all.

The reference plate is a prior on the world it was painted in, not just on the
cast (the same law as 10.9, arriving from the palette side). Style-block words
lose to plate pixels wherever they disagree.

**The fix, verified:** repaint the castplate itself into the target world first
— "keep every pose, proportion and construction line identical; change ONLY
the colour world" — then condition every frame on the world-native plate. One
$0.039 image turned the half-night into a complete night with the character
intact through both hops.

So a film's look locks in this order: name the world against the catalogue →
repaint the castplate into it → empty layout plate in the same world → frames.

**Fallback note, same session:** WaveSpeed serves nano-banana/edit with the
same request shape (base-URL swap; `images` not `image_urls`). Mechanically
proven as an emergency path when fal runs dry; the one sample showed visibly
weaker scene geometry, so it is a fallback, not an equal.
