/**
 * Publishing cadence guard.
 *
 * WHY THIS EXISTS. YouTube's YPP policy (clarified 2026-08, "generic and
 * repetitive") is evaluated on the CHANNEL, not the video. On 2026-08-01 this
 * channel published fourteen verticals in forty-eight hours: same visual
 * treatment, same caption system, same structure, cut mechanically from two
 * films. Every one of them was a distinct argument with cited sources, and the
 * channel's recent upload history still read as the exact shape the policy
 * names - "lots of videos really quickly that are very similar".
 *
 * The intent was right and the surface was wrong. A guard fixes the surface.
 *
 * COUNTS ACROSS MANIFESTS, NOT WITHIN ONE. The risk is per channel and there is
 * one manifest per film, so a per-manifest limit would let two films drain two
 * queues on the same day and miss the thing entirely.
 *
 * COUNTS DISTINCT SHORTS, NOT JOBS. One short going to YouTube, TikTok and
 * Instagram is one upload on each of three channels - it is one video's worth
 * of cadence, not three.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join } from 'node:path'

export const DEFAULT_PER_DAY = 2
const DIR = 'output/publish'

/** Every posted timestamp on the account, newest first, across all manifests. */
function postedTimes() {
  const out = []
  for (const f of readdirSync(DIR).filter(f => /^manifest.*\.json$/.test(f))) {
    let m
    try { m = JSON.parse(readFileSync(join(DIR, f), 'utf8')) } catch { continue }
    for (const s of m.shorts ?? []) {
      // One entry per SHORT, using its earliest post across platforms: that is
      // the day the video entered the world.
      const stamps = Object.values(s.status ?? {})
        .filter(v => v && v.state === 'posted' && v.at)
        .map(v => Date.parse(v.at))
        .filter(Number.isFinite)
      if (stamps.length) out.push({ key: `${f}:${s.slug}`, at: Math.min(...stamps) })
    }
  }
  return out.sort((a, b) => b.at - a.at)
}

/** Distinct shorts first published in the last `hours`. */
export function recent(hours = 24, now = Date.now()) {
  const cutoff = now - hours * 3600_000
  return postedTimes().filter(x => x.at >= cutoff)
}

/**
 * How many more shorts may go out right now, and when the next slot opens.
 * `limit` is per rolling 24h. Infinity disables the guard.
 */
export function budget(limit = DEFAULT_PER_DAY, now = Date.now()) {
  if (!Number.isFinite(limit)) return { allowed: Infinity, used: 0, nextAt: null }
  const used = recent(24, now)
  const allowed = Math.max(0, limit - used.length)
  // The oldest post inside the window is the one whose expiry frees a slot.
  const nextAt = allowed > 0 || !used.length
    ? null
    : new Date(Math.min(...used.map(x => x.at)) + 24 * 3600_000)
  return { allowed, used: used.length, nextAt }
}
