import { test, expect } from '@playwright/test'
import { LANDING } from '../fixtures/selectors'

test.describe('Dark Mode', () => {
  test('theme toggle cycles through modes', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector(LANDING, { timeout: 15000 })

    // Find theme toggle button
    const themeBtn = await page.$('[data-testid="theme-toggle"], [aria-label*="theme" i], [aria-label*="Toggle" i]')
    if (!themeBtn) return

    // Get initial theme
    const initialTheme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme') || 'light'
    )

    // Click to cycle
    await themeBtn.click()
    await page.waitForTimeout(200)

    const nextTheme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme') || 'light'
    )

    // Should have changed
    expect(nextTheme).not.toBe(initialTheme)
  })

  test('dark mode applies correct background color', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector(LANDING, { timeout: 15000 })

    // Force dark mode, then poll the computed style: body has a
    // background-color transition, and a fixed sleep lost to it on WebKit.
    await page.evaluate(() => {
      document.documentElement.setAttribute('data-theme', 'dark')
    })
    await page.waitForFunction(() => {
      const m = getComputedStyle(document.body).backgroundColor.match(/rgb\((\d+), (\d+), (\d+)\)/)
      return !!m && Number(m[1]) < 50 && Number(m[2]) < 50 && Number(m[3]) < 50
    }, undefined, { timeout: 10000 })

    const bg = await page.evaluate(() => {
      return getComputedStyle(document.body).backgroundColor
    })

    // Should be a dark color (rgb values < 50)
    const match = bg.match(/rgb\((\d+), (\d+), (\d+)\)/)
    if (match) {
      const [, r, g, b] = match.map(Number)
      expect(r).toBeLessThan(50)
      expect(g).toBeLessThan(50)
      expect(b).toBeLessThan(50)
    }
  })
})
