#!/usr/bin/env node
/**
 * Add house captions to a vertical video. One command, one job.
 *
 *   node tools/caption.mjs clip.mp4
 *   node tools/caption.mjs clip.mp4 --style pop     # punchier, for gags
 *
 * Writes <name>-captioned.mp4 next to the input.
 *
 * Word-by-word, tomato highlight, safe-zone positioned. ~70% of top explainer
 * channels use word-by-word; it turns passive watching into active reading.
 */

import { call, open as openProject, useTimeline } from './palmier/client.mjs'
import { PAGE } from './shorts/template.mjs'
import { existsSync } from 'node:fs'
import { resolve, dirname, basename, extname } from 'node:path'
import { homedir } from 'node:os'

const SCRATCH = resolve(homedir(), 'Documents/Palmier Pro/captioner.palmier')

const STYLES = {
  // Whole line visible, spoken word highlighted — the researched default.
  read: { animation: 'highlightPop', maxWords: 4 },
  // One word at a time, scaling in. Punchier; good for a joke.
  pop:  { animation: 'wordPop', maxWords: 3 },
}

const HOUSE = {
  fontName: 'Courier Prime', fontSize: 64, bold: true,
  color: '#1F1E1D', fontCase: 'uppercase', tracking: -0.01, alignment: 'center',
  outline: { enabled: true, color: '#FAF9F6', width: 6 },
  shadow: { enabled: true, color: '#1F1E1D', opacity: 0.25,
            blur: 8, offset: { x: 0, y: 2 } },
}

const file = resolve(process.argv[2] || '')
const styleName = (process.argv.includes('--style')
  ? process.argv[process.argv.indexOf('--style') + 1] : 'read')
const style = STYLES[styleName] || STYLES.read

if (!process.argv[2] || !existsSync(file)) {
  console.error('usage: node tools/caption.mjs <video.mp4> [--style read|pop]')
  process.exit(1)
}

const out = resolve(dirname(file),
  `${basename(file, extname(file))}-captioned.mp4`)

const step = m => console.log('·', m)

try {
  step('opening captioner project')
  // A dedicated scratch project keeps film projects untouched. Create once.
  await openProject(SCRATCH).catch(() =>
    call('manage_project', { action: 'create', name: 'captioner',
                             aspectRatio: '9:16', fps: 30, quality: '1080p' }))

  step('fresh timeline')
  const tl = await call('create_timeline', { name: `cap-${Date.now() % 100000}` })
  await useTimeline(tl.timelineId)

  step('importing video')
  // import_media returns mediaRef (not id) and add_clips takes `entries`
  // (not `clips`) — both mismatches silently return empty results.
  const asset = await call('import_media', { source: { path: file } })
  await call('add_clips', { entries: [{ mediaRef: asset.mediaRef, startFrame: 0 }] })

  step(`captioning — ${style.animation}`)
  const caps = await call('add_captions', {
    ...style,
    highlightColor: '#E24E1B',
    style: HOUSE,
    // 0.64, not 0.70. At 0.70 bold 64px type bottoms out at 1424px against a
    // 1436px limit — 12px, and none once a caption wraps. See SHORTS-TEMPLATE.md.
    transform: { centerY: PAGE.captions.centerY },
  })
  const group = caps.captionGroups?.[0]
  if (!group) throw new Error('no captions produced — is there speech on the track?')
  step(`${group.clipCount} caption clips`)

  step('exporting')
  const res = await call('export_project', { mode: 'video', outputPath: out })
  console.log(`\n${out}\n${res.durationSeconds}s · ${res.format}`)
  console.log('\nNote: export completes in Palmier\'s Export dialog.')
} catch (e) {
  console.error('\nFAILED:', e.message)
  if (/speech/i.test(e.message)) {
    console.error('Check the clip actually has audio:')
    console.error(`  ffmpeg -i "${file}" -af volumedetect -f null /dev/null 2>&1 | grep mean_volume`)
  }
  process.exit(1)
}
