#!/usr/bin/env node
// Assemble a film composition from conformed beats and tinted frames.
//
// Emits a single index.html with one <img> clip per frame plus the narration
// track. The last film used one sub-composition per narration line, which is
// worth the indirection when a line has typography and staging in it; here
// every beat is a still with motion, so a sub-composition per frame would be
// 116 files that each hold one image tag.
//
// MOTION IS THE EXCEPTION, NOT THE DEFAULT. The first cut moved all 108 clips
// and Isaac's note was that the pans and zooms need still frames between them.
// He is right, and constant motion is self-defeating: if everything drifts,
// nothing reads as drifting, and the frames that should LAND have no stillness
// to land into.
//
// So a frame holds still unless it earns a move, and it earns one only by being
// long. A 6-second hold on a dead still image goes slack; a 2-second cut does
// not need help. Two movers never sit back to back, and the landing frames -
// the numbers, the coat, the closing image - are always still no matter how
// long they run.
//
// The zoom range is deliberately small. Sources were downscaled to exactly
// 1920x1080 at generation time and the originals were not kept, so ANY zoom in
// is upsampling. 4.5% is the ceiling: invisible at delivery resolution and
// after platform compression. If a future film wants real Ken Burns range,
// keep the 2752px originals.
//
// Usage: node tools/video/build-composition.mjs <film-dir>
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const FILM = join(REPO, process.argv[2] || '')
if (!process.argv[2]) { console.error('usage: build-composition.mjs <film-dir>'); process.exit(1) }

const ZOOM = 0.032          // max scale excursion; see note above
const DRIFT = 0.6           // max percent translate
const MOVE_MIN = 3.4        // only holds at least this long earn a move
// Frames that carry a claim. These land, so they are never in motion.
const ALWAYS_STILL = new Set([
  '030a', '030b', '030c',   // the five bars - the film's central evidence
  '031b',                   // the ordinary desk, on "the thing you do for a living"
  '047c', '048a',           // the stranger, and the finger pointed at them
  '053b',                   // the coat with the clinical lining
  '067a',                   // the small engine doing honest work
  '070a', '071a',           // the last two images
])
const MIN_HOLD = 1.15       // no frame shorter than this; below it reads as a flash

const conf = JSON.parse(readFileSync(join(FILM, 'production', 'beats-conformed.json'), 'utf8'))
const meta = JSON.parse(readFileSync(join(FILM, 'production', 'prompts-meta.json'), 'utf8'))
const man = JSON.parse(readFileSync(join(FILM, 'audio', 'manifest.json'), 'utf8'))

// Frame ids only line up with beat ids by luck. On a board whose frames are
// numbered sequentially (001a..133a) against 72 beats, matching on the id
// prefix SILENTLY DROPPED 62 frames - the render succeeded and half the film
// was missing. Every project writes production/frame-beats.json mapping frame
// id -> beat id + letter; the prefix match is only a fallback for old projects.
const mapPath = join(FILM, 'production', 'frame-beats.json')
const frameBeats = existsSync(mapPath)
  ? JSON.parse(readFileSync(mapPath, 'utf8'))
  : null
const framesFor = id => frameBeats
  ? Object.keys(frameBeats).filter(f => frameBeats[f].slice(0, 3) === id)
      .sort((a, b) => frameBeats[a].localeCompare(frameBeats[b]))
  : meta.filter(m => m.id.slice(0, 3) === id).map(m => m.id).sort()

// Expand beats into frames. Where a beat is too short to carry all its boarded
// frames at MIN_HOLD, drop the tail rather than flash them - the board sized
// frames against an ESTIMATE and the recording came in shorter in places.
const clips = []
let dropped = 0
for (const b of conf.beats) {
  let ids = framesFor(b.id)
  if (!ids.length) continue
  const maxFrames = Math.max(1, Math.floor(b.duration / MIN_HOLD))
  if (ids.length > maxFrames) { dropped += ids.length - maxFrames; ids = ids.slice(0, maxFrames) }
  const each = b.duration / ids.length
  ids.forEach((id, i) => {
    clips.push({ id, act: b.act, line: b.line,
                 start: b.start + i * each, duration: each })
  })
}

// A beat can be shorter than MIN_HOLD on its own ("Said kindly." runs 1.0s),
// and no per-beat frame count fixes that. Merge any clip still under the floor
// into its predecessor: the previous image simply holds across the short line.
// Those lines are deliberate rhythm beats and read better on a held frame than
// on an image that flashes and is gone.
let merged = 0
for (let i = clips.length - 1; i > 0; i--) {
  if (clips[i].duration < MIN_HOLD) {
    clips[i - 1].duration += clips[i].duration
    clips.splice(i, 1)
    merged++
  }
}

// Rounding start and duration independently to 3dp leaves 1ms gaps and 1ms
// overlaps, and the linter rejects overlapping clips on one track. Quantise the
// starts first, then derive each duration from the NEXT rounded start so the
// clips tile exactly.
const q = v => Math.round(v * 1000) / 1000
clips.forEach(c => { c.start = q(c.start) })
clips.forEach((c, i) => {
  c.duration = i < clips.length - 1 ? q(clips[i + 1].start - c.start)
                                    : q(conf.runtime - c.start)
})

const missing = clips.filter(c => !existsSync(join(FILM, 'public', 'images', 'tinted', `${c.id}-final.png`)))
if (missing.length) { console.error('missing tinted frames:', missing.map(c => c.id)); process.exit(1) }

const runtime = Math.max(conf.runtime, man.duration)
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;')

const els = clips.map((c, i) => {
  const w = Math.round(1920 * (1 + ZOOM)), h = Math.round(1080 * (1 + ZOOM))
  return `      <img id="f${i}" class="clip frame" src="public/images/tinted/${c.id}-final.png"\n` +
         `           style="width:${w}px;height:${h}px;margin-left:${-w / 2}px;margin-top:${-h / 2}px"\n` +
         `           data-start="${c.start.toFixed(3)}" data-duration="${c.duration.toFixed(3)}"\n` +
         `           data-track-index="1" alt="${esc(c.line.slice(0, 80))}" />`
}).join('\n')

// One tween per frame. Even frames settle outward (scale down toward 1:1),
// odd frames press inward - so the cut between them is a change of direction.
let lastMoved = false
clips.forEach((c, i) => {
  c.moves = c.duration >= MOVE_MIN && !ALWAYS_STILL.has(c.id) && !lastMoved
  lastMoved = c.moves
})

const tweens = clips.map((c, i) => {
  const lo = 1 / (1 + ZOOM), hi = 1
  if (!c.moves) {
    // Held frames still need a scale set, or they would render at the oversized
    // natural width. One static tween, no movement.
    return `  tl.set("#f${i}", { scale: ${lo.toFixed(4)}, xPercent: 0, yPercent: 0 });`
  }
  const inward = i % 2 === 1
  const from = inward ? lo : hi, to = inward ? hi : lo
  const dx = ((i * 37) % 7 - 3) / 3 * DRIFT      // deterministic spread, no RNG
  const dy = ((i * 23) % 5 - 2) / 2 * DRIFT
  return `  tl.fromTo("#f${i}", { scale: ${from.toFixed(4)}, xPercent: ${(-dx).toFixed(2)}, yPercent: ${(-dy).toFixed(2)} },\n` +
         `    { scale: ${to.toFixed(4)}, xPercent: ${dx.toFixed(2)}, yPercent: ${dy.toFixed(2)}, duration: ${c.duration.toFixed(3)}, ease: "none" }, ${c.start.toFixed(3)});`
}).join('\n')

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>You Happen to Life</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      html, body { width:100%; height:100%; margin:0; overflow:hidden; background:#F4E8C8; }
      #film-root { position:relative; width:1920px; height:1080px; overflow:hidden; background:#F4E8C8; }
      /* Frames are oversized and centred by negative margin, then scaled by
         GSAP. Centring via transform would be overwritten by the scale tween. */
      .frame { position:absolute; left:50%; top:50%; will-change:transform; }
    </style>
  </head>
  <body>
    <div id="film-root" data-composition-id="you-happen-to-life" data-start="0"
         data-width="1920" data-height="1080" data-duration="${runtime.toFixed(3)}">
${els}
      <audio id="narration" src="audio/narration.mp3" data-start="0"
             data-duration="${man.duration.toFixed(3)}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
${tweens}
      window.__timelines["you-happen-to-life"] = tl;
    </script>
  </body>
</html>
`

writeFileSync(join(FILM, 'index.html'), html)
writeFileSync(join(FILM, 'meta.json'), JSON.stringify({ id: 'you-happen-to-life', name: 'You Happen to Life' }) + '\n')
writeFileSync(join(FILM, 'package.json'), JSON.stringify({
  name: 'you-happen-to-life', private: true, type: 'module',
  scripts: { dev: 'npx --yes hyperframes@0.7.83 preview',
             check: 'npx --yes hyperframes@0.7.83 check',
             render: 'npx --yes hyperframes@0.7.83 render' },
}, null, 2) + '\n')

const m = Math.floor(runtime / 60)
console.log(`${clips.length} clips · ${m}:${(runtime - m * 60).toFixed(1).padStart(4, '0')}`)
console.log(`mean hold ${(clips.reduce((s, c) => s + c.duration, 0) / clips.length).toFixed(2)}s · ` +
            `shortest ${Math.min(...clips.map(c => c.duration)).toFixed(2)}s`)
const movers = clips.filter(c => c.moves).length
console.log(`${movers} clips move, ${clips.length - movers} hold still (${Math.round(100*movers/clips.length)}% in motion)`)
if (merged) console.log(`${merged} clips merged into their predecessor: shorter than the ${MIN_HOLD}s floor`)
if (dropped) console.log(`${dropped} boarded frames dropped: their beat was too short to hold them above ${MIN_HOLD}s`)
