#!/usr/bin/env node
// Concept art — The Million-Dollar Pigeon. SIX probes, $0.23.
//
// Not a world bake-off. The series world is already locked by two shipped
// episodes (mid-century painted cel), and four episodes in four worlds is an
// anthology while a recurring world is a show. What these probes settle is
// whether THIS SUBJECT can be staged in it — because the episode's whole
// comedy engine is a two-sided frame: a human side that means everything and a
// bird side that means nothing, in the same picture.
//
// So each probe is a scene from CAST.md that has to work, and each one asks a
// different question:
//   p1 auction     can a frame hold a sweating man and an indifferent bird,
//                  and read as absurd without mocking anybody?
//   p2 widowhood   the emotional engine. Two birds, no humans. If this is not
//                  tender the whole third act collapses.
//   p3 liberation  the episode's widest image — a thousand birds off one lorry.
//                  Can the idiom do SCALE?
//   p4 horse lab   the best sourced gag in the film. Needs the horse trophies
//                  to dwarf the tiny jar, or the joke does not exist.
//   p5 cher ami    played straight, no comedy staging. Can the world do
//                  GRAVITY? Three episodes of jokes have not tested this.
//   p6 fancier     the Goode/McBride portrait — a man and his obsession, the
//                  frame that decides whether the audience loves him.
//
// Lessons from the queue episode, all applied below:
//   - the camera is a CROP, not a noun ("CLOSE on" is advisory and gets ignored)
//   - countable things get COUNTS ("a line of SIX", not "a queue")
//   - every frame with a person NAMES A FACE ACTION
//   - absences are described as present things; nothing is negated
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

const HERO = 'THE FANCIER: a small slight man with a round face and a big confident nose, ' +
  'EXACTLY TWO hairs and no more than two sticking up from his crown, kinked and leaning at ' +
  'different angles, a flat VERMILION RED coat, thin stick legs and ABSURDLY oversized shoes'

const KIM = 'THE HEN: a plump grey racing pigeon with a tiny head, a bright orange eye and ' +
  'ONE white splash on her left wing, drawn with a strong readable silhouette'

const CAM = {
  CU:    'CLOSE-UP: the subject FILLS THE FRAME, cropped at the chest, only a suggestion of ' +
         'background behind.',
  MED:   'MEDIUM SHOT, the figures cut off at the knees and filling most of the frame height.',
  WIDE:  'WIDE SHOT: the full figures stand well inside the frame with the setting around them.',
  XWIDE: 'VERY WIDE SHOT: the figures are SMALL in a large landscape that fills the frame.',
}

const WORLD =
  'a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom of the ' +
  'late 1950s: flat gouache-painted backgrounds and flat painted cel figures with confident ' +
  'tapering ink outlines and no interior shading, in a warm graphic palette of INK BLUE, ' +
  'mustard GOLD, sage GREEN, dusty ORANGE, cream and flat VERMILION RED, each scene keying ' +
  'its own dominant colour from that set. Expressions are BOLD, exaggerated and readable at ' +
  'a glance, in the tradition of classic theatrical cartoon animation. Visible gouache ' +
  'texture, flat matte, NO gradients, NO airbrushed shading, NO photographic texture, NO ' +
  'three-dimensional rendering. There is NO text, NO lettering, NO numbers and NO writing of ' +
  'any kind anywhere in the image; any sign, board, placard or banner is completely BLANK. ' +
  'ONLY the people and animals described above appear in this image. Any crowd is ' +
  'individuated: different faces, different builds, clothes in DIFFERENT colours from the ' +
  'palette, never a row of matching coats. These are ORIGINAL characters in a general ' +
  'mid-century cartoon idiom: NO existing cartoon characters, NO studio logos, NO trade ' +
  'dress, and no likeness of any real person. ONE SINGLE COHERENT SCENE, NOT a grid of ' +
  'panels, NOT a sheet of studies. 16:9, edge to edge, one scene, one camera.'

const P = {
  p1_auction: [CAM.MED,
    `An auctioneer in a sharp suit hammering a gavel with his eyes bulging, his mouth open ` +
    `mid-shout and sweat flying off his forehead, one arm flung upward — while on a bare ` +
    `velvet cushion beside him, with nothing under it and nothing beside it, ${KIM} calmly ` +
    `preens one wing and pays no attention whatsoever. TWO bidding paddles are raised out ` +
    `of the dark at the bottom of the frame, one vast and gold, one small and black, both ` +
    `completely smooth and bare.`],

  p2_widowhood: [CAM.CU,
    `Inside a wooden loft, TWO pigeons on one perch: ${KIM}, and beside her a scruffier cock ` +
    `with his feathers ruffled on one side, the two of them leaning very slightly together ` +
    `and doing nothing at all. Warm mustard GOLD light through the slats. It is quiet and it ` +
    `is tender.`],

  p3_liberation: [CAM.XWIDE,
    `Dawn over a VAST empty field: one lorry with all its side hatches dropped open, and ` +
    `HUNDREDS of pigeons BLASTING out of it in a torrent that climbs steeply across the ` +
    `frame and off the top edge, wings beating hard, birds overlapping and crowding each ` +
    `other, the nearest ones LARGE and the furthest ones tiny specks. TWO tiny men stand ` +
    `beside the lorry with their hats blown out of their hands, heads tipped all the way ` +
    `back, mouths open.`],

  p4_horse_lab: [CAM.MED,
    `A laboratory hung with ENORMOUS oil paintings of racehorses and crowded with COLOSSAL ` +
    `gold horse-racing trophies — and in the middle of it a small official in a white coat ` +
    `holding up a TINY specimen jar in a pair of tweezers, squinting at it with one eye shut ` +
    `and his eyebrows climbing, his mouth pursed in complete disbelief at how small it is.`],

  p5_cher_ami: [CAM.CU,
    `A young soldier's mud-caked hands cupped around one small grey pigeon like a match held ` +
    `out of the wind, his face above just visible, jaw set, eyes exhausted and steady. Behind ` +
    `him a shattered forest and drifting smoke, keyed to cold INK BLUE and cream. Nothing in ` +
    `this picture is funny.`],

  p6_fancier: [CAM.WIDE,
    `${HERO} alone on a brick rooftop at dusk beside a wooden pigeon loft, standing on an ` +
    `upturned crate with a stopwatch held up at arm's length and his head tipped right back, ` +
    `his mouth open and his eyebrows raised in hope, staring at an ENORMOUS empty sky that ` +
    `fills two thirds of the frame. A thermos and an enamel mug sit cooling on the parapet ` +
    `beside him. Washing lines and chimney pots run away behind.`],
}

mkdirSync(OUT, { recursive: true })
const only = process.argv.filter(a => a.startsWith('p'))
const ids = only.length ? only : Object.keys(P)
console.log(`${ids.length} images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const id of ids) {
  process.stdout.write(`  ${id} ... `)
  const [cam, scene] = P[id]
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: `${cam} ${scene} ${WORLD}`, num_images: 1,
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
        writeFileSync(join(OUT, `${id}.png`),
          Buffer.from(await (await fetch(url)).arrayBuffer()))
        console.log('ok')
      } else console.log('no image url')
      done = true
    } else if (st.status === 'FAILED' || st.status === 'ERROR') { console.log('FAILED'); done = true }
  }
  if (!done) console.log('timed out')
}
console.log(`\n${OUT}`)
