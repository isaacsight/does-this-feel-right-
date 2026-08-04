#!/usr/bin/env python3
"""Compose image prompts from a film's frame book.

STORYBOARD.md is the single source of truth for what is in every frame. This
reads it and emits production/prompts.json, injecting the per-act paper colour
and the style block so those exist in exactly one place. Hand-authoring the
prompt file separately guarantees the two drift, and then every art-direction
fix has to be applied twice.

Expected board shape:

    ## Act 4 - The numbers · pale olive `#E2E3CC` · ...
    ### 030a · 179.0s
    **Line:** "..."            (optional; carried for the record, not prompted)
    **Image:** the description, which may
    wrap across lines until a blank line.

Usage: python3 build-prompts.py <STORYBOARD.md> <out.json>
"""
import json
import pathlib
import re
import sys

# The invariants — true of EVERY frame of EVERY film. The world (palette,
# ground, light) is NOT here: it varies per film by house rule, and it is read
# from the film's own WORLD.md. Hardcoding one film's world into the shared
# tool is how three consecutive films ended up in the same cream world without
# anyone choosing it.
COMMON = (
    # The recurring character is deliberately NOT described here. An earlier
    # version hardcoded "the recurring character wears a red jacket..." into
    # every prompt. That was fine on a film where he was in most frames and
    # wrong on one with researchers, technicians and three mothers: it put him
    # into all 133 whether the board wanted him or not, so every researcher
    # came back as the protagonist. WHO is in a frame is the board's call;
    # this block carries only what is true of every frame.
    "Draw only the people the description names, and nobody else. "
    "NO text, NO labels, NO lettering, NO numerals, NO signage of any kind "
    "anywhere in the image. "
    "Fill the entire canvas edge to edge with the background colour - no "
    "border, no frame, no white margin, no inset panel. "
    "ONE single continuous scene from ONE camera - never a split panel, "
    "never a diptych, never side-by-side comparison boxes, never a grid of "
    "sub-images unless the description explicitly asks for one. 16:9."
)


def world_clause(board_path):
    """Read the locked world from the film's WORLD.md — the blockquote under
    '## The locked clause'. Refuse to guess: a film without a locked, tested
    world has not finished its art direction, and inventing one here would put
    an unvalidated world into every prompt at once."""
    w = pathlib.Path(board_path).parent / 'WORLD.md'
    if not w.exists():
        sys.exit(f'no {w} — lock and test the world before building prompts '
                 '(PRODUCTION-PLAYBOOK 10.33)')
    text = w.read_text()
    m = re.search(r'##\s*The locked clause\s*\n(.*?)(?:\n##|\Z)', text, re.S)
    if not m:
        sys.exit(f'{w} has no "## The locked clause" section')
    quoted = [l.lstrip('> ').rstrip() for l in m.group(1).split('\n')
              if l.strip().startswith('>')]
    clause = ' '.join(x for x in quoted if x).strip()
    if not clause:
        sys.exit(f'{w}: the locked clause blockquote is empty')
    return clause

# Two board shapes are supported, because the format changed when the frame
# book grew a motion column and the chairs started filing richer boards:
#
#   BLOCK  ### 030a · 179.0s      +  **Line:** / **Image:** fields
#   TABLE  ### ACT 1 — NAME · 0:00–0:58 · 12 frames
#          | # | Line | Hold | Motion | Information | Punchline | Scene |
#          | **b01** | "..." | 5.1 | STILL | ... | ... | <the scene> |
#
# The table form carries the motion mark, which the block form never had, so it
# is the one to prefer. Both are parsed rather than migrating old films.
ACT_RE = re.compile(r'^##\s+Act\s+(\d+)\s*[-–—]\s*(.+?)\s*·.*?`(#[0-9A-Fa-f]{6})`')
FRAME_RE = re.compile(r'^###\s+([0-9]{3}[a-h])\s*·')
TACT_RE = re.compile(r'^###\s+ACT\s+(\d+)\s*[-–—]\s*(.+?)\s*·')
TROW_RE = re.compile(r'^\|\s*\*\*(b\d+)\*\*\s*\|')


def parse_table(path):
    """Parse the table board. The SCENE column is the image description; the
    MOTION column is carried through so the Cinematographer can be handed the
    LIVE beats without re-reading the board."""
    act = act_name = None
    frames = []
    for raw in open(path):
        line = raw.rstrip('\n')
        m = TACT_RE.match(line)
        if m:
            act, act_name = int(m.group(1)), m.group(2).strip()
            continue
        if not TROW_RE.match(line):
            continue
        # Split on unescaped pipes, drop the empty edges.
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 7:
            sys.exit(f'{cells[0] if cells else line[:40]}: expected 7 columns, got {len(cells)}')
        fid = re.sub(r'\*+', '', cells[0]).strip()
        frames.append({
            'id': fid, 'act': act, 'act_name': act_name,
            'paper': None,                      # world is per-film now, not per-act
            'line': cells[1].strip().strip('*').strip('"').strip("'"),
            'hold': cells[2], 'motion': re.sub(r'\*+', '', cells[3]).strip(),
            'image': cells[6],
        })
    return frames


def parse(path):
    act = paper = act_name = None
    frames = []
    cur = None
    field = None

    for raw in open(path):
        line = raw.rstrip('\n')

        m = ACT_RE.match(line)
        if m:
            act, act_name, paper = int(m.group(1)), m.group(2), m.group(3)
            continue

        m = FRAME_RE.match(line)
        if m:
            if cur:
                frames.append(cur)
            if paper is None:
                sys.exit(f'frame {m.group(1)} appears before any act header')
            cur = {'id': m.group(1), 'act': act, 'act_name': act_name,
                   'paper': paper, 'line': '', 'image': ''}
            field = None
            continue

        if cur is None:
            continue

        if line.startswith('**Line:**'):
            cur['line'] = line.split('**Line:**', 1)[1].strip().strip('"')
            field = 'line'
        elif line.startswith('**Image:**'):
            cur['image'] = line.split('**Image:**', 1)[1].strip()
            field = 'image'
        elif line.strip() == '' or line.startswith('#') or line.startswith('---'):
            field = None
        elif field:
            # continuation of a wrapped field
            cur[field] += ' ' + line.strip()

    if cur:
        frames.append(cur)
    return frames


# The recurring character, described canonically. This is expanded wherever the
# board NAMES him, and nowhere else.
#
# Learned the hard way twice. Putting this in the style block forced him into
# all 133 frames of a film that also has researchers and three mothers, so every
# researcher came back as the protagonist. Removing it entirely was worse: the
# board only ever says "the person in the red jacket", the reference sheet alone
# did not hold him, and across 133 frames he drifted between bald, one tuft, a
# fringe, and two different head shapes. A reference is necessary and it is not
# sufficient - the words have to carry the design too, at the point of use.
CHARACTER = (
    "the person in the red jacket - a short round-headed adult, completely bald "
    "except for EXACTLY TWO short thin hairs sticking straight up from the crown "
    "of the head, small dot eyes with simple straight eyebrows, wearing a red zip "
    "jacket over a cream shirt, black trousers and cream shoes"
)


WORLD = None


# Production furniture that must never reach the image model. A frame book is
# written for the crew as much as for the generator: it carries plate
# filenames, continuity-group codes, LIVE class numbers and motion direction.
# All of it is instruction ABOUT the frame, not content IN it — and a model
# handed "G1 · Live L1 · class 1" will cheerfully letter it into the picture,
# which is the same failure as a hex code coming back drawn as text.
FURNITURE = [
    # Production furniture, stripped AFTER references are resolved. Every
    # pattern is word-bounded on BOTH sides: an earlier version used
    # r'\bAnchor\s*' which matched inside "Anchored to", leaving a frame
    # description that began "ed to ." — 15 of 88 prompts were damaged that
    # way, and the damage is invisible unless you read the prompts rather than
    # the frame count.
    r'\bG\d+[a-z]?\b\s*·?\s*',                  # continuity group codes (G1, G3b)
    r'\bLive\s+L\d+\b\s*·?\s*class\s*\d+\.?',  # LIVE class markers
    r'\bAnchored?\b\s+(?:to|on)?\s*',           # "Anchor", "Anchored to"
    r'\bPlate\b\s*',
    r'Establishing wide \d+ of \d+\.?',
    r'Field composition\.?',
    r'\*?What moves:\*?.*$',
    r'Motion starts after the cut[^.]*\.',
    r'Image-to-video from the approved still\.?',
    r'\bDRIFT:[^.]*\.',
]

# A clause that points at another frame or a plate file is meaningless to an
# image model — "same horizon height as b57" tells it nothing it can act on.
# Delete the whole clause rather than the token, or the prompt is left with
# "same horizon height as ." Applied before FURNITURE so the connective goes
# with its object.
# Cross-references and plate names are meaningless to an image model, but they
# sit INSIDE sentences that carry real content. An earlier version deleted the
# whole clause containing them and took the sentence's SUBJECT with it:
#
#   b37  "The protagonist crouched at eye level with it..."  ->  "at eye level with it..."
#   b41  "One figure holding out the block, the other taking it"  ->  "the other taking it"
#
# That damaged 19 of 88 prompts — worse than the 15 the previous bug damaged —
# and it shipped because the fix was spot-checked on four prompts instead of
# verified on all of them. Remove the REFERENCE PHRASE ONLY. "same horizon
# height as b57" -> "same horizon height" is harmless filler; losing the
# subject is not.
REFERENCE = [
    r'\s*(?:,\s*)?\b(?:as|to|in|at|from|with|than|like)\s+`?b\d+`?\b',  # "as b57"
    r'\s*`?b\d+`?\b',                                       # a bare frame id
    r'\s*`[^`]*\.png`',                                      # a plate filename
    r'\s*\bas reference #\d+',
]

# Notes written for the crew that must never reach the model. Whole sentences,
# not clauses — these stand alone and carry no scene content.
ANNOTATION = [
    # NOTE the lazy run-to-next-capital rather than [^.]*\. — "Hold risk: below
    # the 1.8s floor" contains a decimal point, so a period-terminated pattern
    # stops inside the number and leaves "8s floor - see §8." in the prompt.
    r'Hold risk:.*?(?=\s+[A-Z]|$)',
    r'Still by ruling.*?(?=\s+[A-Z]|$)',
    r'See\s*§\s*\d+.*?(?=\s+[A-Z]|$)',
    r'\bAccepted risk.*?(?=\s+[A-Z]|$)',
    r'\bFallback.*?(?=\s+[A-Z]|$)',
    # Sentences that exist only to name a plate or its provenance.
    r'[—-]?\s*this frame (?:is|establishes)[^.]*\.',
    r'\bDoubles as production frame[^.]*\.',
    r'On the measured read[^.]*\.',
    r'\bthis should be the (?:longest|shortest)[^.]*\.',
]


# A frame that describes itself as "identical framing to b07" is unbuildable:
# the model has never seen b07 and cannot follow a pointer. The board writes
# these deliberately - it is how continuity groups are expressed to a human -
# so resolve them by INLINING the referenced frame's description, then letting
# the local modification ("hands lowered to the figure's sides") apply on top.
# Stripping the reference instead leaves "Identical framing to , hands
# lowered", which is worse than either.
XREF = re.compile(r'(?:identical framing to|same composition as|composition is '
                  r'reused exactly at|same framing as)\s*`?(b\d+)`?', re.I)


def resolve_xrefs(frames):
    by_id = {f['id']: f for f in frames}
    for f in frames:
        m = XREF.search(f['image'])
        if not m:
            continue
        src = by_id.get(m.group(1))
        if not src:
            sys.exit(f"{f['id']}: references {m.group(1)}, not in the board")
        if XREF.search(src['image']):
            sys.exit(f"{f['id']} -> {m.group(1)}: chained reference; the board must "
                     "anchor to a frame that stands on its own")
        f['image'] = src['image'].rstrip(' .') + '. ' + XREF.sub('Same framing', f['image'], count=1)
        f['xref'] = m.group(1)
    return frames


def compose(f):
    """Strip the board's own emphasis markers and production furniture - they
    are notes to a human reader and mean nothing to an image model."""
    img = re.sub(r'\*\*(.+?)\*\*', r'\1', f['image'])
    img = re.sub(r'\*(.+?)\*', r'\1', img)
    for pat in ANNOTATION:
        img = re.sub(pat, ' ', img, flags=re.I)
    for pat in REFERENCE:
        img = re.sub(pat, '', img, flags=re.I)
    # Removing what a preposition pointed at strands the preposition:
    # "Same tread dimensions as `stair.png`." -> "Same tread dimensions as."
    # "seated as in `b61`, alone now"          -> "seated as, alone now"
    img = re.sub(r'\s+\b(?:as|to|at|in|from|than|with|like|on)\b\s*(?=[.,;])', '', img, flags=re.I)
    img = re.sub(r'\s+\bas\b\s*(?=[.,;])', '', img, flags=re.I)
    img = img.replace('`', ' ')
    for pat in FURNITURE:
        img = re.sub(pat, ' ', img, flags=re.I | re.M)
    img = re.sub(r',\s*\.', '.', img)                  # "Same field,." -> "Same field."
    img = re.sub(r'\s*([,.;])\s*\1+', r'\1', img)     # ",." / ".." from removals
    # A sentence reduced to "Same field." no longer says what it matches, so it
    # is noise rather than instruction. Drop the fragment, keep the rest.
    img = re.sub(r'(?:^|(?<=\. ))(?:Same|Identical)\s+\w+(?:\s+\w+)?\.\s*', '', img)
    # A sentence reduced to a stub by the removals above ("Anchor.", "+.",
    # "this frame is the, generated from.") is noise, not instruction. Rebuild
    # from the sentences that still carry content.
    keep = []
    for s in re.split(r'(?<=[.!?])\s+', img):
        core = re.sub(r'[^A-Za-z ]', ' ', s)
        words = [w for w in core.split() if len(w) >= 2]
        s = s.strip()
        if len(words) >= 2 and re.match(r'^[A-Z0-9"\']', s):
            keep.append(s)
    img = ' '.join(keep)
    # STRAND: "seated as, alone now" — the reference the preposition pointed at
    # is gone. Run after the rebuild as well as before it, because a rebuild
    # can re-join sentences and expose new strands.
    img = re.sub(r'\s*\b(?:as|to|at|in|from|than|with|like|on)\b\s*(?=[.,;])', '', img, flags=re.I)
    img = re.sub(r'^[\s,.;—-]+', '', img)
    img = re.sub(r'\s+([,.;])', r'\1', img)
    img = re.sub(r'\s{2,}', ' ', img).strip(' .·—-') + '.' 
    # An ALL-CAPS motif name reads to the generator as a label to letter in.
    img = re.sub(r'\b[A-Z]{3,}(?:\s+[A-Z]{3,})*\b',
                 lambda m: m.group(0).capitalize(), img).strip()
    # Expand the character at first mention only; later mentions in the same
    # frame stay short so the prompt does not become a list of his clothes.
    if re.search(r'the person in the red jacket', img, re.I):
        img = re.sub(r'the person in the red jacket', CHARACTER, img, count=1, flags=re.I)
    return f"{img} {WORLD} {COMMON}"


def verify(frames, prompts):
    """Check EVERY prompt before anything is written. Two bugs shipped from
    this file because a fix was spot-checked on a handful of prompts and
    declared clean — the first damaged 15 of 88, the second 19 of 88, and both
    produced frames that looked plausible and were wrong. A sample cannot
    clear a transform that runs on all of them.

    The content-retention check is the one that matters: it compares the
    composed scene against the board's own words and fails when the transform
    has eaten the description. Both historical bugs would have tripped it."""
    bad = []
    for f in frames:
        fid = f['id']
        scene = prompts[fid].split(WORLD)[0].strip() if WORLD in prompts[fid] else prompts[fid]

        # 1. Production furniture that must never survive.
        for pat, label in [(r'`', 'backtick'), (r'\bb\d{2}\b', 'frame ref'),
                           (r'\bG\d+[a-z]?\b', 'group code'), (r'\.png', 'plate file'),
                           (r'reference #', 'reference marker'),
                           (r'Hold risk|See §|What moves', 'QA prose')]:
            if re.search(pat, scene):
                bad.append((fid, f'{label} survived: ...{scene[max(0,re.search(pat,scene).start()-30):][:60]}'))

        # 2. A description that lost its subject reads as a fragment.
        if scene and not re.match(r'^[A-Z0-9"\']', scene):
            bad.append((fid, f'starts mid-sentence: "{scene[:50]}"'))
        if re.match(r'^(?:at|in|on|the other|then|and|but|with|from|as)\b', scene, re.I):
            bad.append((fid, f'starts with a fragment: "{scene[:50]}"'))

        # 3. Punctuation left dangling by a removal.
        for pat, label in [(r'\s[,.;]', 'space before punctuation'), (r'[,;]\s*\.', 'orphaned comma'),
                           (r'\s{2,}', 'double space'), (r'\b(?:as|to|at|from|than)\s*[.,]', 'dangling preposition')]:
            if re.search(pat, scene):
                bad.append((fid, f'{label}'))

        # 4. CONTENT RETENTION - the check that catches a transform eating the
        #    description. Compare against the board's raw scene text.
        raw = re.sub(r'[*`]', '', f['image'])
        for pat in ANNOTATION + FURNITURE + REFERENCE:
            raw = re.sub(pat, ' ', raw, flags=re.I | re.M)
        raw_words = set(w.lower() for w in re.findall(r"[A-Za-z']{4,}", raw))
        got_words = set(w.lower() for w in re.findall(r"[A-Za-z']{4,}", scene))
        if raw_words:
            kept = len(raw_words & got_words) / len(raw_words)
            # Deliberately loose. The PRECISE checks are the fragment tests
            # above — they caught both real bugs by name. This is a backstop
            # for catastrophic loss, and it has to tolerate crew commentary
            # the annotation list cannot enumerate exhaustively.
            if kept < 0.55:
                bad.append((fid, f'lost {100*(1-kept):.0f}% of the board\'s words '
                                 f'({len(raw_words & got_words)}/{len(raw_words)} kept)'))
    return bad


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)

    frames = resolve_xrefs(parse_table(sys.argv[1]) or parse(sys.argv[1]))
    if not frames:
        sys.exit('no frames parsed - check the board headings')
    globals()['WORLD'] = world_clause(sys.argv[1])

    missing = [f['id'] for f in frames if not f['image']]
    if missing:
        sys.exit(f'frames with no **Image:** description: {missing}')

    dupes = {f['id'] for f in frames if [x['id'] for x in frames].count(f['id']) > 1}
    if dupes:
        sys.exit(f'duplicate frame ids: {sorted(dupes)}')

    prompts = {f['id']: compose(f) for f in frames}

    problems = verify(frames, prompts)
    if problems:
        print(f'\nVERIFY FAILED - {len(problems)} problem(s) across '
              f'{len({p[0] for p in problems})} of {len(frames)} prompts. '
              f'Nothing written.\n')
        for fid, why in problems:
            print(f'  {fid}  {why}')
        sys.exit(1)
    print(f'verify: all {len(frames)} prompts clean')

    json.dump(prompts, open(sys.argv[2], 'w'), indent=2)

    meta = sys.argv[2].replace('.json', '-meta.json')
    json.dump(frames, open(meta, 'w'), indent=2)

    by_act = {}
    for f in frames:
        by_act.setdefault((f['act'], f['act_name']), []).append(f)
    print(f'{len(frames)} prompts -> {sys.argv[2]}')
    for (a, n), fs in sorted(by_act.items()):
        marks = {}
        for f in fs:
            k = (f.get('motion') or 'STILL').split()[0]
            marks[k] = marks.get(k, 0) + 1
        m = ' '.join(f'{k}:{v}' for k, v in sorted(marks.items()))
        print(f'  Act {a} {n[:34]:<34} {len(fs):>3} frames   {m}')
    live = [f['id'] for f in frames if 'LIVE' in (f.get('motion') or '')]
    if live:
        print(f'  LIVE beats: {live}')
    xr = [(f['id'], f['xref']) for f in frames if f.get('xref')]
    if xr:
        print(f'  cross-references resolved by inlining: {xr}')
