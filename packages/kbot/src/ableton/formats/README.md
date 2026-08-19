# Ableton file formats — `packages/kbot/src/ableton/formats/`

Read and write the files Ableton Live consumes, **without a running Live**:
Live Sets (`.als`), rack presets (`.adg`), device presets (`.adv`), Standard
MIDI Files (`.mid`), Max for Live device skeletons (`.maxpat` + JS) and a
Remote Script (Control Surface) scaffold. Node stdlib only (`zlib` for gzip),
TypeScript ESM, no new dependencies.

```ts
import { readLiveSet, writeLiveSet, readRack, writeInstrumentRack, writeDevicePreset,
         writeMidiFile, writeMaxForLiveSkeleton, writeRemoteScriptScaffold } from './index.js';
```

## The rule behind every writer: clone, never invent

Live's XML has hundreds of view-state and bookkeeping elements per track. The
writers therefore never synthesise Live XML from scratch. `skeletons.ts` (a
GENERATED file) embeds gzip+base64 fragments cut from files that **Live 12.4d1
itself saved** (all `MinorVersion 12.0_12402`, from the Live 12 Beta app bundle
on this Mac), stripped of content and stateful values:

| skeleton | cut from |
|---|---|
| Live Set envelope (`<LiveSet>` minus tracks/scenes), MIDI track, both return tracks (Reverb / Delay), scene, session `MidiClip` | `Core Library/Templates/Quick Start Beat.als` |
| audio track | `Core Library/Templates/8-Track Template.als` |
| arrangement locator | `Core Library/Lessons/Demo Songs/Chuck Sutton - Patience (Live 12 Suite Demo).als` |
| rack devices + branch presets (instrument / audio effect / MIDI effect / drum) and the `AbletonDevicePreset` wrapper | `Core Library/Racks/Instrument Racks/Piano & Keys/E-Piano Wurli.adg`, `…/Audio Effect Racks/Mixing & Mastering/MS Rack Template.adg`, `…/MIDI Effect Racks/Rhythmic/Arp Up.adg`, `…/Drum Racks/Acoustic/Ahlimba Kit.adg` (nested Drum Rack) |
| native devices (see catalog) | `Core Library/Defaults/Audio Effects/*.adv`, `Core Library/Devices/**` presets, the 8-Track Template's Compressor / Gate / Channel EQ |

`SKELETON_SOURCES` records file, Creator and sha256 for each; the derivation
is reproducible with `npx --prefix packages/kbot tsx tools/ableton/derive-format-skeletons.mts`
(the script refuses to touch any element that is not present in the source file).

The writer patches names, tempo, time signature, notes, devices and parameters
into these fragments, then renumbers every id in Live's global "pointee" space
(`AutomationTarget`, `ModulationTarget`, `Pointee`, `*ModulationTarget`,
`ControllerTargets.N`, track ids) so all are unique and `NextPointeeId` is
`max + 1` — the invariant observed in every Live-saved set.

## What each module produces

### `als.ts` — Live Set
* `readLiveSet(path | Buffer)` → `{ version, tempo, timeSig, tracks, scenes, locators }`.
  Tracks: `kind` (`midi | audio | return | group | master`), `id`, `name`,
  `color`, mixer state, `devices` (tag, name, on/off, rack chains recursively,
  plug-in / Max patch reference), `sessionClips` (slot, name, length, loop,
  notes), `arrangementClips` (time, …), `takeLaneClips` (Live 11+ comping).
  Notes: `pitch, time, duration, velocity, offVelocity, enabled, probability, velocityDeviation, noteId`.
  Handles Live 12's `MainTrack` and older `MasterTrack`. Time signature is
  decoded from Live's single-int encoding `(num-1) + 99*log2(den)` (4/4 = 201).
* `writeLiveSet(spec)` → gzip `.als` bytes; `buildLiveSetXml(spec)` for the XML.
  Spec: `tempo`, `timeSig`, `tracks[{ kind: midi|audio, name, color, devices, clips[{ slot, name, length, loop, notes }], volume, pan, muted, armed }]`,
  `scenes[]`, `locators[]`. Every set gets Live's two default return tracks
  (A-Reverb, B-Delay), a Main track, ≥ 8 scenes (more if a clip slot needs
  it) and clip slots on every track for each scene.

### `adg.ts` — racks
* `readRack(path | Buffer)` → `{ kind: instrument|audioEffect|midiEffect|drum, name, chains[{ name, devices[], deviceDetails, note, keyRange, velocityRange }], returnChains, macros, allMacros, visibleMacroCount }`. Nested racks are read recursively (`deviceDetails[].rack`).
* `writeRack({ kind, name, chains[{ name, devices, note, chokeGroup, keyRange, velocityRange }], macros })` plus `writeInstrumentRack / writeAudioEffectRack / writeMidiEffectRack / writeDrumRack`. Chain contents are validated against the rack kind (MIDI effects → one instrument → audio effects).

### `adv.ts` — device presets
* `readDevicePreset(path | Buffer)` → `{ tag, device, name, kind, enabled, params }` where `params` maps every parameter path (`PreDrive`, `Bands.0/ParameterA/Freq`, …) to its stored value.
* `writeDevicePreset({ name, params, displayName, enabled })` for any catalog device.

### `devices.ts` — device catalog
Real device XML for: Auto Filter, Chorus-Ensemble, Delay, EQ Eight, Hybrid Reverb, Limiter,
Phaser-Flanger, Reverb, Roar, Saturator, Utility, Compressor, Gate, Channel EQ (audio effects);
Drift, Operator, Wavetable (instruments — Core Library presets, not "init" patches; see `DEVICE_CATALOG[].note`);
Arpeggiator, Note Length, Chord, Pitch, Random, Scale, Velocity (MIDI effects).
`instantiateDevice({ name, params, displayName, enabled })` patches `<Param>/Manual`
values by path and rejects unknown paths with the list of valid ones.

### `midi.ts` — Standard MIDI Files
* `writeMidiFile({ ppq, tempo, timeSig, tracks[{ name, program, notes[{ pitch, start, duration, velocity, channel }] }] })` → SMF type 1 (conductor track with tempo + time-signature meta, one `MTrk` per track, explicit status bytes, end-of-track). Live imports the result by drag-and-drop.
* `readMidiFile(buffer)` → `{ format, ppq, tempo, timeSig, tracks[{ name, program, notes }] }` (type 0/1, running status, note-on velocity 0 = note-off).

### `maxpat.ts` — Max for Live skeletons
* `writeMaxForLiveSkeleton({ name, kind: midi_effect|audio_effect|instrument, useNodeForMax, nodePort })` → `{ maxpat, files }`. The patcher is Max 8/9 JSON (`{"patcher":{"fileversion":1,"appversion":{…},"boxes":[…],"lines":[…]}}`) with `midiin → midiout`, `plugin~ → plugout~`, or `midiin → midiparse → mtof → cycle~ → plugout~`, plus `[live.thisdevice] → [js kbot_liveapi.js]` and, optionally, `[node.script kbot_node.js <port>]`.
* `kbot_liveapi.js`: LiveAPI helper — `get|set|call|describe|children|observe|unobserve <path> : <prop|method> [args]`, JSON replies on outlet 0.
* `kbot_node.js` + `package.json`: Node for Max TCP JSON-lines bridge that forwards LOM requests to the `[js]` box.
* **We do not write `.amxd`.** Live wraps the patcher JSON in a binary container that only Max writes reliably; the emitted README explains the copy-into-a-device-patcher-and-save path.

### `remote-script.ts` — Control Surface scaffold
`writeRemoteScriptScaffold({ name, port })` → `{ folder, files: { '__init__.py', '<module>.py', 'tcp_server.py', 'README.md' } }`,
modelled on `packages/kbot/src/integrations/KBotBridge/*.py`: `create_instance`,
a `ControlSurface` subclass pumping a non-blocking `select` TCP server from a
`schedule_message(1, tick)` loop, actions `ping / tracks / lom_get / lom_set /
lom_call / lom_describe / lom_children` with Max-LiveAPI-style paths.

## What was verified, against which real files

`formats.test.ts` (vitest, 35 tests; the ones needing real files skip when they are absent):

* **Read** `~/Music/Ableton/Factory Packs/Sequencers/Sequencers Demo Set.als`
  (Live 12.2d1): 4 MIDI tracks + Main, tempo 109, 4/4, devices with rack chains
  and Max device names, an arrangement clip with notes, take-lane clips.
* **Read** `DefaultLiveSet.als` from the Live 12 Beta bundle (2 MIDI + 2 audio + 2 returns, 8 scenes, 120 bpm, Reverb/Delay on returns).
* **Write → read back**: a set with 2 MIDI tracks (Drift + Saturator; clip in slot 0 and slot 9), an audio track (Utility + Compressor), 3/4 at 128 bpm, scenes, locators — names, tempo, time signature, devices, mixer values, scenes, locators and every note (pitch/time/duration/velocity/off-velocity/probability) round-trip exactly; the gunzipped XML re-walks with the parser (and `xmllint --noout` when available); every track/pointee id is unique and `NextPointeeId = max + 1`.
* **Shape oracle**: the written MIDI and audio tracks have exactly the element shape of the skeleton *and* of Live's own `Core Library/Defaults/Creating Tracks/{MIDI,Audio} Track/Default *.als` (the tracks Live creates itself); the written clip has the shape of the Quick Start Beat session clip.
* **Racks**: read Core Library `MS Rack Template.adg` (chains Mid/Sides → Utility), `E-Piano Wurli.adg` (Electric → Phaser-Flanger → Reverb → Limiter, macros), `Ahlimba Kit.adg` (nested Drum Rack, 16 pads with notes), Factory Pack `Sequencers/…/Torn Sub.adg`; write instrument / audio-effect / MIDI-effect / drum racks and read them back (chains, devices, macros, key ranges, pad notes, patched parameters).
* **Presets**: read Core Library `Saturator/Basic Soft.adv`; write Saturator/Utility/Drift presets and read them back.
* **Corpus sweep**: every Core Library template set + 150 racks + 150 device presets parse. Run ad hoc on this Mac against everything on disk: 31 `.als`, 2,492 `.adg`, 3,111 `.adv` — 5,634 files, 0 failures (Factory Packs + Core Library + Builtin).
* **MIDI**: variable-length-quantity table (0 … 0x0FFFFFFF), type-1 round trip with chords, retriggers, channels, a 300-beat gap, program change, 6/8 at 128 bpm; a hand-built type-0 file with running status.
* **maxpat**: JSON parses; I/O objects per kind; every patchline references an existing box; Node for Max variant adds `node.script` + `package.json`.
* **Remote Script**: files, `create_instance`, `schedule_message` tick, port, handlers; generated Python passes `python3 -m py_compile`.

Run: `cd packages/kbot && npx vitest run src/ableton/formats && npx tsc --noEmit -p .`

## Known limits

* **Not yet opened in Live.** This task was built offline by contract (Live's
  UDP/TCP ports were off limits). The written `.als`/`.adg`/`.adv` are
  structurally identical to Live-saved files and pass every re-walk, but the
  first real load belongs to the Live phase — open a `writeLiveSet` output
  in Live 12.4 and confirm before relying on it.
* `.als` writer: MIDI and audio tracks only (no group tracks); session MIDI
  clips only (no arrangement clips, no audio clips / sample references, no
  automation envelopes, no MIDI mappings); devices limited to the catalog
  (no plug-ins, no Max devices, no nested racks on tracks); the `Creator`
  attribute is the skeleton's ("Ableton Live 12.4d1") unless overridden.
* `.adg` writer: catalog devices only, no nested racks, no macro→parameter
  mappings, no return chains, no drum-pad sample loading (Simpler/Drum Sampler
  need a sample reference we do not synthesise).
* Instrument skeletons are Core Library presets (Drift "Deep Bass", Operator
  "Tesseract Unpredictable Velocity", Wavetable "Fluffy zap"), so a rack's
  instrument starts from that preset's parameters, not from Live's init patch.
* Reader: `readLiveSet` reads notes from the `KeyTracks` layout (Live 9–12);
  audio-clip warp markers, envelopes and MIDI mappings are not surfaced.
* `.maxpat` only — no `.amxd`; the JS is not run here (Max/Live specific).
* No SMPTE-division MIDI files; SysEx is skipped on read.
