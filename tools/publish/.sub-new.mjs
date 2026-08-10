import { chromium } from 'playwright'
// Open a fresh Substack draft and report its post id. Typing (never pasting)
// is the rule for prose; the source is already ASCII-only.
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 1000 } })
const page = await ctx.newPage()
await page.goto('https://kernelchat.substack.com/publish/post?type=newsletter',
                { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(9000)
console.log('url:', page.url())
await ctx.close()
