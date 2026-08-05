# QC — GATE 2 (the frames) · cognitive-debt · RE-RUN 2

**Filed 2026-08-04 · QC chair · run before any motion or assembly is paid for.**
Artifacts audited: 88 frames in `public/images/frames/`, `production/prompts.json`,
`production/prompt-archive/prompts-20260804-162359.json`, 4 contact sheets in
`production/qc/`, `STORYBOARD.md`, `WORLD.md`.

This supersedes the first Gate 2 report of the same date. A short record of what
run 1 failed, and whether it is now fixed, is in **§A** below — nothing from run 1
is dropped.

---

## VERDICT — **FAIL**

**Do not commission motion. Do not assemble.** The five LIVE stills cost ~$1.96 to
animate; **two of the five cannot be animated as boarded at all**, and one of those
two (`b72`) is the identical failure filed in run 1 and not touched since.

**Blocking items, worst first:**

1. **`b08` — the LIVE thesis beat is unanimatable.** The stair in `b08` is not the
   film's stair. It is a generated outline staircase with **risers, ~8 steps, no
   tread fills, no gap and no red tread**. The boarded motion is *"the tomato-red
   tread lowers into the gap and settles."* There is no gap and no red tread.
   Measured: `b06`/`b07`/`b83` all share a byte-identical tread grid (six sage
   treads at 229×68 px on a 141/−74 pitch); **`b08` contains zero 229×68 tread
   blobs.** The figure's arms are also raised, where the board says "hands lowered
   to the figure's sides."
2. **`b72` — the LIVE landing beat does not contain its composition.** Board: *the
   identical `b53` framing, sheet lifted at the bottom corner, bare bottom edge,
   a hand arrives and sets the dot down.* Delivered: **two figures standing on the
   ground line. No sheet, no corner, no hand, no dot.** Identical to run 1. The
   film's best visual rhyme (`b53`→`b72`) is dead on one side.
3. **`b33` has black bars painted into the image.** Confirmed and measured: pure
   black (max channel < 10) rows `0–109` and `971–1079`. The painted panel is
   **1920×861 (2.23:1)** inside a 1920×1080 file. PLAYBOOK 10.7.
4. **`b04` contains an emoji.** A **red heart glyph** is drawn on the fingertip.
   Rubric item 7 forbids emoji outright; the board forbids marks on every object.
5. **The forbidden red margin rule survives in `b13`, `b21`, `b87`** — full-height
   (vcov = 1.00), 8–14 px, measurably redder than the paper baseline. `b13` is the
   **G2 anchor** and `b21` is the three-desks plate frame. WORLD.md §2 forbids it
   by name and by test.
6. **Motif 3 (THE DOCUMENTS) is still substituted.** `sheaf.png` is *"a thick loose
   stack of blank pale sheets, no binding, no clip, no writing of any kind."*
   Delivered as **bound books with solid red label-blocks on the spines and covers**
   in `b27` `b29` `b55` `b60` `b67`. Run-1 R7, unfixed.
7. **Ten frames the board specifies as figure-free contain a figure**, including
   **`b69` ("Nobody came to the funeral")** — board: *"No figures. No crowd. Nothing
   else in the frame at all."* Delivered: a figure. Run-1 R8, unfixed.
8. **Motif 5 (THE SHELF) does not exist in half of G5.** `b76` and `b78` contain no
   shelf board at all; `b78`'s boxes float in mid-air. `b75`'s shelf is **tomato-red**;
   `b77`'s is pale with **brown** boxes. Run-1 R10, unfixed.
9. **A second chromatic accent — warm brown/tan — is in the film.** `b31`'s desk
   field is 10.75 % of frame at hue 30–45 (the red is 8.18 %); also `b02` `b05`
   `b70` `b74` `b77`. WORLD.md: *"no warm or brown tint anywhere."*

**Genuinely fixed since run 1:** the world colour lock, the station cap, `b17`'s
lettering, `b23`'s invented cube, `b85`'s tread count, Carr's face, the `b11`↔`b81`
inverse pair, the two-hair count, and the prompt archive. Detail in §A.

**~50 of 88 frames require retake.** List in Returns.

---

## Item table

| # | Check | Evidence | Verdict |
|---|---|---|---|
| **2.1** | Frame count vs prompts.json | `ls public/images/frames \| wc -l` = **88**. `len(json.load(prompts.json))` = **88**, keys `b01`–`b88`. Archive `prompts-20260804-162359.json` is **byte-identical** to the live file (`p == a` → `True`), so every frame can now be audited against the text that made it. Run-1 finding closed. | **PASS** |
| **2.2** | 1920×1080, no inset painted panel | `magick identify` on all 88: every file `1920x1080`. Fuzz-0 trim = `1920x1080+0+0` on all 88. Edge-strip luminance scan on all 88 (24 px, four edges): 87 frames sit at 0.89–0.95 mean. **`b33` = 0.000 top and bottom.** Row analysis: pure-black bands `y0–109` and `y971–1079`; painted panel **1920×861**, aspect 2.23:1. Letterboxing painted into the pixels. | **FAIL — b33** |
| **2.3** | No lettering, numbers, hex-code artifacts | All four contact sheets read end to end, then 14 zoomed crops at 1.5–2.5×. **No lettering, no numerals, no glyph strings, no `D9EE13D`-class artifact anywhere in the 88.** The run-1 `b17` screen glyphs are gone — verified at 2.5× (`b17` panel is blank pale, no screen content, no LED). **But painted non-type marks are present and are board prohibition 1:** `b04` red **heart glyph** on a fingertip; `b39` red dot on the back of the hand; `b15` solid red square **on the machine's pale panel**; `b27` `b29` `b67` red label-blocks on book spines; `b64` a red pen on the plinth; `b80` a red tab on the machine lid. | **FAIL — b04 (emoji), b15, b27, b29, b39, b64, b67, b80** |
| **2.4** | Character holds: head shape, EXACTLY two hairs, jacket | Two automated counters disagreed with each other and with the sheet, so a **third pass** was run per the hard rule: 26 crowns cropped by head-bbox and read at 420 px. **Two hairs on every one** — `b01 b02 b05 b07 b08 b11 b12 b25 b26 b27 b35 b37 b45 b50 b51 b56 b57 b58 b62 b69 b73 b81 b84 b86 b87 b88`. Head shape and red hooded jacket hold across all 88. Run-1's `b18`/`b51`/`b87` hair failures are **resolved**. **Two defects remain:** (a) `b46` (LIVE) shows a **bare crown, zero hairs**, where its own anchor `b45` has two — inside a group whose board text says "identical framing to `b45`"; (b) the protagonist's cream hand is drawn as a **solid tomato-red hand** in `b82`, breaking the character's own palette in the frame that must match `b03`. | **FAIL — b46, b82** |
| **2.5** | One accent per frame; world matches WORLD.md | **Paper lock PASSES decisively.** Modal background across 87 frames (excl. `b33`): rgb(228–231, 230–233, 218–221), hue 64.6–70.0, sat 5.2–5.6, val 90.2–91.4. **Zero warm/brown drift in the ground, zero cream-world collision with the last three films.** Ruled lines horizontal throughout. **Two failures:** (a) **the forbidden vertical margin rule is in `b13` `b21` `b87`** — differential paper-redness scan, columns x124–137 / x210–217 / x240–252, dev +12.5/+13.0, **vertical coverage 1.00**, confirmed visually on a 3-up left-strip crop; (b) **a second chromatic accent, warm brown/tan (hue 30–45)**, at 10.75 % of frame in `b31` (exceeding the red at 8.18 %), 1.61 % in `b77`, plus `b02` (2.09 % h15–30), `b05` (3.40 %), `b70`, `b74`. | **FAIL — b13, b21, b87 (margin rule); b02, b05, b31, b70, b74, b77 (brown)** |
| **2.6** | No donated / invented / substituted props | Sheets cross-read against STORYBOARD.md §2/§5. **Motif substitution:** `sheaf.png` (blank loose sheets) drawn as **bound books with red spine labels** in `b27 b29 b55 b60 b67`. **Motif absence:** the shelf board of `shelf.png` is **missing entirely** from `b76` and `b78`. **Motif colour drift:** `single-sheet.png` is pale in `b44`–`b49` and **tomato-red** in `b43` and `b50`; the hinged slab machine is pale in `b02 b13`–`b17 b79`, **red** in `b63`, **dark grey** in `b80`. **Invented props:** `b64` a red **pen**; `b30` a large red block under the fanned stack; `b39` a red dot on a hand; `b04` a heart. **Object substitution:** `b41` carries a small red **cup** where `b40` set down a large red **block** — the carried-claim object breaks between two adjacent frames. | **FAIL** |
| **2.7** | Animated frames carry no data; RMSE drifts looked at | `find . -name "*.mp4"` returns nothing. No animate-frames log exists. Nothing to read. | **NOT RUN — no artifact yet** |
| **2.8** | Every clip corresponds to a `LIVE` beat | `renders/` empty, zero `.mp4` in the tree. No unrequested clip can exist. Board marks exactly 5 `LIVE`. | **PASS (vacuous — no clips)** |
| **2.9** | 4–6 `LIVE`, non-adjacent, classed, "what moves" line, no data | **The board's plan passes, again.** 5 LIVE: `b08 b14 b46 b72 b88`; gaps 6/32/26/16, none adjacent; classes 1·3·5·1·2, all in the five-class set; each carries an explicit "what moves, and why" line; six data-carrying beats explicitly refused. **The stills fail 3 of 5.** `b08` — no gap, no red tread, wrong stair object, wrong pose: **nothing to animate**. `b72` — the boarded composition is absent: **nothing to animate**. `b46` — animatable in isolation, but it is not "identical framing to `b45`": different window (2-pane sash vs 4-pane cross), different position, **black office chair vs pale wooden chair**, and a bare crown against `b45`'s two hairs. The cut into it will jump and the motion will advertise the jump. **`b14` PASSES** (cap present, hourglass present with a sand column that can fall, cord correct). **`b88` PASSES** (small figure, facing away, wide ruled field, ground line y=903 matching `b86`/`b83`/`b01`, two hairs clearly present to lift). | **FAIL — b08, b72 unanimatable; b46 breaks its group** |
| **2.10** | Each clip: one motion, starts after the cut, settles, 30fps | No clips exist. | **NOT RUN — no artifact yet** |

### Board fidelity — graded separately because it is where the film is losing

| Finding | Evidence |
|---|---|
| **Ten "no figure" frames contain a figure** | Board says no person; a person is drawn: `b42`✔(clean) but **`b51` `b52` `b55` `b57` `b60` `b64` `b69` `b72` `b79`** and `b43`-adjacent. **`b69`** — *"Nobody came to the funeral" / "No figures. No crowd. Nothing else in the frame at all."* — has a figure. **`b79`** — board asks for *three objects in a row, no figure*; delivered is **three protagonists**. **`b52`** — board asks for *three objects, no figure*; delivered is **two figures and no objects**. |
| **`b51` contains a solid black humanoid silhouette** | Board: *"Both on the ruled ground, side by side... The folded sheet flat and settled; the thick stack squarely upright beside it. **No figure.**"* Delivered: the protagonist at left and a **tall solid-black featureless figure** at right. Neither boarded object is present. The black figure appears nowhere else in the film's design and reads as a different world. |
| **G4 (Carr) has no invariants left** | Board invariants: face never visible ✔ (**resolved**); *chair feet on the same ruled line*; *the window frame's left edge at the same frame position*; *the folded sheet the same size in every frame*. Delivered: `b45` 4-pane window far left + pale chair; `b46` 2-pane sash centre-left + **black chair**; `b47` **no window**, two pale chairs; `b48` no window; `b49` a **large 4-pane window centred**, and the third figure holds a sheet where the board requires the slab machine; `b50` **no chair, no window**, figure standing, sheet **red**. |
| **G3 (the field count) is three unrelated cameras** | Board: *identical camera height and horizon rule; figures the same size in all three.* `b31` is a deep perspective recession with figures at a dozen scales and a horizon at y=150; `b33` is a flat centred row at y≈530 inside black bars; `b34` is two flat blocks of unequal size (≈12 vs ≈9), so the "one in six / a scatter" comparison the board calls *the argument* is not legible. |
| **G3b (the plinths) is four different objects** | `b64` a cream **box**; `b65` a classical **column**; `b66` a row of grey **bars of unequal height**; `b67` white **boxes**; `b68`/`b69` a low grey **slab**. `b66` additionally reads as a bar chart of varying heights — the exact PLAYBOOK 10.17b failure the board wrote a paragraph to prevent. |
| **`b03` → `b82` callback is broken** | Both fail the boarded camera (*"close from directly above"*); both read as a hand raised beside a standing sheet. And they do not match each other: `b03` a **cream hand with a red cuff**, sheet bottom on the ground line; `b82` a **solid red hand, no wrist, no cuff**, smaller, lower, sheet larger and crossing the line. Board: *"same camera height, same hand position, same sheet size."* |
| **`b23` → `b24` "identical framing" is broken** | `b23` — two figures seated on the bare ground, no furniture. `b24` — the same two at a **table on stools**. The punchline (*the hand stays open, and stays empty*) needs the two frames to be the same shot. |
| **`b85`: right count, unreadable picture** | Tread count **fixed** — 3 treads, middle red, hand touching (measured: sage 512×192 at x704, RED 512×192 at x1094, sage 435×192 at x1484). **But** the arm entering frame is a solid tomato-red sleeve of **141,852 px — 43 % larger than the red tread's 99,009 px**, in the identical accent colour, immediately adjacent. The tread reads as a continuation of the sleeve. The one thing this frame exists to show — *a different colour from everything it belongs to* — is destroyed. Tread aspect 2.7:1 vs `b83`'s 3.4:1, so "same tread geometry as `b83`" also fails. |
| **`b01` is not the establishing wide it is boarded as** | Board: *"A very small figure... far to the left, seen from behind and slightly above... the room is enormous."* Delivered: a medium-scale figure near centre-left, seen from the side, at a table. Chair limit is three wides; the film's cold-open frame is not one of them. |
| **The protagonist is mass-replicated** | `b31` renders roughly ninety copies of the spine character; `b38` `b59` `b71` `b79` render "plain adult figures" as the protagonist; `b45`–`b50` render **Nicholas Carr** as the protagonist, two hairs and red hood included. WORLD.md: *"The character is spine; supporting cast varies per film and is governed per frame."* Governance is absent. |

---

## §A — What run 1 failed, and where it stands now

| Run-1 return | Status |
|---|---|
| **R1** `b17` green segmented display with glyph characters | **FIXED.** Verified at 2.5×: blank pale panel, no screen content, no LED, no second accent. |
| **R2** STATION motif absent from 10 of 11 frames | **FIXED.** The disc-studded pale cap and the single cord are present in `b13 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b32`. |
| **R3** `b85` EIGHT treads | **FIXED** on the count (3 treads, red centre, measured). **NEW FAIL:** the red sleeve now swamps the red tread — see the board-fidelity table. |
| **R4** Carr's face visible in `b45` `b46` `b50` | **FIXED.** Face not visible in any of the three (verified at zoom). |
| **R5** red vertical margin rule in 7 frames | **PARTLY FIXED.** 7 → **3**: `b13` `b21` `b87`. Still a WORLD.md violation and still blocking. |
| **R6** hair count `b18` `b51` `b87` | **FIXED.** Two hairs on all 26 crowns read at 420 px. |
| **R7** donated/substituted props | **PARTLY FIXED.** `b23`'s red cube **gone**; `b82`'s paperclip **gone**; `b60`'s red bricks **gone**. **Books-for-sheaf persists** in `b27 b29 b55 b60 b67`, now with red spine labels added. |
| **R8** ten "No figure" frames contain a figure | **NOT FIXED.** `b51 b52 b55 b57 b60 b64 b69 b72 b79` still carry a figure. `b69` and `b79` are unchanged in kind. |
| **R9** extra / wrong figures where the board names one | **PARTLY FIXED.** `b25` and `b37` now read; `b36` now has **three** figures where the board says two; `b38` renders protagonists as "plain adult figures". |
| **R10** inverted punchlines | **NOT FIXED.** `b41` (cup, not the block), `b62` (on the ground, not the stool), `b75`/`b76`/`b78` (shelf red / absent / absent), `b66` (unequal-height bar chart). `b56` and `b34` improved but `b34` is still illegible. |
| **R11** `DEAD_CLAUSE` regex damage in `prompts.json` | **FIXED at the tooling level and archived.** `prompts.json` and the archive are byte-identical; frames are now auditable against their prompts. |
| **R12** the LIVE stills | **NOT FIXED.** `b14` and `b88` are good. `b08` and `b72` are still unanimatable; `b46` is animatable but breaks G4. |
| **R13** `b11`↔`b81` inverse pair dead | **FIXED, cleanly.** `b11` walks left→right at the left third, line drawn ahead to the right edge, nothing behind. `b81` walks right→left at the right third, line ahead to the left edge, nothing behind. Ground line y=908 vs y=901 — 7 px apart. The Act 1 → Act 6 callback reads. |
| **Prompt archive missing** | **FIXED.** `production/prompt-archive/prompts-20260804-162359.json`. |
| **`b33` black bars** | Newly confirmed and measured this run — see 2.2. |

---

## Verified correct — recorded so the re-check is cheap

- **The world clause held.** 87 of 88 frames sit inside rgb(228–231, 230–233,
  218–221) / hue 64.6–70.0 / sat 5.2–5.6. This is the single best-executed thing
  in the film and no retake should be allowed to move it.
- **The stair grid is deterministic and exact.** `b06`, `b07`, `b83` share a
  byte-identical tread grid: six sage treads at 229×68 on a 141/−74 pitch, gap at
  position 4. `b83` places the red tread at x[1046–1275] y[611–679] — **precisely
  the vacancy in `b06`/`b07`**. `b83` is the best frame in the film.
- **`b53`** — the footnote plate: lifted corner, exactly one red dot, correct scale.
- **`b14`, `b88`** — LIVE stills, safe to animate as boarded.
- **`b11` / `b81`** — the inverse pair, correct in both directions.
- Frames passing clean on every check run: `b06 b07 b09 b10 b12 b14 b19 b20 b22
  b25 b26 b28 b32 b35 b40 b42 b44 b47 b53 b54 b56 b58 b61 b65 b71 b73 b81 b83
  b84 b86 b88`.

---

## Returns

### R1 — Art Director · PLAYBOOK 10.7 · **`b33`**
Black bars painted into the pixels: rows 0–109 and 971–1079, painted panel
1920×861 (2.23:1). **Fixed looks like:** the edge-strip scan returns mean > 0.8 on
all four edges of `b33`, and the ruled ground runs to all four frame edges.
Re-check is one command.

### R2 — Art Director · rubric item 7 / board §1 prohibition 1 · **`b04`**
A **red heart glyph** on the fingertip. Emoji are forbidden outright, and the board
forbids marks on every object. Also `b04` is not the boarded overhead of three
identical sheets with a hand flat beside them. **Fixed looks like:** the boarded
overhead, three identical blank pale sheets, cream hand, no mark of any kind on
skin or paper.

### R3 — Art Director · WORLD.md §2 · **`b13` `b21` `b87`**
Full-height red vertical margin rule. `b13` is the G2 anchor; `b21` is the
three-desks plate frame. **Fixed looks like:** the differential paper-redness scan
returns **zero** thin columns with vertical coverage > 0.75 across all 88.

### R4 — Cinematographer / Art Director · board §4 L1 · **`b08`** — DO NOT BUY THIS CLIP
`b08` must be `b07`'s exact frame — same tread grid (six sage treads at 229×68,
origin x623 y833, pitch 141/−74), gap at position 4, ruled ground at y=903 — with
the figure's hands **at their sides**. It currently contains a different object: an
outlined staircase with risers and no fills. **Fixed looks like:** `magick compare`
of `b07` and `b08` shows difference only in the figure's arms; a connected-component
tread count on `b08` returns six 229×68 sage blobs with the position-4 vacancy at
x[1046–1275] y[611–679]. Verify by coordinates, not by eye.

### R5 — Cinematographer / Art Director · board §4 L4 · **`b72`** — DO NOT BUY THIS CLIP
The boarded composition is absent for the second run running. `b72` must be `b53`'s
frame with a bare bottom edge. **Fixed looks like:** `b72` and `b53` agree on the
sheet bbox and the lifted-corner angle to within a few pixels, and `b72` contains
**zero** red blobs on the sheet's bottom edge.

### R6 — Art Director · PLAYBOOK 10.9 / board §5 G4 · **`b45`–`b50`**
Face is fixed; nothing else in the group is. Window present in 3 of 6 frames, in
three different shapes and three different positions; chair pale / black / absent;
the folded sheet pale in four frames and **tomato-red** in `b43` and `b50`.
**Fixed looks like:** `b45` re-approved as the anchor, then `b46`–`b50` generated
from it with the window's left edge at a fixed x, the chair identical, and the
folded sheet the same pale object at the same size in all five.

### R7 — Art Director · PLAYBOOK 10.8 / board §2 Motif 3 · the DOCUMENTS
Books-for-sheaf in `b27 b29 b55 b60 b67`, now carrying **red label-blocks** on the
spines. **Fixed looks like:** `refs/sheaf.png` anchored as reference #1 on every
sheaf beat; loose blank pale sheets, no binding, no spine, no label, no red.

### R8 — Art Director · board §2 Motif 5 · **`b75` `b76` `b77` `b78`**
`b76` and `b78` have **no shelf board**; `b78`'s boxes float. `b75`'s shelf is red,
`b77`'s is pale with brown boxes. **Fixed looks like:** `refs/shelf.png` anchored
as reference #1; one pale bracketed board at a fixed height in all four; boxes the
same pale object at the same size; the only red in the frame is the jacket.

### R9 — Art Director · board §5 / the "no figure" ruling · **`b51` `b52` `b55` `b57` `b60` `b64` `b69` `b79`**
Each of these frames is boarded with objects and no person, and each contains a
person. `b69` is the film's coldest line and its board says "nothing else in the
frame at all". `b79` and `b52` render objects as people. `b51` additionally invents
a **solid black humanoid silhouette** that exists nowhere else in the film.
**Fixed looks like:** eight frames regenerated from their archived prompts with the
figure deleted, and the boarded objects present and countable.

### R10 — Art Director · WORLD.md the locked clause · **`b31` `b02` `b05` `b70` `b74` `b77`**
Warm brown/tan as a second chromatic accent — 10.75 % of `b31` at hue 30–45, more
of the frame than the red. **Fixed looks like:** the hue census returns no bucket
above 0.30 % outside hue 0–15 on any of the 88.

### R11 — Art Director · board §3 G3 / G3b · **`b31` `b33` `b34`** and **`b64` `b66` `b67` `b68` `b69`**
Neither group has a shared camera or a shared object. `b66` reads as a bar chart of
unequal heights, which the board wrote a paragraph forbidding. **Fixed looks like:**
one approved anchor per group, then every member generated from it; identical
horizon y, identical figure size, identical plinth height and silhouette; `b34`'s
two blocks the same size so the proportion is the only difference between them.

### R12 — Art Director · board §9 the four callbacks · **`b03`/`b82`** and **`b85`**
`b82` uses a solid red hand where `b03` uses a cream hand with a red cuff, at a
different size and position; neither is the boarded overhead. `b85`'s red sleeve is
43 % larger than the red tread it sits against, in the same colour, so the motif is
illegible in its payoff. **Fixed looks like:** `b03` and `b82` differ in nothing a
pixel diff can find outside the sheet's contents; `b85` shows a cream hand and a
minimal sleeve, red confined to the single tread, tread aspect matching `b83`.

### R13 — Art Director · board §1 prohibition 1 · **`b15` `b39` `b64` `b80`**
Marks painted on objects: a red square on the machine's pale panel (`b15`), a red
dot on a hand (`b39`), a red pen (`b64`), a red tab on the machine lid (`b80`).
**Fixed looks like:** every object in these four frames blank, and the only red in
frame is the boarded accent.

### R14 — Art Director · PLAYBOOK 10.20 / WORLD.md cast governance
The protagonist is replicated ~90× in `b31`, stands in for "plain adult figures" in
`b38` `b59` `b71` `b79`, and **is Nicholas Carr** in `b45`–`b50`. **Fixed looks
like:** supporting cast described at point of use as a distinct figure — no red
hood, no two hairs — in every frame the board does not name the protagonist.

### R15 — Art Director · board §5 · inverted or broken punchlines
`b41` (red cup, not the block from `b40`) · `b62` (on the ground, not the stool from
`b61`) · `b36` (three figures, board says two) · `b23`/`b24` (not the same shot) ·
`b01` (not a wide, not from behind and above).

### R16 — Storyboard · one correction to the board's own record
`b09` is boarded as *"a plain parked car"* in a world of flat fills and even
outlines. The delivered car is the most rendered object in the film — grille,
mirrors, wheel arches, window shading. Either the board specifies the car in this
world's vocabulary, or the beat takes a simpler object. Recorded so it is decided
rather than regenerated three times.

---

## Retake list — 50 frames

```
b01 b02 b03 b04 b05 b08 b13 b15 b21 b23 b24 b27 b29 b30 b31 b33 b34 b36
b38 b39 b41 b43 b45 b46 b48 b49 b50 b51 b52 b55 b57 b59 b60 b62 b63 b64
b66 b67 b68 b69 b70 b72 b74 b75 b76 b77 b78 b79 b80 b82 b85 b87
```

**Hold as approved reference points, do not regenerate:** `b06` `b07` `b83`
(the stair grid — `b08` must be built to match these, not the reverse),
`b53` (the footnote — `b72` must be built to match it), `b11` and `b81`
(the inverse pair), `b14` and `b88` (the two sound LIVE stills), `b86`
(the G7 anchor).

**Gate 2 does not reopen on the retaken frames alone.** Every item in the table
above is re-run against all 88 — the margin-rule scan failed once at three frames
after failing at seven, and a check that has failed twice does not get sampled a
third time.

---

*Item 3.4, the listen gate, belongs to Gate 3 and to a human ear. It is not
addressed here and must never be marked done by an agent.*
