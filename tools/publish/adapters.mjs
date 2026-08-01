/**
 * One adapter per platform. Each picks the MOST ROBUST transport that platform
 * offers — not one approach for all three. Today's evidence:
 *
 *   youtube    official API          3/3 posted
 *   tiktok     playwright            3/3 posted
 *   instagram  playwright            1/3 posted  <-- flaky, prefer Graph API
 *
 * Every adapter returns { id?, url?, note? } on success or throws. None of them
 * touch the manifest; the runner owns state.
 */

import { chromium } from 'playwright'
import { execFileSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import { resolve } from 'node:path'
import { homedir } from 'node:os'

const PROFILE = resolve(homedir(), '.config/kernel/social-browser-profile')
export const log = (...a) => console.log('   ·', ...a)

// ---------------------------------------------------------------- browser --

let _ctx = null
/** One browser for the whole run — launching per post wastes ~4s each and
 *  risks two processes fighting over the same profile directory. */
export async function ctx() {
  if (_ctx) return _ctx
  _ctx = await chromium.launchPersistentContext(PROFILE, {
    headless: false,
    viewport: { width: 1440, height: 900 },
    args: ['--disable-blink-features=AutomationControlled'],
  })
  for (const page of _ctx.pages()) {
    if (page.url() === 'about:blank') await page.close().catch(() => {})
  }
  return _ctx
}
export async function closeBrowser() {
  if (_ctx) { await _ctx.close().catch(() => {}); _ctx = null }
}

/**
 * Onboarding tours, cookie bars and "video posts are now reels" prompts all
 * swallow clicks. TikTok's react-joyride overlay reports as visible+stable
 * while intercepting pointer events, so Playwright retries forever instead of
 * failing. Dismiss politely, then remove what remains.
 */
async function clearOverlays(page) {
  // A composer is not an overlay. "Close" and "Dismiss" below match Instagram's
  // OWN X button on the create-post dialog, so running the full sweep inside the
  // composer closes the upload and raises "Discard post?", which then sits on
  // top of Next and blocks the rest of the walk. Shorts over ~55s failed
  // reliably and shorter ones passed, purely by winning a race against that
  // button rendering inside the 800ms probe.
  //
  // So: if the discard prompt is already up, answer Cancel and get out. If a
  // composer is open, only clear things that are genuinely in front of it.
  const cancel = page.getByRole('button', { name: /^cancel$/i }).first()
  if (await page.getByText(/discard post\?/i).first()
    .isVisible({ timeout: 800 }).catch(() => false)) {
    await cancel.click({ timeout: 3000 }).catch(() => {})
    await page.waitForTimeout(600)
  }
  // Detect the composer by the DIALOG, not by its header text: the header
  // changes every step (Crop -> Edit -> New reel), so matching on words meant
  // the guard held at step one and lapsed at step two, closing the post there
  // instead. The dialog is present the whole way through.
  const inComposer = await page.getByRole('dialog').first()
    .isVisible({ timeout: 800 }).catch(() => false)

  const SAFE = [/^ok$/i, /skip/i, /got it/i, /not now/i, /allow all|accept all/i]
  const DESTRUCTIVE = [/^close$/i, /dismiss/i]
  for (const name of inComposer ? SAFE : [...SAFE, ...DESTRUCTIVE]) {
    const b = page.getByRole('button', { name }).first()
    if (await b.isVisible({ timeout: 800 }).catch(() => false)) {
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

// ---------------------------------------------------------------- youtube --

export async function youtube({ short, caption, publish }) {
  if (!publish) return { note: 'dry-run' }
  const meta = resolve(`output/publish/meta-${short.slug}.json`)
  if (!existsSync(meta)) throw new Error(`missing ${meta}`)
  const out = execFileSync('.venv-youtube/bin/python',
    ['tools/youtube-upload.py', '--meta', meta, '--privacy', 'public'],
    { encoding: 'utf8', maxBuffer: 1 << 22 })
  const m = out.match(/youtu\.be\/([\w-]+)/)
  if (!m) throw new Error('no video id in uploader output')
  return { id: m[1], url: `https://youtu.be/${m[1]}` }
}

// ----------------------------------------------------------------- tiktok --

export async function tiktok({ short, caption, publish }) {
  const page = await (await ctx()).newPage()
  try {
    await page.goto('https://www.tiktok.com/tiktokstudio/upload',
      { waitUntil: 'domcontentloaded' })
    const input = page.locator('input[type=file]').first()
    await input.waitFor({ state: 'attached', timeout: 60_000 })
    await input.setInputFiles(resolve(short.file))
    log('file attached')

    const box = page.locator('div[contenteditable="true"]').first()
    await box.waitFor({ state: 'visible', timeout: 180_000 })
    await clearOverlays(page)
    await box.click({ force: true })

    // TikTok pre-fills the description with the FILENAME. On macOS Control+A
    // is "move to line start", not select-all — using it silently prepends the
    // caption and leaves the filename welded to the last hashtag.
    await page.keyboard.press('ControlOrMeta+A')
    await page.keyboard.press('Backspace')
    const left = (await box.innerText().catch(() => '')).trim()
    if (left) {
      log(`field not empty ("${left.slice(0, 30)}") — clearing again`)
      for (let i = 0; i < left.length + 5; i++) await page.keyboard.press('Backspace')
    }
    // Typed, not pasted: the editor drops fast input and only turns "#word"
    // into a tag chip on keystrokes.
    await box.type(caption, { delay: 12 })
    const got = (await box.innerText().catch(() => '')).trim()
    if (!got.startsWith(caption.slice(0, 20))) throw new Error('caption did not take')
    log('caption verified')

    await page.screenshot({ path: `output/publish/proof-tiktok-${short.slug}.png` })
    if (!publish) return { note: 'staged' }

    const post = page.getByRole('button', { name: /^post$/i }).first()
    await post.waitFor({ state: 'visible', timeout: 60_000 })
    await post.click({ force: true })
    // Confirm the composer actually closed — clicking is not proof of posting.
    await page.waitForURL(u => !u.toString().includes('/upload'), { timeout: 90_000 })
      .catch(() => {})
    await page.waitForTimeout(4000)
    return { url: 'https://www.tiktok.com/@kernel.chat' }
  } finally { await page.close().catch(() => {}) }
}

// -------------------------------------------------------------- instagram --

const IG_GRAPH_VERSION = process.env.IG_GRAPH_VERSION || 'v24.0'
const IG_GRAPH_HOST = process.env.IG_GRAPH_HOST || 'graph.instagram.com'

function graphError(label, body, status) {
  const e = body?.error
  const details = [
    status ? `HTTP ${status}` : null,
    e?.type,
    e?.code != null ? `code ${e.code}` : null,
    e?.message,
  ].filter(Boolean).join(': ')
  return new Error(`${label} failed${details ? ` (${details})` : ''}`)
}

async function graphJson(label, url, init) {
  const res = await fetch(url, init)
  const body = await res.json().catch(() => ({}))
  if (!res.ok || body?.error) throw graphError(label, body, res.status)
  return body
}

/**
 * Graph API path — preferred when the video is already public. Instagram Login
 * only supports URL ingestion; resumable local uploads belong to the separate
 * Facebook Login API (graph.facebook.com + rupload.facebook.com). Return null
 * for local files so the caller uses the browser uploader instead.
 */
async function instagramGraph({ short, caption, publish }) {
  const uid = process.env.IG_USER_ID, tok = process.env.IG_ACCESS_TOKEN
  if (!uid || !tok || !short.public_url) return null
  if (!publish) return { note: 'dry-run' }

  const graph = `https://${IG_GRAPH_HOST}/${IG_GRAPH_VERSION}`
  const createPayload = new URLSearchParams({
    media_type: 'REELS',
    caption,
    access_token: tok,
    video_url: short.public_url,
  })
  const create = await graphJson('graph create', `${graph}/${uid}/media`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: createPayload,
  })
  if (!create.id) throw new Error('graph create failed (missing container id)')

  // Meta fetches and transcodes asynchronously; publishing early 400s.
  let finished = false
  for (let i = 0; i < 60; i++) {
    const qs = new URLSearchParams({
      fields: 'status_code,status',
      access_token: tok,
    })
    const st = await graphJson('graph status', `${graph}/${create.id}?${qs}`)
    if (st.status_code === 'FINISHED') { finished = true; break }
    if (st.status_code === 'ERROR' || st.status_code === 'EXPIRED') {
      throw new Error(`graph transcode ${st.status_code.toLowerCase()}`)
    }
    await new Promise(r => setTimeout(r, 5000))
  }
  if (!finished) throw new Error('graph transcode timed out')

  const pub = await graphJson('graph publish', `${graph}/${uid}/media_publish`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ creation_id: create.id, access_token: tok }),
  })
  if (!pub.id) throw new Error('graph publish failed (missing media id)')
  return {
    id: pub.id,
    url: `https://www.instagram.com/kerneldotchat/`,
    note: 'graph-api-url',
  }
}

export async function instagram({ short, caption, publish }) {
  const viaApi = await instagramGraph({ short, caption, publish })
  if (viaApi) return viaApi

  const page = await (await ctx()).newPage()
  try {
    await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(3000)
    await clearOverlays(page)

    const login = page.getByRole('link', { name: /^log in$/i }).first()
      .or(page.locator('input[name="username"]').first())
    if (await login.isVisible({ timeout: 3000 }).catch(() => false)) {
      log('sign in to @kerneldotchat in the opened Instagram window')
      await page.waitForURL(
        url => !url.toString().includes('/accounts/login'),
        { timeout: 300_000 },
      ).catch(() => {})
      await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' })
      await page.waitForTimeout(3000)
      await clearOverlays(page)
    }

    for (const attempt of [
      () => page.locator('svg[aria-label="New post"]').first().click({ timeout: 8000 }),
      () => page.getByRole('link', { name: /^create$/i }).first().click({ timeout: 8000 }),
    ]) {
      await attempt().catch(() => {})
      const postMenuItem = page.getByText('Post', { exact: true }).first()
      if (await postMenuItem.isVisible({ timeout: 1500 }).catch(() => false)) {
        await postMenuItem.click({ force: true })
        await page.waitForTimeout(1200)
      }
      if (await page.getByText(/create new post|drag photos and videos/i).first()
        .isVisible({ timeout: 4000 }).catch(() => false)) break
    }
    if (!await page.getByText(/create new post|drag photos and videos/i).first()
      .isVisible().catch(() => false)) {
      await page.screenshot({
        path: `output/publish/debug-instagram-${short.slug}.png`,
        fullPage: true,
      }).catch(() => {})
      throw new Error(`composer never opened (${await page.title()} — ${page.url()})`)
    }
    log('composer open')

    await page.locator('input[type=file]').last().setInputFiles(resolve(short.file))
    log('file attached')
    await page.waitForTimeout(5000)
    await clearOverlays(page)

    // Crop -> edit -> share. The step count varies with media type, so walk
    // forward until Next stops appearing rather than assuming a fixed number.
    //
    // The FIRST Next is the slow one: Instagram transcodes the upload before it
    // will let you past the crop step, and that scales with the file. At a flat
    // 20s budget every short over ~55s failed while the shorter ones in the same
    // run passed — the loop broke on step one, the composer was later dismissed,
    // and the caption wait then timed out against the home feed 60s later. The
    // error pointed at the caption box, three steps downstream of the cause.
    let advanced = 0
    for (let step = 0; step < 4; step++) {
      const nextButton = page.getByRole('button', { name: /^next$/i }).first()
      const next = await nextButton.isVisible({ timeout: 1500 }).catch(() => false)
        ? nextButton
        : page.getByText('Next', { exact: true }).first()
      const budget = step === 0 ? 180_000 : 20_000
      if (!await next.isVisible({ timeout: budget }).catch(() => false)) break
      await next.click({ force: true })
      advanced++
      await page.waitForTimeout(2500)
      await clearOverlays(page)
    }
    // Zero clicks means the composer never advanced at all. Falling through
    // here is what turned a clear "crop step never became ready" into a
    // mystery timeout further down.
    if (!advanced) {
      const shot = `output/publish/debug-instagram-next-${short.slug}.png`
      await page.screenshot({ path: shot, fullPage: true }).catch(() => {})
      throw new Error(`composer never advanced past crop — still processing? (${shot})`)
    }

    const box = page.getByRole('textbox', { name: /caption/i }).first()
      .or(page.locator('div[contenteditable="true"]').first())
    // Screenshot on failure. This step times out DETERMINISTICALLY on some
    // uploads while others in the same run sail through, and without a picture
    // of the stuck composer there is nothing to debug — the error only says a
    // locator never appeared, not what the page was showing instead.
    try {
      await box.waitFor({ state: 'visible', timeout: 60_000 })
    } catch (e) {
      const shot = `output/publish/debug-instagram-caption-${short.slug}.png`
      await page.screenshot({ path: shot, fullPage: true }).catch(() => {})
      const seen = await page.locator('body').innerText().catch(() => '')
      throw new Error(`caption box never appeared (${shot}) — page said: ` +
                      seen.replace(/\s+/g, ' ').slice(0, 300))
    }
    await box.click({ force: true })
    await box.type(caption, { delay: 8 })
    log('caption written')

    await page.screenshot({ path: `output/publish/proof-instagram-${short.slug}.png` })
    if (!publish) return { note: 'staged' }

    const share = page.getByRole('button', { name: /^share$/i }).first()
    await share.waitFor({ state: 'visible', timeout: 30_000 })
    await share.click({ force: true })
    // "Your reel has been shared" is the only reliable success signal.
    await page.getByText(/reel has been shared|post shared/i)
      .first().waitFor({ timeout: 180_000 })
    return { url: 'https://www.instagram.com/kerneldotchat/reels/' }
  } finally { await page.close().catch(() => {}) }
}

export const ADAPTERS = { youtube, tiktok, instagram }
