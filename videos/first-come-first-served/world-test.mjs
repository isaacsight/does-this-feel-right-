#!/usr/bin/env node
// World test — First Come, First Served. THREE DIRECTIONS, 5 probes each.
//
// These are EPISODES now, not one-off films, so all three keep the mid-century
// animation idiom established in the underdog episode. What changes is the
// DIRECTION, not the medium — four episodes in four worlds is an anthology; a
// recurring world is a show.
//
//   krisel  Jonathan Krisel's rigid centred symmetry: the queue runs dead down
//           the middle to a vanishing point, everything still, comedy from
//           composure. Cheapest, strongest series continuity.
//   erakey  Mary Blair's colour keying: ONE idiom, three eras, each with its
//           own emotional palette - 1837 Paris soot and ochre, 1986 New York
//           concrete and subway orange, today cool grey-blue and screen light.
//           Fixes repetition at the source rather than by re-staging after.
//   route   Vignelli transit-diagram logic: the queue drawn as a bold flat
//           ROUTE LINE running through every composition, people as beads on
//           it. Best pure idea, real risk - the ISOTYPE probe proved diagram
//           worlds cannot hold an expression, and this episode lives on a tut.
//
// The probes are chosen so the three directions are judged on the SAME jobs:
//   k1  THE LINE     a queue running to a vanishing point - the episode's motif
//   k2  THE TUT      the enforcement mechanism of the entire system, in close-up
//   k3  1837         Carlyle's Paris bread queue - can the direction do history
//   k4  1986         Milgram's New York intrusion - can it do the experiment
//   k5  THE CROWD    ordinary strangers, individuated, mildly disapproving
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

// The established cast, carried across from the underdog episode. A recurring
// character is the single cheapest series signal we have.
const HERO =
  'the recurring character in mid-century cartoon style: a small slight man with a ' +
  'round young face and a big confident nose, EXACTLY TWO hairs standing from the ' +
  'crown that KINK and LEAN at different angles and are different lengths (never ' +
  'symmetrical, never vertical), a flat VERMILION RED coat, thin stick legs and ' +
  'ABSURDLY oversized shoes, drawn with a strong readable silhouette and a ' +
  'confident tapering ink outline'

const BASE =
  'a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation ' +
  'idiom of the late 1950s: flat gouache-painted backgrounds, characters painted as ' +
  'flat cels with confident tapering ink outlines and no interior shading. Crowds ' +
  'are painted as ranked rows of simplified flat graphic shapes with distinct faces. ' +
  'Visible painted gouache texture and slight brush grain. Expressions are BOLD and ' +
  'readable at a glance. Flat matte throughout: NO gradients, NO airbrushed shading, ' +
  'NO photographic texture, NO three-dimensional rendering, NO modern digital gloss. ' +
  'This is an ORIGINAL character and an original scene in a general mid-century ' +
  'cartoon idiom: NO existing cartoon characters, NO studio logos, NO trade dress, ' +
  'NO recognisable franchise designs. There is NO text, NO lettering, NO numbers, NO ' +
  'signage copy and NO writing of any kind anywhere in the image; any sign or board ' +
  'that appears is completely BLANK. ONE SINGLE COHERENT SCENE, NOT a grid, NOT a ' +
  'sheet of studies. 16:9, edge to edge, one scene, one camera.'

const DIRS = {
  krisel: {
    style: 'The palette is warm and graphic from INK BLUE, mustard GOLD, sage GREEN, ' +
      'dusty ORANGE, cream and flat VERMILION RED. ' +
      'DIRECTION: rigid CENTRED SYMMETRY - the composition is mirrored left to right ' +
      'about a dead-centre vertical axis, everything squared to the frame, the camera ' +
      'perfectly level and head-on, every figure still and composed. Deadpan, formal, ' +
      'held a beat too long. ' + BASE,
    keys: { k3: '', k4: '', },
  },
  erakey: {
    style: 'DIRECTION: the scene is COLOUR KEYED to its era in the manner of Mary ' +
      'Blair - one dominant emotional palette per scene rather than one palette for ' +
      'the whole film, with the drawing idiom held constant. ' + BASE,
    keys: {
      k1: 'The palette is keyed COOL: slate grey-blue, pale concrete, cold white daylight, one flat VERMILION accent. ',
      k2: 'The palette is keyed COOL: slate grey-blue, pale concrete, cold white daylight, one flat VERMILION accent. ',
      k3: 'The palette is keyed to 1837 PARIS: soot black, ochre, bread-crust brown, dirty cream, one flat VERMILION accent. ',
      k4: 'The palette is keyed to 1986 NEW YORK: concrete grey, subway ORANGE, fluorescent GREEN, dull steel, one flat VERMILION accent. ',
      k5: 'The palette is keyed WARM: mustard gold, dusty orange, sage green, cream, one flat VERMILION accent. ',
    },
  },
  route: {
    style: 'The palette is bold and flat from INK BLUE, mustard GOLD, sage GREEN, ' +
      'dusty ORANGE, cream and flat VERMILION RED. ' +
      'DIRECTION: a bold flat ROUTE LINE in the manner of a mid-century transit ' +
      'diagram runs through the composition, thick and unbroken with rounded corners ' +
      'and strict horizontal, vertical and forty-five degree angles, and the waiting ' +
      'people are strung along it like beads on a wire. The diagram line and the ' +
      'painted scene occupy the same picture. ' + BASE,
    keys: {},
  },
}

const PROBES = {
  k1: `A queue of DOZENS of ordinary people standing one behind another, running away ` +
      `from the camera to a distant vanishing point, with ${HERO} standing third from ` +
      `the front looking back along it.`,
  k2: `CLOSE on ${HERO} making one small disapproving noise with his tongue - lips ` +
      `pursed, eyes flat, chin slightly raised, the tiniest possible act of ` +
      `enforcement - while behind him the queue continues, unbothered.`,
  k3: `A bread queue outside a bakery in Paris in the 1790s: DOZENS of hungry people ` +
      `in long coats and shawls standing patiently in a line down a narrow street, ` +
      `one baker's shutter, nothing else. Cold, orderly and desperate.`,
  k4: `A busy 1980s New York railway ticket hall: a line of DOZENS of commuters, and ` +
      `one man in a plain jacket stepping in at the second position from the front ` +
      `while the man behind him reacts with a look but does not move.`,
  k5: `A wall of DOZENS of ordinary people in a queue, each with a distinct face, ` +
      `every single one of them wearing the same small expression of mild ` +
      `disapproval - eyebrows slightly raised, mouths flat - and not one of them ` +
      `actually doing anything about it.`,
}

mkdirSync(OUT, { recursive: true })
const jobs = []
for (const [did, d] of Object.entries(DIRS))
  for (const [pid, probe] of Object.entries(PROBES))
    jobs.push({ id: `${did}-${pid}`, prompt: `${probe} ${d.keys[pid] ?? ''}${d.style}` })

console.log(`${jobs.length} images x $0.039 = $${(jobs.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const job of jobs) {
  process.stdout.write(`  ${job.id} ... `)
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: job.prompt, num_images: 1,
                           aspect_ratio: '16:9', output_format: 'png' }),
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
      if (url) {
        writeFileSync(join(OUT, `${job.id}.png`),
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
