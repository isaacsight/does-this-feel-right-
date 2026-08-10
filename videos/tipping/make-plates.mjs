#!/usr/bin/env node
// Build the castplate. ONE image, $0.04. The layout plate is built LOCALLY
// with ImageMagick (already in production/refs/) because the model will not
// return a picture of nothing and a picture of nothing is the requirement.
//
// Queue-episode lessons, still enforced:
//   - the plate contains ONLY what is true of the film's spine: the Man, the
//     Barista, the Screen, on nothing. No cafe, no counter, no jury.
//   - the plate's expressions are a prior: the Man is mid-wince, the Barista
//     mid-quarter-turn. A neutral plate produces a neutral film.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const OUT = join(FILM, 'production', 'refs')
const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

const STYLE =
  'Drawn as a MID-CENTURY ANIMATION CEL in the American limited-animation idiom of the late ' +
  '1950s: flat gouache-painted figures with confident tapering ink outlines and no interior ' +
  'shading, in a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, ' +
  'cream and flat VERMILION RED. Expressions are BOLD, exaggerated and readable at a glance. ' +
  'Visible gouache texture, flat matte, NO gradients, NO airbrushed shading, NO photographic ' +
  'texture, NO three-dimensional rendering. There is NO text, NO lettering and NO numbers ' +
  'anywhere. ORIGINAL characters in a general mid-century cartoon idiom: NO existing cartoon ' +
  'characters, NO studio logos, NO trade dress, no likeness of any real person. ONE SINGLE ' +
  'SCENE, NOT a grid of panels, NOT a sheet of studies. 16:9, edge to edge.'

const PROMPT =
  'TWO characters and ONE object on a COMPLETELY EMPTY flat cream background with NOTHING ' +
  'else in the picture at all: no cafe, no counter, no floor line, no props, no other ' +
  'people, no horizon. ' +
  'ON THE LEFT: a small slight man with a round face and a big confident nose, his head ' +
  'bald and smooth with bare scalp at the sides, bare above the ears, and at the very top ' +
  'of his crown a single lonely PAIR of hairs: one thin hair kinking left, one thin hair ' +
  'leaning right, bare smooth scalp everywhere else; a flat VERMILION RED coat with ' +
  'THREE round buttons, thin stick legs, and ENORMOUS rounded oversized shoes each nearly ' +
  'a third as long as he is tall, comically too big for him; his face is mid-WINCE: eyes ' +
  'wide, eyebrows shot up, mouth pressed into a flat line of dread, one thumb half-raised ' +
  'and frozen. ' +
  'IN THE MIDDLE: an oversized matte near-black tablet slab drawn like a monument on ONE ' +
  'steel counter-mount arm, its dark face showing FOUR blank rounded rectangles in one ' +
  'vertical column: a first large rectangle at the top, a second identical large rectangle ' +
  'below it, a third identical large rectangle below that, and at the bottom a fourth ' +
  'rectangle, much smaller than the other three, cleaner and newer than everything around ' +
  'it. ' +
  'ON THE RIGHT: a tall young woman in a cream shirt with sleeves rolled to the elbow, a ' +
  'SAGE GREEN half-apron with ONE front pocket holding TWO pens, a completely blank name ' +
  'badge, her hair in a high knot with ONE pencil pushed through it; she is caught ' +
  'MID-QUARTER-TURN, both hands rotating the slab with the precise neutral formality of a ' +
  'bailiff presenting evidence, her eyes politely elsewhere. ' + STYLE

mkdirSync(OUT, { recursive: true })
console.log('1 image x $0.039 = $0.04')
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))
const sub = await fetch('https://queue.fal.run/fal-ai/nano-banana', {
  method: 'POST', headers: H,
  body: JSON.stringify({ prompt: PROMPT, aspect_ratio: '16:9', num_images: 1 }),
})
const txt = await sub.text()
if (!sub.ok) { console.error(`${sub.status}: ${txt.slice(0, 200)}`); process.exit(1) }
const { status_url, response_url } = JSON.parse(txt)
for (let i = 0; i < 60; i++) {
  await sleep(4000)
  const st = await (await fetch(status_url, { headers: H })).json()
  if (st.status === 'COMPLETED') {
    const out = await (await fetch(response_url, { headers: H })).json()
    const url = out?.images?.[0]?.url ?? out?.data?.images?.[0]?.url
    if (!url) { console.error('completed but no image url in: ' + JSON.stringify(out).slice(0, 300)); process.exit(1) }
    writeFileSync(join(OUT, 'castplate.png'), Buffer.from(await (await fetch(url)).arrayBuffer()))
    console.log('castplate.png written')
    process.exit(0)
  }
  if (['FAILED', 'ERROR'].includes(st.status)) { console.error(JSON.stringify(st).slice(0, 200)); process.exit(1) }
}
console.error('timed out')
process.exit(1)
