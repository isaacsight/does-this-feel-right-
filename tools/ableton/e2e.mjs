#!/usr/bin/env node
// tools/ableton/e2e.mjs -- Live acceptance test for kbot_ext (spec 3.5).
//
//   node tools/ableton/e2e.mjs            # run; exit 1 on any FAIL
//   KEEP=1 node tools/ableton/e2e.mjs     # leave the scratch track in the Set
//
// Serialized flow against the RUNNING Live (needs UDP 11001 free -- only one client
// may hold the AbletonOSC reply port): create MIDI track -> insert Operator -> write a
// 4-bar clip -> add automation -> set send A -> insert Saturator + EQ Eight -> fire ->
// read back every step -> stop -> cleanup (delete the track). Prints PASS/FAIL per
// step. Every PASS is a read-back from Live, never the value we sent. Re-runnable:
// stale "kbot-e2e" tracks from an aborted run are deleted first.
import { OscClient } from './osc-lib.mjs';

const TRACK_NAME = 'kbot-e2e';
const c = new OscClient();
try { await c.open(); } catch (e) { console.error('FAIL bind UDP 11001:', e.message, '(another client holds the reply port?)'); process.exit(2); }
const sleep = ms => new Promise(r => setTimeout(r, ms));
const results = [];
let trackIndex = null;
const short = v => { const s = JSON.stringify(v); return s.length > 220 ? s.slice(0, 220) + '...' : s; };

function record(name, ok, detail) {
  results.push({ name, ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? '  -- ' + detail : ''}`);
  return ok;
}
async function step(name, fn) {
  try {
    const out = await fn();
    if (out && out.__fail) return record(name, false, out.__fail);
    return record(name, true, out === undefined ? '' : (typeof out === 'string' ? out : short(out)));
  } catch (e) {
    return record(name, false, String(e && e.message || e));
  }
}
const kb = (n, a, t) => c.kbot(n, a, t);
const need = (r, what) => { if (!r || !r.ok) throw new Error(`${what}: ${r ? r.error : 'no reply'}`); return r; };
const eq = (a, b, what) => { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(`${what}: got ${short(a)}, want ${short(b)}`); };
const near = (a, b, tol, what) => { if (typeof a !== 'number' || Math.abs(a - b) > tol) throw new Error(`${what}: got ${a}, want ~${b}`); };
const track = () => { if (trackIndex === null) throw new Error('no scratch track'); return trackIndex; };
const tp = () => `live_set tracks ${track()}`;

// 0. handler alive
const alive = await step('ping /live/kbot/ping', async () => {
  const r = need(await kb('ping', [], 3000), 'ping');
  return `kbot_ext ${r.kbot_ext} live ${r.live} handlers ${r.handlers}`;
});
if (!alive) { console.log('kbot_ext not answering; run: node tools/ableton/kbot-reload.mjs'); c.close(); process.exit(1); }

// 1. pre-clean stale scratch tracks (re-runnable), remembering the user's track count
let baseline = null;
await step('pre-clean stale scratch tracks', async () => {
  for (let guard = 0; guard < 8; guard++) {
    const r = need(await kb('lom/get', ['live_set', 'tracks']), 'list tracks');
    const stale = r.value.findIndex(t => t.name === TRACK_NAME);
    if (stale < 0) { baseline = r.value.length; return `baseline ${baseline} tracks`; }
    need(await kb('track/delete', [stale]), 'delete stale');
  }
  throw new Error('could not clear stale scratch tracks');
});

// 2. create MIDI track
await step('track/create midi -1 kbot-e2e', async () => {
  const r = need(await kb('track/create', ['midi', -1, TRACK_NAME]), 'track/create');
  const rb = need(await kb('lom/get', [`live_set tracks ${r.index}`, 'name']), 'read back name');
  eq(rb.value, TRACK_NAME, 'track name read-back');
  const midi = need(await kb('lom/get', [`live_set tracks ${r.index}`, 'has_midi_input']), 'has_midi_input');
  eq(midi.value, true, 'has_midi_input');
  trackIndex = r.index;
  return `index ${r.index}, name ${rb.value}`;
});

// 3. insert Operator
await step('track/insert_device Operator', async () => {
  const r = need(await kb('track/insert_device', [track(), 'Operator'], 8000), 'insert Operator');
  const rb = need(await kb('lom/get', [tp(), 'devices']), 'read back devices');
  eq(rb.value.map(d => d.name), ['Operator'], 'devices after Operator');
  return `method ${r.method}, devices ${short(rb.value.map(d => d.name))}`;
});

// 4. create a 4-bar (16 beat) clip + notes
const NOTES = [
  { pitch: 36, start: 0, duration: 1, velocity: 110 },
  { pitch: 43, start: 4, duration: 1, velocity: 100 },
  { pitch: 48, start: 8, duration: 2, velocity: 96 },
  { pitch: 55, start: 12, duration: 4, velocity: 90 },
];
await step('create 4-bar clip (clip_slots 0 create_clip 16.0)', async () => {
  need(await kb('lom/call', [`${tp()} clip_slots 0`, 'create_clip', '[16.0]']), 'create_clip');
  const rb = need(await kb('lom/get', [`${tp()} clip_slots 0`, 'has_clip']), 'has_clip');
  eq(rb.value, true, 'has_clip');
  const len = need(await kb('lom/get', [`${tp()} clip_slots 0 clip`, 'length']), 'length');
  near(len.value, 16, 1e-6, 'clip length');
  return `has_clip true, length ${len.value}`;
});
await step('clip/notes set (4 notes) + read back', async () => {
  const r = need(await kb('clip/notes', ['set', track(), 0, JSON.stringify(NOTES)]), 'notes set');
  const rb = need(await kb('clip/notes', ['get', track(), 0]), 'notes get');
  const got = rb.notes.map(n => [n.pitch, n.start, n.duration, n.velocity]);
  eq(got, NOTES.map(n => [n.pitch, n.start, n.duration, n.velocity]), 'notes read-back');
  return `count ${rb.count}`;
});

// 5. automation on the Operator's first non-quantized parameter (values in the parameter's own units)
await step('clip/automation on Operator param + read back', async () => {
  const d = need(await kb('lom/describe', [`${tp()} devices 0`]), 'describe Operator');
  // find first non-quantized parameter index by walking parameters
  let pIndex = null, pName = null, pMin = 0, pMax = 1;
  for (let i = 1; i < 12; i++) {
    const q = await kb('lom/get', [`${tp()} devices 0 parameters ${i}`, 'is_quantized']);
    if (q && q.ok && q.value === false) {
      pIndex = i;
      pName = need(await kb('lom/get', [`${tp()} devices 0 parameters ${i}`, 'name']), 'param name').value;
      pMin = need(await kb('lom/get', [`${tp()} devices 0 parameters ${i}`, 'min']), 'param min').value;
      pMax = need(await kb('lom/get', [`${tp()} devices 0 parameters ${i}`, 'max']), 'param max').value;
      break;
    }
  }
  if (pIndex === null) throw new Error('no non-quantized Operator parameter found in the first 12');
  const v1 = pMin + (pMax - pMin) * 0.25, v2 = pMin + (pMax - pMin) * 0.75;
  const r = need(await kb('clip/automation', [`${tp()} clip_slots 0 clip`, `${tp()} devices 0 parameters ${pIndex}`,
    JSON.stringify([[0, 4, v1], [8, 4, v2]])]), 'automation');
  const he = need(await kb('lom/get', [`${tp()} clip_slots 0 clip`, 'has_envelopes']), 'has_envelopes');
  eq(he.value, true, 'has_envelopes');
  if (!Array.isArray(r.readback) || r.readback.length !== 2) throw new Error('readback missing');
  // Transpose-like integer parameters round; accept within 1 unit of the requested value
  near(r.readback[0][1], v1, Math.max(1, (pMax - pMin) * 0.02), 'value at step 1');
  near(r.readback[1][1], v2, Math.max(1, (pMax - pMin) * 0.02), 'value at step 2');
  return `${pName} (#${pIndex}) envelope created=${r.created_envelope} readback ${short(r.readback)} type=${d.type}`;
});

// 6. set send A
await step('set send A = 0.5 (mixer_device sends 0) + read back', async () => {
  const r = need(await kb('lom/set', [`${tp()} mixer_device sends 0`, 'value', 0.5]), 'set send A');
  const rb = need(await kb('lom/get', [`${tp()} mixer_device sends 0`, 'value']), 'read send A');
  near(rb.value, 0.5, 1e-4, 'send A');
  return `send A ${rb.value} (previous ${r.previous})`;
});

// 7. Saturator + EQ Eight
await step('track/insert_device Saturator + EQ Eight', async () => {
  need(await kb('track/insert_device', [track(), 'Saturator'], 8000), 'insert Saturator');
  need(await kb('track/insert_device', [track(), 'EQ Eight'], 8000), 'insert EQ Eight');
  const rb = need(await kb('lom/get', [tp(), 'devices']), 'read back devices');
  eq(rb.value.map(d => d.name), ['Operator', 'Saturator', 'EQ Eight'], 'device chain');
  return short(rb.value.map(d => d.name));
});
await step('device/set_active Saturator off/on + read back', async () => {
  need(await kb('device/set_active', [track(), 1, 0]), 'set inactive');
  const off = need(await kb('lom/get', [`${tp()} devices 1`, 'is_active']), 'read is_active');
  eq(off.value, false, 'is_active after off');
  need(await kb('device/set_active', [track(), 1, 1]), 'set active');
  const on = need(await kb('lom/get', [`${tp()} devices 1`, 'is_active']), 'read is_active');
  eq(on.value, true, 'is_active after on');
  return 'false -> true';
});

// 8. fire, read back, stop
await step('fire clip slot 0, read is_playing, stop', async () => {
  need(await kb('lom/call', [`${tp()} clip_slots 0`, 'fire', '[]']), 'fire');
  let playing = false;
  for (let i = 0; i < 12 && !playing; i++) {
    await sleep(250);
    const r = await kb('lom/get', [`${tp()} clip_slots 0 clip`, 'is_playing']);
    playing = !!(r && r.ok && r.value);
  }
  const songPlaying = need(await kb('lom/get', ['live_set', 'is_playing']), 'song is_playing').value;
  need(await kb('lom/call', ['live_set', 'stop_playing', '[]']), 'stop_playing');
  await sleep(300);
  const after = need(await kb('lom/get', ['live_set', 'is_playing']), 'song is_playing after stop').value;
  if (!playing) throw new Error(`clip never reported is_playing (song is_playing=${songPlaying})`);
  if (after) throw new Error('song still playing after stop_playing');
  return `clip is_playing true, song is_playing ${songPlaying} -> ${after}`;
});

// 9. undo group: two edits, one undo reverts both
await step('song/undo_group begin/end + one undo reverts both edits', async () => {
  need(await kb('song/undo_group', ['begin']), 'begin');
  need(await kb('lom/set', [tp(), 'name', TRACK_NAME + '-undo']), 'rename');
  need(await kb('lom/set', [`${tp()} mixer_device panning`, 'value', 0.4]), 'pan');
  need(await kb('song/undo_group', ['end']), 'end');
  await c.query('/live/song/undo', [], 500); // AbletonOSC undo has no reply
  await sleep(300);
  const name = need(await kb('lom/get', [tp(), 'name']), 'name').value;
  const pan = need(await kb('lom/get', [`${tp()} mixer_device panning`, 'value']), 'pan').value;
  eq(name, TRACK_NAME, 'name reverted');
  near(pan, 0, 1e-6, 'pan reverted');
  return `name ${name}, pan ${pan}`;
});

// 10. snapshot sanity
await step('snapshot < 60000 bytes and lists the scratch track', async () => {
  const r = need(await kb('snapshot', []), 'snapshot');
  const bytes = JSON.stringify(r).length;
  if (bytes >= 60000) throw new Error(`snapshot ${bytes} bytes`);
  const names = (r.tracks || []).map(t => t.name);
  if (!names.includes(TRACK_NAME)) throw new Error(`scratch track missing from snapshot: ${short(names)}`);
  return `${bytes} bytes, truncated=${r.truncated}, level=${r.level}, ${r.counts.tracks} tracks`;
});

// 11. cleanup
if (process.env.KEEP) {
  record('cleanup (skipped, KEEP=1)', true, `track ${trackIndex} kept`);
} else {
  await step('cleanup: track/delete scratch + track count restored', async () => {
    need(await kb('track/delete', [track()]), 'delete');
    const r = need(await kb('lom/get', ['live_set', 'tracks']), 'list tracks');
    if (r.value.some(t => t.name === TRACK_NAME)) throw new Error('scratch track still present');
    if (baseline !== null && r.value.length !== baseline) throw new Error(`track count ${r.value.length} != baseline ${baseline}`);
    return `${r.value.length} tracks (baseline ${baseline})`;
  });
}

c.close();
const fails = results.filter(r => !r.ok).length;
console.log(`\n${results.length - fails}/${results.length} PASS, ${fails} FAIL`);
process.exit(fails ? 1 : 0);
