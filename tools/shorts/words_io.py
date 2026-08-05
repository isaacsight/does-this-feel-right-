"""One reader for audio/words.json, because three shapes exist in this repo.

The older films wrote {"words": [{"w","s","e"}]}. tools/video/narrate-acts.mjs
writes a bare list of {"word","start","end"}. And pick-spans.py internally mixes
the two namings — sentences() reads w['w'] while --list reads w['start'].

Rather than rewrite finished films' artifacts or the producer that map-shots.py
depends on, normalise once, here, and hand back words carrying BOTH namings.
"""
import json
from pathlib import Path


def load_words(film):
    raw = json.load(open(Path(film) / 'audio' / 'words.json'))
    items = raw['words'] if isinstance(raw, dict) else raw
    out = []
    for x in items:
        w = x.get('w', x.get('word'))
        s = x.get('s', x.get('start'))
        e = x.get('e', x.get('end'))
        out.append({'w': w, 's': s, 'e': e, 'word': w, 'start': s, 'end': e})
    return out
