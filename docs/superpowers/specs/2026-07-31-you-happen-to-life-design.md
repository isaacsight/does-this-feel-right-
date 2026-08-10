# You Happen to Life — design

> kernel.chat film on locus of control and the limits of the agency
> argument. Target runtime ~7:00, seven acts, stills.
> Written 2026-07-31, after shipping *You Are Not Finished* and validating
> its register as the house voice.

## Why this film, and why now

The previous two films took a published finding and then said the part most
retellings skip. This one **inverts that structure**: the assertion comes from
a podcast, and the correction comes from the literature.

The source is Jett Franzen's "Why Almost Nobody Gets The Life They Want" —
25,673 words, the largest transcript in the Modern Wisdom corpus. Word-frequency
analysis of it returns *people, you're, going, that's, thing, because, doing,
something*: pure conversational filler, no technical vocabulary, no named
constructs, no studies. There are ten sponsor reads across sixty minutes.

**As evidence it is empty, and that is not a problem, because it is not the
evidence. It is the position being examined.** The film never cites the
interview. It examines a belief the interview states unusually plainly, and
which is held far more widely than by one guest.

The argument being examined, in his own words: *"I happen to life, life
doesn't happen to me."* Around it sit two more claims — that the difference
between people who make it and people who don't is sustained dedication, and
that most people are not disadvantaged but simply mid-bell-curve.

## Spine

The belief that you are steering your own life is real, measurable, and sixty
years old. It predicts good things. It is also partly a **consequence** of how
much control you actually had — which is where the advice built on it turns
cruel.

## Sources, verified

Every number below was traced to the published work before it was written
into an act. Nothing in this film is sourced to the podcast.

**Rotter, J. B. (1966).** "Generalized expectancies for internal versus
external control of reinforcement." *Psychological Monographs*, 80(1), 1–28.
The Internal–External Locus of Control Scale.

- **Internal:** outcomes follow from your own effort, skill, ability.
- **External:** outcomes follow from luck, fate, chance, or powerful others.
- The construct measures **perception, not circumstance**. Two people under
  identical constraints can diverge sharply in how much agency they feel.
  This is the property the whole film turns on.

**Macnamara, B. N., Hambrick, D. Z., & Oswald, F. L. (2014).** "Deliberate
practice and performance in music, games, sports, education, and professions:
a meta-analysis." *Psychological Science*, 25(8), 1608–1618.

Variance in performance explained by deliberate practice:

| Domain | Variance explained |
|---|---|
| Games | 26% |
| Music | 21% |
| Sports | 18% |
| Education | 4% |
| Professions | **less than 1%** |

The shape of this table *is* Act 4. The practice claim is strongest at chess
and weakest at the thing most viewers actually do for a living.

**The poverty-attribution literature.** Individualistic explanations of
poverty track with internal locus of control; structural explanations track
with chance locus. How you explain a stranger's outcome and how you explain
your own turn out to be readings from the same instrument. This is the
evidential basis for Act 6 and it is the reason Act 6 exists.

## The honesty gate

Act 6 is the act this film is for, and it is the one that can go wrong.

**Argue with the claim, never the man.** He is making a widely held argument,
not an unusual one. The film is better and fairer if it treats the belief as
the room's, not one guest's. **No name, no clip, no photograph, no
impression.** The line in Act 1 is delivered as something you have heard,
because you have.

**Do not overclaim the correlation.** That internal locus correlates with
actual control does not mean agency beliefs are worthless or purely
downstream. Act 7 has to leave something real standing, or the film is just
the mirror-image of the thing it is criticising.

## Acts

| # | Act | The move |
|---|---|---|
| 1 | The claim | Someone says it plainly: *I happen to life. Life doesn't happen to me.* You recognise it — it is the whole self-improvement register. |
| 2 | It is a real thing | Rotter, 1966. It has a name and a scale, and internals do better on a lot of measures. |
| 3 | And the practice claim | "The difference is dedication." Also testable. |
| 4 | **The numbers** | 26% games. 21% music. 18% sports. 4% education. **Under 1% in professions.** Strongest at chess, weakest at your job. |
| 5 | **Which way does it point** | Internal locus correlates with actual control. Feeling like an author is partly a *report* on your circumstances, not only a cause of them. |
| 6 | Where it turns cruel | The same instrument that predicts your confidence predicts how you explain a stranger's poverty. Told to someone without power, "take more agency" is a diagnosis dressed as encouragement. |
| 7 | What survives | Something smaller, and still worth having. |

## Voice

Targets from `reference_film_voice_spec`, validated on *You Are Not Finished*:

| Metric | Target |
|---|---|
| Flesch reading ease | ≥72 |
| Grade level | 6–7 |
| Syllables per word | ≤1.42 |
| 3+ syllable words | ≤10% |
| Words per sentence | 14–17 |
| "you" per 1,000 | 40–55 |
| "we" per 1,000 | **10–20** |

The "we" band is the new dial and it is not cosmetic. *You Are Not Finished*
scored **0.0 on "we"** across 1,161 words. Seven minutes of unbroken second
person reads as diagnosis from outside — survivable there, fatal here. A film
that spends seven minutes telling *you* that you are wrong about agency
becomes the very thing it is criticising. The confession beats are what earn
Act 6.

**Gate before boarding.** `tools/video/register-profile.py` runs on the draft
until it passes. No frame is generated against an ungated script.

## Production

**Stills**, same fal pipeline as the last film, ~$8 of frames. WaveSpeed
nano-banana-2 was bench-tested on frame 23b and rejected for this film: 2.7×
the cost, 2.2× slower, and — decisively — visibly weaker reference
conditioning, drawing an anatomical ribcage where our style is flat and
diagrammatic. On a 100-plus-frame film, matching the sheet is the entire job.
The key and `tools/video/wavespeed-test.mjs` are retained; switching later is
a small change. WaveSpeed's Veo endpoint remains the choice for motion, where
there is no sheet to match.

Three changes bought by the School of Life shorts study:

1. **Assembly-level motion** on each still — slow scale and drift, applied in
   the composition, not generated.
2. **A colour field that shifts per beat** rather than one palette across the
   film.
3. **Shorts cut to 55–59s**, not the 40–51s of the last set.

**Carry the three playbook rules** (`docs/video/PRODUCTION-PLAYBOOK.md`
§10.7–10.9): audit the frame edge with `magick %@` before assembly; never
plan a post-hoc generative patch; lock the character reference up front,
remembering that a reference image is a prior on everything it contains —
its cast, its captions, its layout.

## Risks

**The subject is close to the channel's own register.** kernel.chat publishes
into the same self-improvement adjacency this film complicates. That is an
argument for making it, not against, but Act 7 has to be written as
something the channel itself is willing to live under.

**Act 4's table is the whole film's load-bearing evidence.** If the
Macnamara figures are misread, the film collapses. They are meta-analytic
variance-explained figures, not effect sizes and not claims that practice is
useless — the script must say what they are, in plain words, without
inflating them.

**Locus of control has a large and mixed literature.** The film should not
imply the 1966 scale is uncontested or that the construct has stood still for
sixty years. Say "measured", not "proven".
