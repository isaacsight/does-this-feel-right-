#!/usr/bin/env node
/**
 * Verify that what the manifests CLAIM is posted actually IS — owner-side.
 *
 *   node tools/publish/verify.mjs                    all manifests, all platforms
 *   node tools/publish/verify.mjs --platform tiktok
 *   node tools/publish/verify.mjs --manifest output/publish/manifest-<film>.json
 *
 * Exists because adapters have twice reported outcomes that did not match the
 * live account: Instagram partially succeeded and reported failure (the retry
 * made a duplicate reel), and TikTok reported eight posts that never existed
 * (PLAYBOOK 10.26). The runner marks state from the adapter's word; this tool
 * is the audit that word is checked against, and it reads OWNER surfaces:
 *
 *   tiktok     Studio's Posts table and its header total — the public profile
 *              grid is virtualised and under-reported 8 where Studio showed 32.
 *   instagram  the reels grid scrolled to a stable count, each recent reel's
 *              caption matched against the manifest hook. Counting alone cannot
 *              tell a duplicate from a new post; the caption can.
 *   x          the profile timeline scrolled deep, hook-matched.
 *   youtube    the Data API via youtube-upload.py --check (read-back, not scrape).
 *
 * Matching is by the first 40 chars of each short's hook — every caption leads
 * with the hook on every platform, so presence of the fragment is presence of
 * the post, and duplicates show up as double matches.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { join } from 'node:path'
import { ctx, closeBrowser } from './adapters.mjs'

const argv = process.argv.slice(2)
const flag = n => { const i = argv.indexOf(`--${n}`); return i > -1 ? argv[i + 1] : null }

const DIR = 'output/publish'
const manifests = flag('manifest')
  ? [flag('manifest')]
  : readdirSync(DIR).filter(f => /^manifest-.*\.json$/.test(f)).map(f => join(DIR, f))
const only = flag('platform')

// Default scope: shorts posted in the last 72h — the ones a drip run just
// touched, and the ones shallow enough in every feed to actually find. --all
// audits everything, which costs a deep Instagram walk. First verify run
// flagged 17 phantom "mismatches" that were really scope errors: posts from
// older films sit below the scan depth, and look identical to missing ones.
const ALL = argv.includes('--all')
const CUTOFF = Date.now() - 72 * 3600_000

// Match on the caption THAT PLATFORM actually carries, not the hook. The hook
// opens most captions but not all — 06-what-it-is-good-at's TikTok caption
// leads "What that study is good at..." while its hook says "Every trial
// tested the child", and matching hooks scored a live post as missing.
const frag = t => (t ?? '').slice(0, 40).replace(/\s+/g, ' ')

const shorts = []
for (const path of manifests) {
  const m = JSON.parse(readFileSync(path, 'utf8'))
  for (const s of m.shorts ?? []) {
    const stamps = Object.values(s.status ?? {})
      .map(v => Date.parse(v.at)).filter(Number.isFinite)
    if (!ALL && (!stamps.length || Math.max(...stamps) < CUTOFF)) continue
    shorts.push({
      film: path.replace(/^.*manifest-|\.json$/g, ''),
      slug: s.slug,
      frags: { tiktok: frag(s.tiktok || s.hook), instagram: frag(s.instagram || s.hook),
               x: frag(s.hook) },
      claimed: Object.fromEntries(Object.entries(s.status ?? {})
        .map(([p, v]) => [p, v.state])),
      ytid: s.status?.youtube?.id ?? s.youtube_id ?? null,
    })
  }
}
console.log(`${shorts.length} short(s) in scope${ALL ? ' (--all)' : ' (posted <72h; --all for everything)'}`)

const problems = []
const report = (platform, slug, claimed, found) => {
  const ok = (claimed === 'posted') === (found >= 1) && found <= 1
  const line = `  ${platform.padEnd(10)} ${slug.padEnd(28)} claimed=${String(claimed).padEnd(8)} found=${found}`
  console.log(line + (ok ? '' : '   <-- MISMATCH'))
  if (!ok) problems.push(line.trim())
}

async function scrollText(page, url, rounds, wheel = 2600) {
  await page.goto(url, { waitUntil: 'domcontentloaded' })
  await page.waitForTimeout(8000)
  // Park the pointer over the CONTENT before wheeling. Playwright dispatches
  // wheel events at the current mouse position, which defaults to (0,0) — on
  // TikTok Studio that is the sidebar, so the posts table never scrolled and
  // everything below the fold read as missing.
  await page.mouse.move(760, 480)
  const captures = []
  for (let i = 0; i < rounds; i++) {
    captures.push((await page.locator('body').innerText().catch(() => '')).replace(/\s+/g, ' '))
    await page.mouse.wheel(0, wheel)
    await page.waitForTimeout(1400)
  }
  return captures
}

/**
 * Count DISTINCT posts matching a fragment across scroll captures.
 *
 * Raw substring counting over concatenated captures counted one live post 20
 * times — once per scroll pass it stayed visible in. Deduplicate on the
 * fragment plus the nearest timestamp after it ("Aug 1, 4:55 PM"): two real
 * copies of a post carry two timestamps, twenty sightings of one carry one.
 */
const distinct = (captures, fragment, mode = 'stamps') => {
  if (mode === 'max') {
    // For surfaces with RELATIVE timestamps (X: "40s" -> "2m" between two
    // captures), stamp-signatures split one post into several. Two REAL copies
    // sit adjacent on a profile timeline and co-appear in one capture, so the
    // per-capture maximum counts them — while twenty sightings of one post
    // across twenty captures still count once.
    let best = 0
    for (const text of captures) {
      let n = 0, i = 0
      while ((i = text.indexOf(fragment, i)) !== -1) { n++; i += fragment.length }
      best = Math.max(best, n)
    }
    return best
  }
  const sigs = new Set()
  for (const text of captures) {
    let i = 0
    while ((i = text.indexOf(fragment, i)) !== -1) {
      const after = text.slice(i, i + 600)
      const t = after.match(/(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+(?:, \d+:\d+\s*[AP]M)?/)
      sigs.add(fragment + '|' + (t ? t[0] : 'no-stamp'))
      i += fragment.length
    }
  }
  return sigs.size
}

// ------------------------------------------------------------------ youtube
if (!only || only === 'youtube') {
  console.log('\nyoutube — Data API read-back')
  const ids = shorts.filter(s => s.ytid && s.claimed.youtube === 'posted')
  if (ids.length) {
    const out = execFileSync('.venv-youtube/bin/python',
      ['tools/youtube-upload.py', '--check', ids.map(s => s.ytid).join(',')],
      { encoding: 'utf8' })
    const status = Object.fromEntries(out.trim().split('\n')
      .filter(l => l.includes(' ')).map(l => l.trim().split(/\s+/)))
    for (const s of ids)
      report('youtube', s.slug, s.claimed.youtube,
        ['public', 'unlisted'].includes(status[s.ytid]) ? 1 : 0)
  }
}

// ------------------------------------------------------------------- tiktok
if (!only || only === 'tiktok') {
  console.log('\ntiktok — Studio post list (owner-side)')
  const page = await (await ctx()).newPage()
  const caps = await scrollText(page, 'https://www.tiktok.com/tiktokstudio/content', 20, 2000)
  const total = caps.join(' ').match(/Posts (\d+)/)?.[1]
  console.log(`  Studio header total: ${total ?? 'NOT READ'}`)
  for (const s of shorts.filter(s => s.claimed.tiktok))
    report('tiktok', s.slug, s.claimed.tiktok, distinct(caps, s.frags.tiktok))
  await page.close()
}

// ---------------------------------------------------------------- instagram
if (!only || only === 'instagram') {
  console.log('\ninstagram — reel captions vs hooks')
  const page = await (await ctx()).newPage()
  await page.goto('https://www.instagram.com/kerneldotchat/reels/', { waitUntil: 'domcontentloaded' })
  await page.waitForTimeout(7000)
  const seen = new Set()
  for (let i = 0, stable = 0; i < 30 && stable < 3; i++) {
    const before = seen.size
    for (const h of await page.$$eval('a[href*="/reel/"]', as => as.map(a => a.getAttribute('href')))) seen.add(h)
    stable = seen.size === before ? stable + 1 : 0
    await page.mouse.wheel(0, 2200); await page.waitForTimeout(1500)
  }
  console.log(`  reels on profile: ${seen.size}`)
  const tally = {}
  // Visiting every reel costs ~4s each; visit the newest N covering the
  // manifests' shorts plus slack for interlopers.
  const need = shorts.filter(s => s.claimed.instagram).length + 12
  for (const h of [...seen].slice(0, need)) {
    await page.goto(`https://www.instagram.com${h}`, { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(3200)
    const b = (await page.locator('body').innerText().catch(() => '')).replace(/\s+/g, ' ')
    const hit = shorts.find(s => b.includes(s.frags.instagram))
    if (hit) tally[hit.slug] = (tally[hit.slug] || 0) + 1
  }
  for (const s of shorts.filter(s => s.claimed.instagram))
    report('instagram', s.slug, s.claimed.instagram, tally[s.slug] ?? 0)
  await page.close()
}

// ------------------------------------------------------------------------ x
if (!only || only === 'x') {
  console.log('\nx — profile timeline')
  const page = await (await ctx()).newPage()
  const caps = await scrollText(page, 'https://x.com/Kernelchatkbot', 30)
  for (const s of shorts.filter(s => s.claimed.x))
    report('x', s.slug, s.claimed.x, distinct(caps, s.frags.x, 'max'))
  await page.close()
}

await closeBrowser()
if (problems.length) {
  console.log(`\n${problems.length} MISMATCH(ES) — the manifest and the live account disagree:`)
  for (const p of problems) console.log('  ' + p)
  console.log('Fix the manifest or the account before publishing anything else.')
  process.exit(1)
}
console.log('\nAll claims verified against the live accounts.')
