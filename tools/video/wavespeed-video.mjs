#!/usr/bin/env node
// Animate one of our own stills with Veo on WaveSpeed.
//
// Image-to-video, not text-to-video, deliberately: handing the model our own
// frame means it only has to MOVE what is already on-model. Asking it to
// invent the style is where it drifts (see the 23b bakeoff, 2026-07-31).
//
// Price comes from the catalog formula, not the marketing page. veo3.1-lite is
//   base 0.30 * (1080p ? 1.6 : 1) * duration/6
// so 8s at 1080p is $0.64. The site's "$0.25/second" headline would say $2.00.
// Always price from GET /api/v3/models?search=<name>.
//
// duration is an enum: 4, 6 or 8 only. There is no 12.
//
// Usage: node tools/video/wavespeed-video.mjs --image F --prompt "..." --out F [--duration 8] [--publish]
import { readFileSync, writeFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const arg = n => { const i = process.argv.indexOf(`--${n}`); return i > -1 ? process.argv[i + 1] : null }
const has = n => process.argv.includes(`--${n}`)

const image = arg('image'), prompt = arg('prompt'), out = arg('out')
const negative = arg('negative') || ''
const duration = Number(arg('duration') || 8)
const resolution = arg('resolution') || '1080p'
if (!image || !prompt || !out) { console.error('need --image --prompt --out'); process.exit(1) }
if (![4, 6, 8].includes(duration)) { console.error('duration must be 4, 6 or 8'); process.exit(1) }

const cost = 0.30 * (resolution === '1080p' ? 1.6 : 1) * duration / 6
console.log(`veo3.1-lite · ${duration}s · ${resolution} · $${cost.toFixed(2)}`)
if (!has('publish')) { console.log('\ndry run. add --publish to spend.'); process.exit(0) }

const KEY = readFileSync(join(REPO, '.env'), 'utf8')
  .split('\n').filter(l => l.startsWith('WAVESPEED_API_KEY='))
  .pop()?.slice('WAVESPEED_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('WAVESPEED_API_KEY not in .env'); process.exit(1) }

// Veo takes a fair-sized still; keep it generous but not absurd over the wire.
const jpg = '/tmp/veo-src.jpg'
execFileSync('magick', [image, '-resize', '1280x', '-quality', '88', jpg])
const dataUri = 'data:image/jpeg;base64,' + readFileSync(jpg).toString('base64')
console.log(`source ${(dataUri.length / 1024).toFixed(0)}KB`)

const H = { 'content-type': 'application/json', authorization: `Bearer ${KEY}` }
const t0 = Date.now()
const sub = await fetch('https://api.wavespeed.ai/api/v3/google/veo3.1-lite/image-to-video', {
  method: 'POST', headers: H,
  body: JSON.stringify({ prompt, image: dataUri, duration, resolution, aspect_ratio: '16:9',
    ...(negative ? { negative_prompt: negative } : {}) }),
})
const txt = await sub.text()
if (!sub.ok) { console.error(`submit ${sub.status}: ${txt.slice(0, 400)}`); process.exit(1) }
const poll = JSON.parse(txt)?.data?.urls?.get
console.log('submitted, polling…')

for (let i = 0; i < 300; i++) {
  await new Promise(r => setTimeout(r, 3000))
  const st = await (await fetch(poll, { headers: H })).json()
  const s = st?.data?.status
  if (s === 'completed') {
    const bin = Buffer.from(await (await fetch(st.data.outputs[0])).arrayBuffer())
    writeFileSync(out, bin)
    console.log(`\ndone in ${((Date.now() - t0) / 1000).toFixed(0)}s → ${out} (${(bin.length / 1048576).toFixed(1)} MB)`)
    process.exit(0)
  }
  if (s === 'failed') { console.error('FAILED:', JSON.stringify(st).slice(0, 400)); process.exit(1) }
}
console.error('timed out')
