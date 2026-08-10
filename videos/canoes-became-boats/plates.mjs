#!/usr/bin/env node
// Build the two reference plates for a CAST-FREE film.
//
// generate-frames.mjs hard-gates on refs/castplate.png and refs/layout-plate.png,
// and that gate should stay: a run once produced 100+ frames with no conditioning
// at all because a path was wrong (PLAYBOOK 10.8). But this film has no cast, so
// the castplate slot would be meaningless if filled with a character sheet.
//
// It is filled with an INK PLATE instead, and the two plates then teach the two
// things conditioning actually has to carry here:
//
//   castplate.png    THE INK PLATE — the two inks, their overlap, the halftone,
//                    the misregistration and the paper stock. Teaches SURFACE.
//   layout-plate.png THE EMPTY WORLD — paper to all four edges, one ground line,
//                    nothing else at all. Teaches GEOMETRY.
//
// The layout plate must be scenically EMPTY. A "plain-looking" reference frame
// donates its props to a quarter of the film (PLAYBOOK 10.9) — and with no cast to
// anchor, anything sitting in this plate would recur everywhere.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const ENDPOINT = 'fal-ai/nano-banana'
const OUT = join(FILM, 'production', 'refs')

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

const WORLD = readFileSync(join(FILM, 'board.py'), 'utf8')
  .split('WORLD = (')[1].split(')\n')[0]
  .split('\n').map(l => l.trim().replace(/^"|"$/g, '').replace(/"\s*$/, ''))
  .join(' ').replace(/"\s+"/g, '').replace(/\s+/g, ' ').trim()

const HERO = (
  'the recurring character, built from CUT AND TORN PAPER: a small round BARE HEAD, fully visible and NOT covered by the hood, cut from pale BLUSH PINK paper with a clear dark outline so it reads against the cream ground, with deckled torn edges, EXACTLY TWO very SHORT stubby hairs on top, each a small blunt torn scrap no longer than the head is wide, kinked and leaning at different angles and different lengths — never long, never tapering, never branched, never antlers, never antennae, never rabbit ears, never symmetrical — and a simple face with two small dot eyes and a plain mouth, a hooded jacket torn ' +
  'from VERMILION RED paper, trousers torn from deep COBALT BLUE paper, shoes cut ' +
  'from cream stock. He wears NO scarf, NO belt, NO gloves and has NO spots or patterns on the jacket. Every part is a separate torn shape layered over the next, ' +
  'casting a faint hard paper shadow')

const PLATES = {
  // Three views on one sheet so the model learns his CONSTRUCTION — which pieces
  // he is made of — rather than one pose.
  castplate:
    `A character reference sheet on bare cream paper: THREE views of the SAME ` +
    `character side by side, standing full length — front, side and back — evenly ` +
    `spaced, all the same height, all in a neutral standing pose with arms at the ` +
    `sides. The character is ${HERO}. Nothing else on the sheet: no background ` +
    `scenery, no props, no other figures, no swatches.`,
  // Scenically EMPTY. A "plain-looking" plate donates its props to a quarter of
  // the film (PLAYBOOK 10.9), and in a collage world a stray scrap left here would
  // reappear in eighty frames.
  'layout-plate':
    `An almost entirely BLANK image. Warm cream paper fills the whole frame, edge ` +
    `to edge, plain and empty. Across the lower third runs ONE single straight ` +
    `horizontal torn strip of slightly darker paper, spanning the full width, as a ` +
    `ground line. That strip is the ONLY object in the picture. There are NO other ` +
    `shapes, NO circles, NO rectangles, NO coloured scraps, NO pile of pieces, NO ` +
    `arrangement of paper, NO tape, NO figure and NO objects of any kind anywhere. ` +
    `Do not compose anything. Empty cream paper and one horizontal line.`,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(PLATES)
console.log(`${ids.length} plates x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const id of ids) {
  process.stdout.write(`  ${id} ... `)
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: `${PLATES[id]} ${WORLD}`, num_images: 1,
                           aspect_ratio: '16:9', output_format: 'png' }),
  })
  const t = await sub.text()
  if (!sub.ok) { console.log(`SUBMIT ${sub.status}: ${t.slice(0, 200)}`); continue }
  const { status_url, response_url } = JSON.parse(t)
  for (let i = 0; i < 120; i++) {
    await sleep(2000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url
      if (!url) { console.log('no image url'); break }
      writeFileSync(join(OUT, `${id}.png`), Buffer.from(await (await fetch(url)).arrayBuffer()))
      console.log('ok'); break
    }
    if (st.status === 'FAILED' || st.status === 'ERROR') { console.log('FAILED'); break }
  }
}
console.log(`\n${OUT}`)
