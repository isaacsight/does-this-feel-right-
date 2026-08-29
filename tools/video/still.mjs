#!/usr/bin/env node
// One-off still generator — text-to-image on fal, for single pieces that are
// not film frames. generate-frames.mjs owns film frames (prompts.json, refs,
// ledger, the film canvas); this owns "give me one picture, now".
//
// Default model is FLUX 1.1 [pro] ultra with raw:true — raw mode is the
// photographic register: candid texture, natural skin, no airbrush. $0.06/image.
//
//   node tools/video/still.mjs "<prompt>" out.png [--ar 16:9] [--model <endpoint>] [--no-raw]
//
// Reads FAL_KEY from .env at the repo root, same as generate-frames.mjs.
import { readFileSync, writeFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')

const args = process.argv.slice(2)
const flag = (name, dflt) => {
  const i = args.indexOf(name)
  return i > -1 ? args.splice(i, 2)[1] : dflt
}
const noRaw = args.includes('--no-raw')
if (noRaw) args.splice(args.indexOf('--no-raw'), 1)
const model = flag('--model', 'fal-ai/flux-pro/v1.1-ultra')
const ar = flag('--ar', '16:9')
const [prompt, dest] = args
if (!prompt || !dest) {
  console.error('usage: still.mjs "<prompt>" out.png [--ar 16:9] [--model <endpoint>] [--no-raw]')
  process.exit(1)
}

const FAL_KEY = readFileSync(join(REPO, '.env'), 'utf8')
  .split('\n').find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!FAL_KEY) { console.error('FAL_KEY not found in .env'); process.exit(1) }

const H = { 'content-type': 'application/json', authorization: `Key ${FAL_KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

const body = { prompt, aspect_ratio: ar, num_images: 1, output_format: 'png' }
if (!noRaw && model.includes('flux-pro')) body.raw = true

const sub = await fetch(`https://queue.fal.run/${model}`, {
  method: 'POST', headers: H, body: JSON.stringify(body),
})
const subText = await sub.text()
if (!sub.ok) { console.error(`submit ${sub.status}: ${subText.slice(0, 300)}`); process.exit(1) }
const { status_url, response_url } = JSON.parse(subText)

for (let i = 0; i < 90; i++) {
  await sleep(2000)
  const st = await (await fetch(status_url, { headers: H })).json()
  if (st.status === 'COMPLETED') {
    const out = await (await fetch(response_url, { headers: H })).json()
    const url = out?.images?.[0]?.url
    if (!url) { console.error('completed but no image url'); process.exit(1) }
    writeFileSync(dest, Buffer.from(await (await fetch(url)).arrayBuffer()))
    console.log(`${dest} <- ${model} (${ar}${body.raw ? ', raw' : ''})`)
    process.exit(0)
  }
  if (st.status === 'FAILED' || st.status === 'ERROR') {
    console.error(JSON.stringify(st).slice(0, 300)); process.exit(1)
  }
}
console.error('timed out'); process.exit(1)
