#!/usr/bin/env node
// Build the castplate. ONE image, $0.04. The layout plate is copied from the
// tipping build (purpose-built EMPTY plate law — the model will not return a
// picture of nothing and a picture of nothing is the requirement).
//
// Standing lessons enforced:
//   - the plate contains ONLY what is true of the film's spine: the Man and
//     the Familiar Stranger, on nothing, NOT facing each other. The gap
//     between them is the film; the plate stages the gap.
//   - expressions are a prior: the Man mid-dread, the Stranger composed.
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs'
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
  'TWO characters standing FAR APART on a COMPLETELY EMPTY flat cream background with ' +
  'NOTHING else in the picture at all: no street, no platform, no props beyond what is ' +
  'named, no other people, no horizon. A wide stretch of empty cream between them; ' +
  'NEITHER character faces the other — both face the viewer, angled slightly away from ' +
  'each other. ' +
  'ON THE LEFT: a small slight YOUNG man with a soft ROUND face, two simple dot eyes, and ' +
  'a big confident nose, his head completely bald and smooth: bare scalp at the sides, ' +
  'bare above the ears with NO tufts of hair over the ears, thin plain eyebrows, and at ' +
  'the very top of his crown EXACTLY TWO thin hairs and not one more: one thin hair ' +
  'kinking left, one thin hair leaning right, bare smooth scalp everywhere else, clean ' +
  'plain skin with no freckles and no stubble; a flat VERMILION RED coat with EXACTLY ' +
  'THREE round dark buttons in one column down the front, thin stick legs, and ENORMOUS ' +
  'rounded oversized DARK INK-BLUE shoes each nearly a third as long as he is tall; BOTH ' +
  'his hands buried deep in his coat pockets, elbows pressed to his sides, his face ' +
  'mid-dread: eyebrows up, eyes wide, mouth pressed flat. ' +
  'ON THE RIGHT: a tall composed woman a full head taller than him, in a flat mustard ' +
  'GOLD coat with ONE single row of round buttons down the front and ONE small INK BLUE ' +
  'scarf knotted at her neck, carrying ONE completely BLANK folded newspaper under one ' +
  'arm, her posture perfectly upright and still, her face completely composed and level, ' +
  'eyes forward, a face that has stood in the same spot every morning for years. ' + STYLE

mkdirSync(OUT, { recursive: true })
copyFileSync(join(REPO, 'videos', 'tipping', 'production', 'refs', 'layout-plate.png'),
  join(OUT, 'layout-plate.png'))
console.log('layout-plate.png copied from tipping')
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
