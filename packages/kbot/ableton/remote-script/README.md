# kbot_ext -- the whole Live Object Model over AbletonOSC

`kbot_ext.py` is one extra AbletonOSC handler (`KbotHandler`, class identifier
`kbot`) that runs inside Ableton Live's embedded Python. It gives an agent
generic read/write/call access to every LOM object plus typed convenience ops
for the things that are awkward to do one property at a time (browser loads,
drum pad building, note editing, arrangement, undo groups).

Design contract: `docs/superpowers/specs/2026-08-18-ableton-full-control-design.md`
(section 3.1). LOM ground truth: `docs/ableton/lom-dump-12.4.5b5.json`
(measured inside Live 12.4.5b5). Nothing in this module names a LOM member that
is not in that dump; version-dependent members (`Track.insert_device`,
`RackDevice.insert_chain`, `SimplerDevice.replace_sample`, ...) are guarded
with `hasattr` and reported in the reply.

## Files

| File | Purpose |
|---|---|
| `kbot_ext.py` | the handler (single file, hot-reloadable via `/live/api/reload`) |
| `kbot_ext_test.py` | offline unittest suite against a fake LOM (no Live needed) |
| `patch_abletonosc.py` | idempotent patcher: copies the module, wires `__init__.py` + `manager.py` |
| `install.sh` | runs the patcher against `~/Music/Ableton/User Library/Remote Scripts/AbletonOSC` and prints the reload commands |

## Reply contract

Every address replies with **exactly one OSC string argument** containing JSON,
sent back to the caller's host on UDP 11001 (AbletonOSC's reply port), on the
same address that was called:

```json
{"ok": true, ...}
{"ok": false, "error": "IndexError: index 99 out of range (len 3) at live_set tracks", "trace": "<last 300 chars>"}
```

Handlers never raise into AbletonOSC's server loop (`BaseException` is caught,
so `exec` code that raises `SystemExit` still answers `ok:false`). Replies
larger than the cap reported by `ping` as `max_reply_bytes` (60000 when the
send buffer could be raised, see below) are replaced by an `ok:false` "reply too
large" error (except `snapshot`, which shrinks itself and sets `"truncated":
true`); error text is clipped to 2000 chars so an oversize exception message
cannot displace the reply. Mutating handlers wrap their work in
`begin_undo_step`/`end_undo_step` and return a read-back of what Live now holds,
not what was sent.

User-supplied member names on the generic plane (`lom/get|set|call` props and
methods, and every attribute token in a path) must be public LOM names: a
leading underscore (`__class__`, `_song`, ...) or embedded whitespace is
rejected with `ValueError` before any `getattr`. `exec` is the only way to run
arbitrary Python and is documented as such.

macOS caps a UDP datagram at the sending socket's SO_SNDBUF
(`net.inet.udp.maxdgram` = 9216 bytes by default): AbletonOSC's `sendto` raised
`EMSGSIZE` for any reply above ~9.2 KB and the client saw only silence (measured
2026-08-18). `KbotHandler.__init__` raises SO_SNDBUF on the shared reply socket
to 65536 so full-size replies arrive; `ping` reports the effective `sndbuf` and
`max_reply_bytes`. If the buffer cannot be raised, the JSON cap follows the real
buffer (`SO_SNDBUF - 512`) instead of handing AbletonOSC a datagram it cannot send.

## Path grammar

Space separated, Max LiveAPI style. Tokens are attribute names; an integer token
indexes the previous list/vector; a bare path implies `live_set`.

```
live_set                       app
live_set tracks 0              live_set return_tracks 1        live_set master_track
live_set scenes 3              live_set cue_points 0           live_set groove_pool grooves 0
live_set view selected_track   live_set view selected_scene    live_set selected_track (shorthand)
live_set tracks 0 clip_slots 2 clip
live_set tracks 0 arrangement_clips 0        live_set tracks 0 take_lanes 0
live_set tracks 0 devices 1 parameters 4
live_set tracks 0 devices 0 chains 1 devices 0        ... return_chains 0
live_set tracks 0 devices 0 drum_pads 36              (index in the drum_pads list)
live_set tracks 0 devices 0 drum_pad_note 36          (the DrumPad whose .note == 36)
live_set tracks 0 mixer_device sends 0                live_set tracks 0 mixer_device volume
app browser instruments        app view
```

`<track>` arguments in typed handlers accept an int (index into `tracks`),
`return:N`, `master`, `selected`, or a full path.

## Addresses (all under `/live/kbot/`)

| Address | Args | Reply (inside `{ok:true,...}`) |
|---|---|---|
| `ping` | -- | `pong, kbot_ext, handlers, python, live, sndbuf, max_reply_bytes` |
| `list` | -- | `addresses[]`, `count` |
| `lom/get` | `<path> [prop]` | `value` (scalar / list / `{_lom,path,name}` stub); no prop = the object itself |
| `lom/set` | `<path> <prop> <json>` | `value` (read-back), `previous`; value coerced to the property's current type (bool/int/float/str); a path string sets object properties |
| `lom/call` | `<path> <method> [json args array]` | `result`; args may contain `{"_path": "..."}` for LOM objects |
| `lom/describe` | `<path>` | `members{name:{kind: property\|method\|listener, value}}`, `listeners[]`, `canonical_path` |
| `lom/children` | `<path>` | `children{prop: count}` for every list-like member |
| `exec` | `<python>` | `mode: eval\|exec`, `result` (`_result` for statements); scope: `song app Live tracks json kbot resolve` |
| `snapshot` | `[level]` | tempo/signature/is_playing/loop/tracks(devices, clip_slots)/returns/master/scenes/counts; `truncated`, `level` |
| `snapshot_file` | `<abs path>` | `path`, `bytes` (full detail incl. device parameter values) |
| `browser/search` | `<query> [category=all] [limit=25]` | `results[{name,uri,is_loadable,is_device,is_folder,category,path}]`, `budget_exhausted` |
| `browser/load` | `<uri-or-name> [target=selected] [category]` | `loaded, uri, method, steps[]`, plus `devices[]` (track/chain) or `pad{note,name,chains[]}` |
| `browser/preview` | `<uri-or-name> [category]` | `previewing, uri` |
| `browser/stop_preview` | -- | `stopped` |
| `device/presets` | `<track> <device>` | PluginDevice: `presets[], count, selected_preset_index`; else `presets:[], reason` |
| `device/load_preset` | `<track> <device> <index-or-name>` | PluginDevice: `selected_preset_index, preset`; native: browser load after the selected device, `devices[]` |
| `track/create` | `<midi\|audio\|return> [index=-1] [name]` | `index` (or `return:N`), `name`, `count` |
| `track/delete` | `<index\|return:N>` (0..n-1; negative indexes are rejected) | `deleted, name, tracks` |
| `track/duplicate` | `<index>` | `source, index, name, added` (`index` = source + tracks added, so a group copy is found after its children) |
| `track/insert_device` | `<track> <name> [position]` | `resolved, method (track.insert_device \| browser.load_item[+move_device]), devices[], added` (+ `warning` when `added` < 1: nothing inserted or a hot-swap -- read `devices`) |
| `device/delete` | `<track> <device>` | `deleted, name, devices[]` |
| `device/move` | `<track> <device> <final index> [target]` | `moved, requested, position (read back), live_position_arg, devices[]`; `Song.move_device`'s position is an insertion slot counted before removal, the handler compensates so you pass the desired FINAL index; Live refuses moves that break MIDI fx -> instrument -> audio fx order |
| `device/set_active` | `<track> <device> <0\|1>` | `is_active, method` (`parameters[0]` "Device On", else `is_active`) |
| `rack/insert_chain` | `<rack path> [name] [note]` | `chain_index, name, chains[], steps[]` |
| `rack/add_macro` | `<rack path>` | `visible_macro_count` |
| `rack/macros` | `<rack path> get\|set [json array or object]` | `macros[{macro,param_index,name,value,min,max,visible}]` |
| `drum/build_pad` | `<rack path \| track path> <note> <sample abs path> [name]` (a track path finds the Drum Rack wherever it sits in the chain) | `pad, chain{in_note,out_note,devices}, sample_file_path, steps[], errors[]`; `ok:false` + `error` if a step failed |
| `clip/notes` | `get\|set\|add\|remove <track> <slot> [json]` (or a clip path instead of track+slot) | `notes[{pitch,start,duration,velocity,mute,probability,velocity_deviation,release_velocity,note_id}]`, `count` |
| `clip/notes/get` `clip/notes/set` `clip/notes/add` `clip/notes/remove` | same without the op arg | same |
| `clip/quantize` | `<track> <slot> <grid enum int\|name> <amount>` | `grid, amount, count`; names `no_grid g_8_bars g_4_bars g_2_bars g_bar g_half g_quarter g_eighth g_sixteenth g_thirtysecond` (also `quarter`, `q_quarter`, any case) |
| `clip/automation` | `<clip path> <parameter path> <json [[time,length,value],...]>` | `created_envelope, written, readback[[mid_time,value]]`; values are in the parameter's OWN units (`min..max`, e.g. Operator Transpose -48..48, integer params round); read-back samples the middle of each step because Live returns the pre-step value at a step's exact start |
| `arrangement/create_clip` | `<track> <start> <length>` | `result`, `arrangement_clips[]` |
| `arrangement/dup_from_session` | `<track> <slot> <time>` | `result`, `arrangement_clips[]` |
| `arrangement/clips` | `<track>` | `clips[{index,name,start_time,end_time,length,midi}]` |
| `song/undo_group` | `begin\|end` | `op, can_undo` |
| `song/data` | `get\|set <key> [json]` | `key, value` (`Song.get_data/set_data`) |
| `app/dialog` | `press <index>` (or `info`) | `open_dialog_count, message, button_count, pressed` |
| `app/message` | `<text>` | `shown, method` -- status bar via `ControlSurface.show_message`; NOT `Application.show_message`, which in Live 12.4.5 is a modal message box |

Browser categories: `all`, `devices`, `instruments`, `audio_effects`,
`midi_effects`, `drums`, `sounds`, `samples`, `max_for_live`, `plugins`,
`user_library`, `packs`, `clips`, `current_project`, `user_folders`, or a
comma-separated list. Name matching prefers an exact (case-insensitive) match
over a substring match, and devices over presets. `browser/load` targets:
`selected`, `track:N`, `return:N`, `master`, `pad:N:NOTE`, `chain:<lom path>`.

Name matching treats `Snare` == `Snare.wav` / `.adv` / `.adg` / `.aif` / `.flac`
as an exact hit. `browser/load` onto an empty pad tries `chain.insert_device(name)`
for device items and falls back to select-chain + `load_item` when Live rejects
the name (Live 12 Drum Sampler presets such as `DS Snare` report `is_device` but
are not insertable by name).

`set` for notes replaces all notes; note objects may also be given as
`[pitch,start,duration,velocity,mute]` arrays. Note reads use
`Clip.get_all_notes_extended`, writes use `Clip.add_new_notes` with
`Live.Clip.MidiNoteSpecification`, removals use `Clip.remove_notes_extended`.

## Install and reload

```sh
cd packages/kbot/ableton/remote-script
./install.sh                # or: python3 patch_abletonosc.py [--dir ...] [--check|--dry-run]
```

The patcher is idempotent. It copies `kbot_ext.py` into
`AbletonOSC/abletonosc/`, appends `from .kbot_ext import KbotHandler` to
`abletonosc/__init__.py`, adds `abletonosc.KbotHandler(self),` to the
`self.handlers = [...]` list in `manager.py`, and makes `reload_imports()`
reload `abletonosc.kbot_ext` before the package so edits are picked up by
`/live/api/reload`. Originals are kept as `*.kbot-orig`; edited files are
byte-compiled and restored on a syntax error.

Then hot-reload (Live keeps running):

```sh
node tools/ableton/kbot-reload.mjs             # /live/api/reload, ping; bootstraps on a first install
node tools/ableton/osc-probe.mjs '[["/live/kbot/list"]]'
node tools/ableton/e2e.mjs                     # acceptance flow, PASS/FAIL per step
```

**First install while Live is already running:** `/live/api/reload` re-imports
the `abletonosc.*` submodules but not `AbletonOSC/manager.py`, so the freshly
patched handlers list is not seen and `ping` stays silent (measured 2026-08-18).
`kbot-reload.mjs` notices and bootstraps through the pre-existing local
`/live/exec` handler: it reloads the `AbletonOSC.manager` module, swaps the
running Manager instance's `__class__` to the new class and calls
`reload_imports()`. After that plain `/live/api/reload` picks up every later
edit. Without `/live/exec` the alternative is toggling the control surface in
Preferences or restarting Live.

If `ping` still stays silent, read `AbletonOSC/logs/abletonosc.log` -- an import
traceback there means the module failed to load; fix and re-run `install.sh`.

## The 11001 single-binder rule

AbletonOSC listens on UDP 11000 and sends every reply to the caller's host on
UDP **11001**. Only ONE process can bind 11001 at a time. If kbot's MCP server,
`osc-probe.mjs`, or any other client already holds it, a second client will
either fail to bind or silently never see replies. Serialize all Live probing:
stop the other client first, run your commands, then release the port.

## Tests

```sh
cd packages/kbot
python3 -m unittest ableton/remote-script/kbot_ext_test.py -v
```

The suite stubs `ableton.v2.control_surface.component`, the AbletonOSC
`.handler`/`.osc_server` siblings and a minimal `Live` module, then drives the
handler through the same `callback(params) -> (json_string,)` contract the OSC
server uses. Passes on Python 3.9, 3.11 (Live 12's embedded version) and 3.14.

Live-verified smoke table + acceptance run: `docs/ableton/VERIFICATION-2026-08-18.md`.

## Examples

```sh
node tools/ableton/osc-probe.mjs '[["/live/kbot/lom/get","live_set","tempo"]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/lom/set","live_set tracks 0","name","Bass"]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/lom/describe","live_set tracks 0 devices 0"]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/browser/search","operator","instruments",5]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/track/insert_device",0,"Saturator"]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/clip/notes","set",0,0,"[{\"pitch\":36,\"start\":0,\"duration\":0.25,\"velocity\":110}]"]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/drum/build_pad","live_set tracks 1 devices 0",36,"/abs/path/kick.wav","Kick"]]'
node tools/ableton/osc-probe.mjs '[["/live/kbot/snapshot_file","/tmp/set.json"]]'
```
