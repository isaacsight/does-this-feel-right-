# CUT-LOG — The Price of a Glance

> **Editor's chair, GALLEY. Filed incrementally 2026-07-23 (resumed pass after a
> prior editor died on an API connection error, not a work failure).** This log
> is written as the cut is built so a second crash cannot lose the record.

## Session recovery — what survived the prior pass

Opened the persisted Palmier project `the-price-of-a-glance`
(`/Users/isaachernandez/Documents/Palmier Pro/the-price-of-a-glance.palmier`).
`get_timeline` + `get_media` on entry showed the prior pass had correctly left:

- **Project settings** — 1920×1080, **fps 30** (confirmed from the timeline, not
  assumed; the Simon-quote frames 193–328 and boundary ~6327 imply 30fps and it
  checks out). totalFrames 7978.
- **Narration** — all seven VO stems on A1 (trackId `620EFBAB`) at the SOUND-BOOK
  measured boundaries: I 0–917, II 917–1924, III 1924–3426, IV 3426–4493,
  V 4493–6519, VI 6519–7096, VII 7096–7828. Verified each boundary against the
  measured table (30.56/64.13/114.20/149.77/217.29/236.52/260.90 s × 30fps). All
  correct. **KEPT — not rebuilt.**
- **Ivory matte** — one image clip (`EEB210D9`, ivory `#FAF9F6`) spanning
  [0,7978] on the single existing video track. **KEPT**, but it sat on the top
  video track; it must be the BOTTOM track. Re-ordered during the picture pass.
- **Media library** — complete: 7 narration stems, room tone + 4 design cues +
  ivory matte, 23 KEEP video clips, 7 stills (shots 06, 11, 15, 17, 23, 28, 30).

**Rebuilt from scratch:** nothing that survived. Added: all 30 shots on a picture
track, cards, room tone, design cues, grade.

## Shot inventory (media → shot)

- Video KEEP clips (23): 01,02,03,04,05,07,08,09,10,12,13,14,16,18,19,20,21,22,24,25,26,27,29
- Stills (7): 06,11,15,17,23,28,30 — shots 6/15/17/30 rejected for adding motion
  (near-still), 23 rejected (arm raise), 11/28 the red-dot spine (freeze-hold).

## Timeline map — planned (fps 30, per-act proportional fit to measured VO)

Picture tiled continuously to fill each measured act; shot durations scaled from
SHOT-BOOK slots. Freeze-splits on 18/19/22 to protect motion per cut warnings.

| Shot | In | Out | Frames | Source/handling |
|---|---:|---:|---:|---|
| 01 | 0 | 350 | 350 | video, speed-fit slow |
| 02 | 350 | 642 | 292 | video, speed-fit slow |
| 03 | 642 | 917 | 275 | video, near-locked, slow |
| 04 | 917 | 1152 | 235 | video |
| 05 | 1152 | 1390 | 238 | video (kling, hands still) |
| 06 | 1390 | 1667 | 277 | STILL, near-still + 1-2% drift |
| 07 | 1667 | 1924 | 257 | video |
| 08 | 1924 | 2146 | 222 | video; rain-marks cue |
| 09 | 2146 | 2379 | 233 | video |
| 10 | 2379 | 2601 | 222 | video vertical descent |
| 11 | 2601 | 2823 | 222 | STILL spine, freeze-hold, locked |
| 12 | 2823 | 3140 | 317 | video, clean window 0-3.3s slow; paper-edge cue |
| 13 | 3140 | 3426 | 286 | video descent, ramp ~0.53x |
| 14 | 3426 | 3614 | 188 | video |
| 15 | 3614 | 3809 | 195 | STILL, near-still + drift |
| 16 | 3809 | 4004 | 195 | video |
| 17 | 4004 | 4199 | 195 | STILL, near-still breath + drift |
| 18 | 4199 | 4493 | 294 | video HERO reach: play 0-3.3s + freeze fingertips |
| 19 | 4493 | 4994 | 501 | video: release 0-3s + freeze settle; settling cue |
| 20 | 4994 | 5403 | 409 | video delicate drift, slow |
| 21 | 5403 | 5880 | 477 | video near-still balance, slow |
| 22 | 5880 | 6519 | 639 | video HERO bloom: open 0-4s + freeze; water-bloom cue |
| 23 | 6519 | 6707 | 188 | STILL, slow push-in (judged — see QC) |
| 24 | 6707 | 6950 | 243 | video HERO pull-back |
| 25 | 6950 | 7096 | 146 | video near-still (trim tail) |
| 26 | 7096 | 7265 | 169 | video |
| 27 | 7265 | 7429 | 164 | video |
| 28 | 7429 | 7578 | 149 | STILL spine, freeze-hold, locked (matches 11) |
| 29 | 7578 | 7697 | 119 | video dust-only (trim tail) |
| 30 | 7697 | 7828 | 131 | STILL locked close |
| C7 colophon | 7828 | 7978 | 150 | ivory + colophon card |

(Status columns below filled as built.)

## Type sheet — planned
- C1 Act I: "A wealth of information creates a poverty of attention." / Herbert Simon, 1971 — on Simon quote, frames 193–328
- C2 Act II: "Not pleasure. The gap." / reward prediction error · Schultz, Dayan & Montague, 1997
- C3 Act III: "Variable ratio. Hardest to extinguish." / of the schedules Ferster & Skinner measured, 1957
- C4 Act IV: "Not interrupting. Just within reach."
- C5 after Act V: "Real. Documented. Smaller than we said." — on "Both are true", before the boundary line
- C6 after Act VI: "No measure but each other."
- C7 colophon: "thirty shots · one voice · ten sources · all verified · rendered for about thirteen dollars — owned outright."
  (Numbers from LEDGER.md ACTUALS: fal spend $12.63 → "about thirteen dollars" rounds AGAINST the film; 30 shots; 10 sources recount confirmed in TREATMENT rev4.)
- House type: EB Garamond editorial body, Courier Prime numerals; ink #1F1E1D on ivory #FAF9F6.

## Type sheet — final (as built)

| Card | In | Out | Font | Content | Notes |
|---|---:|---:|---|---|---|
| C1 | 193 | 328 | EBGaramond-Regular 60 | "A wealth of information creates / a poverty of attention. / Herbert Simon · 1971" | on Simon quote per brief; ivory scrim 0.82 |
| C2 | 1450 | 1620 | EBGaramond-Regular 58 | "Not pleasure. The gap. / reward prediction error / Schultz, Dayan & Montague · 1997" | mid Act II, over shot 6 |
| C3 | 2050 | 2230 | EBGaramond-Regular 56 | "Variable ratio. / Hardest to extinguish. / of the schedules Ferster & Skinner measured · 1957" | early Act III |
| C4 | 4020 | 4190 | EBGaramond-Regular 66 | "Not interrupting. / Just within reach." | over shot 17 breath, before hero reach |
| C5 | 6150 | 6320 | EBGaramond-Regular 66 | "Real. Documented. / Smaller than we said." | on "Both are true", ENDS before boundary line 6327 |
| C6 | 6760 | 6940 | EBGaramond-Regular 62 | "No measure but each other." | over shot 24 pull-back |
| C7 colophon | 7838 | 7965 | CourierPrime-Regular 32 | "thirty shots · one voice · ten sources · all verified / rendered for about thirteen dollars — owned outright" | on ivory matte tail; numbers from LEDGER ACTUALS |

All cards: ink #1F1E1D, centered, fadeIn. C1–C6 on a soft ivory #FAF9F6 scrim
(0.82 opacity) for legibility over the paper shots; C7 clean on the matte.

**COLOPHON NUMBERS — verified against LEDGER.md actuals:**
- **thirty shots** — 30 generated shots (25 KEEP video clips + 5 rejected shots held
  as stills 6/15/17/23/30; spine 11/28 also as stills). Confirmed 30, not the
  brief header's "30 clips + 12 cards" confusion.
- **ten sources** — TREATMENT rev4 recount: 9 spoken works + Sean Parker's
  on-record statement = 10 sources heard. Orben 2020 verified but NOT spoken, excluded.
- **about thirteen dollars** — LEDGER running film spend is **$12.63** fal
  (keyframes $2.40 + clip batch $6.45 + retake batch $2.90; audio all $0.00 on
  subscription credits). "About thirteen dollars" rounds UP — i.e. AGAINST the
  film's own frugality, the only honest direction for a film about honest
  measurement. The treatment's draft "about eleven dollars" was a pre-ledger
  estimate and is corrected here to the actual.

## Grade — final (all 33 picture clips, one consistent warm-paper grade; matte ungraded)

Documented ranges only; temperature left untouched (undocumented scale).
- exposure **+0.15 EV** (light, paper-forward lift)
- contrast **1.06** (gentle)
- blacks **+0.06** (faded-paper lift so nothing crushes to hard black)
- whites **-0.03** (hold the ivory off pure clip)
- vibrance **+0.08** (protects the single red accent without oversaturating)
- midsHue **40 / midsAmount 0.05** (a whisper of warm in the midtones — warmth
  achieved WITHOUT temperature, per the hard rule)

Single grade across the film because it is one continuous paper world; per-act
variation would fracture the ivory ground the whole film sits on.

## QC record — real observations

- **One-frame gap scan (picture track V2):** PASS. Clips run fully contiguous
  0→7828 with no gaps and no one-frame slivers (get_timeline reports no `gaps`
  key on V2). Matte V1 contiguous 0→7978; narration A1 contiguous 0→7828; room
  tone A2 contiguous 0→7977. Card track V3 and cue track A3 are intentionally
  intermittent (overlays / one-shots), not defects.
- **Duration:** 7978 frames @ 30fps = 265.93 s = 4:25.93. = narration 4:20.9 +
  ~5 s colophon/ivory tail. On target (≈4:20.9 + card tail).
- **Eight frames inspected across the film (inspect_timeline):**
  - f498 shot 2 — paper drift, one red slip, warm light. Clean.
  - f1495 C2 card over shot 6 — EB Garamond, ink on scrim, no typo, RPE peak behind. Clean.
  - f2493 shot 10 — cord + red knot + hand shadow, descent. Clean.
  - f3490 shot 14 — teacup + taut red thread, one cup. Clean.
  - f4487 shot 18 frozen fingertips — hand at rest OUTSIDE the red ring ("never arrives"). Correct window held.
  - f5484 shot 21 — potato (red thread) + spectacles balanced, both objects present. Clean.
  - f6482 shot 22 frozen settled bloom — red bloom, far side clear. Calm under the closing line. Clean.
  - f7479 shot 28 spine — drained grey-red dot dead centre. Clean.
- **Spine check (11 vs 28):** f2710 shot 11 = saturated red dot dead centre;
  f7479 shot 28 = same dot position drained to muted grey-red. Framing locked
  and identical; the red→grey drain across the film is intact. PASS.
- **Card typos / fonts:** C1 (f260) and colophon (f7900) inspected directly —
  correct copy, EB Garamond (cards) and Courier Prime (colophon) both rendering,
  no typos. C5 (f6230) ends before the boundary line at 6327 as required.
- **Colophon numbers:** "thirty shots · one voice · ten sources · all verified ·
  rendered for about thirteen dollars — owned outright" — all TRUE per ledger.
- **Last frame (f7976):** pure ivory matte — intentional, breathes to paper, not black.
- **Shot 23 judgment:** the slow push-in (scale 1.0→1.05 over 188 f) on the held
  keyframe reads CALM and intimate, not dead — the seated ring around the ember
  has enough life. KEEP; no paid veo escalation warranted.

## Master
- Path: `/Users/isaachernandez/blog design/output/the-price-of-a-glance-master.mp4`
- Format: H.264, 1920×1080, 30fps, 7978 frames / 265.93 s. (ffprobe verification below.)

## Editions — master only this pass (9:16 is a separate pass, not built here)

## Notes back — (filled at close)

---

# STILLS CUT — Isaac's direction, filed 2026-07-24

> **A separate deliverable, not a revision of the animated cut above.** Isaac's
> direction overrides every earlier animation plan for THIS cut: **still images
> only, no motion of any kind, no transitions, hard cut to the next image
> always. The entire craft is timing** — how long each image holds and exactly
> where it cuts. Built in a new Palmier timeline `stills-cut` (timelineId
> `9162900A`); the e-ink `Timeline 1` and `animation-proof` timelines were left
> untouched.

## Sources bound

- **Frames:** the 30 character-driven (true-Zenn) keyframes from FRAME-BOOK's
  storyboard build — `output/images/*.png`, staged into
  `videos/attention-social-media/stills-cut/frames/scene-01..30.png` and imported.
  All 1376×768 (16:9); fill 1920×1080 with a ~0.8% side crop, no letterbox
  (verified on the composited frames).
- **Voice:** the seven FINAL narration stems, measured durations exact —
  I 27.63 / II 30.19 / III 50.90 / IV 35.34 / V 77.65 / VI 20.57 / VII 29.63 s.
  Laid on two audio tracks (A1/A2) alternating per act so no stem tail is clipped.
- **No score.** Narration only, one consistent level, as directed.
- Project: 1920×1080, 30 fps. Total timeline **8368 frames = 278.93 s** =
  271.91 s spoken + 3.0 s title pre-roll + 4.0 s colophon.

## Method — how the timing was set

`get_transcript` at segment granularity for the map, then word granularity at
every mid-sentence cut. Each image is cut to arrive a hair (≈8 frames / 0.27 s)
**before** the words it serves, so the viewer reads the picture then hears the
line land. Act-opening images align to the act's first word. Holds vary by the
narration: punchy lines cut short, slow ideas sit. No slot equals 271.91/30.

## Timeline map (image track V1, frame-exact, hard cuts)

Bookend title card: frames 0–90 (3.0 s), ivory ground.

| Scene | Frames | Hold | Serves (narration beat) | Note |
|---|---|---:|---|---|
| 1 sleeping reach | 90–262 | 5.7 s | "Watch your hand… knows where the phone is" | |
| 2 blizzard / scarcity | 262–609 | 11.6 s | "Herbert Simon, 1971… the less attention you've got" | long, flagged |
| 3 the sale / buyer's hand | 609–911 | 10.1 s | "scarce things get a price… fifty-five years later" | price beat lands on the hand |
| 4 tap & wait | 911–1082 | 5.7 s | "little hits of dopamine… wrong in the way that counts" | |
| 5 1997 / burst | 1082–1456 | 12.5 s | "three scientists… the gap between expected and got" | **flagged** |
| 6 mesmerised / guessing | 1456–1817 | 12.0 s | "get something you didn't see coming… keep you guessing" | **flagged** |
| 7 Skinner box peck | 1817–2141 | 10.8 s | "That guessing has a name… never a pattern you can crack" | |
| 8 pellet in tray | 2141–2425 | 9.5 s | "hardest habit to break… pigeon fed at random" | |
| 9 pull-to-refresh | 2425–2553 | 4.3 s | "Now look at your phone… slot machine lever" | quick, punchy |
| 10 red badge | 2553–2712 | 5.3 s | "The red badge… something somewhere happened" | |
| 11 feed no bottom | 2712–2944 | 7.7 s | "the feed with no bottom… An end" | |
| 12 builder confession | 2944–3343 | 13.3 s | "In 2017, one of Facebook's founders… did it anyway" | **flagged** |
| 13 desk / cost in numbers | 3343–3464 | 4.0 s | "what does it cost you? Not in outrage. In numbers" | |
| 14 thread taut / residue | 3464–3737 | 9.1 s | "Sophie Leroy, 2009… attention residue" | |
| 15 temples / memory test | 3737–4036 | 10.0 s | "Adrian Ward, 2017… desk, pocket, another room" | |
| 13b (reuse of 13) | 4036–4270 | 7.8 s | "Switching it off did nothing. Distance did…" | **cut-back**, see below |
| 16 reach & stop | 4270–4404 | 4.5 s | "doesn't have to buzz… within reach" | |
| 17 honest shrug | 4404–4537 | 4.4 s | "That last study is the weakest thing I've shown you" | |
| 18 flat-line card | 4537–4787 | 8.3 s | "In 2022, someone ran it again… No effect" | |
| 19 clock / aside | 4787–4868 | 2.7 s | "I just spent thirty-five seconds on that" | shortest live hold — the joke |
| 20 pinch "small" | 4868–5137 | 9.0 s | "a review pooled twenty-two… a seventh of an SD. Small" | |
| 21 teen field | 5137–5529 | 13.1 s | "the biggest look… 355,000 teenagers" | long but busy image; flagged |
| 20b (reuse of 20) | 5529–5777 | 8.3 s | "…at most four tenths of one percent" | **cut-back** (pinch = smallness) |
| 22 potato / glasses | 5777–5984 | 6.9 s | "eating potatoes… glasses one-and-a-half times worse" | |
| 23 branching paths | 5984–6173 | 6.3 s | "six hundred million defensible ways" | |
| 17b (reuse of 17) | 6173–6503 | 11.0 s | "to be clear… the harm is small… both are true at once" | **cut-back** (return to direct address) |
| 24 drop in basin | 6503–6733 | 7.7 s | "a tiny average… spread across millions it never touched" | |
| 25 small circle | 6733–7122 | 13.0 s | "Festinger, 1954… a few dozen faces" | long, flagged |
| 26 wall bursts open | 7122–7300 | 5.9 s | "Now the room is everyone. Ranked… never closes" | |
| 27 alone at the wall | 7300–7350 | 1.7 s | "And you're in it." | deliberate snap-to-you |
| 28 calm / ledger | 7350–7742 | 13.1 s | "None of this is a conspiracy… never know what you'll get next" | long, flagged |
| 29 badge drains | 7742–8093 | 11.7 s | "You're not going to out-willpower that… predictable and boring" | flagged |
| 30 phone down / window | 8093–8248 | 5.2 s | "easy to put down… nothing left to wait for" | |

Colophon card: frames 8248–8368 (4.0 s), ivory ground, hard cut in and out.

**Cut-backs (the long-slot remedy).** Three holds ran past ~13 s on a single
still — the direction says cut back to a related image rather than let a static
frame sag. So scene 15's 17.8 s Ward block splits into 15 (the test) + a return
to scene 13 (desk, phone in reach = the "distance" motif); scene 21's 21.3 s
Orben block splits into 21 (the field) + a return to scene 20 (the pinch =
"four tenths of one percent"); and scene 24's 18.7 s closing block splits into
a return to scene 17 (the honest, to-camera shrug = "to be clear…") + 24 (the
drop). Each cut-back is thematically matched, not filler.

## Type sheet

| Card | Text | Font | Size | Colour | Frames |
|---|---|---|---|---|---|
| Title | THE PRICE / OF A GLANCE | EBGaramond-Regular | 92 | `#1F1E1D` on `#FAF9F6` | 0–90 |
| Colophon line 1 | THE PRICE OF A GLANCE | EBGaramond-Regular | 58 | `#1F1E1D` | 8248–8368 |
| Colophon line 2 | thirty stills · one voice · ten sources · all verified · owned outright | CourierPrime-Regular | 24 | `#1F1E1D` | 8248–8368 |

No animation on any type — static cards, hard cut, per direction. Colophon
numbers are the ones verifiable as true (30 distinct stills; one voice, Eric;
ten sources cited in the VO, all VERIFIED in the TREATMENT source table). **The
dollar figure was omitted deliberately** — no clean per-film render cost is
isolable from the LEDGER (it folds in the retired e-ink pass), and this
assembly pass spent nothing, so no cost is stated rather than an untrue one.

## Grade

None. Isaac's direction is stills as delivered, timing is the whole job; no
grade was applied. The frames already carry the true-Zenn palette (muted warm
sets, one tomato-red accent). Flag if a light unifying grade is wanted later.

## QC record

- **Gaps:** image track V1 is contiguous 0→8368, zero gaps (confirmed in
  get_timeline; every clip end == next clip start). Narration is continuous
  across A1/A2 with no silent hole; the 1–2 frame act-boundary overlaps sit on
  different tracks and are inaudible.
- **Duration:** timeline 8368 f / 278.93 s; ffprobe on the master reports
  `duration=278.933333`, `nb_frames=8368`, 1920×1080, 30/1 fps, h264 + aac,
  size 71,003,327 bytes. Matches.
- **8 frames looked at (actually inspected, not sampled on status):** f45 title
  card (Garamond, clean), f348 scene 2 (blizzard, one red slip), f1046 scene 4
  (tap, one red dot), f2440 scene 9 (pull-to-refresh, red spinner), f3138 scene
  12 (builder, one red phone), f5230 scene 21 (teen field, single red figure —
  one-accent rule held on the crowd shot), f6624 scene 24 (red drop opening in
  the basin), f8019 scene 29 (badge draining red→grey). All correct, all
  full-frame, one red accent each, no letterbox.
- **Last frame:** f8367 is the colophon card — the one intended.

## Master

- Path: `/Users/isaachernandez/blog design/output/the-price-of-a-glance-stills.mp4`
- H.264, 1920×1080, 30 fps, 8368 frames, **278.93 s**, aac audio, 71.0 MB.
  ffprobe-verified.

## Slots I judge too long for a single still — candidates for extra frames ($0.08 ea)

Ranked by how badly a static hold drags. Cut-backs already rescued the three
worst (15/21/24); the rest are single stills held long:

1. **Act II is under-framed** — 3 stills for 30.19 s. Scene 5 (12.5 s, f1082–1456)
   and scene 6 (12.0 s, f1456–1817) both sit ~12 s. **One extra Act II frame**
   (e.g. a dedicated "…and it spikes" beat between the 1997 discovery and the
   mesmerised lean-in) would drop both to ~8 s.
2. **Scene 12 — builder confession, 13.3 s (f2944–3343).** Two full sentences on
   one image. A second builder/hero beat for "…they did it anyway" would split it.
3. **Scene 28 — calm/ledger, 13.1 s (f7350–7742)** and **Scene 25 — small circle,
   13.0 s (f6733–7122)** and **Scene 21 — teen field, 13.1 s (f5137–5529).** All
   ~13 s. 21 and 25 are busy images that tolerate it; 28 is the emptiest of the
   three and would benefit most from a second Act VII frame.
4. **Scene 2 — blizzard/scarcity, 11.6 s (f262–609)** and **Scene 29 — badge
   drains, 11.7 s (f7742–8093).** Borderline; acceptable as-is but a second frame
   each would let the cut breathe.

If you green-light frames, the highest-value single buy is **one Act II frame**
(fixes two long holds at once).

## What fought me

- **Only 30 stills for 271.91 s = 9.1 s average hold.** With zero motion and zero
  transitions, that average is high for stills; the timing had to lean on the
  natural sentence structure to keep most holds in the 4–10 s range and push the
  unavoidable long ones onto the busiest images. The cut-backs are the honest
  fix for the three that no single image could carry.
- **Colophon overwrite.** Two colophon text lines placed on one track at the same
  frames overwrote each other (same-track clips can't overlap); the second buried
  the first. Fixed by putting the Garamond title line on its own track above the
  mono line. Caught at the QC frame-inspection, not assumed.
- Nothing else. Frames and stems were all on disk and gate-passed upstream; no
  generation was needed or fired ($0 spent, as directed).


---

# STILLS CUT v2 — the 75-frame comedic cut, filed 2026-07-24

> **Replaces the 30-still cut above as the delivered stills film.** Same
> non-negotiables: still images only, no motion of any kind, no transitions,
> hard cut always. The craft is timing and nothing else. Built in a new Palmier
> timeline `stills-cut-v2` (timelineId `693E159B`); `Timeline 1`,
> `animation-proof` and `stills-cut` were left untouched. **$0 spent — assembly
> only, no generation of any kind.**

## Sources bound

- **Frames:** the 75-row STILLS CUT LIST from `FRAME-BOOK.md` (the ZENN-PACE
  EXPANSION block), staged in screen order to
  `videos/attention-social-media/stills-cut-v2/frames/f01-1.png … f75-30a.png`
  and imported as library folder `v2-frames`. All 75 verified present on disk,
  all 1376×768, all 75 paths unique. They fill 1920×1080 with a ~0.8% side crop
  — no letterbox, confirmed on every composited frame inspected.
- **Voice:** the seven FINAL narration stems, at the SOUND-BOOK measured
  boundaries — I 0:00 / II 27.63 / III 57.82 / IV 108.72 / V 144.06 / VI 221.71
  / VII 242.28, spoken end 271.91 s. Laid on two audio tracks (A1: I, III, V,
  VII · A2: II, IV, VI) so no stem tail is clipped where a boundary rounds.
- **No score, no room tone, no design cues.** Narration only, one level, as in
  the approved v1 stills cut. The brief specified the seven stems and nothing
  else; if room tone is wanted under the film that is a one-call addition.
- **No grade.** Frames as delivered, per Isaac's direction.

## Shape

| | Frames | Seconds |
|---|---:|---:|
| Title card (static, hard cut out) | 0–90 | 3.00 |
| Picture — 83 cuts across 75 frames | 90–8410 | 277.33 |
| ⤷ narration under picture | 90–8248 | 271.93 |
| ⤷ closing hold `30a` in silence | 8248–8410 | 5.40 |
| Colophon (static, hard cut in) | 8410–8530 | 4.00 |
| **Total** | **8530** | **284.33** |

## How the timing was set

`get_transcript` at **segment** granularity gave 82 sentence boundaries across
the seven stems; **word** granularity gave every word's project frame. Because
there are more sentence boundaries (82) than frames (75), **every cut in the
film lands on a sentence or clause boundary — none lands mid-phrase.** Each cut
sits 8 frames (0.27 s) ahead of the words it serves, so the picture arrives
just before the line.

The suggested holds in the FRAME-BOOK were the starting point and were
overridden wherever they fought the transcript. They were computed against the
book's slot arithmetic, which drifts from the recorded speech by as much as 8
seconds by mid-Act II — for example the book gives the dopamine-tap beat until
0:37.00, but the 1997 sentence actually begins at 0:36.3 (frame 1090). **The
transcript won every disagreement.**

Rules held mechanically, not by eye:

- no hold over 8.00 s (longest is `24a` at 7.93 s)
- no hold under 1.00 s (shortest is `4` at 1.03 s)
- no three consecutive holds of equal length; no two adjacent holds within 2 frames
- act shape: III fastest, V most spacious

## Timing map by act (image track V2, frame-exact, hard cuts)

`↩` marks a cut-back to an already-used frame.

**Act I**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `1` | setup | 90 | 206 | 116 | 3.87 s | act open / watch your hand |
| `1a` | snap | 206 | 250 | 44 | 1.47 s | it already knows where |
| `1b` | reaction | 250 | 397 | 147 | 4.90 s | the phone is / into Simon |
| `2` | setup | 397 | 609 | 212 | 7.07 s | looking at information cost you attention + more info less attention |
| `2a` | reaction | 609 | 732 | 123 | 4.10 s | that makes it scarce, scarce things get a price |
| `3a` | setup | 732 | 788 | 56 | 1.87 s | 55 years later |
| `3` | snap | 788 | 834 | 46 | 1.53 s | somebody's buying yours |
| `3b` | reaction | 834 | 919 | 85 | 2.83 s | and the sale closes in milliseconds |

**Act II**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `4a` | setup | 919 | 1001 | 82 | 2.73 s | little hits of dopamine |
| `4` | hold | 1001 | 1032 | 31 | 1.03 s | That's close. |
| `4b` | snap | 1032 | 1228 | 196 | 6.53 s | also wrong in the way that counts + held over the 1997 citation |
| `5a` | setup | 1228 | 1307 | 79 | 2.63 s | worked out what dopamine actually tracks |
| `5` | snap | 1307 | 1352 | 45 | 1.50 s | Not pleasure |
| `5b` | escalation | 1352 | 1392 | 40 | 1.33 s | surprise. |
| `5c` | reaction | 1392 | 1550 | 158 | 5.27 s | the gap between what you expected and what you got |
| `6` | setup | 1550 | 1662 | 112 | 3.73 s | get something you didn't see coming, and it spikes |
| `6a` | escalation | 1662 | 1737 | 75 | 2.50 s | the machine isn't built to make you happy |
| `6b` | snap | 1737 | 1825 | 88 | 2.93 s | it's built to keep you guessing |

**Act III**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `7a` | setup | 1825 | 1934 | 109 | 3.63 s | that guessing has a name / in 1957 two researchers |
| `7` | hold | 1934 | 2049 | 115 | 3.83 s | Ferster and Skinner mapped what happens |
| `7b` | snap | 2049 | 2141 | 92 | 3.07 s | not every time, never a pattern you can crack |
| `8` | setup | 2141 | 2251 | 110 | 3.67 s | hardest habit to break |
| `8a` | escalation | 2251 | 2352 | 101 | 3.37 s | a pigeon fed at random keeps |
| `8b` | reaction | 2352 | 2425 | 73 | 2.43 s | a pigeon fed like clockwork gives up |
| `9a` | setup | 2425 | 2465 | 40 | 1.33 s | now look at your own phone |
| `9` | hold | 2465 | 2515 | 50 | 1.67 s | pull to refresh |
| `9b` | snap | 2515 | 2553 | 38 | 1.27 s | that's the slot machine lever |
| `10a` | setup | 2553 | 2586 | 33 | 1.10 s | the red badge |
| `10` | snap | 2586 | 2625 | 39 | 1.30 s | which tells you |
| `10b` | escalation | 2625 | 2712 | 87 | 2.90 s | nothing except that something somewhere happened |
| `11a` | setup | 2712 | 2776 | 64 | 2.13 s | the feed with no bottom |
| `11` | hold | 2776 | 2890 | 114 | 3.80 s | which took the one thing every page used to have |
| `11b` | escalation | 2890 | 2944 | 54 | 1.80 s | an end, and it was on purpose |
| `12` | setup | 2944 | 3088 | 144 | 4.80 s | in 2017 one of Facebook's founders said it out loud |
| `12a` | snap | 3088 | 3255 | 167 | 5.57 s | built a social approval loop that exploits a weakness |
| `12` ↩ | cut-back | 3255 | 3352 | 97 | 3.23 s | and in his words, they did it anyway |

**Act IV**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `13a` | setup | 3352 | 3396 | 44 | 1.47 s | so what does it actually cost you |
| `13` | snap | 3396 | 3465 | 69 | 2.30 s | not in outrage. in numbers. |
| `14a` | setup | 3465 | 3663 | 198 | 6.60 s | Sophie Leroy 2009 / part of your head stays behind |
| `14` | hold | 3663 | 3738 | 75 | 2.50 s | she called it attention residue |
| `14b` | escalation | 3738 | 3825 | 87 | 2.90 s | Adrian Ward's team, 2017 |
| `15` | setup | 3825 | 3893 | 68 | 2.27 s | people took memory tests |
| `15a` | snap | 3893 | 4037 | 144 | 4.80 s | desk, pocket, another room |
| `16` | setup | 4037 | 4131 | 94 | 3.13 s | switching it off did nothing |
| `16a` | escalation | 4131 | 4271 | 140 | 4.67 s | distance did / the further away the phone |
| `16` ↩ | cut-back | 4271 | 4321 | 50 | 1.67 s | it doesn't have to buzz |
| `16a` ↩ | cut-back | 4321 | 4412 | 91 | 3.03 s | it just has to be within reach |

**Act V**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `17a` | setup | 4412 | 4494 | 82 | 2.73 s | okay. that last study is |
| `17` | snap | 4494 | 4537 | 43 | 1.43 s | the weakest thing I've shown you |
| `18` | hold | 4537 | 4735 | 198 | 6.60 s | in 2022 someone ran it again, properly |
| `18a` | snap | 4735 | 4787 | 52 | 1.73 s | nothing. no effect. |
| `19` | hold | 4787 | 4868 | 81 | 2.70 s | I just spent 35 seconds on that |
| `19a` | snap | 4868 | 4980 | 112 | 3.73 s | a review pooled 22 of these studies |
| `20` | setup | 4980 | 5104 | 124 | 4.13 s | about a seventh of a standard deviation |
| `20a` | escalation | 5104 | 5196 | 92 | 3.07 s | small. then the biggest look we have. |
| `21a` | setup | 5196 | 5329 | 133 | 4.43 s | Amy Orben and Andrew Przybylski, 2019 |
| `21` | snap | 5329 | 5529 | 200 | 6.67 s | every reasonable version at once, across 355,000 teenagers |
| `21b` | reaction | 5529 | 5711 | 182 | 6.07 s | the link is real and negative |
| `20a` ↩ | cut-back | 5711 | 5777 | 66 | 2.20 s | at most four tenths of one percent |
| `22` | hold | 5777 | 5905 | 128 | 4.27 s | eating potatoes looked almost as bad |
| `22a` | snap | 5905 | 5984 | 79 | 2.63 s | wearing glasses looked 1.5 times worse |
| `23` | hold | 5984 | 6089 | 105 | 3.50 s | and in one of those data sets alone |
| `23a` | escalation | 6089 | 6173 | 84 | 2.80 s | 600 million defensible ways to run the numbers |
| `17` ↩ | cut-back | 6173 | 6328 | 155 | 5.17 s | so to be clear / the tricks are real |
| `18` ↩ | cut-back | 6328 | 6442 | 114 | 3.80 s | the harm is small and badly measured |
| `24` | setup | 6442 | 6503 | 61 | 2.03 s | both are true at once |
| `24a` | snap | 6503 | 6741 | 238 | 7.93 s | a tiny average is what a real effect looks like |

**Act VI**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `25` | setup | 6741 | 6857 | 116 | 3.87 s | Festinger 1954 / you work out how you're doing |
| `25a` | snap | 6857 | 6962 | 105 | 3.50 s | no objective yardstick, you use whoever's around |
| `26a` | setup | 6962 | 7122 | 160 | 5.33 s | the people in the room / a few dozen faces |
| `26` | snap | 7122 | 7187 | 65 | 2.17 s | now the room is everyone |
| `26b` | escalation | 7187 | 7313 | 126 | 4.20 s | ranked on their best day, and it never closes |
| `27alt` | snap | 7313 | 7360 | 47 | 1.57 s | and you're in it |
| `27` | hold | 7360 | 7399 | 39 | 1.30 s | tail / none of this is a conspiracy |

**Act VII**

| Frame | Role | In | Out | f | Hold | Lands on |
|---|---|---:|---:|---:|---:|---|
| `28` | setup | 7399 | 7523 | 124 | 4.13 s | it's a business model, right there in the filings |
| `28a` | escalation | 7523 | 7607 | 84 | 2.80 s | they sell your attention over and over |
| `28` ↩ | cut-back | 7607 | 7742 | 135 | 4.50 s | you never quite know what you'll get next |
| `28a` ↩ | cut-back | 7742 | 7823 | 81 | 2.70 s | you're not going to out-willpower that |
| `29a` | setup | 7823 | 8003 | 180 | 6.00 s | nobody does / change the machine / turn off the badges |
| `29` | snap | 8003 | 8093 | 90 | 3.00 s | make the rewards predictable and boring |
| `29b` | reaction | 8093 | 8156 | 63 | 2.10 s | and then it gets easy to put down |
| `30` | hold | 8156 | 8248 | 92 | 3.07 s | because there's nothing left to wait for |
| `30a` | hold | 8248 | 8410 | 162 | 5.40 s | final silence hold |

## Act shape as built

| Act | Feel required | Clips | Avg hold | Fastest | Longest breath |
|---|---|---:|---:|---|---|
| I | opening breath | 8 | 3.45 s | `1a` 1.47 s | `2` 7.07 s |
| II | setup/snap pairs | 10 | 3.02 s | `4` 1.03 s | `4b` 6.53 s |
| III | **fastest in the film** | 18 | **2.83 s** | `10a` 1.10 s | `12a` 5.57 s |
| IV | heavier, deliberate | 11 | 3.21 s | `13a` 1.47 s | `14a` 6.60 s |
| V | **most spacious** | 20 | **3.88 s** | `17` 1.43 s | `24a` **7.93 s** |
| VI | tightening to the snap | 7 | 3.13 s | `27` 1.30 s | `26a` 5.33 s |
| VII | settling, warm | 9 | 3.74 s | `29b` 2.10 s | `29a` 6.00 s |

**Film: 83 cuts, 75 unique frames, average hold 3.34 s** (v1 was 9.1 s).
Act III at 2.83 s is the fastest and Act V at 3.88 s the most spacious, exactly
as `TIMING-SPEC.md` requires.

## The snaps — the holds chosen, and why

| Frame | Hold | The joke it lands on |
|---|---:|---|
| `1a` phone balanced on his nose | **1.47 s** | cut on "it already knows" — the arm has curled back before the sentence resolves |
| `3` grey hand snatches the phone | **1.53 s** | cut on "somebody's **buying yours**" — the snatch and the word are simultaneous |
| `4` poking the dead screen | **1.03 s** | the film's shortest hold, on the two-word sentence "That's close." A blink of nothing-happening between the expectant lean-in and the collapse |
| `5` blown off his feet | **1.50 s** | on "Not pleasure" |
| `5b` flung higher, shoes off | **1.33 s** | on the single word "**surprise.**" |
| `9b` catapulted somersault | **1.27 s** | on "that's the slot machine lever" |
| `10` recoiling at one dot | **1.30 s** | on "the red badge, which tells you…" |
| `13` the snapped pencil | **2.30 s** | held dry across "Not in outrage. In numbers." |
| `17` the caught-out shrug | **1.43 s** | on "the **weakest** thing I've shown you" — the film's own retraction gets the hardest cut in Act V |
| `18a` deflated spike on his head | **1.73 s** | on "Nothing. No effect." |
| `26` spiral eyes at the endless wall | **2.17 s** | on "Now the room is everyone" |
| `27alt` **wedged inside the panel** | **1.57 s** | on "and you're in it" — cut first, as instructed |
| `27` craning back at the wall | **1.30 s** | the resolving tail, running under "None of this is a conspiracy" |
| `29` flicking the toggle | **3.00 s** | on "make the rewards predictable and boring" |

### Setup → snap pairs, as built

- **`4a` 2.73 → `4` 1.03 → `4b` 6.53.** The inversion that works best in the
  film. `4b` (flat dead-eyed stare, flies, grimy shirt) is not cut short — it is
  **held 6.5 s straight through the dry Schultz/Dayan/Montague citation.** The
  FRAME-BOOK's own composition note says "hold it, the deadpan is a held beat,"
  and holding a deadpan stare at the viewer while a scientific citation is read
  is funnier than any short cut. This freed `5a` to be a tight 2.63 s crouch
  before the explosion.
- **`5a` 2.63 → `5` 1.50 → `5b` 1.33 → `5c` 5.27.** Tight brace, then three
  accelerating beats of being launched, then a long crash-landed recovery.
- **`9a` 1.33 → `9` 1.67 → `9b` 1.27.** The fastest three-beat run in the film,
  sitting on "Now look at your own phone. / Pull to refresh. / That's the slot
  machine lever." — three short sentences, three short holds.
- **`10a` 1.10 → `10` 1.30 → `10b` 2.90.** The yawn is the shortest setup in
  the film; the badge mound then gets the longest hold of the three, so the
  escalation reads as accumulation.
- **`13a` 1.47 → `13` 2.30.** Reversed from the book (4.5 → 3.78) because the
  three sentences it serves total only 4.0 s. The fake-serene smile is a flash;
  the snapped pencil holds through the dry "In numbers."

### Escalation runs

- **Act III, badges:** 1.10 → 1.30 → 2.90 (accumulating), and the feed ribbon
  2.13 → 3.80 → 1.80, closing hard on the word "**end**."
- **Act III, pigeons:** 3.67 → 3.37 → 2.43, each successive hold shorter, so
  the sledgehammer escalation reads as mounting pressure and `8b`'s guilty
  glance lands on "gives up."
- **Act IV, the rubber arms:** 3.13 → 4.67 → 1.67 → 3.03 as an A/B/A/B
  alternation of `16`/`16a`, so the pull escalates and `16a` (both arms looped
  round the desk leg) lands on "It just has to be within reach."
- **Act V:** deliberately does **not** accelerate. It is the honest turn and
  carries the film's four longest holds.

### `27alt` → `27`, as instructed

`27alt` cuts **first** at 7313 as the snap, 1.57 s, landing 8 frames before
"and you're in it." `27` follows at 7360 as the tail. **The tail is 1.30 s, not
the ~2.3 s the brief asked for** — the transcript would not give more: "and
you're in it" ends at frame 7344 and Act VII's first claim begins at 7358.
Rather than crush the snap, I let `27`'s tail run *past* the act boundary and
play under "None of this is a conspiracy," cutting to `28` on "It's a business
model." That reads better than the arithmetic did: the awe-struck man at the
wall holds while the narrator begins the calm close, then the deadpan folded
arms arrive on the word "model."

## Cut-backs — 8 cuts, 75 unique frames, 83 cuts total

Where a beat ran past 8 s on a single still, I cut back to a thematically
matched frame rather than let a static image sag (TIMING-SPEC rule 7). Every
one is a callback, not filler:

| Cut-back | At | Hold | Why it is the right image |
|---|---:|---:|---|
| `12` | 3255 | 3.23 s | the builder's **crossed fingers behind his back** returning on "and in his words, they did it anyway" — the frame *is* the line |
| `16` | 4271 | 1.67 s | one rubbery arm on "It doesn't have to buzz" |
| `16a` | 4321 | 3.03 s | both arms looped, hauling, on "It just has to be within reach" |
| `20a` | 5711 | 2.20 s | three stacked magnifying glasses on "at most **four tenths of one percent**" — smallness, restated |
| `17` | 6173 | 5.17 s | the to-camera shrug returning for "So to be clear, this isn't me letting them off" |
| `18` | 6328 | 3.80 s | the flat-line card returning for "the harm … is **small and badly measured**" |
| `28` | 7607 | 4.50 s | the jittering, begging phone on "you never quite know what you'll get next" |
| `28a` | 7742 | 2.70 s | the phone in a full begging-dog pose on "You're not going to out-willpower that" |

Two of these — `20a` on the percentage and `17` on "to be clear" — repeat
cut-backs that the v1 log recorded as working, and they work again.

## Where the suggested hold fought the transcript

The book's holds were treated as a proposal. 27 of the 75 diverged by ≥1.5 s.
The largest, and what I did:

| Frame | Book | Cut | What happened |
|---|---:|---:|---|
| `4b` | 2.37 | **6.53** | promoted from snap to the act's long held deadpan, over the citation (see above) |
| `14a` | 3.00 | **6.60** | the Sophie Leroy sentence is one unbroken 6.5 s clause; there is no legal cut inside it |
| `24a` | 4.71 | **7.93** | the film's longest hold, on its closing argument. Deliberate — Act V is where the film slows to be believed |
| `13a` | 4.50 | **1.47** | its three sentences total 4.0 s; 4.5 s was arithmetically impossible |
| `17` | 4.44 | **1.43** | "the weakest thing I've shown you" is the sharpest self-correction in the film and wanted the hardest cut, not a 4.4 s sit |
| `24` | 5.00 | **2.03** | compressed to give `24a` the 7.93 s breath it needed |
| `26a` | 2.50 | **5.33** | expanded to cover "the people in the room / A few dozen faces" — the small-room read, which is `26a`'s whole meaning |
| `21` | 4.00 | **6.67** | the 355,000-teenagers sentence runs 6.6 s and is a busy crowd frame that carries it |
| `29a` | 3.50 | **6.00** | held long deliberately, so the toggle-flick snap has something to snap against |

**Root cause worth filing:** the FRAME-BOOK's suggested holds sum to each
beat's *slot*, but the slots came from the treatment's arithmetic, not from the
recorded speech. By mid-Act II the drift is ~8 s. The holds were a useful
proposal; they were not a cut.

## Type sheet

| Card | Text | Font | Size | Colour | Frames | Animation |
|---|---|---|---:|---|---|---|
| Title | THE PRICE / OF A GLANCE | EBGaramond-Regular | 92 | `#1F1E1D` on `#FAF9F6` | 0–90 | **off** |
| Colophon line 1 | THE PRICE OF A GLANCE | EBGaramond-Regular | 58 | `#1F1E1D` | 8410–8530 | **off** |
| Colophon line 2 | seventy-five frames · one voice · ten sources · all verified · owned outright | CourierPrime-Regular | 24 | `#1F1E1D` | 8410–8530 | **off** |

No animation on any type; both cards hard-cut in and out over the ivory matte.
The two colophon lines sit on **separate tracks** (V3 Garamond, V4 Courier) —
the v1 log records that two text clips at the same frames on one track overwrite
each other, and that lesson was applied rather than rediscovered.

**Colophon claims, all true:**
- **seventy-five frames** — 75 unique frames placed (83 cuts; 8 are cut-backs).
  The v1 "thirty stills" is corrected, as instructed.
- **one voice** — Eric, `cjVigY5qzO86Huf0OWal`, all seven stems.
- **ten sources** — TREATMENT rev4/5 recount: 9 spoken works + Sean Parker's
  on-record statement.
- **all verified** — every figure transcript-verified in SOUND-BOOK.
- **owned outright** — true.
- **No dollar figure**, per the brief.

## Grade

None applied. Isaac's direction is the frames as delivered; they already carry
the muted warm palette and the one-flat-red accent. Flag if a unifying grade is
wanted.

## Matte

Full-length ivory `#FAF9F6` (`9700AC54`) on the **bottom** video track V1,
spanning 0–8530, so the cards breathe to paper and never to black. The 1376×768
frames fill the 1920×1080 canvas, so the matte is visible only behind the two
cards — which is where it is doing its job.

## QC record — real observations

**Gap scan (picture track V2, 83 clips):** PASS. No `gaps` key reported; every
clip's out-frame equals the next clip's in-frame across the whole 90→8410 run.
Verified independently against the computed plan: 83 spans, monotonic, no
overlap, no one-frame sliver, sum of holds == 8320 frames == 8410 − 90 exactly.
Matte V1 contiguous 0→8530. Narration A1 ∪ A2 continuous 90→8248 with no silent
hole (the alternating-track boundaries overlap by 1 frame on *different* tracks
and are inaudible). Card tracks V3/V4 are intentionally intermittent.

**Duration:** timeline 8530 f / 284.33 s. ffprobe on the master:
`duration=284.333333`, `nb_frames=8530`, 1920×1080, `r_frame_rate=30/1`,
h264 + aac (44.1 kHz mono), 86,439,256 bytes. Matches the timeline exactly.
Against target: 271.93 s of narration (≈ the 271.91 s measured spine) + 3.0 s
title + 5.4 s silent closing hold + 4.0 s colophon.

**Black-frame scan:** `ffmpeg blackdetect=d=0.05:pix_th=0.10` across the whole
master returned **no detections**. No black frames anywhere in the file.

**Eighteen composited frames inspected (actually looked at, not sampled on
status):**

- **f45** title card — EB Garamond, ink on ivory, centred, no typo.
- **f360** `1b` — one enormous bloodshot eye, hands clamped on the red-screen
  phone, hair blown back. Correct frame held into the Simon citation.
- **f900** `3b` — empty cupped hands, one sweat drop, the blank red price tag on
  the floor. Lands on "the sale closes in milliseconds."
- **f1440** `5c` — crash-landed, spiral eyes, ecstatic grin, dust puffs, already
  groping for the phone. One red = phone screen.
- **f1980** `7` — the pigeon working the red lever, hero kneeling in a lab coat
  with a clipboard, perfectly deadpan.
- **f2521** `9b` — catapulted backwards off the giant screen, hair on end. One
  red = the refresh arrow.
- **f3061** `12` — the builder sliding the phone across the drafting table,
  oversized crossed fingers behind his back clearly readable.
- **f3601** `14a` — gripping his head over the blank page, vein squiggle, the
  red-screen phone visible through the doorway in the next room. No ghost head
  yet — correct, the ghosts belong to `14`/`14b`.
- **f4141** `16a` — both arms rubbery and looped round the desk leg, biting the
  desk edge, heels dragging. Lands on "Distance did."
- **f4661** `18` — deadpan, half-lidded, holding the card with the one flat red
  line, the deflated spike collapsed behind him.
- **f5161** `20a` — three magnifying glasses stacked in front of one enormous
  eye, pinching the speck. Lands on the single word "small."
- **f5661** `21b` — in the crowd, red phone screen held up as a shield,
  terrified. **One-accent rule held on a crowd frame** — one red phone, no red
  figure among ~30 grey ones.
- **f6161** `23a` — the printout tower arched right over him like a breaking
  wave, and he is serenely adding one more sheet.
- **f6660** `24a` — a whole crowd of grey telescopes and binoculars aimed at the
  speck in his tweezers. The film's longest hold and it earns it.
- **f7160** `26` — spiral eyes at the panel grid, exactly one red panel.
- **f7340** `27alt` — **he is inside the panel**, knees up, waving stiffly, with
  a grey figure on the ground below looking up at him. The gag reads instantly.
- **f7380** `27` — same grid wall, clutching the phone, craning back.
- **f7660** `28` (cut-back) — arms folded, unimpressed, the phone physically
  jittering with dust puffs beside him.
- **f8160** `30` — feet up, hands behind head, enormous contented grin, red cup,
  phone face-down and forgotten.
- **f8380** `30a` — asleep in the chair, feet still up, snore bubble, long
  evening light. The film's last picture, held 5.4 s in silence.
- **f8529 (last frame)** — the colophon. Both lines rendering in both fonts, no
  typo, claims true, no dollar figure. **The frame I meant.**

**Set continuity within beats:** confirmed on every inspected pair — the frames
either side of each inspected cut share their set and framing, so no cut reads
as a jump. **One observation:** `27alt` and `27` are both panel-grid frames but
their walls are not identical — `27alt`'s grid has yellow mullions and window
depth, `27`'s is a flatter grey panel field. The hard cut reads as "same wall,
different distance," which is acceptable, but it is the loosest set match in the
film. Upstream asset difference, not an assembly defect.

**No letterbox:** every composited frame fills 1920×1080 edge to edge. The
1376×768 sources (1.792:1) fill the 1.778:1 canvas with a ~0.8% side crop.

## Master

- **Path:** `/Users/isaachernandez/blog design/output/the-price-of-a-glance-v2.mp4`
- H.264, 1920×1080, 30 fps, **8530 frames / 284.33 s**, aac 44.1 kHz mono,
  86.4 MB. ffprobe-verified, black-frame-scanned.

## Editions

**Master only.** The 9:16 edition was explicitly out of scope for this pass and
was not built. Nothing published.

## Beats that still feel slow

Honest list, in order of how much they drag:

1. **`14a` — 6.60 s (f3465–3663), Act IV.** The worst remaining hold. The
   Sophie Leroy sentence is one unbroken clause with no legal interior cut, and
   the frame is a fairly static "gripping his own head" pose with no ghost head
   yet. **This is the single highest-value place for one more frame** — an
   in-between beat for "get pulled away before you finish" would split it into
   two ~3.3 s holds.
2. **`4b` — 6.53 s (f1032–1228), Act II.** Defensible and I stand by it, but it
   is a *deliberate* long deadpan and if Isaac reads it as slow rather than dry,
   the fix is a second Act II frame for the citation, not a shorter `4b`.
3. **`2` — 7.07 s (f397–609), Act I.** Two full sentences on the paper-avalanche
   frame. Busy enough to carry it, but it is the longest hold in the opening act
   and Act I has the least new material per second in the film.
4. **`21` — 6.67 s (f5329–5529), Act V.** A very busy crowd frame, so it holds
   better than its length suggests. Acceptable.
5. **`29a` — 6.00 s (f7823–8003), Act VII.** Long by design, to load the toggle
   snap. Reads as anticipation, not sag — but it is the one I would watch.

`24a` at 7.93 s is the film's longest hold and I am **not** flagging it: it is
the closing argument of the honest turn, it wants that room, and the frame (a
forest of telescopes) is the busiest in the film.

## Notes back — for the next film

- **Give the Editor the measured VO before the frame slots are written.** The
  FRAME-BOOK's suggested holds were computed against treatment arithmetic and
  drift up to 8 s from the recorded speech by mid-Act II. They were a useful
  proposal but 27 of 75 had to be overridden. If the slot table is built from
  `get_transcript` segment boundaries instead, the frame count per beat comes
  out right the first time and the Editor's job becomes tuning rather than
  re-deriving.
- **Frames per sentence is the useful unit, not frames per act.** The places
  this cut strains are all single long sentences with no interior clause break —
  `14a`'s Sophie Leroy line, `2`'s information pair. When the Art Director
  budgets frames, budget one per sentence, plus one per comic beat.
- **75 frames at a 3.34 s average is the right density.** v1's 9.1 s read as a
  slideshow; this reads as a cut. Do not go below ~70 frames for a 4.5-minute
  stills film.
- **The setup→snap pair is the highest-yield thing the frame set gave me.** Every
  place the Cinematographer built a three-frame beat (setup / snap / reaction on
  one set) produced a working joke. Beats with only two frames (`12`/`12a`,
  `13a`/`13`, `15`/`15a`, `28`/`28a`) all needed either a cut-back or a
  compromise. **Build in threes.**
- **`27alt` was the right call and should be the pattern.** When a line is four
  words and has no image ("And you're in it"), the answer was a literal, absurd
  frame, not a mood frame. It is the sharpest cut in Act VI.
- **Two frames whose sets don't quite match cost more than a missing frame.**
  `27alt`/`27` is the one loose join in the film. When a new in-between frame is
  added to an existing beat, matching the *wall* matters as much as matching the
  character.

---

# STILLS CUT v3 — nine narration-repair frames swapped, filed 2026-07-24

> **A targeted re-export of v2, not a re-timing.** Nine frames were regenerated
> upstream because their pictures contradicted their lines (FRAME-BOOK
> **NARRATION-MATCH REPAIR** block). Every one of the 83 cuts, every hold, the
> act shape, the snaps, the cut-backs and the bookends are **exactly as timed in
> v2** — nothing was re-timed, no neighbouring hold was touched, the narration
> was not re-placed. Built in Palmier timeline `stills-cut-v3` (timelineId
> `884D9134`), duplicated from `stills-cut-v2` (`693E159B`), which is left
> intact. **$0 spent — assembly only, no generation.**

## The swap

Palmier has no replace-source operation, so v2 was duplicated and the nine
images were re-placed onto the picture track (V2, `C3327010`) at byte-identical
frame ranges. The nine repaired PNGs were staged to
`videos/attention-social-media/stills-cut-v3/frames/v3-f*.png` and imported as
library folder `v3-frames`. All nine verified 1376×768 and all nine md5-unique.

Before swapping, the nine staged v2 files were md5-compared against both the
superseded and the new paths: **all nine matched the superseded image**, so the
right nine clips were confirmed to be carrying the wrong pictures.

**Nine frames, eleven clips** — `18` and `28` each appear twice, as cut-backs:

| Frame | Clip frames | v2 asset | v3 asset |
|---|---|---|---|
| `1b` | 250–397 | `f03-1b` | `v3-f03-1b` |
| `3b` | 834–919 | `f08-3b` | `v3-f08-3b` |
| `8b` | 2352–2425 | `f24-8b` | `v3-f24-8b` |
| `10a` | 2553–2586 | `f28-10a` | `v3-f28-10a` |
| `15` | 3825–3893 | `f41-15` | `v3-f41-15` |
| `17a` | 4412–4494 | `f45-17a` | `v3-f45-17a` |
| `18` | 4537–4735 | `f47-18` | `v3-f47-18` |
| `18a` | 4735–4787 | `f48-18a` | `v3-f48-18a` |
| `18` ↩ | 6328–6442 | `f47-18` | `v3-f47-18` |
| `28` | 7399–7523 | `f69-28` | `v3-f69-28` |
| `28` ↩ | 7607–7742 | `f69-28` | `v3-f69-28` |

The mutation returned exactly 11 new clips and exactly 11 `removedClipIds`, with
every `frames` pair and every `trimEndFrame` identical to the v2 clip it
replaced. **Timing is provably unchanged.** Type sheet, matte, grade (none),
narration placement and colophon copy are all untouched from v2 — the colophon
still reads "seventy-five frames" and that is still true (75 unique frames, nine
of them now the repaired versions).

## QC record — real observations

**Gap scan:** PASS. Picture track V2 reports 83 clips and **no `gaps` key** —
contiguous 90→8410, no one-frame gaps, no slivers. Matte V1 contiguous 0–8530.
A1/A2 narration unchanged (the reported gaps are the alternating-track act
boundaries, as in v2). Total 8530 frames.

**Duration:** 8530 f / 284.333 s — **identical to v2**. ffprobe on the master:
`duration=284.333333`, `nb_frames=8530`, 1920×1080, `r_frame_rate=30/1`,
h264 + aac 44.1 kHz mono, 85,619,032 bytes. (v2 was 86,439,256 — the small
delta is the new images' compression, not a timing change.)

**Black-frame scan:** `ffmpeg blackdetect=d=0.05:pix_th=0.10` across the whole
master returned **no detections**.

**All nine replaced clips inspected individually on the timeline** (composited,
not sampled on status). Bald hero, exactly one flat tomato-red element, no
lettering on every one:

- **f320 `1b`** — extreme macro of the bald face, both eyes cracked into gummy
  just-woken slits, the phone's flat red screen throwing red light across the
  near cheek. **No clock anywhere.** One red = phone screen.
- **f876 `3b`** — the patch pocket is sewn to the grey shirt with the grey hand's
  fingers inside it, motion lines trailing off frame right; hero mid-blink,
  dopey smile at the phone, hasn't noticed. The theft reads instantly.
- **f2388 `8b`** — **the mallet is on the pigeon**, where the gag belongs. Manic
  pigeon two-handed on the mallet, feathers and dust; clockwork pigeon flat on
  its back with × eyes; hero deadpan in the lab coat, clipboard, hands empty.
  One red = the manic pigeon's lever handle, the second lever grey.
- **f2570 `10a`** — one flat red badge dot on the phone held screen-out, grey
  shirt, dead-eyed half-lidded stare, one eyebrow hiked, **mouth shut**. The
  retake's two defects are both gone: no `??` glyphs, no tan torso, no yawn.
- **f3859 `15`** — the comic gulf: hero at the desk near-left writing freely,
  bright-eyed, thought-bubble lightbulb; the phone tiny and abandoned by the far
  doorway across an empty grey floor. One red = the distant screen.
- **f4453 `17a`** — **the repair that mattered most.** Palm-up apologetic shrug,
  the other hand scratching the back of the bald head, wincing sheepish grimace
  with one eye squinted, single sweat drop, phone set down on the floor and
  ignored. **No triumphant stomp, no grin, no foot on the phone.** It now reads
  as *I have to be straight with you* under "that last study is the weakest
  thing I've shown you." Correct clip, correct line.
- **f4636 `18`** and **f6380 `18` ↩** — deadpan half-lidded, blank card with one
  dead-flat red line, the spike deflated to a punctured grey balloon skin beside
  him. **No water anywhere.** Both occurrences carry the new image.
- **f4761 `18a`** — **the hero is unmistakably BALD.** Smooth scalp, nothing
  touching or overlapping it; the spike lies completely flat on the floor at his
  feet. Wreckage carried by slumped shoulders, buckled knees and the card
  drooping from a loose hand. The identity break is closed.
- **f7461 `28`** and **f7680 `28` ↩** — the uncertainty engine as a machine: coin
  slot, side lever hauled, giant phone body with a red screen, grey shop counter
  behind. Eyes bulging, mouth open. One red = the machine's screen.

**Neighbour checks on the three Art-Director-flagged frames** (f230 `1a`, f450
`2`; f3780 `14b`, f3950 `15a`; f7380 `27`, f7560 `28a`) — see the observations
section below.

**Spot checks that nothing else moved:** f4515 `17` (untouched) is the same warm
wall and window as the new `17a`, so the pair reads as one place; f8529 last
frame is the colophon, both lines, both fonts, on ivory. The frame I meant.

## Master

- **Path:** `/Users/isaachernandez/blog design/output/the-price-of-a-glance-v3.mp4`
- H.264, 1920×1080, 30 fps, **8530 frames / 284.33 s**, aac 44.1 kHz mono,
  85.6 MB. ffprobe-verified, black-frame-scanned.

## Editions

**Master only.** The 9:16 edition was explicitly out of scope. Nothing published.

## Observations on the three flagged frames

Filed as observations, not re-timed — the timing is Isaac's call.

1. **`1b` (250–397, 4.90 s) — the texture outlier is exposed by its hold, not by
   its neighbours.** The set match is fine: `1a` before it and `1b` are the same
   bedroom, and it reads correctly as a punch-in on the face. What shows is the
   *finish* — `1a` (f230) and `2` (f450) are flat confident linework, and `1b` is
   soft airbrushed gradient with a glow falloff. At 4.90 s it is the third-longest
   hold in Act I, long enough for the eye to settle and register a different
   renderer rather than a fast macro insert. **If anything is ever changed here,
   the fix is a shorter hold, not a new frame** — a macro insert of ~2 s would
   read as a punch and the finish would pass unnoticed. It does not *jar* at the
   cut; it lingers.
2. **`15` (3825–3893, 2.27 s) — the wide is the shortest of its three, and that
   is the one real tension in the swap.** The run is `14b` medium (three ghost
   heads) → `15` **very wide** → `15a` tight close-up at the desk. Two large
   scale jumps around the film's widest frame, held 2.27 s, in which the viewer
   has to find a tiny phone across an empty floor *and* read a thought-bubble
   lightbulb. The composition wants more room than the hold gives it. **Against
   that: the swap improved the argument.** The new `15` (far phone, clear head,
   writing freely) followed by `15a` (phone on the desk, head steaming) now
   states Ward's finding in the right order as a visual pair, which the old
   generic head-gripping frame did not. My judgement: worth ~20–30 extra frames
   if Isaac ever reopens the timing, but it is not a defect and I did not touch it.
3. **`28` (7399–7523 and 7607–7742) — the counter is a non-event; the phone's
   *size* is the thing to know.** The grey counter is a low muted slab behind
   left, palette-correct, reads as furniture, does not jar. But the new `28` is a
   **machine-scale giant phone** and its partner `28a` (f7560) is a **small
   hand-sized phone on the floor** in the same warm room — and Act VII alternates
   `28`/`28a`/`28`↩/`28a`↩, so that scale jump happens **four times**. The old `28`
   held a small phone and matched. It still reads (the machine is obviously a
   machine, the small phone obviously a phone), and the beat is coherent as
   "the engine" cutting to "the thing in your hand" — but it is now the loosest
   set match in the film, taking that title from `27alt`/`27`. Filed for the Art
   Director rather than fixed, because fixing it means a new frame, not an edit.

## Anything else noticed now that the images match their lines

- **The credibility turn actually works now.** `17a` → `17` (4412–4494 → 4494–4537)
  reads as an escalating admission on one wall: the sheepish head-scratch, then
  the full-body shrug. In v2 the same two clips fought each other — a victory
  stomp followed by a caught-out shrug — and the hardest cut in Act V (`17`'s
  1.43 s) was landing on a contradiction. The timing was always right; it was the
  picture that was wrong. **This is the single biggest gain in v3** and it needed
  no re-timing to collect.
- **`18`/`18a` now reads as a two-stage deflation** — card up and deadpan, then
  slumped with the card drooping and the spike flat on the floor. Because the
  spike came off the scalp entirely, `18a`'s 1.73 s snap on "Nothing. No effect."
  lands on a *silhouette change* (shoulders drop, knees buckle), which is exactly
  what a 52-frame hold can carry. The old grey-mop version was also visually
  busier at the head, which is where the eye goes. The repair improved the snap
  as well as the identity.
- **`8b` fixed a comprehension bug, not just a prop bug.** With the mallet on the
  human, the three-beat pigeon run (`8` → `8a` → `8b`) had the hero changing role
  mid-beat. Now all three beats keep the hero as the deadpan observer and the
  escalation belongs entirely to the bird, so the 3.67 → 3.37 → 2.43 s
  accelerating holds read as mounting pressure on the *pigeon* — which is what
  the narration is about.
- **`10a`'s 1.10 s hold is now doing real work.** It is the shortest setup in the
  film and it is now the frame that introduces the badge, which is the subject of
  the next two sentences. In v2 the badge did not appear until `10` at 2586, so
  the run's first beat was empty. The escalation 1.10 → 1.30 → 2.90 s now
  accumulates from something.
- **The v2 QC record contains two now-stale observations**, both explained by the
  superseded images: it described f360 `1b` as "one enormous bloodshot eye" and
  f900 `3b` as "empty cupped hands, a blank red price tag on the floor." Those
  were accurate readings of the images that were then on the timeline. The v3
  readings above supersede them.

## Notes back — for the next film

- **The v2 lesson repeats with a sharper edge: an image that contradicts its line
  makes good timing look like bad timing.** `17`'s 1.43 s snap was flagged in v2
  as the hardest cut in Act V and it read as slightly too hard — because it was
  cutting away from a victory celebration. The same frames at the same lengths
  read as *right* now. **Before re-timing a beat that feels off, check that the
  picture says what the line says.** Half of "eight frames too long" is really
  "wrong frame."
- **Stage props at the feet, never on or behind the head.** The `18a` root cause
  is worth carrying forward as a house rule: any object drawn on, over or behind
  the hero's scalp renders as hair, and negative prompting cannot beat a
  silhouette. The fix that finally held was compositional, not lexical.
- **When a repair changes a frame's scale or set, say which of its neighbours it
  now has to cut against.** The `15` (scale) and `28` (prop scale) notes above
  are both cases where the repaired frame is correct in isolation and slightly
  loose in sequence. A repair brief that names the two adjacent frames — and, for
  a cut-back frame like `28`, names them *twice* — would have caught the giant-vs-
  small phone before the render.
- **Frames that appear more than once cost double when they are wrong.** `18` and
  `28` are each used twice, so nine bad images were eleven bad cuts. Worth
  flagging repeat-use frames in the cut list so the gate reads them against both
  their lines.
- **Duplicate-then-replace is the safe re-export shape.** Because Palmier has no
  replace-source operation, the reliable move is: duplicate the timeline, then
  `add_clips` the new asset at the *exact* `[start, end)` of the clip it replaces.
  The mutation delta returns identical `frames` and `trimEndFrame` values, which
  is a machine-checkable proof that nothing was re-timed — much stronger than
  re-reading and eyeballing 83 rows.

---

# STILLS CUT v4 — the no-repeat cut, filed 2026-07-24

> **Nine sources swapped, zero frames re-timed.** Isaac watched v3 and named the
> defect: 83 cuts, only 75 unique pictures. Eight of those cuts were cut-backs —
> honest editing, now out of policy. Eight new frames were built upstream, one
> per cut-back, and separately `28` was rebuilt to fix the Act VII phone scale
> and room continuity. This pass places those nine images at byte-identical
> frame ranges. Built in Palmier timeline `stills-cut-v4` (timelineId
> `92A206E0`), duplicated from `stills-cut-v3` (`884D9134`), which is left
> intact. **$0 spent — assembly only, no generation.**

## The swap — nine clips, nine images, identical timing

Same method as v3: Palmier has no replace-source operation, so v3 was duplicated
and the nine images were re-placed onto picture track V2 (`420A8BEA`, index 2)
at the exact `[start, end)` of the clip each replaces. The nine PNGs were staged
to `videos/attention-social-media/stills-cut-v4/frames/v4-*.png` and imported as
library folder `v4-frames`. All nine verified 1376×768 and all nine md5-unique.

| Frame | Clip frames | f | v3 asset | v4 asset | Source PNG |
|---|---|---:|---|---|---|
| `12b` | 3255–3352 | 97 | `f34-12` ↩ | `v4-12b` | `019f95ad-ff07-7b61-b970-d4297e4a4e61.png` |
| `16b` | 4271–4321 | 50 | `f43-16` ↩ | `v4-16b` | `019f95a0-c8af-7801-bcd7-8a17730f94e8.png` |
| `16c` | 4321–4412 | 91 | `f44-16a` ↩ | `v4-16c` | `019f95a0-c905-7f12-a8e1-8189ef5413a4.png` |
| `20b` | 5711–5777 | 66 | `f52-20a` ↩ | `v4-20b` | `019f95a0-c959-7e51-a717-2857c99ea092.png` |
| `17b` | 6173–6328 | 155 | `f46-17` ↩ | `v4-17b` | `019f95a0-cbcb-7ef0-90f1-957939257735.png` |
| `18b` | 6328–6442 | 114 | `v3-f47-18` ↩ | `v4-18b` | `019f95a0-cc2c-7691-b7ae-4a2517e37c28.png` |
| `28` | 7399–7523 | 124 | `v3-f69-28` | `v4-28` | `019f95b5-0c6b-76a2-af77-7cba944b93de.png` |
| `28b` | 7607–7742 | 135 | `v3-f69-28` ↩ | `v4-28b` | `019f95b6-ebac-7953-bb22-914ef759e8eb.png` |
| `29c` | 7742–7823 | 81 | `f70-28a` ↩ | `v4-29c` | `019f95a0-cce5-7982-987a-d4bffc174f2a.png` |

**One correction to the brief.** The dispatch listed `28`'s first instance at
`7461–7607`. The live v3 timeline has it at **7399–7523** (`7461` is the frame
the v3 QC record inspected inside that clip, and `7607` is where the *next*
swap begins). The timeline was treated as the authority, so `28` was replaced
at 7399–7523 and its neighbour `28a` at 7523–7607 was left untouched. Had the
brief's range been used literally it would have overwritten `28a`.

**Timing is provably unchanged.** The mutation returned exactly **9 new clips**
and exactly **9 `removedClipIds`**, with every `frames` pair and every
`trimEndFrame` identical to the v3 clip it replaced. No neighbouring hold was
touched, the narration was not re-placed, the matte and the title card are as
built in v2.

Suffix order is not screen order, per the Art Director: cut to frame numbers.
`20b` plays after `21b`; `17b` and `18b` play after `23a`; `29c` plays before
`29a`. All four landed in frame order, not alphabetical order.

## Type sheet — one change

| Card | v3 text | v4 text | Frames | Font | Colour |
|---|---|---|---|---|---|
| Colophon line 2 | seventy-five frames · one voice · ten sources · all verified · owned outright | **eighty-three frames** · one voice · ten sources · all verified · owned outright | 8410–8530 | CourierPrime-Regular 24 | `#1F1E1D` |

The count was true in v2 and v3 and is false in v4 — the film now runs 83 cuts
on 83 distinct pictures. A card may not carry a claim that is no longer true, so
the numeral was corrected. Nothing else on the card moved: same font, same size,
same colour, same box, same 120-frame hold. Title card (`THE PRICE OF A GLANCE`,
EBGaramond-Regular 58) untouched.

## Grade

None. No grade applied in v2, v3 or v4 — the frames are flat ivory-ground
line art and the ivory matte carries the paper. Unchanged.

## Matte

Ivory `#FAF9F6` (`ivory-ground`, `9700AC54`) full-length on V1, frames 0–8530.
Unchanged from v2.

## QC record — real observations

**The headline check — no image appears twice.** All 83 picture clips were read
off the timeline and checked three ways:

1. **83 clips, 83 distinct `mediaRef` values.** `sort -u` on the ordered ref
   list returns 83; `uniq -d` returns nothing.
2. **83 distinct backing files.** Every `mediaRef` was mapped to its staged PNG
   (66 in `stills-cut-v2/frames`, 8 in `stills-cut-v3/frames`, 9 in
   `stills-cut-v4/frames` — 66 + 8 + 9 = 83) and the mapping was verified
   bidirectionally complete against the timeline.
3. **83 distinct md5 hashes.** Content-level, not name-level: two different
   library assets pointing at identical bytes would have been caught. No
   duplicate-content group exists. **83 / 83.**

**Dead paths — all three absent, checked by content hash, not by filename.**

| Dead file | Was | md5 | On timeline |
|---|---|---|---|
| `019f9579-4cde-7bb1-aac0-6ec0da554222.png` | old `28` | `e6d05767…` | **absent** |
| `019f95a0-cc8a-7113-b3e3-4c671706a4b8.png` | old `28b` | `dd1ea717…` | **absent** |
| `019f95b5-0d55-7de1-b365-c4c9c9665ba4.png` | `28b` first pass | `099e479c…` | **absent** |

The v3 asset `v3-f69-28` (`E4779A62`), which carried the machine-scale `28`, is
also gone from the timeline entirely — both of its occurrences were replaced.
And each of the nine FINAL paths in the frame book was hashed and matched to the
clip it was supposed to land on: **9 / 9 OK.**

**Gap scan:** PASS. Picture track V2 reports 83 clips and **no `gaps` key**.
Independently re-derived by arithmetic across all 83 `[start, end)` pairs:
contiguous **90 → 8410**, zero gaps, zero overlaps. Shortest clip is 31 frames
(`4`, 1.03 s) — no slivers. Matte V1 contiguous 0–8530. A1/A2 narration
unchanged (the reported gaps are the alternating-track act boundaries, as in v2
and v3).

**Duration:** 8530 frames / **284.333 s** — identical to v3 and v2. ffprobe on
the master: `duration=284.333333`, `nb_frames=8530`, 1920×1080,
`r_frame_rate=30/1`, h264 + aac 44.1 kHz mono, 84,799,878 bytes. (v3 was
85,619,032 — the delta is the nine new images' compression, not a timing change.)

**Black-frame scan:** `ffmpeg blackdetect=d=0.05:pix_th=0.10` across the whole
master returned **no detections**.

**Last frame:** f8529 is the colophon — both lines, both fonts, on ivory, with
the corrected "eighty-three frames". The frame I meant.

**All nine replaced clips inspected individually, composited on the timeline.**
Bald hero, exactly one flat tomato-red element, zero lettering on every one:

- **f3300 `12b`** — the builder has tipped his chair right back with both boots
  on the drafting table, one arm behind his head, waving breezily, eyes shut in
  a contented grin. The finished phone lies beside the boots, red screen up. The
  hero is small at frame right with speed lines, already walking out. Widest
  frame in the workshop set — bench tools, timber, cabinets. One red = the phone
  screen. The "they did it anyway" shrug is entirely in the boots.
- **f4295 `16b`** — the only fully static frame in Act IV: hero bolt upright,
  shoulders at his ears, both palms flat on the tan desk, eyeballs swivelled
  hard sideways at a phone that is doing absolutely nothing. One sweat drop.
  One red = the inert screen. Against `16`'s rubber arm it reads as stillness,
  which is the point of "it doesn't have to buzz".
- **f4365 `16c`** — the chair is behind him with wobble lines and dust puffs, he
  is out of it entirely, cheek laid on the desk an inch from the phone, one long
  arm stretched all the way back holding a grey pencil over the chair. Eyes
  clamped, tongue out. Desk renders grey here where `16b`'s is tan — same wall,
  same window, and on a 1.67 s cut it does not read as a new room. One red = the
  screen at the desk corner.
- **f5744 `20b`** — the scale reversal lands. A vast empty tan plane with a
  single horizon line and the hero tiny at dead centre, on all fours, loupe in
  one eye, nose almost on the floor, examining a red speck a few pixels across.
  The most negative space in the film. One red = the speck.
- **f6250 `17b`** — standing square to camera, level brows, firm mouth, counting
  on his fingers. No shrug, no wince, no sweat. Warm wall and window behind,
  phone ignored on the floor. It is the only direct-address posture in Act V and
  it carries "the tricks are real" without turning sincerity into a gag. One red
  = the phone screen on the floor.
- **f6385 `18b`** — down on one knee with two grey rulers gone bent and wavy like
  cooked noodles, wobble lines along both, one folding over on itself. Both
  rulers **completely blank** — no printed scale, no tick marks, no numerals.
  Half-lidded deadpan, one brow hiked. One red = the speck on the floor being
  measured. "Badly measured" is the picture, not a caption.
- **f7460 `28`** — the scale fix. Waist-high grey cabinet, lever hauled down, the
  hand-sized phone sitting in a grey cradle on the front with its red screen up.
  Window upper-left, grey counter beneath it, bald head clear against plain tan
  wall. Bulging eyes, open mouth, sweat flying. One red = the small phone screen.
  The giant machine-phone is gone.
- **f7675 `28b`** — the anticlimax, and it is staged as a mirror of `28`: cabinet
  at frame left, hero at frame right, lever standing untouched, face gone
  completely flat. He is holding up a grey sock. Payout tray open and empty with
  one dust puff. Cabinet front is bare grey metal — no second screen, no display
  panel. Zero lettering, no `?` glyph, no numerals on the till. One red = the
  phone in the cradle.
- **f7780 `29c`** — extreme backward lean, arms wrapped round his own chest,
  heels skidding with motion lines and dust, teeth gritted, eyes clamped, sweat
  flying — while the phone sits calmly upright on the floor doing nothing and
  winning. One red = the upright screen. Physical comedy against total stillness.

**Act VII now reads as one room, one phone.** The four consecutive cuts were
checked as a run at f7460 `28` → f7565 `28a` → f7675 `28b` → f7780 `29c`. All
four share the warm tan wall, the grey floor and the tall window with a grey
sill, and the phone is hand-sized in all four. The old giant-versus-hand
flip-flop is gone. The residual read is positional, not scale: the phone is
*docked in the cabinet* in `28` and `28b` and *on the floor* in `28a` and `29c`.
That is a far smaller jump than the old one and each gag needs the phone where
it is — `28a`'s whole joke is the phone begging on the floor. The window sits
upper-left with the counter beneath it in `28`/`28b` and centre-right without a
counter in `28a`/`29c`, which reads as two angles on one room rather than two
rooms. Accepted as built.

**Eight frames extracted across the film and actually looked at** — f533 `2`
(drowning in grey mail, one red flag), f1599 `6` (crouched over the phone,
red screen), f2665 `10b` (mound of grey badges, one red on top, × eyes),
f3731 `14` (ghost head drifting to the doorway, distant red screen), f4798 `19`
(clock face, one red hand), f5864 `22` (potato tied with red string vs glasses),
f6930 `25a` (ring of grey figures round one red fire), f7996 `29` (badge
deflating with a frowning face). Bald hero where he appears, one flat red each,
no lettering anywhere.

## Master

- **Path:** `/Users/isaachernandez/blog design/output/the-price-of-a-glance-final.mp4`
- H.264, 1920×1080, 30 fps, **8530 frames / 284.333 s**, aac 44.1 kHz mono,
  84,799,878 bytes. ffprobe-verified, black-frame-scanned, gap-scanned.

## Editions

**Master only.** The 9:16 edition was explicitly out of scope for this pass.
Nothing published; nothing sent to Channel Studio's approval register.

## Anything noticed now that no image repeats

- **The film got less repetitive in a way that is bigger than eight frames.**
  Every cut-back sat at the *end* of a beat — the third or fourth cut in a run,
  the one that had to carry the longest hold. Returning to a picture there was
  quietly telling the viewer the beat was over. With eight fresh pictures those
  eight beats now escalate to the end instead of settling, and Act V in
  particular reads as one long climb rather than three climbs and a rest.
- **The cut-backs had been hiding a pacing problem.** `17` ↩ was a 5.17 s hold on
  a picture the viewer had already had 1.43 s of. That is why it felt slow in v2
  — not the length, the familiarity. `17b` at the same 5.17 s does not drag. The
  same is true of `12` ↩ (3.23 s) and `28` ↩ (4.50 s). **Length is not what makes
  a hold feel long; novelty is.** I would now read every hold over 4 s as a
  question about the picture, not the timing.
- **`20b` is the strongest single frame added.** It solves "at most four tenths
  of one percent" by *changing the scale of the frame* rather than adding a prop
  to the existing one. Every other escalation in the film stacks objects; this
  one removes them. It is also the quietest frame in a loud act and the cut into
  it lands harder for it.
- **The `28`/`28b` mirror is a technique worth reusing.** Same room, same
  furniture, staging flipped left-to-right, lever hauled vs lever at rest. It
  reads instantly as *later*, with no dissolve and no card, which is exactly
  what a hard-cut-only film needs for "time passed".
- **Only two frames in the whole 83 now share a set at the same angle**
  (`16b`/`16c`, and their desk colour differs). The film is more varied than any
  previous version and it no longer has a "we're back here again" feeling in
  Acts III, IV, V or VII.

## Notes back — for the next film

- **Budget frames per cut, not per beat.** The eight cut-backs existed because
  the shot list was built per beat and the cut needed more pictures than beats.
  Count the cuts the transcript wants first, then commission that many frames.
  On this film that would have been 83 from the start instead of 75 + 8 + 9.
- **A colophon that counts anything will go stale.** "seventy-five frames" was
  true for two exports and false for the third, and only caught because the last
  frame is on the QC list. Either count nothing on the card, or make the count
  the last thing set before export. I would now write the colophon *after* the
  final picture lock, not with the rest of the type.
- **Frame-range instructions should be quoted from the timeline, not from a QC
  record.** The `7461` in this dispatch came from a v3 inspection frame and would
  have destroyed `28a` if placed literally. Dispatches that name frame ranges
  should cite the `frames` pair from `get_timeline`, which is unambiguous.
- **Verify uniqueness by content hash, not by asset name.** Library assets are
  cheap to duplicate under new names; three of the media entries in this project
  point at the same picture under different labels from earlier passes. The md5
  pass is the only check that would have caught a rename.
- **Naming a new frame after the frame it retires is a trap.** `20b`, `17b`,
  `18b` and `29c` all sort into the wrong place alphabetically and none of them
  plays next to its namesake. Name replacement frames by their *position* in the
  cut, not by their ancestry.

---

# v5 — THREE VERTICAL EDITIONS, filed 2026-07-24

> **Social editions only. The master `output/the-price-of-a-glance-final.mp4` and
> every timeline in `the-price-of-a-glance.palmier` — including `stills-cut-v4`
> — are untouched.** Same non-negotiables as the master: still images only, no
> motion, no keyframed transforms, no transitions, hard cuts always.
> **$0 spent — assembly only, no generation of any kind.**

## Why a separate Palmier project

Palmier's aspect ratio is a **project** setting, not a per-timeline one.
Switching this project to 9:16 would have re-fitted every clip in
`stills-cut-v4` and the three earlier timelines. So the verticals were built in
a **new** project, `the-price-of-a-glance-shorts.palmier`
(`/Users/isaachernandez/Documents/Palmier Pro/the-price-of-a-glance-shorts.palmier`),
1080×1920 @ 30 fps, three timelines: `short-1-pigeons` (`31D94E93`),
`short-2-potatoes` (`DD87CEB5`), `short-3-thirty-five-seconds` (`1490A5D4`).
That satisfies "leave the earlier timelines untouched" more strongly than a new
timeline in the same project would have.

## Sources bound

- **Picture** — the same 83 live v4 PNGs (`stills-cut-v2/v3/v4 frames/`),
  pre-cropped offline to 1101×768 (10 % off each side) so the vertical layout
  needs only a transform, not a keyframed crop. No image is reused inside a short.
- **Voice** — cut out of the published master's own audio track, so the verticals
  are provably the same performance at the same level as the long form. Nothing
  re-recorded, nothing re-rendered.
- **Word timings** — `inspect_media wordTimestamps` on the master audio, on-device.
  Every segment boundary sits in a measured inter-word gap, never inside a word.
- **Caption text** — spellings taken from `output/publish/captions-en.srt`
  (Ferster, Orben, Przybylski, Leroy, Ward all corrected off the ASR).
- **No score, no room tone, no grade** — as in the master.

## The vertical layout — and why it is not a 9:16 crop

A true 9:16 cover-crop of a 1376×768 frame keeps **31 % of the width**. Every
two-object gag in this film dies at that crop: the potato and the spectacles sit
either side of centre, both pigeons sit either side of the scientist, the crowd
frames run to both edges. The FRAME-BOOK flagged shot 21 specifically; the same
problem applies to `8`, `8a`, `8b`, `21`, `21a`, `22`, `22a` and `24`.

So the vertical is a **designed page, not a crop**:

| Band | y | Content |
|---|---|---|
| top | 0–20 % | ivory; running kicker at 15 % (CourierPrime 19, tracking 4, `#8A8784`) |
| picture | 20.0–59.2 % | full canvas width, 1080×754, source cropped 10 % L/R |
| caption | 59.2–~78 % | HelveticaNeue-Bold 46, `#1F1E1D`, box centred (0.5, 0.66), width 0.73 |
| chrome | 78–100 % | ivory, deliberately empty |

The ivory `#FAF9F6` house matte runs full length on the bottom track of all
three, so the empty bands read as the film's own paper, not as letterbox. Type
sits on flat ivory, which is the highest contrast available and needs no scrim.

**Safe zones held:** top 10 % (platform chrome), bottom 22 % (caption /
handle / description drawer) and right 12 % (action rail) are all free of type.
Type boxes were narrowed from 0.86 to **0.73** after the first export showed the
kicker "FERSTER & SKINNER · 1957" and the widest captions grazing the right rail
at x = 950. Picture is allowed under the rail; type is not.

## SHORT 1 — "The Pigeons"

`output/publish/short-1-pigeons.mp4` — 1080×1920, 30 fps, **1324 f / 44.13 s**,
h264 + aac 48 kHz mono, 9,626,805 bytes. ffprobe-verified.

**Beat used (master seconds):** 55.59–98.22, reordered into three chunks —
hook `71.37–81.09`, then setup `55.59–71.37`, then payoff `81.09–98.22`.

**Hook:** first line "Of everything they tested, it was the hardest habit to
break." over frame `8` — the manic mallet pigeon, the deadpan scientist and the
flat-on-its-back clockwork pigeon, which is the funniest single frame in the
film and the right thumbnail. No title card, no build.

**Landing:** frame `11b` held 3.40 s, closing on "An end, and it was on purpose."

| Frame | In | Out | f | Hold |
|---|---:|---:|---:|---:|
| `8` | 0 | 110 | 110 | 3.67 s |
| `8a` | 110 | 211 | 101 | 3.37 s |
| `8b` | 211 | 292 | 81 | 2.70 s |
| `6a` | 292 | 361 | 69 | 2.30 s |
| `6b` | 361 | 449 | 88 | 2.93 s |
| `7a` | 449 | 558 | 109 | 3.63 s |
| `7` | 558 | 673 | 115 | 3.83 s |
| `7b` | 673 | 765 | 92 | 3.07 s |
| `9a` | 765 | 797 | 32 | 1.07 s |
| `9` | 797 | 847 | 50 | 1.67 s |
| `9b` | 847 | 887 | 40 | 1.33 s |
| `10a` | 887 | 918 | 31 | 1.03 s |
| `10` | 918 | 957 | 39 | 1.30 s |
| `10b` | 957 | 1049 | 92 | 3.07 s |
| `11a` | 1049 | 1108 | 59 | 1.97 s |
| `11` | 1108 | 1222 | 114 | 3.80 s |
| `11b` | 1222 | 1324 | 102 | 3.40 s |

17 cuts, 17 unique frames, **average hold 2.60 s** (master 3.34 s). 37 caption
cards. Kickers: VARIABLE RATIO / FERSTER & SKINNER · 1957 / THE LEVER IN YOUR HAND.

## SHORT 2 — "Potatoes and Glasses"

`output/publish/short-2-potatoes.mp4` — 1080×1920, 30 fps, **1429 f / 47.63 s**,
h264 + aac 48 kHz mono, 11,822,685 bytes. ffprobe-verified.

**Beat used:** 166–217 of the master, reordered — hook `192.70–199.89`, then
`171.30–192.70`, then `199.89–216.95`.

**Hook:** "In the same data, eating potatoes looked almost as bad for you." over
frame `22` — the human weighing scale, potato on one palm, spectacles on the
other. The sharpest claim in the act, on screen at frame 0.

**Landing:** frame `24` (the podium, the speck in the tweezers) held 3.80 s over
"Both are true at once." and 2.0 s of silence after it.

**How the shot-21 crop problem was solved.** Not by stacking, not by
substituting `22a`, and not by a pan (unavailable). By **refusing the 9:16
centre crop entirely**: the picture block spans the full canvas width, so the
frame is only cropped 10 % off each side. The potato sits at 24–36 % of source
width and the spectacles at 61–76 % — both survive a 10–90 % window with room to
spare, the red thread on the potato stays inside the visible column and clear of
the action rail, and the two-shot reads as a comparison exactly as composed.
Verified on the exported file at frame 0 with the safe zones overlaid.
The same decision rescues `8` (both pigeons), `21`/`21a`/`21b` (crowd to both
edges) and `24` (podium plus crowd) at no extra cost.

| Frame | In | Out | f | Hold |
|---|---:|---:|---:|---:|
| `22` | 0 | 124 | 124 | 4.13 s |
| `22a` | 124 | 216 | 92 | 3.07 s |
| `20a` | 216 | 276 | 60 | 2.00 s |
| `21a` | 276 | 405 | 129 | 4.30 s |
| `21` | 405 | 516 | 111 | 3.70 s |
| CARD `355,000 / TEENAGERS` | 516 | 619 | 103 | 3.43 s |
| `21b` | 619 | 712 | 93 | 3.10 s |
| `20` | 712 | 789 | 77 | 2.57 s |
| `20b` | 789 | 858 | 69 | 2.30 s |
| `23` | 858 | 957 | 99 | 3.30 s |
| `23a` | 957 | 1044 | 87 | 2.90 s |
| `17b` | 1044 | 1144 | 100 | 3.33 s |
| CARD `THE TRICKS / ARE REAL.` | 1144 | 1201 | 57 | 1.90 s |
| `18b` | 1201 | 1315 | 114 | 3.80 s |
| `24` | 1315 | 1429 | 114 | 3.80 s |

15 cuts, 13 unique frames + 2 cards, **average 3.18 s**. 30 caption cards.
`20` (the single magnifying glass) is lifted out of master order to serve "And
negative," so that `20b`'s vast empty plane can land on "four tenths of one
percent" — the two magnifier frames pair, so the cut does not read as a jump.

## SHORT 3 — "Thirty-five seconds"

`output/publish/short-3-thirty-five-seconds.mp4` — 1080×1920, 30 fps,
**1493 f / 49.77 s**, h264 + aac 48 kHz mono, 9,209,533 bytes. ffprobe-verified.

**Beat used:** Act IV→V, 113–163 of the master, reordered — hook
`146.67–151.11`, then setup `114.45–146.67`, then the retraction `151.11–162.42`.

**Hook:** "Okay. That last study is the weakest thing I've shown you." over frame
`17a` — the sheepish palm-up shrug, phone set down and ignored. The film's own
self-correction is the first thing on screen, which is the whole reason this
short exists.

**Landing:** frame `19a` (the dry aside at the clock, stopwatch in hand) held
1.80 s in silence after "I just spent 35 seconds on that."

| Frame | In | Out | f | Hold |
|---|---:|---:|---:|---:|
| `17a` | 0 | 94 | 94 | 3.13 s |
| `17` | 94 | 133 | 39 | 1.30 s |
| `13` | 133 | 163 | 30 | 1.00 s |
| `14a` | 163 | 249 | 86 | 2.87 s |
| `14` | 249 | 363 | 114 | 3.80 s |
| `14b` | 363 | 436 | 73 | 2.43 s |
| `16b` | 436 | 523 | 87 | 2.90 s |
| `15a` | 523 | 592 | 69 | 2.30 s |
| `15` | 592 | 729 | 137 | 4.57 s |
| `16` | 729 | 831 | 102 | 3.40 s |
| `16a` | 831 | 975 | 144 | 4.80 s |
| `16c` | 975 | 1100 | 125 | 4.17 s |
| `18` | 1100 | 1186 | 86 | 2.87 s |
| CARD `2022 / SAME STUDY, AGAIN` | 1186 | 1301 | 115 | 3.83 s |
| `18a` | 1301 | 1354 | 53 | 1.77 s |
| `19` | 1354 | 1439 | 85 | 2.83 s |
| `19a` | 1439 | 1493 | 54 | 1.80 s |

17 cuts, 16 unique frames + 1 card, **average 2.93 s**. 38 caption cards.
Ward's frames were re-timed against the transcript rather than copied from the
master: `16b` is promoted to carry "Adrian Ward's team, 2017." so that `15`
(the comic gulf, phone abandoned across an empty floor) can carry the
desk / pocket / another-room list, which is the finding it actually states.

## Type sheet — all three editions

| Element | Font | Size | Colour | Position | Animation |
|---|---|---:|---|---|---|
| Burned-in captions | HelveticaNeue-Bold | 46 | `#1F1E1D` | (0.50, 0.66), w 0.73 | **off** |
| Running kicker | CourierPrime-Regular | 19, tracking 4 | `#8A8784` | (0.50, 0.15), w 0.73 | **off** |
| Number / claim cards | CourierPrime-Regular | 54, tracking 2 | `#1F1E1D` | (0.50, 0.396), w 0.70 | **off** |

No animation anywhere — the hard-cut rule applies to type as well as picture.
House type is kept for the kicker and the cards; captions use a bold grotesque
because EB Garamond and Courier Prime both fail the phone-size legibility test
at caption weight. That is a deliberate, documented departure from house type
for the social editions only.

**Every card claim is in the Director's verified source table:** 355,000
teenagers (Orben & Przybylski 2019), "the tricks are real" (spoken verbatim),
2022 / same study, again (the pre-registered replication of Ward 2017).

## QC record — real observations

- **Gap scan.** Short 1 picture track contiguous 0→1324, no `gaps` key. Short 2
  picture reports gaps `[516,619]` and `[1144,1201]`; Short 3 reports `[1186,1301]`
  — those are the three card beats, where the ivory is meant to show. No
  one-frame slivers anywhere; shortest picture clip is 30 f (`13`, 1.00 s).
  Two one-frame caption gaps found on Short 1 (f765) and Short 2 (f858) at
  segment joins and closed.
- **Duration and format.** ffprobe on all three: `1080×1920`, `r_frame_rate=30/1`,
  h264 + aac 48 kHz mono. 1324 f / 44.133 s, 1429 f / 47.633 s, 1493 f / 49.767 s
  — each matching its timeline exactly. All inside the 40–60 s target.
- **Levels.** `volumedetect`: mean −24.0 / −25.0 / −25.4 dB, peak −3.9 / −7.1 /
  −5.2 dB. Consistent across the three and matching the master's −24.8 dB mean,
  with real headroom left for platform normalisation.
- **Black-frame scan.** `blackdetect=d=0.05:pix_th=0.10` — **zero detections** on
  all three. Nothing fades to black; the ground is ivory throughout.
- **A silent first export was caught and fixed.** The first pass produced three
  files at −91 dB — digital silence. Cause: the segment extractor used
  output-side `-ss`, so the `afade=t=out` filter ran against un-reset input
  timestamps and its fade-out had already completed before the segment began.
  Fixed by moving the seek to input-side (`-ss`/`-t` before `-i`) and re-cut.
  **This is exactly why levels get measured and not assumed.**
- **Nine frames extracted from the exported files and looked at**, each with the
  three unsafe zones drawn on (top 10 %, bottom 22 %, right 12 %):
  - **S1 f0** — both pigeons and the scientist present, mallet inside frame, red
    lever handle clear of the rail; caption two lines, well above the bottom band.
    Good thumbnail.
  - **S1 f760** — pellet lodged in the forehead, kicker now clear of the right
    rail (it was not, in the first export).
  - **S1 f1000** — the endless feed ribbon, one red dot, caption clean.
  - **S2 f0** — **the potato/glasses two-shot intact.** Potato with red thread at
    frame left, spectacles at frame right, both fully inside the visible column.
    The FRAME-BOOK's vertical warning is closed.
  - **S2 f340** — Orben/Przybylski kicker one line, inside the rail.
  - **S2 f560** — the `355,000 TEENAGERS` card, Courier Prime, centred, clean.
  - **S3 f0** — the sheepish shrug and the red phone on the floor, "OKAY." on
    screen at frame 0.
  - **S3 f470** — the side-eye at the inert phone, "ADRIAN WARD'S TEAM, 2017."
    spelt correctly.
  - **S3 f1420** — the clock, red hand, "35 SECONDS ON THAT."
- **Last frame checked on each:** S1 f1323 `11b`, S2 f1428 `24`, S3 f1492 `19a`.
  All three are the held landing frame with no caption on screen and no dead
  air — the frames I meant.
- **Caption spellings** cross-checked against `captions-en.srt`: Ferster,
  Skinner, Orben, Przybylski, Leroy, Ward all correct. The ASR's "Firster",
  "Orban", "Prubilsky" and "Not an outrage" were all corrected before placement.

## Editions

| File | Format | Duration | Serves |
|---|---|---:|---|
| `output/publish/short-1-pigeons.mp4` | 1080×1920 h264 30 fps | 44.13 s | Shorts · TikTok · Reels · X |
| `output/publish/short-2-potatoes.mp4` | 1080×1920 h264 30 fps | 47.63 s | Shorts · TikTok · Reels · X |
| `output/publish/short-3-thirty-five-seconds.mp4` | 1080×1920 h264 30 fps | 49.77 s | Shorts · TikTok · Reels · X |

One file per short serves all four platforms: 40–60 s clears every length
ceiling, and the layout respects the most aggressive chrome of the four.
**Nothing published. Nothing sent to Channel Studio's approval register.**

## What fought the vertical

- **`8` (two pigeons)** — the clockwork pigeon's head and the little clock prop
  sit at 90–96 % of source width and land under the action rail. The gag still
  reads (body, legs-up pose and the manic pigeon all survive), but it is the one
  frame where the rail eats something the composition wanted.
- **`22`/`22a`** — solved by full-width layout, but they had **no** margin left:
  at any crop tighter than ~80 % of source width the comparison dies. If a future
  film wants a real 9:16 cover-crop, two-object gags have to be composed inside
  the centre 34–66 % or shot twice.
- **`20b`** (the vast empty plane, hero a few pixels across) is the frame that
  suffers most at phone size — the FRAME-BOOK warned the emptiness is the
  content, and at 1080×754 the figure is very small. It survives because it holds
  only 2.30 s and the caption carries the number.
- **`16a`** at 4.80 s and **`15`** at 4.57 s are the two slowest holds in Short 3,
  both in the Ward setup. Both are busy frames, but they are the places a viewer
  could leave.
- **The bottom 22 % is empty ivory in every frame of all three.** That is
  correct — it is the platform's chrome zone — but on a device with light
  chrome it will read as generous white space rather than as design. Accepted.

## Notes back — for the next film

- **Compose for two aspect ratios or accept a designed page.** Nothing in this
  frame set can survive a true 9:16 cover-crop, because every gag is a
  left-versus-right comparison. Either the Art Director puts the subject and the
  accent inside the centre 34–66 % column, or the Editor builds a vertical page
  and gives up on full-bleed. The page won here and it is the better answer for
  a paper-ground film, but it was a decision forced late.
- **A running kicker is worth more than a title card.** It gives the vertical a
  visible change on every act turn, uses the dead top band, names the researcher
  where the caption cannot afford the characters, and costs no screen time. Build
  it into the type sheet from the start.
- **House type is not caption type.** EB Garamond and Courier Prime are right for
  the film and wrong for a muted phone. Budget a third face — one bold grotesque —
  in the design language, so the social editions are not an exception each time.
- **Numbers belong on cards, and cards belong in the picture block.** Cutting the
  picture out entirely for `355,000 TEENAGERS` reads as a beat, not an
  interruption, and it also solved the pacing problem in the middle of Short 2's
  setup. Two of the three shorts needed exactly this; plan one card per short.
- **Cut the audio out of the finished master, not from the stems.** Reordering
  the beats meant three audio chunks per short; taking them from the published
  master guaranteed the same performance and the same level as the long form,
  and made the levels check a one-line comparison. Do not re-mix a vertical.
- **Measure the export, always.** The first three files were digitally silent and
  looked perfectly fine on every frame inspection. Only `volumedetect` caught it.
