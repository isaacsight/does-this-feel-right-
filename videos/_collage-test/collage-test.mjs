#!/usr/bin/env node
// World test: the COLLAGE world, from Isaac's mood board (2026-08-05).
//
// WHAT THE BOARD ACTUALLY IS. Not a style — an ASSEMBLY. Every element is a
// torn-edge paper scrap layered on cream board and taped down, with gold leaf as
// the accent. The contents of the scraps vary enormously (impasto, Ben-Day dots,
// art deco linework, impressionist sea, graffiti, classical marble) but the
// assembly never does. That invariance is the world; the variety is its licence.
//
// THE RISK THAT MATTERS. The board contains almost no SCENES. It is fragments.
// Our films need a character in an environment doing a specific thing with an
// expression. Exactly one element on the board is a scene — the stair into the
// clouds: flat shapes, orange circle sun, one small figure in an archway — and
// that is the model for what a frame has to be. If these come back as handsome
// boards of unrelated scraps, the world is wrong FOR US however good it looks.
//
// Five frames, each aimed at one risk:
//   k1  SCENE       does it compose a single coherent picture, not a mood board
//   k2  CHARACTER   does he survive as cut paper, readable at a distance
//   k3  CLOSE-UP    does an expression survive torn edges
//   k4  GOLD        does gold leaf read as flat matte gold, or as a gradient
//   k5  ENVIRONMENT does a cluttered comic environment hold together
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const ENDPOINT = 'fal-ai/nano-banana'
const OUT = join(FILM, 'test')

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

// The character as a collage element: cut paper, not drawn. His palette maps onto
// the board's own — the red hood is the vermilion scrap, the trousers the cobalt
// or near-black, his face bare cream stock. Two hairs stay KINKED and different
// lengths: thin read as antennae in riso and thick vertical read as rabbit ears,
// so shape is the axis that works.
const HERO =
  'the recurring character, built entirely from CUT AND TORN PAPER: a small round ' +
  'head cut from plain cream paper stock with visibly deckled torn edges, EXACTLY ' +
  'TWO hairs standing up from the crown as two torn paper slivers that KINK and ' +
  'LEAN at different angles and are different lengths (never symmetrical, never ' +
  'vertical, never rabbit ears), a hooded jacket torn from VERMILION RED paper, ' +
  'trousers torn from deep COBALT BLUE paper, shoes cut from cream stock. Every ' +
  'part of him is a separate paper shape with a torn edge, layered slightly over ' +
  'the next, casting a faint hard paper shadow'

// Colours in WORDS, never hex — a hex in a prompt comes back drawn into the frame
// as a string (PLAYBOOK 10.33).
const WORLD =
  'a PAPER COLLAGE: the entire image is built from torn and cut pieces of paper ' +
  'layered on a warm cream paper ground, and every single shape has a visibly ' +
  'TORN OR DECKLED EDGE with the white core of the paper showing along the tear. ' +
  'Pieces overlap and cast faint hard-edged paper shadows. A few pieces are held ' +
  'down with short strips of pale masking tape. The palette is strictly limited to ' +
  'VERMILION RED, deep COBALT BLUE, soft BLUSH PINK, MUSTARD YELLOW, dark FOREST ' +
  'GREEN, near-BLACK and the cream paper itself, plus small accents of flat MATTE ' +
  'GOLD LEAF. Surfaces carry real paper texture: some pieces show coarse halftone ' +
  'dot printing, some show thick dry brushed paint, some show plain flat pulp. ' +
  'Flat matte finish throughout: NO gradients, NO soft airbrushed shading, NO glow, ' +
  'NO metallic sheen or shine on the gold, NO photographic texture, NO drop shadows ' +
  'other than the hard paper offsets. There is NO text, NO lettering, NO numbers ' +
  'and NO writing of any kind anywhere in the image. ' +
  // The failure this world is most likely to produce, forbidden explicitly.
  'This is ONE SINGLE COHERENT SCENE assembled from paper, NOT a mood board, NOT a ' +
  'grid of samples, NOT a sheet of unrelated swatches or separate framed pictures. ' +
  '16:9, edge to edge, one scene, one camera.'

const TESTS = {
  k1_scene:
    `A single wide scene: an enormous flight of pale stairs climbing from the bottom ` +
    `left up into a bank of clouds, a large flat VERMILION circle sun high in a ` +
    `FOREST GREEN sky, and a tall archway standing at the top of the stairs. ` +
    `${HERO} stands small in the archway, seen from behind, one arm raised. Nothing else.`,
  k2_character:
    `A wide scene on one ground line: ${HERO} standing alone in the middle of a large ` +
    `open cream field, arms at his sides, seen from the front. A single flat COBALT ` +
    `shape lies on the ground behind him. Nothing else in the frame.`,
  k3_closeup:
    `EXTREME CLOSE-UP filling the whole frame on the head of ${HERO}, facing the ` +
    `camera, mouth torn open ABSURDLY wide in alarm, thick brows shot up high, eyes ` +
    `wide. His features are separate torn paper pieces. Nothing else.`,
  k4_gold:
    `${HERO} standing at the left, reaching up toward an ENORMOUS flat MATTE GOLD ` +
    `LEAF circle that hangs high at the right of the frame, far bigger than he is. ` +
    `The gold is flat and matte with visible leaf texture and NO shine. A dark ` +
    `FOREST GREEN ground line runs beneath. Nothing else.`,
  k5_environment:
    `A cluttered laboratory scene assembled from torn paper: a long bench, three ` +
    `oversized round flasks, coiled tubing, tall cabinets, and enormous leaves ` +
    `pushing in from both edges. ${HERO} stands at the bench with both arms thrown ` +
    `up in alarm. Comic and busy, but every shape big, bold and clearly torn paper.`,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(TESTS)
console.log(`${ids.length} collage-test images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const id of ids) {
  process.stdout.write(`  ${id} ... `)
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: `${TESTS[id]} ${WORLD}`, num_images: 1,
                           aspect_ratio: '16:9', output_format: 'png' }),
  })
  const t = await sub.text()
  if (!sub.ok) { console.log(`SUBMIT ${sub.status}`); continue }
  const { status_url, response_url } = JSON.parse(t)
  let done = false
  for (let i = 0; i < 120 && !done; i++) {
    await sleep(2000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url
      if (url) {
        writeFileSync(join(OUT, `${id}.png`),
          Buffer.from(await (await fetch(url)).arrayBuffer()))
        console.log('ok')
      } else console.log('no image url')
      done = true
    } else if (st.status === 'FAILED' || st.status === 'ERROR') {
      console.log('FAILED'); done = true
    }
  }
  if (!done) console.log('timed out')
}
console.log(`\n${OUT}`)
