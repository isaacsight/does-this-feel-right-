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
  deadpan:
    'DIRECTION: DEADPAN - the composition is butler-formal: perfectly symmetrical, squared ' +
    'to the camera, generous still space around the subject, and every character HOLDS ' +
    'PERFECTLY STILL mid-absurdity with a completely composed face, as if posing for a ' +
    'formal portrait while something ridiculous is plainly happening; flat even light, ' +
    'nothing dramatic; the joke is the stillness.',
  club:
    'DIRECTION: CLUB - a dark room and ONE hard spotlight circle; the surround is filled ' +
    'with the dark silhouettes of seated onlookers, rows of them, individuated in outline; ' +
    'ONE wall glows a deep warm brick red at the back; whatever the point of the frame is ' +
    'stands lit inside the spotlight circle and everything else keeps politely to the dark.',
  twist:
    'DIRECTION: TWIST - the scene is drawn clean, orderly and reassuring, with EXACTLY ONE ' +
    'wrong detail placed quietly for the second look (never central, never pointed at); ' +
    'flat daylight, tidy composition, the wrongness sized small and matter-of-fact; ' +
    'everyone in the frame behaves as if the wrong detail is completely normal.',
}

const DONKEY = 'ONE grey donkey with a composed patient face standing exactly midway between ONE neat pile of hay and ONE full pail of water'

const SCENES = {
  s1_donkey:
    `${DONKEY}, its head facing straight forward between them, on a bare flat field, the hay ` +
    `and the pail drawn at exactly equal size and exactly equal distance.`,
  s2_gym_wall:
    `A gymnasium wall with ONE large completely BLANK framed plaque mounted high, and below ` +
    `it ${MAN} mid-jumping-jack, arms up, looking up at the blank plaque with his brows ` +
    `knotted, TWO dumbbells parked neatly at his feet.`,
  s3_snowstorm_tickets:
    `A theatre entrance in a heavy snowstorm, snow driving sideways: a queue of FIVE people ` +
    `wrapped in coats and scarves gripping ONE completely BLANK ticket each, leaning into ` +
    `the wind toward the doors, and ${MAN} among them in his red coat, his scarf straight ` +
    `out behind him, his ticket held in both mittens.`,
  s4_windowsill_plant:
    `A small potted plant on a windowsill in morning light, ONE elderly hand tipping ONE ` +
    `small watering can over it, the water mid-pour, a plain calm room behind.`,
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
