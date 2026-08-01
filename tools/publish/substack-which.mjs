import { chromium } from 'playwright'
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 900 } })
const page = await ctx.newPage()
await page.goto('https://substack.com/publish/post', { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(9000)
console.log('url:', page.url())
console.log('title field:', await page.locator('[data-testid="post-title"], textarea[placeholder*="Title"], input[placeholder*="Title"]').count())
const t = (await page.locator('body').innerText().catch(()=>'')).slice(0,350).replace(/\n{2,}/g,' | ')
console.log('page:', t)
await page.screenshot({ path: 'output/publish/proof-substack.png' })
await ctx.close()
