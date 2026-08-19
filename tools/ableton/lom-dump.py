import json, inspect
out = {}
def members(obj):
    names = [a for a in dir(obj) if not a.startswith('_')]
    res = {}
    for n in names:
        try:
            v = getattr(obj, n)
        except Exception as e:
            res[n] = 'ERR'
            continue
        if callable(v):
            res[n] = 'method'
        else:
            res[n] = type(v).__name__
    return res
def cls_members(cls):
    return sorted([a for a in dir(cls) if not a.startswith('_')])
song = song
tr = song.tracks[0]
out['Song'] = members(song)
out['Song.View'] = members(song.view)
out['Application'] = members(app)
out['Application.View'] = members(app.view)
out['Track'] = members(tr)
out['Track.View'] = members(tr.view)
out['MixerDevice'] = members(tr.mixer_device)
out['DeviceParameter'] = members(tr.mixer_device.volume)
out['ClipSlot'] = members(tr.clip_slots[0])
cs = tr.clip_slots[0]
if cs.has_clip:
    out['Clip(midi)'] = members(cs.clip)
    out['Clip.View'] = members(cs.clip.view)
out['Scene'] = members(song.scenes[0])
out['GroovePool'] = members(song.groove_pool)
if len(song.groove_pool.grooves): out['Groove'] = members(song.groove_pool.grooves[0])
rt = song.return_tracks[0]
if len(rt.devices):
    out['Device'] = members(rt.devices[0])
    out['Device.View'] = members(rt.devices[0].view)
out['Browser'] = members(app.browser)
try:
    out['BrowserItem'] = members(app.browser.instruments)
except Exception as e:
    out['BrowserItem'] = str(e)
# Class-level members from Live module for classes we can't instantiate right now
L = Live
for modname in ['Song','Track','Clip','ClipSlot','Device','DeviceParameter','RackDevice','Chain','DrumPad','DrumChain','Scene','MixerDevice','Sample','SimplerDevice','PluginDevice','MaxDevice','CompressorDevice','Eq8Device','WavetableDevice','HybridReverbDevice','SpectralResonatorDevice','DriftDevice','MeldDevice','RoarDevice','ShifterDevice','ChainMixerDevice','CuePoint','Groove','GroovePool','TuningSystem','Browser','Application','MidiMap','LomObject','ControlSurface']:
    try:
        mod = getattr(L, modname)
        cls = getattr(mod, modname)
        out['class:'+modname] = cls_members(cls)
        # nested classes e.g. Clip.Clip.View
        for sub in dir(mod):
            if not sub.startswith('_') and sub != modname:
                try:
                    o = getattr(mod, sub)
                    if inspect.isclass(o):
                        out['class:'+modname+'.'+sub] = cls_members(o)
                except Exception: pass
    except Exception as e:
        out['class:'+modname] = 'ERR '+str(e)
out['Live.modules'] = sorted([m for m in dir(L) if not m.startswith('_')])
json.dump(out, open('/tmp/kbot-lom-dump.json','w'), indent=1, default=str)
_result = 'wrote %d keys' % len(out)
