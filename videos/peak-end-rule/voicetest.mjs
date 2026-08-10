/**
 * Audition narrator voices on the film's actual hook line.
 *
 * Premade ElevenLabs voices are available on every account, so these ids are
 * stable. Costs nothing: elevenlabs-v2 runs direct, zero fal spend.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
const DIR = fileURLToPath(new URL('.', import.meta.url))

const LINE = `You can make a bad experience feel less bad by making it longer. <break time="0.8s" /> That's not a typo. <break time="0.5s" /> It's a bucket of cold water, and a Nobel prize.`

const VOICES = [
  ['george',  'JBFqnCBsd6RMkjVDRZzb'],  // British, warm, storytelling
  ['chris',   'iP95p4xoKVk53GoZ742B'],  // casual conversational
  ['brian',   'nPczCjzI2devNBz1zQrb'],  // deep documentary
  ['will',    'bIHbv24MWmeRgasZH58o'],  // friendly conversational
  ['davis',   'Z2fsAwk7IblvPhYzfslC'],  // the current take, for comparison
]

const post = async (p, b) => {
  const r = await fetch(`${ENGINE}${p}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify(b),
  })
  const t = await r.text()
  if (!r.ok) throw new Error(`${p} ${r.status}: ${t.slice(0, 200)}`)
  return JSON.parse(t)
}

mkdirSync(join(DIR, 'voicetest'), { recursive: true })
const jobs = []
for (const [name, voice] of VOICES) {
  const body = {
    text: LINE, voice, provider: 'elevenlabs-v2',
    voiceSettings: { stability: 0.4, similarityBoost: 0.75, style: 0 },
  }
  try {
    const est = await post('/v1/audio/estimate', body)
    const job = await post('/v1/audio/speech', { ...body, quoteToken: est.quoteToken })
    jobs.push({ id: name, jobId: job.jobId })
    console.log(`${name.padEnd(8)} -> ${job.jobId}`)
  } catch (e) {
    console.log(`${name.padEnd(8)} FAILED ${e.message}`)
  }
}
writeFileSync(join(DIR, 'jobs-voicetest.json'), JSON.stringify(jobs, null, 2))
