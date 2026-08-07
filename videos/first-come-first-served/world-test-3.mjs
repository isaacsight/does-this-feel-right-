#!/usr/bin/env node
// World test ROUND 3 — THE SPLIT CLAUSE. Proving the fix before rebuilding.
//
// WHAT WENT WRONG. Round 2's five probes passed, so the world was locked and
// 102 frames were generated. 85 passed every gate and the world had still
// failed: marks appeared on frames declared `none`, spread as background
// texture rather than emanating from him, and the intrusion arc died.
//
// THE CAUSE IS ARCHITECTURAL, NOT AESTHETIC. The second-medium description was
// put in the SHARED world clause appended to all 102 prompts, and then switched
// off per frame with "absolutely NO scratched marks anywhere". That cannot
// work: you cannot negate a concept you have just introduced in the same
// prompt. Every frame was told in detail how to draw scratched charcoal and
// then asked not to. The introduction wins.
//
// The round-2 probes did not catch it because each probe was written STANDALONE
// with the mark language only in the frames that wanted it. Five bespoke
// prompts do not test a shared clause. A probe must exercise the thing that
// will actually ship.
//
// THE FIX: two clauses, selected by the frame's declared intrusion level.
//   CLEAN  — no mention of marks, ink, charcoal or scratching ANYWHERE. Not
//            "no marks". No mention at all. Omission, not negation.
//   MARKED — the two-material clause, used only on hairline/crack/storm/dot.
//
// WHAT THIS PROBE HAS TO SETTLE, and it is one question:
//   does the CLEAN clause come back genuinely clean, on the kinds of frames
//   that failed last time — the empty room, the calm queue, the closing street?
// Three of the five probes are clean frames for exactly that reason. Two are
// marked frames, to confirm the split did not weaken the intrusion.
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

const LAWS =
  'There is NO text, NO lettering, NO numbers and NO writing of any kind anywhere in ' +
  'the image; any sign, board or banner is completely BLANK. This is an ORIGINAL ' +
  'character in a general mid-century cartoon idiom: NO existing cartoon characters, ' +
  'NO studio logos, NO trade dress. ONE SINGLE COHERENT SCENE, NOT a grid of panels, ' +
  'NOT a sheet of studies. 16:9, edge to edge, one scene, one camera.'

const PAINT =
  'a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom ' +
  'of the late 1950s: flat gouache-painted backgrounds and flat painted cel figures ' +
  'with confident tapering ink outlines and no interior shading, in a warm graphic ' +
  'palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, cream and flat ' +
  'VERMILION RED. Everyone is calm, composed and perfectly ordinary. Visible gouache ' +
  'texture, flat matte, NO gradients, NO airbrushed shading, NO photographic texture, ' +
  'NO three-dimensional rendering.'

// CLEAN. Note what is NOT here: no ink, no charcoal, no scratch, no "marks",
// not even a denial of them. The word never appears.
const CLEAN = `${PAINT} The whole picture is smooth, tidy and evenly painted throughout. ${LAWS}`

// MARKED. Only ever appended to frames that actually want an intrusion.
const MARKED = `${PAINT} ` +
  'AND SEPARATELY, drawn in a COMPLETELY DIFFERENT MATERIAL sitting ON TOP of the ' +
  'painted image: raw hand-scratched BLACK INK and smeared CHARCOAL with visible ' +
  'pressure, torn scribbled strokes and scratched hatching, crude and urgent and ' +
  'hand-made, obviously a different substance from the smooth painted world beneath. ' +
  'The raw marks emanate ONLY from the man in the red coat and touch nothing else: ' +
  'every OTHER person in the frame stays completely clean flat paint with no marks on ' +
  'or near them, and NOBODY reacts to the marks or looks at them. The two materials ' +
  'NEVER blend, with a hard visible boundary between them. ' + LAWS

const TESTS = {
  // The three that failed last time. If these come back clean, the fix works.
  c1_empty_room:
    { p: `An empty painted police station front desk with nobody behind it at all, the ` +
         `shutter down, a clock on the wall with a completely BLANK face.`, w: CLEAN },
  c2_calm_queue:
    { p: `${HERO} standing third in a calm orderly queue of six ordinary people inside a ` +
         `small shop, everything composed and pleasant, a shopkeeper working slowly.`, w: CLEAN },
  c3_closing_street:
    { p: `A VAST calm painted street with one long orderly queue running through it and ` +
         `${HERO} standing TINY and content somewhere in the middle of it.`, w: CLEAN },
  // The two that must still work.
  m1_crack:
    { p: `${HERO} standing third in a calm queue with a perfectly pleasant composed face ` +
         `as a pleasant oblivious man in a sage green raincoat steps in at the second ` +
         `position, and a jagged CRACK of raw scratched black ink bursts outward from ` +
         `the man in the red coat across the flat painted background like a windscreen ` +
         `fracture.`, w: MARKED },
  m2_dot:
    { p: `CLOSE on ${HERO} making one small disapproving noise with his tongue, lips ` +
         `pursed and eyes flat, and the ONLY raw mark anywhere in the entire frame is ` +
         `ONE SMALL BLACK DOT of scratched ink beside his mouth.`, w: MARKED },
}

mkdirSync(OUT, { recursive: true })
const ids = Object.keys(TESTS)
console.log(`${ids.length} images x $0.039 = $${(ids.length * 0.039).toFixed(2)}`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const sleep = ms => new Promise(r => setTimeout(r, ms))

for (const id of ids) {
  process.stdout.write(`  ${id} ... `)
  const { p, w } = TESTS[id]
  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: `${p} ${w}`, num_images: 1,
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
        writeFileSync(join(OUT, `split-${id}.png`),
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
