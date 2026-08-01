#!/usr/bin/env python3
"""Build a cut-verticals segments.json from a HyperFrames literal edit map.

The edit map's `cue` field IS the locked script, already carrying exact
start/end times per shot. That is the source of truth for captions — never
ASR, which mangles proper nouns and chunks on speech pauses
(docs/video/CAPTION-SPEC.md, docs/video/SHORTS-TEMPLATE.md).

Cues are written for the ear and run long — up to ~120 characters against a
two-line, ~30-characters-per-line card. This splits them at natural syntactic
breaks and allocates each fragment a share of the cue's duration proportional
to its length, so cards track the voice without ASR.

Accepts either a HyperFrames literal edit map (frames/shots/cue) or a
conformed beat map (production/beats-conformed.json), which is what films
assembled by tools/video/build-composition.mjs produce. Both reduce to the same
thing: spans of (start, end, spoken text) taken from the locked script.

Usage: python3 build-segments.py <edit-map|beats-conformed.json> <out.json> [fps]
"""
import json, re, sys

MAX_CHARS = 38      # spec budget: 2 lines x <=21 chars. Measured: 76pt in an
                    # 880px box wraps to 2 lines at <=52 chars of lowercase and
                    # 3 lines past that, and 3 lines trips the tool's shrink.
                    # 38/46 is the widest budget where no card in this film
                    # shrank -- caps and wide glyphs eat the difference.
HARD_MAX = 46       # absolute ceiling: past this the card wraps to 3 lines and
                    # the tool steps the point size down, breaking the locked look
MIN_SEC = 1.10      # never flash a card shorter than this
BREAK = re.compile(r'(?<=[.!?;:—])\s+|(?<=,)\s+')


def split_cue(text):
    """Greedily pack syntactic fragments into <=MAX_CHARS cards."""
    parts = [p.strip() for p in BREAK.split(text.strip()) if p and p.strip()]
    if not parts:
        return []
    cards, cur = [], ''
    for p in parts:
        cand = f'{cur} {p}'.strip()
        if cur and len(cand) > MAX_CHARS:
            cards.append(cur)
            cur = p
        else:
            cur = cand
    if cur:
        cards.append(cur)

    # A single fragment can still exceed the budget (no comma to break on).
    # Fall back to a word-wrap so a card never overflows to four lines.
    out = []
    for c in cards:
        while len(c) > MAX_CHARS:
            cut = c.rfind(' ', 0, MAX_CHARS)
            if cut <= 0:
                break
            out.append(c[:cut])
            c = c[cut + 1:]
        out.append(c)
    return out


def main(map_path, out_path, fps=30.0):
    doc = json.load(open(map_path))
    fps = float(fps)

    if 'beats' in doc:
        # Conformed beat map: one beat is already one narration line, so there
        # is nothing to collapse.
        spans = [[b['start'], b['start'] + b['duration'], b['line'].strip()]
                 for b in doc['beats']]
    else:
        # Edit map: one cue can span several shots (the same line held over a
        # cut). Collapse to unique cue spans first, or the same words get
        # carded once per shot.
        spans = []
        for frame in doc['frames']:
            for shot in frame['shots']:
                cue = shot['cue'].strip()
                if spans and spans[-1][2] == cue:
                    spans[-1][1] = shot['end']
                else:
                    spans.append([shot['start'], shot['end'], cue])

    segments, stubborn = [], []
    for start, end, cue in spans:
        cards = split_cue(cue)
        if not cards:
            continue
        span = end - start

        # Greedy packing leaves orphan remainders ("anxiety", "weather,") that
        # would flash for a third of a second. Merge the shortest card into a
        # neighbour and re-share until every card holds long enough to read,
        # or merging would overflow the box.
        for _ in range(40):
            if len(cards) < 2:
                break
            total = sum(len(c) for c in cards)
            shares = [span * len(c) / total for c in cards]
            i = min(range(len(cards)), key=lambda k: shares[k])
            if shares[i] >= MIN_SEC:
                break
            # Merge backwards where possible: these are continuations.
            j = i - 1 if i > 0 else i + 1
            lo, hi = min(i, j), max(i, j)
            joined = f'{cards[lo]} {cards[hi]}'
            if len(joined) <= HARD_MAX:
                cards[lo:hi + 1] = [joined]
                continue
            # Too long to merge. Rebalance instead: re-split the pair at the
            # word boundary nearest the middle, so neither half is an orphan.
            cut = joined.rfind(' ', 0, len(joined) // 2 + 1)
            a, b = joined[:cut], joined[cut + 1:]
            if cut <= 0 or max(len(a), len(b)) > HARD_MAX or [a, b] == cards[lo:hi + 1]:
                stubborn.append((round(shares[i], 2), cards[i]))
                break
            cards[lo:hi + 1] = [a, b]

        total = sum(len(c) for c in cards)
        t = start
        for i, c in enumerate(cards):
            b = end if i == len(cards) - 1 else t + span * len(c) / total
            segments.append([round(t * fps), round(b * fps), c])
            t = b

    json.dump({'fps': fps, 'segments': segments}, open(out_path, 'w'), indent=1)
    longest = max(segments, key=lambda s: len(s[2]))
    fast = [s for s in segments if (s[1] - s[0]) / fps < MIN_SEC]
    print(f'{len(spans)} cues -> {len(segments)} cards')
    print(f'longest card: {len(longest[2])} chars  "{longest[2]}"')
    print(f'cards under {MIN_SEC}s: {len(fast)}')
    for dur, text in stubborn:
        print(f'  could not merge (would overflow): {dur}s  "{text}"')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
