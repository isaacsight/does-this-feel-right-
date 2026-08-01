#!/usr/bin/env node
/**
 * Open every superseded post in one window so a human can delete them.
 *
 * Deletion is not automated here on purpose: it is irreversible, and the
 * adapters in this directory have twice reported an outcome that did not match
 * what was actually live. Opening the tabs is the safe half of the job — the
 * click stays with the owner.
 *
 * Uses the same persistent profile the adapters post from, so Instagram and
 * TikTok are already signed in. YouTube Studio may ask for the channel account
 * (kernel.chat@gmail.com) since that session lives elsewhere.
 *
 * The process stays alive until interrupted; closing it closes the window.
 */
import { chromium } from 'playwright'

const TABS = [
  ['Instagram  old 02-cause-or-report', 'https://www.instagram.com/kerneldotchat/reel/DbekkqoAAaI/'],
  ['Instagram  old 03-said-kindly', 'https://www.instagram.com/kerneldotchat/reel/DbekrpLgMwu/'],
  ['TikTok     old 02-cause-or-report', 'https://www.tiktok.com/@kernel.chat/video/7668854341100440845'],
  ['TikTok     old 03-said-kindly', 'https://www.tiktok.com/@kernel.chat/video/7668854405214571790'],
  ['YouTube    EhHqTYoquhA (private)', 'https://studio.youtube.com/video/EhHqTYoquhA/edit'],
  ['YouTube    89z0MlqfM-U (private)', 'https://studio.youtube.com/video/89z0MlqfM-U/edit'],
]

const ctx = await chromium.launchPersistentContext(
  process.env.HOME + '/.config/kernel/social-browser-profile',
  { headless: false, viewport: { width: 1440, height: 900 } })

for (const [label, url] of TABS) {
  const page = await ctx.newPage()
  await page.goto(url, { waitUntil: 'domcontentloaded' }).catch(() => {})
  console.log(`  ${label}\n     ${url}`)
  await page.waitForTimeout(1200)
}
console.log('\nSix tabs open. Delete from the ... menu on each.')
console.log('Window stays open until this is stopped.')
await new Promise(() => {})
