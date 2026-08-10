# THE PRICE OF A GLANCE
**A five-minute film on attention, behaviour science, and the social feed**

| | |
|---|---|
| Format | 16:9 · 5:00 · kernel.chat editorial |
| Engine | GALLEY (`:5412`) → fal.ai · ElevenLabs VO · Palmier Pro cut |
| Art direction | Comforting e-ink — warm risograph paper, soft grain, colour |
| Audio | ElevenLabs for everything — voice, score, sound design |
| Narrator | Daniel — Steady Broadcaster, `onwK4e9ZLuTAKqWW03F9`, `elevenlabs-v2` direct |
| Status | APPROVED 2026-07-23 · $16.10 · Director in citation pass |

---

## Editorial position

Most films on this subject are alarm bells. This one is a ledger.

The mechanisms are real, documented, and older than the products that use
them. The population-level harm is smaller and worse-measured than the
discourse admits. Both facts ship in the same film — the honest beat at
3:20 is the reason the rest of it can be believed. Count what gets read;
cut what doesn't; file the audit in public.

No scare footage. No faces. No doom. The film is calm on purpose: a calm
film about a system engineered to make you uncalm is itself the argument.

---

## Art direction — "comforting e-ink, in colour"

The world is **soft colour e-ink**: a warm, matte, paperlike surface with
gentle contrast and no gloss. Everything reads as calm and present-tense.
No noir, no volumetric drama, no glass-and-chrome futurism.

**NOT mid-century.** Isaac's note, 2026-07-23, and it supersedes the first
draft of this section. The earlier direction — risograph, field guide,
halftone, deliberate mis-registration, slate-and-sand palette — was
period pastiche, and it dated a film about a live argument. What we keep
from it is the *comfort*, the paper warmth, and the one-accent
discipline. What we drop is every signal that says "printed in 1958":

| Drop | Because |
|---|---|
| risograph, halftone dots, mis-registration | vintage print artifacts |
| "field guide", specimen plates, botanical framing | mid-century natural history |
| slate-teal + sand palette | the most dated pairing in the set |
| brass, punch cards, gramophones, antique apparatus | period props |

Contemporary and timeless instead: simple rounded forms, soft ambient
light, generous negative space, very fine paper grain rather than print
texture. Objects should be things that exist now or belong to no
particular decade.

**Palette:**

| Role | Hex | Use |
|---|---|---|
| Paper | `#FAF9F6` ivory | ground, always |
| Ink | `#1F1E1D` | line work, type, soft shadow |
| Accent | `#E24E1B` tomato | exactly one element per frame — the "reward" |
| Depth | `#7C93A6` soft blue | distance, shadow tone, cool relief |

Four colours, not five. A tighter palette reads contemporary; a wider one
starts to look like a period swatch card.

**Style block — prefix EVERY keyframe prompt with this verbatim:**

> Soft matte colour illustration on warm off-white paper, e-ink display
> aesthetic — paperlike, non-glossy, gentle low contrast. Contemporary
> and timeless, not retro, not vintage, not mid-century. Simple rounded
> forms, clean shapes, generous negative space, very fine paper grain.
> Soft ambient light with no harsh shadows. Limited palette: warm
> off-white ground, soft near-black line work, muted soft blue for depth.
> Exactly one small tomato-red element as the focal point. Calm,
> comforting, quiet. 16:9 composition. No halftone dots, no print
> registration marks, no visible screen pixels. No text, no lettering,
> no words, no numerals, no human faces.

**Motion direction — append to EVERY clip prompt:**

> Hold every shape crisp and unchanged; move slowly and only one thing
> at a time. Grain stays static like paper.

**Shot list needs an Art Director pass.** The 30 scene lines below were
written to the superseded mid-century direction and are full of period
props — an antique brass balance, field-guide birds, a gramophone, brass
calipers, an auction gavel. The *intent* of each shot stands; the objects
do not. Re-specify them contemporary before quoting the keyframe batch.

Two rules learned the hard way on the last two films: models garble
lettering, so all type is added in Palmier, never generated; and faces
break consistency across shots, so the film has hands and silhouettes
only.

---

## Audio plan — one house, three routes

Everything the film is heard through comes from ElevenLabs, so the publication
has one voice in the literal sense as well as the editorial one.

| Layer | Route | Price | Plan |
|---|---|---:|---|
| Narration | `elevenlabs-v2` direct, `eleven_multilingual_v2` | **$0 fal** (subscription credits) | recorded in seven act blocks, not one take |
| Score | `elevenlabs-music` | $0.80 per started minute | five 60s act beds |
| Design | `elevenlabs-sfx` | $0.10 per generation | eight cues + one room tone |

**Narration must pass `provider: "elevenlabs-v2"` explicitly.** The engine
default is `elevenlabs-turbo` — the fal-routed model, which sounds worse and
is the only speech route that bills fal dollars. The direct route needs
`ELEVENLABS_API_KEY` in the video-server process and a real voice id, not a
voice name.

**Five beds, not one long cue.** `elevenlabs-music` allows a single 300s
generation, and it would cost exactly the same $4.00 as five 60s beds. The
beds win anyway: the score turns with the acts, a bad note costs $0.80 to
retake instead of $4.00, and the Editor gets crossfade points instead of a
monolith to fight.

Score intent per act — the film is comforting, so the score stays under the
voice throughout and never announces a beat:

| Act | Bed intent |
|---|---|
| I — the arithmetic | warm, slow, a room being settled into; almost nothing |
| II–III — the mechanism | a quiet pulse enters, patient rather than tense |
| IV — the cost | thins out; the film gets lonelier without getting darker |
| V — the honest number | air and space, the sound of a claim being set down |
| VI–VII — tribe and close | the warmth of act I returns, resolved |

Design cues land only where picture has a physical event: paper turn, the
lever, the bead settling, the scroll unrolling, the dial. Plus one 22s room
tone laid full-length so the quiet has texture rather than being digital
nothing.

---

## Full VO script — 690 words · ≈ 4:50 with pauses

> **ACT I — THE ARITHMETIC · 0:00–0:38**
>
> "In 1971, an economist named Herbert Simon wrote a sentence that has
> aged into a description of your afternoon. A wealth of information, he
> said, creates a poverty of attention.
>
> He was not complaining. He was doing arithmetic. Information consumes
> attention. So an abundance of the first must produce a scarcity of the
> second. And a scarcity is a thing that can be priced.
>
> Fifty-five years later, that price has a market, a buyer, and a
> settlement time measured in milliseconds."

> **ACT II — WHAT DOPAMINE ACTUALLY DOES · 0:38–1:28**
>
> "You have heard that your feed gives you a dopamine hit. That is close
> enough to be useful, and wrong enough to matter.
>
> In 1997, Wolfram Schultz and his colleagues published the finding that
> reorganised the field. Dopamine neurons do not fire for pleasure. They
> fire for surprise — specifically, for the gap between the reward you
> expected and the reward you got. Reward prediction error.
>
> A reward you fully expect produces almost nothing. A reward you could
> not have predicted produces a spike.
>
> Read that twice, because it is the entire design brief. The system is
> not tuned to make you happy. It is tuned to keep you uncertain."

> **ACT III — THE PLAYBOOK · 1:28–2:30**
>
> "Uncertainty is a schedule, and the schedule has a name. B. F. Skinner
> called it variable ratio reinforcement. Reward the behaviour — but not
> every time, and never on a pattern the animal can learn.
>
> It is the most extinction-resistant schedule ever measured. The pigeon
> that is fed sometimes keeps pecking long after the pigeon that is fed
> always has given up.
>
> Now count the variable-ratio surfaces on your phone. Pull to refresh —
> a slot machine lever with a better return policy. The red badge, which
> carries no information except that something happened. And the scroll
> with no bottom, which quietly removes the one thing every page used to
> give you: a place to stop.
>
> The engineer who built infinite scroll has spent years publicly
> regretting it. He shipped a surface with no natural end, and the
> industry copied it inside of eighteen months."

> **ACT IV — THE COST, MEASURED · 2:30–3:20**
>
> "So what does it cost you? Not in outrage. In measurements.
>
> Sophie Leroy, two thousand nine: switch tasks with the first one
> unfinished, and part of your attention stays behind. She called it
> attention residue. Your performance on the next task drops — and you do
> not notice, because the capacity you are missing is the capacity you
> would have used to notice.
>
> Adrian Ward and colleagues, two thousand seventeen: participants sat
> cognitive tests with a phone on the desk. Face down. Powered off.
> Available working memory measurably fell. Not from using it. From it
> being within reach.
>
> The phone does not have to interrupt you. It only has to be reachable."

> **ACT V — THE HONEST NUMBER · 3:20–4:05**
>
> "Here is where a film like this usually lies to you. We won't.
>
> In two thousand nineteen, Amy Orben and Andrew Przybylski ran the
> specification curve — every defensible analysis, all at once, across
> three large datasets. The association between digital technology use
> and adolescent wellbeing came back negative, real, and tiny. Comparable
> in size to the association with eating potatoes.
>
> That is not a defence of the industry. It is a correction to the
> discourse. The mechanisms are real and well documented. The
> population-level effect is small and badly measured. Both are true —
> and only one of them sells a documentary."

> **ACT VI — THE TRIBE AT SCALE · 4:05–4:35**
>
> "The part that is not small is comparison. Leon Festinger, nineteen
> fifty-four: people evaluate themselves against others, and where there
> is no objective standard, they will use whoever is nearby.
>
> Your brain evolved to run that comparison against roughly a hundred and
> fifty people. It is now running it, continuously, against an
> algorithmically ranked selection of everyone's best day."

> **ACT VII — THE CLOSE · 4:35–5:00**
>
> "None of this is a conspiracy. It is a business model, and it is
> legible in the filings. Attention, sold by the second, to the highest
> bidder, with your uncertainty as the raw material.
>
> You cannot willpower your way out of a reinforcement schedule. But you
> can change the schedule. Kill the badge. Make the reward predictable.
>
> A boring machine is a machine you can put down."

---

## Sources cited in VO (all real, all checkable)

| Beat | Source |
|---|---|
| Poverty of attention | Simon, H. (1971), *Designing Organizations for an Information-Rich World* |
| Reward prediction error | Schultz, Dayan & Montague (1997), *Science* 275:1593 |
| Variable ratio schedules | Ferster & Skinner (1957), *Schedules of Reinforcement* |
| Infinite scroll regret | Aza Raskin, widely reported public statements |
| Attention residue | Leroy, S. (2009), *Organizational Behavior and Human Decision Processes* |
| Phone brain drain | Ward, Duke, Bos & Bos (2017), *JACR* 2(2) |
| Specification curve | Orben & Przybylski (2019), *Nature Human Behaviour* 3:173 |
| Social comparison | Festinger, L. (1954), *Human Relations* 7(2) |
| ~150 relationships | Dunbar, R. (1992) |

Verify every one before the film ships. A film whose thesis is
"measure it honestly" cannot carry a soft citation.

---

## Shot list — 30 generated clips + 7 built cards

> **Card copy below is SUPERSEDED.** The header previously said 12 cards
> against a list of 7; the list was right and the count was mine. Corrected
> 2026-07-23.
>
> `TREATMENT.md` is now canonical for all card copy — C2, C3, C4, C5, C6 and
> the colophon were all rewritten after the citation pass and the writers'
> room, and the versions in the table below are the pre-verification drafts.
> They are kept only so the shot slots read in context. Set type from the
> treatment, never from here.
>
> The shot *scene prompts* below are also superseded by `FRAME-BOOK.md`,
> which carries the contemporary re-specification. Intent is unchanged.

All clips: `seedance-lite`, 5s, image-to-video from a nano-banana-2
keyframe. Palmier holds/ramps each to its slot length. Cards are built
free in Palmier (type on ivory, house fonts) and carry the numbers —
because the models cannot draw numbers.

### Act I — the arithmetic

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 1 | 0:00–0:10 | a single small tomato-red paper flag planted in a vast empty ivory field of soft printed grain, seen from far above | the field breathes almost imperceptibly; extremely slow push in on the flag |
| 2 | 0:10–0:19 | an antique brass balance scale on a wooden desk, one pan heaped with tiny printed paper slips, the other holding one small red bead | the heaped pan settles slowly downward; slips shift once |
| 3 | 0:19–0:28 | an overhead flat-lay of hundreds of tiny printed cards fanned across a table like a tide, one red card face-up among them | slow lateral drift across the tide of cards |
| C1 | 0:28–0:38 | **CARD** — "A wealth of information creates a poverty of attention." / *Herbert Simon, 1971* | wordReveal, ivory ground |

### Act II — reward prediction error

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 4 | 0:38–0:47 | cross-section diagram of a single neuron drawn as a warm printed field-guide illustration, one red synaptic point glowing | the red point pulses once, softly; everything else still |
| 5 | 0:47–0:56 | two identical wooden feeding bowls side by side on paper, one with a small red seed, one empty, soft cast shadow | a hand-shadow passes over both; the red seed glows faintly |
| 6 | 0:56–1:06 | a printed line graph rendered as embroidery on paper, flat and level, with one sharp red spike rising at the far right | the flat line draws in left to right, then the red spike jumps |
| 7 | 1:06–1:16 | a wrapped parcel on a doorstep in soft printed light, its red string half-untied, contents unknown | the string sways once; nothing opens |
| C2 | 1:16–1:28 | **CARD** — "Not pleasure. Surprise." / *reward prediction error · Schultz et al., 1997* | popIn |

### Act III — the playbook

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 8 | 1:28–1:37 | a small wooden mechanical lever with a red knob mounted on a printed panel, gears visible behind cut-away paper | the lever pulls down once and springs back |
| 9 | 1:37–1:46 | two printed field-guide birds on separate perches inside soft paper cages, a scatter of red seeds beneath only one | the seedless bird keeps pecking; the fed bird sits still |
| 10 | 1:46–1:55 | macro of a paper card being pulled downward and released, springing back up, a red arrow curving around it | the card pulls down and snaps back once |
| 11 | 1:55–2:04 | a single small red dot on a vast empty ivory page, tiny and insistent, enormous negative space | the dot pulses gently three times |
| 12 | 2:04–2:13 | a long paper scroll unrolling downward off the edge of a wooden table, pooling endlessly on the floor, no visible end | the scroll unrolls continuously downward at constant speed |
| 13 | 2:13–2:22 | a printed staircase that continues past the bottom edge of the page with no landing, soft grain, one red step | slow downward tilt following the stairs, never arriving |
| C3 | 2:22–2:30 | **CARD** — "Variable ratio. The most extinction-resistant schedule ever measured." | typewriter |

### Act IV — the cost

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 14 | 2:30–2:39 | a cup of tea on paper with a red thread leading away from it out of frame, the thread taut | the thread pulls taut; the cup does not move |
| 15 | 2:39–2:48 | two open printed books side by side, a soft red smudge of ink transferred from the left page onto the right | the smudge spreads very slightly on the right page |
| 16 | 2:48–2:57 | a printed measuring jug of warm liquid, clearly filled below its marked line, one red graduation mark | the level lowers a fraction and settles |
| 17 | 2:57–3:06 | a small flat rectangle lying face-down on a wooden desk beside an open notebook, a faint red halo printed around it | the halo breathes slowly; nothing else moves |
| 18 | 3:06–3:14 | a hand-shadow reaching across paper toward the face-down rectangle and stopping short | the shadow reaches and holds, does not arrive |
| C4 | 3:14–3:20 | **CARD** — "It does not have to interrupt you. It only has to be reachable." | wordReveal |

### Act V — the honest number

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 19 | 3:20–3:29 | thousands of tiny printed dots forming a soft grey cloud on ivory, a single red dot near the centre | the cloud settles imperceptibly; the red dot holds |
| 20 | 3:29–3:38 | a printed field-guide potato rendered with great seriousness on a specimen card, one red pin through its corner | the pin glints once; the card sits perfectly still |
| 21 | 3:38–3:47 | a set of brass calipers measuring something almost too small to see on printed paper, red measurement tick | the calipers close very slightly and stop |
| 22 | 3:47–3:56 | a printed forest of thin identical grey trees with one red-leafed tree barely distinguishable among them | soft parallax drift; the red tree stays centred |
| C5 | 3:56–4:05 | **CARD** — "Real. Documented. And smaller than you were told." | popIn |

### Act VI — the tribe at scale

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 23 | 4:05–4:13 | a warm printed campfire circle of small seated paper silhouettes, close together, one holding a red ember | the ember glows; the circle is still and companionable |
| 24 | 4:13–4:21 | the same campfire circle repeated and tiled into an enormous grid receding to the horizon, thousands of circles | slow pull-back revealing the grid extending endlessly |
| 25 | 4:21–4:29 | a printed hand-mirror lying on paper reflecting not a face but a grid of tiny bright windows, one red | the windows flicker gently in the reflection |
| C6 | 4:29–4:35 | **CARD** — "Built for one hundred and fifty. Running against everyone." | wordReveal |

### Act VII — the close

| # | Slot | Keyframe scene prompt | Motion |
|---|---|---|---|
| 26 | 4:35–4:42 | a printed auction gavel resting on a ledger page ruled with fine lines, a red ribbon bookmark | the ribbon settles; the gavel does not fall |
| 27 | 4:42–4:48 | a hand-shadow turning a small wooden dial from a red setting to a plain one on a printed panel | the dial turns once, decisively, and stops |
| 28 | 4:48–4:53 | the small red dot from shot 11 fading to soft grey on the same vast ivory page | the red drains slowly to grey; the page stays warm |
| 29 | 4:53–4:57 | the flat rectangle face-down on the wooden desk, a warm cup beside it, evening light on paper | dust drifts slowly in the warm light; total stillness |
| 30 | 4:57–5:00 | wide printed view of the whole desk, tidy and warm, one small red bookmark in a closed book | the light warms fractionally; hold |
| C7 | over 30 | **COLOPHON** — "thirty shots · one voice · nine cited papers · rendered for about eleven dollars — owned outright" | typewriter |

---

## Cost — real estimates pulled from GALLEY, 2026-07-22

| Line | Unit | Qty | Total |
|---|---:|---:|---:|
| Keyframes — `fal-ai/nano-banana-2` | $0.08 | 30 | **$2.40** |
| Keyframe retakes (allowance) | $0.08 | ~10 | **$0.80** |
| Clips — `seedance-lite` 5s image-to-video | $0.20 | 30 | **$6.00** |
| Clip retakes (allowance) | $0.20 | ~5 | **$1.00** |
| Narration — `elevenlabs-v2` direct, ~4,300 chars | $0.00 | 1 | **$0.00** |
| Score — `elevenlabs-music` 60s act beds | $0.80 | 5 | **$4.00** |
| Sound design — `elevenlabs-sfx` cues + room tone | $0.10 | 9 | **$0.90** |
| Audio retakes (allowance) | — | — | **$1.00** |
| Palmier cut, type, cards, grade, mix, export | $0 | — | **$0.00** |
| | | **Total** | **≈ $16.10** |

Narration bills ElevenLabs subscription credits rather than fal, so it is
$0.00 against the fal cap but is not free — it still passes the approval gate.

Optional upgrade: promote the eight hero shots (1, 6, 12, 18, 22, 24, 28,
30) to `kling-pro` at $0.35/5s for smoother motion — **+$1.20**.

**Blockers, both needing Isaac:**

1. The engine's daily cap is `$10` and `$5.21` is already spent today.
2. `ELEVENLABS_API_KEY` must be in the video-server process for the direct
   narration route, and a real ElevenLabs voice id must be chosen.

Both are fixed by one restart:

```bash
kill $(lsof -ti :5412); cd "/Users/isaachernandez/blog design"; FAL_DAILY_SPEND_LIMIT=30 ELEVENLABS_API_KEY="$EK" npm run video-server
```

---

## Production order

1. Raise the cap and supply the ElevenLabs key; confirm `GET /health` shows
   `ok` and `hasKey`.
2. **Director** verifies all nine citations, files `TREATMENT.md`.
3. **Sound pass one** — cast the voice, record the seven act blocks on
   `elevenlabs-v2`, measure the real durations. Every shot slot below is
   re-derived from those measurements, not from the script estimate.
4. Estimate → approve → generate all 30 keyframes as one batch.
4. **REVIEW GATE:** look at all 30. Check palette discipline (one red
   element), paper texture consistency, and that no lettering crept in.
   Frames are $0.08; clips are $0.20 — retake freely here, not later.
6. Estimate → approve → generate 30 clips as one batch, image-to-video
   from each keyframe's fal `sourceUrl`.
7. **Sound pass two** — score the five act beds and the nine design cues
   against locked picture. Deliver separate stems, never pre-mixed.
8. **Editor**: import, lay narration at frame 0, `get_transcript` at word
   granularity, auto-cut to the transcript, build the 7 cards, ivory
   matte `#FAF9F6` on the bottom track so every fade breathes to paper,
   then mix the stems under the voice.
9. QC: gap check, ffprobe duration ≈ 300s, extract 8 frames, inspect.
10. Export 16:9 master, then the 9:16 social edition — hook in the first two
    seconds, burned-in captions, type inside the safe band. Cut only;
    publishing goes through Channel Studio's approval register.
11. Log the actual ledger in `LEDGER.md` and `SCRATCHPAD.md`; commit.
