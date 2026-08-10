# SHOT BOOK — The Price of a Glance

> **MOTION RESHOOT RE-SPEC — filed 2026-07-23 by the Cinematographer.** The
> first two clip batches (below, preserved as the audit trail) shipped 25 KEEP
> clips that Isaac judged **dull and static — camera motion too weak, editing
> not matching the story.** The new standard is anime / motion-design studio
> craft. This section re-specs the camera motion for **every** shot around one
> technique: **an explicit, motivated CAMERA move over a held subject** — the
> lens moves, the scene does not. That is both the craft upgrade and the
> consistency guarantee, because moving the lens (not the content) is what
> stops the elaboration defects — multiplied objects, invented figures, faces,
> devices resolving — that wrecked the seedance batch.
>
> **Nothing is generated in this dispatch. Quote and stop.** Every price below
> was fetched live from `POST /v1/videos/estimate` on 2026-07-23 against each
> shot's real `sourceUrl` as `imageUrl`, at the chosen model and duration; all
> 27 reshot lines returned a non-null `usd` and a live quote token.

| | |
|---|---|
| Upstream | `FRAME-BOOK.md` (Art Director, 30/30 FINAL) · `SOUND-BOOK.md` (measured) · `TREATMENT.md` |
| Engine | fal proxy `:5412`, `ok true`, `hasKey true`, engine cap $50, **film ceiling $30 (Isaac)**, spent today $12.63 |
| Clip spec | image-to-video, `16:9`; kling default 5s, 10s on the three movement shots; the Editor holds/ramps to slot |
| Models live | **kling-pro $0.07/s** (workhorse) · veo-3-fast $0.40/s **(clamps to 8s = $3.20/clip)** · seedance-lite $0.04/s **(RETIRED — caused the defects)** · luma-ray $0.10/s (no image) |
| Reshoot quote | **$10.50** (27 shots on kling; reuse 18/22/24 at $0). Fits the ~$17.37 remaining with $6.87 retake headroom |
| Spent this dispatch | **$0.00** — nothing submitted |

---

## Model choices — the reshoot split, and why

**seedance-lite is retired for this film.** Every elaboration defect across two
batches — multiplied peaks, invented figures and feet, a smear ballooning into
splatter, a slab resolving into a lit device, treads recolouring, a book
flipping open — landed on seedance. It cannot hold structure under a move. It
does not appear anywhere below.

**kling-pro is the workhorse — every reshot shot.** At $0.07/s it holds
structure far better and takes camera-motion prompts cleanly, which is the
whole technique: prompt an explicit lens move and lock the content, and the
model moves the camera rather than inventing scene motion. This is the direct
fix for the five shots that never passed (6, 15, 17, 23, 30) as much as it is
the craft upgrade for the 22 that passed-but-dull.

**Reuse the three clean kling heroes at $0 — 18, 22, 24.** These are the only
shots in the film with genuinely complex, motivated motion (the reach that
stops, the fluid bloom, the vertigo pull-back), they passed clean, and they are
by definition the *least* dull shots in the picture. Reshooting them spends
money to risk a clean take for no gain. Their existing clips carry forward
unchanged.

**veo-3-fast is NOT recommended, and the live price is why the brief's math
moves.** veo clamps a 5s request up to 8s and bills $3.20/clip (confirmed live),
not the $2.00/5s the brief assumed. More important: veo's strength is rich,
physically-plausible motion — which is exactly what this film does **not** want
on its problem shots. The repeat failures (23's ring, 17's slab, 30's book) are
*stillness* failures where the fix is holding content still; a photoreal-motion
model is the wrong instrument and, on 23, an 8s clip only gives a figure more
time to move. The film's genuine complex motions (18/22/24) already passed on
kling and are reused. So veo rescues nothing here. One honest veo option is
offered — a bigger showpiece pull-back on 24 — as a splurge, not a need.

| # | Model | Dur | Price | Note |
|---|---|---:|---:|---|
| 1 | kling-pro | 10s | $0.70 | opening push; 9.00s slot wants sustained native motion, not a ramped 5s |
| 2 | kling-pro | 5s | $0.35 | |
| 3 | kling-pro | 5s | $0.35 | near-still |
| 4 | kling-pro | 5s | $0.35 | |
| 5 | kling-pro | 5s | $0.35 | reshoot for a real lateral track (old clip was a weak drift) |
| 6 | kling-pro | 5s | $0.35 | **never passed** — camera-reveal over a frozen printed graph |
| 7 | kling-pro | 5s | $0.35 | |
| 8 | kling-pro | 5s | $0.35 | |
| 9 | kling-pro | 5s | $0.35 | |
| 10 | kling-pro | 5s | $0.35 | vertical descent |
| 11 | kling-pro | 5s | $0.35 | locked-off spine (matches 28) |
| 12 | kling-pro | 10s | $0.70 | vertical descent, "no bottom" — the film's longest move; native 10s, not ramped |
| 13 | kling-pro | 10s | $0.70 | endless stairs — movement is the beat; native 10s |
| 14 | kling-pro | 5s | $0.35 | |
| 15 | kling-pro | 5s | $0.35 | **never passed** — near-locked push, frozen printed smear |
| 16 | kling-pro | 5s | $0.35 | vertical rise (old clip missed the move) |
| 17 | kling-pro | 5s | $0.35 | **never passed** — near-locked breath, slab explicitly forbidden to resolve |
| **18** | **REUSE** | — | **$0** | clean kling hero — tender reach that halts; carried forward |
| 19 | kling-pro | 5s | $0.35 | Act V stillness |
| 20 | kling-pro | 5s | $0.35 | Act V stillness — delicate |
| 21 | kling-pro | 5s | $0.35 | Act V stillness — near-still balance |
| **22** | **REUSE** | — | **$0** | clean kling hero — fluid bloom; carried forward |
| 23 | kling-pro | 5s | $0.35 | **never passed** — strictest locked-off hold; highest residual retake risk |
| **24** | **REUSE** | — | **$0** | clean kling hero — vertigo pull-back; carried forward (veo upgrade offered below) |
| 25 | kling-pro | 5s | $0.35 | near-still |
| 26 | kling-pro | 5s | $0.35 | |
| 27 | kling-pro | 5s | $0.35 | |
| 28 | kling-pro | 5s | $0.35 | locked-off spine (matches 11) |
| 29 | kling-pro | 5s | $0.35 | dust-only near-still |
| 30 | kling-pro | 5s | $0.35 | **never passed** — locked-off, light and book pinned |

**24 shots × kling 5s $0.35 = $8.40 · 3 shots × kling 10s $0.70 = $2.10 · reuse
18/22/24 = $0 · reshoot batch $10.50.**

---

## Camera grammar across the acts

Deliberately varied so the film is not thirty push-ins. Pushes for intimacy;
lateral drift for survey; vertical descent as Act III's "no place to stop"
motif; a single pull-back reserved for the one scale moment (24); locked-off
where the viewer must stop.

| Act | Dominant grammar |
|---|---|
| I — the arithmetic | slow pushes into empty space; shot 3 near-locked |
| II — reward prediction error | push (4, 7), lateral reveal (5, 6) |
| III — the playbook | the downward motif — vertical descents (10, 12, 13) reading "no bottom, no place to stop," broken by the locked insistent dot (11) |
| IV — the cost | lateral (14), push (15), vertical (16), locked breath (17), the reaching hero (18) |
| V — the honest number (the turn) | the calmest act: a small release (19), delicate hairline drift (20), near-still balance (21), the one fluid bloom (22) |
| VI — the tribe at scale | locked intimacy (23) → the film's only pull-back (24) → near-still reflection (25) |
| VII — the close | lateral (26), gentle push (27), locked spine (28), dust-only stillness (29), locked close (30) |

---

## Shot table — motion prompts as they will be submitted

Slot = the picture window from `FRAME-BOOK.md`. Every clip is generated at 5s;
the Editor holds or ramps to the slot (see cut warnings). Act V slots are
provisional per the Art Director's flag. Each prompt carries the e-ink
anti-warble line verbatim: *"Hold every shape crisp and unchanged, edges stable
with no warping or rippling; move slowly and only one thing at a time; paper
grain stays static like print, never crawling."*

### Act I — the arithmetic

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 1 | 9.00 | slow push-in | Very slow push-in toward the single red paper flag at the centre of the empty field. The flag stays perfectly upright and still; nothing else enters. + anti-warble |
| 2 | 7.50 | push into depth | Slow push forward into the drift of pale paper slips, settling toward the single red slip in the clear space at the near edge. The paper does not shift or scatter; only the camera advances. + anti-warble |
| 3 | 7.06 | near-locked | Locked and almost still: the two hands hold position and the red bead hangs motionless in the gap between the palms, with only the faintest settle. Camera barely breathes forward. + anti-warble |

### Act II — reward prediction error

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 4 | 5.94 | slow push-in | Very slow push-in toward the red node glowing at the branch junction. The branching form holds every line fixed; nothing bends or grows. + anti-warble |
| 5 | 6.00 | lateral drift L→R | Slow lateral drift from the open empty left palm across to the loosely closed right hand where the red thread shows between the fingers. Hands stay still; only the camera glides. + anti-warble |
| 6 | 7.00 | lateral reveal L→R | Slow lateral reveal travelling left to right along the flat level line across the empty ivory, arriving on the single red peak just right of centre. The line and peak stay fixed and crisp; the line never thickens. + anti-warble |
| 7 | 6.50 | slow push-in | Gentle slow push-in toward the wrapped parcel on the doorstep, its loose red string held exactly in place. The parcel does not move; only the camera advances. + anti-warble |

### Act III — the playbook

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 8 | 7.00 | lateral drift | Slow lateral drift across the wet stone step, gliding over the scattered dark water marks and the single red mark among them. The marks stay fixed; none are added or moved. + anti-warble |
| 9 | 7.33 | slow push-in | Gentle slow push-in toward the right dish and its single red seed, the two bird silhouettes held perfectly still. Nothing leans or shifts; only the camera advances. + anti-warble |
| 10 | 7.00 | vertical descent | Slow vertical push descending down the hanging pale cord toward the red knot at its lowest point, the hand-shadow gripping below. The cord stays taut and fixed. + anti-warble |
| 11 | 7.00 | **locked-off** | Locked and still: the single red dot holds dead centre on the empty page and does not move; the camera is fixed, only the faint static life of paper. The dot never drifts. + anti-warble |
| 12 | 10.00 | vertical descent | Slow continuous vertical descent following the unbroken pale paper band down over the table edge toward the coils pooling on the floor, the red mark drifting up out of frame as the camera lowers. The band stays smooth and crisp. + anti-warble |
| 13 | 9.00 | vertical descent | Slow unhurried downward drift descending the flight of stairs into the soft blue distance, never reaching a landing, the single red tread passing through. Treads stay crisp and evenly spaced. + anti-warble |

### Act IV — the cost

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 14 | 6.27 | lateral drift left | Slow lateral drift left, travelling along the taut red thread away from the still white teacup toward the frame edge. The cup does not move; the thread stays straight and fixed. + anti-warble |
| 15 | 6.50 | slow push-in | Slow push-in toward the single red smear crossing the gutter between the two open blank books. The books stay flat and fixed; the smear holds its shape. + anti-warble |
| 16 | 6.50 | vertical rise | Slow vertical rise up the side of the water glass, travelling from the still water line up through the clear empty glass to the red painted stripe above. The glass does not tilt; the water stays level. + anti-warble |
| 17 | 6.50 | near-locked breath | A slow quiet breath of a push toward the face-down slab and the faint red ring drawn around it on the table. Nothing else moves. + anti-warble |
| 18 | 9.80 | **reach, decelerate, stop** *(kling)* | A single hand-shadow reaches slowly across the table toward the face-down slab and decelerates to a stop, fingertips coming to rest just outside the red ring, never arriving. One smooth tender motion that halts; the slab and ring stay fixed. + anti-warble |

### Act V — the honest number (the turn) · slots provisional

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 19 | 14.70 | small release | Two hands release the small red stone onto the table, the fingers lifting slowly clear as the stone settles flat and still, then stillness. The hands do not follow through the frame. + anti-warble |
| 20 | 12.00 | very slow lateral drift | Very slow lateral drift across the wide empty page, travelling along the hair-fine red line so it stays exactly as thin. The line does not thicken or waver. + anti-warble |
| 21 | 14.00 | near-still balance push | Near-still symmetrical slow push holding the potato and the spectacles in equal balance, the red thread on the potato fixed. Neither object is favoured or moves. + anti-warble |
| 22 | 18.71 | **fluid bloom** *(kling)* | The single red drop, having just touched the water near one rim, blooms slowly and smoothly outward across the shallow dish; the far side of the water stays perfectly clear and the bloom never reaches the far rim. Only the colour opens. The dish and rim stay fixed. + anti-warble |

### Act VI — the tribe at scale

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 23 | 5.19 | **locked-off** | Tight and still: the close ring of seated silhouettes holds and the red ember at the centre glows with the faintest steady life. Camera fixed. + anti-warble |
| 24 | 6.70 | **slow pull-back** *(kling)* | A slow continuous pull-back from the intimate ring at the near centre; the seated silhouettes soften and merge outward in every direction into a warm boundaryless field with no edge ever resolving, the red ember staying sharp at the near centre. One smooth outward motion. + anti-warble |
| 25 | 4.00 | near-still | Near-still: the shallow pool holds, the soft crowd of blue reflections barely shimmers and the single red ember burns steady in the reflection. Camera fixed. + anti-warble |

### Act VII — the close

| # | Slot (s) | Move | Motion prompt |
|---|---:|---|---|
| 26 | 5.67 | lateral drift | Slow lateral drift across the open ruled page, following the red ribbon marker as it trails onto the table. The book stays open and fixed, pages flat. + anti-warble |
| 27 | 5.50 | gentle push | Gentle slow push toward the fingers resting on the small round knob, the short red mark on its face held to one side. The knob and fingers stay still. + anti-warble |
| 28 | 5.00 | **locked-off (spine)** | Locked and still, matching the earlier red-dot frame exactly: the faded part-drained dot holds dead centre and does not move; the camera is fixed. The dot never drifts. + anti-warble |
| 29 | 4.00 | dust-only near-still | Total stillness except for fine dust drifting slowly through the warm evening light above the table; the face-down unlit slab, the plain cup and the slack red thread all stay fixed. + anti-warble |
| 30 | 4.36 | **locked-off (close)** | Locked and still: the wide cleared table holds in warm evening light, the single closed book with its red ribbon marker fixed. The camera does not move; the film is closing. + anti-warble |

---

## Stillness map

At least a fifth of the film should barely move. Nine shots are near-still or
locked-off, plus one delicate barely-moving shot — well over the fifth, and
they cluster exactly where the treatment wants breath: the 11/28 red-dot spine,
Act V's turn, and Act VII's close.

| # | Register | Why it barely moves |
|---|---|---|
| 3 | near-locked | the bead hangs; a whisper of a push only |
| 11 | locked-off | the insistent dot, dead centre; must not drift (spine, matches 28) |
| 17 | near-locked breath | a quiet breath before the reach of 18 |
| 20 | delicate drift | the hairline is nearly invisible; the move is barely there by design |
| 21 | near-still balance | the two equal objects; neither may move |
| 23 | locked-off | tight intimate ring, 5.19s — hold it |
| 25 | near-still | shortest live shot (4.00s); one small shimmer |
| 28 | locked-off | the draining dot; continuity spine, matches 11 frame for frame |
| 29 | dust-only | evening stillness; only dust drifts |
| 30 | locked-off | the closing frame; the film is putting itself down |

**Act V is the calmest passage in the film** as the treatment requires: 19 is a
small release, 20 a delicate drift, 21 near-still, and 22 the single genuine
motion. The camera does its most active work in Acts I–III and returns to rest
for the turn and the close.

---

## Cut warnings

Every clip is generated at **5.0s**. Slots shorter than or near 5s are covered.
The clips below have slots meaningfully longer than 5s, so the Editor must hold
or ramp; flagged with the usable window and the recommended fill so the Editor
does not rediscover it on the timeline.

| # | Slot (s) | Clip (s) | Usable window | Fill guidance |
|---|---:|---:|---|---|
| 1 | 9.00 | 5.0 | full 0.0–5.0 | slow push; ramp to ~0.55× or freeze-hold the last frame to fill 9.0s |
| 12 | 10.00 | 5.0 | full 0.0–5.0 | the AD composed this as a 10s move; a 5s clip fills it only by ramping to ~0.5×. If the descent ramps unevenly, hold the tail. |
| 13 | 9.00 | 5.0 | full 0.0–5.0 | continuous downward drift; ramp to ~0.55×. AD asked it to sustain up to 13s if C3's breath moves onto picture — ramp harder if so. |
| 18 | 9.80 | 5.0 | full 0.0–5.0 | the reach-and-stop; let the reach play 0.0–~3.5s then hold on the stopped fingertips to fill 9.8s. Do **not** ramp the reach itself slower than natural or the hand reads underwater. |
| 19 | 14.70 | 5.0 | full 0.0–5.0 | release plays early (~0.0–2.5s), then the stone is at rest — freeze-hold the settled frame to fill the remaining ~12s. Near-still tail is free. |
| 20 | 12.00 | 5.0 | full 0.0–5.0 | delicate drift; ramp to ~0.4× across the full slot, or drift 0.0–5.0 then hold. Barely-moving, so a long hold is invisible. |
| 21 | 14.00 | 5.0 | full 0.0–5.0 | near-still; hold the frame to fill. Cheapest long slot to sustain. |
| 22 | 18.71 | 5.0 | full 0.0–5.0 | the longest slot in the film against a 5s clip. The bloom opens 0.0–~4.0s; ramp the bloom to ~0.3× so it opens across the full slot, or open then hold on the settled bloom. Kling was chosen so this ramps cleanly. |

No clip has a *defect* window shorter than its slot at this stage — usable
windows are confirmed only after the clips are watched in the generation
dispatch, and any warble/overrun found there is filed then.

### Cut warnings confirmed at the gate (KEEP clips only)

| # | Finding | Usable in/out | Guidance |
|---|---|---|---|
| 11 | Slight camera drift across the clip; the spine requires 11 and 28 to match frame for frame. | freeze a single frame | **Freeze-hold frame 0** (the keyframe) rather than playing the drift, so the 11/28 spine stays matched. Both dots sit dead centre at t=0. |
| 12 | Clean vertical descent, but a wood-plank floor and a soft blue wash creep into the lower-right from roughly the two-thirds mark. | ~0.0–3.3s clean | Favour the earlier clean portion when ramping the 5s clip across the 10s slot; hold before the blue wash dominates. |
| 18 | The reach decelerates and comes to rest, but by the very tail the fingertips drift onto the slab — the "never arrives" intent is best served earlier. | reach 0.0–~3.3s, hold there | Play the reach to the stop at ~3.3s, then freeze on the stopped fingertips to fill 9.80s. Do **not** use the final frame where the hand over-arrives; do not ramp the reach slower than natural. |
| 28 | Same slight drift as 11 (they are the spine pair). | freeze a single frame | **Freeze-hold frame 0** to match 11 exactly. |

All other KEEP clips are usable full 0.0–5.0s within their slot per the planning
table above; fill guidance there stands.

---

## Vertical notes — the 9:16 social edition

The Editor builds the social edition from these clips, not new ones. Notes are
per shot: survives a centre crop (subject + accent inside the middle ninth),
and whether the shot is strong enough to **open** a 30s recut (front-loaded
motion that reads at phone size). Locked-off and near-still shots survive the
crop but make poor openers.

| # | Survives 9:16 centre crop | Strong opener? | Note |
|---|---|---|---|
| 1 | yes | yes | flag centred; slow push reads on phone |
| 2 | yes | ok | red slip at near edge but within centre column |
| 3 | yes | no | near-still; hands centred |
| 4 | yes | ok | node centred |
| 5 | yes — do not crop tighter than centre | no | accent 36–65% width (AD flag); right hand near edge |
| 6 | yes | ok | peak at ~62% width — inside the safe band but near its right edge; do not crop tighter |
| 7 | yes | ok | parcel centred |
| 8 | yes | ok | red mark placement varies; drift keeps it central |
| 9 | yes — do not crop tighter than centre | no | accent near edge (AD flag); right dish |
| 10 | yes | **yes** | vertical descent is native to 9:16; cord centred |
| 11 | yes | no | locked spine; centred dot — perfect crop, weak opener |
| 12 | yes | **yes** | the film's biggest vertical move — ideal 9:16 opener; band runs down centre |
| 13 | yes | **yes** | downward drift, native to vertical |
| 14 | risk | no | thread runs **out of frame left** — a left-drift walks the accent toward the crop edge; keep the cup-and-near-thread centred, do not follow the thread far |
| 15 | yes | ok | smear crosses the centre gutter — sits in the column |
| 16 | yes | ok | vertical gap on the glass; glass centred |
| 17 | yes | no | near-still; ring centred |
| 18 | yes | ok | emotional centre; the reach crosses toward the centred ring — reads at phone size, front-loaded reach |
| 19 | yes | ok | stone settles at centre; hands leave frame (don't follow) so accent stays central |
| 20 | **weak** | no | hair-fine line across a wide page — the delicate horizontal move barely reads even at 16:9; on a phone it may vanish. Carry this on the horizontal master, not the vertical. |
| **21** | **NO** | no | **Cannot survive a centre crop.** Potato and spectacles sit either side of centre; a 9:16 crop loses one and kills the comparison. Inherent to a two-object shot (AD flag carried forward). Needs a pan or a rebuild in the vertical edition. |
| 22 | yes | **yes** | drop blooms near one rim toward centre — keep the crop on the blooming side; front-loaded fluid motion, strong opener |
| 23 | yes | no | locked intimate ring, centred |
| 24 | yes | **yes** | pull-back from a centred ember; vertigo reads hard at phone size — a strong opener, push the move if anything |
| 25 | yes | no | near-still; ember centred |
| 26 | yes — do not crop tighter than centre | ok | ribbon trails off the page; keep the marker central |
| 27 | yes | no | knob and fingers centred; gentle |
| 28 | yes | no | locked spine; centred dot (matches 11) |
| 29 | yes | no | near-still; slab/cup/thread centred, evening |
| 30 | yes | no | locked close; book centred |

**Best openers for the social edition:** 12, 24, 22, 13, 10 — all either a
strong vertical descent or a bloom/pull-back with the accent held at centre and
motion that survives phone-size and re-encoding. **Do not open on** 11, 28, 30,
23, 29 (locked or near-still) or 20 (too delicate to read).

**One shot cannot go vertical without help:** shot 21. Flagged to the Editor:
pan or rebuild for the 9:16 edition.

---

## Batch quote — approvable

Fetched live from `POST /v1/videos/estimate` on 2026-07-23, each with the
shot's real `sourceUrl` as `imageUrl`, `durationSeconds: 5`, at the chosen
model. All thirty returned a non-null `usd` and a live quote token. No price
came back null.

| Line | Value |
|---|---|
| Route | `POST /v1/videos/generations` (image-to-video), 5s each, `16:9` |
| seedance-lite | 27 × $0.20 = **$5.40** |
| kling-pro (heroes 18, 22, 24) | 3 × $0.35 = **$1.05** |
| **Batch total, as planned** | **$6.45** |
| All-seedance floor (no heroes) | 30 × $0.20 = **$6.00** |
| **Upgrade delta for the 3 kling heroes** | **+$0.45** |

Running film spend if approved: $3.28 keyframes + $6.45 clips = **$9.73**
against the $16.10 authorisation, leaving ~$6.37 headroom for retakes.

Retakes are **not** covered by this quote. The review gate on a thirty-shot
film typically returns two to four clips; each retake batch is estimated and
approved on its own.

**Not submitted. Awaiting Isaac's explicit yes on $6.45 (or $6.00 without the
heroes). A later dispatch runs the generation.** Quote tokens expire in five
minutes and will be re-fetched fresh at submit time.

---

## Generation dispatch — batch run, gate, and results

**Filed 2026-07-23. Isaac approved $6.45 (27 seedance-lite + 3 kling-pro heroes
18/22/24). All thirty submitted, all thirty polled to terminal `done`, all
thirty watched with my own eyes via 5-frame contact sheets across the full
duration, with dense 8-frame strips pulled on every borderline shot.** No shot
was sampled; each clip was inspected across its whole span.

**Protocol honoured.** The `production_submit` MCP wrapper was skipped (its
quote/submit hash-mismatch bug bit the Art Director repeatedly). Each shot went
through the documented HTTP proxy: fresh `POST /v1/videos/estimate` immediately
before submit with the exact body (`imageUrl` = the shot's `sourceUrl`, 5s,
chosen model), per-shot price checked against the filed figure, then
`POST /v1/videos/generations` with the identical body + fresh `quoteToken` +
capability bearer. Every seedance estimate returned exactly $0.20 and every
kling estimate exactly $0.35 — zero price drift. The loop hard-capped at $6.45
and halted-on-drift logic never fired. No transient fal error occurred; no
resubmit was needed. Preflight `ok true`, `hasKey true`, cap $30. Spent-today
went $3.28 → $9.73 (delta $6.45, confirmed at `/health`).

Clips are 5.04s, 16:9 — seedance at 1248x704, the three kling heroes at
1928x1072. Local path pattern: `output/videos/<jobId>.mp4`
(absolute: `/Users/isaachernandez/blog design/output/videos/<jobId>.mp4`).

### Results table — job id, path, verdict

| # | Model | $ | Job id | Local clip | Verdict |
|---|---|---:|---|---|---|
| 1 | seedance-lite | 0.20 | 019f9018-ad3e-78c1-800e-884a3e64f7d7 | output/videos/019f9018-ad3e-78c1-800e-884a3e64f7d7.mp4 | **KEEP** — clean push-in, flag upright, one accent, no warble |
| 2 | seedance-lite | 0.20 | 019f9018-af26-7a22-9ca5-ee34b191f8d2 | output/videos/019f9018-af26-7a22-9ca5-ee34b191f8d2.mp4 | **KEEP** — one red slip tracked to the near edge; faint blue table smudge, minor |
| 3 | seedance-lite | 0.20 | 019f9018-b10f-7ea1-9551-0540ef5fa512.mp4 | output/videos/019f9018-b10f-7ea1-9551-0540ef5fa512.mp4 | **KEEP** — near-locked, bead holds, only a faint settle |
| 4 | seedance-lite | 0.20 | 019f9018-b315-74b2-9f0d-2a5c787de8ba | output/videos/019f9018-b315-74b2-9f0d-2a5c787de8ba.mp4 | **KEEP** — node glow pulses (single motion), branches fixed |
| 5 | kling-pro | 0.35 | 019f905c-81b2-7850-a63a-6a78c97fea17 | output/videos/019f905c-81b2-7850-a63a-6a78c97fea17.mp4 | **KEEP (retake)** — both hands held completely still, right hand never uncurls, red thread visible between the fingers throughout; gentle drift. Defect gone. |
| 6 | seedance-lite | 0.20 | 019f905c-81fd-77a0-917a-1fd6b7344c24 | output/videos/019f905c-81fd-77a0-917a-1fd6b7344c24.mp4 | **REJECT (2nd round)** — the single peak multiplied into a whole range of red peaks; worse than round one. Held for a third batch. |
| 7 | seedance-lite | 0.20 | 019f9018-b938-7291-9edb-138cea69f587 | output/videos/019f9018-b938-7291-9edb-138cea69f587.mp4 | **KEEP** — gentle push, parcel + string fixed |
| 8 | seedance-lite | 0.20 | 019f905c-8246-77e2-8ac9-9f06e5ed821a | output/videos/019f905c-8246-77e2-8ac9-9f06e5ed821a.mp4 | **KEEP (retake)** — no figure, no feet, no flooding pool, no drips; red stays a single dry printed mark. Minor: a couple of faint stray red specks near it late, well inside tolerance. Defect gone. |
| 9 | seedance-lite | 0.20 | 019f905c-8294-7a63-a960-358e80452e31 | output/videos/019f905c-8294-7a63-a960-358e80452e31.mp4 | **KEEP (retake)** — exactly one red seed in the right dish across the whole clip; no multiplication; birds still, gentle push. Defect gone. |
| 10 | seedance-lite | 0.20 | 019f9018-bf5b-7990-a4e1-383d24883005 | output/videos/019f9018-bf5b-7990-a4e1-383d24883005.mp4 | **KEEP** — near-static; cord + knot + grip hold |
| 11 | seedance-lite | 0.20 | 019f9018-c163-7361-a9f0-d1f89b390012 | output/videos/019f9018-c163-7361-a9f0-d1f89b390012.mp4 | **KEEP** — slight camera drift; freeze-hold frame 0 for spine (see cut warnings) |
| 12 | seedance-lite | 0.20 | 019f9018-c378-71e2-92eb-0ca92bff7e55 | output/videos/019f9018-c378-71e2-92eb-0ca92bff7e55.mp4 | **KEEP** — clean descent, red mark drifts out; late wood/blue floor wash (window note) |
| 13 | seedance-lite | 0.20 | 019f905c-8305-7e91-b9a8-145c92435b78 | output/videos/019f905c-8305-7e91-b9a8-145c92435b78.mp4 | **KEEP (retake)** — exactly one tomato-red tread holds its colour the whole descent; no other tread recolours red or blue, no fade. Defect gone. |
| 14 | seedance-lite | 0.20 | 019f905c-834d-7611-8d10-6a5bb6983b01 | output/videos/019f905c-834d-7611-8d10-6a5bb6983b01.mp4 | **KEEP (retake)** — exactly one cup, no second cup; the red thread stays visible and taut to the frame edge the whole time. Defect gone. |
| 15 | seedance-lite | 0.20 | 019f905c-8399-7f90-8365-7927801af002 | output/videos/019f905c-8399-7f90-8365-7927801af002.mp4 | **REJECT (2nd round)** — the smear still balloons into a thick brushstroke and gains splatter spray at both ends. Held for a third batch. |
| 16 | seedance-lite | 0.20 | 019f905c-83e5-7961-a046-55929a40b64a | output/videos/019f905c-83e5-7961-a046-55929a40b64a.mp4 | **KEEP (retake)** — clean near-still: no invented grey droplet, water perfectly still and level, red stripe above the water, glass untilted. The invented-element defect is gone; reads as a stable near-still as the reject note pre-approved. |
| 17 | seedance-lite | 0.20 | 019f905c-842d-7ba2-a473-b75fcc0f856c | output/videos/019f905c-842d-7ba2-a473-b75fcc0f856c.mp4 | **REJECT (2nd round)** — the slab resolved into a wooden block with a glowing red rounded-rectangle inset (a lit screen); the device defect returned amplified. Held for a third batch. |
| **18** | **kling-pro** | 0.35 | 019f9018-cfc9-78d0-8344-88b99e9e86ad | output/videos/019f9018-cfc9-78d0-8344-88b99e9e86ad.mp4 | **KEEP — HERO CLEAN.** Tender organic reach, one motion, halts; not mechanical. Cut window note below |
| 19 | seedance-lite | 0.20 | 019f9018-d1cd-7c72-aca3-715513c1e045 | output/videos/019f9018-d1cd-7c72-aca3-715513c1e045.mp4 | **KEEP** — two hands release the stone and lift clear, stone settles alone |
| 20 | seedance-lite | 0.20 | 019f9018-d3de-7e40-aaf7-14fc18966d6c | output/videos/019f9018-d3de-7e40-aaf7-14fc18966d6c.mp4 | **KEEP** — delicate near-still hairline, thin and steady |
| 21 | seedance-lite | 0.20 | 019f9018-d5e8-7363-8b9c-38f185b25f99 | output/videos/019f9018-d5e8-7363-8b9c-38f185b25f99.mp4 | **KEEP** — balanced symmetric push, neither object favoured (vertical crop still fails per AD flag) |
| **22** | **kling-pro** | 0.35 | 019f9018-d7ed-7373-b36a-6db54f4b087d | output/videos/019f9018-d7ed-7373-b36a-6db54f4b087d.mp4 | **KEEP — HERO CLEAN.** Smooth fluid bloom, reads as liquid not texture; far side stays clear |
| 23 | kling-pro | 0.35 | 019f905c-8474-76b3-8959-3fecdc13bb00 | output/videos/019f905c-8474-76b3-8959-3fecdc13bb00.mp4 | **REJECT (2nd round)** — kling held the shapes crisp but still animated a back-right figure into a raised-arm steeple mid-clip. The figure-holds-still bar was not met. Held for a third batch. |
| **24** | **kling-pro** | 0.35 | 019f9018-dc10-7e13-bccc-9b1266357710 | output/videos/019f9018-dc10-7e13-bccc-9b1266357710.mp4 | **KEEP — HERO CLEAN.** Smooth pull-back, ember sharp at centre, soft field softens without edge-crawl |
| 25 | seedance-lite | 0.20 | 019f9018-de11-7240-bb2b-4a77fd3ed990 | output/videos/019f9018-de11-7240-bb2b-4a77fd3ed990.mp4 | **KEEP** — near-still pool, ember steady, faint shimmer |
| 26 | seedance-lite | 0.20 | 019f905c-8510-7b23-beb9-9fbc28dbe86d | output/videos/019f905c-8510-7b23-beb9-9fbc28dbe86d.mp4 | **KEEP (retake)** — book stays open and flat, pages never flip; ribbon stays a straight flat marker, never curls; exactly one red element. Defect gone. |
| 27 | seedance-lite | 0.20 | 019f9018-e238-7c12-acc7-fa3e42e7455a | output/videos/019f9018-e238-7c12-acc7-fa3e42e7455a.mp4 | **KEEP** — gentle push, knob + red mark + fingers hold |
| 28 | seedance-lite | 0.20 | 019f9018-e437-72d2-99d7-e95425fa3d23 | output/videos/019f9018-e437-72d2-99d7-e95425fa3d23.mp4 | **KEEP** — faded dot crisp and singular; same slight drift as 11, freeze-hold for spine |
| 29 | seedance-lite | 0.20 | 019f905c-8557-7363-9ee4-def643435ce8 | output/videos/019f905c-8557-7363-9ee4-def643435ce8.mp4 | **KEEP (retake)** — slab stays face down, unlit, no screen and no glow ever appears; slack red thread is the only red. Device-inversion defect gone. Note: warm evening light intensifies across the clip — within the shot's warm-light/dust brief; Editor may favour the earlier-to-mid frames. |
| 30 | seedance-lite | 0.20 | 019f905c-859e-7451-8a21-d0328159fe11 | output/videos/019f905c-859e-7451-8a21-d0328159fe11.mp4 | **REJECT (2nd round)** — a harsh warm light beam and hard shadow still sweep across the frame, and the closed book animates open (pages lift). Two faults in the closing locked-off shot. Held for a third batch. |

> **Superseded by the retake batch below — see "Retake batch — dispatch, gate,
> and results." After the retake, 25 of 30 shots have a KEEP clip; shots 6, 15,
> 17, 23, 30 remain open for a third batch.**

**Gate result (first pass): 17 KEEP, 13 REJECT. All three kling heroes (18, 22, 24) came
back clean** — the exact failures they were promoted to avoid (mechanical hand,
texture-crawl bloom, edge-crawling soft field) did not occur. The rejections
cluster almost entirely on seedance-lite shots whose subject is a hand, a
figure, a liquid, or a single small mark — the register where the model
elaborates rather than holds: it invents figures and second objects, multiplies
or floods the accent, and articulates what should be still. Batch spend $6.45,
exactly as approved.

### Rejections — defect named, and the change for the retake

Retakes are **not** covered by the $6.45 approval. Each is its own batch, its
own estimate, its own yes. Held pending Isaac.

| # | Defect (named precisely) | Change on the retake |
|---|---|---|
| 5 | The right hand uncurls from a loose fist to a fully splayed open palm across the clip — a second organic motion competing with the camera drift — and the concealed red thread is lost as it opens. Breaks "hands stay still; only the camera glides." | Lock the hands hard ("both hands completely motionless, not one finger moves; only the camera glides left to right"); consider promoting to kling-pro, where hand geometry holds under a move. Re-quote as an upgrade. |
| 6 | The red peak scales taller in place and a new rounded hump sprouts on the flat line — the graph animates itself instead of a camera reveal. Breaks "the line and peak stay fixed; the line never thickens." | Forbid any change to line or peak explicitly ("the line and peak are printed and frozen, they never grow, rise, or change shape; only the camera glides"). |
| 8 | A standing figure's legs and feet are invented into the frame, and the single red mark floods into a large spreading red pool with drips down the step edge — reads as blood. Gross departure; accent size/shape violated; figure added. | Forbid figures and any spread ("no people, no feet; the marks are dry printed spots that never spread, grow, drip, or move; only the camera drifts laterally"). |
| 9 | The single red seed multiplies to two, then three, in the right dish (confirmed on the dense strip). Breaks the one-accent / one-seed discipline. | Pin the count ("exactly one red seed, and never more than one; no seed is ever added"). |
| 13 | The red tread fades and multiple treads recolour to blue in a cascade; late frames carry no clear red accent — a breach of "one red thing in every frame." | Pin the accent ("exactly one tread stays tomato red for the whole shot and never changes colour; no other tread ever turns red or blue; only the camera descends"). |
| 14 | A second teacup materialises mid-clip and the red thread vanishes by the end — added object, accent lost. | Pin object count and accent ("exactly one cup, no second cup ever appears; the red thread stays visible and taut the whole time; only the camera drifts left"). |
| 15 | The red smear balloons into a thick splattering brushstroke and extra red spots appear on the left page — accent does not hold shape and multiplies. | Freeze the mark ("the red smear is dry and printed, it never grows, spreads, or splatters, and no new red appears; only the camera pushes in"). |
| 16 | The briefed vertical camera rise never happens; instead an unbriefed grey droplet falls and settles inside the glass. Accent and palette are fine — this is a wrong-motion / invented-element reject, the weakest of the thirteen. **Salvageable as a near-still** if Isaac prefers not to spend. | Specify the camera move explicitly and forbid interior motion ("the camera rises slowly up the outside of the glass; nothing inside the glass moves, no drop falls, the water is perfectly still"). |
| 17 | A hand and a wooden tray enter a shot briefed as "nothing else moves," and the slab starts to read as a device. Locked-breath discipline broken. | Hard lock ("no hand, no tray, nothing enters; the slab stays face down and featureless; only a barely-perceptible camera breath"). |
| 23 | The seated silhouettes raise their arms into a steeple over the ember — a large invented motion in a shot mapped as locked-off still. | Hard lock the figures ("everyone stays perfectly still and seated, no arms raise, no one moves; only the ember's faint glow; camera fixed"). Consider kling if seedance keeps animating the ring. |
| 26 | The book pages flip up, the ribbon curls into a heart shape on the table, and a transient second red squiggle appears on the left page. Breaks "the book stays open and fixed, pages flat." | Freeze the book ("the open book and its flat pages never move or turn; the ribbon is a straight flat marker that never curls or forms shapes; exactly one red element"). |
| 29 | The slab flips face-up with a glowing dark-blue screen — reintroduces in motion the exact device defect the keyframe retake killed, and puts blue in a subject role. The film's closing "device put down" beat is inverted. | Hard lock ("the slab stays face down, unlit, blank; no screen, no glow ever appears; the only red is the slack thread; only dust drifts"). |
| 30 | A harsh warm spotlight and a hard-edged shadow sweep across the frame — the style block forbids harsh shadows, and this locked-off closing frame must be still. | Lock light and camera ("soft even warm evening light that does not change; no hard shadow, no moving light; the camera is completely fixed; the film is closing"). |

**Retake batch is 12 or 13 shots** depending on whether Isaac wants shot 16
re-shot or kept as a near-still. Several fixes (5, 23) may warrant a kling-pro
upgrade, which re-quotes as a new line. On approval I will estimate the exact
batch live, present per-shot and total, and hard-cap it. Rough seedance-only
floor for 13 retakes is 13 × $0.20 = $2.60, well inside the ~$6.37 headroom
under the $16.10 authorisation — but the estimate governs, not this figure.

---

## Retake batch — dispatch, gate, and results

**Filed 2026-07-23. Isaac approved $2.90 for all 13 rejects: 11 seedance-lite
with tightened, elaboration-forbidding prompts, and shots 5 and 23 promoted to
kling-pro ($0.35) as new price lines.** Submitted through the documented HTTP
proxy (the `production_submit` MCP wrapper was skipped for its quote/submit
hash-mismatch bug). Each shot was re-estimated immediately before submit with
the exact body (`imageUrl` = the shot's `sourceUrl`, 5s, chosen model); every
seedance estimate returned exactly $0.20 and every kling estimate exactly $0.35
— zero drift. The loop hard-capped at $2.90 and never tripped. All 13 polled to
terminal `done`; no transient fal error occurred, so no resubmit was needed.
Batch spend **$2.90**, taking the film to **$12.63** of the $16.10
authorisation. Clips are 5.04s, 16:9; local path `output/videos/<jobId>.mp4`.

Every retake was watched via an 8-frame contact sheet across the full
duration, with dense 12-frame strips pulled on shots 8, 15, and 23. The bar was
specific: each retake must **not reproduce the named defect it was re-shot to
fix**, and shots 5 and 23 were held to the figure-holds-still standard.

### Second-round gate — 8 pass, 5 fail

| # | Model | Verdict | Finding |
|---|---|---|---|
| 5 | kling-pro | **KEEP** | Both hands held completely motionless; the right hand never uncurls; the red thread stays visible between the fingers the whole time. Met the figure-holds-still bar. |
| 6 | seedance-lite | **REJECT (2nd)** | The single red peak multiplied into a whole range of red peaks — the elaboration got worse, not better. |
| 8 | seedance-lite | **KEEP** | No figure, no feet, no flooding pool, no drips; accent stays a single dry printed mark. Minor faint stray red specks near it late, inside tolerance. |
| 9 | seedance-lite | **KEEP** | Exactly one red seed throughout; no multiplication. |
| 13 | seedance-lite | **KEEP** | Exactly one tomato-red tread holds its colour the whole descent; no blue recolour cascade, no fade. |
| 14 | seedance-lite | **KEEP** | Exactly one cup; the red thread stays visible and taut to the frame edge throughout. |
| 15 | seedance-lite | **REJECT (2nd)** | The smear still balloons into a thick brushstroke and gains splatter spray at both ends (confirmed on the dense strip). |
| 16 | seedance-lite | **KEEP** | Clean near-still: no invented droplet, water still and level, red stripe above the water, glass untilted. The near-still outcome the reject note pre-approved. |
| 17 | seedance-lite | **REJECT (2nd)** | The slab resolved into a wooden block with a glowing red rounded-rectangle inset — a lit screen. The device defect returned amplified. |
| 23 | kling-pro | **REJECT (2nd)** | Kling held the shapes crisp but still animated a back-right figure into a raised-arm steeple mid-clip (confirmed on the dense strip). The figure-holds-still bar was not met. |
| 26 | seedance-lite | **KEEP** | Book open and flat, pages never flip; ribbon a straight flat marker, never curls; one red element. |
| 29 | seedance-lite | **KEEP** | Slab face down, unlit, no screen or glow; slack red thread the only red. Note: warm evening light intensifies across the clip — within the shot's brief; Editor may favour the earlier-to-mid frames. |
| 30 | seedance-lite | **REJECT (2nd)** | A harsh warm light beam and hard shadow sweep across the frame, and the closed book animates open. Two faults in the closing locked-off shot. |

**Standing after the retake: 25 of 30 shots have a KEEP clip.** The five still
open — **6, 15, 17, 23, 30** — are held for a third batch, which is its own
estimate and its own approval. The $2.90 approval is fully spent; nothing is
resubmitted without Isaac's explicit yes on a fresh quote.

### Third-batch strategy (not yet quoted, for the next pass)

Each of the five is the model elaborating past a hard prohibition. For the next
approval I will consider:

- **6** — seedance ignored "no new peak ever appears" and grew a range. Try a
  near-locked framing that treats the peak as printed and frozen, or promote to
  kling-pro (held graph-like geometry better on other shots).
- **15** — the smear keeps growing and splattering under a push-in. Drop the
  push to a near-locked hold so there is no scale change to trigger growth, or
  kling-pro.
- **17** — seedance keeps resolving the slab into a lit device. This is the same
  failure the keyframe pass fought; consider kling-pro and language forbidding
  any inset panel, glow, or screen by name.
- **23** — kling still raised an arm; the ring wants a true locked-off. Consider
  a shorter effective hold or veo-3-fast only if Isaac wants to spend on the one
  figure the model refuses to hold. (5.19s slot — the shortest of the five.)
- **30** — the closing shot needs the book to stay closed and the light fixed.
  A locked-off with an explicit "book stays closed, light does not change" line;
  kling-pro if seedance keeps sweeping light.

---

## MOTION RESHOOT — dispatch, gate, and results (kling-pro, whole film)

**Filed 2026-07-23. Isaac approved $10.50 — 27 shots reshot on kling-pro
(image-to-video from each locked frame), 3 heroes (18, 22, 24) reused at $0, no
veo.** This batch supersedes both seedance batches above: the reshoot exists
because Isaac found the seedance clips dull and defect-prone, and the new
standard is an explicit motivated CAMERA move over a held subject. All 27
submitted through the documented HTTP proxy (the `production_submit` MCP wrapper
skipped for its quote/submit hash-mismatch bug): fresh `POST /v1/videos/estimate`
immediately before each submit with the exact body (`imageUrl` = the shot's
`sourceUrl`, correct duration, model kling-pro), price checked, then
`POST /v1/videos/generations` with identical body + fresh `quoteToken` +
capability bearer.

**Every 5s estimate returned exactly $0.35 and every 10s estimate exactly $0.70
— zero drift; the hard-cap-at-$10.50 and halt-on-drift logic never fired. All
27 polled to terminal `done`; no transient fal error, no resubmit.** Preflight
`ok true`, `hasKey true`, engine cap $50, film ceiling $30. Spent-today
**$12.63 → $23.13** (delta $10.50, confirmed at `/health`), leaving $6.87 of the
$30 ceiling. Clips are 5.04s / 10.04s, 16:9; local path
`output/videos/<jobId>.mp4`.

Every reshot clip watched with my own eyes via a 6-frame contact sheet (8-frame
on the three 10s shots) across the full duration, with dense 12-frame strips
pulled on the two borderlines (16, 19) and on all five historically-failing
shots (6, 15, 17, 23, 30).

### Reshoot results — job id, path, verdict

Path prefix: `/Users/isaachernandez/blog design/output/videos/`.

| # | Model | Dur | $ | Job id | Verdict |
|---|---|---:|---:|---|---|
| 1 | kling-pro | 10s | 0.70 | 019f9277-8739-7af2-8722-e582f825ca21 | **KEEP** — sustained slow push-in, flag scales up, upright, one accent, grain stable |
| 2 | kling-pro | 5s | 0.35 | 019f9277-87e3-7ac0-834b-61ff223db9e6 | **KEEP** — camera advances into the drift, red slip grows, paper never scatters |
| 3 | kling-pro | 5s | 0.35 | 019f9277-8876-7830-a996-d38a30378a47 | **KEEP** — near-locked (stillness map), bead holds, faint breath |
| 4 | kling-pro | 5s | 0.35 | 019f9277-890f-7e23-bc01-d97cbd0a0e4e | **KEEP** — clean push-in, branch form scales, node stays red, nothing sprouts |
| 5 | kling-pro | 5s | 0.35 | 019f9277-89db-7ce3-9f2e-66091c8910bc | **KEEP** — lateral drift reads, both hands held, right fist never uncurls, thread visible |
| 6 | kling-pro | 5s | 0.35 | 019f9277-8a6e-7e73-a86c-176a4e6e4eb6 | **KEEP** (never passed before) — one peak the whole clip, line never thickens, no new humps; dense strip confirmed |
| 7 | kling-pro | 5s | 0.35 | 019f9277-8b06-76e1-82cb-b5e16ff4dd06 | **KEEP** — push-in, parcel + red string held |
| 8 | kling-pro | 5s | 0.35 | 019f9277-8bae-7e22-a91e-103d4d995a61 | **KEEP** — lateral drift, single red mark stays singular, no figure, no flood |
| 9 | kling-pro | 5s | 0.35 | 019f9277-8c40-7d83-9b09-e4d9fc70fe0a | **KEEP** — push-in, exactly one red seed throughout, birds hold |
| 10 | kling-pro | 5s | 0.35 | 019f9277-8cdf-7b50-8b0d-d82fb8c6dd7a | **KEEP** — vertical descent reads, cord taut, one red knot, grip stable |
| 11 | kling-pro | 5s | 0.35 | 019f9277-8db2-7c42-8cef-71966d67330c | **KEEP** — locked spine, dot dead centre, stable (freeze-hold frame 0 for 11/28 match) |
| 12 | kling-pro | 10s | 0.70 | 019f9277-8e41-72d3-8992-17a1806c53fb | **KEEP** — strong 10s vertical descent, band scrolls cleanly, red mark drifts out, no wood-floor wash |
| 13 | kling-pro | 10s | 0.70 | 019f9277-8ed1-73b0-9e32-4eacc4c69ee1 | **KEEP** (recolour cascade before) — 10s downward drift, one red tread rides up and out, no blue recolour |
| 14 | kling-pro | 5s | 0.35 | 019f9277-8f54-78a3-a2e5-a9636ce8fdde | **KEEP** (second cup before) — lateral drift left, one cup, thread taut to the edge |
| 15 | kling-pro | 5s | 0.35 | 019f9277-8ff9-7c91-90a5-9feca581e956 | **KEEP** (never passed) — push-in, smear stays one continuous stroke, no splatter, no extra red; dense strip confirmed |
| 16 | kling-pro | 5s | 0.35 | 019f9277-9092-73a1-99ef-53cf55d3f0a3 | **REJECT — KEEP OLD.** Glass geometry doubles into two offset outlines from midpoint on (edges not stable); dense strip confirmed. Old seedance near-still (019f905c-83e5-7961-a046-55929a40b64a) is clean; retained. Retake offered. |
| 17 | kling-pro | 5s | 0.35 | 019f9277-9118-7913-a3ac-a86c892252b7 | **KEEP** (device defect twice) — quiet push breath, slab stays featureless, NO screen/glow ever, no hand/tray; dense strip confirmed |
| 18 | **REUSE** | 9.8s | 0 | 019f9018-cfc9-78d0-8344-88b99e9e86ad | **KEEP (hero, carried forward)** — tender reach that halts; cut window below |
| 19 | kling-pro | 5s | 0.35 | 019f9277-91cb-74c1-863f-7a17bb5d9b11 | **REJECT — KEEP OLD.** Large solid-blue-filled second hand sweeps in from left in back half (invented element + blue-as-subject); dense strip confirmed. Old seedance clip (019f9018-d1cd-7c72-aca3-715513c1e045) is a clean KEEP with the release gesture; retained. |
| 20 | kling-pro | 5s | 0.35 | 019f9277-924e-7002-97e8-ccbd9ee81829 | **KEEP** — delicate lateral drift, hairline stays thin, no waver |
| 21 | kling-pro | 5s | 0.35 | 019f9277-92cf-7682-be91-d0c2150f468c | **KEEP** — near-still symmetric push, both objects held equally (9:16 crop still fails, AD flag) |
| 22 | **REUSE** | 5s | 0 | 019f9018-d7ed-7373-b36a-6db54f4b087d | **KEEP (hero, carried forward)** — fluid bloom, far side stays clear |
| 23 | kling-pro | 5s | 0.35 | 019f9277-934f-7b72-8af2-ee53988caa5a | **KEEP** (arm-steeple before) — locked ring holds seated, NO arms raise, ember steady; dense strip confirmed |
| 24 | **REUSE** | 6.7s | 0 | 019f9018-dc10-7e13-bccc-9b1266357710 | **KEEP (hero, carried forward)** — vertigo pull-back, ember sharp, soft field no edge-crawl |
| 25 | kling-pro | 5s | 0.35 | 019f9277-9418-7bb3-a720-6c5810da567d | **KEEP** — near-still pool, faint shimmer, red ember steady in reflection |
| 26 | kling-pro | 5s | 0.35 | 019f9277-949d-73b1-9196-0f29e0cc5ac1 | **KEEP** (pages-flip + heart before) — lateral drift over a flat book, pages stay flat, ribbon one marker, no heart |
| 27 | kling-pro | 5s | 0.35 | 019f9277-9520-7b93-b061-f20d10ec50a5 | **KEEP** — gentle push-in, knob + fingers held, one red mark to the side |
| 28 | kling-pro | 5s | 0.35 | 019f9277-95f6-7070-a8dd-6f1c48b981d1 | **KEEP** — locked spine, faded dot dead centre, matches 11 (freeze-hold frame 0) |
| 29 | kling-pro | 5s | 0.35 | 019f9277-9680-78c2-8e8b-07d4c771aa8d | **KEEP** (device-flip before) — gentle push, slab stays face down and unlit, slack red thread only red |
| 30 | kling-pro | 5s | 0.35 | 019f9277-9708-74c3-b0f3-d467927f04fa | **KEEP** (light-sweep + book-opens before) — gentle push, book stays closed, light soft, ribbon held; dense strip confirmed |

**Gate result: 25 of 27 reshoots PASS, 2 REJECT (keep old).** All five shots
that never passed on seedance (6, 15, 17, 23, 30) came back clean on kling —
the camera-over-held-subject technique held structure where seedance elaborated.
The camera move genuinely reads on every passer (pushes, lateral drifts,
vertical descents), and no elaboration defect recurred on any passer. The two
failures are kling *animating content* rather than moving the lens: 16 doubled
the glass, 19 invented a second hand. **All 30 shots now have a KEEP clip: 25
new kling reshoots + 3 reused kling heroes (18/22/24) + 2 retained old seedance
clips (16, 19).**

### Old clips kept over a worse reshoot

| # | Old clip retained | Why kept over the reshoot |
|---|---|---|
| 16 | `output/videos/019f905c-83e5-7961-a046-55929a40b64a.mp4` | Reshoot doubled the glass outline (structural warble). Old clip is a clean defect-free near-still; it lacks the wanted vertical rise, so a retake is offered — but never ship the doubling take. |
| 19 | `output/videos/019f9018-d1cd-7c72-aca3-715513c1e045.mp4` | Reshoot swept a big solid-blue second hand into frame. Old clip cleanly releases the stone and lifts clear — the intended gesture, defect-free. Retake optional. |

### Consolidated retake quote — NOT submitted, awaiting Isaac

Two failures. Both re-quote as kling-pro 5s image-to-video from the same locked
`sourceUrl`, with tightened prompts that forbid the specific defect. Estimated
live 2026-07-23; each returned `usd 0.35`, token present.

| Line | Model | Unit | Qty | Total |
|---|---|---:|---:|---:|
| Shot 16 — rise, forbid glass doubling ("only one glass, outline never doubles/splits/ghosts; nothing inside moves") | kling-pro 5s | $0.35 | 1 | $0.35 |
| Shot 19 — release, forbid second hand ("both hands lift straight up and out; no hand sweeps back in, no new hand or blue shape enters") | kling-pro 5s | $0.35 | 1 | $0.35 |
| **Retake batch total** | | | **2** | **$0.70** |

Fits the $6.87 headroom under the $30 ceiling (would take the film to $23.83).
**Not submitted; held for Isaac's explicit yes.** Note: shot 19's retained old
clip is fully usable, so its retake is optional; shot 16's retake is the one
that actually buys the missing vertical motion. If only 16 is approved, the
batch is $0.35.

### Stillness map — unchanged after reshoot

The stillness register above stands. Near-still / locked shots that barely move
by design and passed as such: 3 (near-locked), 11 (locked spine), 20 (delicate
hairline drift), 21 (near-still balance), 23 (locked ring, held), 25 (near-still
pool), 28 (locked spine, matches 11), plus the retained old near-stills 16 and
19. Well over the fifth the film wants, clustered on the 11/28 spine, Act V's
turn, and Act VII's close. The reshoot added deliberate gentle motion to 29 and
30 (formerly locked) per Isaac's less-dull mandate, but both still read calm.

### Cut warnings — carried forward and updated

The planning-table fill guidance (shots 1, 12, 13, 18, 19, 20, 21, 22) still
stands: every clip is 5s or 10s and the Editor ramps/holds to the slot. Updates
from this gate:

| # | Finding | Usable in/out | Guidance |
|---|---|---|---|
| 11 | Kling clip is near-locked but carries a faint drift; spine must match 28. | freeze a single frame | Freeze-hold frame 0 (the keyframe) so the 11/28 spine stays matched. |
| 28 | Same near-locked faint drift as 11 (spine pair). | freeze a single frame | Freeze-hold frame 0 to match 11 exactly. |
| 16 | Retained OLD seedance near-still (reshoot rejected for glass doubling). | full 0.0–5.0s | Clean but near-still; no vertical rise. If the $0.35 retake is approved and passes, swap in the kling rise. |
| 19 | Retained OLD seedance clip (reshoot rejected for invented blue hand). | release ~0.0–2.5s, hold | Release plays early; freeze-hold the settled stone to fill the 14.70s slot. |
| 1, 12, 13 | Native 10s / 9s slots now shot at 10s (1 is a 9.0s slot filled by a 10s clip). | full | Shots 12, 13 fill their 10s/9s slots natively; shot 1's 10s clip covers the 9.0s slot with headroom. |

### Vertical notes — unchanged

The per-shot 9:16 table above stands; the accents were composed to the centre
column at the keyframe stage and the kling moves hold the subject central.
Strongest social-edition openers remain the front-loaded movers: 12, 24, 22,
13, 10 — and 1 now has a real sustained push that reads at phone size. Shot 21
still cannot survive a centre crop (two-object comparison, AD flag). Retained
old clips 16 and 19 keep their accents centred and survive the crop; both are
near-still, so neither opens.
