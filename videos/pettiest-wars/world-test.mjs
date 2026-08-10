#!/usr/bin/env node
// World test: THREE candidate worlds for the pettiest-wars film, 5 probes each.
//
//   bayeux   stitched narrative tapestry — how wars get mythologized
//   tin      toy armies on a campaign map table — states as boys with toys
//   litho    heroic victory lithograph — pettiness dressed as glory
//
// Probes, adapted to this film's actual scenes:
//   k1  SCENE       two tiny armies facing off across a valley, trophy between
//   k2  CHARACTER   does he survive translation into the medium
//   k3  CLOSE-UP    does an aggrieved/awed expression survive it
//   k4  TROPHY      the film's whole gag — a BUCKET venerated like a relic
//   k5  ENVIRONMENT a crowded war council losing its mind over something tiny
//
// The kill-risks per world, named so the sheets get read honestly:
//   bayeux  does thread texture read at 16:9, or come back as flat clipart
//   tin     does every frame collapse into the same tabletop composition
//   litho   can it do a SCENE at all, or only monuments
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
  bayeux: {
    hero:
      'the recurring character as an EMBROIDERED FIGURE: a small man with a round ' +
      'young face stitched in outline, EXACTLY TWO couched-thread hairs standing ' +
      'from the crown that KINK and LEAN at different angles and different lengths ' +
      '(never symmetrical), a tunic stitched in VERMILION RED wool, thin stitched ' +
      'legs, every part of him made of visible laid-and-couched wool thread',
    world:
      'a MEDIEVAL EMBROIDERED TAPESTRY in the manner of the Bayeux Tapestry: ' +
      'figures and objects stitched in coloured wool thread on coarse natural ' +
      'LINEN cloth, with visible individual stitches, laid-and-couched work in the ' +
      'solid areas and stem-stitch outlines. The palette is wool colours only: ' +
      'VERMILION RED, deep INDIGO BLUE, MUSTARD OCHRE, sage GREEN, walnut BROWN ' +
      'and the bare linen ground, with small accents of couched GOLD THREAD. ' +
      'Figures are stylised and slightly stiff like Romanesque embroidery, with ' +
      'expressive oversized hands and faces. A narrow decorative embroidered ' +
      'border of small beasts runs along the top and bottom edges. The linen weave ' +
      'is visible everywhere. Flat matte, NO photographic depth, NO gradients, NO ' +
      'digital smoothness.',
  },
  tin: {
    hero:
      'the recurring character as a PAINTED TIN SOLDIER: a small round-headed ' +
      'figurine with a round young painted face, EXACTLY TWO wire hairs soldered ' +
      'to the crown that KINK and LEAN at different angles and different lengths, ' +
      'a glossy VERMILION RED painted coat with visible brushstrokes and chipped ' +
      'paint at the edges, standing on a small round tin base',
    world:
      'a MINIATURE WARGAME TABLE photographed as a painted still life: regiments ' +
      'of small painted tin soldiers arranged on a large canvas campaign map with ' +
      'painted rivers and hills, wooden blocks for towns, and measuring sticks. ' +
      'Warm lamplight from one side, shallow toy-scale depth. The palette is ' +
      'VERMILION RED and PRUSSIAN BLUE regiments, cream map canvas, MUSTARD and ' +
      'sage map terrain, dark walnut table wood. Everything is visibly TOY: ' +
      'chipped enamel paint, solder seams, tin bases, the map\'s painted edge. ' +
      'Painterly matte finish like a museum diorama painting, NO photorealism.',
  },
  litho: {
    hero:
      'the recurring character drawn in a VICTORY LITHOGRAPH: a small man with a ' +
      'round young face, EXACTLY TWO lithographic-crayon hairs standing from the ' +
      'crown that KINK and LEAN at different angles and different lengths, an ' +
      'oversized VERMILION RED military coat with gold buttons, tiny legs, drawn ' +
      'in soft lithographic crayon with flat spot-colour fills',
    world:
      'a NINETEENTH-CENTURY COMMEMORATIVE LITHOGRAPH in the manner of heroic ' +
      'victory prints: soft lithographic crayon shading with flat spot colours - ' +
      'VERMILION RED, PRUSSIAN BLUE, MUSTARD GOLD, sage GREEN - on warm cream ' +
      'paper, with dramatic heroic staging: billowing smoke, radiating sunbeams, ' +
      'laurel garlands, fluttering blank banners and ornate scrollwork corners. ' +
      'Everything is staged with ABSURD monumental pomp regardless of subject. ' +
      'Flat matte stone-print texture with visible crayon grain, NO photographic ' +
      'texture, NO digital gradients.',
  },
}

const probes = (W) => ({
  k1_scene:
    `A wide valley scene: TWO tiny armies facing each other from opposite hillsides, ` +
    `one dressed in vermilion and one in blue, and in the exact centre of the empty ` +
    `valley floor between them stands one ordinary wooden BUCKET, small and alone. ` +
    `${W.hero} stands at the front of the vermilion army, pointing at the bucket.`,
  k2_character:
    `${W.hero}, standing alone on an open ground, holding one ordinary wooden bucket ` +
    `out at arm's length with both hands, looking at it with deep suspicion. Nothing else.`,
  k3_closeup:
    `CLOSE-UP filling the frame on the head and shoulders of ${W.hero}, eyes ABSURDLY ` +
    `wide with outrage, mouth open mid-protest, both hands raised into frame. Nothing else.`,
  k4_trophy:
    `One ordinary wooden BUCKET displayed like a holy relic: raised on an ornate ` +
    `pedestal, surrounded by candles, with TWO kneeling guards flanking it and golden ` +
    `rays radiating from behind it, drawn with ABSURD reverence. Nothing else.`,
  k5_environment:
    `A crowded war council: DOZENS of generals around an ENORMOUS table, every one of ` +
    `them shouting and pointing at the centre of the table, where one TINY dead pig ` +
    `lies on a velvet cushion. ${W.hero} stands on his chair to see it. Comic and busy ` +
    `but one clear focal point.`,
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
