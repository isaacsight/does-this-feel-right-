/**
 * Frame generation for "The Last Thing That Happens".
 *
 *   node videos/peak-end-rule/generate.mjs --estimate       # free
 *   node videos/peak-end-rule/generate.mjs --validate       # frames 1 and 9 only
 *   node videos/peak-end-rule/generate.mjs --rest           # the remaining 15
 *
 * The hero MUST be passed as params.image_urls — an array nested INSIDE params.
 * At the top level the proxy silently drops it, fal receives image_urls: [] and
 * rejects the job asynchronously, AFTER billing. That cost $0.24 on the last
 * film. The MCP production tools cannot express this (their params schema takes
 * scalars only), which is why this talks to the proxy directly.
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
const HERO = 'https://v3b.fal.media/files/b/0aa37f8b/o9m6ImAnSEVwp8kVc6CN1_znkpMuiW.png'
const MODEL = 'fal-ai/nano-banana-2/edit'
// fileURLToPath, NOT .pathname — the latter percent-encodes the space in
// "blog design", so writes land in a literal blog%20design/ directory.
const OUT = fileURLToPath(new URL('.', import.meta.url))

/**
 * The comedy mandate, verbatim from PRODUCTION-PLAYBOOK.md.
 *
 * Do not add "calm", "comforting", "quiet", "gentle", "restrained" or
 * "tasteful". Those nine words caused three full rebuilds of the last film.
 */
const STYLE = `Crude, funny hand-drawn cartoon in the style of a comedic explainer channel. \
Thin stick-figure character with a round head and a BIG exaggerated expression — wide bulging eyes, \
dropped jaw, raised brows, or a flat deadpan stare, whichever the joke needs. Cartoon reaction \
conventions welcome: sweat drops, motion lines, squiggles, wobble lines, exaggerated posture. \
Muted flat colour set with confident black outlines — warm tans, muted yellows, soft greys. \
Exactly ONE flat tomato-red element as the accent. Comic, energetic, absurd situation played \
completely straight. Legible at a glance. 16:9.

CRITICAL CONSTRAINT: there must be absolutely NO letters, words, numbers, labels, captions, \
signage, or comic sound-effect text anywhere in the image. No writing of any kind.`

/** Situations, not symbols. The hero reacts in every one. Absurd played straight. */
const FRAMES = [
  { id: 'f01', hold: 3.0, scene: 'The character sits at a plain wooden table with one thin hand submerged in a steel bucket of ice water. Flat deadpan stare directly ahead, completely expressionless. A red stopwatch sits on the table beside the bucket.' },
  { id: 'f02', hold: 2.2, scene: 'Tight close-up on a steel bucket of ice water on a table. Ice cubes float on the surface. A glass thermometer with a red liquid column leans against the rim. A thin cartoon wrist disappears into the water.' },
  { id: 'f03', hold: 1.8, scene: 'Extreme close-up of the character\'s round head and face only. Mildly betrayed expression, mouth a flat wobbling line, one large sweat drop at the temple. A small red button pinned to the collar.' },
  { id: 'f04', hold: 3.4, scene: 'Wide shot of a bare laboratory room. The character is small in frame, seated at a table with the bucket. A second stick figure in a white coat stands watching, holding a clipboard with a red clip, entirely impassive.' },
  { id: 'f05', hold: 2.0, scene: 'A large stopwatch held up in a thin cartoon hand against a plain tan wall. The sweep hand is mid-arc. The second hand is bright red.' },
  { id: 'f06', hold: 3.4, scene: 'The character slumped forward with one cheek flat on the table, arm still down in the steel bucket, eyes half closed in weary resignation. A single tiny wisp of vapour rises from the water. The thermometer column is red.' },
  { id: 'f07', hold: 2.2, scene: 'The character turns to stare directly at a thermometer held in front of their face, utterly unmoved, dead-eyed, mouth a flat line. Squiggle lines beside the head. The thermometer liquid is red.' },
  { id: 'f08', hold: 3.2, scene: 'Two identical steel buckets sit side by side on a grey floor. The character stands between them, chin resting in one hand, genuinely deliberating, one foot mid-tap. A red tag hangs from the right-hand bucket.' },
  { id: 'f09', hold: 1.6, scene: 'The character points with enormous confidence at the right-hand of two steel buckets, huge open grin, other hand planted on hip, chest out. A red tag hangs from the bucket being pointed at.' },
  { id: 'f10', hold: 3.0, scene: 'A room full of about ten identical stick figures. Most of them are crowded together on the right side around a single bucket, packed shoulder to shoulder. The bucket is red.' },
  { id: 'f11', hold: 2.4, scene: 'Three lone stick figures stand on the left side of a mostly empty room, looking around at the empty space with confused expressions and sweat drops. A small red bucket sits at their feet.' },
  { id: 'f12', hold: 3.4, scene: 'Cross-section cutaway of the character\'s round head in profile, showing the inside is almost entirely empty. Two small polaroid photographs hang from a wire strung across the interior. One clothespin is red.' },
  { id: 'f13', hold: 3.0, scene: 'Close-up of two polaroid photographs lying on a table. One photograph shows a howling screaming cartoon face. The other shows the same face giving a flat indifferent shrug. One polaroid has a red border.' },
  { id: 'f14', hold: 2.8, scene: 'A long strip of film laid flat across a table, running the width of the frame. Almost every frame in the strip is blank and empty. Exactly two frames contain a picture. One of those two frames is red.' },
  { id: 'f15', hold: 3.2, scene: 'An airport departure gate with rows of empty seats. The character stands holding a duffel bag, skin burnt bright pink from sun, staring blankly ahead with a completely vacant expression. The duffel bag is red.' },
  { id: 'f16', hold: 3.0, scene: 'Two stick figures at the end of an argument in a doorway. One is half-turned to leave with slumped shoulders. The other gives a small awkward apologetic wave. The door is red.' },
  { id: 'f17', hold: 3.4, scene: 'The character sits alone in a dim room watching two images loop on a small projector screen. Their back is to us, head tilted slightly. The projector beam is red.' },
]

/**
 * Reshoots. Three frames failed the gate on first pass:
 *
 * - f12 asked for a cross-section of the hero's HEAD. The model rendered a
 *   separate grey disc standing beside the hero instead. This is the documented
 *   trap: anything staged on or in the head goes wrong. Restaged at floor level.
 * - f13 rendered the word "SCREAM". f14 rendered "A" and "B".
 *   The trailing "no lettering" lost to a scene concept that IMPLIED labels.
 *   Both are restaged to avoid implying a label at all, and the style block now
 *   carries an explicit final constraint rather than a trailing clause.
 */
const RESHOOTS = [
  { id: 'f12', hold: 3.4, scene: 'A short length of string is tied between the backs of two wooden chairs in an otherwise completely bare room. Exactly two small polaroid photographs hang from it by pegs. Nothing else hangs on the string. The character stands to one side looking at them, head tilted, puzzled. One peg is red.' },
  { id: 'f13', hold: 3.0, scene: 'Two polaroid photographs lie side by side on a plain table, viewed from directly above. The left photograph shows a cartoon face with its mouth stretched wide open in agony, eyes screwed shut. The right photograph shows the same face completely relaxed and indifferent, shoulders raised in a small shrug. The right photograph has a red border.' },
  { id: 'f14', hold: 2.8, scene: 'A long strip of camera film lies flat across a table, stretching the full width of the frame. Every panel in the strip is empty and blank except two: one panel near the middle holds a tiny picture, and one panel near the end is filled with solid red. The character leans over the strip inspecting it with a magnifying glass, eyes wide.' },
]

const post = async (path, body) => {
  const res = await fetch(`${ENGINE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` },
    body: JSON.stringify(body),
  })
  const text = await res.text()
  if (!res.ok) throw new Error(`${path} ${res.status}: ${text.slice(0, 400)}`)
  return JSON.parse(text)
}

const bodyFor = f => ({
  endpoint: MODEL,
  prompt: `${f.scene}\n\n${STYLE}`,
  // THE array must be nested here. Top level is silently dropped.
  params: { image_urls: [HERO], aspect_ratio: '16:9' },
})

const mode = process.argv[2] || '--estimate'
const pick = mode === '--validate' ? FRAMES.filter(f => ['f01', 'f09'].includes(f.id))
           : mode === '--rest'     ? FRAMES.filter(f => !['f01', 'f09'].includes(f.id))
           : mode === '--reshoot'  ? RESHOOTS
           : FRAMES

if (mode === '--estimate') {
  const e = await post('/v1/images/estimate', bodyFor(FRAMES[0]))
  console.log(`per frame: $${e.usd}  (${e.pricingText || 'no pricing text'})`)
  console.log(`${FRAMES.length} frames: $${(e.usd * FRAMES.length).toFixed(2)}`)
  process.exit(0)
}

console.log(`submitting ${pick.length} frames — ${pick.map(f => f.id).join(', ')}`)
const jobs = []
for (const f of pick) {
  const body = bodyFor(f)
  // Each submit needs a live quoteToken bound to its own body; they expire in 5 min.
  const { usd, quoteToken } = await post('/v1/images/estimate', body)
  if (!quoteToken) throw new Error(`${f.id}: estimate returned no quoteToken`)
  const j = await post('/v1/images/fal', { ...body, quoteToken })
  jobs.push({ id: f.id, jobId: j.jobId, usd })
  console.log(`  ${f.id} -> ${j.jobId}  $${usd}`)
}

mkdirSync(join(OUT, 'frames'), { recursive: true })
writeFileSync(join(OUT, `jobs-${mode.slice(2)}.json`), JSON.stringify(jobs, null, 2))
console.log(`\njob ids written to jobs-${mode.slice(2)}.json`)
console.log('poll with: node videos/peak-end-rule/poll.mjs')
