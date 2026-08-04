# TREATMENT — One Study Deep

> Director's chair. Filed 2026-08-04. Revised three times the same day: after the
> writers' room was convened, after QC Gate 1 returned FAIL, and after the room
> was re-convened to write the sixth act. Locked script at `script.txt` —
> **1,252 spoken words / 1,256 gate-words, register gate PASS on all six.**

---

## Thesis

The evidence that AI is costing us something cognitively is far thinner than the
phrase that carried it — and the fact that we believed it anyway, exactly as we
did with Google in 2011, is the more interesting finding.

## The turn

**Act 5 opens the history at 4:42 — word 834 of 1,252, or 67% in. Dead on
two-thirds.** The viewer's model flips at 5:33 on "Nobody came to the funeral"
(79%), and the act lands the thesis at 7:03.

Up to that point the film has shown the study is thin and that the belief
predates it. The turn is that this has happened before, in full: the 2011 Google
Effects study became the defining fact about technology and the mind for a
decade, its headline experiment failed to replicate in 2018 and again in 2020,
and nobody noticed.

What changes in the viewer's head: **the subject stops being AI and becomes us.**
We do not reach for these studies to find something out. We reach for them to
license a feeling we already have.

Landing line: *"We had the feeling first, and then we went looking for a
footnote."* Act 4 has already made that literal — see source rows 22–24.

## Act table

| Act | Span | Job | Exit condition |
|---|---|---|---|
| 1 | 0:00–0:58 | The recognition. A room, a night, an object. No study, no statistics. | "This is about a thing I have felt and never said." |
| 2 | 0:58–2:03 | Deliver Kosmyna et al. straight and make the apparatus vivid. Earn the phrase. | "There is a real experiment here and I understand what it measured." |
| 3 | 2:03–3:10 | The retraction — including the decay of the study's own famous number. | "The number I repeated was the least durable thing in the paper. And something is still there." |
| 4 | 3:10–4:42 | **THE ORDER OF EVENTS.** Why we believed it so fast: the belief did not come from the evidence, and there is a paper trail. | "I did not get this from a study. So the study failing will not take it away." |
| 5 | 4:42–5:49 | **The turn.** Sparrow 2011, the 2018 and 2020 failures, the pattern. | "This is not a story about AI. It is about what I do with evidence." |
| 6 | 5:49–7:03 | The honest beat and the landing. The surviving finding cuts both ways; the film indicts itself; a test that can be run tonight. | "The worry survives, I am not off the hook, and I have something to do." |

**Act 4 is new** (2026-08-04, third revision). Its job is the one the film was
missing: it showed the study was thin and that the pattern recurs, but never
explained *why the belief keeps outrunning the evidence*. Without it the turn
lands as pattern-recognition; with it, the turn lands as explanation — the
replication failures in Act 5 read as sad rather than as a scoreboard, because
the viewer already knows the belief was never resting on them.

### The house rate — measured, and the error that was in this file

The previous version of this treatment used **~115 wpm** and every timing in it
was wrong. Two compounding mistakes, both recorded here because the second one
is not obvious:

1. It divided narration words by **total film runtime** (887 words ÷ 466.6s on
   `batman-effect`), which includes every second after the last word is spoken.
   That is not a speech rate.
2. `batman-effect` was itself recorded **slowed**, and that was treated as the
   house default.

Measured directly from the only two films carrying per-word timings:

| Artifact | Script words | Narration duration | Rate |
|---|---:|---:|---:|
| `you-happen-to-life/audio/words.json` | 1199 | 388.0s | **185.4 wpm** |
| `you-watched-it-happen/audio/words.json` | 1193 | 423.7s | **169.0 wpm** |

**House rate ≈ 177 script-words per minute of narration at default speed**, with
a ~9% spread between voices and reads. These are also the two films VOICE-SPEC
names as the ones whose narration was judged good, so this is the rate of the
work we like, not just the rate we happen to have measured.

**The speed parameter is the whole discrepancy.** 169.0 × 0.75 = 126.8 wpm, and
QC measured `batman-effect` at 126.5 — a 0.2% match. So:

| Setting | Rate | This script (1,1xx words) |
|---|---:|---|
| default | ~177 wpm | the target band |
| `speed: 0.75` | ~133 wpm | ~33% longer |

**Runtime is therefore a decision Sound and the Director make together, not a
property of the script.** Choose the speed with the length; never discover it
afterwards. This film records at **default speed** — see the length ruling below.

**Sound still measures the real read and all spans are re-cut from
`audio/words.json`, never from this table.**

### The length ruling

**Resolved.** At 1,252 spoken words the film runs a **band of 6:45 – 7:24**,
mean **7:03**. That band straddles the brief's 7:00 ceiling; the mean is three
seconds over it and Sound's measured read settles it. No trim is pre-nominated.

How it got here. The film measured **4:45** when the rate error was found —
ninety seconds *short*, not over. There were two ways to close that and only one
was honest:

- **Record at `speed: 0.75`.** 847 words → 6:20, in band, no writing required.
  **Rejected.** Solving a length problem with a setting is "slow before you
  write" — the inverse of cut-before-you-compress and just as lazy. It would also
  put this film at a slower read than the two films the register band is built on.
- **Write the material the film was missing.** Taken, in two passes: the two ends
  (Act 1, the close), then the sixth act.

**Rejected on the merits, with the words available.** A fourth writer filed a
strong act on *the standard of evidence* — what a study would need before it
could carry this claim, built from the 2018 project's actual conduct (5× samples,
pre-registered, plans sent to the original authors before collection). It is
verified and it is good. It is cut because the film could not hold both it and
Act 4, and Act 4 is more on-thesis: the film's method is confession, and the
standard act was, in its own writer's words, "we-free by design" — the one act in
the film that is not confessing. Filed at `PAGES-standard.md` if a future cut
wants it.

**Register margins, which is where a trim will actually bite.** `you` sits at
36.6 against a floor of 35.0 — about two tokens of slack. `we` at 16.7 is
mid-band and no longer the binding constraint it was at 847 words. `words_sentence`
at 13.36 against a floor of 13.0 is the tightest: this script has been fused
**seven times** to hold it, because merging several writers' pages selects for
each writer's punchiest lines and quietly loses the connective ones. That is the
bridges failure arriving through a different door — nothing is trimmed, but the
prose still loses its joins. **Any downstream edit re-runs the gate.**

Bridges that must not be cut: Act 4's first sentence, Act 5's first sentence,
Act 6's first four — **and Act 6's last four**, which carry the film's principal
callback and would die silently to a runtime trim without tripping the gate.

---

## Locked VO

> Generated from `script.txt`. If these differ, `script.txt` wins.

### ACT 1 — THE RECOGNITION · 0:00–0:58

It was a Tuesday, probably. The kitchen table, because the desk had something
on it, and the overhead light off, because it was late. One thing left before
bed: a page of a proposal, a reply to a landlord, forty lines of code that had
to run in the morning. It took you less time than it used to. You read it back
and it was better than fine. And somewhere in the middle of it there was a step
that you did not take. You can point at the sentence before it. You can point
at the sentence after it. The part between them arrived. Not wrong. Just not
yours the way the rest of it is yours. It is not guilt exactly, it is closer to
arriving somewhere and not remembering the drive. Most of us have had that
feeling and never said it out loud. We have a machine that finishes our
sentences now, and we have quietly started to wonder what that costs us. Last
June, a paper told us.

### ACT 2 — THE STUDY THAT NAMED IT · 0:58–2:03

It came out of the MIT Media Lab, where Nataliya Kosmyna and seven colleagues
sat fifty-four people at a Mac in thirty-two electrodes. They had twenty
minutes to write an essay from an old SAT paper. If you were in the first group
you could use ChatGPT and nothing else, in the second any website you liked
that was not a chatbot, and in the third a text editor and your own head.
Connectivity is the word the paper leans on, and it does not mean how hard you
are working. Second by second, for every pair of those sensors, it asks which
one is leading and which one is following. The brain-only group's networks were
the strongest and the widest. The search group landed in between, and the
ChatGPT group's were the weakest of the three. Then an interviewer asked them
to do the part you would think was easiest. Quote one line from the essay you
just wrote. Five out of every six in the ChatGPT group could not. We have all
sent something we could not quote back an hour later. The paper gave it a name.
Cognitive debt.

### ACT 3 — WHAT THE STUDY ACTUALLY IS · 2:03–3:10

You probably met that phrase before you ever met the study, because inside a
week it was a fact you could use in an argument. So here is what you were
actually leaning on. The paper is a preprint, and if you look, every page of
the current version still says under review. Fifty-four people wrote essays in
the first three sessions, but the accumulation, the debt, the thing the title
promises you, rests on a fourth session where people swapped tools. Eighteen
came back. And that five-out-of-six figure is the first session only. Asked the
same question in the third session, five of eighteen could not. The authors
write that the question might have caught people off guard the first time they
heard it, and they describe the effect as persisting, but attenuated. So
something is there. It is about a third of the number you were handed. At the
end of last year, four researchers filed a formal comment. Milos Stankovic and
his colleagues congratulated the team, then listed the sample size, the
reproducibility of the analysis, the EEG methods, and inconsistencies in how
the results were reported. The study said preliminary. We heard proof.

### ACT 4 — THE ORDER OF EVENTS · 3:10–4:42

So how did a preliminary result become something you could repeat without
checking it? Not from the evidence, because the evidence was late, and you can
put a date on that. In July of 2008, The Atlantic ran an essay by Nicholas
Carr. You know the title, and you have probably used it. Is Google Making Us
Stupid? Most of us have never read the piece underneath it. It is a man
describing his own attention. He says reading used to be easy, and that now his
concentration starts to drift after two or three pages. That is the same kind
of evidence you have, and he is careful about what it is worth. Anecdotes alone
don't prove much, he says, and we still await the long-term neurological and
psychological experiments. He even points out that Socrates made the same
complaint about writing, and that Socrates was not wrong about it, only
shortsighted. Near the end, he tells the reader to be skeptical of his
skepticism. That essay is seventeen years older than the paper you heard about
last June. It is three years older than the experiment that came next. And when
that experiment was published, it named Carr once, as the last entry on the
list of references, inside a sentence saying that the disadvantages of being
constantly wired are still being debated. So the worry was in print first, and
the evidence you were given turned up second. Which means you did not get this
from a study. It was there before the study, and it will still be there when
you have forgotten which study it was.

### ACT 5 — THE TURN · 4:42–5:49

We have done this before, and it is worth knowing how it ended last time. In
2011 the journal Science published the four experiments by Betsy Sparrow, Jenny
Liu and Daniel Wegner, and they called it Google Effects on Memory. The famous
one worked like this, and you have probably heard it. Somebody asks you a hard
trivia question, and afterwards you are slower to name the colour of a word
like screen, or internet. Your mind has already gone looking for the machine.
That became the fact about technology and the mind, and it stayed in the books
and the talks and the arguments for a decade. Then in 2018 a project re-ran
twenty-one social science experiments from Science and Nature, and thirteen of
them held up. The Google priming effect was not one of the thirteen. A separate
attempt in 2020, with twice as many people, found nothing either. Nobody came
to the funeral. The belief carried on without it, which tells you what that
study was really doing for us. It was not helping us find out, it was helping
us confirm. We had the feeling first, and then we went looking for a footnote.

### ACT 6 — THE HONEST BEAT AND THE LANDING · 5:49–7:03

So the easy ending is that the evidence was thin and you can relax. It is not
available. The piece that fell over was the one that agreed with us. What
survived is the duller half. Storm and Stone, 2015: save one file, and you
learn the next one better. Runge and colleagues replicated that in 2021, and
found the cost. The file you saved gets harder to reach. Both, at once.
Offloading buys you room and charges you for whatever you put down. This film
was written and drawn and read aloud by the machines it is about. We cannot get
back inside it either. So the question is probably not whether you remember. It
is whether you could walk it back. That has a shape. Open the last thing you
sent with your name at the top of it. Find the step in the middle that you did
not take, the part that arrived. Then say out loud, to nobody, why it is that
way and not the other way. Why that number, why that order, why that word and
not the ordinary one. The test is not whether the answer is right. It is
whether a reason comes up at all, or only the shape of one. Nobody has measured
how much of that we are carrying.

---

## Source table

Every source opened this session. Where a number appears in the preprint, it was
verified by direct text extraction of **both v1 and v2 of the PDF**, not from an
abstract, a summary, or a writer's transcription.

| # | Act | Claim | Source | Status |
|---|---|---|---|---|
| 1 | 2 | MIT Media Lab; Nataliya Kosmyna and seven colleagues (8 authors) | Kosmyna, Hauptmann, Yuan, Situ, Liao, Beresnitzky, Braunstein, Maes — *Your Brain on ChatGPT*, arXiv:2506.08872 (v1 2025-06-10, v2 2025-12-31) | **VERIFIED** |
| 2 | 2 | Fifty-four people; thirty-two electrodes; three groups | v2 l.138: *"18 participants per group, 54 total."* 32-channel EEG per methods | **VERIFIED** |
| 3 | 2 | Twenty minutes; essay prompts from an old SAT paper | Paper methods (extracted text) | **VERIFIED** |
| 4 | 2 | Group conditions: ChatGPT only / any non-chatbot website / text editor and own head | Paper methods | **VERIFIED** |
| 5 | 2 | Connectivity is directional, not effort — which sensor leads and which follows | The paper's dDTF (directed transfer function) connectivity analysis | **VERIFIED** |
| 6 | 2 | Brain-only strongest and widest; search in between; LLM weakest | Abstract, v1 and v2 | **VERIFIED** |
| 7 | 2 | **Five out of every six in the ChatGPT group could not quote a line** | v1 l.101 / v2 l.1474, identical: *"In the LLM-assisted group, 83.3 % of participants (15/18) failed to provide a correct quotation, whereas only 11.1 % (2/18) in both the Search-Engine and Brain-Only groups encountered the same difficulty."* Rendered as a fraction for the ear. | **VERIFIED** |
| 8 | 3 | It is a preprint still under review | v2 page footer, every page: *"Preprint, under review"* | **VERIFIED** |
| 9 | 3 | 54 in sessions 1–3; 18 completed session 4 | v2 l.70: *"participants for Sessions 1, 2, 3, and 18 participants among them completed session 4."* | **VERIFIED** |
| 10 | 3 | **Asked the same question in the third session, five of eighteen could not** | **Question 3 body text, both versions** — v1 l.1388–89 / v2 l.1734–35: *"The LLM group mentioned that they might experience some challenges with quoting ability (13/18 indicated being able to quote)."* 13 able → **5 of 18 not able**, the same Question 3 measure as the Session 1 headline (15/18). Session 1 Q3 = 15/18 → Session 3 Q3 = 5/18. | **VERIFIED** |
| 10b | — | *Not narrated.* The paper's own Discussion (v2 l.5180–82) fuses the two measures: *"83% of participants (15/18) **reporting difficulty quoting** in Session 1 … with 6 out of 18 participants **still failing to quote correctly** by Session 3."* The first clause is Question 3, the second is Question 4. An earlier draft of this treatment cited that sentence as the paper's own like-for-like comparison. It is not one. **Quoting a source's summary of itself is not the same as checking the source** — recorded because it is the exact error this film is about. | **VERIFIED (as a fact about the paper)** |
| 11 | 3 | The authors say the question might have caught people off guard the first time | v1 l.203 / v2 l.1608, identical: *"Unlike Session 1, where the quoting question might have caught the participants off-guard, as they heard it for the first time…"* Corroborated at v1 l.177: *"We expected the trend in responses in sessions 2 and 3 to be different, as the participants now knew what types of questions to expect."* | **VERIFIED** |
| 12 | 3 | They describe the effect as persisting, but attenuated | v2 l.5181, the authors' own words: *"persisted albeit attenuated"* | **VERIFIED** |
| 13 | 3 | Four researchers filed a formal comment at the end of last year | Stankovic, Hirche, Kollatzsch & Doetsch, arXiv:2601.00856, submitted 2025-12-29 | **VERIFIED** |
| 14 | 3 | The comment congratulated the team, then listed sample size, reproducibility, EEG methods, reporting inconsistencies | Same, abstract, verbatim | **VERIFIED** |
| 15 | 4 | Science, 2011, four experiments, Sparrow, Liu & Wegner, *Google Effects on Memory* | *Science* 333, 776–778 (2011) | **VERIFIED** |
| 16 | 4 | The famous one: after a hard trivia question, slower to name the colour of computer words | Sparrow Experiment 1, modified Stroop, as described in Hesselmann (2020) PeerJ 8:e10325 | **VERIFIED** |
| 17 | 4 | 2018 project re-ran 21 experiments from Science and Nature; thirteen held up | Camerer, Dreber, Holzmeister et al., **Nature Human Behaviour** 2, 637–644 (2018): *"a significant effect in the same direction as the original study for 13 (62%) studies"* | **VERIFIED** |
| 18 | 4 | The Google priming effect was not one of the thirteen | Hesselmann (2020) PeerJ 8:e10325: the 2018 project *"did not show a significant effect despite adequate statistical power"*; corroborated by the FORRT FLoRA Replication Atlas entry for doi:10.1126/science.1207745. **Camerer's per-study table is paywalled and was not opened directly — two independent secondary sources, one peer-reviewed.** | **VERIFIED (secondary)** |
| 19 | 4 | A 2020 attempt with twice as many people found nothing | Hesselmann, G. (2020), PeerJ 8:e10325. 117 recruited / 89 analysed vs ~46 original. *"No conclusive evidence."* | **VERIFIED** |
| 20 | 5 | Storm and Stone, 2015: save one file, learn the next one better | Storm & Stone, **Psychological Science** 26(2), 182–188 (2015), PMID 25491269: *"saving one file before studying a new file significantly improved memory for the contents of the new file"* | **VERIFIED** |
| 21 | 5 | Runge and colleagues replicated it in 2021, and found the cost | Runge, Frings & Tempel, **Psychological Research** 85, 1633–1644 (2021): *"Across three experiments, we replicated and specified this saving-enhanced memory effect"*, plus a cost effect — saved information becomes less accessible | **VERIFIED** |
| 22 | 4 | In July of 2008, The Atlantic ran an essay by Nicholas Carr, *Is Google Making Us Stupid?* | Carr, N., *Is Google Making Us Stupid? What the Internet is doing to our brains*, **The Atlantic**, July/August 2008. Full text downloaded and extracted this session (`scratchpad/carr.txt`). Masthead read verbatim off the page. | **VERIFIED (primary)** |
| 23 | 4 | It is a man describing his own attention; his concentration drifts after two or three pages | Same, verbatim: *"Immersing myself in a book or a lengthy article used to be easy… Now my concentration often starts to drift after two or three pages."* Narrated as **reported speech**, deliberately — see ruling 7. | **VERIFIED (primary)** |
| 24 | 4 | "Anecdotes alone don't prove much, he says, and we still await the long-term neurological and psychological experiments" | Same, verbatim: *"Anecdotes alone don't prove much. And we still await the long-term neurological and psychological experiments that will provide a definitive picture of how Internet use affects cognition."* Two sentences joined, trailing clause dropped, **no word added**. | **VERIFIED (primary, verbatim)** |
| 25 | 4 | He points out that Socrates made the same complaint about writing, and that Socrates was not wrong, only shortsighted | Same, verbatim: *"In Plato's Phaedrus, Socrates bemoaned the development of writing… 'cease to exercise their memory and become forgetful.'… Socrates wasn't wrong—the new technology did often have the effects he feared—but he was shortsighted."* **The film attributes this to Carr, not to Plato** — it is a verified fact about Carr's essay, which avoids quoting Plato at second hand. See ruling 6. | **VERIFIED (primary)** |
| 26 | 4 | Near the end he tells the reader to be skeptical of his skepticism | Same, verbatim: *"So, yes, you should be skeptical of my skepticism."* Rendered as reported speech to keep first-person singular out of the narrator's mouth — see ruling 7. | **VERIFIED (primary, verbatim)** |
| 27 | 4 | Seventeen years older than last June's paper; three years older than the experiment that came next | Carr July/Aug 2008 → Kosmyna arXiv:2506.08872 v1, 2025-06-10 (= 17y). Carr 2008 → Sparrow et al., **Science** 333(6043):776–778, PDF footer *"Published online 14 July 2011"*, running head *"5 AUGUST 2011"* (= 3y on either date). | **VERIFIED (arithmetic over two dated primaries)** |
| 28 | 4 | **That experiment named Carr once, as the last entry on the list of references, inside a sentence saying the disadvantages of being constantly wired are still being debated** | Sparrow PDF, extracted this session (`scratchpad/sparrow.txt`). Reference list item 9, line 458, verbatim: **`9. N. Carr, Atlantic 302, 56 (2008).`** — the last entry in the printed list (10–13 are in the Supporting Online Material). Sole body call site, lines 428–431, verbatim: *"This gives us the advantage of access to a vast range of information, although the disadvantages of being constantly 'wired' are still being debated (9)."* **Verified independently by this chair, not taken from the writer's transcription.** | **VERIFIED (primary PDF)** |

### Not narrated — recorded for the colophon and for QC

- **The v1 → v2 statistics change.** v1 reported `F(2,51) = 79.98, p < .001` and
  pairwise `t = 8.999` for the quoting result. **v2 removes the F-statistic and
  the t-values entirely and reports only p-values.** v2 was submitted 2025-12-31,
  two days after the Stankovic comment was filed. The film does **not** narrate
  this. Timing is not causation, and stating the sequence aloud would be innuendo
  dressed as reporting — the register forbids it. Recorded because it is true,
  checkable, and the Editor may want it in the colophon.
- **Gong & Yang (2024)**, *Frontiers in Public Health* 12:1332030 — 22 articles,
  35 comparisons, 30,889 participants; the Google effect real but heavily
  moderated. Verified; cut for room, available to the colophon.

### Claims cut

| Cut | Why |
|---|---|
| `F(2,51) = 79.98` and all test statistics | Present in v1, **removed in v2**. Narrating a statistic the authors have withdrawn would be a defect. Never reinstate. |
| "Session 2 quoting failures were 4 of 18" | Real, but it is **Question 4** (correct quoting) while the 15/18 headline is **Question 3** (ability to quote at all). Tracking one measure across sessions then switching to another mid-sentence is exactly the "two experiments fused into one" error. The film uses only the paper's own like-for-like Discussion comparison: 15/18 in Session 1, 6/18 by Session 3. |
| "…and never looked for the study that would have let us off" | **False of this production.** See ruling 3. Cut. |
| "We are not going to give you that" | Narrator making a promise = narrator as character. See ruling 4. Cut. |
| Any framing of the study as debunked, wrong, or overturned | It is preliminary and attenuated, which is what its authors say. The register forbids triumph. |
| *"and got read as the answer"* (Act 4) | A claim about **reception**, and no named commentator was found saying the 2011 study settled Carr. The writer offered to cut it before defending it. Cut. Act 4 now claims chronology only — two dates and a citation — and lets the viewer close the gap. |
| Carr's best sentence — *"someone, or something, has been tinkering with my brain"* | First-person singular in the narrator's mouth. See ruling 7. |
| Any direct quotation of Plato | The film cites **Carr citing Plato**, which is a verified fact about a document open on this desk. Quoting the *Phaedrus* would mean adjudicating translations for a line the film does not need. See ruling 6. |
| A third precedent (television and attention — Christakis 2004 / Foster & Watkins 2010) | Real and partly verified, but the *pre-existing* worry would rest on a 1977 book nobody opened, and three half-shown cases turn a documented observation into a survey. The Carr chronology is stronger because it is narrow: one essay, one paper, one footnote, three years. |
| The Sparrow authors' line *"It may be no more that nostalgia at this point…"* | Verified, sitting one sentence after the Carr citation, and left out. It would let the film use those authors to sneer at the worry. The register forbids sneering in either direction. Colophon. |

---

## Register

**Narrator voice.** A colleague thinking out loud at the end of a long day —
someone who read the paper, wanted it to be true, checked anyway, and is telling
you what they found without making a performance of it. Level, unhurried,
specific. Not a warning. Not a scold. Never pleased with itself for catching a
study out.

**Emotional temperature.** Cool and even for five acts, with one warm patch: Act
6, from *"The piece that fell over was the one that agreed with us"* to *"We
cannot get back inside it either."* That is the only place the read softens. Act
5's *"Nobody came to the funeral"* is the coldest line in the film — flat, with
air after it.

**Stance inside the band.** Measured **36.6 `you` / 16.7 `we`**. Near the "you"
floor, mid-band on "we". The last three films sat at 41 / 41 / 65 on "you". This
one steps back from accusation on purpose: a film that accuses the viewer of
cognitive debt while being made by a machine has no standing. The confession is
the argument.

**What the film must never feel like.** A debunk. A gotcha. A defence of AI. A
warning about AI.

**Platform — two standing rules this film added.** The narrator is never a
character: no name, no face, no first-person singular, no credentials.

1. **The narrator may not make promises about the film.** "We are not going to
   give you that", "we will come back to this", "stay with me" create a speaking
   agent with intentions — bucket-3 exposure whatever the topic. State the world;
   never announce the edit. See ruling 4.
2. **No first-person singular, even inside a quotation.** Quoted speech is
   rendered as reported speech. `grep -Eo "\b(I|my|me|mine)\b"` returns **0** on
   the locked script and must keep returning 0. See ruling 7.

---

## Intent notes — per act

**Act 1 — recognition, gently uncomfortable.** Domestic, not technological. A
kitchen table at night, one object, a light that is off. The discomfort is that
it is ordinary. The motif is established here as a **picture**, not a phrase:
two things you can point at and one you cannot.

**Act 2 — genuine interest, leaning in.** The film is on the study's side here
and should feel that way. Apparatus, curiosity, the pleasure of a clean
experiment. There is real hardware to look at — a desk, a cap of sensors, a
twenty-minute clock — and the three conditions are a shape the viewer must be able
to hold. Land "cognitive debt" with a small satisfying click, because the film is
about to take it apart.

**Act 3 — the floor going soft.** Not alarm. Deflation. Scale is the lever:
fifty-four becoming eighteen should feel like a room emptying, and five-in-six
becoming five-in-eighteen is the film's thesis as a single picture. It must not
tip into gloating — *"So something is there"* is the act's honest hinge and needs
its own beat, not a throwaway.

**Act 4 — the ground moving backwards.** The newest act and the quietest. Not an
exposé: the feeling is of a document being turned over and found to have said the
careful thing first. This act is mostly *paper* — a magazine page from 2008, a
reference list, one line near the bottom of it. The single image the act must
land is the citation itself: a name in a list, small, at the end, inside a
sentence that says the question is still open. That picture is the film's title
card for its own thesis, and it pays off ninety seconds later on the word
"footnote". Do not draw it twice.

**Act 5 — recognition again, colder and wider.** The floor extends backwards in
time. The only act permitted to feel like history. *"Nobody came to the funeral"*
wants stillness and space — the one place a held, near-empty image is right.

**Act 6 — implicated, and oddly relieved.** The admission should feel like weight
coming off, not an apology. The two-sided finding needs an image that is
genuinely double — a gain and a cost in the same object, not two objects. Land on
something the viewer could actually do, held long enough to be considered, and
return to Act 1's object one last time.

---

## Title

**Primary: `One Study Deep`.** Breaks the second-person-imperative run (*You Are
Not Finished*, *You Happen to Life*, *You Watched It Happen*) — a noun phrase,
not an address. Names the real subject: the shallowness of the discourse, not the
badness of the study.

Alternates: `A Feeling Looking For a Footnote` · `Nobody Came to the Funeral`
(strongest as a short) · `Every Technology Gets Its Study`.

---

## Chair notes — the room, and seven rulings

The room has now been convened twice: once on Acts 2 and 5, once on the two ends
and the sixth act. **Six writers have worked this film.** Every structural
improvement in it came from that, and the first draft of this treatment — written
with no room at all, and disclosed as a fault at the time — is the control group.

**Ruling 1 — the 83% goes back in, with its decay.** Cut in the first pass
because no primary statement could be opened; restored once it was, with the
context that makes it honest. Five out of six in Session 1, five of eighteen by
Session 3, the authors' own off-guard caveat, their own phrase *persisting, but
attenuated* — then *"So something is there."* Reporting the collapse without the
persistence would be this film committing its own sin in the opposite direction.

**Ruling 2 — v2 is real and it changed one thing.** Every narrated number is
identical in v1 and v2; verified by extracting and grepping both PDFs. v2 drops
`F(2,51) = 79.98` and the t-values. No narrated line cited a statistic, so nothing
changed — but the finding carries a standing "do not reinstate". The film does not
narrate the two-day gap between the Stankovic comment and the revision. That
sequence is true and it is innuendo.

**Ruling 3 — "never looked for the study that would have let us off" is CUT.**
The line asked this chair to certify a claim about our own process, and it is
false: the exculpatory study was found *because* it was looked for, and it is in
Act 6. Claiming a vice we did not commit in order to sound humble is performative
confession — the worst failure available to a film about honesty.

**Ruling 4 — "We are not going to give you that" is CUT; the writer was right and
the Director was wrong.** A narrator making promises becomes a character. Promoted
to the standing rule in Register, above.

**Ruling 5 — the Q3/Q4 fusion, and the lesson under it.** QC caught the film
pairing *five out of six* (Question 3, ability to quote, Session 1, 15/18) with
*six of eighteen* (Question **4**, correct quoting, Session 3) — the same fusion
this chair had rejected one layer up. Verified independently: the like-for-like
Question 3 figure is **13/18 able → 5 of 18 not**, v1 l.1388–89 / v2 l.1734–35,
present in **both** versions. The arithmetic confirms it: 5/18 ÷ 15/18 = **0.3333**,
which is what *"about a third"* already said; the fused pairing gives 0.40. The
sentence fitted the number the film had not used.

The deeper lesson, and the reason this is the film's own subject arriving in its
own production: the earlier treatment justified the pairing by citing the paper's
Discussion as a like-for-like comparison. **That sentence is itself the fusion.**
Quoting a source's summary of itself is not checking the source. Recorded at
source row 10b.

**Ruling 6 — Plato is cited through Carr, not directly.** The room filed a full
263-word act built on the *Phaedrus* (Theuth and Thamus, Stephanus 274c–275b,
two public-domain translations opened). It is good work and it is **cut** — its
own writer noted that the film would otherwise say *the worry predates its
evidence* three times in four minutes, and offered its act as the one to go. It
was right. But the depth survives for **22 words**, because Carr's 2008 essay
*already makes the Plato argument itself*, including its own honest correction:
*"Socrates wasn't wrong… but he was shortsighted."* Verified by this chair in the
extracted text. That is a better version: the essay that launched the modern
worry already knew the worry was 2,400 years old, already knew it had been right
before, and already told the reader to doubt it — and the confident version
arrived three years later anyway.

**Ruling 7 — no first-person singular, even inside a quotation.** Two writers
offered Carr's own words in the first person; the strongest was *"you should be
skeptical of my skepticism."* Both are rendered as reported speech. The reasoning
is mechanical rather than aesthetic: QC greps for `\b(I|my|me)\b` and gets zero
matches, and that is a bright line worth more than one unit of snap. A quoted
"my" makes a machine-checkable property into a human judgement call at every
future gate. **Confirmed after the merge: zero matches.** Standing rule.

### What the room gave, by writer

| Angle | Outcome |
|---|---|
| **mechanism** (Act 2) | Merged. Thirty-two electrodes, the twenty-minute SAT essay, the second-person group assignment, *"it does not mean how hard you are working"*, the leading/following gloss, *"five out of every six"*. |
| **confession** (Act 5) | Merged. *"It is not available"*, *"The piece that fell over was the one that agreed with us"*, *"Both, at once"*, *"We cannot get back inside it either"*. |
| **the two ends** | Merged. Act 1 became a room on a Tuesday; the motif became drawable — *"You can point at the sentence before it. You can point at the sentence after it. The part between them arrived."* The close became a procedure with a non-prescriptive clamp. Cut on its own advice: an invented *"about ten minutes"* (a film about a misused number must not open with one it made up) and *"better than you are on a Tuesday"* (warmth belongs to Act 6). |
| **chronology** | Superseded by the fuller act, but it made the find of the production: **Sparrow cites Carr at reference 9.** |
| **the standard** | Cut for room; verified and filed. It caught its own fabrication — it wrote "average age twenty-two" where the paper says M = 22.9, flagged it as "a writer's reason, not an honest one", and asked to be corrected. That is the room working. |
| **the complaint is older** | Cut as an act, folded to 22 words via Carr. See ruling 6. |

### Outstanding

- **R3 / Gate 1.6 — motif plates — is Storyboard's and is still open.** The film's
  principal motif is now much more boardable than it was: Act 1's *"You can point
  at the sentence before it… the part between them arrived"* and Act 6's *"the
  step in the middle that you did not take, the part that arrived"* describe **the
  same object**, and it must be drawn as the same object, not as two drawings of
  an idea. Two further recurring objects need canonical plates: the study
  apparatus (desk, cap of sensors, twenty-minute clock) and Act 6's single
  double-sided object — a gain and a cost in one thing, not two things.
- **QC item 3.4 — no human has listened to this film.** Cannot be satisfied by any
  agent. Outstanding at Gate 3.
- **The act table's spans are computed, not measured.** They are honest arithmetic
  at 177 wpm, but they are still arithmetic. Sound re-cuts every span from
  `audio/words.json`.
