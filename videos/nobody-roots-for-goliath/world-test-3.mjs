#!/usr/bin/env node
// World test ROUND 3: the CHUCK JONES idiom — Isaac's call after the woodcut
// cut came back creepy, humourless, and short on continuity.
//
// WHY THIS WORLD IS STRUCTURALLY RIGHT, not just warmer:
// Wile E. Coyote IS Goliath — better equipped, better funded, technically
// superior, universally resented; the Road Runner does nothing but be small
// and lucky and everyone loves him for it. Jones animated this exact asymmetry
// for twenty years. And the idiom solves the two demands the woodcut strained
// at: the deadpan LOOK TO CAMERA is the best implicate-the-viewer device in
// animation, and the TAKE (smallest movement, biggest read) turns a crowd
// sour with charm instead of dread.
//
// WHAT THE WOODCUT GOT WRONG, measured:
//   character in frame  26% (vs 44-56% in the three films that worked)
//   abstract-object frames 13% — the board illustrated the MECHANISM, not the
//   story, so the pictures floated free of the narration
//   no colour anchor — black-and-white removed the vermilion jersey, and the
//   character stopped being recognisable frame to frame
//
// GUARDRAILS, both in the clause:
//   NO Looney Tunes characters, names or trade dress. We describe the IDIOM
//   (mid-century UPA / Jones-era animation, Maurice Noble background design),
//   never the properties.
//   NO TEXT, stated hard — this idiom's reflex is to letter everything, and a
//   BLANK held sign is funnier than a lettered one anyway.
//
// Probes:
//   k1  BACKGROUND   Noble-style arena: can it build a WORLD, not just a gag
//   k2  CHARACTER    silhouette-locked, vermilion jersey, both kinked hairs
//   k3  DIGNITY      the champion alone — dignified like Wile E., never pitiable
//   k4  TO CAMERA    the deadpan glance at the audience: the film's thesis shot
//   k5  THE TAKE     a crowd turning sour in one held pose, and the blank sign
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

const HERO =
  'the recurring character drawn in mid-century cartoon style: a small slight ' +
  'athlete with a round young face, a big confident nose, EXACTLY TWO hairs ' +
  'standing from the crown that KINK and LEAN at different angles and are ' +
  'different lengths (never symmetrical, never vertical), a flat VERMILION RED ' +
  'sleeveless jersey, thin stick legs and oversized shoes, drawn with a strong ' +
  'readable SILHOUETTE and a confident tapering ink outline'

const CHAMP =
  'the CHAMPION drawn in the same mid-century cartoon style: a large barrel-chested ' +
  'athlete with a heavy brow and a long dignified face, meticulous and impeccably ' +
  'turned out in a flat INK BLUE jersey, drawn with real dignity and a wry ' +
  'intelligence, never grotesque and never pitiable'

const WORLD =
  'a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation ' +
  'idiom of the late 1950s: flat gouache-painted background shapes with stylised ' +
  'ANGULAR GEOMETRY and exaggerated theatrical perspective, characters painted as ' +
  'flat cels with confident tapering ink outlines and no interior shading. The ' +
  'palette is warm and graphic: dusty ORANGE and terracotta, INK BLUE, mustard ' +
  'GOLD, sage GREEN, cream and flat VERMILION RED accents. Crowds are painted as ' +
  'ranked rows of simplified flat graphic shapes rather than rendered faces. ' +
  'Visible painted gouache texture and slight brush grain in the background ' +
  'washes. Expressions are BOLD and readable at a glance. Flat matte throughout: ' +
  'NO gradients, NO airbrushed shading, NO photographic texture, NO three-' +
  'dimensional rendering, NO modern digital gloss. ' +
  // Guardrails.
  'This is an ORIGINAL character and an original scene in a general mid-century ' +
  'cartoon idiom: NO existing cartoon characters, NO studio logos, NO trade dress, ' +
  'NO recognisable franchise designs of any kind. ' +
  'There is NO text, NO lettering, NO numbers, NO signage copy and NO writing of ' +
  'any kind anywhere in the image; any sign or board that appears is completely ' +
  'BLANK. This is ONE SINGLE COHERENT SCENE, NOT a grid, NOT a model sheet, NOT a ' +
  'sheet of studies. 16:9, edge to edge, one scene, one camera.'

const TESTS = {
  k1_background:
    `A wide stylised arena built from flat angular painted shapes: a sweeping ` +
    `terracotta bowl of ranked seating rendered as rows of simplified flat graphic ` +
    `spectator shapes, an exaggerated raked perspective, a flat cream floor, and ` +
    `${HERO} standing TINY at the centre of it. Bold, graphic and warm.`,
  k2_character:
    `${HERO}, standing alone on a flat cream floor against a plain dusty orange ` +
    `background, one arm raised in a small hopeful salute, weight on one leg. ` +
    `Nothing else in the frame.`,
  k3_dignity:
    `${CHAMP} standing alone in the centre of an empty stylised arena, perfectly ` +
    `composed, immaculate, one eyebrow slightly raised, entirely alone, with the ` +
    `ranked flat spectator shapes behind him all turned away from him.`,
  k4_tocamera:
    `CLOSE on ${CHAMP} looking DIRECTLY out of the frame at the viewer with a flat ` +
    `deadpan expression and one eyebrow raised a fraction, holding the look, while ` +
    `far behind him a crowd of flat graphic spectator shapes cheers for somebody ` +
    `else off-frame.`,
  k5_thetake:
    `A crowd of DOZENS of flat graphic spectators packed in ranked rows, caught in ` +
    `one held moment as their cheer curdles: mouths flattening, eyes narrowing, arms ` +
    `folding, all in unison — and in the front row one spectator holds up a large ` +
    `completely BLANK white sign board with nothing written on it at all.`,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(TESTS)
console.log(`${ids.length} jones-test images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
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
        writeFileSync(join(OUT, `jones-${id}.png`),
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
