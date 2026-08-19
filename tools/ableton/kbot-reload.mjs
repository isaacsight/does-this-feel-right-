// tools/ableton/kbot-reload.mjs -- hot-reload kbot_ext.py inside the running Live.
//
//   node tools/ableton/kbot-reload.mjs            # /live/api/reload, then ping; bootstrap if needed
//   node tools/ableton/kbot-reload.mjs --bootstrap # force the manager.py class swap
//
// Why bootstrap: /live/api/reload re-imports the abletonosc.* submodules but NOT
// AbletonOSC/manager.py itself, so on the very FIRST install (Live already running with
// the pre-patch Manager class) the KbotHandler line in manager.py's handlers list is not
// seen and /live/kbot/ping stays silent. This script uses the pre-existing local
// /live/exec handler to reload the AbletonOSC.manager module, swap the live Manager
// instance's __class__ to the fresh class, and call reload_imports() -- after which
// plain /live/api/reload works for every later edit. Needs UDP 11001 free.
import { OscClient } from './osc-lib.mjs';

const BOOTSTRAP = `import sys, importlib
mgr = [c for c in app.control_surfaces if type(c).__name__ == "Manager" and type(c).__module__ == "AbletonOSC.manager"][0]
mod = importlib.reload(sys.modules["AbletonOSC.manager"])
mgr.__class__ = mod.Manager
mgr.reload_imports()
_result = "bootstrapped: handlers=%d kbot=%s" % (len(mgr.handlers), any(type(h).__name__ == "KbotHandler" for h in mgr.handlers))
`;

const force = process.argv.includes('--bootstrap');
const c = new OscClient();
try { await c.open(); } catch (e) { console.error('cannot bind UDP 11001 (another client holds it?):', e.message); process.exit(2); }
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ok = false;
if (!force) {
  await c.query('/live/api/reload', [], 800);
  await sleep(1200);
  const p = await c.kbot('ping', [], 2500);
  if (p.ok) { console.log('reload ok:', JSON.stringify(p)); ok = true; }
  else console.log('ping after /live/api/reload: no reply -> bootstrapping via /live/exec');
}
if (!ok) {
  const d = await c.query('/live/exec', [BOOTSTRAP], 6000);
  console.log('bootstrap:', d ? JSON.stringify(d.args) : 'no reply from /live/exec (is the local /live/exec edit loaded?)');
  await sleep(1200);
  const p = await c.kbot('ping', [], 2500);
  if (p.ok) { console.log('ping ok:', JSON.stringify(p)); ok = true; }
  else console.log('ping still silent; read AbletonOSC/logs/abletonosc.log');
}
c.close();
process.exit(ok ? 0 : 1);
