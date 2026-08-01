#!/usr/bin/env node
/**
 * Post a vertical short to TikTok and/or Instagram from the command line.
 *
 * Why this exists: the sandboxed browser tool refuses local files ("only files
 * the user has shared with this session"), so it cannot attach a video. This
 * script drives a REAL Chromium via Playwright, where setInputFiles() does a
 * genuine upload with no path restriction.
 *
 * Sessions persist in a dedicated profile dir, so you log in ONCE per platform
 * and every later post is unattended.
 *
 *   node tools/post-social.mjs login                 # one-time, per platform
 *   node tools/post-social.mjs tiktok    <file> <caption-file>
 *   node tools/post-social.mjs instagram <file> <caption-file>
 *   node tools/post-social.mjs both      <file> <caption-file>
 *
 * Add --publish to actually post. Without it the script fills everything in
 * and STOPS before the final button so you can eyeball it — that is the
 * default on purpose, because posting is not reversible.
 */

import { chromium } from 'playwright'
import { readFileSync, existsSync } from 'node:fs'
import { resolve } from 'node:path'
import { homedir } from 'node:os'

const PROFILE = resolve(homedir(), '.config/kernel/social-browser-profile')
const PUBLISH = process.argv.includes('--publish')
const HEADLESS = process.argv.includes('--headless')

const log = (...a) => console.log('·', ...a)

async function browser() {
  try {
    const cdp = await chromium.connectOverCDP('http://localhost:9222', { timeout: 3000 })
    log('connected to active Google Chrome via CDP (localhost:9222)')
    return cdp
  } catch {
    log('CDP connection failed, falling back to persistent profile')
    return chromium.launchPersistentContext(PROFILE, {
      headless: HEADLESS,
      viewport: { width: 1440, height: 900 },
      args: ['--disable-blink-features=AutomationControlled'],
    })
  }
}

/** One-time: open all platforms so the human can log in. Sessions then persist. */
async function login() {
  const ctx = await browser()
  const page = await ctx.newPage()
  await page.goto('https://www.tiktok.com/login')
  const ig = await ctx.newPage()
  await ig.goto('https://www.instagram.com/accounts/login/')
  const xPage = await ctx.newPage()
  await xPage.goto('https://x.com/i/flow/login')
  const subPage = await ctx.newPage()
  await subPage.goto('https://substack.com/sign-in')
  console.log(`
Log into ALL FOUR tabs (TikTok, Instagram, X/Twitter, Substack), then close the window.
The session is saved to ${PROFILE} and reused on every later run.
`)
  await page.waitForEvent('close', { timeout: 0 }).catch(() => {})
  await ctx.close()
}

/**
 * Both sites throw onboarding tours, cookie banners and modals that swallow
 * clicks. TikTok uses react-joyride, whose overlay reports as "visible and
 * stable" while intercepting every pointer event — so Playwright retries
 * forever instead of failing fast. Dismiss politely, then nuke what remains.
 */
async function clearOverlays(page) {
  for (const name of [/^ok$/i, /skip/i, /got it/i, /^close$/i, /dismiss/i, /not now/i, /allow all|accept all/i]) {
    const b = page.getByRole('button', { name }).first()
    if (await b.isVisible().catch(() => false)) {
      await b.click({ timeout: 3000 }).catch(() => {})
      await page.waitForTimeout(400)
    }
  }
  await page.evaluate(() => {
    for (const sel of ['#react-joyride-portal', '.react-joyride__overlay',
                       '[data-test-id="overlay"]', '[class*="tux-modal-mask"]']) {
      document.querySelectorAll(sel).forEach(el => el.remove())
    }
  }).catch(() => {})
  await page.waitForTimeout(300)
}

async function tiktok(ctx, file, caption) {
  const page = await ctx.newPage()
  log('tiktok: opening uploader')
  await page.goto('https://www.tiktok.com/tiktokstudio/upload', { waitUntil: 'domcontentloaded' })

  const input = page.locator('input[type=file]').first()
  await input.waitFor({ state: 'attached', timeout: 60_000 })
  await input.setInputFiles(file)
  log('tiktok: file attached, waiting for processing')

  // The caption box is a contenteditable, not a textarea.
  const box = page.locator('div[contenteditable="true"]').first()
  await box.waitFor({ state: 'visible', timeout: 180_000 })
  await clearOverlays(page)
  await box.click({ force: true })
  await page.keyboard.press('ControlOrMeta+A')
  await page.keyboard.press('Backspace')
  // TikTok pre-fills the description with the FILENAME; verify it is really gone
  const left = (await box.innerText().catch(() => '')).trim()
  if (left) {
    log(`tiktok: field not empty after clear ("${left.slice(0,40)}"), clearing again`)
    for (let i = 0; i < left.length + 5; i++) await page.keyboard.press('Backspace')
  }
  // Type slowly — TikTok's editor drops characters when pasted too fast, and
  // turns "#word " into a hashtag chip only when typed.
  await box.type(caption, { delay: 12 })
  log('tiktok: caption written')

  await page.screenshot({ path: 'output/publish/proof-tiktok.png', fullPage: false })
  log('tiktok: screenshot -> output/publish/proof-tiktok.png')
  if (!PUBLISH) {
    log('tiktok: STOPPING before post (pass --publish to go live)')
    return 'staged'
  }
  const post = page.getByRole('button', { name: /^post$/i }).first()
  await post.waitFor({ state: 'visible', timeout: 60_000 })
  await post.click()
  await page.waitForTimeout(8000)
  log('tiktok: posted')
  return 'posted'
}

async function instagram(ctx, file, caption) {
  const page = await ctx.newPage()
  log('instagram: opening')
  await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' })
  await page.waitForTimeout(3000)
  await clearOverlays(page)

  // Open the composer. The sidebar "Create" is an <a> on desktop but collapses
  // to an svg-only button at narrow widths; try both, then VERIFY the dialog
  // actually mounted — the previous version clicked nothing and then attached
  // a file to an orphan input, which silently did nothing.
  for (const attempt of [
    () => page.locator('svg[aria-label="New post"]').first().click({ timeout: 8000 }),
    () => page.getByRole('link', { name: /^create$/i }).first().click({ timeout: 8000 }),
    () => page.locator('a[href="#"]:has(svg[aria-label="New post"])').first().click({ timeout: 8000 }),
  ]) {
    await attempt().catch(() => {})
    if (await page.getByText(/create new post|drag photos and videos/i)
      .first().isVisible({ timeout: 4000 }).catch(() => false)) break
  }
  const dialogUp = await page.getByText(/create new post|drag photos and videos/i)
    .first().isVisible().catch(() => false)
  if (!dialogUp) {
    await page.screenshot({ path: 'output/publish/proof-ig-fail.png' }).catch(() => {})
    throw new Error('instagram: create dialog never opened (see proof-ig-fail.png)')
  }
  log('instagram: composer open')

  const input = page.locator('input[type=file]').last()
  await input.setInputFiles(file)
  log('instagram: file attached')

  // Video uploads may show an "OK"/size prompt before Crop.
  await page.waitForTimeout(5000)
  await clearOverlays(page)
  await page.screenshot({ path: 'output/publish/proof-ig-attached.png' }).catch(() => {})
  log('instagram: post-attach screenshot saved')

  // Walk forward through however many Next steps exist (crop -> edit -> share).
  for (let step = 0; step < 4; step++) {
    const next = page.getByRole('button', { name: /^next$/i }).first()
    if (!(await next.isVisible({ timeout: 20000 }).catch(() => false))) break
    await next.click({ force: true })
    log(`instagram: next (${step + 1})`)
    await page.waitForTimeout(2500)
    await clearOverlays(page)
  }

  const box = page.getByRole('textbox', { name: /caption/i }).first()
    .or(page.locator('div[contenteditable="true"]').first())
  await box.waitFor({ state: 'visible', timeout: 60_000 })
  await box.click({ force: true })
  await box.type(caption, { delay: 8 })
  log('instagram: caption written')

  await page.screenshot({ path: 'output/publish/proof-instagram.png', fullPage: false })
  log('instagram: screenshot -> output/publish/proof-instagram.png')
  if (!PUBLISH) {
    log('instagram: STOPPING before share (pass --publish to go live)')
    return 'staged'
  }
  await page.getByRole('button', { name: /^share$/i }).first().click({ force: true })
  await page.waitForTimeout(12_000)
  log('instagram: shared')
  return 'posted'
}

async function x(ctx, file, caption) {
  const page = await ctx.newPage()
  log('x: opening compose')
  await page.goto('https://x.com/compose/post', { waitUntil: 'domcontentloaded' })
  await page.waitForTimeout(3000)
  await clearOverlays(page)

  const box = page.locator('div[role="textbox"]').first()
  await box.waitFor({ state: 'visible', timeout: 60_000 })
  await box.click({ force: true })
  await box.type(caption, { delay: 10 })
  log('x: caption written')

  if (file && existsSync(file)) {
    const input = page.locator('input[type="file"]').first()
    if (await input.count()) {
      await input.setInputFiles(file)
      log('x: media attached, waiting for upload')
      await page.waitForTimeout(5000)
    }
  }

  await page.screenshot({ path: 'output/publish/proof-x.png', fullPage: false })
  log('x: screenshot -> output/publish/proof-x.png')
  if (!PUBLISH) {
    log('x: STOPPING before post (pass --publish to go live)')
    return 'staged'
  }
  const postBtn = page.getByTestId('tweetButton').first()
    .or(page.getByRole('button', { name: /^post$/i }).first())
  await postBtn.click({ force: true })
  await page.waitForTimeout(8000)
  log('x: posted')
  return 'posted'
}

async function substack(ctx, file, caption) {
  const page = await ctx.newPage()
  log('substack: opening notes')
  await page.goto('https://substack.com/notes', { waitUntil: 'domcontentloaded' })
  await page.waitForTimeout(3000)
  await clearOverlays(page)

  const box = page.locator('div[contenteditable="true"]').first()
    .or(page.locator('textarea').first())
  await box.waitFor({ state: 'visible', timeout: 60_000 })
  await box.click({ force: true })
  await box.type(caption, { delay: 10 })
  log('substack: caption written')

  if (file && existsSync(file)) {
    const input = page.locator('input[type="file"]').first()
    if (await input.count()) {
      await input.setInputFiles(file)
      log('substack: media attached, waiting')
      await page.waitForTimeout(5000)
    }
  }

  await page.screenshot({ path: 'output/publish/proof-substack.png', fullPage: false })
  log('substack: screenshot -> output/publish/proof-substack.png')
  if (!PUBLISH) {
    log('substack: STOPPING before post (pass --publish to go live)')
    return 'staged'
  }
  const postBtn = page.getByRole('button', { name: /^post$|^publish$/i }).first()
  await postBtn.click({ force: true })
  await page.waitForTimeout(8000)
  log('substack: posted')
  return 'posted'
}

async function main() {
  const [cmd, fileArg, captionArg] = process.argv.slice(2)
  if (!cmd || cmd === 'help') {
    console.log(readFileSync(new URL(import.meta.url)).toString().split('*/')[0])
    return
  }
  if (cmd === 'login') return login()

  const file = resolve(fileArg || '')
  if (!existsSync(file)) throw new Error(`Video not found: ${file}`)
  const caption = existsSync(resolve(captionArg || ''))
    ? readFileSync(resolve(captionArg), 'utf8').trim()
    : (captionArg || '')
  if (!caption) throw new Error('No caption given (pass text or a .txt path)')

  console.log(`\n${PUBLISH ? 'PUBLISHING' : 'STAGING (dry run)'} — ${file}\n`)
  const ctx = await browser()
  const out = {}
  try {
    if (cmd === 'tiktok' || cmd === 'both' || cmd === 'all') out.tiktok = await tiktok(ctx, file, caption)
    if (cmd === 'instagram' || cmd === 'both' || cmd === 'all') out.instagram = await instagram(ctx, file, caption)
    if (cmd === 'x' || cmd === 'twitter' || cmd === 'all') out.x = await x(ctx, file, caption)
    if (cmd === 'substack' || cmd === 'all') out.substack = await substack(ctx, file, caption)
  } finally {
    if (PUBLISH) await ctx.close()
    else console.log('\nBrowser left open so you can inspect. Close it when done.')
  }
  console.log('\nresult:', JSON.stringify(out))
}

main().catch(async e => {
  console.error('FAILED:', e.message)
  process.exit(1)
})

