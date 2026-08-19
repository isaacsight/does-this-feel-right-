// Tests for tools/ableton-lom.ts (+ the read-back fixes in ableton.ts and the
// tier-3 OSC fallback in ableton-bridge-tools.ts).
//
// Nothing here touches Ableton Live. A fake AbletonOSC responder is bound on
// ephemeral loopback ports and the AbletonOSC client statics are pointed at
// it BEFORE the first connect. UDP 11000/11001 and TCP 9997 are never used:
// the kbot-control (TCP 9000) and bridge (9001/9997) probes are mocked out.

import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest'
import { vi } from 'vitest'
import * as dgram from 'node:dgram'
import type { AddressInfo } from 'node:net'
import { mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

// ── Mocks (hoisted) ─────────────────────────────────────────────────────

vi.mock('../integrations/ableton.js', () => ({
  tryKc: async () => undefined,
  routed: async (_kc: unknown, osc: () => Promise<unknown>) => osc(),
}))

vi.mock('../integrations/ableton-bridge.js', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../integrations/ableton-bridge.js')>()
  return {
    ...actual,
    tryAbletonBridge: async () => null,
    tryKBotRemote: async () => null,
    getAvailableBridge: async () => null,
  }
})

// Imported after the mocks so the tool modules pick up the stubs.
const oscMod = await import('../integrations/ableton-osc.js')
const { AbletonOSC, encodeOscMessage, decodeOscMessage } = oscMod
type OscArg = import('../integrations/ableton-osc.js').OscArg

const lom = await import('./ableton-lom.js')
const {
  kbotCall, kbotTry, kbotAddress, timeoutFor, parseKbotReply, toJsonArg, normalizeGrid, formatReply,
  KbotLiveError, HANDLER_TIMEOUTS, registerAbletonLomTools,
} = lom
const abletonMod = await import('./ableton.js')
const { registerAbletonTools, parseOscNotes, countMatchedNotes, replyNumber, parseCreatedTrackIndex } = abletonMod
const bridgeTools = await import('./ableton-bridge-tools.js')
const { registerAbletonBridgeTools, browserItemsFromKbotReply, insertDeviceConfirmed } = bridgeTools
const { getTool } = await import('./index.js')

// ── Fake AbletonOSC responder ───────────────────────────────────────────

type Responder = (args: OscArg[]) => OscArg[] | null | undefined

class FakeAbletonOSC {
  socket!: dgram.Socket
  port = 0
  replyPort = 0
  received: Array<{ address: string; args: OscArg[] }> = []
  responders = new Map<string, Responder>()

  async start(replyPort: number): Promise<void> {
    this.replyPort = replyPort
    this.socket = dgram.createSocket('udp4')
    this.socket.on('message', (msg: Buffer) => {
      let decoded: { address: string; args: OscArg[] }
      try { decoded = decodeOscMessage(msg) } catch { return }
      this.received.push(decoded)
      if (decoded.address === '/live/test') {
        this.reply('/live/test', [{ type: 's', value: 'ok' }])
        return
      }
      const responder = this.responders.get(decoded.address)
      if (!responder) return
      const out = responder(decoded.args)
      if (out) this.reply(decoded.address, out)
    })
    await new Promise<void>((resolve) => this.socket.bind(0, '127.0.0.1', resolve))
    this.port = (this.socket.address() as AddressInfo).port
  }

  reply(address: string, args: OscArg[]): void {
    const buf = encodeOscMessage(address, args)
    this.socket.send(buf, 0, buf.length, this.replyPort, '127.0.0.1')
  }

  /** Canned single-string JSON reply for a /live/kbot/* handler. */
  json(nameOrAddress: string, body: Record<string, unknown> | ((args: OscArg[]) => unknown)): void {
    const address = kbotAddress(nameOrAddress)
    this.responders.set(address, (args) => {
      const obj = typeof body === 'function' ? (body as (a: OscArg[]) => unknown)(args) : body
      return [{ type: 's', value: JSON.stringify(obj) }]
    })
  }

  /** Canned raw AbletonOSC reply (e.g. (track, clip, value)). */
  raw(address: string, body: (number | string)[] | ((args: OscArg[]) => (number | string)[] | null)): void {
    this.responders.set(address, (args) => {
      const vals = typeof body === 'function' ? body(args) : body
      if (!vals) return null
      return oscMod.oscArgs(...vals)
    })
  }

  silence(nameOrAddress: string): void {
    this.responders.delete(kbotAddress(nameOrAddress))
  }

  last(address: string): { address: string; args: OscArg[] } | undefined {
    return [...this.received].reverse().find((m) => m.address === address)
  }

  clear(): void {
    this.received = []
    this.responders.clear()
  }

  async stop(): Promise<void> {
    await new Promise<void>((resolve) => this.socket.close(() => resolve()))
  }
}

async function freeUdpPort(): Promise<number> {
  const s = dgram.createSocket('udp4')
  await new Promise<void>((resolve) => s.bind(0, '127.0.0.1', resolve))
  const port = (s.address() as AddressInfo).port
  await new Promise<void>((resolve) => s.close(() => resolve()))
  return port
}

const fake = new FakeAbletonOSC()

beforeAll(async () => {
  const replyPort = await freeUdpPort()
  await fake.start(replyPort)
  // Point the client at the fake BEFORE the first connect. Never 11000/11001.
  AbletonOSC.SEND_PORT = fake.port
  AbletonOSC.RECV_PORT = replyPort
  AbletonOSC.HOST = '127.0.0.1'
  AbletonOSC.TIMEOUT = 600
  registerAbletonLomTools()
  registerAbletonTools()
  registerAbletonBridgeTools()
})

afterAll(async () => {
  try { AbletonOSC.getInstance().disconnect() } catch { /* ignore */ }
  await fake.stop()
})

beforeEach(() => {
  fake.clear()
})

const vals = (args: OscArg[]) => args.map((a) => (a.type === 'b' ? '[blob]' : a.value))

// ── Pure helpers ────────────────────────────────────────────────────────

describe('pure helpers', () => {
  it('kbotAddress prefixes bare names and passes full addresses through', () => {
    expect(kbotAddress('lom/get')).toBe('/live/kbot/lom/get')
    expect(kbotAddress('/lom/get')).toBe('/lom/get')
    expect(kbotAddress('/live/kbot/ping')).toBe('/live/kbot/ping')
    expect(kbotAddress(' ping ')).toBe('/live/kbot/ping')
  })

  it('timeoutFor uses the per-handler table with a default', () => {
    expect(timeoutFor('ping')).toBe(lom.DEFAULT_TIMEOUT)
    expect(timeoutFor('browser/search')).toBe(HANDLER_TIMEOUTS['browser/search'])
    expect(timeoutFor('/live/kbot/snapshot')).toBe(HANDLER_TIMEOUTS['snapshot'])
  })

  it('parseKbotReply accepts one JSON string arg', () => {
    const r = parseKbotReply('/live/kbot/ping', [{ type: 's', value: '{"ok":true,"pong":1}' }])
    expect(r).toEqual({ ok: true, pong: 1 })
  })

  it('parseKbotReply rejects bad shapes with the address in the message', () => {
    expect(() => parseKbotReply('/live/kbot/x', [])).toThrow(/\/live\/kbot\/x: expected one JSON string/)
    expect(() => parseKbotReply('/live/kbot/x', [{ type: 'i', value: 1 }])).toThrow(/expected one JSON string/)
    expect(() => parseKbotReply('/live/kbot/x', [{ type: 's', value: 'not json' }])).toThrow(/not valid JSON/)
    expect(() => parseKbotReply('/live/kbot/x', [{ type: 's', value: '[1,2]' }])).toThrow(/not an object/)
    expect(() => parseKbotReply('/live/kbot/x', [{ type: 's', value: '{"value":1}' }])).toThrow(/no boolean "ok"/)
  })

  it('toJsonArg coerces tool params into JSON text', () => {
    expect(toJsonArg(undefined)).toBe('null')
    expect(toJsonArg(null)).toBe('null')
    expect(toJsonArg(120)).toBe('120')
    expect(toJsonArg(true)).toBe('true')
    expect(toJsonArg('120')).toBe('120')
    expect(toJsonArg('"Bass"')).toBe('"Bass"')
    expect(toJsonArg('Bass')).toBe('"Bass"')
    expect(toJsonArg('')).toBe('""')
    expect(toJsonArg('[1, 2]')).toBe('[1, 2]')
    expect(toJsonArg({ a: 1 })).toBe('{"a":1}')
  })

  it('normalizeGrid maps shorthands onto Live.Clip.GridQuantization names', () => {
    expect(normalizeGrid(undefined)).toBe('g_sixteenth')
    expect(normalizeGrid('1/16')).toBe('g_sixteenth')
    expect(normalizeGrid('1/8')).toBe('g_eighth')
    expect(normalizeGrid('bar')).toBe('g_bar')
    expect(normalizeGrid('g_quarter')).toBe('g_quarter')
    expect(normalizeGrid('none')).toBe('no_grid')
    expect(normalizeGrid('weird')).toBe('weird')
  })

  it('formatReply pretty-prints', () => {
    expect(formatReply({ ok: true })).toBe('{\n  "ok": true\n}')
  })

  it('parseOscNotes skips the (track, clip) prefix and groups by 5', () => {
    expect(parseOscNotes([0, 1])).toEqual([])
    expect(parseOscNotes([0, 1, 60, 0, 1, 100, 0, 64, 1, 0.5, 90, 1])).toEqual([
      { pitch: 60, start: 0, duration: 1, velocity: 100, mute: 0 },
      { pitch: 64, start: 1, duration: 0.5, velocity: 90, mute: 1 },
    ])
  })

  it('countMatchedNotes matches on pitch/start/duration without double counting', () => {
    const wanted = [
      { pitch: 60, start: 0, duration: 1, velocity: 100 },
      { pitch: 60, start: 0, duration: 1, velocity: 100 },
      { pitch: 67, start: 2, duration: 1, velocity: 100 },
    ]
    const actual = [
      { pitch: 60, start: 0, duration: 1, velocity: 100, mute: 0 },
      { pitch: 67, start: 2.0004, duration: 1, velocity: 100, mute: 0 },
    ]
    expect(countMatchedNotes(wanted, actual)).toBe(2)
  })

  it('browserItemsFromKbotReply maps snake_case items', () => {
    const items = browserItemsFromKbotReply({
      ok: true,
      items: [{ name: 'Saturator', uri: 'query:AudioFx#Saturator', is_loadable: true, is_device: true, path: 'Audio Effects/Saturator' }],
    })
    expect(items).toEqual([{ name: 'Saturator', uri: 'query:AudioFx#Saturator', isLoadable: true, isDevice: true, isFolder: false }])
    // tolerates a differently named array field
    expect(browserItemsFromKbotReply({ ok: true, hits: [{ name: 'X', uri: 'u' }] })[0].name).toBe('X')
    expect(browserItemsFromKbotReply({ ok: true })).toEqual([])
  })
})

// ── kbotCall over the fake transport ────────────────────────────────────

describe('kbotCall', () => {
  it('sends positional args and parses the single JSON string reply', async () => {
    fake.json('lom/get', (args) => ({ ok: true, path: vals(args)[0], prop: vals(args)[1], value: 120 }))
    const reply = await kbotCall('lom/get', 'live_set', 'tempo')
    expect(reply).toEqual({ ok: true, path: 'live_set', prop: 'tempo', value: 120 })
    const sent = fake.last('/live/kbot/lom/get')!
    expect(sent.args.map((a) => a.type)).toEqual(['s', 's'])
    expect(vals(sent.args)).toEqual(['live_set', 'tempo'])
  })

  it('auto-types ints and floats', async () => {
    fake.json('arrangement/create_clip', { ok: true, start: 4, length: 8.5 })
    await kbotCall('arrangement/create_clip', 2, 4, 8.5)
    const sent = fake.last('/live/kbot/arrangement/create_clip')!
    expect(sent.args.map((a) => a.type)).toEqual(['i', 'i', 'f'])
  })

  it('throws KbotLiveError carrying the Live-side error text on ok:false', async () => {
    fake.json('lom/set', { ok: false, error: "AttributeError: 'Song' has no attribute 'nope'" })
    await expect(kbotCall('lom/set', 'live_set', 'nope', '1')).rejects.toBeInstanceOf(KbotLiveError)
    await expect(kbotCall('lom/set', 'live_set', 'nope', '1')).rejects.toThrow(/Live rejected \/live\/kbot\/lom\/set: AttributeError: 'Song' has no attribute 'nope'/)
  })

  it('times out with an install hint when the handler is silent', async () => {
    const prev = HANDLER_TIMEOUTS['ping']
    HANDLER_TIMEOUTS['ping'] = 200
    try {
      fake.silence('ping')
      await expect(kbotCall('ping')).rejects.toThrow(/timeout.*kbot_ext\.py/s)
    } finally {
      if (prev === undefined) delete HANDLER_TIMEOUTS['ping']
      else HANDLER_TIMEOUTS['ping'] = prev
    }
  }, 10_000)

  it('rejects malformed replies with a clear shape error', async () => {
    fake.responders.set('/live/kbot/list', () => [{ type: 'i', value: 7 }])
    await expect(kbotCall('list')).rejects.toThrow(/expected one JSON string reply, got 1 arg/)
  })

  it('kbotTry never throws', async () => {
    fake.json('ping', { ok: false, error: 'boom' })
    expect(await kbotTry('ping')).toEqual({ ok: false, error: 'boom' })
    fake.json('ping', { ok: true, pong: true })
    expect(await kbotTry('ping')).toEqual({ ok: true, pong: true })
  })
})

// ── ableton_lom tool ────────────────────────────────────────────────────

describe('ableton_lom tool', () => {
  const tool = () => getTool('ableton_lom')!

  it('is registered with the documented actions', () => {
    expect(tool()).toBeDefined()
    expect(tool().description).toMatch(/0-BASED/)
    expect(tool().parameters.action.description).toMatch(/snapshot_file/)
  })

  it('get returns Live\'s reply as pretty JSON', async () => {
    const body = { ok: true, path: 'tracks 0', prop: 'name', value: 'Drums' }
    fake.json('lom/get', body)
    const out = await tool().execute({ action: 'get', path: 'tracks 0', prop: 'name' })
    expect(out).toBe(JSON.stringify(body, null, 2))
  })

  it('set JSON-encodes the value and returns the read-back', async () => {
    fake.json('lom/set', (args) => ({ ok: true, prop: vals(args)[1], value: JSON.parse(String(vals(args)[2])) }))
    const out = await tool().execute({ action: 'set', path: 'tracks 0', prop: 'name', value: 'Bass' })
    expect(JSON.parse(out)).toEqual({ ok: true, prop: 'name', value: 'Bass' })
    expect(vals(fake.last('/live/kbot/lom/set')!.args)).toEqual(['tracks 0', 'name', '"Bass"'])

    await tool().execute({ action: 'set', path: 'live_set', prop: 'tempo', value: 128 })
    expect(vals(fake.last('/live/kbot/lom/set')!.args)).toEqual(['live_set', 'tempo', '128'])
  })

  it('call defaults args to [] and forwards JSON arrays', async () => {
    fake.json('lom/call', { ok: true, result: null })
    await tool().execute({ action: 'call', path: 'tracks 0 clip_slots 0', method: 'fire' })
    expect(vals(fake.last('/live/kbot/lom/call')!.args)).toEqual(['tracks 0 clip_slots 0', 'fire', '[]'])
    await tool().execute({ action: 'call', path: 'tracks 0', method: 'create_midi_clip', args: '[0, 4]' })
    expect(vals(fake.last('/live/kbot/lom/call')!.args)).toEqual(['tracks 0', 'create_midi_clip', '[0, 4]'])
  })

  it('describe / children / exec / snapshot / snapshot_file / list / ping hit the right addresses', async () => {
    for (const name of ['lom/describe', 'lom/children', 'exec', 'snapshot', 'snapshot_file', 'list', 'ping']) {
      fake.json(name, { ok: true, handler: name })
    }
    expect(JSON.parse(await tool().execute({ action: 'describe', path: 'live_set' })).handler).toBe('lom/describe')
    expect(JSON.parse(await tool().execute({ action: 'children', path: 'live_set' })).handler).toBe('lom/children')
    const execOut = await tool().execute({ action: 'exec', code: 'song.tempo = 100' })
    expect(execOut).toMatch(/^# exec sent to Live \(\/live\/kbot\/exec\):\nsong\.tempo = 100\n/)
    expect(JSON.parse(execOut.slice(execOut.indexOf('{'))).handler).toBe('exec')
    expect(vals(fake.last('/live/kbot/exec')!.args)).toEqual(['song.tempo = 100'])
    expect(JSON.parse(await tool().execute({ action: 'snapshot' })).handler).toBe('snapshot')
    expect(fake.last('/live/kbot/snapshot')!.args).toEqual([])
    await tool().execute({ action: 'snapshot', depth: 2 })
    expect(vals(fake.last('/live/kbot/snapshot')!.args)).toEqual([2])
    await tool().execute({ action: 'snapshot_file', file: '/tmp/set.json' })
    expect(vals(fake.last('/live/kbot/snapshot_file')!.args)).toEqual(['/tmp/set.json'])
    expect(JSON.parse(await tool().execute({ action: 'list' })).handler).toBe('list')
    expect(JSON.parse(await tool().execute({ action: 'ping' })).handler).toBe('ping')
  })

  it('surfaces Live-side errors instead of claiming success', async () => {
    fake.json('lom/get', { ok: false, error: 'IndexError: list index out of range' })
    const out = await tool().execute({ action: 'get', path: 'tracks 99', prop: 'name' })
    expect(out).toMatch(/Live returned an error/)
    expect(out).toMatch(/IndexError: list index out of range/)
    expect(out).not.toMatch(/success/i)
  })

  it('validates required params and unknown actions without hitting the wire', async () => {
    expect(await tool().execute({ action: 'get', path: 'tracks 0' })).toMatch(/Missing required parameter "prop"/)
    expect(await tool().execute({ action: 'nope' })).toMatch(/Unknown action "nope"/)
    // set without a value must not silently send "null" (which would rename a track to "null")
    expect(await tool().execute({ action: 'set', path: 'tracks 0', prop: 'name' })).toMatch(/set requires "value"/)
    expect(fake.received.length).toBe(0)
  })
})

// ── ableton_browser tool ────────────────────────────────────────────────

describe('ableton_browser tool', () => {
  const tool = () => getTool('ableton_browser')!

  it('search forwards query [category] [limit] in contract order', async () => {
    fake.json('browser/search', { ok: true, items: [{ name: 'Operator', uri: 'query:Synths#Operator', is_loadable: true, is_device: true }] })
    const out = await tool().execute({ action: 'search', query: 'Operator', category: 'instruments', limit: 5 })
    expect(JSON.parse(out).items[0].name).toBe('Operator')
    expect(vals(fake.last('/live/kbot/browser/search')!.args)).toEqual(['Operator', 'instruments', 5])
    await tool().execute({ action: 'search', query: 'kick' })
    expect(vals(fake.last('/live/kbot/browser/search')!.args)).toEqual(['kick'])
  })

  it('load builds the target from track when target is omitted', async () => {
    fake.json('browser/load', { ok: true, devices: ['Operator'] })
    await tool().execute({ action: 'load', item: 'query:Synths#Operator', track: 2 })
    expect(vals(fake.last('/live/kbot/browser/load')!.args)).toEqual(['query:Synths#Operator', 'track:2'])
    await tool().execute({ action: 'load', item: 'kick.wav', target: 'pad:0:36' })
    expect(vals(fake.last('/live/kbot/browser/load')!.args)).toEqual(['kick.wav', 'pad:0:36'])
    await tool().execute({ action: 'load', item: 'x' })
    expect(vals(fake.last('/live/kbot/browser/load')!.args)).toEqual(['x', 'selected'])
  })

  it('presets / load_preset / insert_device use 0-based indexes and typed preset', async () => {
    fake.json('device/presets', { ok: true, presets: ['Init', 'Warm Pad'] })
    fake.json('device/load_preset', { ok: true, preset: 'Warm Pad' })
    fake.json('track/insert_device', { ok: true, devices: ['EQ Eight'] })
    await tool().execute({ action: 'presets', track: 1, device: 0 })
    expect(vals(fake.last('/live/kbot/device/presets')!.args)).toEqual([1, 0])
    await tool().execute({ action: 'load_preset', track: 1, device: 0, preset: '3' })
    expect(fake.last('/live/kbot/device/load_preset')!.args.map((a) => a.type)).toEqual(['i', 'i', 'i'])
    await tool().execute({ action: 'load_preset', track: 1, device: 0, preset: 'Warm Pad' })
    expect(vals(fake.last('/live/kbot/device/load_preset')!.args)).toEqual([1, 0, 'Warm Pad'])
    await tool().execute({ action: 'insert_device', track: 0, name: 'EQ Eight', position: 0 })
    expect(vals(fake.last('/live/kbot/track/insert_device')!.args)).toEqual([0, 'EQ Eight', 0])
    await tool().execute({ action: 'insert_device', track: 0, name: 'EQ Eight' })
    expect(vals(fake.last('/live/kbot/track/insert_device')!.args)).toEqual([0, 'EQ Eight'])
  })

  it('preview / stop_preview', async () => {
    fake.json('browser/preview', { ok: true })
    fake.json('browser/stop_preview', { ok: true })
    await tool().execute({ action: 'preview', item: 'query:Samples#kick' })
    expect(vals(fake.last('/live/kbot/browser/preview')!.args)).toEqual(['query:Samples#kick'])
    await tool().execute({ action: 'stop_preview' })
    expect(fake.last('/live/kbot/browser/stop_preview')!.args).toEqual([])
  })
})

// ── ableton_structure tool ──────────────────────────────────────────────

describe('ableton_structure tool', () => {
  const tool = () => getTool('ableton_structure')!

  it('create_track: kind [index] [name]', async () => {
    fake.json('track/create', (args) => ({ ok: true, index: 3, name: vals(args)[2] ?? 'MIDI' }))
    const out = await tool().execute({ action: 'create_track', kind: 'midi', name: 'Drums' })
    expect(JSON.parse(out)).toEqual({ ok: true, index: 3, name: 'Drums' })
    expect(vals(fake.last('/live/kbot/track/create')!.args)).toEqual(['midi', -1, 'Drums'])
    await tool().execute({ action: 'create_track', kind: 'audio', index: 1 })
    expect(vals(fake.last('/live/kbot/track/create')!.args)).toEqual(['audio', 1])
    await tool().execute({ action: 'create_track' })
    expect(vals(fake.last('/live/kbot/track/create')!.args)).toEqual(['midi'])
    expect(await tool().execute({ action: 'create_track', kind: 'group' })).toMatch(/kind must be/)
  })

  it('track / device ops', async () => {
    for (const n of ['track/delete', 'track/duplicate', 'device/delete', 'device/move', 'device/set_active']) fake.json(n, { ok: true, h: n })
    await tool().execute({ action: 'delete_track', track: 2 })
    expect(vals(fake.last('/live/kbot/track/delete')!.args)).toEqual([2])
    await tool().execute({ action: 'duplicate_track', track: 2 })
    expect(vals(fake.last('/live/kbot/track/duplicate')!.args)).toEqual([2])
    await tool().execute({ action: 'delete_device', track: 0, device: 1 })
    expect(vals(fake.last('/live/kbot/device/delete')!.args)).toEqual([0, 1])
    await tool().execute({ action: 'move_device', track: 0, device: 1, index: 0 })
    expect(vals(fake.last('/live/kbot/device/move')!.args)).toEqual([0, 1, 0])
    await tool().execute({ action: 'set_device_active', track: 0, device: 1, active: false })
    expect(vals(fake.last('/live/kbot/device/set_active')!.args)).toEqual([0, 1, 0])
    await tool().execute({ action: 'set_device_active', track: 0, device: 1 })
    expect(vals(fake.last('/live/kbot/device/set_active')!.args)).toEqual([0, 1, 1])
  })

  it('rack ops and drum pads', async () => {
    for (const n of ['rack/insert_chain', 'rack/add_macro', 'rack/macros', 'drum/build_pad']) fake.json(n, { ok: true, h: n })
    await tool().execute({ action: 'insert_chain', path: 'tracks 0 devices 0', name: 'Kick' })
    expect(vals(fake.last('/live/kbot/rack/insert_chain')!.args)).toEqual(['tracks 0 devices 0', 'Kick'])
    await tool().execute({ action: 'add_macro', path: 'tracks 0 devices 0' })
    expect(vals(fake.last('/live/kbot/rack/add_macro')!.args)).toEqual(['tracks 0 devices 0'])
    await tool().execute({ action: 'macros', path: 'tracks 0 devices 0' })
    expect(vals(fake.last('/live/kbot/rack/macros')!.args)).toEqual(['tracks 0 devices 0', 'get'])
    await tool().execute({ action: 'macros', path: 'tracks 0 devices 0', value: '{"0": 0.5}' })
    expect(vals(fake.last('/live/kbot/rack/macros')!.args)).toEqual(['tracks 0 devices 0', 'set', '{"0": 0.5}'])
    await tool().execute({ action: 'build_pad', path: 'tracks 0 devices 0', note: 36, sample: '/tmp/kick.wav', name: 'Kick' })
    expect(vals(fake.last('/live/kbot/drum/build_pad')!.args)).toEqual(['tracks 0 devices 0', 36, '/tmp/kick.wav', 'Kick'])
  })

  it('clip notes / quantize / automation', async () => {
    for (const n of ['clip/notes', 'clip/quantize', 'clip/automation']) fake.json(n, { ok: true, h: n })
    await tool().execute({ action: 'clip_notes', track: 0, slot: 1 })
    expect(vals(fake.last('/live/kbot/clip/notes')!.args)).toEqual(['get', 0, 1])
    const notes = '[{"pitch":60,"start_time":0,"duration":1,"velocity":100}]'
    await tool().execute({ action: 'clip_notes', op: 'set', track: 0, slot: 1, value: notes })
    expect(vals(fake.last('/live/kbot/clip/notes')!.args)).toEqual(['set', 0, 1, notes])
    expect(await tool().execute({ action: 'clip_notes', op: 'add', track: 0, slot: 1 })).toMatch(/requires "value"/)
    await tool().execute({ action: 'clip_notes', op: 'remove', track: 0, slot: 1 })
    expect(vals(fake.last('/live/kbot/clip/notes')!.args)).toEqual(['remove', 0, 1])
    await tool().execute({ action: 'quantize', track: 0, slot: 1, grid: '1/8', amount: 0.5 })
    expect(vals(fake.last('/live/kbot/clip/quantize')!.args)).toEqual([0, 1, 'g_eighth', 0.5])
    await tool().execute({ action: 'quantize', track: 0, slot: 1 })
    expect(vals(fake.last('/live/kbot/clip/quantize')!.args)).toEqual([0, 1, 'g_sixteenth', 1])
    await tool().execute({ action: 'automation', path: 'tracks 0 clip_slots 0 clip', param_path: 'tracks 0 devices 0 parameters 1', value: '[[0,1,0.2],[4,1,0.8]]' })
    expect(vals(fake.last('/live/kbot/clip/automation')!.args)).toEqual(['tracks 0 clip_slots 0 clip', 'tracks 0 devices 0 parameters 1', '[[0,1,0.2],[4,1,0.8]]'])
  })

  it('arrangement / undo / data / dialogs / messages', async () => {
    for (const n of ['arrangement/create_clip', 'arrangement/dup_from_session', 'arrangement/clips', 'song/undo_group', 'song/data', 'app/dialog', 'app/message']) fake.json(n, { ok: true, h: n })
    await tool().execute({ action: 'arr_create_clip', track: 0, start: 8, length: 16 })
    expect(vals(fake.last('/live/kbot/arrangement/create_clip')!.args)).toEqual([0, 8, 16])
    expect(await tool().execute({ action: 'arr_create_clip', track: 0 })).toMatch(/requires "length"/)
    await tool().execute({ action: 'arr_dup_from_session', track: 0, slot: 2, time: 32 })
    expect(vals(fake.last('/live/kbot/arrangement/dup_from_session')!.args)).toEqual([0, 2, 32])
    await tool().execute({ action: 'arr_clips', track: 0 })
    expect(vals(fake.last('/live/kbot/arrangement/clips')!.args)).toEqual([0])
    await tool().execute({ action: 'undo_begin' })
    expect(vals(fake.last('/live/kbot/song/undo_group')!.args)).toEqual(['begin'])
    await tool().execute({ action: 'undo_end' })
    expect(vals(fake.last('/live/kbot/song/undo_group')!.args)).toEqual(['end'])
    await tool().execute({ action: 'data_get', key: 'kbot.session' })
    expect(vals(fake.last('/live/kbot/song/data')!.args)).toEqual(['get', 'kbot.session'])
    await tool().execute({ action: 'data_set', key: 'kbot.session', value: '{"v":1}' })
    expect(vals(fake.last('/live/kbot/song/data')!.args)).toEqual(['set', 'kbot.session', '{"v":1}'])
    await tool().execute({ action: 'dialog_press', index: 1 })
    expect(vals(fake.last('/live/kbot/app/dialog')!.args)).toEqual(['press', 1])
    await tool().execute({ action: 'message', text: 'hello from kbot' })
    expect(vals(fake.last('/live/kbot/app/message')!.args)).toEqual(['hello from kbot'])
  })

  it('accepts handler-address aliases for actions (docs spelling) and maps notes_* onto clip_notes ops', async () => {
    for (const n of ['track/create', 'track/delete', 'device/set_active', 'rack/macros', 'clip/notes', 'clip/quantize', 'app/message', 'track/insert_device']) fake.json(n, { ok: true, h: n })
    await tool().execute({ action: 'track_create', kind: 'audio' })
    expect(vals(fake.last('/live/kbot/track/create')!.args)).toEqual(['audio'])
    await tool().execute({ action: 'device_set_active', track: 0, device: 1, active: false })
    expect(vals(fake.last('/live/kbot/device/set_active')!.args)).toEqual([0, 1, 0])
    await tool().execute({ action: 'rack_macros', path: 'tracks 0 devices 0' })
    expect(vals(fake.last('/live/kbot/rack/macros')!.args)).toEqual(['tracks 0 devices 0', 'get'])
    await tool().execute({ action: 'notes_get', track: 0, slot: 1 })
    expect(vals(fake.last('/live/kbot/clip/notes')!.args)).toEqual(['get', 0, 1])
    await tool().execute({ action: 'notes_set', path: 'tracks 0 clip_slots 0 clip', value: '[{"pitch":42,"start_time":0,"duration":0.25,"velocity":90}]' })
    expect(vals(fake.last('/live/kbot/clip/notes')!.args)).toEqual(['set', 'tracks 0 clip_slots 0 clip', '[{"pitch":42,"start_time":0,"duration":0.25,"velocity":90}]'])
    await tool().execute({ action: 'notes_remove', path: 'tracks 0 arrangement_clips 0' })
    expect(vals(fake.last('/live/kbot/clip/notes')!.args)).toEqual(['remove', 'tracks 0 arrangement_clips 0'])
    await tool().execute({ action: 'clip_quantize', track: 0, slot: 0, grid: 'bar' })
    expect(vals(fake.last('/live/kbot/clip/quantize')!.args)).toEqual([0, 0, 'g_bar', 1])
    await tool().execute({ action: 'app_message', text: 'hi' })
    expect(vals(fake.last('/live/kbot/app/message')!.args)).toEqual(['hi'])
    await tool().execute({ action: 'track_insert_device', track: 2, name: 'Saturator', position: 1 })
    expect(vals(fake.last('/live/kbot/track/insert_device')!.args)).toEqual([2, 'Saturator', 1])
    await tool().execute({ action: 'insert_device', track: 2, name: 'Saturator' })
    expect(vals(fake.last('/live/kbot/track/insert_device')!.args)).toEqual([2, 'Saturator'])
    // delete_track kind=return -> "return:N"
    await tool().execute({ action: 'delete_track', track: 1, kind: 'return' })
    expect(vals(fake.last('/live/kbot/track/delete')!.args)).toEqual(['return:1'])
    // clip_notes needs a locator
    expect(await tool().execute({ action: 'clip_notes' })).toMatch(/needs either "track" \+ "slot" or a clip "path"/)
  })

  it('renders Live errors verbatim', async () => {
    fake.json('track/delete', { ok: false, error: 'RuntimeError: cannot delete the last track' })
    const out = await tool().execute({ action: 'delete_track', track: 0 })
    expect(out).toMatch(/Live returned an error/)
    expect(out).toMatch(/cannot delete the last track/)
  })
})

// ── ableton_clip create + ableton_midi write read-back gating ────────────

describe('ableton_clip create read-back', () => {
  const tool = () => getTool('ableton_clip')!

  it('reports NOT confirmed when has_clip reads back false', async () => {
    fake.raw('/live/clip_slot/get/has_clip', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 0])
    const out = await tool().execute({ action: 'create', track: 1, clip: 1, length: 8, name: 'Test' })
    expect(out).toMatch(/NOT confirmed/)
    expect(out).toMatch(/has_clip = false/)
    expect(out).not.toMatch(/^Created/)
    // the create was still sent with 0-based indexes
    expect(vals(fake.last('/live/clip_slot/create_clip')!.args)).toEqual([0, 0, 8])
  })

  it('reports confirmed with name/length when has_clip reads back true', async () => {
    fake.raw('/live/clip_slot/get/has_clip', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 1])
    fake.raw('/live/clip/get/name', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 'Test'])
    fake.raw('/live/clip/get/length', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 8])
    const out = await tool().execute({ action: 'create', track: 2, clip: 3, length: 8, name: 'Test' })
    expect(out).toMatch(/^Created clip/)
    expect(out).toMatch(/Read-back confirmed: slot 3 on track 2 has a clip \(name "Test", length 8 beats\)/)
  })

  it('says so explicitly when the read-back itself fails', async () => {
    // no has_clip responder -> query times out
    const out = await tool().execute({ action: 'create', track: 1, clip: 1, length: 4 })
    expect(out).toMatch(/Read-back FAILED/)
    expect(out).toMatch(/Clip state unknown/)
  }, 10_000)
})

describe('ableton_midi write read-back', () => {
  const tool = () => getTool('ableton_midi')!

  it('confirms when every written note reads back', async () => {
    fake.raw('/live/clip/get/notes', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 60, 0, 1, 100, 0, 64, 1, 1, 100, 0])
    const out = await tool().execute({ action: 'write', track: 1, clip: 1, notes: '[{"pitch":60,"start":0,"duration":1,"velocity":100},{"pitch":64,"start":1,"duration":1,"velocity":100}]' })
    expect(out).toMatch(/^Wrote \*\*2 notes\*\*/)
    expect(out).toMatch(/Read-back confirmed: all 2 notes present/)
    expect(fake.received.filter((m) => m.address === '/live/clip/add/notes').length).toBe(2)
  })

  it('reports NOT confirmed when the clip reads back fewer notes', async () => {
    fake.raw('/live/clip/get/notes', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 60, 0, 1, 100, 0])
    const out = await tool().execute({ action: 'write', track: 1, clip: 1, notes: 'C4 E4' })
    expect(out).toMatch(/^Sent \*\*2 notes\*\*/)
    expect(out).toMatch(/NOT confirmed: read-back found 1 of 2 written notes/)
  })

  it('read uses the (track, clip, ...) offset', async () => {
    fake.raw('/live/clip/get/notes', (args) => [Number(vals(args)[0]), Number(vals(args)[1]), 62, 0.5, 0.25, 90, 0])
    const out = await tool().execute({ action: 'read', track: 1, clip: 1 })
    expect(out).toMatch(/\| 62 \| D4 \| 0\.50 \| 0\.25 \| 90 \|/)
  })
})

// ── ableton_create_track / audio_analysis rerouted addresses ─────────────

describe('ableton.ts dead-address fixes', () => {
  it('ableton_create_track uses /live/kbot/track/create and reports the read-back', async () => {
    fake.json('track/create', (args) => ({ ok: true, index: 4, name: vals(args)[2] ?? 'MIDI', kind: vals(args)[0] }))
    const out = await getTool('ableton_create_track')!.execute({ type: 'midi', name: 'Lead' })
    expect(vals(fake.last('/live/kbot/track/create')!.args)).toEqual(['midi', -1, 'Lead'])
    expect(out).toMatch(/Created midi track \*\*Lead\*\* \(track 5\)/)
    expect(out).toMatch(/kbot handler read-back/)
    expect(fake.received.some((m) => m.address.startsWith('/live/kbot/create_'))).toBe(false)
  })

  it('ableton_create_track reads a return-track reply as a return, not as track index "count"', async () => {
    fake.json('track/create', { ok: true, kind: 'return', index: 'return:2', name: 'C-Return', count: 3 })
    const out = await getTool('ableton_create_track')!.execute({ type: 'return', instrument: 'Operator' })
    expect(vals(fake.last('/live/kbot/track/create')!.args)).toEqual(['return'])
    expect(out).toMatch(/Created return track \*\*return track C \(return index 2\)\*\*/)
    expect(out).toMatch(/instrument "Operator" NOT loaded/)
    expect(out).not.toMatch(/\(track 4\)/)
    // no instrument load was attempted against song.tracks[2]
    expect(fake.received.some((m) => m.address === '/live/track/load/device')).toBe(false)
  })

  it('replyNumber / parseCreatedTrackIndex never guess a different numeric field', () => {
    expect(replyNumber({ ok: true, index: 'return:0', count: 3 }, ['index'])).toBeNull()
    expect(replyNumber({ ok: true, value: 0.5 })).toBe(0.5)
    expect(replyNumber({ ok: true, value: '0.25' })).toBe(0.25)
    expect(parseCreatedTrackIndex({ ok: true, index: 4 })).toEqual({ kind: 'track', index: 4 })
    expect(parseCreatedTrackIndex({ ok: true, index: 'return:1' })).toEqual({ kind: 'return', index: 1 })
    expect(parseCreatedTrackIndex({ ok: true, count: 3 })).toBeNull()
  })

  it('ableton_create_track falls back to native AbletonOSC when the handler is silent', async () => {
    const prev = HANDLER_TIMEOUTS['track/create']
    HANDLER_TIMEOUTS['track/create'] = 200
    try {
      fake.raw('/live/song/get/num_tracks', [3])
      const out = await getTool('ableton_create_track')!.execute({ type: 'audio' })
      expect(fake.last('/live/song/create_audio_track')).toBeDefined()
      expect(out).toMatch(/native AbletonOSC/)
      expect(out).toMatch(/not read back/)
    } finally {
      if (prev === undefined) delete HANDLER_TIMEOUTS['track/create']
      else HANDLER_TIMEOUTS['track/create'] = prev
    }
  }, 10_000)

  it('ableton_audio_analysis reads master meters via lom/get master_track', async () => {
    fake.json('lom/get', (args) => ({ ok: true, path: vals(args)[0], prop: vals(args)[1], value: vals(args)[1] === 'output_meter_left' ? 0.5 : 0.25 }))
    const out = await getTool('ableton_audio_analysis')!.execute({})
    const calls = fake.received.filter((m) => m.address === '/live/kbot/lom/get').map((m) => vals(m.args))
    expect(calls).toEqual([['master_track', 'output_meter_left'], ['master_track', 'output_meter_right']])
    expect(fake.received.some((m) => m.address.startsWith('/live/master/'))).toBe(false)
    expect(out).toMatch(/Master Output/)
    expect(out).toMatch(/-6\.0 dB/)
  })

  it('ableton_load_sample routes an existing absolute path to drum/build_pad on the TRACK path', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'kbot-lom-'))
    const wav = join(dir, 'kick.wav')
    writeFileSync(wav, 'RIFF')
    fake.json('drum/build_pad', (args) => ({ ok: true, rack: 'Drum Rack', note: vals(args)[1], sample: vals(args)[2], sample_file_path: vals(args)[2] }))
    const out = await getTool('ableton_load_sample')!.execute({ track: 3, pad: 36, sample: wav })
    expect(vals(fake.last('/live/kbot/drum/build_pad')!.args)).toEqual(['tracks 2', 36, wav])
    expect(out).toMatch(/via \/live\/kbot\/drum\/build_pad/)
    expect(fake.received.some((m) => m.address === '/live/kbot/browser/load')).toBe(false)
  })

  it('ableton_load_sample routes search terms to browser/load pad:T:note', async () => {
    fake.json('browser/load', (args) => ({ ok: true, target: vals(args)[1], name: 'kick_808.wav' }))
    const out = await getTool('ableton_load_sample')!.execute({ track: 1, pad: 36, sample: 'kick_808' })
    expect(vals(fake.last('/live/kbot/browser/load')!.args)).toEqual(['kick_808', 'pad:0:36', 'user_library,user_folders,samples'])
    expect(out).toMatch(/via \/live\/kbot\/browser\/load/)
    expect(out).toMatch(/"name": "kick_808.wav"/)
    expect(fake.received.some((m) => m.address === '/live/kbot/load_sample_file')).toBe(false)
  })
})

// ── ableton-bridge-tools tier-3 OSC fallback ─────────────────────────────

describe('bridge tools tier-3 fallback (9001 and 9997 unreachable)', () => {
  it('ableton_browse answers via the OSC kbot handler and says so', async () => {
    fake.json('browser/search', { ok: true, items: [{ name: 'Saturator', uri: 'query:AudioFx#Saturator', is_loadable: true, is_device: true }] })
    const out = await getTool('ableton_browse')!.execute({ query: 'satur', category: 'fx' })
    expect(vals(fake.last('/live/kbot/browser/search')!.args)).toEqual(['satur', 'audio_effects'])
    expect(out).toMatch(/via AbletonOSC kbot handler/)
    expect(out).toMatch(/\*\*Saturator\*\*/)
  })

  it('ableton_load_effect inserts via track/insert_device and prints the read-back', async () => {
    fake.json('track/insert_device', { ok: true, devices: [{ name: 'Saturator', index: 0 }] })
    const out = await getTool('ableton_load_effect')!.execute({ track: 1, name: 'Saturator', position: 'before' })
    expect(vals(fake.last('/live/kbot/track/insert_device')!.args)).toEqual([0, 'Saturator', 0])
    expect(out).toMatch(/via AbletonOSC kbot handler/)
    expect(out).toMatch(/"name": "Saturator"/)
  })

  it('ableton_load_preset falls back to device/load_preset', async () => {
    fake.json('device/load_preset', { ok: true, preset: 'Warm Pad' })
    const out = await getTool('ableton_load_preset')!.execute({ track: 2, device: 0, preset_name: 'Warm Pad' })
    expect(vals(fake.last('/live/kbot/device/load_preset')!.args)).toEqual([1, 0, 'Warm Pad'])
    expect(out).toMatch(/via AbletonOSC kbot handler/)
  })

  it('ableton_effect_chain inserts each device and reports per-item outcomes from the read-back', async () => {
    const chainSoFar: string[] = []
    fake.json('track/insert_device', (args) => {
      const name = String(vals(args)[1])
      if (name === 'Nope') return { ok: false, error: 'not found' }
      if (name === 'Ghost') return { ok: true, added: 0, devices: chainSoFar.slice(), warning: 'device count unchanged' }
      chainSoFar.push(name)
      return { ok: true, added: 1, devices: chainSoFar.slice() }
    })
    const out = await getTool('ableton_effect_chain')!.execute({ track: 1, chain: ['Compressor', 'Nope', 'Ghost', 'EQ Eight'] })
    expect(out).toMatch(/\*\*Compressor\*\* loaded/)
    expect(out).toMatch(/\*\*Nope\*\* — not found/)
    expect(out).toMatch(/\*\*Ghost\*\* — NOT confirmed/)
    expect(out).toMatch(/\*\*EQ Eight\*\* loaded/)
    expect(out).toMatch(/\*\*2\*\* loaded, \*\*2\*\* failed out of 4 effects \(via AbletonOSC kbot handler\)/)
  })

  it('ableton_load_effect does not claim "Loaded" when the read-back shows no new device', async () => {
    fake.json('track/insert_device', { ok: true, added: 0, devices: ['Operator'], warning: 'device count unchanged' })
    const out = await getTool('ableton_load_effect')!.execute({ track: 1, name: 'Saturator' })
    expect(out).toMatch(/NOT confirmed/)
    expect(out).not.toMatch(/^Loaded/)
    expect(out).toMatch(/added=0/)
  })

  it('insertDeviceConfirmed trusts added, then the device list, never ok alone', () => {
    expect(insertDeviceConfirmed({ ok: true, added: 1 }, 'Saturator')).toBe(true)
    expect(insertDeviceConfirmed({ ok: true, added: 0, devices: ['Saturator'] }, 'Saturator')).toBe(false)
    expect(insertDeviceConfirmed({ ok: true, devices: ['Operator', 'Saturator'] }, 'saturator')).toBe(true)
    expect(insertDeviceConfirmed({ ok: true, devices: [{ name: 'Saturator' }] }, 'Saturator')).toBe(true)
    expect(insertDeviceConfirmed({ ok: true }, 'Saturator')).toBe(false)
    expect(insertDeviceConfirmed({ ok: false, added: 1 }, 'Saturator')).toBe(false)
  })

  it('reports all three tiers when nothing answers', async () => {
    const prev = HANDLER_TIMEOUTS['browser/search']
    HANDLER_TIMEOUTS['browser/search'] = 200
    try {
      const out = await getTool('ableton_browse')!.execute({ query: 'x' })
      expect(out).toMatch(/AbletonOSC kbot handler also failed/)
      expect(out).toMatch(/Option 3/)
    } finally {
      HANDLER_TIMEOUTS['browser/search'] = prev
    }
  }, 10_000)
})
