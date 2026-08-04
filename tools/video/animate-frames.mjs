#!/usr/bin/env node
// Animate selected film frames with LTX-2-fast, on model.
//
// Closes the last finding from the School of Life shorts study: their frames
// MOVE, ours were stills with an assembly-level zoom.
//
// ---------------------------------------------------------------- THE RULES
// All four were established by measurement on 2026-07-31, not by taste.
//
// 1. NEVER ASK LTX FOR A CAMERA MOVE. Asked for a "very slow" dolly down an
//    archive, it travelled several metres: by 2s it was inside the drawers and
//    by 4s it had invented a symmetrical corridor that was not the source
//    scene, with the character and furniture gone. "Slowly" is not a
//    constraint it honours. Camera moves belong in the composition, where
//    build-composition.mjs already does them deterministically.
//    So every prompt here LOCKS the camera, in five explicit negatives.
//
// 2. SEND FULL-RESOLUTION PNG, NOT A DOWNSCALED JPEG. On flat line art the
//    edges ARE the image. A 1280px q88 jpeg seeded visible floor debris and
//    scratch artefacts from 4s onward; the same prompt on the full PNG came
//    back clean for the whole clip.
//
// 3. NAME THE CLEAN SURFACES. There is no negative_prompt field on this model,
//    so "the floor is clean and empty, no marks, no debris" has to go in the
//    positive prompt. It works.
//
// 4. NEVER ANIMATE A FRAME THAT CARRIES DATA. The five-bar chart - the film's
//    central evidence, a collapse from 26% to under 1% - came back after 6s as
//    roughly eight bars of near-equal height. The model treats a chart as
//    decorative shapes and rearranges them. Animating it would have shipped a
//    picture that CONTRADICTS the narration.
//    Charts, tables, diagrams and anything whose geometry IS the argument stay
//    still. This is not a quality setting; it is a correctness rule.
//
// 5. SUBJECT MOTION ONLY, AND IT IS A TREADMILL. A figure asked to walk across
//    frame walks IN PLACE while the background shifts. Do not fight it - board
//    for motion in place, or translate the finished clip in assembly.
//
// Measured v1 (jpeg + "slowly") vs v2 (full png + locked):
//    frame-to-frame delta   1.50 -> 1.29 /255
//    spurious change        1.25% -> 0.94% of pixels
//    RMSE drift over 6s     0.145 -> 0.155 (drifting) vs 0.145 -> 0.144 (holds)
//
// PROVIDER: fal, kling-video v2.5-turbo pro image-to-video, $0.07/s.
//
// Moved off WaveSpeed's LTX-2-fast (2026-08-05) for two reasons. One is
// housekeeping: one provider, one balance, one ledger. The other is craft -
// the playbook records kling as the workhorse that HOLDS STRUCTURE, and these
// clips are a tread lowering into a gap, one red dot being placed, and two
// hairs lifting. LTX is the model that redrew a five-bar chart into different
// data. $0.03/s more is the cheapest insurance on the board.
//
// Kling takes camera prompts well. We still never ask for one - see rule 1.
// Duration is a free integer up to 10s, not LTX's enum, so a 5s beat costs 5s.
//
// Usage:
//   node tools/video/animate-frames.mjs <film-dir> --spec motion.json [--publish]
//
// motion.json: { "030a": "the five bars settle very slightly", ... }
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i > -1 && argv[i + 1] ? argv[i + 1] : d }
const has = n => argv.includes(`--${n}`)

const FILM = join(REPO, argv[0] || '')
const spec = arg('spec')
const seconds = Number(arg('seconds', 6))
const fps = Number(arg('fps', 30))
if (!argv[0] || !spec) { console.error('need <film-dir> --spec motion.json'); process.exit(1) }
if (!(Number.isInteger(seconds) && seconds >= 1 && seconds <= 10)) {
  console.error('seconds must be a whole number 1-10 (kling max is 10)'); process.exit(1)
}

// The camera lock and the clean-surface clause are not per-shot decisions.
// They are the two things that make output usable, so they are appended to
// every prompt rather than left to whoever writes the spec.
const LOCK =
  'The camera is completely locked off and does not move at all: no dolly, no push, ' +
  'no zoom, no pan, no tilt; the framing is identical in every frame. ' +
  'All surfaces stay clean and empty with no marks, no debris, no scratches, no specks. ' +
  'Flat illustrated line art; the drawing style, line weight and colours stay exactly ' +
  'as in the source image and never change.'

const motions = JSON.parse(readFileSync(join(FILM, spec), 'utf8'))
const ids = Object.keys(motions)
const cost = ids.length * USD_PER_SECOND * seconds
console.log(`${ids.length} frames x ${seconds}s = $${cost.toFixed(2)}`)
for (const id of ids) console.log(`  ${id}  ${motions[id].slice(0, 68)}`)
if (!has('publish')) { console.log('\ndry run. add --publish to spend.'); process.exit(0) }

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .filter(l => l.startsWith('FAL_KEY='))
  .pop()?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not in .env'); process.exit(1) }

const ENDPOINT = 'fal-ai/kling-video/v2.6/pro/image-to-video'
const USD_PER_SECOND = 0.07
const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const OUT = join(FILM, 'public', 'clips'); mkdirSync(OUT, { recursive: true })
const sleep = ms => new Promise(r => setTimeout(r, ms))

async function animate(id) {
  const dest = join(OUT, `${id}.mp4`)
  if (existsSync(dest)) return 'skip'
  // Rule 2: the full-resolution PNG, untouched. No resize, no jpeg.
  const src = join(FILM, 'public', 'images', 'tinted', `${id}-final.png`)
  if (!existsSync(src)) return 'no-frame'
  const image = 'data:image/png;base64,' + readFileSync(src).toString('base64')

  const sub = await fetch(`https://queue.fal.run/${ENDPOINT}`, {
    method: 'POST', headers: H,
    body: JSON.stringify({ image_url: image, prompt: `${motions[id]} ${LOCK}`,
                           duration: String(seconds),
                           // Sound owns every sound in a GALLEY film, and
                           // native audio also doubles the per-second rate.
                           generate_audio: false }),
  })
  const txt = await sub.text()
  if (!sub.ok) throw new Error(`${sub.status}: ${txt.slice(0, 180)}`)
  const { status_url, response_url } = JSON.parse(txt)

  for (let i = 0; i < 90; i++) {
    await sleep(6000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.video?.url ?? out?.videos?.[0]?.url
      if (!url) throw new Error(`${id}: completed but no video url`)
      const raw = join(OUT, `.${id}-src.mp4`)
      writeFileSync(raw, Buffer.from(await (await fetch(url)).arrayBuffer()))
      // Conform 25 -> the film's rate. Without this the cut judders against
      // the stills around it.
      execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', raw,
        '-vf', `fps=${fps}`, '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
        '-pix_fmt', 'yuv420p', '-an', dest])
      execFileSync('rm', ['-f', raw])

      // CONTENT-DRIFT GATE. Frame-to-frame delta measures MELTING, not meaning:
      // the bar-chart clip that destroyed its own data scored BETTER on it
      // (1.18/255, 0.80% spurious) than the clip that was fine (1.29, 0.94%).
      // What catches content drift is RMSE against the SOURCE over time - the
      // chart held at 0.125 for four seconds and then jumped to 0.182.
      const rmse = t => {
        const f = join(OUT, `.probe-${id}.png`)
        execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(t), '-i', dest,
          '-vframes', '1', f])
        const r = execFileSync('sh', ['-c',
          `magick compare -metric RMSE '${src}' '${f}' null: 2>&1 || true`]).toString()
        execFileSync('rm', ['-f', f])
        return Number(r.match(/\(([\d.]+)\)/)?.[1] ?? 0)
      }
      // LIMITATION, found immediately after building this: the gate measures
      // change from SOURCE, and legitimate large subject motion also changes
      // the frame. A figure walking away down a corridor scored +0.036 and was
      // flagged, but the clip was fine - the "drift" WAS the intended motion.
      // So this is a FLAG, not a verdict. It is reliable for the case it was
      // built for (a frame that should barely move, quietly reorganising
      // itself) and it will false-positive on any shot where the subject
      // deliberately traverses depth or crosses frame. Always look at a flag
      // before acting on it.
      const a = rmse(0.2), b = rmse(seconds - 0.3)
      const drift = b - a
      if (drift > 0.02) {
        return `FLAG drift ${a.toFixed(3)}->${b.toFixed(3)} (+${drift.toFixed(3)}) ` +
               `- LOOK at it: content corruption, or just large intended motion?`
      }
      return `ok  drift ${(drift >= 0 ? '+' : '')}${drift.toFixed(3)}`
    }
    if (['FAILED', 'ERROR'].includes(st.status)) throw new Error(JSON.stringify(st).slice(0, 180))
  }
  throw new Error('timed out')
}

let spent = 0
for (const id of ids) {
  try {
    const r = await animate(id)
    if (!['skip', 'no-frame'].includes(r)) spent += USD_PER_SECOND * seconds
    console.log(`  ${id}  ${r}`)
  } catch (e) { console.log(`  FAIL     ${id}: ${e.message}`) }
}
console.log(`\nspent ~$${spent.toFixed(2)} -> ${OUT}`)
