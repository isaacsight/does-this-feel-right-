#!/usr/bin/env node
// Animate a film's frames into clips via fal image-to-video — SHARED tool.
//
// TWO MODES:
//   --spec motion.json    the original mode: a flat {id: "what moves"} map,
//                         one model, one duration for every clip.
//   --board               the motion-film mode (grip-strength onward): reads
//                         production/board.json, which carries per-shot
//                         motion_class, motion_prompt, clip_seconds and an
//                         optional per-row model. Rows with motion_class
//                         "data" generate NO clip — the measured rule ("the
//                         model redraws data wrong") is enforced here as well
//                         as at the board, because a rule enforced in one
//                         place is a rule waiting to be bypassed.
//
// Model routing goes through tools/video-models.mjs (the verified registry)
// rather than a hardcoded endpoint — the registry knows prices, endpoints,
// duration formats and per-vendor input quirks (wan's negative_prompt and
// prompt-expansion-off live there, not here).
//
// THE MEASURED RULES (2026-07-31), all still enforced:
//   1. Never ask the model for a camera move. The LOCK names the camera as
//      locked; camera feel is assembly's job.
//   2. Send the FULL-RESOLUTION PNG. A downscaled jpeg seeded floor debris
//      from 4s onward on flat art.
//   3. Name the clean surfaces in the positive prompt (most models have no
//      negative prompt; wan does, and gets the prohibitions there too).
//   4. Data frames are never animated (board mode refuses them).
//   5. Subject motion is a treadmill — board for motion in place.
//
// DRIFT GATE: RMSE against the source at t=0.2s and t=end-0.3s. In board
// mode the verdict depends on the row's class: a BIG move legitimately
// changes the frame (the known false-positive), so flags on big:* rows are
// reported and WAIVED; an ambient row that drifts is a real failure and the
// clip is moved to public/clips/quarantine/ so a re-run regenerates it.
//
// Usage:
//   node tools/video/animate-frames.mjs <film-dir> --spec motion.json [--seconds 6] [--publish]
//   node tools/video/animate-frames.mjs <film-dir> --board [--model kling-pro]
//        [--only b13] [--fps 30] [--publish]
import { readFileSync, writeFileSync, existsSync, mkdirSync, renameSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { getModel, pickEndpoint, estimateUsd, buildInput } from '../video-models.mjs'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i > -1 && argv[i + 1] ? argv[i + 1] : d }
const has = n => argv.includes(`--${n}`)

const FILM = join(REPO, argv[0] || '')
const spec = arg('spec')
const boardMode = has('board')
const only = arg('only')
const fps = Number(arg('fps', 30))
const defaultModel = arg('model', 'kling-pro')
// Drift threshold is WORLD-DEPENDENT: 0.02 was measured on flat line art on
// cream; the grip film's dark glow-and-grain world breathes ~5x that
// innocently (eyeballed range: +0.03-0.09 all sound, real failures at +0.15
// and +0.44). Pass --drift per world; the default preserves old behaviour.
const DRIFT = Number(arg('drift', 0.02))
if (!argv[0] || (!spec && !boardMode)) {
  console.error('need <film-dir> and either --spec motion.json or --board'); process.exit(1)
}

// The camera lock and the clean-surface clause are not per-shot decisions.
// (The old opener named a specific idiom — "flat illustrated line art" — which
// was one film's style leaking into a shared tool. The style authority is now
// solely "as in the source image", which is what the clause always meant.)
const LOCK =
  'The camera is completely locked off and does not move at all: no dolly, no push, ' +
  'no zoom, no pan, no tilt; the framing is identical in every frame. ' +
  'All surfaces stay clean with no marks, no debris, no scratches, no specks. ' +
  'The drawing style, line weight and colours stay exactly as in the source image ' +
  'and never change. No text, lettering or numerals ever appear.'
// For the models that have a negative_prompt (wan): the same prohibitions,
// stated as the things to avoid.
const NEG = 'camera movement, dolly zoom pan tilt, text, lettering, numerals, watermark, ' +
  'debris, scratches, specks, style change, new objects appearing, extra elements'

// Build the work list: [{id, prompt, secs, model, big}]
let jobs = []
if (boardMode) {
  const rows = JSON.parse(readFileSync(join(FILM, 'production', 'board.json'), 'utf8'))
  jobs = rows
    .filter(r => r.motion_class !== 'data')
    .filter(r => !only || r.id === only)
    .map(r => ({ id: r.id, prompt: r.motion_prompt, secs: r.clip_seconds,
                 model: r.model ?? defaultModel, big: r.motion_class.startsWith('big:') }))
  for (const j of jobs) {
    if (!getModel(j.model)) { console.error(`${j.id}: unknown model ${j.model}`); process.exit(1) }
    if (getModel(j.model).retired) { console.error(`${j.id}: model ${j.model} is RETIRED`); process.exit(1) }
  }
} else {
  const seconds = Number(arg('seconds', 6))
  if (!(Number.isInteger(seconds) && seconds >= 1 && seconds <= 10)) {
    console.error('seconds must be a whole number 1-10'); process.exit(1)
  }
  const motions = JSON.parse(readFileSync(join(FILM, spec), 'utf8'))
  jobs = Object.entries(motions)
    .filter(([id]) => !only || id === only)
    .map(([id, prompt]) => ({ id, prompt, secs: seconds, model: defaultModel, big: false }))
}

const quote = jobs.reduce((s, j) => s + estimateUsd(j.model, j.secs), 0)
const byModel = {}
for (const j of jobs) byModel[j.model] = (byModel[j.model] ?? 0) + estimateUsd(j.model, j.secs)
console.log(`${jobs.length} clips = $${quote.toFixed(2)}  ` +
  Object.entries(byModel).map(([m, u]) => `${m}:$${u.toFixed(2)}`).join('  '))
for (const j of jobs) {
  console.log(`  ${j.id}  ${j.secs}s ${j.model}${j.big ? ' BIG' : ''}  ${j.prompt.slice(0, 56)}`)
}
if (!has('publish')) { console.log('\ndry run. add --publish to spend.'); process.exit(0) }

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .filter(l => l.startsWith('FAL_KEY='))
  .pop()?.slice('FAL_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('FAL_KEY not in .env'); process.exit(1) }

const H = { 'content-type': 'application/json', authorization: `Key ${KEY}` }
const OUT = join(FILM, 'public', 'clips'); mkdirSync(OUT, { recursive: true })
const QUAR = join(OUT, 'quarantine')
const sleep = ms => new Promise(r => setTimeout(r, ms))

function sourceFrame(id) {
  // The composition films keep composited frames in tinted/; the motion films
  // animate the gated frame directly.
  for (const dir of ['tinted', 'frames']) {
    const p = join(FILM, 'public', 'images', dir, `${id}-final.png`)
    if (existsSync(p)) return p
  }
  return null
}

async function animate(job) {
  const dest = join(OUT, `${job.id}.mp4`)
  if (existsSync(dest)) return 'skip'
  const src = sourceFrame(job.id)
  if (!src) return 'no-frame'
  // Rule 2: the full-resolution PNG, untouched. No resize, no jpeg.
  const image = 'data:image/png;base64,' + readFileSync(src).toString('base64')

  const model = getModel(job.model)
  const endpoint = pickEndpoint(job.model, true)
  const input = buildInput(job.model, `${job.prompt} ${LOCK}`, job.secs, image,
                           { negativePrompt: NEG })
  // Audio off is a hard rule; kling and veo take the flag, wan has no audio tier.
  if (/kling|veo/.test(job.model)) input.generate_audio = false

  const sub = await fetch(`https://queue.fal.run/${endpoint}`, {
    method: 'POST', headers: H, body: JSON.stringify(input),
  })
  const txt = await sub.text()
  if (!sub.ok) throw new Error(`${sub.status}: ${txt.slice(0, 180)}`)
  const { status_url, response_url } = JSON.parse(txt)

  for (let i = 0; i < 90; i++) {
    await sleep(6000)
    const st = await (await fetch(status_url, { headers: H })).json()
    if (st.status === 'COMPLETED') {
      const out = await (await fetch(response_url, { headers: H })).json()
      const url = out?.video?.url ?? out?.videos?.[0]?.url ?? out?.data?.video?.url
      // A completed job with no findable url is a SCHEMA problem, and the only
      // way to fix a schema problem is to see the schema.
      if (!url) throw new Error(`${job.id}: completed but no video url in: ` +
                                JSON.stringify(out).slice(0, 400))
      const raw = join(OUT, `.${job.id}-src.mp4`)
      writeFileSync(raw, Buffer.from(await (await fetch(url)).arrayBuffer()))
      // Conform to the film's rate or the cut judders.
      execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', raw,
        '-vf', `fps=${fps}`, '-c:v', 'libx264', '-crf', '17', '-preset', 'slow',
        '-pix_fmt', 'yuv420p', '-an', dest])
      execFileSync('rm', ['-f', raw])

      // CONTENT-DRIFT GATE: RMSE vs SOURCE at both ends of the clip.
      const rmse = t => {
        const f = join(OUT, `.probe-${job.id}.png`)
        execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(t), '-i', dest,
          '-vframes', '1', f])
        const r = execFileSync('sh', ['-c',
          `magick compare -metric RMSE '${src}' '${f}' null: 2>&1 || true`]).toString()
        execFileSync('rm', ['-f', f])
        return Number(r.match(/\(([\d.]+)\)/)?.[1] ?? 0)
      }
      const a = rmse(0.2), b = rmse(job.secs - 0.3)
      const drift = b - a
      if (drift > DRIFT) {
        if (job.big) {
          // The known false-positive: a BIG move legitimately changes the
          // frame. Reported, kept, waived — but still LOOK at it in QC.
          return `ok  drift +${drift.toFixed(3)} WAIVED (big move) - eyeball in QC`
        }
        // An ambient frame that drifted is a real failure: quarantine so a
        // re-run regenerates, keep the evidence for eyes.
        mkdirSync(QUAR, { recursive: true })
        renameSync(dest, join(QUAR, `${job.id}-drift${drift.toFixed(3)}.mp4`))
        return `DRIFT-FAIL +${drift.toFixed(3)} -> quarantined; re-run to retry`
      }
      return `ok  drift ${(drift >= 0 ? '+' : '')}${drift.toFixed(3)}`
    }
    if (['FAILED', 'ERROR'].includes(st.status)) throw new Error(JSON.stringify(st).slice(0, 180))
  }
  throw new Error('timed out')
}

// Generation is network-bound and the drift gate is per-clip, so clips run
// CONCURRENTLY (bounded). The serial design was inherited from the assembly
// memory lesson, which never applied here — a 33-clip batch was taking ~90
// minutes that four workers do in ~25.
const JOBS = Math.max(1, Math.min(4, Number(arg('jobs', 4))))
let spent = 0, cursor = 0
await Promise.all(Array.from({ length: Math.min(JOBS, jobs.length) }, async () => {
  while (cursor < jobs.length) {
    const job = jobs[cursor++]
    try {
      const r = await animate(job)
      if (!['skip', 'no-frame'].includes(r)) spent += estimateUsd(job.model, job.secs)
      console.log(`  ${job.id}  ${r}`)
    } catch (e) { console.log(`  FAIL     ${job.id}: ${e.message}`) }
  }
}))
console.log(`\nspent ~$${spent.toFixed(2)} -> ${OUT}`)
