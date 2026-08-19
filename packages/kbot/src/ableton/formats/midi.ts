/**
 * midi.ts — Standard MIDI File (SMF) writer and reader.
 *
 * writeMidiFile() emits a type-1 file: track 0 carries tempo + time
 * signature meta events, then one track per spec track with note on/off
 * events (running status not used, for maximum reader compatibility) and an
 * end-of-track meta. Times are in beats (quarter notes), converted with the
 * given PPQ. Live imports these directly (drag onto a track or Session slot).
 *
 * readMidiFile() parses type 0/1 files back into the same shape (notes,
 * tempo, time signature, track names) so round-trips can be asserted.
 */

export interface MidiNoteSpec {
  pitch: number;
  /** Start in beats. */
  start: number;
  /** Length in beats. */
  duration: number;
  velocity?: number;
  /** 0–15 (default 0). */
  channel?: number;
}

export interface MidiTrackSpec {
  name?: string;
  notes: MidiNoteSpec[];
  /** Program change (0–127) at time 0. */
  program?: number;
}

export interface MidiFileSpec {
  /** Pulses per quarter note (default 480). */
  ppq?: number;
  /** BPM (default 120). */
  tempo?: number;
  timeSig?: { numerator: number; denominator: number };
  tracks: MidiTrackSpec[];
}

export interface MidiFileNote {
  pitch: number;
  start: number;
  duration: number;
  velocity: number;
  channel: number;
}

export interface MidiFileTrack {
  name?: string;
  notes: MidiFileNote[];
  program?: number;
}

export interface MidiFile {
  format: number;
  ppq: number;
  tempo?: number;
  timeSig?: { numerator: number; denominator: number };
  tracks: MidiFileTrack[];
}

// ---------------------------------------------------------------------------
// Encoding helpers
// ---------------------------------------------------------------------------

export function encodeVarLen(v: number): number[] {
  if (!Number.isInteger(v) || v < 0 || v > 0x0fffffff) throw new Error(`variable-length quantity out of range: ${v}`);
  const bytes = [v & 0x7f];
  v >>>= 7;
  while (v > 0) {
    bytes.unshift((v & 0x7f) | 0x80);
    v >>>= 7;
  }
  return bytes;
}

export function decodeVarLen(buf: Uint8Array, offset: number): { value: number; next: number } {
  let value = 0;
  let i = offset;
  for (let k = 0; k < 4; k++) {
    if (i >= buf.length) throw new Error('truncated variable-length quantity');
    const b = buf[i++];
    value = (value << 7) | (b & 0x7f);
    if ((b & 0x80) === 0) return { value: value >>> 0, next: i };
  }
  throw new Error('variable-length quantity longer than 4 bytes');
}

function u32(v: number): number[] { return [(v >>> 24) & 0xff, (v >>> 16) & 0xff, (v >>> 8) & 0xff, v & 0xff]; }
function u16(v: number): number[] { return [(v >>> 8) & 0xff, v & 0xff]; }
function u24(v: number): number[] { return [(v >>> 16) & 0xff, (v >>> 8) & 0xff, v & 0xff]; }

function chunk(id: string, body: number[]): number[] {
  return [...Buffer.from(id, 'ascii'), ...u32(body.length), ...body];
}

function clamp7(v: number): number { return Math.max(0, Math.min(127, Math.round(v))); }

interface Ev { tick: number; order: number; bytes: number[] }

function encodeEvents(events: Ev[]): number[] {
  events.sort((a, b) => a.tick - b.tick || a.order - b.order);
  const out: number[] = [];
  let last = 0;
  for (const e of events) {
    out.push(...encodeVarLen(e.tick - last), ...e.bytes);
    last = e.tick;
  }
  return out;
}

function textMeta(type: number, text: string): number[] {
  const bytes = [...Buffer.from(text, 'utf8')];
  return [0xff, type, ...encodeVarLen(bytes.length), ...bytes];
}

// ---------------------------------------------------------------------------
// Writer
// ---------------------------------------------------------------------------

export function writeMidiFile(spec: MidiFileSpec): Buffer {
  const ppq = spec.ppq ?? 480;
  if (!Number.isInteger(ppq) || ppq <= 0 || ppq > 32767) throw new Error(`ppq must be an integer 1..32767 (got ${ppq})`);
  const tempo = spec.tempo ?? 120;
  if (!(tempo > 0)) throw new Error(`tempo must be > 0 (got ${tempo})`);
  const ts = spec.timeSig ?? { numerator: 4, denominator: 4 };
  const denLog = Math.log2(ts.denominator);
  if (!Number.isInteger(denLog) || denLog < 0) throw new Error(`time signature denominator must be a power of two (got ${ts.denominator})`);
  const toTicks = (beats: number) => Math.round(beats * ppq);

  const chunks: number[][] = [];

  // Track 0: conductor (tempo, time signature)
  const conductor: Ev[] = [];
  conductor.push({ tick: 0, order: 0, bytes: textMeta(0x03, 'kbot') });
  conductor.push({ tick: 0, order: 1, bytes: [0xff, 0x51, 0x03, ...u24(Math.round(60_000_000 / tempo))] });
  conductor.push({ tick: 0, order: 2, bytes: [0xff, 0x58, 0x04, ts.numerator & 0xff, denLog & 0xff, 24, 8] });
  conductor.push({ tick: 0, order: 3, bytes: [0xff, 0x2f, 0x00] });
  chunks.push(chunk('MTrk', encodeEvents(conductor)));

  spec.tracks.forEach((t, ti) => {
    const evs: Ev[] = [];
    let order = 0;
    if (t.name) evs.push({ tick: 0, order: order++, bytes: textMeta(0x03, t.name) });
    if (t.program !== undefined) evs.push({ tick: 0, order: order++, bytes: [0xc0 | ((t.notes[0]?.channel ?? 0) & 0x0f), clamp7(t.program)] });
    let lastTick = 0;
    for (const n of t.notes) {
      if (!Number.isFinite(n.start) || n.start < 0) throw new Error(`track ${ti}: note start must be >= 0`);
      if (!(n.duration > 0)) throw new Error(`track ${ti}: note duration must be > 0`);
      const ch = (n.channel ?? 0) & 0x0f;
      const on = toTicks(n.start);
      const off = Math.max(on + 1, toTicks(n.start + n.duration));
      const vel = Math.max(1, clamp7(n.velocity ?? 100));
      // note-offs first at equal ticks (order 1 vs 2) so re-triggers of the same pitch survive
      evs.push({ tick: on, order: 1000 + order++, bytes: [0x90 | ch, clamp7(n.pitch), vel] });
      evs.push({ tick: off, order: 500, bytes: [0x80 | ch, clamp7(n.pitch), 64] });
      lastTick = Math.max(lastTick, off);
    }
    evs.push({ tick: lastTick, order: 1_000_000, bytes: [0xff, 0x2f, 0x00] });
    chunks.push(chunk('MTrk', encodeEvents(evs)));
  });

  const header = chunk('MThd', [...u16(1), ...u16(chunks.length), ...u16(ppq)]);
  return Buffer.from([...header, ...chunks.flat()]);
}

// ---------------------------------------------------------------------------
// Reader
// ---------------------------------------------------------------------------

export function readMidiFile(input: Buffer | Uint8Array): MidiFile {
  const buf = input instanceof Uint8Array ? input : new Uint8Array(input);
  let i = 0;
  const readStr = (n: number) => { const s = Buffer.from(buf.subarray(i, i + n)).toString('ascii'); i += n; return s; };
  const rd32 = () => { const v = ((buf[i] << 24) | (buf[i + 1] << 16) | (buf[i + 2] << 8) | buf[i + 3]) >>> 0; i += 4; return v; };
  const rd16 = () => { const v = (buf[i] << 8) | buf[i + 1]; i += 2; return v; };
  if (buf.length < 14 || readStr(4) !== 'MThd') throw new Error('not a MIDI file (missing MThd)');
  const hlen = rd32();
  const format = rd16();
  const ntrks = rd16();
  const division = rd16();
  if (division & 0x8000) throw new Error('SMPTE time division is not supported');
  i = 8 + hlen;
  const file: MidiFile = { format, ppq: division, tracks: [] };

  for (let t = 0; t < ntrks && i < buf.length; t++) {
    const id = readStr(4);
    const len = rd32();
    const end = i + len;
    if (id !== 'MTrk') { i = end; continue; }
    const track: MidiFileTrack = { notes: [] };
    const open = new Map<string, { start: number; velocity: number }>();
    let tick = 0;
    let status = 0;
    while (i < end) {
      const dv = decodeVarLen(buf, i);
      tick += dv.value;
      i = dv.next;
      let b = buf[i];
      if (b === 0xff) {
        const type = buf[i + 1];
        const l = decodeVarLen(buf, i + 2);
        const data = buf.subarray(l.next, l.next + l.value);
        i = l.next + l.value;
        if (type === 0x03 && !track.name) track.name = Buffer.from(data).toString('utf8');
        else if (type === 0x51 && file.tempo === undefined) file.tempo = Math.round((60_000_000 / ((data[0] << 16) | (data[1] << 8) | data[2])) * 1000) / 1000;
        else if (type === 0x58 && file.timeSig === undefined) file.timeSig = { numerator: data[0], denominator: 2 ** data[1] };
        else if (type === 0x2f) { i = end; }
        continue;
      }
      if (b === 0xf0 || b === 0xf7) {
        const l = decodeVarLen(buf, i + 1);
        i = l.next + l.value;
        continue;
      }
      if (b & 0x80) { status = b; i++; } else { b = status; }
      const hi = status & 0xf0;
      const ch = status & 0x0f;
      const nData = (hi === 0xc0 || hi === 0xd0) ? 1 : 2;
      const d1 = buf[i];
      const d2 = nData === 2 ? buf[i + 1] : 0;
      i += nData;
      if (hi === 0x90 && d2 > 0) {
        open.set(`${ch}:${d1}`, { start: tick, velocity: d2 });
      } else if (hi === 0x80 || (hi === 0x90 && d2 === 0)) {
        const key = `${ch}:${d1}`;
        const o = open.get(key);
        if (o) {
          open.delete(key);
          track.notes.push({ pitch: d1, start: o.start / division, duration: Math.max(tick - o.start, 1) / division, velocity: o.velocity, channel: ch });
        }
      } else if (hi === 0xc0 && track.program === undefined) {
        track.program = d1;
      }
    }
    i = end;
    track.notes.sort((a, b2) => a.start - b2.start || a.pitch - b2.pitch);
    file.tracks.push(track);
  }
  return file;
}
