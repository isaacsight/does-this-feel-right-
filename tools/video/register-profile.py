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


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 2 or len(args) % 2:
        sys.exit(__doc__)
    for i in range(0, len(args), 2):
        profile(args[i], sorted(globmod.glob(args[i + 1])))
