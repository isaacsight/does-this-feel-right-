/**
 * als.ts — Ableton Live Set (.als) reader and writer.
 *
 * A .als is gzip-compressed XML:
 *   <Ableton MajorVersion Creator ...><LiveSet><Tracks><MidiTrack Id=…>…
 *
 * readLiveSet() turns any Live 9–12 set into a plain structure (tracks,
 * devices, session + arrangement clips with notes, scenes, locators, tempo).
 *
 * writeLiveSet() produces a minimal but valid Live 12 set by cloning XML
 * fragments that Live itself saved (see skeletons.ts / SKELETON_SOURCES) and
 * patching names, tempo, tracks, devices and session MIDI clips into them.
 * Nothing is synthesised from scratch except note events and locators, whose
 * element shapes are copied from real files.
 */
import { readFileSync } from 'node:fs';
import { gunzipSync, gzipSync } from 'node:zlib';
import {
  parseXml, serializeXml, find, findAll, child, childrenOf, clone, setValue, value, numberValue,
  boolValue, elements, valueEl, el, type XmlNode, type XmlDoc,
} from './xml.js';
import { skeletonXml, ABLETON_ROOT_ATTRS } from './skeletons.js';
import {
  instantiateDevice, deviceDisplayName, isRackTag, renumberPointees, IdCounter,
  type DeviceSpec,
} from './devices.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface LiveSetVersion {
  major: number;
  minor: string;
  schemaChangeCount?: number;
  creator: string;
  revision?: string;
}

export interface TimeSignature { numerator: number; denominator: number; }

export interface LiveNote {
  pitch: number;
  /** Beats from clip start. */
  time: number;
  /** Beats. */
  duration: number;
  velocity: number;
  offVelocity?: number;
  /** Live 11+ per-note fields, present only when they differ from defaults. */
  enabled?: boolean;
  probability?: number;
  velocityDeviation?: number;
  noteId?: number;
}

export interface LiveClip {
  kind: 'midi' | 'audio';
  /** Session clips: slot index. */
  slot?: number;
  /** Arrangement clips: start time in beats. */
  time?: number;
  name: string;
  color?: number;
  /** Playing length in beats (loop length when looping, else end-start). */
  length: number;
  start: number;
  end: number;
  loop: { start: number; end: number; on: boolean };
  notes: LiveNote[];
  /** Audio clips: referenced sample. */
  sample?: { path?: string; relativePath?: string; name?: string };
}

export interface LiveDevice {
  tag: string;
  name: string;
  /** Live's display name for the tag when different from `name` (name = UserName if set). */
  displayName: string;
  enabled?: boolean;
  /** Racks: chains with nested devices. */
  chains?: LiveChain[];
  /** Plug-ins / Max devices: the plug-in or patch identifier. */
  ref?: string;
}

export interface LiveChain {
  name: string;
  devices: LiveDevice[];
  /** Drum pads. */
  note?: number;
  outNote?: number;
  chokeGroup?: number;
}

export type LiveTrackKind = 'midi' | 'audio' | 'return' | 'group' | 'master';

export interface LiveTrack {
  kind: LiveTrackKind;
  id: number;
  name: string;
  color?: number;
  groupId?: number;
  muted?: boolean;
  soloed?: boolean;
  armed?: boolean;
  volume?: number;
  pan?: number;
  devices: LiveDevice[];
  sessionClips: LiveClip[];
  arrangementClips: LiveClip[];
  /** Clips sitting in comping take lanes (Live 11+), with their lane index. */
  takeLaneClips?: Array<LiveClip & { lane: number }>;
}

export interface LiveScene { name: string; color?: number; tempo?: number; tempoEnabled?: boolean; }
export interface LiveLocator { name: string; time: number; }

export interface LiveSet {
  version: LiveSetVersion;
  tempo: number;
  timeSig: TimeSignature;
  tracks: LiveTrack[];
  scenes: LiveScene[];
  locators: LiveLocator[];
}

// ---------------------------------------------------------------------------
// Time signature encoding (Live stores one int: (num-1) + 99*log2(den))
// ---------------------------------------------------------------------------

export function encodeTimeSignature(ts: TimeSignature): number {
  const num = Math.max(1, Math.min(99, Math.round(ts.numerator)));
  const den = Math.round(ts.denominator);
  const log = Math.log2(den);
  if (!Number.isInteger(log) || log < 0 || log > 4) {
    throw new Error(`time signature denominator must be 1, 2, 4, 8 or 16 (got ${ts.denominator})`);
  }
  return (num - 1) + 99 * log;
}

export function decodeTimeSignature(v: number): TimeSignature {
  const log = Math.floor(v / 99);
  return { numerator: (v % 99) + 1, denominator: 2 ** log };
}

// ---------------------------------------------------------------------------
// Load helpers
// ---------------------------------------------------------------------------

const GZIP_MAGIC_0 = 0x1f;
const GZIP_MAGIC_1 = 0x8b;

/** Read a .als/.adg/.adv file (or buffer) and return its XML text. */
export function readAbletonXml(input: string | Buffer): string {
  const buf = typeof input === 'string' ? readFileSync(input) : input;
  if (buf.length >= 2 && buf[0] === GZIP_MAGIC_0 && buf[1] === GZIP_MAGIC_1) {
    return gunzipSync(buf).toString('utf8');
  }
  return buf.toString('utf8');
}

export function parseAbletonDoc(input: string | Buffer): XmlDoc {
  const doc = parseXml(readAbletonXml(input));
  if (doc.root.tag !== 'Ableton') {
    throw new Error(`not an Ableton document: root element is <${doc.root.tag}>`);
  }
  return doc;
}

export function readVersion(root: XmlNode): LiveSetVersion {
  const a = root.attrs;
  return {
    major: Number(a.MajorVersion ?? 0),
    minor: a.MinorVersion ?? '',
    ...(a.SchemaChangeCount !== undefined ? { schemaChangeCount: Number(a.SchemaChangeCount) } : {}),
    creator: a.Creator ?? '',
    ...(a.Revision !== undefined ? { revision: a.Revision } : {}),
  };
}

// ---------------------------------------------------------------------------
// Reader
// ---------------------------------------------------------------------------

export function readLiveSet(input: string | Buffer): LiveSet {
  const doc = parseAbletonDoc(input);
  const root = doc.root;
  const ls = child(root, 'LiveSet');
  if (!ls) throw new Error('not a Live Set: no <LiveSet> element');

  // Live 12 renamed MasterTrack -> MainTrack.
  const master = child(ls, 'MainTrack') ?? child(ls, 'MasterTrack');
  const mixer = find(master, 'DeviceChain/Mixer');
  const tempo = numberValue(mixer, 'Tempo/Manual') ?? 120;
  const tsRaw = numberValue(mixer, 'TimeSignature/Manual');
  const timeSig = tsRaw === undefined ? { numerator: 4, denominator: 4 } : decodeTimeSignature(tsRaw);

  const tracks: LiveTrack[] = [];
  for (const t of elements(child(ls, 'Tracks') ?? el('Tracks'))) {
    const kind = trackKind(t.tag);
    if (!kind) continue;
    tracks.push(readTrack(t, kind));
  }
  if (master) tracks.push(readTrack(master, 'master'));

  const scenes: LiveScene[] = childrenOf(child(ls, 'Scenes'), 'Scene').map((s) => ({
    name: value(s, 'Name') ?? '',
    color: numberValue(s, 'Color'),
    tempo: numberValue(s, 'Tempo'),
    tempoEnabled: boolValue(s, 'IsTempoEnabled'),
  }));

  const locators: LiveLocator[] = findAll(ls, 'Locators/Locators/Locator').map((l) => ({
    name: value(l, 'Name') ?? '',
    time: numberValue(l, 'Time') ?? 0,
  }));

  return { version: readVersion(root), tempo, timeSig, tracks, scenes, locators };
}

function trackKind(tag: string): LiveTrackKind | undefined {
  switch (tag) {
    case 'MidiTrack': return 'midi';
    case 'AudioTrack': return 'audio';
    case 'ReturnTrack': return 'return';
    case 'GroupTrack': return 'group';
    case 'MainTrack': case 'MasterTrack': return 'master';
    default: return undefined;
  }
}

function readTrack(t: XmlNode, kind: LiveTrackKind): LiveTrack {
  const mixer = find(t, 'DeviceChain/Mixer');
  const seq = find(t, 'DeviceChain/MainSequencer');
  const track: LiveTrack = {
    kind,
    id: Number(t.attrs.Id ?? -1),
    name: value(t, 'Name/EffectiveName') ?? value(t, 'Name/UserName') ?? '',
    color: numberValue(t, 'Color'),
    devices: readDevices(find(t, 'DeviceChain/DeviceChain/Devices')),
    sessionClips: [],
    arrangementClips: [],
  };
  const groupId = numberValue(t, 'TrackGroupId');
  if (groupId !== undefined && groupId >= 0) track.groupId = groupId;
  const speaker = boolValue(mixer, 'Speaker/Manual');
  if (speaker !== undefined) track.muted = !speaker;
  const solo = boolValue(mixer, 'SoloSink/Manual') ?? boolValue(t, 'SoloSink');
  if (solo !== undefined) track.soloed = solo;
  const armed = boolValue(seq, 'Recorder/IsArmed');
  if (armed !== undefined) track.armed = armed;
  const vol = numberValue(mixer, 'Volume/Manual');
  if (vol !== undefined) track.volume = vol;
  const pan = numberValue(mixer, 'Pan/Manual');
  if (pan !== undefined) track.pan = pan;

  if (seq) {
    findAll(seq, 'ClipSlotList/ClipSlot').forEach((slot, i) => {
      const v = find(slot, 'ClipSlot/Value');
      for (const c of elements(v ?? el('Value'))) {
        const clip = readClip(c);
        if (clip) { clip.slot = i; track.sessionClips.push(clip); }
      }
    });
    const arrEvents = [
      ...findAll(seq, 'ClipTimeable/ArrangerAutomation/Events/MidiClip'),
      ...findAll(seq, 'Sample/ArrangerAutomation/Events/AudioClip'),
    ];
    for (const c of arrEvents) {
      const clip = readClip(c);
      if (clip) { clip.time = Number(c.attrs.Time ?? clip.start); track.arrangementClips.push(clip); }
    }
    track.arrangementClips.sort((a, b) => (a.time ?? 0) - (b.time ?? 0));
  }
  const lanes = findAll(t, 'TakeLanes/TakeLanes/TakeLane');
  if (lanes.length) {
    const out: Array<LiveClip & { lane: number }> = [];
    lanes.forEach((lane, li) => {
      for (const c of elements(find(lane, 'ClipAutomation/Events') ?? el('Events'))) {
        const clip = readClip(c);
        if (clip) out.push({ ...clip, time: Number(c.attrs.Time ?? clip.start), lane: li });
      }
    });
    if (out.length) track.takeLaneClips = out;
  }
  return track;
}

function readClip(c: XmlNode): LiveClip | undefined {
  if (c.tag !== 'MidiClip' && c.tag !== 'AudioClip') return undefined;
  const start = numberValue(c, 'CurrentStart') ?? 0;
  const end = numberValue(c, 'CurrentEnd') ?? 0;
  const loopStart = numberValue(c, 'Loop/LoopStart') ?? start;
  const loopEnd = numberValue(c, 'Loop/LoopEnd') ?? end;
  const loopOn = boolValue(c, 'Loop/LoopOn') ?? false;
  const clip: LiveClip = {
    kind: c.tag === 'MidiClip' ? 'midi' : 'audio',
    name: value(c, 'Name') ?? '',
    color: numberValue(c, 'Color') ?? numberValue(c, 'ColorIndex'),
    start,
    end,
    loop: { start: loopStart, end: loopEnd, on: loopOn },
    length: loopOn ? loopEnd - loopStart : end - start,
    notes: [],
  };
  if (c.tag === 'MidiClip') clip.notes = readNotes(c);
  else {
    const ref = find(c, 'SampleRef/FileRef');
    if (ref) {
      clip.sample = {
        path: value(ref, 'Path'),
        relativePath: value(ref, 'RelativePath'),
        name: value(ref, 'Name') ?? basename(value(ref, 'RelativePath') ?? value(ref, 'Path') ?? ''),
      };
    }
  }
  return clip;
}

function basename(p: string): string {
  const i = p.lastIndexOf('/');
  return i === -1 ? p : p.slice(i + 1);
}

/** Read notes from a MidiClip (Live 9–12 KeyTracks layout). */
export function readNotes(clip: XmlNode): LiveNote[] {
  const notes: LiveNote[] = [];
  for (const kt of findAll(clip, 'Notes/KeyTracks/KeyTrack')) {
    const pitch = numberValue(kt, 'MidiKey') ?? 60;
    for (const ev of findAll(kt, 'Notes/MidiNoteEvent')) {
      const a = ev.attrs;
      const n: LiveNote = {
        pitch,
        time: Number(a.Time ?? 0),
        duration: Number(a.Duration ?? 0),
        velocity: Number(a.Velocity ?? 100),
      };
      if (a.OffVelocity !== undefined) n.offVelocity = Number(a.OffVelocity);
      if (a.IsEnabled !== undefined) n.enabled = a.IsEnabled === 'true';
      if (a.Probability !== undefined) n.probability = Number(a.Probability);
      if (a.VelocityDeviation !== undefined) n.velocityDeviation = Number(a.VelocityDeviation);
      if (a.NoteId !== undefined) n.noteId = Number(a.NoteId);
      notes.push(n);
    }
  }
  notes.sort((x, y) => x.time - y.time || x.pitch - y.pitch);
  return notes;
}

/** Devices in a <Devices> list, recursing into racks. */
export function readDevices(list: XmlNode | undefined): LiveDevice[] {
  if (!list) return [];
  return elements(list).map(readDevice);
}

export function readDevice(d: XmlNode): LiveDevice {
  const userName = value(d, 'UserName') ?? '';
  const display = deviceDisplayName(d.tag);
  const dev: LiveDevice = { tag: d.tag, name: userName || display, displayName: display };
  const on = boolValue(d, 'On/Manual');
  if (on !== undefined) dev.enabled = on;
  if (d.tag === 'PluginDevice' || d.tag === 'AuPluginDevice') {
    const ref = value(d, 'PluginDesc/VstPluginInfo/PlugName')
      ?? value(d, 'PluginDesc/Vst3PluginInfo/Name')
      ?? value(d, 'PluginDesc/AuPluginInfo/Name');
    if (ref) { dev.ref = ref; if (!userName) dev.name = ref; }
  } else if (d.tag.startsWith('MxDevice')) {
    const ref = value(d, 'PatchSlot/Value/MxPatchRef/FileRef/RelativePath')
      ?? value(d, 'PatchSlot/Value/MxPatchRef/FileRef/Path');
    if (ref) {
      dev.ref = ref;
      if (!userName) dev.name = basename(ref).replace(/\.amxd$/i, '');
    }
  }
  if (isRackTag(d.tag)) dev.chains = readChains(d);
  return dev;
}

function readChains(rack: XmlNode): LiveChain[] {
  const out: LiveChain[] = [];
  for (const b of elements(child(rack, 'Branches') ?? el('Branches'))) {
    const chain: LiveChain = { name: value(b, 'Name/EffectiveName') ?? value(b, 'Name/UserName') ?? '', devices: [] };
    const dc = child(b, 'DeviceChain');
    if (dc) {
      for (const inner of elements(dc)) {
        if (inner.tag.endsWith('DeviceChain')) chain.devices.push(...readDevices(child(inner, 'Devices')));
      }
    }
    const info = child(b, 'BranchInfo');
    if (info) {
      const rn = numberValue(info, 'ReceivingNote'); if (rn !== undefined) chain.note = rn;
      const sn = numberValue(info, 'SendingNote'); if (sn !== undefined) chain.outNote = sn;
      const cg = numberValue(info, 'ChokeGroup'); if (cg !== undefined) chain.chokeGroup = cg;
    }
    out.push(chain);
  }
  return out;
}

// ---------------------------------------------------------------------------
// Writer
// ---------------------------------------------------------------------------

export interface WriteNote {
  pitch: number;
  /** Beats from clip start. */
  time: number;
  /** Beats. */
  duration: number;
  velocity?: number;
  offVelocity?: number;
  enabled?: boolean;
  probability?: number;
}

export interface WriteClipSpec {
  /** Session slot index (0-based). */
  slot: number;
  name?: string;
  /** Loop length in beats. Default: notes rounded up to whole bars (min one bar). */
  length?: number;
  color?: number;
  loop?: boolean;
  notes?: WriteNote[];
}

export interface WriteTrackSpec {
  kind: 'midi' | 'audio';
  name: string;
  color?: number;
  /** Catalog devices to place on the track, in order. */
  devices?: Array<string | DeviceSpec>;
  /** Session MIDI clips (MIDI tracks only). */
  clips?: WriteClipSpec[];
  volume?: number;
  pan?: number;
  muted?: boolean;
  armed?: boolean;
}

export interface WriteLiveSetSpec {
  tempo?: number;
  timeSig?: TimeSignature;
  tracks: WriteTrackSpec[];
  /** Scene names; the set gets max(8, longest track, scenes.length) scenes. */
  scenes?: string[];
  /** Arrangement locators (markers). */
  locators?: Array<{ name: string; time: number }>;
  /** Override the <Ableton Creator> attribute (default: the skeleton's own, Live 12.4d1). */
  creator?: string;
}

const DEFAULT_TRACK_COLORS = [19, 26, 12, 21, 4, 24, 15, 9, 60, 33, 46, 55];
const MIN_SCENES = 8;

/** Build the uncompressed XML of a Live Set from a spec. */
export function buildLiveSetXml(spec: WriteLiveSetSpec): string {
  const doc = parseXml(skeletonXml('als.set'));
  const root = doc.root;
  if (spec.creator) root.attrs.Creator = spec.creator;
  const ls = child(root, 'LiveSet')!;
  const tracksEl = child(ls, 'Tracks')!;
  const scenesEl = child(ls, 'Scenes')!;
  const timeSig = spec.timeSig ?? { numerator: 4, denominator: 4 };
  const beatsPerBar = timeSig.numerator * (4 / timeSig.denominator);
  const tsCode = encodeTimeSignature(timeSig);

  // Scene count
  let sceneCount = Math.max(MIN_SCENES, spec.scenes?.length ?? 0);
  for (const t of spec.tracks) for (const c of t.clips ?? []) sceneCount = Math.max(sceneCount, c.slot + 1);

  const ids = new IdCounter(1);

  // Tracks
  const midiSkel = parseXml(skeletonXml('als.midiTrack')).root;
  const audioSkel = parseXml(skeletonXml('als.audioTrack')).root;
  const clipSkel = parseXml(skeletonXml('als.midiClip')).root;
  spec.tracks.forEach((ts, index) => {
    if (ts.kind !== 'midi' && ts.kind !== 'audio') throw new Error(`track ${index}: kind must be "midi" or "audio"`);
    const t = clone(ts.kind === 'midi' ? midiSkel : audioSkel);
    setValue(t, 'Name/EffectiveName', ts.name);
    setValue(t, 'Name/UserName', ts.name);
    setValue(t, 'Color', ts.color ?? DEFAULT_TRACK_COLORS[index % DEFAULT_TRACK_COLORS.length]);
    const mixer = find(t, 'DeviceChain/Mixer')!;
    if (ts.volume !== undefined) setValue(mixer, 'Volume/Manual', ts.volume);
    if (ts.pan !== undefined) setValue(mixer, 'Pan/Manual', ts.pan);
    if (ts.muted !== undefined) setValue(mixer, 'Speaker/Manual', !ts.muted);
    if (ts.armed !== undefined) setValue(t, 'DeviceChain/MainSequencer/Recorder/IsArmed', ts.armed);
    ensureSlots(t, sceneCount);

    // Devices
    const devList = find(t, 'DeviceChain/DeviceChain/Devices')!;
    (ts.devices ?? []).forEach((d, di) => {
      const dev = instantiateDevice(d);
      dev.attrs.Id = String(di);
      devList.children.push(dev);
    });

    // Session clips
    if (ts.clips?.length) {
      if (ts.kind !== 'midi') throw new Error(`track "${ts.name}": session MIDI clips need a MIDI track`);
      const slots = findAll(t, 'DeviceChain/MainSequencer/ClipSlotList/ClipSlot');
      ts.clips.forEach((cs, ci) => {
        const holder = find(slots[cs.slot], 'ClipSlot/Value')!;
        holder.children = [buildMidiClip(clipSkel, cs, ci, beatsPerBar, tsCode, ts.color ?? DEFAULT_TRACK_COLORS[index % DEFAULT_TRACK_COLORS.length])];
      });
    }
    tracksEl.children.push(t);
  });

  // Return tracks (Live's default A-Reverb / B-Delay, from the skeleton)
  tracksEl.children.push(parseXml(skeletonXml('als.returnTrackA')).root);
  tracksEl.children.push(parseXml(skeletonXml('als.returnTrackB')).root);

  // Scenes
  const sceneSkel = parseXml(skeletonXml('als.scene')).root;
  for (let i = 0; i < sceneCount; i++) {
    const s = clone(sceneSkel);
    s.attrs.Id = String(i);
    setValue(s, 'Name', spec.scenes?.[i] ?? '');
    setValue(s, 'Tempo', spec.tempo ?? 120);
    setValue(s, 'TimeSignatureId', tsCode);
    scenesEl.children.push(s);
  }

  // Locators
  if (spec.locators?.length) {
    const locList = find(ls, 'Locators/Locators')!;
    const locSkel = parseXml(skeletonXml('als.locator')).root;
    spec.locators.forEach((l, i) => {
      const n = clone(locSkel);
      n.attrs.Id = String(i);
      setValue(n, 'Name', l.name);
      setValue(n, 'Time', l.time);
      locList.children.push(n);
    });
  }

  // Tempo / time signature live on the main track's mixer
  const main = child(ls, 'MainTrack')!;
  setValue(main, 'DeviceChain/Mixer/Tempo/Manual', spec.tempo ?? 120);
  setValue(main, 'DeviceChain/Mixer/TimeSignature/Manual', tsCode);

  // Ids: tracks first (1..n), then every pointee gets a fresh unique id; NextPointeeId = last + 1
  for (const t of elements(tracksEl)) t.attrs.Id = String(ids.take());
  for (const t of elements(tracksEl)) renumberPointees(t, ids);
  renumberPointees(main, ids);
  const preHear = child(ls, 'PreHearTrack');
  if (preHear) renumberPointees(preHear, ids);
  for (const c of elements(ls)) {
    if (c.tag === 'Tracks' || c.tag === 'MainTrack' || c.tag === 'PreHearTrack') continue;
    renumberPointees(c, ids);
  }
  setValue(ls, 'NextPointeeId', ids.next);

  return serializeXml(doc);
}

/** Make sure a track has `count` clip slots in its main + freeze sequencers. */
function ensureSlots(track: XmlNode, count: number): void {
  for (const seqName of ['MainSequencer', 'FreezeSequencer']) {
    const list = find(track, `DeviceChain/${seqName}/ClipSlotList`);
    if (!list) continue;
    const slots = childrenOf(list, 'ClipSlot');
    if (slots.length === 0) continue; // return-style sequencer without slots
    const template = slots[0];
    while (childrenOf(list, 'ClipSlot').length < count) {
      const s = clone(template);
      s.attrs.Id = String(childrenOf(list, 'ClipSlot').length);
      const v = find(s, 'ClipSlot/Value');
      if (v) v.children = [];
      list.children.push(s);
    }
  }
}

function buildMidiClip(skel: XmlNode, cs: WriteClipSpec, clipId: number, beatsPerBar: number, tsCode: number, fallbackColor: number): XmlNode {
  const clip = clone(skel);
  const notes = [...(cs.notes ?? [])];
  for (const n of notes) {
    if (!Number.isFinite(n.pitch) || n.pitch < 0 || n.pitch > 127) throw new Error(`note pitch out of range: ${n.pitch}`);
    if (!(n.duration > 0)) throw new Error(`note duration must be > 0 (pitch ${n.pitch} at ${n.time})`);
    if (n.time < 0) throw new Error(`note time must be >= 0 (pitch ${n.pitch})`);
  }
  let maxEnd = 0;
  for (const n of notes) maxEnd = Math.max(maxEnd, n.time + n.duration);
  const length = cs.length ?? Math.max(beatsPerBar, Math.ceil(maxEnd / beatsPerBar - 1e-9) * beatsPerBar);
  clip.attrs.Id = String(clipId);
  clip.attrs.Time = '0';
  setValue(clip, 'CurrentStart', 0);
  setValue(clip, 'CurrentEnd', length);
  setValue(clip, 'Loop/LoopStart', 0);
  setValue(clip, 'Loop/LoopEnd', length);
  setValue(clip, 'Loop/StartRelative', 0);
  setValue(clip, 'Loop/LoopOn', cs.loop ?? true);
  setValue(clip, 'Loop/OutMarker', length);
  setValue(clip, 'Loop/HiddenLoopStart', 0);
  setValue(clip, 'Loop/HiddenLoopEnd', length);
  setValue(clip, 'Name', cs.name ?? '');
  setValue(clip, 'Color', cs.color ?? fallbackColor);
  setValue(clip, 'ScrollerTimePreserver/LeftTime', 0);
  setValue(clip, 'ScrollerTimePreserver/RightTime', length);
  const rts = find(clip, 'TimeSignature/TimeSignatures/RemoteableTimeSignature');
  if (rts) {
    const dec = decodeTimeSignature(tsCode);
    setValue(rts, 'Numerator', dec.numerator);
    setValue(rts, 'Denominator', dec.denominator);
    setValue(rts, 'Time', 0);
  }

  // Notes: one KeyTrack per pitch (ascending), events sorted by time, sequential NoteIds
  const keyTracks = find(clip, 'Notes/KeyTracks')!;
  keyTracks.children = [];
  const byPitch = new Map<number, WriteNote[]>();
  for (const n of notes) {
    const list = byPitch.get(n.pitch) ?? [];
    list.push(n);
    byPitch.set(n.pitch, list);
  }
  let nextNoteId = 1;
  let ktId = 0;
  for (const pitch of [...byPitch.keys()].sort((a, b) => a - b)) {
    const evs = byPitch.get(pitch)!.sort((a, b) => a.time - b.time);
    const notesEl = el('Notes');
    for (const n of evs) {
      const attrs: Record<string, string> = {
        Time: num(n.time),
        Duration: num(n.duration),
        Velocity: num(clamp(n.velocity ?? 100, 1, 127)),
        OffVelocity: num(clamp(n.offVelocity ?? 64, 0, 127)),
      };
      if (n.probability !== undefined && n.probability !== 1) attrs.Probability = num(n.probability);
      if (n.enabled === false) attrs.IsEnabled = 'false';
      attrs.NoteId = String(nextNoteId++);
      notesEl.children.push({ tag: 'MidiNoteEvent', attrs, children: [] });
    }
    keyTracks.children.push(el('KeyTrack', { Id: String(ktId++) }, [notesEl, valueEl('MidiKey', pitch)]));
  }
  setValue(clip, 'Notes/NoteIdGenerator/NextId', nextNoteId);
  return clip;
}

function clamp(v: number, lo: number, hi: number): number { return Math.max(lo, Math.min(hi, v)); }
function num(v: number): string { return Number.isInteger(v) ? String(v) : String(Number(v.toPrecision(15))); }

/** Build a Live Set and return the gzip-compressed .als bytes. */
export function writeLiveSet(spec: WriteLiveSetSpec): Buffer {
  const xml = buildLiveSetXml(spec);
  return gzipSync(Buffer.from(xml, 'utf8'), { level: 6 });
}

/** The <Ableton> root attributes the writer emits (Live 12.4 schema). */
export const WRITER_ROOT_ATTRS = ABLETON_ROOT_ATTRS;
