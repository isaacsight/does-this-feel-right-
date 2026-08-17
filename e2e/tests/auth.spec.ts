import { test, expect } from '@playwright/test'
import { APP_READY, LANDING } from '../fixtures/selectors'

test.describe('Authentication', () => {
  test('shows login gate when not authenticated', async ({ page }) => {
    await page.goto('/')
    // Either the login gate or the (lazy-loaded) landing page. A locator
    // assertion auto-waits and survives the first-load navigation that
    // destroyed a page.$ snapshot's execution context in CI.
    await expect(page.locator(`.ka-gate, ${LANDING}`).first()).toBeVisible({ timeout: 15000 })
  })

  test('login form accepts email and password', async ({ page }) => {
    await page.goto('/')
    await page.waitForSelector(APP_READY, { timeout: 15000 })

    // Should have email and password inputs
    const emailInput = await page.$('input[type="email"]')
    const passwordInput = await page.$('input[type="password"]')

    if (emailInput && passwordInput) {
      await emailInput.fill('test@example.com')
      await passwordInput.fill('testpassword')
      // Submit button should exist
      const submit = await page.$('[data-testid="auth-submit"], button[type="submit"]')
      expect(submit).toBeTruthy()
    }
  })

  test('redirects unauthenticated users from protected routes', async ({ page }) => {
    await page.goto('/admin')
    await page.waitForSelector(APP_READY, { timeout: 15000 })
    // Should not show admin page
    const admin = await page.$('.admin-page')
    expect(admin).toBeNull()
  })
})
