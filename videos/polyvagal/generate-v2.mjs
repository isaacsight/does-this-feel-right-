/**
 * Frame generation for "The Third Thing".
 *
 *   node videos/polyvagal/generate.mjs --estimate
 *   node videos/polyvagal/generate.mjs --validate    # f01 and f35 only
 *   node videos/polyvagal/generate.mjs --batch 1     # 20 at a time
 *
 * The hero MUST be passed as params.image_urls — an array nested INSIDE params.
 * At the top level the proxy drops it, fal rejects the job asynchronously AFTER
 * billing, and nothing is produced. That cost $0.24 on the first film, which is
 * also why this talks to the proxy directly: the MCP production tools take only
 * scalar params and cannot express an array.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { V2 as FRAMES, V2_FIX, V2_FILL, V2_CONT } from './frames-v2.mjs'

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
const HERO = 'https://v3b.fal.media/files/b/0aa37f8b/o9m6ImAnSEVwp8kVc6CN1_znkpMuiW.png'
const MODEL = 'fal-ai/nano-banana-2/edit'
// fileURLToPath, NOT .pathname — the latter percent-encodes the space in
// "blog design" and writes into a literal blog%20design/ directory.
const OUT = fileURLToPath(new URL('.', import.meta.url))

/**
 * The comedy mandate, verbatim from PRODUCTION-PLAYBOOK.md, plus the explicit
 * final constraint. Do NOT add calm/comforting/quiet/gentle/restrained/tasteful
 * — those nine words caused three full rebuilds of the first film.
 *
 * The trailing "no lettering" clause alone is too weak: it lost twice to scene
 * concepts that implied labels (an A/B comparison produced "A" and "B"; a
 * scream produced "SCREAM"). Hence the CRITICAL block.
 *
 * NEVER name a concrete example object in the style block. It is applied to
 * every frame, so an example becomes an instruction: an opossum offered once
 * as an illustration of "silly but not arbitrary" was then drawn into seven of
 * ten frames. The style block describes HOW to draw. Scene text says WHAT.
 * (The opossum was kept — deliberately, as a running character — but that was
 * a decision made after the fact, not what the prompt asked for.)
 */
const STYLE = `Crude, funny hand-drawn cartoon in the style of a comedic explainer channel. \
Thin stick-figure character with a round head and a BIG exaggerated expression — wide bulging eyes, \
dropped jaw, raised brows, or a flat deadpan stare, whichever the joke needs. Cartoon reaction \
conventions welcome: sweat drops, motion lines, squiggles, wobble lines, exaggerated posture. \
Muted flat colour set with confident black outlines — warm tans, muted yellows, soft greys. \
Exactly ONE flat tomato-red element as the accent. Comic, energetic, absurd situation played \
completely straight. Legible at a glance. 16:9.

CARTOON PHYSICS: this world runs on classic cartoon logic, and the rules of the real one do not \
apply. Bodies deflate, stretch, snap off, melt, sink through solid floors, leave character-shaped \
holes in walls, hover in mid-air until they look down. Jaws detach and hit the ground. Eyes leave \
their sockets. Skeletons fall out. Steam leaves ears. A person can be flattened completely and peel \
themselves up. Consequences are enormous and instant and wildly out of proportion to their cause.

THE FORMULA: every frame is a SITUATION AN ORDINARY PERSON HAS LIVED THROUGH, resolved by an \
IMPOSSIBLE CARTOON CONSEQUENCE. The setup must be recognisable — a meeting, a text message, a sofa, \
a bad phone call. The payoff must be physically impossible. Never draw a diagram, a symbol or a \
metaphor object; draw the person it is happening to. And nobody in frame ever acknowledges that \
anything strange has occurred — everyone carries on completely normally.

CRITICAL CONSTRAINT: there must be absolutely NO letters, words, numbers, labels, captions, \
signage, or comic sound-effect text anywhere in the image. No writing of any kind.`

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

const bodyFor = f => ({
  endpoint: MODEL,
  prompt: `${f.scene}\n\n${STYLE}`,
  params: { image_urls: [HERO], aspect_ratio: '16:9' },   // array MUST nest here
})

const mode = process.argv[2] || '--estimate'
const VALIDATE = ['g01', 'g39']
const BATCH = 20

let pick, tag
if (mode === '--cont') { pick = V2_CONT; tag = 'cont' }
else if (mode === '--fill2') { pick = V2_FILL; tag = 'fill2' }
else if (mode === '--fix') { pick = V2_FIX; tag = 'fix' }
else if (mode === '--validate') { pick = FRAMES.filter(f => VALIDATE.includes(f.id)); tag = 'validate' }
else if (mode === '--batch') {
  const n = Number(process.argv[3] || 1)
  const rest = FRAMES.filter(f => !VALIDATE.includes(f.id))
  pick = rest.slice((n - 1) * BATCH, n * BATCH)
  tag = `batch${n}`
  console.log(`batch ${n} of ${Math.ceil(rest.length / BATCH)}`)
} else {
  const e = await post('/v1/images/estimate', bodyFor(FRAMES[0]))
  console.log(`per frame $${e.usd} · ${FRAMES.length} frames = $${(e.usd * FRAMES.length).toFixed(2)}`)
  process.exit(0)
}

if (!pick.length) { console.log('nothing in that batch'); process.exit(0) }
console.log(`submitting ${pick.length}: ${pick.map(f => f.id).join(' ')}`)
const jobs = []
for (const f of pick) {
  const body = bodyFor(f)
  // Each submit needs a live quoteToken bound to its own body; they expire in 5 min.
  const { usd, quoteToken } = await post('/v1/images/estimate', body)
  if (!quoteToken) throw new Error(`${f.id}: no quoteToken`)
  const j = await post('/v1/images/fal', { ...body, quoteToken })
  jobs.push({ id: f.id, jobId: j.jobId, usd })
  console.log(`  ${f.id} -> ${j.jobId}`)
}
mkdirSync(join(OUT, 'frames-v2'), { recursive: true })
writeFileSync(join(OUT, `jobs-v2-${tag}.json`), JSON.stringify(jobs, null, 2))
console.log(`\nwritten jobs-v2-${tag}.json · spend $${(jobs.length * 0.08).toFixed(2)}`)
console.log(`poll: node videos/polyvagal/poll.mjs jobs-v2-v2-${tag}.json`)
