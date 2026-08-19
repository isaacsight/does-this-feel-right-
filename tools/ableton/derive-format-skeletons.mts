/**
 * derive-format-skeletons.mts — regenerate
 * packages/kbot/src/ableton/formats/skeletons.ts from real Live-saved files.
 *
 * Every XML skeleton the format writers clone (.als Live Set, tracks, clip,
 * rack device / branch presets, native device presets) is cut out of a file
 * that Ableton Live itself wrote, then stripped of content (devices, clips,
 * notes) and stateful values. Nothing is invented; the writers only clone and
 * patch these fragments.
 *
 * Sources (all Ableton Live 12.4d1, MinorVersion 12.0_12402, shipped inside
 * the Live 12 Beta app bundle — never touched the running Live process):
 *   Core Library/Templates/Quick Start Beat.als     -> Live Set envelope, MIDI track, return tracks, scene, MIDI clip
 *   Core Library/Templates/8-Track Template.als     -> audio track, Compressor2/Gate/ChannelEq devices
 *   Core Library/Lessons/Demo Songs/... Suite Demo.als -> Locator (arrangement marker)
 *   Core Library/Racks/**                            -> rack device + branch presets (instrument / audio / MIDI / drum)
 *   Core Library/Defaults/Audio Effects/*.adv        -> native audio-effect device skeletons
 *   Core Library/Devices/**                          -> Utility, Drift, Operator, Wavetable, MIDI effects
 *
 * Run from the repo root:
 *   npx --prefix packages/kbot tsx tools/ableton/derive-format-skeletons.mts
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { gunzipSync, gzipSync } from 'node:zlib';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  parseXml, serializeXml, find, findAll, child, childrenOf, clone, walk, value, fmt,
  type XmlNode,
} from '../../packages/kbot/src/ableton/formats/xml.js';

/** Strict setter: only patches elements that already exist in the source file (never invents structure). */
function setValue(node: XmlNode, path: string, v: string | number | boolean): void {
  const target = find(node, path);
  if (!target) throw new Error(`refusing to invent <${path}> under <${node.tag}> — not present in the source file`);
  target.attrs.Value = fmt(v);
}

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, '..', '..', 'packages', 'kbot', 'src', 'ableton', 'formats', 'skeletons.ts');
const APP = process.env.LIVE_APP_RESOURCES
  ?? '/Applications/Ableton Live 12 Beta.app/Contents/App-Resources';
const CL = join(APP, 'Core Library');

interface Source { key: string; file: string; sha256: string; creator: string; minorVersion: string; }
const sources: Source[] = [];
const blobs: Record<string, string> = {};
let rootAttrs: Record<string, string> | undefined;

function load(file: string, key: string): XmlNode {
  const raw = readFileSync(file);
  const xml = gunzipSync(raw).toString('utf8');
  const doc = parseXml(xml);
  const rel = file.startsWith(APP) ? file.slice(APP.length + 1) : file;
  sources.push({
    key, file: rel,
    sha256: createHash('sha256').update(raw).digest('hex'),
    creator: doc.root.attrs.Creator ?? '', minorVersion: doc.root.attrs.MinorVersion ?? '',
  });
  if (!rootAttrs) rootAttrs = { ...doc.root.attrs };
  else if (doc.root.attrs.MinorVersion !== rootAttrs.MinorVersion) {
    throw new Error(`schema mismatch: ${file} is ${doc.root.attrs.MinorVersion}, expected ${rootAttrs.MinorVersion}`);
  }
  return doc.root;
}

function put(key: string, node: XmlNode): void {
  const xml = serializeXml(node, { declaration: false });
  blobs[key] = gzipSync(Buffer.from(xml, 'utf8'), { level: 9 }).toString('base64');
  console.log(`  ${key.padEnd(34)} ${String(xml.length).padStart(7)} bytes xml`);
}

function must<T>(v: T | undefined, what: string): T {
  if (v === undefined) throw new Error(`missing: ${what}`);
  return v;
}

function emptyChildren(n: XmlNode | undefined, what: string): void {
  must(n, what).children = [];
}

/** Zero every pointee-space Id (AutomationTarget/ModulationTarget/Pointee/…) the way .adv/.adg presets do. */
function zeroPointeeIds(n: XmlNode): void {
  walk(n, (x) => {
    if (x.attrs.Id !== undefined && isPointeeTag(x.tag)) x.attrs.Id = '0';
  });
}
function isPointeeTag(tag: string): boolean {
  return tag === 'AutomationTarget' || tag === 'ModulationTarget' || tag === 'Pointee'
    || tag.endsWith('ModulationTarget') || tag.startsWith('ControllerTargets.');
}

// ---------------------------------------------------------------------------
// 1. Live Set pieces
// ---------------------------------------------------------------------------
console.log('Live Set pieces');
const qsb = load(join(CL, 'Templates', 'Quick Start Beat.als'), 'als.set');
const eight = load(join(CL, 'Templates', '8-Track Template.als'), 'als.audioTrack');

{
  const set = clone(qsb);
  const ls = must(child(set, 'LiveSet'), 'LiveSet');
  const tracks = must(child(ls, 'Tracks'), 'Tracks');
  const midiSrc = childrenOf(tracks, 'MidiTrack')[3]; // "4 Synth Keys": no clips, one rack — stripped below
  const returns = childrenOf(tracks, 'ReturnTrack');
  if (returns.length !== 2) throw new Error('expected 2 return tracks');

  // MIDI track skeleton
  const midi = clone(midiSrc);
  stripTrack(midi, 'midi');
  put('als.midiTrack', midi);

  // Return tracks (keep Live's default Reverb / Delay devices — they are Live's own XML)
  put('als.returnTrackA', stripReturn(clone(returns[0])));
  put('als.returnTrackB', stripReturn(clone(returns[1])));

  // Session MIDI clip skeleton: first clip found in the set
  let clipSrc: XmlNode | undefined;
  for (const t of childrenOf(tracks, 'MidiTrack')) {
    for (const slot of findAll(t, 'DeviceChain/MainSequencer/ClipSlotList/ClipSlot')) {
      const c = find(slot, 'ClipSlot/Value/MidiClip');
      if (c) { clipSrc = c; break; }
    }
    if (clipSrc) break;
  }
  const clip = clone(must(clipSrc, 'session MidiClip'));
  emptyChildren(find(clip, 'Notes/KeyTracks'), 'KeyTracks');
  emptyChildren(find(clip, 'Notes/PerNoteEventStore/EventLists'), 'EventLists');
  emptyChildren(find(clip, 'Notes/NoteProbabilityGroups'), 'NoteProbabilityGroups');
  setValue(clip, 'Notes/NoteIdGenerator/NextId', 1);
  setValue(clip, 'Notes/ProbabilityGroupIdGenerator/NextId', 1);
  emptyChildren(find(clip, 'Envelopes/Envelopes'), 'clip Envelopes');
  setValue(clip, 'Name', '');
  setValue(clip, 'Annotation', '');
  setValue(clip, 'TimeSelection/AnchorTime', 0);
  setValue(clip, 'TimeSelection/OtherTime', 0);
  setValue(clip, 'ScrollerTimePreserver/LeftTime', 0);
  setValue(clip, 'IsInKey', false);
  clip.attrs.Id = '0';
  clip.attrs.Time = '0';
  put('als.midiClip', clip);

  // Scene skeleton
  const scenes = must(child(ls, 'Scenes'), 'Scenes');
  const scene = clone(must(childrenOf(scenes, 'Scene')[0], 'Scene'));
  scene.attrs.Id = '0';
  setValue(scene, 'Name', '');
  setValue(scene, 'Annotation', '');
  setValue(scene, 'Color', -1);
  setValue(scene, 'LomId', 0);
  put('als.scene', scene);

  // Set envelope: no tracks, no scenes, neutral transport / view state
  tracks.children = [];
  scenes.children = [];
  setValue(ls, 'LomId', 0);
  setValue(ls, 'LomIdView', 0);
  setValue(ls, 'Transport/CurrentTime', 0);
  setValue(ls, 'Transport/LoopStart', 8);
  setValue(ls, 'Transport/LoopLength', 16);
  setValue(ls, 'Transport/LoopOn', false);
  setValue(ls, 'ScaleInformation/Root', 0);
  setValue(ls, 'ScaleInformation/Name', 0);
  setValue(ls, 'InKey', false);
  setValue(ls, 'HighlightedTrackIndex', 0);
  setValue(ls, 'SelectedDocumentViewInMainWindow', 0);
  emptyChildren(find(ls, 'Locators/Locators'), 'Locators');
  emptyChildren(find(ls, 'GroovePool/Grooves'), 'Grooves');
  setValue(ls, 'ViewStates/SessionIO', 1);
  // MainTrack: keep as-is (no devices in this source); reset selection state
  const main = must(child(ls, 'MainTrack'), 'MainTrack');
  setValue(main, 'IsContentSelectedInDocument', false);
  emptyChildren(find(main, 'AutomationEnvelopes/Envelopes'), 'main envelopes');
  emptyChildren(find(main, 'DeviceChain/DeviceChain/Devices'), 'main devices');
  put('als.set', set);
}

{
  const ls = must(child(eight, 'LiveSet'), 'LiveSet');
  const src = must(childrenOf(must(child(ls, 'Tracks'), 'Tracks'), 'AudioTrack')[0], 'AudioTrack');
  const audio = clone(src);
  stripTrack(audio, 'audio');
  // Match Live's own "Default Audio Track.als" (Core Library/Defaults/Creating Tracks): monitor Off, latency kept
  setValue(audio, 'DeviceChain/MainSequencer/MonitoringEnum', 2);
  setValue(audio, 'DeviceChain/MainSequencer/KeepRecordMonitoringLatency', true);
  // This source set numbers its send holders 0/2; the Quick Start Beat envelope numbers them 0/1.
  const holders = findAll(audio, 'DeviceChain/Mixer/Sends/TrackSendHolder');
  holders.forEach((h, i) => { h.attrs.Id = String(i); });
  put('als.audioTrack', audio);
}

// Locator (arrangement marker) skeleton — the Quick Start templates carry none, the demo song does
{
  const demo = load(join(CL, 'Lessons', 'Demo Songs', 'Chuck Sutton - Patience (Live 12 Suite Demo).als'), 'als.locator');
  const loc = clone(must(find(demo, 'LiveSet/Locators/Locators/Locator'), 'Locator'));
  loc.attrs.Id = '0';
  setValue(loc, 'LomId', 0);
  setValue(loc, 'Time', 0);
  setValue(loc, 'Name', '');
  setValue(loc, 'Annotation', '');
  setValue(loc, 'IsSongStart', false);
  put('als.locator', loc);
}

function stripTrack(t: XmlNode, kind: 'midi' | 'audio'): void {
  t.attrs.Id = '0';
  for (const k of Object.keys(t.attrs)) if (k !== 'Id') delete t.attrs[k]; // SelectedToolPanel etc.
  setValue(t, 'LomId', 0);
  setValue(t, 'LomIdView', 0);
  setValue(t, 'IsContentSelectedInDocument', false);
  setValue(t, 'Name/EffectiveName', '');
  setValue(t, 'Name/UserName', '');
  setValue(t, 'Name/Annotation', '');
  setValue(t, 'Name/MemorizedFirstClipName', '');
  setValue(t, 'Color', 0);
  setValue(t, 'TrackUnfolded', true);
  setValue(t, 'TrackGroupId', -1);
  setValue(t, 'SavedPlayingSlot', -1);
  setValue(t, 'SavedPlayingOffset', 0);
  setValue(t, 'Freeze', false);
  setValue(t, 'ViewData', '{}');
  // fresh-track view state (values as in Core Library/Defaults/Creating Tracks/*.als)
  setValue(t, 'DeviceChain/ClipEnvelopeChooserViewState/SelectedDevice', 1);
  setValue(t, 'DeviceChain/ClipEnvelopeChooserViewState/SelectedEnvelope', 0);
  for (const dev of ['Mixer', 'MainSequencer', 'FreezeSequencer']) {
    const d = find(t, `DeviceChain/${dev}`);
    if (!d) continue;
    setValue(d, 'LastSelectedClipEnvelopeIndex', 0);
    setValue(d, 'LastSelectedTimeableIndex', 0);
    setValue(d, 'ShouldShowPresetName', false);
  }
  emptyChildren(find(t, 'AutomationEnvelopes/Envelopes'), 'track envelopes');
  emptyChildren(find(t, 'TakeLanes/TakeLanes'), 'take lanes');
  emptyChildren(find(t, 'DeviceChain/DeviceChain/Devices'), 'devices');
  // Live keeps one visible automation lane per track: keep the first source lane, reset its state
  const lanes = must(find(t, 'DeviceChain/AutomationLanes/AutomationLanes'), 'lanes');
  const lane = must(lanes.children[0], 'first automation lane');
  lanes.children = [lane];
  lane.attrs.Id = '0';
  setValue(lane, 'SelectedDevice', 1);
  setValue(lane, 'SelectedEnvelope', 0);
  setValue(lane, 'IsContentSelectedInDocument', false);
  setValue(lane, 'LaneHeight', 68);
  for (const seq of ['MainSequencer', 'FreezeSequencer']) {
    const s = find(t, `DeviceChain/${seq}`);
    if (!s) continue;
    for (const slot of findAll(s, 'ClipSlotList/ClipSlot')) {
      emptyChildren(find(slot, 'ClipSlot/Value'), 'slot value');
      setValue(slot, 'HasStop', true);
      setValue(slot, 'LomId', 0);
    }
    const arrMidi = find(s, 'ClipTimeable/ArrangerAutomation/Events');
    if (arrMidi) arrMidi.children = [];
    const arrAudio = find(s, 'Sample/ArrangerAutomation/Events');
    if (arrAudio) arrAudio.children = [];
    const rec = find(s, 'Recorder');
    if (rec) { setValue(rec, 'IsArmed', false); setValue(rec, 'TakeCounter', 0); }
    setValue(s, 'LomId', 0);
    setValue(s, 'ViewData', '{}');
  }
  const mixer = must(find(t, 'DeviceChain/Mixer'), 'mixer');
  setValue(mixer, 'Volume/Manual', 1);
  setValue(mixer, 'Volume/LomId', 0);
  setValue(mixer, 'Pan/Manual', 0);
  setValue(mixer, 'Speaker/Manual', true);
  for (const h of findAll(mixer, 'Sends/TrackSendHolder')) setValue(h, 'Send/Manual', 0.0003162277571);
}

function stripReturn(t: XmlNode): XmlNode {
  setValue(t, 'IsContentSelectedInDocument', false);
  emptyChildren(find(t, 'AutomationEnvelopes/Envelopes'), 'return envelopes');
  emptyChildren(find(t, 'TakeLanes/TakeLanes'), 'return take lanes');
  return t;
}

// ---------------------------------------------------------------------------
// 2. Rack pieces
// ---------------------------------------------------------------------------
console.log('Rack pieces');
const rackSources: Array<[string, string]> = [
  ['instrument', join(CL, 'Racks', 'Instrument Racks', 'Piano & Keys', 'E-Piano Wurli.adg')],
  ['audioEffect', join(CL, 'Racks', 'Audio Effect Racks', 'Mixing & Mastering', 'MS Rack Template.adg')],
  ['midiEffect', join(CL, 'Racks', 'MIDI Effect Racks', 'Rhythmic', 'Arp Up.adg')],
];
const catalog: Array<{ name: string; tag: string; kind: 'instrument' | 'audio_effect' | 'midi_effect'; source: string; note?: string }> = [];

function stripRackDevice(dev: XmlNode): XmlNode {
  zeroPointeeIds(dev);
  dev.attrs.Id = '0';
  setValue(dev, 'LomId', 0);
  setValue(dev, 'LomIdView', 0);
  setValue(dev, 'UserName', '');
  setValue(dev, 'Annotation', '');
  setValue(dev, 'IsExpanded', true);
  setValue(dev, 'IsFolded', false);
  setValue(dev, 'ViewData', '{}');
  emptyChildren(find(dev, 'Branches'), 'Branches');
  emptyChildren(find(dev, 'ReturnBranches'), 'ReturnBranches');
  emptyChildren(find(dev, 'MacroVariations/MacroSnapshots'), 'MacroSnapshots');
  // LastPresetRef -> empty (a fresh, unsaved rack)
  const lpr = must(find(dev, 'LastPresetRef'), 'LastPresetRef');
  lpr.children = [{ tag: 'Value', attrs: {}, children: [] }];
  for (let i = 0; i < 16; i++) {
    setValue(dev, `MacroDisplayNames.${i}`, `Macro ${i + 1}`);
    setValue(dev, `MacroControls.${i}/Manual`, 0);
    setValue(dev, `MacroDefaults.${i}`, -1);
    setValue(dev, `MacroAnnotations.${i}`, '');
    const mc = find(dev, `MacroColor.${i}`);
    if (mc) mc.attrs.Value = '0';
  }
  setValue(dev, 'NumVisibleMacroControls', 8);
  setValue(dev, 'AreMacroControlsVisible', true);
  setValue(dev, 'IsBranchesListVisible', true);
  const sel = find(dev, 'ChainSelector/Manual');
  if (sel) sel.attrs.Value = '0';
  return dev;
}

function stripBranch(bp: XmlNode): XmlNode {
  zeroPointeeIds(bp);
  bp.attrs.Id = '0';
  setValue(bp, 'Name', '');
  setValue(bp, 'IsSoloed', false);
  emptyChildren(find(bp, 'DevicePresets'), 'DevicePresets');
  setValue(bp, 'AutoColored', true);
  const mixerDev = find(bp, 'MixerPreset/AbletonDevicePreset/Device');
  if (mixerDev) {
    for (const d of mixerDev.children) {
      const vol = find(d, 'Volume/Manual'); if (vol) vol.attrs.Value = '1';
      const pan = find(d, 'Panorama/Manual'); if (pan) pan.attrs.Value = '0';
      const spk = find(d, 'Speaker/Manual'); if (spk) spk.attrs.Value = 'true';
      const sends = find(d, 'SendInfos'); if (sends) sends.children = [];
      const lpr = find(d, 'LastPresetRef'); if (lpr) lpr.children = [{ tag: 'Value', attrs: {}, children: [] }];
    }
  }
  return bp;
}

let devicePresetWrapper: XmlNode | undefined;
let groupPresetOverwrite = '3077';

for (const [kind, file] of rackSources) {
  const root = load(file, `rack.${kind}`);
  const gd = must(child(root, 'GroupDevicePreset'), 'GroupDevicePreset');
  groupPresetOverwrite = value(gd, 'OverwriteProtectionNumber') ?? groupPresetOverwrite;
  const dev = clone(must(child(gd, 'Device'), 'Device').children[0]);
  put(`rack.${kind}.device`, stripRackDevice(dev));
  const bps = must(child(gd, 'BranchPresets'), 'BranchPresets');
  const bp = clone(must(bps.children[0], 'branch preset'));
  // harvest devices from the branch before stripping it
  const presets = findAll(bp, 'DevicePresets/AbletonDevicePreset');
  if (!devicePresetWrapper && presets.length) {
    const w = clone(presets[0]);
    emptyChildren(find(w, 'Device'), 'wrapper Device');
    // PresetRef -> AbletonDefaultPresetRef with an empty FileRef (pattern from Live's own nested-rack presets)
    w.children = w.children.filter((c) => c.tag !== 'PresetRef');
    w.children.push(parseXml(`<PresetRef><AbletonDefaultPresetRef Id="0"><FileRef><RelativePathType Value="0" /><RelativePath Value="" /><Path Value="" /><Type Value="2" /><LivePackName Value="" /><LivePackId Value="" /><OriginalFileSize Value="0" /><OriginalCrc Value="0" /><SourceHint Value="" /></FileRef><DeviceId Name="DEVICE" /></AbletonDefaultPresetRef></PresetRef>`).root);
    devicePresetWrapper = w;
  }
  if (kind === 'midiEffect') {
    for (const p of presets) {
      const d = must(child(p, 'Device'), 'Device').children[0];
      const name = { MidiArpeggiator: 'Arpeggiator', MidiNoteLength: 'Note Length' }[d.tag];
      if (name) addDevice(name, clone(d), 'midi_effect', file);
    }
  }
  put(`rack.${kind}.branch`, stripBranch(bp));
}

// Drum rack: nested inside an Instrument Rack in the Core Library
{
  const file = join(CL, 'Racks', 'Drum Racks', 'Acoustic', 'Ahlimba Kit.adg');
  const root = load(file, 'rack.drum');
  const nested = must(find(root, 'GroupDevicePreset/BranchPresets/InstrumentBranchPreset/DevicePresets/GroupDevicePreset'), 'nested drum GroupDevicePreset');
  const dev = clone(must(child(nested, 'Device'), 'Device').children[0]);
  if (dev.tag !== 'DrumGroupDevice') throw new Error('expected DrumGroupDevice');
  put('rack.drum.device', stripRackDevice(dev));
  const bp = clone(must(child(nested, 'BranchPresets'), 'BranchPresets').children[0]);
  if (bp.tag !== 'DrumBranchPreset') throw new Error('expected DrumBranchPreset');
  stripBranch(bp);
  setValue(bp, 'ZoneSettings/ReceivingNote', 60);
  setValue(bp, 'ZoneSettings/SendingNote', 60);
  setValue(bp, 'ZoneSettings/ChokeGroup', 0);
  put('rack.drum.branch', bp);
}
put('rack.devicePreset', must(devicePresetWrapper, 'device preset wrapper'));

// ---------------------------------------------------------------------------
// 3. Native device catalog
// ---------------------------------------------------------------------------
console.log('Device catalog');
function addDevice(name: string, dev: XmlNode, kind: 'instrument' | 'audio_effect' | 'midi_effect', source: string, note?: string): void {
  zeroPointeeIds(dev);
  dev.attrs.Id = '0';
  setValue(dev, 'LomId', 0);
  setValue(dev, 'LomIdView', 0);
  setValue(dev, 'UserName', '');
  setValue(dev, 'Annotation', '');
  setValue(dev, 'IsFolded', false);
  const lpr = find(dev, 'LastPresetRef');
  if (lpr) lpr.children = [{ tag: 'Value', attrs: {}, children: [] }];
  const sc = find(dev, 'SourceContext');
  if (sc) sc.children = [{ tag: 'Value', attrs: {}, children: [] }];
  const rel = source.startsWith(APP) ? source.slice(APP.length + 1) : source;
  catalog.push({ name, tag: dev.tag, kind, source: rel, ...(note ? { note } : {}) });
  put(`device.${dev.tag}`, dev);
}

function loadPresetDevice(name: string, file: string, kind: 'instrument' | 'audio_effect' | 'midi_effect', note?: string, patch?: (d: XmlNode) => void): void {
  const root = load(file, `device.${name}`);
  const dev = clone(root.children[0]);
  if (patch) patch(dev);
  addDevice(name, dev, kind, file, note);
}

const DEFAULTS = join(CL, 'Defaults', 'Audio Effects');
loadPresetDevice('Auto Filter', join(DEFAULTS, 'Auto Filter.adv'), 'audio_effect');
loadPresetDevice('Chorus-Ensemble', join(DEFAULTS, 'Chorus-Ensemble.adv'), 'audio_effect');
loadPresetDevice('Delay', join(DEFAULTS, 'Delay.adv'), 'audio_effect');
loadPresetDevice('EQ Eight', join(DEFAULTS, 'EQ Eight.adv'), 'audio_effect');
loadPresetDevice('Hybrid Reverb', join(DEFAULTS, 'Hybrid Reverb.adv'), 'audio_effect');
loadPresetDevice('Limiter', join(DEFAULTS, 'Limiter.adv'), 'audio_effect');
loadPresetDevice('Phaser-Flanger', join(DEFAULTS, 'Phaser-Flanger.adv'), 'audio_effect');
loadPresetDevice('Reverb', join(DEFAULTS, 'Reverb.adv'), 'audio_effect');
loadPresetDevice('Roar', join(DEFAULTS, 'Roar.adv'), 'audio_effect');
loadPresetDevice('Saturator', join(DEFAULTS, 'Saturator.adv'), 'audio_effect');
loadPresetDevice('Utility', join(CL, 'Devices', 'Audio Effects', 'Utility', 'Mono.adv'), 'audio_effect',
  'Core Library "Mono" preset with Mono=false, i.e. a neutral stereo Utility',
  (d) => { setValue(d, 'Mono/Manual', false); setValue(d, 'ChannelMode/Manual', 1); setValue(d, 'StereoWidth/Manual', 1); });

// Compressor / Gate / Channel EQ from the 8-Track Template's audio tracks (no Defaults file exists for them)
{
  const ls = must(child(eight, 'LiveSet'), 'LiveSet');
  const want: Record<string, string> = { Compressor2: 'Compressor', Gate: 'Gate', ChannelEq: 'Channel EQ' };
  const seen = new Set<string>();
  for (const t of childrenOf(must(child(ls, 'Tracks'), 'Tracks'), 'AudioTrack')) {
    for (const d of findAll(t, 'DeviceChain/DeviceChain/Devices/AudioEffectGroupDevice')) {
      // devices sit inside racks in this template: dig into branches
      for (const inner of findAll(d, 'Branches/AudioEffectBranch')) {
        for (const dd of must(find(inner, 'DeviceChain/AudioToAudioDeviceChain/Devices'), 'chain devices').children) {
          if (want[dd.tag] && !seen.has(dd.tag)) { seen.add(dd.tag); addDevice(want[dd.tag], clone(dd), 'audio_effect', join(CL, 'Templates', '8-Track Template.als'), 'default parameters as saved in the 8-Track Template'); }
        }
      }
    }
    for (const dd of findAll(t, 'DeviceChain/DeviceChain/Devices/*')) void dd;
    for (const dd of must(find(t, 'DeviceChain/DeviceChain/Devices'), 'devices').children) {
      if (want[dd.tag] && !seen.has(dd.tag)) { seen.add(dd.tag); addDevice(want[dd.tag], clone(dd), 'audio_effect', join(CL, 'Templates', '8-Track Template.als'), 'default parameters as saved in the 8-Track Template'); }
    }
  }
  for (const tag of Object.keys(want)) if (!seen.has(tag)) console.warn(`  (warn) ${tag} not found in 8-Track Template`);
}

// Instruments (Core Library presets; a preset, not an "init" patch — documented in the catalog note)
loadPresetDevice('Drift', join(CL, 'Devices', 'Instruments', 'Drift', 'Bass', 'Deep Bass.adv'), 'instrument', 'Core Library preset "Deep Bass"');
loadPresetDevice('Operator', join(CL, 'Devices', 'Instruments', 'Operator', 'Effects', 'Tesseract Unpredictable Velocity.adv'), 'instrument', 'Core Library preset "Tesseract Unpredictable Velocity"');
loadPresetDevice('Wavetable', join(CL, 'Devices', 'Instruments', 'Wavetable', 'Percussive', 'Fluffy zap.adv'), 'instrument', 'Core Library preset "Fluffy zap"');

// MIDI effects (smallest Core Library preset per device)
const ME = join(CL, 'Devices', 'MIDI Effects');
loadPresetDevice('Chord', join(ME, 'Chord', pickSmallest(join(ME, 'Chord'))), 'midi_effect', 'Core Library preset');
loadPresetDevice('Pitch', join(ME, 'Pitch', pickSmallest(join(ME, 'Pitch'))), 'midi_effect', 'Core Library preset');
loadPresetDevice('Random', join(ME, 'Random', pickSmallest(join(ME, 'Random'))), 'midi_effect', 'Core Library preset');
loadPresetDevice('Scale', join(ME, 'Scale', pickSmallest(join(ME, 'Scale'))), 'midi_effect', 'Core Library preset');
loadPresetDevice('Velocity', join(ME, 'Velocity', pickSmallest(join(ME, 'Velocity'))), 'midi_effect', 'Core Library preset');

function pickSmallest(dir: string): string {
  const files = readdirSync(dir).filter((f) => f.endsWith('.adv'));
  files.sort((a, b) => statSync(join(dir, a)).size - statSync(join(dir, b)).size);
  if (!files.length) throw new Error(`no .adv in ${dir}`);
  return files[0];
}

// ---------------------------------------------------------------------------
// 4. Emit skeletons.ts
// ---------------------------------------------------------------------------
const lines: string[] = [];
lines.push('/* GENERATED FILE — do not edit by hand.');
lines.push(' * Regenerate with: npx --prefix packages/kbot tsx tools/ableton/derive-format-skeletons.mts');
lines.push(' *');
lines.push(' * Every blob below is a fragment of XML cut out of a file that Ableton Live');
lines.push(' * itself saved (see SKELETON_SOURCES for the file, its Creator and sha256),');
lines.push(' * stripped of content and gzip+base64 encoded. The format writers clone and');
lines.push(' * patch these fragments; they never synthesise Live XML from scratch.');
lines.push(` * Generated ${new Date().toLocaleDateString('sv-SE')} (local date).`);
lines.push(' */');
lines.push("import { gunzipSync } from 'node:zlib';");
lines.push('');
lines.push('/** Attributes of the <Ableton> root element of every source file. */');
lines.push(`export const ABLETON_ROOT_ATTRS: Record<string, string> = ${JSON.stringify(rootAttrs, null, 2)};`);
lines.push('');
lines.push(`export const GROUP_PRESET_OVERWRITE_PROTECTION = ${JSON.stringify(groupPresetOverwrite)};`);
lines.push('');
lines.push('export interface SkeletonSource { key: string; file: string; sha256: string; creator: string; minorVersion: string; }');
lines.push(`export const SKELETON_SOURCES: SkeletonSource[] = ${JSON.stringify(sources, null, 2)};`);
lines.push('');
lines.push("export type DeviceKind = 'instrument' | 'audio_effect' | 'midi_effect';");
lines.push('export interface CatalogDevice { name: string; tag: string; kind: DeviceKind; source: string; note?: string; }');
lines.push(`export const DEVICE_CATALOG: CatalogDevice[] = ${JSON.stringify(catalog, null, 2)};`);
lines.push('');
lines.push('const BLOBS: Record<string, string> = {');
for (const k of Object.keys(blobs)) lines.push(`  ${JSON.stringify(k)}: ${JSON.stringify(blobs[k])},`);
lines.push('};');
lines.push('');
lines.push('export const SKELETON_KEYS: string[] = Object.keys(BLOBS);');
lines.push('');
lines.push('const cache = new Map<string, string>();');
lines.push('');
lines.push('/** Decompressed XML text of a skeleton fragment. Throws for unknown keys. */');
lines.push('export function skeletonXml(key: string): string {');
lines.push('  const hit = cache.get(key);');
lines.push('  if (hit !== undefined) return hit;');
lines.push('  const b64 = BLOBS[key];');
lines.push("  if (b64 === undefined) throw new Error(`unknown skeleton: ${key}`);");
lines.push("  const xml = gunzipSync(Buffer.from(b64, 'base64')).toString('utf8');");
lines.push('  cache.set(key, xml);');
lines.push('  return xml;');
lines.push('}');
lines.push('');
writeFileSync(OUT, lines.join('\n'));
console.log(`wrote ${OUT} (${(lines.join('\n').length / 1024).toFixed(1)} KB)`);
