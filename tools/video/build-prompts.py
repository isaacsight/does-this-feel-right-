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
import re
import sys

STYLE = (
    "Flat mid-century comic line art. Clean black outlines of even weight. "
    "Flat solid colour fills only - no halftone dots, no stipple, no gradients, "
    "no texture. Plain cream #F4E8C8 background. Ink is near-black #1F1E1D. "
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

ACT_RE = re.compile(r'^##\s+Act\s+(\d+)\s*[-–—]\s*(.+?)\s*·.*?`(#[0-9A-Fa-f]{6})`')
FRAME_RE = re.compile(r'^###\s+([0-9]{3}[a-h])\s*·')


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


def compose(f):
    """Strip the board's own emphasis markers - they are notes to a human
    reader and mean nothing to an image model."""
    img = re.sub(r'\*\*(.+?)\*\*', r'\1', f['image'])
    # An ALL-CAPS motif name reads to the generator as a label to letter in.
    img = re.sub(r'\b[A-Z]{3,}(?:\s+[A-Z]{3,})*\b',
                 lambda m: m.group(0).capitalize(), img).strip()
    # Expand the character at first mention only; later mentions in the same
    # frame stay short so the prompt does not become a list of his clothes.
    if re.search(r'the person in the red jacket', img, re.I):
        img = re.sub(r'the person in the red jacket', CHARACTER, img, count=1, flags=re.I)
    return f"{img} {STYLE.format(paper=f['paper'])}"


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)

    frames = parse(sys.argv[1])
    if not frames:
        sys.exit('no frames parsed - check the board headings')

    missing = [f['id'] for f in frames if not f['image']]
    if missing:
        sys.exit(f'frames with no **Image:** description: {missing}')

    dupes = {f['id'] for f in frames if [x['id'] for x in frames].count(f['id']) > 1}
    if dupes:
        sys.exit(f'duplicate frame ids: {sorted(dupes)}')

    json.dump({f['id']: compose(f) for f in frames},
              open(sys.argv[2], 'w'), indent=2)

    meta = sys.argv[2].replace('.json', '-meta.json')
    json.dump(frames, open(meta, 'w'), indent=2)

    by_act = {}
    for f in frames:
        by_act.setdefault((f['act'], f['act_name'], f['paper']), []).append(f['id'])
    print(f'{len(frames)} prompts -> {sys.argv[2]}')
    for (a, n, p), ids in sorted(by_act.items()):
        print(f'  Act {a} {n:<28} {p}  {len(ids):>3} frames')
