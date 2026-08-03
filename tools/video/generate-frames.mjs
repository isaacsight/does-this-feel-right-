#!/usr/bin/env node
// Generate a film's frames against fal.ai (nano-banana/edit) — SHARED tool.
//
// Until 2026-08-02 each film carried its own copy of this script with its own
// hardcoded reference paths, and the paths were different in every film. That
// is how a run generated 100+ frames with no conditioning at all: the caller
// assumed one film's layout on another film. One tool, one layout, no copies:
//
//   videos/<film>/production/prompts.json        (build-prompts.py)
//   videos/<film>/production/refs/castplate.png  REQUIRED - character sheet
//   videos/<film>/production/refs/layout-plate.png REQUIRED - scenically EMPTY
//   videos/<film>/public/images/frames/<id>-final.png   output
//   videos/<film>/production/spend.log           append-only ledger
//
// Both plates are required because each teaches a different thing and the
// model needs both: the sheet teaches construction and palette, the empty
// plate teaches full-bleed geometry. A reference is a prior on EVERYTHING it
// contains (PLAYBOOK 10.8-10.10) - so the layout plate must be flat colour to
// all four edges, one horizon, one small figure, nothing else.
//
// Direct rather than through local-video-server: the wrapper caps params at
// 2,000 chars (the reference data URI is ~96KB) and reserves image_url. Going
// direct bypasses the engine's spend guard, so this script keeps its own
// ledger and refuses to exceed --budget.
//
// Usage:
//   node tools/video/generate-frames.mjs <film-dir> --only 02a
//   node tools/video/generate-frames.mjs <film-dir> --all [--concurrency 4]
//                                        [--layout production/refs/dial-plate.png]
//                                        [--budget 12] [--publish]
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const ENDPOINT = 'fal-ai/nano-banana/edit'
const USD_PER_IMAGE = 0.039

const argv = process.argv.slice(2)
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d }
const FILM = argv[0] && !argv[0].startsWith('--') ? join(REPO, argv[0]) : null
const only = arg('only', null)
const all = argv.includes('--all')
const publish = argv.includes('--publish')
const concurrency = Number(arg('concurrency', 4))
const BUDGET_USD = Number(arg('budget', 12))
if (!FILM || (!only && !all)) {
  console.error('usage: generate-frames.mjs <film-dir> (--only <id> | --all) [--publish]')
  process.exit(1)
}

const OUT_DIR = join(FILM, 'public', 'images', 'frames')
const LEDGER = join(FILM, 'production', 'spend.log')
const REFERENCE = join(FILM, 'production', 'refs', 'castplate.png')
const LAYOUT_REF = arg('layout', null)
  ? join(FILM, arg('layout', null))
  : join(FILM, 'production', 'refs', 'layout-plate.png')

// HARD GATE, not a warning. Frames generated without conditioning drift, and
// there is no cheap repair once they have (PLAYBOOK 10.8).
for (const [name, p] of [['character sheet', REFERENCE], ['layout plate', LAYOUT_REF]]) {
  if (!existsSync(p)) {
    console.error(`missing ${name}: ${p}`)
    console.error('Both plates are required. Scaffold with tools/video/new-film.mjs, or')
    console.error('build the plate first — generating unconditioned is a different job.')
    process.exit(1)
  }
}

const prompts = JSON.parse(readFileSync(join(FILM, 'production', 'prompts.json'), 'utf8'))

const FAL_KEY = readFileSync(join(REPO, '.env'), 'utf8')
  .split('\n').find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!FAL_KEY) { console.error('FAL_KEY not found in .env'); process.exit(1) }

// Downscale hard before encoding: fal only needs the sheet legible enough to
// copy construction and palette.
const enc = (src, tag) => {
  const j = join(FILM, 'production', `.ref-${tag}.jpg`)
  execFileSync('magick', [src, '-resize', '1024x', '-quality', '82', j])
  return 'data:image/jpeg;base64,' + readFileSync(j).toString('base64')
}
const refDataUri = enc(REFERENCE, 'chars')
const layoutDataUri = enc(LAYOUT_REF, 'layout')

mkdirSync(OUT_DIR, { recursive: true })
const sleep = ms => new Promise(r => setTimeout(r, ms))
const H = { 'content-type': 'application/json', authorization: `Key ${FAL_KEY}` }

let spent = existsSync(LEDGER)
  ? readFileSync(LEDGER, 'utf8').trim().split('\n').filter(Boolean).length * USD_PER_IMAGE
  : 0

const ids = only ? [only] : Object.keys(prompts)
const todo = ids.filter(id => !existsSync(join(OUT_DIR, `${id}-final.png`)))
const cost = todo.length * USD_PER_IMAGE
console.log(`${todo.length} to generate x $${USD_PER_IMAGE} = $${cost.toFixed(2)} | ` +
  `ledger $${spent.toFixed(2)} | budget $${BUDGET_USD.toFixed(2)} | concurrency ${concurrency}`)
if (!publish) { console.log('dry run. add --publish to spend.'); process.exit(0) }

async function generate(id) {
  const dest = join(OUT_DIR, `${id}-final.png`)
  if (existsSync(dest)) return { id, status: 'skip' }
  const prompt = prompts[id]
  if (!prompt) return { id, status: 'no-prompt' }
  if (spent + USD_PER_IMAGE > BUDGET_USD) return { id, status: 'BUDGET' }
  spent += USD_PER_IMAGE

  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt, image_urls: [refDataUri, layoutDataUri], num_images: 1 }),
  })
  const subText = await sub.text()
  if (!sub.ok) throw new Error(`submit ${sub.status}: ${subText.slice(0, 220)}`)
  const { status_url, response_url } = JSON.parse(subText)
  appendFileSync(LEDGER, `${new Date().toISOString()} ${id} ${ENDPOINT} ${USD_PER_IMAGE}\n`)

  for (let i = 0; i < 150; i++) {
    await sleep(2000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url
      if (!url) throw new Error(`${id}: completed but no image url`)
      const raw = join(OUT_DIR, `.${id}-raw.png`)
      writeFileSync(raw, Buffer.from(await (await fetch(url)).arrayBuffer()))
      // Sources arrive well above 1920; downscale to the film canvas, never up.
      execFileSync('magick', [raw, '-resize', '1920x1080^', '-gravity', 'center',
                              '-extent', '1920x1080', dest])
      execFileSync('rm', ['-f', raw])
      return { id, status: 'ok' }
    }
    if (st.status === 'FAILED' || st.status === 'ERROR') {
      throw new Error(`${id}: ${JSON.stringify(st).slice(0, 200)}`)
    }
  }
  throw new Error(`${id}: timed out`)
}

const results = []
let cursor = 0
async function worker() {
  while (cursor < todo.length) {
    const id = todo[cursor++]
    try {
      const r = await generate(id)
      results.push(r)
      console.log(`  ${r.status.padEnd(6)} ${id}  (${results.length}/${todo.length})`)
    } catch (err) {
      results.push({ id, status: 'FAIL', error: err.message })
      console.log(`  FAIL   ${id}: ${err.message}`)
    }
  }
}
await Promise.all(Array.from({ length: Math.min(concurrency, todo.length) }, worker))

const ok = results.filter(r => r.status === 'ok').length
const failed = results.filter(r => r.status === 'FAIL')
const budget = results.filter(r => r.status === 'BUDGET').length
console.log(`\n${ok} generated, ${failed.length} failed, ${budget} skipped on budget | spent ~$${spent.toFixed(2)}`)
for (const f of failed) console.log(`  FAILED ${f.id}: ${f.error}`)
