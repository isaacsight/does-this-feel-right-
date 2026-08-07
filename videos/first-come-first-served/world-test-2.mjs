#!/usr/bin/env node
// World test ROUND 2 — THE SECOND MEDIUM. An original direction, not a
// reference pulled off a shelf.
//
// WHY. Round 1 tested three borrowed directions (Krisel symmetry, Blair era
// keying, Vignelli route line) and all three came back handsome and slightly
// inert. The reason is that every one of them draws only the EXTERIOR, and this
// episode has no exterior. A man is third in a queue, loses forty seconds, and
// nothing whatsoever happens. What happens is inside him: his temperature
// changes, he can hear his own heartbeat, his body reacted before his brain.
//
// THE RULE: two media in one frame. The world stays calm and flat and painted -
// the queue, the shop, the other people, all composed and fine. His INTERIOR
// arrives as a second material breaking into the same picture: raw scratched
// ink and smeared charcoal with real pressure behind it, sitting ON TOP of the
// painted world, touching nothing. Nobody in the frame ever reacts to it. The
// narration never mentions it.
//
// It has an ARC, and the arc is the episode:
//   k1  a hairline of scratched black at the edge of his silhouette
//   k2  it cracks outward across the flat background at the moment of intrusion
//   k3  it consumes a third of the frame while nine people stand calmly inside it
//   k4  it collapses to a single dot as he tuts - that was the whole discharge
//   k5  gone. A calm painted world with nothing in it at all.
//
// THE RISK THIS PROBE EXISTS TO SETTLE: generative models BLEND two media
// rather than keeping them separate. If these come back as muddy texture over
// the whole frame instead of a clean collision between painted world and raw
// mark, the direction fails and we say so.
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
  'the recurring character in mid-century cartoon style: a small slight man with a ' +
  'round young face and a big confident nose, EXACTLY TWO hairs standing from the ' +
  'crown that KINK and LEAN at different angles and are different lengths, a flat ' +
  'VERMILION RED coat, thin stick legs and ABSURDLY oversized shoes, drawn with a ' +
  'strong readable silhouette and a confident tapering ink outline'

// The world half. Deliberately CALM — the composure is what makes the second
// medium legible as an intrusion rather than as style.
const WORLD =
  'THE WORLD IS PAINTED: a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American ' +
  'limited-animation idiom of the late 1950s, flat gouache-painted backgrounds and ' +
  'flat painted cel figures with confident tapering ink outlines and no interior ' +
  'shading, in a warm graphic palette of INK BLUE, mustard GOLD, sage GREEN, dusty ' +
  'ORANGE, cream and flat VERMILION RED. Everyone in the scene is calm, composed and ' +
  'perfectly ordinary. Visible gouache texture, flat matte, NO gradients, NO ' +
  'airbrushed shading, NO photographic texture, NO three-dimensional rendering.'

// The interior half. A DIFFERENT material, not a style variation.
const MARK =
  'AND SEPARATELY, drawn in a COMPLETELY DIFFERENT MATERIAL sitting ON TOP of the ' +
  'painted image: raw hand-scratched BLACK INK and smeared CHARCOAL marks with ' +
  'visible pressure, torn scribbled strokes, dry-brush drag and scratched hatching - ' +
  'crude, urgent and hand-made, obviously a different substance from the smooth ' +
  'painted world beneath it. The two materials NEVER blend and never share a texture: ' +
  'the painted world stays perfectly clean and flat everywhere the raw marks are not, ' +
  'with a hard visible boundary between them. NOBODY in the scene reacts to the marks ' +
  'or looks at them.'

const COMMON =
  'There is NO text, NO lettering, NO numbers and NO writing of any kind anywhere in ' +
  'the image; any sign or board is completely BLANK. This is an ORIGINAL character in ' +
  'a general mid-century cartoon idiom: NO existing cartoon characters, NO studio ' +
  'logos, NO trade dress. ONE SINGLE COHERENT SCENE, NOT a grid, NOT a sheet of ' +
  'studies. 16:9, edge to edge, one scene, one camera.'

const TESTS = {
  k1_hairline:
    `${HERO} standing third in a calm orderly queue of ordinary people in a shop ` +
    `interior, everything composed and pleasant, and a single THIN HAIRLINE of raw ` +
    `scratched black ink running along the outer edge of his silhouette and nowhere ` +
    `else in the frame. Almost unnoticeable. ${WORLD} ${MARK}`,
  k2_crack:
    `${HERO} standing third in the same calm queue as a stranger steps into the line ` +
    `ahead of him, and at that exact moment a jagged CRACK of raw scratched black ink ` +
    `bursts outward from him across the flat painted background wall behind, like a ` +
    `windscreen fracture. The other people in the queue stand calmly and do not look ` +
    `at it. ${WORLD} ${MARK}`,
  k3_fury:
    `${HERO} standing perfectly still and expressionless in a queue while a DENSE ` +
    `STORM of raw scratched charcoal and torn ink scribble fills roughly a third of ` +
    `the frame around him, violent and hand-made, and NINE ordinary people stand ` +
    `calmly inside and around the storm, entirely unbothered, none of them looking at ` +
    `it. ${WORLD} ${MARK}`,
  k4_collapse:
    `CLOSE on ${HERO} making one small disapproving noise with his tongue, lips ` +
    `pursed and eyes flat, and the only raw mark left anywhere in the frame is a ` +
    `SINGLE SMALL BLACK DOT of scratched ink beside his mouth. Everything else is ` +
    `calm flat paint. ${WORLD} ${MARK}`,
  k5_clean:
    `${HERO} standing third in a calm orderly queue of ordinary people, everything ` +
    `flat and painted and composed, absolutely no scratched or charcoal marks ` +
    `anywhere in the frame at all, the whole picture clean and quiet. ${WORLD}`,
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(TESTS)
console.log(`${ids.length} images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const id of ids) {
  process.stdout.write(`  ${id} ... `)
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: `${TESTS[id]} ${COMMON}`, num_images: 1,
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
        writeFileSync(join(OUT, `mark-${id}.png`),
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
