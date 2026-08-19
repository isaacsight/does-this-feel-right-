# kbot_ext / Ableton full control -- Live verification, 2026-08-18

Phase B of `docs/superpowers/specs/2026-08-18-ableton-full-control-design.md`:
install `kbot_ext.py` into the loaded AbletonOSC, hot-reload, smoke every
`/live/kbot/*` address against the running Live, run the acceptance script,
drive the TS tools through kbot's registry, and record what Live actually
answered. Honesty rule: PASS only where a read-back line from Live is quoted;
raw replies for the smoke-table probes are in
`docs/ableton/verification-2026-08-18-smoke-log.jsonl` (209 rows, includes the
failing runs before each fix). Not in that file: `ping` / `list` (replies quoted
verbatim in sections 1 and 5), the e2e-only probes (`fire` / `stop_playing`,
section 4 output) and the TS-registry pass (section 5). Audited 2026-08-18
against the log, `kbot_ext.py` and `ableton-lom.ts`: two alias addresses were
never sent to Live (rows 59-60, marked below); everything else in the table has
a matching log row or quoted output.

| Fact | Value |
|---|---|
| Live | `Application.get_version_string()` = `12.4.5b8` at first ping, `12.4.5b9`, `12.4.5b10` later the same session (the suffix increments per reload; task called it 12.4.5b5); Python 3.11.6 |
| AbletonOSC | `~/Music/Ableton/User Library/Remote Scripts/AbletonOSC` at `0ca6821` + local edits (`/live/exec`, ...) |
| Set at start | 4 tracks (1-MIDI, 2-MIDI, 3-Audio, 4-Audio), returns A-Reverb / B-Delay, 8 scenes; no clips (the earlier 4-beat clip in track 0 slot 0 was gone -- Live had been restarted at 20:05, `abletonosc.log`) |
| Set at end | identical: 4 tracks, 2 returns, 8 scenes (`lom/children live_set` -> `{"return_tracks":2,"scenes":8,"tracks":4}`) |
| 11001 rule | `lsof -nP -iUDP:11001` empty before, between and after every probe batch; every probe was a short-lived binder |
| Live traffic sent by | `tools/ableton/osc-probe.mjs`, `tools/ableton/kbot-reload.mjs`, `tools/ableton/e2e.mjs`, a scratch `k.mjs` driver on `tools/ableton/osc-lib.mjs`, and `npx tsx` scripts using the real kbot `AbletonOSC` client (bound 11001) |

## 1. Install + reload

`git status --short` in `.../AbletonOSC` **before** `install.sh`:

```
 M abletonosc/device.py
 M abletonosc/song.py
?? logs/
```

`packages/kbot/ableton/remote-script/install.sh` output (first run):

```
copied   .../packages/kbot/ableton/remote-script/kbot_ext.py -> .../AbletonOSC/abletonosc/kbot_ext.py
backup   __init__.py -> __init__.py.kbot-orig
patched  __init__.py: appended 'from .kbot_ext import KbotHandler'
patched  manager.py: added 'abletonosc.KbotHandler(self),' to handlers list
patched  manager.py: reload_imports() now reloads abletonosc.kbot_ext
backup   manager.py -> manager.py.kbot-orig
ok       manager.py, abletonosc/__init__.py, abletonosc/kbot_ext.py compile
```

`git status --short` **after** (final state, identical after every re-install; `install.sh --check` exits 0):

```
 M abletonosc/__init__.py          (+1 line: from .kbot_ext import KbotHandler)
 M abletonosc/device.py            (pre-existing local edit, untouched)
 M abletonosc/song.py              (pre-existing local edit, untouched)
 M manager.py                      (+3 lines: KbotHandler(self) in handlers; reload hook)
?? abletonosc/__init__.py.kbot-orig
?? abletonosc/kbot_ext.py
?? logs/
?? manager.py.kbot-orig
```

`git diff --stat`: `__init__.py | 1 +`, `manager.py | 3 ++`, plus the pre-existing 230 lines in device.py/song.py.

### Reload -- first attempt FAILED, root cause, fix

`/live/api/reload` then `/live/kbot/ping`:

```
-> /live/api/reload []            <- /live/startup []
-> /live/kbot/ping []             <- /live/error ["Unknown OSC address: /live/kbot/ping"]
```

`abletonosc.log`: `Reloading abletonosc... Reloaded code ... [ERROR] Unknown OSC address: /live/kbot/ping`.
No import traceback: `kbot_ext.py` was fine. Cause: `Manager.reload_imports()` reloads the `abletonosc.*`
submodules but **not `AbletonOSC/manager.py`**; the running instance still executes the pre-patch `init_api()`
whose handlers list has no `KbotHandler`. Only a Live restart (or a Control Surface toggle) would pick it up.

Fix without restarting Live -- `tools/ableton/kbot-reload.mjs --bootstrap` (new): through the pre-existing local
`/live/exec` handler it runs
`mgr = [c for c in app.control_surfaces if type(c).__name__=="Manager"][0]; mod = importlib.reload(sys.modules["AbletonOSC.manager"]); mgr.__class__ = mod.Manager; mgr.reload_imports()`:

```
<- /live/exec ["bootstrapped: handlers=10 kbot=True"]
-> /live/kbot/ping []  <- {"pong":true,"kbot_ext":"0.1.0","handlers":41,"python":"3.11.6","live":"12.4.5b8","ok":true}
-> /live/kbot/list []  <- {"addresses":["/live/kbot/app/dialog", ... 41 total], "count":41, "ok":true}
```

Afterwards plain `/live/api/reload` keeps the handlers (verified: reload -> ping ok, repeated after every one of the
seven re-installs below). `kbot-reload.mjs` (no flag) does reload -> ping and only bootstraps when ping is silent.

## 2. Smoke table -- every address in `/live/kbot/list` (41)

Scratch tracks used: `kbot-e2e` (index 4, MIDI) and `kbot-e2e-drums` (index 5, MIDI); both deleted at the end
(`track/delete 5` -> `{"deleted":5,"name":"kbot-e2e-drums","tracks":5}`, `track/delete 4` -> `{"deleted":4,"name":"kbot-e2e","tracks":4}`,
then `lom/get live_set tracks` -> the four user tracks). Returns/master: reads only, plus one create+delete of a
temporary `C-Return` (returns back to `["A-Reverb","B-Delay"]`, read back). Replies below are trimmed; `ok:true`
elided where the excerpt makes it obvious.

| # | Address | Args sent | Reply (trimmed) | Result | Read-back proof |
|---|---|---|---|---|---|
| 1 | `ping` | -- | `{"pong":true,"kbot_ext":"0.1.1","handlers":41,"python":"3.11.6","sndbuf":65536,"max_reply_bytes":60000,"live":"12.4.5b10"}` | PASS | reply is the read-back |
| 2 | `list` | -- | `{"addresses":[41 items],"count":41}` | PASS | count matches registered handlers |
| 3 | `lom/get` | `live_set tempo` | **first: FAIL** `TypeError: 'Song' object is not callable` (bug A) -> after fix `{"path":"live_set","prop":"tempo","value":120}` | PASS | value 120 |
| 4 | `lom/get` | `live_set tracks 0 name` | `{"value":"1-MIDI"}` | PASS | |
| 5 | `lom/get` | `master_track mixer_device volume value` | `{"value":0.85}` | PASS | |
| 6 | `lom/get` | `live_set tracks 0` (no prop) | `{"type":"Track","value":{"_lom":"Track","path":"live_set tracks 0","name":"1-MIDI"}}` | PASS | |
| 7 | `lom/get` | `live_set tracks` | list of 4 `{"_lom":"Track","path":"live_set tracks N","name":...}` | PASS | |
| 8 | `lom/get` | `view selected_track name` / `live_set selected_track name` (shorthand) | `{"value":"1-MIDI"}` both | PASS | |
| 9 | `lom/get` | `live_set tracks 0 clip_slots 0 clip name` (empty slot) | first: `AttributeError: 'NoneType' has no member 'name'`; after fix `LookupError: path '...' resolves to None (empty clip slot / unset property)` | PASS (correct error) | |
| 10 | `lom/set` | `live_set tracks 4 name kbot-e2e-renamed` | `{"value":"kbot-e2e-renamed","previous":"kbot-e2e"}` | PASS | `lom/get ... name` -> `kbot-e2e-renamed`; set back -> `{"value":"kbot-e2e","previous":"kbot-e2e-renamed"}` |
| 11 | `lom/set` | `live_set tracks 4 mute "true"` / `0`; `color_index 12` | `{"value":true,"previous":false}`, `{"value":false,"previous":true}`, `{"value":12,"previous":3}` | PASS | `lom/get mute` -> true; `lom/get color_index` -> 12 |
| 12 | `lom/set` | `live_set view selected_track "live_set tracks 5"` (object property from path) | `{"value":{"_lom":"Track","name":"kbot-e2e-drums"}}` | PASS | `lom/get live_set view selected_track name` -> `kbot-e2e-drums` |
| 13 | `lom/set` | `live_set tracks 4 mixer_device panning value 0.5` | `{"value":0.5,"previous":0}` | PASS | `lom/get` -> 0.5 |
| 14 | `lom/call` | `live_set tracks 4 clip_slots 0 create_clip [4.0]` | `{"result":{"_lom":"Clip","path":"live_set tracks 4 clip_slots 0 clip"}}` | PASS | `lom/get clip_slots 0 has_clip` -> true; `clip length` -> 4 |
| 15 | `lom/call` | `... clip automation_envelope [{"_path":"... devices 0 parameters 1"}]` | `{"args":[{"_lom":"DeviceParameter","name":"Algorithm"}],"result":{"_lom":"Envelope"}}` | PASS | `_path` arg resolved to a LOM object |
| 16 | `lom/call` | `... clip clear_envelope [{"_path":...}]`; `... clip set_fire_button_state [false]`; `live_set get_data ["kbot_test",null]` | `result:null`; `result:null`; `result:{"x":1}` | PASS | |
| 17 | `lom/call` | `live_set tracks 4 clip_slots 0 fire []` (e2e) ; `live_set stop_playing []` | -- | PASS | clip `is_playing` true within 3 s; song `is_playing` true -> false after stop |
| 18 | `lom/describe` | `tracks 0` | `{"type":"Track","members":{...},"listeners":[...],"count":...,"canonical_path":"live_set tracks 0"}` 7627 bytes | PASS | |
| 19 | `lom/describe` | `master_track mixer_device volume` | `{"type":"DeviceParameter","members":{"name":{"value":"Track Volume"},"value":{"value":0.85},"min":0,"max":1,"is_quantized":false,...},"count":23,"canonical_path":"live_set master_track mixer_device volume"}` | PASS | |
| 20 | `lom/describe` | `app browser` | `{"type":"Browser","members":{"audio_effects":{"value":{"_lom":"BrowserItem","name":"Audio Effects"}},"load_item":{"kind":"method"},"hotswap_target":{"value":null},...}}` | PASS | |
| 21 | `lom/describe` | `tracks 4 clip_slots 0 clip`; `live_set tracks 0 clip_slots 0`; `live_set` | Clip (6613 bytes); ClipSlot (`"clip":{"value":null},"has_clip":false`, 1518 bytes); Song (>9216 bytes -- arrived only after bug B fix) | PASS | |
| 22 | `lom/children` | `live_set` | `{"children":{"cue_points":0,"return_tracks":2,"scale_intervals":7,"scenes":8,"tracks":4,"visible_tracks":4}}` | PASS | |
| 23 | `lom/children` | `tracks 4` | `{"arrangement_clips":2,"clip_slots":8,"devices":3,"take_lanes":0,"available_input_routing_types":7,...}` | PASS | |
| 24 | `exec` | eval `[(i,p.name,p.is_quantized) ...]`; exec statement with `_result` | `{"mode":"eval","result":[[0,"Device On",true],[1,"Algorithm",true],[2,"Transpose",false],...]}`; `{"mode":"exec","result":[0.85,0.3,0.85,0.85,0.9,0.85]}` | PASS | |
| 25 | `exec` | `"x"*12000` | **first: FAIL** silence, `abletonosc.log`: `OSError: [Errno 40] Message too long` (bug B) -> after fix 12000-char string arrives; `"x"*59900` arrives; `"x"*60000` -> `{"ok":false,"error":"reply too large (60037 bytes > 60000)...","bytes":60037}` | PASS | cap semantics proven both sides |
| 26 | `snapshot` | -- / `1` | `{"tempo":120,"signature":[4,4],"counts":{"tracks":6,"returns":2,"scenes":8},"tracks":[...],"truncated":false,"level":0}` 3538 bytes; level 1: 2368 bytes, empty slots dropped | PASS | size < 60000; `truncated:false` on this Set (the shrink ladder + `truncated:true` is unit-tested with 303 fake tracks; not reachable on a 6-track Set) |
| 27 | `snapshot_file` | `/tmp/kbot-snapshot.json` | `{"path":"/tmp/kbot-snapshot.json","bytes":25681}` | PASS | file exists, 25681 bytes, `tracks` names = the six tracks then present, `device_params` sets = 3 for track 4 |
| 28 | `browser/search` | `Operator instruments 5` | `{"count":4,"results":[{"name":"Operator","uri":"query:Synths#Operator","is_loadable":true,"is_device":true,"path":"Instruments/Operator"},{"name":"Operator Hihat.adv",...},...]}` | PASS | |
| 29 | `browser/search` | `Saturator audio_effects 5`; `EQ Eight devices 5`; `Drum Rack instruments 5`; `Simpler instruments 5`; `AUDelay plugins 5`; `Snare samples,user_library 6` | one exact hit each (`query:AudioFx#Saturator`, `query:AudioFx#EQ%20Eight`, `query:Synths#Drum%20Rack`, `query:Synths#Simpler`, `query:Plugins#AUv2:Apple:AUDelay`); samples list `505 Snare.flac`, ... | PASS | |
| 30 | `browser/load` | `Saturator track:4` | `{"loaded":"Saturator","uri":"query:AudioFx#Saturator","method":"load_item","devices":["Operator","EQ Eight","Saturator"],"steps":["select track","browser.load_item"]}` | PASS | `lom/get tracks 4 devices` -> 3 devices, last `Saturator` |
| 31 | `browser/load` | `Utility selected audio_effects` | `{"target":"selected","track":4,"devices":["Operator Hihat","EQ Eight","Saturator","Utility"]}` | PASS | then `device/delete 4 3` -> Utility gone |
| 32 | `browser/load` | `Compressor chain:live_set tracks 5 devices 0 chains 0` | `{"method":"chain.insert_device","devices":["Kick_808","Compressor"]}` | PASS | `lom/get ... chains 0 devices` -> `[SimplerDevice Kick_808, CompressorDevice Compressor]` |
| 33 | `browser/load` | `Snare.wav pad:5:38 user_library` (pad with existing chain) | `{"method":"selected_drum_pad+load_item","pad":{"note":38,"name":"Snare","chains":[{"name":"Snare","devices":["Snare"]}]}}` | PASS | `lom/get drum_pad_note 38 chains 0 devices` -> `SimplerDevice "Snare"` |
| 34 | `browser/load` | `Simpler pad:5:40` (empty pad, device item) | `{"method":"insert_chain+chain.insert_device","pad":{"note":40,"chains":[{"name":"Simpler","devices":["Simpler"]}]}}` | PASS | `lom/get drum_pad_note 40 chains 0 devices` -> SimplerDevice |
| 35 | `browser/load` | `Snare pad:4:38 user_library,user_folders,samples` (empty pad, bare term) | **first (via ableton_load_sample, category all): FAIL** `ValueError: Device DS Snare not found.` and a stray empty chain (bug C) -> after fix `{"loaded":"Snare.wav","uri":"query:UserLibrary#Samples:kbot-trap-kit:Snare.wav","method":"selected_drum_pad+load_item"}` | PASS | `lom/get ... drum_pad_note 38 chains 0 devices 0 sample file_path` -> `.../kbot-trap-kit/Snare.wav` |
| 36 | `browser/load` | `DS Snare pad:4:40` (Live 12 Drum Sampler preset, `is_device:true`) | `{"method":"insert_chain+select_chain+load_item","steps":[...,"chain.insert_device failed: Device DS Snare not found.","select chain","focus Detail/DeviceChain","browser.load_item"],"pad":{"note":40,"name":"DS Snare","chains":[{"devices":["DS Snare"]}]}}` | PASS | `lom/get drum_pad_note 40 chains 0 devices` -> `MaxDevice "DS Snare"` |
| 37 | `browser/load` | `query:Plugins#AUv2:Apple:AUDelay track:4 plugins` (URI) | `{"loaded":"AUDelay","devices":[...,"AUDelay"]}` | PASS | `lom/get tracks 4 devices` -> `PluginDevice AUDelay` at index 3 |
| 38 | `browser/preview` | `Operator Hihat.adv instruments` | `{"previewing":"Operator Hihat.adv","uri":"query:Synths#Operator:Percussive:FileId_27286"}` | PASS | no LOM read-back exists for preview state; reply is Live's item |
| 39 | `browser/stop_preview` | -- | `{"stopped":true}` | PASS | (same caveat) |
| 40 | `device/presets` | `4 0` (Operator) | `{"device":"Operator","class":"Operator","presets":[],"reason":"not a PluginDevice (class Operator); native presets are browser items - use browser/search"}` | PASS (graceful reason) | |
| 41 | `device/presets` | `4 3` (AUDelay) | `{"class":"AuPluginDevice","presets":["Default"],"count":1,"selected_preset_index":0}` | PASS | `lom/get tracks 4 devices 3 class_name` -> `AuPluginDevice` |
| 42 | `device/load_preset` | `4 3 0` (PluginDevice) | `{"method":"selected_preset_index","selected_preset_index":0,"preset":"Default"}` | PASS | selected_preset_index read back (only one preset exists on AUDelay) |
| 43 | `device/load_preset` | `4 0 "Operator Hihat.adv"` (native) | `{"method":"browser.load_item after selected device","loaded":"Operator Hihat.adv","devices":["Operator Hihat","EQ Eight","Saturator"]}` | PASS | `lom/get tracks 4 devices` -> device 0 now named `Operator Hihat` (hot-swapped) |
| 44 | `track/create` | `midi -1 kbot-e2e` | `{"kind":"midi","index":4,"name":"kbot-e2e","count":5}` | PASS | `lom/get live_set tracks` lists it at 4 |
| 45 | `track/create` | `audio -1 kbot-e2e-audio`; `return` | `{"index":6,"name":"kbot-e2e-audio","count":7}`; `{"index":"return:2","name":"C-Return","count":3}` | PASS | `has_midi_input` -> false; `lom/get return_tracks` -> A,B,C-Return |
| 46 | `track/delete` | `6`; `return:2`; `5`; `4` | `{"deleted":6,"tracks":6}`; `{"deleted":"return:2","name":"C-Return","returns":2}`; ... | PASS | `lom/get tracks` / `return_tracks` back to the user's 4 + 2 |
| 47 | `track/duplicate` | `4` | `{"source":4,"index":5,"name":"kbot-e2e","tracks":6}` | PASS | `lom/get tracks` shows two `kbot-e2e`; `track/delete 5` -> 5 tracks |
| 48 | `track/insert_device` | `4 Operator`; `4 Saturator`; `4 "EQ Eight"`; `5 "Drum Rack"`; `4 "EQ Eight" 1` (position) | `{"resolved":"Operator","method":"track.insert_device","devices":["Operator"],"added":1,"errors":[]}`; ... `["Operator","Saturator","EQ Eight"]`; `["Drum Rack"]`; position 1 -> `["Operator","EQ Eight","EQ Eight"]` | PASS | `lom/get tracks 4 devices` matches each time (`Eq8Device` for EQ Eight, `RackDevice` for Drum Rack) |
| 49 | `device/delete` | `4 2` (Saturator) etc. | `{"deleted":2,"name":"Saturator","devices":["Operator","EQ Eight"]}` | PASS | `lom/get tracks 4 devices` -> 2 devices |
| 50 | `device/move` | `4 2 0` (EQ Eight to 0 -- before instrument) | `{"moved":"EQ Eight","position":0,"devices":["Operator","EQ Eight","Saturator"]}` -- Live placed it after Operator | PASS (Live semantics) | |
| 51 | `device/move` | `4 0 2` (Operator after audio fx) | `RuntimeError: Couldn't move device. (Live refuses moves that break chain order: MIDI effects -> instrument -> audio effects; device 'Operator' to position 2 in [...])` | PASS (correct refusal, hint added) | |
| 52 | `device/move` | `4 1 2` (Saturator later) | **first: FAIL** result 2 but read-back left it at index 1 (bug D: `move_device` position is an insertion slot counted before removal) -> after fix `{"requested":2,"position":2,"live_position_arg":3,"devices":["Operator","EQ Eight","Saturator"]}`; `4 2 1` -> `{"position":1,"live_position_arg":1,"devices":["Operator","Saturator","EQ Eight"]}` | PASS | `position` is found by identity in `track.devices` after the move |
| 53 | `device/set_active` | `4 1 0` / `4 1 1` | `{"device":"Saturator","is_active":false,"method":"parameters[0]"}` / `is_active:true` | PASS | `lom/get tracks 4 devices 1 is_active` -> false, then true |
| 54 | `rack/insert_chain` | `live_set tracks 5 devices 0 Snare 38` | `{"chain_index":1,"name":"Snare","chains":["Kick","Snare"],"steps":["rack.insert_chain()","in_note=38","out_note=38"]}` | PASS | `lom/get ... devices 0 chains` -> `[DrumChain Kick, DrumChain Snare]` |
| 55 | `rack/add_macro` | `live_set tracks 5 devices 0` | `{"visible_macro_count":10}` (was 8; Live adds macros in pairs) | PASS | `rack/macros get` -> `visible_macro_count:10`, macros 8 and 9 `visible:true` |
| 56 | `rack/macros` | `... get`; `... set [0.25,0.75]` | `{"visible_macro_count":8,"macros":[{"macro":0,"param_index":1,"name":"Macro 1","value":0,"min":0,"max":127,"visible":true},...16]}`; after set macros 0/1 `value:0.25` / `0.75` | PASS | second `get` -> 0.25 / 0.75 |
| 57 | `drum/build_pad` | `live_set tracks 5 devices 0 36 /Users/.../User Library/Samples/kbot-trap-kit/Kick_808.wav Kick` | `{"pad":{"note":36,"name":"Kick","chains":[{"name":"Kick","devices":["Kick_808"]}]},"sample_file_path":".../Kick_808.wav","chain":{"in_note":36,"out_note":36,"devices":["Kick_808"]},"steps":["rack.insert_chain()","in_note=36","out_note=36","chain.name","chain.insert_device('Simpler')","simpler.replace_sample"],"errors":[]}` | PASS | `lom/get ... drum_pad_note 36 name` -> `Kick`; `... chains 0 devices 0 sample file_path` -> the WAV path; `... chains 0 in_note` -> 36 |
| 58 | `clip/notes` | `set 4 0 [{60,0,0.5,100},{64,1,0.5,90,"probability":0.5},[67,2,0.25,80,false]]` | `{"op":"set","added":3,"count":3,"notes":[{"pitch":60,"start":0,"duration":0.5,"velocity":100,"mute":false,"probability":1,...,"note_id":1},{"pitch":64,...,"probability":0.5,...},{"pitch":67,...}]}` | PASS | `clip/notes get 4 0` -> the same 3 notes incl. `probability:0.5` |
| 59 | `clip/notes/add` / `clip/notes/get` (path form) / `clip/notes remove` (op form) / `clip/notes/get` | `4 0 [{"pitch":72,"start":3,"duration":1}]`; `"live_set tracks 4 clip_slots 0 clip"`; `4 0 {"pitch":72,"pitch_span":1}`; `4 0` | `count:4` with note 72; get (path) -> 4 notes; `{"removed_range":[72,1,-8192,16384],"count":3}`; get -> 3 notes, no 72 | PASS (`clip/notes/add`, `clip/notes/get`); the `clip/notes/remove` alias itself was NOT sent -- only the op form `clip/notes remove` was | each op followed by a get; alias registration is proven by `list` (41) and unit-tested against the fake |
| 60 | `clip/notes/set` alias | **not sent to Live** -- e2e and the log use the op form `clip/notes set ...` (row 58, e2e step 6: `count:4`, get returns `[36,0,1,110],[43,4,1,100],[48,8,2,96],[55,12,4,90]`) | -- | NOT DIRECTLY EXERCISED (op form PASS) | the alias is a one-line lambda prepending `"set"` (`kbot_ext.py` `init_api`); registered (in `list`), not probed |
| 61 | `clip/quantize` | `4 0 q_quarter 1.0` | **first: FAIL** `ValueError: unknown grid 'q_quarter'` (bug E) -> after fix `{"grid":6,"amount":1,"count":3}`; `4 0 4 0.5` -> `grid:4`; `g_sixteenth 0.5` -> `grid:8` | PASS | note count read back after each; enum ints from `Live.Clip.GridQuantization.values` (`g_bar=4, g_half=5, g_quarter=6, g_eighth=7, g_sixteenth=8`) |
| 62 | `clip/automation` | `... clip` `... devices 0 parameters 2` (Transpose, -48..48) `[[0,1,12],[2,1,-7]]` | **first (values 0.2/0.8, read at step start): FAIL** read-back `[[0,0],[2,0]]` (bug F: read at step start returns the pre-step value; and 0.2 semitones rounds to 0) -> after fix `{"parameter":"Transpose","created_envelope":true,"written":2,"readback":[[0.5,12],[2.5,-7]]}` | PASS | `lom/get clip has_envelopes` -> true; `exec value_at_time(0.5/2.5)` -> 12 / -7 |
| 63 | `clip/automation` | `... clip` `tracks 4 mixer_device volume` `[[0,1,0.3],[2,1,0.9]]`; `... devices 0 parameters 4` (Volume 0..1) `[[0,1,0.2],[2,1,0.8]]` | `{"parameter":"Track Volume","readback":[[0.5,0.3],[2.5,0.9]]}` (after fix); `{"parameter":"Volume","created_envelope":false,"readback":[[0.5,0.2],[2.5,0.8]]}` | PASS | `exec [env.value_at_time(t) for t in (0,0.5,1.5,2,2.5,3.9)]` -> `[0.85,0.3,0.85,0.85,0.9,0.85]` |
| 64 | `arrangement/create_clip` | `4 0 4` | `{"result":{"_lom":"Clip","path":"live_set tracks 4 arrangement_clips 0"},"arrangement_clips":[{"index":0,"start_time":0,"end_time":4,"length":4,"midi":true}]}` | PASS | `arrangement/clips 4` -> `count:1` same clip |
| 65 | `arrangement/dup_from_session` | `4 0 8` | `{"result":{"_lom":"Clip","path":"live_set tracks 4 arrangement_clips 1"},"arrangement_clips":[{...0-4},{"index":1,"start_time":8,"end_time":12,"length":4}]}` | PASS | `arrangement/clips 4` -> `count:2` |
| 66 | `arrangement/clips` | `4` | `{"count":2,"clips":[...]}` | PASS | matches `lom/children tracks 4` -> `arrangement_clips:2` |
| 67 | `song/undo_group` | `begin`; `lom/set name undo-A`; `lom/set panning 0.5`; `end`; `/live/song/undo` (no reply by design) | `{"op":"begin","can_undo":true}` ... `{"op":"end","can_undo":true}` | PASS | after ONE undo: `lom/get name` -> `kbot-e2e`, `lom/get panning value` -> 0 (both reverted); repeated in e2e step 12 |
| 68 | `song/data` | `set kbot_test {"x":1}`; `get kbot_test` | `{"key":"kbot_test","value":{"x":1},"stored":"native"}`; `{"value":{"x":1}}` | PASS | also `lom/call live_set get_data ["kbot_test",null]` -> `{"x":1}` |
| 69 | `app/dialog` | `info` | `{"open_dialog_count":0,"message":"","button_count":0}` | PASS (info) | `press` not exercised: no dialog was open and opening one on the user's Live was out of bounds; unit-tested against the fake |
| 70 | `app/message` | `kbot e2e ok` | **first: FAIL** `Boost.Python.ArgumentError ... show_message(TPyHandle<ASongApp>, TText text, int buttons=..., ...)` (bug G: `Application.show_message` is a MODAL message box in 12.4.5) -> after fix `{"shown":"kbot e2e ok","method":"manager.show_message"}` (status bar) | PASS | no LOM read-back exists for the status bar; ControlSurface.show_message is what AbletonOSC's own `/live/api/show_message` uses |
| 71 | stock `/live/clip_slot/create_clip` | `4 1 4.0` | (no reply, by AbletonOSC design) | PASS | `lom/get live_set tracks 4 clip_slots 1 has_clip` -> true |
| 72 | stock `/live/clip/add/notes` | `4 1 60 0.0 1.0 100 0 64 1.0 0.5 100 0` | (no reply) | PASS | stock `/live/clip/get/notes 4 1` -> `[4,1,60,0,1,100,false,64,1,0.5,100,false]` (both notes exact, reply starts with track,clip -- the offset the TS parser fix relies on) |

Count: 39/41 addresses were sent to Live and answered with `ok:true` on the final code; the two remaining
addresses are the `clip/notes/set` and `clip/notes/remove` aliases, whose op forms (`clip/notes set|remove`) were
exercised but which were not themselves sent (rows 59-60). `app/dialog` only via `info`; `browser/preview` /
`stop_preview` and `app/message` have no LOM read-back by nature -- their PASS is "Live accepted the call and
echoed the item/text", not a state read. Zero FAILs on the final code among the addresses that were sent.

## 3. Bugs fixed (file:line refer to the repo copies; installed copy is a byte-identical `install.sh` output)

| # | Symptom in Live | Cause | Fix |
|---|---|---|---|
| A | every path op: `TypeError: 'Song' object is not callable` | `ableton.v2` `Component.__init__` stores the Song in an instance attribute `_song`; the handler's `_song()` method was shadowed | `packages/kbot/ableton/remote-script/kbot_ext.py:280` `_get_song()` (all 19 call sites); test shim `kbot_ext_test.py` `Component.__init__` now sets `_song`/`_layer`/`_parent` like the real class |
| B | replies > ~9.2 KB never arrive; `abletonosc.log`: `OSError: [Errno 40] Message too long` in `osc_server.send` | macOS `net.inet.udp.maxdgram` = 9216 caps a datagram at the socket's SO_SNDBUF; AbletonOSC's `send()` only catches `BuildError` | `kbot_ext.py:158` `_raise_send_buffer()` sets SO_SNDBUF to `SEND_BUFFER_BYTES` (65536) on the shared reply socket at handler init; `ping` reports `sndbuf`; proven with 12000/40000/59900-char replies |
| C | `browser/load Snare pad:T:N` on an empty pad -> `ValueError: Device DS Snare not found.` and a stray empty chain | Live 12 Drum Sampler presets report `is_device:true` but `Chain.insert_device(name)` only knows real device names; the deterministic branch did not fall back; the sample lane searched `all` so the instruments root won | `kbot_ext.py:1148,1185` try `chain.insert_device`, on failure select chain + focus + `browser.load_item` (recorded in `steps`); `kbot_ext.py:935` `EXACT_NAME_EXTENSIONS` (`Snare` == `Snare.wav` exact); `kbot_ext.py:950` `user_folders` allowed inside comma-separated categories; `packages/kbot/src/tools/ableton.ts:181` `loadSampleToPad` passes `user_library,user_folders,samples` |
| D | `device/move 4 1 2` returned `result:2` but the device stayed at index 1 | `Song.move_device(position)` is an insertion slot counted before removal (moving 1 -> "3" puts it last) | `kbot_ext.py:1420` caller passes the desired FINAL index, handler adds 1 when moving later inside the same container, reads the final index back by identity (`position`, `live_position_arg`, `warning` on mismatch); `kbot_ext.py:1436` chain-order refusal explained in the error; fake `move_device` in the test mirrors Live |
| E | `clip/quantize ... q_quarter` -> `unknown grid` | enum members are `g_bar g_half g_quarter g_eighth g_sixteenth ...` (`Live.Clip.GridQuantization.names`) | `kbot_ext.py:1816` `_grid_enum` accepts `g_*`, bare (`quarter`), `q_*`, any case; error lists the known names; test stub renumbered to Live's real values |
| F | `clip/automation` read-back `[[0,0],[2,0]]` although the envelope was written | `Envelope.value_at_time(t)` at a step's exact start returns the pre-step value; sampling was at `t`; also values are in the parameter's own units (0.2 semitones rounds to 0) | `kbot_ext.py:1886` read back at `t + length/2`; README documents native units; e2e derives values from `min`/`max` |
| G | `app/message` -> `Boost.Python.ArgumentError ... show_message(TText, int buttons=...)` | in 12.4.5 `Application.show_message` is a modal message box (`show_on_the_fly_message` too) -- would block Live | `kbot_ext.py:2010` uses `ControlSurface.show_message` (status bar) via `self.manager`, reply carries `method` |
| H | first install: `/live/api/reload` -> `Unknown OSC address: /live/kbot/ping` | `manager.py` is not reloaded by `reload_imports()`; the running instance keeps the pre-patch `init_api` | new `tools/ableton/kbot-reload.mjs` (`--bootstrap` via `/live/exec`: reload `AbletonOSC.manager`, swap `mgr.__class__`, `reload_imports()`); documented in `install.sh`, `README.md`, `docs/ableton/CONTROL.md` |
| I | TS `ableton_structure macros` would have sent `rack/macros <path> <json>` -> handler `op must be get\|set` | arg order mismatch vs the handler contract | `packages/kbot/src/tools/ableton-lom.ts:510` sends `path get` / `path set <json>`; `ableton-lom.test.ts` expectations updated |
| J | `lom/get tracks 0 clip_slots 0 clip name` -> `'NoneType' has no member 'name'` | empty slot resolves to `None` | `kbot_ext.py:643,659` and resolver: `LookupError: path '...' resolves to None (empty clip slot / unset property)` |

Also: `KBOT_EXT_VERSION` 0.1.0 -> 0.1.1; `ping` gained `sndbuf` and `max_reply_bytes`; automation/units, move
semantics, grid names and the message-box trap are documented in
`packages/kbot/ableton/remote-script/README.md`.

## 4. `tools/ableton/e2e.mjs` (spec 3.5) -- output of the final run

Run three times this session (after the last install); all three identical apart from the version suffix. Exit code 0.

```
PASS  ping /live/kbot/ping  -- kbot_ext 0.1.1 live 12.4.5b10 handlers 41
PASS  pre-clean stale scratch tracks  -- baseline 4 tracks
PASS  track/create midi -1 kbot-e2e  -- index 4, name kbot-e2e
PASS  track/insert_device Operator  -- method track.insert_device, devices ["Operator"]
PASS  create 4-bar clip (clip_slots 0 create_clip 16.0)  -- has_clip true, length 16
PASS  clip/notes set (4 notes) + read back  -- count 4
PASS  clip/automation on Operator param + read back  -- Transpose (#2) envelope created=true readback [[2,-24],[10,24]] type=Device
PASS  set send A = 0.5 (mixer_device sends 0) + read back  -- send A 0.5 (previous 0)
PASS  track/insert_device Saturator + EQ Eight  -- ["Operator","Saturator","EQ Eight"]
PASS  device/set_active Saturator off/on + read back  -- false -> true
PASS  fire clip slot 0, read is_playing, stop  -- clip is_playing true, song is_playing true -> false
PASS  song/undo_group begin/end + one undo reverts both edits  -- name kbot-e2e, pan 0
PASS  snapshot < 60000 bytes and lists the scratch track  -- 3073 bytes, truncated=false, level=0, 5 tracks
PASS  cleanup: track/delete scratch + track count restored  -- 4 tracks (baseline 4)

14/14 PASS, 0 FAIL
```

Re-runnable: it deletes any stale `kbot-e2e` track first and asserts the track count returns to the baseline;
`KEEP=1` leaves the track for inspection. Exit 1 on any FAIL, 2 if UDP 11001 cannot be bound.

## 5. TS tools through kbot's registry (real `AbletonOSC` client, bound 11001)

Driver: `npx tsx` script importing `registerAbletonLomTools` / `registerAbletonTools` and `getTool(name).execute(args)`
from `packages/kbot/src` (no build needed; `npm run dev` uses tsx too). Outputs verbatim (trimmed where noted):

```
### ableton_lom {"action":"ping"}  (100ms)
{ "pong": true, "kbot_ext": "0.1.0", "handlers": 41, "python": "3.11.6", "sndbuf": 65536, "max_reply_bytes": 60000, "live": "12.4.5b9", "ok": true }
   (this pass ran while the installed copy still reported 0.1.0 at 12.4.5b9; KBOT_EXT_VERSION was bumped to 0.1.1 later the same session, section 3 -- the smoke table's row 1 is the final 0.1.1 ping)

### ableton_lom {"action":"describe","path":"tracks 0"}  (102ms)
{ "path": "tracks 0", "type": "Track", "members": { "View": {...}, "add_arm_listener": {"kind": "listener"}, ... [11074 chars]

### ableton_browser {"action":"search","query":"Operator","category":"instruments","limit":5}  (255ms)
{ "query": "Operator", "category": "instruments", "count": 4, "results": [ {"name":"Operator","uri":"query:Synths#Operator","is_loadable":true,"is_device":true,...},
  {"name":"Operator Hihat.adv",...}, {"name":"Operator Kick.adv",...}, {"name":"Operator Snare.adv",...} ], "budget_exhausted": false, "ok": true }

### ableton_structure {"action":"create_track","kind":"midi","name":"kbot-ts-e2e"}  (25ms)
{ "kind": "midi", "index": 4, "name": "kbot-ts-e2e", "count": 5, "ok": true }

### ableton_lom {"action":"get","path":"tracks 4","prop":"name"}  (76ms)
{ "path": "tracks 4", "prop": "name", "value": "kbot-ts-e2e", "ok": true }

### ableton_browser {"action":"insert_device","track":4,"name":"Saturator"}  (165ms)
{ "track": 4, "requested": "Saturator", "resolved": "Saturator", "method": "track.insert_device", "devices": ["Saturator"], "added": 1, "errors": [], "ok": true }

### ableton_lom {"action":"set","path":"tracks 4","prop":"name","value":"kbot-ts-e2e-2"}  (36ms)
{ "path": "tracks 4", "prop": "name", "value": "kbot-ts-e2e-2", "previous": "kbot-ts-e2e", "ok": true }

### ableton_structure {"action":"delete_track","track":4}  (117ms)
{ "deleted": 4, "name": "kbot-ts-e2e-2", "tracks": 4, "ok": true }

### ableton_lom {"action":"get","path":"live_set","prop":"tracks"}  (93ms)
{ ..., "value": [ {"name":"1-MIDI"}, {"name":"2-MIDI"}, {"name":"3-Audio"}, {"name":"4-Audio"} ], "ok": true }
recvPort used by TS client: 11001
```

Second pass -- the `ableton.ts` tools Phase A re-routed onto kbot handlers (1-based indexes on that plane):

```
### ableton_create_track {"type":"midi","name":"kbot-ts-e2e"}  (182ms)
Created midi track **kbot-ts-e2e** (track 5)
Via kbot handler read-back: {"kind":"midi","index":4,"name":"kbot-ts-e2e","count":5,"ok":true}

### ableton_clip {"action":"create","track":5,"clip":1,"length":8,"name":"ts-clip"}  (470ms)
Created clip **ts-clip** (8 beats / 2 bars) on track 5, slot 1
Read-back confirmed: slot 1 on track 5 has a clip (name "ts-clip", length 8 beats).

### ableton_midi {"action":"write","track":5,"clip":1,"notes":"[{60,0,1,100},{64,1,0.5,90}]"}  (199ms)
Wrote **2 notes** to track 5, clip 1: C4 at beat 0, E4 at beat 1
Read-back confirmed: all 2 notes present (clip now holds 2 notes).

### ableton_midi {"action":"read","track":5,"clip":1}  (146ms)
| 60 | C4 | 0.00 | 1.00 | 100 |   | 64 | E4 | 1.00 | 0.50 | 90 |

### ableton_browser {"action":"insert_device","track":4,"name":"Drum Rack"}   -> devices ["Drum Rack"], ok
### ableton_structure {"action":"macros","path":"tracks 4 devices 0"}          -> visible_macro_count 8, 16 macros, values 0
### ableton_structure {"action":"macros","path":"tracks 4 devices 0","value":"[0.5, 1]"} -> Macro 1 value 0.5, Macro 2 value 1 (read back)
### ableton_structure {"action":"build_pad","path":"tracks 4 devices 0","note":36,"sample":".../kbot-trap-kit/Kick_808.wav","name":"Kick"}
{ "pad": {"note":36,"name":"Kick","chains":[{"name":"Kick","devices":["Kick_808"]}]}, "sample_file_path": ".../Kick_808.wav", "steps": [...], "errors": [], "ok": true }

### ableton_load_sample {"track":5,"pad":38,"sample":"Snare"}  (110ms)      [first run FAILED: "Device DS Snare not found." -> bug C fixed]
Loaded onto pad D1 (track 5) via /live/kbot/browser/load. Live read-back:
{ "loaded": "Snare.wav", "uri": "query:UserLibrary#Samples:kbot-trap-kit:Snare.wav", "category": "user_library", "target": "pad:4:38", "method": "selected_drum_pad+load_item", "pad": {"note":38,"name":"Snare",...} ... }

### ableton_lom {"action":"get","path":"tracks 4 devices 0 drum_pad_note 38 chains 0","prop":"devices"} -> [SimplerDevice "Snare"]
### ableton_mixer {"action":"snapshot"} -> table of 5 tracks at 85% / C
### ableton_audio_analysis {}  (255ms)
## Audio Levels  **Master Output**  Left: [....] -inf dB  Right: [....] -inf dB  (master meters via lom/get master_track output_meter_left/right; -inf = silence, not "no signal")
### ableton_structure {"action":"delete_track","track":4} -> {"deleted":4,"name":"kbot-ts-e2e","tracks":4}
### ableton_lom {"action":"children","path":"live_set"} -> {"return_tracks":2,"scenes":8,"tracks":4,"visible_tracks":4}
```

## 6. Offline test runs (exact commands)

| Command | Result |
|---|---|
| `cd packages/kbot && python3 -m unittest ableton/remote-script/kbot_ext_test.py` (3.14.6) | Ran 34 tests, OK |
| `cd packages/kbot && python3.11 -m unittest ableton/remote-script/kbot_ext_test.py` (Live's major.minor) | Ran 34 tests, OK |
| `cd packages/kbot && npx vitest run src/tools/ableton-lom.test.ts` | 1 file, 48 tests passed |
| `cd packages/kbot && npx vitest run` | 74 files, 1392 tests passed |
| `cd packages/kbot && npx tsc --noEmit -p .` | exit 0 |
| `packages/kbot/ableton/remote-script/install.sh --check` | exit 0 (`ok kbot_ext fully installed`) |
| `node tools/ableton/e2e.mjs` (x3) | 14/14 PASS, exit 0 |

## 7. Known limits / not proven here

- `clip/notes/set` and `clip/notes/remove` (the slash aliases) were never sent to Live; the op forms were. See rows 59-60.
- `app/dialog press` -- only `info` was exercised (no dialog was open); `press` is unit-tested against the fake.
- `snapshot` `truncated:true` -- the shrink ladder is unit-tested (303 fake tracks x 64 slots); on the 6-track Set the
  reply is 3.5 KB and never truncates. `exec "x"*60000` proved the generic oversize path (`reply too large`).
- `browser/preview` / `stop_preview` / `app/message` have no LOM state to read back; PASS means Live accepted the
  call and echoed the item/text.
- The kbot `AbletonOSC` TS client falls back to 11002.. when 11001 is busy, but AbletonOSC always replies to 11001 --
  a busy 11001 therefore looks like a timeout, not a bind error. Pre-existing behaviour, left as is; documented in
  `docs/ableton/CONTROL.md` section 2.
- `Application.get_version_string()` reported `12.4.5b8` -> `b10` across the session; the suffix appears to be a
  build/reload counter, not the marketed beta number.

## Addendum — 0.1.2 re-verified on Live 12.4.5b11 (2026-08-18 20:5x)

Live auto-updated b5 -> b11 (delta chain via WebConnector; Live relaunched itself
at 20:26:17). AbletonOSC (UDP 11000), KBotBridge (TCP 9997) and kbot_ext loaded
on the new build without changes. After the adversarial review bumped kbot_ext to
0.1.2 (private/dunder member guard, BaseException catch, SO_SNDBUF-aware reply cap,
index guards), it was installed and hot-reloaded (`kbot-reload.mjs` ->
`{"kbot_ext":"0.1.2","handlers":41,"python":"3.11.6","live":"12.4.5b11"}`) and:

- `node tools/ableton/e2e.mjs` -> 14/14 PASS, exit 0 (scratch track cleaned, 4 tracks restored)
- guard: `lom/get live_set __dict__` -> `ok:false "property name '__dict__' is not allowed"`; `lom/get live_set tempo` -> 120.0
- offline: unittest 42/42, vitest ableton-lom + formats 89/89, kbot suite 1398/1398, `tsc --noEmit` exit 0, `install.sh --check` exit 0
