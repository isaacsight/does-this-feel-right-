/**
 * The manifest is the single source of truth AND the state machine.
 *
 * Content (video, per-platform caption, hook) and state (posted / failed /
 * pending, with the platform's own id) live together, so a run is resumable
 * and re-running is safe. Nothing here knows how a platform works.
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'

export const PLATFORMS = ['youtube', 'tiktok', 'instagram']

export function load(path = 'output/publish/manifest.json') {
  const p = resolve(path)
  if (!existsSync(p)) throw new Error(`No manifest at ${p}`)
  const m = JSON.parse(readFileSync(p, 'utf8'))
  m._path = p
  for (const s of m.shorts) {
    s.status ||= {}
    for (const pl of PLATFORMS) {
      // normalise legacy string statuses into records
      if (typeof s.status[pl] === 'string') s.status[pl] = { state: s.status[pl] }
      s.status[pl] ||= { state: 'pending' }
    }
  }
  return m
}

export function save(m) {
  const { _path, ...clean } = m
  writeFileSync(_path, JSON.stringify(clean, null, 2))
}

/** Record an outcome and persist immediately — a crash must not lose state. */
export function mark(m, slug, platform, state, extra = {}) {
  const s = m.shorts.find(x => x.slug === slug)
  if (!s) throw new Error(`Unknown short: ${slug}`)
  s.status[platform] = { state, at: new Date().toISOString(), ...extra }
  save(m)
  return s.status[platform]
}

/** Work still to do. `posted` is never retried; `failed` is. */
export function pending(m, platforms = PLATFORMS, only = null) {
  const out = []
  for (const s of m.shorts) {
    if (only && s.slug !== only) continue
    for (const pl of platforms) {
      if (s.status[pl]?.state !== 'posted') out.push({ short: s, platform: pl })
    }
  }
  return out
}

export function caption(short, platform) {
  const text = short[platform] || short.tiktok || ''
  if (!text) throw new Error(`No ${platform} caption for ${short.slug}`)
  return text
}
