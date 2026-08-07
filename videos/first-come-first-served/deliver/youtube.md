# YouTube package — First Come, First Served

Master: `build/first-come-first-served-master.mp4` — 7:56, 1920x1080, 133 frames.
Thumbnail: `deliver/thumbnail.png` — 1280x720, checked at 320px.
Shorts: `deliver/shorts/` — four, with burned-in karaoke captions and SRT sidecars.

Nothing here is published. Uploading, pinning and scheduling are outward-facing
and need Isaac's explicit go.

## Title

**Why Nobody Stops the Man Who Cuts in Line**

Alternates, in the order I'd try them:

1. Why Nobody Stops the Man Who Cuts in Line
2. The Entire Justice System Is One Small Noise
3. Scientists Cut Into 129 Real Queues. Almost Nobody Stopped Them.
4. The Cheapest Institution in the World

Why 1: it names the thing the viewer has personally experienced and withholds
the answer. Title 3 is the strongest curiosity gap but leads with the study
rather than the feeling, and this episode's hook is the body reacting before
the brain does. Title 2 is the best line in the film and the worst title —
it means nothing until you have watched it.

## Description

> Somebody steps into the line ahead of you and your body reacts before your
> brain does. Your temperature changes. You can hear your own heartbeat. You
> are now doing arithmetic about roughly forty seconds.
>
> The queue has no police force. Nobody signed it. There is no penalty for
> breaking it and no court that will hear the case — and it holds anyway.
>
> In 1986 Stanley Milgram sent researchers into 129 real waiting lines in New
> York and had them cut in. Only about 10% of the time did anybody physically
> stop them. About half the time somebody reacted — a look, a tut, an
> eye-roll — and then let them stay. With two intruders instead of one,
> objection jumped to about 91%.
>
> So the enforcement arm of the fairest system we have is a small disapproving
> noise made with the tongue, followed by nothing. This is a film about why
> that is not a failure.
>
> ---
>
> SOURCES
>
> Milgram, Liberty, Toledo & Wackenhut (1986), "Response to Intrusion into
> Waiting Lines," Journal of Personality and Social Psychology 51(4), 683–689.
>
> Thomas Carlyle, The French Revolution: A History (1837) — the first written
> description of a queue in English, describing Parisians during the bread
> shortages standing in "Queues, or Tails ... so that the first-come be the
> first served."
>
> Joe Moran on the queue as a product of urbanised industrial societies.
>
> Allon & Hanany, "Cutting in Line: Social Norms in Queues" (Wharton).
>
> This film does NOT claim the British invented queueing. The first written
> description is of a French queue, written by a Scot.
>
> ---
>
> CHAPTERS
> [paste deliver/chapters.txt here]
>
> ---
>
> Made by KERNEL PRESS. Narration is synthetic; the script, the research and
> the frame book are written. Every factual claim in this film is sourced in
> the pinned comment.

## Chapters

In `deliver/chapters.txt`, computed from the script's act boundaries — 17 of
them, first at 0:00, none shorter than 20 seconds.

## Pinned comment

> Sources, in order of appearance:
>
> • Carlyle's 1837 description of Parisians queueing for bread — The French
>   Revolution: A History. The phrase in the film is his: "so that the
>   first-come be the first served."
> • Joe Moran on the queue arriving with railways, factories and dense cities
>   rather than with good manners.
> • Milgram, Liberty, Toledo & Wackenhut (1986), "Response to Intrusion into
>   Waiting Lines," JPSP 51(4), 683–689 — the 129 queues, the ~10% who
>   physically intervened, the ~50% who reacted and let it go, and the jump to
>   ~91% with two intruders.
> • Allon & Hanany (Wharton), "Cutting in Line: Social Norms in Queues."
>
> One thing the film is careful about: it does not claim the British invented
> queueing. That is a national self-image, not a finding.

**Pinning is Studio-only.** The API can post this comment but cannot pin it.
Four films now carry an unpinned sources comment because that step was assumed
rather than checked — do it by hand in Studio immediately after upload.

## Tags

queue, queueing, waiting in line, line cutting, queue jumping, Stanley Milgram,
Milgram experiment, social norms, social psychology, unwritten rules, Thomas
Carlyle, French Revolution, Joe Moran, British queueing, civility, fairness,
first come first served, behavioural science, KERNEL PRESS

## Shorts

Four, which is the ceiling — measured, bursts of eight lose 81% of views to
self-competition while bursts of four lose about 4%. Cadence is 2 per 24h
across ALL films, enforced by `tools/publish/cadence.mjs`; do not bypass it.

| file | length | opens on | kicker |
|---|---|---|---|
| 01-the-noise | 21.4s | "That tiny cowardly noise is not a failure." | THE NOISE IS THE SYSTEM |
| 02-two-intruders | 27.8s | "And then Milgram tried one more thing…" | TWO PEOPLE BREAKS IT |
| 03-ten-percent | 18.8s | "And the queues held, but barely…" | ONLY 10% STOPPED THEM |
| 04-your-turn | 19.2s | "But the next time you're third in a queue…" | IT'S YOUR TURN |

Every in- and out-point is snapped to a sentence boundary in `audio/words.json`,
not to an estimated beat map — five of six shorts on an earlier film opened
mid-word because they were cut from estimates.

Suggested short description, all four:

> From "Why Nobody Stops the Man Who Cuts in Line" — full film on the channel.
> Source: Milgram et al. (1986), Response to Intrusion into Waiting Lines.

## Still to do, and only Isaac can do it

- Pin the sources comment (Studio only).
- Unpublish the auto-caption track and upload the SRT, so YouTube does not
  serve an ASR transcript that mangles "Carlyle" and "Milgram".
- Add the film to the playlist (PLck9Xx5O7sBY) and set end screens.
