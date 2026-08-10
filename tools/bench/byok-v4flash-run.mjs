#!/usr/bin/env node
// BYOK test: DeepSeek V4 Flash on kbot-shaped tasks.
// Usage: DEEPSEEK_API_KEY=sk-... node tools/bench/byok-v4flash-run.mjs [--model <id>] [--runs N]
//
// Preflight discovers the exact V4 Flash model id from the API (kbot's
// provider table predates V4 Flash, so ids are verified, not assumed) and
// reports the account balance so the free-grant burn is visible per run.
// Results append to tools/bench/results/byok-v4flash.jsonl — one line per
// run, so successive runs (other models, other providers) diff cleanly.

import { TASKS } from './byok-v4flash-tasks.mjs'
import { mkdirSync, appendFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const API = 'https://api.deepseek.com'
const KEY = process.env.DEEPSEEK_API_KEY
// Public-beta pricing per 1M tokens, 2026-08 (cache-miss input / output).
const PRICE = { input: 0.14, output: 0.28 }

const args = process.argv.slice(2)
const flag = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null }
const RUNS = Number(flag('--runs') ?? 1)

if (!KEY) {
  console.error(`No DEEPSEEK_API_KEY set.

To get one free (5M tokens, no credit card, 30 days):
  1. Create an account at https://platform.deepseek.com
  2. Create an API key under "API keys"
  3. export DEEPSEEK_API_KEY="sk-..." and re-run this script`)
  process.exit(1)
}

async function api(path, body) {
  const res = await fetch(API + path, {
    method: body ? 'POST' : 'GET',
    headers: { authorization: `Bearer ${KEY}`, 'content-type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(`${path} -> HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`)
  return res.json()
}

// --- Preflight -------------------------------------------------------------
const models = (await api('/models')).data.map(m => m.id)
const MODEL = flag('--model')
  ?? models.find(id => /v4.*flash|flash.*v4/i.test(id))
  ?? models.find(id => id === 'deepseek-chat')  // DeepSeek aliases the current flagship here
if (!MODEL) throw new Error(`No V4 Flash candidate among: ${models.join(', ')}`)

let balance = null
try {
  const b = await api('/user/balance')
  balance = b.balance_infos?.map(x => `${x.total_balance} ${x.currency}`).join(', ')
} catch { /* balance endpoint is informational only */ }

console.log(`model: ${MODEL}   available: [${models.join(', ')}]`)
if (balance) console.log(`balance: ${balance}`)

// --- Suite -----------------------------------------------------------------
async function chat(prompt) {
  const t0 = performance.now()
  const r = await api('/chat/completions', {
    model: MODEL,
    messages: [{ role: 'user', content: prompt }],
    temperature: 0,
  })
  return {
    text: r.choices[0].message.content ?? '',
    usage: r.usage,
    ms: Math.round(performance.now() - t0),
  }
}

const totals = { pass: 0, fail: 0, error: 0, in: 0, out: 0, ms: 0 }
const results = []

for (let run = 0; run < RUNS; run++) {
  for (const task of TASKS) {
    let row
    try {
      const r = await chat(task.prompt)
      const g = task.grade(r.text)
      row = { task: task.id, pass: g.pass, ms: r.ms, in: r.usage.prompt_tokens, out: r.usage.completion_tokens, detail: g.detail }
      totals[g.pass ? 'pass' : 'fail']++
      totals.in += r.usage.prompt_tokens; totals.out += r.usage.completion_tokens; totals.ms += r.ms
    } catch (e) {
      row = { task: task.id, pass: false, error: String(e.message).slice(0, 200) }
      totals.error++
    }
    results.push(row)
    console.log(`${row.pass ? 'PASS' : 'FAIL'}  ${task.id.padEnd(24)} ${row.ms ?? '-'}ms  ${row.detail ?? row.error ?? ''}`)
  }
}

// --- Report ----------------------------------------------------------------
const n = TASKS.length * RUNS
const cost = (totals.in * PRICE.input + totals.out * PRICE.output) / 1e6
const summary = {
  ts: new Date().toISOString(), model: MODEL, provider: 'deepseek', harness: 'raw-api',
  tasks: n, pass: totals.pass, fail: totals.fail, error: totals.error,
  passRate: +(totals.pass / n).toFixed(3),
  tokens: { in: totals.in, out: totals.out },
  estCostUSD: +cost.toFixed(5),
  medianMs: results.filter(r => r.ms).map(r => r.ms).sort((a, b) => a - b)[Math.floor(n / 2)] ?? null,
  results,
}

const outDir = join(dirname(fileURLToPath(import.meta.url)), 'results')
mkdirSync(outDir, { recursive: true })
appendFileSync(join(outDir, 'byok-v4flash.jsonl'), JSON.stringify(summary) + '\n')

console.log(`\n${totals.pass}/${n} passed  |  ~$${cost.toFixed(4)} (free-grant covers ~$8.40)  |  median ${summary.medianMs}ms`)
console.log(`appended to tools/bench/results/byok-v4flash.jsonl`)
