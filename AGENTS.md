# AGENTS.md — kernel.chat operating contract for Codex

> Codex auto-loads this file. It is the operating contract, not the full
> reference. Read the linked docs before design work. The canonical project
> reference is [`KERNEL.md`](./KERNEL.md).

## What this is (30 seconds)

**Two surfaces, one publication.** (1) **kbot** — an open-source terminal AI
agent. (2) **kernel.chat** — an editorial magazine. You will almost always be
working on the magazine: interactive issues, spreads, and standalone artifacts.
The room is a magazine; speak like one.

## Read before you design

The detailed design, interaction, and verification law lives outside this file.
Before any design or layout task, read:

- [`.agents/AGENTS.md`](.agents/AGENTS.md) — full design / interaction / verification law
- [`KERNEL.md`](./KERNEL.md) — project shape, directory map, ship flow
- [`docs/design-language.md`](docs/design-language.md) — visual grammar
- [`docs/interaction-language.md`](docs/interaction-language.md) — motion + calmness law

## Non-negotiables (these override convenience)

1. **Magazine vocabulary** in all user-visible copy: *issue, feature, spread,
   folio, monument, colophon, dateline, postmark* — never *dashboard, panel,
   card, widget, modal*. Never name the visual homage ("POPEYE") on the site.
2. **No emojis** in code or user-visible copy. The single system asterisk `★`
   is the only exception.
3. **No JS animation runtimes** (Framer Motion, motion.dev, Lottie) on editorial
   surfaces. Page/editorial motion is CSS-only. Script motion is allowed only
   inside a framed mechanism (`plate`/`bore`) and must collapse under
   `prefers-reduced-motion`.
4. **Never touch secrets.** Do not read, edit, print, or commit `.env`, `*.key`,
   `*.pem`, or `supabase/config.toml` secrets. Never hardcode keys or tokens.
5. **Never push to `main`.** See workflow below — `main` is the live publisher.

## How you work (full-auto, one hard stop)

You work autonomously. Branch, edit, verify, commit, push the branch, open a PR
— all without asking. You stop at exactly one line: **merging or pushing to
`main`.** That is a human decision because it deploys.

1. **Branch** off `main`: `feat/<short-slug>` (or `fix/<slug>`). Never commit
   directly on `main`.
2. **Edit** freely within the repo.
3. **Verify** — the gate below must pass before you call anything done.
4. **Commit** with an evidence-cited message (cite the numbers/reason, per the
   project's commit discipline).
5. **Push the branch** and open a PR. Then **STOP** and hand back to the human
   for the merge.

### Verify gate (must pass before "done")

```bash
npx tsc --noEmit          # must be clean
npm run build             # must be clean (tsc && vite build)
npm run lint:adherence    # brand/adherence checks
npm run lint:editorial    # editorial checks
```

Plus a visual check: preview with `npm run dev`, confirm the issue accent is
POPEYE-safe, the `★` glyph renders, and there is **zero horizontal scroll at
390px and 393px**. Print preview (`Cmd+P`) must stack all interactive states
with no chrome.

## Deploy — do not

`npm run deploy` is retired. `main` is the only publisher: any push to `main`
triggers CI deploy (~90s). You never push to `main` and never run deploy
scripts. Opening the PR is where your job ends.

## Preview loop

```bash
npm run dev               # vite dev server → open the printed localhost URL
```

Iterate against the live preview. That is how the person next to you sees your
work in real time.
