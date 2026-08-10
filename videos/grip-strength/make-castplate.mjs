#!/usr/bin/env node
// Castplate for the Instrument Room. ONE image, $0.039.
//
// The plate carries ONLY what is true of every frame (the queue episode's
// paid-for lesson: a reference is a prior on EVERYTHING it contains). Here
// that is: the warm hand, the dynamometer with its orange needle, the dark
// field — and the hand is drawn MID-ACTION, closing, because a plate's energy
// is a prior too and a neutral plate produced eight minutes of neutral frames
// once already.
import { readFileSync, writeFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const OUT = join(FILM, 'production', 'refs', 'castplate.png')
const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

const PROMPT =
  'A single warm-skinned human hand, drawn bold and simplified in flat graphic ' +
  'motion-design style, closing around the steel handle of a hand dynamometer, tendons ' +
  'rising — and beside it an oversized round dial with plain tick marks and one luminous ' +
  'SIGNAL ORANGE needle mid-sweep. These two subjects sit on a COMPLETELY BARE deep ' +
  'ink-blue-black field with nothing else in the picture: bare dark space around them on ' +
  'every side. Flat graphic MOTION-DESIGN illustration in the register of a high-end studio ' +
  'explainer: bold simplified forms, engineered clean line work, generous negative space, 2D ' +
  'planes, NO photorealism, NO 3D rendering, NO gradients beyond a single soft vignette. ' +
  'Palette: deep ink-blue-black field, warm bone-white line work, steel-grey instrument ' +
  'body, one warm muted skin tone, one luminous SIGNAL ORANGE accent on the needle only. ' +
  'Fine even film grain, flat matte. There is NO text, NO lettering, NO numerals and NO ' +
  'writing of any kind anywhere; the dial face carries plain tick marks only. ONE SINGLE ' +
  'COHERENT SCENE, NOT a grid of panels. 16:9, edge to edge, one locked camera.'

console.log('1 image x $0.039 = $0.04')
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }
const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))
const sub = await fetch('https://queue.fal.run/fal-ai/nano-banana', {
  method: 'POST', headers: H,
  body: JSON.stringify({ prompt: PROMPT, num_images: 1, aspect_ratio: '16:9', output_format: 'png' }),
})
if (!sub.ok) { console.error(`SUBMIT ${sub.status}`); process.exit(1) }
const { status_url, response_url } = JSON.parse(await sub.text())
for (let i = 0; i < 120; i++) {
  await sleep(2000)
  const st = await (await fetch(status_url, { headers: H })).json()
  if (st.status === 'COMPLETED') {
    const out = await (await fetch(response_url, { headers: H })).json()
    const url = out?.images?.[0]?.url
    if (!url) { console.error('no image url'); process.exit(1) }
    writeFileSync(OUT, Buffer.from(await (await fetch(url)).arrayBuffer()))
    console.log(OUT); process.exit(0)
  }
  if (['FAILED', 'ERROR'].includes(st.status)) { console.error('FAILED'); process.exit(1) }
}
console.error('timed out'); process.exit(1)
