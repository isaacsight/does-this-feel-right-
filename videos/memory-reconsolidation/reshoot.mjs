/**
 * Reshoots for the five frames the full-resolution audit rejected.
 *
 *   node videos/memory-reconsolidation/reshoot.mjs
 *
 * Two lessons applied from m38:
 *   1. The generic LOCKED_CAMERA clause is NOT strong enough on its own — m38
 *      already had it and still drifted. The constraints have to sit in the
 *      scene text, naming the specific things that must not move.
 *   2. The kitchen frames drifted because m01 was first in its group, so
 *      m02–m06 each received the character sheet rather than the preceding
 *      frame and no camera lock ever fired. Here m03/m04/m05 are each anchored
 *      DIRECTLY to m01 rather than chained through one another — a chain
 *      compounds drift instead of removing it.
 */
import { readFileSync, writeFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
const OUT = fileURLToPath(new URL('.', import.meta.url))
const PRO_EDIT = 'fal-ai/nano-banana-pro/edit'
const SHEET = 'https://v3b.fal.media/files/b/0aa3db9d/U3r7UQmtGuB_4TO6vWphS_3036eLDG.png'

const log = JSON.parse(readFileSync(join(OUT, 'batch-log.json'), 'utf8'))
const url = id => log.frames.find(f => f.id === id).url

/** Names the specific things that must not move. Generic wording lost to m38. */
const LOCK = `The camera has not moved between the reference image and this one. Preserve exactly: \
the camera position, height, distance, crop and lens; the size of the protagonist in frame and \
the height of their eyeline; where their feet meet the floor; the wall corners, the floor line, \
the counter, the sink and the window; and all lighting and colour. The protagonist's full body \
is visible from head to feet with nothing cropped at any edge, exactly as in the reference. \
Only the single change described above is different.`

const HANDS = `Hands are relaxed and naturally shaped. When an open hand is visible, draw exactly \
five clearly separated fingers. Never draw a hand as a dangling hook, a curl or a stump — if a \
hand would otherwise dangle awkwardly, rest it flat against the body instead.`

const STYLE = `Crude, funny hand-drawn cartoon in the style of a comedic explainer channel. \
Thin stick-figure character with a round head and a BIG exaggerated expression. Cartoon reaction \
conventions welcome: motion lines, squiggles, wobble lines, exaggerated posture. \
Confident black outlines. Muted flat colour: warm beige rooms, charcoal interiors, cream paper, \
soft greys, restrained grey clothing. At most ONE flat red element per image.

RED DISCIPLINE: red means EVIDENCE, CORRECTION or CONTAMINATION, only ever on a small object \
someone is handling. Red must NEVER appear on a person — not skin, hands, faces, hair or \
clothing. Zero red is correct and preferred over a wrongly placed red.

CRITICAL CONSTRAINT: absolutely NO letters, words, numbers, labels, captions, signage or \
sound-effect text anywhere in the image. No writing of any kind.`

const JOBS = [
  { id: 'm03', refs: [url('m01'), SHEET], lock: true, scene:
    `This is the SAME kitchen, SAME camera and SAME protagonist as the reference image. The \
protagonist stands in the identical spot with arms folded, facing the viewer, unaware. The ONLY \
changes: a second smaller stick-figure archivist now stands on a wooden stepladder at the window \
behind them, calmly painting the curtains with a brush — the left curtain is finished and blue, \
the right one is still plain unpainted cream fabric.` },

  { id: 'm04', refs: [url('m01'), SHEET], lock: true, scene:
    `This is the SAME kitchen, SAME camera and SAME protagonist as the reference image, in the \
identical arms-folded pose with the identical pleased, certain expression. The ONE AND ONLY \
change in the entire picture: the window now has NO curtains whatsoever — just the bare curtain \
rail, plain glass and the window frame. The red mug, the sink, the counter, the walls and the \
protagonist are all completely unchanged.` },

  { id: 'm05', refs: [url('m01'), SHEET], lock: true, scene:
    `This is the SAME kitchen and SAME camera as the reference image, and the protagonist stands \
in the identical spot at the identical size. The window has no curtains, only a bare rail. The \
ONLY changes: the protagonist has twisted to look sharply back over one shoulder with wide eyes \
and an open mouth, having just noticed something; and a folded wooden stepladder now leans \
against the wall behind them.` },

  { id: 'm12', refs: [url('m11'), SHEET], lock: false, scene:
    `This is the SAME two people in the SAME plain room on the SAME two chairs in the SAME \
positions as the reference image, with the same camera. The teller on the left is now gesturing \
wildly with both arms raised and body leaning, animated and mid-story. The listener on the right \
sits perfectly still and calm. The listener's open notebook page shows a small neat grid of \
evenly spaced round DOTS — just dots, no lines, no marks, no letters, no writing of any kind. \
The dots are arranged in tidy even rows like a polka pattern.` },

  { id: 'm25', refs: [url('m26'), SHEET], lock: false, scene:
    `This is the SAME two people in the SAME plain beige room with the SAME chair and the SAME \
camera as the reference image. The seated figure on the left is unchanged — same position, same \
neutral flat expression, hands in lap. The ONLY change is the standing questioner on the right, \
who is now UPRIGHT and still rather than leaning: shoulders level, weight even on both feet, \
holding the small blank cream notepad in one hand, and with the other arm hanging straight down \
so that the hand rests flat and open against the side of their thigh, fingers together. Their \
mouth is a small neutral oval as they ask a short quiet question. Calm and procedural. No \
raised arm, no motion lines.` },
]

const post = async (p, b) => {
  const r = await fetch(ENGINE + p, { method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + TOKEN },
    body: JSON.stringify(b) })
  const t = await r.text()
  if (!r.ok) throw new Error(`${p} ${r.status}: ${t.slice(0, 200)}`)
  return JSON.parse(t)
}

for (const c of ['image-to-image', 'text-to-image']) {
  await fetch(`${ENGINE}/v1/catalog?category=${c}`, { headers: { Authorization: 'Bearer ' + TOKEN } })
}

let spent = 0
for (const j of JOBS) {
  const prompt = [j.scene, j.lock ? LOCK : null, HANDS, STYLE].filter(Boolean).join('\n\n')
  const body = { endpoint: PRO_EDIT, prompt,
    params: { image_urls: j.refs, aspect_ratio: '16:9', resolution: '2K' } }
  try {
    const q = await post('/v1/images/estimate', body)
    const job = await post('/v1/images/fal', { ...body, quoteToken: q.quoteToken })
    const id = job.jobId || job.id
    let out = null
    for (let i = 0; i < 48; i++) {
      await new Promise(r => setTimeout(r, 5000))
      const s = await (await fetch(`${ENGINE}/v1/videos/jobs/${id}`,
        { headers: { Authorization: 'Bearer ' + TOKEN } })).json()
      if (s.status === 'done') { out = s.sourceUrl || s.imageUrl; break }
      if (s.status === 'failed') throw new Error(s.error)
    }
    if (!out) throw new Error('timed out')
    writeFileSync(join(OUT, 'assets', `${j.id}-reshoot.png`),
      Buffer.from(await (await fetch(out)).arrayBuffer()))
    spent += q.usd
    console.log(`${j.id} ok  ${out}`)
  } catch (e) { console.log(`${j.id} FAILED — ${e.message}`) }
}
console.log(`\nreshoot spend $${spent.toFixed(2)}`)
