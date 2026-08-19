// tools/ableton/osc-probe.mjs — short-lived AbletonOSC client for smoke tests.
// Usage: node tools/ableton/osc-probe.mjs '[["/live/test"],["/live/song/get/tempo"]]'
// Env: WAIT=ms between sends (default 400). Binds UDP 11001 for the duration; only
// ONE process may hold 11001 at a time (kbot MCP included) — run probes serially.
// Minimal OSC client: send to 11000, listen on 11001, print replies.
import dgram from 'node:dgram';
const pad4 = n => (4 - (n % 4)) % 4;
function encStr(s){ const b=Buffer.from(s+'\0','utf8'); return Buffer.concat([b,Buffer.alloc(pad4(b.length))]); }
function encode(addr,args){ let tags=','; const parts=[];
  for(const a of args){ if(typeof a==='number'&&Number.isInteger(a)){tags+='i';const b=Buffer.alloc(4);b.writeInt32BE(a);parts.push(b);}
    else if(typeof a==='number'){tags+='f';const b=Buffer.alloc(4);b.writeFloatBE(a);parts.push(b);}
    else if(typeof a==='boolean'){tags+=a?'T':'F';}
    else {tags+='s';parts.push(encStr(String(a)));} }
  return Buffer.concat([encStr(addr),encStr(tags),...parts]); }
function decode(buf){ let o=0; const rs=()=>{let e=buf.indexOf(0,o); const s=buf.toString('utf8',o,e); o=e+1; o+=pad4(o); return s;};
  const addr=rs(); if(!addr.startsWith('/'))return null; const tags=rs(); const args=[];
  for(const t of tags.slice(1)){ if(t==='i'){args.push(buf.readInt32BE(o));o+=4;} else if(t==='f'){args.push(+buf.readFloatBE(o).toFixed(4));o+=4;} else if(t==='d'){args.push(buf.readDoubleBE(o));o+=8;} else if(t==='s'){args.push(rs());} else if(t==='T'){args.push(true);} else if(t==='F'){args.push(false);} else if(t==='N'){args.push(null);} else {args.push('?'+t);} }
  return {addr,args}; }
const sock=dgram.createSocket('udp4');
const pending=[];
sock.on('message',m=>{const d=decode(m); if(d) console.log('  <-',d.addr,JSON.stringify(d.args).slice(0,300));});
await new Promise(r=>sock.bind(11001,'127.0.0.1',r));
const cmds=JSON.parse(process.argv[2]);
for(const [addr,...args] of cmds){ console.log('->',addr,JSON.stringify(args)); sock.send(encode(addr,args),11000,'127.0.0.1'); await new Promise(r=>setTimeout(r,Number(process.env.WAIT||400))); }
await new Promise(r=>setTimeout(r,600)); sock.close();
