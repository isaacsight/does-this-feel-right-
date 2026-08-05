#!/usr/bin/env node
// World test for the RISOGRAPH clause. Unconditioned by design: we are testing
// whether the medium survives from text alone, before any plate is built in it.
// Plates come after the world locks, not before — a plate built in an unlocked
// world just propagates whatever is wrong with it to every frame.
//
// Three compositions, each aimed at a specific risk named in
// docs/video/WORLD-risograph.md:
//   t1 WIDE + figure     does the misregistration hold ONE direction, and does
//                        the character survive a halftoned surface
//   t2 CLOSE-UP          the ledger world drifted warm on close-ups while wides
//                        held; a world test without a close-up finds that late
//   t3 LARGE FLAT AREAS  does the halftone alias, and does the two-ink overlap
//                        actually multiply into a third colour
//
// Usage: node world-test.mjs [--publish]
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const ENDPOINT = 'fal-ai/nano-banana'          // text-to-image; /edit needs inputs
const USD = 0.039
const OUT = join(FILM, 'production', 'world-test')

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

// Colours in WORDS, never hex — a hex in a prompt comes back drawn into the frame
// as a string (PLAYBOOK 10.33).
const WORLD = `
a RISOGRAPH PRINT: the whole image is printed in exactly TWO inks on uncoated
off-white paper with visible paper tooth. The two inks are a bright FLUORESCENT
PINK and a deep BLUE, and nothing else. Every filled area is a coarse visible
halftone of round dots, never a smooth flat fill. The two ink layers are slightly
MISREGISTERED - every pink shape sits a few millimetres DOWN AND TO THE RIGHT of
the blue shape it belongs to, the SAME offset and the SAME direction everywhere
in the frame - so a narrow band of bare paper shows along one side of every shape.
Where the two inks overlap they multiply into a single darker violet. The ink is
semi-transparent with uneven roller coverage, patchy density and occasional light
streaking. No gradients, no soft shading, no glow, no drop shadows, no photographic
texture. Edges are slightly ragged from the screen. There is NO text, NO lettering,
NO numbers and NO writing of any kind anywhere in the image. 16:9, edge to edge,
one scene, one camera.`.replace(/\s+/g, ' ').trim()

// SET 1 (run, judged): t1_wide_figure / t2_closeup_face / t3_flat_shapes.
// Verdict — the medium passes convincingly and the halftone survives the render
// push without moiré, but the CHARACTER does not survive: halftone plus deliberate
// misregistration destroys the small consistent details the protagonist is built
// from, and the two fine hairs read as insect antennae. Hence: cast-free.
//
// SET 2 tests the object-led vocabulary this film will actually use, and measures
// whether the misregistration holds ONE direction across frames — the failure that
// cost the ledger world its margin rule (a good effect the model cannot place
// consistently is worse than no effect).
const TESTS = {
  t4_quantity:
    `A very wide field. Many small identical plain circles arranged in even rows ` +
    `receding to a high horizon, hundreds of them, absolutely uniform, and ONE circle ` +
    `near the front is a different ink from all the others. No people, no figures.`,
  t5_two_rooms:
    `Two plain empty rectangular rooms side by side, seen straight on in cross-section, ` +
    `sharing one horizontal ground line. The LEFT room is almost entirely filled by one ` +
    `large flat block; the RIGHT room is almost entirely empty with one tiny block in ` +
    `the corner. No people, no figures, nothing else.`,
  t6_scatter:
    `A wide field with a dense cloud of small plain dots scattered unevenly, thick in ` +
    `the middle and thinning toward the edges, with one plain horizontal line running ` +
    `through the cloud. No people, no figures, no letters, no numbers.`,
  t7_closeup_object:
    `EXTREME CLOSE-UP filling the whole frame on the corner of one plain rectangular ` +
    `card lying on a flat surface, its edge slightly curled, enormous at this scale. ` +
    `No people, no figures, nothing else.`,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(TESTS)
console.log(`${ids.length} world-test images x $${USD} = $${(ids.length * USD).toFixed(2)}`)
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
  const text = await sub.text()
  if (!sub.ok) { console.log(`SUBMIT ${sub.status}: ${text.slice(0, 200)}`); continue }
  const { status_url, response_url } = JSON.parse(text)
  let done = false
  for (let i = 0; i < 120 && !done; i++) {
    await sleep(2000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url
      if (!url) { console.log('completed but no image url'); done = true; break }
      writeFileSync(join(OUT, `${id}.png`), Buffer.from(await (await fetch(url)).arrayBuffer()))
      console.log('ok'); done = true
    } else if (st.status === 'FAILED' || st.status === 'ERROR') {
      console.log(`FAILED: ${JSON.stringify(st).slice(0, 160)}`); done = true
    }
  }
  if (!done) console.log('timed out')
}
console.log(`\n${OUT}`)
