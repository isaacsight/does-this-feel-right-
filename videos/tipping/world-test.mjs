#!/usr/bin/env node
// Direction bake-off — TIPPING. Three staging rules inside the SERIES world
// (mid-century painted cel — the world is not up for audition, the direction
// is). Each direction carries its own STAGING + LIGHTING + CAMERA rule,
// because light and lens are what make a direction legible:
//
//   tribunal  commerce drawn as JUSTICE. One high overhead shaft on the
//             accused, long floor shadows. Camera frontal, symmetrical,
//             eye-level: the formality IS the joke.
//   theatre   the transaction as PERFORMANCE. Warm footlight wash from
//             below plus one hard spotlight circle. Camera from the stalls:
//             proscenium wides, audience-POV.
//   customs   the tip as BORDER PAPERWORK. Cold daylight in dusty shafts
//             from high windows, green-shade desk lamps. Camera slightly
//             ELEVATED three-quarter views: the surveillance angle.
//
// Four CAST scenes per direction (same dramatic material, so only the
// direction varies): the quarter-turn, the Grand Waiter's palm, the 1912
// rally, the split-check table. 12 images x $0.039 = $0.47.
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
  'round young face and a big confident nose, EXACTLY TWO hairs sticking up from his crown ' +
  'that kink and lean at different angles, a flat VERMILION RED coat with THREE round ' +
  'buttons, thin stick legs and ABSURDLY oversized shoes'
const BARISTA = 'THE BARISTA: a tall young woman in a cream shirt with sleeves rolled to the ' +
  'elbow, a SAGE GREEN half-apron with ONE front pocket, hair in a high knot with ONE pencil ' +
  'through it, a completely BLANK badge, polite and equally embarrassed'
const SLAB = 'an OVERSIZED matte near-black tablet on a steel counter mount, drawn like a ' +
  'monument, with THREE large completely BLANK buttons stacked on its face and ONE small ' +
  'button beneath them'

const WORLD =
  'a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom of ' +
  'the late 1950s: flat gouache-painted backgrounds and flat painted cel figures with ' +
  'confident tapering ink outlines and no interior shading, in a warm graphic palette of ' +
  'INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, cream and flat VERMILION RED. ' +
  'Expressions are BOLD, exaggerated and readable at a glance. Visible gouache texture, ' +
  'flat matte, NO gradients, NO photographic texture, NO 3D rendering. There is NO text, ' +
  'NO lettering, NO numbers and NO writing anywhere; every sign, badge, sash, bill and ' +
  'screen is completely BLANK. Any crowd is individuated: different faces and builds, ' +
  'clothes in DIFFERENT colours from the palette. ORIGINAL characters, NO existing cartoon ' +
  'characters, NO trade dress, no likeness of any real person. ONE SINGLE COHERENT SCENE, ' +
  '16:9, edge to edge, one scene, one camera.'

const DIRS = {
  tribunal:
    'DIRECTION: the scene is staged as a COURTROOM even though it is not one — frontal, ' +
    'symmetrical, eye-level camera squared to the frame; ONE high overhead shaft of light ' +
    'falling on the person being judged, long soft floor shadows, everything else a half ' +
    'step darker; the composition formal and still as a verdict.',
  theatre:
    'DIRECTION: the scene is staged as LIVE THEATRE — the camera sits in the stalls looking ' +
    'at a proscenium; warm footlight wash rising from below on the principals, ONE hard ' +
    'spotlight circle on the point of the drama, the surrounding space falling into warm ' +
    'darkness like a house with the lights down; onlookers arranged like an audience.',
  customs:
    'DIRECTION: the scene is staged as a CUSTOMS HALL of bureaucracy — the camera slightly ' +
    'ELEVATED at a three-quarter angle like a surveillance mezzanine; cold pale daylight in ' +
    'dusty visible shafts from high windows, small warm pools from green-shade desk lamps; ' +
    'counters, gates and rubber stamps as the furniture of the ritual.',
}

const SCENES = {
  s1_quarter_turn:
    `Inside a small cafe, ${BARISTA} rotating ${SLAB} a quarter turn toward ${MAN} with both ` +
    `hands, formally, like presenting evidence, her eyes politely on the middle distance — ` +
    `while he freezes mid-reach for his wallet, eyes wide, and behind him a line of FIVE ` +
    `people in five different palette colours all elaborately look at ceilings and shoes ` +
    `except ONE small child in a striped jumper staring directly at him.`,
  s2_grand_waiter:
    `A magnificent 1890s grand-hotel waiter in a black tailcoat with TWO points, white ` +
    `waistcoat and white bow tie, gold watch-chain in a shallow arc, holding a silver tray ` +
    `aloft with his bare hand while his other hand, in ONE white glove, is held discreetly ` +
    `open at hip height — and ${MAN}, in his same red coat, placing one small coin onto the ` +
    `gloved palm while looking the other way, in a marble hotel lobby with chandeliers.`,
  s3_rally_1912:
    `A 1912 American main street rally: a reformer in a straw boater, rolled shirtsleeves ` +
    `with sleeve garters and a MUSTARD GOLD completely BLANK sash, mid-speech on a soapbox ` +
    `with pamphlets thrust into the air, before a crowd of TWELVE in boaters and cloth caps ` +
    `and shirtwaists, bunting overhead — and ${MAN} in his unchanged red coat among them, ` +
    `holding a pamphlet upside down.`,
  s4_split_check:
    `EIGHT diners around one round restaurant table after dinner, a single BLANK bill ` +
    `standing in the centre like an unexploded device, every face doing a different ` +
    `calculation — one scribbling sums on a napkin, one asleep, one already at the coat ` +
    `rack, one with fingers raised counting — each diner keyed to a different palette ` +
    `colour, one loosened necktie, one pair of reading glasses pushed up a forehead.`,
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
    await sleep(2000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.images?.[0]?.url
      if (url) { writeFileSync(join(OUT, `${job.id}.png`), Buffer.from(await (await fetch(url)).arrayBuffer())); console.log('ok') }
      else console.log('no image url')
      done = true
    } else if (['FAILED','ERROR'].includes(st.status)) { console.log('FAILED'); done = true }
  }
  if (!done) console.log('timed out')
}
console.log(OUT)
