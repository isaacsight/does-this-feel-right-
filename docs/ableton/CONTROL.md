# CONTROL.md — how Fable 5 / kbot drives Ableton Live

> Operator manual for the "control all of Ableton" substrate. Design contract:
> [`docs/superpowers/specs/2026-08-18-ableton-full-control-design.md`](../superpowers/specs/2026-08-18-ableton-full-control-design.md).
> Member-by-member reachability: [`lom-coverage.md`](./lom-coverage.md) (generated; regenerate with
> `node tools/ableton/gen-coverage.mjs`). History of how the planes were discovered:
> [`packages/kbot-ableton-extension/ABLETON_CONTROL_PLANES.md`](../../packages/kbot-ableton-extension/ABLETON_CONTROL_PLANES.md).

_Facts below marked **measured** were taken on 2026-08-18 on Isaac's Mac against Live 12.4.5b5 (the beta as
labelled by `Info.plist`; inside Live `Application.get_version_string()` reported `12.4.5b8` .. `b10` the same day,
the suffix increments per reload -- see VERIFICATION). Everything else is the contract the code is built to;
verify against Live before repeating it as fact. Tool action names in this file were reconciled against
`packages/kbot/src/tools/ableton-lom.ts` on 2026-08-18 (they are `create_track`, `clip_notes`, ... -- not the
address-derived `track_create` / `notes_set` the earlier draft assumed)._

---

## 0. Ground truth (measured 2026-08-18)

| Fact | Evidence |
|---|---|
| Live **12.4.5b5** running (`/Applications/Ableton Live 12 Beta.app`); 12.2 Suite also installed | `ps`, `Info.plist` |
| **AbletonOSC** loaded (UDP **11000** in / **11001** out) from `~/Music/Ableton/User Library/Remote Scripts/AbletonOSC`, upstream commit `0ca6821` + ~230 lines of local edits (`/live/exec`, `/live/track/load/device`, `/live/device/configure_all`, `/live/device/show_gui`, `/live/device/get/type_info`) | `lsof`, `git diff` |
| **KBotBridge** loaded (TCP **9997**, `127.0.0.1`, JSON-lines `{"action":...}`), 7 actions: `ping`, `browser_search`, `browser_load`, `browser_load_by_name`, `browser_categories`, `list_tracks`, `list_devices` | probe, `kbot_control_surface.py` |
| **AbletonBridge (TCP 9001) is NOT running** — kbot's `ableton_load_effect` / `ableton_browse` / `ableton_load_preset` / `ableton_effect_chain` are dead until routed through the OSC browser handlers | `lsof` |
| `kbot_bridge.py` (the March `/live/kbot/*` handlers) is **not installed** in the loaded AbletonOSC — at measurement time `ableton_create_track`, `ableton_load_sample`, `ableton_build_drum_rack` called addresses that do not exist; those three were re-routed onto `kbot_ext.py` the same day (`track/create`, `browser/load`, `drum/build_pad`, Live-verified). `produce_beat` and `design_sound` still call the dead March addresses (section 10) | `find`, `manager.py`, `grep` |
| `/live/master/*` does not exist in AbletonOSC (`ableton_audio_analysis` used it; now reads `master_track output_meter_*` through `/live/kbot/lom/get`); neither do `/live/device/set/enabled` (still sent by `ableton_device enable/disable`) and `/live/song/set/current_track` (still sent by `ableton_load_plugin`) | source grep, re-checked 2026-08-18 |
| OSC clip layer **works**: `create_clip` → `add/notes` → `get/notes` reads back exactly. The June "clip bug" is gone | probe |
| `/live/exec` works: arbitrary Python inside Live with `song`, `app`, `Live`, `tracks` in scope | probe |
| Full LOM dump taken from inside Live: `docs/ableton/lom-dump-12.4.5b5.json` (114 keys: 18 instance dumps + 95 class lists + `Live.modules` = 43 modules) | `/live/exec` → file |
| Only **one** process can bind UDP 11001 → Live probing must be serialized | `dgram` |
| AbletonOSC binds `0.0.0.0:11000` and replies to the sender's IP on 11001 | `abletonosc/osc_server.py` lines 15-16 |

---

## 1. The four planes

```
Fable 5 / kbot tools (TS)  ──UDP 11000──▶  AbletonOSC + kbot_ext.py (inside Live)  ──▶ LOM
        │                                       ▲ /live/api/reload hot-reloads it
        ├──TCP 9997──▶ KBotBridge (kept, thin)   │
        ├──peekaboo/computer-use──▶ Live UI (freeze/export/save/dialogs)
        ├──file generators──▶ .als / .adg / .adv / .mid / .maxpat / Remote Script / Extension
        └──Extensions SDK (human right-click) / Max for Live (real-time)  — unchanged
```

| Plane | What | Agent-driveable | Use it for |
|---|---|---|---|
| **A. Live control** — AbletonOSC + `kbot_ext.py` | Remote Script inside Live speaking UDP; `kbot_ext.py` adds a generic LOM plane (`/live/kbot/lom/*`) plus typed ops, all with JSON read-back | yes, primary | everything the LOM can do: transport, structure, notes, automation, devices, browser, racks, drum pads, undo groups |
| **B. Extensions SDK** | TS/JS that runs inside Live, triggered from a right-click menu | no (human triggers) | authoring with a native undo step when a human is at the keyboard; see `ABLETON_CONTROL_PLANES.md` |
| **C. Max for Live** | devices in the chain (`kbot-control.amxd`, `kbot-bridge.amxd`) | yes, within a device | real-time DSP, sample-accurate timing, `live.observer` listeners |
| **D. UI automation** | peekaboo / computer-use driving Live's windows and menus | yes | what the LOM cannot do: freeze, flatten, export, save/open, preferences, plugin GUIs (section 9) |

Plane A is the substrate; B and C are unchanged from the June map; D is documented but not built (spec section 5).

---

## 2. Ports and processes

| Port | Proto | Who | Status |
|---|---|---|---|
| **11000** | UDP | AbletonOSC listens (binds `0.0.0.0`) | required, loaded |
| **11001** | UDP | AbletonOSC replies to the sender's IP; **the kbot OSC client binds this to hear replies** | required — single binder rule below |
| **9997** | TCP | KBotBridge (`127.0.0.1`), JSON-lines | loaded, kept as a thin fallback (7 actions) |
| **9001** | TCP | AbletonBridge (353-tool Python bridge) | **optional / not running** — superseded by the OSC browser handlers |
| **9000** | TCP | `kbot-control.amxd` (JSON-RPC 2.0, `packages/kbot-control-standalone/`) | optional; only when the device is on a track |

### The single-binder-on-11001 rule

AbletonOSC sends every reply to UDP 11001. Only one process can bind that port. Consequences:

- Two agents probing Live at once = one of them gets `EADDRINUSE` (or, worse, swallows the other's replies).
  **Serialize all Live access.** Sub-agents that are not explicitly given Live must not send to 11000/9997,
  must not run `tools/ableton/osc-probe.mjs`, and must not call `mcp__kbot__ableton_*`.
- The kbot MCP server holds 11001 while it is up. Ad-hoc scripts (`osc-probe.mjs`) fail with a bind error while
  kbot is running: stop one or route through the other.
- A hung 11001 binder looks exactly like "AbletonOSC is down" (every request times out). Check `lsof -nP -iUDP:11001`
  before reinstalling anything.
- kbot's own TS client (`packages/kbot/src/integrations/ableton-osc.ts` `bindRecvSocket`) falls back to 11002, 11003, ...
  when 11001 is taken -- but AbletonOSC still replies to 11001, so from inside kbot a busy 11001 shows up as timeouts,
  never as a bind error. Same check: `lsof -nP -iUDP:11001`.

---

## 3. Install and hot-reload

Layout inside Live's user library (measured):

```
~/Music/Ableton/User Library/Remote Scripts/
  AbletonOSC/            upstream 0ca6821 + local edits
    manager.py           ControlSurface; init_api() builds self.handlers = [SongHandler, ...]
    abletonosc/          song.py track.py clip.py clip_slot.py device.py scene.py view.py application.py midimap.py
    abletonosc/kbot_ext.py   <- KbotHandler (spec 3.1); source of truth: packages/kbot/ableton/remote-script/kbot_ext.py
  KBotBridge/            tcp_server.py + kbot_control_surface.py (TCP 9997)
```

Install / update `kbot_ext.py` (Phase B of the plan; the installer does this, by hand it is):

1. Copy `packages/kbot/ableton/remote-script/kbot_ext.py` to `.../AbletonOSC/abletonosc/kbot_ext.py`.
2. `abletonosc/__init__.py`: add `from .kbot_ext import KbotHandler`.
3. `manager.py` `init_api()`: append `abletonosc.KbotHandler(self)` to the `self.handlers` list.
4. `manager.py` `reload_imports()`: add `importlib.reload(abletonosc.kbot_ext)` **before** `importlib.reload(abletonosc)`
   (the package reload re-exports the handler classes; reloading the module after it leaves the old class registered).
5. Hot-reload without touching Live's preferences: send `/live/api/reload` to UDP 11000. `reload_imports()` reloads
   the modules, then `clear_api()` (drops every OSC handler and listener) and `init_api()` (rebuilds them). Existing
   `start_listen` subscriptions die on reload — re-arm them.
6. Verify: `/live/test` → replies `("ok",)` and shows "Received OSC OK" in Live's status bar; then
   `/live/kbot/lom/get live_set tempo` must come back as `{"ok":true,...}`.

Only step 5 is needed after editing `kbot_ext.py` in place. `manager.py` itself is NOT reloaded by
`/live/api/reload`, so on the very first install (Live already running with the pre-patch Manager) the new
handlers-list entry is invisible and `/live/kbot/ping` stays silent (measured 2026-08-18). Instead of restarting
Live, `node tools/ableton/kbot-reload.mjs` bootstraps through the local `/live/exec` handler: it reloads the
`AbletonOSC.manager` module, swaps the running Manager instance's `__class__` to the fresh class and calls
`reload_imports()`; from then on plain `/live/api/reload` works. Scripted install: `packages/kbot/ableton/remote-script/install.sh`
then `node tools/ableton/kbot-reload.mjs`, then `node tools/ableton/e2e.mjs` (acceptance flow). Live-verified smoke
table: `docs/ableton/VERIFICATION-2026-08-18.md`.

Two transport facts measured the same day: (a) macOS caps a UDP datagram at the socket's SO_SNDBUF
(`net.inet.udp.maxdgram` = 9216) so replies over ~9.2 KB made AbletonOSC's `sendto` raise EMSGSIZE and the client
saw silence -- `KbotHandler.__init__` raises SO_SNDBUF to 65536 on the shared reply socket (`ping` reports `sndbuf`);
(b) `ableton.v2` `Component` keeps the Song in an instance attribute named `_song`, so a handler method of that
name is shadowed (`'Song' object is not callable`) -- kbot_ext uses `_get_song()`.

Logs: `.../AbletonOSC/logs/abletonosc.log` (level via `/live/api/set/log_level debug`). Errors are also relayed as
OSC `/live/error` messages.

---

## 4. Wire format for the kbot plane

Every `kbot_ext.py` handler replies with **one OSC string argument** that is JSON:

```
{"ok": true, ...read-back...}
{"ok": false, "error": "...", "trace": "<last 300 chars of the Python traceback>"}
```

Handlers never raise into AbletonOSC's server loop; a bug shows up as `ok:false`, not as silence. Silence (timeout)
means transport: wrong port, 11001 held by someone else, Live not running, or the handler is not registered.

Address groups (spec 3.1), all under `/live/kbot/`:

| group | addresses |
|---|---|
| generic LOM | `ping` · `list` · `lom/get <path> <prop>` · `lom/set <path> <prop> <json>` · `lom/call <path> <method> <json args>` · `lom/describe <path>` · `lom/children <path>` · `exec <code>` · `snapshot [depth]` · `snapshot_file <path>` |
| browser | `browser/search <query> [category] [limit]` · `browser/load <uri\|name> [target] [category]` (target `track:N` / `return:N` / `master` / `pad:N:note` / `chain:<path>` / `selected`, default `selected`) · `browser/preview <uri>` · `browser/stop_preview` · `device/presets <track> <device>` · `device/load_preset <track> <device> <index\|name>` |
| structure | `track/create midi\|audio\|return [index] [name]` · `track/delete <index\|return:N>` · `track/duplicate <index>` · `track/insert_device <track> <name> [position]` · `device/delete <track> <device>` · `device/move <track> <device> <final index> [target track\|chain path]` · `device/set_active <track> <device> <0\|1>` · `rack/insert_chain <path> [name]` · `rack/add_macro <path>` · `rack/macros <path> get\|set [json]` · `drum/build_pad <rack path> <note> <sample abs path> [name]` |
| clips | `clip/notes get\|set\|add\|remove <track> <slot> [json]` or `<clip path> [json]` (aliases `clip/notes/get\|set\|add\|remove` prepend the op; set = replace all) · `clip/quantize <track> <slot> <grid> <amount>` · `clip/automation <clip path> <param path> [[time,len,value]...]` (writes/creates; does not clear -- use `lom/call ... clear_envelope`) · `arrangement/create_clip <track> <start> <length>` · `arrangement/dup_from_session <track> <slot> <time>` · `arrangement/clips <track>` |
| song / app | `song/undo_group begin\|end` · `song/data get\|set <key> [json]` · `app/dialog info\|press [index]` · `app/message <text>` (status bar via `ControlSurface.show_message`; NOT `Application.show_message`, which is a modal box in 12.4.5) |

The kbot TS tools that speak them (action names as shipped in `packages/kbot/src/tools/ableton-lom.ts`;
`lom-coverage.md` uses the same names):

- `ableton_lom` -- `get` / `set` / `call` / `describe` / `children` / `exec` / `snapshot` / `snapshot_file` / `list` / `ping`
- `ableton_browser` -- `search` / `load` / `preview` / `stop_preview` / `presets` / `load_preset` / `insert_device`
  (`insert_device` speaks `track/insert_device`; `load` passes `target` through verbatim, so `chain:<path>` works)
- `ableton_structure` -- `create_track` / `delete_track` / `duplicate_track` / `delete_device` / `move_device` /
  `set_device_active` / `insert_chain` / `add_macro` / `macros` / `build_pad` / `clip_notes` (`op` = get|set|add|remove) /
  `quantize` / `automation` / `arr_create_clip` / `arr_dup_from_session` / `arr_clips` / `undo_begin` / `undo_end` /
  `data_get` / `data_set` / `dialog_press` / `message`

Where the raw handler accepts more than the TS action exposes (`track/delete return:N`, `clip/notes/get <clip path>`,
`device/delete <chain path> <idx>`), `lom-coverage.md` names the raw address.

Stock AbletonOSC addresses (`/live/song/*`, `/live/track/*`, `/live/clip/*`, ...) keep working unchanged and are
what the older `ableton_transport` / `ableton_track` / `ableton_clip` / `ableton_midi` / `ableton_device` /
`ableton_song` / `ableton_view` tools use. `lom-coverage.md` lists every one of them next to the LOM member it maps to.

---

## 5. Path grammar for `ableton_lom`

Paths are **Max LiveAPI style**: space-separated tokens, child-list name followed by a **0-based** index.
They are what `/live/kbot/lom/*` resolves inside Live (`song`, `app` are the roots).

| path | resolves to |
|---|---|
| `live_set` | the Song |
| `view` | `Song.View` (selected track/scene, detail clip) |
| `app` · `app view` · `app browser` · `app browser instruments` | Application, Application.View, Browser, a browser root |
| `tracks 0` · `return_tracks 1` · `master_track` | tracks by kind and index |
| `scenes 3` · `cue_points 0` · `groove_pool grooves 0` · `tuning_system` | Song children |
| `tracks 0 clip_slots 2` · `tracks 0 clip_slots 2 clip` | a slot; the clip in it (only if `has_clip`) |
| `tracks 0 arrangement_clips 0` · `tracks 0 take_lanes 0` | arrangement clips; take lanes |
| `tracks 0 devices 1` · `tracks 0 devices 1 parameters 4` | a device; one of its parameters |
| `tracks 0 devices 0 chains 1 devices 0` | a device inside a rack chain |
| `tracks 0 devices 0 drum_pads 36 chains 0` · `tracks 0 devices 0 drum_pad_note 36 chains 0` · `... chains 0 devices 0 sample` | a drum pad's chain (`drum_pads N` = list index, 128 pads in note order; `drum_pad_note N` = look the pad up by its `.note` -- the form used in the 2026-08-18 read-backs); Simpler's Sample |
| `tracks 0 mixer_device volume` · `master_track mixer_device crossfader` | mixer DeviceParameters |
| `app control_surfaces 0` | a ControlSurfaceProxy (AbletonOSC / KBotBridge appear here) |

Rules:

- 0-based everywhere. Live's UI shows track 1 for `tracks 0`.
- `describe <path>` returns members with kinds and current scalar values; `children <path>` returns the counts of
  every list property (`tracks`, `devices`, `clip_slots`, `chains`, `drum_pads`, `parameters`, ...). Use them before
  guessing an index.
- Enum-valued properties take and return ints (`Clip.WarpMode`, `Song.Quantization`, ...); the int enums and their
  names are listed in `lom-coverage.md`.
- `set` takes JSON: `true`, `120.0`, `"kbot Drums"`, `[60, 64, 67]`. `call` takes a JSON array of args.

Examples (arguments after the path are shown as the tool would send them):

```
ableton_lom get      live_set tempo                                  -> {"ok":true,"value":124.0}
ableton_lom set      tracks 0 name "Drums"                           -> {"ok":true,"value":"Drums"}
ableton_lom children tracks 0                                        -> {"ok":true,"children":{"devices":2,"clip_slots":8,"arrangement_clips":0,...}}
ableton_lom describe tracks 0 devices 1                              -> {"ok":true,"type":"Saturator","members":{...},"listeners":[...],"count":N,"canonical_path":"live_set tracks 0 devices 1"}
ableton_lom call     tracks 0 clip_slots 0 clip get_notes_extended [0,128,0,16]
ableton_lom get      tracks 0 devices 0 drum_pads 36 chains 0 devices 0 sample file_path
ableton_lom set      master_track mixer_device volume value 0.85     (parameter path + "value")
ableton_lom call     app view show_view ["Detail/Clip"]
```

---

## 6. The "always read back" rule

**A write is not done until Live says so.** Every mutating `kbot_ext.py` handler returns the state it changed;
every kbot tool reports *what Live returned*, not what it sent. This is the lesson from June (an optimistic
"clip created" while `list` showed nothing) and it is enforced in code, but the operator has to keep it too:

1. Send the write.
2. Read the same thing back through a *different* path than the write when you can (`notes/get` after
   `notes/add`; `arrangement/clips` after `arrangement/create_clip`; `children` after `track/create`).
3. Compare to intent. Only then say "done".

Worked example — a 1-bar hat pattern on track 0, slot 0:

```
# 1. make sure the slot is empty and the track is MIDI
ableton_lom get tracks 0 has_midi_input                 -> true
ableton_lom get tracks 0 clip_slots 0 has_clip          -> false

# 2. create the clip (stock OSC, 4 beats)
/live/clip_slot/create_clip 0 0 4.0

# 3. read back — the slot must now own a clip of length 4
ableton_lom get tracks 0 clip_slots 0 has_clip          -> true
ableton_lom get tracks 0 clip_slots 0 clip length       -> 4.0

# 4. write eight 16th-note hats (pitch 42, vel 90, 0.25 long)
ableton_structure clip_notes op=set track=0 slot=0 value='[{"pitch":42,"start":0.0,"duration":0.25,"velocity":90}, ... x8]'
   -> {"ok":true,"op":"set","added":8,"count":8,"notes":[...]}      (raw: /live/kbot/clip/notes set 0 0 <json>)

# 5. read back through the other path and diff
/live/clip/get/notes 0 0                                 -> 8 notes, pitch 42, starts 0.0,0.5,...3.5
```

If step 5 disagrees with step 4, the write failed even though the tool "returned"; report the disagreement,
do not report success. Wrap steps 2-4 in `undo_begin` / `undo_end` so one Cmd-Z reverts the lot.

---

## 7. `/live/exec` — the escape hatch

`/live/exec <code>` (local edit in `abletonosc/device.py`) runs arbitrary Python inside Live's interpreter with
`song`, `app`, `Live`, `tracks` in scope; expressions are `eval`'d and their value returned as a string, statements
are `exec`'d and `_result` is returned. `kbot_ext.py` re-exposes the same behaviour JSON-wrapped as
`/live/kbot/exec <code>` (kbot: `ableton_lom exec`). It is how the LOM dump was taken and how anything not yet typed
gets done today.

Caveats — read before using it:

- **Unauthenticated.** Anyone who can send a UDP packet to port 11000 can run Python inside Live as Isaac.
  AbletonOSC binds `0.0.0.0` (measured), so "localhost only" is a *policy*, not an enforced property: keep this Mac's
  11000 closed at the firewall / off untrusted networks, never port-forward it, never expose it through a tunnel.
- kbot does not expose it by default outside `ableton_lom exec`, whose output echoes the code it sent (so the transcript records it next to the result).
- Blocking or throwing code stalls AbletonOSC's tick (Live's embedded Python has no threads); an exception comes
  back as `"ERROR: ..."`. Long-running loops freeze Live's UI.
- No undo grouping unless the code opens one (`song.begin_undo_step()` / `end_undo_step()`).
- It is dev-only. Anything used twice should become a typed handler (next section).

---

## 8. How Fable expands coverage itself: describe → exec → promote

The generic plane means there is no LOM member Fable cannot reach; the loop for turning "reachable" into "typed":

1. **describe.** `ableton_lom describe <path>` (and `children`) to learn the exact member names, kinds and current
   values on the *running* Live — not from memory, not from the Max docs. `lom-coverage.md` says which members were
   only enumerated at class level (`~` / `?` kinds); those need a `describe` first.
2. **exec.** Do the operation once with `ableton_lom call` / `set` or, if it needs Python control flow,
   `ableton_lom exec`. Read it back (section 6). Note the exact args that worked and the read-back that proved it.
3. **promote.** Add a handler to `packages/kbot/ableton/remote-script/kbot_ext.py` (try/except, JSON read-back,
   undo group if it mutates), a fake-LOM unit test, a case in the TS tool, and a row in
   `tools/ableton/coverage-map.json` with `via:"tool"`. Regenerate `lom-coverage.md`. Reinstall + `/live/api/reload`
   (section 3), smoke it against Live, then it counts as covered.

Do not promote from memory of the Max LOM docs — promote from a `describe` on 12.4.5b5. Members differ between
versions (12.4 added `Track.create_midi_clip`, `Track.insert_device`, `Song.move_device`, `Clip.create_automation_envelope`,
`RackDevice.add_macro`, `Song.begin_undo_step`, `Song.get_data`, `Song.tuning_system` — all measured present).

---

## 9. What still needs the UI (Plane D)

Not in the 12.4.5b5 LOM at all — the coverage matrix marks these `ui` with the menu path:

| Task | Menu / gesture | LOM state you *can* read |
|---|---|---|
| Freeze / unfreeze a track | track header context menu > Freeze Track / Unfreeze Track | `Track.can_be_frozen`, `Track.is_frozen` |
| Flatten a frozen track | track header context menu > Flatten | `Track.is_frozen` |
| Export audio / stems | File > Export Audio/Video (Cmd-Shift-R) | — (Extensions SDK can render pre-FX audio offline; not the same thing) |
| Save / Save As / Open a Set | File > Save Live Set (Cmd-S) · Save Live Set As... · Open Live Set (Cmd-O) | `Song.file_path`, `Song.name` |
| New Set | File > New Live Set (Cmd-N) | — |
| Preferences (audio device, buffer, Remote Script slots) | Live > Settings... (Cmd-,) | `Application.control_surfaces` |
| Interact with a plugin GUI (VST/AU) | `/live/device/show_gui` opens the window (local edit); clicks inside it are UI | `PluginDevice.is_editor_open`, `PluginDevice.parameters` |
| Load a Max for Live device | only via the browser (`ableton_browser load` on an `.amxd` item) — no direct method | `Browser.max_for_live` |
| Consolidate, Crop to loop (arrangement), Slice to new MIDI track, Convert audio to MIDI | Edit / Create menus | `Clip.crop`, `Clip.duplicate_region` exist for clips; the arrangement-level commands do not |
| Collect All and Save, Manage Files | File > Collect All and Save · File > Manage Files | — |
| Dismiss a dialog | **LOM can do this one:** `dialog_press <index>` (`Application.press_current_dialog_button`), read `current_dialog_message` first | `Application.open_dialog_count` |

Plane D uses peekaboo / computer-use against the Live window; the rule of section 6 still applies (read the LOM back
after the gesture: `is_frozen` flips, `file_path` changes, `open_dialog_count` drops to 0).

---

## 10. Known-dead addresses (do not use)

| address | used by | why |
|---|---|---|
| `/live/kbot/create_midi_track`, `/live/kbot/create_audio_track`, `/live/kbot/load_sample_file`, `/live/kbot/load_plugin`, `/live/kbot/load_device`, `/live/kbot/lom_get`, `/live/kbot/lom_set` (March `kbot_bridge.py`) | still sent by `produce_beat` (`producer-engine.ts`: `create_midi_track`, `load_plugin`, `load_device`) and `design_sound` (`sound-designer.ts`: `load_plugin`); `ableton_create_track` / `ableton_load_sample` / `ableton_build_drum_rack` were re-routed 2026-08-18 | not installed in the loaded AbletonOSC (measured); replaced by `/live/kbot/track/create`, `/live/kbot/browser/load`, `/live/kbot/track/insert_device`, `/live/kbot/drum/build_pad`, `/live/kbot/lom/get|set` |
| `/live/master/get/output_meter_left|right` | formerly `ableton_audio_analysis` (fixed 2026-08-18: reads `master_track output_meter_left|right` through `/live/kbot/lom/get`) | no `/live/master/*` in AbletonOSC; use `ableton_lom get master_track output_meter_left` |
| `/live/device/set/enabled` | `ableton_device enable/disable` (still sends it) | not an AbletonOSC address; use `ableton_structure set_device_active` (sets `Device On` / LOM `Device.is_active`, read-back) |
| `/live/song/set/current_track` | `ableton_load_plugin` | not an AbletonOSC address; use `/live/view/set/selected_track` |
| TCP 9001 (AbletonBridge) | `ableton_load_effect`, `ableton_browse`, `ableton_load_preset`, `ableton_effect_chain` | process not running; route through `ableton_browser` |

---

## 11. Quick checklist before saying "Live did X"

- [ ] I was the only process on 11001 (`lsof -nP -iUDP:11001`).
- [ ] The reply was `{"ok":true,...}` (kbot plane) or a value (stock OSC), not a timeout.
- [ ] I read the change back through a second path and it matched.
- [ ] Multi-step edits were inside `undo_begin` / `undo_end`.
- [ ] Anything I did with `exec` twice is on the promote list (section 8).
