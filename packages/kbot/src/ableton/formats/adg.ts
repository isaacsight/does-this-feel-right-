/**
 * adg.ts — Ableton rack preset (.adg) reader / writer.
 *
 * An .adg is gzip-compressed XML:
 *   <Ableton …><GroupDevicePreset>
 *     <Device><InstrumentGroupDevice|AudioEffectGroupDevice|MidiEffectGroupDevice|DrumGroupDevice/></Device>
 *     <PresetRef/>
 *     <BranchPresets><…BranchPreset Id=n><Name/><DevicePresets>(AbletonDevicePreset|GroupDevicePreset)*</DevicePresets>
 *                                     <MixerPreset/><ZoneSettings/>…</…BranchPreset></BranchPresets>
 *     <ReturnBranchPresets/>
 *   </GroupDevicePreset></Ableton>
 *
 * The writer clones rack-device / branch-preset / device-preset fragments cut
 * from Core Library racks (see skeletons.ts) and fills them with catalog
 * devices. Nested racks and macro mappings are read but not written.
 */
import { gzipSync } from 'node:zlib';
import { parseXml, serializeXml, find, child, clone, setValue, value, numberValue, elements, type XmlNode } from './xml.js';
import { skeletonXml, ABLETON_ROOT_ATTRS, GROUP_PRESET_OVERWRITE_PROTECTION } from './skeletons.js';
import { instantiateDevice, catalogDevice, deviceDisplayName, deviceKindOf, isRackTag, type DeviceSpec, type DeviceKind } from './devices.js';
import { parseAbletonDoc, readVersion, type LiveSetVersion } from './als.js';
import { describeDevice, type DevicePreset } from './adv.js';

export type RackKind = 'instrument' | 'audioEffect' | 'midiEffect' | 'drum';

const RACK_TAGS: Record<RackKind, string> = {
  instrument: 'InstrumentGroupDevice',
  audioEffect: 'AudioEffectGroupDevice',
  midiEffect: 'MidiEffectGroupDevice',
  drum: 'DrumGroupDevice',
};
const RACK_KIND_BY_TAG: Record<string, RackKind> = Object.fromEntries(
  Object.entries(RACK_TAGS).map(([k, v]) => [v, k as RackKind]),
) as Record<string, RackKind>;

export interface RackChainDevice {
  tag: string;
  name: string;
  /** Nested rack. */
  rack?: RackInfo;
  preset?: DevicePreset;
}

export interface RackChain {
  name: string;
  devices: string[];
  deviceDetails: RackChainDevice[];
  /** Drum pads: incoming MIDI note. */
  note?: number;
  outNote?: number;
  chokeGroup?: number;
  keyRange?: { min: number; max: number };
  velocityRange?: { min: number; max: number };
}

export interface RackInfo {
  kind: RackKind;
  tag: string;
  name: string;
  chains: RackChain[];
  returnChains: RackChain[];
  /** Names of the visible macros. */
  macros: string[];
  /** All 16 macro display names. */
  allMacros: string[];
  visibleMacroCount: number;
  version: LiveSetVersion;
}

export function readRack(input: string | Buffer): RackInfo {
  const doc = parseAbletonDoc(input);
  const gp = child(doc.root, 'GroupDevicePreset');
  if (!gp) {
    const first = elements(doc.root)[0];
    throw new Error(`not a rack preset: found <${first?.tag ?? 'nothing'}> (use readDevicePreset / readLiveSet)`);
  }
  return readGroupPreset(gp, readVersion(doc.root));
}

function readGroupPreset(gp: XmlNode, version: LiveSetVersion): RackInfo {
  const dev = elements(child(gp, 'Device') ?? { tag: 'Device', attrs: {}, children: [] })[0];
  if (!dev || !isRackTag(dev.tag)) throw new Error(`GroupDevicePreset without a rack device (found <${dev?.tag}>)`);
  const kind = RACK_KIND_BY_TAG[dev.tag];
  const userName = value(dev, 'UserName') ?? '';
  const presetPath = value(gp, 'PresetRef/FilePresetRef/FileRef/RelativePath') ?? value(gp, 'PresetRef/FilePresetRef/FileRef/Path');
  const presetName = presetPath ? presetPath.split('/').pop()!.replace(/\.adg$/i, '') : '';
  const allMacros: string[] = [];
  for (let i = 0; i < 16; i++) allMacros.push(value(dev, `MacroDisplayNames.${i}`) ?? `Macro ${i + 1}`);
  const visible = numberValue(dev, 'NumVisibleMacroControls') ?? 8;
  const chains = elements(child(gp, 'BranchPresets') ?? { tag: 'BranchPresets', attrs: {}, children: [] }).map((b) => readBranchPreset(b, version));
  const returnChains = elements(child(gp, 'ReturnBranchPresets') ?? { tag: 'ReturnBranchPresets', attrs: {}, children: [] }).map((b) => readBranchPreset(b, version));
  return {
    kind,
    tag: dev.tag,
    name: userName || presetName || deviceDisplayName(dev.tag),
    chains,
    returnChains,
    macros: allMacros.slice(0, visible),
    allMacros,
    visibleMacroCount: visible,
    version,
  };
}

function readBranchPreset(b: XmlNode, version: LiveSetVersion): RackChain {
  const chain: RackChain = { name: value(b, 'Name') ?? '', devices: [], deviceDetails: [] };
  for (const p of elements(child(b, 'DevicePresets') ?? { tag: 'DevicePresets', attrs: {}, children: [] })) {
    if (p.tag === 'GroupDevicePreset') {
      const nested = readGroupPreset(p, version);
      chain.deviceDetails.push({ tag: nested.tag, name: nested.name, rack: nested });
      chain.devices.push(nested.name);
    } else {
      const dev = elements(child(p, 'Device') ?? { tag: 'Device', attrs: {}, children: [] })[0];
      if (!dev) continue;
      const preset = describeDevice(dev, version);
      chain.deviceDetails.push({ tag: dev.tag, name: preset.name, preset });
      chain.devices.push(preset.name);
    }
  }
  const zs = child(b, 'ZoneSettings');
  if (zs) {
    const rn = numberValue(zs, 'ReceivingNote'); if (rn !== undefined) chain.note = rn;
    const sn = numberValue(zs, 'SendingNote'); if (sn !== undefined) chain.outNote = sn;
    const cg = numberValue(zs, 'ChokeGroup'); if (cg !== undefined) chain.chokeGroup = cg;
    const kr = child(zs, 'KeyRange');
    if (kr) chain.keyRange = { min: numberValue(kr, 'Min') ?? 0, max: numberValue(kr, 'Max') ?? 127 };
    const vr = child(zs, 'VelocityRange');
    if (vr) chain.velocityRange = { min: numberValue(vr, 'Min') ?? 1, max: numberValue(vr, 'Max') ?? 127 };
  }
  return chain;
}

// ---------------------------------------------------------------------------
// Writer
// ---------------------------------------------------------------------------

export interface WriteRackChainSpec {
  name: string;
  devices?: Array<string | DeviceSpec>;
  /** Drum racks: pad note (0–127). */
  note?: number;
  outNote?: number;
  chokeGroup?: number;
  keyRange?: { min: number; max: number };
  velocityRange?: { min: number; max: number };
}

export interface WriteRackSpec {
  kind: RackKind;
  /** Rack title (UserName). */
  name?: string;
  chains: WriteRackChainSpec[];
  /** Macro names (1–16); shown macros = macros.length. */
  macros?: string[];
}

function expectedKinds(kind: RackKind): DeviceKind[] {
  switch (kind) {
    case 'audioEffect': return ['audio_effect'];
    case 'midiEffect': return ['midi_effect'];
    default: return ['midi_effect', 'instrument', 'audio_effect'];
  }
}

function checkChainOrder(kind: RackKind, chainName: string, tags: string[]): void {
  const allowed = expectedKinds(kind);
  let stage = 0; // 0 midi, 1 instrument, 2 audio
  for (const tag of tags) {
    const k = deviceKindOf(tag);
    if (k === 'unknown') continue;
    if (!allowed.includes(k)) {
      throw new Error(`chain "${chainName}": ${deviceDisplayName(tag)} is a ${k.replace('_', ' ')}, not allowed in a ${kind} rack`);
    }
    const s = k === 'midi_effect' ? 0 : k === 'instrument' ? 1 : 2;
    if (s < stage) {
      throw new Error(`chain "${chainName}": ${deviceDisplayName(tag)} (${k.replace('_', ' ')}) cannot follow ${stage === 1 ? 'an instrument' : 'an audio effect'}`);
    }
    if (s === 1 && stage === 1) throw new Error(`chain "${chainName}": only one instrument per chain`);
    stage = s;
  }
}

/** Uncompressed XML of a rack preset. */
export function buildRackXml(spec: WriteRackSpec): string {
  if (!RACK_TAGS[spec.kind]) throw new Error(`unknown rack kind "${spec.kind}"`);
  if (!spec.chains?.length) throw new Error('a rack needs at least one chain');
  const rackDev = parseXml(skeletonXml(`rack.${spec.kind}.device`)).root;
  const branchSkel = parseXml(skeletonXml(`rack.${spec.kind}.branch`)).root;
  const wrapperSkel = parseXml(skeletonXml('rack.devicePreset')).root;

  setValue(rackDev, 'UserName', spec.name ?? '');
  if (spec.macros) {
    if (spec.macros.length > 16) throw new Error('a rack has at most 16 macros');
    spec.macros.forEach((m, i) => setValue(rackDev, `MacroDisplayNames.${i}`, m));
    setValue(rackDev, 'NumVisibleMacroControls', Math.max(1, spec.macros.length));
  }

  const branchPresets: XmlNode = { tag: 'BranchPresets', attrs: {}, children: [] };
  spec.chains.forEach((c, ci) => {
    const b = clone(branchSkel);
    b.attrs.Id = String(ci);
    setValue(b, 'Name', c.name);
    const list = find(b, 'DevicePresets')!;
    const specs = c.devices ?? [];
    const tags = specs.map((d) => {
      const nm = typeof d === 'string' ? d : d.name;
      const cd = catalogDevice(nm);
      if (!cd) throw new Error(`chain "${c.name}": unknown device "${nm}"`);
      return cd.tag;
    });
    checkChainOrder(spec.kind, c.name, tags);
    specs.forEach((d, di) => {
      const dev = instantiateDevice(d);
      dev.attrs.Id = String(di);
      const w = clone(wrapperSkel);
      w.attrs.Id = String(di);
      find(w, 'Device')!.children = [dev];
      const idRef = find(w, 'PresetRef/AbletonDefaultPresetRef/DeviceId');
      if (idRef) idRef.attrs.Name = dev.tag;
      list.children.push(w);
    });
    const zs = child(b, 'ZoneSettings');
    if (zs) {
      if (spec.kind === 'drum') {
        const note = c.note ?? (36 + ci);
        if (note < 0 || note > 127) throw new Error(`chain "${c.name}": drum note out of range`);
        setValue(zs, 'ReceivingNote', note);
        setValue(zs, 'SendingNote', c.outNote ?? 60);
        setValue(zs, 'ChokeGroup', c.chokeGroup ?? 0);
      } else {
        if (c.keyRange) { setValue(zs, 'KeyRange/Min', c.keyRange.min); setValue(zs, 'KeyRange/Max', c.keyRange.max); setValue(zs, 'KeyRange/CrossfadeMin', c.keyRange.min); setValue(zs, 'KeyRange/CrossfadeMax', c.keyRange.max); }
        if (c.velocityRange) { setValue(zs, 'VelocityRange/Min', c.velocityRange.min); setValue(zs, 'VelocityRange/Max', c.velocityRange.max); setValue(zs, 'VelocityRange/CrossfadeMin', c.velocityRange.min); setValue(zs, 'VelocityRange/CrossfadeMax', c.velocityRange.max); }
      }
    }
    branchPresets.children.push(b);
  });

  // Group preset ref: default-preset ref naming the rack device (pattern from Live's nested-rack presets)
  const presetRef = clone(find(wrapperSkel, 'PresetRef')!);
  const idRef = find(presetRef, 'AbletonDefaultPresetRef/DeviceId');
  if (idRef) idRef.attrs.Name = rackDev.tag;

  const gp: XmlNode = {
    tag: 'GroupDevicePreset', attrs: {}, children: [
      { tag: 'OverwriteProtectionNumber', attrs: { Value: GROUP_PRESET_OVERWRITE_PROTECTION }, children: [] },
      { tag: 'Device', attrs: {}, children: [rackDev] },
      presetRef,
      branchPresets,
      { tag: 'ReturnBranchPresets', attrs: {}, children: [] },
    ],
  };
  const root: XmlNode = { tag: 'Ableton', attrs: { ...ABLETON_ROOT_ATTRS }, children: [gp] };
  return serializeXml({ root });
}

export function writeRack(spec: WriteRackSpec): Buffer {
  return gzipSync(Buffer.from(buildRackXml(spec), 'utf8'), { level: 6 });
}

export function writeInstrumentRack(spec: Omit<WriteRackSpec, 'kind'>): Buffer {
  return writeRack({ ...spec, kind: 'instrument' });
}

export function writeAudioEffectRack(spec: Omit<WriteRackSpec, 'kind'>): Buffer {
  return writeRack({ ...spec, kind: 'audioEffect' });
}

export function writeMidiEffectRack(spec: Omit<WriteRackSpec, 'kind'>): Buffer {
  return writeRack({ ...spec, kind: 'midiEffect' });
}

export function writeDrumRack(spec: Omit<WriteRackSpec, 'kind'>): Buffer {
  return writeRack({ ...spec, kind: 'drum' });
}
