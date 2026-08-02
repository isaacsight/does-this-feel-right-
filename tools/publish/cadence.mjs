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
 *
 * PER PLATFORM, BECAUSE ONLY YOUTUBE HAS THIS RULE. The first version of this
 * guard throttled every platform equally, which over-applied one platform's
 * policy to three that do not share it (checked against the primary sources
 * 2026-08-02, see docs/video/PLATFORM-POLICY.md):
 *
 *   YouTube   YPP is assessed on the CHANNEL and names "generic and repetitive"
 *             as a demonetising bucket. This is the only real constraint.
 *   Instagram Meta's originality policy is about reposting OTHER people's work -
 *             stitching, reacting, minor edits. It says nothing about the volume
 *             of your own original output.
 *   TikTok    Originality is defined against copying others too. Separately,
 *             Creator Rewards needs 60s+ videos, so our shorts are outside the
 *             programme entirely and cadence is not the binding constraint.
 *   X         No originality or repetition rule in the monetization standards
 *             at all.
 *
 * Throttling all four bought nothing on three of them and cost reach.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join } from 'node:path'

/** Per-platform ceiling per rolling 24h. Infinity = unconstrained by policy. */
export const PER_DAY = {
  youtube: 2,
  instagram: Infinity,
  tiktok: Infinity,
  x: Infinity,
}
export const DEFAULT_PER_DAY = PER_DAY.youtube
const DIR = 'output/publish'

/** Posted timestamps for one platform, newest first, across all manifests. */
function postedTimes(platform) {
  const out = []
  for (const f of readdirSync(DIR).filter(f => /^manifest.*\.json$/.test(f))) {
    let m
    try { m = JSON.parse(readFileSync(join(DIR, f), 'utf8')) } catch { continue }
    for (const s of m.shorts ?? []) {
      const v = (s.status ?? {})[platform]
      if (!v || v.state !== 'posted' || !v.at) continue
      const at = Date.parse(v.at)
      if (Number.isFinite(at)) out.push({ key: `${f}:${s.slug}`, at })
    }
  }
  return out.sort((a, b) => b.at - a.at)
}

/** Distinct shorts published to `platform` in the last `hours`. */
export function recent(platform = 'youtube', hours = 24, now = Date.now()) {
  const cutoff = now - hours * 3600_000
  return postedTimes(platform).filter(x => x.at >= cutoff)
}

/**
 * How many more shorts may go out to `platform` right now, and when the next
 * slot opens. `limit` defaults to that platform's policy ceiling.
 */
export function budget(platform = 'youtube', limit = PER_DAY[platform] ?? Infinity,
                       now = Date.now()) {
  if (!Number.isFinite(limit)) return { allowed: Infinity, used: 0, nextAt: null }
  const used = recent(platform, 24, now)
  const allowed = Math.max(0, limit - used.length)
  // The oldest post inside the window is the one whose expiry frees a slot.
  const nextAt = allowed > 0 || !used.length
    ? null
    : new Date(Math.min(...used.map(x => x.at)) + 24 * 3600_000)
  return { allowed, used: used.length, nextAt }
}
