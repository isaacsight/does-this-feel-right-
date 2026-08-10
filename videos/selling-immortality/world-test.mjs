#!/usr/bin/env node
// Direction bake-off — THE LONELY CHAPTER. Three staging rules inside the
// SERIES world (mid-century painted cel — the world is never up for audition,
// the direction is). Each direction is a complete staging + lighting + camera
// grammar fitted to THIS subject:
//
//   ember       LIGHT IS MEMBERSHIP. Every warm light in the frame belongs
//               to a group the man is not in — golden lodge windows, lit
//               bars, lamplit rooms — while he stands in cool ink-blue dusk.
//               Camera at street level, framed through thresholds, windows
//               and doorways: the light is always one pane away.
//   vacancy     THE EMPTY SECOND PLACE. Flat even daylight, nothing moody —
//               the composition itself carries the loss: an unoccupied
//               chair squared to an occupied one, half a booth, a handshake
//               offered to open air. Camera frontal and still; the absence
//               is drawn as carefully as a character.
//   procession  THE MIRRORED CENTURY. Formal group-portrait compositions —
//               lodge rows, parade formations, banquet tables — and the
//               present day repeats the SAME composition with one figure.
//               Camera centered and ceremonial, portrait height; the 1920s
//               frames run full mustard-and-ink pageantry.
//
// Four CAST scenes per direction (same dramatic material, only the direction
// varies): the phone on the table, the lodge in 1924, the sidewalk goodbye,
// the two chairs. 12 images x $0.039 = $0.47.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const REPO = join(FILM, '..', '..')
const OUT = join(FILM, 'test')
const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('FAL_KEY='))?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not found'); process.exit(1) }

const MAN = 'the recurring character in mid-century cartoon style: a small slight man with a ' +
  'round young face and a big confident nose, his head bald and smooth except for a single ' +
  'lonely PAIR of hairs at the very top of his crown — one thin hair kinking left, one ' +
  'leaning right — a flat VERMILION RED coat with THREE round buttons, thin stick legs and ' +
  'ABSURDLY oversized shoes'

const WORLD =
  'a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom of ' +
  'the late 1950s: flat gouache-painted backgrounds and flat painted cel figures with ' +
  'confident tapering ink outlines and no interior shading, in a warm graphic palette of ' +
  'INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, cream and flat VERMILION RED. ' +
  'Expressions are BOLD, exaggerated and readable at a glance. Visible gouache texture, ' +
  'flat matte, NO gradients, NO photographic texture, NO 3D rendering. There is NO text, ' +
  'NO lettering, NO numbers and NO writing anywhere; every sign, banner, book and screen ' +
  'is completely BLANK. Any crowd is individuated: different faces and builds, clothes in ' +
  'DIFFERENT colours from the palette. ORIGINAL characters, NO existing cartoon ' +
  'characters, NO trade dress, no likeness of any real person. ONE SINGLE COHERENT SCENE, ' +
  '16:9, edge to edge, one scene, one camera.'

const DIRS = {
  midway:
    'DIRECTION: WARMTH AS BAIT - the booth and its product glow with warm MUSTARD GOLD ' +
    'light exactly like a lit window full of company, strings of warm round bulbs, and ' +
    'the crowd leans toward the glow while the surrounding scene sits in cool flat INK ' +
    'BLUE evening; the camera stands in the queue at eye level, so the booth is always ' +
    'slightly above and ahead, the way a stage is.',
  apothecary:
    'DIRECTION: ORDER AS AUTHORITY - shelves of identical glass bottles in neat ranks, ' +
    'polished wood and brass, and the light in the scene passes THROUGH the coloured ' +
    'liquid before it reaches any face, tinting the believers a soft warm amber; the ' +
    'camera is frontal and symmetrical like a shop portrait, everything squared, every ' +
    'label a completely BLANK paper rectangle.',
  prospectus:
    'DIRECTION: PAPER AS PROMISE - the scene is staged around DOCUMENTS: certificates ' +
    'with wax seals and ribbons, prospectuses, ledgers, all completely BLANK, handled ' +
    'like treasure; dusty pale daylight in long soft beams from high windows, small warm ' +
    'pools from desk lamps; the camera slightly elevated at a three-quarter angle, the ' +
    'angle of an auditor.',
}

const ELIXIR = 'ONE small glass vial of softly GLOWING warm amber liquid, the same warm amber in every era'

const SCENES = {
  s1_lecture_1889:
    `A Paris lecture hall in 1889: an old bearded professor at the lectern holding up ` +
    `ONE small syringe with a flourish, his other fist raised in triumph, before rows of ` +
    `TWELVE astonished bearded physicians in frock coats leaning forward as one, ${ELIXIR} ` +
    `standing on the lectern beside him, and ${MAN} in his same red coat seated among the ` +
    `physicians, leaning forward exactly as far as the rest.`,
  s2_gland_clinic_1925:
    `A 1925 private clinic: a surgeon in a white coat gesturing proudly at a wall chart of ` +
    `ONE ape drawn in profile (the chart completely BLANK of any writing), while THREE rich ` +
    `old men in dark suits with canes wait in a row of chairs, each holding a numbered-` +
    `looking BLANK ticket, and through the window ONE palm tree and ONE distant monkey ` +
    `sitting on a fence, and ${MAN} in his red coat at the end of the row holding his ` +
    `ticket with both hands.`,
  s3_radium_shelf_1930:
    `A 1930 pharmacy counter: a beaming pharmacist in a bow tie setting down ONE crate of ` +
    `small identical bottles, a pyramid of the same bottles already stacked on the counter, ` +
    `each bottle glowing faintly warm amber, a BLANK poster of a strongman flexing on the ` +
    `wall behind him, and ${MAN} in his red coat at the counter reaching for one bottle ` +
    `while looking over his shoulder at us.`,
  s4_modern_lounge:
    `A modern longevity clinic lounge: FOUR recliner chairs in a row, each with ONE IV ` +
    `stand holding ONE bag of warm amber liquid, THREE relaxed wealthy clients reclining ` +
    `with devices, ONE white-coated attendant with a tablet held like a clipboard, floor-to-` +
    `ceiling glass, ONE potted fig tree, and ${MAN} in his red coat perched on the edge of ` +
    `the last recliner, sleeve rolled up, eyes sideways on the amber bag.`,
}

mkdirSync(OUT, { recursive: true })
const jobs = []
const ONLY = process.env.ONLY
for (const [d, style] of Object.entries(DIRS))
  for (const [s, scene] of Object.entries(SCENES))
    { const id = `${d}-${s}`; if (!ONLY || id === ONLY) jobs.push({ id, prompt: `${scene} ${style} ${WORLD}` }) }
console.log(`${jobs.length} images x $0.039 = $${(jobs.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))
for (const job of jobs) {
  process.stdout.write(`  ${job.id} ... `)
  const sub = await fetch('https://queue.fal.run/fal-ai/nano-banana', {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: job.prompt, num_images: 1, aspect_ratio: '16:9', output_format: 'png' }),
  })
  if (!sub.ok) { console.log(`SUBMIT ${sub.status}`); continue }
  const { status_url, response_url } = JSON.parse(await sub.text())
  let done = false
  for (let i = 0; i < 120 && !done; i++) {
    await sleep(4000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url ?? out?.data?.images?.[0]?.url
      if (!url) { console.log('no image url'); done = true; break }
      writeFileSync(join(OUT, `${job.id}.png`), Buffer.from(await (await fetch(url)).arrayBuffer()))
      console.log('ok'); done = true
    } else if (['FAILED', 'ERROR'].includes(st.status)) { console.log(st.status); done = true }
  }
  if (!done) console.log('timeout')
}
