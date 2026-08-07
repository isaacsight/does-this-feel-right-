#!/usr/bin/env python3
"""Profile the reading level and vocabulary of narration, so a new script can be
written to a measured register instead of a remembered impression.

Built to compare a reference corpus (e.g. a channel's transcript archive)
against our own locked script. Two classes of metric, deliberately separated:

  VOCABULARY  — reliable on any text, punctuated or not. Syllables per word,
                share of 3+ syllable words, mean word length, type/token ratio,
                and second-person density (how much the script addresses "you").

  SENTENCE    — needs real punctuation. YouTube auto-captions have none, so
                these are computed ONLY over texts that actually carry it, and
                the sample size is reported. Never average a reading grade over
                unpunctuated ASR: words-per-sentence becomes words-per-file and
                the grade level is meaningless.

Usage: python3 register-profile.py <label> <glob> [<label> <glob> ...]
"""
import glob as globmod
import re
import sys

VOWELS = 'aeiouy'
SECOND_PERSON = {'you', "you're", 'your', 'yours', "you've", "you'll", 'yourself'}
FIRST_PLURAL = {'we', "we're", 'our', 'ours', "we've", "we'll", 'us', 'ourselves'}


def syllables(word):
    """Vowel-group heuristic. Not perfect; consistent, which is what matters
    when the number is only ever used comparatively."""
    w = re.sub(r"[^a-z]", '', word.lower())
    if not w:
        return 0
    groups = re.findall(r'[aeiouy]+', w)
    n = len(groups)
    if w.endswith('e') and n > 1 and not w.endswith(('le', 'ee', 'ye')):
        n -= 1
    return max(1, n)


def clean(text):
    """Strip transcript furniture: front matter, minute stamps, markdown."""
    text = re.sub(r'^.*?^---\s*$', '', text, flags=re.S | re.M)
    text = re.sub(r'\*\*\[\d+:\d+\]\*\*', ' ', text)
    text = re.sub(r'\[[^\]]*\]\([^)]*\)', ' ', text)
    text = re.sub(r'[*#>`|]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def profile(label, paths):
    words, sylls, poly, types = 0, 0, 0, set()
    second, first = 0, 0
    sent_words, sent_sylls, sentences, punctuated_files = 0, 0, 0, 0
    files = 0

    for p in paths:
        try:
            raw = open(p, errors='ignore').read()
        except OSError:
            continue
        body = clean(raw)
        toks = re.findall(r"[A-Za-z']+", body)
        if len(toks) < 50:
            continue
        files += 1

        for t in toks:
            s = syllables(t)
            words += 1
            sylls += s
            if s >= 3:
                poly += 1
            types.add(t.lower())
            lw = t.lower()
            if lw in SECOND_PERSON:
                second += 1
            elif lw in FIRST_PLURAL:
                first += 1

        # Sentence metrics only where punctuation genuinely exists.
        marks = len(re.findall(r'[.!?]', body))
        if marks / max(len(toks), 1) > 0.01:
            punctuated_files += 1
            sentences += marks
            sent_words += len(toks)
            sent_sylls += sum(syllables(t) for t in toks)

    if not words:
        print(f'{label}: no usable text')
        return

    spw = sylls / words
    print(f'\n=== {label}')
    print(f'  files {files:>5}   words {words:>9,}   vocabulary {len(types):>7,}')
    print(f'  VOCABULARY')
    print(f'    syllables/word        {spw:6.2f}')
    print(f'    3+ syllable words     {100*poly/words:6.1f}%')
    print(f'    type/token (lex var)  {len(types)/words:6.4f}')
    print(f'    "you" per 1k words    {1000*second/words:6.1f}')
    print(f'    "we" per 1k words     {1000*first/words:6.1f}')

    if sentences:
        wps = sent_words / sentences
        s2 = sent_sylls / sent_words
        ease = 206.835 - 1.015 * wps - 84.6 * s2
        grade = 0.39 * wps + 11.8 * s2 - 15.59
        print(f'  SENTENCE  (from {punctuated_files} punctuated file(s) only)')
        print(f'    words/sentence        {wps:6.1f}')
        print(f'    Flesch reading ease   {ease:6.1f}')
        print(f'    Flesch-Kincaid grade  {grade:6.1f}')
    else:
        print('  SENTENCE  — no punctuated source; not computed')


# ---------------------------------------------------------------- the gate --
#
# THE HOUSE BAND, measured 2026-08-04 against 997 School of Life transcripts
# (963k words), 10 Modern Wisdom transcripts, and our own three films.
#
# The corpora sit at opposite ends of the address axis and neither is us:
#
#                    you/1k   we/1k    syll/wd   FK grade
#   School of Life     13.8    38.8       1.49        8.9   confesses, literary
#   Modern Wisdom      34.7    11.2       1.39        6.3   addresses, conversational
#   OUR FILMS          49.2     7.9       1.33        6.2   accuses, plain
#
# Two things that band is built to prevent, both of which actually happened:
#
#   1. The RITUALS failure - a script with "you" ZERO times in 1,043 words,
#      the likeliest cause of two "I got lost watching it" rejections. Hence a
#      FLOOR on "you".
#   2. The over-correction - `you-are-not-finished` measured 65.5 "you" per 1k
#      and "we" EXACTLY ZERO. A film that only ever accuses is a lecture. The
#      house line is "you accuses, we confesses", and the honest beat this
#      publication is built on cannot be written without "we". Hence a FLOOR on
#      "we" and a CEILING on "you".
#
# The band is centred on the two films whose narration was judged good, not on
# either corpus - we are not trying to become School of Life, we are trying to
# stay ourselves on purpose rather than by accident.
# REVISED 2026-08-05, and the reason matters more than the numbers.
#
# The previous band was measured from OUR OWN THREE FILMS and then enforced as a
# rule. That is circular: it described what we were doing and made us keep doing
# it. Two of those three films have since been shelved as not good, and Isaac's
# note on the third was "I don't know what this is about." The band was locking in
# the register of films that did not work.
#
# What he actually wants: "when I listen to podcasts and School of Life it feels
# like I'm there with them." Same room. That register is not what we had.
#
# Three changes, all pointed at the room rather than at the lectern:
#
# CONTRACTIONS, newly measured and newly enforced. Every film before this ran at
# 0.0 to 2.4 per 1k. We were writing WRITTEN ENGLISH and having it read aloud —
# "it is not fraud and it is not sloppiness" is a sentence nobody has said in a
# room. This is the single biggest lever on the same-room feel and it was
# invisible because nothing measured it.
#
# The band is MEASURED, not guessed. First attempt used 12-34 from an assumption
# that "natural speech runs 15-30", which was never checked against anything:
#     School of Life   1,001 files, 990,682 words   22.6 / 1k   (scripted)
#     Modern Wisdom       10 files,  90,128 words   43.2 / 1k   (unscripted)
# So 20-46 spans a written-to-be-heard essay at one end and real podcast talk at
# the other. A first draft written to this rule came in at 65.8, which is looser
# than unscripted conversation — the lesson cuts both ways.
#
# WE over YOU. School of Life sits at we 38.8 / you 13.8 and feels like company;
# we sat at the inverse and feel like a lecture. "You" accuses from a distance,
# "we" sits beside. The floor on `we` goes up hard and the floor on `you` comes
# down.
#
# LONGER SENTENCES ARE ALLOWED. School of Life runs 17.3 words at grade 8.9 and is
# perfectly easy to listen to. Clipped declaratives read as pronouncements.
BAND = {
    'you_per_1k':          (15.0, 45.0),
    'we_per_1k':           (18.0, 45.0),
    'contractions_per_1k': (20.0, 46.0),
    'syllables_word':      (1.26, 1.45),
    'words_sentence':      (13.0, 20.0),
    'flesch_ease':         (70.0, 84.0),
    'fk_grade':            (5.6,  8.2),
}


def gate(path):
    """Measure one script against the house band. Exit 1 on any breach."""
    # Reuse the module's own reader and tokeniser rather than inventing
    # parallel ones — a gate that measures text differently from the profiler
    # is a gate measuring a different script.
    body = clean(open(path, errors='ignore').read())
    words = [w.lower() for w in re.findall(r"[A-Za-z']+", body)]
    n = len(words)
    if not n:
        sys.exit(f'{path}: no words')
    second = sum(1 for w in words if w in SECOND_PERSON)
    first = sum(1 for w in words if w in FIRST_PLURAL)
    sylls = sum(syllables(w) for w in words)
    sents = [s for s in re.split(r'[.!?]+', body) if s.strip()]
    wps = n / max(1, len(sents))
    s2 = sylls / n

    got = {
        'you_per_1k':     1000 * second / n,
        # Apostrophe-'s is BOTH a contraction and a possessive, and the first
        # version of this counted "somebody's face" and "Bartlett's students" as
        # speech. It read 67/1k on a script that actually sits near 40. Count the
        # unambiguous suffixes anywhere, and 's only after the pronouns and
        # function words where it can only be a contraction.
        'contractions_per_1k': 1000 * (
            len(re.findall(r"\b\w+n't\b|\b\w+'(?:re|ve|ll|m)\b", body, re.I))
            + len(re.findall(
                r"\b(?:it|that|there|here|what|who|he|she|let|this|"
                r"how|where|why|one|nobody|somebody|everybody)'s\b", body, re.I))
            + len(re.findall(r"\b(?:i|you|we|they|he|she|it|that|there)'d\b", body, re.I))
        ) / n,
        'we_per_1k':      1000 * first / n,
        'syllables_word': s2,
        'words_sentence': wps,
        'flesch_ease':    206.835 - 1.015 * wps - 84.6 * s2,
        'fk_grade':       0.39 * wps + 11.8 * s2 - 15.59,
    }

    print(f'\nREGISTER GATE — {path}   ({n} words, {len(sents)} sentences)\n')
    fails = []
    for k, (lo, hi) in BAND.items():
        v = got[k]
        ok = lo <= v <= hi
        if not ok:
            fails.append((k, v, lo, hi))
        print(f'  {"pass" if ok else "FAIL"}  {k:<16} {v:7.2f}   band {lo}–{hi}')

    if not fails:
        print('\nIn band. Cleared for boarding.\n')
        return 0
    print(f'\n{len(fails)} BREACH(ES) — fix the script, not the band:\n')
    for k, v, lo, hi in fails:
        direction = 'below' if v < lo else 'above'
        note = {
            'contractions_per_1k': ("this reads as WRITTEN english, not speech. "
                "Every film before 2026-08-05 ran 0.0-2.4 per 1k against 15-30 in "
                "natural talk. 'It is not fraud' is not a sentence anyone says out "
                "loud; 'it's not fraud' is. This is the biggest single lever on "
                "sounding like you are in the room"),
            'you_per_1k': ('too little direct address — the rituals failure, and '
                           'the likeliest cause of "I got lost watching it"'
                           if v < lo else
                           'relentless accusation — every sentence points at the viewer'),
            'we_per_1k': ('the film never confesses. "you" accuses, "we" confesses; '
                          'a film with no "we" is a lecture'
                          if v < lo else 'so much "we" the argument goes soft'),
        }.get(k, 'outside the measured house register')
        print(f'  {k}: {v:.2f} is {direction} {lo}–{hi} — {note}')
    print()
    return 1


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--gate':
        if len(args) != 2:
            sys.exit('usage: register-profile.py --gate <script.txt>')
        sys.exit(gate(args[1]))
    if len(args) < 2 or len(args) % 2:
        sys.exit(__doc__)
    for i in range(0, len(args), 2):
        profile(args[i], sorted(globmod.glob(args[i + 1])))
