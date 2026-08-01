#!/usr/bin/env node
/**
 * Ground truth for what is actually on TikTok.
 *
 * Neither the adapter nor the public profile can be trusted for this:
 *  - the adapter reported "posted" for eight uploads that did not exist
 *    (it swallowed its own verification, fixed 2026-08-01);
 *  - the public profile grid is virtualised and showed 8 posts where Studio
 *    shows 32, so a scroll-and-count there under-reports badly.
 *
 * Studio's Posts table is the record. Read the newest rows and match each one
 * against the manifest hooks. Usage: node tools/publish/tiktok-audit.mjs
 */
import { chromium } from 'playwright'
import { readFileSync } from 'node:fs'

const FP = []
for (const f of ['you-happen-to-life', 'you-watched-it-happen']) {
  const m = JSON.parse(readFileSync(`output/publish/manifest-${f}.json`, 'utf8'))
  for (const s of m.shorts) FP.push([s.slug, s.hook.slice(0, 40).replace(/\s+/g, ' ')])
}
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: false, viewport: { width: 1500, height: 1000 } })
const page = await ctx.newPage()
await page.goto('https://www.tiktok.com/tiktokstudio/content', { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(11000)

const rows = await page.$$eval('div[class*="Container"], tr', els => els
  .map(e => (e.innerText || '').replace(/\s+/g, ' '))
  .filter(t => /\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d+, \d+:\d+ [AP]M/.test(t) && t.length < 900))
const uniq = [...new Set(rows)]
console.log(`AUDIT ${uniq.length} rows read from Studio`)
for (const r of uniq.slice(0, 14)) {
  const when = r.match(/((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d+, \d+:\d+ [AP]M)/)?.[1] ?? '?'
  const hit = FP.find(([, frag]) => r.includes(frag))
  console.log(`AUDIT   ${when.padEnd(18)} ${hit ? hit[0] : '(unmatched)'}`)
}
await ctx.close()
