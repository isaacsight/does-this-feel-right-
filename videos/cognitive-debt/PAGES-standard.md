# PAGES — THE STANDARD

> Writer's chair. Filed 2026-08-04. New act, sits between Act 4 ("we went
> looking for a footnote") and Act 5 ("So the easy ending…").
> 169 words · ~57s at 178 wpm.

---

## Angle

The film diagnoses and then hands over a personal test, and between those two
things it never says what good evidence would have looked like. So the viewer
leaves able to distrust *this* headline and no better equipped for the next one.
This act closes that. It is not a methods lecture and not a checklist — it is two
questions, both drawn from documents the film has already cited, that a person
can carry out of the room and use on something the film has never seen.

The two questions, and why these two:

1. **Was the plan written down first?** Sourced entirely from what the 2018
   replication project actually did — five times the sample, analysis registered
   publicly in advance, plan sent to the original authors before a single data
   point was collected. The act does not define pre-registration. It describes
   one instance of it, concretely, and lets the standard be visible in the
   behaviour.
2. **How far is it from what got measured to what you are afraid of?** The
   generalisation gap, said with the study's own numbers — and, crucially,
   attributed to the paper itself, which lists this under its own limitations.
   The film does not catch the authors out. The authors already said it.

I deliberately did not use the Stankovic list as the spine, even though it is the
obvious material. It is five abstract nouns in a row, it is already narrated in
Act 3, and repeating it here would turn the act into the checklist the brief
forbids. Its work is done better by showing one team's conduct.

---

## Pages

### NEW ACT — THE STANDARD

So what would it take to actually know? Not a better feeling. A study you could
grade.

Two questions do most of the work.

The first one: was the plan written down before anybody looked? When a team
re-ran those twenty-one experiments in 2018, they used about five times as many
people, they registered the analysis in public first, and they sent it to the
original authors for comment before collecting a single data point. That is a
very hard thing to fool yourself inside. Ask it of the next headline that reaches
you. Most of them have none of it.

The second one: how far is it from what got measured to what you are actually
afraid of? Fifty-four students, five universities, one city, average age
twenty-two, twenty minutes on an SAT prompt. The paper lists that under its own
limitations. You are not frightened of twenty minutes. You are frightened of
years.

Neither question tells you a study is wrong. They tell you what it will hold.

---

## Source notes

Every source below was opened this session by this chair. Camerer was read as
extracted PDF text from the open-access copy, not from an abstract or a summary.
Kosmyna was read as extracted text from v2 of the arXiv PDF.

| Line | Claim | Source | What it actually says |
|---|---|---|---|
| "a team re-ran those twenty-one experiments in 2018" | 21 experiments, 2018 | Camerer, Dreber, Holzmeister, Ho, Huber, Johannesson, Kirchler, Nave, Nosek, Pfeiffer et al., *Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015*, **Nature Human Behaviour** 2, 637–644 (2018) | Abstract, verbatim: *"We replicate 21 systematically selected experimental studies in the social sciences published in Nature and Science between 2010 and 2015."* Open copy: `pure.eur.nl/ws/files/37359856/` |
| "about five times as many people" | 5× sample size | Same, abstract | Verbatim: *"The replications are high powered, with sample sizes on average about five times higher than in the original studies."* Corroborated in the Discussion: *"with replication sample sizes about five times larger as the original studies."* Two-stage design: stage 1 ~3× original, stage 2 ~6×. |
| "they registered the analysis in public first" | pre-registration | Same, Methods | Verbatim: *"All of the replication and analysis plans were made publicly known on the project website, pre-registered at the Open Science Framework (OSF)."* Abstract: *"The replications follow analysis plans reviewed by the original authors and pre-registered prior to the replications."* |
| "sent it to the original authors for comment before collecting a single data point" | plans reviewed by originals, pre-collection | Same, Methods | Verbatim: *"…and sent to the original authors for feedback and verification prior to data collection."* The film's phrasing compresses "feedback and verification" to "comment"; it does not overstate. |
| "Fifty-four students" | n=54 | Kosmyna et al., *Your Brain on ChatGPT*, arXiv:2506.08872 v2 | *"We recruited a total of 54"* / 18 per group. 60 originally recruited, 55 completed, 54 reported to keep groups even. |
| "five universities, one city" | recruitment base | Same, Participants | Verbatim: *"all recruited from the following 5 universities in greater Boston area: MIT…, Wellesley…, Harvard…, Tufts…, and Northeastern."* |
| "average age twenty-two" | mean age | Same, Participants | Verbatim: *"between the ages of 18 to 39 years old (age M = 22.9, SD = 1.69)."* Rendered as "average age twenty-two" for the ear. 22.9 rounds to 23 — see *Lines I am unsure of*. |
| "twenty minutes on an SAT prompt" | task | Same, Protocol | Verbatim: *"produce an essay based on the topic's assignment within a 20 minutes time limit"*; *"All the topics were taken from SAT tests."* |
| "The paper lists that under its own limitations" | attribution | Same, *Limitations and Future Work* | Verbatim: *"In this study we had a limited number of participants recruited from a specific geographical area, several large academic institutions, located very close to each other. For future work it will be important to include a larger number of participants coming with diverse backgrounds like professionals in different areas, age groups…"* |

**Verified but not narrated.** Stankovic, Hirche, Kollatzsch & Doetsch,
arXiv:2601.00856, submitted 2025-12-29 — abstract opened and read this session.
The five concerns are, verbatim: *"(i) study design considerations, including
the limited sample size; (ii) the reproducibility of the analyses; (iii)
methodological issues related to the EEG analysis; (iv) inconsistencies in the
reporting of results; and (v) limited transparency in several aspects of the
study's procedures and findings."* Note for the Director: the locked Act 3
narrates four of these five and drops **transparency**. That is a defensible
compression, not an error, but it is worth knowing it is a compression.

**No line in this act is `[UNSOURCED]`.**

---

## Register gate — measured, both ways

Run against `tools/video/register-profile.py --gate`, on the merged script with
this act inserted between Acts 4 and 5.

| metric | script.txt now | with this act | band |
|---|---:|---:|---|
| you /1k | 37.78 | **39.25** | 35–58 |
| we /1k | 21.25 | **17.66** | 8–22 |
| syll/word | 1.38 | **1.39** | 1.26–1.42 |
| words/sent | 13.66 | **13.06** | 13–19 |
| Flesch | 76.21 | **75.85** | 72–84 |
| FK grade | 6.02 | **5.93** | 5.6–7.2 |

All six pass, exit 0. Two things the Director should know:

- The act is **"we"-free by design**, which pulls `we` off the ceiling from 21.25
  to 17.66. The treatment flagged that margin as thin. This buys it back. The act
  earns the exemption: it is the one place in the film that is not a confession,
  it is an instrument being handed over.
- **`words_sentence` lands at 13.06 against a floor of 13.00.** That is the
  tightest number in the film and it is my act that did it. Lever if the Director
  needs margin: merging *"Not a better feeling. A study you could grade."* into
  *"Not a better feeling, but a study you could grade."* moves it to **13.25**
  and costs the film one beat of rhythm. Measured, both versions. I recommend
  keeping the two sentences and spending the margin elsewhere.

---

## Lines I would fight for

1. **"That is a very hard thing to fool yourself inside."** The whole act in one
   sentence, and it does not say the word "bias" or the word "rigour". It also
   pays back Act 4 — the film has just spent two minutes describing people
   fooling themselves, and this is the shape of a room where that is difficult.
2. **"You are not frightened of twenty minutes. You are frightened of years."**
   The generalisation gap as a felt thing rather than a methods point. Two short
   sentences, same shape, and the second one is the film's actual subject.
3. **"They tell you what it will hold."** The act must not end on a debunk, and
   the treatment forbids triumph. This ends on load-bearing capacity — the study
   is a structure, and you are asking how much weight to put on it. It is the
   only landing I found that grants the study its due and still hands over a
   grade.

---

## Lines I am unsure of

- **"average age twenty-two."** The paper says M = 22.9, which rounds to 23. I
  wrote twenty-two because "twenty-two" is what the number *feels* like next to
  "students" and because 22.9 read aloud is a stumble. That is a writer's reason,
  not an honest one. **Recommend the Director change it to "average age
  twenty-three"** — it is one syllable, it costs nothing, and it is right. I have
  left it as filed so the choice is visible rather than buried.
- **"Ask it of the next headline that reaches you."** The closest this act comes
  to instruction, and the register is allergic to instruction. I kept it because
  it is the reason the act exists and because the action is in the world, not in
  the film — it is not "pause here". If it reads as a lecture in the room, the
  act survives without it; cut the sentence and "Most of them have none of it"
  still lands.
- **"Two questions do most of the work."** A shade close to a checklist
  announcement. The alternative was to let the two questions arrive unannounced,
  but a viewer with no scrollback needs to be told there are two, or the second
  one arrives as a non-sequitur. I think the signpost earns itself. Not certain.

---

## Structural notes

Written as notes. Nothing below is enacted in the pages.

1. **Placement.** After Act 4, not before. Before the turn, "what would good
   evidence look like" reads as a continuation of the takedown, and the film has
   already ruled out being a debunk. After "we went looking for a footnote", the
   same words are a different act: the film has just admitted that we reach for
   studies to license feelings, and this is the immediate, practical answer to
   "so what would I reach for instead". The act is only usable in that one slot.
2. **The act changes what Act 5 is doing, for the better.** As locked, Act 5
   carries both the honest beat *and* the only tool the film gives anybody, and
   the tool is a private one ("could you walk it back"). With this act in front
   of it, Act 5's test stops being the film's whole answer and becomes the
   personal half of a pair — public standard, private standard. I did not
   restructure Act 5 and would not; I am flagging that the meaning of its last
   four sentences shifts slightly when something precedes them.
3. **The act table's timings are dead.** Every span in `TREATMENT.md` is computed
   at ~115 wpm. At the measured ~178 the whole table is fiction, including the
   turn at 4:56 that the thesis section leans on. This act should not be
   timed into that table — the table needs recomputing from Sound's read, and
   the treatment already says so in its own footnote. Worth doing before the
   next chair inherits the numbers as fact.
4. **One thing this act deliberately does not do.** It never says the Kosmyna
   study fails these two questions. It supplies the questions and the study's own
   numbers in adjacent sentences and lets the viewer close the gap. That is the
   difference between handing over a standard and performing a verdict, and it is
   the only version of this act the register permits.
