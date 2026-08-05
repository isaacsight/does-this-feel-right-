#!/usr/bin/env node
// Assemble the film: 88 stills against the narration, cut on sentence boundaries.
//
// Cut points come from audio/words.json, never from an estimated beat map — five
// of six shorts once opened mid-word because the starts were syllable-spread
// guesses. A word ending in . ! or ? ends a sentence; each frame holds from its
// first sentence's first word to its last sentence's last word.
//
// The script has 94 sentences and the board has 88 frames, so six frames carry two
// sentences. Allocation is proportional to word count rather than sentence count,
// so a frame over two short sentences does not outstay one over a long one.
//
// No motion clips: the five LIVE beats are an enhancement and the film reads as a
// stills film. Each frame gets a slow deterministic push (DRIFT) so the picture is
// never completely static under a talking voice.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const FILM = dirname(fileURLToPath(import.meta.url))
const FRAMES = join(FILM, 'public', 'images', 'frames')
const AUDIO = join(FILM, 'audio', 'narration.mp3')
const BUILD = join(FILM, 'build')
mkdirSync(BUILD, { recursive: true })

const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'default=nw=1:nk=1', AUDIO]).toString().trim())

// map-shots.py anchors every frame to ITS OWN narration line, read out of the
// storyboard. Always prefer it: the fallback below spreads frames evenly across
// sentences, which is what made the first cut's images land near their line
// instead of on it. Regenerate with `python3 map-shots.py` after a board change.
const MAPPED = join(BUILD, 'shots.json')
if (existsSync(MAPPED)) {
  const shots = JSON.parse(readFileSync(MAPPED, 'utf8'))
  render(shots)
} else {
  console.error('build/shots.json missing — run: python3 map-shots.py')
  process.exit(1)
}

function render(shots) {
for (const s of shots) {
  if (!existsSync(join(FRAMES, `${s.id}-final.png`))) {
    console.error(`missing ${s.id}`); process.exit(1)
  }
}
// Close every gap: each shot runs until the next one starts, and the last runs to
// the end of the audio, so no black frame can appear between images.
for (let i = 0; i < shots.length - 1; i++) shots[i].end = shots[i + 1].start
shots[shots.length - 1].end = dur
for (const s of shots) s.dur = Math.max(0.7, s.end - s.start)

console.log(`${shots.length} shots over ${dur.toFixed(1)}s | ` +
  `mean ${(dur / shots.length).toFixed(2)}s | ` +
  `min ${Math.min(...shots.map(s => s.dur)).toFixed(2)}s | ` +
  `max ${Math.max(...shots.map(s => s.dur)).toFixed(2)}s`)
writeFileSync(join(BUILD, 'shots.json'), JSON.stringify(shots, null, 1))

// --- render ----------------------------------------------------------------
// One filter per still: scale up slightly and push, so the frame breathes. The
// push alternates direction by index so the film does not feel like one long
// zoom in the same direction.
const FPS = 30
const inputs = []
const filters = []
shots.forEach((s, i) => {
  // A SINGLE input frame, with no -loop/-t. zoompan's `d` is output frames per
  // INPUT frame, so looping the still first makes it emit d frames for every one
  // of the dur*fps inputs — `on` then runs far past n and the zoom grows without
  // bound, which is what rendered the back half of the film as blank paper.
  inputs.push('-i', join(FRAMES, `${s.id}-final.png`))
  const n = Math.max(2, Math.round(s.dur * FPS))
  const dir = i % 2 === 0 ? 1 : -1
  // zoompan CROPS from its input and cannot zoom out, so its output size `s` must
  // equal the input size for z=1 to show the whole picture. Setting s smaller than
  // the input crops instead of fitting — that is what produced a first render at a
  // quarter of the frame and a second at blank paper. So: push at 2880 with a
  // matching s, then scale down to the film canvas.
  const z = dir > 0 ? `1.00+0.05*on/${n}` : `1.05-0.05*on/${n}`
  filters.push(
    `[${i}:v]scale=2880:1620,zoompan=z='${z}':d=${n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'` +
    `:s=2880x1620:fps=${FPS},scale=1920:1080,setsar=1[v${i}]`)
})
const concat = shots.map((_, i) => `[v${i}]`).join('') + `concat=n=${shots.length}:v=1:a=0[vout]`
const script = join(BUILD, 'filter.txt')
writeFileSync(script, filters.join(';') + ';' + concat)

const OUT = join(BUILD, 'cognitive-debt-master.mp4')
console.log('rendering...')
execFileSync('ffmpeg', ['-y', ...inputs, '-i', AUDIO,
  '-filter_complex_script', script,
  '-map', '[vout]', '-map', `${shots.length}:a`,
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
  '-c:a', 'aac', '-b:a', '192k', '-shortest', OUT], { stdio: 'inherit' })

const outDur = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'default=nw=1:nk=1', OUT]).toString().trim()
console.log(`\n${OUT}\n${Number(outDur).toFixed(1)}s`)
}
