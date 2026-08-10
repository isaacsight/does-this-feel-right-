#!/usr/bin/env node
// World test: THREE candidate worlds for the duel film, 5 probes each.
//
//   gillray   hand-coloured Regency etching — the medium that killed the duel
//   manual    copperplate etiquette-manual plates — the code duello as diagrams
//   theatre   Victorian toy theatre — men moved by rules like paper puppets
//
// Same probe set as the collage test, adapted to this film's actual scenes:
//   k1  SCENE       the dawn field, two figures, seconds — one coherent picture
//   k2  CHARACTER   does he survive translation into the medium
//   k3  CLOSE-UP    does an aggrieved expression survive it
//   k4  MEDIUM      the risk specific to this world (wash, diagram grammar, rods)
//   k5  ENVIRONMENT the crowded drawing room where the hat gets bumped
//
// NO TEXT is the house rule and the etiquette-manual world is the one most
// likely to break it — a manual WANTS captions. Its clause forbids letters and
// leans on pointing hands and dotted arrows instead. If it comes back covered
// in pseudo-text, that world fails its own probe and we say so.
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
  'There is NO text, NO lettering, NO numbers, NO signatures and NO writing of ' +
  'any kind anywhere in the image. This is ONE SINGLE COHERENT SCENE, NOT a ' +
  'grid, NOT a sheet of studies. 16:9, edge to edge, one scene, one camera.'

const WORLDS = {
  gillray: {
    hero:
      'the recurring character drawn as a REGENCY CARICATURE: a small round-headed ' +
      'man with EXACTLY TWO hairs standing from the crown that KINK and LEAN at ' +
      'different angles and different lengths (never symmetrical, never rabbit ' +
      'ears), a huge VERMILION RED tailcoat far too big for him, tiny spindly legs, ' +
      'buckled shoes, drawn in fine crosshatched etched linework with flat ' +
      'watercolour wash',
    world:
      'a HAND-COLOURED REGENCY ETCHING in the manner of British satirical prints ' +
      'circa 1800: fine crosshatched copper-etched linework in warm sepia-black ink ' +
      'on aged cream laid paper, coloured with flat translucent watercolour washes ' +
      'in vermilion red, prussian blue, mustard yellow, sage green and rose pink ' +
      'that sit loosely inside the lines. Faces and bodies are CARICATURED: bulging ' +
      'eyes, ballooning coats, tiny legs, enormous indignant gestures. Visible ' +
      'plate tone and paper grain, slightly uneven wash edges, a faint plate-mark ' +
      'border. Flat matte, NO photographic texture, NO digital gradients.',
  },
  manual: {
    hero:
      'the recurring character drawn as an INSTRUCTIONAL FIGURE: a small ' +
      'round-headed man with EXACTLY TWO kinked hairs of different lengths leaning ' +
      'at different angles, wearing a plain tailcoat, rendered in precise ' +
      'copperplate-engraved outline with fine parallel-line shading, posed stiffly ' +
      'like a figure demonstrating correct form in a manual',
    world:
      'a COPPERPLATE ENGRAVING PLATE from an eighteenth-century instruction manual: ' +
      'precise fine-lined engraving in near-black ink on cream laid paper, figures ' +
      'posed in stiff instructional attitudes, with DOTTED GUIDE LINES, measuring ' +
      'chains, small pointing-hand manicule symbols and dashed arrows indicating ' +
      'correct movement and distance. One spot colour only: a flat VERMILION RED ' +
      'accent on one element per scene. Ruled thin double border like a book ' +
      'plate. Flat matte, engraved parallel-line and crosshatch shading only, NO ' +
      'photographic texture, NO gradients.',
  },
  theatre: {
    hero:
      'the recurring character as a TOY THEATRE PAPER ACTOR: a small flat ' +
      'cut-paper figure of a round-headed man with EXACTLY TWO kinked hairs of ' +
      'different lengths, a VERMILION RED tailcoat, painted in flat gouache with ' +
      'visible brush texture, mounted on a thin visible BRASS CONTROL ROD entering ' +
      'from the side or below, casting a small footlight shadow',
    world:
      'a VICTORIAN TOY THEATRE scene: a miniature paper stage with painted ' +
      'cardboard scenery flats in layered rows, a decorated proscenium arch at the ' +
      'edges, warm footlight glow from below, flat cut-paper actors on visible ' +
      'brass rods. Palette of vermilion red, prussian blue, mustard yellow, sage ' +
      'green and cream, painted in flat gouache with visible brushwork on ' +
      'cardboard. Everything is visibly PAPER AND CARDBOARD on a small stage. ' +
      'Flat matte, NO photographic realism, NO digital gradients.',
  },
}

const probes = (W) => ({
  k1_scene:
    `A wide dawn scene on an empty misty field: two small figures standing ` +
    `back-to-back in the middle distance about to pace apart, ${W.hero} as the ` +
    `left figure, a taller stouter gentleman as the right figure, one bare tree, ` +
    `a huge pale rising sun low on the horizon. Nothing else.`,
  k2_character:
    `${W.hero}, standing alone facing the camera in the middle of an open field, ` +
    `holding a muddy hat in both hands at arm's length, looking at it with dismay. ` +
    `Nothing else in the frame.`,
  k3_closeup:
    `CLOSE-UP filling the frame on the head and shoulders of ${W.hero}, face ` +
    `contorted in ABSURD aggrieved indignation: eyes bulging, brows shot up, mouth ` +
    `open mid-complaint, one hand raised in protest. Nothing else.`,
  k4_medium:
    `Two duelling pistols lying in an open velvet-lined case, ENORMOUS in frame, ` +
    `presented like sacred objects, with ${W.hero} peering over the edge of the ` +
    `case from behind, only his eyes and two hairs visible. Nothing else.`,
  k5_environment:
    `A crowded candlelit drawing room: DOZENS of gentlemen in tailcoats frozen ` +
    `mid-gasp, all staring toward ${W.hero} who stands at the centre holding his ` +
    `knocked-off hat, beside a card table with scattered cards. Comic and busy but ` +
    `one clear focal point.`,
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
