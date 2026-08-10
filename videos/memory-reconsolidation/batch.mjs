/**
 * Batch runner — Acts I–V.
 *
 *   node videos/memory-reconsolidation/batch.mjs 1 5     # acts 1 through 5
 *
 * Enforces the $10/day proxy cap in this script as well as in the server: it
 * refuses to start a frame that would cross CAP, and it counts money already
 * spent today from batch-log.json rather than assuming a clean slate.
 *
 * Sequential reference ordering: within a continuity group, each frame receives
 * the PREVIOUS APPROVED FRAME as reference #1, ahead of the character sheet.
 * That ordering is what held the m25/m26 pair — the returning figure stayed the
 * same drawing rather than a similar one.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { ACTS_I_V, ACTS_VI_IX, HANDS, LOCKED_CAMERA, EMPHATIC_NOT_ANGRY } from './frames.mjs'
const ALL = [...ACTS_I_V, ...ACTS_VI_IX]

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
const OUT = fileURLToPath(new URL('.', import.meta.url))
const LOG = join(OUT, 'batch-log.json')
const PRO_EDIT = 'fal-ai/nano-banana-pro/edit'

const SHEET_REF = 'https://v3b.fal.media/files/b/0aa3db9d/U3r7UQmtGuB_4TO6vWphS_3036eLDG.png'
const PLATE_REF = 'https://v3b.fal.media/files/b/0aa3dbea/wPtgltibbZy-ymCj2sev9_Zdje7YjN.png'

// Isaac explicitly authorised exceeding the $10/day guard for this run
// ("ill pay for it"). The server's own FAL_DAILY_SPEND_LIMIT is raised to match
// via the launch environment, NOT by editing .env. Put both back afterwards.
const CAP = Number(process.env.RUN_CAP || 20.00)
const SPENT_BEFORE = Number(process.env.SPENT_TODAY || 0)

const STYLE = `Crude, funny hand-drawn cartoon in the style of a comedic explainer channel. \
Thin stick-figure character with a round head and a BIG exaggerated expression. Cartoon reaction \
conventions welcome: motion lines, squiggles, wobble lines, exaggerated posture. \
Confident black outlines. Muted flat colour: warm beige rooms, charcoal interiors, cream paper, \
soft greys, restrained grey clothing. At most ONE flat red element per image. \
Comic, absurd situation played completely straight. Legible at a glance.

RED DISCIPLINE: red means EVIDENCE, CORRECTION or CONTAMINATION. It may only ever appear on a \
small object that someone is handling, filing or repairing. Red must NEVER appear on a person: \
not on skin, hands, faces, hair or clothing. If no object in the scene qualifies, use no red at \
all — an image with zero red is correct and preferred over a red body part.

CRITICAL CONSTRAINT: there must be absolutely NO letters, words, numbers, labels, captions, \
signage, or comic sound-effect text anywhere in the image. No writing of any kind.`

const STYLE_ENV = `Crude hand-drawn cartoon in the style of a comedic explainer channel. \
Confident black outlines. Muted flat colour: warm beige rooms, charcoal interiors, cream paper, \
soft greys. At most ONE flat red element as the accent, never on a person. Legible at a glance.

CRITICAL CONSTRAINT ONE: this is an EMPTY ROOM. There are no people in this picture. No \
characters, no figures, no faces, no bodies, no hands, no silhouettes. Architecture, furniture \
and objects only.

CRITICAL CONSTRAINT TWO: absolutely NO letters, words, numbers, labels, captions, signage or \
sound-effect text anywhere in the image. No writing of any kind.`

const post = async (path, body) => {
  const res = await fetch(`${ENGINE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify(body),
  })
  const text = await res.text()
  if (!res.ok) throw new Error(`${path} ${res.status}: ${text.slice(0, 300)}`)
  return JSON.parse(text)
}

// Per-category catalog warm-up. Without it catalogEntry() misses, no quote
// token is issued, and every submission answers 409.
for (const cat of ['image-to-image', 'text-to-image']) {
  await fetch(`${ENGINE}/v1/catalog?category=${cat}`, { headers: { Authorization: `Bearer ${TOKEN}` } })
}

const log = existsSync(LOG) ? JSON.parse(readFileSync(LOG, 'utf8')) : { frames: [], spentUsd: 0 }
const done = new Map(log.frames.map(f => [f.id, f]))
// Writes go straight into the canonical dir. A separate frames/ directory was
// how uncorrected originals could be picked up by assembly by mistake; there is
// now exactly one place frames live. Compositing corrections are applied in
// place there, with the untouched generations kept in frames-original-backup/.
const CANON = 'frames-canonical'
mkdirSync(join(OUT, CANON), { recursive: true })

const [from, to] = [Number(process.argv[2] || 1), Number(process.argv[3] || 5)]
const queue = ALL.filter(f => f.act >= from && f.act <= to && !done.has(f.id))
console.log(`${queue.length} frames to generate · already spent today $${(SPENT_BEFORE + log.spentUsd).toFixed(2)}`)

const lastInGroup = new Map()
for (const f of log.frames) if (f.group) lastInGroup.set(f.group, f.url)

for (const f of queue) {
  const spentToday = SPENT_BEFORE + log.spentUsd
  if (spentToday + 0.15 > CAP) {
    console.log(`\nSTOPPING — next frame would cross the $${CAP.toFixed(2)} cap (at $${spentToday.toFixed(2)}).`)
    break
  }

  // Reference ordering: previous-in-group FIRST, then character, then environment.
  const prev = f.group ? lastInGroup.get(f.group) : null
  const refs = []
  if (prev) refs.push(prev)
  if (f.people !== false) refs.push(SHEET_REF)
  if (f.env === 'workshop') refs.push(PLATE_REF)
  if (!refs.length) refs.push(PLATE_REF)

  const parts = [f.scene]
  if (f.people !== false) parts.push(HANDS)
  if (f.emphatic) parts.push(EMPHATIC_NOT_ANGRY)
  if (prev) parts.push(LOCKED_CAMERA)
  parts.push(f.people === false ? STYLE_ENV : STYLE)
  const prompt = parts.join('\n\n')

  const body = { endpoint: PRO_EDIT, prompt, params: { image_urls: refs, aspect_ratio: '16:9', resolution: '2K' } }

  try {
    const quote = await post('/v1/images/estimate', body)
    if (!quote.quoteToken) throw new Error('no quote token')
    const job = await post('/v1/images/fal', { ...body, quoteToken: quote.quoteToken })
    const id = job.jobId || job.id

    let url = null
    for (let i = 0; i < 48; i++) {
      await new Promise(r => setTimeout(r, 5000))
      const s = await (await fetch(`${ENGINE}/v1/videos/jobs/${id}`, { headers: { Authorization: `Bearer ${TOKEN}` } })).json()
      if (s.status === 'done') { url = s.sourceUrl || s.imageUrl; break }
      if (s.status === 'failed' || s.status === 'error') throw new Error(`job ${s.status}: ${s.error}`)
    }
    if (!url) throw new Error('timed out')

    writeFileSync(join(OUT, CANON, `${f.id}.png`), Buffer.from(await (await fetch(url)).arrayBuffer()))
    log.frames.push({
      id: f.id, act: f.act, group: f.group || null, env: f.env, people: f.people !== false,
      url, jobId: id, usd: quote.usd, refs, refOrder: refs.map((r, i) =>
        `${i + 1}:${r === prev ? 'prev-in-group' : r === SHEET_REF ? 'character-sheet' : 'style-plate'}`),
      clauses: [f.people !== false ? 'HANDS' : null, f.emphatic ? 'EMPHATIC_NOT_ANGRY' : null,
                prev ? 'LOCKED_CAMERA' : null, f.people === false ? 'STYLE_ENV' : 'STYLE'].filter(Boolean),
      prompt,
    })
    log.spentUsd = Math.round((log.spentUsd + quote.usd) * 100) / 100
    if (f.group) lastInGroup.set(f.group, url)
    writeFileSync(LOG, JSON.stringify(log, null, 1))
    console.log(`${f.id} ok  $${(SPENT_BEFORE + log.spentUsd).toFixed(2)} spent  refs:${refs.length}${prev ? ' (seq)' : ''}`)
  } catch (err) {
    console.log(`${f.id} FAILED — ${err.message}`)
    log.frames.push({ id: f.id, act: f.act, error: err.message })
    writeFileSync(LOG, JSON.stringify(log, null, 1))
  }
}
console.log(`\ndone. batch $${log.spentUsd.toFixed(2)} · today $${(SPENT_BEFORE + log.spentUsd).toFixed(2)} of $${CAP.toFixed(2)}`)
