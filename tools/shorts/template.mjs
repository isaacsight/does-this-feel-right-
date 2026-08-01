/**
 * The kernel.chat shorts template — geometry, beats, and the safe-zone check.
 *
 * Spec and sources: docs/video/SHORTS-TEMPLATE.md
 *
 * The point of this file is that safe zones stop being something you remember
 * and start being something that fails a test. The three published shorts each
 * cleared the editor and each had a defect visible only on a phone.
 */

export const CANVAS = { w: 1080, h: 1920 }

/**
 * Platform chrome reserves, in pixels, as the union of all three platforms.
 *
 * Published figures disagree — one source puts TikTok's bottom margin at 320px,
 * another at 484px. Where sources conflict on a safe zone we take the MAXIMUM:
 * over-caution costs nothing, under-caution costs the caption.
 */
export const RESERVE = { top: 130, bottom: 484, left: 60, right: 140 }

/** Promoted posts lose more: TikTok CTA ~+50px, IG "Sponsored" ~+80px. */
export const RESERVE_PROMOTED = { ...RESERVE, bottom: 534 }

export const safeBox = (r = RESERVE) => ({
  x0: r.left, x1: CANVAS.w - r.right,
  y0: r.top,  y1: CANVAS.h - r.bottom,
  get w() { return this.x1 - this.x0 }, // 880
  get h() { return this.y1 - this.y0 }, // 1306
})

/**
 * The page. Fractions of canvas height.
 *
 * captions sat at 0.70 on the published shorts, which centres type at 1344px
 * against a bottom limit of 1436px — twelve pixels of clearance, and none once
 * a caption wraps. 0.64 clears every platform with ~127px to spare.
 */
export const PAGE = {
  kicker:   { centerY: 0.11, fontSize: 34, tracking: 0.18 },
  picture:  { top: 0.18, bottom: 0.56, fullWidth: true },
  // fontSize is canvas POINTS, not pixels — 52 renders ~48px per glyph at
  // 1080 wide, which is ~21 characters per line. Size by character budget.
  captions: { centerY: 0.63, fontSize: 52, maxChars: 21, maxLines: 2,
              font: 'AvenirNextCondensed-Heavy', secondsPerCard: 2.0 },
}

/**
 * Beat structure for a 45s single-idea short.
 *
 * ~71% of viewers decide in the first few seconds; a hook/promise/payoff laid
 * down by 3–5s correlates with 15–25% more viewers reaching ten seconds.
 * Education tolerates +5–10s over entertainment and wants slower cuts — what
 * kills an explainer is a slack opening, not a long middle.
 */
export const BEATS = [
  { name: 'hook',     from: 0,  to: 3,  note: 'the claim that sounds wrong. no preamble.' },
  { name: 'promise',  from: 3,  to: 5,  note: 'name the study or the number.' },
  { name: 'body',     from: 5,  to: 38, note: 'one idea, cited on screen.' },
  { name: 'turn',     from: 38, to: 43, note: 'what it means for the viewer.' },
  { name: 'signoff',  from: 43, to: 45, note: 'the mark. no ask.' },
]

/** Comic timing is UNEVEN timing. Uniform cutting kills every joke. */
export const HOLDS = {
  snap:   [1.0, 2.0],   // the punchline
  quick:  [1.5, 2.5],   // escalating runs
  setup:  [3.0, 5.0],   // let them read the situation
  breath: [5.0, 8.0],   // after a big beat
  targetAverage: 3.0,
  max: 8.0,             // past this a still dies
}

/**
 * Check a cut list against the template. Returns issues, empty if clean.
 *
 * Takes [{ id, seconds }]. Deliberately catches the things that actually
 * shipped broken: overlong stills, a uniform rhythm, and repeated images.
 */
export function checkCuts(cuts) {
  const issues = []
  if (!cuts?.length) return ['no cuts supplied']

  const secs = cuts.map(c => c.seconds)
  const total = secs.reduce((a, b) => a + b, 0)
  const avg = total / secs.length

  for (const c of cuts) {
    if (c.seconds > HOLDS.max) issues.push(`${c.id}: ${c.seconds}s exceeds the ${HOLDS.max}s ceiling — a still dies past this`)
    if (c.seconds < 0.6) issues.push(`${c.id}: ${c.seconds}s is below the readable floor`)
  }
  if (avg > 4.5) issues.push(`average hold ${avg.toFixed(2)}s — drags; target ~${HOLDS.targetAverage}s`)

  // A flat rhythm reads as competent and kills comedy. Spread, not mean.
  const spread = Math.max(...secs) - Math.min(...secs)
  if (spread < 1.5) issues.push(`holds vary by only ${spread.toFixed(2)}s — uniform cutting kills every joke`)

  const seen = new Map()
  for (const c of cuts) {
    if (c.image && seen.has(c.image)) issues.push(`${c.id}: reuses image from ${seen.get(c.image)} — every image must differ`)
    if (c.image) seen.set(c.image, c.id)
  }
  return issues
}

/** Does an element at this vertical fraction, with this type size, stay clear? */
export function checkVertical(centerY, fontSize, { lines = 2, promoted = false } = {}) {
  const box = safeBox(promoted ? RESERVE_PROMOTED : RESERVE)
  const half = (fontSize * 1.25 * lines) / 2   // 1.25 line-height
  const top = centerY * CANVAS.h - half
  const bottom = centerY * CANVAS.h + half
  const issues = []
  if (top < box.y0) issues.push(`top ${Math.round(top)}px is inside the ${box.y0}px chrome reserve`)
  if (bottom > box.y1) issues.push(`bottom ${Math.round(bottom)}px is inside the bottom reserve (limit ${box.y1}px)`)
  return { ok: !issues.length, issues, top: Math.round(top), bottom: Math.round(bottom), limit: box.y1 }
}
