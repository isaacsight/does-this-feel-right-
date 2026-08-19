# Ableton full control — design (2026-08-18)

> Goal, in Isaac's words: "make sure you can control all of Ableton and make
> anything for it." Operator: Fable 5 via kbot. This spec is the evidence-led
> design; the plan is at the bottom.

## 1. Ground truth on this Mac (measured 2026-08-18)

| Fact | Evidence |
|---|---|
| Live 12.4.5b5 running (`/Applications/Ableton Live 12 Beta.app`); 12.2 Suite also installed | `ps`, `Info.plist` |
| **AbletonOSC** loaded (UDP 11000 in / 11001 out) from `~/Music/Ableton/User Library/Remote Scripts/AbletonOSC` at upstream commit `0ca6821` + 230 lines of local edits (`/live/exec`, `/live/track/load/device`, `/live/device/configure_all`, `show_gui`, `get/type_info`) | `lsof`, `git diff` |
| **KBotBridge** loaded (TCP 9997, JSON-lines, `{"action":...}`), 7 actions: ping, browser_search/load/load_by_name/categories, list_tracks, list_devices | probe |
| **AbletonBridge (9001) NOT running** — `ableton_load_effect/browse/load_preset/effect_chain` in kbot are dead | `lsof` |
| `kbot_bridge.py` (17 `/live/kbot/*` handlers from March) is **not installed** in the loaded AbletonOSC — `ableton_create_track`, `ableton_load_sample`, `ableton_build_drum_rack` call addresses that don't exist | `find`, `manager.py` |
| `/live/master/*` addresses used by `ableton_mixer` don't exist in AbletonOSC | source grep |
| OSC clip layer **works** (create_clip → add/notes → get/notes read back exact) — the June "clip bug" is gone | probe |
| `/live/exec` works: arbitrary Python inside Live with `song`, `app`, `Live`, `tracks` in scope | probe |
| Full LOM dump taken from inside Live: `docs/ableton/lom-dump-12.4.5b5.json` (114 classes, 43 `Live.*` modules) | `/live/exec` → file |
| Only ONE process can bind UDP 11001 → Live probing must be serialized | `dgram` |

Present in the 12.4.5 LOM (so reachable by an agent): `Track.create_midi_clip/
create_audio_clip` (arrangement), `duplicate_clip_to_arrangement`,
`Track.insert_device`, `Song.move_device/find_device_position`,
`Clip.create_automation_envelope/automation_envelope/clear_envelope`,
`Clip.quantize/crop/duplicate_region/get_all_notes_extended/apply_note_modifications`,
`RackDevice.insert_chain/add_macro/randomize_macros/store_variation`,
`DrumChain.in_note/out_note/choke_group`, `SimplerDevice.replace_sample/warp_*/
slicing`, `PluginDevice.presets/selected_preset_index`, `Browser.load_item/
preview_item/hotswap_target`, `Song.begin_undo_step/end_undo_step`,
`Song.get_data/set_data`, `Song.tuning_system`, `Track.take_lanes`,
`Application.press_current_dialog_button/show_message`, listeners on everything.

NOT in the LOM (need UI automation or a file-level tool): freeze/flatten,
export audio/stems, save/open Set, preferences, plugin GUI interaction,
loading a Max for Live device programmatically is via browser only.

## 2. Architecture — one substrate, four planes, always read back

```
Fable 5 / kbot tools (TS)  ──UDP 11000──▶  AbletonOSC + kbot_ext.py (inside Live)  ──▶ LOM
        │                                       ▲ /live/api/reload hot-reloads it
        ├──TCP 9997──▶ KBotBridge (kept, thin)   │
        ├──peekaboo/computer-use──▶ Live UI (freeze/export/save/dialogs)
        ├──file generators──▶ .als / .adg / .adv / .mid / .maxpat / Remote Script / Extension
        └──Extensions SDK (human right-click) / Max for Live (real-time)  — unchanged
```

**Plane A — Live control (agent-driveable, primary):** AbletonOSC stays the
transport; we add **one** module `kbot_ext.py` registered as an AbletonOSC
handler (`KbotHandler`) that exposes the **whole LOM generically** plus typed
convenience ops. Every mutating handler returns a JSON read-back of the thing
it changed. `/live/exec` stays as the last-resort escape hatch (localhost only;
documented as such).

**Plane B — Extensions SDK** and **Plane C — Max for Live**: unchanged
(see `packages/kbot-ableton-extension/ABLETON_CONTROL_PLANES.md`).

**Plane D — UI automation:** for what the LOM cannot do (freeze, flatten,
export, save, open, prefs) kbot drives Live's UI via peekaboo/computer-use.
Out of scope to build this session; documented in the coverage matrix as
"UI-only" with the menu path.

**"Make anything for it" — file generators (no Live needed):**
`packages/kbot/src/ableton/formats/`: `.als` (Live Set, gzip XML) read/inspect
+ write-from-template, `.adg`/`.adv` (rack / device preset), `.mid` (SMF from
notes), `.maxpat` (M4L device skeleton: LiveAPI js + Node for Max),
Remote-Script scaffold. Extension scaffold already exists.

## 3. Components

### 3.1 `kbot_ext.py` (Python 3, runs inside Live) — `packages/kbot/ableton/remote-script/`
Registered by patching `manager.py` `handlers` list. Address prefix `/live/kbot/`.
All replies are one OSC string arg = JSON `{ok, ...}` or `{ok:false, error}`.

Generic LOM (the "control everything" primitive):
- `lom/get <path> <prop>` · `lom/set <path> <prop> <json>` · `lom/call <path> <method> <json args>`
- `lom/describe <path>` → members with types + current scalar values
- `lom/children <path>` → counts of list props (tracks, devices, clip_slots …)
- Path grammar (Max LiveAPI style, space-separated): `live_set`, `tracks 0`,
  `return_tracks 1`, `master_track`, `scenes 3`, `cue_points 0`, `groove_pool
  grooves 0`, `view`, `tracks 0 clip_slots 2 clip`, `tracks 0 devices 1
  parameters 4`, `... devices 0 chains 1 devices 0`, `... drum_pads 36 chains 0`,
  `app`, `app browser instruments`, `this_device` not needed.
- `exec <code>` (existing behaviour, JSON-wrapped) · `snapshot [depth]` (whole Set as JSON) · `snapshot_file <path>`

Browser (absorbs KBotBridge's proven search/load logic; KBotBridge stays as-is):
- `browser/search <query> [category] [limit]` → `[{name, uri, is_loadable, is_device, path}]`
- `browser/load <uri|name> <target>` target = `track:N` | `pad:N:note` | `selected`; read-back = device list of target
- `browser/preview <uri>` / `browser/stop_preview`
- `device/presets <track> <device>` (PluginDevice.presets, else browser hotswap children) · `device/load_preset <track> <device> <index|name>`

Structure & authoring:
- `track/create midi|audio|return [index] [name]` → `{index,name}`; `track/delete`, `track/duplicate`
- `track/insert_device <track> <name> [position]` (native via browser; read-back devices)
- `device/delete`, `device/move`, `device/set_active`
- `rack/insert_chain <path> [name]`, `rack/add_macro <path>`, `rack/macros <path>` get/set
- `drum/build_pad <rack path> <note> <sample abs path> [name]` → insert chain → Simpler → `replace_sample`; read-back pad name + sample path
- `clip/notes/get|set|add|remove` (set = replace all), `clip/quantize`, `clip/automation <clip path> <param path> [[time,len,value]…]`
- `arrangement/create_clip <track> <start> <length>` (MIDI) / `arrangement/dup_from_session <track> <slot> <time>` / `arrangement/clips <track>`
- `song/undo_group begin|end`, `song/data get|set <key> [json]`
- `app/dialog press <index>` · `app/message <text>`

### 3.2 kbot TS tools — `packages/kbot/src/tools/`
- NEW `ableton-lom.ts`: `ableton_lom` (get/set/call/describe/children/exec/snapshot),
  `ableton_browser` (search/load/preview/presets/load_preset) — OSC via existing
  `ableton-osc.ts` client. Read-back surfaced in tool output.
- FIX `ableton.ts`: `/live/kbot/create_*`, `/live/kbot/load_sample_file` →
  new handlers; `/live/master/*` → `lom/get master_track …`; `ableton_clip
  create` + `ableton_midi add` verify by read-back before saying "success".
- FIX `ableton-bridge-tools.ts`: route `load_effect/browse/load_preset/effect_chain`
  through the new OSC browser handlers; 9001 becomes an optional fallback.
- Tests: fake OSC server (node:dgram) in vitest; JSON reply shape; read-back gating.

### 3.3 Docs
- `docs/ableton/lom-coverage.md` — generated from the dump: class × member →
  {tool action | `ableton_lom` generic | UI-only | n/a}. Regenerable by script.
- `docs/ableton/CONTROL.md` — how Fable/kbot drives Live: planes, ports,
  reload, install, verification rule, examples. Update `ABLETON_CONTROL_PLANES.md`.

### 3.4 File generators — `packages/kbot/src/ableton/formats/`
`als.ts` (gunzip → XML → structure JSON; write minimal Set from template with
N MIDI/audio tracks, tempo, clips+notes), `adg.ts` (Instrument/Audio-Effect
Rack with chains + macros), `adv.ts` (device preset), `midi.ts` (SMF type 1
writer), `maxpat.ts` (M4L skeleton), `remote-script.ts` (Control Surface
scaffold). Round-trip test against a Live-saved `.als` on disk.

### 3.5 Live E2E — `tools/ableton/e2e.mjs`
Serialized script: create MIDI track → insert Operator → write 4-bar clip →
add automation → set send A → insert Saturator + EQ Eight → fire → read back
every step → stop → cleanup (delete track). Prints PASS/FAIL per step. This
is the acceptance test.

## 4. Error handling & safety
- Every kbot_ext handler try/excepts and returns `{ok:false,error,trace_tail}`;
  never raises into AbletonOSC's server loop.
- Writes are read back; the TS tool reports what Live says, not what we sent.
- `/live/exec` is localhost-only, unauthenticated: documented as dev-only; not
  exposed by default in kbot MCP outside `ableton_lom exec` (which logs code).
- Undo grouping wraps multi-step ops so one Cmd-Z reverts.
- Reload without touching Live prefs: `/live/api/reload`.

## 5. Out of scope (this session)
Plane D UI automation implementation; Extensions SDK changes; new M4L devices
beyond the skeleton; AbletonBridge (9001) — superseded.

## 6. Plan (executed via ultracode workflow; Live access serialized)
Phase A (parallel, no Live): (1) kbot_ext.py + fake-LOM unit tests; (2) TS tools
+ fixes + vitest; (3) formats package + tests; (4) coverage matrix + CONTROL.md.
Phase B (sequential, Live): install → reload → smoke every handler → fix →
E2E. Phase C: adversarial review of diff, claims re-verified against Live.
