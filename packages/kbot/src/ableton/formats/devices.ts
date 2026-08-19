/**
 * devices.ts — native Live device skeletons and helpers shared by the
 * .als / .adg / .adv writers.
 *
 * Every device the writers can place comes from DEVICE_CATALOG in
 * skeletons.ts: real device XML cut from Core Library presets, with all
 * pointee ids zeroed the way Live's own .adv/.adg presets are stored.
 * Parameters are patched by path (`<Param>/Manual Value="…"`), which is the
 * only place Live keeps a parameter's stored value.
 */
import { DEVICE_CATALOG, skeletonXml, type CatalogDevice, type DeviceKind } from './skeletons.js';
import { parseXml, find, walk, setValue, fmt, type XmlNode } from './xml.js';

export type { CatalogDevice, DeviceKind };

export type DeviceParams = Record<string, number | boolean | string>;

export interface DeviceSpec {
  /** Catalog name ("Saturator") or Live tag ("StereoGain"). */
  name: string;
  /** Parameter paths → values, e.g. { 'PreDrive': 12, 'DryWet': 0.5, 'Bands.0/ParameterA/Freq': 200 }. */
  params?: DeviceParams;
  /** Display name shown in Live's title bar (UserName). */
  displayName?: string;
  /** Device on/off (default on). */
  enabled?: boolean;
}

/** Friendly names for Live device tags that are not in the catalog. */
const TAG_DISPLAY_NAMES: Record<string, string> = {
  OriginalSimpler: 'Simpler',
  MultiSampler: 'Sampler',
  InstrumentVector: 'Wavetable',
  UltraAnalog: 'Analog',
  Operator: 'Operator',
  Collision: 'Collision',
  StringStudio: 'Tension',
  LoungeLizard: 'Electric',
  InstrumentImpulse: 'Impulse',
  Drift: 'Drift',
  InstrumentMeld: 'Meld',
  DrumCell: 'Drum Sampler',
  DrumGroupDevice: 'Drum Rack',
  InstrumentGroupDevice: 'Instrument Rack',
  AudioEffectGroupDevice: 'Audio Effect Rack',
  MidiEffectGroupDevice: 'MIDI Effect Rack',
  MxDeviceInstrument: 'Max Instrument',
  MxDeviceAudioEffect: 'Max Audio Effect',
  MxDeviceMidiEffect: 'Max MIDI Effect',
  PluginDevice: 'Plug-in',
  AuPluginDevice: 'AU Plug-in',
  Compressor2: 'Compressor',
  GlueCompressor: 'Glue Compressor',
  Eq8: 'EQ Eight',
  FilterEQ3: 'EQ Three',
  ChannelEq: 'Channel EQ',
  StereoGain: 'Utility',
  AutoFilter: 'Auto Filter',
  AutoFilter2: 'Auto Filter',
  AutoPan: 'Auto Pan',
  AutoPan2: 'Auto Pan-Tremolo',
  BeatRepeat: 'Beat Repeat',
  Chorus2: 'Chorus-Ensemble',
  PhaserNew: 'Phaser-Flanger',
  Hybrid: 'Hybrid Reverb',
  Reverb: 'Reverb',
  Delay: 'Delay',
  Echo: 'Echo',
  FilterDelay: 'Filter Delay',
  GrainDelay: 'Grain Delay',
  Redux2: 'Redux',
  Saturator: 'Saturator',
  Overdrive: 'Overdrive',
  Pedal: 'Pedal',
  Roar: 'Roar',
  DrumBuss: 'Drum Buss',
  Limiter: 'Limiter',
  Gate: 'Gate',
  MultibandDynamics: 'Multiband Dynamics',
  Amp: 'Amp',
  Cabinet: 'Cabinet',
  Erosion: 'Erosion',
  Vinyl: 'Vinyl Distortion',
  Tube: 'Dynamic Tube',
  Corpus: 'Corpus',
  Resonator: 'Resonators',
  Shifter: 'Shifter',
  FrequencyShifter: 'Frequency Shifter',
  Vocoder: 'Vocoder',
  SpectralResonator: 'Spectral Resonator',
  SpectralTime: 'Spectral Time',
  Looper: 'Looper',
  Tuner: 'Tuner',
  Spectrum: 'Spectrum',
  ProxyAudioEffectDevice: 'External Audio Effect',
  ProxyInstrumentDevice: 'External Instrument',
  MidiArpeggiator: 'Arpeggiator',
  MidiChord: 'Chord',
  MidiNoteLength: 'Note Length',
  MidiPitcher: 'Pitch',
  MidiRandom: 'Random',
  MidiScale: 'Scale',
  MidiVelocity: 'Velocity',
  MidiEffectDeviceCC: 'CC Control',
};

const byName = new Map<string, CatalogDevice>();
const byTag = new Map<string, CatalogDevice>();
for (const d of DEVICE_CATALOG) {
  byName.set(d.name.toLowerCase(), d);
  byTag.set(d.tag.toLowerCase(), d);
}

/** Look up a catalog device by friendly name or Live tag (case-insensitive). */
export function catalogDevice(nameOrTag: string): CatalogDevice | undefined {
  const k = nameOrTag.trim().toLowerCase();
  return byName.get(k) ?? byTag.get(k);
}

/** Names of every device the writers can place. */
export function catalogDeviceNames(kind?: DeviceKind): string[] {
  return DEVICE_CATALOG.filter((d) => !kind || d.kind === kind).map((d) => d.name);
}

/** Human-readable name for a Live device tag. */
export function deviceDisplayName(tag: string): string {
  return byTag.get(tag.toLowerCase())?.name ?? TAG_DISPLAY_NAMES[tag] ?? tag;
}

/** Whether a device tag is a rack. */
export function isRackTag(tag: string): boolean {
  return tag === 'InstrumentGroupDevice' || tag === 'AudioEffectGroupDevice'
    || tag === 'MidiEffectGroupDevice' || tag === 'DrumGroupDevice';
}

/**
 * Best-effort device kind from its tag (catalog first, then naming
 * conventions Live uses in its XML).
 */
export function deviceKindOf(tag: string): DeviceKind | 'unknown' {
  const c = byTag.get(tag.toLowerCase());
  if (c) return c.kind;
  if (tag === 'InstrumentGroupDevice' || tag === 'DrumGroupDevice' || tag === 'MxDeviceInstrument'
    || tag === 'OriginalSimpler' || tag === 'MultiSampler' || tag === 'InstrumentVector'
    || tag === 'UltraAnalog' || tag === 'Operator' || tag === 'Collision' || tag === 'StringStudio'
    || tag === 'LoungeLizard' || tag === 'InstrumentImpulse' || tag === 'InstrumentMeld' || tag === 'DrumCell'
    || tag === 'ProxyInstrumentDevice') return 'instrument';
  if (tag === 'MidiEffectGroupDevice' || tag === 'MxDeviceMidiEffect' || tag.startsWith('Midi')) return 'midi_effect';
  if (tag === 'AudioEffectGroupDevice' || tag === 'MxDeviceAudioEffect') return 'audio_effect';
  return 'unknown';
}

/** Fresh clone of a catalog device's XML (all pointee ids 0, no UserName). */
export function deviceSkeleton(nameOrTag: string): XmlNode {
  const c = catalogDevice(nameOrTag);
  if (!c) {
    throw new Error(`unknown device "${nameOrTag}". Known devices: ${catalogDeviceNames().join(', ')}`);
  }
  return parseXml(skeletonXml(`device.${c.tag}`)).root;
}

/**
 * Every parameter path of a device (paths whose element carries a
 * `<Manual Value>` child), mapped to the stored value string.
 */
export function listDeviceParams(dev: XmlNode): Record<string, string> {
  const out: Record<string, string> = {};
  const rec = (n: XmlNode, prefix: string) => {
    for (const c of n.children) {
      if (c.tag === '#text') continue;
      const p = prefix ? `${prefix}/${c.tag}` : c.tag;
      const manual = find(c, 'Manual');
      if (manual && manual.attrs.Value !== undefined) out[p] = manual.attrs.Value;
      // recurse: nested parameter groups (Eq8 Bands.N, Operator operators, ...)
      if (c.children.length) rec(c, p);
    }
  };
  rec(dev, '');
  return out;
}

/** Patch parameter values in place. Throws for unknown paths (lists candidates). */
export function applyDeviceParams(dev: XmlNode, params: DeviceParams | undefined): XmlNode {
  if (!params) return dev;
  for (const [key, val] of Object.entries(params)) {
    // Live tags contain literal dots ("Bands.0"), so "/" is the only separator.
    const target = find(dev, key);
    if (!target) {
      const known = Object.keys(listDeviceParams(dev));
      throw new Error(`device ${dev.tag} has no parameter "${key}". Known parameters: ${known.join(', ')}`);
    }
    if (target.tag === 'Manual') {
      target.attrs.Value = fmt(val);
      continue;
    }
    const manual = find(target, 'Manual');
    if (!manual) throw new Error(`"${key}" on ${dev.tag} is not a parameter (no Manual value)`);
    manual.attrs.Value = fmt(val);
  }
  return dev;
}

/** Instantiate a catalog device from a spec: clone, patch params, name, on/off. */
export function instantiateDevice(spec: DeviceSpec | string): XmlNode {
  const s: DeviceSpec = typeof spec === 'string' ? { name: spec } : spec;
  const dev = deviceSkeleton(s.name);
  applyDeviceParams(dev, s.params);
  if (s.displayName !== undefined) setValue(dev, 'UserName', s.displayName);
  if (s.enabled !== undefined) setValue(dev, 'On/Manual', s.enabled);
  return dev;
}

// ---------------------------------------------------------------------------
// Pointee-id bookkeeping (shared by .als assembly)
// ---------------------------------------------------------------------------

/** Tags whose `Id` attribute lives in Live's global "pointee" id space. */
export function isPointeeTag(tag: string): boolean {
  return tag === 'AutomationTarget' || tag === 'ModulationTarget' || tag === 'Pointee'
    || tag.endsWith('ModulationTarget') || tag.startsWith('ControllerTargets.');
}

export class IdCounter {
  constructor(public next = 1) {}
  take(): number { return this.next++; }
}

/**
 * Give every pointee-space element under `node` a fresh unique id from
 * `counter`, and rewrite `<PointeeId Value>` references inside the same
 * subtree so envelopes still point at their targets.
 */
export function renumberPointees(node: XmlNode, counter: IdCounter): void {
  const map = new Map<string, string>();
  walk(node, (n) => {
    if (n.attrs.Id !== undefined && isPointeeTag(n.tag)) {
      const fresh = String(counter.take());
      map.set(n.attrs.Id, fresh);
      n.attrs.Id = fresh;
    }
  });
  if (map.size === 0) return;
  walk(node, (n) => {
    if (n.tag === 'PointeeId' && n.attrs.Value !== undefined) {
      const m = map.get(n.attrs.Value);
      if (m !== undefined) n.attrs.Value = m;
    }
  });
}

/** Zero every pointee-space id (preset form). */
export function zeroPointees(node: XmlNode): void {
  walk(node, (n) => {
    if (n.attrs.Id !== undefined && isPointeeTag(n.tag)) n.attrs.Id = '0';
  });
}
