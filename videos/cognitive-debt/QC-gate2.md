# QC — GATE 2 (the frames) · cognitive-debt

**Filed 2026-08-04 · QC chair · run before any motion or assembly is paid for.**
Artifacts audited: 88 frames in `public/images/frames/`, `production/prompts.json`,
`production/refs/` (10 plates), `STORYBOARD.md`, `WORLD.md`.

---

## VERDICT — **FAIL**

Do not pay for motion. Do not assemble.

**Blocking items, in order of severity:**

1. **2.3 — LETTERING IS IN THE FILM.** `b17`'s machine screen carries a rendered
   scene with a green segmented display showing garbled glyph characters.
2. **2.6 / 2.4 — the STATION motif is absent from 10 of its 11 frames.** The
   electrode cap and cords exist correctly in `refs/station.png` and appear only
   in `b13`. Elsewhere they are a red or black **baseball cap**, or nothing.
3. **2.4 — the STAIR motif breaks at `b85`: EIGHT treads**, measured, not
   eyeballed. The film's principal motif is "exactly seven".
4. **2.9 — 4 of the 5 LIVE stills are not animatable as boarded.** `b72`'s
   composition is entirely absent; `b08` cannot show a tread lowering into a gap;
   `b46` shows the face the board forbids; `b14` has the wrong cap.
5. **WORLD violation — the forbidden red margin rule is in 7 frames.**
6. **Board prohibition 2 violated — the Carr figure's face is visible** in `b45`,
   `b46`, `b50`. Named living person.
7. **`production/prompts.json` is still damaged in 19 of 88 records** — a
   different bug from the one reported, still live, and it deletes frame subjects.
8. **10 frames the board specifies as "No figure" contain a figure**, including
   `b69` ("Nobody came to the funeral"), which is the exact inverse of its board.

**63 of 88 frames require retake.** Full list in Returns.

---

## Item table

| # | Check | Evidence | Verdict |
|---|---|---|---|
| 2.1 | Frame count vs prompts.json | `ls public/images/frames \| wc -l` = **88**; `len(json.load(prompts.json))` = **88**; key sets identical (`b01`–`b88`) | **PASS** |
| 2.2 | 1920×1080, no inset painted panel | `magick identify` on all 88: every frame `1920x1080 sRGB 8`. Trim-box at fuzz 0 = `1920x1080+0+0` on all 88. Fuzz-3% trim run on all 88 (not the 12 floor): width stays 1920 on 87 of 88; only vertical trim (top ≤49px, bottom ≤50px) = paper margin above the first rule, not an inset. `b60` = `1891x985+0+46` (29px width loss, no x-offset) — not a panel. | **PASS** |
| 2.3 | No lettering anywhere | Whole film contact-sheeted (3 sheets, 8-up) and read; then re-read at 458px in six 4×4 sheets. **`b17` FAILS**: the machine screen carries an interior scene with a green segmented display bearing glyph characters (~"8A8"), plus a red LED block and a thumbnail panel. Verified at 2.5× crop. No lettering found in the other 87. | **FAIL — b17** |
| 2.4 | Character holds: head shape, EXACTLY two hairs, jacket | All 88 crowns cropped via red-jacket anchor and read; ambiguous frames re-zoomed twice (third pass run where reads disagreed, per hard rule). **Head shape: holds on all 88. Jacket: holds on all 88 — no deviation found.** **Hair-count deviations: 3 — `b18` (ZERO hairs), `b51` (ONE), `b87` (ONE).** Separately the crown is covered by a **wrong hat** in 5 frames (`b14` `b15` `b20` `b22` `b24`) and is bare where the board requires the capped head in `b19`. Note `b06`/`b07` initially read as one hair at 0.47× and are TWO at 1.25× — third pass confirms two; recorded because the low-zoom read was wrong. | **FAIL — b18, b51, b87** |
| 2.5 | One accent per frame; world matches WORLD.md | Hue census across all 88. A **second chromatic accent — saturated warm brown/tan (h≈30-36, s 0.33-0.47, v 0.57-0.81)** — appears in `b14 b17 b18 b20 b22 b27 b32 b47 b75 b76 b77`; **blue** (h=224) in `b24`; **amber** headlamp/marker in `b09`; **cyan/teal/green** inside `b17`'s screen. Desks are brown in `b02 b17 b40 b65` and grey/white in `b13 b15 b18 b20 b32` — inconsistent inside continuity group G2. **World clause violation:** the forbidden red vertical margin rule is present in **7 frames — `b04` `b18` `b22` `b30` `b50` `b82` `b87`** (detected on the R−G channel at two independent thresholds; confirmed visually on a 7-up left-strip crop). WORLD.md §2 forbids it by name and by test. World is the ledger, not a previous film's cream — no catalogue collision. | **FAIL** |
| 2.6 | No donated / invented props | Cross-read against STORYBOARD.md §5. **Invented props:** `b23` a small tomato-red cube in the interviewer's palm — the board says the hand is **empty**, and `b24`'s punchline is that it stays empty; `b82` a large red paperclip on the sheet, absent from `b03` which `b82` must match exactly; `b60` a stack of red bricks where the board asks for one sheaf and a blank card. **Motif substitution:** the `sheaf.png` stack (blank pale sheets) is drawn as **bound books with coloured spines/edges** in `b27 b29 b42 b60 b63 b80`. **Motif absence:** the electrode cap + cords of `refs/station.png` are missing from `b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b32` — present only in `b13`. | **FAIL** |
| 2.7 | Animated frames carry no data; RMSE drifts looked at | No clips exist; no animate-frames log exists (`find` returns nothing for `*.mp4`, `*animate*`). Nothing to read. | **NOT RUN — no artifact yet** |
| 2.8 | Every clip corresponds to a `LIVE` beat | `renders/` empty, no clips directory, zero `.mp4` in the tree. No unrequested clip can exist. Board's motion column marks exactly 5 `LIVE`. | **PASS (vacuous — no clips)** |
| 2.9 | 4–6 `LIVE`, non-adjacent, classed, "what moves" line, no data | Board §4: **5 LIVE** — `b08` `b14` `b46` `b72` `b88`. Non-adjacent (gaps 6/32/26/16). Classes assigned 1·3·5·1·2, each in the five-class set (class 1 used twice, class 4 unused — permitted). Each carries an explicit "what moves, and why this beat needs it" line. Six data-carrying beats (`b21 b31 b33 b34 b37 b66`) explicitly refused for LIVE. **The board's plan passes.** **The stills do not:** `b72` does not contain the boarded composition at all (no sheet, no lifted corner, no dot, no hand); `b08` shows the figure standing on the stair with both arms raised and no gap, so "the red tread lowers into the gap" has nothing to lower into and no matching `b07` framing; `b46` shows the face; `b14` has a baseball cap instead of the electrode cap. Only `b88` is animatable as boarded. | **FAIL — 4 of 5 stills unsafe to animate** |
| 2.10 | Each clip: one motion, starts after the cut, settles, 30fps | No clips exist. | **NOT RUN — no artifact yet** |

### Additional findings outside the numbered rubric — filed, not waived

| Finding | Evidence |
|---|---|
| **`production/prompts.json` is damaged in 19 of 88 records, right now** | The reported `\bAnchor\s*` bug is genuinely fixed — I reconstructed the old builder and diffed; it accounts for 5 records, not 15. The live damage is the **`DEAD_CLAUSE` regex** `[^,.;]*\b`?b\d+`?\b[^,.;]*`, which deletes the whole clause containing a frame reference **including the sentence's subject**. `b72` → *"same last sheet lifted at the same bottom corner…"* (lost the entire composition). `b37` → *"at eye level with it…"* (lost "The protagonist crouched"). `b41` → *"the other taking it…"* (lost the tomato-red block). `b55` → *"then a gap, then the two thick stacks together"* (lost the folded sheet). `b62` → lost "The protagonist seated as in b61". `b70`, `b51`, `b31`, `b45`, `b46`, `b86`, `b88` likewise. Production codes leak **into** the prompt in `b66 b67 b69` ("G3b."), and `b69` carries QA prose: *"Hold risk: below the 1.8s floor — see §8."* `b03`/`b82` self-inline into a duplicate with a dangling *", same hand position, same sheet size."* |
| **The prompts that produced these frames no longer exist** | `spend.log` last write 22:15:46; `prompts.json` mtime 15:22 local (7 min later). No archived copy. **No frame in this film can be audited against the text that made it.** Archive the prompt file with the batch. |
| **The plates are correct; the frames ignored them** | `refs/stair.png` = seven treads, fourth red ✔. `refs/station.png` = electrode cap + cords ✔. `refs/three-desks.png` = three capped stations ✔. `refs/footnote.png` = lifted corner + exactly one red dot ✔. `refs/castplate.png` = two hairs on all three views ✔. `refs/shelf.png`, `layout-plate.png` ✔. Every failing motif above had a correct master on disk. This is a batch/reference failure, not a plate failure. |
| **`stair-gap.png` does not double as `b06`** | `magick compare -metric AE` = 2,028,310 px differing (97.8%). Board §7 counts them as one image for budget. They are two. |
| **`castplate.png` and `layout-plate.png` are 1344×768**, not 1920×1080 | The two most-used anchors are a different aspect (1.750 vs 1.778) from the frames they condition. |
| **The `b11`↔`b81` DRIFT inverse pair is dead** | `b11` shows the walker at the left third **facing and walking LEFT**, with the ground line running to the right **behind** them. The board requires left-to-right with the line drawn **ahead**. `b81` is correct (right third, walking left). Both now walk the same way: the inverse pair is not inverse, and the Act 1 → Act 6 callback does not read. |
| **3 of the 4 board-declared plant/payoff callbacks are broken** | stair (`b06 b07 b08` → `b83 b85 b87`): `b85` is eight treads. sheet-from-above (`b03` → `b82`): `b82` adds a red paperclip and does not match `b03`'s camera or hand. ground line (`b11` → `b81`): direction inverted. Only the footnote pair survives on one side — `b53` is correct, `b72` is absent. |

---

## Verified correct — recorded so re-checks are cheap

Measured by connected-component analysis of tread fills, not by eye:

- **`b06`** — 6 sage treads at 230×69 on a 141/−74 pitch, position 4 (1046,611) **absent**. Gap correct. PASS.
- **`b07`** — tread grid byte-identical to `b06`, gap at 4. Geometry PASS (composition fails, below).
- **`b08`** — 6 sage + red at (894,611) = **7 treads, red fourth**. Geometry PASS.
- **`b83`** — 6 sage + red at (1046,611), grid **identical to `b06`/`b07`**. **7 treads, red fourth, gap position matched exactly.** The best-executed frame in the film.
- **`b85`** — 7 sage + red at (752,565) on a ~190px pitch = **EIGHT treads**, three below the red and **four above**, flight running off both frame edges. FAIL.
- **`b87` — Isaac's revised judgment is CORRECT.** One tomato-red tread lying flat on the ground line (273×104 at 568,783), protagonist crouched beside it, hand resting on it. Matches the board. (It still carries the margin rule and one hair.)
- **`b53`** and **`b54`** — the footnote plant and its echo, both correct, exactly one dot each.
- Frames passing clean: `b01 b02 b05 b06 b10 b12 b13 b26 b28 b31 b35 b36 b39 b42 b44 b47 b53 b54 b58 b61 b67 b71 b73 b77 b81 b83 b84 b88`.

---

## Returns

### R1 — Art Director · PLAYBOOK 10.7 / 2.3 · **b17**
The hinged slab machine is drawn as a rendered console containing a scene, a red
LED, coloured cabling and a **green display bearing glyph characters**. Board §1
prohibition 1: *"a plain hinged slab with a blank pale panel and a key deck, no
marks on it… no screen image."*
**Fixed looks like:** `b17` regenerated with a blank pale panel, flat fills, no
screen content, no second accent colour. Re-check = re-read the crop at 2.5×.

### R2 — Art Director · PLAYBOOK 10.9 / 10.11 · the STATION motif
`refs/station.png` and `refs/three-desks.png` are correct and were not used as
reference #1 as board §7 requires. Retake with the plate anchored:
`b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b32`.
**Fixed looks like:** every G2 frame carries the soft pale disc-studded cap and
the cord exiting frame on the same side; `b21` is three *stations*, not three
standing figures; `b15`'s arcade cabinet and `b23`'s red cube are gone.

### R3 — Art Director · board §2 Motif 1 · **b85**
Eight treads. The motif is exactly seven, fourth red, three below and three above.
`b85` is also boarded as a **close on three treads**; it shows the whole flight.
**Fixed looks like:** three treads in frame, the red one centre, hand touching it,
tread pitch matching `b83`. Re-check = the CC tread count, which must be 3.

### R4 — Art Director · board §1 prohibition 2 · **b45 b46 b50**
Nicholas Carr's face is visible. `b45` is the G4 anchor, so the whole group
inherits it. `b46` is a LIVE beat.
**Fixed looks like:** figure from behind and slightly to one side, face not
visible in any frame; window frame at a fixed left-edge position across
`b45`–`b50`; `b48` and `b49` regain the window.

### R5 — Art Director · WORLD.md §2 · the margin rule
`b04 b18 b22 b30 b50 b82 b87` carry a full-height red vertical rule. WORLD.md
forbids it explicitly and by test.
**Fixed looks like:** zero hits from the R−G thin-tall-component scan across all 88.

### R6 — Art Director · PLAYBOOK 10.20 / 2.4 · **b18 b51 b87**
Hair count: `b18` zero, `b51` one, `b87` one. `castplate.png` is correct.
**Fixed looks like:** exactly two hairs, counted, in every frame containing the
protagonist's uncovered crown.

### R7 — Art Director · PLAYBOOK 10.8 / 2.6 · donated and substituted props
`b23` red cube · `b82` red paperclip · `b60` red bricks · books-for-sheaf in
`b27 b29 b42 b60 b63 b80`.
**Fixed looks like:** `refs/sheaf.png` anchored as reference #1 on every sheaf
beat; the interviewer's hand empty in `b23`; `b82` identical to `b03`.

### R8 — Art Director · the ten "No figure" frames
Board specifies no person; a person is drawn: `b43 b51 b52 b55 b57 b60 b64 b69
b72 b79`. `b69` ("Nobody came to the funeral") is the inverse of its board — the
plinth is absent and a figure is present. `b79` renders three objects as three
people. `b55` renders two stacks as two people.
**Fixed looks like:** each of the ten regenerated from a repaired prompt (see R11)
with no figure in frame.

### R9 — Art Director · extra / wrong figures where the board names one
`b25` (two, board says alone) · `b27` (two) · `b33` (a giant foreground figure
inside establishing wide 2 of 3, breaking G3's "figures the same size in all
three") · `b37` (two crouching adults) · `b38` (four figures, no handshake; board
requires five and a handshake) · `b59` (protagonists where the board says plain
adult figures).

### R10 — Art Director · beats whose punchline is inverted
- `b56` — the block is held in both hands. The beat is *empty hands, and the thing
  still carried*.
- `b41` — the single large red block became two small cubes; the carried-claim
  object breaks between `b40` and `b41`.
- `b62` — the figure sits on the ground, not the stool from `b61`, and is not
  reaching; the measured *delay* is the beat.
- `b75` — the second box under the arm is missing; *hands free, and immediately
  full again* does not read.
- `b78` — the shelf board has vanished; two boxes float.
- `b34` / `b66` — both carry a proportion and neither is legible: `b34`'s two
  blocks show the same ratio, `b66` shows eight plinths all occupied where the
  board asks for a long row running off both edges, most occupied, some bare.

### R11 — **Director / tooling owner** · `tools/video/build-prompts.py`
The `DEAD_CLAUSE` regex deletes the clause containing a frame reference **and the
sentence subject with it**. 19 of 88 current prompts are damaged; at least 8 lost
the frame's subject entirely. Production codes (`G3b.`) and QA prose ("Hold risk:
below the 1.8s floor — see §8") leak into image prompts.
**Fixed looks like:** `python3 -c` scan over `prompts.json` returns zero records
that begin lowercase, zero containing `G\d+b?\b`, zero containing `anchor[.,]`,
zero containing `§`, and every record's scene text is a complete sentence.
**And:** the prompt file is archived alongside the batch before generation, so a
future Gate 2 can audit a frame against the text that made it.

### R12 — Art Director / Cinematographer · the LIVE stills
Do not commission clips. `b72` must be regenerated as the exact `b53` composition
with a bare bottom edge; `b08` must match `b07`'s framing with the figure's hands
at their sides and the stair at `b07`'s tread grid (origin 623,833); `b46` must
hide the face; `b14` must carry the electrode cap. Re-check `b08` and `b72`
against `b07` and `b53` by CC coordinates, not by eye.

### R13 — Storyboard · two small corrections to the board's own record
- §7 counts `stair-gap.png` and `b06` as one image; they differ by 97.8% of pixels.
- `b11`'s scene text and the delivered frame disagree on walk direction. Confirm
  the board is right and the frame is wrong (it is), and note that the inverse
  pair needs both frames re-checked together, not separately.

---

## Retake list — 63 frames

```
b03 b04 b07 b08 b09 b11 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b25
b27 b29 b30 b32 b33 b34 b37 b38 b40 b41 b43 b45 b46 b48 b49 b50 b51 b52
b55 b56 b57 b59 b60 b62 b63 b64 b65 b66 b68 b69 b70 b72 b74 b75 b76 b78
b79 b80 b82 b85 b86 b87
```
plus `b39`-adjacent check on `b38`, and `b47`/`b53`/`b54` held as the G4/G6
reference points they now are.

**Gate 2 does not reopen until every item above is re-run, not just the retaken
frames — a sampled check that failed once has made the sample the population.**
