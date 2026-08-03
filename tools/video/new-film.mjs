#!/usr/bin/env node
// Scaffold a new GALLEY film with the STANDARD layout.
//
//   node tools/video/new-film.mjs <slug> --title "The Film Title"
//
// Every prior film invented its own layout - refs in production/refs/ for one,
// public/images/REFERENCE-*.png for another, per-film generate-frames copies
// with different hardcoded paths. That divergence caused a real failure: an
// agent looked in the standard place, found nothing, and generated 100+
// unconditioned frames. The standard layout the shared tools assume:
//
//   videos/<slug>/
//     script.txt                     locked VO (gate with register-profile.py)
//     STORYBOARD.md                  one image per beat, tagged to its line
//     production/
//       act-paras.json               act -> paragraph ranges (conform-beats)
//       prompts.json                 build-prompts.py output
//       refs/castplate.png           character sheet         REQUIRED
//       refs/layout-plate.png        scenically EMPTY plate  REQUIRED
//       spend.log                    fal ledger (generate-frames.mjs)
//     audio/parts/                   narrate.mjs stems + words.json
//     public/images/frames/          <id>-final.png
//     renders/                       masters
//     deliver/shorts/                verticals + srt
//     shorts.json                    cut config (karaoke on by default)
//
// The pipeline order lives in docs/video/PRODUCTION-PLAYBOOK.md; the platform
// constraints in docs/video/PLATFORM-POLICY.md.
import { mkdirSync, writeFileSync, existsSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const argv = process.argv.slice(2)
const slug = argv[0]
const arg = (n, d) => { const i = argv.indexOf(`--${n}`); return i >= 0 && argv[i + 1] ? argv[i + 1] : d }
const title = arg('title', null)
if (!slug || !title || slug.startsWith('--')) {
  console.error('usage: new-film.mjs <slug> --title "The Film Title"')
  process.exit(1)
}
const FILM = join(REPO, 'videos', slug)
if (existsSync(FILM)) { console.error(`${FILM} already exists`); process.exit(1) }

for (const d of ['production/refs', 'audio/parts', 'public/images/frames',
                 'renders', 'deliver/shorts'])
  mkdirSync(join(FILM, d), { recursive: true })

writeFileSync(join(FILM, 'meta.json'), JSON.stringify({
  slug, title, created: new Date().toISOString().slice(0, 10),
  canvas: '1920x1080', fps: 30,
}, null, 2) + '\n')

writeFileSync(join(FILM, 'script.txt'),
  `# ${title}\n# Gate with: python3 tools/video/register-profile.py before boarding.\n`)

writeFileSync(join(FILM, 'STORYBOARD.md'),
  `# ${title} — frame book\n\nOne image per beat, tagged to the narration line it sits under.\n` +
  `Every recurring object gets its own canonical plate BEFORE the batch.\n`)

writeFileSync(join(FILM, 'production', 'act-paras.json'), JSON.stringify(
  [{ n: 1, slug: 'act-one', paras: [0, 0] }], null, 2) + '\n')

// Karaoke on by default: word timings exist for every film now, and the
// static path is only a fallback for cards that fail alignment.
writeFileSync(join(FILM, 'shorts.json'), JSON.stringify({
  master: 'renders/REPLACE-ME.mp4',
  segments: 'segments.json',
  words: 'audio/words.json',
  karaoke: true,
  out: 'deliver/shorts',
  shorts: [],
}, null, 2) + '\n')

console.log(`videos/${slug}/ scaffolded.

Next, in order (docs/video/PRODUCTION-PLAYBOOK.md has the why):
  1. script.txt          write, then register-profile.py gate
  2. production/refs/    castplate.png + layout-plate.png (EMPTY - 10.9)
  3. build-beats.py -> STORYBOARD.md -> build-prompts.py
  4. tools/video/generate-frames.mjs videos/${slug} --all
  5. narrate.mjs -> conform-beats.py -> build-composition.mjs -> render
  6. pick-spans.py (61-74s) -> cut-verticals.py (karaoke)
  7. publish through tools/publish/ - the drip owns the cadence`)
