#!/usr/bin/env python3
"""Turn a locked narration script into a timed beat map.

Why this exists: the frame book has to be pinned to narration lines, and
hand-timing a hundred beats is both slow and wrong. Estimating from WORD count
is also wrong — "through" and "a" are not the same length out loud. Speech
duration tracks SYLLABLES, so that is what this counts.

The rate is measured, not guessed. From the last shipped film:

    You Are Not Finished — 1,161 words, syllables/word 1.38, runtime 7:01
    => 1,602 syllables / 421s = 3.80 syllables per second

Paragraph breaks in the script are real breaths and get an explicit gap; the
sentence gap is shorter. Both are separated from the rate so a re-record at a
different speed only changes one number.

These timings are an ESTIMATE and stay one until narration exists. Once the VO
is recorded, conform against the real transcript — never ship a cut that was
only ever timed against this file.

Usage: python3 build-beats.py <script.txt> <out.json> [--rate 3.80]
"""
import json
import re
import sys

SYLL_RATE = 3.88        # syllables per second, measured (see below)
# DO NOT add per-sentence or per-paragraph gaps here. The first version of this
# tool added 0.22s per sentence and 0.55s per paragraph and over-predicted the
# recording by 29 seconds on a 6:28 film - 34.5s of invented silence against
# 7.2s of real silence. ElevenLabs already places its own pauses at punctuation
# inside a single request, so any gap added here is double-counted. The only
# real silence is the gap the assembly inserts BETWEEN acts.
SENT_GAP = 0.0
PARA_GAP = 0.0
MIN_HOLD = 1.30         # no beat shorter than this, however short the line


def syllables(word):
    """Same vowel-group heuristic as register-profile.py. Consistency between
    the two tools matters more than absolute accuracy — the rate above was
    calibrated with this exact function."""
    w = re.sub(r"[^a-z]", '', word.lower())
    if not w:
        return 0
    n = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and n > 1 and not w.endswith(('le', 'ee', 'ye')):
        n -= 1
    return max(1, n)


def line_syllables(line):
    return sum(syllables(t) for t in re.findall(r"[A-Za-z']+", line))


def split_sentences(para):
    """Keep the terminator attached so the narration line reads as written."""
    parts = re.findall(r'[^.!?]+[.!?]*', para)
    return [p.strip() for p in parts if p.strip()]


def build(path):
    paras = [p.strip() for p in open(path).read().split('\n\n') if p.strip()]
    beats, t = [], 0.0

    for pi, para in enumerate(paras):
        for si, sent in enumerate(split_sentences(para)):
            syl = line_syllables(sent)
            dur = max(MIN_HOLD, syl / SYLL_RATE)
            beats.append({
                'id': f'{len(beats)+1:03d}',
                'paragraph': pi,
                'line': sent,
                'start': round(t, 2),
                'duration': round(dur, 2),
                'syllables': syl,
            })
            t += dur + SENT_GAP
        t += PARA_GAP - SENT_GAP      # paragraph break replaces the sentence gap

    return beats, t


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        sys.exit(__doc__)
    if '--rate' in sys.argv:
        SYLL_RATE = float(sys.argv[sys.argv.index('--rate') + 1])

    beats, total = build(args[0])
    json.dump({'source': args[0], 'rate_syll_per_sec': SYLL_RATE,
               'estimated_runtime': round(total, 2), 'beats': beats},
              open(args[1], 'w'), indent=2)

    m, s = divmod(total, 60)
    print(f'{len(beats)} beats · estimated {int(m)}:{s:04.1f} · '
          f'mean line {total/len(beats):.2f}s')
