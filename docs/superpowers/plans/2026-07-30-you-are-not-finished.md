# You Are Not Finished — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a ~5:30 kernel.chat film on the end-of-history illusion, plus three captioned verticals, hitting a measured voice spec and without repeating the frame-geometry and character-drift defects of *Why Humans Need Rituals*.

**Architecture:** Script is written and gated locally against a measured register profile before any art exists. A locked character reference is generated and approved before batch one. Images come from Gemini in the browser (free on the Pro account); narration from ElevenLabs in the browser (so `speed` is actually settable). Assembly follows the HyperFrames `build-literal-final.mjs` pattern already proven on the last film. Every stage ends in a measurement, not an opinion.

**Tech Stack:** HyperFrames 0.7.83 (pinned), ffmpeg (NO libass, NO libfreetype — see Global Constraints), ImageMagick 7, Python 3, Node 20+, Gemini web UI, ElevenLabs web UI.

## Global Constraints

- Project root: `videos/you-are-not-finished/`
- Canvas: **1920×1080 @ 30fps** (see Resolution below). One frame geometry for the entire film, decided in Task 4 and never varied.
- Paper colour: `#F4E8C8`. Ink: `#1F1E1D`. Accent: tomato `#E24E1B`.
- **No emojis** in code or user-visible copy (CLAUDE.md rule 4).
- Magazine vocabulary in any user-visible copy: issue / feature / spread / folio / monument / colophon. Never dashboard / panel / card / widget / modal. Never name "POPEYE" on the site.
- This machine's ffmpeg has **no libass and no libfreetype**: `subtitles=`, `ass=`, `drawtext=` are all unavailable. Caption cards are ImageMagick composites. `magick -list font` is empty — always pass the font by path.
- Caption font path: `/System/Library/Fonts/Avenir Next Condensed.ttc`
- Voice targets (hard gate, Task 2): syllables/word ≤1.52 · 3+ syllable words ≤13% · "you" ≥10 per 1,000 words (floor only) · Flesch reading ease ≥62 · words/sentence ~16
- Narration pace target: **145–155 wpm overall, no single line above 165 wpm**
- Loudness target: **−18 LUFS** integrated on the narration bed (matches last film)
- `videos/**` is gitignored (`.gitignore:147`). Plan artifacts under `docs/` ARE tracked.

---

### Task 1: Scaffold the project

**Files:**
- Create: `videos/you-are-not-finished/package.json`
- Create: `videos/you-are-not-finished/meta.json`
- Create: `videos/you-are-not-finished/BRIEF.md`

**Interfaces:**
- Consumes: nothing
- Produces: project root at `videos/you-are-not-finished/`, referenced by every later task

- [ ] **Step 1: Create the directory tree**

```bash
cd "/Users/isaachernandez/blog design"
mkdir -p videos/you-are-not-finished/{production,compositions/literal,public/images/literal-16x9,audio,renders,deliver/shorts}
```

- [ ] **Step 2: Write package.json with the pinned CLI**

```json
{
  "name": "you-are-not-finished",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "npx --yes hyperframes@0.7.83 preview",
    "check": "npx --yes hyperframes@0.7.83 check",
    "render": "npx --yes hyperframes@0.7.83 render"
  }
}
```

Pin matches the last film so re-renders stay reproducible.

- [ ] **Step 3: Write meta.json**

```json
{ "id": "you-are-not-finished", "name": "You Are Not Finished" }
```

- [ ] **Step 4: Copy BRIEF.md from the spec**

```bash
cp docs/superpowers/specs/2026-07-30-end-of-history-illusion-design.md \
   videos/you-are-not-finished/BRIEF.md
```

- [ ] **Step 5: Verify**

```bash
ls videos/you-are-not-finished
```
Expected: `BRIEF.md audio compositions deliver meta.json package.json production public renders`

---

### Task 2: Write the script and pass the voice gate

This is the task that justifies the whole plan. Do not proceed to art until it passes.

**Files:**
- Create: `videos/you-are-not-finished/SCRIPT.md` (prose, for humans)
- Create: `videos/you-are-not-finished/script.txt` (bare narration text, for measurement)

**Interfaces:**
- Consumes: the six-act structure in `BRIEF.md`
- Produces: `script.txt` — the locked narration. Every later stage (frame book, VO, captions) derives from this file and never re-words it.

- [ ] **Step 1: Draft the six acts to the structure in BRIEF.md**

Act 1 The receipt (0:00–1:10) · Act 2 The finding (1:10–2:30) · Act 3 Why it happens (2:30–3:30) · Act 4 The objection (3:30–4:30) · Act 5 What it costs (4:30–5:10) · Act 6 Close (5:10–5:30).

Target ~820 words total (5:30 at 150 wpm).

Writing rules, in force for every line:

1. **Second person throughout.** "You" at least 10 times per 1,000 words, no upper limit. The last film said it zero times in 1,043 words. This is the defect being fixed.
2. **Spend polysyllables on jokes only.** The formal-diction comedy ("appropriate moral seriousness", "an office that has technically ceased to exist") is the house voice and must survive. Explanatory connective tissue gets plain words. Density is only a problem where it is doing no comic work.
3. **Signpost before you explain.** Name the thing, then explain it. Never the reverse.
4. **Example before term.** Concrete case first, label second.
5. **No orphan metaphors** — any image introduced gets used again or cut.

Verified facts available (do not exceed these):
- Quoidbach, Gilbert & Wilson, *Science* 339(6115):96–98, 4 January 2013
- Over 19,000 participants, ages 18–68, six investigations
- Domains: personality traits, core values, preferences
- Willingness to pay: **$129** for today's favourite band in ten years vs **$80** for the band loved ten years ago playing today
- Objections: cross-sectional not longitudinal; autobiographical memory; and if direction of change is unpredictable, "no change" is the rational prediction

- [ ] **Step 2: Extract the bare narration to script.txt**

`script.txt` contains narration only — no act headings, no stage directions, no image notes. The profiler measures what is spoken.

- [ ] **Step 3: Run the voice gate**

```bash
cd "/Users/isaachernandez/blog design"
python3 tools/video/register-profile.py \
  "DRAFT" "videos/you-are-not-finished/script.txt" \
  "RITUALS (last film)" "/tmp/rituals-script.txt"
```

If `/tmp/rituals-script.txt` is absent, regenerate it:

```bash
python3 -c "
import json
d=json.load(open('videos/why-humans-need-rituals/LITERAL_EDIT_MAP.json'))
seen=[]
[seen.append(s['cue']) for f in d['frames'] for s in f['shots'] if not seen or seen[-1]!=s['cue']]
open('/tmp/rituals-script.txt','w').write(' '.join(seen))
"
```

- [ ] **Step 4: Check every metric against the gate**

Expected on the DRAFT block, all five simultaneously:

| Metric | Must be |
|---|---|
| syllables/word | ≤ 1.52 |
| 3+ syllable words | ≤ 13.0% |
| "you" per 1k words | ≥ 10.0 (floor, no ceiling) |
| Flesch reading ease | ≥ 62.0 |
| words/sentence | 14 – 18 |

If any metric misses, revise and re-run Step 3. Do NOT proceed on a near miss — this gate is cheap and the failure it prevents is a whole rebuild.

- [ ] **Step 5: Record the passing numbers in SCRIPT.md**

Paste the profiler output verbatim under a `## Voice gate — PASSED` heading, with the date. Later sessions need the evidence, not the claim.

---

### Task 3: Write the frame book

**Files:**
- Create: `videos/you-are-not-finished/STORYBOARD.md`

**Interfaces:**
- Consumes: `script.txt` from Task 2
- Produces: one numbered frame per beat, each with `id`, the narration line it sits under, and an image prompt. Task 5 generates directly from these prompts.

- [ ] **Step 1: Break the script into beats**

Target ~3.0s average hold. At 5:30 that is roughly 100–110 frames. Never exceed 8s on a still — past that a static image dies.

Hold vocabulary: Snap 1.0–2.0s (punchline) · Quick 1.5–2.5s (escalating runs) · Setup 3.0–5.0s (read the situation) · Breath 5.0–8.0s (after a big beat).

- [ ] **Step 2: Write one frame entry per beat**

Each entry, exactly this shape:

```markdown
### 07b
**Line:** "You would pay a hundred and twenty-nine dollars to see them in ten years."
**Hold:** 2.5s (Quick)
**Image:** The character at a ticket window, sliding a thick stack of notes under
the glass. The clerk is the cyan companion. A calendar on the wall behind reads
ten years ahead. Flat mid-century comic line art, cream paper, halftone shading.
```

Rules, carried from PRODUCTION-PLAYBOOK §10.3:
- Each frame is **one specific gag with a specific consequence**, not an illustration of the topic
- The image explains, it does not pun on the words
- Every image different — a repeat reads as a budget, not a motif
- No lettering inside images. Any text on screen is added at assembly, never generated

- [ ] **Step 3: Verify coverage**

Every sentence in `script.txt` must be covered by at least one frame, and no frame may reference a line that is not in `script.txt`. Read the two side by side and confirm.

---

### Task 4: Lock the character reference

**This gate exists because the last film's companion silently became a different character mid-film, and 2026-07-30 proved there is no cheap repair.** See PRODUCTION-PLAYBOOK §10.8.

**Files:**
- Create: `videos/you-are-not-finished/public/images/REFERENCE.png`
- Create: `videos/you-are-not-finished/STYLE.md`

**Interfaces:**
- Consumes: nothing
- Produces: `REFERENCE.png` (2752x1536 native) — pasted into every Gemini generation session in Task 5, and the thing every frame is checked against

- [ ] **Step 1: Write the style block into STYLE.md**

Record exactly: palette (`#F4E8C8` paper, `#1F1E1D` ink, `#E24E1B` accent, cyan companion), line weight, halftone shading, flat mid-century comic register, and **full-bleed to all four edges — no painted margins, no inset panel, no border**.

That last clause is the frame-geometry decision. It is made here, once.

- [ ] **Step 2: Generate a character sheet in Gemini**

Open `https://gemini.google.com/app` in the browser. Prompt for a single sheet showing the two recurring characters — the person and the cyan companion — in front, three-quarter and side view, plus three expressions each, on the cream paper, full bleed.

- [ ] **Step 3: Save it and verify it is full bleed**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished/public/images"
magick REFERENCE.png -fuzz 4% -format "%@\n" info:
magick REFERENCE.png -format "%wx%h\n" info:
```
Expected: offset `+0+0` (or within 8px). Any larger offset means the generator painted a margin — regenerate before proceeding.

- [ ] **Step 4: Approval gate**

Show `REFERENCE.png` to Isaac and get an explicit yes before generating a single frame. Everything downstream inherits this.

---

### Task 5: Generate the frames, in audited batches

**Files:**
- Create: `videos/you-are-not-finished/public/images/literal-16x9/*.png`
- Create: `videos/you-are-not-finished/production/frame-audit.sh`

**Interfaces:**
- Consumes: `STORYBOARD.md` prompts, `REFERENCE.png`
- Produces: one 1920×1080 PNG per frame, named `<id>-final.png` matching the storyboard ids

- [ ] **Step 1: Write the audit script**

```bash
#!/usr/bin/env bash
# Frame-edge audit. PRODUCTION-PLAYBOOK §10.7 — a generator handed a 1920x1080
# canvas will not necessarily draw to the edge of it.
cd "$(dirname "$0")/../public/images/literal-16x9" || exit 1
fail=0
for f in *.png; do
  bb=$(magick "$f" -fuzz 4% -format "%@" info:)
  off=${bb##*+}; off=${bb#*+}; off=${off%+*}
  size=$(magick "$f" -format "%wx%h" info:)
  if [ "$size" != "1920x1080" ]; then echo "  WRONG SIZE $f  $size"; fail=1; fi
  if [ "$off" -gt 8 ] 2>/dev/null; then echo "  PAINTED MARGIN $f  x-offset ${off}px"; fail=1; fi
done
[ "$fail" -eq 0 ] && echo "  all frames full-bleed 1920x1080" || echo "  AUDIT FAILED"
exit $fail
```

```bash
chmod +x videos/you-are-not-finished/production/frame-audit.sh
```

- [ ] **Step 2: Generate in batches of 10**

For each batch, in the Gemini browser tab: paste `REFERENCE.png` first, then the batch's prompts. Keeping the reference in-conversation is what holds the character across a long session.

Download each result to `public/images/literal-16x9/<id>-final.png`.

- [ ] **Step 3: Audit each batch before generating the next**

```bash
./videos/you-are-not-finished/production/frame-audit.sh
```
Expected: `all frames full-bleed 1920x1080`

If a frame fails, regenerate it now. Do not accumulate debt — the last film's defect was discovered only in the master.

- [ ] **Step 4: Character check each batch**

Build a contact sheet of the batch beside the reference and confirm the characters have not drifted:

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished/public/images/literal-16x9"
ffmpeg -v error -pattern_type glob -i "*.png" \
  -vf "scale=400:-1,tile=5x2:padding=4:color=0xE24E1B" -frames:v 1 -y /tmp/batch.png
```

Read `/tmp/batch.png`. If the companion's construction has changed at all, regenerate before continuing.

---

### Task 6: Record the narration

**Files:**
- Create: `videos/you-are-not-finished/audio/narration.mp3`
- Create: `videos/you-are-not-finished/audio/manifest.json`

**Interfaces:**
- Consumes: `script.txt` (verbatim — never re-worded for the microphone)
- Produces: `narration.mp3` plus per-line durations that Task 7 turns into cue timings

- [ ] **Step 1: Record in the ElevenLabs browser UI**

Voice **Chris** (`iP95p4xoKVk53GoZ742B`), model `eleven_multilingual_v2`, stability 0.5, similarity 0.75.

Set **speed 0.9**. The last film ran at speed 1.0 and delivered a 106–183 wpm spread; the fastest passages were the second act and the closing payoff. Driving the UI directly is the reason we can set this at all — the local proxy does not forward `speed`.

Record one file per act, six files, into `audio/parts/`.

- [ ] **Step 2: Measure the pace before accepting**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
for f in audio/parts/*.mp3; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "$f $d"
done
```

Compute words ÷ duration × 60 per act.
Expected: every act between **145 and 165 wpm**. Overall 145–155.

Any act outside the band gets re-recorded at an adjusted speed. This is the check the last film never ran.

- [ ] **Step 3: Concatenate and normalise**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
printf "file '%s'\n" audio/parts/*.mp3 > /tmp/vo.txt
ffmpeg -v error -f concat -safe 0 -i /tmp/vo.txt \
  -af loudnorm=I=-18:TP=-1.5:LRA=11 -y audio/narration.mp3
```

- [ ] **Step 4: Verify loudness**

```bash
ffmpeg -hide_banner -nostats -i audio/narration.mp3 -af ebur128 -f null /dev/null 2>&1 | grep -A3 Integrated
```
Expected: integrated within ±1 LUFS of −18.

---

### Task 7: Build the edit map

**Files:**
- Create: `videos/you-are-not-finished/LITERAL_EDIT_MAP.json`
- Create: `videos/you-are-not-finished/production/build-map.mjs`

**Interfaces:**
- Consumes: `STORYBOARD.md`, `audio/manifest.json`
- Produces: `LITERAL_EDIT_MAP.json` with the exact shape the last film used — `{version, source, duration, cutCount, exactClauseTiming, frames[]}`, each frame `{frame, label, start, end, duration, shots[]}`, each shot `{id, start, end, duration, cue, shot, image}`.

That shape is load-bearing: `tools/shorts/build-segments.py` reads `frames[].shots[].cue/start/end`, and the assembly script reads `shots[].image`.

- [ ] **Step 1: Write build-map.mjs**

Model it on `videos/why-humans-need-rituals/production/build-literal-map.mjs`. Read that file first.

- [ ] **Step 2: Generate and validate**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
node production/build-map.mjs
python3 -c "
import json
d=json.load(open('LITERAL_EDIT_MAP.json'))
shots=[s for f in d['frames'] for s in f['shots']]
print('frames',len(d['frames']),'shots',len(shots),'duration',d['duration'])
assert all('cue' in s and 'image' in s for s in shots), 'shot missing cue or image'
gaps=[(a['end'],b['start']) for a,b in zip(shots,shots[1:]) if abs(a['end']-b['start'])>0.001]
print('timeline gaps:',len(gaps))
assert not gaps, gaps[:3]
print('OK')
"
```
Expected: `OK`, and duration within 2s of the narration duration.

---

### Task 8: Assemble and render

**Files:**
- Create: `videos/you-are-not-finished/production/build-final.mjs`
- Create: `videos/you-are-not-finished/index.html` (generated)
- Create: `videos/you-are-not-finished/compositions/literal/*.html` (generated)

**Interfaces:**
- Consumes: `LITERAL_EDIT_MAP.json`, the PNGs, `audio/narration.mp3`
- Produces: a rendered master in `renders/`

- [ ] **Step 1: Write build-final.mjs**

Model on `videos/why-humans-need-rituals/production/build-literal-final.mjs`. Read it first. Keep `background: #f4e8c8` on the root and every scene container — that is what makes a pixels-only correction possible later without touching HTML.

- [ ] **Step 2: Build and check**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
node production/build-final.mjs
npm run check
```
Expected: no errors. Review warnings before rendering.

- [ ] **Step 3: Render**

```bash
npm run render
```
Run in background — roughly 5 minutes for 5:30 at 30fps. Expected: a file in `renders/` with duration matching the edit map.

- [ ] **Step 4: Verify the master**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
M=$(ls -t renders/*.mp4 | head -1)
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration -of default=nw=1 "$M"
ffmpeg -hide_banner -nostats -i "$M" -af ebur128 -f null /dev/null 2>&1 | grep -A3 Integrated
```
Expected: 1920×1080, 30/1, duration 5:15–5:45, integrated loudness within ±1 LUFS of −18.

---

### Task 9: Contact-sheet QC

**Files:**
- Create: `videos/you-are-not-finished/production/qa/` (sheets)

**Interfaces:**
- Consumes: the rendered master
- Produces: a pass/fail judgement recorded in `SCRATCHPAD.md`

- [ ] **Step 1: Build the sheets**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
mkdir -p production/qa
M=$(ls -t renders/*.mp4 | head -1)
for i in 0 1 2; do
  ffmpeg -v error -ss $((i*120)) -t 120 -i "$M" \
    -vf "fps=1/7,scale=460:-1,tile=4x4:padding=6:color=0x222222" \
    -frames:v 1 -y production/qa/sheet$i.png
done
```

- [ ] **Step 2: Read all three sheets and check**

- No repeated image
- No frame with a painted margin (the edge should be identical on every tile)
- The companion is the same character on the first sheet and the last
- No lettering baked into any image

- [ ] **Step 3: State the limit**

Record explicitly, every time: *a contact sheet cannot catch anything that exists only in motion.* Then watch the film end to end.

---

### Task 10: Cut the three verticals

**Files:**
- Create: `videos/you-are-not-finished/segments.json`
- Create: `videos/you-are-not-finished/shorts.json`
- Create: `videos/you-are-not-finished/deliver/shorts/*.mp4` + `*.srt`

**Interfaces:**
- Consumes: `LITERAL_EDIT_MAP.json`, the rendered master
- Produces: three 1080×1920 captioned verticals with SRT sidecars

- [ ] **Step 1: Build caption segments from the locked script**

```bash
cd "/Users/isaachernandez/blog design/videos/you-are-not-finished"
python3 ../../tools/shorts/build-segments.py LITERAL_EDIT_MAP.json segments.json 30
```
Expected: `cards under 1.1s: 0`, longest card ≤46 chars, no "could not merge" lines.

Never use ASR for these. The cue text is the locked script.

- [ ] **Step 2: Write shorts.json**

```json
{
  "master": "renders/<the-master>.mp4",
  "segments": "segments.json",
  "out": "deliver/shorts",
  "shorts": [
    { "name": "01-you-have-changed",  "from": 0,    "to": 1200, "kicker": "YOU HAVE CHANGED" },
    { "name": "02-nineteen-thousand", "from": 2100, "to": 3300, "kicker": "AT EVERY AGE" },
    { "name": "03-a-hundred-and-twenty-nine", "from": 8100, "to": 9200, "kicker": "$129 VERSUS $80" }
  ]
}
```

`from`/`to` are frame numbers at 30fps. Adjust to the real act boundaries in `LITERAL_EDIT_MAP.json` once it exists. Each short must open on its hook inside 3.0s.

**Do not set `pictureY`** — this film is full-bleed 16:9, so the tool's default of 380 is correct. That key exists for 3:2 sources only.

- [ ] **Step 3: Cut**

```bash
python3 ../../tools/shorts/cut-verticals.py shorts.json
```
Expected: three `OK` lines and **no `shrunk to Npt` lines**. A shrink means a caption broke the locked 76pt look — fix the card budget, do not accept it.

- [ ] **Step 4: Verify safe zones**

```bash
cd deliver/shorts
for f in *.mp4; do
  ffmpeg -v error -ss 5 -i "$f" -frames:v 1 -y /tmp/sz.png
  echo "$f  caption bbox: $(magick /tmp/sz.png -crop 1080x920+0+1000 +repage -fuzz 12% -trim -format '%wx%h%O' info:)"
done
```

Convert each bbox to absolute coordinates and confirm everything sits inside **x 60→940, y 130→1436**. Add 1000 to the reported y offset.

- [ ] **Step 5: Check the SRTs**

```bash
grep -l -- "-1:59" *.srt || echo "no negative timecodes"
```
Expected: `no negative timecodes`.

- [ ] **Step 6: Check on a phone**

Post one short as unlisted and look at it on an actual phone with the platform chrome drawn over it. The `centerY` defect that cost a rebuild was invisible in the editor and invisible in the exported frame at desktop scale.

---

## Self-review

**Spec coverage.** Every section of the design maps to a task: voice spec → Task 2; six acts → Tasks 2 and 3; source material and objections → Task 2 Step 1; build pipeline → Tasks 5, 6, 8, 10; the four gates → Tasks 2, 4, 5, 9; success criteria → Tasks 8, 9, 10; out-of-scope items appear in no task, correctly.

**Placeholders.** One deliberate: the `from`/`to` frame numbers in Task 10 Step 2 cannot be known until the edit map exists, and the step says so and says how to derive them. The master filename in `shorts.json` is likewise resolved at that step. No other placeholders.

**Type consistency.** `LITERAL_EDIT_MAP.json` shape is stated once in Task 7 and consumed unchanged by Tasks 8 and 10. Image naming `<id>-final.png` is set in Task 5 and referenced by Task 7's `shots[].image`. Frame ids originate in Task 3 and are used unchanged thereafter.
