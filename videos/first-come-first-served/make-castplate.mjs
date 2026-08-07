#!/usr/bin/env node
// Rebuild the character sheet. ONE image, $0.039.
//
// WHY. generate-frames.mjs conditions all 102 frames on production/refs/
// castplate.png, and a reference is a prior on EVERYTHING it contains, not just
// on the character. The castplate this episode has been using contains:
//
//   - a QUEUE of five people, and the v2 board produced a queue in 77% of frames
//   - five CALM, BLANK, pleasant faces, and the v2 cut was rejected for having
//     "no feeling and expression in each slide"
//   - a street of flat buildings, which turned up behind beats set indoors
//
// I diagnosed both of those faults in the board and rewrote the board. The
// board was half the cause. The other half was sitting in the reference the
// whole time, being applied to every single frame.
//
// This plate therefore contains ONLY what should be true of every frame:
//   the two characters, and a BIG expression, on nothing at all.
// No queue, no street, no props, no third party. The layout plate stays empty
// (it already is) so geometry comes from there and construction from here.
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
  'TWO cartoon characters standing on a COMPLETELY EMPTY flat cream background with ' +
  'NOTHING else in the picture at all: no buildings, no street, no furniture, no props, ' +
  'no other people, no horizon, no queue, no line, nothing. ' +
  'ON THE LEFT: a small slight man with a round young face and a big confident nose, ' +
  'EXACTLY TWO hairs and NO MORE THAN TWO sticking up from the crown — count them, there ' +
  'are TWO single hairs, not three and not four — which KINK and LEAN at different angles ' +
  'and are different lengths, a flat VERMILION RED coat, thin stick legs and ABSURDLY ' +
  'oversized shoes far too big for him — and his face is doing something ENORMOUS: eyes wide open and ' +
  'bulging, eyebrows shot up, mouth open in outrage. ' +
  'ON THE RIGHT: a pleasant unremarkable middle-aged man in a sage green raincoat and a ' +
  'soft hat, mild and completely oblivious, faintly smiling, never smug and never a villain. ' +
  'Drawn as a MID-CENTURY ANIMATION CEL in the American limited-animation idiom of the ' +
  'late 1950s: flat gouache-painted figures with confident tapering ink outlines and no ' +
  'interior shading, in a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, ' +
  'dusty ORANGE, cream and flat VERMILION RED. Expressions are BOLD, exaggerated and ' +
  'readable at a glance. Visible gouache texture, flat matte, NO gradients, NO airbrushed ' +
  'shading, NO photographic texture, NO three-dimensional rendering. There is NO text, NO ' +
  'lettering and NO numbers anywhere. ORIGINAL characters: NO existing cartoon characters, ' +
  'NO studio logos, NO trade dress. ONE SINGLE SCENE, NOT a grid of panels, NOT a sheet of ' +
  'studies. 16:9, edge to edge.'

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
    console.log(OUT)
    process.exit(0)
  }
  if (st.status === 'FAILED' || st.status === 'ERROR') { console.error('FAILED'); process.exit(1) }
}
console.error('timed out')
process.exit(1)
