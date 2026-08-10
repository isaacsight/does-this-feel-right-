/**
 * Frame generation for "Your Memory Is Not the Original".
 *
 *   node videos/memory-reconsolidation/generate.mjs --sheet
 *
 * Routing directive (2026-07-26): drafts on nano-banana-2, finals on
 * nano-banana-pro, ALL production frames on nano-banana-pro/edit with the
 * character sheet + style reference passed in.
 *
 * Two traps carried over from the last film, both of which cost real money:
 *   - image_urls MUST be an array nested inside `params`. At the top level the
 *     proxy drops it and fal bills before failing asynchronously.
 *   - fileURLToPath, NOT .pathname — the latter percent-encodes the space in
 *     "blog design" and writes into a literal blog%20design/ directory.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
const OUT = fileURLToPath(new URL('.', import.meta.url))

// The protagonist, carried forward from THE THIRD THING so the strand has one
// continuous character. This is the only text-free source of truth for the face.
const HERO = 'https://v3b.fal.media/files/b/0aa37f8b/o9m6ImAnSEVwp8kVc6CN1_znkpMuiW.png'

const PRO_EDIT = 'fal-ai/nano-banana-pro/edit'

/**
 * Style block. Adapted from the polyvagal film's, with this episode's palette.
 * Do NOT add calm/comforting/quiet/gentle/restrained/tasteful — those words
 * caused three full rebuilds of the first film.
 * NEVER name a concrete example object here; the block is applied to every
 * frame, so an example becomes an instruction.
 */
const STYLE = `Crude, funny hand-drawn cartoon in the style of a comedic explainer channel. \
Thin stick-figure character with a round head and a BIG exaggerated expression. Cartoon reaction \
conventions welcome: sweat drops, motion lines, squiggles, wobble lines, exaggerated posture. \
Confident black outlines. Muted flat colour: warm beige rooms, charcoal interiors, cream paper, \
soft greys, restrained grey clothing. At most ONE flat red element per image. \
Comic, absurd situation played completely straight. Legible at a glance.

RED DISCIPLINE: red means EVIDENCE, CORRECTION or CONTAMINATION. It may only ever appear on a \
small object that someone is handling, filing or repairing. Red must NEVER appear on a person: \
not on skin, hands, faces, hair or clothing. If no object in the scene qualifies, use no red at \
all — an image with zero red is correct and preferred over a red body part.

CRITICAL CONSTRAINT: there must be absolutely NO letters, words, numbers, labels, captions, \
signage, or comic sound-effect text anywhere in the image. No writing of any kind. All \
typography is added later in composition.`

/**
 * "Character sheet" reads to the model as EXPRESSION variations — the first
 * attempt returned three forward-facing emotional states, one with a red head,
 * which is useless as a neutral conditioning reference. Describe the rotation
 * as a physical fact about each figure instead, and forbid expression change.
 */
const SHEET = `The same single stick-figure character standing in three positions side by side \
against a completely plain flat beige background, with clear empty space between each figure. \
LEFT FIGURE: body and face pointing directly at the viewer, both eyes visible, arms hanging at \
the sides. MIDDLE FIGURE: the same character having rotated 45 degrees to their left, so the \
body is angled away and both eyes are still visible. RIGHT FIGURE: the same character having \
rotated fully 90 degrees, seen entirely from the side, so only ONE eye is visible and the nose \
line breaks the edge of the face. All three have the exact same calm neutral expression, mouth \
a small flat line, no eyebrows raised. Identical height, proportions, round head and plain grey \
top. Full body, head to feet, nothing cropped. No props, no furniture, no shadows, no motion \
lines, no sweat drops. Skin and head stay the same pale cream colour in all three figures.`

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

// The proxy prices from its catalog cache, and the cache is filled PER CATEGORY.
// nano-banana-*/edit lives under image-to-image; until that category has been
// fetched at least once, catalogEntry() misses, usdPerImage is null, no quote
// token is issued, and /v1/images/fal answers 409. Warm it first.
for (const cat of ['image-to-image', 'text-to-image']) {
  await fetch(`${ENGINE}/v1/catalog?category=${cat}`, { headers: { Authorization: `Bearer ${TOKEN}` } })
}

// The locked protagonist turnaround. Reference #1 on every production frame.
const SHEET_REF = 'https://v3b.fal.media/files/b/0aa3db9d/U3r7UQmtGuB_4TO6vWphS_3036eLDG.png'
// Reference #2 — the CLEAN empty plate. Set after --plate2 lands.
const M25_REF = process.env.M25_REF || ''
const PLATE_REF = process.env.PLATE_REF
  || 'https://v3b.fal.media/files/b/0aa3dbb6/UWIS-MoakJt3IsqOQD4hY_4AU01DSd.png'

/**
 * The style plate. Establishes the world's palette, light and line weight in
 * one image so later frames can be conditioned on it instead of re-deriving
 * the look from adjectives. Deliberately EMPTY of people: a plate with a
 * character in it competes with the character sheet as a reference.
 * It doubles as the Act III establishing shot.
 */
const PLATE = `A wide empty interior of a cluttered film-restoration workshop, seen straight on \
from across the room. Charcoal-grey walls and deep shadow at the edges, warm beige light pooling \
in the middle of the floor. Tall wooden shelving along both walls, stacked with plain cream-\
coloured folders and cardboard document boxes, slightly untidy, some leaning. In the centre of \
the floor, a small half-built theatrical stage set of a domestic room — three flat painted walls \
propped up from behind by timber braces, obviously fake when seen from this angle. A workbench \
to one side with brushes and pots. Exactly ONE tomato-red object in the whole room, small, \
sitting on the workbench. Completely empty of people. Nobody in frame.`

const PRO = 'fal-ai/nano-banana-pro' // text-to-image; no refs, so not the edit endpoint

// Clean environment plate, reference #2. Passing ANY character reference
// inserts that character — the first plate came back populated despite
// "nobody in frame", because the image beat the instruction. So: no refs,
// which means text-to-image rather than edit.
/**
 * The STYLE BLOCK was inserting the person, not the reference image. Its first
 * sentence is a standing instruction to draw a character ("Thin stick-figure
 * character with a round head and a BIG exaggerated expression"), applied to
 * every frame — so an environment plate got one anyway, off-model and grimacing,
 * with no reference passed at all and the prompt shouting that the room is empty.
 *
 * Same lesson as the last film's opossum, one level up: the style block says HOW
 * to draw, and anything it NAMES becomes a thing that must appear. For frames
 * with no people, the character clause has to come out entirely.
 *
 * Also: "tomato-red" produced a literal tomato on the workbench. Use "flat red".
 */
const STYLE_ENV = `Crude hand-drawn cartoon in the style of a comedic explainer channel. \
Confident black outlines. Muted flat colour: warm beige rooms, charcoal interiors, cream paper, \
soft greys. Exactly ONE flat red element as the accent. Legible at a glance.

CRITICAL CONSTRAINT ONE: this is an EMPTY ROOM. There are no people in this picture. No \
characters, no figures, no faces, no bodies, no hands, no silhouettes. Architecture, furniture \
and objects only.

CRITICAL CONSTRAINT TWO: absolutely NO letters, words, numbers, labels, captions, signage or \
sound-effect text anywhere in the image. No writing of any kind.`

const PLATE_EMPTY = `${PLATE} The room is deserted, photographed between shifts.`

const M16 = `A wide interior of the cluttered charcoal-grey film-restoration workshop shown in \
the reference image, same shelving, same warm pool of beige light on the floor, same half-built \
theatrical set of a domestic room braced with timber. The stick-figure character from the other \
reference is standing just inside the doorway at the left, stopped dead, staring at the room \
with a huge shocked open-mouthed expression, arms limp at their sides. Two archivist figures in \
the background continue working on the set and do not look up at him.`

const M26 = `A plain, sparse beige room, seen straight on. On the left, a stick-figure person \
sits on a simple chair, facing the viewer, hands in their lap, entirely neutral flat expression. \
On the right, a second stick-figure person stands holding a small cream notepad, leaning \
forward and gesturing emphatically with one hand as they ask a question, mouth open wide, \
eyebrows up. Nothing else in the room. No furniture beyond the one chair. Flat even lighting.`


/**
 * m25 / m26 — the 1974 pair. Their whole argument is that the SEATED figure and
 * the QUESTIONER are the same people in both frames; only the questioner's
 * posture changes ("hit" vs "smashed"). So m25 is generated first and passed to
 * m26 as reference #1, ahead of the character sheet, to dominate identity.
 *
 * The workshop plate is deliberately NOT passed here — this is a plain room,
 * and the plate would drag shelving and film canisters into it.
 */
const ROOM_1974 = `A plain sparse room with warm beige walls and a beige floor, seen straight \
on, wide. On the LEFT, a stick-figure person sits on a simple wooden chair angled slightly \
toward the centre, both feet on the floor, hands resting in their lap, with a completely \
neutral flat expression — a small straight line for a mouth, no eyebrows raised. On the RIGHT, \
a second stick-figure person stands facing them, holding a small blank cream notepad in one \
hand. The room is otherwise completely empty: no other furniture, no pictures, no objects. \
Flat even lighting. Both figures are drawn full body, head to feet, nothing cropped.`

const M25 = `${ROOM_1974}

The standing questioner is UPRIGHT and still, weight evenly on both feet, shoulders level, \
free hand held low and relaxed near their side, mouth a small neutral open oval as they ask a \
short quiet question. Calm and procedural. No motion lines, no sweat drops, no wobble.`

const M26_PAIR = `${ROOM_1974}

This is the SAME two people in the SAME room and the SAME camera position as the reference \
image — identical faces, identical heights, identical grey tops, identical chair, identical \
wall and floor colours. The seated figure on the left has not moved at all and keeps the exact \
same neutral flat expression. The ONLY change is the standing questioner on the right, who is \
now leaning forward from the waist toward the seated figure, free hand raised and open in an \
emphatic gesture, mouth open wider, eyebrows down and pressed together, asking the same \
question far more forcefully. A few small motion lines behind their raised arm.`

const MODE = process.argv[2] || '--plate2'
const JOBS = {
  '--sheet':  { prompt: SHEET,       refs: [HERO],                  file: 'character-sheet-v2.png', endpoint: PRO_EDIT },
  '--plate':  { prompt: PLATE,       refs: [SHEET_REF],             file: 'style-plate.png',        endpoint: PRO_EDIT },
  '--plate2': { prompt: PLATE_EMPTY, refs: [],                      file: 'style-plate-empty.png',  endpoint: PRO, style: STYLE_ENV },
  '--m16':    { prompt: M16,         refs: [SHEET_REF, PLATE_REF],  file: 'validate-m16.png',       endpoint: PRO_EDIT },
  '--m26':    { prompt: M26,         refs: [SHEET_REF, PLATE_REF],  file: 'validate-m26.png',       endpoint: PRO_EDIT },
  '--m25p':   { prompt: M25,         refs: [SHEET_REF],             file: 'validate-m25.png',       endpoint: PRO_EDIT },
  '--m26p':   { prompt: M26_PAIR,    refs: [M25_REF, SHEET_REF],    file: 'validate-m26-pair.png',  endpoint: PRO_EDIT },
}
const spec = JOBS[MODE]
if (!spec) { console.log(`unknown mode ${MODE} — one of ${Object.keys(JOBS).join(', ')}`); process.exit(1) }

const body = {
  endpoint: spec.endpoint,
  prompt: `${spec.prompt}\n\n${spec.style || STYLE}`,
  params: {
    ...(spec.refs.length ? { image_urls: spec.refs } : {}), // array MUST nest here
    aspect_ratio: '16:9',
    resolution: '2K',
  },
}

// Submission requires a token from this endpoint's OWN estimate, same body.
const quote = await post('/v1/images/estimate', body)
console.log(`quoted $${quote.usd}/image`)
if (!quote.quoteToken) throw new Error(`no quote token: ${JSON.stringify(quote).slice(0, 200)}`)

const job = await post('/v1/images/fal', { ...body, quoteToken: quote.quoteToken })
console.log('submitted:', JSON.stringify(job).slice(0, 300))

const id = job.id || job.jobId || job.job_id
if (!id) { console.log('no job id returned — inspect the payload above'); process.exit(1) }

for (let i = 0; i < 60; i++) {
  await new Promise(r => setTimeout(r, 5000))
  const res = await fetch(`${ENGINE}/v1/videos/jobs/${id}`, {
    headers: { Authorization: `Bearer ${TOKEN}` },
  })
  const s = await res.json()
  const state = s.status || s.state
  process.stdout.write(`  ${i * 5}s ${state}\n`)
  // 'done' is this proxy's terminal state. Omitting it made the loop spin the
  // full 300s on a finished job and never save the file.
  if (state === 'done' || state === 'succeeded' || state === 'completed' || s.output || s.url) {
    // This proxy returns sourceUrl (fal CDN) and imageUrl (its own local cache).
    // Prefer sourceUrl: it is the durable original and needs no running server.
    const url = s.sourceUrl || s.imageUrl || s.url || s.output?.images?.[0]?.url
    console.log('URL:', url)
    if (url) {
      mkdirSync(join(OUT, 'assets'), { recursive: true })
      const buf = Buffer.from(await (await fetch(url)).arrayBuffer())
      const p = join(OUT, 'assets', spec.file)
      writeFileSync(p, buf)
      console.log('saved:', p, `${(buf.length / 1024).toFixed(0)}KB`)
    }
    console.log(JSON.stringify(s).slice(0, 500))
    break
  }
  if (state === 'failed' || state === 'error') { console.log('FAILED:', JSON.stringify(s).slice(0, 500)); break }
}
