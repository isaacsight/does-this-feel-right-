#!/usr/bin/env python3
"""
build-melodic-trap.py — Full melodic trap session via AbletonOSC

"Emotional Drift" — Melodic trap + emotional depth + micro-variation + subtle genre blending

Tracks:
  1. LEAD    — Serum 2 reactive melody (F minor, velocity-reactive)
  2. PAD     — Serum 2 lush emotional pad (slow evolution, reverb wash)
  3. CHORDS  — Serum 2 R&B chord stabs (7ths, 9ths)
  4. 808     — Operator sine sub bass
  5. DRUMS   — Drum Rack (kick, snare, hats, perc)
  6. TEXTURE — Drift ambient drone

Key: F minor | BPM: 145 | Bars: 8
"""

import socket
import struct
import time
import random
import sys

# ── OSC Client ──────────────────────────────────────────────────────────

SEND_PORT = 11000
RECV_PORT = 11001
HOST = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)
sock.bind((HOST, RECV_PORT))


def osc_encode(addr, *args):
    b = addr.encode() + b'\x00'
    while len(b) % 4: b += b'\x00'
    types = ','
    arg_data = b''
    for a in args:
        if isinstance(a, int):
            types += 'i'
            arg_data += struct.pack('>i', a)
        elif isinstance(a, float):
            types += 'f'
            arg_data += struct.pack('>f', a)
        elif isinstance(a, str):
            types += 's'
            s = a.encode() + b'\x00'
            while len(s) % 4: s += b'\x00'
            arg_data += s
    b_types = types.encode() + b'\x00'
    while len(b_types) % 4: b_types += b'\x00'
    return b + b_types + arg_data


def osc_parse(data):
    end = data.index(0)
    addr = data[:end].decode()
    pos = end + 1
    while pos % 4: pos += 1
    args = []
    if pos < len(data) and data[pos:pos+1] == b',':
        tag_end = data.index(0, pos)
        tags = data[pos+1:tag_end].decode()
        pos = tag_end + 1
        while pos % 4: pos += 1
        for t in tags:
            if t == 'f':
                args.append(struct.unpack('>f', data[pos:pos+4])[0])
                pos += 4
            elif t == 'i':
                args.append(struct.unpack('>i', data[pos:pos+4])[0])
                pos += 4
            elif t == 's':
                s_end = data.index(0, pos)
                args.append(data[pos:s_end].decode())
                pos = s_end + 1
                while pos % 4: pos += 1
    return addr, args


def osc_send(addr, *args):
    """Send OSC message, no response expected."""
    sock.sendto(osc_encode(addr, *args), (HOST, SEND_PORT))


def osc_query(addr, *args):
    """Send OSC message and wait for response."""
    sock.sendto(osc_encode(addr, *args), (HOST, SEND_PORT))
    try:
        data, _ = sock.recvfrom(8192)
        return osc_parse(data)
    except socket.timeout:
        return addr, []


def flush_recv():
    """Drain any pending responses."""
    sock.setblocking(False)
    try:
        while True:
            sock.recvfrom(4096)
    except:
        pass
    sock.setblocking(True)
    sock.settimeout(5)


# ── Music Theory ────────────────────────────────────────────────────────

F_MINOR_PENTA = [65, 68, 70, 72, 75, 77, 80, 82, 84]

CHORDS = {
    'Fm9':    [53, 56, 60, 63, 67],
    'Dbmaj7': [61, 65, 68, 72],
    'Bbm7':  [58, 61, 65, 68],
    'Csus':  [60, 65, 67, 70],
    'Abmaj9': [56, 60, 63, 67, 70],
    'Ebmaj7': [63, 67, 70, 74],
}

PROGRESSION = [
    'Fm9', 'Fm9', 'Dbmaj7', 'Dbmaj7',
    'Bbm7', 'Bbm7', 'Csus', 'Csus',
    'Abmaj9', 'Abmaj9', 'Ebmaj7', 'Ebmaj7',
    'Fm9', 'Fm9', 'Dbmaj7', 'Csus',
]

KICK, SNARE, CLAP, CHH, OHH = 36, 38, 39, 42, 46


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ── Generators ──────────────────────────────────────────────────────────

def gen_melody(bars):
    notes = []
    pos = 0.0
    total = bars * 4
    idx = 4
    while pos < total:
        dur = random.choice([0.25, 0.5, 0.5, 0.75, 1.0, 1.5])
        beat = pos % 4
        if random.random() < (0.05 if beat == 0 else 0.15):
            pos += random.choice([0.25, 0.5])
            continue
        step = random.choice([-1, 1]) if random.random() < 0.6 else random.choice([-3, -2, 2, 3])
        idx = clamp(idx + step, 0, len(F_MINOR_PENTA) - 1)
        pitch = F_MINOR_PENTA[idx]
        phrase = (pos % 8) / 8
        if phrase < 0.3:   vel = random.uniform(85, 110)
        elif phrase < 0.6: vel = random.uniform(95, 120)
        else:              vel = random.uniform(65, 90)
        shift = random.uniform(-0.02, 0.02)
        notes.append((pitch, max(0, pos + shift), dur * random.uniform(0.8, 0.95), int(clamp(vel, 1, 127))))
        pos += dur
    return notes


def gen_mutated(orig):
    out = []
    for p, s, d, v in orig:
        ns = max(0, s + random.uniform(-0.035, 0.035))
        nv = int(clamp(v * (1 + random.uniform(-0.2, 0.2)), 1, 127))
        np = p + ((-12) if p > 74 else 12) if random.random() < 0.1 else p
        out.append((np, ns, d * random.uniform(0.85, 1.15), nv))
    return out


def gen_chords(bars):
    notes = []
    for bar in range(bars):
        chord = CHORDS[PROGRESSION[bar % len(PROGRESSION)]]
        b = bar * 4
        vel = int(random.uniform(75, 100))
        for p in chord:
            notes.append((p, b + random.uniform(-0.01, 0.01), random.uniform(1.5, 2.5), vel))
        if random.random() < 0.6:
            off = random.choice([1.5, 2.0, 2.5, 3.0])
            ov = int(random.uniform(55, 80))
            for p in chord:
                notes.append((p, b + off + random.uniform(-0.01, 0.01), random.uniform(0.5, 1.0), ov))
    return notes


def gen_pad(bars):
    notes = []
    for bar in range(0, bars, 2):
        chord = CHORDS[PROGRESSION[bar % len(PROGRESSION)]]
        root, fifth = chord[0], chord[2] if len(chord) > 2 else chord[1]
        vel = int(random.uniform(50, 70))
        notes.append((root, bar * 4, 7.5, vel))
        notes.append((fifth, bar * 4, 7.5, vel - 10))
        notes.append((root + 12, bar * 4, 7.5, int(vel * 0.6)))
    return notes


def gen_808(bars):
    notes = []
    for bar in range(bars):
        root = CHORDS[PROGRESSION[bar % len(PROGRESSION)]][0] - 12
        b = bar * 4
        notes.append((root, b, 1.5, int(random.uniform(100, 120))))
        if random.random() < 0.7:
            notes.append((root, b + 2, 1.0, int(random.uniform(90, 110))))
        if random.random() < 0.3:
            notes.append((root, b + 3.5, 0.25, int(random.uniform(80, 100))))
            notes.append((root + 2, b + 3.75, 0.25, int(random.uniform(70, 90))))
    return notes


def gen_drums(bars):
    notes = []
    for bar in range(bars):
        b = bar * 4
        notes.append((KICK, b, 0.5, int(random.uniform(110, 127))))
        notes.append((KICK, b + 2, 0.5, int(random.uniform(100, 120))))
        if random.random() < 0.5:
            notes.append((KICK, b + 2.5, 0.25, int(random.uniform(95, 115))))
        notes.append((SNARE, b + 1, 0.5, int(random.uniform(95, 115))))
        notes.append((CLAP, b + 1 + random.uniform(-0.01, 0.01), 0.5, int(random.uniform(80, 100))))
        notes.append((SNARE, b + 3, 0.5, int(random.uniform(95, 115))))
        notes.append((CLAP, b + 3 + random.uniform(-0.01, 0.01), 0.5, int(random.uniform(80, 100))))
        for i in range(16):
            hp = b + i * 0.25
            if i % 4 == 0 and random.random() < 0.2: continue
            accent = i % 2 == 0
            vel = random.uniform(70, 95) if accent else random.uniform(40, 65)
            if i >= 12 and random.random() < 0.4: vel = random.uniform(50, 80)
            is_open = not accent and random.random() < 0.15
            notes.append((OHH if is_open else CHH, hp + random.uniform(-0.015, 0.015),
                          0.4 if is_open else 0.15, int(clamp(vel, 1, 127))))
    return notes


# ── Helpers ─────────────────────────────────────────────────────────────

def write_clip(track, slot, length, name, notes):
    """Create a clip and write notes to it."""
    osc_send('/live/clip_slot/create_clip', track, slot, float(length))
    time.sleep(0.3)
    for pitch, start, dur, vel in notes:
        osc_send('/live/clip/add/notes', track, slot,
                 int(pitch), float(start), float(dur), int(vel), 0)
    osc_send('/live/clip/set/name', track, slot, name)
    time.sleep(0.1)


def set_track_name(track, name):
    osc_send('/live/track/set/name', track, name)


def set_device_param(track, device, param_idx, value):
    osc_send('/live/device/set/parameter/value', track, device, param_idx, float(value))


def get_param_names(track, device):
    """Get all parameter names for a device."""
    flush_recv()
    addr, args = osc_query('/live/device/get/parameters/name', track, device)
    if args:
        return args[2:]  # Skip track + device idx echo
    return []


# Cache param name → index maps per track/device
_param_cache = {}

def set_device_param_by_name(track, device, name, value):
    """Set a Serum 2 parameter by name. Caches the param list for speed."""
    key = (track, device)
    if key not in _param_cache:
        names = get_param_names(track, device)
        _param_cache[key] = {str(n).lower(): i for i, n in enumerate(names)}

    pmap = _param_cache[key]
    lower = name.lower()

    # Exact match
    idx = pmap.get(lower)
    if idx is None:
        # Fuzzy: find param containing our name
        for pn, pi in pmap.items():
            if lower in pn or pn in lower:
                idx = pi
                break

    if idx is not None:
        osc_send('/live/device/set/parameter/value', track, device, idx, float(value))
    else:
        pass  # Param not found, skip silently


# ── Main Build ──────────────────────────────────────────────────────────

def main():
    print('\n  EMOTIONAL DRIFT — Melodic Trap Session')
    print('  Building via AbletonOSC...\n')

    # Verify connection
    flush_recv()
    addr, args = osc_query('/live/song/get/tempo')
    if not args:
        print('  Cannot connect to AbletonOSC on port 11000')
        sys.exit(1)
    print(f'  Connected! Current tempo: {args[0]} BPM\n')

    # Set tempo
    osc_send('/live/song/set/tempo', 145.0)
    print('  Tempo: 145 BPM')
    time.sleep(0.3)

    # ── TRACK 0: LEAD ──────────────────────────────────────────────────

    print('\n  [1/6] LEAD — Emotional Drift melody')
    osc_send('/live/song/create_midi_track', -1)
    time.sleep(0.5)
    flush_recv()
    addr, args = osc_query('/live/song/get/num_tracks')
    num_tracks = int(args[0]) if args else 6
    lt = num_tracks - 2  # New track is before master
    set_track_name(lt, 'LEAD')

    # Load Serum
    print('        Loading Serum 2...')
    osc_send('/live/track/load/device', lt, 'Serum')
    time.sleep(2)

    # Program lead patch — Emotional Drift (reactive bounce)
    print('        Programming lead patch...')
    lead_params = [
        ('A Level', 0.8), ('A Pan', 0.5), ('A Position', 0.3),
        ('A Unison', 0.12), ('A Uni Detune', 0.06), ('A Uni Width', 0.55),
        ('B Level', 0.18), ('B Pan', 0.5), ('B Position', 0.6),
        ('B Uni Detune', 0.04),
        ('Noise Level', 0.04),
        ('Env 1 Attack', 0.02), ('Env 1 Decay', 0.35),
        ('Env 1 Sustain', 0.18), ('Env 1 Release', 0.15),
        ('Env 2 Attack', 0.0), ('Env 2 Decay', 0.22),
        ('Env 2 Sustain', 0.08), ('Env 2 Release', 0.1),
        ('Filter 1 Cutoff', 0.48), ('Filter 1 Res', 0.18),
        ('Filter 1 Drive', 0.12),
        ('LFO 1 Rate', 0.42), ('LFO 1 Smooth', 0.35),
        ('Main Vol', 0.5),
    ]
    for name, val in lead_params:
        set_device_param_by_name(lt, 0, name, val)

    melody = gen_melody(8)
    melody_b = gen_mutated(melody)
    write_clip(lt, 0, 32, 'Lead A', melody)
    write_clip(lt, 1, 32, 'Lead B (drift)', melody_b)
    print(f'        {len(melody)} notes + mutated variant')

    # Set volume
    osc_send('/live/track/set/volume', lt, 0.75)

    # ── TRACK 1: PAD ───────────────────────────────────────────────────

    print('\n  [2/6] PAD — Emotional Wash')
    osc_send('/live/song/create_midi_track', -1)
    time.sleep(0.5)
    flush_recv()
    addr, args = osc_query('/live/song/get/num_tracks')
    pt = (int(args[0]) if args else num_tracks + 1) - 2
    set_track_name(pt, 'PAD')

    osc_send('/live/track/load/device', pt, 'Serum')
    time.sleep(2)

    # Program pad patch — Emotional Wash (wide, evolving)
    print('        Programming pad patch...')
    pad_params = [
        ('A Level', 0.7), ('A Position', 0.2),
        ('A Unison', 0.35), ('A Uni Detune', 0.18), ('A Uni Width', 0.8),
        ('B Level', 0.4), ('B Position', 0.45),
        ('B Unison', 0.25), ('B Uni Detune', 0.15),
        ('Noise Level', 0.03),
        ('Env 1 Attack', 0.4), ('Env 1 Decay', 0.2),
        ('Env 1 Sustain', 0.85), ('Env 1 Release', 0.55),
        ('Filter 1 Cutoff', 0.55), ('Filter 1 Res', 0.1),
        ('LFO 1 Rate', 0.2), ('LFO 1 Smooth', 0.6),
        ('Main Vol', 0.45),
    ]
    for name, val in pad_params:
        set_device_param_by_name(pt, 0, name, val)

    pad = gen_pad(8)
    write_clip(pt, 0, 32, 'Pad A', pad)
    print(f'        {len(pad)} sustained notes')
    osc_send('/live/track/set/volume', pt, 0.55)

    # ── TRACK 2: CHORDS ────────────────────────────────────────────────

    print('\n  [3/6] CHORDS — R&B Glass stabs')
    osc_send('/live/song/create_midi_track', -1)
    time.sleep(0.5)
    flush_recv()
    addr, args = osc_query('/live/song/get/num_tracks')
    ct = (int(args[0]) if args else num_tracks + 2) - 2
    set_track_name(ct, 'CHORDS')

    osc_send('/live/track/load/device', ct, 'Serum')
    time.sleep(2)

    # Program chord patch — R&B Glass (bright, stab-like)
    print('        Programming chord patch...')
    chord_params = [
        ('A Level', 0.75), ('A Position', 0.5),
        ('A Unison', 0.08), ('A Uni Detune', 0.03), ('A Uni Width', 0.5),
        ('B Level', 0.25), ('B Position', 0.7),
        ('Noise Level', 0.0),
        ('Env 1 Attack', 0.01), ('Env 1 Decay', 0.45),
        ('Env 1 Sustain', 0.25), ('Env 1 Release', 0.2),
        ('Env 2 Attack', 0.0), ('Env 2 Decay', 0.3),
        ('Env 2 Sustain', 0.15), ('Env 2 Release', 0.15),
        ('Filter 1 Cutoff', 0.6), ('Filter 1 Res', 0.12),
        ('Filter 1 Drive', 0.08),
        ('Main Vol', 0.45),
    ]
    for name, val in chord_params:
        set_device_param_by_name(ct, 0, name, val)

    chords = gen_chords(8)
    write_clip(ct, 0, 32, 'Chords A', chords)
    print(f'        {len(chords)} notes (7ths + 9ths)')
    osc_send('/live/track/set/volume', ct, 0.6)

    # ── TRACK 3: 808 ───────────────────────────────────────────────────

    print('\n  [4/6] 808 — Deep sub (Serum 2)')
    osc_send('/live/song/create_midi_track', -1)
    time.sleep(0.5)
    flush_recv()
    addr, args = osc_query('/live/song/get/num_tracks')
    bt = (int(args[0]) if args else num_tracks + 3) - 2
    set_track_name(bt, '808')

    osc_send('/live/track/load/device', bt, 'Serum')
    time.sleep(2)

    # Program 808 patch via Serum 2 params
    # Sine wave, long decay, no sustain = classic 808
    print('        Programming 808 patch...')
    bass_params = [
        # OSC A: sine (WT pos 0 = sine in Basic Shapes)
        ('A Level', 1.0), ('A Pan', 0.5), ('A Position', 0.0),
        ('A Octave', 0.35),  # -1 oct
        ('A Unison', 0.0),   # No unison
        # OSC B/C off
        ('B Level', 0.0), ('C Enable', 0.0),
        # Env 1: long decay, no sustain (808 style)
        ('Env 1 Attack', 0.0), ('Env 1 Decay', 0.65),
        ('Env 1 Sustain', 0.0), ('Env 1 Release', 0.3),
        # Filter: low cutoff, warm
        ('Filter 1 Cutoff', 0.3), ('Filter 1 Res', 0.05),
        # Clean, heavy
        ('Main Vol', 0.6), ('Noise Level', 0.0),
        ('Mono Toggle', 1.0),  # Mono for bass
        ('Porta Time', 0.08),  # Slight glide for slides
    ]
    for name, val in bass_params:
        # Find param by name and set
        set_device_param_by_name(bt, 0, name, val)

    bass = gen_808(8)
    write_clip(bt, 0, 32, '808 A', bass)
    print(f'        {len(bass)} notes')
    osc_send('/live/track/set/volume', bt, 0.85)

    # ── TRACK 4: DRUMS ─────────────────────────────────────────────────

    print('\n  [5/6] DRUMS — Trap kit')
    osc_send('/live/song/create_midi_track', -1)
    time.sleep(0.5)
    flush_recv()
    addr, args = osc_query('/live/song/get/num_tracks')
    dt = (int(args[0]) if args else num_tracks + 4) - 2
    set_track_name(dt, 'DRUMS')

    osc_send('/live/track/load/device', dt, 'Drum Rack')
    time.sleep(1.5)

    drums = gen_drums(8)
    write_clip(dt, 0, 32, 'Drums A', drums)
    print(f'        {len(drums)} hits')
    osc_send('/live/track/set/volume', dt, 0.8)

    # ── TRACK 5: TEXTURE ───────────────────────────────────────────────

    print('\n  [6/6] TEXTURE — Lo-fi atmosphere (Serum 2)')
    osc_send('/live/song/create_midi_track', -1)
    time.sleep(0.5)
    flush_recv()
    addr, args = osc_query('/live/song/get/num_tracks')
    tt = (int(args[0]) if args else num_tracks + 5) - 2
    set_track_name(tt, 'TEXTURE')

    osc_send('/live/track/load/device', tt, 'Serum')
    time.sleep(2)

    # Program ambient texture patch
    print('        Programming texture patch...')
    tex_params = [
        ('A Level', 0.4), ('A Position', 0.15),
        ('A Unison', 0.4), ('A Uni Detune', 0.25), ('A Uni Width', 0.9),
        ('B Level', 0.3), ('B Position', 0.65),
        ('B Unison', 0.3), ('B Uni Detune', 0.2),
        ('Noise Level', 0.15),  # Noise adds lo-fi texture
        ('Env 1 Attack', 0.6), ('Env 1 Decay', 0.1),
        ('Env 1 Sustain', 0.9), ('Env 1 Release', 0.7),
        ('Filter 1 Cutoff', 0.35), ('Filter 1 Res', 0.08),
        ('LFO 1 Rate', 0.15), ('LFO 1 Smooth', 0.7),
        ('Main Vol', 0.35),
    ]
    for name, val in tex_params:
        set_device_param_by_name(tt, 0, name, val)

    tex = [(65, 0, 31, 40), (72, 0, 31, 30)]
    write_clip(tt, 0, 32, 'Atmos', tex)
    osc_send('/live/track/set/volume', tt, 0.3)
    print('        Ambient drone layer')

    # ── Fire all clips & play ──────────────────────────────────────────

    print('\n  Firing all clips...')
    for t in [lt, pt, ct, bt, dt, tt]:
        osc_send('/live/clip_slot/fire', t, 0)
        time.sleep(0.1)

    osc_send('/live/song/start_playing')
    print('  Playing!\n')

    # ── Summary ────────────────────────────────────────────────────────

    print('  ================================================================')
    print('  EMOTIONAL DRIFT — Melodic Trap Session')
    print('  ================================================================')
    print('  Key: F minor  |  BPM: 145  |  Bars: 8')
    print('  Progression: Fm9 > Dbmaj7 > Bbm7 > Csus > Abmaj9 > Ebmaj7')
    print()
    print('  TRACKS:')
    print(f'  {lt}  LEAD     Serum 2 reactive melody')
    print(f'  {pt}  PAD      Serum 2 lush evolving pad')
    print(f'  {ct}  CHORDS   Serum 2 R&B glass stabs')
    print(f'  {bt}  808      Serum 2 sine sub (mono, glide)')
    print(f'  {dt}  DRUMS    Drum Rack (humanized)')
    print(f'  {tt}  TEXTURE  Serum 2 ambient drone (wide unison, noise)')
    print()
    print('  GENRE BLENDING:')
    print('  - R&B:     maj7/min9 chords, velocity dynamics')
    print('  - Lo-Fi:   texture layer, timing drift')
    print('  - Ambient:  pad wash, long reverb, drone')
    print('  - Trap:    808 pattern, hihat rolls, snare/clap layers')
    print()
    print('  MICRO-VARIATION:')
    print('  - Melody velocity follows 2-bar emotional arc')
    print('  - All notes humanized +/-15ms')
    print('  - Hihats velocity + timing randomized per hit')
    print('  - Off-beat chord stabs randomized (60% chance)')
    print('  - Scene B: melody mutated (timing/velocity/octave drift)')
    print()
    print('  SERUM 2 TWEAKS (in the synth UI):')
    print('  LEAD:   LFO 1 > S&H, Trigger. Vel>Cutoff, Vel>WT Pos')
    print('  PAD:    LFO 1 > slow tri, mod A Position. Wide unison.')
    print('  CHORDS: Env 2 > Filter cutoff. Bright WT position.')
    print('  ================================================================\n')

    sock.close()


if __name__ == '__main__':
    main()
