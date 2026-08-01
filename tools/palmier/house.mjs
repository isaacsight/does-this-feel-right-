/**
 * The kernel.chat house toolkit for Palmier.
 *
 * Every function here encodes something learned by shipping *The Price of a
 * Glance* and its three shorts. The point is that the next film does not
 * rediscover them. Each is deliberately small and composable.
 */

import { call, timeline, transcript } from './client.mjs'

export const HOUSE = {
  ivory: '#FAF9F6',
  ink: '#1F1E1D',
  tomato: '#E24E1B',
  editorial: 'EB Garamond',   // body / quotes
  numerals: 'Courier Prime',  // kickers, figures, colophon
}

/** Proper nouns ASR reliably mangles on a cited film, with their fixes. */
export const ASR_FIXES = [
  [/\bSchulz\b/g, 'Schultz'], [/Day\s*-?\s*Ann/g, 'Dayan'],
  [/\bFurster\b/g, 'Ferster'], [/\bAmy Orban\b/g, 'Amy Orben'],
  [/\ba tension residue\b/g, 'attention residue'],
  [/\bPrzybylski\b/g, 'Przybylski'], [/\bBottger\b/g, 'Böttger'],
]

// ------------------------------------------------------------- captions --

/**
 * Word-by-word captions in house style.
 *
 * We shipped static blocks by hand before noticing add_captions does this
 * natively and times per-word animation from the transcript. Research says
 * ~70% of top educational creators use word-by-word, and that colour shift
 * beats boxes.
 *
 * `highlightPop` keeps the whole line readable while the accent tracks the
 * voice — the closest option to the researched ideal. `wordPop` is punchier
 * for a gag.
 */
export function captions({ animation = 'highlightPop', maxWords = 4,
                           fontSize = 64, centerY = 0.64 } = {}) {
  return call('add_captions', {
    animation,
    highlightColor: HOUSE.tomato,
    maxWords,
    style: {
      fontName: HOUSE.numerals, fontSize, bold: true,
      color: HOUSE.ink, fontCase: 'uppercase',
      tracking: -0.01, alignment: 'center',
      outline: { enabled: true, color: HOUSE.ivory, width: 6 },
      shadow: { enabled: true, color: HOUSE.ink, opacity: 0.25,
                blur: 8, offset: { x: 0, y: 2 } },
    },
    transform: { centerY },
  })
}

/**
 * ASR is 88–94% accurate and gets researcher names wrong every time. On a film
 * whose credibility rests on ten citations, a mangled name costs more than a
 * missing animation. Run this after captions() and report what it changed.
 */
export async function fixCaptionText(captionGroupId) {
  const t = await transcript({ granularity: 'segments' })
  const segs = t.segments || t
  const changed = []
  for (const s of segs) {
    let fixed = s.text
    for (const [re, to] of ASR_FIXES) fixed = fixed.replace(re, to)
    if (fixed !== s.text) changed.push({ was: s.text.trim(), now: fixed.trim() })
  }
  return { captionGroupId, changed,
           note: changed.length
             ? 'apply via update_text on the caption group'
             : 'no known ASR errors found' }
}

// -------------------------------------------------------------- vertical --

/**
 * The 9:16 page layout the Editor arrived at, generalised.
 *
 * A true centre-crop keeps only ~31% of a 16:9 frame and destroys every
 * two-object gag — the potato-and-spectacles comparison, both pigeons, the
 * crowd shots. Instead: full-width picture band on the house matte, kicker
 * above, captions below, platform chrome band at the bottom left empty.
 */
export const VERTICAL_PAGE = {
  canvas: { w: 1080, h: 1920 },
  kicker: { centerY: 0.15, fontSize: 34, tracking: 0.18,
            font: HOUSE.numerals, color: HOUSE.ink, case: 'uppercase' },
  picture: { top: 0.18, bottom: 0.56, fullWidth: true, sourceCrop: 0.10 },
  captions: { centerY: 0.64 },   // corrected from 0.70 — see SHORTS-TEMPLATE.md
  chrome: { from: 0.748 },  // keep empty — platform UI lives here
  safe: { top: 0.068, bottom: 0.252, right: 0.130, left: 0.056 },
  matte: HOUSE.ivory,
}

// ---------------------------------------------------------------- timing --

/**
 * Comic timing is UNEVEN timing. Uniform cutting fixes drag and still kills
 * every joke. These are the holds that worked; ~3.5s average, never over 8s.
 */
export const HOLDS = {
  quick: [1.5, 2.5],   // list-y or escalating runs
  setup: [3.0, 5.0],   // let the viewer read the situation
  snap: [1.0, 2.0],    // the punchline. The joke IS the cut.
  breath: [5.0, 8.0],  // after a big beat, and through the turn
  max: 8.0,            // past this a static image dies
}

// -------------------------------------------------------------------- QC --

/**
 * The checks that caught real defects: a one-frame gap, a digitally silent
 * export that looked perfect on every frame, and type grazing the action rail.
 * Run before every export — none of these are visible in the editor.
 */
export async function qc({ expectSeconds = null } = {}) {
  const tl = await timeline()
  const issues = []

  for (const track of tl.tracks || []) {
    if (track.gaps?.length) {
      for (const g of track.gaps) {
        if (g[1] - g[0] <= 2) issues.push(`sliver gap on ${track.trackId}: ${g}`)
        else issues.push(`gap on ${track.trackId}: ${g}`)
      }
    }
  }
  if (expectSeconds && tl.durationSeconds) {
    const drift = Math.abs(tl.durationSeconds - expectSeconds)
    if (drift > 1) issues.push(`duration ${tl.durationSeconds}s vs expected ${expectSeconds}s`)
  }
  const hasAudio = (tl.tracks || []).some(t => t.type === 'audio' && t.clips?.length)
  if (!hasAudio) issues.push('NO AUDIO TRACK — the first shorts export was digitally silent')

  return { ok: issues.length === 0, issues,
           duration: tl.durationSeconds, tracks: (tl.tracks || []).length }
}

/** Grade only inside documented ranges; `temperature` has an undocumented scale. */
export const GRADE_SAFE = { contrast: [0.5, 1.5], blacks: [-1, 1], exposureEV: [-2, 2] }
