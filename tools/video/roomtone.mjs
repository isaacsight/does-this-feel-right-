#!/usr/bin/env node
// Generate a room tone bed and mix it under a finished film.
//
// WHY NOT A VIDEO-TO-AUDIO MODEL. wavespeed-ai/mmaudio-v2 costs $0.001/s and
// looks perfect for this. It returned near-silence on our film: 28 of 29
// seconds at -57 dBFS with one blip. It is a video-TO-audio model - it infers
// sound from visible physical events, and our films are flat illustration with
// near-static frames, so it has nothing to key off. It is built for footage of
// things happening. Measured 2026-07-31, cost $0.03 to find out.
//
// WHY SONILO AND NOT MIRELO. Bakeoff at 30s on identical prompts:
//   sonilo/v1/text-to-sfx        RMS -53, peak -39, per-second spread  3 dB
//   mirelo-ai/sfx-1.6 (ambience) RMS -25, peak  -4, per-second spread 13 dB
// Mirelo has real EVENTS in it, which pull attention off the narration. A bed
// has to be boring. Sonilo is steady and 5x cheaper ($0.002/s vs $0.01/s).
// Its very low output level is not a defect - a bed gets normalised into place.
//
// The model caps at 180s, so longer films loop the tone with a crossfade at the
// seam rather than paying for one continuous pass.
//
// Usage:
//   node tools/video/roomtone.mjs --film <in.mp4> --out <out.mp4> [--publish]
//   node tools/video/roomtone.mjs --film ... --duck -20   # dB under programme
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs'
import { execFileSync, spawnSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i > -1 && argv[i + 1] ? argv[i + 1] : d }
const has = n => argv.includes(`--${n}`)

const film = arg('film'), out = arg('out')
const duck = Number(arg('duck', -20))          // bed level relative to programme
const chunk = 180                              // sonilo's ceiling
const PROMPT = arg('prompt',
  // NEVER ask for a HUM. This prompt previously said "soft low air handling
  // hum" and the model delivered exactly that: a harmonic series at 120/240/
  // 360/600 Hz with a third of its energy below 200 Hz. Under narration it
  // hid; in the act gaps it added 48 dB of low end and was plainly audible as
  // mains hum on a published film. Ask for AIR, not for a tone.
  'the faint airy hiss of a very quiet empty room at night, soft broadband air, ' +
  'no tone, no hum, no drone, no buzz, no motor, no music, no voices, no footsteps, ' +
  'featureless and completely steady')
if (!film || !out) { console.error('need --film and --out'); process.exit(1) }

const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'default=nw=1:nk=1', film]).toString().trim())
const cost = 0.002 * chunk
console.log(`film ${dur.toFixed(1)}s · one ${chunk}s tone at $${cost.toFixed(2)}, looped`)
if (!has('publish')) { console.log('\ndry run. add --publish to spend.'); process.exit(0) }

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .filter(l => l.startsWith('WAVESPEED_API_KEY='))
  .pop()?.slice('WAVESPEED_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('WAVESPEED_API_KEY not in .env'); process.exit(1) }

const H = { 'content-type': 'application/json', authorization: `Bearer ${KEY}` }
const tmp = join(REPO, 'output', 'roomtone'); mkdirSync(tmp, { recursive: true })
const tone = join(tmp, 'tone.wav')

if (!existsSync(tone)) {
  const sub = await fetch('https://api.wavespeed.ai/api/v3/sonilo/v1/text-to-sfx', {
    method: 'POST', headers: H,
    body: JSON.stringify({ prompt: PROMPT, duration: chunk, audio_format: 'wav' }),
  })
  const txt = await sub.text()
  if (!sub.ok) { console.error(`submit ${sub.status}: ${txt.slice(0, 300)}`); process.exit(1) }
  const poll = JSON.parse(txt).data.urls.get
  process.stdout.write('generating')
  for (let i = 0; i < 120; i++) {
    await new Promise(r => setTimeout(r, 5000)); process.stdout.write('.')
    const st = await (await fetch(poll, { headers: H })).json()
    if (st.data.status === 'completed') {
      writeFileSync(tone, Buffer.from(await (await fetch(st.data.outputs[0])).arrayBuffer()))
      console.log(' done'); break
    }
    if (st.data.status === 'failed') { console.error('\nFAILED', JSON.stringify(st).slice(0, 200)); process.exit(1) }
  }
}

// Loop to length. aloop on a decoded stream is exact and avoids the seam
// artefacts a concat demuxer leaves between identical mp3/wav chunks.
const bed = join(tmp, 'bed.wav')
execFileSync('ffmpeg', ['-v', 'error', '-y', '-stream_loop', '-1', '-i', tone,
  // Belt and braces: strip everything below 180 Hz regardless of what came
  // back. A room bed has no business carrying low end - that band belongs to
  // the voice, and anything left in it reads as hum.
  '-t', String(dur), '-af', 'highpass=f=180,highpass=f=180,afade=t=in:st=0:d=3',
  '-ac', '2', '-ar', '48000', bed])

// The bed is normalised to a fixed target and then ducked, rather than mixed by
// raw gain: the model's output level varies between generations, so a fixed
// gain would put the bed somewhere different every time.
execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', film, '-i', bed,
  '-filter_complex',
  `[1:a]loudnorm=I=${duck}:TP=-3:LRA=7,afade=t=out:st=${(dur - 4).toFixed(2)}:d=4[bed];` +
  `[0:a][bed]amix=inputs=2:duration=first:weights=1 1:normalize=0[a]`,
  '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
  '-movflags', '+faststart', out])

// ffmpeg writes ebur128 to STDERR, not stdout, so the summary has to be read
// from there - execFileSync's return value is stdout and would be empty.
const li = s => {
  const r = spawnSync('ffmpeg', ['-i', s, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
    { encoding: 'utf8' })
  // ebur128 prints a RUNNING I: on every frame, starting at -70 before it has
  // enough audio to measure. Taking the first match reports -70 for every file.
  // The summary is the last one.
  const all = [...(r.stderr || '').matchAll(/I:\s+(-?[\d.]+)/g)]
  return all.length ? all[all.length - 1][1] : '?'
}
console.log(`\nbed at ${duck} LUFS under a programme of ${li(film)} LUFS`)
console.log(`out ${out} · ${li(out)} LUFS`)
