import { chromium } from 'playwright'
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 900 } })
const page = await ctx.newPage()
await page.goto('https://x.com/home', { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(7000)
console.log('url:', page.url())
console.log('composer present:', await page.locator('[data-testid="tweetTextarea_0"]').count() > 0)
const who = await page.locator('[data-testid="SideNav_AccountSwitcher_Button"]').innerText().catch(()=>'(unknown)')
console.log('account:', who.replace(/\n/g,' '))
await ctx.close()
