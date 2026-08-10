/**
 * Poll submitted frame jobs and save the finished PNGs.
 *
 *   node videos/peak-end-rule/poll.mjs jobs-validate.json
 *
 * A job that stays `queued` while its batch siblings finish is a FAILURE, not
 * a slow job — read pollError immediately rather than waiting it out. Spend is
 * counted at submission, so a job that fails async still costs.
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ENGINE = 'http://127.0.0.1:5412'
const TOKEN = readFileSync(join(homedir(), '.config/kernel/galley-engine-token'), 'utf8').trim()
// fileURLToPath, NOT .pathname — the latter percent-encodes the space in
// "blog design", so writes land in a literal blog%20design/ directory.
const DIR = fileURLToPath(new URL('.', import.meta.url))
const file = process.argv[2] || 'jobs-validate.json'

const jobs = JSON.parse(readFileSync(join(DIR, file), 'utf8'))
mkdirSync(join(DIR, 'frames'), { recursive: true })

// The route is /v1/videos/jobs/ for every kind, images included — there is no
// /v1/images/jobs/. Polling the wrong path returns 404 forever and reads as a
// hung job while the frames are in fact already finished.
const get = async jobId => {
  const res = await fetch(`${ENGINE}/v1/videos/jobs/${jobId}`, {
    headers: { Authorization: `Bearer ${TOKEN}` },
  })
  return res.json()
}

const pending = new Map(jobs.map(j => [j.jobId, j]))
const done = []

for (let round = 0; pending.size && round < 60; round++) {
  for (const [jobId, meta] of [...pending]) {
    const s = await get(jobId)
    if (s.status === 'done' || s.sourceUrl || s.localUrl) {
      const url = s.imageUrl || s.audioUrl || s.videoUrl || s.localUrl || s.sourceUrl
      const buf = Buffer.from(await (await fetch(url)).arrayBuffer())
      // Extension and folder follow the asset kind, not a hardcoded .png —
      // the same poller handles frames and the voice stem.
      const ext = (url.match(/\.(png|jpe?g|webp|mp3|wav|mp4)(?:\?|$)/i)?.[1] || 'png').toLowerCase()
      const sub = /mp3|wav/.test(ext) ? 'voice' : 'frames'
      mkdirSync(join(DIR, sub), { recursive: true })
      const out = join(DIR, sub, `${meta.id}.${ext}`)
      writeFileSync(out, buf)
      console.log(`${meta.id}  done  ${Math.round(buf.length / 1024)}kb`)
      done.push({ ...meta, sourceUrl: s.sourceUrl, file: out })
      pending.delete(jobId)
    } else if (s.status === 'failed' || s.pollError) {
      console.log(`${meta.id}  FAILED  ${s.pollError || s.error || 'unknown'}`)
      pending.delete(jobId)
    }
  }
  if (pending.size) await new Promise(r => setTimeout(r, 5000))
}

if (pending.size) {
  console.log(`\nstill pending after 5 min: ${[...pending.values()].map(j => j.id).join(', ')}`)
  console.log('a job outliving its siblings is a failure — check pollError')
}
writeFileSync(join(DIR, file.replace('jobs-', 'done-')), JSON.stringify(done, null, 2))
console.log(`\n${done.length}/${jobs.length} saved to frames/`)
