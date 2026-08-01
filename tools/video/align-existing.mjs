#!/usr/bin/env node
// Retrofit exact word timings onto narration that was already recorded.
//
// narrate.mjs gets word timings for free by recording through
// /with-timestamps. Films recorded BEFORE that existed have none, so their
// captions come from the estimate chain - which measured +0.41s mean drift and
// 62% of cards more than half a second out (PLAYBOOK 10.21).
//
// ElevenLabs' /v1/forced-alignment takes the audio you already have plus the
// text you know was said, and returns character-level timings for it. No
// re-record, so the published audio is untouched and the captions still match
// the film that shipped.
//
// Writes the same audio/words.json that narrate.mjs produces, so everything
// downstream - segments-from-words.py, karaoke captions - works identically.
//
// Usage: node tools/video/align-existing.mjs <film-dir> [--publish]
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const FILM = join(REPO, argv[0] || '')
if (!argv[0]) { console.error('usage: align-existing.mjs <film-dir> [--publish]'); process.exit(1) }

const man = JSON.parse(readFileSync(join(FILM, 'audio', 'manifest.json'), 'utf8'))
const gap = man.actGapSeconds ?? 1.2

console.log(`${man.lines.length} acts · ${man.duration.toFixed(1)}s of recorded narration`)
for (const m of man.lines) console.log(`  ${m.act.padEnd(26)} ${m.duration.toFixed(1)}s`)
if (!argv.includes('--publish')) { console.log('\ndry run. add --publish to call the API.'); process.exit(0) }

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .filter(l => l.startsWith('ELEVENLABS_API_KEY='))
  .pop()?.slice('ELEVENLABS_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('ELEVENLABS_API_KEY not in .env'); process.exit(1) }

const timeline = []
let cursor = 0

for (const m of man.lines) {
  const mp3 = join(FILM, m.path)
  const txt = mp3.replace(/\.mp3$/, '.txt')
  if (!existsSync(mp3) || !existsSync(txt)) { console.error(`missing ${m.act}`); process.exit(1) }

  // curl rather than fetch: multipart with a file part is fiddly to build by
  // hand and this only runs once per film.
  const out = `/tmp/.fa-${m.act}.json`
  execFileSync('curl', ['-s', '-m', '600', '-X', 'POST',
    'https://api.elevenlabs.io/v1/forced-alignment',
    '-H', `xi-api-key: ${KEY}`,
    '-F', `file=@${mp3}`,
    '-F', `text=${readFileSync(txt, 'utf8').trim()}`,
    '-o', out])
  const al = JSON.parse(readFileSync(out, 'utf8'))
  if (!al.characters) { console.error(`${m.act}: ${JSON.stringify(al).slice(0, 200)}`); process.exit(1) }

  // Fold characters into words: whitespace closes a word, anything else
  // extends it. Same rule as narrate.mjs so the two paths agree exactly.
  let cur = null, n = 0
  for (const c of al.characters) {
    if (/\s/.test(c.text)) { if (cur) { timeline.push(cur); cur = null; n++ } continue }
    if (!cur) cur = { w: '', start: +(c.start + cursor).toFixed(3), end: 0 }
    cur.w += c.text; cur.end = +(c.end + cursor).toFixed(3)
  }
  if (cur) { timeline.push(cur); n++ }
  console.log(`  ok ${m.act.padEnd(26)} ${n} words`)
  cursor += m.duration + gap
}

writeFileSync(join(FILM, 'audio', 'words.json'),
  JSON.stringify({ count: timeline.length, words: timeline,
                   source: 'forced-alignment on the shipped audio' }, null, 1))
console.log(`\n${timeline.length} word timings -> audio/words.json`)
console.log(`span ${timeline[0].start}s -> ${timeline[timeline.length - 1].end}s`)
