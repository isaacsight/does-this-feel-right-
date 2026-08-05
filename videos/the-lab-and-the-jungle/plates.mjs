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
  'the recurring cartoon character: a small round bald head, EXACTLY TWO hairs ' +
  'standing up from the crown drawn as THICK solid strokes that KINK and LEAN at ' +
  'different angles and are different lengths, like a cowlick — never two straight ' +
  'vertical strokes, never symmetrical, never rabbit ears, never antennae. A hooded ' +
  'jacket in the PINK ink, trousers in the DEEP BLUE ink, pale shoes left as bare ' +
  'paper. Big simple shapes, heavy outlines, no fine detail on him anywhere')

const PLATES = {
  // A real castplate this time — the film HAS a character. Three views on one sheet
  // so the model learns his construction rather than one pose.
  castplate:
    `A character reference sheet on bare paper: THREE views of the SAME character ` +
    `side by side, standing full length — front view, side view, and back view — ` +
    `evenly spaced, all the same height, all in the same neutral standing pose with ` +
    `arms at the sides. The character is ${HERO}. Nothing else on the sheet: no ` +
    `background, no props, no scenery, no other figures.`,
  // Scenically EMPTY. With a cast in play this matters more, not less: anything
  // sitting in this plate would be donated into every frame of the film.
  'layout-plate':
    `A completely EMPTY scene: bare off-white paper running to all four edges of the ` +
    `frame, with ONE single plain horizontal ground line running the full width in ` +
    `the lower third. There is nothing else in the image at all — no character, no ` +
    `object, no plant, no shape, no mark. Just the paper and the one line.`,
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
