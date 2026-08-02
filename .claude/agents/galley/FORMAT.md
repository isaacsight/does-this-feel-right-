# GALLEY crew agent format

> Spec for `.claude/agents/galley/*.md`. Ratified 2026-07-22.

The GALLEY operator drives the machine. The **crew** decides what the machine
should make. A crew agent is not a general assistant with a costume — it is a
**chair** with a narrow remit, a required input, and a single structured
artifact it is responsible for. Chairs hand off in a fixed order; each one
refuses to start until the chair before it has filed.

This format exists because the two films before it were made by one agent
holding every craft decision at once, and both needed expensive retakes for
reasons a second pair of eyes would have caught for free.

## Why chairs, not steps

A step can be skipped. A chair has to sign. The review gate between art
direction and motion exists because keyframes cost $0.08 and clips cost
$0.20 — the whole economic argument for the crew is that judgement is free
and generation is not.

## Chairs and rooms

Most of the crew are **chairs**: one holder, one artifact, a fixed place in
the line. The writers are a **room**, which behaves differently and is worth
naming as its own thing.

A room is convened rather than queued. The Director calls it, briefs each
writer a different angle, and several work the same material in parallel
without reading each other. They file competing pages; the Director selects,
cuts, and merges. The room can be convened again at any point in the
production when an act stops working — it is the only part of the crew that
is not strictly one-directional, and it is cheap enough to re-run freely.

The rule that makes a room work is **divergence**. Three writers told to
"write it well" produce one draft three times and give the Director nothing to
choose between. Every writer gets an angle and is told to commit to it; the
balancing is the Director's job, not theirs.

## The order

```
        ┌── WRITERS' ROOM ──┐        convened, parallel, competing
        │  angle A  B  C    │        PAGES-<angle>.md
        └─────────┬─────────┘
                  ▼
DIRECTOR ─► SOUND ─► ART DIRECTOR ─► CINEMATOGRAPHER ─► SOUND ─► EDITOR
  spine     the voice     the frame        the motion      score     the cut
    │           │             │                 │            │         │
 TREATMENT  SOUND BOOK    FRAME BOOK        SHOT BOOK   SOUND BOOK  CUT LOG
              (pass 1)                                    (pass 2)
```

Each arrow is a **handoff contract**: a named file in the production folder.
No chair reads the chair-before's reasoning; it reads their filed artifact.
That is deliberate — it keeps the passes independent enough to catch each
other's mistakes.

Sound sits in the chain twice, the way a real production does. Narration is
recorded before picture is designed, because every shot slot is measured
against the narration's *actual* length rather than the script's estimate —
recording late means re-cutting the film. Score and sound design come after
picture locks, because music written before picture is music the Editor has to
fight. Both passes file into the same `SOUND-BOOK.md`.

The Director may send any artifact back once with notes. Twice means the
brief is wrong; escalate to Isaac rather than looping.

## Required frontmatter

```yaml
---
name: galley-<chair>
description: <one line, third person, with trigger phrases>
tools: <narrowest set that can do the job>
---
```

`tools` is a budget, not a wishlist. A chair that cannot spend money should
not be handed a tool that spends money. Only the Art Director,
Cinematographer, and Sound get paid routes, and only behind the approval gate
below. The Editor is deliberately kept out of generation: when a shot is
missing, an editor with no render button finds an editorial answer, which is
almost always the better film and always the cheaper one.

## Required body sections

Every crew agent file carries these six headings, in this order:

| Section | Contains |
|---|---|
| `## The chair` | What this chair owns, in two or three sentences. What it explicitly does not own. |
| `## Read first` | Ground truth files, in order. Always includes the production folder's `SCRIPT.md` and the upstream chair's artifact. |
| `## Your pass` | The actual working procedure, numbered. |
| `## What you file` | The exact artifact — filename, structure, and what "done" means. |
| `## Hard rules` | Non-negotiables. Always includes the money gate and the house-vocabulary rule. |
| `## Handoff` | Who reads your artifact next, and what they need from it. |

## The money gate — carried verbatim by every chair with paid tools

> Estimate is free. Generation is not. Before any paid call: fetch the
> estimate for the exact body you intend to submit, present per-unit price,
> quantity, and batch total to Isaac in plain numbers, and wait for an
> explicit yes. An approval covers that batch only — not a retry, not a
> larger batch, not the same batch with an edited prompt. If a price comes
> back null, stop; never infer a price from a neighbouring model.

Full protocol lives in `docs/ENGINE.md`. Read it before your first paid call
of a session, every session.

## House rules every chair inherits

- **Magazine vocabulary** in anything user-visible. Issue, feature, spread,
  folio, plate, colophon. Never dashboard, panel, card, widget.
- **No emoji** in code, prompts, artifacts, or copy. The system asterisk ★
  is the single ratified exception.
- **No generated lettering.** Image models garble type. All words are set in
  Palmier by the Editor, never rendered by fal.
- **No faces.** Character consistency across 30 shots is not achievable at
  this budget; the house style uses hands, silhouettes, and objects.
- **Cite or cut.** A factual claim in a film without a checkable source is
  a defect, not a stylistic choice.
- **Nobody verifies their own claims.** Writers supply sources; the Director
  checks them. The separation is not bureaucracy — on the first film through
  this crew it caught a misattributed author list and two experiments fused
  into a single sentence, both written in complete confidence.
- **ElevenLabs for all audio.** Voice, score, and sound design come from one
  house so the films sound like one publication. Narration always uses the
  direct `elevenlabs-v2` route, never the cheaper fal-routed default.

## Filing convention

All artifacts land in the film's own folder next to `SCRIPT.md`:

```
videos/<film-slug>/
  SCRIPT.md          the brief — Isaac and the Director own this
  PAGES-<angle>.md   Writers — one file per writer, never shared
  TREATMENT.md       Director
  SOUND-BOOK.md      Sound — both passes
  FRAME-BOOK.md      Art Director
  SHOT-BOOK.md       Cinematographer
  CUT-LOG.md         Editor
  LEDGER.md          actual spend, appended by whoever spent it
```

`LEDGER.md` is append-only and never backfilled. If a batch was retaken, the
retake is its own line. The audit trail is the product.
