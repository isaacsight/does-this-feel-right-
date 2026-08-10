// Task suite for the BYOK V4 Flash test. Every task is deterministically
// gradable — no LLM judge, so a pass means the output actually worked.
// grade() returns { pass, detail }. Tasks that execute model output do so
// in a child process with a timeout, never in the runner's own process.

import { execFileSync } from 'node:child_process'
import { writeFileSync, mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

function runNode(code, timeoutMs = 5000) {
  const dir = mkdtempSync(join(tmpdir(), 'byok-grade-'))
  const file = join(dir, 'candidate.mjs')
  writeFileSync(file, code)
  try {
    const out = execFileSync(process.execPath, [file], {
      timeout: timeoutMs, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
    })
    return { ok: true, out: out.trim() }
  } catch (e) {
    return { ok: false, out: String(e.stdout || '') + String(e.stderr || e.message) }
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }
}

// Pull the first fenced code block out of a model reply, or the raw text.
export function extractCode(text) {
  const m = text.match(/```(?:\w+)?\n([\s\S]*?)```/)
  return (m ? m[1] : text).trim()
}

function extractJson(text) {
  const code = extractCode(text)
  const m = code.match(/[[{][\s\S]*[\]}]/)
  if (!m) return null
  try { return JSON.parse(m[0]) } catch { return null }
}

export const TASKS = [
  {
    id: 'bugfix-offbyone',
    prompt: `This JavaScript function should return the last N elements of an array, in order, but it is buggy. Fix it and reply with ONLY the corrected function in a code block.\n\nfunction lastN(arr, n) {\n  return arr.slice(arr.length - n - 1)\n}`,
    grade(reply) {
      const code = extractCode(reply)
      const r = runNode(`${code}\nconst a = lastN([1,2,3,4,5], 2)\nconst b = lastN([1,2], 5)\nconsole.log(JSON.stringify([a, b]))`)
      const pass = r.ok && r.out === JSON.stringify([[4, 5], [1, 2]])
      return { pass, detail: r.out.slice(0, 200) }
    },
  },
  {
    id: 'regex-emails',
    prompt: `Extract every email address from the text below. Reply with ONLY a JSON array of strings, sorted alphabetically, no duplicates.\n\n"Contact sandra@keancoffee.example or ops@kernel.example. CC: ops@kernel.example and the team lead (lead+films@galley.example)."`,
    grade(reply) {
      const got = extractJson(reply)
      const want = ['lead+films@galley.example', 'ops@kernel.example', 'sandra@keancoffee.example']
      return { pass: JSON.stringify(got) === JSON.stringify(want), detail: JSON.stringify(got)?.slice(0, 200) ?? 'no JSON' }
    },
  },
  {
    id: 'json-schema-adherence',
    prompt: `Convert this sentence into JSON with EXACTLY these keys: title (string), year (number), tags (array of lowercase strings). Reply with ONLY the JSON object.\n\n"America Banned Tipping. It Lost. is a 2026 short film about labor history and restaurant economics."`,
    grade(reply) {
      const j = extractJson(reply)
      const pass = !!j && typeof j.title === 'string' && j.year === 2026 &&
        Array.isArray(j.tags) && j.tags.length > 0 &&
        j.tags.every(t => typeof t === 'string' && t === t.toLowerCase()) &&
        Object.keys(j).length === 3
      return { pass, detail: JSON.stringify(j)?.slice(0, 200) ?? 'no JSON' }
    },
  },
  {
    id: 'sql-aggregate',
    prompt: `Given this SQLite schema:\n\nCREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT, runtime_s INTEGER, shipped INTEGER);\n\nWrite ONE SQLite query returning two columns: shipped (0 or 1) and avg_runtime (average runtime_s per shipped value), ordered by shipped ascending. Reply with ONLY the SQL in a code block.`,
    grade(reply) {
      const sql = extractCode(reply).replace(/;\s*$/, '')
      const harness = `
import { DatabaseSync } from 'node:sqlite'
const db = new DatabaseSync(':memory:')
db.exec("CREATE TABLE films (id INTEGER PRIMARY KEY, title TEXT, runtime_s INTEGER, shipped INTEGER)")
db.exec("INSERT INTO films VALUES (1,'a',100,1),(2,'b',200,1),(3,'c',50,0),(4,'d',150,0)")
const rows = db.prepare(${JSON.stringify(sql)}).all()
console.log(JSON.stringify(rows.map(r => Object.values(r))))`
      const r = runNode(harness)
      return { pass: r.ok && r.out === JSON.stringify([[0, 100], [1, 150]]), detail: r.out.slice(0, 200) }
    },
  },
  {
    id: 'testgen-passing',
    prompt: `Write a Node.js test script (plain asserts, no framework) for this function. It must import nothing, define the function inline, cover at least 3 cases including an edge case, and exit 0 if all pass. Reply with ONLY the script in a code block.\n\nfunction clampWords(s, max) {\n  const w = s.split(/\\s+/).filter(Boolean)\n  return w.length <= max ? s.trim() : w.slice(0, max).join(' ') + '…'\n}`,
    grade(reply) {
      const code = extractCode(reply)
      if (!code.includes('assert') && !code.includes('throw')) return { pass: false, detail: 'no assertions' }
      const r = runNode(code)
      return { pass: r.ok, detail: r.out.slice(0, 200) }
    },
  },
  {
    id: 'refactor-preserve',
    prompt: `Refactor this function to remove the duplicated branches WITHOUT changing behavior. Reply with ONLY the refactored function in a code block, keeping the name formatBytes.\n\nfunction formatBytes(n) {\n  if (n < 1024) { return n + ' B' }\n  else if (n < 1024 * 1024) { return (n / 1024).toFixed(1) + ' KB' }\n  else if (n < 1024 * 1024 * 1024) { return (n / (1024 * 1024)).toFixed(1) + ' MB' }\n  else { return (n / (1024 * 1024 * 1024)).toFixed(1) + ' GB' }\n}`,
    grade(reply) {
      const code = extractCode(reply)
      const r = runNode(`${code}\nconsole.log(JSON.stringify([formatBytes(512), formatBytes(2048), formatBytes(5*1024*1024), formatBytes(3*1024*1024*1024)]))`)
      return { pass: r.ok && r.out === JSON.stringify(['512 B', '2.0 KB', '5.0 MB', '3.0 GB']), detail: r.out.slice(0, 200) }
    },
  },
  {
    id: 'toolcall-format',
    prompt: `You have one tool available:\n{"name":"production_quote","parameters":{"type":"object","properties":{"model":{"type":"string"},"seconds":{"type":"number"},"count":{"type":"integer"}},"required":["model","seconds","count"]}}\n\nThe user says: "quote me 12 five-second clips on kling". Reply with ONLY the JSON tool call as {"name": ..., "arguments": {...}}.`,
    grade(reply) {
      const j = extractJson(reply)
      const a = j?.arguments
      const pass = j?.name === 'production_quote' && !!a &&
        String(a.model).toLowerCase().includes('kling') && a.seconds === 5 && a.count === 12
      return { pass, detail: JSON.stringify(j)?.slice(0, 200) ?? 'no JSON' }
    },
  },
  {
    id: 'commit-message',
    prompt: `Write a conventional-commit message (type(scope): subject, subject <= 72 chars, imperative mood, no trailing period) for a diff that adds retry-with-backoff to tools/publish/cadence.mjs when the YouTube API returns 503. Reply with ONLY the one-line message.`,
    grade(reply) {
      const line = reply.trim().split('\n')[0].replace(/^`|`$/g, '')
      const m = line.match(/^(feat|fix|chore|refactor|perf|build|ci)\([\w./-]+\): \S.{0,70}$/)
      const pass = !!m && !line.endsWith('.') && /retry|backoff|503/i.test(line)
      return { pass, detail: line.slice(0, 120) }
    },
  },
]
