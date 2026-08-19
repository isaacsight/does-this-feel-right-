import { describe, it, expect } from 'vitest';
import { existsSync, mkdtempSync, writeFileSync, readdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir, homedir } from 'node:os';
import { join } from 'node:path';
import { gunzipSync } from 'node:zlib';

import { parseXml, serializeXml, find, findAll, value, tagPaths, XmlParseError, walk } from './xml.js';
import { SKELETON_KEYS, SKELETON_SOURCES, DEVICE_CATALOG, skeletonXml, ABLETON_ROOT_ATTRS } from './skeletons.js';
import { catalogDevice, catalogDeviceNames, instantiateDevice, listDeviceParams, isPointeeTag, deviceDisplayName } from './devices.js';
import { readLiveSet, writeLiveSet, buildLiveSetXml, encodeTimeSignature, decodeTimeSignature, readAbletonXml } from './als.js';
import { readRack, writeRack, writeInstrumentRack, buildRackXml } from './adg.js';
import { readDevicePreset, writeDevicePreset, buildDevicePresetXml } from './adv.js';
import { writeMidiFile, readMidiFile, encodeVarLen, decodeVarLen, type MidiFileSpec } from './midi.js';
import { writeMaxForLiveSkeleton, writeMaxPatcher } from './maxpat.js';
import { writeRemoteScriptScaffold } from './remote-script.js';

// ---------------------------------------------------------------------------
// Real files on this machine (tests that need them skip when absent)
// ---------------------------------------------------------------------------
const HOME = homedir();
const SEQ_DEMO = process.env.KBOT_ALS_FIXTURE
  ?? join(HOME, 'Music', 'Ableton', 'Factory Packs', 'Sequencers', 'Sequencers Demo Set.als');
const APP_RES = process.env.LIVE_APP_RESOURCES ?? '/Applications/Ableton Live 12 Beta.app/Contents/App-Resources';
const CORE = join(APP_RES, 'Core Library');
const DEFAULT_SET = join(APP_RES, 'Builtin', 'Templates', 'DefaultLiveSet.als');
const MS_RACK = join(CORE, 'Racks', 'Audio Effect Racks', 'Mixing & Mastering', 'MS Rack Template.adg');
const WURLI = join(CORE, 'Racks', 'Instrument Racks', 'Piano & Keys', 'E-Piano Wurli.adg');
const AHLIMBA = join(CORE, 'Racks', 'Drum Racks', 'Acoustic', 'Ahlimba Kit.adg');
const SAT_PRESET = join(CORE, 'Devices', 'Audio Effects', 'Saturator', 'Basic Soft.adv');
const TORN_SUB = join(HOME, 'Music', 'Ableton', 'Factory Packs', 'Sequencers', 'Racks', 'Instrument Racks', 'Bass', 'Torn Sub.adg');
const DEFAULT_MIDI_TRACK = join(CORE, 'Defaults', 'Creating Tracks', 'MIDI Track', 'Default MIDI Track.als');
const DEFAULT_AUDIO_TRACK = join(CORE, 'Defaults', 'Creating Tracks', 'Audio Track', 'Default Audio Track.als');

const has = (p: string) => existsSync(p);
const hasXmllint = (() => { try { execFileSync('xmllint', ['--version'], { stdio: 'ignore' }); return true; } catch { return false; } })();
const hasPython = (() => { try { execFileSync('python3', ['--version'], { stdio: 'ignore' }); return true; } catch { return false; } })();

function xmllintOk(xml: string): boolean {
  if (!hasXmllint) return true;
  const dir = mkdtempSync(join(tmpdir(), 'kbot-formats-'));
  const f = join(dir, 'x.xml');
  writeFileSync(f, xml);
  execFileSync('xmllint', ['--noout', f], { stdio: 'pipe' });
  return true;
}

// ---------------------------------------------------------------------------
// xml.ts
// ---------------------------------------------------------------------------
describe('xml', () => {
  it('parses Live-style XML and preserves attributes, quotes and entities', () => {
    const src = `<?xml version="1.0" encoding="UTF-8"?>\n<Ableton MajorVersion="5" Creator="Ableton Live 12.4d1">\n\t<LiveSet>\n\t\t<ViewData Value='{"a": "b", "n": [1, 2]}' />\n\t\t<Name Value="Tom &amp; Jerry &lt;3 &quot;q&quot; &#65;" />\n\t\t<Empty />\n\t\t<!-- comment -->\n\t</LiveSet>\n</Ableton>\n`;
    const doc = parseXml(src);
    expect(doc.root.tag).toBe('Ableton');
    expect(doc.root.attrs.Creator).toBe('Ableton Live 12.4d1');
    expect(value(doc.root, 'LiveSet/ViewData')).toBe('{"a": "b", "n": [1, 2]}');
    expect(value(doc.root, 'LiveSet/Name')).toBe('Tom & Jerry <3 "q" A');
    const out = serializeXml(doc);
    expect(out.startsWith('<?xml version="1.0" encoding="UTF-8"?>\n<Ableton MajorVersion="5"')).toBe(true);
    // Live's own quoting: single quotes around values containing double quotes
    expect(out).toContain(`<ViewData Value='{"a": "b", "n": [1, 2]}' />`);
    expect(out).toContain(`<Name Value='Tom &amp; Jerry &lt;3 "q" A' />`);
    // a value holding both quote kinds falls back to double quotes with &quot;
    expect(serializeXml(parseXml(`<A V="it's &quot;x&quot;" />`), { declaration: false })).toBe(`<A V="it's &quot;x&quot;" />\n`);
    expect(out).toContain('\t\t<Empty />');
    // idempotent
    expect(serializeXml(parseXml(out))).toBe(out);
  });

  it('rejects malformed documents', () => {
    expect(() => parseXml('<A><B></A>')).toThrow(XmlParseError);
    expect(() => parseXml('<A>')).toThrow(XmlParseError);
    expect(() => parseXml('<A /><B />')).toThrow(/exactly one root/);
  });

  it('tolerates unquoted attributes, CDATA and DOCTYPE', () => {
    const doc = parseXml('<!DOCTYPE x [ <!ELEMENT x ANY> ]><x a=1 b="2"><![CDATA[<raw>]]></x>');
    expect(doc.root.attrs.a).toBe('1');
    expect(doc.root.children[0].text).toBe('<raw>');
  });
});

// ---------------------------------------------------------------------------
// skeletons.ts / devices.ts
// ---------------------------------------------------------------------------
describe('skeletons', () => {
  it('every embedded fragment decompresses to well-formed XML with the expected root', () => {
    expect(SKELETON_KEYS.length).toBeGreaterThan(20);
    for (const key of SKELETON_KEYS) {
      const xml = skeletonXml(key);
      const root = parseXml(xml).root;
      if (key === 'als.set') expect(root.tag).toBe('Ableton');
      else if (key === 'als.midiTrack') expect(root.tag).toBe('MidiTrack');
      else if (key === 'als.audioTrack') expect(root.tag).toBe('AudioTrack');
      else if (key.startsWith('als.returnTrack')) expect(root.tag).toBe('ReturnTrack');
      else if (key === 'als.midiClip') expect(root.tag).toBe('MidiClip');
      else if (key === 'als.scene') expect(root.tag).toBe('Scene');
      else if (key === 'als.locator') expect(root.tag).toBe('Locator');
      else if (key.endsWith('.device') && key.startsWith('rack.')) expect(root.tag).toMatch(/GroupDevice$/);
      else if (key.endsWith('.branch')) expect(root.tag).toMatch(/BranchPreset$/);
      else if (key === 'rack.devicePreset') expect(root.tag).toBe('AbletonDevicePreset');
      else if (key.startsWith('device.')) expect(root.tag).toBe(key.slice('device.'.length));
      else throw new Error(`unexpected skeleton key ${key}`);
    }
  });

  it('records provenance: every source is a Live 12.4 file with a sha256', () => {
    expect(SKELETON_SOURCES.length).toBeGreaterThan(10);
    for (const s of SKELETON_SOURCES) {
      expect(s.sha256).toMatch(/^[0-9a-f]{64}$/);
      expect(s.minorVersion).toBe(ABLETON_ROOT_ATTRS.MinorVersion);
      expect(s.creator).toMatch(/^Ableton Live 12/);
    }
    expect(ABLETON_ROOT_ATTRS.MajorVersion).toBe('5');
  });

  it('device catalog: every device instantiates, has parameters and zeroed pointee ids', () => {
    expect(DEVICE_CATALOG.length).toBeGreaterThan(15);
    for (const d of DEVICE_CATALOG) {
      const dev = instantiateDevice(d.name);
      expect(dev.tag).toBe(d.tag);
      const params = listDeviceParams(dev);
      expect(Object.keys(params).length).toBeGreaterThan(0);
      expect(params.On).toBe('true');
      walk(dev, (n) => { if (isPointeeTag(n.tag) && n.attrs.Id !== undefined) expect(n.attrs.Id).toBe('0'); });
    }
    expect(catalogDevice('utility')?.tag).toBe('StereoGain');
    expect(catalogDevice('StereoGain')?.name).toBe('Utility');
    expect(catalogDeviceNames('instrument')).toEqual(expect.arrayContaining(['Drift', 'Operator', 'Wavetable']));
    expect(deviceDisplayName('Eq8')).toBe('EQ Eight');
    expect(deviceDisplayName('OriginalSimpler')).toBe('Simpler');
  });

  it('applies parameters by path and rejects unknown ones', () => {
    const sat = instantiateDevice({ name: 'Saturator', params: { PreDrive: 12, 'On': false }, displayName: 'Hot' });
    expect(value(sat, 'PreDrive/Manual')).toBe('12');
    expect(value(sat, 'On/Manual')).toBe('false');
    expect(value(sat, 'UserName')).toBe('Hot');
    const eq = instantiateDevice({ name: 'EQ Eight', params: { 'Bands.0/ParameterA/Freq': 200 } });
    expect(value(eq, 'Bands.0/ParameterA/Freq/Manual')).toBe('200');
    expect(() => instantiateDevice({ name: 'Saturator', params: { Nope: 1 } })).toThrow(/no parameter "Nope"/);
    expect(() => instantiateDevice('Not A Device')).toThrow(/unknown device/);
    // Utility skeleton is neutral stereo
    const util = instantiateDevice('Utility');
    expect(value(util, 'Mono/Manual')).toBe('false');
    expect(value(util, 'StereoWidth/Manual')).toBe('1');
  });
});

// ---------------------------------------------------------------------------
// als.ts — read real sets
// ---------------------------------------------------------------------------
describe('als read (real files)', () => {
  it.skipIf(!has(SEQ_DEMO))('reads the Sequencers Demo Set: tracks, tempo, devices, clips with notes', () => {
    const set = readLiveSet(SEQ_DEMO);
    expect(set.version.major).toBe(5);
    expect(set.version.creator).toMatch(/^Ableton Live 12/);
    expect(set.tracks.length).toBeGreaterThan(0);
    expect(typeof set.tempo).toBe('number');
    expect(set.tempo).toBe(109);
    expect(set.timeSig).toEqual({ numerator: 4, denominator: 4 });
    const midi = set.tracks.filter((t) => t.kind === 'midi');
    expect(midi.length).toBe(4);
    expect(midi.map((t) => t.name)).toEqual(['Step Arp Drips', 'SQ Pluck', 'SQ Bass', 'Rhythmic Steps']);
    expect(set.tracks.find((t) => t.kind === 'master')?.name).toBe('Main');
    // every MIDI track carries devices; racks expose chains
    for (const t of midi) expect(t.devices.length).toBeGreaterThan(0);
    const rack = midi[0].devices.find((d) => d.chains);
    expect(rack).toBeDefined();
    expect(rack!.chains![0].devices.length).toBeGreaterThan(0);
    // Max for Live device names resolve from the patch reference
    expect(midi[0].devices[0].name).toBe('Step Arp');
    // at least one clip with notes (arrangement clip on the first track)
    const clips = set.tracks.flatMap((t) => [...t.sessionClips, ...t.arrangementClips]);
    const withNotes = clips.filter((c) => c.notes.length > 0);
    expect(withNotes.length).toBeGreaterThan(0);
    const c = withNotes[0];
    expect(c.length).toBeGreaterThan(0);
    for (const n of c.notes) {
      expect(n.pitch).toBeGreaterThanOrEqual(0);
      expect(n.pitch).toBeLessThanOrEqual(127);
      expect(n.duration).toBeGreaterThan(0);
      expect(n.velocity).toBeGreaterThan(0);
    }
    // take-lane clips (Live 11+ comping) are surfaced too
    expect(midi.some((t) => (t.takeLaneClips?.length ?? 0) > 0)).toBe(true);
  });

  it.skipIf(!has(DEFAULT_SET))('reads Live 12 DefaultLiveSet.als (2 MIDI + 2 audio + 2 returns, 8 scenes, 120 bpm)', () => {
    const set = readLiveSet(DEFAULT_SET);
    expect(set.tempo).toBe(120);
    expect(set.tracks.map((t) => t.kind)).toEqual(['midi', 'midi', 'audio', 'audio', 'return', 'return', 'master']);
    expect(set.scenes.length).toBe(8);
    expect(set.tracks[4].devices.map((d) => d.name)).toEqual(['Reverb']);
    expect(set.tracks[5].devices.map((d) => d.name)).toEqual(['Delay']);
  });

  it('accepts a Buffer and raw XML alike', () => {
    const buf = writeLiveSet({ tracks: [{ kind: 'midi', name: 'X' }] });
    const fromBuf = readLiveSet(buf);
    const fromXml = readLiveSet(Buffer.from(readAbletonXml(buf)));
    expect(fromXml.tracks.map((t) => t.name)).toEqual(fromBuf.tracks.map((t) => t.name));
  });
});

// ---------------------------------------------------------------------------
// corpus sweep (real files): parser robustness across Live's own library
// ---------------------------------------------------------------------------
function listFiles(dir: string, ext: string, limit: number): string[] {
  const out: string[] = [];
  const rec = (d: string) => {
    if (out.length >= limit) return;
    let entries: import('node:fs').Dirent[];
    try { entries = readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      if (out.length >= limit) return;
      const p = join(d, e.name);
      if (e.isDirectory()) rec(p);
      else if (e.name.endsWith(ext)) out.push(p);
    }
  };
  rec(dir);
  return out;
}

describe('corpus sweep (real files)', () => {
  it.skipIf(!has(CORE))('reads every Core Library template set and a sample of racks + device presets', () => {
    const sets = listFiles(join(CORE, 'Templates'), '.als', 20);
    expect(sets.length).toBeGreaterThan(3);
    for (const f of sets) {
      const set = readLiveSet(f);
      expect(set.tracks.length).toBeGreaterThan(0);
      expect(set.tempo).toBeGreaterThan(0);
    }
    const racks = listFiles(join(CORE, 'Racks'), '.adg', 150);
    expect(racks.length).toBe(150);
    const kinds = new Set<string>();
    for (const f of racks) { const r = readRack(f); kinds.add(r.kind); expect(r.chains.length).toBeGreaterThan(0); }
    expect(kinds.size).toBeGreaterThan(1);
    const presets = listFiles(join(CORE, 'Devices'), '.adv', 150);
    expect(presets.length).toBe(150);
    for (const f of presets) { const p = readDevicePreset(f); expect(p.tag.length).toBeGreaterThan(0); expect(Object.keys(p.params).length).toBeGreaterThan(0); }
  });
});

// ---------------------------------------------------------------------------
// als.ts — write + read back
// ---------------------------------------------------------------------------
describe('als write', () => {
  const notesA = [
    { pitch: 60, time: 0, duration: 1 },
    { pitch: 64, time: 1, duration: 0.5, velocity: 90 },
    { pitch: 67, time: 1.5, duration: 0.25, velocity: 70, offVelocity: 40 },
    { pitch: 60, time: 2, duration: 2, probability: 0.5 },
  ];
  const spec = {
    tempo: 128,
    timeSig: { numerator: 3, denominator: 4 },
    scenes: ['Intro', 'Verse'],
    locators: [{ name: 'Drop', time: 32 }, { name: 'Outro', time: 96 }],
    tracks: [
      { kind: 'midi' as const, name: 'Lead', color: 12, devices: ['Drift', { name: 'Saturator', params: { PreDrive: 6 } }], clips: [{ slot: 0, name: 'A', notes: notesA }] },
      { kind: 'midi' as const, name: 'Bass', clips: [{ slot: 9, name: 'B', length: 6, loop: false, notes: [{ pitch: 36, time: 0, duration: 3 }] }] },
      { kind: 'audio' as const, name: 'Vox', devices: [{ name: 'Utility', params: { Gain: 0.5 } }, 'Compressor'], volume: 0.8, pan: -0.25, muted: true },
    ],
  };

  it('writes a gzip .als whose XML re-walks cleanly and reads back names, tempo, notes, devices, scenes, locators', () => {
    const buf = writeLiveSet(spec);
    expect(buf[0]).toBe(0x1f);
    expect(buf[1]).toBe(0x8b);
    const xml = gunzipSync(buf).toString('utf8');
    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>\n<Ableton MajorVersion="5"')).toBe(true);
    // independent re-walk of the emitted XML
    const doc = parseXml(xml);
    expect(doc.root.tag).toBe('Ableton');
    expect(doc.root.attrs.Creator).toBe(ABLETON_ROOT_ATTRS.Creator);
    expect(xmllintOk(xml)).toBe(true);

    const back = readLiveSet(buf);
    expect(back.tempo).toBe(128);
    expect(back.timeSig).toEqual({ numerator: 3, denominator: 4 });
    expect(back.tracks.map((t) => [t.kind, t.name])).toEqual([
      ['midi', 'Lead'], ['midi', 'Bass'], ['audio', 'Vox'], ['return', 'A-Reverb'], ['return', 'B-Delay'], ['master', 'Main'],
    ]);
    expect(back.tracks[0].color).toBe(12);
    expect(back.tracks[0].devices.map((d) => d.name)).toEqual(['Drift', 'Saturator']);
    expect(back.tracks[2].devices.map((d) => d.name)).toEqual(['Utility', 'Compressor']);
    expect(back.tracks[2].volume).toBeCloseTo(0.8);
    expect(back.tracks[2].pan).toBeCloseTo(-0.25);
    expect(back.tracks[2].muted).toBe(true);
    // scenes: 10 because slot 9 was used
    expect(back.scenes.length).toBe(10);
    expect(back.scenes.map((s) => s.name).slice(0, 3)).toEqual(['Intro', 'Verse', '']);
    expect(back.locators).toEqual([{ name: 'Drop', time: 32 }, { name: 'Outro', time: 96 }]);

    // clips + notes round-trip exactly
    const lead = back.tracks[0].sessionClips;
    expect(lead.length).toBe(1);
    expect(lead[0].slot).toBe(0);
    expect(lead[0].name).toBe('A');
    expect(lead[0].length).toBe(6); // 3/4: 4 beats of notes -> 2 bars = 6 beats
    expect(lead[0].loop.on).toBe(true);
    const got = lead[0].notes.map((n) => [n.pitch, n.time, n.duration, n.velocity, n.offVelocity ?? 64]);
    const want = [...notesA].sort((a, b) => a.time - b.time || a.pitch - b.pitch).map((n) => [n.pitch, n.time, n.duration, n.velocity ?? 100, n.offVelocity ?? 64]);
    expect(got).toEqual(want);
    expect(lead[0].notes.find((n) => n.pitch === 60 && n.time === 2)?.probability).toBe(0.5);
    const bass = back.tracks[1].sessionClips[0];
    expect(bass.slot).toBe(9);
    expect(bass.length).toBe(6);
    expect(bass.loop.on).toBe(false);
    expect(bass.notes).toEqual([{ pitch: 36, time: 0, duration: 3, velocity: 100, offVelocity: 64, noteId: 1 }]);
  });

  it('keeps every track and pointee id unique and NextPointeeId = max + 1', () => {
    const doc = parseXml(buildLiveSetXml(spec));
    const ls = find(doc.root, 'LiveSet')!;
    const seen = new Map<string, string>();
    walk(ls, (n) => {
      if (n.attrs.Id === undefined) return;
      if (isPointeeTag(n.tag) || /^(MidiTrack|AudioTrack|ReturnTrack|GroupTrack)$/.test(n.tag)) {
        expect(seen.has(n.attrs.Id), `duplicate id ${n.attrs.Id} on ${n.tag} and ${seen.get(n.attrs.Id)}`).toBe(false);
        seen.set(n.attrs.Id, n.tag);
      }
    });
    const max = Math.max(...[...seen.keys()].map(Number));
    expect(Number(value(ls, 'NextPointeeId'))).toBe(max + 1);
    // every track has 10 clip slots in main + freeze sequencers
    for (const t of findAll(ls, 'Tracks/MidiTrack')) {
      expect(findAll(t, 'DeviceChain/MainSequencer/ClipSlotList/ClipSlot').length).toBe(10);
      expect(findAll(t, 'DeviceChain/FreezeSequencer/ClipSlotList/ClipSlot').length).toBe(10);
    }
    // main track carries tempo + time signature
    expect(value(ls, 'MainTrack/DeviceChain/Mixer/Tempo/Manual')).toBe('128');
    expect(value(ls, 'MainTrack/DeviceChain/Mixer/TimeSignature/Manual')).toBe(String(encodeTimeSignature({ numerator: 3, denominator: 4 })));
  });

  it('written tracks have exactly the element shape of the Live-saved skeleton', () => {
    const doc = parseXml(buildLiveSetXml(spec));
    const written = find(doc.root, 'LiveSet/Tracks/MidiTrack')!;
    const skel = parseXml(skeletonXml('als.midiTrack')).root;
    const strip = (s: Set<string>) => new Set([...s].filter((p) => !/\/Devices\/|\/Value\/MidiClip|\/KeyTracks\//.test(p)));
    expect(strip(tagPaths(written))).toEqual(strip(tagPaths(skel)));
    const clip = find(written, 'DeviceChain/MainSequencer/ClipSlotList/ClipSlot/ClipSlot/Value/MidiClip')!;
    const clipSkel = parseXml(skeletonXml('als.midiClip')).root;
    const stripNotes = (s: Set<string>) => new Set([...s].filter((p) => !p.includes('/KeyTracks/')));
    expect(stripNotes(tagPaths(clip))).toEqual(stripNotes(tagPaths(clipSkel)));
  });

  it.skipIf(!has(DEFAULT_MIDI_TRACK) || !has(DEFAULT_AUDIO_TRACK))('written tracks match the element shape of Live 12.4\'s own default track presets', () => {
    // Oracle: Core Library/Defaults/Creating Tracks/*.als are the tracks Live itself creates. They carry no
    // return-track send holders (that set has no returns), so those are excluded from the comparison.
    const doc = parseXml(buildLiveSetXml({ tracks: [{ kind: 'midi', name: 'M', clips: [{ slot: 0, notes: [{ pitch: 60, time: 0, duration: 1 }] }] }, { kind: 'audio', name: 'A' }] }));
    const noSends = (s: Set<string>) => new Set([...s].filter((p) => !p.includes('/Sends/TrackSendHolder') && !/\/Devices\/|\/Value\/MidiClip|\/KeyTracks\//.test(p)));
    for (const [tag, file] of [['MidiTrack', DEFAULT_MIDI_TRACK], ['AudioTrack', DEFAULT_AUDIO_TRACK]] as const) {
      const written = find(doc.root, `LiveSet/Tracks/${tag}`)!;
      const oracle = find(parseXml(readAbletonXml(file)).root, `LiveSet/Tracks/${tag}`)!;
      expect(oracle.attrs.Id).toBeDefined();
      expect(noSends(tagPaths(written))).toEqual(noSends(tagPaths(oracle)));
      // and the values Live cares about for a fresh track agree
      for (const p of ['DeviceChain/MainSequencer/MonitoringEnum', 'DeviceChain/Mixer/Volume/Manual', 'DeviceChain/Mixer/Pan/Manual', 'TrackGroupId', 'Freeze', 'DeviceChain/AudioOutputRouting/Target', 'DeviceChain/MidiInputRouting/Target']) {
        expect(value(written, p), p).toBe(value(oracle, p));
      }
    }
  });

  it('time signature codec matches Live (4/4 = 201, 3/4 = 200, 6/8 = 302)', () => {
    expect(encodeTimeSignature({ numerator: 4, denominator: 4 })).toBe(201);
    expect(encodeTimeSignature({ numerator: 3, denominator: 4 })).toBe(200);
    expect(encodeTimeSignature({ numerator: 6, denominator: 8 })).toBe(302);
    expect(decodeTimeSignature(201)).toEqual({ numerator: 4, denominator: 4 });
    expect(decodeTimeSignature(302)).toEqual({ numerator: 6, denominator: 8 });
    expect(() => encodeTimeSignature({ numerator: 4, denominator: 3 })).toThrow();
  });

  it('rejects invalid specs with useful errors', () => {
    expect(() => writeLiveSet({ tracks: [{ kind: 'audio', name: 'A', clips: [{ slot: 0, notes: [] }] }] })).toThrow(/MIDI track/);
    expect(() => writeLiveSet({ tracks: [{ kind: 'midi', name: 'A', clips: [{ slot: 0, notes: [{ pitch: 200, time: 0, duration: 1 }] }] }] })).toThrow(/pitch/);
    expect(() => writeLiveSet({ tracks: [{ kind: 'midi', name: 'A', clips: [{ slot: 0, notes: [{ pitch: 60, time: 0, duration: 0 }] }] }] })).toThrow(/duration/);
    expect(() => writeLiveSet({ tracks: [{ kind: 'midi', name: 'A', devices: ['Not A Device'] }] })).toThrow(/unknown device/);
    expect(() => writeLiveSet({ tracks: [{ kind: 'group' as unknown as 'midi', name: 'G' }] })).toThrow(/kind/);
  });
});

// ---------------------------------------------------------------------------
// adg.ts / adv.ts
// ---------------------------------------------------------------------------
describe('adg / adv read (real files)', () => {
  it.skipIf(!has(MS_RACK))('reads a Core Library Audio Effect Rack (chains + devices + macros)', () => {
    const r = readRack(MS_RACK);
    expect(r.kind).toBe('audioEffect');
    expect(r.tag).toBe('AudioEffectGroupDevice');
    expect(r.chains.map((c) => c.name)).toEqual(['Mid', 'Sides']);
    expect(r.chains.map((c) => c.devices)).toEqual([['Utility'], ['Utility']]);
    expect(r.macros.length).toBe(8);
    expect(r.allMacros.length).toBe(16);
  });

  it.skipIf(!has(WURLI))('reads a Core Library Instrument Rack', () => {
    const r = readRack(WURLI);
    expect(r.kind).toBe('instrument');
    expect(r.name).toBe('E-Piano Wurli');
    expect(r.chains[0].devices).toEqual(['Electric', 'Phaser-Flanger', 'Reverb', 'Limiter']);
    expect(r.macros).toContain('Tone Decay');
    expect(r.chains[0].keyRange).toEqual({ min: 0, max: 127 });
  });

  it.skipIf(!has(AHLIMBA))('reads a Drum Rack nested in an Instrument Rack (pads with notes)', () => {
    const r = readRack(AHLIMBA);
    expect(r.kind).toBe('instrument');
    const nested = r.chains[0].deviceDetails.find((d) => d.rack);
    expect(nested?.rack?.kind).toBe('drum');
    expect(nested!.rack!.chains.length).toBe(16);
    for (const pad of nested!.rack!.chains) {
      expect(pad.note).toBeGreaterThanOrEqual(0);
      expect(pad.devices).toEqual(['Drum Sampler']);
    }
  });

  it.skipIf(!has(TORN_SUB))('reads a Factory Pack rack (Sequencers / Torn Sub)', () => {
    const r = readRack(TORN_SUB);
    expect(r.kind).toBe('instrument');
    expect(r.chains[0].devices[0]).toBe('Wavetable');
  });

  it.skipIf(!has(SAT_PRESET))('reads a Core Library Saturator preset with its parameters', () => {
    const p = readDevicePreset(SAT_PRESET);
    expect(p.tag).toBe('Saturator');
    expect(p.device).toBe('Saturator');
    expect(p.kind).toBe('audio_effect');
    expect(Number(p.params.PreDrive)).toBeGreaterThan(0);
    expect(p.params.On).toBe('true');
    expect(() => readRack(SAT_PRESET)).toThrow(/not a rack/);
    expect(() => readDevicePreset(MS_RACK)).toThrow(/not a device preset/);
  });
});

describe('adg / adv write', () => {
  it('writes an Instrument Rack (.adg) that reads back with chains, devices, macros and re-walks as XML', () => {
    const buf = writeInstrumentRack({
      name: 'kbot Layer',
      macros: ['Cutoff', 'Res', 'Drive'],
      chains: [
        { name: 'Sub', devices: ['Drift', { name: 'Saturator', params: { PreDrive: 6 } }], keyRange: { min: 0, max: 60 } },
        { name: 'Top', devices: ['Arpeggiator', 'Operator', 'Utility', 'EQ Eight'] },
        { name: 'Empty' },
      ],
    });
    const xml = gunzipSync(buf).toString('utf8');
    expect(xmllintOk(xml)).toBe(true);
    const doc = parseXml(xml);
    expect(find(doc.root, 'GroupDevicePreset/Device/InstrumentGroupDevice')).toBeDefined();
    const back = readRack(buf);
    expect(back.kind).toBe('instrument');
    expect(back.name).toBe('kbot Layer');
    expect(back.macros).toEqual(['Cutoff', 'Res', 'Drive']);
    expect(back.visibleMacroCount).toBe(3);
    expect(back.chains.map((c) => c.name)).toEqual(['Sub', 'Top', 'Empty']);
    expect(back.chains.map((c) => c.devices)).toEqual([['Drift', 'Saturator'], ['Arpeggiator', 'Operator', 'Utility', 'EQ Eight'], []]);
    expect(back.chains[0].keyRange).toEqual({ min: 0, max: 60 });
    expect(back.chains[0].deviceDetails[1].preset?.params.PreDrive).toBe('6');
    // every device preset names its device id
    for (const ref of findAll(doc.root, 'GroupDevicePreset/BranchPresets/InstrumentBranchPreset')) {
      for (const dp of findAll(ref, 'DevicePresets/AbletonDevicePreset')) {
        const dev = find(dp, 'Device')!.children[0];
        expect(find(dp, 'PresetRef/AbletonDefaultPresetRef/DeviceId')!.attrs.Name).toBe(dev.tag);
      }
    }
  });

  it('writes Audio Effect, MIDI Effect and Drum racks', () => {
    const fx = readRack(writeRack({ kind: 'audioEffect', chains: [{ name: 'A', devices: ['Compressor', 'Reverb'] }, { name: 'B', devices: ['Delay'] }] }));
    expect(fx.kind).toBe('audioEffect');
    expect(fx.chains.map((c) => c.devices)).toEqual([['Compressor', 'Reverb'], ['Delay']]);
    const midi = readRack(writeRack({ kind: 'midiEffect', name: 'Arps', chains: [{ name: 'Up', devices: ['Arpeggiator', 'Scale'] }] }));
    expect(midi.kind).toBe('midiEffect');
    expect(midi.chains[0].devices).toEqual(['Arpeggiator', 'Scale']);
    const drum = readRack(writeRack({ kind: 'drum', chains: [{ name: 'Kick', note: 36, devices: ['Drift'] }, { name: 'Snare', note: 38, chokeGroup: 1, devices: ['Operator', 'Saturator'] }] }));
    expect(drum.kind).toBe('drum');
    expect(drum.chains.map((c) => [c.name, c.note, c.chokeGroup])).toEqual([['Kick', 36, 0], ['Snare', 38, 1]]);
    expect(drum.chains[1].devices).toEqual(['Operator', 'Saturator']);
  });

  it('validates chain contents against the rack kind', () => {
    expect(() => writeRack({ kind: 'audioEffect', chains: [{ name: 'A', devices: ['Drift'] }] })).toThrow(/not allowed in a audioEffect rack/);
    expect(() => writeRack({ kind: 'midiEffect', chains: [{ name: 'A', devices: ['Saturator'] }] })).toThrow(/not allowed/);
    expect(() => writeRack({ kind: 'instrument', chains: [{ name: 'A', devices: ['Saturator', 'Drift'] }] })).toThrow(/cannot follow/);
    expect(() => writeRack({ kind: 'instrument', chains: [{ name: 'A', devices: ['Drift', 'Operator'] }] })).toThrow(/only one instrument/);
    expect(() => writeRack({ kind: 'instrument', chains: [] })).toThrow(/at least one chain/);
    expect(() => buildRackXml({ kind: 'instrument', chains: [{ name: 'A' }], macros: new Array(17).fill('m') })).toThrow(/16 macros/);
  });

  it('writes a device preset (.adv) that reads back with patched parameters', () => {
    const buf = writeDevicePreset({ name: 'Saturator', params: { PreDrive: 12, DryWet: 0.5 }, displayName: 'Warm' });
    const xml = gunzipSync(buf).toString('utf8');
    expect(xmllintOk(xml)).toBe(true);
    const back = readDevicePreset(buf);
    expect(back.tag).toBe('Saturator');
    expect(back.name).toBe('Warm');
    expect(back.params.PreDrive).toBe('12');
    expect(back.params.DryWet).toBe('0.5');
    const util = readDevicePreset(writeDevicePreset('Utility'));
    expect(util.tag).toBe('StereoGain');
    expect(util.device).toBe('Utility');
    expect(util.params.Mono).toBe('false');
    expect(buildDevicePresetXml('Drift')).toContain('<Drift Id="0">');
  });
});

// ---------------------------------------------------------------------------
// midi.ts
// ---------------------------------------------------------------------------
describe('midi', () => {
  it('encodes and decodes variable-length quantities per the SMF spec', () => {
    const cases: Array<[number, number[]]> = [
      [0, [0x00]], [0x40, [0x40]], [0x7f, [0x7f]], [0x80, [0x81, 0x00]], [0x2000, [0xc0, 0x00]],
      [0x3fff, [0xff, 0x7f]], [0x4000, [0x81, 0x80, 0x00]], [0x1fffff, [0xff, 0xff, 0x7f]],
      [0x200000, [0x81, 0x80, 0x80, 0x00]], [0x0fffffff, [0xff, 0xff, 0xff, 0x7f]],
    ];
    for (const [v, bytes] of cases) {
      expect(encodeVarLen(v)).toEqual(bytes);
      expect(decodeVarLen(new Uint8Array(bytes), 0)).toEqual({ value: v, next: bytes.length });
    }
    expect(() => encodeVarLen(0x10000000)).toThrow();
  });

  it('writes a type-1 SMF with tempo/time-signature and reads it back exactly', () => {
    const spec: MidiFileSpec = {
      ppq: 960,
      tempo: 128,
      timeSig: { numerator: 6, denominator: 8 },
      tracks: [
        { name: 'Lead', notes: [
          { pitch: 60, start: 0, duration: 1 },
          { pitch: 60, start: 1, duration: 0.5, velocity: 80 },      // retrigger same pitch back to back
          { pitch: 64, start: 0.5, duration: 2, channel: 1 },
          { pitch: 67, start: 0, duration: 1, velocity: 127 },        // chord with the first note
          { pitch: 72, start: 300.25, duration: 0.125 },              // long delta -> multi-byte VLQ
        ] },
        { name: 'Bass', program: 33, notes: [{ pitch: 36, start: 0, duration: 4 }] },
        { notes: [] },
      ],
    };
    const buf = writeMidiFile(spec);
    // header: MThd, len 6, format 1, 4 tracks (conductor + 3), ppq 960
    expect([...buf.subarray(0, 14)]).toEqual([0x4d, 0x54, 0x68, 0x64, 0, 0, 0, 6, 0, 1, 0, 4, 0x03, 0xc0]);
    const back = readMidiFile(buf);
    expect(back.format).toBe(1);
    expect(back.ppq).toBe(960);
    expect(back.tempo).toBe(128);
    expect(back.timeSig).toEqual({ numerator: 6, denominator: 8 });
    expect(back.tracks.length).toBe(4);
    expect(back.tracks[0].name).toBe('kbot');
    const lead = back.tracks[1];
    expect(lead.name).toBe('Lead');
    const want = spec.tracks[0].notes
      .map((n) => ({ pitch: n.pitch, start: n.start, duration: n.duration, velocity: n.velocity ?? 100, channel: n.channel ?? 0 }))
      .sort((a, b) => a.start - b.start || a.pitch - b.pitch);
    expect(lead.notes).toEqual(want);
    expect(back.tracks[2].program).toBe(33);
    expect(back.tracks[2].notes).toEqual([{ pitch: 36, start: 0, duration: 4, velocity: 100, channel: 0 }]);
    expect(back.tracks[3].notes).toEqual([]);
    // every track chunk ends with end-of-track
    let i = 14;
    for (let t = 0; t < 4; t++) {
      expect(buf.subarray(i, i + 4).toString('ascii')).toBe('MTrk');
      const len = buf.readUInt32BE(i + 4);
      expect([...buf.subarray(i + 8 + len - 3, i + 8 + len)]).toEqual([0xff, 0x2f, 0x00]);
      i += 8 + len;
    }
    expect(i).toBe(buf.length);
  });

  it('reads running status and note-on velocity 0 as note-off', () => {
    const track = [
      0x00, 0x90, 60, 100,   // note on
      0x60, 62, 100,         // running status: another note on
      0x60, 60, 0,           // running status: note off via velocity 0
      0x60, 62, 0,
      0x00, 0xff, 0x2f, 0x00,
    ];
    const buf = Buffer.from([
      0x4d, 0x54, 0x68, 0x64, 0, 0, 0, 6, 0, 0, 0, 1, 0, 96,
      0x4d, 0x54, 0x72, 0x6b, 0, 0, 0, track.length, ...track,
    ]);
    const f = readMidiFile(buf);
    expect(f.format).toBe(0);
    expect(f.tracks[0].notes).toEqual([
      { pitch: 60, start: 0, duration: 2, velocity: 100, channel: 0 },
      { pitch: 62, start: 1, duration: 2, velocity: 100, channel: 0 },
    ]);
  });

  it('rejects bad specs', () => {
    expect(() => writeMidiFile({ ppq: 0, tracks: [] })).toThrow(/ppq/);
    expect(() => writeMidiFile({ tempo: 0, tracks: [] })).toThrow(/tempo/);
    expect(() => writeMidiFile({ tracks: [{ notes: [{ pitch: 60, start: -1, duration: 1 }] }] })).toThrow(/start/);
    expect(() => readMidiFile(Buffer.from('nope'))).toThrow(/MThd/);
  });
});

// ---------------------------------------------------------------------------
// maxpat.ts
// ---------------------------------------------------------------------------
describe('maxpat', () => {
  const boxTexts = (json: string) => {
    const doc = JSON.parse(json) as { patcher: { fileversion: number; appversion: { major: number }; classnamespace: string; boxes: Array<{ box: { id: string; maxclass: string; text?: string } }>; lines: Array<{ patchline: { source: [string, number]; destination: [string, number] } }> } };
    return doc;
  };

  it('emits a Max patcher with the right I/O objects per device kind and consistent patchlines', () => {
    for (const kind of ['midi_effect', 'audio_effect', 'instrument'] as const) {
      const json = writeMaxPatcher({ name: 'Test Device', kind });
      const doc = boxTexts(json);
      expect(doc.patcher.fileversion).toBe(1);
      expect(doc.patcher.appversion.major).toBe(8);
      expect(doc.patcher.classnamespace).toBe('box');
      const texts = doc.patcher.boxes.map((b) => b.box.text ?? '');
      if (kind === 'midi_effect') { expect(texts).toContain('midiin'); expect(texts).toContain('midiout'); }
      if (kind === 'audio_effect') { expect(texts).toContain('plugin~'); expect(texts).toContain('plugout~'); }
      if (kind === 'instrument') { expect(texts).toContain('midiin'); expect(texts).toContain('plugout~'); expect(texts).toContain('cycle~'); }
      expect(texts).toContain('js kbot_liveapi.js');
      expect(texts).toContain('live.thisdevice');
      const ids = new Set(doc.patcher.boxes.map((b) => b.box.id));
      expect(ids.size).toBe(doc.patcher.boxes.length);
      for (const l of doc.patcher.lines) {
        expect(ids.has(l.patchline.source[0])).toBe(true);
        expect(ids.has(l.patchline.destination[0])).toBe(true);
      }
      expect(doc.patcher.lines.length).toBeGreaterThan(3);
    }
    expect(() => writeMaxPatcher({ name: 'x', kind: 'nope' as unknown as 'instrument' })).toThrow(/unknown/);
  });

  it('bundles kbot_liveapi.js (LiveAPI get/set/call/describe/observe) and optional Node for Max files', () => {
    const plain = writeMaxForLiveSkeleton({ name: 'My Dev', kind: 'midi_effect' });
    expect(Object.keys(plain.files).sort()).toEqual(['My_Dev.maxpat', 'README.md', 'kbot_liveapi.js']);
    expect(plain.files['My_Dev.maxpat']).toBe(plain.maxpat);
    const js = plain.files['kbot_liveapi.js'];
    for (const fn of ['function get(', 'function set(', 'function call(', 'function describe(', 'function children(', 'function observe(', 'new LiveAPI(']) expect(js).toContain(fn);
    expect(plain.files['README.md']).toMatch(/\.amxd/);
    expect(plain.files['README.md']).toMatch(/do not write \.amxd/);

    const node = writeMaxForLiveSkeleton({ name: 'Bridge', kind: 'audio_effect', useNodeForMax: true, nodePort: 9123 });
    expect(Object.keys(node.files).sort()).toEqual(['Bridge.maxpat', 'README.md', 'kbot_liveapi.js', 'kbot_node.js', 'package.json']);
    const texts = boxTexts(node.maxpat).patcher.boxes.map((b) => b.box.text ?? '');
    expect(texts).toContain('node.script kbot_node.js 9123');
    expect(texts).toContain('script start');
    expect(node.files['kbot_node.js']).toContain("require('max-api')");
    expect(node.files['kbot_node.js']).toContain('9998'); // default in the script, overridden by the box argument
    const pkg = JSON.parse(node.files['package.json']);
    expect(pkg.main).toBe('kbot_node.js');
    expect(pkg.dependencies).toEqual({});
  });
});

// ---------------------------------------------------------------------------
// remote-script.ts
// ---------------------------------------------------------------------------
describe('remote-script', () => {
  it('scaffolds a Control Surface with create_instance, a schedule_message tick and a TCP JSON-lines server', () => {
    const s = writeRemoteScriptScaffold({ name: 'KbotSurface', port: 9997 });
    expect(s.folder).toBe('KbotSurface');
    expect(Object.keys(s.files).sort()).toEqual(['README.md', '__init__.py', 'kbot_surface.py', 'tcp_server.py']);
    expect(s.files['__init__.py']).toContain('def create_instance(c_instance):');
    expect(s.files['__init__.py']).toContain('return KbotSurface(c_instance)');
    const mod = s.files['kbot_surface.py'];
    expect(mod).toContain('class KbotSurface(ControlSurface):');
    expect(mod).toContain('self.schedule_message(1, self._tick)');
    expect(mod).toContain('TCPServer(port=9997)');
    for (const a of ['"ping"', '"tracks"', '"lom_get"', '"lom_set"', '"lom_call"', '"lom_describe"', '"lom_children"']) expect(mod).toContain(a);
    expect(s.files['tcp_server.py']).toContain('LISTEN_PORT = 9997');
    expect(s.files['tcp_server.py']).toContain('select.select(');
    expect(s.files['README.md']).toContain('Remote Scripts/KbotSurface/');
  });

  it.skipIf(!hasPython)('generated Python compiles', () => {
    const s = writeRemoteScriptScaffold({ name: 'KbotSurface', port: 9997 });
    const dir = mkdtempSync(join(tmpdir(), 'kbot-rs-'));
    for (const [f, c] of Object.entries(s.files)) writeFileSync(join(dir, f), c);
    for (const f of Object.keys(s.files).filter((x) => x.endsWith('.py'))) {
      execFileSync('python3', ['-m', 'py_compile', join(dir, f)], { stdio: 'pipe' });
    }
  });

  it('rejects bad names and ports', () => {
    expect(() => writeRemoteScriptScaffold({ name: 'bad name', port: 9000 })).toThrow(/identifier/);
    expect(() => writeRemoteScriptScaffold({ name: 'Ok', port: 80 })).toThrow(/port/);
  });
});
