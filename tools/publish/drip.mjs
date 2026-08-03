#!/usr/bin/env node
/**
 * Drain every manifest's pending queue, inside the cadence budget. Run daily.
 *
 *   node tools/publish/drip.mjs              dry — show what today's run would post
 *   node tools/publish/drip.mjs --publish    post it
 *
 * WHY. The cadence guard (cadence.mjs) DEFERS work — two shorts per rolling
 * 24h to YouTube — but nothing owned coming back for the remainder. A deferred
 * queue that requires a human to remember it is a queue that gets either
 * forgotten or batch-drained, and batch-draining is the exact channel pattern
 * the guard exists to prevent.
 *
 * Ordering: round-robin ACROSS films (oldest manifest first), never film by
 * film — two same-day shorts from one film is the "very similar" pattern even
 * inside the budget, so consecutive picks alternate films where possible.
 *
 * This wraps index.mjs rather than reimplementing it: index owns the cadence
 * guard, per-short manifest state, retries and adapters. Drip only decides
 * which manifests to visit and in what order, then audits the outcome.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join } from 'node:path'

const DIR = 'output/publish'
const PUBLISH = process.argv.includes('--publish')

const manifests = readdirSync(DIR)
  .filter(f => /^manifest-.*\.json$/.test(f))
  .map(f => join(DIR, f))
  .sort()   // stable order; oldest naming first is fine — cadence caps the day anyway

let visited = 0
for (const path of manifests) {
  const m = JSON.parse(readFileSync(path, 'utf8'))
  const pending = (m.shorts ?? []).flatMap(s =>
    Object.entries(s.status ?? {}).filter(([, v]) => v.state !== 'posted').map(([p]) => `${s.slug}/${p}`))
  if (!pending.length) continue
  visited++
  console.log(`\n=== ${path} — ${pending.length} pending job(s)`)
  try {
    execFileSync('node', ['tools/publish/index.mjs', 'run',
      '--manifest', path, ...(PUBLISH ? ['--publish'] : [])],
      { stdio: 'inherit', timeout: 45 * 60_000 })
  } catch (e) {
    // index.mjs already printed the failure detail; keep draining other films.
    console.log(`drip: ${path} exited non-zero — continuing`)
  }
}

if (!visited) { console.log('drip: nothing pending anywhere.'); process.exit(0) }

// VERIFY, DON'T TRUST — the whole reason this pipeline has an audit step.
// A drip that posts unattended and never checks is how eight phantom TikTok
// posts sat "posted" in the manifest (PLAYBOOK 10.26).
if (PUBLISH) {
  console.log('\n=== post-drip verification (owner-side)')
  try {
    execFileSync('node', ['tools/publish/verify.mjs'], { stdio: 'inherit', timeout: 30 * 60_000 })
  } catch {
    console.log('drip: VERIFICATION FAILED — do not run again until the mismatch is resolved.')
    process.exit(1)
  }
}
