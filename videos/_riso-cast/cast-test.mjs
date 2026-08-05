#!/usr/bin/env node
// Character test for the RISOGRAPH world — can this render carry a cast at all?
//
// The riso world test (videos/who-you-measured/WORLD.md) found it could NOT, with
// the existing house protagonist: the figure came back an unreadable blob in the
// wide, and in close-up its two fine hairs rendered as insect antennae with the
// whole head reading as a bug. Halftone plus deliberate misregistration eats fine
// detail. That is a fact about the DESIGN, not necessarily about the medium — real
// risograph illustration carries characters constantly, but they are drawn for it:
// big silhouettes, chunky forms, oversized features, almost no fine line.
//
// So this tests OUR character, adapted only where the process demands it: the two
// fine hairs become two thick solid strokes, and expression is carried by big brow
// and mouth shapes rather than by small eyes.
//
// Six frames, aimed at the specific risks:
//   c1  WIDE          does the character read at all when small
//   c2  XCU face      do expressions survive the screen
//   c3  two-shot      do two characters stay distinct from each other
//   c4  environment   does a busy comic environment stay legible in two inks
//   c5  action        does a big physical gag read
//   c6  crowd         do many characters stay readable
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

// THE HOUSE PROTAGONIST, crossing into the riso universe.
//
// This is the same character as the last four films — he is spine, the way the
// narrator's voice is. What changes is only what the process demands. The riso
// world test failed him on exactly one feature: his TWO FINE HAIRS came back as
// insect antennae and turned the whole head into a bug. Fine strands cannot
// survive a coarse dot screen with deliberate misregistration.
//
// So the hairs get thick and everything else stays. His palette is already
// two-ink native, which is why this crossover works at all:
//   tomato-red hood  -> the PINK ink
//   black trousers   -> the BLUE ink
//   cream face/shoes -> bare paper
const HERO =
  'the same recurring cartoon character: a small round bald head, EXACTLY TWO ' +
  'hairs standing straight up from the crown drawn THICK and solid like two fat ' +
  'brush strokes (never thin, never wispy, never antennae), a hooded jacket in the ' +
  'PINK ink, trousers in the DEEP BLUE ink, and pale shoes left as bare paper. ' +
  'Big simple shapes, heavy outlines, no fine detail anywhere on him'

const WORLD =
  'a RISOGRAPH PRINT: printed in exactly TWO inks on uncoated off-white paper with ' +
  'visible paper tooth, and the paper is the SAME warm off-white across the whole ' +
  'frame with no cool grey and no pure white anywhere. The two inks are a bright ' +
  'FLUORESCENT PINK and a deep BLUE, and nothing else. Every filled area is a coarse ' +
  'visible halftone of round dots, never a smooth flat fill. The two ink layers are ' +
  'slightly MISREGISTERED so their edges do not line up and a narrow band of bare ' +
  'paper shows along one side of every shape. Where the two inks overlap they ' +
  'multiply into a single darker violet. Semi-transparent ink, uneven roller ' +
  'coverage, patchy density, occasional streaking. Bold heavy outlines. No gradients, ' +
  'no soft shading, no glow, no drop shadows, no photographic texture. Edges slightly ' +
  'ragged from the screen. There is NO text, NO lettering, NO numbers and NO writing ' +
  'of any kind anywhere in the image. 16:9, edge to edge, one scene, one camera.'

const TESTS = {
  c1_wide_reads:
    `A WIDE shot of a laboratory that is being swallowed by jungle: thick vines ` +
    `wound around tall equipment cabinets, enormous leaves pushing in from both ` +
    `sides, one tall plant growing straight out of a machine. Standing small in the ` +
    `middle of it, ${HERO}, arms at their sides, looking up at the plant.`,
  c2_face_expression:
    `EXTREME CLOSE-UP filling the whole frame on the face of ${HERO}, mouth stretched ` +
    `ABSURDLY wide in alarm, thick brow shot up high, one enormous leaf drooping into ` +
    `the top of the frame. Nothing else.`,
  c3_two_shot:
    `Two characters facing each other in a jungle laboratory. On the left ${HERO}, ` +
    `holding up an enormous round flask. On the right a SECOND, clearly different ` +
    `character: a much taller plain figure in a long coat in the BLUE ink, with a ` +
    `small head and no hairs at all, leaning down with a flat unimpressed mouth. ` +
    `Vines behind them.`,
  c4_environment:
    `A busy laboratory overrun by jungle, seen wide: cabinets, tangled tubing, three ` +
    `oversized flasks bubbling over, hanging vines, huge leaves, one monkey sitting on ` +
    `top of a cabinet holding a flask. ${HERO} stands below with both arms thrown up. ` +
    `Comic, cluttered, but every shape big and bold.`,
  c5_action_gag:
    `${HERO} mid-air, having been launched backwards off their stubby feet by an ` +
    `ENORMOUS eruption of foam bursting out of a flask on a bench, arms and legs ` +
    `flung wide, goggles knocked crooked, mouth wide open. Vines and huge leaves ` +
    `all around. The foam is far larger than the character.`,
  c6_crowd:
    `A jungle laboratory seen wide, with SEVEN of these characters at once, each one ` +
    `${HERO}, all doing something different — one on a ladder in the vines, one under ` +
    `a bench, one holding a huge leaf, one running, one asleep, one pointing up, one ` +
    `covered in foam. Chaotic and comic, every figure big and readable.`,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(TESTS)
console.log(`${ids.length} cast-test images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
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
