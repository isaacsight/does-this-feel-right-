#!/usr/bin/env npx tsx
// ─────────────────────────────────────────────────────────────
//  Stereoscope Slack Bot — Socket Mode presence for the
//  Stereoscope Coffee workspace.
//  Run: npx tsx tools/stereoscope/bot.ts
//
//  Same architecture as tools/slack-bot.ts (the kernel.chat
//  presence): Socket Mode websocket, per-thread history, Claude
//  via the Supabase claude-proxy (repo rule: never call Anthropic
//  directly). Separate env vars so both bots can run side by side
//  without ever crossing workspaces:
//    STEREOSCOPE_SLACK_BOT_TOKEN   xoxb-…
//    STEREOSCOPE_SLACK_APP_TOKEN   xapp-… (Socket Mode)
// ─────────────────────────────────────────────────────────────

import * as dotenv from 'dotenv'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const here = dirname(fileURLToPath(import.meta.url))
dotenv.config({ path: resolve(here, '..', '..', '.env') })

const BOT_TOKEN = process.env.STEREOSCOPE_SLACK_BOT_TOKEN
const APP_TOKEN = process.env.STEREOSCOPE_SLACK_APP_TOKEN
const SUPABASE_URL = process.env.VITE_SUPABASE_URL || ''
const SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY || ''
const PROXY_URL = `${SUPABASE_URL}/functions/v1/claude-proxy`

if (!BOT_TOKEN) {
  console.error('[stereoscope-bot] error: STEREOSCOPE_SLACK_BOT_TOKEN is not set in .env')
  process.exit(1)
}
if (!APP_TOKEN) {
  console.error('[stereoscope-bot] error: STEREOSCOPE_SLACK_APP_TOKEN (xapp-...) is not set in .env')
  process.exit(1)
}
if (!SUPABASE_URL || !SERVICE_KEY) {
  console.error('[stereoscope-bot] error: VITE_SUPABASE_URL or SUPABASE_SERVICE_KEY is missing in .env')
  process.exit(1)
}

const PERSONALITY = `You are the Stereoscope assistant — an AI presence in the Stereoscope Coffee Company Slack workspace, run for the ops team by kernel.chat studio.

WHO YOU TALK TO: baristas, shift leads, location managers, and the ops team, across all shops.

VOICE:
- Warm, direct, practical. Coffee-shop floor language, not corporate language.
- Lead with the answer. Short paragraphs — people read Slack on their phones mid-shift.
- No emojis.
- Use Slack markdown sparingly: *bold* for emphasis, > for quoting.

HARD RULES:
- Never invent policy, recipes, prices, schedules, or numbers. If you have not been given the current handbook text, recipe card, or POS data for what is being asked, say you do not have it and point the person to their location manager or the pinned Handbook & Informational Updates tab in #stereoscope-announcements.
- Wage, labor, sales, and personnel questions are for managers and the private ops channel — decline politely in public channels.
- If something needs a decision from ops or from Isaac — scope, money, commitments — say so plainly rather than guessing.
- If you do not know, say you do not know.`

// Per-conversation history, keyed by channel:thread. Threads are the
// natural session boundary in Slack — each discussion keeps its own
// context without bleeding into others.
const MAX_TURNS = 24
const MAX_CONVERSATIONS = 200
const histories = new Map<string, { role: string; content: string }[]>()

function historyFor(key: string): { role: string; content: string }[] {
  let h = histories.get(key)
  if (h) {
    // Re-insert so Map order tracks recency for eviction
    histories.delete(key)
  } else {
    h = []
    if (histories.size >= MAX_CONVERSATIONS) {
      const oldest = histories.keys().next().value
      if (oldest !== undefined) histories.delete(oldest)
    }
  }
  histories.set(key, h)
  return h
}

async function callClaude(messages: { role: string; content: string }[], system: string): Promise<string> {
  const body = {
    mode: 'text',
    model: 'sonnet',
    system,
    max_tokens: 4096,
    messages,
  }

  const res = await fetch(PROXY_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${SERVICE_KEY}`,
      apikey: SERVICE_KEY,
    },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Claude proxy error (${res.status}): ${err}`)
  }

  const { text } = await res.json() as { text: string }
  return text
}

async function sendMessage(channel: string, text: string, threadTs?: string) {
  const res = await fetch('https://slack.com/api/chat.postMessage', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${BOT_TOKEN}`,
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: JSON.stringify({
      channel,
      text,
      unfurl_links: false,
      ...(threadTs ? { thread_ts: threadTs } : {}),
    }),
  })
  const json = (await res.json()) as { ok: boolean; error?: string }
  if (!json.ok) {
    throw new Error(`Slack chat.postMessage error: ${json.error ?? 'unknown_error'}`)
  }
}

// Socket Mode main loop with reconnection
async function connectSocketMode() {
  console.log('[stereoscope-bot] requesting websocket connection URL from Slack')
  const response = await fetch('https://slack.com/api/apps.connections.open', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${APP_TOKEN}`,
      'Content-type': 'application/json',
    },
  })

  const data = await response.json() as { ok: boolean; url?: string; error?: string }
  if (!data.ok || !data.url) {
    throw new Error(`Failed to open connection: ${data.error || 'Unknown error'}`)
  }

  const ws = new WebSocket(data.url)

  ws.onopen = () => {
    console.log('[stereoscope-bot] connected to Slack Socket Mode')
  }

  ws.onmessage = async (event) => {
    try {
      const rawData = typeof event.data === 'string' ? event.data : event.data.toString()
      const msg = JSON.parse(rawData) as {
        envelope_id?: string
        type: string
        payload?: {
          event?: {
            type: string
            text?: string
            user?: string
            channel: string
            bot_id?: string
            ts?: string
            thread_ts?: string
          }
        }
      }

      // Acknowledge receipt of the event immediately to prevent retries
      if (msg.envelope_id) {
        ws.send(JSON.stringify({ envelope_id: msg.envelope_id }))
      }

      if (msg.type === 'events_api' && msg.payload?.event) {
        const ev = msg.payload.event

        // Skip messages from bots (including self) to prevent loops
        if (ev.bot_id) return

        const channelId = ev.channel
        const text = ev.text || ''
        const user = ev.user || 'unknown'
        const isDm = channelId.startsWith('D')
        const isMention = ev.type === 'app_mention'

        // Respond if it's a DM or the bot is mentioned
        if (isDm || isMention) {
          console.log(`[stereoscope-bot] message from ${user} in ${channelId}: "${text}"`)

          const cleanText = text.replace(/<@[A-Z0-9]+>/g, '').trim()

          // In channels, always answer in a thread (rooted at the message
          // if one doesn't exist yet) so shop channels stay tidy.
          // DMs stay flat.
          const threadTs = ev.thread_ts ?? (isDm ? undefined : ev.ts)

          // Run Claude request asynchronously to keep WebSocket loop responsive
          processMessage(channelId, cleanText, threadTs)
        }
      }
    } catch (err) {
      console.error('[stereoscope-bot] error handling message:', err)
    }
  }

  ws.onclose = (event) => {
    console.log(`[stereoscope-bot] websocket closed (code ${event.code}), reconnecting in 5s`)
    scheduleReconnect()
  }

  ws.onerror = (err) => {
    console.error('[stereoscope-bot] websocket error:', err)
  }
}

// Reconnect attempts must never surface an unhandled rejection — that
// would terminate the process and take the bot offline mid-shift.
// Failed attempts retry indefinitely with a fixed delay.
function scheduleReconnect() {
  setTimeout(() => {
    connectSocketMode().catch(err => {
      console.error('[stereoscope-bot] reconnect failed, retrying:', err)
      scheduleReconnect()
    })
  }, 5000)
}

async function processMessage(channelId: string, text: string, threadTs?: string) {
  const history = historyFor(`${channelId}:${threadTs ?? 'main'}`)
  history.push({ role: 'user', content: text })
  if (history.length > MAX_TURNS) history.splice(0, history.length - MAX_TURNS)

  try {
    const responseText = await callClaude([...history], PERSONALITY)
    history.push({ role: 'assistant', content: responseText })

    console.log(`[stereoscope-bot] sending response to ${channelId}`)
    await sendMessage(channelId, responseText, threadTs)
  } catch (err) {
    console.error('[stereoscope-bot] failed to process or send message:', err)
    // Nobody on bar should be left with silence — acknowledge the failure.
    await sendMessage(
      channelId,
      'Something went wrong on my end. Isaac has the log — please try again in a minute.',
      threadTs,
    ).catch(sendErr => console.error('[stereoscope-bot] failed to send error notice:', sendErr))
  }
}

// Start bot
connectSocketMode().catch(err => {
  console.error('[stereoscope-bot] fatal error starting Slack bot:', err)
  process.exit(1)
})
