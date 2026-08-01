#!/usr/bin/env node
// Generate frames on WaveSpeed nano-banana-2/edit.
//
// Used for one-off pieces (channel intro) rather than films. On a 122-frame
// film this model drifts from the character sheet and costs 2.7x fal; on a
// standalone piece its denser illustration is the point and there is nothing
// to stay consistent with.
//
// Usage: node tools/video/wavespeed-gen.mjs <prompts.json> <out-dir> [--refs a.png,b.png]
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const USD = 0.105                        // 2k tier, the one that matches fal's resolution

const [specPath, outDir] = process.argv.slice(2)
if (!specPath || !outDir) { console.error('usage: <prompts.json> <out-dir> [--refs a.png,b.png]'); process.exit(1) }
const refArg = process.argv.indexOf('--refs')
const refFiles = refArg > -1 ? process.argv[refArg + 1].split(',') : []

const KEY = readFileSync(join(REPO, '.env'), 'utf8')
  .split('\n').filter(l => l.startsWith('WAVESPEED_API_KEY='))
  .pop()?.slice('WAVESPEED_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('WAVESPEED_API_KEY not in .env'); process.exit(1) }

const enc = (src, i) => {
  const j = join('/tmp', `wsref-${i}.jpg`)
  execFileSync('magick', [src, '-resize', '1024x', '-quality', '82', j])
  return 'data:image/jpeg;base64,' + readFileSync(j).toString('base64')
}
const refs = refFiles.map(enc)          // data URIs are accepted; verified 2026-07-31

const prompts = JSON.parse(readFileSync(specPath, 'utf8'))
mkdirSync(outDir, { recursive: true })
const H = { 'content-type': 'application/json', authorization: `Bearer ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

let spent = 0
async function gen(id, prompt) {
  const dest = join(outDir, `${id}.png`)
  if (existsSync(dest)) return 'skip'
  const body = { prompt, resolution: '2k', aspect_ratio: '16:9', output_format: 'png' }
  if (refs.length) body.images = refs
  const sub = await fetch('https://api.wavespeed.ai/api/v3/google/nano-banana-2/edit', {
    method: 'POST', headers: H, body: JSON.stringify(body),
  })
  const txt = await sub.text()
  if (!sub.ok) throw new Error(`${sub.status}: ${txt.slice(0, 200)}`)
  spent += USD
  const poll = JSON.parse(txt)?.data?.urls?.get
  for (let i = 0; i < 150; i++) {
    await sleep(2000)
    const st = await (await fetch(poll, { headers: H })).json()
    if (st?.data?.status === 'completed') {
      const bin = Buffer.from(await (await fetch(st.data.outputs[0])).arrayBuffer())
      writeFileSync(dest, bin)
      return 'ok'
    }
    if (st?.data?.status === 'failed') throw new Error(JSON.stringify(st).slice(0, 200))
  }
  throw new Error('timed out')
}

const ids = Object.keys(prompts)
console.log(`${ids.length} frames, ~$${(ids.length * USD).toFixed(2)}`)
const results = await Promise.all(ids.map(async id => {
  try { const r = await gen(id, prompts[id]); console.log(`  ${r.padEnd(5)} ${id}`); return r }
  catch (e) { console.log(`  FAIL  ${id}: ${e.message}`); return 'fail' }
}))
console.log(`\n${results.filter(r => r === 'ok').length} generated · ~$${spent.toFixed(2)}`)
