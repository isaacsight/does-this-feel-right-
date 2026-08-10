# You Happen to Life — script and voice gate record

Locked 2026-07-31. Narration lives in `script.txt` (1,198 words, ~7:00 at the
house pace). Spec: `docs/superpowers/specs/2026-07-31-you-happen-to-life-design.md`.

## Gate result

Run: `python3 tools/video/register-profile.py "film" "videos/you-happen-to-life/script.txt"`

| Metric | Target | Draft 1 | Draft 2 | **Locked** |
|---|---|---|---|---|
| Flesch reading ease | ≥72 | 89.7 | 81.4 | **78.8** |
| Flesch-Kincaid grade | 6–7 | 2.8 ✗ | 5.6 ✗ | **6.5** |
| Syllables per word | ≤1.42 | 1.28 | 1.30 | **1.31** |
| 3+ syllable words | ≤10% | 4.3% | 5.3% | **5.7%** |
| Words per sentence | 14–17 | 8.4 ✗ | 14.9 | **16.9** |
| "you" per 1,000 | 40–55 | 40.8 | 35.8 ✗ | **41.7** |
| "we" per 1,000 | 10–20 | 4.4 ✗ | 11.4 | **10.9** |

**What draft 1 got wrong is worth keeping on record.** It over-corrected into
staccato: plain words *and* short sentences, which is the opposite of the
lesson the last film taught. Words per sentence came in at 8.4 against a 14–17
band and the grade level fell to 2.8 — the script read as a list of slogans,
which is precisely the register this film is criticising. Four one-line
sentences of percentages in Act 4 were the single largest cost; merging them
into one sentence moved words-per-sentence by more than a full point.

Solving Flesch backwards is what made draft 3 converge in one pass. At
~16 words per sentence, ease ≥72 requires `84.6 × syllables-per-word ≤ 119`,
so syllables per word must stay under 1.41 — roughly one polysyllable per
eight words. Grade level then has only two levers, sentence length and
syllable density, and both were already near their ceilings, so the last fix
had to add second person by **substitution rather than addition**.

## Acts, and where they sit in the narration

| # | Act | Opens at | The move |
|---|---|---|---|
| 1 | The claim | "There is a line you have heard before" | You recognise the sentence. It sounds brave. |
| 2 | It is a real thing | "In 1966 a man named Julian Rotter" | Rotter's scale. Internals do better on a lot of measures. |
| 3 | And the practice claim | "The same room makes a second claim" | "The difference is dedication." Also testable. |
| 4 | The numbers | "In 2014 three researchers" | 26 / 21 / 18 / 4 / under 1. Strongest at chess, weakest at your job. |
| 5 | Which way does it point | "So we have a belief that feels true" | Feeling in control tracks with being in control. Cause, or report? |
| 6 | Where it turns cruel | "And here is where it stops being interesting" | One dial. It also sets how you explain a stranger. |
| 7 | What survives | "So what is left for us." | One small engine, honest work, conditions we did not pick. |

## Rules this script is holding

**No name, no clip, no photograph.** Act 1 delivers the line as something you
have heard, because you have. The film argues with a widely held belief, not
with the man who happened to state it plainly on a podcast. The word "podcast"
appears once, as one of three places the line might reach you.

**"We" is reserved for confession.** It appears at the five places the film
admits the failure is shared — "so have I", "none of us wants that number to
be true", "we should not pretend otherwise", "we have all been on the wrong
side of it", "conditions we did not pick" — and at the close. Everything
explanatory stays in "you". Per `reference_film_voice_spec`: **"you" accuses,
"we" confesses.**

**Act 4 says what the numbers are.** They are meta-analytic variance-explained
figures. The script states plainly that this is not a claim practice is
useless, immediately after the table, because the table is the film's
load-bearing evidence and the misreading is the obvious one.

**Act 7 leaves something standing.** "Inside the room you already have, acting
like the author of your day beats acting like a passenger in it." Without that,
the film is only the mirror image of the thing it criticises.
