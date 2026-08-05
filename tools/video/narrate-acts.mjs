#!/usr/bin/env node
// Narrate a film: one request per act, with word timestamps. SHARED tool.
//
// The older tools/video/narrate.mjs is wired to one film's paragraph map
// (beats.json + drops.json + hardcoded ACT paragraph ranges) and breaks on any
// film that lacks them. This one needs nothing but script.txt: a blank line is an
// act break, which is how the scripts are already written.
//
// Usage: node tools/video/narrate-acts.mjs videos/<slug> [--publish]
//
// with-timestamps rather than the plain endpoint because the cut is built from
// word timings, never from a beat map — five of six shorts once opened mid-word
// because the starts were syllable-spread estimates.
//
// previous_text / next_text carry prosody across the act seams so the voice does
// not reset its intonation at every paragraph break.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const argv = process.argv.slice(2)
const FILM = argv[0] && !argv[0].startsWith("--") ? join(dirname(fileURLToPath(import.meta.url)), "..", "..", argv[0]) : null
if (!FILM) { console.error("usage: narrate.mjs <film-dir> [--publish] [--voice <id>] [--speed <n>]"); process.exit(1) }
const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..")
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 && argv[i+1] && !argv[i+1].startsWith('--') ? argv[i+1] : d }
const VOICE = arg('voice', 'iP95p4xoKVk53GoZ742B')   // Chris - charming, down-to-earth
const MODEL = 'eleven_multilingual_v2'
// 0.95 is the house value for long-form with Chris, MEASURED. speed is badly
// non-linear across voices — re-measure if the voice changes, never assume.
const SPEED = Number(arg('speed', 0.95))
const OUT = join(FILM, 'audio')

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .find(l => l.startsWith('ELEVENLABS_API_KEY='))
  ?.slice('ELEVENLABS_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('no ELEVENLABS_API_KEY'); process.exit(1) }

const ascii = t => t.replace(/[—–]/g, ' - ').replace(/[‘’]/g, "'")
  .replace(/[“”]/g, '"').replace(/…/g, '...').replace(/ /g, ' ')
  .normalize('NFKD').replace(/[^\x00-\x7E]/g, '')

const acts = readFileSync(join(FILM, 'script.txt'), 'utf8')
  .split(/\n\s*\n/).map(s => ascii(s.trim())).filter(Boolean)

const chars = acts.reduce((n, a) => n + a.length, 0)
console.log(`${acts.length} acts, ${chars} chars (~${chars} credits)`)
if (!process.argv.includes('--publish')) { console.log('dry run. --publish to spend.'); process.exit(0) }

mkdirSync(OUT, { recursive: true })
mkdirSync(join(OUT, 'parts'), { recursive: true })

const words = []
const partFiles = []
let offset = 0
let prevIds = []

for (let i = 0; i < acts.length; i++) {
  process.stdout.write(`  act ${i + 1}/${acts.length} ... `)
  const res = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps`,
    { method: 'POST',
      headers: { 'xi-api-key': KEY, 'content-type': 'application/json' },
      body: JSON.stringify({
        text: acts[i],
        model_id: MODEL,
        voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: SPEED },
        previous_text: i > 0 ? acts[i - 1] : undefined,
        next_text: i < acts.length - 1 ? acts[i + 1] : undefined,
        previous_request_ids: prevIds.slice(-3),
      }) })
  if (!res.ok) { console.error(`\nHTTP ${res.status}: ${(await res.text()).slice(0, 300)}`); process.exit(1) }
  const rid = res.headers.get('request-id')
  if (rid) prevIds.push(rid)
  const j = await res.json()

  const mp3 = join(OUT, 'parts', `act-${i + 1}.mp3`)
  writeFileSync(mp3, Buffer.from(j.audio_base64, 'base64'))
  partFiles.push(mp3)

  // Rebuild words from the character alignment: a word runs from the start of its
  // first non-space character to the end of its last.
  const al = j.alignment || j.normalized_alignment
  let cur = null
  for (let c = 0; c < al.characters.length; c++) {
    const ch = al.characters[c]
    if (/\s/.test(ch)) { if (cur) { words.push(cur); cur = null } continue }
    if (!cur) cur = { word: '', start: offset + al.character_start_times_seconds[c], end: 0 }
    cur.word += ch
    cur.end = offset + al.character_end_times_seconds[c]
  }
  if (cur) words.push(cur)

  const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
    '-of', 'default=nw=1:nk=1', mp3]).toString().trim())
  offset += dur
  console.log(`${dur.toFixed(2)}s`)
}

// Concatenate. Re-encode rather than stream-copy: mp3 frame boundaries do not land
// on act seams and a copy-concat drifts against the timestamps we just computed.
const list = join(OUT, 'parts', 'list.txt')
writeFileSync(list, partFiles.map(f => `file '${f}'`).join('\n'))
const master = join(OUT, 'narration.mp3')
execFileSync('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', list,
  '-c:a', 'libmp3lame', '-b:a', '192k', master], { stdio: 'ignore' })

writeFileSync(join(OUT, 'words.json'), JSON.stringify(words, null, 1))
const total = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'default=nw=1:nk=1', master]).toString().trim())
console.log(`\nnarration.mp3  ${Math.floor(total / 60)}:${String(Math.round(total % 60)).padStart(2, '0')}`)
console.log(`words.json     ${words.length} words`)
console.log(`rate           ${(words.length / (total / 60)).toFixed(1)} wpm`)
