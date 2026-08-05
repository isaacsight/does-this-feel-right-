#!/usr/bin/env node
// Assemble a stills film: one clip per shot, then concatenate. SHARED tool.
//
// WHY THIS SHAPE — it crashed Isaac's machine on 2026-08-04.
//
// The previous assembler passed all 78 stills to ONE ffmpeg as 78 simultaneous
// `-i` inputs and built a single filter_complex that scaled every one of them to
// 2880x1620 for the push. ffmpeg allocates decode and filter buffers per input, so
// peak memory scaled with the number of frames in the film, not with the size of
// one frame. At 78 inputs it exhausted RAM and took the machine down mid-render.
//
// Here each shot is rendered by its own short-lived ffmpeg, sequentially, and the
// clips are joined with the concat demuxer using stream copy. Peak memory is one
// frame regardless of film length, and nothing is re-encoded at join time.
//
// The shape has a second benefit that matters more than it should: it RESUMES.
// A finished clip is left on disk, so a crash, a Ctrl-C or a full disk costs the
// current shot rather than the whole render.
//
// Usage:
//   node tools/video/assemble-stills.mjs videos/<slug> [--fps 30] [--fresh]
//
// Reads  <film>/build/shots.json   (map-shots.py — frames anchored to their lines)
//        <film>/audio/narration.mp3
// Writes <film>/build/clips/*.mp4  (intermediate, resumable)
//        <film>/build/<slug>-master.mp4
import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync, statSync } from 'node:fs'
import { join, dirname, basename } from 'node:path'
import { execFileSync, spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d }
if (!argv[0] || argv[0].startsWith('--')) {
  console.error('usage: assemble-stills.mjs <film-dir> [--fps 30] [--fresh]')
  process.exit(1)
}
const FILM = join(REPO, argv[0])
const SLUG = basename(FILM)
const FPS = Number(arg('fps', 30))
const FRESH = argv.includes('--fresh')
// Bounded on purpose. Unbounded parallelism here is the same mistake as the
// 78-input filter graph, one level up: peak memory would again scale with the
// film. Each job holds roughly one 1920x1080 push buffer.
const JOBS = Math.max(1, Math.min(4, Number(arg('jobs', 3))))
// HOUSE DEFAULT: no camera movement at all. Isaac's call, 2026-08-04 — the films
// are narration over stills, and a drifting frame is decoration the form does not
// want. `--move` opts back in to the board's per-shot moves. Rendering a true still
// also skips zoompan entirely, which is far cheaper than a 1.001 zoom.
const MOVE = argv.includes('--move')

const FRAMES = join(FILM, 'public', 'images', 'frames')
const AUDIO = join(FILM, 'audio', 'narration.mp3')
const BUILD = join(FILM, 'build')
const CLIPS = join(BUILD, 'clips')
const OUT = join(BUILD, `${SLUG}-master.mp4`)

for (const p of [AUDIO, join(BUILD, 'shots.json')]) {
  if (!existsSync(p)) { console.error(`missing ${p}`); process.exit(1) }
}
if (FRESH && existsSync(CLIPS)) rmSync(CLIPS, { recursive: true })
mkdirSync(CLIPS, { recursive: true })

const ffprobe = f => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries',
  'format=duration', '-of', 'default=nw=1:nk=1', f]).toString().trim())

const shots = JSON.parse(readFileSync(join(BUILD, 'shots.json'), 'utf8'))
const dur = ffprobe(AUDIO)
// Close every gap so no black frame can appear between images, and let the last
// shot run to the end of the narration.
for (let i = 0; i < shots.length - 1; i++) shots[i].end = shots[i + 1].start
shots[shots.length - 1].end = dur
for (const s of shots) s.dur = Math.max(0.7, s.end - s.start)

console.log(`${shots.length} shots over ${dur.toFixed(1)}s | mean ${(dur / shots.length).toFixed(2)}s | ` +
  `min ${Math.min(...shots.map(s => s.dur)).toFixed(2)}s | max ${Math.max(...shots.map(s => s.dur)).toFixed(2)}s`)

// zoompan CROPS from its input and cannot zoom out, so its output size must EQUAL
// the input size for z=1 to show the whole picture. And feed ONE input frame with
// no -loop/-t: `d` is output frames per INPUT frame, so looping first makes `on`
// run far past `n` and the zoom grows without bound.
//
// NO SUPERSAMPLE. An earlier version scaled each frame to 2880x1620 before the
// push. The source frames ARE 1920x1080, so there was no extra detail to sample —
// it paid 2.25x the pixels for nothing. Measured on a 5s clip: 6.9s with it, 3.1s
// without, indistinguishable at 100% on halftone. Encoder preset barely mattered
// (6.9 -> 6.6); the SCALE was the whole cost.
//
// PER-SHOT MOVES. The first two films used one push, alternating direction by
// index — motion by formula. The board now names a move per beat and this honours
// it. A pan or tilt needs headroom to travel into, so those hold a fixed zoom and
// travel across it; a push and a pull change zoom and stay centred.
const MOVES = {
  HOLD:  n => ({ z: '1.001', x: 'iw/2-(iw/zoom/2)',        y: 'ih/2-(ih/zoom/2)' }),
  PUSH:  n => ({ z: `1.00+0.06*on/${n}`, x: 'iw/2-(iw/zoom/2)', y: 'ih/2-(ih/zoom/2)' }),
  PULL:  n => ({ z: `1.06-0.06*on/${n}`, x: 'iw/2-(iw/zoom/2)', y: 'ih/2-(ih/zoom/2)' }),
  PANR:  n => ({ z: '1.08', x: `(iw-iw/zoom)*on/${n}`,     y: 'ih/2-(ih/zoom/2)' }),
  PANL:  n => ({ z: '1.08', x: `(iw-iw/zoom)*(1-on/${n})`, y: 'ih/2-(ih/zoom/2)' }),
  TILTD: n => ({ z: '1.08', x: 'iw/2-(iw/zoom/2)',         y: `(ih-ih/zoom)*on/${n}` }),
  TILTU: n => ({ z: '1.08', x: 'iw/2-(iw/zoom/2)',         y: `(ih-ih/zoom)*(1-on/${n})` }),
}

let built = 0, reused = 0
const queue = []
shots.forEach((s, i) => {
  const src = join(FRAMES, `${s.id}-final.png`)
  if (!existsSync(src)) { console.error(`missing frame ${s.id}`); process.exit(1) }
  const clip = join(CLIPS, `${String(i).padStart(4, '0')}.mp4`)

  // Resume: keep a clip only if it exists AND already has the duration we want.
  if (existsSync(clip) && statSync(clip).size > 1024) {
    try {
      if (Math.abs(ffprobe(clip) - s.dur) < 0.05) { reused++; return }
    } catch { /* unreadable, fall through and rebuild */ }
  }

  const n = Math.max(2, Math.round(s.dur * FPS))
  if (!MOVE) {
    // A true still. -loop/-t is safe HERE precisely because there is no zoompan:
    // the `d` trap only exists when zoompan multiplies its output per input frame.
    queue.push(['-y', '-loglevel', 'error', '-loop', '1', '-t', s.dur.toFixed(3),
      '-i', src, '-vf', `scale=1920:1080,fps=${FPS},setsar=1`,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
      '-pix_fmt', 'yuv420p', clip])
    return
  }
  const key = MOVES[s.move] ? s.move : (i % 2 === 0 ? 'PUSH' : 'PULL')
  const m = MOVES[key](n)
  queue.push(['-y', '-loglevel', 'error', '-i', src,
    '-filter_complex',
    `[0:v]zoompan=z='${m.z}':d=${n}:x='${m.x}':y='${m.y}'` +
    `:s=1920x1080:fps=${FPS},setsar=1[v]`,
    '-map', '[v]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-pix_fmt', 'yuv420p', clip])
})

if (MOVE) {
  const mc = shots.reduce((a, s) => (a[s.move || 'PUSH'] = (a[s.move || 'PUSH'] || 0) + 1, a), {})
  console.log('moves: ' + Object.entries(mc).sort().map(([k, v]) => `${k}=${v}`).join('  '))
} else console.log('STILLS — no camera movement (--move to enable the board\'s moves)')
console.log(`${reused} clips reused, ${queue.length} to build, ${JOBS} at a time`)
let cursor = 0
await Promise.all(Array.from({ length: Math.min(JOBS, queue.length) }, async () => {
  while (cursor < queue.length) {
    const a = queue[cursor++]
    await new Promise((res, rej) => {
      const c = spawn('ffmpeg', a, { stdio: 'inherit' })
      c.on('exit', code => code === 0 ? res() : rej(new Error(`ffmpeg exit ${code}`)))
    })
    built++
    if (built % 10 === 0 || built === queue.length) console.log(`  ${built}/${queue.length}`)
  }
}))

// Concat with stream copy — no second encode of the picture, and no filter graph
// holding every clip open at once.
const list = join(BUILD, 'clips.txt')
writeFileSync(list, shots.map((_, i) =>
  `file '${join(CLIPS, `${String(i).padStart(4, '0')}.mp4`)}'`).join('\n'))
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
  '-i', list, '-i', AUDIO, '-map', '0:v', '-map', '1:a',
  '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', OUT], { stdio: 'inherit' })

const d = ffprobe(OUT)
console.log(`\n${OUT}\n${Math.floor(d / 60)}:${String(Math.round(d % 60)).padStart(2, '0')}  ` +
  `${(statSync(OUT).size / 1048576).toFixed(0)}MB`)
