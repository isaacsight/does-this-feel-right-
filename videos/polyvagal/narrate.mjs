/**
 * Record the narration for "The Third Thing".
 *
 *   export $(ps eww $(pgrep -f local-video-server.mjs | head -1) | tr ' ' '\n' | grep ^ELEVENLABS_API_KEY=)
 *   node videos/polyvagal/narrate.mjs
 *
 * The VO is PARSED OUT OF SCRIPT.md rather than copied here. On the last film
 * the script lived in two places and drifted; captions are built from the same
 * file, so parsing it once means the audio and the caption text cannot disagree.
 *
 * Calls ElevenLabs directly, not the engine proxy: the proxy's /v1/audio/speech
 * route forwards only stability / similarity_boost / style, and `speed` is the
 * setting that actually fixes pace. ElevenLabs bills subscription credits, so
 * there is no fal spend either way.
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const DIR = fileURLToPath(new URL('.', import.meta.url))
const VOICE = 'iP95p4xoKVk53GoZ742B'   // Chris — charming, casual, conversational
const MODEL = 'eleven_multilingual_v2'

/**
 * Every voice on the account reads 166–186 wpm by default, well above the
 * 135–145 a captioned film needs. 0.75 puts Chris at ~148. NOT linear across
 * voices — re-measure if the voice ever changes.
 */
const SPEED = 0.75

/** Pull the locked VO out of the script. Act headers become longer pauses. */
function loadVO() {
  const raw = readFileSync(join(DIR, 'SCRIPT.md'), 'utf8')
  const block = raw.split('## VO — locked')[1].split('\n**')[0]

  const paras = []
  let cur = []
  let actBreakPending = false

  for (const line of block.split('\n')) {
    const t = line.trim()
    if (!t.startsWith('>')) continue
    const body = t.replace(/^>+/, '').trim()

    if (!body) {                      // blank quoted line ends a paragraph
      if (cur.length) { paras.push({ text: cur.join(' '), act: actBreakPending }); cur = []; actBreakPending = false }
      continue
    }
    if (/^\*\*[IVX]+ —/.test(body)) { // act header — not spoken, but it is a beat
      if (cur.length) { paras.push({ text: cur.join(' '), act: false }); cur = [] }
      actBreakPending = true
      continue
    }
    cur.push(body)
  }
  if (cur.length) paras.push({ text: cur.join(' '), act: actBreakPending })

  // A pause between thoughts does as much for perceived pace as wpm does.
  return paras
    .map(p => `${p.text} <break time="${p.act ? '1.1s' : '0.7s'}" />`)
    .join('\n\n')
}

const VO = loadVO()
const words = VO.replace(/<break[^>]*>/g, ' ').trim().split(/\s+/).length
const breaks = (VO.match(/<break/g) || []).length

const KEY = process.env.ELEVENLABS_API_KEY
if (!KEY) {
  console.error('ELEVENLABS_API_KEY not set. It lives only in the running video-server process:')
  console.error('  export $(ps eww $(pgrep -f local-video-server.mjs | head -1) | tr " " "\\n" | grep ^ELEVENLABS_API_KEY=)')
  process.exit(1)
}

console.log(`${words} words · ${breaks} pauses · speed ${SPEED}`)

const res = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${VOICE}?output_format=mp3_44100_128`,
  {
    method: 'POST',
    headers: { 'xi-api-key': KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: VO,
      model_id: MODEL,
      voice_settings: { stability: 0.45, similarity_boost: 0.75, style: 0, speed: SPEED },
    }),
  },
)
if (!res.ok) throw new Error(`elevenlabs ${res.status}: ${(await res.text()).slice(0, 300)}`)

mkdirSync(join(DIR, 'voice'), { recursive: true })
const out = join(DIR, 'voice', 'vo.mp3')
writeFileSync(out, Buffer.from(await res.arrayBuffer()))
console.log(out)
console.log('ALWAYS verify it is not silent — the first shorts shipped at -91dB:')
console.log(`  ffmpeg -i "${out}" -af volumedetect -f null /dev/null 2>&1 | grep mean_volume`)
