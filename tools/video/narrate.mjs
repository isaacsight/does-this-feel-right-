#!/usr/bin/env node
// Record film narration on ElevenLabs, one act per request.
//
// Direct against api.elevenlabs.io rather than through tools/local-video-server.mjs
// because that proxy builds voice_settings from stability/similarity/style only
// and never forwards `speed`. Every voice otherwise runs 166-186 wpm, which is
// the defect that made the last two films feel rushed; the shipped setting is
// 0.9 and it has to actually reach the API.
//
// ONE REQUEST PER ACT, not per sentence. Two reasons:
//   - within an act the model places its own pauses and keeps one breath line,
//     which no amount of concatenating sentence clips reproduces;
//   - across acts, previous_text / next_text plus previous_request_ids let the
//     model carry prosody over the seam, so act 4 does not open in a different
//     mood from the one act 3 closed in.
//
// Input is production/narration.txt (already ASCII-sanitised). Do NOT feed
// script.txt: an em dash pasted into TTS came back as mojibake and cost a
// re-record on the last film.
//
// WORD TIMINGS. This calls /with-timestamps, which returns character-level
// alignment alongside the audio, and folds it into per-word timings written to
// audio/words.json. That is what drives karaoke-style captions - the highlight
// has to land within ~80ms of the voice, and no approximation gets there.
// Do NOT try to derive word times by splitting a line's duration across
// characters: that is fine for FRAME timing (conform-beats.py) where a few
// hundred ms is invisible, and useless for a caption highlight.
//
// Usage: node tools/video/narrate.mjs <film-dir> [--publish] [--only 3]
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d }
const FILM = join(REPO, argv[0] || '')
if (!argv[0]) { console.error('usage: narrate.mjs <film-dir> [--publish]'); process.exit(1) }

// Settings carried verbatim from You Are Not Finished's audio/manifest.json,
// which is the validated house voice. Do not drift these casually.
const VOICE = 'iP95p4xoKVk53GoZ742B'          // "Chris"
const MODEL = 'eleven_multilingual_v2'
// speed IS honoured by eleven_multilingual_v2 on the direct API - measured
// 2026-07-31 on identical text: 0.7 -> 21.1s, 0.9 -> 15.3s, 1.0 -> 12.5s. The
// "narration has to go through the browser" constraint was only ever about the
// local proxy dropping the field.
// 0.9 gives ~175 wpm over a whole film, which matches the pace Isaac approved
// on You Are Not Finished. 0.85 measured 148 wpm / 7:38 - too slow and over
// the runtime target.
// DO NOT set this from one act's rate. Act 3 alone reads 188 wpm at speed 0.9
// because it is short punchy sentences; the film average is 175. Measure pace
// across all acts or not at all.
const SETTINGS = { stability: 0.5, similarity_boost: 0.75, style: 0.0, use_speaker_boost: true, speed: 0.95 }
const ACT_GAP = 1.2                            // seconds of room tone between acts
const TARGET_LUFS = -18

// Act structure is FILM-SPECIFIC. An earlier version hardcoded one film's
// paragraph ranges here; run against a different script it gave two acts a
// single word each. Every film writes production/act-paras.json alongside its
// script, and this reads it. The fallback below only exists so an old project
// without that file still runs.
const ACTS = existsSync(join(FILM, 'production', 'act-paras.json'))
  ? JSON.parse(readFileSync(join(FILM, 'production', 'act-paras.json'), 'utf8'))
  : [
      { n: 1, slug: 'act-1', paras: [0, 4] },
      { n: 2, slug: 'act-2', paras: [5, 10] },
      { n: 3, slug: 'act-3', paras: [11, 13] },
      { n: 4, slug: 'act-4', paras: [14, 19] },
      { n: 5, slug: 'act-5', paras: [20, 24] },
      { n: 6, slug: 'act-6', paras: [25, 30] },
      { n: 7, slug: 'act-7', paras: [31, 35] },
    ]

const beats = JSON.parse(readFileSync(join(FILM, 'production', 'beats.json'), 'utf8')).beats
const drops = new Set(JSON.parse(readFileSync(join(FILM, 'production', 'drops.json'), 'utf8')))
const kept = beats.filter(b => !drops.has(b.id))

const ascii = t => t.replace(/[—]/g, ' - ').replace(/[–]/g, '-')
  .replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
  .replace(/…/g, '...').replace(/ /g, ' ')
  .normalize('NFKD').replace(/[^\x00-\x7E]/g, '')

const actText = a => {
  const lines = kept.filter(b => b.paragraph >= a.paras[0] && b.paragraph <= a.paras[1])
  // Paragraph breaks are real breaths; keep them as blank lines so the model
  // pauses where the writer did.
  let out = '', prev = null
  for (const b of lines) {
    if (prev !== null && b.paragraph !== prev) out += '\n\n'
    else if (prev !== null) out += ' '
    out += ascii(b.line); prev = b.paragraph
  }
  return out.trim()
}

const parts = ACTS.map(a => ({ ...a, text: actText(a) }))
const chars = parts.reduce((n, p) => n + p.text.length, 0)
const words = parts.reduce((n, p) => n + p.text.split(/\s+/).length, 0)
console.log(`${parts.length} acts · ${words} words · ${chars} characters`)
for (const p of parts) console.log(`  act ${p.n} ${p.slug.padEnd(22)} ${String(p.text.split(/\s+/).length).padStart(4)} words`)

const nonAscii = parts.flatMap(p => [...p.text].filter(c => c.charCodeAt(0) > 126))
if (nonAscii.length) { console.error('NON-ASCII in TTS input:', nonAscii); process.exit(1) }

if (!argv.includes('--publish')) {
  console.log('\ndry run. add --publish to spend ElevenLabs credits.')
  process.exit(0)
}

const KEY = readFileSync(join(REPO, '.env'), 'utf8').split('\n')
  .filter(l => l.startsWith('ELEVENLABS_API_KEY='))
  .pop()?.slice('ELEVENLABS_API_KEY='.length).trim().replace(/^["']|["']$/g, '')
if (!KEY) { console.error('ELEVENLABS_API_KEY not in .env'); process.exit(1) }

const OUT = join(FILM, 'audio', 'parts')
mkdirSync(OUT, { recursive: true })

const only = arg('only', null)
const prevIds = []
const manifest = []
const actWords = []

for (let i = 0; i < parts.length; i++) {
  const p = parts[i]
  const stem = `${String(p.n).padStart(2, '0')}-${p.slug}`
  const mp3 = join(OUT, `${stem}.mp3`)
  writeFileSync(join(OUT, `${stem}.txt`), p.text + '\n')
  if (only && String(p.n) !== only) continue
  if (existsSync(mp3)) { console.log(`  skip  act ${p.n}`); continue }

  const body = {
    text: p.text,
    model_id: MODEL,
    voice_settings: SETTINGS,
    // Context the model reads but does not speak - it only shapes delivery
    // at the seams.
    previous_text: i > 0 ? parts[i - 1].text.slice(-400) : undefined,
    next_text: i < parts.length - 1 ? parts[i + 1].text.slice(0, 400) : undefined,
    previous_request_ids: prevIds.slice(-3),
  }
  const resp = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${VOICE}/with-timestamps?output_format=mp3_44100_128`,
    { method: 'POST', headers: { 'xi-api-key': KEY, 'content-type': 'application/json' },
      body: JSON.stringify(body) })
  if (!resp.ok) {
    console.error(`act ${p.n} FAILED ${resp.status}: ${(await resp.text()).slice(0, 300)}`)
    process.exit(1)
  }
  const rid = resp.headers.get('request-id')
  if (rid) prevIds.push(rid)

  // /with-timestamps returns JSON, not audio bytes.
  const payload = await resp.json()
  writeFileSync(mp3, Buffer.from(payload.audio_base64, 'base64'))

  // Fold character alignment into words. A character that is whitespace closes
  // the current word; everything else extends it.
  const al = payload.alignment ?? payload.normalized_alignment ?? {}
  const words = []
  let cur = null
  const chars = al.characters ?? []
  const cs = al.character_start_times_seconds ?? []
  const ce = al.character_end_times_seconds ?? []
  for (let k = 0; k < chars.length; k++) {
    if (/\s/.test(chars[k])) { if (cur) { words.push(cur); cur = null } continue }
    if (!cur) cur = { w: '', start: cs[k], end: ce[k] }
    cur.w += chars[k]; cur.end = ce[k]
  }
  if (cur) words.push(cur)
  actWords.push({ act: stem, words })
  const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
    '-of', 'default=nw=1:nk=1', mp3]).toString().trim())
  manifest.push({ act: stem, path: `audio/parts/${stem}.mp3`, duration: dur,
                  words: p.text.split(/\s+/).length, wpm: p.text.split(/\s+/).length / dur * 60 })
  console.log(`  ok    act ${p.n} ${stem.padEnd(24)} ${dur.toFixed(1)}s  ${(manifest.at(-1).wpm).toFixed(0)} wpm`)
}

if (only) process.exit(0)

// Stitch with a measured gap between acts, then normalise once over the whole
// thing - normalising parts separately would make each act a different loudness.
const listFile = join(FILM, 'audio', '.concat.txt')
const silence = join(FILM, 'audio', '.gap.mp3')
execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'lavfi', '-i',
  `anullsrc=r=44100:cl=mono:d=${ACT_GAP}`, '-c:a', 'libmp3lame', '-b:a', '128k', silence])
const seq = []
manifest.forEach((m, i) => { seq.push(join(FILM, m.path)); if (i < manifest.length - 1) seq.push(silence) })
writeFileSync(listFile, seq.map(f => `file '${f}'`).join('\n') + '\n')

const raw = join(FILM, 'audio', '.narration-raw.mp3')
// Re-encode rather than -c copy: copying mp3 frames carries each part's
// encoder delay into the stream and ffmpeg reports non-monotonic dts.
execFileSync('ffmpeg', ['-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', listFile,
  '-ar', '44100', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '192k', raw])
const final = join(FILM, 'audio', 'narration.mp3')
execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', raw,
  '-af', `loudnorm=I=${TARGET_LUFS}:TP=-1.5:LRA=11`, '-c:a', 'libmp3lame', '-b:a', '192k', final])

const total = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration',
  '-of', 'default=nw=1:nk=1', final]).toString().trim())
// Word timings, offset into the FINAL mix. Each act starts after the sum of
// the acts before it plus one ACT_GAP each, which is exactly how the concat
// above lays them out.
let cursor = 0
const timeline = []
for (const m of manifest) {
  const src = actWords.find(a => a.act === m.act)
  for (const w of src?.words ?? []) {
    timeline.push({ w: w.w, start: +(w.start + cursor).toFixed(3), end: +(w.end + cursor).toFixed(3) })
  }
  cursor += m.duration + ACT_GAP
}
writeFileSync(join(FILM, 'audio', 'words.json'),
  JSON.stringify({ count: timeline.length, words: timeline }, null, 1))
console.log(`\n${timeline.length} word timings -> audio/words.json`)

writeFileSync(join(FILM, 'audio', 'manifest.json'), JSON.stringify({
  voice: 'Chris', voiceId: VOICE, modelId: MODEL, ...SETTINGS,
  outputFormat: 'mp3_44100_128', actGapSeconds: ACT_GAP, targetLufs: TARGET_LUFS,
  duration: total, words, overallWpm: words / total * 60,
  recordedVia: 'direct ElevenLabs API (tools/video/narrate.mjs) - the local proxy does not forward speed',
  lines: manifest,
}, null, 1))

const m = Math.floor(total / 60)
console.log(`\nnarration.mp3  ${m}:${(total - m * 60).toFixed(1).padStart(4, '0')}  ${(words / total * 60).toFixed(1)} wpm`)
