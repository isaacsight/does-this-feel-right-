#!/usr/bin/env python3
"""Conform a film's beat map to the narration that actually got recorded.

build-beats.py produces an ESTIMATE from a syllable rate. It is good enough to
board against and it is never good enough to cut against - on this film the
estimate said 6:57 and the recording came in at 6:28, a 29-second drift that
would have smeared every frame in the back half.

Method: the narration is recorded one file per act, so each act's true duration
is known exactly. Within an act, distribute that duration across its beats in
proportion to SYLLABLES, not words - speech duration tracks syllables, and a
within-act rate is uniform enough that proportional assignment lands inside a
few hundred milliseconds. That is well under the ~3.8s frame hold.

Using the per-act measured rate rather than one global rate is the point: the
acts in this film ran from 159 to 197 wpm, so a single rate would be wrong
everywhere.

Dropped beats (production/drops.json) are excluded, and their ids are recorded
so the assembly knows which frames are orphaned.

Usage: python3 conform-beats.py <film-dir>
"""
import json
import re
import sys
from pathlib import Path

# Act structure is FILM-SPECIFIC and lives in production/act-paras.json, written
# alongside the script. An earlier version hardcoded one film's paragraph ranges
# here and silently mis-assigned every beat when run on a different script.
def load_acts(film):
    import pathlib
    f = pathlib.Path(film) / 'production' / 'act-paras.json'
    if f.exists():
        # the manifest keys acts by their numbered stem, e.g. '01-the-party'
        return [('%02d-%s' % (a['n'], a['slug']), a['paras'][0], a['paras'][1])
                for a in json.load(open(f))]
    raise SystemExit(f'no {f} - write it before conforming')




def syllables(word):
    w = re.sub(r"[^a-z]", '', word.lower())
    if not w:
        return 0
    n = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and n > 1 and not w.endswith(('le', 'ee', 'ye')):
        n -= 1
    return max(1, n)


def main(film):
    film = Path(film)
    beats = json.load(open(film / 'production' / 'beats.json'))['beats']
    drops = set(json.load(open(film / 'production' / 'drops.json')))
    man = json.load(open(film / 'audio' / 'manifest.json'))
    gap = man['actGapSeconds']
    dur = {m['act']: m['duration'] for m in man['lines']}

    kept = [b for b in beats if b['id'] not in drops]
    out, t = [], 0.0

    acts = load_acts(film)
    for i, (slug, lo, hi) in enumerate(acts):
        if slug not in dur:
            sys.exit(f'no recorded audio for act {slug}')
        act_beats = [b for b in kept if lo <= b['paragraph'] <= hi]
        total_syl = sum(b['syllables'] for b in act_beats) or 1
        rate = dur[slug] / total_syl                    # seconds per syllable, measured
        start = t
        for b in act_beats:
            d = b['syllables'] * rate
            out.append({**b, 'act': slug, 'start': round(t, 3), 'duration': round(d, 3)})
            t += d
        # snap to the measured act end so rounding cannot accumulate
        t = start + dur[slug]
        if i < len(acts) - 1:
            t += gap
        print(f'  {slug:<24} {dur[slug]:6.1f}s  {len(act_beats):>2} beats  '
              f'{1/rate:5.2f} syll/s')

    json.dump({'source': 'conformed to audio/manifest.json',
               'runtime': round(t, 3),
               'dropped': sorted(drops),
               'beats': out},
              open(film / 'production' / 'beats-conformed.json', 'w'), indent=2)

    m, s = divmod(t, 60)
    print(f'\n{len(out)} beats conformed · {int(m)}:{s:04.1f} · '
          f'-> production/beats-conformed.json')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
