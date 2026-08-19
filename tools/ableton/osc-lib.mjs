// tools/ableton/osc-lib.mjs -- tiny AbletonOSC client shared by e2e.mjs and kbot-reload.mjs.
// Sends to UDP 11000, listens on UDP 11001 (the AbletonOSC reply port). Only ONE process
// may hold 11001 at a time (kbot MCP server, osc-probe.mjs, this) -- run serially.
import dgram from 'node:dgram';

const pad4 = n => (4 - (n % 4)) % 4;
function encStr(s) { const b = Buffer.from(s + '\0', 'utf8'); return Buffer.concat([b, Buffer.alloc(pad4(b.length))]); }
export function encode(addr, args) {
  let tags = ','; const parts = [];
  for (const a of args) {
    if (typeof a === 'number' && Number.isInteger(a)) { tags += 'i'; const b = Buffer.alloc(4); b.writeInt32BE(a); parts.push(b); }
    else if (typeof a === 'number') { tags += 'f'; const b = Buffer.alloc(4); b.writeFloatBE(a); parts.push(b); }
    else if (typeof a === 'boolean') { tags += a ? 'T' : 'F'; }
    else { tags += 's'; parts.push(encStr(String(a))); }
  }
  return Buffer.concat([encStr(addr), encStr(tags), ...parts]);
}
export function decode(buf) {
  let o = 0;
  const rs = () => { const e = buf.indexOf(0, o); const s = buf.toString('utf8', o, e); o = e + 1; o += pad4(o); return s; };
  const addr = rs(); if (!addr.startsWith('/')) return null;
  const tags = rs(); const args = [];
  for (const t of tags.slice(1)) {
    if (t === 'i') { args.push(buf.readInt32BE(o)); o += 4; }
    else if (t === 'f') { args.push(buf.readFloatBE(o)); o += 4; }
    else if (t === 'd') { args.push(buf.readDoubleBE(o)); o += 8; }
    else if (t === 'h') { args.push(Number(buf.readBigInt64BE(o))); o += 8; }
    else if (t === 's') { args.push(rs()); }
    else if (t === 'T') { args.push(true); }
    else if (t === 'F') { args.push(false); }
    else if (t === 'N') { args.push(null); }
    else { args.push('?' + t); }
  }
  return { addr, args };
}

export class OscClient {
  constructor({ host = '127.0.0.1', sendPort = 11000, recvPort = 11001 } = {}) {
    this.host = host; this.sendPort = sendPort; this.recvPort = recvPort;
    this.sock = dgram.createSocket({ type: 'udp4', recvBufferSize: 1 << 20 });
    this.waiters = new Map(); // addr -> [resolve]
    this.log = [];
    this.sock.on('message', m => {
      const d = decode(m); if (!d) return;
      this.log.push(d);
      const q = this.waiters.get(d.addr);
      if (q && q.length) q.shift()(d);
    });
  }
  async open() {
    await new Promise((res, rej) => { this.sock.once('error', rej); this.sock.bind(this.recvPort, this.host, res); });
  }
  close() { try { this.sock.close(); } catch {} }
  /** Send addr+args and wait for the first reply on the SAME address (AbletonOSC replies on the request address). */
  query(addr, args = [], timeoutMs = 3000) {
    return new Promise(resolve => {
      const timer = setTimeout(() => {
        const q = this.waiters.get(addr) || []; const i = q.indexOf(onReply); if (i >= 0) q.splice(i, 1);
        resolve(null);
      }, timeoutMs);
      const onReply = d => { clearTimeout(timer); resolve(d); };
      if (!this.waiters.has(addr)) this.waiters.set(addr, []);
      this.waiters.get(addr).push(onReply);
      this.sock.send(encode(addr, args), this.sendPort, this.host);
    });
  }
  /** kbot handler call: /live/kbot/<name>, reply is one JSON string. Returns parsed object or {ok:false,error:'timeout'}. */
  async kbot(name, args = [], timeoutMs = 4000) {
    const addr = name.startsWith('/') ? name : '/live/kbot/' + name;
    const d = await this.query(addr, args, timeoutMs);
    if (!d) return { ok: false, error: 'timeout: no reply on ' + addr, _timeout: true };
    const s = d.args[0];
    if (typeof s !== 'string') return { ok: false, error: 'non-string reply', raw: d.args };
    try { return JSON.parse(s); } catch (e) { return { ok: false, error: 'bad JSON reply: ' + e.message, raw: s.slice(0, 200) }; }
  }
}
