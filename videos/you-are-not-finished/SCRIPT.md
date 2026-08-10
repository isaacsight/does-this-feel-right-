# You Are Not Finished — script

The locked narration is [`script.txt`](script.txt). That file is the single
source of truth: the frame book, the VO recording and the short-form caption
cards all derive from it, and none of them re-word it. This document records
the act boundaries and the voice gate.

## Acts

| # | Act | Opens on | Target |
|---|---|---|---|
| 1 | The receipt | "Think of who you were ten years ago." | 0:00–1:10 |
| 2 | The finding | "In 2013, three researchers put the question…" | 1:10–2:30 |
| 3 | Why it happens | "So why would the same mistake turn up at every age?" | 2:30–3:30 |
| 4 | The objection | "Now the part that most retellings leave out…" | 3:30–4:30 |
| 5 | What it costs | "The researchers went further, and put a price on that gap." | 4:30–5:10 |
| 6 | Close | "So here is the part you can use." | 5:10–5:30 |

Names are deliberately not spoken. "Three researchers" is what the ear gets;
Quoidbach, Gilbert and Wilson go on a card at assembly. Spoken proper nouns
are the single most common thing an ear loses, and the citation reads better
than it says.

## Voice gate — 2026-07-30

Measured with `tools/video/register-profile.py` against the target in
[`BRIEF.md`](BRIEF.md), which was derived from 1001 School of Life transcripts
(963,514 words) and the *Why Humans Need Rituals* script.

```
=== FINAL
  files     1   words       833   vocabulary     325
  VOCABULARY
    syllables/word          1.35
    3+ syllable words        7.6%
    "you" per 1k words      52.8
    "we" per 1k words        0.0
  SENTENCE
    words/sentence          14.6
    Flesch reading ease     77.4
    Flesch-Kincaid grade     6.1
```

| Metric | Gate | Result | |
|---|---|---|---|
| Syllables per word | ≤1.52 | 1.35 | PASS |
| 3+ syllable words | ≤13% | 7.6% | PASS |
| Words per sentence | 14–18 | 14.6 | PASS |
| Flesch reading ease | ≥62 | 77.4 | PASS |
| "you" per 1,000 words | 10–14 | 52.8 | **OVER — see below** |

Runtime: 825 words, 5:30 at 150 wpm. Inside the 5:15–5:45 criterion.

### On the "you" ceiling

The 10–14 band was taken from the average across 1001 School of Life videos.
That corpus includes essays on architecture, Adam Smith and Samuel Beckett,
where direct address is naturally rare, so the average is not a ceiling that
governs a film whose subject *is* the viewer's own future self.

The defect this gate was written to prevent was **zero** — the rituals script
said "you" not once in 1,043 words. That is fixed.

Recommendation: amend the gate to a floor (**≥10 per 1,000, no ceiling**) and
record the actual figure per film rather than constraining it. Pending Isaac's
decision.

### Revision history

Two passes were needed, and both misses are worth recording.

**Draft 1** came in at 9.9 words/sentence and 85.5 reading ease (grade 3.8) —
an overcorrection. Having learned that the last film failed by being short and
abstract, the first draft went short and plain, which is simpler than the
reference corpus and read thin. It had also sanded off the dry formal irony
that is the house voice's best quality.

**Draft 2 and 3** merged short sentences and put the wit back ("all the same
opinions professionally upholstered", "the obviousness arranged itself
backwards", "with enormous confidence, that nothing much is coming"), moving
words/sentence 9.9 → 13.6 → 14.6 while vocabulary stayed well inside gate.

The rule that produced the fix: **spend polysyllables on jokes and nowhere
else.** Formal diction is a comic instrument; it is only a defect in
explanatory connective tissue.
