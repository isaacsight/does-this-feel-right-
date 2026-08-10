# THE LAST THING THAT HAPPENS — locked script

**Short.** ~50s. Single beat. Vertical 1080×1920.
**Voice:** Davis — ElevenLabs `Z2fsAwk7IblvPhYzfslC`.
**Template:** [`docs/video/SHORTS-TEMPLATE.md`](../../docs/video/SHORTS-TEMPLATE.md)

Runs ~50s rather than 45s. The template allows it: explainer content tolerates
+5–10s over entertainment's ceiling, and what kills an explainer is a slack
opening, not a long middle. The hook lands at 0.0s.

## The claim, and where it comes from

Kahneman, D., Fredrickson, B. L., Schreiber, C. A., & Redelmeier, D. A. (1993).
*When More Pain Is Preferred to Less: Adding a Better End.*
**Psychological Science, 4(6), 401–405.**

Verified 2026-07-24 against the paper as hosted by the University of Zurich
Faculty of Law, and against the SAGE record. Design and figure both confirmed:

- **Short trial:** one hand in **14°C** water for **60 seconds**.
- **Long trial:** the other hand, **14°C for 60 seconds**, then **30 seconds
  more** while the water is raised to **15°C** — still painful, marginally less.
- The long trial is *strictly worse*: it contains all of the short trial's
  discomfort plus thirty additional seconds of it.
- Asked which to repeat, **69% chose the long trial.**

Two things the script must NOT say, because the paper does not support them:

- That the extra 30 seconds were *pleasant*. They were not — 15°C is still cold.
  The finding is about a *less bad* ending, not a good one.
- That duration is ignored entirely. The paper says duration plays a **small**
  role, not no role. "Duration neglect" is the term of art, and it overstates.

## VO — locked. Captions take this text, not the ASR's.

> You can make a bad experience feel *less* bad by making it longer.
>
> That's not a typo. It's a bucket of cold water and a Nobel prize.
>
> Kahneman's team had people hold one hand in fourteen-degree water for sixty
> seconds. Unpleasant.
>
> Then a second round. Same sixty seconds — plus thirty more, while the water
> came up by a single degree. Still cold. Just slightly less awful right at the
> end.
>
> So round two is strictly worse. Same pain, plus extra pain.
>
> Then they asked which one people would rather do again.
>
> Sixty-nine percent picked the longer one.
>
> Because your memory doesn't add up the seconds. It keeps two snapshots — the
> worst moment, and the last one.
>
> Which means the end of a thing is doing far more work than the middle. The
> last day of a holiday. How an argument finishes.
>
> You're not remembering it. You're remembering the highlights.

~140 words. At conversational pace, ~50 seconds.

Proper nouns for the caption pass: **Kahneman**. ASR will render it "Conaman",
"Karnahan", or similar every time.

## Frame book — 17 frames, every one different

Hero is the established stick figure, reference-conditioned via
`nano-banana-2/edit` with `params.image_urls`. Situations, not symbols. Camera
held over the subject, never "calm, comforting, quiet" in the style block —
those nine words caused three rebuilds on the last film.

| # | Hold | Frame |
|---|---|---|
| 1 | 3.0 setup | Hero seated at a plain table, one hand submerged in a steel bucket, expression flat. Camera square on. |
| 2 | 2.2 quick | Tight on the bucket. Ice, and a thermometer reading fourteen. |
| 3 | 1.8 snap | Hero's face. Mildly betrayed. |
| 4 | 3.4 setup | Wide: a researcher with a clipboard, watching. Hero small in the room. |
| 5 | 2.0 quick | A stopwatch mid-sweep. |
| 6 | 3.4 setup | Hero still in the bucket. Thermometer now fifteen. One apologetic wisp of vapour. |
| 7 | 2.2 quick | Hero looking at the thermometer, wholly unmoved by one degree. |
| 8 | 3.2 setup | Two buckets side by side. Hero deliberating, chin in hand. |
| 9 | 1.6 snap | Hero pointing, confidently, at the worse one. |
| 10 | 3.0 setup | A crowd of hero figures. Roughly seven in ten stand on the worse side. |
| 11 | 2.4 quick | The three hold-outs on the other side, looking around, uncertain. |
| 12 | 3.4 setup | Hero's head in cross-section. Inside: two polaroids on a wire, nothing else. |
| 13 | 3.0 setup | The two polaroids close. One a howl. One a shrug. |
| 14 | 2.8 quick | A long strip of film. Two frames in colour, the rest blank. |
| 15 | 3.2 setup | An airport gate. Hero sunburnt, holding a bag, last day of a holiday. |
| 16 | 3.0 setup | Two figures finishing an argument. One at a door, one half-waving. |
| 17 | 3.4 breath | Hero alone, watching a small projected reel of two images, looping. |

**Total ~47.0s of picture** against ~50s of VO — the last frame carries the
sign-off and holds slightly longer in the cut.

## Estimate

17 frames × ~$0.08 = **~$1.36** image generation.
Narration via ElevenLabs. No score — the last film's sound held up unscored.
