/**
 * Record the narration for "The Last Thing That Happens".
 *
 *   node videos/peak-end-rule/narrate.mjs
 *
 * Sound records BEFORE picture is locked — the cut is built against the VO
 * transcript, not the other way round.
 *
 * This calls the ElevenLabs API directly rather than going through the engine
 * proxy. The proxy's /v1/audio/speech route forwards only stability,
 * similarity_boost and style, so `speed` — the one setting that actually fixed
 * this film — is unreachable through it. ElevenLabs bills subscription credits,
 * so there is no fal spend either way.
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const DIR = fileURLToPath(new URL('.', import.meta.url))

const VOICE = 'iP95p4xoKVk53GoZ742B'   // Chris — charming, casual, conversational
const MODEL = 'eleven_multilingual_v2'

/**
 * Pace. Every narrator on the account runs 166–186wpm at default settings,
 * well above the 135–145 conversational band a captioned short needs — the
 * viewer is reading, watching and listening at once.
 *
 * speed 0.75 puts Chris at ~148wpm. It is NOT linear across voices (Will barely
 * moved at 0.85), so re-measure whenever the voice changes.
 */
const SPEED = 0.75

/**
 * The locked script. Captions take THIS text, never the ASR's guess at it.
 * <break> tags carry the pauses between thoughts; "too fast" is usually as much
 * about missing pauses as about words per minute.
 */
const VO = `You can make a bad experience feel less bad by making it longer. <break time="0.9s" />

That's not a typo. <break time="0.5s" /> It's a bucket of cold water, and a Nobel prize. <break time="0.9s" />

Kahneman's team had people hold one hand in fourteen-degree water, for sixty seconds. <break time="0.6s" /> Unpleasant. <break time="0.8s" />

Then a second round. <break time="0.5s" /> The same sixty seconds — plus thirty more, <break time="0.3s" /> while the water came up by a single degree. <break time="0.6s" /> Still cold. <break time="0.4s" /> Just slightly less awful, right at the end. <break time="0.9s" />

So round two is strictly worse. <break time="0.5s" /> Same pain, plus extra pain. <break time="0.9s" />

Then they asked which one people would rather do again. <break time="0.8s" />

Sixty-nine percent picked the longer one. <break time="1.0s" />

Because your memory doesn't add up the seconds. <break time="0.6s" /> It keeps two snapshots. <break time="0.5s" /> The worst moment, <break time="0.3s" /> and the last one. <break time="1.0s" />

Which means the end of a thing is doing far more work than the middle. <break time="0.7s" /> The last day of a holiday. <break time="0.5s" /> How an argument finishes. <break time="1.0s" />

You're not remembering it. <break time="0.5s" /> You're remembering the highlights.`

const KEY = process.env.ELEVENLABS_API_KEY
if (!KEY) {
  console.error('ELEVENLABS_API_KEY not set.')
  console.error('It lives only in the running video-server process, not in .env:')
  console.error('  export $(ps eww $(pgrep -f local-video-server.mjs | head -1) | tr " " "\\n" | grep ^ELEVENLABS_API_KEY=)')
  process.exit(1)
}

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

const words = VO.replace(/<break[^>]*>/g, ' ').trim().split(/\s+/).length
console.log(`${out}\n${words} words at speed ${SPEED}`)
console.log('verify it is not silent:')
console.log(`  ffmpeg -i "${out}" -af volumedetect -f null /dev/null 2>&1 | grep mean_volume`)
