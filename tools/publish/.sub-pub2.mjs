import { chromium } from 'playwright'
const ID = process.argv[2]
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 1000 } })
const page = await ctx.newPage()
await page.goto(`https://kernelchat.substack.com/publish/post/${ID}`, { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(9000)
const chars = (await page.locator('div[contenteditable="true"]').first().innerText().catch(()=>'')).length
console.log('body chars:', chars)
const MIN = Number(process.argv[3] ?? 7000)  // floor matches the essay, not a fixed magic number
if (chars < MIN) { console.log(`ABORT - body ${chars} below floor ${MIN}`); await ctx.close(); process.exit(1) }
await page.getByRole('button', { name: /^Continue$/ }).click()
await page.waitForTimeout(5000)
await page.getByRole('button', { name: /Send to everyone now/ }).first().click()
await page.waitForTimeout(4000)
const n = page.getByRole('button', { name: /Publish without buttons/ })
if (await n.count()) { console.log('clearing upsell modal'); await n.first().click() }
await page.waitForTimeout(15000)
console.log('url:', page.url())
await ctx.close()
