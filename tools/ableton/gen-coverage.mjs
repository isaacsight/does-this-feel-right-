#!/usr/bin/env node
// gen-coverage.mjs — LOM coverage matrix generator.
//
// Reads the measured Live 12.4.5b5 LOM dump (docs/ableton/lom-dump-12.4.5b5.json,
// taken from inside Live via /live/exec) and the authored coverage map
// (tools/ableton/coverage-map.json) and writes docs/ableton/lom-coverage.md:
// one section per class, a table member | kind | how to reach it from kbot | notes,
// then a summary table with counts per "via".
//
// npm-free. Run:  node tools/ableton/gen-coverage.mjs [--dump p] [--map p] [--out p] [--stdout]
// Test:           node --test tools/ableton/gen-coverage.test.mjs
//
// Rules (see coverage-map.json _meta):
//   - exact "Class.member" beats "Class.*"; a class listed in _inherits falls back to its base
//   - anything unmapped is reachable through the generic plane: via "lom"
//     (property -> ableton_lom get/set, method -> ableton_lom call)
//   - listener plumbing (add_*_listener / remove_*_listener / *_has_listener) is skipped from
//     the tables and counted in the footer
//   - int enums (classes exposing as_integer_ratio + names + values) render as a value list

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const REPO = resolve(HERE, '..', '..')

export const DEFAULTS = {
  dump: resolve(REPO, 'docs/ableton/lom-dump-12.4.5b5.json'),
  map: resolve(HERE, 'coverage-map.json'),
  out: resolve(REPO, 'docs/ableton/lom-coverage.md'),
}

// Instance-dump keys that need a canonical class name.
const INSTANCE_ALIASES = { 'Clip(midi)': 'Clip', BrowserItem: 'Browser.BrowserItem' }

// Python int builtins that appear on int-enum classes; not LOM members.
const INT_BUILTINS = new Set([
  'as_integer_ratio', 'bit_count', 'bit_length', 'conjugate', 'denominator', 'from_bytes',
  'imag', 'name', 'names', 'numerator', 'real', 'to_bytes', 'values', 'is_integer',
])

// Members whose name alone tells us they are methods (used only when the instance dump
// did not capture the class; rendered as "method~").
const METHOD_PREFIXES = [
  'add_', 'remove_', 'insert_', 'delete_', 'create_', 'duplicate_', 'get_', 'set_', 'store_',
  'save_', 'recall_', 'randomize_', 'copy_', 'clear_', 'move_', 'reset_', 'replace_', 'guess_',
  'select_', 'deselect_', 'apply_', 'jump_', 'begin_', 'end_', 'press_', 'show_', 'hide_',
  'focus_', 'scroll_', 'zoom_', 'toggle_', 'stop_', 'start_', 'capture_', 'trigger_', 'force_',
  'find_', 'note_number_', 'beat_to_', 'sample_to_', 'seconds_to_', 're_enable_', 'load_',
  'preview_', 'relation_to_', 'iter_', 'can_warp_', 'warp_', 'send_', 'subscribe_', 'unsubscribe_',
  'grab_', 'release_control', 'fetch_', 'enable_', 'disable_',
]
// Names whose shape says "property" (type still unknown; rendered as "property~").
const PROPERTY_PREFIXES = ['is_', 'has_', 'can_', 'visible_', 'selected_', 'available_']
const PROPERTY_SUFFIXES = ['_count', '_index', '_name', '_enabled', '_mode', '_pads', '_chains', '_markers', '_group']
const METHOD_EXACT = new Set([
  'crop', 'fire', 'stop', 'scrub', 'quantize', 'quantize_pitch', 'undo', 'redo', 'tap_tempo',
  'View', 'append', 'extend', 'has_option', 'is_view_visible', 'available_main_views',
])

// Section order: families first, then everything else alphabetically.
const ORDER = [
  'Song', 'Song.View', 'Song.CuePoint', 'Application', 'Application.View',
  'Application.ControlSurfaceProxy', 'Track', 'Track.View', 'MixerDevice', 'ChainMixerDevice',
  'ClipSlot', 'Clip', 'Clip.View', 'Scene', 'Device', 'Device.View', 'DeviceParameter',
  'RackDevice', 'Chain', 'DrumPad', 'DrumChain', 'SimplerDevice', 'Sample', 'PluginDevice',
  'MaxDevice', 'CompressorDevice', 'Eq8Device', 'WavetableDevice', 'HybridReverbDevice',
  'SpectralResonatorDevice', 'DriftDevice', 'MeldDevice', 'RoarDevice', 'ShifterDevice',
  'Browser', 'Browser.BrowserItem', 'GroovePool', 'Groove', 'TuningSystem',
]

const VIA_LABEL = {
  tool: 'typed kbot handler',
  lom: 'generic ableton_lom plane',
  osc: 'stock AbletonOSC address',
  ui: 'UI only (Plane D)',
  na: 'constant / record — not addressed',
}

export function isListenerNoise(name) {
  return (
    (name.startsWith('add_') && name.endsWith('_listener')) ||
    (name.startsWith('remove_') && name.endsWith('_listener')) ||
    name.endsWith('_has_listener')
  )
}

export function isIntEnum(members) {
  const s = new Set(members)
  return s.has('as_integer_ratio') && s.has('names') && s.has('values')
}

export function inferKindByName(name) {
  if (METHOD_EXACT.has(name)) return 'method~'
  for (const p of METHOD_PREFIXES) if (name.startsWith(p)) return 'method~'
  for (const p of PROPERTY_PREFIXES) if (name.startsWith(p)) return 'property~'
  for (const s of PROPERTY_SUFFIXES) if (name.endsWith(s)) return 'property~'
  return '?'
}

// Build the canonical class table from the raw dump.
//   classes: Map<className, Map<member, kindString>>
//   footer:  { errors: [...], empty: [...], modules: [...] }
export function buildClasses(dump) {
  const classes = new Map()
  const footer = { errors: [], empty: [], modules: [] }
  const globalKinds = new Map() // member name -> instance kind (for inference)

  const ensure = (cls) => {
    if (!classes.has(cls)) classes.set(cls, new Map())
    return classes.get(cls)
  }

  // Pass 1: instance dumps (kinds are measured).
  for (const [key, val] of Object.entries(dump)) {
    if (key.startsWith('class:') || key === 'Live.modules') continue
    if (typeof val !== 'object' || Array.isArray(val)) { footer.errors.push(`${key}: ${String(val)}`); continue }
    const cls = INSTANCE_ALIASES[key] || key
    const m = ensure(cls)
    for (const [member, kind] of Object.entries(val)) {
      m.set(member, kind)
      if (!globalKinds.has(member) && kind !== 'ERR') globalKinds.set(member, kind)
    }
  }
  // Pass 2: class-level name lists (kinds inferred).
  for (const [key, val] of Object.entries(dump)) {
    if (!key.startsWith('class:')) continue
    const cls = key.slice('class:'.length)
    if (typeof val === 'string') { footer.errors.push(`${cls}: ${val}`); continue }
    if (!Array.isArray(val)) continue
    if (val.length === 0) { footer.empty.push(cls); continue }
    const m = ensure(cls)
    for (const member of val) {
      if (m.has(member)) continue
      const g = globalKinds.get(member)
      m.set(member, g ? `${g}~` : inferKindByName(member))
    }
  }
  if (Array.isArray(dump['Live.modules'])) footer.modules = dump['Live.modules']
  return { classes, footer }
}

// Resolve the coverage entry for Class.member. Precedence:
// exact > base exact > glob > base glob > default(lom).
export function resolveEntry(map, cls, member, kind) {
  const inherits = map._inherits || {}
  const chain = [cls]
  let base = inherits[cls]
  while (base && !chain.includes(base)) { chain.push(base); base = inherits[base] }
  for (const c of chain) if (map[`${c}.${member}`]) return { ...map[`${c}.${member}`], _from: `${c}.${member}` }
  for (const c of chain) if (map[`${c}.*`]) return { ...map[`${c}.*`], _from: `${c}.*` }
  return defaultEntry(cls, member, kind)
}

export function defaultEntry(cls, member, kind) {
  const isMethod = kind === 'method' || kind === 'method~'
  const unknown = kind === '?'
  const path = examplePath(cls)
  if (member === 'View') return { via: 'na', ref: `nested class ${cls}.View — see its own section`, _from: 'default' }
  if (unknown) return { via: 'lom', ref: `ableton_lom describe ${path} → then get/set or call ${member}`, _from: 'default' }
  if (isMethod) return { via: 'lom', ref: `ableton_lom call ${path} ${member} [args]`, _from: 'default' }
  if (member === 'canonical_parent' || member.startsWith('can_') || member.startsWith('has_')) {
    return { via: 'lom', ref: `ableton_lom get ${path} ${member} (read-only)`, _from: 'default' }
  }
  return { via: 'lom', ref: `ableton_lom get ${path} ${member} · set ${path} ${member} <json>`, _from: 'default' }
}

// A representative LiveAPI-style path for a class (0-based indices).
export function examplePath(cls) {
  const P = {
    Song: 'live_set', 'Song.View': 'view', 'Song.CuePoint': 'live_set cue_points 0',
    Application: 'app', 'Application.View': 'app view', 'Application.ControlSurfaceProxy': 'app control_surfaces 0',
    Track: 'tracks N', 'Track.View': 'tracks N view', MixerDevice: 'tracks N mixer_device',
    ChainMixerDevice: 'tracks N devices M chains 0 mixer_device',
    ClipSlot: 'tracks N clip_slots S', Clip: 'tracks N clip_slots S clip', 'Clip.View': 'tracks N clip_slots S clip view',
    Scene: 'scenes N', Device: 'tracks N devices M', 'Device.View': 'tracks N devices M view',
    DeviceParameter: 'tracks N devices M parameters K', RackDevice: 'tracks N devices M',
    Chain: 'tracks N devices M chains C', DrumPad: 'tracks N devices M drum_pads 36',
    DrumChain: 'tracks N devices M drum_pads 36 chains 0', SimplerDevice: 'tracks N devices M',
    Sample: 'tracks N devices M sample', PluginDevice: 'tracks N devices M', MaxDevice: 'tracks N devices M',
    Browser: 'app browser', 'Browser.BrowserItem': 'app browser instruments',
    GroovePool: 'live_set groove_pool', Groove: 'live_set groove_pool grooves 0',
    TuningSystem: 'live_set tuning_system',
  }
  if (P[cls]) return P[cls]
  if (cls.endsWith('Device')) return 'tracks N devices M'
  return `<${cls} path>`
}

export function renderKind(kind) {
  if (kind === 'method') return 'method'
  if (kind === 'method~') return 'method~'
  if (kind === 'property~') return 'property~'
  if (kind === '?') return '?'
  if (kind === 'ERR') return 'property (getter raised on the dumped instance)'
  if (kind.endsWith('~')) return `property (${kind.slice(0, -1)})~`
  return `property (${kind})`
}

const esc = (s) => String(s ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ')

export function orderClasses(names) {
  const set = new Set(names)
  const first = ORDER.filter((n) => set.has(n))
  const rest = names.filter((n) => !ORDER.includes(n)).sort()
  return [...first, ...rest]
}

export function generate(dump, map, opts = {}) {
  const { classes, footer } = buildClasses(dump)
  const counts = { tool: 0, lom: 0, osc: 0, ui: 0, na: 0 }
  const perClass = []
  let listeners = 0
  let total = 0
  const lines = []
  const today = opts.date || localDate()

  lines.push('# LOM coverage matrix — Live 12.4.5b5 × kbot')
  lines.push('')
  lines.push(`> Generated ${today} by \`node tools/ableton/gen-coverage.mjs\` from`)
  lines.push('> `docs/ableton/lom-dump-12.4.5b5.json` (measured inside Live via `/live/exec`) and')
  lines.push('> `tools/ableton/coverage-map.json` (authored). Do not hand-edit; edit the map and regenerate.')
  lines.push('> Operator manual: [`CONTROL.md`](./CONTROL.md).')
  lines.push('')
  lines.push('**How to read it.** Every LOM member is reachable from kbot one of five ways:')
  lines.push('')
  lines.push('| via | meaning |')
  lines.push('|---|---|')
  lines.push('| `tool` | a typed kbot handler (`ableton_lom` / `ableton_browser` / `ableton_structure` → `kbot_ext.py` `/live/kbot/*`), with JSON read-back |')
  lines.push('| `lom` | the generic plane: `ableton_lom get` / `set` / `call` / `describe` / `children` `<path> ...` — the default for anything without a typed handler |')
  lines.push('| `osc` | a stock AbletonOSC address (upstream `0ca6821` + local edits); listed where one exists, with the existing kbot tool that speaks it |')
  lines.push('| `ui` | the LOM cannot do it; the Live menu path is given (Plane D, peekaboo/computer-use) |')
  lines.push('| `na` | enum constant or record class; not addressed, passed as a value |')
  lines.push('')
  lines.push('**Kind column.** `property (type)` / `method` are measured on a live instance. A trailing `~` means the kind was')
  lines.push('inferred (the class was only enumerated at class level; the type came from a same-named member elsewhere or from the')
  lines.push('name); `?` means unknown — `ableton_lom describe <path>` reports it at runtime. Paths are Max LiveAPI style, 0-based.')
  lines.push('')
  const all = orderClasses([...classes.keys()])
  const main = all.filter((c) => ORDER.includes(c))
  const value = all.filter((c) => !ORDER.includes(c))
  lines.push('Classes: ' + main.map((c) => `[${c}](#${anchor(c)})`).join(' · '))
  lines.push('')
  lines.push('Enums and value classes: ' + value.map((c) => `[${c}](#${anchor(c)})`).join(' · '))
  lines.push('')

  for (const cls of all) {
    const members = classes.get(cls)
    const names = [...members.keys()]
    lines.push(`## ${cls}`)
    lines.push('')
    if (isIntEnum(names)) {
      const values = names.filter((n) => !INT_BUILTINS.has(n))
      const e = resolveEntry(map, cls, '*', 'enum')
      counts.na += values.length
      total += values.length
      perClass.push({ cls, n: values.length, via: { na: values.length } })
      lines.push(`Int enum (${values.length} values): ${values.map((v) => `\`${v}\``).join(', ')}.`)
      lines.push('')
      lines.push(`_${esc(e.ref)}_`)
      lines.push('')
      continue
    }
    const visible = names.filter((n) => !isListenerNoise(n))
    const noise = names.length - visible.length
    listeners += noise
    lines.push(`Path example: \`${examplePath(cls)}\` · ${visible.length} members` + (noise ? ` (+ ${noise} listener add/remove/has methods, omitted)` : ''))
    lines.push('')
    lines.push('| member | kind | how to reach it from kbot | notes |')
    lines.push('|---|---|---|---|')
    const via = {}
    for (const member of visible.sort()) {
      const kind = members.get(member)
      const e = resolveEntry(map, cls, member, kind)
      const v = counts[e.via] === undefined ? 'lom' : e.via
      counts[v]++
      via[v] = (via[v] || 0) + 1
      total++
      lines.push(`| \`${member}\` | ${renderKind(kind)} | \`${v}\` — ${esc(e.ref)} | ${esc(e.note || '')} |`)
    }
    perClass.push({ cls, n: visible.length, via })
    lines.push('')
  }

  lines.push('## Summary')
  lines.push('')
  lines.push('| via | members | share |')
  lines.push('|---|---:|---:|')
  for (const k of ['tool', 'osc', 'lom', 'ui', 'na']) {
    lines.push(`| \`${k}\` — ${VIA_LABEL[k]} | ${counts[k]} | ${total ? ((100 * counts[k]) / total).toFixed(1) : '0.0'}% |`)
  }
  lines.push(`| **total (non-listener members)** | **${total}** | 100% |`)
  lines.push('')
  lines.push('Per class:')
  lines.push('')
  lines.push('| class | members | tool | osc | lom | ui | na |')
  lines.push('|---|---:|---:|---:|---:|---:|---:|')
  for (const r of perClass) {
    lines.push(`| ${r.cls} | ${r.n} | ${r.via.tool || 0} | ${r.via.osc || 0} | ${r.via.lom || 0} | ${r.via.ui || 0} | ${r.via.na || 0} |`)
  }
  lines.push('')
  lines.push('## Footer')
  lines.push('')
  lines.push(`- Listener plumbing omitted from the tables: **${listeners}** \`add_*_listener\` / \`remove_*_listener\` / \`*_has_listener\` methods across ${classes.size} classes. All are reachable generically (\`ableton_lom call <path> add_<prop>_listener\` is not useful over one-shot OSC; use \`/live/<class>/start_listen/<prop>\` where AbletonOSC exposes it, or a Max for Live \`live.observer\`).`)
  lines.push(`- Classes reachable from \`Live.*\` (${footer.modules.length} modules): ${footer.modules.map((m) => `\`${m}\``).join(', ')}.`)
  const notDumped = footer.modules.filter((m) => !classes.has(m) && !['Base', 'Conversions', 'Listener'].includes(m))
  if (notDumped.length) lines.push(`- Modules present but not dumped as classes (no instance in the probed Set): ${notDumped.map((m) => `\`${m}\``).join(', ')} — reachable via \`ableton_lom describe\` when an instance exists (e.g. \`tracks N take_lanes 0\`, \`... clip automation_envelope\`).`)
  if (footer.empty.length) lines.push(`- Class lists captured empty (no public members at class level): ${footer.empty.map((m) => `\`${m}\``).join(', ')}.`)
  if (footer.errors.length) lines.push(`- Dump errors (name lookup failed in the dump script, not missing from Live): ${footer.errors.map((m) => `\`${esc(m)}\``).join('; ')}.`)
  lines.push('- Not in the LOM at all (UI only): freeze/flatten, export audio/stems, save/open Set, preferences, plugin GUI interaction, loading a Max for Live device other than through the browser. See CONTROL.md "What still needs the UI".')
  lines.push('')
  return { md: lines.join('\n') + '\n', counts, total, listeners, classes: classes.size }
}

export function localDate(d = new Date()) {
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`
}

export function anchor(s) {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, '')
}

function parseArgs(argv) {
  const o = { ...DEFAULTS, stdout: false }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--dump') o.dump = resolve(argv[++i])
    else if (a === '--map') o.map = resolve(argv[++i])
    else if (a === '--out') o.out = resolve(argv[++i])
    else if (a === '--stdout') o.stdout = true
    else if (a === '--help' || a === '-h') { console.log('usage: gen-coverage.mjs [--dump p] [--map p] [--out p] [--stdout]'); process.exit(0) }
  }
  return o
}

function main() {
  const o = parseArgs(process.argv.slice(2))
  const dump = JSON.parse(readFileSync(o.dump, 'utf8'))
  const map = JSON.parse(readFileSync(o.map, 'utf8'))
  const { md, counts, total, listeners, classes } = generate(dump, map)
  if (o.stdout) { process.stdout.write(md); return }
  mkdirSync(dirname(o.out), { recursive: true })
  writeFileSync(o.out, md)
  console.log(`wrote ${o.out}: ${classes} classes, ${total} members (${listeners} listener methods omitted); via ${JSON.stringify(counts)}`)
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main()
