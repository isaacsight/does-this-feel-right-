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
  ember:
    'DIRECTION: LIGHT IS MEMBERSHIP — every warm golden light in the frame belongs to a ' +
    'group of people somewhere the man is not: lit windows, glowing doorways, lamplit ' +
    'rooms full of company; he stands in cool INK BLUE dusk outside them. The camera is ' +
    'at street level and frames him through or beside a threshold — a window pane, a ' +
    'doorway, a fence — so the warmth is always exactly one pane of glass away. The warm ' +
    'areas are flat MUSTARD GOLD, the cool areas flat ink blue, both painted matte.',
  vacancy:
    'DIRECTION: THE EMPTY SECOND PLACE — flat, even, ordinary daylight with no dramatic ' +
    'lighting at all; the composition itself carries the feeling by drawing a clearly ' +
    'EMPTY place set for a second person as carefully as a character: the vacant chair ' +
    'squared to the occupied one, the empty half of the frame given equal weight. Camera ' +
    'frontal, still, eye-level, perfectly balanced so the absence sits in the picture ' +
    'like a person would.',
  procession:
    'DIRECTION: THE MIRRORED CENTURY — the scene is staged as a FORMAL GROUP PORTRAIT or ' +
    'ceremonial procession: rows, ranks, symmetrical banquet formations, composed square ' +
    'to the camera at portrait height like a photographer\'s studio. Scenes set in the ' +
    'past are FULL: ranks of men in regalia, mustard sashes and ceremonial collars ' +
    'filling the frame. Scenes set today hold the SAME formal composition nearly EMPTY, ' +
    'the ranks drawn as bare floor.',
}

const SCENES = {
  s1_phone:
    `A small living room at dusk: ${MAN} sitting on ONE end of a two-person sofa, hands ` +
    `on his knees, staring at a telephone lying on the coffee table an arm's length away, ` +
    `leaning very slightly toward it without reaching, the other sofa cushion empty beside ` +
    `him.`,
  s2_lodge_1924:
    `A grand lodge hall in 1924 in full ceremony: TWELVE men in dark suits with mustard ` +
    `GOLD ceremonial collars and completely BLANK sashes standing in two facing rows, one ` +
    `raising a gavel, banners overhead all completely BLANK, candles lit — and ${MAN}, in ` +
    `his same red coat among the ranks, mid-secret-handshake with a large beaming man, ` +
    `both their faces lit with the pleasure of a Tuesday.`,
  s3_sidewalk_goodbye:
    `A sidewalk outside a small restaurant at midday: ${MAN} and a big warm man in a sage ` +
    `GREEN jacket parting after lunch, both walking BACKWARD away from each other in ` +
    `opposite directions, both waving, both mouths open in cheerful promises, the distance ` +
    `between them already wide and widening.`,
  s4_two_chairs:
    `A small back porch in late afternoon: TWO folding chairs set up side by side facing ` +
    `the yard, ${MAN} sitting in one holding TWO bottles of soda, one in each hand, the ` +
    `second chair empty, a small cooler between the chairs with its lid open.`,
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
