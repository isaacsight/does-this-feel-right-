# HUMAN-VOICE — the research behind the humanity gate (law 15)

Commissioned by Isaac 2026-08-11: "the writing needs to feel more human than
AI — it's already great, needs slight improvement." Two studies: the
published stylometrics of AI-vs-human prose, and an empirical comparison of
our four shipped scripts against 81 School of Life transcripts (the corpus
Isaac named as the feel-like-I'm-there-with-them standard).

## What the measurements found (ours vs the masters, per equivalent text)

| dimension | masters | our four films | verdict |
|---|---|---|---|
| snap reversals ("X isn't Y. It's Z.") per 1k | 0.40 | 0.6 → 2.3 → 1.6 → 4.2 | our #1 machinery, worsening monotonically |
| triplet lists per 1k | 1.9 | 2.9–4.2 | double the masters |
| sentences ≥30 words | **16%** | 6–8% | THE missing organ — see below |
| questions (% of sentences) | 3.7% | 3.5 → 3.3 → 0.0 → 0.9 | we stopped asking |
| friction markers per 1k | 0.35 | ~0 | frictionless = generated |
| very short sentences (≤5 words) | 10% | 15–21% | we over-snap |

The published literature agrees on the frame: AI text shows low burstiness
(uniform sentence lengths), formulaic discourse markers, and uniform
structural rhythm; combined stylometric features detect it at F1 ≈ 0.94, with
sentence-length statistics among the most important features. Our corpus
study just makes it specific to THIS voice.

## The five techniques (room-brief law, every episode)

1. **The unspooling sentence.** At least one genuinely long sentence
   (35–50 words) per act — a thought that wanders through subordinate
   clauses and comes home, the way a person talks when they're working
   something out. This is the single highest-leverage change: the masters
   run long sentences at twice our rate, and it is where human thinking is
   audible. The register gate's 13–20 mean still holds — long sentences are
   paid for with short ones, which raises true burstiness.
2. **Ask the room questions.** 2–4% of sentences are questions — not
   rhetorical tics but genuine turns to the listener ("So what was the hand
   on his shoulder made of?"). Questions are what make narration company
   rather than broadcast.
3. **Retire the reversal.** "X isn't Y. It's Z." at most 2–3 per film, each
   earning its place. When the twist instinct fires, reach for other shapes:
   the delayed subject, the list that breaks its own pattern, the sentence
   that simply states the fact and stops.
4. **One snag per film, minimum.** A self-interruption ("Well — the skeleton
   is"), a mid-thought correction ("call it forty — no, call it what the
   study called it"), one aside that goes nowhere on purpose. Humans snag;
   the snag is trust.
5. **The non-load-bearing particular.** Each act carries one specific the
   claims allow but didn't supply — the 7:40 showing, a Tuesday-night
   league, the third-floor window. AI defaults to categorical nouns;
   humans remember particulars.

## Enforcement

`tools/video/slop-lint.py --gate` runs after the register gate, before
boarding. Ten checks: snap cap (4 and ≤1.5/1k), signpost-repeat cap, triplet
cap, house-word caps (quietly ≤2, small ≤5), ≥3 non-epigram act closes,
act-length CV ≥0.18, long-sentence floor ≥10%, question floor ≥2%, friction
floor 1 (warn). Even the catalog's cleanest script fails the corpus floors —
by design. Fix the script, never the caps.

## Sources

Stylometric/burstiness literature: ResearchGate "Sentence Structure in Human
and AI-Generated Texts"; "Feature-Based Detection of AI-Generated Text"
(combined stylometric+perplexity features, F1 0.94, sentence-length among
top features); arXiv 2601.07974 on detector generalization through
linguistic analysis. Corpus: transcripts/the-school-of-life/ (81-file
sample, seed 7), measured 2026-08-11.
