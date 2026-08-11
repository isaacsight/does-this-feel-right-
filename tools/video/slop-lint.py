#!/usr/bin/env python3
"""Slop lint — the humanity gate. Law 15 (Isaac, 2026-08-11: "the writing
needs to feel more human — it's already great, slight improvement").

The register gate measures ADDRESS (you/we, contractions, sentence weight).
This gate measures MACHINERY — the die-stamps that make good writing read as
generated. Each check was calibrated against the four shipped catalog
scripts, which Isaac rates "pretty great, needs slight improvement": the caps
sit just under what those scripts do, so every future script must be slightly
more human than the catalog's average, forever.

WHAT IT CATCHES (fix the script, never the caps):
  SNAP TEMPLATE   "X isn't Y. It's Z." — the reversal die-stamp. Good twice,
                  machinery at six.
  SIGNPOST TIC    the same attention phrase reused ("Here's the...", "Sit
                  with that") — signposting is FOR the ear (VO law), so
                  variety is required, not absence.
  TRIPLET METER   comma-lists of exactly three, over and over. Humans list
                  two things, or four, or one.
  HOUSE WORDS     quietly/quiet, small — the corpus watermark.
  EPIGRAM CLOSES  every act ending on a short aphorism. At least three acts
                  must end on a fact, an image, or a number.
  EVEN ACTS       act lengths too uniform. Human essays are lopsided.
  FRICTION (warn) at least one controlled imperfection — a self-interruption
                  ("Well — "), a correction ("or rather", "call it"), an
                  aside. Slop is frictionless; humans snag.

Usage: python3 slop-lint.py <script.txt> [--gate]
"""
import re, sys, statistics

path = sys.argv[1]
text = open(path).read().strip()
acts = [a.strip() for a in re.split(r'\n\s*\n', text) if a.strip()]
words = re.findall(r"[A-Za-z']+", text)
n = len(words)

checks = []   # (name, value, cap, direction, detail)

# 1. SNAP TEMPLATE — "isn't/not/never X. It's/That's/They're Y."
snaps = re.findall(r"\b(?:isn't|not|never)\s+[^.!?]{2,60}[.!?]\s+(?:It's|That's|They're|It was|That was)\b", text)
checks.append(('snap_template', len(snaps), 4, '<=', '; '.join(s[:40] for s in snaps[:6])))

# 2. SIGNPOST TIC — identical signpost phrases reused.
SIGNS = [r"here's the", r"and here's", r"read that again", r"sit with that",
         r"say (?:it|that) again", r"look at (?:what|the)", r"the part that matters",
         r"hold (?:that|onto)"]
worst, worst_n = '', 0
for s in SIGNS:
    c = len(re.findall(s, text, re.I))
    if c > worst_n: worst, worst_n = s, c
checks.append(('signpost_repeat', worst_n, 2, '<=', f'"{worst}" x{worst_n}'))

# 3. TRIPLET METER — lists of exactly three vs all lists.
lists = re.findall(r'\b\w[\w\s]{0,24}?,\s+(?:the\s+)?\w[\w\s]{0,24}?,\s+(?:and|or)\s+', text)
all_lists = re.findall(r'\b\w[\w\s]{0,24}?,\s+(?:the\s+)?\w[\w\s]{0,24}?,(?:\s+(?:the\s+)?\w[\w\s]{0,24}?,)*\s+(?:and|or)\s+', text)
share = len(lists) / max(1, len(all_lists))
checks.append(('triplet_count', len(lists), 6, '<=', f'{len(lists)} triplets of {len(all_lists)} lists'))

# 4. HOUSE WORDS.
q = len(re.findall(r'\bquiet(?:ly)?\b', text, re.I))
sm = len(re.findall(r'\bsmall\b', text, re.I))
checks.append(('quietly', q, 2, '<=', f'{q} uses'))
checks.append(('small', sm, 5, '<=', f'{sm} uses'))

# 5. EPIGRAM CLOSES — acts ending on a short numberless aphorism.
def is_epigram(act):
    last = re.split(r'(?<=[.!?])\s+', act)[-1]
    w = re.findall(r"[A-Za-z']+", last)
    return len(w) <= 12 and not re.search(r'\d', last)
epi = sum(1 for a in acts if is_epigram(a))
non_epi = len(acts) - epi
checks.append(('non_epigram_closes', non_epi, 3, '>=', f'{epi}/{len(acts)} acts end on an epigram'))

# 6. EVEN ACTS — coefficient of variation of act lengths.
lens = [len(re.findall(r"[A-Za-z']+", a)) for a in acts]
cv = statistics.pstdev(lens) / statistics.mean(lens)
checks.append(('act_length_cv', round(cv, 3), 0.18, '>=', f'act words {min(lens)}-{max(lens)}'))

# 7. FRICTION (warn only) — controlled imperfection present.
friction = len(re.findall(r'\bWell\s+—|—\s*(?:no|or rather|call it|sorry)\b|\bactually,\b', text, re.I))
has_friction = friction >= 1

print(f'\nSLOP LINT — {path}   ({n} words, {len(acts)} acts)\n')
fails = []
for name, val, cap, d, detail in checks:
    ok = (val <= cap) if d == '<=' else (val >= cap)
    if not ok: fails.append(name)
    print(f'  {"pass" if ok else "FAIL"}  {name:<20} {val:>6}   {"cap" if d=="<=" else "floor"} {cap}   {detail}')
print(f'  {"pass" if has_friction else "warn"}  {"friction":<20} {friction:>6}   floor 1   controlled imperfection (warn only)')

if fails:
    print(f'\n{len(fails)} MACHINERY BREACH(ES) — fix the script, not the caps.\n')
    sys.exit(1 if '--gate' in sys.argv else 0)
print('\nHuman enough. Cleared.\n')
