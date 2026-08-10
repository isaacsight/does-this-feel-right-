import { chromium } from 'playwright'
import { readFileSync } from 'node:fs'
const ID = process.argv[2]
const md = readFileSync('videos/lonely-chapter/deliver/substack-post-ascii.md', 'utf8')
const lines = md.split('\n')
const title = lines[0].replace(/^#\s*/, '').trim()
const subtitle = lines[2].replace(/^\*|\*$/g, '').trim()
const body = lines.slice(3).join('\n').replace(/\*/g, '')
  .split(/\n\s*\n/).map(s => s.trim()).filter(Boolean)

const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: true, viewport: { width: 1440, height: 1000 } })
const page = await ctx.newPage()
await page.goto(`https://kernelchat.substack.com/publish/post/${ID}`, { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(9000)
await page.locator('textarea[placeholder*="Title"], input[placeholder*="Title"]').first().fill(title)
await page.waitForTimeout(500)
await page.locator('textarea[placeholder*="subtitle" i], input[placeholder*="subtitle" i]').first().fill(subtitle)
await page.waitForTimeout(500)
const ed = page.locator('div[contenteditable="true"]').first()
await ed.click(); await page.waitForTimeout(400)
await page.keyboard.press('Meta+A'); await page.keyboard.press('Backspace')
await page.waitForTimeout(800)
for (const para of body) {
  await page.keyboard.type(para, { delay: 3 })
  await page.keyboard.press('Enter')
  await page.waitForTimeout(110)
}
await page.waitForTimeout(5000)
const txt = await ed.innerText()
console.log('paragraphs:', body.length, '| chars:', txt.length)
console.log('starts:', JSON.stringify(txt.slice(0, 70)))
console.log('ends  :', JSON.stringify(txt.trim().slice(-64)))
console.log('asterisks:', /\*/.test(txt))
await ctx.close()
