import { chromium } from 'playwright'
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 900 } })
const page = await ctx.newPage()
await page.goto('https://substack.com/home', { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(7000)
console.log('url:', page.url())
const signin = await page.getByText(/sign in/i).count()
console.log('sign-in prompts:', signin)
const body = (await page.locator('body').innerText().catch(()=>'')).slice(0,300).replace(/\n+/g,' | ')
console.log('page:', body)
await ctx.close()
