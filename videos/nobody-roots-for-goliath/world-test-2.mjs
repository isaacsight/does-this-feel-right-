#!/usr/bin/env node
// World test ROUND 2: three more worlds, probed against the WILLIAMSON demands
// the first round never tested.
//
//   woodcut   Masereel-style wordless woodcut novel — the individual vs the mass
//   isotype   Neurath ISOTYPE pictogram — statistics made visible, quantity as picture
//   ukiyoe    Japanese woodblock print — sumo crowds, flat colour, real faces
//
// WHY THESE THREE. Round 1 tested whether a world could stage a contest. This
// film's register is Chris Williamson: reveal a mechanism, implicate the viewer,
// re-read the same image, and stay STILL rather than absurd. So:
//   woodcut  invented for exactly this story — Masereel's wordless novels are
//            one small figure against a carved mass of identical heads
//   isotype  invented to make social statistics visible to ordinary people,
//            which is the film's citations turned into pictures
//   ukiyoe   crowds AND expressive faces AND a native giant (the sumo), flat matte
//
// THE PROBES ARE THE FOUR UNTESTED DEMANDS, plus a cast check:
//   k1  CROWD-POV      are we INSIDE the crowd — the film's real subject is us
//   k2  CHARACTER      does he survive, and does he sit in the same drawing
//                      register as the adults (round 1's litho made him a mascot)
//   k3  LONELY GIANT   the favourite's isolation — the emotional payload
//   k4  SKIN IN GAME   the mechanism made physical: a wager changing hands
//   k5  THE TURN       DOZENS of faces souring in unison, mid-flip
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

const NOTEXT =
  'There is NO text, NO lettering, NO numbers and NO writing of any kind ' +
  'anywhere in the image. This is ONE SINGLE COHERENT SCENE, NOT a grid, NOT a ' +
  'sheet of studies. 16:9, edge to edge, one scene, one camera.'

const WORLDS = {
  woodcut: {
    hero:
      'the recurring character cut as a WOODCUT FIGURE: a small man carved in bold ' +
      'black and white with EXACTLY TWO hairs standing from the crown that KINK ' +
      'and LEAN at different angles and are different lengths (never symmetrical), ' +
      'a plain working tunic, thin legs, his face built from a few decisive gouged ' +
      'white cuts through solid black — drawn with the same carved weight and adult ' +
      'seriousness as every other figure in the scene, never cartoonish',
    world:
      'a BLACK AND WHITE WOODCUT PRINT in the manner of Frans Masereel and German ' +
      'expressionist wordless novels: bold carved black shapes on white paper, all ' +
      'form made by decisive GOUGED WHITE CUTS through solid black ink, with ' +
      'visible chisel and burin marks and slightly ragged carved edges. Strong ' +
      'diagonal composition and heavy dramatic contrast. Crowds are carved as ' +
      'dense masses of nearly identical heads. Faces are simplified but genuinely ' +
      'expressive, weighted and serious. Real relief-print texture with ink ' +
      'variation and paper grain. STRICTLY BLACK AND WHITE ONLY, no colour ' +
      'anywhere, no grey wash, no gradients, no photographic texture.',
  },
  isotype: {
    hero:
      'the recurring character as an ISOTYPE PICTOGRAM: a small flat symbol of a ' +
      'man in solid VERMILION RED, simplified to a geometric silhouette, with ' +
      'EXACTLY TWO tiny hairs standing from the crown that KINK and LEAN at ' +
      'different angles and different lengths, rendered with the same flat ' +
      'diagrammatic clarity as every other pictogram in the frame',
    world:
      'an ISOTYPE PICTORIAL STATISTICS CHART in the manner of Otto Neurath and ' +
      'Gerd Arntz, 1930s Vienna: flat geometric PICTOGRAM figures repeated in ' +
      'orderly rows to show quantity, printed in a strictly limited palette of ' +
      'VERMILION RED, INK BLACK, MUSTARD GOLD and pale GREY-BLUE on warm cream ' +
      'paper. Every shape is flat, geometric and hard-edged with no modelling. ' +
      'Quantity is always shown by REPEATING a symbol, never by making it bigger, ' +
      'except where the picture deliberately shows power. Clean horizontal ' +
      'register lines organise the composition. Flat matte print, NO gradients, NO ' +
      'shading, NO photographic texture, NO three-dimensional perspective.',
  },
  ukiyoe: {
    hero:
      'the recurring character drawn as a UKIYO-E WOODBLOCK FIGURE: a small slight ' +
      'wrestler with a round young face drawn in fine confident black outline with ' +
      'flat colour fill, EXACTLY TWO hairs standing from the crown that KINK and ' +
      'LEAN at different angles and are different lengths (never symmetrical), a ' +
      'VERMILION RED belt, drawn with the same adult seriousness as every other ' +
      'figure, never cartoonish',
    world:
      'a JAPANESE UKIYO-E WOODBLOCK PRINT in the manner of Edo-period sumo and ' +
      'theatre prints: fine confident black keyblock OUTLINES filled with flat ' +
      'unmodulated colour in vermilion RED, indigo BLUE, mustard OCHRE, soft ' +
      'GREEN and the warm cream of the paper, with visible woodgrain in the flat ' +
      'areas and slight registration offset between colour blocks. Faces are drawn ' +
      'with a few precise expressive lines. Crowds are stacked in tiers of ' +
      'individually drawn heads. Bold flat pattern everywhere, strong diagonal ' +
      'composition, and a plain colour-block sky. Flat matte print, NO gradients, ' +
      'NO photographic depth, NO digital smoothness.',
  },
}

const probes = (W) => ({
  k1_crowdpov:
    `Seen from INSIDE a crowd of spectators, over and between the shoulders and ` +
    `heads of DOZENS of people in the near foreground who fill the lower half of ` +
    `the frame with their backs to us, all of them looking down at a distant arena ` +
    `floor far below where one TINY figure stands alone. We are standing in the ` +
    `crowd, not watching it.`,
  k2_character:
    `${W.hero}, standing alone on an empty arena floor, one arm raised in a small ` +
    `hopeful salute, looking up and away. Nothing else in the frame.`,
  k3_lonelygiant:
    `CLOSE-UP filling the frame on the head and shoulders of an ENORMOUS champion: ` +
    `a huge powerful man with a heavy jaw, alone, mouth flat, eyes lowered and ` +
    `tired, no triumph in him at all, while far behind him a blurred mass of ` +
    `spectators face the other way. Nothing else.`,
  k4_skininthegame:
    `CLOSE on a single spectator's TWO hands in the foreground, COLOSSAL in frame, ` +
    `pressing a small folded wager slip into another person's palm, while behind ` +
    `and above them DOZENS of tiny cheering spectators fill the stands. The hands ` +
    `are the subject; the crowd is the background.`,
  k5_theturn:
    `A dense wall of DOZENS of spectator faces filling the entire frame, all at the ` +
    `exact same moment of turning sour: mouths flattening, brows lowering, arms ` +
    `beginning to fold, every single face looking in the same direction off-frame ` +
    `with the cheer draining out of it.`,
})

mkdirSync(OUT, { recursive: true })
const jobs = []
for (const [wid, W] of Object.entries(WORLDS))
  for (const [pid, prompt] of Object.entries(probes(W)))
    jobs.push({ id: `${wid}-${pid}`, prompt: `${prompt} ${W.world} ${NOTEXT}` })

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
