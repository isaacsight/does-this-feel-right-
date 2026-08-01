#!/usr/bin/env node
/**
 * Publish shorts to YouTube, TikTok and Instagram from one manifest.
 *
 *   node tools/publish/index.mjs status                      what is posted where
 *   node tools/publish/index.mjs run                         stage pending (dry)
 *   node tools/publish/index.mjs run --publish               actually post
 *   node tools/publish/index.mjs run --platform tiktok --publish
 *   node tools/publish/index.mjs run --short short-2-potatoes --publish
 *
 * Design notes, all learned the hard way today:
 *  - IDEMPOTENT. State lives in the manifest and is written after every single
 *    post, so a crash mid-batch loses nothing and re-running skips what is done.
 *    The first version had no state and left "7 of 9 posted" to be audited by
 *    hand against the live profiles.
 *  - PER-PLATFORM TRANSPORT. YouTube uses its API, TikTok uses Playwright,
 *    Instagram prefers the Graph API and only falls back to Playwright. Picking
 *    the most robust route per platform beats one clever approach for all.
 *  - VERIFY, DON'T TRUST. Clicking a button is not evidence of publishing; each
 *    adapter waits for a real success signal.
 *  - DRY BY DEFAULT. Posting is irreversible, so --publish is explicit.
 */

import { load, mark, pending, caption, PLATFORMS } from './manifest.mjs'
import { ADAPTERS, closeBrowser, log } from './adapters.mjs'

let stopping = false
for (const signal of ['SIGINT', 'SIGTERM']) {
  process.once(signal, async () => {
    if (stopping) return
    stopping = true
    await closeBrowser()
    process.exit(signal === 'SIGINT' ? 130 : 143)
  })
}

const argv = process.argv.slice(2)
const cmd = argv[0] || 'status'
const flag = n => { const i = argv.indexOf(`--${n}`); return i > -1 ? argv[i + 1] : null }
const has = n => argv.includes(`--${n}`)

const PUBLISH = has('publish')
const RETRIES = Number(flag('retries') ?? 2)

const ICON = { posted: '✓', failed: '✗', pending: '·', staged: '~' }

function status(m) {
  // Manifests exist in two shapes: the first film nested {film:{title,url}},
  // every one since has flat film/film_url. Read both rather than migrating —
  // the older manifest is a published record and rewriting it would edit history.
  const title = m.film?.title ?? m.film
  const url = m.film?.url ?? m.film_url
  console.log(`\n${title} — ${url}\n`)
  const w = Math.max(...m.shorts.map(s => s.slug.length))
  console.log('  ' + 'short'.padEnd(w) + '  ' + PLATFORMS.map(p => p.padEnd(10)).join(''))
  for (const s of m.shorts) {
    const cells = PLATFORMS.map(p => {
      const st = s.status[p]?.state ?? 'pending'
      return `${ICON[st] ?? '?'} ${st}`.padEnd(10)
    })
    console.log('  ' + s.slug.padEnd(w) + '  ' + cells.join(''))
  }
  const todo = pending(m).length
  console.log(`\n  ${todo} of ${m.shorts.length * PLATFORMS.length} still to post\n`)
}

async function attempt(job, m) {
  const { short, platform } = job
  const text = caption(short, platform)
  for (let try_ = 1; try_ <= RETRIES + 1; try_++) {
    try {
      const res = await ADAPTERS[platform]({ short, caption: text, publish: PUBLISH })
      const state = PUBLISH ? 'posted' : 'staged'
      mark(m, short.slug, platform, state, res)
      console.log(`  ${ICON[state]} ${platform}/${short.slug}${res.url ? ' → ' + res.url : ''}`)
      return true
    } catch (e) {
      const last = try_ === RETRIES + 1
      log(`attempt ${try_} failed: ${e.message.split('\n')[0]}`)
      if (last) {
        mark(m, short.slug, platform, 'failed', { error: e.message.split('\n')[0] })
        console.log(`  ✗ ${platform}/${short.slug} — ${e.message.split('\n')[0]}`)
        return false
      }
      // Back off — most failures here are a slow transcode or a late modal.
      await new Promise(r => setTimeout(r, 5000 * try_))
    }
  }
}

async function run(m) {
  const platforms = flag('platform') ? [flag('platform')] : PLATFORMS
  const jobs = pending(m, platforms, flag('short'))
  if (!jobs.length) return console.log('\nNothing pending. All posted.\n')

  console.log(`\n${PUBLISH ? 'PUBLISHING' : 'STAGING (dry run — pass --publish to post)'}`)
  console.log(`${jobs.length} job(s)\n`)

  let ok = 0
  for (const job of jobs) {
    console.log(`→ ${job.platform}/${job.short.slug}`)
    if (await attempt(job, m)) ok++
  }
  await closeBrowser()
  console.log(`\n${ok}/${jobs.length} succeeded. Re-run to retry failures.\n`)
  status(m)
}

const m = load(flag('manifest') ?? 'output/publish/manifest.json')
if (cmd === 'status') status(m)
else if (cmd === 'run') await run(m)
else { console.log('commands: status | run'); process.exit(1) }
