# Driving Codex on kernel.chat — a designer's one-pager

You're building magazine issues, spreads, and interactive artifacts. Codex does
the typing; you do the direction, the taste, and the review. This page is
everything you need to start.

## Start it

Open a terminal in the project folder and run:

```bash
cd "/Users/isaachernandez/blog design"
codex --profile kernel
```

The `kernel` profile means Codex works on its own — it edits, builds, tests, and
commits without stopping to ask. It has exactly **one** hard stop: it will never
publish (push to `main`) on its own. That's yours to approve.

## See your work as it happens

In a second terminal:

```bash
npm run dev
```

Open the `localhost` URL it prints. Leave it running — the page reloads itself
as Codex edits. This is your live proof; watch it, don't imagine it.

## How to ask for something

Describe the *outcome and the feel*, not the code. Codex already knows the house
rules (they're in `AGENTS.md`). Good asks sound like:

- "Build the Issue 427 hero spread — full-bleed monument, dateline top-left, the
  accent should feel like cold morning light."
- "The folio numbers are too loud at 390px. Quiet them and re-check for
  horizontal scroll."
- "Make this bore collapse cleanly under reduced-motion."

Use magazine words (*spread, folio, monument, colophon, dateline*), not app
words (*card, panel, widget*). If you use an app word, Codex will push back —
that's the brand guardrail doing its job.

## Reading what Codex did

When Codex says it's done, it has already run the checks (`tsc`, `build`,
adherence + editorial linters) and worked on a branch — not on the live site.
You'll get a **PR** (a proposed change) to look at. To review:

- Look at the live preview first. Does it feel right?
- Skim the diff Codex shows you. You don't need to read every line — check that
  it touched what you expected.

## The two moments you hand back to Isaac

Codex will stop and wait for a human at exactly these points:

1. **Publishing** — merging the PR / pushing to `main`. This deploys to the live
   site in ~90 seconds. Isaac (or you, deliberately) presses this button.
2. **Anything with secrets or deploy scripts** — Codex won't touch `.env`, keys,
   or the deploy pipeline. If a task seems to need that, it'll say so.

Everything else — design, layout, motion, copy, components — is yours to drive
at full speed.

## If something looks off

- Page won't load? Check the `npm run dev` terminal for a red error line.
- Codex went the wrong direction? Just tell it — "undo that, the accent was
  better before." It can revert.
- Not sure if it's safe to publish? It isn't urgent. Leave the PR; ask Isaac.

## The rules, if you're curious

- `AGENTS.md` (repo root) — the contract Codex follows every turn.
- `.agents/AGENTS.md` — the deep design + interaction + verification law.
- `KERNEL.md` — the whole project map.
