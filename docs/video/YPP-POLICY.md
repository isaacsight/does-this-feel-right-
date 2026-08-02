# YPP — what we will and will not ship

Standing constraints for every GALLEY film and every social edition cut from
one. Written 2026-08-02 from YouTube's own clarification of the policy formerly
called "inauthentic content" (Matt Koval, YouTube Creator Insider, 2026-08).

**The policy did not change; the language did.** YouTube replaced the catch-all
"inauthentic content" with three named buckets. Nothing here is a guess about
enforcement — it is their wording, plus what it means for how we work.

**Two things to hold on to before the detail:**

1. **YPP is judged on the CHANNEL, not the video.** "We look at the channel as a
   whole." A defensible video inside an indefensible upload pattern does not
   help.
2. **YouTube is explicitly agnostic to tools.** "If you make it with genAI
   great, if you make it without genAI that's great too... our policies are
   independent of how the content is made." Generated imagery is not the
   exposure. What the channel looks like in aggregate is.

---

## Bucket 1 — generic and repetitive

> "Made with templates and there's not much variation from video to video."
> "Lots of videos really quickly that are very similar... don't really have a
> narrative arc and don't really show your creativity."

**This is our only real exposure, and it is a cadence problem, not a content
problem.**

The films are not at risk: original script, distinct narrative arc, primary
sources cited on screen and in the pinned comment, register-gated before
boarding. That is close to a description of what the policy asks for.

The shorts are. On 2026-08-01 the channel published **fourteen verticals in
forty-eight hours** — same visual treatment, same caption system, same
structure, cut mechanically from two films. Each one was a distinct argument.
The channel's recent history still read as the exact shape the policy names.

### Rules

- **Ship at most two shorts per rolling 24 hours, across all films.**
  Enforced by `tools/publish/cadence.mjs`; on by default in
  `tools/publish/index.mjs`. Overriding it is a deliberate act
  (`--per-day N` / `--no-cadence`), not a default.
- **Never publish a queue in one run.** The queue is a backlog to drip, not a
  batch to drain.
- **Every short carries its sources.** "Full film, with sources: <url>" in the
  description and the pinned comment. This is the single clearest signal that a
  video is not farmed.
- **Two shorts from the same film never go out on the same day.** Adjacent
  passages in one house style are what "very similar" means.

---

## Bucket 2 — off-putting, distressing, emotionally manipulative

> "An animal in distress... someone comes and saves the animal." "Putting minors
> in distressing situations." "Trying to just get views by doing something
> emotionally manipulative."

**Not a current risk and must not become one.** No distress bait, no
manufactured jeopardy, no thumbnail or hook that promises harm.

Note the shape of their example: it is not that the subject is sad, it is that
the *channel is dedicated to* manufacturing an emotional reaction. Films about
hard subjects are fine. A channel built on making people wince is not.

---

## Bucket 3 — AI personas on sensitive topics

> "AI personas may be fine overall, but if you have AI personas that are talking
> about finance or legal issues or health care, medical issues, we don't want to
> provide an incentive for that."

**We touch the sensitive topics.** *You Watched It Happen* is about children's
health. Films on psychology, medicine and behaviour will keep landing here, and
the narration is a synthetic voice.

**What keeps us out of this bucket is that we have no persona.** A persona is a
synthetic *person* presented as a source of authority. We have documentary
narration over illustration: no name, no face, no character, no claimed
credentials, and the argument defers to cited primary research rather than to
the speaker.

### Rules

- **The narrator is never a character.** No name, no avatar, no "hosted by", no
  recurring identity, no first-person credentials. The voice is a narrator, not
  a presenter. This is permanent.
- **On any health, medical, legal or financial claim, the authority is the
  citation, never the narration.** Name the study, the year and the journal in
  the film and in the description.
- **Never let the narration claim expertise or give advice.** "The research
  found X" is reporting. "You should do X" is a persona giving medical advice.

---

## What this changes upstream

| Chair | Constraint |
|---|---|
| Director | Sensitive-topic films must carry primary citations; no advice register; the narrator never becomes a character. |
| Writer | No first-person expertise ("in my experience as..."). Authority sits with the source. |
| Editor | Every social edition carries the sources line. Shorts from one film are spaced, never batched. |
| Publisher | Cadence guard on by default. Two per 24h across all films. |

## What is NOT a problem

Worth stating, so nobody optimises against a phantom:

- **Generated imagery.** Explicitly agnostic to tools.
- **Synthetic narration**, absent a persona.
- **Altered-content disclosure.** Non-realistic animation is exempt; there is
  also no `containsSyntheticMedia` field on the Data API — that was a phantom we
  sent for weeks and YouTube silently dropped (PLAYBOOK 10.26).
- **Flags from viewers or competitors.** "The number of flags has nothing to do
  with how an evaluation is done" — stated with "100% conviction".

## If it goes wrong

21 days to appeal a suspension. Reapply after 90 days with new content; "people
reapply after 90 days all the time and lots of them get back in."
