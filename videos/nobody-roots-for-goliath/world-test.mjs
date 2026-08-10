#!/usr/bin/env node
// World test: THREE candidate worlds for the underdog-bias film, 5 probes each.
//
//   attic    Greek vase painting — the world where athletic crowds were FIRST painted
//   glass    stained glass — David and Goliath's own medium, mythic and reverent
//   litho    1950s-60s halftone sports poster — Chamberlain's own era
//
// This film's register is Chris Williamson, not Larry David: REVEAL a mechanism,
// don't litigate a rule. So the probes test whether a world can carry a TURN —
// the same crowd reading two ways — rather than an escalating gag.
//
// Probes:
//   k1  SCENE       the crowd leaning toward the small figure, away from the big
//   k2  CHARACTER   does he survive translation into the medium
//   k3  CLOSE-UP    does the FAVOURITE's isolated face survive it
//   k4  REVERSAL    the same figure now large — the crowd has turned
//   k5  ENVIRONMENT a packed arena, busy but with one focal point
//
// Kill-risks, named so the sheets get read honestly:
//   attic  can it do an EXPRESSION, or is silhouette too flat for a face
//   glass  is it too reverent to carry a debunk; do leads eat small figures
//   litho  is it illustration rather than a world (same fault that sank the
//          victory-lithograph world for the duel film)
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
  attic: {
    hero:
      'the recurring character painted as a GREEK VASE FIGURE: a small man in ' +
      'glossy black silhouette on terracotta ground, with EXACTLY TWO hairs ' +
      'standing from the crown that KINK and LEAN at different angles and are ' +
      'different lengths (never symmetrical), a short belted tunic, thin legs, ' +
      'his face and features drawn as fine INCISED lines scratched through the ' +
      'black glaze to the clay beneath',
    world:
      'an ANCIENT GREEK VASE PAINTING in the black-figure and red-figure manner: ' +
      'figures in glossy black slip on warm TERRACOTTA orange clay, with fine ' +
      'INCISED linework scratched through the glaze for muscles, faces and folds, ' +
      'plus small touches of added white and oxblood PURPLE-RED. Figures are ' +
      'stylised and profile-facing with large almond eyes and expressive ' +
      'oversized hands. Bands of geometric MEANDER key-pattern and palmette ' +
      'ornament run along the top and bottom edges. The clay surface shows real ' +
      'ceramic texture and slight firing mottle. Flat matte, NO photographic ' +
      'depth, NO gradients, NO digital smoothness.',
  },
  glass: {
    hero:
      'the recurring character rendered in STAINED GLASS: a small man built from ' +
      'panes of coloured glass held in thick black lead came, with EXACTLY TWO ' +
      'hairs standing from the crown as two thin leaded slivers that KINK and ' +
      'LEAN at different angles and different lengths, a tunic of deep RUBY RED ' +
      'glass, limbs of amber glass, his face a pale glass pane with painted ' +
      'black line detail',
    world:
      'a MEDIEVAL STAINED GLASS WINDOW: every shape is a pane of coloured glass ' +
      'bounded by thick BLACK LEAD CAME lines, glowing as if strongly backlit. ' +
      'The palette is jewel glass only: deep RUBY RED, COBALT BLUE, emerald ' +
      'GREEN, AMBER gold, violet and pale white glass. Faces and drapery carry ' +
      'painted black trace-line detail and stippled shading fired onto the glass. ' +
      'Figures are stylised and frontal like Romanesque church glass. A border of ' +
      'small repeating glass quatrefoils runs along the top and bottom edges. The ' +
      'glass shows real surface texture, bubbles and streaks. Flat luminous ' +
      'colour, NO photographic depth, NO digital gradients.',
  },
  litho: {
    hero:
      'the recurring character drawn as a MID-CENTURY SPORTS POSTER FIGURE: a ' +
      'small athlete with a round young face, EXACTLY TWO hairs standing from the ' +
      'crown that KINK and LEAN at different angles and different lengths, a ' +
      'VERMILION RED jersey, thin legs, drawn in bold flat colour blocks with ' +
      'coarse halftone dot shading and slightly misregistered outlines',
    world:
      'a 1950s SPORTS POSTER PRINT: bold flat colour blocks in VERMILION RED, ' +
      'INK BLUE, MUSTARD GOLD and cream newsprint, printed with coarse visible ' +
      'HALFTONE DOTS and slightly MISREGISTERED colour plates that shift a hair ' +
      'off the linework. Heavy confident black outlines. Crowds are rendered as ' +
      'fields of simplified dot-textured heads. Visible newsprint paper grain and ' +
      'a little ink spread. Flat matte, NO photographic texture, NO digital ' +
      'gradients, NO glossy modern sheen.',
  },
}

const probes = (W) => ({
  k1_scene:
    `A wide arena scene: on the left a TINY small figure standing alone, on the ` +
    `right an ENORMOUS towering giant twice his height, and behind them a crowd of ` +
    `DOZENS of spectators all leaning and reaching toward the TINY figure, their ` +
    `backs turned to the giant. ${W.hero} is the tiny figure.`,
  k2_character:
    `${W.hero}, standing alone in the centre of an empty arena floor, one arm ` +
    `raised in a small hopeful salute, looking up. Nothing else in the frame.`,
  k3_closeup:
    `CLOSE-UP filling the frame on the head and shoulders of the ENORMOUS giant: a ` +
    `powerful champion with a heavy jaw, caught in a moment of complete isolation, ` +
    `mouth flat, eyes tired, no triumph in him at all. Nothing else.`,
  k4_reversal:
    `The SAME small figure now grown ENORMOUS and towering, standing victorious ` +
    `with arms raised, while the crowd of DOZENS below has turned away from him ` +
    `with folded arms and sour faces, several pointing at a new TINY challenger at ` +
    `the frame's edge.`,
  k5_environment:
    `A packed arena: DOZENS of spectators in steep tiers all around, every face ` +
    `turned toward the centre where ${W.hero} stands ABSURDLY small on the sand ` +
    `beside an ENORMOUS fallen giant. Busy and crowded but one clear focal point.`,
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
