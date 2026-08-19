// node --test tools/ableton/gen-coverage.test.mjs
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import {
  DEFAULTS, buildClasses, resolveEntry, defaultEntry, isListenerNoise, isIntEnum,
  inferKindByName, generate, renderKind, examplePath,
} from './gen-coverage.mjs'

const dump = JSON.parse(readFileSync(DEFAULTS.dump, 'utf8'))
const map = JSON.parse(readFileSync(DEFAULTS.map, 'utf8'))

test('listener noise filter', () => {
  assert.equal(isListenerNoise('add_tempo_listener'), true)
  assert.equal(isListenerNoise('remove_tempo_listener'), true)
  assert.equal(isListenerNoise('tempo_has_listener'), true)
  assert.equal(isListenerNoise('tempo'), false)
  assert.equal(isListenerNoise('add_macro'), false) // real method, not a listener
  assert.equal(isListenerNoise('add_new_notes'), false)
})

test('int enum detection', () => {
  assert.equal(isIntEnum(dump['class:Song.CaptureDestination']), true)
  assert.equal(isIntEnum(dump['class:Song.BeatTime']), false)
  assert.equal(isIntEnum(dump['class:Application.Variants']), false)
})

test('kind inference by name', () => {
  assert.equal(inferKindByName('insert_chain'), 'method~')
  assert.equal(inferKindByName('randomize_macros'), 'method~')
  assert.equal(inferKindByName('has_drum_pads'), 'property~')
  assert.equal(inferKindByName('chain_selector'), '?')
  assert.equal(renderKind('bool~'), 'property (bool)~')
  assert.equal(renderKind('ERR'), 'property (getter raised on the dumped instance)')
})

test('buildClasses canonicalises instance aliases and merges class lists', () => {
  const { classes, footer } = buildClasses(dump)
  assert.ok(classes.has('Clip'))
  assert.ok(!classes.has('Clip(midi)'))
  assert.ok(classes.has('Browser.BrowserItem'))
  assert.ok(!classes.has('BrowserItem'))
  // measured kind wins over class-list inference
  assert.equal(classes.get('Song').get('tempo'), 'float')
  assert.equal(classes.get('Song').get('start_playing'), 'method')
  // class-only members are present with inferred kinds
  assert.equal(classes.get('RackDevice').get('insert_chain'), 'method~')
  assert.equal(classes.get('RackDevice').get('name'), 'str~')
  // dump errors and Live.modules end up in the footer, not as classes
  assert.ok(footer.errors.some((e) => e.startsWith('CuePoint:')))
  assert.ok(footer.modules.includes('Song'))
  assert.ok(!classes.has('Live.modules'))
})

test('resolveEntry precedence: exact > base exact > glob > base glob > default', () => {
  const m = {
    _inherits: { RackDevice: 'Device' },
    'Device.name': { via: 'osc', ref: 'A' },
    'Device.*': { via: 'ui', ref: 'B' },
    'RackDevice.insert_chain': { via: 'tool', ref: 'C' },
  }
  assert.equal(resolveEntry(m, 'RackDevice', 'insert_chain', 'method').ref, 'C')
  assert.equal(resolveEntry(m, 'RackDevice', 'name', 'str').ref, 'A')
  assert.equal(resolveEntry(m, 'RackDevice', 'zzz', 'str').ref, 'B')
  assert.equal(resolveEntry(m, 'Chain', 'zzz', 'str').via, 'lom')
  assert.equal(resolveEntry(m, 'Chain', 'zzz', 'str')._from, 'default')
})

test('defaults: property -> get/set, method -> call, unknown -> describe, View -> na', () => {
  assert.match(defaultEntry('Track', 'name', 'str').ref, /ableton_lom get tracks N name · set tracks N name/)
  assert.match(defaultEntry('Track', 'insert_device', 'method').ref, /ableton_lom call tracks N insert_device/)
  assert.match(defaultEntry('RackDevice', 'chain_selector', '?').ref, /ableton_lom describe/)
  assert.equal(defaultEntry('Song', 'View', 'method').via, 'na')
  assert.match(defaultEntry('Song', 'can_undo', 'bool').ref, /read-only/)
  assert.equal(examplePath('DrumChain'), 'tracks N devices M drum_pads 36 chains 0')
})

test('coverage map is well-formed', () => {
  for (const [k, v] of Object.entries(map)) {
    if (k.startsWith('_')) continue
    assert.ok(['tool', 'lom', 'osc', 'ui', 'na'].includes(v.via), `${k}: bad via ${v.via}`)
    assert.equal(typeof v.ref, 'string', `${k}: ref must be a string`)
    assert.ok(v.ref.length > 0, `${k}: empty ref`)
  }
})

test('every non-glob map key names a member that exists in the dump', () => {
  const { classes } = buildClasses(dump)
  const missing = []
  for (const k of Object.keys(map)) {
    if (k.startsWith('_') || k.endsWith('.*')) continue
    const i = k.lastIndexOf('.')
    const cls = k.slice(0, i), member = k.slice(i + 1)
    if (!classes.has(cls) || !classes.get(cls).has(member)) missing.push(k)
  }
  assert.deepEqual(missing, [], `map keys not in the LOM dump: ${missing.join(', ')}`)
})

test('generate produces the expected sections and summary', () => {
  const { md, counts, total } = generate(dump, map, { date: '2026-08-18' })
  assert.match(md, /^# LOM coverage matrix/)
  assert.match(md, /\n## Song\n/)
  assert.match(md, /\n## RackDevice\n/)
  assert.match(md, /\n## Summary\n/)
  assert.match(md, /listener add\/remove\/has methods, omitted/)
  assert.equal(md.includes('`add_tempo_listener`'), false)
  assert.equal(counts.tool + counts.lom + counts.osc + counts.ui + counts.na, total)
  assert.ok(counts.tool > 50, 'typed handlers mapped')
  assert.ok(counts.osc > 150, 'stock OSC mapped')
  assert.ok(counts.ui >= 4, 'UI-only items present')
  // spot checks from the task brief
  assert.match(md, /`create_midi_clip` \| [^|]+\| `tool` — ableton_structure arr_create_clip/)
  assert.match(md, /`create_automation_envelope` \| [^|]+\| `tool` — ableton_structure automation/)
  assert.match(md, /`replace_sample` \| [^|]+\| `tool` — ableton_structure build_pad/)
  assert.match(md, /`presets` \| [^|]+\| `tool` — ableton_browser presets/)
  assert.match(md, /`load_item` \| [^|]+\| `tool` — ableton_browser load/)
  assert.match(md, /`begin_undo_step` \| [^|]+\| `tool` — ableton_structure undo_begin/)
  assert.match(md, /`press_current_dialog_button` \| [^|]+\| `tool` — ableton_structure dialog_press/)
  assert.match(md, /`is_frozen` \| [^|]+\| `ui` — /)
  assert.match(md, /`add_new_notes` \| [^|]+\| `osc` — \/live\/clip\/add\/notes/)
})
