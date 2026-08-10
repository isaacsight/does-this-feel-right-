/**
 * Narration. Calls ElevenLabs DIRECTLY, not through the GALLEY proxy — the
 * proxy does not forward the `speed` parameter, and every voice runs 166–186
 * wpm without it. The film is written for 0.75.
 *
 * The key is read from the environment only. It is never written to .env and
 * never printed.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { join } from 'node:path'

const KEY = process.env.ELEVENLABS_API_KEY
if (!KEY) { console.error('ELEVENLABS_API_KEY not in environment'); process.exit(1) }
const OUT = fileURLToPath(new URL('.', import.meta.url))
const VOICE = 'iP95p4xoKVk53GoZ742B' // Chris

// Pull the quoted VO block out of SCRIPT.md and strip the [C7]-style claim tags.
const md = readFileSync(join(OUT, process.env.SCRIPT || 'SCRIPT.md'), 'utf8')
const body = md.split('## VO')[1].split('---')[0]
const text = body.split('\n')
  .filter(l => l.trim().startsWith('>'))
  .map(l => l.replace(/^\s*>\s?/, '').replace(/`\[C\d+\]\[?C?\d*\]?`/g, '').replace(/\*/g, '').trim())
  .filter(l => l && !l.startsWith('('))
  .join('\n\n')
console.log(`${text.split(/\s+/).length} words`)

const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE}`, {
  method: 'POST',
  headers: { 'xi-api-key': KEY, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text,
    model_id: 'eleven_multilingual_v2',
    voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: 0.75 },
  }),
})
if (!res.ok) { console.error('TTS failed', res.status, (await res.text()).slice(0, 200)); process.exit(1) }
mkdirSync(join(OUT, 'audio'), { recursive: true })
const p = join(OUT, 'audio', process.env.OUTMP3 || 'narration.mp3')
writeFileSync(p, Buffer.from(await res.arrayBuffer()))
console.log('saved', p)
