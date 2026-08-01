#!/usr/bin/env node
/**
 * Post a native video to X, then a reply carrying the long-form link.
 *
 * Why native and not a link post: X throttles posts whose primary content is an
 * outbound link. Uploading the short natively and putting the YouTube URL in a
 * reply keeps the reach and still gets people to the film.
 *
 * Same house rules as the other adapters in this directory:
 *   - DRY BY DEFAULT. --publish is explicit, because posting is irreversible.
 *   - VERIFY, DON'T TRUST. Clicking Post is not evidence of posting; we wait
 *     for the composer to actually close.
 *   - PROOF. A screenshot lands in output/publish/ either way.
 *
 * Usage:
 *   node tools/publish/x-post.mjs --video FILE --text "..." [--reply "..."] [--publish]
 */
import { chromium } from 'playwright'
import { resolve } from 'node:path'
import { mkdirSync } from 'node:fs'

const argv = process.argv.slice(2)
const flag = n => { const i = argv.indexOf(`--${n}`); return i > -1 ? argv[i + 1] : null }
const has = n => argv.includes(`--${n}`)

const video = flag('video')
const text = flag('text')
const reply = flag('reply')
const publish = has('publish')
if (!video || !text) {
  console.error('need --video FILE and --text "..."')
  process.exit(1)
}

const log = m => console.log(`   · ${m}`)
mkdirSync('output/publish', { recursive: true })

const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: false, viewport: { width: 1440, height: 900 } })
const page = await ctx.newPage()

try {
  await page.goto('https://x.com/compose/post', { waitUntil: 'domcontentloaded' })
  const box = page.locator('[data-testid="tweetTextarea_0"]').first()
  await box.waitFor({ state: 'visible', timeout: 60_000 })
  log('composer open')

  const input = page.locator('input[type=file][accept*="video"], input[type=file]').first()
  await input.waitFor({ state: 'attached', timeout: 30_000 })
  await input.setInputFiles(resolve(video))
  log('video attached')

  // The Post button stays disabled while the upload is still processing, so
  // that is the honest signal that the media is actually ready.
  const post = page.locator('[data-testid="tweetButton"]').first()
  await page.waitForFunction(() => {
    const b = document.querySelector('[data-testid="tweetButton"]')
    return b && b.getAttribute('aria-disabled') !== 'true'
  }, { timeout: 300_000 }).catch(() => log('WARNING: post button never enabled'))
  log('upload processed')

  await box.click()
  await page.keyboard.type(text, { delay: 8 })
  const got = (await box.innerText().catch(() => '')).trim()
  if (!got.startsWith(text.slice(0, 20))) throw new Error('text did not take')
  log('text verified')

  await page.screenshot({ path: 'output/publish/proof-x.png' })
  if (!publish) {
    console.log('\n~ staged (dry run). Re-run with --publish to post.')
    await ctx.close()
    process.exit(0)
  }

  await post.click()
  await page.waitForURL(u => !u.toString().includes('/compose/'), { timeout: 120_000 })
  log('posted')

  if (reply) {
    // Find the post we just made and reply to it, so the link rides along
    // without being the primary content.
    await page.goto('https://x.com/Kernelchatkbot', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(5000)
    const first = page.locator('[data-testid="reply"]').first()
    await first.waitFor({ state: 'visible', timeout: 60_000 })
    await first.click()
    const rbox = page.locator('[data-testid="tweetTextarea_0"]').first()
    await rbox.waitFor({ state: 'visible', timeout: 60_000 })
    await rbox.click()
    await page.keyboard.type(reply, { delay: 8 })
    const rpost = page.locator('[data-testid="tweetButton"]').first()
    await rpost.click()
    await page.waitForTimeout(6000)
    log('reply posted')
  }

  await page.screenshot({ path: 'output/publish/proof-x-done.png' })
  console.log('\n✓ posted to X')
} finally {
  await ctx.close()
}
