import { chromium } from 'playwright'
const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 1000 } })
const page = await ctx.newPage()
await page.goto('https://kernelchat.substack.com/archive', { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(7000)
const links = await page.locator('a[href*="/p/"]').evaluateAll(as => [...new Set(as.map(a => a.href))].slice(0, 3))
links.forEach(l => console.log(' ', l))
const hit = links.find(l => /pigeon/i.test(l))
if (hit) {
  const p2 = await ctx.newPage(); await p2.goto(hit, { waitUntil: 'domcontentloaded' })
  await p2.waitForTimeout(5000)
  const b = await p2.locator('body').innerText()
  console.log('\nLIVE:', hit, '| chars:', b.length)
  console.log('has close  :', b.includes('be glad'))
  console.log('has sources:', b.includes('Dickin Medal'))
  console.log('has link   :', b.includes('youtu.be/w9To0_UF_Ro'))
}
await ctx.close()
