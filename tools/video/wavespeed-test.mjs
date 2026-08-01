#!/usr/bin/env node
// One-frame bakeoff: WaveSpeed nano-banana-2/edit against the fal frame we
// already have, using identical prompt and references.
//
// Two unknowns this answers, both of which the docs leave open:
//   1. does `images` accept a data URI, or only externally-hosted URLs?
//      Our whole reference approach is a ~96KB data URI. If it needs a URL we
//      have to host the character sheet before every run.
//   2. what does the 2k tier actually return? fal gives 2752px for $0.039;
//      WaveSpeed's comparable tier is $0.105.
//
// Usage: node tools/video/wavespeed-test.mjs <frame-id>
import { readFileSync, writeFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const FILM = join(REPO, 'videos', 'you-are-not-finished')
const id = process.argv[2] || '23b'

const KEY = readFileSync(join(REPO, '.env'), 'utf8')
  .split('\n').filter(l => l.startsWith('WAVESPEED_API_KEY='))
  .pop()?.slice('WAVESPEED_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('WAVESPEED_API_KEY not in .env'); process.exit(1) }

const prompts = JSON.parse(readFileSync(join(FILM, 'production', 'prompts.json'), 'utf8'))
const prompt = prompts[id]
if (!prompt) { console.error(`no prompt for ${id}`); process.exit(1) }

const enc = (src, tag) => {
  const j = join('/tmp', `ws-${tag}.jpg`)
  execFileSync('magick', [src, '-resize', '1024x', '-quality', '82', j])
  return 'data:image/jpeg;base64,' + readFileSync(j).toString('base64')
}
const refs = [
  enc(join(FILM, 'public', 'images', 'REFERENCE-notext.png'), 'chars'),
  enc(join(FILM, 'public', 'images', 'literal-16x9', '01a-final.png'), 'layout'),
]
console.log(`frame ${id} · ${refs.length} refs · ${(refs[0].length/1024).toFixed(0)}KB + ${(refs[1].length/1024).toFixed(0)}KB`)

const H = { 'content-type': 'application/json', authorization: `Bearer ${KEY}` }
const t0 = Date.now()
const sub = await fetch('https://api.wavespeed.ai/api/v3/google/nano-banana-2/edit', {
  method: 'POST', headers: H,
  body: JSON.stringify({ prompt, images: refs, resolution: '2k', aspect_ratio: '16:9', output_format: 'png' }),
})
const text = await sub.text()
if (!sub.ok) {
  console.error(`\nSUBMIT FAILED ${sub.status}`)
  console.error(text.slice(0, 500))
  console.error('\nIf this rejects the data URI, references must be hosted at a public URL first.')
  process.exit(1)
}
const poll = JSON.parse(text)?.data?.urls?.get
console.log('submitted, polling…')

for (let i = 0; i < 150; i++) {
  await new Promise(r => setTimeout(r, 2000))
  const st = await (await fetch(poll, { headers: H })).json()
  const s = st?.data?.status
  if (s === 'completed') {
    const url = st.data.outputs?.[0]
    const bin = Buffer.from(await (await fetch(url)).arrayBuffer())
    const out = join('/tmp', `wavespeed-${id}.png`)
    writeFileSync(out, bin)
    const size = execFileSync('magick', [out, '-format', '%wx%h', 'info:']).toString()
    console.log(`\ncompleted in ${((Date.now()-t0)/1000).toFixed(1)}s`)
    console.log(`  ${out}  ${size}  ${(bin.length/1024/1024).toFixed(2)} MB`)
    console.log(`  cost: $0.105 (2k tier) vs fal $0.039`)
    process.exit(0)
  }
  if (s === 'failed') { console.error('\nFAILED:', JSON.stringify(st).slice(0, 400)); process.exit(1) }
}
console.error('timed out')
