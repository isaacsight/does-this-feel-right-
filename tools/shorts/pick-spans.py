#!/usr/bin/env python3
"""Choose vertical-short IN/OUT points that land on real sentence boundaries.

WHY. The first six shorts were cut on beat boundaries from
production/beats-conformed.json. Those starts are ESTIMATES - conform-beats.py
spreads an act's measured duration across its beats in proportion to syllables,
which is accurate to a few hundred milliseconds. That is fine for holding a
frame and wrong for a cut, because a few hundred milliseconds is a whole word.
Five of six shorts opened mid-sentence:

    "three researchers gathered every trial they could find"   (lost "In 2019,")
    "of us have said it to somebody"                           (lost "Most")
    "in. And what it is good at is the mother"                 (lost the clause)

On a vertical short the first second IS the hook, so this is not cosmetic.

METHOD. audio/words.json has the exact start and end of every spoken word, so
sentence boundaries are known rather than modelled. A sentence starts at the
first word after one ending in . ! or ?; the film's own opening word starts the
first sentence. Given a rough target, snap the IN point to the nearest sentence
start and then take whole sentences until the span fits the platform window.

Prefer the LONGEST span inside the window rather than the first one that fits:
the difference is usually one more complete sentence, and a short that ends on
a finished thought beats one that ends because the clock ran out.

Usage:
    python3 pick-spans.py <film-dir> <rough-start-seconds> [more starts...]
    python3 pick-spans.py <film-dir> --list        # every sentence with its time
"""
import json
import re
import sys
from pathlib import Path

MIN_SEC = 52.0          # below this a short reads as thin
MAX_SEC = 59.0          # YouTube Shorts / Reels / TikTok all take 60
LEAD = 0.18             # breath before the first word, so it does not clip


def sentences(words):
    """Split the word list into sentences. Returns [(start_i, end_i)] pairs."""
    out, start = [], 0
    for i, w in enumerate(words):
        if re.search(r'[.!?]["\')\]]?$', w['w']):
            out.append((start, i))
            start = i + 1
    if start < len(words):
        out.append((start, len(words) - 1))
    return out


def pick(words, sents, target):
    """Longest whole-sentence span starting at/after `target` that fits."""
    # First sentence whose start is not before the target, so a rough target
    # never cuts into the sentence it lands in.
    begin = next((k for k, (s, _) in enumerate(sents)
                  if words[s]['start'] >= target - 0.5), None)
    if begin is None:
        return None
    t0 = words[sents[begin][0]]['start']
    best = None
    for k in range(begin, len(sents)):
        t1 = words[sents[k][1]]['end']
        if t1 - t0 > MAX_SEC:
            break
        if t1 - t0 >= MIN_SEC:
            best = (t0, t1, begin, k)      # keep extending; last fit wins
    return best


def main(film, targets):
    film = Path(film)
    words = json.load(open(film / 'audio' / 'words.json'))['words']
    sents = sentences(words)

    if targets == ['--list']:
        for s, e in sents:
            print(f"{words[s]['start']:7.1f}  "
                  f"{' '.join(w['w'] for w in words[s:e + 1])[:88]}")
        return

    for target in targets:
        got = pick(words, sents, float(target))
        if not got:
            print(f'{target}s  -- no whole-sentence span fits the window')
            continue
        t0, t1, a, b = got
        text = ' '.join(w['w'] for w in words[sents[a][0]:sents[b][1] + 1])
        print(f'\n[{max(0.0, t0 - LEAD):7.2f} - {t1:7.2f}]  {t1 - t0:4.1f}s  '
              f'{b - a + 1} sentences')
        print(f'  OPENS: {text[:96]}')
        print(f'  ENDS:  ...{text[-96:]}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
