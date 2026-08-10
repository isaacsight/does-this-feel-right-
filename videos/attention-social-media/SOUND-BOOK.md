# SOUND BOOK — The Price of a Glance

> **Pass one COMPLETE, filed 2026-07-24. TREATMENT revision five (the
> Zenn-voice rework) is canonical.** Every line of VO changed, so any prior
> pre-Zenn measured table is void. This file is the final pass-one record for
> the locked script.
>
> **STATUS: FINAL for this script. All seven acts recorded and measured.** The
> four acts refused at the credit wall on 2026-07-23 (III, IV, V, VII) recorded
> cleanly on 2026-07-24 after the ElevenLabs plan was topped up (Creator tier,
> 148,500 characters). The Act II pronunciation defect was retaken with the
> "Day-an" respelling and is fixed. Acts I and VI were left untouched — they were
> already clean and their stems exist. **Measured film total: 271.91 s = 4:31.91
> spoken.**

| | |
|---|---|
| Pass | One — the voice (re-record) |
| Status | **FINAL — 7 of 7 acts recorded, measured, transcript-verified** |
| Cast | **Eric** — `cjVigY5qzO86Huf0OWal`, `elevenlabs-v2` direct (`eleven_multilingual_v2`) |
| Settings | stability 0.35 · style 0.0 · similarity 0.75 (tuned server defaults, no override used) |
| Measured total | **271.91 s = 4:31.91** spoken (all seven acts) |
| Spend | $0.00 fal · ElevenLabs subscription credits (Creator tier) · fal cap untouched |

---

## Voice — unchanged, and why it fits the Zenn register

**Eric, `cjVigY5qzO86Huf0OWal`, `elevenlabs-v2` direct.** Cast by Isaac on ear
in the prior pass. The revision-five Register asks for a plain, second-person,
dry read — a person levelling with one listener, allowed to say "I." Eric was
recorded at the tuned defaults (stability 0.35 / style 0.0 / similarity 0.75);
no per-request `voiceSettings` override was needed on any of the three acts that
recorded — all three read conversational, not announced. The lower stability at
style 0.0 gives the natural, slightly loose delivery the new voice wants.

---

## Narration stems — all seven recorded, measured, verified (FINAL)

Recorded as seven separate act blocks. Character counts are exact from the live
estimate. Measured durations are `ffprobe` container durations to two decimals.
**This measured table is the spine the 30-scene build times to; the treatment's
~160 wpm projections are obsolete.**

| Act | Chars | File — `output/audio/` | **Measured** | wpm | State |
|---|---:|---|---:|---:|---|
| I — The arithmetic | 437 | `bc779096-3eb6-497d-b64b-34e136ab57b4.mp3` | **27.63 s** | 162.9 | done, clean (untouched) |
| II — What dopamine does (retake) | 476 | `a4fd77a9-6e35-4a7a-ae34-14e96e49ec22.mp3` | **30.19 s** | — | done, clean — **"Day-an" fixed** |
| III — The playbook | 763 | `3dfca594-5a08-4d25-9aaf-2784f1f80a6c.mp3` | **50.90 s** | — | done, clean |
| IV — The cost, measured | 508 | `6665a6a0-9884-45bb-913b-67f4b7e7ecbd.mp3` | **35.34 s** | — | done, clean — **self-reference target** |
| V — The honest number | 1,163 | `1b325541-8b39-4211-a274-98a7c624be50.mp3` | **77.65 s** | — | done, clean — all figures verified |
| VI — The tribe at scale | 324 | `99212a7a-15f3-41b6-a352-31486c401cd1.mp3` | **20.57 s** | 166.3 | done, clean (untouched) |
| VII — The close | 451 | `067cafd6-4ef5-4840-a7ce-0b283a230f23.mp3` | **29.63 s** | — | done, clean |

**Measured film total: 27.63 + 30.19 + 50.90 + 35.34 + 77.65 + 20.57 + 29.63 =
271.91 s = 4:31.91 spoken.** Finished runtime will be longer once the Editor
adds act-boundary breaths; this is the spoken floor.

**The Act II retake (`a4fd77a9`) replaces the superseded Act II stem
(`06a7318c`, 30.88 s, the "Dion" defect).** The superseded take is retained on
disk per the append-only rule but must not be used in the film.

The five newly recorded stems (II-retake, III, IV, V, VII) are all fresh
2026-07-24 generations; Acts I and VI are the clean 2026-07-23 stems, unchanged.

---

## Act IV self-reference — RESOLVED

Act V's line **"I just spent thirty-five seconds on that"** is a checkable
self-reference to the length of the passage that precedes it — the Act IV run,
the Ward "brain drain" study the turn then dismantles.

- **Measured Act IV = 35.34 s.**
- The treatment's rule: keep "thirty-five" if Act IV lands at 33–37 s; round
  *against* the film (understate) only if it runs longer.
- **35.34 s is squarely inside the 33–37 s band. "Thirty-five seconds" is
  honest and stands. No change to the spoken number.**

A viewer with a stopwatch measuring from the top of Act IV to the "I just spent
thirty-five seconds on that" line will read ~35 s. The one line in the film a
viewer can check is true. **Director: reconciliation closed — the spoken number
holds; no VO change required.**

---

## Pronunciation notes — all seven acts (FINAL)

**Method.** I cannot listen. Each block was transcribed locally
(`whisper-cli`, `ggml-small.en`) and diffed against the locked VO. Confidence is
graded rather than asserted. Years and big numbers were confirmed present and
correctly read.

### Act I — clean (untouched)
"In 1971" reads as "nineteen seventy-one"; "Fifty-five years later" clean;
"Herbert Simon" clean.

### Act II retake — DEFECT FIXED
The naming sentence now transcribes as *"three scientists, Schulz, Day-Ann, and
Montague."*

| Token | Submitted grapheme | Heard as | Verdict |
|---|---|---|---|
| Schultz | Schultz | "Schulz" | Correct — same sound (SHOOLTS); ASR spelling only |
| Dayan | **Day-an** (respelled) | **"Day-Ann"** | **FIXED** — reads as two syllables DAY-an; the prior "Dion/Dyan" misread is gone |
| Montague | Montague | "Montague" | Correct |
| "1997" | 1997 | "1997" | Correct — "nineteen ninety-seven" |

The closing line **"It's built to keep you guessing"** is present and complete.
The submitted string respells "Dayan" as "Day-an" **only**; reversing that one
token reproduces the locked script exactly. The displayed/locked script keeps
"Dayan". No other change.

### Act III — clean
- **Ferster** → "Furster" — the correct sound (FUR-ster); ASR spelling only.
- **Skinner** clean. "1957" and "2017" read correctly. "Facebook's founders" clean.

### Act IV — clean
- **Sophie Leroy** clean. **Adrian Ward** clean. "2009" and "2017" correct.
- "attention residue" transcribes as "a-tension residue" — an ASR word-boundary
  artifact, not a mispronunciation. Minor note: "Not in outrage" transcribes as
  "Not an outrage" — unstressed "in"/"an" are near-homophones to the ASR; this
  is not a name or number and reads correctly either way. No retake.

### Act V — clean, all load-bearing figures verified
- **Amy Orben** → "Orban" — same sound (OR-ben); ASR spelling only.
- **Andrew Przybylski** → transcribed exactly — the hardest name in the film
  reads right.
- **355,000** ✓ · **"four tenths of one percent"** (= 0.4%) ✓ · **"600 million"**
  (six hundred million) ✓ · "twenty-two studies" ✓ · "a seventh of a standard
  deviation" ✓ · **"35 seconds"** ✓. "2019" and "2022" correct.
- Ruiz Pardo (2022 replication) and Böttger (2023 meta-analysis) are **not named
  in the spoken VO** — the VO says "someone ran it again" and "a review pooled
  twenty-two" — so there is no surname to mispronounce. Citation-table only.

### Act VI — clean (untouched)
"Leon Festinger, 1954" reads correctly ("nineteen fifty-four").

### Act VII — clean
No proper nouns. "out-willpower" reads as intended; "the filings" clean.

**Every high-risk name and number on the watch list is confirmed clean. No new
mispronunciation surfaced. No further retake required.**

---

## The credit blocker — RESOLVED 2026-07-24

On 2026-07-23 Acts III, IV, V, VII refused with ElevenLabs `401 quota_exceeded`
(0 of the 10,000-credit cycle remaining); the batch was stopped rather than
falling back to the fal-routed `elevenlabs-turbo` default, which would have
spent fal dollars on the worse model against the approved route.

Isaac topped the plan up to **Creator tier (148,500 characters, 0 used,
verified)**. On 2026-07-24 the four refused acts plus the Act II retake — one
$0-fal batch, **3,361 characters**, `elevenlabs-v2` direct, Eric, tuned defaults
— recorded cleanly. Each was re-estimated for a fresh quote token immediately
before submit (all `usd 0`, subscription credits) and submitted via the
documented HTTP proxy with `--data-binary` (not `-d @-`, which strips newlines
and breaks the quote hash). All five polled to terminal `done`. The blocker is
closed; pass one is complete.

---

## Handoff — pass one COMPLETE

**Art Director: build to this measured spine.** All seven acts are final:
I 27.63 · II 30.19 · III 50.90 · IV 35.34 · V 77.65 · VI 20.57 · VII 29.63 s,
**film total 271.91 s = 4:31.91** spoken. Every shot slot resets against these
numbers, not the treatment's ~160 wpm projections. Note the Act II duration is
the **retake** (30.19 s), not the superseded 30.88 s take.

**Director: the "thirty-five seconds" reconciliation is closed.** Measured
Act IV = 35.34 s, inside the 33–37 s band, so the spoken "thirty-five seconds"
is honest and stands. No VO change required.

**Everyone: pass one is closed.** Seven clean stems, all names and numbers
transcript-verified, "Day-an" fixed.

---

## Pass two (score and design) — carried over, mapping now provisional

*A later pass, out of scope for this re-record; recorded here only so the assets
are not lost. The prior pass-two boundary/shot mappings were built against the
VOID old assembly and the object-based shot list. They must be re-mapped once
the re-record completes and the Art Director's character-driven
FRAME-BOOK/SHOT-BOOK exist.*

**Design cues (done, $0 fal, real assets — placement to be re-mapped):**

| Cue | Measured | Path (`output/audio/`) |
|---|---:|---|
| Rain marks | 4.00 s | `3b6690f6-39db-44ba-bf1f-2d0cf45a2be5.mp3` |
| Water bloom | 3.00 s | `a3d11829-dde0-4502-a82e-3748f504d406.mp3` |
| Settling | 3.00 s | `122b5360-2ef4-4715-9c41-eb2ad0f16acc.mp3` |
| Paper edge | 3.00 s | `7e20ef4a-eba3-4430-9bbb-19e15ffaa0d5.mp3` |

**Room tone (done, $0 fal):** 22.00 s, mean −60.1 dB —
`output/audio/053db547-4dae-4c00-a9f1-4168f661e0db.mp3`. Loop full-length under
the film at a very low level; it is the texture the quiet passages are made of.

**Score:** BLOCKED — the `elevenlabs-music-direct` route returns
`402 paid_plan_required` (Music API gated on the free plan). No beds exist,
nothing spent. Same root cause as the voice blocker: the ElevenLabs plan.
Resolving the plan unblocks both.

**Mix guidance (deferred):** the load-bearing items — Act V ducking, the
room-tone-only air around Act V's closing line, the retraction-beat silence, and
the Act IV length constraint — cannot be given real timecodes until the back
half records. They carry over in principle and will be re-addressed with measured
boundaries.

---

## Nothing is pre-mixed

The seven narration stems are separate, unnormalised, unprocessed act blocks.
Design cues and room tone are separate stems. The Editor balances against
picture; no stem was pre-mixed.
