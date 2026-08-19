/**
 * maxpat.ts — Max for Live device skeletons (.maxpat + bundled JS).
 *
 * writeMaxForLiveSkeleton() returns a valid Max 8/9 patcher document
 * ({"patcher":{fileversion, appversion, boxes, lines, …}}) with the right I/O
 * objects for the device kind, a [js kbot_liveapi.js] box (LiveAPI get / set /
 * call / describe / observe by LOM path) fed by [live.thisdevice], and — when
 * useNodeForMax is set — a [node.script kbot_node.js] box plus package.json.
 *
 * What it does NOT do: write an .amxd. Live's .amxd container wraps the
 * patcher JSON in a binary framing (ampf/meta/ptch chunks + device metadata)
 * that we do not reproduce; open the .maxpat in Max and save it from a Max for
 * Live device patcher instead (see the README the generator emits).
 */

export type M4LDeviceKind = 'midi_effect' | 'audio_effect' | 'instrument';

export interface M4LSkeletonSpec {
  /** Device name (used for file names). */
  name: string;
  kind: M4LDeviceKind;
  /** Add a [node.script kbot_node.js] box + package.json (Node for Max). */
  useNodeForMax?: boolean;
  /** TCP port for the Node for Max JSON-lines bridge (default 9998). */
  nodePort?: number;
  /** Max version to stamp in appversion (default 8.6.5). */
  maxVersion?: { major: number; minor: number; revision: number };
}

export interface M4LSkeleton {
  /** The .maxpat JSON text. */
  maxpat: string;
  /** Every file to write next to each other: <name>.maxpat, kbot_liveapi.js, (kbot_node.js, package.json), README.md */
  files: Record<string, string>;
}

interface Box {
  id: string;
  maxclass: string;
  text?: string;
  numinlets: number;
  numoutlets: number;
  outlettype?: string[];
  patching_rect: [number, number, number, number];
  extra?: Record<string, unknown>;
}

interface Line { source: [string, number]; destination: [string, number]; }

class PatchBuilder {
  boxes: Box[] = [];
  lines: Line[] = [];
  private n = 0;

  obj(text: string, x: number, y: number, io: { in: number; out: number; outlettype?: string[] }, w = Math.max(40, text.length * 7 + 12)): string {
    const id = `obj-${++this.n}`;
    this.boxes.push({ id, maxclass: 'newobj', text, numinlets: io.in, numoutlets: io.out, outlettype: io.outlettype ?? new Array(io.out).fill(''), patching_rect: [x, y, w, 22] });
    return id;
  }

  msg(text: string, x: number, y: number, w = Math.max(40, text.length * 7 + 12)): string {
    const id = `obj-${++this.n}`;
    this.boxes.push({ id, maxclass: 'message', text, numinlets: 2, numoutlets: 1, outlettype: [''], patching_rect: [x, y, w, 22] });
    return id;
  }

  comment(text: string, x: number, y: number, w = 320, h = 20): string {
    const id = `obj-${++this.n}`;
    this.boxes.push({ id, maxclass: 'comment', text, numinlets: 1, numoutlets: 0, patching_rect: [x, y, w, h] });
    return id;
  }

  connect(from: string, outlet: number, to: string, inlet: number): void {
    this.lines.push({ source: [from, outlet], destination: [to, inlet] });
  }
}

const NODE_FILE = 'kbot_node.js';
const LIVEAPI_FILE = 'kbot_liveapi.js';

/** Build the .maxpat JSON string only. */
export function writeMaxPatcher(spec: M4LSkeletonSpec): string {
  const p = new PatchBuilder();
  const kindLabel = { midi_effect: 'MIDI Effect', audio_effect: 'Audio Effect', instrument: 'Instrument' }[spec.kind];
  if (!kindLabel) throw new Error(`unknown Max for Live device kind "${spec.kind}"`);

  p.comment(`${spec.name} - kbot Max for Live ${kindLabel} skeleton. Save from a Max ${kindLabel} device patcher inside Live to get an .amxd.`, 30, 15, 560, 33);

  // I/O
  if (spec.kind === 'midi_effect') {
    const midiin = p.obj('midiin', 30, 70, { in: 1, out: 1, outlettype: ['int'] });
    const midiout = p.obj('midiout', 30, 250, { in: 1, out: 0 });
    p.connect(midiin, 0, midiout, 0);
    p.comment('MIDI passes straight through; put your processing between midiin and midiout.', 100, 70, 400);
  } else if (spec.kind === 'audio_effect') {
    const pin = p.obj('plugin~', 30, 70, { in: 1, out: 2, outlettype: ['signal', 'signal'] });
    const pout = p.obj('plugout~', 30, 250, { in: 2, out: 0 });
    p.connect(pin, 0, pout, 0);
    p.connect(pin, 1, pout, 1);
    p.comment('Audio passes straight through; put your DSP between plugin~ and plugout~.', 100, 70, 400);
  } else {
    // Instrument: minimal sine voice so the device makes sound out of the box
    const midiin = p.obj('midiin', 30, 70, { in: 1, out: 1, outlettype: ['int'] });
    const parse = p.obj('midiparse', 30, 105, { in: 1, out: 8, outlettype: ['', '', '', 'int', 'int', 'int', 'int', 'int'] });
    const unpack = p.obj('unpack 0 0', 30, 140, { in: 1, out: 2, outlettype: ['int', 'int'] });
    const mtof = p.obj('mtof', 30, 175, { in: 1, out: 1, outlettype: ['float'] });
    const osc = p.obj('cycle~', 30, 210, { in: 2, out: 1, outlettype: ['signal'] });
    const gain = p.obj('*~ 0.1', 30, 245, { in: 2, out: 1, outlettype: ['signal'] });
    const pout = p.obj('plugout~', 30, 290, { in: 2, out: 0 });
    p.connect(midiin, 0, parse, 0);
    p.connect(parse, 0, unpack, 0);
    p.connect(unpack, 0, mtof, 0);
    p.connect(mtof, 0, osc, 0);
    p.connect(osc, 0, gain, 0);
    p.connect(gain, 0, pout, 0);
    p.connect(gain, 0, pout, 1);
    p.comment('Placeholder sine voice: replace cycle~ with your synth.', 100, 70, 400);
  }

  // LiveAPI helper
  const thisdev = p.obj('live.thisdevice', 400, 70, { in: 1, out: 3, outlettype: ['bang', 'int', 'int'] });
  const initMsg = p.msg('describe live_set', 400, 110);
  const js = p.obj(`js ${LIVEAPI_FILE}`, 400, 200, { in: 1, out: 2, outlettype: ['', ''] }, 140);
  const printer = p.obj('print kbot', 400, 250, { in: 1, out: 0 });
  p.connect(thisdev, 0, initMsg, 0);
  p.connect(initMsg, 0, js, 0);
  p.connect(js, 0, printer, 0);
  const ex1 = p.msg('get live_set : tempo', 560, 110);
  const ex2 = p.msg('set live_set : tempo 120', 560, 140);
  const ex3 = p.msg('call live_set : create_midi_track -1', 560, 170);
  p.connect(ex1, 0, js, 0);
  p.connect(ex2, 0, js, 0);
  p.connect(ex3, 0, js, 0);
  p.comment('LiveAPI by path: get|set|call|describe|children|observe <path> : <prop|method> [args]', 400, 285, 420);

  if (spec.useNodeForMax) {
    const port = spec.nodePort ?? 9998;
    const node = p.obj(`node.script ${NODE_FILE} ${port}`, 400, 340, { in: 1, out: 2, outlettype: ['', ''] }, 220);
    const start = p.msg('script start', 400, 310);
    p.connect(thisdev, 0, start, 0);
    p.connect(start, 0, node, 0);
    // node -> js (LOM requests over TCP arrive as "lom get live_set : tempo" lists) and back
    p.connect(node, 0, js, 0);
    p.connect(js, 1, node, 0);
    p.comment(`Node for Max bridge: JSON lines on TCP 127.0.0.1:${port} -> LiveAPI, replies back on the socket.`, 400, 375, 420);
  }

  const mv = spec.maxVersion ?? { major: 8, minor: 6, revision: 5 };
  const doc = {
    patcher: {
      fileversion: 1,
      appversion: { major: mv.major, minor: mv.minor, revision: mv.revision, architecture: 'x64', modernui: 1 },
      classnamespace: 'box',
      rect: [100.0, 100.0, 900.0, 520.0],
      bglocked: 0,
      openinpresentation: 0,
      default_fontsize: 12.0,
      default_fontface: 0,
      default_fontname: 'Arial',
      gridonopen: 1,
      gridsize: [15.0, 15.0],
      gridsnaponopen: 1,
      objectsnaponopen: 1,
      statusbarvisible: 2,
      toolbarvisible: 1,
      lefttoolbarpinned: 0,
      toptoolbarpinned: 0,
      righttoolbarpinned: 0,
      bottomtoolbarpinned: 0,
      toolbars_unpinned_last_save: 0,
      tallnewobj: 0,
      boxanimatetime: 200,
      enablehscroll: 1,
      enablevscroll: 1,
      devicewidth: 0.0,
      description: `${spec.name} (${kindLabel}) generated by kbot`,
      digest: '',
      tags: 'kbot',
      style: '',
      subpatcher_template: '',
      assistshowspatchername: 0,
      boxes: p.boxes.map((b) => ({ box: { ...(b.extra ?? {}), id: b.id, maxclass: b.maxclass, ...(b.text !== undefined ? { text: b.text } : {}), numinlets: b.numinlets, numoutlets: b.numoutlets, ...(b.outlettype ? { outlettype: b.outlettype } : {}), patching_rect: b.patching_rect } })),
      lines: p.lines.map((l) => ({ patchline: { source: l.source, destination: l.destination } })),
      dependency_cache: [],
      autosave: 0,
    },
  };
  return JSON.stringify(doc, null, '\t');
}

/** Patcher + bundled JS + README, ready to write to a folder. */
export function writeMaxForLiveSkeleton(spec: M4LSkeletonSpec): M4LSkeleton {
  const maxpat = writeMaxPatcher(spec);
  const safe = spec.name.replace(/[^\w.-]+/g, '_');
  const files: Record<string, string> = {
    [`${safe}.maxpat`]: maxpat,
    [LIVEAPI_FILE]: liveApiJs(),
    'README.md': readme(spec, safe),
  };
  if (spec.useNodeForMax) {
    files[NODE_FILE] = nodeScript();
    files['package.json'] = JSON.stringify({ name: safe.toLowerCase(), version: '0.1.0', private: true, main: NODE_FILE, description: `Node for Max bridge for ${spec.name} (kbot)`, dependencies: {} }, null, 2) + '\n';
  }
  return { maxpat, files };
}

function readme(spec: M4LSkeletonSpec, safe: string): string {
  const kind = { midi_effect: 'Max MIDI Effect', audio_effect: 'Max Audio Effect', instrument: 'Max Instrument' }[spec.kind];
  return `# ${spec.name} - Max for Live skeleton (kbot)

Files:
- ${safe}.maxpat - the patcher (Max 8/9 JSON). Open it in Max to inspect.
- ${LIVEAPI_FILE} - LiveAPI helper for the [js] box: get / set / call / describe / children / observe by LOM path.
${spec.useNodeForMax ? `- ${NODE_FILE} + package.json - Node for Max script: TCP JSON-lines bridge on 127.0.0.1:${spec.nodePort ?? 9998}.\n` : ''}
## Turning this into an .amxd

We do not write .amxd files: Live wraps the patcher JSON in a binary container
(ampf / meta / ptch chunks plus device metadata) that only Max writes reliably.
Do this instead:

1. In Live, drop an empty "${kind}" from the browser (Max for Live > ${kind}) onto a track.
2. Click the device's Edit button; Max opens the device patcher.
3. In Max: File > Open... ${safe}.maxpat, select all (Cmd/Ctrl-A), copy, switch to the device
   patcher, paste, then Cmd/Ctrl-S. Live saves the .amxd next to your set (or into the User Library
   with Save As...). Copy ${LIVEAPI_FILE}${spec.useNodeForMax ? `, ${NODE_FILE} and package.json` : ''} next to the .amxd
   (Max resolves [js] / [node.script] files relative to the device, or add the folder to Max's search path).
4. The [live.thisdevice] bang sends "describe live_set" to the [js] box on load; check the Max console.

## Message grammar for [js ${LIVEAPI_FILE}]

    get <path> : <property>            e.g. get live_set tracks 0 : name
    set <path> : <property> <value>    e.g. set live_set : tempo 128
    call <path> : <method> [args...]   e.g. call live_set : create_midi_track -1
    describe <path>                    properties, children and functions of the object
    children <path>                    child counts (tracks, devices, clip_slots...)
    observe <path> : <property>        outlet 0 fires on every change (property or a list child)
    unobserve <path> : <property>

Paths use the Live Object Model grammar (space separated): live_set, tracks 0, devices 1,
clip_slots 2 clip, view, master_track, return_tracks 0, scenes 3, cue_points 0, this_device.
Replies leave outlet 0 as one JSON symbol; errors are {"ok":false,"error":...}.
`;
}

function liveApiJs(): string {
  return `// kbot_liveapi.js - LiveAPI helper for Max for Live [js] boxes (generated by kbot).
// Messages: get|set|call|describe|children|observe|unobserve <path> : <prop|method> [args]
// Outlet 0: JSON reply as one symbol. Outlet 1: JSON forwarded to a Node for Max box (if wired).
autowatch = 1;
inlets = 1;
outlets = 2;

var observers = {};

function out(obj) {
  var s = JSON.stringify(obj);
  outlet(0, s);
  outlet(1, s);
}

function splitArgs(args) {
  // "<path tokens...> : <rest tokens...>"; if there is no ':' the last token is the rest
  var i = -1;
  for (var k = 0; k < args.length; k++) { if (String(args[k]) === ':') { i = k; break; } }
  if (i === -1) {
    if (args.length < 2) return { path: args.join(' '), rest: [] };
    return { path: args.slice(0, args.length - 1).join(' '), rest: [args[args.length - 1]] };
  }
  return { path: args.slice(0, i).join(' '), rest: args.slice(i + 1) };
}

function open(path) {
  var api = new LiveAPI(null, path);
  if (!api || api.id == 0) throw new Error('no object at path "' + path + '"');
  return api;
}

function coerce(v) {
  if (typeof v !== 'string') return v;
  if (v === 'true') return 1;
  if (v === 'false') return 0;
  var n = Number(v);
  return isNaN(n) ? v : n;
}

function get() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  try {
    var api = open(s.path);
    var prop = s.rest[0];
    var v = api.get(prop);
    out({ ok: true, op: 'get', path: api.unquotedpath, id: api.id, prop: prop, value: v });
  } catch (e) { out({ ok: false, op: 'get', path: s.path, error: String(e) }); }
}

function set() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  try {
    var api = open(s.path);
    var prop = s.rest[0];
    var vals = s.rest.slice(1).map(coerce);
    api.set(prop, vals.length === 1 ? vals[0] : vals);
    out({ ok: true, op: 'set', path: api.unquotedpath, id: api.id, prop: prop, value: api.get(prop) });
  } catch (e) { out({ ok: false, op: 'set', path: s.path, error: String(e) }); }
}

function call() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  try {
    var api = open(s.path);
    var method = s.rest[0];
    var args = s.rest.slice(1).map(coerce);
    var r = api.call.apply(api, [method].concat(args));
    out({ ok: true, op: 'call', path: api.unquotedpath, id: api.id, method: method, result: r === undefined ? null : r });
  } catch (e) { out({ ok: false, op: 'call', path: s.path, error: String(e) }); }
}

function describe() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  try {
    var api = open(s.path || a.join(' '));
    var info = String(api.info).split('\\n');
    var props = [], children = [], funcs = [], type = '';
    for (var i = 0; i < info.length; i++) {
      var parts = info[i].replace(/^\\s+|\\s+$/g, '').split(' ');
      if (parts[0] === 'type') type = parts.slice(1).join(' ');
      else if (parts[0] === 'property') props.push({ name: parts[1], type: parts.slice(2).join(' ') });
      else if (parts[0] === 'child') children.push({ name: parts[1], type: parts.slice(2).join(' ') });
      else if (parts[0] === 'children') children.push({ name: parts[1], type: parts.slice(2).join(' '), list: true });
      else if (parts[0] === 'function') funcs.push(parts.slice(1).join(' '));
    }
    out({ ok: true, op: 'describe', path: api.unquotedpath, id: api.id, type: type, properties: props, children: children, functions: funcs });
  } catch (e) { out({ ok: false, op: 'describe', path: a.join(' '), error: String(e) }); }
}

function children() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  try {
    var api = open(s.path || a.join(' '));
    var counts = {};
    var info = String(api.info).split('\\n');
    for (var i = 0; i < info.length; i++) {
      var parts = info[i].replace(/^\\s+|\\s+$/g, '').split(' ');
      if (parts[0] === 'children') counts[parts[1]] = api.getcount(parts[1]);
    }
    out({ ok: true, op: 'children', path: api.unquotedpath, id: api.id, counts: counts });
  } catch (e) { out({ ok: false, op: 'children', path: a.join(' '), error: String(e) }); }
}

function observe() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  var key = s.path + ' : ' + s.rest[0];
  try {
    if (observers[key]) { observers[key].property = ''; delete observers[key]; }
    var api = new LiveAPI(function (args) {
      out({ ok: true, op: 'observe', path: s.path, prop: s.rest[0], value: args });
    }, s.path);
    if (!api || api.id == 0) throw new Error('no object at path "' + s.path + '"');
    api.property = s.rest[0];
    observers[key] = api;
    out({ ok: true, op: 'observe', path: api.unquotedpath, id: api.id, prop: s.rest[0], subscribed: true });
  } catch (e) { out({ ok: false, op: 'observe', path: s.path, error: String(e) }); }
}

function unobserve() {
  var a = arrayfromargs(arguments), s = splitArgs(a);
  var key = s.path + ' : ' + s.rest[0];
  if (observers[key]) { observers[key].property = ''; delete observers[key]; }
  out({ ok: true, op: 'unobserve', path: s.path, prop: s.rest[0] });
}

// Requests forwarded from Node for Max arrive as "lom <op> <path> : <rest>"
function lom() {
  var a = arrayfromargs(arguments);
  var op = String(a.shift());
  var fn = { get: get, set: set, call: call, describe: describe, children: children, observe: observe, unobserve: unobserve }[op];
  if (!fn) { out({ ok: false, error: 'unknown op ' + op }); return; }
  fn.apply(this, a);
}

function anything() {
  out({ ok: false, error: 'unknown message ' + messagename });
}
`;
}

function nodeScript(): string {
  return `// kbot_node.js - Node for Max bridge (generated by kbot).
// Listens on TCP 127.0.0.1:<port> for JSON lines {"op":"get","path":"live_set","prop":"tempo"} and
// forwards them to the [js kbot_liveapi.js] box as "lom get live_set : tempo". Replies coming back
// into this script (JSON symbols from the js box) are written to every connected socket.
const net = require('node:net');
const maxApi = require('max-api');

const port = Number(process.argv[2] || 9998);
const sockets = new Set();

function toList(msg) {
  const path = String(msg.path || 'live_set').split(/\\s+/).filter(Boolean);
  const rest = [];
  if (msg.prop) rest.push(msg.prop);
  if (msg.method) rest.push(msg.method);
  if (msg.value !== undefined) rest.push(...(Array.isArray(msg.value) ? msg.value : [msg.value]));
  if (Array.isArray(msg.args)) rest.push(...msg.args);
  return ['lom', msg.op, ...path, ...(rest.length ? [':', ...rest] : [])];
}

const server = net.createServer((sock) => {
  sockets.add(sock);
  let buf = '';
  sock.on('data', (d) => {
    buf += d.toString('utf8');
    let i;
    while ((i = buf.indexOf('\\n')) !== -1) {
      const line = buf.slice(0, i).trim();
      buf = buf.slice(i + 1);
      if (!line) continue;
      try {
        const msg = JSON.parse(line);
        if (msg.op === 'ping') { sock.write(JSON.stringify({ ok: true, op: 'ping', service: 'kbot-m4l' }) + '\\n'); continue; }
        maxApi.outlet(...toList(msg));
      } catch (e) {
        sock.write(JSON.stringify({ ok: false, error: String(e) }) + '\\n');
      }
    }
  });
  sock.on('close', () => sockets.delete(sock));
  sock.on('error', () => sockets.delete(sock));
});

server.listen(port, '127.0.0.1', () => maxApi.post('kbot_node: listening on 127.0.0.1:' + port));

// Any message that comes into the node.script inlet is treated as a reply for the sockets.
maxApi.addHandler(maxApi.MESSAGE_TYPES.ALL, (handled, ...args) => {
  const text = args.length === 1 && typeof args[0] === 'string' ? args[0] : JSON.stringify(args);
  for (const s of sockets) s.write(text + '\\n');
});
`;
}
