# STATUS — Your Memory Is Not the Original

Working title. 5–6 min, 1920×1080, 30fps. Episode 3 of the kernel.chat
science strand, after *The Price of a Glance* and *The Third Thing*.

## Gate state

| Gate | Artifact | State |
|---|---|---|
| **1** | `RESEARCH.md`, `CLAIMS.md` | **COMPLETE — awaiting review** |
| 2 | `SCRIPT.md`, `BEAT-SHEET.md` | not started |
| **3** | `FRAME-BOOK.md`, `SHOT-LIST.md`, character sheet, style plate | **COMPLETE — awaiting approval** |
| 4 | Animatic, temp narration | **blocked** — see below |
| 5 | Final render, `deliver/` | blocked |

## Blockers

**1. `ELEVENLABS_API_KEY` is gone — narration cannot be recorded.**
It lived only in the running `local-video-server` process and was never written
to `.env`. That process died in the 2026-07-26 restart. It is not recoverable
from this machine. **Isaac must mint a new key at elevenlabs.io and add it to
`.env`.** Blocks Gate 4 and everything after. Gates 2 and 3 are unaffected.

Once the key exists, add it to `.env` **and verify it persists** — this is the
second time it has been lost.

**2. The GALLEY proxy is not running.** `:5412` is dead; the capability token at
`~/.config/kernel/galley-engine-token` survived. Restart before Gate 3:

```bash
node tools/engine.mjs
```

**3. ffmpeg still has no libass or libfreetype** (unchanged by the OS upgrade —
verified). All burned-in text goes through ImageMagick cards composited with
`overlay`. See `docs/video/CAPTION-SPEC.md` Finding 6 and
`tools/shorts/cut-verticals.py`.

## Image generation — routing directive (2026-07-26)

Binding for this episode. **Preflight at Gate 3:** the previous film used
`fal-ai/nano-banana-2/edit`; `nano-banana-pro` has not yet been confirmed
present in the fal catalog from this machine (proxy down). Check before
budgeting.

| Use | Endpoint |
|---|---|
| Drafts | `fal-ai/nano-banana-2` |
| First final-quality stills | `fal-ai/nano-banana-pro` |
| **All production frames** | `fal-ai/nano-banana-pro/edit` |

Every production frame passes, as references:
1. the canonical protagonist character sheet,
2. the kernel.chat visual-style reference,
3. the previous approved frame where continuity matters.

**Never rebuild the protagonist from text alone.** Preserve face, head shape,
proportions, clothing, line weight, palette.

2K output. 16:9 for the film, 9:16 for shorts. **No text inside generated
images** — all typography is composited afterwards.

Carried over from the last film and still true:
- `params.image_urls` must be an **array nested inside `params`**. At the top
  level the proxy drops it and fal bills before failing asynchronously.
- Poll `/v1/videos/jobs/<id>` for every job kind, images included.
- Use `fileURLToPath`, never `.pathname` — the latter percent-encodes the
  space in "blog design" and writes to a literal `blog%20design/`.

## Cost

Nothing spent. No paid generation without Isaac's explicit approval —
standing rule. Estimate at Gate 3, once frame count and endpoint are fixed.
The last film cost $18.72 across three builds; a clean single build of ~60
frames should be well under that, but `nano-banana-pro` pricing is unknown
until the catalog is reachable.

## Do not touch

`videos/polyvagal/` is finished and shipped. Read it; never write to it.
`videos/interoception/` holds a parked editorial package for a different
episode (six files, no production). Leave it.

## Gate 3 preflight — 2026-07-26

**Fixed a real bug in `tools/engine.mjs`.** Line 9 documented that the video
server reads `FAL_KEY` via `--env-file`; line 16 spawned it without the flag.
`node tools/engine.mjs` therefore always produced a keyless server and every
paid route failed. Added the flag; server now reports `key loaded`. This has
presumably been broken for as long as the comment has been there — the last
film worked because it was launched directly, not through `engine.mjs`.

**Endpoint preflight — inconclusive, needs a paid test.**

| Finding | Detail |
|---|---|
| Route | `/v1/images/estimate` and `/v1/images/fal` — **not** `/v1/estimate` |
| Catalog | 110 fal endpoints, **no nano-banana of any version** — including `nano-banana-2/edit`, which the last film used successfully. The catalog is curated and is **not authoritative** for `/v1/images/fal`, which passes endpoints through |
| Pricing | `nano-banana-pro/edit` **and** `nano-banana-2/edit` both return `usd: null`, `quoteToken: null` |

**Consequence:** the proxy cannot price either endpoint, so it cannot issue a
quote token and **cannot pre-cost the build**. Whether the $10/day spend limit
applies to unpriced endpoints needs checking before any batch runs — an
unpriced route that bypasses the cap is the worst possible combination.

**RESOLVED — from fal's public model page, at no cost.** I asked for a paid
validation image before checking the free source. The docs answered every
question:

| | |
|---|---|
| Endpoint | `fal-ai/nano-banana-pro/edit` **exists** (Google Gemini 3 Pro Image) |
| Price | **$0.15/image** at 1K and 2K · $0.30 at 4K |
| Reference images | **up to 14** — our 3-reference scheme is well inside |
| Aspect ratios | 16:9 and 9:16 both supported |
| Consistency | holds resemblance for up to 5 people |

**2K costs the same as 1K.** Only 4K doubles. The directive's 2K target is free
of penalty — take it.

### Budget, and a conflict with the spend cap

| Item | Count | Cost |
|---|---|---|
| Character sheet + style reference | 6 | $0.90 |
| Production frames @ 2K | 60 | $9.00 |
| Reshoot allowance (~25%) | 15 | $2.25 |
| Shorts-specific 9:16 frames | 6 | $0.90 |
| **Total** | **87** | **≈ $13.05** |

**This exceeds the proxy's $10.00/day spend limit.** Three ways through:

1. **Split across two days** — character sheet + Acts I–V on day one, rest on
   day two. No config change, no risk. *Recommended.*
2. **Raise the cap** for the build, then put it back.
3. **Draft on `nano-banana-2`** per the routing directive and promote only
   approved frames to pro/edit. Cheapest, but doubles the review pass.

Whichever is chosen, note the earlier finding still stands: the proxy returns
`usd: null` for these endpoints, so **it cannot price them and cannot gate
them**. The $10 cap may not actually fire on an unpriced route. Verify that
before trusting it as a backstop — real cost is now known to be $0.15/image, so
budget by frame count, not by the cap.

## Gate 3 — canonical character sheet LOCKED (2026-07-26)

**`assets/character-sheet-v2.png`** — front / three-quarter / profile, neutral
expression, no red, no lettering. Generated on `fal-ai/nano-banana-pro/edit`
at 2K 16:9, conditioned on the polyvagal hero so the strand keeps one character.

**Durable fal URL — pass this as reference #1 on every production frame:**
```
https://v3b.fal.media/files/b/0aa3db9d/U3r7UQmtGuB_4TO6vWphS_3036eLDG.png
```

Superseded: `character-sheet.png` (v1) returned three forward-facing emotional
states with a red head — "character sheet" reads to the model as *expression*
variations. Describe rotation as a physical fact per figure ("rotated 90
degrees, only ONE eye visible, the nose line breaks the edge of the face") and
forbid expression change. Kept for reference; do not use as a conditioning input.

Known cosmetic flaw in v2: the profile figure's legs merge into one line.
Irrelevant for conditioning — head, face and proportions are what carry.

**Spend so far: $0.30** (2 images @ $0.15). Balance $43.54.

### Four bugs fixed getting here — all would have blocked any batch

1. `tools/engine.mjs` spawned the video server without `--env-file`, so it
   always started with **no FAL_KEY**. A comment claimed otherwise.
2. **Catalog is cached per category.** `nano-banana-*/edit` lives under
   `image-to-image`; until that category is fetched once, `catalogEntry()`
   misses, `usdPerImage` is null, no quote token issues, and `/v1/images/fal`
   returns **409 "A valid estimate quote is required"**. `generate.mjs` now
   warms it first — this is the single most important line in the file.
3. Submission needs a `quoteToken` from **this endpoint's own** estimate,
   and estimate only issues one when a non-empty `prompt` is in the body.
4. The proxy's terminal job state is **`done`**, not `succeeded`/`completed`,
   and the result URL is **`sourceUrl`** (fal CDN, durable) or `imageUrl`
   (local cache, needs the server running). Prefer `sourceUrl`.


## Gate 3 complete — 2026-07-26

`assets/style-plate.png` · `FRAME-BOOK.md` (61 frames) · `SHOT-LIST.md`.

**Style plate URL — reference #2 on every production frame:**
```
https://v3b.fal.media/files/b/0aa3dbb6/UWIS-MoakJt3IsqOQD4hY_4AU01DSd.png
```

**Finding: a character reference overrides "nobody in frame."** The plate was
prompted "Completely empty of people" and came back with the protagonist in it,
because reference #1 was the character sheet. The image beat the instruction.
For pure environment plates, pass no character reference. Accepted as-is — it
doubles as the Act III reveal (`m16`) and everything else landed, including the
single red element resolving as the red mug carried over from the last film.

**Spend: $0.45** (3 images). Batch not started — awaiting approval.

Two frames to validate before any batch: **m16** (workshop, most complex) and
**m26** (the 1974 pair, where cross-frame identity is the argument).

## Gate 3 validations — 2026-07-26

**Clean environment plate — reference #2, replaces the populated one:**
```
https://v3b.fal.media/files/b/0aa3dbea/wPtgltibbZy-ymCj2sev9_Zdje7YjN.png
```

**My first diagnosis was wrong.** I blamed the character reference for the
populated plate. Regenerating with **zero references** still produced a person —
off-model and grimacing — despite the prompt insisting the room was deserted.
The real cause was the **style block's own first sentence**: *"Thin stick-figure
character with a round head and a BIG exaggerated expression"* is a standing
instruction to draw a character, applied to every frame. Anything the style
block NAMES becomes a thing that must appear. Same lesson as the opossum, one
level up. Fixed with a `STYLE_ENV` variant that drops the character clause for
people-free frames.

Also: **"tomato-red" produced a literal tomato** on the workbench. Now "flat red".

### m16 — PASS
Room is near-identical to the plate: same shelving, bench, red tape reel, set,
light pool. Protagonist on-model and shocked; two archivists working, not
looking up. No lettering. **Multi-reference conditioning (character + environment)
works and preserves the room almost exactly** — this is the technique the whole
film depends on, and it is now proven.

### m26 — FAIL, one defect
Structure correct: seated neutral figure, emphatic questioner, blank notepad,
plain beige room, no lettering. **But the questioner's hand is red.** The style
block only asked for "one red element" and the model put it on a body, which
breaks the film's colour logic.

**Fix applied — RED DISCIPLINE clause added to the style block:** red means
evidence, correction or contamination; it may only appear on a small handled
object; never on skin, hands, faces, hair or clothing; **zero red is correct and
preferred over a red body part.**

**m26 needs a reshoot with the amended block. Not yet re-run.**

### Caveat on what m26 actually tested
m26 alone cannot validate what it was chosen for. Its purpose is *cross-frame
identity* with m25 — the same questioner in two postures. That needs the pair,
with m25 generated first and passed as reference #3 to m26. Validate the pair
before trusting the technique for the five *set* groups in FRAME-BOOK.

**Spend: $1.05** (7 images). Batch not started.

## Acts I–V generated + audited — 2026-07-26

**39/39 frames, 0 failures. $5.85 batch · $7.20 of the $10.00 cap. Cap respected,
never raised.** Full per-frame record in [`BATCH-LOG.md`](BATCH-LOG.md) and
[`batch-log.json`](batch-log.json). Contact sheets: `assets/sheet1-3.png`.

**No seeds available** — the proxy neither returns nor accepts one, so frames are
not bit-reproducible. Continuity rests on reference ordering, recorded per frame.

### The three fixes, and whether they worked

| Fix | Result |
|---|---|
| 1. m26 emphatic, not angry | **Worked.** Face is neutral-pleasant, emphasis is in the lean and the raised hand. No brow, no shout, no sweat |
| 2. Hand instructions | **Mostly worked.** No dangling hooks anywhere in 39 frames. Open hands read as five fingers. Some distant hands simplify to mittens — acceptable at hold size |
| 3. Locked-camera clause | **Worked well.** The workshop is near pixel-stable across 12 frames spanning two acts |

### Audit

| Criterion | Verdict |
|---|---|
| Character identity | **Pass.** Protagonist consistent across all 39. Archivists read as a consistent second type |
| Hand anatomy | **Pass.** The m25 hook did not recur |
| Accidental lettering | **Provisional pass.** Nothing at contact-sheet scale; box labels render as blank rectangles. **Still needs a 100%-zoom pass per frame before animation** |
| Framing drift | **Pass with two exceptions** — see below |
| Scientific accuracy | **Pass.** m26 no longer implies the manipulation required aggression |
| Red discipline | **PARTIAL FAIL** — see below |

### Defect 1 — red discipline, systemic

The environment plate baked a **red tape reel onto the workbench**, so every one
of the 12 workshop frames inherits it. Frames that then add a legitimate red
evidence object — m23's correction strip, m27's scattered fragments — carry
**two reds**, and the bench reel is decorative, which is precisely what the rule
forbids.

Not a generation failure; the rule was satisfied frame by frame. The plate was
approved before RED DISCIPLINE existed and carried a violation forward into
everything conditioned on it.

Three ways out, cheapest first:
1. **Desaturate the bench reel in compositing** — one mask reused across 12
   frames, no regeneration, ~$0. *Recommended.*
2. Regenerate the plate without any red and re-run the 12 workshop frames — $1.95.
3. Accept it as workshop equipment and relax the rule to "one red *evidence*
   object", tolerating a fixed decorative red in the set. Weakest option: it
   makes red mean two things.

### Defect 2 — framing drift, two places

- **m37 → m38** genuinely drifted: different camera angle and the archivist
  changes scale. They are meant to be the same shot one beat apart. Reshoot m38
  with m37 as reference #1 — $0.15.
- **m05 / m06** sit closer to the counter than m01–m04. Not wrong (no locked
  camera was specified between them) but the kitchen anchor reads better if all
  six match. Optional.

### Not yet done

- 100%-zoom lettering pass on all 39
- Acts VI–IX (23 frames, ~$3.45) — **not started, awaiting approval**
- Nothing animated

---

# RESUME HERE — end of session 2026-07-26

## >> DECISION: ASSEMBLE IN PALMIER PRO <<

Isaac chose Palmier for assembly. **Do not use `place.py` / `edl.json`** — they
are kept only as a record of the placement analysis. Palmier owns the cut.

**Why this resolves the blocker.** My hand-rolled EDL left 9 holds over the 8s
ceiling (worst 24s) because the narration clusters and 62 frames cannot cover
the sparse stretches — m31, m53 and m37 are the worst. In Palmier you can see
those gaps on the timeline and fix them by eye, and you still have the option to
generate ~6 extra frames (~$0.90) for those passages if they read as stalls.

**Palmier traps, all paid for on the polyvagal film:**

1. **The media cache is the expensive one.** Overwriting a file and re-importing
   the same path both silently fail. **Only importing under a genuinely NEW
   filename works.** This cost three full export cycles. Version filenames.
2. `get_transcript({granularity:'segments'})` for timings — it will match the
   `segments.json` already written here from whisper.
3. **Captions: `add_texts`, never `add_captions`.** `maxWords` cannot slow auto
   captions — 84 cards at 3, 5 and 10 alike. Build cards from the locked script.
4. `fontSize` is canvas **points**, not pixels. 52 ≈ the locked look.
5. Timeline positions are **frames**; source positions are **seconds**. Never
   multiply by fps yourself.
6. Import order: `import_media` → `add_clips` → `export_project`.

**Frames come from `frames-canonical/` only.** `frames-original-backup/` holds
uncorrected and rejected generations. `MANIFEST.json` is the authority.

Target: 1920×1080 · 30fps · H.264 · AAC · ~6:42. Frames are 2752×1536, so they
scale down.



**Branch: `galley/memory-reconsolidation`** (created clean; `fix/page-load-reliability`
is untouched and unrelated). Everything under `videos/memory-reconsolidation/`
is still untracked — nothing committed yet.

## Done

| | |
|---|---|
| Gates 1–3 | RESEARCH · CLAIMS · SCRIPT · BEAT-SHEET · FRAME-BOOK · SHOT-LIST |
| Character sheet | `assets/character-sheet-v2.png` — reference #1 |
| Environment plate | `assets/style-plate-empty.png` — reference #2 |
| Acts I–V | 39 frames, audited at 100%, 5 reshot, 0 FAIL remaining |
| Acts VI–IX | running at session end — check `ls frames-canonical \| wc -l`, target **62** |
| Narration | `audio/narration.mp3` — 6:42, Chris @ 0.75 |
| Compositing fix | bench tape reel desaturated on 14 workshop frames |

**Spend ≈ $11.55.** Note the batch log over-reports: it adds `SPENT_TODAY` to a
running total that already includes the Acts I–V batch. Read the real figure by
summing `usd` in `batch-log.json`, not from stdout.

## Do these first, in order

**1. Narration verified — NOT blocking. Cleared 2026-07-26.**
I flagged this as a likely defect and was wrong. The extractor pulls exactly 88
lines, first line "You remember the kitchen perfectly", last line "But useful is
not the same thing as exact", with no commentary, no table rows and no register-
audit text. The "798 words" figure in SCRIPT.md was my own estimate written when
drafting, never counted; the real script is **906 words**. SCRIPT.md is corrected.

906 words at ~135 wpm gives 6:42, which matches the recorded audio. The film runs
**~40s over the 5–6 minute target** — trim in Act IV (the family-story beat is the
most compressible) or accept 6:42.

**2. Transcript → segments.json**, same shape as `videos/polyvagal/segments.json`
(`{fps, segments: [[startFrame, endFrame, text], …]}`).

**3. Content-lock placement.** Adapt `videos/polyvagal/place-v5.py`. Two bugs
that bit there and will bite again:
- **Never advance a monotonic cursor** through segments — match every frame
  independently against all segments, then sort by resulting start time. Frame
  ids do not sort in narration order once reshoots are appended.
- Use slack-bounded snapping, `slack = max(0, MAX - even_spacing)`, or the last
  frame strands.
- **Audit coverage before export**: every narration line must have a matched
  frame, and any hold over **8.0s** fails the build.

**4. Assemble** 1920×1080 · 30fps · H.264 · AAC. Frames are 2752×1536, so scale
down. Source frames from **`frames-canonical/` only** — `frames-original-backup/`
holds uncorrected and rejected generations and must never reach assembly.
`MANIFEST.json` is the authority.

**5. SRT**, then **3 shorts** via `tools/shorts/cut-verticals.py` with a
`shorts.json` here. Captions are ImageMagick cards composited with ffmpeg
`overlay` — this machine's ffmpeg has **no libass and no libfreetype**. Wrap on
**measured** width, never character count. Safe-box centre is x=500, not 540.

**6. Thumbnails**, **deliver/**, then **watch the film in motion** before calling
it done.

## Still open from the audit — judgement calls, not defects

`m10` two reds + jigsaw is a forbidden symbol · `m30` five reds · `m31`
protagonist repeats m29's pose · `m35` intrusion direction looks inverted.
See `FULL-RES-AUDIT.md`.

## Secrets

`ELEVENLABS_API_KEY` lives in `~/Desktop/clAUDE_API/creative.rtf`, **outside the
repo**. `narrate.mjs` reads it from the environment only:

```
ELEVENLABS_API_KEY="$(textutil -convert txt -stdout ~/Desktop/clAUDE_API/creative.rtf | grep -oE 'sk_[a-zA-Z0-9_-]{20,}' | head -1)" node videos/memory-reconsolidation/narrate.mjs
```

Never write it to `.env`, never print it, never commit `creative.rtf`.
**Outstanding: rotate the Google API key and the two Higgsfield keys** — an
earlier grep of that file printed them into a session transcript.

## Server

Started with a raised cap for this run:
`FAL_DAILY_SPEND_LIMIT=25 node tools/engine.mjs`. **Put it back to the default
$10 once the film is finished.** `engine.mjs` was also fixed this session — it
spawned the video server without `--env-file`, so it had no `FAL_KEY` at all.
