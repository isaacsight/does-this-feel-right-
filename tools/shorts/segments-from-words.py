#!/usr/bin/env python3
"""Build caption segments from REAL per-word timings.

Supersedes build-segments.py wherever audio/words.json exists.

WHY. build-segments.py estimates twice over: conform-beats.py spreads an act's
measured duration across its beats in proportion to SYLLABLES, then the card
splitter divides each beat by CHARACTER COUNT. Both are reasonable and both are
approximations, and they stack. Measured on You Watched It Happen against the
true word timings: mean drift +0.41s, and 62% of cards more than 0.5s out, with
the worst at 3.3s. A caption three seconds early is not a caption.

Estimation was the only option before. tools/video/narrate.mjs now records with
ElevenLabs' /with-timestamps endpoint and writes audio/words.json, so a card can
start exactly when its first word is spoken and end exactly when its last one
finishes. There is nothing left to model.

Cards are packed to the same budget as the old splitter - the 76pt type in an
880px safe box wraps to two lines at <= ~46 characters - and are broken at
punctuation first, word boundaries second.

Usage: python3 segments-from-words.py <film-dir> <out.json> [fps]
"""
import json
import re
import sys
from pathlib import Path

MAX_CHARS = 38          # comfortable two-line card
HARD_MAX = 46           # past this the tool shrinks the point size
MIN_SEC = 1.10          # never flash a card shorter than this
GAP_BREAK = 0.45        # a pause this long is a natural card boundary


def build(film, fps):
    film = Path(film)
    words = json.load(open(film / 'audio' / 'words.json'))['words']

    cards, cur = [], []
    def flush():
        if cur:
            cards.append(list(cur)); cur.clear()

    for i, w in enumerate(words):
        cand = ' '.join([x['w'] for x in cur] + [w['w']])
        # Break BEFORE adding when the card is already full, or when the speaker
        # left a real pause - the ear hears that pause as the end of a thought,
        # so a card that runs across it reads as lagging.
        gap = w['start'] - cur[-1]['end'] if cur else 0
        if cur and (len(cand) > MAX_CHARS or gap >= GAP_BREAK):
            flush()
        cur.append(w)
        # Punctuation closes a card as long as it is not left too short.
        if re.search(r'[.!?;:]$', w['w']) and len(' '.join(x['w'] for x in cur)) >= 12:
            flush()
    flush()

    # Merge any card too brief to read into its neighbour, where the merge fits.
    i = 0
    while i < len(cards):
        dur = cards[i][-1]['end'] - cards[i][0]['start']
        if dur >= MIN_SEC or len(cards) == 1:
            i += 1; continue
        j = i - 1 if i > 0 else i + 1
        joined = ' '.join(x['w'] for x in cards[min(i, j)] + cards[max(i, j)])
        if len(joined) <= HARD_MAX:
            lo, hi = min(i, j), max(i, j)
            cards[lo:hi + 1] = [cards[lo] + cards[hi]]
            i = max(0, lo - 1)
        else:
            i += 1

    # Hold short cards past their last word. Reading time is not bounded by
    # speech: the START must be exact, because that is what "in sync" means to
    # the eye, but the END can run into the silence before the next card. This
    # is what fixes a flashing card without touching sync at all.
    out = []
    for i, c in enumerate(cards):
        start, end = c[0]['start'], c[-1]['end']
        ceiling = cards[i + 1][0]['start'] if i + 1 < len(cards) else end + MIN_SEC
        if end - start < MIN_SEC:
            end = min(ceiling, start + MIN_SEC)
        out.append([round(start * fps), round(end * fps),
                    ' '.join(x['w'] for x in c)])
    return out


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    fps = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
    segs = build(sys.argv[1], fps)
    json.dump({'fps': fps, 'segments': segs}, open(sys.argv[2], 'w'), indent=1)

    longest = max(segs, key=lambda s: len(s[2]))
    short = [s for s in segs if (s[1] - s[0]) / fps < MIN_SEC]
    print(f'{len(segs)} cards -> {sys.argv[2]}  (from real word timings)')
    print(f'longest {len(longest[2])} chars: "{longest[2]}"')
    print(f'cards under {MIN_SEC}s: {len(short)}')
