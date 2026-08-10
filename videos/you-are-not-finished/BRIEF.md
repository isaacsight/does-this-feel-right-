# You Are Not Finished — design

> kernel.chat film on the end-of-history illusion. Target runtime ~5:30.
> Written 2026-07-30, immediately after shipping *Why Humans Need Rituals*
> and auditing what was wrong with it.

## Why this film, and why now

The last film's post-mortem produced two measured defects and one editorial
one. This film exists partly to not repeat them, so the design carries the
fixes as gates rather than intentions.

**Measured against the reference corpus.** Profiling 1001 School of Life
transcripts (963,514 words) against the rituals script (1,043 words) with
`tools/video/register-profile.py`:

| Metric | Reference corpus | Rituals | Target here |
|---|---|---|---|
| Syllables per word | 1.49 | 1.66 | **≤1.52** |
| 3+ syllable words | 12.5% | 17.6% | **≤13%** |
| "you" per 1,000 words | 13.8 | **0.0** | **≥10, no ceiling** |
| "we" per 1,000 words | 38.8 | 24.0 | 25–40 |
| Words per sentence | 17.3 | 12.3 | ~16 |
| Flesch reading ease | 62.2 | 54.1 | **≥62** |

The zero is the headline. In 1,043 words of narration the rituals film never
once said "you". It spoke *about* people in an abstract "we" while the
reference speaks *to* the person watching. That is the most plausible
explanation on the table for the "I got lost watching it" failure recorded in
`docs/video/PRODUCTION-PLAYBOOK.md` §10.1 — not pacing, not images, but that
nobody in the room was addressed.

Note the counterintuitive pair: reference sentences are ~40% *longer* than
ours and read *easier*. Short sentences packed with abstract polysyllables are
harder to follow than long sentences of plain words. The last film optimised
the wrong variable.

Type/token ratio was also computed (0.487 vs 0.029) and is **discarded** — that
is a corpus-size artifact, not a difference in lexical variety.

## Spine

At every age you can see clearly how much you have changed, and you cannot see
that you will keep changing. The error is not about your past. It is a failure
to imagine a future self — and part of the famous finding may be a statistical
artifact, which this film says out loud.

## Source material

Quoidbach, J., Gilbert, D. T., & Wilson, T. D. (2013). "The End of History
Illusion." *Science*, 339(6115), 96–98. Published 4 January 2013.

- Over **19,000 participants**, ages **18 to 68**
- Six investigations across personality traits, core values, and preferences
- At every age, participants reported large past change and predicted small
  future change
- Willingness-to-pay follow-up: **$129** to see today's favourite band play in
  ten years, versus **$80** to see the band they loved ten years ago play today

**Live objections, all of which the film carries in Act 4:**

1. Cross-sectional, not longitudinal — it compares different people of
   different ages rather than following the same people over time
2. It leans on autobiographical memory, which is unreliable
3. The statistical objection: if you know you will change but cannot predict
   the *direction*, then predicting "no change" is the rational answer. Under
   this reading part of the illusion is an artifact of the measure

Objection 3 is the strongest and is treated as the film's turn, not as a
footnote. A film that presents the famous finding *and* the argument against it
is doing what kernel.chat claims to do.

## Acts

| # | Act | Time | Job |
|---|---|---|---|
| 1 | The receipt | 0:00–1:10 | You have changed — proven from the viewer's own life. Hook by 3s: remembering who you were is easy, picturing who you'll be is blurry. |
| 2 | The finding | 1:10–2:30 | 19,000 people, 18 to 68. Same pattern at every age. Everyone believes they just arrived. |
| 3 | Why it happens | 2:30–3:30 | Remembering is retrieval; predicting is construction. The blank comes back as "nothing will change" rather than "I can't see it." |
| 4 | The objection | 3:30–4:30 | Cross-sectional. Memory. The maths. Then: what survives. |
| 5 | What it costs | 4:30–5:10 | $129 vs $80. We buy permanence for a person who will not be there. |
| 6 | Close | 5:10–5:30 | You are not finished. |

Every act is written in second person. This is a structural requirement, not a
stylistic preference — it is the fix for the measured defect above.

## Build pipeline

| Stage | Where | Note |
|---|---|---|
| Script | Here | Measured against the voice spec before anything else happens |
| Frame book | Here | One gag per beat with a consequence, tagged to its narration line |
| Images | **Gemini, browser** | Free on the Pro account. Generation from a locked reference is the case it handles well |
| Narration | **ElevenLabs, browser** | Driving the UI directly means `speed` can actually be set — the local proxy does not forward it, and every voice otherwise runs 166–186 wpm |
| Assembly | HyperFrames | `build-literal-final.mjs` pattern, as the last film |
| Shorts | `tools/shorts/` | `build-segments.py` then `cut-verticals.py`, both fixed 2026-07-30 |

## Gates

Each gate exists because something specific went wrong before. None are
optional.

1. **Voice gate.** The script does not go to boards until
   `register-profile.py` reports it inside spec. Cheapest possible place to
   catch the defect that sank two previous builds.
2. **Character gate.** A reference sheet is generated and approved *before*
   batch one, and every batch is checked against it. The rituals companion
   drifted mid-film and 2026-07-30 proved there is no cheap repair —
   generative editors regenerate rather than patch, and return 1024px.
   See PRODUCTION-PLAYBOOK §10.8.
3. **Frame-geometry gate.** One geometry decided up front, then audited every
   batch with `magick "$f" -fuzz 4% -format "%@" info:` before assembly. The
   rituals film shipped with three different frame widths because nobody
   measured until the master existed. See PRODUCTION-PLAYBOOK §10.7.
4. **Contact-sheet gate.** Midpoint frame of every cut, reviewed in one pass —
   and it is stated every time that this cannot catch anything existing only
   in motion.

## Success criteria

- Runtime 5:15–5:45
- 1920×1080 throughout, downscaled from ~2752px sources; nothing upscaled
- All six voice metrics inside spec, verified and recorded
- One character reference, zero drift across all frames
- One frame geometry, zero variance measured across all frames
- Act 4 present and unhedged — the objection is stated plainly, not buried
- Three verticals cut from the same locked script

## Out of scope

- Re-cutting or re-scoring *Why Humans Need Rituals*
- Any repair of its companion-design inconsistency
- The unfinished delivery kit for that film (README, YouTube metadata,
  thumbnails) — tracked separately

## Open questions

None blocking. The willingness-to-pay figures were verified 2026-07-30 before
being written into this spec.
