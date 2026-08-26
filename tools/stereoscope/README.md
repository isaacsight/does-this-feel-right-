# Stereoscope Slack bot

Slack presence for the Stereoscope Coffee Company workspace
(`stereoscope-coffee-co.slack.com`), run by kernel.chat studio.

Origin: 2026-07-14 DM with James (Stereoscope ops). Out of the
11-item integration menu, the one that got the checkmark:

> every monday, one post in this slack — how all 6 shops did last
> week + the one thing to fix.

Two pieces, shipped in that order of importance:

## 1. Monday brief (`post-brief.ts` + `brief.ts`)

One post, every Monday, into a **private ops channel**: per-shop
sales with week-over-week deltas, average ticket, labor as a
percent of sales, then a single deterministic "one thing to fix"
and a short watch list. Every number is arithmetic over the week
file — no LLM in the loop, so the post can be trusted and the
logic is unit-tested (`brief.test.ts`).

```sh
# Dry run against the bundled sample (prints, sends nothing)
npm run stereoscope:brief

# Real week
npx tsx tools/stereoscope/post-brief.ts --data /path/to/week.json --post
```

The week file shape is `WeekData` in `brief.ts`; see
`sample-week.json` for a filled-in example. `prevSales`,
`prevTransactions`, and `laborCost` are optional — shops that do
not track a metric yet simply render without it. `laborTarget`
defaults to 0.30 of sales.

Data feed: James runs Zapier against the POS. The intended wiring
is Zapier (or cron) producing the week JSON and invoking the CLI —
Zapier stays the trigger layer, this stays the memory/format layer.

Sample shop names: four are real (Newport Beach, Buena Park,
Echo Park, Hollywood); the last two are placeholders — edit
`sample-week.json` to the actual roster before demoing.

## 2. Conversational presence (`bot.ts`)

Socket Mode bot, same architecture as `tools/slack-bot.ts` (the
kernel.chat client presence): answers DMs and @-mentions, threads
replies in channels, keeps per-thread history, calls Claude through
the Supabase claude-proxy (repo rule: never call Anthropic
directly). The personality is scoped hard: it never invents policy,
recipes, prices, or numbers, and it routes wage/sales/personnel
questions to managers and the private ops channel.

```sh
npm run stereoscope:bot
```

## Setup

Create a Slack app in the Stereoscope workspace with:

- **Socket Mode** enabled (app-level token with `connections:write`)
- Bot token scopes: `chat:write`, `app_mentions:read`, `im:history`,
  `im:read`, `im:write`
- Event subscriptions: `app_mention`, `message.im`

Then in `.env` (never committed):

```
STEREOSCOPE_SLACK_BOT_TOKEN=xoxb-...
STEREOSCOPE_SLACK_APP_TOKEN=xapp-...
STEREOSCOPE_BRIEF_CHANNEL=C...        # private ops channel ID
```

The env vars are deliberately separate from `SLACK_BOT_TOKEN` /
`SLACK_APP_TOKEN` (the kernel workspace) so a misconfigured shell
can never post Stereoscope ops numbers into the wrong workspace,
or kernel content into theirs. Labor and sales data belongs in a
private ops channel with the right people in it — not anywhere the
whole team can read it.

## Tests

```sh
npx vitest run tools/stereoscope/brief.test.ts
```
