// kbot Ableton LOM tools — generic Live Object Model control over the
// /live/kbot/* handlers (kbot_ext.py, registered inside AbletonOSC).
//
// Contract (docs/superpowers/specs/2026-08-18-ableton-full-control-design.md,
// section 3.1): every /live/kbot/<name> handler takes positional OSC args and
// replies with exactly ONE string arg = JSON {ok:true,...} | {ok:false,error}.
// Every mutating handler returns a read-back of the thing it changed; these
// tools print Live's reply verbatim (pretty JSON) and never say "success"
// on their own authority.
//
// Tools:
//   ableton_lom        — get/set/call/describe/children/exec/snapshot/snapshot_file/list/ping
//   ableton_browser    — search/load/preview/stop_preview/presets/load_preset/insert_device
//   ableton_structure  — tracks, devices, racks, drum pads, clip notes, quantize,
//                        automation, arrangement, undo groups, song data, dialogs
//
// Index convention on this plane: track / slot / device / scene indexes are
// 0-BASED (raw LOM), unlike the older 1-based convenience tools in ableton.ts.
//
// Path grammar (Max LiveAPI style, space-separated): "live_set", "tracks 0",
// "return_tracks 1", "master_track", "scenes 3", "cue_points 0",
// "groove_pool grooves 0", "view", "tracks 0 clip_slots 2 clip",
// "tracks 0 devices 1 parameters 4", "... devices 0 chains 1 devices 0",
// "... drum_pads 36 chains 0", "app", "app browser instruments".

import { registerTool } from './index.js'
import { ensureAbleton, formatAbletonError, type OscArg } from '../integrations/ableton-osc.js'

// ── Types ───────────────────────────────────────────────────────────────────

export interface KbotReply {
  ok: boolean
  error?: string
  [key: string]: unknown
}

/** Thrown when Live's kbot handler replied {ok:false,error}. */
export class KbotLiveError extends Error {
  readonly address: string
  readonly reply: KbotReply
  constructor(address: string, reply: KbotReply) {
    super(`Live rejected ${address}: ${reply.error ?? 'unknown error'}`)
    this.name = 'KbotLiveError'
    this.address = address
    this.reply = reply
  }
}

// ── Pure helpers (unit-tested) ──────────────────────────────────────────────

export const KBOT_PREFIX = '/live/kbot/'

/** Default per-handler timeouts (ms). Anything not listed uses DEFAULT_TIMEOUT. */
export const DEFAULT_TIMEOUT = 8_000
export const HANDLER_TIMEOUTS: Record<string, number> = {
  'browser/search': 20_000,
  'browser/load': 20_000,
  'browser/preview': 10_000,
  'device/presets': 15_000,
  'device/load_preset': 20_000,
  'track/insert_device': 20_000,
  'drum/build_pad': 20_000,
  'snapshot': 30_000,
  'snapshot_file': 30_000,
  'exec': 20_000,
}

/** Normalize a handler name or full address into the full /live/kbot/... address. */
export function kbotAddress(nameOrAddress: string): string {
  const n = String(nameOrAddress).trim()
  if (n.startsWith('/')) return n
  return KBOT_PREFIX + n.replace(/^\/+/, '')
}

/** Timeout for a handler (accepts a bare name or full address). */
export function timeoutFor(nameOrAddress: string): number {
  const addr = kbotAddress(nameOrAddress)
  const name = addr.startsWith(KBOT_PREFIX) ? addr.slice(KBOT_PREFIX.length) : addr
  return HANDLER_TIMEOUTS[name] ?? DEFAULT_TIMEOUT
}

/**
 * Parse the single-string JSON reply of a /live/kbot/* handler.
 * Throws on shape violations (no string arg, invalid JSON, missing ok).
 */
export function parseKbotReply(address: string, args: OscArg[]): KbotReply {
  const strArgs = args.filter((a): a is { type: 's'; value: string } => a.type === 's')
  if (strArgs.length === 0) {
    throw new Error(
      `${address}: expected one JSON string reply, got ${args.length} arg(s) ` +
      `[${args.map(a => a.type).join(',')}]`,
    )
  }
  // Contract says exactly one string; if a handler ever sends several, join
  // them in order (a defensive concat, not a chunking protocol).
  const text = strArgs.length === 1 ? strArgs[0].value : strArgs.map(a => a.value).join('')
  let parsed: unknown
  try {
    parsed = JSON.parse(text)
  } catch (err) {
    throw new Error(`${address}: reply is not valid JSON (${(err as Error).message}): ${text.slice(0, 200)}`)
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error(`${address}: reply JSON is not an object: ${text.slice(0, 200)}`)
  }
  const obj = parsed as Record<string, unknown>
  if (typeof obj.ok !== 'boolean') {
    throw new Error(`${address}: reply JSON has no boolean "ok": ${text.slice(0, 200)}`)
  }
  return obj as KbotReply
}

/**
 * Coerce a tool parameter into the JSON string a handler expects.
 * - undefined/null -> "null"
 * - string that parses as JSON -> passed through unchanged
 * - any other string -> JSON-quoted
 * - numbers / booleans / objects -> JSON.stringify
 */
export function toJsonArg(value: unknown): string {
  if (value === undefined || value === null) return 'null'
  if (typeof value === 'string') {
    const trimmed = value.trim()
    if (trimmed === '') return '""'
    try {
      JSON.parse(trimmed)
      return trimmed
    } catch {
      return JSON.stringify(value)
    }
  }
  return JSON.stringify(value)
}

/** Pretty-print a reply for tool output. */
export function formatReply(reply: unknown): string {
  return JSON.stringify(reply, null, 2)
}

/** Grid shorthands -> Live.Clip.GridQuantization member names (from the 12.4.5 LOM dump). */
export const GRID_ALIASES: Record<string, string> = {
  '0': 'no_grid', none: 'no_grid', no_grid: 'no_grid',
  '8bar': 'g_8_bars', '8_bars': 'g_8_bars', g_8_bars: 'g_8_bars',
  '4bar': 'g_4_bars', '4_bars': 'g_4_bars', g_4_bars: 'g_4_bars',
  '2bar': 'g_2_bars', '2_bars': 'g_2_bars', g_2_bars: 'g_2_bars',
  bar: 'g_bar', '1bar': 'g_bar', '1/1': 'g_bar', '1': 'g_bar', g_bar: 'g_bar',
  half: 'g_half', '1/2': 'g_half', '2': 'g_half', g_half: 'g_half',
  quarter: 'g_quarter', '1/4': 'g_quarter', '4': 'g_quarter', g_quarter: 'g_quarter',
  eighth: 'g_eighth', '1/8': 'g_eighth', '8': 'g_eighth', g_eighth: 'g_eighth',
  sixteenth: 'g_sixteenth', '1/16': 'g_sixteenth', '16': 'g_sixteenth', g_sixteenth: 'g_sixteenth',
  thirtysecond: 'g_thirtysecond', '1/32': 'g_thirtysecond', '32': 'g_thirtysecond', g_thirtysecond: 'g_thirtysecond',
}

export function normalizeGrid(raw: unknown): string {
  const key = String(raw ?? '1/16').trim().toLowerCase().replace(/\s+/g, '')
  return GRID_ALIASES[key] ?? key
}

// ── kbotCall: the one transport helper ──────────────────────────────────────

/**
 * Query a /live/kbot/* handler and return its parsed JSON reply.
 *
 * - `nameOrAddress` may be "lom/get" or "/live/kbot/lom/get".
 * - Args are sent positionally as OSC ints/floats/strings (auto-typed).
 * - Throws KbotLiveError when Live answered {ok:false,error}.
 * - Throws a plain Error (with an install hint) on timeout / bad shape.
 */
export async function kbotCall(
  nameOrAddress: string,
  ...args: (number | string)[]
): Promise<KbotReply> {
  const address = kbotAddress(nameOrAddress)
  const osc = await ensureAbleton()
  let raw: OscArg[]
  try {
    raw = await osc.queryWithTimeout(timeoutFor(address), address, ...args)
  } catch (err) {
    const msg = (err as Error).message
    if (/timeout/i.test(msg)) {
      throw new Error(
        `${msg}. No reply from the kbot handler — is kbot_ext.py installed in AbletonOSC ` +
        `and loaded (send /live/api/reload, or check Live's Log.txt)? For very large ` +
        `results (snapshot) prefer snapshot_file: single UDP replies are capped by the OS.`,
      )
    }
    throw err
  }
  const reply = parseKbotReply(address, raw)
  if (!reply.ok) throw new KbotLiveError(address, reply)
  return reply
}

/** Same as kbotCall but never throws: returns {ok:false,error} for the caller to render. */
export async function kbotTry(
  nameOrAddress: string,
  ...args: (number | string)[]
): Promise<KbotReply> {
  try {
    return await kbotCall(nameOrAddress, ...args)
  } catch (err) {
    if (err instanceof KbotLiveError) return err.reply
    return { ok: false, error: (err as Error).message }
  }
}

// ── Param helpers ───────────────────────────────────────────────────────────

function reqStr(args: Record<string, unknown>, key: string): string {
  const v = args[key]
  if (v === undefined || v === null || String(v).trim() === '') {
    throw new Error(`Missing required parameter "${key}"`)
  }
  return String(v)
}

function reqInt(args: Record<string, unknown>, key: string): number {
  const v = args[key]
  if (v === undefined || v === null || v === '') throw new Error(`Missing required parameter "${key}"`)
  const n = Number(v)
  if (!Number.isFinite(n)) throw new Error(`Parameter "${key}" must be a number (got ${JSON.stringify(v)})`)
  return Math.trunc(n)
}

function optInt(args: Record<string, unknown>, key: string): number | undefined {
  const v = args[key]
  if (v === undefined || v === null || v === '') return undefined
  const n = Number(v)
  if (!Number.isFinite(n)) throw new Error(`Parameter "${key}" must be a number (got ${JSON.stringify(v)})`)
  return Math.trunc(n)
}

function optNum(args: Record<string, unknown>, key: string): number | undefined {
  const v = args[key]
  if (v === undefined || v === null || v === '') return undefined
  const n = Number(v)
  if (!Number.isFinite(n)) throw new Error(`Parameter "${key}" must be a number (got ${JSON.stringify(v)})`)
  return n
}

function optStr(args: Record<string, unknown>, key: string): string | undefined {
  const v = args[key]
  if (v === undefined || v === null) return undefined
  const s = String(v)
  return s === '' ? undefined : s
}

/** Uniform error rendering for the three tools. */
function renderError(err: unknown): string {
  if (err instanceof KbotLiveError) {
    return `Live returned an error:\n${formatReply(err.reply)}`
  }
  const msg = (err as Error).message ?? String(err)
  if (/Could not connect to Ableton|not connected/i.test(msg)) {
    return `Ableton connection failed: ${msg}\n\n${formatAbletonError()}`
  }
  return `Error: ${msg}`
}

const ZERO_BASED = 'Indexes (track/slot/device/scene) are 0-BASED here (raw LOM), unlike the 1-based ableton_track/ableton_clip tools.'

/**
 * ableton_structure action aliases: the handler-address spelling ("track/create" -> "track_create",
 * "clip/notes/get" -> "notes_get") used by docs/ableton/CONTROL.md and the coverage matrix maps onto
 * the canonical action names. Both spellings are accepted.
 */
export const STRUCTURE_ACTION_ALIASES: Record<string, string> = {
  track_create: 'create_track',
  track_delete: 'delete_track',
  track_duplicate: 'duplicate_track',
  track_insert_device: 'insert_device',
  device_delete: 'delete_device',
  device_move: 'move_device',
  device_set_active: 'set_device_active',
  rack_insert_chain: 'insert_chain',
  rack_add_macro: 'add_macro',
  rack_macros: 'macros',
  notes_get: 'clip_notes:get',
  notes_set: 'clip_notes:set',
  notes_add: 'clip_notes:add',
  notes_remove: 'clip_notes:remove',
  clip_quantize: 'quantize',
  clip_automation: 'automation',
  app_message: 'message',
  app_dialog: 'dialog_press',
  song_data_get: 'data_get',
  song_data_set: 'data_set',
}

/** Resolve an ableton_structure action name (canonical or alias) to {action, op?}. */
export function resolveStructureAction(raw: unknown): { action: string; op?: string } {
  const key = String(raw ?? '').toLowerCase().trim()
  const mapped = STRUCTURE_ACTION_ALIASES[key] ?? key
  const [action, op] = mapped.split(':')
  return op ? { action, op } : { action }
}

// ── Tool registration ───────────────────────────────────────────────────────

export function registerAbletonLomTools(): void {

  // ─── 1. ableton_lom ───────────────────────────────────────────────────

  registerTool({
    name: 'ableton_lom',
    description:
      'Generic Ableton Live Object Model access via the kbot handlers inside AbletonOSC (/live/kbot/lom/*). ' +
      'get/set any property, call any method, describe members, count children, run Python (exec), ' +
      'or snapshot the whole Set as JSON. Path grammar is Max LiveAPI style, space-separated: ' +
      '"live_set", "tracks 0", "master_track", "tracks 0 clip_slots 2 clip", "tracks 0 devices 1 parameters 4", ' +
      '"tracks 0 devices 0 chains 1 devices 0", "tracks 0 devices 0 drum_pads 36 chains 0", "app", "app browser instruments". ' +
      ZERO_BASED + ' Output is Live\'s read-back JSON, verbatim.',
    parameters: {
      action: { type: 'string', description: '"get" | "set" | "call" | "describe" | "children" | "exec" | "snapshot" | "snapshot_file" | "list" | "ping"', required: true },
      path: { type: 'string', description: 'LOM path (e.g. "tracks 0", "master_track", "live_set"). Required for get/set/call/describe/children.' },
      prop: { type: 'string', description: 'Property name for get/set (e.g. "name", "tempo", "output_meter_left").' },
      value: { type: 'string', description: 'For set: new value as JSON text (e.g. "120", "\\"Bass\\"", "true", "[1,2]"). Plain strings are auto-quoted.' },
      method: { type: 'string', description: 'For call: method name (e.g. "fire", "create_midi_clip", "insert_device").' },
      args: { type: 'string', description: 'For call: JSON array of positional args (default "[]").' },
      code: { type: 'string', description: 'For exec: Python source run inside Live (song, app, Live, tracks in scope). Unauthenticated escape hatch (AbletonOSC binds 0.0.0.0:11000, so keep that port off untrusted networks); use sparingly and prefer get/set/call.' },
      depth: { type: 'number', description: 'For snapshot: recursion depth (handler default if omitted).' },
      file: { type: 'string', description: 'For snapshot_file: absolute path Live writes the JSON snapshot to.' },
    },
    tier: 'free',
    timeout: 45_000,
    async execute(args) {
      const action = String(args.action ?? '').toLowerCase().trim()
      try {
        switch (action) {
          case 'get': {
            const reply = await kbotCall('lom/get', reqStr(args, 'path'), reqStr(args, 'prop'))
            return formatReply(reply)
          }
          case 'set': {
            if (args.value === undefined || args.value === null) {
              return 'Error: set requires "value" (JSON text; pass the string "null" to set a property to null explicitly)'
            }
            const reply = await kbotCall('lom/set', reqStr(args, 'path'), reqStr(args, 'prop'), toJsonArg(args.value))
            return formatReply(reply)
          }
          case 'call': {
            const jsonArgs = args.args === undefined || args.args === null || args.args === '' ? '[]' : toJsonArg(args.args)
            const reply = await kbotCall('lom/call', reqStr(args, 'path'), reqStr(args, 'method'), jsonArgs)
            return formatReply(reply)
          }
          case 'describe': {
            const reply = await kbotCall('lom/describe', reqStr(args, 'path'))
            return formatReply(reply)
          }
          case 'children': {
            const reply = await kbotCall('lom/children', reqStr(args, 'path'))
            return formatReply(reply)
          }
          case 'exec': {
            const code = reqStr(args, 'code')
            const reply = await kbotCall('exec', code)
            // Echo the code that ran inside Live so the transcript records it next to the result.
            return `# exec sent to Live (/live/kbot/exec):\n${code}\n\n${formatReply(reply)}`
          }
          case 'snapshot': {
            const depth = optInt(args, 'depth')
            const reply = depth === undefined ? await kbotCall('snapshot') : await kbotCall('snapshot', depth)
            return formatReply(reply)
          }
          case 'snapshot_file': {
            const reply = await kbotCall('snapshot_file', reqStr(args, 'file'))
            return formatReply(reply)
          }
          case 'list': {
            const reply = await kbotCall('list')
            return formatReply(reply)
          }
          case 'ping': {
            const reply = await kbotCall('ping')
            return formatReply(reply)
          }
          default:
            return `Unknown action "${action}". Options: get, set, call, describe, children, exec, snapshot, snapshot_file, list, ping`
        }
      } catch (err) {
        return renderError(err)
      }
    },
  })

  // ─── 2. ableton_browser ───────────────────────────────────────────────

  registerTool({
    name: 'ableton_browser',
    description:
      'Ableton browser over the kbot handlers (/live/kbot/browser/*, device/*, track/insert_device): search the browser, ' +
      'load an item (device / preset / sample) onto a track, a drum pad or the selected target, preview items, ' +
      'list and load device presets, insert a native device by name. ' +
      ZERO_BASED + ' Output is Live\'s read-back JSON (e.g. the device list of the target after a load).',
    parameters: {
      action: { type: 'string', description: '"search" | "load" | "preview" | "stop_preview" | "presets" | "load_preset" | "insert_device"', required: true },
      query: { type: 'string', description: 'For search: text to search for (e.g. "Operator", "808 kick", "Saturator").' },
      category: { type: 'string', description: 'For search: optional browser root — instruments, audio_effects, midi_effects, drums, sounds, samples, packs, plugins, user_library, presets.' },
      limit: { type: 'number', description: 'For search: max results (handler default if omitted).' },
      item: { type: 'string', description: 'For load/preview: browser item URI (from search) or an exact name.' },
      target: { type: 'string', description: 'For load: "track:N" (0-based) | "pad:N:note" (drum rack on track N, MIDI note) | "selected". Defaults to "track:<track>" when track is given.' },
      track: { type: 'number', description: 'Track index, 0-based (presets/load_preset/insert_device, or to build the load target).' },
      device: { type: 'number', description: 'Device index on the track, 0-based (presets/load_preset).' },
      preset: { type: 'string', description: 'For load_preset: preset index (number) or name.' },
      name: { type: 'string', description: 'For insert_device: native device name (e.g. "Operator", "EQ Eight", "Drum Rack").' },
      position: { type: 'number', description: 'For insert_device: device chain position (0-based). Omit to append.' },
    },
    tier: 'free',
    timeout: 45_000,
    async execute(args) {
      const action = String(args.action ?? '').toLowerCase().trim()
      try {
        switch (action) {
          case 'search': {
            const query = reqStr(args, 'query')
            const category = optStr(args, 'category')
            const limit = optInt(args, 'limit')
            const callArgs: (number | string)[] = [query]
            if (category !== undefined) callArgs.push(category)
            if (limit !== undefined) {
              if (category === undefined) callArgs.push('')
              callArgs.push(limit)
            }
            const reply = await kbotCall('browser/search', ...callArgs)
            return formatReply(reply)
          }
          case 'load': {
            const item = reqStr(args, 'item')
            let target = optStr(args, 'target')
            if (!target) {
              const t = optInt(args, 'track')
              target = t === undefined ? 'selected' : `track:${t}`
            }
            const reply = await kbotCall('browser/load', item, target)
            return formatReply(reply)
          }
          case 'preview': {
            const reply = await kbotCall('browser/preview', reqStr(args, 'item'))
            return formatReply(reply)
          }
          case 'stop_preview': {
            const reply = await kbotCall('browser/stop_preview')
            return formatReply(reply)
          }
          case 'presets': {
            const reply = await kbotCall('device/presets', reqInt(args, 'track'), reqInt(args, 'device'))
            return formatReply(reply)
          }
          case 'load_preset': {
            const presetRaw = reqStr(args, 'preset')
            const preset: number | string = /^\d+$/.test(presetRaw.trim()) ? Number(presetRaw) : presetRaw
            const reply = await kbotCall('device/load_preset', reqInt(args, 'track'), reqInt(args, 'device'), preset)
            return formatReply(reply)
          }
          case 'insert_device': {
            const track = reqInt(args, 'track')
            const name = reqStr(args, 'name')
            const position = optInt(args, 'position')
            const reply = position === undefined
              ? await kbotCall('track/insert_device', track, name)
              : await kbotCall('track/insert_device', track, name, position)
            return formatReply(reply)
          }
          default:
            return `Unknown action "${action}". Options: search, load, preview, stop_preview, presets, load_preset, insert_device`
        }
      } catch (err) {
        return renderError(err)
      }
    },
  })

  // ─── 3. ableton_structure ─────────────────────────────────────────────

  registerTool({
    name: 'ableton_structure',
    description:
      'Structural authoring in Ableton over the kbot handlers: create/delete/duplicate tracks, insert/delete/move/enable devices, ' +
      'rack chains and macros, build drum pads from sample files, get/set/add/remove clip notes, quantize, write clip ' +
      'automation, create arrangement clips, duplicate session clips to the arrangement, list arrangement clips, ' +
      'group edits into one undo step, read/write song data, press dialog buttons, show status-bar messages. ' +
      ZERO_BASED + ' Output is Live\'s read-back JSON.',
    parameters: {
      action: {
        type: 'string',
        required: true,
        description:
          '"create_track" | "delete_track" | "duplicate_track" | "insert_device" | "delete_device" | "move_device" | "set_device_active" | ' +
          '"insert_chain" | "add_macro" | "macros" | "build_pad" | "clip_notes" | "quantize" | "automation" | ' +
          '"arr_create_clip" | "arr_dup_from_session" | "arr_clips" | "undo_begin" | "undo_end" | "data_get" | "data_set" | ' +
          '"dialog_press" | "message". Handler-address spellings are accepted as aliases (track_create, device_set_active, ' +
          'notes_get/notes_set/notes_add/notes_remove, rack_macros, clip_quantize, app_message, ...).',
      },
      kind: { type: 'string', description: 'create_track: "midi" | "audio" | "return" (default midi). delete_track: "return" deletes return track <track> instead of a regular track.' },
      track: { type: 'number', description: 'Track index, 0-based (most actions).' },
      index: { type: 'number', description: 'create_track: insert position (0-based; omit/-1 = end). dialog_press: button index. move_device: destination position.' },
      name: { type: 'string', description: 'create_track / insert_chain / build_pad: optional name.' },
      device: { type: 'number', description: 'Device index on the track, 0-based (delete_device / move_device / set_device_active).' },
      active: { type: 'boolean', description: 'set_device_active: true = enabled, false = bypassed.' },
      path: { type: 'string', description: 'LOM path of a rack (insert_chain / add_macro / macros), a rack or track (build_pad: "tracks 1 devices 0" or just "tracks 1" to find the Drum Rack on that track), or a clip (automation; clip_notes when track/slot are omitted, e.g. "tracks 0 clip_slots 0 clip" or "tracks 0 arrangement_clips 0").' },
      param_path: { type: 'string', description: 'automation: LOM path of the DeviceParameter, e.g. "tracks 0 devices 1 parameters 3" or "tracks 0 mixer_device volume".' },
      note: { type: 'number', description: 'build_pad: MIDI note of the pad (36 = C1).' },
      sample: { type: 'string', description: 'build_pad: absolute path of the sample file.' },
      slot: { type: 'number', description: 'Clip slot index, 0-based (clip_notes / quantize / arr_dup_from_session).' },
      position: { type: 'number', description: 'insert_device: device chain position (0-based). Omit to append.' },
      op: { type: 'string', description: 'clip_notes: "get" | "set" (replace all) | "add" | "remove". Default get.' },
      value: { type: 'string', description: 'JSON payload: clip_notes notes array [{pitch,start_time,duration,velocity,mute}], automation points [[time,length,value]...] or [{time,length,value}] with value in the parameter\'s OWN units (min..max, e.g. Operator Transpose -48..48; integer params round), macros set {index:value} or [v0,v1,...], data_set value.' },
      grid: { type: 'string', description: 'quantize: grid — "1/16" (default), "1/8", "1/4", "1/2", "bar", "1/32", or a Live.Clip.GridQuantization name.' },
      amount: { type: 'number', description: 'quantize: strength 0..1 (default 1).' },
      start: { type: 'number', description: 'arr_create_clip: start time in beats.' },
      length: { type: 'number', description: 'arr_create_clip: length in beats.' },
      time: { type: 'number', description: 'arr_dup_from_session: arrangement position in beats.' },
      key: { type: 'string', description: 'data_get / data_set: song data key.' },
      text: { type: 'string', description: 'message: status-bar text.' },
    },
    tier: 'free',
    timeout: 45_000,
    async execute(args) {
      const resolved = resolveStructureAction(args.action)
      const action = resolved.action
      if (resolved.op && (args.op === undefined || args.op === null || args.op === '')) args = { ...args, op: resolved.op }
      try {
        switch (action) {
          case 'create_track': {
            const kind = String(args.kind ?? 'midi').toLowerCase()
            if (!['midi', 'audio', 'return'].includes(kind)) return `Error: kind must be midi, audio or return (got "${kind}")`
            const idx = optInt(args, 'index')
            const name = optStr(args, 'name')
            const callArgs: (number | string)[] = [kind]
            if (idx !== undefined || name !== undefined) callArgs.push(idx ?? -1)
            if (name !== undefined) callArgs.push(name)
            return formatReply(await kbotCall('track/create', ...callArgs))
          }
          case 'delete_track': {
            const track = reqInt(args, 'track')
            const isReturn = String(args.kind ?? '').toLowerCase() === 'return'
            return formatReply(await kbotCall('track/delete', isReturn ? `return:${track}` : track))
          }
          case 'duplicate_track':
            return formatReply(await kbotCall('track/duplicate', reqInt(args, 'track')))
          case 'insert_device': {
            const track = reqInt(args, 'track')
            const name = reqStr(args, 'name')
            const position = optInt(args, 'position')
            return formatReply(position === undefined
              ? await kbotCall('track/insert_device', track, name)
              : await kbotCall('track/insert_device', track, name, position))
          }
          case 'delete_device':
            return formatReply(await kbotCall('device/delete', reqInt(args, 'track'), reqInt(args, 'device')))
          case 'move_device':
            return formatReply(await kbotCall('device/move', reqInt(args, 'track'), reqInt(args, 'device'), reqInt(args, 'index')))
          case 'set_device_active': {
            const active = args.active === undefined ? true : (args.active === true || String(args.active).toLowerCase() === 'true' || args.active === 1)
            return formatReply(await kbotCall('device/set_active', reqInt(args, 'track'), reqInt(args, 'device'), active ? 1 : 0))
          }
          case 'insert_chain': {
            const name = optStr(args, 'name')
            return formatReply(name === undefined
              ? await kbotCall('rack/insert_chain', reqStr(args, 'path'))
              : await kbotCall('rack/insert_chain', reqStr(args, 'path'), name))
          }
          case 'add_macro':
            return formatReply(await kbotCall('rack/add_macro', reqStr(args, 'path')))
          case 'macros': {
            // handler contract: rack/macros <rack path> get|set [json values]
            // (verified against Live 12.4.5 on 2026-08-18: sending the JSON as the
            // 2nd arg made kbot_ext reply "op must be get|set").
            const value = args.value
            return formatReply(value === undefined || value === null || value === ''
              ? await kbotCall('rack/macros', reqStr(args, 'path'), 'get')
              : await kbotCall('rack/macros', reqStr(args, 'path'), 'set', toJsonArg(value)))
          }
          case 'build_pad': {
            const name = optStr(args, 'name')
            const base: (number | string)[] = [reqStr(args, 'path'), reqInt(args, 'note'), reqStr(args, 'sample')]
            if (name !== undefined) base.push(name)
            return formatReply(await kbotCall('drum/build_pad', ...base))
          }
          case 'clip_notes': {
            const op = String(args.op ?? 'get').toLowerCase()
            if (!['get', 'set', 'add', 'remove'].includes(op)) return `Error: op must be get, set, add or remove (got "${op}")`
            // Either track + slot (session clip) or path (any clip: "tracks 0 clip_slots 0 clip", "tracks 0 arrangement_clips 0").
            const clipPath = optStr(args, 'path')
            const hasTrackSlot = args.track !== undefined && args.track !== null && args.track !== '' &&
              args.slot !== undefined && args.slot !== null && args.slot !== ''
            const locator: (number | string)[] = hasTrackSlot
              ? [reqInt(args, 'track'), reqInt(args, 'slot')]
              : clipPath !== undefined ? [clipPath] : []
            if (locator.length === 0) return 'Error: clip_notes needs either "track" + "slot" or a clip "path"'
            if (op === 'get') return formatReply(await kbotCall('clip/notes', op, ...locator))
            const value = args.value
            if (op !== 'remove' && (value === undefined || value === null || value === '')) {
              return `Error: clip_notes ${op} requires "value" (JSON notes array)`
            }
            return formatReply(value === undefined || value === null || value === ''
              ? await kbotCall('clip/notes', op, ...locator)
              : await kbotCall('clip/notes', op, ...locator, toJsonArg(value)))
          }
          case 'quantize': {
            const grid = normalizeGrid(args.grid)
            const amount = optNum(args, 'amount') ?? 1
            return formatReply(await kbotCall('clip/quantize', reqInt(args, 'track'), reqInt(args, 'slot'), grid, amount))
          }
          case 'automation': {
            const value = args.value
            if (value === undefined || value === null || value === '') return 'Error: automation requires "value" (JSON points)'
            return formatReply(await kbotCall('clip/automation', reqStr(args, 'path'), reqStr(args, 'param_path'), toJsonArg(value)))
          }
          case 'arr_create_clip': {
            const start = optNum(args, 'start') ?? 0
            const length = optNum(args, 'length')
            if (length === undefined) return 'Error: arr_create_clip requires "length" (beats)'
            return formatReply(await kbotCall('arrangement/create_clip', reqInt(args, 'track'), start, length))
          }
          case 'arr_dup_from_session': {
            const time = optNum(args, 'time') ?? 0
            return formatReply(await kbotCall('arrangement/dup_from_session', reqInt(args, 'track'), reqInt(args, 'slot'), time))
          }
          case 'arr_clips':
            return formatReply(await kbotCall('arrangement/clips', reqInt(args, 'track')))
          case 'undo_begin':
            return formatReply(await kbotCall('song/undo_group', 'begin'))
          case 'undo_end':
            return formatReply(await kbotCall('song/undo_group', 'end'))
          case 'data_get':
            return formatReply(await kbotCall('song/data', 'get', reqStr(args, 'key')))
          case 'data_set':
            return formatReply(await kbotCall('song/data', 'set', reqStr(args, 'key'), toJsonArg(args.value)))
          case 'dialog_press':
            return formatReply(await kbotCall('app/dialog', 'press', reqInt(args, 'index')))
          case 'message':
            return formatReply(await kbotCall('app/message', reqStr(args, 'text')))
          default:
            return `Unknown action "${action}". Options: create_track, delete_track, duplicate_track, insert_device, delete_device, move_device, ` +
              'set_device_active, insert_chain, add_macro, macros, build_pad, clip_notes, quantize, automation, arr_create_clip, ' +
              'arr_dup_from_session, arr_clips, undo_begin, undo_end, data_get, data_set, dialog_press, message'
        }
      } catch (err) {
        return renderError(err)
      }
    },
  })
}
