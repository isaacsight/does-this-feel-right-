#!/usr/bin/env node
// Build the two conditioning plates. TWO images, $0.08.
//
// Both lessons from the queue episode are baked in:
//   CASTPLATE  contains ONLY what is true of every frame — the cast, on
//              nothing. The queue episode's plate contained a five-person
//              QUEUE and five calm blank faces, and a reference is a prior on
//              everything it holds: 77% of frames came back with a queue in
//              them and not one named a face action. The plate was doing half
//              the damage the board got blamed for.
//   BIG FACES  the plate's expressions are a prior too, so the fancier is
//              drawn mid-expression rather than neutral. Blankness in the
//              plate becomes blankness in the film.
// The layout plate is generated EMPTY on purpose (see reference: a
// "plain-looking" reference frame donates its props to a quarter of the film).
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

const PLATES = {
  castplate:
    'THREE characters on a COMPLETELY EMPTY flat cream background with NOTHING else in the ' +
    'picture at all: no loft, no rooftop, no sky, no props, no other people, no horizon. ' +
    'ON THE LEFT: a small slight man with a round face and a big confident nose, EXACTLY TWO ' +
    'hairs and no more than two sticking up from his crown — count them, there are TWO single ' +
    'hairs — kinked and leaning at different angles, a flat VERMILION RED coat, thin stick ' +
    'legs and ABSURDLY oversized shoes far too big for him; his face is doing something ' +
    'ENORMOUS: eyes wide and bulging, eyebrows shot up, mouth open in hope. ' +
    'IN THE MIDDLE: a plump grey racing pigeon with a tiny head, a bright orange eye and ONE ' +
    'white splash on her left wing, standing calm and still and entirely unbothered. ' +
    'ON THE RIGHT: a second grey pigeon, scruffier, his feathers ruffled on one side. ' + STYLE,
  'layout-plate':
    'A completely EMPTY flat cream field filling the entire picture. Nothing is drawn on it: ' +
    'no figures, no objects, no horizon line, no shadow, no texture beyond a faint even ' +
    'gouache grain. It is a blank painted ground, edge to edge. ' + STYLE,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(PLATES)
console.log(`${ids.length} images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }
const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))
for (const id of ids) {
  process.stdout.write(`  ${id} ... `)
  const sub = await fetch('https://queue.fal.run/fal-ai/nano-banana', {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: PLATES[id], num_images: 1, aspect_ratio: '16:9', output_format: 'png' }),
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
      if (url) { writeFileSync(join(OUT, `${id}.png`), Buffer.from(await (await fetch(url)).arrayBuffer())); console.log('ok') }
      else console.log('no image url')
      done = true
    } else if (st.status === 'FAILED' || st.status === 'ERROR') { console.log('FAILED'); done = true }
  }
  if (!done) console.log('timed out')
}
console.log(`\n${OUT}`)
