# THE THIRD THING — status

## Ready to assemble

| Asset | Where | State |
|---|---|---|
| Script v5 (locked) | `SCRIPT-V5.md` | 606 words, Flesch 87.6, 0 sentences >20w |
| Narration | `voice/vo-v5.mp3` | **4:35**, −26.0dB, Chris @ speed 0.75 |
| Frames | `frames/v01…v50.png` | **50**, all passed gate, 5 reshot |
| Frame defs + line locks | `frames-v5.mjs` | every entry has `line` + `kind` |

Shot mix as built: 64% literal · 14% objection · 10% physics · 10% chair · 2% flourish.

## Remaining: assembly only

1. New timeline in the `polyvagal` project, 16:9 1080p 30fps.
2. Import `voice/vo-v5.mp3` + `frames/v*.png`; place audio at 0.
3. `get_transcript({granularity:'segments'})`.
4. **Content-lock every frame** — match each entry's `line` to its segment by
   text similarity, independently (see below). Never distribute evenly.
5. Re-time: floor 54 frames (1.8s), ceiling 240 (8.0s), max drift ~45 frames.
6. Export, then verify by sampling EVERY cut against its line — not a dozen.

Working scripts from the v2 build are in the session scratchpad
(`place57.py`, `retime.py`) and port directly — only `SEG`/`REF` change.

## Hard-won rules — do not relearn these

- **Match each frame independently against ALL segments, then sort by result.**
  A forward-walking cursor assumes ids sort in narration order; that broke the
  moment fill frames were appended and pinned four of them to the last segment.
- **Even distribution between sparse anchors is what lost the viewer in v1.**
  71 of 86 frames floated and every image landed a beat early for 7 minutes.
- **Reshoots must go to a NEW FILENAME.** Overwriting the file fails; re-importing
  the same path fails; Palmier caches its decode by source path. Cost 3 exports.
- **Poll route is `/v1/videos/jobs/<id>` for every kind, images included.**
- **`params.image_urls` must nest inside `params`** — top level is dropped and
  the job is rejected AFTER billing. MCP production tools can't express arrays.
- **Use `fileURLToPath`, never `.pathname`** — the space in "blog design" gets
  percent-encoded and writes land in a literal `blog%20design/` directory.
- **Never name an example object in the style block.** An opossum offered once
  as an illustration was drawn into 7 of 10 frames.
- **Motion in a scene description invites sound-effect text.** "Falls and
  smashes" → "crash"; a swinging door → "WOBBLE". Stage the aftermath instead.
- **ELEVENLABS_API_KEY is not in `.env`** — only in the running video-server
  process. Recover without printing:
  `export $(ps eww $(pgrep -f local-video-server.mjs | head -1) | tr ' ' '\n' | grep ^ELEVENLABS_API_KEY=)`

## Why v5 exists (v1 and v2 both shipped and both failed)

- **v1** 7:17 / 86 frames — scenes illustrated the *concept*, not the experience;
  only 15 frames anchored, 71 drifted. Viewer got lost.
- **v2** 5:06 / 61 frames — content-locked and funnier, but every image was a
  *visual pun on the words* rather than an explanation. Still didn't make sense.
- **v5** 4:35 / 50 frames — script rewritten **for the ear** (signposting,
  example-before-term, deliberate repetition, no orphaned metaphors); narrator
  now pre-empts the viewer's objections so there is conflict and a character;
  and the three states are ONE RECURRING SHOT — same chair, three ways (`v22`).

## Spend

v1 $8.72 · v2 $5.04 · v5 $4.40 · **total $18.16**

---

## FINAL — shipped 2026-07-25

**Master:** `output/publish/the-third-thing.mp4` — 4:35, 1920×1080, 8258
frames, 81MB, −26.0 dB. 57 clips, 4.83s average (floor 1.8s, ceiling 11.6s).

**Delivery kit: [`deliver/`](deliver/)** — master + SRT + isolated VO + two
thumbnails + three captioned verticals + all platform copy. See
[`deliver/README.md`](deliver/README.md). Nothing there needs a re-render.

**Verticals** were cut with [`tools/shorts/cut-verticals.py`](../../tools/shorts/cut-verticals.py),
not Palmier — this machine's ffmpeg has no libass/libfreetype, so captions are
ImageMagick cards composited via `overlay`. Method in
[`docs/video/CAPTION-SPEC.md`](../../docs/video/CAPTION-SPEC.md) Finding 6.

**Spend:** $18.72 this film (v1 $8.72 · v2 $5.04 · v5 $4.96).

**Open defects** (reviewed from contact sheets, not in motion — motion-only
defects may remain):

1. `w01` @ 3:49 renders **CLATTER** twice. Reshoot.
2. `v17` @ 1:13 shows an **empty chair** on "And here's the third" — inverts
   the meaning and breaks the three-chair anchor. Reshoot.
3. Holds past the 8s ceiling: v03 11.6s, v41 10.1s, w02 9.9s, v09/v48 8.0s.
   Re-time pass.

Lessons generalised into
[`docs/video/PRODUCTION-PLAYBOOK.md`](../../docs/video/PRODUCTION-PLAYBOOK.md) §10.

## Recovered from scratchpad before the 2026-07-25 restart

These were only in a session temp dir and would have been lost:

- `edl-v5.json` — the shipped edit decision list: 57 entries, each a
  `mediaRef` + `startFrame`/`endFrame`. This IS the cut. Re-assembling the film
  without it means redoing the placement pass.
- `place-v5.py` — content-lock + re-time. Holds the frame-id → media-ref map
  and the slack-bounded snapping (`MIN,MAX,DRIFT = 54,240,45`).
- `extract-cuts.py` / `make-contact-sheets.py` — the frame-by-frame review rig.
- `segments.json` — the 92 narration segments with frame timings, also used by
  `tools/shorts/cut-verticals.py`.
