# The voice — measured, not remembered

The narrator is one voice forever (`galley-sound`, ratified 2026-08-03). This
document is about the *writing* that voice reads: the register, measured
against real corpora, and enforced by a gate rather than by memory.

Run before boarding, every time:

```
python3 tools/video/register-profile.py --gate videos/<film>/script.txt
```

Non-zero exit means the script is out of band. **Fix the script, not the band.**

---

## Where we actually sit

Measured 2026-08-04 against 997 School of Life transcripts (963,514 words),
10 Modern Wisdom transcripts (89,279 words), and our own three films.

| | you /1k | we /1k | syll/word | words/sent | Flesch | FK grade |
|---|---:|---:|---:|---:|---:|---:|
| School of Life | 13.8 | **38.8** | 1.49 | 17.3 | 62.2 | 8.9 |
| Modern Wisdom | 34.7 | 11.2 | 1.39 | 14.0 | 74.9 | 6.3 |
| **kernel.chat** | **49.2** | 7.9 | 1.33 | 15.7 | 78.7 | 6.2 |

Two things fall out, and both are worth stating plainly.

**We are not School of Life, and should stop half-imitating them.** They
*confess* — "we" outnumbers "you" nearly three to one — in longer, denser,
grade-8.9 sentences. We *address* — "you" outnumbers "we" six to one — in
plainer, grade-6.2 sentences. That is a different publication, not a worse one.
Our register is built for the ear (a film is heard once, in order, with no
scrollback), and grade 6.2 at Flesch 78.7 is the right target for that. The
corpus is a reference point, not a destination.

**But the ratio has drifted too far, and one film proves it.**

| film | you /1k | we /1k |
|---|---:|---:|
| you-watched-it-happen | 40.8 | 12.5 |
| you-happen-to-life | 41.7 | 10.9 |
| **you-are-not-finished** | **65.5** | **0.0** |

`you-are-not-finished` says "you" 65 times per thousand words and "we" **not
once**. That is the over-correction from the opposite failure: the rituals
script said "you" *zero* times in 1,043 words, which is the likeliest cause of
two "I got lost watching it" rejections. We fixed a floor by removing a ceiling.

**"You" accuses. "We" confesses.** A film that only accuses is a lecture, and
this publication's whole method is the honest beat — the place where the easy
version of the argument overstates itself and the film says so. That beat cannot
be written without "we". The two films with "we" around 11–12 are the two whose
narration was judged good.

---

## The house band

Centred on the two good films, not on either corpus.

| metric | band | why the edge exists |
|---|---|---|
| `you_per_1k` | **35 – 58** | floor: the rituals failure. ceiling: relentless accusation |
| `we_per_1k` | **8 – 22** | floor: a film with no "we" is a lecture. ceiling: the argument goes soft |
| `syllables_word` | 1.26 – 1.42 | written for the ear |
| `words_sentence` | 13 – 19 | long enough to think in, short enough to hear |
| `flesch_ease` | 72 – 84 | plain, not simple |
| `fk_grade` | 5.6 – 7.2 | accessible without condescending |

The band measures *density*, not placement. Passing it is necessary and not
sufficient — the Director still owns whether the "we" lands where the film is
being honest, or is sprinkled to clear a number. A gate can count words; it
cannot tell whether the confession is real.

---

## What varies per film, and what does not

- **The voice** — one narrator, forever, unnamed. Spine.
- **The register band** — fixed. This document.
- **The delivery** — varies per film: pace, temperature, where the read goes
  quiet, set by the Director's register line and executed by Sound.
- **The stance inside the band** — a film may sit at 38 "you" or 55 "you" and
  both are in register. Choose it deliberately per film and write it in the
  treatment.

## The corpora

`transcripts/the-school-of-life/` — 1,001 files, `transcripts/modern-wisdom/`
— 10 files. Keep them. They are how any future claim about our register gets
checked against something real instead of remembered.
