# BRIEF — Who You Measured

Working title. Breaks the `You ___` pattern that the first three films fell into,
and names the error the film is about rather than the subject.

## The thesis

Three fields spent decades explaining why people are the way they are — one with
a chemical, one with a gene, one with a sample. All three made **the same move**:
they took something measured in a narrow slice and reported it as a universal
cause. And all three failed in the same way, at roughly the same time, once
somebody checked at scale.

## The turn — and it is a single fact

**Heritability is not a property of a trait. It is a property of a population in
an environment.** Turkheimer et al. 2003 measured IQ in 7-year-old twins, many
near or below the poverty line: in impoverished families about **60% of the
variance is shared environment and the genetic contribution is close to zero; in
affluent families it is almost exactly the reverse.**

The same trait. The same measure. Two different numbers, because two different
rooms. That one fact dissolves the gene story and the sample story at once, and
it should land at roughly two-thirds.

## The three legs

**1 · THE CHEMICAL.** Dopamine is not the pleasure chemical. The research
tradition is about prediction and motivation — wanting rather than liking. The
pop version ("dopamine hits", "dopamine detox") inverts the finding while
borrowing its authority. *Verify: Schultz on reward prediction error; Berridge &
Robinson on wanting vs liking; the origin of "dopamine fasting" (Cameron Sepah,
2019, as a clinician's framing, not a research finding).*

**2 · THE GENE.** The candidate-gene era's flagship claims did not survive scale.
**Border et al. 2019** (*American Journal of Psychiatry*) took the 18 genes most
studied for depression — each with 10+ published studies — and tested them in
samples from **62,138 to 443,264** people. They were no more associated with
depression than randomly chosen genes. **VERIFIED.**

The bridge between leg 1 and leg 2 is literal, not rhetorical: `DRD4` and `DRD2`
are **dopamine receptor genes**, and they were the era's marquee candidates —
DRD4 as "the novelty-seeking gene". *Be careful here:* Munafò's meta-analysis
found the DRD4 association **survives for novelty seeking and impulsivity but
with significant publication bias and a failed replication at the trait
extremes**. That is contested-and-biased, NOT cleanly refuted. Board it honestly;
overstating it would be the film committing its own subject.

**3 · THE SAMPLE.** Henrich, Heine & Norenzayan 2010, *The weirdest people in the
world?* — roughly **96% of behavioural-science subjects come from Western,
Educated, Industrialized, Rich, Democratic societies, about 12% of humanity** —
and those subjects are frequently **outliers**, not a neutral default. The paper's
own reviewed domains include **the heritability of IQ**, so leg 3 was already
reaching for leg 2 in 2010. **VERIFIED.**

## The honest beat

House doctrine says retract your own strongest evidence. Here the retraction is
structural and unavoidable: **this film is written, boarded and narrated by
models trained overwhelmingly on WEIRD text.** The film's own instrument has the
defect the film is describing. Say it plainly, in the film, and do not soften it
into a joke.

Second honest beat, and the one that keeps this from being a debunk: **the science
did not vanish.** Heritability is real and large. Dopamine is real and central.
What collapsed was the *single* gene, the *single* feeling, and the *single*
sample standing in for everyone. A film that leaves the viewer thinking "so none
of it is true" has failed.

## Candidate landing

Not "distrust research". Closer to: a finding always comes with a population
attached, and the popular version is what you get when that population is
stripped off. The question to leave the viewer with is *who was measured* — which
is also the title.

## Constraints

- **Render: RISOGRAPH two-ink.** See `docs/video/WORLD-risograph.md`. Inks are
  **fluorescent pink + blue**, chosen structurally: the pop story is hot and
  about pleasure, the mechanism is cool and predictive, and the violet where the
  two inks overlap is exactly where the public confusion lives. The world is NOT
  locked until it survives a world test.
- **Stills only.** No motion clips on this film, by decision.
- `docs/video/VOICE-SPEC.md` — gate before boarding:
  `python3 tools/video/register-profile.py --gate videos/who-you-measured/script.txt`
  Band: "you" 35–58/1k, "we" 8–22/1k and never zero. This film needs "we" badly —
  the honest beat IS a confession.
- `docs/video/PLATFORM-POLICY.md` — the narrator is never a character, and on any
  health or medical claim the authority is the citation. This film touches
  psychiatry and IQ, which is the most sensitive ground we have worked on. Every
  number is named with its study, year and journal, in the film and in the source
  table.
- **IQ and heritability are live political territory.** Report what the studies
  found and who they measured. Do not editorialise beyond the evidence, and do
  not let the film be recruited by anyone's argument — the Turkheimer finding cuts
  against determinism, and saying so accurately is enough.
- Length: 6–7 minutes at the measured house rate (~178 script-words per minute of
  narration). Measured, never estimated.
- Films open cold: no intro (PLAYBOOK 10.31).
- Board against PLAYBOOK **10.38** from the first draft, not as a later pass:
  camera quota, an explicit expression per frame, and scale/posture exaggeration.
  `board-v2.py` in `videos/cognitive-debt/` is the working example.

## What Isaac wants back

`TREATMENT.md`: thesis in one sentence, the turn and its timecode, act table,
locked VO, a source table where every claim is marked verified, the register
line, and per-act intent.
