#!/usr/bin/env node
// World test ROUND 4 — the painted world with the marks removed, and the faces
// switched back on.
//
// THE ONE RULE THIS PROBE OBEYS: it reads production/prompts.json and sends
// those exact strings. It does not compose its own.
//
// Round 2's probes passed and the 102-frame batch failed, because each probe
// was hand-written standalone while the pipeline appended a shared clause the
// probes never saw. Five bespoke prompts do not test a shared clause. A probe
// must exercise the production path, so this one IS the production path with a
// five-item filter on it.
//
// WHAT IT HAS TO SETTLE, in order:
//   b13  does a FACE come back? Eyes crossing, hairs rising, buttons pinging.
//        v2 shipped 102 frames with no face in any of them
//   b44  can the model do exaggerated-and-literal — a colossal arm from the
//        clouds whose fist is a tiny pair of pursed lips. If this comes back as
//        a normal arm, the whole "painted literally" thesis is in trouble
//   b50  a CROWD all doing one thing at once, mouths open, arms up. v2's crowds
//        were rows of calm bystanders
//   b19  a landscape with no hero in it at all, to prove the episode can travel
//   b12  two characters INTERACTING, which was the fourth thing named
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const ENDPOINT = 'fal-ai/nano-banana'
const OUT = join(FILM, 'test')
const PICK = ['b13', 'b44', 'b50', 'b19', 'b12']

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

const PROMPTS = JSON.parse(readFileSync(join(FILM, 'production', 'prompts.json'), 'utf8'))
const missing = PICK.filter(id => !PROMPTS[id])
if (missing.length) { console.error('not in prompts.json: ' + missing.join(' ')); process.exit(1) }

// The marks must be gone from the production prompts, not just from my intent.
const dirty = PICK.filter(id => /charcoal|scratched ink|scribbled hatching/i.test(PROMPTS[id]))
if (dirty.length) { console.error('second-medium language still present: ' + dirty.join(' ')); process.exit(1) }

mkdirSync(OUT, { recursive: true })
console.log(`${PICK.length} images x $0.039 = $${(PICK.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const id of PICK) {
  process.stdout.write(`  ${id} ... `)
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: PROMPTS[id], num_images: 1,
                           aspect_ratio: '16:9', output_format: 'png' }),
  })
  if (!sub.ok) { console.log(`SUBMIT ${sub.status}`); continue }
  const { status_url, response_url } = JSON.parse(await sub.text())
  let done = false
  for (let i = 0; i < 120 && !done; i++) {
    await sleep(2000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url
      if (url) {
        writeFileSync(join(OUT, `v3-${id}.png`),
          Buffer.from(await (await fetch(url)).arrayBuffer()))
        console.log('ok')
      } else console.log('no image url')
      done = true
    } else if (st.status === 'FAILED' || st.status === 'ERROR') {
      console.log('FAILED'); done = true
    }
  }
  if (!done) console.log('timed out')
}
console.log(`\n${OUT}`)
