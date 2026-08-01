#!/usr/bin/env python3
"""Write an SRT from a film's conformed beats.

Captions come from the LOCKED SCRIPT, never from ASR. The script is what was
actually said, it already carries correct punctuation and proper nouns, and ASR
reliably mangles names and numbers - which matters here because an act of this
film is nothing but numbers.

A narration line is often too long to read in one card, so lines are split into
cue-sized chunks on punctuation first and word boundaries second, and each
chunk gets a share of its line's duration proportional to its characters.

Reading-speed guard: no card is left on screen for less than MIN_CARD seconds,
and no card carries more than MAX_CHARS characters.

If the delivered cut is topped with a channel intro, pass --offset <seconds>.
Forgetting this is a silent failure: the SRT still validates, still loads, and
is simply wrong by the length of the intro for the whole film.

Usage: python3 build-srt.py <film-dir> <out.srt> [--offset 12.2]
"""
import json
import re
import sys

MAX_CHARS = 84          # two lines of ~42, comfortable at 1080p
MIN_CARD = 1.0
WRAP = 42


def timecode(sec):
    sec = max(0.0, sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', ',')


def chunk(text):
    """Split a narration line into cue-sized pieces, preferring punctuation."""
    if len(text) <= MAX_CHARS:
        return [text]
    # try clause boundaries first
    pieces, buf = [], ''
    for part in re.split(r'(?<=[,;:])\s+', text):
        if buf and len(buf) + 1 + len(part) > MAX_CHARS:
            pieces.append(buf); buf = part
        else:
            buf = f'{buf} {part}'.strip()
    if buf:
        pieces.append(buf)
    # anything still too long gets split on words
    out = []
    for p in pieces:
        while len(p) > MAX_CHARS:
            cut = p.rfind(' ', 0, MAX_CHARS)
            if cut <= 0:
                cut = MAX_CHARS
            out.append(p[:cut].strip()); p = p[cut:].strip()
        if p:
            out.append(p)
    return out


def wrap(text):
    """Two lines maximum, balanced on a word boundary."""
    if len(text) <= WRAP:
        return text
    cut = text.rfind(' ', 0, len(text) // 2 + 8)
    if cut <= 0:
        cut = text.find(' ', len(text) // 2)
    return text if cut <= 0 else text[:cut] + '\n' + text[cut + 1:]


def main(film, out, offset=0.0):
    conf = json.load(open(f'{film}/production/beats-conformed.json'))
    cards = []
    for b in conf['beats']:
        pieces = chunk(b['line'])
        total = sum(len(p) for p in pieces) or 1
        t = b['start'] + offset
        for p in pieces:
            d = b['duration'] * len(p) / total
            cards.append([t, t + d, p])
            t += d

    # enforce the reading floor by borrowing from the following card
    for i in range(len(cards) - 1):
        if cards[i][1] - cards[i][0] < MIN_CARD:
            cards[i][1] = cards[i][0] + MIN_CARD
            if cards[i + 1][0] < cards[i][1]:
                cards[i + 1][0] = cards[i][1]

    # Quantise to milliseconds BEFORE writing, then re-enforce monotonicity.
    # Rounding at format time is what produces a card ending at 08.969 while the
    # next starts at 08.968 - the same 1ms-overlap class the composition linter
    # rejects, and some players drop a card that starts before the previous ends.
    for c in cards:
        c[0] = round(c[0], 3)
        c[1] = round(c[1], 3)
    for i in range(1, len(cards)):
        if cards[i][0] < cards[i - 1][1]:
            cards[i][0] = cards[i - 1][1]
        if cards[i][1] <= cards[i][0]:
            cards[i][1] = round(cards[i][0] + MIN_CARD, 3)

    with open(out, 'w') as f:
        for i, (a, b, text) in enumerate(cards, 1):
            f.write(f'{i}\n{timecode(a)} --> {timecode(b)}\n{wrap(text)}\n\n')

    longest = max(len(c[2]) for c in cards)
    print(f'{len(cards)} cards -> {out}')
    print(f'longest card {longest} chars · shortest '
          f'{min(c[1]-c[0] for c in cards):.2f}s')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        sys.exit(__doc__)
    off = float(sys.argv[sys.argv.index('--offset') + 1]) if '--offset' in sys.argv else 0.0
    main(args[0], args[1], off)
