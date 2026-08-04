# QC — GATE 1 (script locked, before narration)

**Film:** cognitive-debt (`One Study Deep`)
**Gate:** 1 — script, run before any narration is recorded
**Run:** 2026-08-04
**Artifacts audited:** `script.txt` (842 words), `TREATMENT.md`, `SCRIPT.md` (history), `STORYBOARD.md`
**Primary sources opened this run:** arXiv:2506.08872 v1 + v2 extracted text, arXiv:2601.00856
(abstract), Crossref records for 10.1126/science.1207745, 10.1038/s41562-018-0399-z,
10.7717/peerj.10325, 10.1177/0956797614559285, 10.1007/s00426-020-01341-0

---

## VERDICT — **FAIL**

Blocking items, in order:

1. **1.2 — source audit.** The Session 1 → Session 3 quoting comparison crosses two
   different measures (Question 3 → Question 4). This is the same fusion the Director
   declared cut; it survived one layer down, inside the paper's own Discussion sentence.
2. **1.5 — length is measured, not estimated.** The "measured house rate (~115 wpm)" is
   not reproducible from any artifact in this repository, and the derivation cited
   divides a narration word count by a *total film* duration. Every runtime in the act
   table, and the trim decision, rests on it.
3. **1.6 — motif plates.** `STORYBOARD.md` is a two-line stub. Zero beats, zero declared
   motifs, no plate plan — while the locked script already carries a recurring object.

Items 1.1, 1.1b, 1.3, 1.4 pass. Nothing was skipped.

---

## Item table

| # | Item | Evidence | Result |
|---|---|---|---|
| 1.1 | Register gate passes | `python3 tools/video/register-profile.py --gate videos/cognitive-debt/script.txt` → `EXIT=0`. 846 gate-words / 62 sentences. you 37.83 (35–58), we 21.28 (8–22), syll/word 1.38 (1.26–1.42), words/sent 13.65 (13–19), Flesch 76.29 (72–84), FK 6.01 (5.6–7.2). All six in band. | **PASS** |
| 1.1b | The "we" is earned confession, not padding | All 18 first-person-plural tokens read in context (full list below). Every one sits on a confession the film is actually making. None is decorative. | **PASS** |
| 1.2 | Every factual claim verified; spot-audit ≥2 | 20 of 21 table rows check out against primary text. **Row 10 fails.** Detail below. | **FAIL** |
| 1.3 | No advice register, no narrator-as-agent | Zero first-person singular (`I/my/me` → no match). Zero promise constructions (`we will / we are going to / stay with me / come back to / as we will see` → no match). Zero credential claims. Two imperatives found, both examined; neither is advice. | **PASS** |
| 1.4 | Skeleton test | Performed literally: 11 example/analogy sentences deleted into a scratch copy, remainder read end to end. All seven act-to-act and within-act bridges survive. | **PASS** |
| 1.5 | Length measured, not estimated | Word count reproduced three ways (842 / 842 / 851→846). The **rate** is not reproducible. Detail below. | **FAIL** |
| 1.6 | Recurring motifs have canonical plates or a plan | `STORYBOARD.md` is 4 lines, 0 beats, 0 named objects. `wc -l` = 4. No plate declared or planned; script contains a deliberate recurring object. | **FAIL** |

---

## 1.2 — the source audit, in detail

### Spot-audit 1 (passed): the Session 1 headline

Script: *"Five out of every six in the ChatGPT group could not."*

Paper, v1 l.1229 and v2 l.1474, identical, Question 3 (*Ability to Quote*), Session 1:

> "In the LLM-assisted group, 83.3 % of participants (15/18) failed to provide a correct
> quotation, whereas only 11.1 % (2/18) in both the Search-Engine and Brain-Only groups
> encountered the same difficulty."

15/18 = five out of six. **Verified against both versions.**

### Spot-audit 2 (FAILED): the Session 3 figure

Script: *"And that five-out-of-six figure is the first session only. By the third session the
paper puts it at six of eighteen."*

The two figures are not the same measure.

| Measure | Session 1, LLM group | Session 2 | Session 3 |
|---|---|---|---|
| **Question 3** — ability to quote at all | **15/18 failed** (v1 l.1229) | 2/18 (v1 l.1338) | **5/18** — "13/18 indicated being able to quote" (v1 l.1388, v2 l.1722) |
| **Question 4** — correct quoting | 18/18 failed — "None of the participants in the LLM group (0/18) produced a correct quote" (v1 l.1245) | 4/18 (v1 l.1343) | **6/18** (v1 l.1391, v2 l.1727) |

The script's "five out of six" is the **Q3** row. Its "six of eighteen" is the **Q4** row.
The sentence *"that five-out-of-six figure is … By the third session the paper puts it at
six of eighteen"* asserts they are one series. They are two.

The Director's own `Claims cut` table rejects *"Session 2 quoting failures were 4 of 18"*
on precisely this ground — "it is **Question 4** … while the 15/18 headline is **Question
3**". But 6/18 at Session 3 is the *same Q4 measure* as the 4/18 that was rejected. The
source table justifies it as "the paper's own like-for-like Discussion comparison". It is
not like-for-like; the paper's Discussion (v2 l.5180–82) commits the fusion itself:

> "83% of participants (15/18) **reporting difficulty quoting** in Session 1, and none
> providing correct quotes. This impairment persisted albeit attenuated in subsequent
> sessions, with 6 out of 18 participants **still failing to quote correctly** by Session 3."

"reporting difficulty quoting" is Q3. "failing to quote correctly" is Q4. The Director
inherited the paper's error by quoting the sentence that contains it. The check wins.

**Corroborating arithmetic.** Act 3 says *"It is about a third of the number you were
handed."* Against the script's own pairing (83.3% → 33.3%) that ratio is 0.40. Against the
like-for-like Q3 pairing (83.3% → 27.8%) it is exactly 0.33. The sentence the film wrote
fits the number the film did not use.

### The rest of the table, re-audited

The sample failed, so the sample became the population. All 21 rows:

| Row | Independently checked against | Result |
|---|---|---|
| 1 | v1 title page: Kosmyna, Hauptmann, Yuan, Situ, Liao, Beresnitzky, + Braunstein, Maes = 8 | OK — see note below |
| 2 | v2 l.138 "18 participants per group, 54 total"; v1 l.995 "Enobio 32 headset" | OK |
| 3 | v1 l.1037 "All the topics were taken from SAT tests"; l.1118 "within a 20 minutes time limit"; l.1011 "The Apple MacBook Pro" | OK |
| 4 | v1 methods, three group conditions | OK |
| 5 | dDTF directed connectivity | OK |
| 6 | Abstract, v1 + v2 | OK |
| 7 | v1 l.1229 / v2 l.1474 (spot-audit 1) | OK |
| 8 | `grep -c "Preprint, under review" brain_v2.txt` → **216** page footers | OK |
| 9 | v2 l.69–70 "We recruited a total of 54 participants for Sessions 1, 2, 3, and 18 participants among them completed session 4"; l.67–69 confirms the session-4 tool swap (LLM-to-Brain / Brain-to-LLM) | OK |
| **10** | **v1 l.1386–94 / v2 l.1722–27 vs l.5180–82** | **FAIL** |
| 11 | v1 l.1331 verbatim | OK |
| 12 | v2 l.5181 verbatim | OK |
| 13 | arXiv:2601.00856 abstract page opened: Stankovic, Hirche, Kollatzsch, Doetsch — 4 authors, "[v1] Mon, 29 Dec 2025" | OK |
| 14 | Same abstract, verbatim: "(i) study design considerations, including the limited sample size; (ii) the reproducibility of the analyses; (iii) methodological issues related to the EEG analysis; (iv) inconsistencies in the reporting of results" — and it does open "We sincerely congratulate Kosmyna et al." | OK |
| 15 | Crossref 10.1126/science.1207745: Sparrow, Liu, Wegner, *Science* 333:776–778, 2011 | OK |
| 16 | Hesselmann 2020 abstract describes the Exp-1 trivia→Stroop design as narrated | OK |
| 17 | Crossref 10.1038/s41562-018-0399-z: Camerer et al., *Nat Hum Behav* 2:637–644, "replicability of social science experiments in Nature and Science between 2010 and 2015" | OK |
| 18 | Hesselmann 2020 abstract, opened directly: the Google Stroop effect "could not be replicated in two recent replication attempts as part of a large replicability project. After the failed replication was published in 2018…" — peer-reviewed corroboration of the paywalled Camerer table | OK (secondary, disclosed) |
| 19 | Crossref 10.7717/peerj.10325: *"No conclusive evidence that difficult general knowledge questions cause a 'Google Stroop effect'. A replication study"*, PeerJ 8:e10325, 2020 | OK |
| 20 | Crossref abstract, Storm & Stone, *Psych Sci* 26:182–188: "saving one file before studying a new file significantly improved memory for the contents of the new file" | OK |
| 21 | Semantic Scholar abstract, Runge, Frings & Tempel, *Psychological Research* 85:1633–1644, DOI 10.1007/s00426-020-01341-0: "Across three experiments, we replicated and specified this saving-enhanced memory effect… In Experiment 3, a cost effect for saved verbal material was present, indicating that externally saving information can reduce the accessibility for this information afterwards" | OK |

**Note, not blocking (row 1).** *"It came out of the MIT Media Lab, where Nataliya Kosmyna
and seven colleagues…"* — the count is right, but three of the eight authors are not at the
Media Lab (Wellesley, MassArt, MIT proper). "Came out of the MIT Media Lab" is fair for the
study; "where … and seven colleagues" places all eight there. Director's call; the ear will
not catch it and no number moves.

---

## 1.3 — the persona line, in detail

This is the film most exposed to bucket 3 that has been written here, and it holds.

- **First-person singular:** none. `grep -Eo "\b(I|I'm|I've|I'd|my|mine|me)\b"` → no match.
- **Promises about the film:** none. `we will`, `we are going to`, `we won't`, `let us`,
  `stay with me`, `come back to`, `as we will see`, `in a moment`, `later in this film`,
  `our job`, `we made`, `we built`, `we wrote` → no match. The Director's removed line
  (*"We are not going to give you that"*) does not survive anywhere, and its replacement,
  *"It is not available."*, has no agent in it.
- **Credentials / expertise:** none. Only false-positive substring matches ("was a").
- **Advice register:** two sentence-initial imperatives, both examined:
  - *"Quote one line from the essay you just wrote."* — the interviewer's question inside
    the study, reported. Not the narrator addressing the viewer.
  - *"Take the thing you finished this week."* — the narrator directing attention to an
    example the viewer already has. No behaviour is prescribed, no outcome promised, no
    expertise claimed. Passes.
- **Closest approach, named for the record:** *"This film was written and drawn and read
  aloud by the machines it is about. We cannot get back inside it either."* This is the one
  place the "we" becomes the production rather than the culture. It states an **incapacity**,
  not an intention, a will, or a promise — it is a statement about the world, which is what
  the standing rule asks for. It passes, and it is the boundary. Any future line in this
  position that adds a verb of intent breaches.

---

## 1.1b — the "we" judgement, in detail

18 first-person-plural tokens, 21.28/1k against a ceiling of 22. Every one, in order:

| # | Line | Verdict |
|---|---|---|
| 1 | "Most of **us** have had that feeling and not said it out loud." | Earned — the recognition the act exists to make |
| 2–4 | "**We** have a machine that finishes **our** sentences now, and **we** have quietly started to wonder what that costs **us**." | Earned — the film's own position, stated before any evidence |
| 5 | "a paper told **us**." | Earned — the culture that received it |
| 6–7 | "**We** have all sent something **we** could not quote back an hour later." | Earned — deliberately absorbs the study's accusation before it lands on the viewer |
| 8 | "The study said preliminary. **We** heard proof." | Earned — the thesis in four words. The film's single best "we" |
| 9 | "**We** have done this before" | Earned — opens the turn |
| 10–12 | "…really doing for **us**. It was not helping **us** find out, it was helping **us** confirm." | Earned — the indictment, and it is of us, not of the researchers |
| 13–14 | "**We** had the feeling first, and then **we** went looking for a footnote." | Earned — the landing line |
| 15 | "the one that agreed with **us**" | Earned — names the bias in the film's own favour |
| 16 | "**We** cannot get back inside it either." | Earned — the self-indictment, and the hardest one |
| 17 | "how much of that **we** are carrying." | Earned — the close |

**Judgement: none is padding.** The distribution is the test and it passes it: the "we"
clusters in Act 1 (recognition), the last line of Act 3, and Acts 4–5 (confession) — the
three places the film is admitting something — and there is **not one "we" in the reporting
stretch** of Act 2 or in the Stankovic passage of Act 3, where a padded script would have
sprinkled them to buy headroom. The pronoun is doing the argument's work.

One structural observation, offered and not charged: the referent shifts at token 16 from
"us, the audience and the culture" to "us, the makers of this film". That shift is the
honest beat and it is load-bearing, but it is the one place a listener could stumble. It is
the Director's call, not a rubric failure.

---

## 1.4 — skeleton test, in detail

Done literally, in `scratchpad/skeleton.txt`. Eleven example/analogy sentences removed:
the "document, a plan, forty lines of code" list; the "not remembering the drive" analogy;
the three-group second-person assignment; the leading/following gloss; the interviewer's
question; "We have all sent something we could not quote back"; the Stroop description;
the Storm & Stone one-liner; "The file you saved gets harder to reach"; and the closing
"Take the thing you finished this week / The step in the middle that you did not take."

The remaining spine reads without a break. All bridges survive: *"Last June, a paper told
us."* → *"So here is what it was attached to."* → *"So something is there."* → *"We have
done this before…"* → *"That became the fact about technology and the mind…"* → *"So the
easy ending is…"* → *"So the question is probably not whether you remember…"*.

Three places the skeleton went rough — *"could not"* with its task removed, *"Your mind has
already gone looking for the machine"* with its experiment removed, *"Runge and colleagues
replicated **that**"* with its antecedent removed. In all three the sentence I deleted was
**content, not example**; those are false positives of my own cut, not fragile bridges.
**PASS.**

**One finding for the Director, tied to the trim question.** The Act 1 → Act 5 callback that
the treatment names as the room's best merge — *"the step in the middle that you did not
take"* — lives entirely inside the two sentences that a trim would classify as an example.
If a runtime cut ever reaches Act 5's last four sentences, the callback dies silently and
the register gate will not notice. The treatment already protects Act 5's *first* four
sentences; it should protect the last two as well.

---

## 1.5 — length, in detail

**Word count (mine, three ways):** whitespace split **842**; `[A-Za-z0-9][A-Za-z0-9'-]*`
**842**; the gate's own `[A-Za-z']+` tokenizer **846**. My first two agreed, the third
disagreed, so I ran a fourth to resolve rather than average: the gate splits 7 hyphenated
tokens into 16 parts (+9) and discards 5 bare numerals (−5). 842 + 9 − 5 = 846. Reconciled.
**The spoken count is 842, which is what the treatment states.** No defect here.

**The rate is the defect.** The treatment derives every timing from:

> "~115 wpm at ElevenLabs `speed: 0.75`, derived from 891 words → 7:46 on a prior film"

I could not reproduce that datum from anything in the repository, and what I did find
contradicts it:

| Measured artifact | Words | Duration | Rate |
|---|---:|---:|---:|
| `batman-effect/audio/transcript.json` (887 tokens) | 887 | narration ends **420.8s** | **126.5 wpm** |
| same words vs `audio/narration.mp3` | 887 | **401.7s** | 132.5 wpm |
| same words vs **film** `renders/batman-effect.mp4` | 887 | **466.6s (7:46.6)** | 114.7 wpm |
| `you-happen-to-life` script vs `words.json` | 1199 | 388.1s | 185.4 wpm |
| `you-watched-it-happen` script vs `words.json` | 1193 | 423.7s | 169.0 wpm |

The third row is the treatment's number. 891 ≈ 887 narration words; 7:46 = 466.6s is the
**total film runtime**, which includes everything after the last word. Dividing narration
words by film duration and labelling the result a *narration* rate ("~115 wpm at `speed:
0.75`") is the error. The film's actual read rate on that artifact is **126.5 wpm**.

Consequence, and it is not cosmetic:

- 842 words at the treatment's 115 wpm → **7:19** — over the 6–7 minute brief, which is why
  two trims are pre-nominated.
- 842 words at the measured narration rate of 126.5 wpm → **6:39** — inside the brief, and
  no trim is needed at all.

The act table's five spans and the whole "if the measured read runs long" section inherit
this. The treatment is right that Sound's measured read decides — but Gate 1 asks for a
runtime *derived at the measured house rate*, and this one was not.

---

## 1.6 — motifs, in detail

`videos/cognitive-debt/STORYBOARD.md` in full is four lines: a title, "One image per beat,
tagged to the narration line it sits under", and "Every recurring object gets its own
canonical plate BEFORE the batch." A correct rule and zero beats.

The check cannot pass on an empty board, and it is not merely early: the locked script
already contains at least one deliberate recurring object and the treatment's per-act
notes imply two more, none of which has a declared plate or a plan for one:

1. **The finished thing with the missing step** — Act 1 *"there was a step that you did not
   take"* → Act 5 *"The step in the middle that you did not take."* The treatment calls this
   callback the room's best merge. It is the film's principal motif and it is described only
   in words, which is the documented failure mode (a motif described in words drifts across
   the sheet).
2. **The apparatus** — the desk, the cap of sensors, the twenty-minute clock, named in the
   Act 2 intent note and recurring across Acts 2–3.
3. **The double object** — Act 5's "a gain and a cost in the same object, not two objects".

---

## Returns

### R1 — Item 1.2 · **Director** · PLAYBOOK: Gate 1.2 (source table) + the film's own `Claims cut` rule

The Session 3 quoting figure is Question 4; the Session 1 headline is Question 3. Fix by
either route:

- **(a)** replace *"six of eighteen"* with the like-for-like Q3 figure — **five of
  eighteen**, sourced at v1 l.1386–88 / v2 l.1722–24 ("13/18 indicated being able to
  quote"). This also makes *"about a third of the number you were handed"* arithmetically
  exact (27.8% / 83.3% = 0.33); or
- **(b)** keep 6/18 and name the measure change aloud, dropping the *"that five-out-of-six
  figure is…"* continuity framing.

Update source-table row 10 to cite the Session 3 body text rather than the Discussion
sentence, and record that the Discussion sentence itself fuses Q3 and Q4 — that is a fact
about the paper worth keeping.

**Fixed looks like:** row 10 cites a single question number across both sessions; the
script's two figures are the same measure; `register-profile.py --gate` re-run and passing.

### R2 — Item 1.5 · **Director** · PLAYBOOK: Gate 1.5 (measured, never estimated)

Restate the house rate from an artifact that exists, with the artifact named. If the rate is
narration words ÷ narration duration, it is **126.5 wpm** (`batman-effect/audio/transcript.json`,
887 tokens, ends 420.8s) and this script is **6:39** — inside the brief, no trim required.
If the intended quantity is total film runtime, say so explicitly and stop calling it wpm.

**Fixed looks like:** the treatment's rate line names the file and the two numbers it
divides; the act table's spans are recomputed from it; the "if the measured read runs long"
section states which of the two quantities the 6–7 minute target refers to.

### R3 — Item 1.6 · **Storyboard** · PLAYBOOK 10.9 (every motif gets its own plate)

Populate `STORYBOARD.md` with the beat list and the motion column, and declare a canonical
plate for each recurring object — minimum: the finished-thing-with-the-missing-step (Act 1
and Act 5 must be the *same object*, not two drawings of the idea), the study apparatus, and
Act 5's single double-sided object. One plate each, built before the batch.

**Fixed looks like:** `STORYBOARD.md` lists every beat with its narration line; a `PLATE`
column names a canonical plate for each object that appears in more than one beat; no
object appears twice without one.

---

## Not rubric items — reported as asked

**Would either pre-nominated trim breach the register band?** No. Both were built and gated:

| variant | words | you/1k | we/1k | Flesch | FK | exit |
|---|---:|---:|---:|---:|---:|---:|
| locked | 842 | 37.83 | 21.28 | 76.29 | 6.01 | 0 |
| trim 1 (drop the SAT/20-minute sentence) | 829 | 38.42 | 21.61 | 76.28 | 6.01 | 0 |
| trim 2 (shorten the Stankovic list) | 837 | 38.05 | 21.40 | 77.18 | 5.86 | 0 |
| both | 824 | 38.65 | 21.74 | 77.19 | 5.86 | 0 |

Both trims, singly and together, stay in band. But the treatment is right that the margin is
thin, and here is the number it should be holding: the script contains **18** first-person-plural
tokens, and the ceiling of 22/1k is breached below **819 gate-words**. After both trims the
script sits at **828**. **Nine further gate-words of "we"-free cutting breaches the ceiling.**
Trim 2 also drops FK grade to 5.86 against a floor of 5.6.

Given R2, the trims may not be needed at all — at the measured narration rate this script is
6:39. Do not cut on the 7:19 estimate until the rate is corrected.

---

## Item 3.4 — the listen gate

Not applicable at Gate 1 (no mix exists). Recorded here so it is not lost: **no human has
listened to this film. 3.4 is not satisfied and cannot be satisfied by any agent, including
this one.** It will be re-stated as outstanding at Gate 3.
