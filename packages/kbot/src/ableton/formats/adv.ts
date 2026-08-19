/**
 * adv.ts — Ableton device preset (.adv) reader / writer.
 *
 * An .adv is gzip-compressed XML whose root <Ableton> element wraps a single
 * device element (e.g. <Saturator>, <StereoGain>, <Operator>). Parameter values
 * live in `<Param>/<Manual Value>` (nested groups such as Eq8 `Bands.0/…`).
 *
 * Writing is limited to the native devices in DEVICE_CATALOG (real Core
 * Library device XML with patched parameters).
 */
import { gzipSync } from 'node:zlib';
import { serializeXml, find, value, elements, type XmlNode } from './xml.js';
import { ABLETON_ROOT_ATTRS } from './skeletons.js';
import {
  instantiateDevice, listDeviceParams, deviceDisplayName, deviceKindOf, catalogDeviceNames,
  type DeviceSpec, type DeviceKind,
} from './devices.js';
import { parseAbletonDoc, readVersion, type LiveSetVersion } from './als.js';

export interface DevicePreset {
  /** Live's XML tag for the device (StereoGain, Saturator, Operator, …). */
  tag: string;
  /** Friendly device name (Utility, Saturator, …). */
  device: string;
  /** Preset name: the device's user title if set, else the referenced preset file name, else the device name. */
  name: string;
  userName: string;
  presetFile?: string;
  kind: DeviceKind | 'unknown';
  enabled?: boolean;
  /** Parameter path → stored value (as text). */
  params: Record<string, string>;
  version: LiveSetVersion;
}

export function readDevicePreset(input: string | Buffer): DevicePreset {
  const doc = parseAbletonDoc(input);
  const dev = elements(doc.root)[0];
  if (!dev) throw new Error('empty .adv: no device element under <Ableton>');
  if (dev.tag === 'GroupDevicePreset' || dev.tag === 'LiveSet') {
    throw new Error(`not a device preset: found <${dev.tag}> (use readRack / readLiveSet)`);
  }
  return describeDevice(dev, readVersion(doc.root));
}

/** Describe a device element (shared with rack reading). */
export function describeDevice(dev: XmlNode, version: LiveSetVersion): DevicePreset {
  const userName = value(dev, 'UserName') ?? '';
  const presetFile = value(dev, 'LastPresetRef/Value/FilePresetRef/FileRef/RelativePath')
    ?? value(dev, 'LastPresetRef/Value/FilePresetRef/FileRef/Path');
  const device = deviceDisplayName(dev.tag);
  const presetName = presetFile ? presetFile.split('/').pop()!.replace(/\.(adv|adg)$/i, '') : undefined;
  const on = find(dev, 'On/Manual')?.attrs.Value;
  return {
    tag: dev.tag,
    device,
    name: userName || presetName || device,
    userName,
    ...(presetFile ? { presetFile } : {}),
    kind: deviceKindOf(dev.tag),
    ...(on !== undefined ? { enabled: on === 'true' } : {}),
    params: listDeviceParams(dev),
    version,
  };
}

/** Uncompressed XML for a device preset built from a catalog device. */
export function buildDevicePresetXml(spec: DeviceSpec | string): string {
  const dev = instantiateDevice(spec);
  const root: XmlNode = { tag: 'Ableton', attrs: { ...ABLETON_ROOT_ATTRS }, children: [dev] };
  return serializeXml({ root });
}

/**
 * Write a native device preset (.adv). `spec.name` must be a catalog device
 * (Utility, Saturator, EQ Eight, Compressor, Reverb, Delay, Drift, …).
 */
export function writeDevicePreset(spec: DeviceSpec | string): Buffer {
  return gzipSync(Buffer.from(buildDevicePresetXml(spec), 'utf8'), { level: 6 });
}

/** Devices writeDevicePreset can produce. */
export function writableDevices(): string[] {
  return catalogDeviceNames();
}
