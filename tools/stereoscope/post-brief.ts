#!/usr/bin/env npx tsx
// ─────────────────────────────────────────────────────────────
//  Stereoscope Monday brief — CLI
//  Dry run (prints the post, sends nothing):
//    npx tsx tools/stereoscope/post-brief.ts
//    npx tsx tools/stereoscope/post-brief.ts --data path/to/week.json
//  Post to Slack:
//    npx tsx tools/stereoscope/post-brief.ts --data week.json --post
//
//  Env (deliberately separate from the kernel workspace vars so a
//  misconfigured shell can never post ops numbers to the wrong
//  workspace):
//    STEREOSCOPE_SLACK_BOT_TOKEN   xoxb-… for the Stereoscope app
//    STEREOSCOPE_BRIEF_CHANNEL     channel ID (private ops channel)
// ─────────────────────────────────────────────────────────────

import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'
import * as dotenv from 'dotenv'
import { composeBrief, type WeekData } from './brief'

const here = dirname(fileURLToPath(import.meta.url))
dotenv.config({ path: resolve(here, '..', '..', '.env') })

function arg(flag: string): string | undefined {
  const i = process.argv.indexOf(flag)
  return i >= 0 ? process.argv[i + 1] : undefined
}

const dataPath = resolve(arg('--data') ?? resolve(here, 'sample-week.json'))
const shouldPost = process.argv.includes('--post')
const channel = arg('--channel') ?? process.env.STEREOSCOPE_BRIEF_CHANNEL

async function main() {
  const raw = JSON.parse(readFileSync(dataPath, 'utf8')) as WeekData
  const brief = composeBrief(raw)

  if (!shouldPost) {
    console.log(brief)
    console.log('\n[post-brief] dry run — nothing sent. Add --post to send.')
    return
  }

  const token = process.env.STEREOSCOPE_SLACK_BOT_TOKEN
  if (!token) {
    console.error('[post-brief] error: STEREOSCOPE_SLACK_BOT_TOKEN is not set')
    process.exit(1)
  }
  if (!channel) {
    console.error('[post-brief] error: no channel — pass --channel or set STEREOSCOPE_BRIEF_CHANNEL')
    process.exit(1)
  }

  const res = await fetch('https://slack.com/api/chat.postMessage', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: JSON.stringify({ channel, text: brief, unfurl_links: false }),
  })
  const json = (await res.json()) as { ok: boolean; ts?: string; error?: string }
  if (!json.ok) {
    console.error(`[post-brief] Slack error: ${json.error ?? 'unknown_error'}`)
    process.exit(1)
  }
  console.log(`[post-brief] posted to ${channel} (ts ${json.ts})`)
}

main().catch((err) => {
  console.error('[post-brief] fatal:', err)
  process.exit(1)
})
