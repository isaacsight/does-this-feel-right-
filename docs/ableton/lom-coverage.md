# LOM coverage matrix — Live 12.4.5b5 × kbot

> Generated 2026-08-18 by `node tools/ableton/gen-coverage.mjs` from
> `docs/ableton/lom-dump-12.4.5b5.json` (measured inside Live via `/live/exec`) and
> `tools/ableton/coverage-map.json` (authored). Do not hand-edit; edit the map and regenerate.
> Operator manual: [`CONTROL.md`](./CONTROL.md).

**How to read it.** Every LOM member is reachable from kbot one of five ways:

| via | meaning |
|---|---|
| `tool` | a typed kbot handler (`ableton_lom` / `ableton_browser` / `ableton_structure` → `kbot_ext.py` `/live/kbot/*`), with JSON read-back |
| `lom` | the generic plane: `ableton_lom get` / `set` / `call` / `describe` / `children` `<path> ...` — the default for anything without a typed handler |
| `osc` | a stock AbletonOSC address (upstream `0ca6821` + local edits); listed where one exists, with the existing kbot tool that speaks it |
| `ui` | the LOM cannot do it; the Live menu path is given (Plane D, peekaboo/computer-use) |
| `na` | enum constant or record class; not addressed, passed as a value |

**Kind column.** `property (type)` / `method` are measured on a live instance. A trailing `~` means the kind was
inferred (the class was only enumerated at class level; the type came from a same-named member elsewhere or from the
name); `?` means unknown — `ableton_lom describe <path>` reports it at runtime. Paths are Max LiveAPI style, 0-based.

Classes: [Song](#song) · [Song.View](#songview) · [Song.CuePoint](#songcuepoint) · [Application](#application) · [Application.View](#applicationview) · [Application.ControlSurfaceProxy](#applicationcontrolsurfaceproxy) · [Track](#track) · [Track.View](#trackview) · [MixerDevice](#mixerdevice) · [ChainMixerDevice](#chainmixerdevice) · [ClipSlot](#clipslot) · [Clip](#clip) · [Clip.View](#clipview) · [Scene](#scene) · [Device](#device) · [Device.View](#deviceview) · [DeviceParameter](#deviceparameter) · [RackDevice](#rackdevice) · [Chain](#chain) · [DrumPad](#drumpad) · [DrumChain](#drumchain) · [SimplerDevice](#simplerdevice) · [Sample](#sample) · [PluginDevice](#plugindevice) · [MaxDevice](#maxdevice) · [CompressorDevice](#compressordevice) · [Eq8Device](#eq8device) · [WavetableDevice](#wavetabledevice) · [HybridReverbDevice](#hybridreverbdevice) · [SpectralResonatorDevice](#spectralresonatordevice) · [DriftDevice](#driftdevice) · [MeldDevice](#melddevice) · [RoarDevice](#roardevice) · [ShifterDevice](#shifterdevice) · [Browser](#browser) · [Browser.BrowserItem](#browserbrowseritem) · [GroovePool](#groovepool) · [Groove](#groove) · [TuningSystem](#tuningsystem)

Enums and value classes: [Application.ControlDescription](#applicationcontroldescription) · [Application.ControlDescriptionVector](#applicationcontroldescriptionvector) · [Application.MessageButtons](#applicationmessagebuttons) · [Application.PushDialogType](#applicationpushdialogtype) · [Application.UnavailableFeature](#applicationunavailablefeature) · [Application.UnavailableFeatureVector](#applicationunavailablefeaturevector) · [Application.Variants](#applicationvariants) · [Browser.BrowserItemVector](#browserbrowseritemvector) · [Browser.FilterType](#browserfiltertype) · [Browser.Relation](#browserrelation) · [Clip.ClipLaunchQuantization](#clipcliplaunchquantization) · [Clip.GridQuantization](#clipgridquantization) · [Clip.LaunchMode](#cliplaunchmode) · [Clip.MidiNote](#clipmidinote) · [Clip.MidiNoteVector](#clipmidinotevector) · [Clip.WarpMarker](#clipwarpmarker) · [Clip.WarpMarkerVector](#clipwarpmarkervector) · [Clip.WarpMode](#clipwarpmode) · [ClipSlot.ClipSlotPlayingState](#clipslotclipslotplayingstate) · [Device.ATimeableValueVector](#deviceatimeablevaluevector) · [Device.DeviceType](#devicedevicetype) · [DeviceParameter.AutomationState](#deviceparameterautomationstate) · [DeviceParameter.ParameterState](#deviceparameterparameterstate) · [Eq8Device.EditMode](#eq8deviceeditmode) · [Eq8Device.GlobalMode](#eq8deviceglobalmode) · [Groove.Base](#groovebase) · [Sample.SlicingBeatDivision](#sampleslicingbeatdivision) · [Sample.SlicingStyle](#sampleslicingstyle) · [Sample.TransientLoopMode](#sampletransientloopmode) · [SimplerDevice.PlaybackMode](#simplerdeviceplaybackmode) · [SimplerDevice.SlicingPlaybackMode](#simplerdeviceslicingplaybackmode) · [Song.BeatTime](#songbeattime) · [Song.CaptureDestination](#songcapturedestination) · [Song.CaptureMode](#songcapturemode) · [Song.Quantization](#songquantization) · [Song.RecordingQuantization](#songrecordingquantization) · [Song.SessionRecordStatus](#songsessionrecordstatus) · [Song.SmptTime](#songsmpttime) · [Song.TimeFormat](#songtimeformat) · [Track.DeviceInsertMode](#trackdeviceinsertmode) · [Track.RoutingChannel](#trackroutingchannel) · [Track.RoutingChannelLayout](#trackroutingchannellayout) · [Track.RoutingChannelVector](#trackroutingchannelvector) · [Track.RoutingType](#trackroutingtype) · [Track.RoutingTypeCategory](#trackroutingtypecategory) · [Track.RoutingTypeVector](#trackroutingtypevector) · [TuningSystem.PitchClassAndOctave](#tuningsystempitchclassandoctave) · [TuningSystem.ReferencePitch](#tuningsystemreferencepitch) · [WavetableDevice.EffectMode](#wavetabledeviceeffectmode) · [WavetableDevice.FilterRouting](#wavetabledevicefilterrouting) · [WavetableDevice.ModulationSource](#wavetabledevicemodulationsource) · [WavetableDevice.UnisonMode](#wavetabledeviceunisonmode) · [WavetableDevice.VoiceCount](#wavetabledevicevoicecount) · [WavetableDevice.Voicing](#wavetabledevicevoicing)

## Song

Path example: `live_set` · 98 members (+ 147 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method | `na` — nested class Song.View — see its own section |  |
| `appointed_device` | property (NoneType) | `lom` — ableton_lom get live_set appointed_device · set live_set appointed_device <json> |  |
| `arrangement_overdub` | property (bool) | `osc` — /live/song/get/arrangement_overdub · /live/song/set/arrangement_overdub · /live/song/start_listen/arrangement_overdub |  |
| `back_to_arranger` | property (bool) | `osc` — /live/song/get/back_to_arranger · /live/song/set/back_to_arranger · /live/song/start_listen/back_to_arranger | kbot: ableton_song back_to_arranger |
| `begin_undo_step` | method | `tool` — ableton_structure undo_begin | wrap multi-step ops so one Cmd-Z reverts |
| `can_capture_midi` | property (bool) | `lom` — ableton_lom get live_set can_capture_midi (read-only) |  |
| `can_jump_to_next_cue` | property (bool) | `lom` — ableton_lom get live_set can_jump_to_next_cue (read-only) |  |
| `can_jump_to_prev_cue` | property (bool) | `lom` — ableton_lom get live_set can_jump_to_prev_cue (read-only) |  |
| `can_redo` | property (bool) | `osc` — /live/song/get/can_redo · /live/song/start_listen/can_redo |  |
| `can_undo` | property (bool) | `osc` — /live/song/get/can_undo · /live/song/start_listen/can_undo |  |
| `canonical_parent` | property (NoneType) | `lom` — ableton_lom get live_set canonical_parent (read-only) |  |
| `capture_and_insert_scene` | method | `osc` — /live/song/capture_and_insert_scene |  |
| `capture_midi` | method | `osc` — /live/song/capture_midi | kbot: ableton_song capture_midi |
| `clip_trigger_quantization` | property (Quantization) | `osc` — /live/song/get/clip_trigger_quantization · /live/song/set/clip_trigger_quantization · /live/song/start_listen/clip_trigger_quantization | kbot: ableton_clip fire (sets quantization) |
| `continue_playing` | method | `osc` — /live/song/continue_playing |  |
| `count_in_duration` | property (int) | `lom` — ableton_lom get live_set count_in_duration · set live_set count_in_duration <json> |  |
| `create_audio_track` | method | `tool` — ableton_structure create_track kind=audio [index=N] [name=...] | read-back {index,name}. Replaces dead /live/kbot/create_audio_track |
| `create_midi_track` | method | `tool` — ableton_structure create_track kind=midi [index=N] [name=...] | read-back {index,name}. Replaces dead /live/kbot/create_midi_track; stock OSC /live/song/create_midi_track <index> has no read-back |
| `create_return_track` | method | `tool` — ableton_structure create_track kind=return [name=...] | read-back {index:"return:N",name}; also /live/song/create_return_track |
| `create_scene` | method | `osc` — /live/song/create_scene | kbot: ableton_scene create |
| `cue_points` | property (Vector) | `osc` — /live/song/get/cue_points · /live/song/cue_point/jump · /live/song/cue_point/add_or_delete · /live/song/cue_point/set/name | kbot: ableton_song cue_jump / cue_add / cue_delete |
| `current_song_time` | property (float) | `osc` — /live/song/get/current_song_time · /live/song/set/current_song_time · /live/song/start_listen/current_song_time | kbot: ableton_transport position |
| `delete_return_track` | method | `tool` — raw handler /live/kbot/track/delete return:N (verified 2026-08-18) | the TS ableton_structure delete_track action takes an int track index only; also /live/song/delete_return_track <index> |
| `delete_scene` | method | `osc` — /live/song/delete_scene |  |
| `delete_track` | method | `tool` — ableton_structure delete_track track=N | also /live/song/delete_track <index> |
| `duplicate_scene` | method | `osc` — /live/song/duplicate_scene |  |
| `duplicate_track` | method | `tool` — ableton_structure duplicate_track track=N | also /live/song/duplicate_track <index> |
| `end_undo_step` | method | `tool` — ableton_structure undo_end |  |
| `exclusive_arm` | property (bool) | `lom` — ableton_lom get live_set exclusive_arm · set live_set exclusive_arm <json> |  |
| `exclusive_solo` | property (bool) | `lom` — ableton_lom get live_set exclusive_solo · set live_set exclusive_solo <json> |  |
| `file_path` | property (str) | `ui` — File > Save Live Set (Cmd-S) / File > Save Live Set As... / File > Open Live Set (Cmd-O) | read the path: ableton_lom get live_set file_path. No save/open method in the LOM |
| `find_device_position` | method | `lom` — ableton_lom call live_set find_device_position [{"_path":"<device path>"},{"_path":"<target path>"},position] | not called by the move_device handler (it reads the final index back by identity instead) |
| `force_link_beat_time` | method | `osc` — /live/song/force_link_beat_time |  |
| `get_beats_loop_length` | method | `lom` — ableton_lom call live_set get_beats_loop_length [args] |  |
| `get_beats_loop_start` | method | `lom` — ableton_lom call live_set get_beats_loop_start [args] |  |
| `get_current_beats_song_time` | method | `lom` — ableton_lom call live_set get_current_beats_song_time [args] |  |
| `get_current_smpte_song_time` | method | `lom` — ableton_lom call live_set get_current_smpte_song_time [args] |  |
| `get_data` | method | `tool` — ableton_structure data_get key=<key> | per-Set persistent key/value; read-back = value |
| `groove_amount` | property (float) | `osc` — /live/song/get/groove_amount · /live/song/set/groove_amount · /live/song/start_listen/groove_amount | kbot: ableton_song groove |
| `groove_pool` | property (GroovePool) | `lom` — ableton_lom children `live_set groove_pool` → grooves |  |
| `is_ableton_link_enabled` | property (bool) | `osc` — /live/song/get/is_ableton_link_enabled · /live/song/set/is_ableton_link_enabled · /live/song/start_listen/is_ableton_link_enabled |  |
| `is_ableton_link_start_stop_sync_enabled` | property (bool) | `lom` — ableton_lom get live_set is_ableton_link_start_stop_sync_enabled · set live_set is_ableton_link_start_stop_sync_enabled <json> |  |
| `is_counting_in` | property (bool) | `lom` — ableton_lom get live_set is_counting_in · set live_set is_counting_in <json> |  |
| `is_cue_point_selected` | method | `lom` — ableton_lom call live_set is_cue_point_selected [args] |  |
| `is_playing` | property (bool) | `osc` — /live/song/get/is_playing · /live/song/start_listen/is_playing | kbot: ableton_transport status |
| `jump_by` | method | `osc` — /live/song/jump_by | kbot: ableton_song jump_by |
| `jump_to_next_cue` | method | `osc` — /live/song/jump_to_next_cue | kbot: ableton_song cue_next |
| `jump_to_prev_cue` | method | `osc` — /live/song/jump_to_prev_cue | kbot: ableton_song cue_prev |
| `last_event_time` | property (float) | `lom` — ableton_lom get live_set last_event_time · set live_set last_event_time <json> |  |
| `loop` | property (bool) | `osc` — /live/song/get/loop · /live/song/set/loop · /live/song/start_listen/loop | kbot: ableton_song loop |
| `loop_length` | property (float) | `osc` — /live/song/get/loop_length · /live/song/set/loop_length · /live/song/start_listen/loop_length | kbot: ableton_song loop_length |
| `loop_start` | property (float) | `osc` — /live/song/get/loop_start · /live/song/set/loop_start · /live/song/start_listen/loop_start | kbot: ableton_song loop_start |
| `master_track` | property (Track) | `lom` — ableton_lom describe master_track · get `master_track mixer_device volume` value | there is no /live/master/* address in AbletonOSC; ableton_audio_analysis reads master meters through /live/kbot/lom/get master_track output_meter_left\|right (since 2026-08-18) |
| `metronome` | property (bool) | `osc` — /live/song/get/metronome · /live/song/set/metronome · /live/song/start_listen/metronome | kbot: ableton_song metronome |
| `midi_recording_quantization` | property (RecordingQuantization) | `osc` — /live/song/get/midi_recording_quantization · /live/song/set/midi_recording_quantization · /live/song/start_listen/midi_recording_quantization |  |
| `move_device` | method | `tool` — ableton_structure move_device track=N device=M index=<final index> | raw handler /live/kbot/device/move <track> <device> <newpos> [target track\|chain path]; the handler compensates for Live's insertion-slot semantics and reads the final index back by identity (bug D, verified 2026-08-18); read-back = device list |
| `name` | property (str) | `ui` — File > Save Live Set As... (the name follows the file) | read: ableton_lom get live_set name |
| `nudge_down` | property (bool) | `osc` — /live/song/get/nudge_down · /live/song/set/nudge_down · /live/song/start_listen/nudge_down |  |
| `nudge_up` | property (bool) | `osc` — /live/song/get/nudge_up · /live/song/set/nudge_up · /live/song/start_listen/nudge_up |  |
| `overdub` | property (bool) | `lom` — ableton_lom get live_set overdub · set live_set overdub <json> |  |
| `play_selection` | method | `lom` — ableton_lom call live_set play_selection [args] |  |
| `punch_in` | property (bool) | `osc` — /live/song/get/punch_in · /live/song/set/punch_in · /live/song/start_listen/punch_in | kbot: ableton_song punch_in |
| `punch_out` | property (bool) | `osc` — /live/song/get/punch_out · /live/song/set/punch_out · /live/song/start_listen/punch_out | kbot: ableton_song punch_out |
| `re_enable_automation` | method | `osc` — /live/song/re_enable_automation |  |
| `re_enable_automation_enabled` | property (bool) | `lom` — ableton_lom get live_set re_enable_automation_enabled · set live_set re_enable_automation_enabled <json> |  |
| `record_mode` | property (bool) | `osc` — /live/song/get/record_mode · /live/song/set/record_mode · /live/song/start_listen/record_mode | kbot: ableton_transport record |
| `redo` | method | `osc` — /live/song/redo | kbot: ableton_song redo |
| `return_tracks` | property (Vector) | `lom` — ableton_lom children live_set → return_tracks; path `return_tracks N` |  |
| `root_note` | property (int) | `osc` — /live/song/get/root_note · /live/song/set/root_note · /live/song/start_listen/root_note |  |
| `scale_intervals` | property (IntVector) | `lom` — ableton_lom get live_set scale_intervals · set live_set scale_intervals <json> |  |
| `scale_mode` | property (bool) | `lom` — ableton_lom get live_set scale_mode · set live_set scale_mode <json> |  |
| `scale_name` | property (str) | `osc` — /live/song/get/scale_name · /live/song/set/scale_name · /live/song/start_listen/scale_name |  |
| `scenes` | property (Vector) | `osc` — /live/song/get/num_scenes · /live/song/get/scenes/name | kbot: ableton_scene list |
| `scrub_by` | method | `lom` — ableton_lom call live_set scrub_by [args] |  |
| `select_on_launch` | property (bool) | `lom` — ableton_lom get live_set select_on_launch · set live_set select_on_launch <json> |  |
| `session_automation_record` | property (bool) | `lom` — ableton_lom get live_set session_automation_record · set live_set session_automation_record <json> |  |
| `session_record` | property (bool) | `osc` — /live/song/get/session_record · /live/song/set/session_record · /live/song/start_listen/session_record |  |
| `session_record_status` | property (int) | `osc` — /live/song/get/session_record_status · /live/song/start_listen/session_record_status |  |
| `set_data` | method | `tool` — ableton_structure data_set key=<key> value=<json> | read-back = data_get |
| `set_or_delete_cue` | method | `osc` — /live/song/set_or_delete_cue | kbot: ableton_song cue_add/cue_delete |
| `signature_denominator` | property (int) | `osc` — /live/song/get/signature_denominator · /live/song/set/signature_denominator · /live/song/start_listen/signature_denominator | kbot: ableton_transport time_sig |
| `signature_numerator` | property (int) | `osc` — /live/song/get/signature_numerator · /live/song/set/signature_numerator · /live/song/start_listen/signature_numerator | kbot: ableton_transport time_sig |
| `song_length` | property (float) | `osc` — /live/song/get/song_length · /live/song/start_listen/song_length |  |
| `start_playing` | method | `osc` — /live/song/start_playing | kbot: ableton_transport play |
| `start_time` | property (float) | `lom` — ableton_lom get live_set start_time · set live_set start_time <json> |  |
| `stop_all_clips` | method | `osc` — /live/song/stop_all_clips | kbot: ableton_song stop_all_clips |
| `stop_playing` | method | `osc` — /live/song/stop_playing | kbot: ableton_transport stop |
| `swing_amount` | property (float) | `lom` — ableton_lom get live_set swing_amount · set live_set swing_amount <json> |  |
| `sync_parameter_changes` | method | `lom` — ableton_lom call live_set sync_parameter_changes [args] |  |
| `tap_tempo` | method | `osc` — /live/song/tap_tempo | kbot: ableton_song tap_tempo |
| `tempo` | property (float) | `osc` — /live/song/get/tempo · /live/song/set/tempo · /live/song/start_listen/tempo | kbot: ableton_transport tempo |
| `tempo_follower_enabled` | property (bool) | `lom` — ableton_lom get live_set tempo_follower_enabled · set live_set tempo_follower_enabled <json> |  |
| `tracks` | property (Vector) | `osc` — /live/song/get/num_tracks · /live/song/get/track_names · /live/song/get/track_data · /live/song/export/structure | kbot: ableton_session_info / ableton_track info; per-track paths via ableton_lom `tracks N` |
| `trigger_session_record` | method | `osc` — /live/song/trigger_session_record |  |
| `tuning_system` | property (NoneType) | `lom` — ableton_lom describe `live_set tuning_system` (TuningSystem: name, note_tunings, reference_pitch...) |  |
| `undo` | method | `osc` — /live/song/undo | kbot: ableton_song undo |
| `view` | property (View) | `lom` — ableton_lom get live_set view · set live_set view <json> |  |
| `visible_tracks` | property (Vector) | `lom` — ableton_lom get live_set visible_tracks |  |

## Song.View

Path example: `view` · 12 members (+ 27 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Song) | `lom` — ableton_lom get view canonical_parent (read-only) |  |
| `detail_clip` | property (Clip) | `lom` — ableton_lom get `view` detail_clip · set to a clip path to open it in Detail View |  |
| `draw_mode` | property (bool) | `lom` — ableton_lom get view draw_mode · set view draw_mode <json> |  |
| `follow_song` | property (bool) | `lom` — ableton_lom get view follow_song · set view follow_song <json> |  |
| `highlighted_clip_slot` | property (ClipSlot) | `osc` — /live/view/get/selected_clip · /live/view/set/selected_clip <track> <scene> | kbot: ableton_view clip (sets track+scene selection) |
| `mod_mapping_device` | property (NoneType) | `lom` — ableton_lom get view mod_mapping_device · set view mod_mapping_device <json> |  |
| `mod_mapping_parameter` | property (NoneType) | `lom` — ableton_lom get view mod_mapping_parameter · set view mod_mapping_parameter <json> |  |
| `select_device` | method | `osc` — /live/view/set/selected_device <track> <device> | kbot: ableton_view device |
| `selected_chain` | property (NoneType) | `lom` — ableton_lom get view selected_chain · set view selected_chain <json> |  |
| `selected_parameter` | property (NoneType) | `lom` — ableton_lom get view selected_parameter · set view selected_parameter <json> |  |
| `selected_scene` | property (Scene) | `osc` — /live/view/get/selected_scene · /live/view/set/selected_scene <scene> · /live/view/start_listen/selected_scene | kbot: ableton_view scene |
| `selected_track` | property (Track) | `osc` — /live/view/get/selected_track · /live/view/set/selected_track <track> · /live/view/start_listen/selected_track | kbot: ableton_view track |

## Song.CuePoint

Path example: `live_set cue_points 0` · 4 members (+ 6 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get live_set cue_points 0 canonical_parent (read-only) |  |
| `jump` | ? | `osc` — /live/song/cue_point/jump <index> | kbot: ableton_song cue_jump |
| `name` | property (str)~ | `osc` — /live/song/get/cue_points · /live/song/cue_point/set/name <index> <name> |  |
| `time` | ? | `osc` — /live/song/get/cue_points (returns name,time pairs) |  |

## Application

Path example: `app` · 23 members (+ 15 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method | `na` — nested class Application.View — see its own section |  |
| `average_process_usage` | property (float) | `osc` — /live/application/get/average_process_usage |  |
| `browser` | property (Browser) | `tool` — ableton_browser search\|load\|preview\|stop_preview\|presets\|load_preset\|insert_device | or ableton_lom describe `app browser` |
| `canonical_parent` | property (NoneType) | `lom` — ableton_lom get app canonical_parent (read-only) |  |
| `control_surfaces` | property (ObjectVector) | `lom` — ableton_lom get app control_surfaces | AbletonOSC + KBotBridge appear here |
| `current_dialog_button_count` | property (int) | `tool` — ableton_structure dialog_press index=N (read-back button_count) · ableton_lom get app current_dialog_button_count | raw handler /live/kbot/app/dialog info reads without pressing (verified 2026-08-18: open_dialog_count 0) |
| `current_dialog_message` | property (str) | `tool` — ableton_structure dialog_press index=N (read-back message) · ableton_lom get app current_dialog_message | raw handler /live/kbot/app/dialog info reads without pressing |
| `get_bugfix_version` | method | `lom` — ableton_lom call app get_bugfix_version [args] |  |
| `get_build_id` | method | `lom` — ableton_lom call app get_build_id [args] |  |
| `get_document` | method | `lom` — ableton_lom call app get_document (returns the Song) |  |
| `get_major_version` | method | `osc` — /live/application/get/version | returns (major, minor) |
| `get_minor_version` | method | `osc` — /live/application/get/version |  |
| `get_variant` | method | `lom` — ableton_lom call app get_variant [args] |  |
| `get_version_string` | method | `lom` — ableton_lom call app get_version_string [args] |  |
| `has_option` | method | `lom` — ableton_lom call app has_option [args] |  |
| `number_of_push_apps_running` | property (int) | `lom` — ableton_lom get app number_of_push_apps_running · set app number_of_push_apps_running <json> |  |
| `open_dialog_count` | property (int) | `tool` — ableton_structure dialog_press index=N (read-back open_dialog_count / open_dialog_count_after) · ableton_lom get app open_dialog_count | raw handler /live/kbot/app/dialog info reads without pressing |
| `peak_process_usage` | property (float) | `lom` — ableton_lom get app peak_process_usage · set app peak_process_usage <json> |  |
| `press_current_dialog_button` | method | `tool` — ableton_structure dialog_press index=N | read-back = open_dialog_count_after + current message; press path unit-tested against the fake only (no dialog was open during the 2026-08-18 Live run) |
| `show_message` | method | `lom` — ableton_lom call app show_message ["text"] -- WARNING: in 12.4.5 this is a MODAL message box (blocks Live until a button is pressed; measured 2026-08-18, VERIFICATION bug G). For a status-bar message use ableton_structure message text=<text> (ControlSurface.show_message via the AbletonOSC manager) or stock /live/api/show_message <text> | the kbot handler /live/kbot/app/message deliberately does NOT call this member |
| `show_on_the_fly_message` | method | `lom` — ableton_lom call app show_on_the_fly_message [args] |  |
| `unavailable_features` | property (UnavailableFeatureVector) | `lom` — ableton_lom get app unavailable_features · set app unavailable_features <json> |  |
| `view` | property (View) | `lom` — ableton_lom get app view · set app view <json> |  |

## Application.View

Path example: `app view` · 12 members (+ 12 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `NavDirection` | method | `lom` — ableton_lom call app view NavDirection [args] |  |
| `available_main_views` | method | `lom` — ableton_lom call app view available_main_views [args] |  |
| `browse_mode` | property (bool) | `lom` — ableton_lom get app view browse_mode · set app view browse_mode <json> |  |
| `canonical_parent` | property (Application) | `lom` — ableton_lom get app view canonical_parent (read-only) |  |
| `focus_view` | method | `lom` — ableton_lom call `app view` focus_view ["Session"] |  |
| `focused_document_view` | property (str) | `lom` — ableton_lom get app view focused_document_view · set app view focused_document_view <json> |  |
| `hide_view` | method | `lom` — ableton_lom call app view hide_view [args] |  |
| `is_view_visible` | method | `lom` — ableton_lom call app view is_view_visible [args] |  |
| `scroll_view` | method | `lom` — ableton_lom call `app view` scroll_view [direction, "Arranger", modifier] |  |
| `show_view` | method | `lom` — ableton_lom call `app view` show_view ["Detail/Clip"] | views: Browser, Arranger, Session, Detail, Detail/Clip, Detail/DeviceChain |
| `toggle_browse` | method | `lom` — ableton_lom call app view toggle_browse [args] |  |
| `zoom_view` | method | `lom` — ableton_lom call `app view` zoom_view [direction, "Arranger", modifier] |  |

## Application.ControlSurfaceProxy

Path example: `app control_surfaces 0` · 12 members (+ 9 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `control_descriptions` | ? | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `enable_receive_midi` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `fetch_received_midi_messages` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `fetch_received_values` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `grab_control` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `pad_layout` | ? | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `release_control` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `send_midi` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `send_value` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `subscribe_to_control` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `type_name` | property~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |
| `unsubscribe_from_control` | method~ | `lom` — ableton_lom describe `app control_surfaces N` | AbletonOSC / KBotBridge proxies |

## Track

Path example: `tracks N` · 72 members (+ 138 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method | `na` — nested class Track.View — see its own section |  |
| `arm` | property (bool) | `osc` — /live/track/get/arm <track> · /live/track/set/arm <track> <v> · /live/track/start_listen/arm | kbot: ableton_track arm/disarm |
| `arrangement_clips` | property (Vector) | `osc` — /live/track/get/arrangement_clips/name\|length\|start_time <track> | kbot: ableton_structure arr_clips track=N (JSON read-back) |
| `available_input_routing_channels` | property (RoutingChannelVector) | `osc` — /live/track/get/available_input_routing_channels <track> |  |
| `available_input_routing_types` | property (RoutingTypeVector) | `osc` — /live/track/get/available_input_routing_types <track> |  |
| `available_output_routing_channels` | property (RoutingChannelVector) | `osc` — /live/track/get/available_output_routing_channels <track> |  |
| `available_output_routing_types` | property (RoutingTypeVector) | `osc` — /live/track/get/available_output_routing_types <track> |  |
| `back_to_arranger` | property (bool) | `lom` — ableton_lom get tracks N back_to_arranger · set tracks N back_to_arranger <json> |  |
| `can_be_armed` | property (bool) | `osc` — /live/track/get/can_be_armed <track> · /live/track/start_listen/can_be_armed |  |
| `can_be_frozen` | property (bool) | `ui` — read-only flag; Freeze via Track context menu > Freeze Track; Flatten via context menu > Flatten | UI automation (peekaboo) — Plane D |
| `can_show_chains` | property (bool) | `lom` — ableton_lom get tracks N can_show_chains (read-only) |  |
| `canonical_parent` | property (Song) | `lom` — ableton_lom get tracks N canonical_parent (read-only) |  |
| `clip_slots` | property (Vector) | `osc` — /live/track/get/clips/name\|length\|color <track> · /live/track/delete_clip <track> <slot> | kbot: ableton_clip list; slot-level ops under ClipSlot |
| `color` | property (int) | `osc` — /live/track/get/color <track> · /live/track/set/color <track> <v> · /live/track/start_listen/color |  |
| `color_index` | property (int) | `osc` — /live/track/get/color_index <track> · /live/track/set/color_index <track> <v> · /live/track/start_listen/color_index | kbot: ableton_track color |
| `create_audio_clip` | method | `lom` — ableton_lom call `tracks N` create_audio_clip ["/abs/file.wav", start_beats] | arrangement audio clip from a file path (12.4 LOM) |
| `create_midi_clip` | method | `tool` — ableton_structure arr_create_clip track=N start=<beats> length=<beats> | arrangement MIDI clip; read-back = arr_clips. Replaces the ClipSlot-only path |
| `create_take_lane` | method | `lom` — ableton_lom call `tracks N` create_take_lane |  |
| `current_input_routing` | property (str) | `lom` — ableton_lom get tracks N current_input_routing · set tracks N current_input_routing <json> |  |
| `current_input_sub_routing` | property (str) | `lom` — ableton_lom get tracks N current_input_sub_routing · set tracks N current_input_sub_routing <json> |  |
| `current_monitoring_state` | property (int) | `osc` — /live/track/get/current_monitoring_state <track> · /live/track/set/current_monitoring_state <track> <v> · /live/track/start_listen/current_monitoring_state | kbot: ableton_track monitoring |
| `current_output_routing` | property (str) | `lom` — ableton_lom get tracks N current_output_routing · set tracks N current_output_routing <json> |  |
| `current_output_sub_routing` | property (str) | `lom` — ableton_lom get tracks N current_output_sub_routing · set tracks N current_output_sub_routing <json> |  |
| `delete_clip` | method | `osc` — /live/track/delete_clip <track> <slot> | kbot: ableton_clip delete |
| `delete_device` | method | `tool` — ableton_structure delete_device track=N device=M | also /live/track/delete_device <track> <device> |
| `devices` | property (Vector) | `osc` — /live/track/get/num_devices · /live/track/get/devices/name\|type\|class_name\|can_have_chains <track> | kbot: ableton_device list; per-device paths via ableton_lom `tracks N devices M` |
| `duplicate_clip_slot` | method | `lom` — ableton_lom call `tracks N` duplicate_clip_slot [slot] | or /live/clip_slot/duplicate_clip_to |
| `duplicate_clip_to_arrangement` | method | `tool` — ableton_structure arr_dup_from_session track=N slot=S time=<beats> | read-back = arr_clips |
| `duplicate_device` | method | `lom` — ableton_lom call tracks N duplicate_device [args] |  |
| `fired_slot_index` | property (int) | `osc` — /live/track/get/fired_slot_index <track> · /live/track/start_listen/fired_slot_index |  |
| `fold_state` | property (getter raised on the dumped instance) | `osc` — /live/track/get/fold_state <track> · /live/track/set/fold_state <track> <v> · /live/track/start_listen/fold_state |  |
| `get_data` | method | `lom` — ableton_lom call `tracks N` get_data ["key", default] |  |
| `group_track` | property (NoneType) | `lom` — ableton_lom get tracks N group_track · set tracks N group_track <json> |  |
| `has_audio_input` | property (bool) | `osc` — /live/track/get/has_audio_input <track> · /live/track/start_listen/has_audio_input |  |
| `has_audio_output` | property (bool) | `osc` — /live/track/get/has_audio_output <track> · /live/track/start_listen/has_audio_output |  |
| `has_midi_input` | property (bool) | `osc` — /live/track/get/has_midi_input <track> · /live/track/start_listen/has_midi_input |  |
| `has_midi_output` | property (bool) | `osc` — /live/track/get/has_midi_output <track> · /live/track/start_listen/has_midi_output |  |
| `implicit_arm` | property (bool) | `lom` — ableton_lom get tracks N implicit_arm · set tracks N implicit_arm <json> |  |
| `input_meter_left` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N input_meter_left · set tracks N input_meter_left <json> |  |
| `input_meter_level` | property (float) | `lom` — ableton_lom get tracks N input_meter_level · set tracks N input_meter_level <json> |  |
| `input_meter_right` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N input_meter_right · set tracks N input_meter_right <json> |  |
| `input_routing_channel` | property (RoutingChannel) | `osc` — /live/track/get/input_routing_channel <track> · /live/track/set/input_routing_channel <track> <name> | kbot: ableton_track input_routing |
| `input_routing_type` | property (RoutingType) | `osc` — /live/track/get/input_routing_type <track> · /live/track/set/input_routing_type <track> <name> | kbot: ableton_track input_routing |
| `input_routings` | property (StringVector) | `lom` — ableton_lom get tracks N input_routings · set tracks N input_routings <json> |  |
| `input_sub_routings` | property (StringVector) | `lom` — ableton_lom get tracks N input_sub_routings · set tracks N input_sub_routings <json> |  |
| `insert_device` | method | `tool` — ableton_browser insert_device track=N name=<device> [position=P] | handler tries Track.insert_device(name) (12.4 LOM method) and falls back to select track + Browser.load_item; read-back = device list. Or ableton_lom call `tracks N` insert_device ["Operator"] |
| `is_foldable` | property (bool) | `osc` — /live/track/get/is_foldable <track> · /live/track/start_listen/is_foldable |  |
| `is_frozen` | property (bool) | `ui` — Track context menu > Freeze Track (read state: ableton_lom get `tracks N` is_frozen) | the LOM exposes is_frozen/can_be_frozen as read-only; no freeze/flatten method exists in 12.4.5b5 |
| `is_grouped` | property (bool) | `osc` — /live/track/get/is_grouped <track> · /live/track/start_listen/is_grouped |  |
| `is_part_of_selection` | property (bool) | `lom` — ableton_lom get tracks N is_part_of_selection · set tracks N is_part_of_selection <json> |  |
| `is_showing_chains` | property (bool) | `lom` — ableton_lom get tracks N is_showing_chains · set tracks N is_showing_chains <json> |  |
| `is_visible` | property (bool) | `osc` — /live/track/get/is_visible <track> · /live/track/start_listen/is_visible |  |
| `jump_in_running_session_clip` | method | `lom` — ableton_lom call tracks N jump_in_running_session_clip [args] |  |
| `mixer_device` | property (MixerDevice) | `lom` — ableton_lom describe `tracks N mixer_device` | volume/panning/sends/track_activator/crossfade_assign |
| `monitoring_states` | method | `lom` — ableton_lom call tracks N monitoring_states [args] |  |
| `mute` | property (bool) | `osc` — /live/track/get/mute <track> · /live/track/set/mute <track> <v> · /live/track/start_listen/mute | kbot: ableton_track mute/unmute |
| `muted_via_solo` | property (bool) | `lom` — ableton_lom get tracks N muted_via_solo · set tracks N muted_via_solo <json> |  |
| `name` | property (str) | `osc` — /live/track/get/name <track> · /live/track/set/name <track> <v> · /live/track/start_listen/name | kbot: ableton_track rename |
| `output_meter_left` | property (getter raised on the dumped instance) | `osc` — /live/track/get/output_meter_left <track> · /live/track/start_listen/output_meter_left | kbot: ableton_audio_analysis |
| `output_meter_level` | property (float) | `osc` — /live/track/get/output_meter_level <track> · /live/track/start_listen/output_meter_level |  |
| `output_meter_right` | property (getter raised on the dumped instance) | `osc` — /live/track/get/output_meter_right <track> · /live/track/start_listen/output_meter_right | kbot: ableton_audio_analysis |
| `output_routing_channel` | property (RoutingChannel) | `osc` — /live/track/get/output_routing_channel <track> · /live/track/set/output_routing_channel <track> <name> | kbot: ableton_track output_routing |
| `output_routing_type` | property (RoutingType) | `osc` — /live/track/get/output_routing_type <track> · /live/track/set/output_routing_type <track> <name> | kbot: ableton_track output_routing |
| `output_routings` | property (StringVector) | `lom` — ableton_lom get tracks N output_routings · set tracks N output_routings <json> |  |
| `output_sub_routings` | property (StringVector) | `lom` — ableton_lom get tracks N output_sub_routings · set tracks N output_sub_routings <json> |  |
| `performance_impact` | property (float) | `lom` — ableton_lom get tracks N performance_impact · set tracks N performance_impact <json> |  |
| `playing_slot_index` | property (int) | `osc` — /live/track/get/playing_slot_index <track> · /live/track/start_listen/playing_slot_index |  |
| `set_data` | method | `lom` — ableton_lom call `tracks N` set_data ["key", value] |  |
| `solo` | property (bool) | `osc` — /live/track/get/solo <track> · /live/track/set/solo <track> <v> · /live/track/start_listen/solo | kbot: ableton_track solo/unsolo |
| `stop_all_clips` | method | `osc` — /live/track/stop_all_clips <track> |  |
| `take_lanes` | property (Vector) | `lom` — ableton_lom children `tracks N` → take_lanes (TakeLane: name, clips ...) |  |
| `view` | property (View) | `lom` — ableton_lom get tracks N view · set tracks N view <json> |  |

## Track.View

Path example: `tracks N view` · 5 members (+ 9 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Track) | `lom` — ableton_lom get tracks N view canonical_parent (read-only) |  |
| `device_insert_mode` | property (bool) | `lom` — ableton_lom get tracks N view device_insert_mode · set tracks N view device_insert_mode <json> |  |
| `is_collapsed` | property (bool) | `lom` — ableton_lom get tracks N view is_collapsed · set tracks N view is_collapsed <json> |  |
| `select_instrument` | method | `lom` — ableton_lom call tracks N view select_instrument [args] |  |
| `selected_device` | property (NoneType) | `osc` — /live/view/get/selected_device · /live/view/set/selected_device <track> <device> | kbot: ableton_view device |

## MixerDevice

Path example: `tracks N mixer_device` · 14 members (+ 9 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Track) | `lom` — ableton_lom get tracks N mixer_device canonical_parent (read-only) |  |
| `crossfade_assign` | property (int) | `lom` — ableton_lom get tracks N mixer_device crossfade_assign · set tracks N mixer_device crossfade_assign <json> |  |
| `crossfade_assignments` | method | `lom` — ableton_lom call tracks N mixer_device crossfade_assignments [args] |  |
| `crossfader` | property (getter raised on the dumped instance) | `lom` — ableton_lom get `master_track mixer_device crossfader` value | master track only (getter raises elsewhere) |
| `cue_volume` | property (getter raised on the dumped instance) | `lom` — ableton_lom get `master_track mixer_device cue_volume` value | master track only |
| `left_split_stereo` | property (DeviceParameter) | `lom` — ableton_lom get tracks N mixer_device left_split_stereo · set tracks N mixer_device left_split_stereo <json> |  |
| `panning` | property (DeviceParameter) | `osc` — /live/track/get/panning <track> · /live/track/set/panning <track> <-1..1> | kbot: ableton_track pan |
| `panning_mode` | property (int) | `lom` — ableton_lom get tracks N mixer_device panning_mode · set tracks N mixer_device panning_mode <json> |  |
| `panning_modes` | method | `lom` — ableton_lom call tracks N mixer_device panning_modes [args] |  |
| `right_split_stereo` | property (DeviceParameter) | `lom` — ableton_lom get tracks N mixer_device right_split_stereo · set tracks N mixer_device right_split_stereo <json> |  |
| `sends` | property (Vector) | `osc` — /live/track/get/send <track> <send> · /live/track/set/send <track> <send> <0..1> | kbot: ableton_mixer send |
| `song_tempo` | property (getter raised on the dumped instance) | `lom` — ableton_lom get `master_track mixer_device song_tempo` value | master track only |
| `track_activator` | property (DeviceParameter) | `lom` — ableton_lom get tracks N mixer_device track_activator · set tracks N mixer_device track_activator <json> |  |
| `volume` | property (DeviceParameter) | `osc` — /live/track/get/volume <track> · /live/track/set/volume <track> <0..1> · /live/track/start_listen/volume | kbot: ableton_track volume / ableton_mixer. Master track: ableton_lom get `master_track mixer_device volume` value (no /live/master/* address exists) |

## ChainMixerDevice

Path example: `tracks N devices M chains 0 mixer_device` · 5 members (+ 3 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M chains 0 mixer_device canonical_parent (read-only) |  |
| `chain_activator` | ? | `lom` — ableton_lom describe tracks N devices M chains 0 mixer_device → then get/set or call chain_activator |  |
| `panning` | property (DeviceParameter)~ | `lom` — ableton_lom get tracks N devices M chains 0 mixer_device panning · set tracks N devices M chains 0 mixer_device panning <json> |  |
| `sends` | property (Vector)~ | `lom` — ableton_lom get tracks N devices M chains 0 mixer_device sends · set tracks N devices M chains 0 mixer_device sends <json> |  |
| `volume` | property (DeviceParameter)~ | `lom` — ableton_lom get tracks N devices M chains 0 mixer_device volume · set tracks N devices M chains 0 mixer_device volume <json> |  |

## ClipSlot

Path example: `tracks N clip_slots S` · 20 members (+ 21 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Track) | `lom` — ableton_lom get tracks N clip_slots S canonical_parent (read-only) |  |
| `clip` | property (Clip) | `lom` — ableton_lom get tracks N clip_slots S clip · set tracks N clip_slots S clip <json> |  |
| `color` | property (NoneType) | `lom` — ableton_lom get tracks N clip_slots S color · set tracks N clip_slots S color <json> |  |
| `color_index` | property (NoneType) | `lom` — ableton_lom get tracks N clip_slots S color_index · set tracks N clip_slots S color_index <json> |  |
| `controls_other_clips` | property (bool) | `osc` — /live/clip_slot/get/controls_other_clips <track> <slot> · /live/clip_slot/start_listen/controls_other_clips |  |
| `create_audio_clip` | method | `lom` — ableton_lom call tracks N clip_slots S create_audio_clip [args] |  |
| `create_clip` | method | `osc` — /live/clip_slot/create_clip <track> <slot> <length_beats> | kbot: ableton_clip create (now read-back gated). Verified 2026-08-18: works |
| `delete_clip` | method | `osc` — /live/clip_slot/delete_clip <track> <slot> | kbot: ableton_clip delete |
| `duplicate_clip_to` | method | `osc` — /live/clip_slot/duplicate_clip_to <track> <slot> <dst_track> <dst_slot> | kbot: ableton_clip duplicate |
| `fire` | method | `osc` — /live/clip_slot/fire <track> <slot> | kbot: ableton_clip fire |
| `has_clip` | property (bool) | `osc` — /live/clip_slot/get/has_clip <track> <slot> · /live/clip_slot/start_listen/has_clip | kbot: ableton_clip info |
| `has_stop_button` | property (bool) | `osc` — /live/clip_slot/get/has_stop_button · /live/clip_slot/set/has_stop_button <track> <slot> <0\|1> |  |
| `is_group_slot` | property (bool) | `osc` — /live/clip_slot/get/is_group_slot <track> <slot> · /live/clip_slot/start_listen/is_group_slot |  |
| `is_playing` | property (bool) | `osc` — /live/clip_slot/get/is_playing <track> <slot> · /live/clip_slot/start_listen/is_playing |  |
| `is_recording` | property (bool) | `lom` — ableton_lom get tracks N clip_slots S is_recording · set tracks N clip_slots S is_recording <json> |  |
| `is_triggered` | property (bool) | `osc` — /live/clip_slot/get/is_triggered <track> <slot> · /live/clip_slot/start_listen/is_triggered |  |
| `playing_status` | property (ClipSlotPlayingState) | `osc` — /live/clip_slot/get/playing_status <track> <slot> · /live/clip_slot/start_listen/playing_status |  |
| `set_fire_button_state` | method | `lom` — ableton_lom call tracks N clip_slots S set_fire_button_state [args] |  |
| `stop` | method | `osc` — /live/clip_slot/stop <track> <slot> | kbot: ableton_clip stop |
| `will_record_on_start` | property (bool) | `osc` — /live/clip_slot/get/will_record_on_start <track> <slot> · /live/clip_slot/start_listen/will_record_on_start |  |

## Clip

Path example: `tracks N clip_slots S clip` · 88 members (+ 102 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method | `na` — nested class Clip.View — see its own section |  |
| `add_new_notes` | method | `osc` — /live/clip/add/notes <track> <slot> pitch start dur vel mute ... | kbot: ableton_midi add (stock OSC); ableton_structure clip_notes op=add track=N slot=S value=<json notes> calls the same member with JSON read-back. Both verified 2026-08-18 |
| `add_warp_marker` | method | `lom` — ableton_lom call tracks N clip_slots S clip add_warp_marker [args] |  |
| `apply_note_modifications` | method | `lom` — ableton_lom call tracks N clip_slots S clip apply_note_modifications [args] |  |
| `automation_envelope` | method | `tool` — ableton_structure automation path=<clip path> param_path=<param path> value=<points> (read side of the same handler) | read side of the same handler |
| `automation_envelopes` | property (Vector) | `lom` — ableton_lom get tracks N clip_slots S clip automation_envelopes · set tracks N clip_slots S clip automation_envelopes <json> |  |
| `available_warp_modes` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N clip_slots S clip available_warp_modes · set tracks N clip_slots S clip available_warp_modes <json> |  |
| `beat_to_sample_time` | method | `lom` — ableton_lom call tracks N clip_slots S clip beat_to_sample_time [args] |  |
| `canonical_parent` | property (ClipSlot) | `lom` — ableton_lom get tracks N clip_slots S clip canonical_parent (read-only) |  |
| `clear_all_envelopes` | method | `lom` — ableton_lom call <clip path> clear_all_envelopes |  |
| `clear_envelope` | method | `lom` — ableton_lom call <clip path> clear_envelope [{"_path":"<param path>"}] | verified 2026-08-18 (result null). No typed handler clears an envelope: ableton_structure automation with an empty point list creates the envelope if missing and writes nothing -- it does NOT clear |
| `color` | property (int) | `osc` — /live/clip/get/color <track> <slot> · /live/clip/set/color <track> <slot> <v> |  |
| `color_index` | property (int) | `osc` — /live/clip/get/color_index <track> <slot> · /live/clip/set/color_index <track> <slot> <v> |  |
| `create_automation_envelope` | method | `tool` — ableton_structure automation path=<clip path> param_path=<param path> value=[[time,len,value]...] | creates the envelope on demand, then insert_step; read-back = envelope value_at_time at each step midpoint, values in the parameter's own units (verified 2026-08-18) |
| `crop` | method | `lom` — ableton_lom call tracks N clip_slots S clip crop [args] |  |
| `deselect_all_notes` | method | `lom` — ableton_lom call tracks N clip_slots S clip deselect_all_notes [args] |  |
| `duplicate_loop` | method | `osc` — /live/clip/duplicate_loop <track> <slot> |  |
| `duplicate_notes_by_id` | method | `lom` — ableton_lom call tracks N clip_slots S clip duplicate_notes_by_id [args] |  |
| `duplicate_region` | method | `lom` — ableton_lom call tracks N clip_slots S clip duplicate_region [args] |  |
| `end_marker` | property (float) | `osc` — /live/clip/get/end_marker <track> <slot> · /live/clip/set/end_marker <track> <slot> <v> |  |
| `end_time` | property (float) | `osc` — /live/clip/get/end_time <track> <slot> · /live/clip/start_listen/end_time |  |
| `file_path` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/file_path <track> <slot> · /live/clip/start_listen/file_path |  |
| `fire` | method | `osc` — /live/clip/fire <track> <slot> | kbot: ableton_clip fire |
| `gain` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/gain <track> <slot> · /live/clip/set/gain <track> <slot> <v> |  |
| `gain_display_string` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/gain_display_string <track> <slot> · /live/clip/start_listen/gain_display_string |  |
| `get_all_notes_extended` | method | `tool` — ableton_structure clip_notes op=get track=N slot=S | returns [{pitch,start,duration,velocity,mute,probability,velocity_deviation,release_velocity,note_id}]; raw handler /live/kbot/clip/notes/get also takes a <clip path> (verified on a session clip 2026-08-18) |
| `get_notes` | method | `lom` — ableton_lom call tracks N clip_slots S clip get_notes [args] |  |
| `get_notes_by_id` | method | `lom` — ableton_lom call tracks N clip_slots S clip get_notes_by_id [args] |  |
| `get_notes_extended` | method | `osc` — /live/clip/get/notes <track> <slot> [pitch_from pitch_count time_from time_count] | kbot: ableton_midi read (session clip). clip_notes op=get uses get_all_notes_extended and falls back to this. Verified 2026-08-18: read-back exact |
| `get_selected_notes` | method | `lom` — ableton_lom call tracks N clip_slots S clip get_selected_notes [args] |  |
| `get_selected_notes_extended` | method | `lom` — ableton_lom call tracks N clip_slots S clip get_selected_notes_extended [args] |  |
| `groove` | property (Groove) | `lom` — ableton_lom get tracks N clip_slots S clip groove · set tracks N clip_slots S clip groove <json> |  |
| `has_envelopes` | property (bool) | `lom` — ableton_lom get tracks N clip_slots S clip has_envelopes (read-only) |  |
| `has_groove` | property (bool) | `osc` — /live/clip/get/has_groove <track> <slot> · /live/clip/start_listen/has_groove |  |
| `is_arrangement_clip` | property (bool) | `lom` — ableton_lom get tracks N clip_slots S clip is_arrangement_clip · set tracks N clip_slots S clip is_arrangement_clip <json> |  |
| `is_audio_clip` | property (bool) | `osc` — /live/clip/get/is_audio_clip <track> <slot> · /live/clip/start_listen/is_audio_clip |  |
| `is_midi_clip` | property (bool) | `osc` — /live/clip/get/is_midi_clip <track> <slot> · /live/clip/start_listen/is_midi_clip |  |
| `is_overdubbing` | property (bool) | `osc` — /live/clip/get/is_overdubbing <track> <slot> · /live/clip/start_listen/is_overdubbing |  |
| `is_playing` | property (bool) | `osc` — /live/clip/get/is_playing <track> <slot> · /live/clip/start_listen/is_playing |  |
| `is_recording` | property (bool) | `osc` — /live/clip/get/is_recording <track> <slot> · /live/clip/start_listen/is_recording |  |
| `is_session_clip` | property (bool) | `lom` — ableton_lom get tracks N clip_slots S clip is_session_clip · set tracks N clip_slots S clip is_session_clip <json> |  |
| `is_take_lane_clip` | property (bool) | `lom` — ableton_lom get tracks N clip_slots S clip is_take_lane_clip · set tracks N clip_slots S clip is_take_lane_clip <json> |  |
| `is_triggered` | property (bool) | `osc` — /live/clip/get/is_triggered <track> <slot> · /live/clip/start_listen/is_triggered |  |
| `launch_mode` | property (int) | `osc` — /live/clip/get/launch_mode <track> <slot> · /live/clip/set/launch_mode <track> <slot> <v> |  |
| `launch_quantization` | property (int) | `osc` — /live/clip/get/launch_quantization <track> <slot> · /live/clip/set/launch_quantization <track> <slot> <v> |  |
| `legato` | property (bool) | `osc` — /live/clip/get/legato <track> <slot> · /live/clip/set/legato <track> <slot> <v> |  |
| `length` | property (float) | `osc` — /live/clip/get/length <track> <slot> · /live/clip/start_listen/length | kbot: ableton_clip info |
| `loop_end` | property (float) | `osc` — /live/clip/get/loop_end <track> <slot> · /live/clip/set/loop_end <track> <slot> <v> |  |
| `loop_start` | property (float) | `osc` — /live/clip/get/loop_start <track> <slot> · /live/clip/set/loop_start <track> <slot> <v> |  |
| `looping` | property (bool) | `osc` — /live/clip/get/looping <track> <slot> · /live/clip/set/looping <track> <slot> <v> | kbot: ableton_clip info/set |
| `move_playing_pos` | method | `lom` — ableton_lom call tracks N clip_slots S clip move_playing_pos [args] |  |
| `move_warp_marker` | method | `lom` — ableton_lom call tracks N clip_slots S clip move_warp_marker [args] |  |
| `muted` | property (bool) | `osc` — /live/clip/get/muted <track> <slot> · /live/clip/set/muted <track> <slot> <v> |  |
| `name` | property (str) | `osc` — /live/clip/get/name <track> <slot> · /live/clip/set/name <track> <slot> <v> | kbot: ableton_clip info/set name |
| `note_number_to_name` | method | `lom` — ableton_lom call tracks N clip_slots S clip note_number_to_name [args] |  |
| `pitch_coarse` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/pitch_coarse <track> <slot> · /live/clip/set/pitch_coarse <track> <slot> <v> |  |
| `pitch_fine` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/pitch_fine <track> <slot> · /live/clip/set/pitch_fine <track> <slot> <v> |  |
| `playing_position` | property (float) | `osc` — /live/clip/get/playing_position <track> <slot> · /live/clip/start_listen/playing_position |  |
| `position` | property (float) | `osc` — /live/clip/get/position <track> <slot> · /live/clip/set/position <track> <slot> <v> |  |
| `quantize` | method | `tool` — ableton_structure quantize track=N slot=S grid=<1/16\|1/8\|1/4\|1/2\|bar\|g_* name> amount=0..1 | quantization grid is a Clip.GridQuantization int (g_bar=4 g_half=5 g_quarter=6 g_eighth=7 g_sixteenth=8, measured); read-back = note count |
| `quantize_pitch` | method | `lom` — ableton_lom call tracks N clip_slots S clip quantize_pitch [args] |  |
| `ram_mode` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/ram_mode <track> <slot> · /live/clip/set/ram_mode <track> <slot> <v> |  |
| `remove_notes` | method | `lom` — ableton_lom call tracks N clip_slots S clip remove_notes [args] |  |
| `remove_notes_by_id` | method | `osc` — /live/clip/remove_notes_by_id <track> <slot> |  |
| `remove_notes_extended` | method | `osc` — /live/clip/remove/notes <track> <slot> [pitch_from pitch_count time_from time_count] | kbot: ableton_midi clear (stock OSC); ableton_structure clip_notes op=remove track=N slot=S [value={pitch,pitch_span,start,time_span}] calls the same member (no value = remove all, read-back = remaining notes). Verified 2026-08-18 |
| `remove_warp_marker` | method | `lom` — ableton_lom call tracks N clip_slots S clip remove_warp_marker [args] |  |
| `replace_selected_notes` | method | `lom` — ableton_lom call tracks N clip_slots S clip replace_selected_notes [args] |  |
| `sample_length` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/sample_length <track> <slot> · /live/clip/start_listen/sample_length |  |
| `sample_rate` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N clip_slots S clip sample_rate · set tracks N clip_slots S clip sample_rate <json> |  |
| `sample_to_beat_time` | method | `lom` — ableton_lom call tracks N clip_slots S clip sample_to_beat_time [args] |  |
| `scrub` | method | `lom` — ableton_lom call tracks N clip_slots S clip scrub [args] |  |
| `seconds_to_sample_time` | method | `lom` — ableton_lom call tracks N clip_slots S clip seconds_to_sample_time [args] |  |
| `select_all_notes` | method | `lom` — ableton_lom call tracks N clip_slots S clip select_all_notes [args] |  |
| `select_notes_by_id` | method | `lom` — ableton_lom call tracks N clip_slots S clip select_notes_by_id [args] |  |
| `set_fire_button_state` | method | `lom` — ableton_lom call tracks N clip_slots S clip set_fire_button_state [args] |  |
| `set_notes` | method | `lom` — ableton_lom call <clip path> set_notes [...] (deprecated Live API) | ableton_structure clip_notes op=set replaces all notes with remove_notes_extended + add_new_notes and does not call this member |
| `signature_denominator` | property (int) | `lom` — ableton_lom get tracks N clip_slots S clip signature_denominator · set tracks N clip_slots S clip signature_denominator <json> |  |
| `signature_numerator` | property (int) | `lom` — ableton_lom get tracks N clip_slots S clip signature_numerator · set tracks N clip_slots S clip signature_numerator <json> |  |
| `start_marker` | property (float) | `osc` — /live/clip/get/start_marker <track> <slot> · /live/clip/set/start_marker <track> <slot> <v> |  |
| `start_time` | property (float) | `osc` — /live/clip/get/start_time <track> <slot> · /live/clip/start_listen/start_time |  |
| `stop` | method | `osc` — /live/clip/stop <track> <slot> | kbot: ableton_clip stop |
| `stop_scrub` | method | `lom` — ableton_lom call tracks N clip_slots S clip stop_scrub [args] |  |
| `velocity_amount` | property (float) | `osc` — /live/clip/get/velocity_amount <track> <slot> · /live/clip/set/velocity_amount <track> <slot> <v> |  |
| `view` | property (View) | `lom` — ableton_lom get tracks N clip_slots S clip view · set tracks N clip_slots S clip view <json> |  |
| `warp_markers` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N clip_slots S clip warp_markers · set tracks N clip_slots S clip warp_markers <json> |  |
| `warp_mode` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/warp_mode <track> <slot> · /live/clip/set/warp_mode <track> <slot> <v> |  |
| `warping` | property (getter raised on the dumped instance) | `osc` — /live/clip/get/warping <track> <slot> · /live/clip/set/warping <track> <slot> <v> |  |
| `will_record_on_start` | property (bool) | `osc` — /live/clip/get/will_record_on_start <track> <slot> · /live/clip/start_listen/will_record_on_start |  |

## Clip.View

Path example: `tracks N clip_slots S clip view` · 7 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Clip) | `lom` — ableton_lom get tracks N clip_slots S clip view canonical_parent (read-only) |  |
| `grid_is_triplet` | property (bool) | `lom` — ableton_lom get tracks N clip_slots S clip view grid_is_triplet · set tracks N clip_slots S clip view grid_is_triplet <json> |  |
| `grid_quantization` | property (GridQuantization) | `lom` — ableton_lom get tracks N clip_slots S clip view grid_quantization · set tracks N clip_slots S clip view grid_quantization <json> |  |
| `hide_envelope` | method | `lom` — ableton_lom call tracks N clip_slots S clip view hide_envelope [args] |  |
| `select_envelope_parameter` | method | `lom` — ableton_lom call tracks N clip_slots S clip view select_envelope_parameter [args] |  |
| `show_envelope` | method | `lom` — ableton_lom call tracks N clip_slots S clip view show_envelope [args] |  |
| `show_loop` | method | `lom` — ableton_lom call tracks N clip_slots S clip view show_loop [args] |  |

## Scene

Path example: `scenes N` · 15 members (+ 30 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Song) | `lom` — ableton_lom get scenes N canonical_parent (read-only) |  |
| `clip_slots` | property (Vector) | `lom` — ableton_lom children `scenes N` → clip_slots; slot ops via ClipSlot |  |
| `color` | property (int) | `osc` — /live/scene/get/color <scene> · /live/scene/set/color <scene> <v> |  |
| `color_index` | property (NoneType) | `osc` — /live/scene/get/color_index <scene> · /live/scene/set/color_index <scene> <v> |  |
| `fire` | method | `osc` — /live/scene/fire <scene> | kbot: ableton_scene fire |
| `fire_as_selected` | method | `osc` — /live/scene/fire_as_selected <scene> · /live/scene/fire_selected |  |
| `is_empty` | property (bool) | `osc` — /live/scene/get/is_empty <scene> · /live/scene/start_listen/is_empty |  |
| `is_triggered` | property (bool) | `osc` — /live/scene/get/is_triggered <scene> · /live/scene/start_listen/is_triggered |  |
| `name` | property (str) | `osc` — /live/scene/get/name <scene> · /live/scene/set/name <scene> <v> | kbot: ableton_scene rename/list |
| `set_fire_button_state` | method | `lom` — ableton_lom call scenes N set_fire_button_state [args] |  |
| `tempo` | property (float) | `osc` — /live/scene/get/tempo <scene> · /live/scene/set/tempo <scene> <v> |  |
| `tempo_enabled` | property (bool) | `osc` — /live/scene/get/tempo_enabled <scene> · /live/scene/set/tempo_enabled <scene> <v> |  |
| `time_signature_denominator` | property (int) | `osc` — /live/scene/get/time_signature_denominator <scene> · /live/scene/set/time_signature_denominator <scene> <v> |  |
| `time_signature_enabled` | property (bool) | `osc` — /live/scene/get/time_signature_enabled <scene> · /live/scene/set/time_signature_enabled <scene> <v> |  |
| `time_signature_numerator` | property (int) | `osc` — /live/scene/get/time_signature_numerator <scene> · /live/scene/set/time_signature_numerator <scene> <v> |  |

## Device

Path example: `tracks N devices M` · 17 members (+ 18 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method | `na` — nested class Device.View — see its own section |  |
| `can_compare_ab` | property (bool) | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool) | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool) | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (Track) | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str) | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str) | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `is_active` | property (bool) | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool) | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float) | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int) | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str) | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector) | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `save_preset_to_compare_ab_slot` | method | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType) | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View) | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## Device.View

Path example: `tracks N devices M view` · 2 members (+ 3 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Device) | `lom` — ableton_lom get tracks N devices M view canonical_parent (read-only) |  |
| `is_collapsed` | property (bool) | `lom` — ableton_lom get tracks N devices M view is_collapsed · set tracks N devices M view is_collapsed <json> |  |

## DeviceParameter

Path example: `tracks N devices M parameters K` · 18 members (+ 15 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `automation_state` | property (int) | `lom` — ableton_lom get tracks N devices M parameters K automation_state · set tracks N devices M parameters K automation_state <json> |  |
| `begin_gesture` | method | `lom` — ableton_lom call tracks N devices M parameters K begin_gesture [args] |  |
| `canonical_parent` | property (MixerDevice) | `lom` — ableton_lom get tracks N devices M parameters K canonical_parent (read-only) |  |
| `default_value` | property (float) | `lom` — ableton_lom get tracks N devices M parameters K default_value · set tracks N devices M parameters K default_value <json> |  |
| `display_value` | property (float) | `lom` — ableton_lom get tracks N devices M parameters K display_value · set tracks N devices M parameters K display_value <json> |  |
| `end_gesture` | method | `lom` — ableton_lom call tracks N devices M parameters K end_gesture [args] |  |
| `is_enabled` | property (bool) | `lom` — ableton_lom get tracks N devices M parameters K is_enabled · set tracks N devices M parameters K is_enabled <json> |  |
| `is_quantized` | property (bool) | `osc` — /live/device/get/parameters/is_quantized <track> <device> |  |
| `max` | property (float) | `osc` — /live/device/get/parameters/max <track> <device> |  |
| `min` | property (float) | `osc` — /live/device/get/parameters/min <track> <device> |  |
| `name` | property (str) | `osc` — /live/device/get/parameter/name <track> <device> <param> | kbot: ableton_device params |
| `original_name` | property (str) | `lom` — ableton_lom get tracks N devices M parameters K original_name · set tracks N devices M parameters K original_name <json> |  |
| `re_enable_automation` | method | `lom` — ableton_lom call tracks N devices M parameters K re_enable_automation [args] |  |
| `short_value_items` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N devices M parameters K short_value_items · set tracks N devices M parameters K short_value_items <json> |  |
| `state` | property (int) | `lom` — ableton_lom get tracks N devices M parameters K state · set tracks N devices M parameters K state <json> |  |
| `str_for_value` | method | `osc` — /live/device/get/parameter/value_string <track> <device> <param> |  |
| `value` | property (float) | `osc` — /live/device/get/parameter/value <track> <device> <param> · /live/device/set/parameter/value <track> <device> <param> <v> · /live/device/start_listen/parameter/value | kbot: ableton_device set; ableton_lom set <param path> value <v> for chains/racks/mixer params |
| `value_items` | property (getter raised on the dumped instance) | `lom` — ableton_lom get tracks N devices M parameters K value_items · set tracks N devices M parameters K value_items <json> |  |

## RackDevice

Path example: `tracks N devices M` · 39 members (+ 48 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class RackDevice.View — see its own section |  |
| `add_macro` | method~ | `tool` — ableton_structure add_macro path=<rack path> | read-back = visible_macro_count (Live adds macros in pairs: 8 -> 10, measured) |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `can_show_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_show_chains (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `chain_selector` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call chain_selector |  |
| `chains` | ? | `tool` — ableton_structure insert_chain (read-back) · ableton_lom children <rack path> |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `copy_pad` | method~ | `lom` — ableton_lom call tracks N devices M copy_pad [args] |  |
| `delete_selected_variation` | method~ | `lom` — ableton_lom call tracks N devices M delete_selected_variation [args] |  |
| `drum_pads` | property~ | `tool` — ableton_structure build_pad (read-back) · ableton_lom children <rack path> | 128 pads, index = MIDI note |
| `has_drum_pads` | property~ | `lom` — ableton_lom get tracks N devices M has_drum_pads (read-only) |  |
| `has_macro_mappings` | property~ | `lom` — ableton_lom get tracks N devices M has_macro_mappings (read-only) |  |
| `insert_chain` | method~ | `tool` — ableton_structure insert_chain path=<rack path> [name=...] | read-back = chain list |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_showing_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_showing_chains · set tracks N devices M is_showing_chains <json> |  |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `macros_mapped` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call macros_mapped |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `tool` — ableton_structure macros path=<rack path> [value=<json>] (get when value omitted, set otherwise) | Macro 1..16 are the rack's DeviceParameters; other rack params via ableton_lom |
| `randomize_macros` | method~ | `lom` — ableton_lom call tracks N devices M randomize_macros [args] |  |
| `recall_last_used_variation` | method~ | `lom` — ableton_lom call tracks N devices M recall_last_used_variation [args] |  |
| `recall_selected_variation` | method~ | `lom` — ableton_lom call tracks N devices M recall_selected_variation [args] |  |
| `remove_macro` | method~ | `lom` — ableton_lom call <rack path> remove_macro [] | no typed handler removes macros (add_macro only adds) |
| `return_chains` | property~ | `lom` — ableton_lom get tracks N devices M return_chains · set tracks N devices M return_chains <json> |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `selected_variation_index` | property~ | `lom` — ableton_lom get tracks N devices M selected_variation_index · set tracks N devices M selected_variation_index <json> |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `store_variation` | method~ | `lom` — ableton_lom call tracks N devices M store_variation [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `variation_count` | property~ | `lom` — ableton_lom get tracks N devices M variation_count · set tracks N devices M variation_count <json> |  |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |
| `visible_drum_pads` | property~ | `lom` — ableton_lom get tracks N devices M visible_drum_pads · set tracks N devices M visible_drum_pads <json> |  |
| `visible_macro_count` | property~ | `tool` — ableton_structure macros path=<rack path> (get) |  |

## Chain

Path example: `tracks N devices M chains C` · 17 members (+ 24 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M chains C canonical_parent (read-only) |  |
| `color` | property (int)~ | `lom` — ableton_lom get tracks N devices M chains C color · set tracks N devices M chains C color <json> |  |
| `color_index` | property (int)~ | `lom` — ableton_lom get tracks N devices M chains C color_index · set tracks N devices M chains C color_index <json> |  |
| `delete_device` | method~ | `lom` — ableton_lom call <chain path> delete_device [index] | the TS ableton_structure delete_device action takes an int track only; the raw handler /live/kbot/device/delete accepts a chain path as its first arg but that form was not exercised against Live |
| `devices` | property (Vector)~ | `lom` — ableton_lom get tracks N devices M chains C devices · set tracks N devices M chains C devices <json> |  |
| `duplicate_device` | method~ | `lom` — ableton_lom call tracks N devices M chains C duplicate_device [args] |  |
| `has_audio_input` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C has_audio_input (read-only) |  |
| `has_audio_output` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C has_audio_output (read-only) |  |
| `has_midi_input` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C has_midi_input (read-only) |  |
| `has_midi_output` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C has_midi_output (read-only) |  |
| `insert_device` | method~ | `tool` — ableton_browser load item=<device name> target=chain:<chain path> | handler tries chain.insert_device(name) first, falls back to select chain + browser.load_item (verified 2026-08-18: Compressor into a drum chain, method chain.insert_device) |
| `is_auto_colored` | property~ | `lom` — ableton_lom get tracks N devices M chains C is_auto_colored · set tracks N devices M chains C is_auto_colored <json> |  |
| `mixer_device` | property (MixerDevice)~ | `lom` — ableton_lom get tracks N devices M chains C mixer_device · set tracks N devices M chains C mixer_device <json> |  |
| `mute` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C mute · set tracks N devices M chains C mute <json> |  |
| `muted_via_solo` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C muted_via_solo · set tracks N devices M chains C muted_via_solo <json> |  |
| `name` | property (str)~ | `lom` — ableton_lom get tracks N devices M chains C name · set tracks N devices M chains C name <json> |  |
| `solo` | property (bool)~ | `lom` — ableton_lom get tracks N devices M chains C solo · set tracks N devices M chains C solo <json> |  |

## DrumPad

Path example: `tracks N devices M drum_pads 36` · 7 members (+ 12 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 canonical_parent (read-only) |  |
| `chains` | ? | `tool` — ableton_structure build_pad path=<rack path> note=N sample=<abs path> [name=...] (read-back) |  |
| `delete_all_chains` | method~ | `lom` — ableton_lom call tracks N devices M drum_pads 36 delete_all_chains [args] |  |
| `mute` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 mute · set tracks N devices M drum_pads 36 mute <json> |  |
| `name` | property (str)~ | `tool` — ableton_structure build_pad (read-back pad name) |  |
| `note` | ? | `lom` — ableton_lom describe tracks N devices M drum_pads 36 → then get/set or call note |  |
| `solo` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 solo · set tracks N devices M drum_pads 36 solo <json> |  |

## DrumChain

Path example: `tracks N devices M drum_pads 36 chains 0` · 20 members (+ 33 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 canonical_parent (read-only) |  |
| `choke_group` | property~ | `lom` — ableton_lom set <chain path> choke_group <n> |  |
| `color` | property (int)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 color · set tracks N devices M drum_pads 36 chains 0 color <json> |  |
| `color_index` | property (int)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 color_index · set tracks N devices M drum_pads 36 chains 0 color_index <json> |  |
| `delete_device` | method~ | `lom` — ableton_lom call <chain path> delete_device [index] | the TS ableton_structure delete_device action takes an int track only; the raw handler /live/kbot/device/delete accepts a chain path as its first arg but that form was not exercised against Live |
| `devices` | property (Vector)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 devices · set tracks N devices M drum_pads 36 chains 0 devices <json> |  |
| `duplicate_device` | method~ | `lom` — ableton_lom call tracks N devices M drum_pads 36 chains 0 duplicate_device [args] |  |
| `has_audio_input` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 has_audio_input (read-only) |  |
| `has_audio_output` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 has_audio_output (read-only) |  |
| `has_midi_input` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 has_midi_input (read-only) |  |
| `has_midi_output` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 has_midi_output (read-only) |  |
| `in_note` | ? | `tool` — ableton_structure build_pad path=<rack path> note=N sample=<abs path> [name=...] | build_pad = insert chain → Simpler → replace_sample → set in_note; also ableton_lom set <chain path> in_note <n> |
| `insert_device` | method~ | `tool` — ableton_browser load item=<device name> target=chain:<chain path> | handler tries chain.insert_device(name) first, falls back to select chain + browser.load_item (verified 2026-08-18: Compressor into a drum chain, method chain.insert_device) |
| `is_auto_colored` | property~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 is_auto_colored · set tracks N devices M drum_pads 36 chains 0 is_auto_colored <json> |  |
| `mixer_device` | property (MixerDevice)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 mixer_device · set tracks N devices M drum_pads 36 chains 0 mixer_device <json> |  |
| `mute` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 mute · set tracks N devices M drum_pads 36 chains 0 mute <json> |  |
| `muted_via_solo` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 muted_via_solo · set tracks N devices M drum_pads 36 chains 0 muted_via_solo <json> |  |
| `name` | property (str)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 name · set tracks N devices M drum_pads 36 chains 0 name <json> |  |
| `out_note` | ? | `lom` — ableton_lom set <chain path> out_note <n> |  |
| `solo` | property (bool)~ | `lom` — ableton_lom get tracks N devices M drum_pads 36 chains 0 solo · set tracks N devices M drum_pads 36 chains 0 solo <json> |  |

## SimplerDevice

Path example: `tracks N devices M` · 38 members (+ 60 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class SimplerDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `can_warp_as` | method~ | `lom` — ableton_lom call tracks N devices M can_warp_as [args] |  |
| `can_warp_double` | method~ | `lom` — ableton_lom call tracks N devices M can_warp_double [args] |  |
| `can_warp_half` | method~ | `lom` — ableton_lom call tracks N devices M can_warp_half [args] |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `crop` | method~ | `lom` — ableton_lom call tracks N devices M crop [args] |  |
| `guess_playback_length` | method~ | `lom` — ableton_lom call tracks N devices M guess_playback_length [args] |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `multi_sample_mode` | property~ | `lom` — ableton_lom get tracks N devices M multi_sample_mode · set tracks N devices M multi_sample_mode <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `note_pitch_bend_range` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call note_pitch_bend_range |  |
| `pad_slicing` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pad_slicing |  |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `pitch_bend_range` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pitch_bend_range |  |
| `playback_mode` | property~ | `lom` — ableton_lom get tracks N devices M playback_mode · set tracks N devices M playback_mode <json> |  |
| `playing_position` | property (float)~ | `lom` — ableton_lom get tracks N devices M playing_position · set tracks N devices M playing_position <json> |  |
| `playing_position_enabled` | property~ | `lom` — ableton_lom get tracks N devices M playing_position_enabled · set tracks N devices M playing_position_enabled <json> |  |
| `replace_sample` | method~ | `tool` — ableton_structure build_pad path=<rack path> note=N sample=<abs path> [name=...] | read-back = sample.file_path; standalone Simpler: ableton_lom call <device path> replace_sample ["/abs/path.wav"] |
| `retrigger` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call retrigger |  |
| `reverse` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call reverse |  |
| `sample` | ? | `tool` — ableton_structure build_pad (read-back file_path) · ableton_lom describe <device path> sample |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `slicing_playback_mode` | property~ | `lom` — ableton_lom get tracks N devices M slicing_playback_mode · set tracks N devices M slicing_playback_mode <json> |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |
| `voices` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call voices |  |
| `warp_as` | method~ | `lom` — ableton_lom call tracks N devices M warp_as [args] |  |
| `warp_double` | method~ | `lom` — ableton_lom call tracks N devices M warp_double [args] |  |
| `warp_half` | method~ | `lom` — ableton_lom call tracks N devices M warp_half [args] |  |

## Sample

Path example: `tracks N devices M sample` · 31 members (+ 60 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `beat_to_sample_time` | method~ | `lom` — ableton_lom call tracks N devices M sample beat_to_sample_time [args] |  |
| `beats_granulation_resolution` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call beats_granulation_resolution |  |
| `beats_transient_envelope` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call beats_transient_envelope |  |
| `beats_transient_loop_mode` | property~ | `lom` — ableton_lom get tracks N devices M sample beats_transient_loop_mode · set tracks N devices M sample beats_transient_loop_mode <json> |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M sample canonical_parent (read-only) |  |
| `clear_slices` | method~ | `lom` — ableton_lom call tracks N devices M sample clear_slices [args] |  |
| `complex_pro_envelope` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call complex_pro_envelope |  |
| `complex_pro_formants` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call complex_pro_formants |  |
| `end_marker` | property (float)~ | `lom` — ableton_lom get tracks N devices M sample end_marker · set tracks N devices M sample end_marker <json> |  |
| `file_path` | property (str)~ | `lom` — ableton_lom get tracks N devices M sample file_path · set tracks N devices M sample file_path <json> |  |
| `gain` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call gain |  |
| `gain_display_string` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call gain_display_string |  |
| `insert_slice` | method~ | `lom` — ableton_lom call tracks N devices M sample insert_slice [args] |  |
| `length` | property (float)~ | `lom` — ableton_lom get tracks N devices M sample length · set tracks N devices M sample length <json> |  |
| `move_slice` | method~ | `lom` — ableton_lom call tracks N devices M sample move_slice [args] |  |
| `remove_slice` | method~ | `lom` — ableton_lom call tracks N devices M sample remove_slice [args] |  |
| `reset_slices` | method~ | `lom` — ableton_lom call tracks N devices M sample reset_slices [args] |  |
| `sample_rate` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call sample_rate |  |
| `sample_to_beat_time` | method~ | `lom` — ableton_lom call tracks N devices M sample sample_to_beat_time [args] |  |
| `slices` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call slices |  |
| `slicing_beat_division` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call slicing_beat_division |  |
| `slicing_region_count` | property~ | `lom` — ableton_lom get tracks N devices M sample slicing_region_count · set tracks N devices M sample slicing_region_count <json> |  |
| `slicing_sensitivity` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call slicing_sensitivity |  |
| `slicing_style` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call slicing_style |  |
| `start_marker` | property (float)~ | `lom` — ableton_lom get tracks N devices M sample start_marker · set tracks N devices M sample start_marker <json> |  |
| `texture_flux` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call texture_flux |  |
| `texture_grain_size` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call texture_grain_size |  |
| `tones_grain_size` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call tones_grain_size |  |
| `warp_markers` | method~ | `lom` — ableton_lom call tracks N devices M sample warp_markers [args] |  |
| `warp_mode` | method~ | `lom` — ableton_lom call tracks N devices M sample warp_mode [args] |  |
| `warping` | ? | `lom` — ableton_lom describe tracks N devices M sample → then get/set or call warping |  |

## PluginDevice

Path example: `tracks N devices M` · 21 members (+ 27 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class PluginDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `get_parameter_names` | method~ | `osc` — /live/device/get/parameters/name <track> <device> · /live/device/configure_all (local edit: force-configure VST3 params) |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_editor_open` | property~ | `ui` — /live/device/show_gui <track> <device> (local edit) opens the floating window; interacting with the plugin GUI itself is UI automation (peekaboo) | the LOM cannot click inside a plugin window |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `presets` | ? | `tool` — ableton_browser presets track=N device=M | PluginDevice.presets when the device exposes them; non-plugin devices get presets:[] + reason (native presets are browser items: ableton_browser search) |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `selected_preset_index` | property~ | `tool` — ableton_browser load_preset track=N device=M preset=<index\|name> | read-back = selected_preset_index + name |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## MaxDevice

Path example: `tracks N devices M` · 25 members (+ 33 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class MaxDevice.View — see its own section |  |
| `audio_inputs` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call audio_inputs |  |
| `audio_outputs` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call audio_outputs |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `get_bank_count` | method~ | `lom` — ableton_lom call tracks N devices M get_bank_count [args] |  |
| `get_bank_name` | method~ | `lom` — ableton_lom call tracks N devices M get_bank_name [args] |  |
| `get_bank_parameters` | method~ | `lom` — ableton_lom call tracks N devices M get_bank_parameters [args] |  |
| `get_value_item_icons` | method~ | `lom` — ableton_lom call tracks N devices M get_value_item_icons [args] |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `midi_inputs` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call midi_inputs |  |
| `midi_outputs` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call midi_outputs |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## CompressorDevice

Path example: `tracks N devices M` · 21 members (+ 30 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class CompressorDevice.View — see its own section |  |
| `available_input_routing_channels` | property (RoutingChannelVector)~ | `lom` — ableton_lom get tracks N devices M available_input_routing_channels · set tracks N devices M available_input_routing_channels <json> |  |
| `available_input_routing_types` | property (RoutingTypeVector)~ | `lom` — ableton_lom get tracks N devices M available_input_routing_types · set tracks N devices M available_input_routing_types <json> |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `input_routing_channel` | property (RoutingChannel)~ | `lom` — ableton_lom get tracks N devices M input_routing_channel · set tracks N devices M input_routing_channel <json> |  |
| `input_routing_type` | property (RoutingType)~ | `lom` — ableton_lom get tracks N devices M input_routing_type · set tracks N devices M input_routing_type <json> |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## Eq8Device

Path example: `tracks N devices M` · 20 members (+ 27 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class Eq8Device.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `edit_mode` | property~ | `lom` — ableton_lom get tracks N devices M edit_mode · set tracks N devices M edit_mode <json> |  |
| `global_mode` | property~ | `lom` — ableton_lom get tracks N devices M global_mode · set tracks N devices M global_mode <json> |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `oversample` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call oversample |  |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## WavetableDevice

Path example: `tracks N devices M` · 37 members (+ 63 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class WavetableDevice.View — see its own section |  |
| `add_parameter_to_modulation_matrix` | method~ | `lom` — ableton_lom call tracks N devices M add_parameter_to_modulation_matrix [args] |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `filter_routing` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call filter_routing |  |
| `get_modulation_target_parameter_name` | method~ | `lom` — ableton_lom call tracks N devices M get_modulation_target_parameter_name [args] |  |
| `get_modulation_value` | method~ | `lom` — ableton_lom call tracks N devices M get_modulation_value [args] |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_parameter_modulatable` | property~ | `lom` — ableton_lom get tracks N devices M is_parameter_modulatable · set tracks N devices M is_parameter_modulatable <json> |  |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `mono_poly` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mono_poly |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `oscillator_1_effect_mode` | property~ | `lom` — ableton_lom get tracks N devices M oscillator_1_effect_mode · set tracks N devices M oscillator_1_effect_mode <json> |  |
| `oscillator_1_wavetable_category` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call oscillator_1_wavetable_category |  |
| `oscillator_1_wavetable_index` | property~ | `lom` — ableton_lom get tracks N devices M oscillator_1_wavetable_index · set tracks N devices M oscillator_1_wavetable_index <json> |  |
| `oscillator_1_wavetables` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call oscillator_1_wavetables |  |
| `oscillator_2_effect_mode` | property~ | `lom` — ableton_lom get tracks N devices M oscillator_2_effect_mode · set tracks N devices M oscillator_2_effect_mode <json> |  |
| `oscillator_2_wavetable_category` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call oscillator_2_wavetable_category |  |
| `oscillator_2_wavetable_index` | property~ | `lom` — ableton_lom get tracks N devices M oscillator_2_wavetable_index · set tracks N devices M oscillator_2_wavetable_index <json> |  |
| `oscillator_2_wavetables` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call oscillator_2_wavetables |  |
| `oscillator_wavetable_categories` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call oscillator_wavetable_categories |  |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `poly_voices` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call poly_voices |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `set_modulation_value` | method~ | `lom` — ableton_lom call tracks N devices M set_modulation_value [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `unison_mode` | property~ | `lom` — ableton_lom get tracks N devices M unison_mode · set tracks N devices M unison_mode <json> |  |
| `unison_voice_count` | property~ | `lom` — ableton_lom get tracks N devices M unison_voice_count · set tracks N devices M unison_voice_count <json> |  |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |
| `visible_modulation_target_names` | property~ | `lom` — ableton_lom get tracks N devices M visible_modulation_target_names · set tracks N devices M visible_modulation_target_names <json> |  |

## HybridReverbDevice

Path example: `tracks N devices M` · 25 members (+ 39 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class HybridReverbDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `ir_attack_time` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call ir_attack_time |  |
| `ir_category_index` | property~ | `lom` — ableton_lom get tracks N devices M ir_category_index · set tracks N devices M ir_category_index <json> |  |
| `ir_category_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call ir_category_list |  |
| `ir_decay_time` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call ir_decay_time |  |
| `ir_file_index` | property~ | `lom` — ableton_lom get tracks N devices M ir_file_index · set tracks N devices M ir_file_index <json> |  |
| `ir_file_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call ir_file_list |  |
| `ir_size_factor` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call ir_size_factor |  |
| `ir_time_shaping_on` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call ir_time_shaping_on |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## SpectralResonatorDevice

Path example: `tracks N devices M` · 29 members (+ 54 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class SpectralResonatorDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `frequency_dial_mode` | property~ | `lom` — ableton_lom get tracks N devices M frequency_dial_mode · set tracks N devices M frequency_dial_mode <json> |  |
| `frequency_dial_mode_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call frequency_dial_mode_list |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `midi_gate` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call midi_gate |  |
| `midi_gate_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call midi_gate_list |  |
| `mod_mode` | property~ | `lom` — ableton_lom get tracks N devices M mod_mode · set tracks N devices M mod_mode <json> |  |
| `mod_mode_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_mode_list |  |
| `mono_poly` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mono_poly |  |
| `mono_poly_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mono_poly_list |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `pitch_bend_range` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pitch_bend_range |  |
| `pitch_mode` | property~ | `lom` — ableton_lom get tracks N devices M pitch_mode · set tracks N devices M pitch_mode <json> |  |
| `pitch_mode_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pitch_mode_list |  |
| `polyphony` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call polyphony |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## DriftDevice

Path example: `tracks N devices M` · 46 members (+ 63 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class DriftDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `mod_matrix_filter_source_1_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_filter_source_1_index · set tracks N devices M mod_matrix_filter_source_1_index <json> |  |
| `mod_matrix_filter_source_1_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_filter_source_1_list |  |
| `mod_matrix_filter_source_2_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_filter_source_2_index · set tracks N devices M mod_matrix_filter_source_2_index <json> |  |
| `mod_matrix_filter_source_2_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_filter_source_2_list |  |
| `mod_matrix_lfo_source_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_lfo_source_index · set tracks N devices M mod_matrix_lfo_source_index <json> |  |
| `mod_matrix_lfo_source_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_lfo_source_list |  |
| `mod_matrix_pitch_source_1_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_pitch_source_1_index · set tracks N devices M mod_matrix_pitch_source_1_index <json> |  |
| `mod_matrix_pitch_source_1_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_pitch_source_1_list |  |
| `mod_matrix_pitch_source_2_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_pitch_source_2_index · set tracks N devices M mod_matrix_pitch_source_2_index <json> |  |
| `mod_matrix_pitch_source_2_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_pitch_source_2_list |  |
| `mod_matrix_shape_source_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_shape_source_index · set tracks N devices M mod_matrix_shape_source_index <json> |  |
| `mod_matrix_shape_source_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_shape_source_list |  |
| `mod_matrix_source_1_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_source_1_index · set tracks N devices M mod_matrix_source_1_index <json> |  |
| `mod_matrix_source_1_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_source_1_list |  |
| `mod_matrix_source_2_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_source_2_index · set tracks N devices M mod_matrix_source_2_index <json> |  |
| `mod_matrix_source_2_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_source_2_list |  |
| `mod_matrix_source_3_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_source_3_index · set tracks N devices M mod_matrix_source_3_index <json> |  |
| `mod_matrix_source_3_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_source_3_list |  |
| `mod_matrix_target_1_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_target_1_index · set tracks N devices M mod_matrix_target_1_index <json> |  |
| `mod_matrix_target_1_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_target_1_list |  |
| `mod_matrix_target_2_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_target_2_index · set tracks N devices M mod_matrix_target_2_index <json> |  |
| `mod_matrix_target_2_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_target_2_list |  |
| `mod_matrix_target_3_index` | property~ | `lom` — ableton_lom get tracks N devices M mod_matrix_target_3_index · set tracks N devices M mod_matrix_target_3_index <json> |  |
| `mod_matrix_target_3_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mod_matrix_target_3_list |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `pitch_bend_range` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pitch_bend_range |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |
| `voice_count_index` | property~ | `lom` — ableton_lom get tracks N devices M voice_count_index · set tracks N devices M voice_count_index <json> |  |
| `voice_count_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call voice_count_list |  |
| `voice_mode_index` | property~ | `lom` — ableton_lom get tracks N devices M voice_mode_index · set tracks N devices M voice_mode_index <json> |  |
| `voice_mode_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call voice_mode_list |  |

## MeldDevice

Path example: `tracks N devices M` · 21 members (+ 30 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class MeldDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `mono_poly` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call mono_poly |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `poly_voices` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call poly_voices |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `selected_engine` | property~ | `lom` — ableton_lom get tracks N devices M selected_engine · set tracks N devices M selected_engine <json> |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `unison_voices` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call unison_voices |  |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## RoarDevice

Path example: `tracks N devices M` · 20 members (+ 24 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class RoarDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `env_listen` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call env_listen |  |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `routing_mode_index` | property~ | `lom` — ableton_lom get tracks N devices M routing_mode_index · set tracks N devices M routing_mode_index <json> |  |
| `routing_mode_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call routing_mode_list |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## ShifterDevice

Path example: `tracks N devices M` · 20 members (+ 24 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `View` | method~ | `na` — nested class ShifterDevice.View — see its own section |  |
| `can_compare_ab` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_compare_ab (read-only) |  |
| `can_have_chains` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_chains (read-only) |  |
| `can_have_drum_pads` | property (bool)~ | `lom` — ableton_lom get tracks N devices M can_have_drum_pads (read-only) |  |
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get tracks N devices M canonical_parent (read-only) |  |
| `class_display_name` | property (str)~ | `lom` — ableton_lom get tracks N devices M class_display_name · set tracks N devices M class_display_name <json> |  |
| `class_name` | property (str)~ | `osc` — /live/device/get/class_name <track> <device> · /live/device/get/type_info (local edit) | kbot: ableton_device list |
| `is_active` | property (bool)~ | `tool` — ableton_structure set_device_active track=N device=M active=true\|false | sets parameters[0] ("Device On") when present, else Device.is_active; read-back = is_active. NOTE: /live/device/set/enabled (used by ableton_device enable/disable) does not exist in AbletonOSC |
| `is_using_compare_preset_b` | property (bool)~ | `lom` — ableton_lom get tracks N devices M is_using_compare_preset_b · set tracks N devices M is_using_compare_preset_b <json> |  |
| `latency_in_ms` | property (float)~ | `lom` — ableton_lom get tracks N devices M latency_in_ms · set tracks N devices M latency_in_ms <json> |  |
| `latency_in_samples` | property (int)~ | `lom` — ableton_lom get tracks N devices M latency_in_samples · set tracks N devices M latency_in_samples <json> |  |
| `name` | property (str)~ | `osc` — /live/device/get/name <track> <device> | kbot: ableton_device list |
| `parameters` | property (ATimeableValueVector)~ | `osc` — /live/device/get/num_parameters · /live/device/get/parameters/name\|value\|min\|max\|is_quantized <track> <device> · /live/device/set/parameters/value <track> <device> <v...> | kbot: ableton_device params/set; racks/chains only via ableton_lom `... devices M parameters K` |
| `pitch_bend_range` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pitch_bend_range |  |
| `pitch_mode_index` | property~ | `lom` — ableton_lom get tracks N devices M pitch_mode_index · set tracks N devices M pitch_mode_index <json> |  |
| `pitch_mode_list` | ? | `lom` — ableton_lom describe tracks N devices M → then get/set or call pitch_mode_list |  |
| `save_preset_to_compare_ab_slot` | method~ | `lom` — ableton_lom call tracks N devices M save_preset_to_compare_ab_slot [args] |  |
| `store_chosen_bank` | method~ | `lom` — ableton_lom call tracks N devices M store_chosen_bank [args] |  |
| `type` | property (DeviceType)~ | `osc` — /live/device/get/type <track> <device> | 0 undefined, 1 instrument, 2 audio_effect, 4 midi_effect |
| `view` | property (View)~ | `lom` — ableton_lom get <device path> view | Device.View.is_collapsed etc. |

## Browser

Path example: `app browser` · 21 members (+ 9 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `audio_effects` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=audio_effects [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `clips` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=clips [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `colors` | property (BrowserItemVector) | `lom` — ableton_lom get `app browser` colors (BrowserItemVector) · describe `app browser` | not a browser/search category (handler categories: instruments, audio_effects, midi_effects, drums, sounds, samples, max_for_live, plugins, user_library, packs, clips, current_project, user_folders, devices, all) |
| `current_project` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=current_project [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `drums` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=drums [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `filter_type` | property (int) | `lom` — ableton_lom get/set `app browser` filter_type | Browser.FilterType int |
| `hotswap_target` | property (NoneType) | `lom` — ableton_lom get `app browser` hotswap_target | no typed handler reads it (ableton_browser presets returns presets:[] + reason for non-PluginDevices; it does not fall back to hotswap children) |
| `instruments` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=instruments [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `legacy_libraries` | property (BrowserItemVector) | `lom` — ableton_lom get `app browser` legacy_libraries (BrowserItemVector) · describe `app browser` | not a browser/search category (see Browser.colors) |
| `load_item` | method | `tool` — ableton_browser load item=<uri\|name> target=track:N\|pad:N:note\|chain:<path>\|return:N\|master\|selected | read-back = device list / pad chains of the target; raw handler browser/load takes an optional 3rd arg [category]; stock-ish OSC alternative: /live/track/load/device (local edit, not upstream) |
| `max_for_live` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=max_for_live [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `midi_effects` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=midi_effects [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `packs` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=packs [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `plugins` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=plugins [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `preview_item` | method | `tool` — ableton_browser preview item=<uri\|name> | no LOM read-back exists for preview state; reply echoes the item (verified 2026-08-18) |
| `relation_to_hotswap_target` | method | `lom` — ableton_lom call `app browser` relation_to_hotswap_target [<item>] |  |
| `samples` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=samples [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `sounds` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=sounds [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `stop_preview` | method | `tool` — ableton_browser stop_preview | reply {stopped:true}; no LOM read-back exists |
| `user_folders` | property (BrowserItemVector) | `tool` — ableton_browser search query=<text> category=user_folders [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |
| `user_library` | property (BrowserItem) | `tool` — ableton_browser search query=<text> category=user_library [limit=N] | walks this root; returns [{name,uri,is_loadable,is_device,is_folder,category,path}] |

## Browser.BrowserItem

Path example: `app browser instruments` · 9 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `children` | property (BrowserItemVector) | `tool` — ableton_browser search (recursion) | search walks BrowserItem.children (Vector); iter_children only as fallback. Or ableton_lom children `app browser instruments` |
| `is_device` | property (bool) | `tool` — ableton_browser search (result field) | uri is what ableton_browser load takes |
| `is_folder` | property (bool) | `tool` — ableton_browser search (result field) | result field of ableton_browser search; uri is what ableton_browser load takes |
| `is_loadable` | property (bool) | `tool` — ableton_browser search (result field) | uri is what ableton_browser load takes |
| `is_selected` | property (bool) | `lom` — ableton_lom describe `app browser instruments` (member) · get <item path> is_selected | not part of the ableton_browser search result (fields: name, uri, is_loadable, is_device, is_folder, category, path) |
| `iter_children` | property (BrowserItemIterator) | `tool` — ableton_browser search (fallback when .children is missing) |  |
| `name` | property (str) | `tool` — ableton_browser search (result field) | uri is what ableton_browser load takes |
| `source` | property (str) | `lom` — ableton_lom get <item path> source | not part of the ableton_browser search result (fields: name, uri, is_loadable, is_device, is_folder, category, path) |
| `uri` | property (str) | `tool` — ableton_browser search (result field) | uri is what ableton_browser load takes |

## GroovePool

Path example: `live_set groove_pool` · 2 members (+ 3 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (Song) | `lom` — ableton_lom get live_set groove_pool canonical_parent (read-only) |  |
| `grooves` | property (Vector) | `lom` — ableton_lom get live_set groove_pool grooves · set live_set groove_pool grooves <json> |  |

## Groove

Path example: `live_set groove_pool grooves 0` · 7 members (+ 15 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `base` | property (Base) | `lom` — ableton_lom get live_set groove_pool grooves 0 base · set live_set groove_pool grooves 0 base <json> |  |
| `canonical_parent` | property (GroovePool) | `lom` — ableton_lom get live_set groove_pool grooves 0 canonical_parent (read-only) |  |
| `name` | property (str) | `lom` — ableton_lom get live_set groove_pool grooves 0 name · set live_set groove_pool grooves 0 name <json> |  |
| `quantization_amount` | property (float) | `lom` — ableton_lom get live_set groove_pool grooves 0 quantization_amount · set live_set groove_pool grooves 0 quantization_amount <json> |  |
| `random_amount` | property (float) | `lom` — ableton_lom get live_set groove_pool grooves 0 random_amount · set live_set groove_pool grooves 0 random_amount <json> |  |
| `timing_amount` | property (float) | `lom` — ableton_lom get live_set groove_pool grooves 0 timing_amount · set live_set groove_pool grooves 0 timing_amount <json> |  |
| `velocity_amount` | property (float) | `lom` — ableton_lom get live_set groove_pool grooves 0 velocity_amount · set live_set groove_pool grooves 0 velocity_amount <json> |  |

## TuningSystem

Path example: `live_set tuning_system` · 8 members (+ 15 listener add/remove/has methods, omitted)

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `canonical_parent` | property (NoneType)~ | `lom` — ableton_lom get live_set tuning_system canonical_parent (read-only) |  |
| `highest_note` | ? | `lom` — ableton_lom describe live_set tuning_system → then get/set or call highest_note |  |
| `lowest_note` | ? | `lom` — ableton_lom describe live_set tuning_system → then get/set or call lowest_note |  |
| `name` | property (str)~ | `lom` — ableton_lom get live_set tuning_system name · set live_set tuning_system name <json> |  |
| `note_tunings` | ? | `lom` — ableton_lom describe live_set tuning_system → then get/set or call note_tunings |  |
| `number_of_notes_in_pseudo_octave` | ? | `lom` — ableton_lom describe live_set tuning_system → then get/set or call number_of_notes_in_pseudo_octave |  |
| `pseudo_octave_in_cents` | ? | `lom` — ableton_lom describe live_set tuning_system → then get/set or call pseudo_octave_in_cents |  |
| `reference_pitch` | ? | `lom` — ableton_lom describe live_set tuning_system → then get/set or call reference_pitch |  |

## Application.ControlDescription

Path example: `<Application.ControlDescription path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `id` | ? | `na` — control-surface descriptor record |  |
| `name` | property (str)~ | `na` — control-surface descriptor record |  |

## Application.ControlDescriptionVector

Path example: `<Application.ControlDescriptionVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Application.MessageButtons

Int enum (6 values): `OK_ACCOUNT_BUTTON`, `OK_BUTTON`, `OK_NEW_SET_BUTTON`, `OK_PURCHASE_BUTTON`, `OK_RETRY_BUTTON`, `SAVE_DONT_SAVE_BUTTON`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Application.PushDialogType

Int enum (3 values): `MESSAGE_BOX`, `OUT_OF_UNLOCKS_DIALOG`, `RENT_TO_OWN_LICENSE_EXPIRED_DIALOG`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Application.UnavailableFeature

Int enum (1 values): `note_velocity_ranges_and_probabilities`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Application.UnavailableFeatureVector

Path example: `<Application.UnavailableFeatureVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Application.Variants

Path example: `<Application.Variants path>` · 6 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `BETA` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `INTRO` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `LITE` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `STANDARD` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `SUITE` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `TRIAL` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |

## Browser.BrowserItemVector

Path example: `<Browser.BrowserItemVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Browser.FilterType

Int enum (9 values): `audio_effect_hotswap`, `count`, `disabled`, `drum_pad_hotswap`, `hotswap_off`, `instrument_hotswap`, `midi_effect_hotswap`, `midi_track_devices`, `samples`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Browser.Relation

Int enum (4 values): `ancestor`, `descendant`, `equal`, `none`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Clip.ClipLaunchQuantization

Int enum (15 values): `q_2_bars`, `q_4_bars`, `q_8_bars`, `q_bar`, `q_eighth`, `q_eighth_triplet`, `q_global`, `q_half`, `q_half_triplet`, `q_none`, `q_quarter`, `q_quarter_triplet`, `q_sixteenth`, `q_sixteenth_triplet`, `q_thirtysecond`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Clip.GridQuantization

Int enum (11 values): `count`, `g_2_bars`, `g_4_bars`, `g_8_bars`, `g_bar`, `g_eighth`, `g_half`, `g_quarter`, `g_sixteenth`, `g_thirtysecond`, `no_grid`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Clip.LaunchMode

Int enum (4 values): `gate`, `repeat`, `toggle`, `trigger`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Clip.MidiNote

Path example: `<Clip.MidiNote path>` · 9 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `duration` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `mute` | property (bool)~ | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `note_id` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `pitch` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `probability` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `release_velocity` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `start_time` | property (float)~ | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `velocity` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |
| `velocity_deviation` | ? | `na` — note record — fields of the JSON that clip_notes op=get returns / op=add\|set takes |  |

## Clip.MidiNoteVector

Path example: `<Clip.MidiNoteVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Clip.WarpMarker

Path example: `<Clip.WarpMarker path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `beat_time` | ? | `na` — warp-marker record — returned as JSON by ableton_lom get <clip path> warp_markers |  |
| `sample_time` | ? | `na` — warp-marker record — returned as JSON by ableton_lom get <clip path> warp_markers |  |

## Clip.WarpMarkerVector

Path example: `<Clip.WarpMarkerVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Clip.WarpMode

Int enum (8 values): `beats`, `complex`, `complex_pro`, `count`, `repitch`, `rex`, `texture`, `tones`.

_enum constant — pass the int (or the name string) to the property that takes it_

## ClipSlot.ClipSlotPlayingState

Int enum (3 values): `recording`, `started`, `stopped`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Device.ATimeableValueVector

Path example: `<Device.ATimeableValueVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Device.DeviceType

Int enum (4 values): `audio_effect`, `instrument`, `midi_effect`, `undefined`.

_enum constant — pass the int (or the name string) to the property that takes it_

## DeviceParameter.AutomationState

Int enum (3 values): `none`, `overridden`, `playing`.

_enum constant — pass the int (or the name string) to the property that takes it_

## DeviceParameter.ParameterState

Int enum (3 values): `disabled`, `enabled`, `irrelevant`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Eq8Device.EditMode

Int enum (2 values): `a`, `b`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Eq8Device.GlobalMode

Int enum (3 values): `left_right`, `mid_side`, `stereo`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Groove.Base

Int enum (7 values): `count`, `gb_eight`, `gb_eight_triplet`, `gb_four`, `gb_sixteen`, `gb_sixteen_triplet`, `gb_thirtytwo`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Sample.SlicingBeatDivision

Int enum (11 values): `eighth`, `eighth_triplett`, `four_bars`, `half`, `half_triplett`, `one_bar`, `quarter`, `quarter_triplett`, `sixteenth`, `sixteenth_triplett`, `two_bars`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Sample.SlicingStyle

Int enum (4 values): `beat`, `manual`, `region`, `transient`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Sample.TransientLoopMode

Int enum (3 values): `alternate`, `forward`, `off`.

_enum constant — pass the int (or the name string) to the property that takes it_

## SimplerDevice.PlaybackMode

Int enum (3 values): `classic`, `one_shot`, `slicing`.

_enum constant — pass the int (or the name string) to the property that takes it_

## SimplerDevice.SlicingPlaybackMode

Int enum (3 values): `mono`, `poly`, `thru`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Song.BeatTime

Path example: `<Song.BeatTime path>` · 4 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `bars` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `beats` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `sub_division` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `ticks` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |

## Song.CaptureDestination

Int enum (3 values): `arrangement`, `auto`, `session`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Song.CaptureMode

Int enum (2 values): `all`, `all_except_selected`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Song.Quantization

Int enum (14 values): `q_2_bars`, `q_4_bars`, `q_8_bars`, `q_bar`, `q_eight`, `q_eight_triplet`, `q_half`, `q_half_triplet`, `q_no_q`, `q_quarter`, `q_quarter_triplet`, `q_sixtenth`, `q_sixtenth_triplet`, `q_thirtytwoth`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Song.RecordingQuantization

Int enum (9 values): `rec_q_eight`, `rec_q_eight_eight_triplet`, `rec_q_eight_triplet`, `rec_q_no_q`, `rec_q_quarter`, `rec_q_sixtenth`, `rec_q_sixtenth_sixtenth_triplet`, `rec_q_sixtenth_triplet`, `rec_q_thirtysecond`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Song.SessionRecordStatus

Int enum (3 values): `off`, `on`, `transition`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Song.SmptTime

Path example: `<Song.SmptTime path>` · 4 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `frames` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `hours` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `minutes` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |
| `seconds` | ? | `na` — enum constant — pass the int (or the name string) to the property that takes it |  |

## Song.TimeFormat

Int enum (6 values): `ms_time`, `smpte_24`, `smpte_25`, `smpte_29`, `smpte_30`, `smpte_30_drop`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Track.DeviceInsertMode

Int enum (4 values): `count`, `default`, `selected_left`, `selected_right`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Track.RoutingChannel

Path example: `<Track.RoutingChannel path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `display_name` | property~ | `na` — routing record {display_name, layout} |  |
| `layout` | ? | `na` — routing record {display_name, layout} |  |

## Track.RoutingChannelLayout

Int enum (3 values): `midi`, `mono`, `stereo`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Track.RoutingChannelVector

Path example: `<Track.RoutingChannelVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## Track.RoutingType

Path example: `<Track.RoutingType path>` · 3 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `attached_object` | ? | `na` — routing record {display_name, category, attached_object}; returned by ableton_lom get `tracks N` available_input_routing_types |  |
| `category` | ? | `na` — routing record {display_name, category, attached_object}; returned by ableton_lom get `tracks N` available_input_routing_types |  |
| `display_name` | property~ | `na` — routing record {display_name, category, attached_object}; returned by ableton_lom get `tracks N` available_input_routing_types |  |

## Track.RoutingTypeCategory

Int enum (8 values): `external`, `invalid`, `master`, `none`, `parent_group_track`, `resampling`, `rewire`, `track`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Track.RoutingTypeVector

Path example: `<Track.RoutingTypeVector path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `append` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `extend` | method~ | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## TuningSystem.PitchClassAndOctave

Path example: `<TuningSystem.PitchClassAndOctave path>` · 2 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `index_in_octave` | ? | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `octave` | ? | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## TuningSystem.ReferencePitch

Path example: `<TuningSystem.ReferencePitch path>` · 3 members

| member | kind | how to reach it from kbot | notes |
|---|---|---|---|
| `frequency` | ? | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `index_in_octave` | ? | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |
| `octave` | ? | `na` — value/vector class — ableton_lom returns these as JSON arrays/objects; not addressed directly |  |

## WavetableDevice.EffectMode

Int enum (4 values): `frequency_modulation`, `none`, `sync_and_pulse_width`, `warp_and_fold`.

_enum constant — pass the int (or the name string) to the property that takes it_

## WavetableDevice.FilterRouting

Int enum (3 values): `parallel`, `serial`, `split`.

_enum constant — pass the int (or the name string) to the property that takes it_

## WavetableDevice.ModulationSource

Int enum (11 values): `amp_envelope`, `envelope_2`, `envelope_3`, `lfo_1`, `lfo_2`, `midi_channel_pressure`, `midi_mod_wheel`, `midi_note`, `midi_pitch_bend`, `midi_random`, `midi_velocity`.

_enum constant — pass the int (or the name string) to the property that takes it_

## WavetableDevice.UnisonMode

Int enum (7 values): `classic`, `fast_shimmer`, `none`, `phase_sync`, `position_spread`, `random_note`, `slow_shimmer`.

_enum constant — pass the int (or the name string) to the property that takes it_

## WavetableDevice.VoiceCount

Int enum (8 values): `eight`, `five`, `four`, `seven`, `six`, `sixteen`, `three`, `two`.

_enum constant — pass the int (or the name string) to the property that takes it_

## WavetableDevice.Voicing

Int enum (2 values): `mono`, `poly`.

_enum constant — pass the int (or the name string) to the property that takes it_

## Summary

| via | members | share |
|---|---:|---:|
| `tool` — typed kbot handler | 76 | 6.6% |
| `osc` — stock AbletonOSC address | 226 | 19.5% |
| `lom` — generic ableton_lom plane | 583 | 50.3% |
| `ui` — UI only (Plane D) | 5 | 0.4% |
| `na` — constant / record — not addressed | 268 | 23.1% |
| **total (non-listener members)** | **1158** | 100% |

Per class:

| class | members | tool | osc | lom | ui | na |
|---|---:|---:|---:|---:|---:|---:|
| Song | 98 | 11 | 49 | 35 | 2 | 1 |
| Song.View | 12 | 0 | 4 | 8 | 0 | 0 |
| Song.CuePoint | 4 | 0 | 3 | 1 | 0 | 0 |
| Application | 23 | 5 | 3 | 14 | 0 | 1 |
| Application.View | 12 | 0 | 0 | 12 | 0 | 0 |
| Application.ControlSurfaceProxy | 12 | 0 | 0 | 12 | 0 | 0 |
| Track | 72 | 4 | 34 | 31 | 2 | 1 |
| Track.View | 5 | 0 | 1 | 4 | 0 | 0 |
| MixerDevice | 14 | 0 | 3 | 11 | 0 | 0 |
| ChainMixerDevice | 5 | 0 | 0 | 5 | 0 | 0 |
| ClipSlot | 20 | 0 | 13 | 7 | 0 | 0 |
| Clip | 88 | 4 | 42 | 41 | 0 | 1 |
| Clip.View | 7 | 0 | 0 | 7 | 0 | 0 |
| Scene | 15 | 0 | 12 | 3 | 0 | 0 |
| Device | 17 | 1 | 4 | 11 | 0 | 1 |
| Device.View | 2 | 0 | 0 | 2 | 0 | 0 |
| DeviceParameter | 18 | 0 | 6 | 12 | 0 | 0 |
| RackDevice | 39 | 7 | 3 | 28 | 0 | 1 |
| Chain | 17 | 1 | 0 | 16 | 0 | 0 |
| DrumPad | 7 | 2 | 0 | 5 | 0 | 0 |
| DrumChain | 20 | 2 | 0 | 18 | 0 | 0 |
| SimplerDevice | 38 | 3 | 4 | 30 | 0 | 1 |
| Sample | 31 | 0 | 0 | 31 | 0 | 0 |
| PluginDevice | 21 | 3 | 5 | 11 | 1 | 1 |
| MaxDevice | 25 | 1 | 4 | 19 | 0 | 1 |
| CompressorDevice | 21 | 1 | 4 | 15 | 0 | 1 |
| Eq8Device | 20 | 1 | 4 | 14 | 0 | 1 |
| WavetableDevice | 37 | 1 | 4 | 31 | 0 | 1 |
| HybridReverbDevice | 25 | 1 | 4 | 19 | 0 | 1 |
| SpectralResonatorDevice | 29 | 1 | 4 | 23 | 0 | 1 |
| DriftDevice | 46 | 1 | 4 | 40 | 0 | 1 |
| MeldDevice | 21 | 1 | 4 | 15 | 0 | 1 |
| RoarDevice | 20 | 1 | 4 | 14 | 0 | 1 |
| ShifterDevice | 20 | 1 | 4 | 14 | 0 | 1 |
| Browser | 21 | 16 | 0 | 5 | 0 | 0 |
| Browser.BrowserItem | 9 | 7 | 0 | 2 | 0 | 0 |
| GroovePool | 2 | 0 | 0 | 2 | 0 | 0 |
| Groove | 7 | 0 | 0 | 7 | 0 | 0 |
| TuningSystem | 8 | 0 | 0 | 8 | 0 | 0 |
| Application.ControlDescription | 2 | 0 | 0 | 0 | 0 | 2 |
| Application.ControlDescriptionVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Application.MessageButtons | 6 | 0 | 0 | 0 | 0 | 6 |
| Application.PushDialogType | 3 | 0 | 0 | 0 | 0 | 3 |
| Application.UnavailableFeature | 1 | 0 | 0 | 0 | 0 | 1 |
| Application.UnavailableFeatureVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Application.Variants | 6 | 0 | 0 | 0 | 0 | 6 |
| Browser.BrowserItemVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Browser.FilterType | 9 | 0 | 0 | 0 | 0 | 9 |
| Browser.Relation | 4 | 0 | 0 | 0 | 0 | 4 |
| Clip.ClipLaunchQuantization | 15 | 0 | 0 | 0 | 0 | 15 |
| Clip.GridQuantization | 11 | 0 | 0 | 0 | 0 | 11 |
| Clip.LaunchMode | 4 | 0 | 0 | 0 | 0 | 4 |
| Clip.MidiNote | 9 | 0 | 0 | 0 | 0 | 9 |
| Clip.MidiNoteVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Clip.WarpMarker | 2 | 0 | 0 | 0 | 0 | 2 |
| Clip.WarpMarkerVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Clip.WarpMode | 8 | 0 | 0 | 0 | 0 | 8 |
| ClipSlot.ClipSlotPlayingState | 3 | 0 | 0 | 0 | 0 | 3 |
| Device.ATimeableValueVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Device.DeviceType | 4 | 0 | 0 | 0 | 0 | 4 |
| DeviceParameter.AutomationState | 3 | 0 | 0 | 0 | 0 | 3 |
| DeviceParameter.ParameterState | 3 | 0 | 0 | 0 | 0 | 3 |
| Eq8Device.EditMode | 2 | 0 | 0 | 0 | 0 | 2 |
| Eq8Device.GlobalMode | 3 | 0 | 0 | 0 | 0 | 3 |
| Groove.Base | 7 | 0 | 0 | 0 | 0 | 7 |
| Sample.SlicingBeatDivision | 11 | 0 | 0 | 0 | 0 | 11 |
| Sample.SlicingStyle | 4 | 0 | 0 | 0 | 0 | 4 |
| Sample.TransientLoopMode | 3 | 0 | 0 | 0 | 0 | 3 |
| SimplerDevice.PlaybackMode | 3 | 0 | 0 | 0 | 0 | 3 |
| SimplerDevice.SlicingPlaybackMode | 3 | 0 | 0 | 0 | 0 | 3 |
| Song.BeatTime | 4 | 0 | 0 | 0 | 0 | 4 |
| Song.CaptureDestination | 3 | 0 | 0 | 0 | 0 | 3 |
| Song.CaptureMode | 2 | 0 | 0 | 0 | 0 | 2 |
| Song.Quantization | 14 | 0 | 0 | 0 | 0 | 14 |
| Song.RecordingQuantization | 9 | 0 | 0 | 0 | 0 | 9 |
| Song.SessionRecordStatus | 3 | 0 | 0 | 0 | 0 | 3 |
| Song.SmptTime | 4 | 0 | 0 | 0 | 0 | 4 |
| Song.TimeFormat | 6 | 0 | 0 | 0 | 0 | 6 |
| Track.DeviceInsertMode | 4 | 0 | 0 | 0 | 0 | 4 |
| Track.RoutingChannel | 2 | 0 | 0 | 0 | 0 | 2 |
| Track.RoutingChannelLayout | 3 | 0 | 0 | 0 | 0 | 3 |
| Track.RoutingChannelVector | 2 | 0 | 0 | 0 | 0 | 2 |
| Track.RoutingType | 3 | 0 | 0 | 0 | 0 | 3 |
| Track.RoutingTypeCategory | 8 | 0 | 0 | 0 | 0 | 8 |
| Track.RoutingTypeVector | 2 | 0 | 0 | 0 | 0 | 2 |
| TuningSystem.PitchClassAndOctave | 2 | 0 | 0 | 0 | 0 | 2 |
| TuningSystem.ReferencePitch | 3 | 0 | 0 | 0 | 0 | 3 |
| WavetableDevice.EffectMode | 4 | 0 | 0 | 0 | 0 | 4 |
| WavetableDevice.FilterRouting | 3 | 0 | 0 | 0 | 0 | 3 |
| WavetableDevice.ModulationSource | 11 | 0 | 0 | 0 | 0 | 11 |
| WavetableDevice.UnisonMode | 7 | 0 | 0 | 0 | 0 | 7 |
| WavetableDevice.VoiceCount | 8 | 0 | 0 | 0 | 0 | 8 |
| WavetableDevice.Voicing | 2 | 0 | 0 | 0 | 0 | 2 |

## Footer

- Listener plumbing omitted from the tables: **1257** `add_*_listener` / `remove_*_listener` / `*_has_listener` methods across 93 classes. All are reachable generically (`ableton_lom call <path> add_<prop>_listener` is not useful over one-shot OSC; use `/live/<class>/start_listen/<prop>` where AbletonOSC exposes it, or a Max for Live `live.observer`).
- Classes reachable from `Live.*` (43 modules): `Application`, `Base`, `Browser`, `CcControlDevice`, `Chain`, `ChainMixerDevice`, `Clip`, `ClipSlot`, `CompressorDevice`, `Conversions`, `Device`, `DeviceIO`, `DeviceParameter`, `DriftDevice`, `DrumCellDevice`, `DrumChain`, `DrumPad`, `Envelope`, `Eq8Device`, `Groove`, `GroovePool`, `HybridReverbDevice`, `Licensing`, `Listener`, `LomObject`, `LooperDevice`, `MaxDevice`, `MeldDevice`, `MidiMap`, `MixerDevice`, `PluginDevice`, `RackDevice`, `RoarDevice`, `Sample`, `Scene`, `ShifterDevice`, `SimplerDevice`, `Song`, `SpectralResonatorDevice`, `TakeLane`, `Track`, `TuningSystem`, `WavetableDevice`.
- Modules present but not dumped as classes (no instance in the probed Set): `CcControlDevice`, `DeviceIO`, `DrumCellDevice`, `Envelope`, `Licensing`, `LomObject`, `LooperDevice`, `MidiMap`, `TakeLane` — reachable via `ableton_lom describe` when an instance exists (e.g. `tracks N take_lanes 0`, `... clip automation_envelope`).
- Class lists captured empty (no public members at class level): `Track.DeviceContainer`, `Clip.MidiNoteSpecification`, `Browser.BrowserItemIterator`, `LomObject`.
- Dump errors (name lookup failed in the dump script, not missing from Live): `CuePoint: ERR module 'Live' has no attribute 'CuePoint'`; `MidiMap: ERR module 'MidiMap' has no attribute 'MidiMap'`; `ControlSurface: ERR module 'Live' has no attribute 'ControlSurface'`.
- Not in the LOM at all (UI only): freeze/flatten, export audio/stems, save/open Set, preferences, plugin GUI interaction, loading a Max for Live device other than through the browser. See CONTROL.md "What still needs the UI".

