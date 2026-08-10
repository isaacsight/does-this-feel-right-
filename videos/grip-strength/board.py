#!/usr/bin/env python3
"""Motion board — Your Grip Is a Crystal Ball. First all-motion piece.

Every shot is a fal.ai clip generated from a gated keyframe, so a row here
carries BOTH halves: the keyframe prompt (what the frame is) and the motion
prompt (the ONE thing that moves). The stills catalog's lessons carry over
where they apply; the ones that don't transfer are replaced, not ignored:

  CARRIED    camera-as-crop; counts-not-nouns; self-reference ban; f-string
             brace check; absences described as present states; sign-shaped
             objects drawn markless (dial faces are ticks-only — type lands
             in post, never generated).
  REPLACED   the face-action gate. The stills films star a face; this world
             stars hands and instruments. Its replacement is THE MOVER GATE:
             every clip row names exactly one mover, the mover appears in the
             keyframe scene, and wherever the mover is an instrument it is
             the SIGNAL ORANGE thing — orange is how the i2v model is told
             what moves.
  NEW        motion hierarchy (5 BIG moves, never adjacent, everything else
             ambient); DATA FRAMES STAY STILL in an all-motion film — the
             measured rule ("the model redraws data wrong") gets sharper
             here, so data rows generate no clip at all and any motion on
             them is deterministic in assembly; duration budget (clip seconds
             must cover the narration hold they will be trimmed to).

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent
WPM = 161.0  # measured house narration rate

HAND = ("a single warm-skinned human hand, drawn bold and simplified in flat "
        "graphic motion-design style, the only organic thing in the picture")

CAM = {
 'XCU':   ("EXTREME CLOSE-UP, the camera pushed right in: the subject FILLS THE ENTIRE "
           "FRAME and is CROPPED HARD by all four edges."),
 'CU':    ("CLOSE-UP: the subject FILLS THE FRAME with generous dark space around it, "
           "centred or third-anchored."),
 'MED':   "MEDIUM SHOT: the subject sits large in the frame with the dark field around it.",
 'WIDE':  "WIDE SHOT: the subject is small against a VAST dark field.",
}

# (line, cam, setting, mclass, secs, mover, scene)
#   mclass: 'big:<class>' | 'ambient' | 'data' (data rows generate NO clip)
#   mover:  the ONE thing that moves, phrased exactly as the motion prompt
S = [
# ACT 1 — the squeeze and the claim -----------------------------------------
(1,"CU","instrument","big:thesis",5,
 "the hand slowly closes around the handle while the orange needle sweeps up the dial and stops",
 f"{HAND} closing around the steel handle of a hand dynamometer, tendons rising, while an "
 f"oversized round dial behind it shows one luminous SIGNAL ORANGE needle risen mid-sweep, "
 f"the dial face marked with plain tick marks only, all on a deep ink-blue-black field."),
(2,"XCU","instrument","ambient",5,
 "the slim orange needle quivers minutely at its peak, staying the same slim shape",
 "An oversized dial face filling the frame, plain tick marks and one luminous SIGNAL ORANGE "
 "needle standing at its peak, a faint glow around the needle tip, on a deep ink-blue-black "
 "field."),
(3,"CU","instrument","data",4,
 "none",
 "The same dial face, needle frozen at its peak, with a wide BLANK bone-white plate below "
 "the pivot where a reading would sit, everything still, on a deep ink-blue-black field."),
# ACT 2 — the two studies and grandpa ---------------------------------------
(4,"WIDE","field","data",6,
 "none",
 "A VAST deep ink-blue-black field holding a single row of SEVENTEEN small bone-white "
 "circles evenly spaced across the width, each drawn as a plain open ring, fine film grain."),
(5,"MED","instrument","big:reveal",5,
 "the blood pressure cuff slowly deflates and slumps while the orange needle beside it rises",
 "A clinical blood-pressure cuff with its rubber bulb, drawn bold and simplified in steel "
 "grey, sagging half-deflated on the left — and on the right a small dynamometer dial with "
 "its SIGNAL ORANGE needle standing high, the two instruments facing each other on a deep "
 "ink-blue-black field."),
(6,"WIDE","field","ambient",5,
 "hundreds of tiny bone-white dots drift slowly upward like rising dust",
 "A VAST deep ink-blue-black field filled with HUNDREDS of tiny bone-white dots scattered "
 "like a star field, denser toward the centre, fine film grain, quiet and enormous."),
(6,"XCU","instrument","ambient",5,
 "the second orange needle sweeps to exactly the same mark",
 "TWO small dial faces side by side filling the frame, plain tick marks, each with one "
 "luminous SIGNAL ORANGE needle standing at the same identical angle, on a deep "
 "ink-blue-black field."),
(7,"MED","hands","ambient",5,
 "the two hands meet and clasp firmly once",
 f"TWO warm-skinned hands meeting in a firm handshake at the centre of the frame, drawn bold "
 f"and simplified, one older and broader, one younger and slimmer, lit warmly from below, on "
 f"a deep ink-blue-black field."),
(8,"XCU","hands","ambient",5,
 "the older hand tightens its grip very slightly",
 "The clasped handshake filling the frame, the older broader hand on the outside, knuckles "
 "and tendons drawn bold, warm instrument light from below, deep ink-blue-black field."),
(9,"CU","paper","data",5,
 "none",
 "A single bone-white ledger page, drawn flat and graphic with plain ruled lines and a wide "
 "BLANK title strip, standing alone and still against a deep ink-blue-black field."),
# ACT 3 — the wrong move, the receipt ---------------------------------------
(10,"CU","instrument","ambient",5,
 "the spring gripper compresses once and reopens",
 "A small spring hand-gripper, steel grey with a SIGNAL ORANGE spring coil, standing upright "
 "and oversized at the centre of a deep ink-blue-black field."),
(11,"MED","hands","ambient",5,
 "the hand pumps the gripper quickly over and over in place",
 f"{HAND} working a small steel spring gripper with an ORANGE coil, mid-squeeze, the wrist "
 f"braced, everything else around it dark and still on a deep ink-blue-black field."),
(12,"WIDE","field","ambient",5,
 "the single orange line under the gripper slowly flattens level",
 "The spring gripper standing small and alone in a VAST deep ink-blue-black field, one thin "
 "SIGNAL ORANGE line running level beneath it like a floor, fine film grain."),
(13,"MED","instrument","big:reveal",5,
 "a bone-white receipt feeds slowly upward out of the slot, one blank line at a time",
 "The round dial now revealed as the top of a small receipt printer: the same tick-marked "
 "face, and below it a steel slot from which a BLANK bone-white receipt strip has begun to "
 "rise, drawn flat and graphic on a deep ink-blue-black field."),
(13,"CU","paper","ambient",5,
 "the second identical receipt slides slowly alongside the first",
 "TWO identical BLANK bone-white receipt strips side by side, faint ruled lines, one a "
 "little ahead of the other, flat and graphic on a deep ink-blue-black field."),
# ACT 4 — what the receipt itemizes ------------------------------------------
(14,"CU","paper","ambient",5,
 "the long receipt strip sways gently",
 "A very long BLANK bone-white receipt strip hanging down the middle of the frame from above, "
 "gently curved, with faint ruled item lines and no writing of any kind, on a deep "
 "ink-blue-black field."),
(14,"MED","hands","ambient",5,
 "the hand hoists the crate smoothly upward past the frame edge",
 "A warm-skinned hand and forearm hoisting a plain bone-white crate drawn flat and "
 "graphic, mid-lift against the dark field, one small ORANGE corner mark on the crate."),
(15,"XCU","hands","ambient",5,
 "the open hand turns palm-up and settles",
 f"{HAND} open and relaxed, palm beginning to turn upward, fingers loose, filling the frame "
 f"against the dark field, warm-lit from one side."),
(16,"MED","instrument","ambient",5,
 "the small dynamometer rotates slowly a quarter turn and stops",
 "A hand dynamometer standing alone like a museum object on a low bone-white plinth drawn "
 "flat and graphic, its ORANGE needle at rest, on a deep ink-blue-black field."),
(16,"CU","instrument","ambient",5,
 "the orange needle returns to exactly the same mark a second time",
 "The dynamometer dial face large in frame, its SIGNAL ORANGE needle at a firm mid-arc "
 "mark, a faint repeated ghost of the needle at the same angle, tick marks plain, on a "
 "deep ink-blue-black field."),
(17,"MED","instrument","ambient",5,
 "the orange fuel-gauge needle sinks slowly toward the bottom of its arc",
 "A car fuel gauge drawn huge and simplified: a half-circle of plain tick marks with one "
 "luminous SIGNAL ORANGE needle high on the arc, steel-grey housing, on a deep "
 "ink-blue-black field."),
(17,"XCU","instrument","ambient",5,
 "a brush stroke of orange paint glides up the gauge glass and stops",
 "The fuel gauge face in extreme close-up, and resting against its glass a small flat "
 "paintbrush loaded with SIGNAL ORANGE, one wet stroke already lying on the glass above "
 "the sunken needle, on a deep ink-blue-black field."),
# ACT 5 — the world that stopped asking --------------------------------------
(18,"MED","eras","big:clock",5,
 "the hay bale swings up and out of frame as the car keys drop gently into its place",
 "A split composition on a deep ink-blue-black field: on the left a rectangular hay bale "
 "drawn bold and golden-bone, mid-lift with a strap around it; on the right a small set of "
 "car keys falling, drawn steel grey with one ORANGE tag; the two objects at the same scale."),
(19,"WIDE","field","ambient",5,
 "the row of streetlights dims from left to right one by one",
 "A VAST dark skyline made of simple flat rooftop shapes along the bottom edge, a row of "
 "SEVEN small bone-white streetlight dots above them, deep ink-blue-black sky filling the "
 "frame, fine grain."),
(20,"MED","eras","data",7,
 "none",
 "Two upright bone-white bars side by side on a deep ink-blue-black field, the left bar "
 "clearly taller than the right, both bars plain and unmarked with a wide BLANK strip "
 "beneath each, drawn flat and graphic, completely still."),
(21,"CU","paper","ambient",5,
 "the receipt strip feeds upward one steady line at a time",
 "The receipt printer slot in close-up, a BLANK bone-white strip rising from it, faint ruled "
 "lines, steel housing warm-lit by its own small ORANGE indicator lamp, dark field around."),
(22,"MED","paper","ambient",5,
 "the folded paper tips forward and comes to rest against the door",
 "A single folded bone-white paper leaning upright against a plain flat-drawn front door in "
 "steel grey, the paper oversized for the door, lit like the only bright thing on the deep "
 "ink-blue-black field."),
(22,"CU","paper","ambient",5,
 "the folded paper slides slowly through the letterbox slot",
 "A plain steel-grey front-door letterbox slot drawn flat and graphic, a folded "
 "bone-white paper halfway through it, the flap resting on the paper, warm light from "
 "the slot, deep ink-blue-black field around."),
# ACT 6 — the part you can't un-know -----------------------------------------
(23,"XCU","instrument","ambient",5,
 "the orange needle ticks once, softly, and holds",
 "The dial face filling the frame in near-darkness, tick marks faint, the SIGNAL ORANGE "
 "needle resting low with a soft glow, deep ink-blue-black all around."),
(24,"MED","hands","ambient",5,
 "the faint orange arc beneath the clasped hands brightens slowly",
 "TWO warm-skinned hands in a handshake at the centre, and beneath them, faint and low, a "
 "thin SIGNAL ORANGE arc of tick marks curving like a hidden dial, on a deep ink-blue-black "
 "field."),
(25,"MED","hands","ambient",5,
 "the older hand squeezes and holds a beat too long",
 "A wedding-warm handshake: an older broad hand gripping a younger hand firmly, both drawn "
 "bold and simplified, a soft bone-white glow behind them like distant room light, deep "
 "ink-blue-black field."),
(25,"XCU","instrument","ambient",5,
 "the orange needle stirs and climbs a small distance",
 "A small dial face in extreme close-up, mostly dark, its SIGNAL ORANGE needle just "
 "off its rest and climbing, a soft glow at the tip, deep ink-blue-black field."),
(26,"WIDE","field","ambient",5,
 "the small receipts drift slowly downward like falling leaves",
 "A VAST deep ink-blue-black field with NINE small bone-white receipt strips scattered "
 "through the air at different heights and angles, each blank, drifting, fine film grain."),
# ACT 7 — the honest use -----------------------------------------------------
(27,"CU","instrument","ambient",5,
 "the orange needle sweeps slowly back to zero and rests",
 "The dynamometer dial large in frame, its SIGNAL ORANGE needle mid-arc on the way down, "
 "tick marks plain, steel housing quiet, on a deep ink-blue-black field."),
(27,"WIDE","instrument","ambient",5,
 "the orange glow around the small dial breathes slowly brighter and dimmer",
 "The dynamometer dial small and alone at the centre of a VAST deep ink-blue-black field, "
 "a soft SIGNAL ORANGE glow held around its needle, fine film grain."),
(28,"XCU","paper","ambient",5,
 "the receipt edge flutters once, gently",
 "The torn end of a bone-white receipt strip filling the frame diagonally, its perforated "
 "edge crisp, faint ruled lines, warm-lit against the deep ink-blue-black field."),
(29,"MED","hands","ambient",5,
 "the hand lifts the heavy case smoothly off the ground",
 f"{HAND} gripping the steel handle of a plain heavy case drawn flat and graphic, arm taut, "
 f"the case just leaving the ground, one small ORANGE tag on the handle, deep ink-blue-black "
 f"field."),
(29,"CU","paper","ambient",5,
 "a fresh bone-white receipt feeds upward steadily",
 "The receipt printer slot in close-up, a crisp new BLANK bone-white strip rising from it "
 "in warm light, its ORANGE indicator lamp lit, deep ink-blue-black field around."),
(30,"CU","instrument","ambient",5,
 "the orange needle climbs steadily and settles higher than before",
 "The dial face large in frame, the SIGNAL ORANGE needle rising through the tick marks with "
 "a faint trail of glow, everything else still, deep ink-blue-black field."),
(31,"CU","instrument","big:held",5,
 "the hand closes around the handle once more and the orange needle sweeps up and holds",
 f"{HAND} closing around the dynamometer handle exactly as at the start, tendons rising, the "
 f"oversized dial behind with its SIGNAL ORANGE needle beginning to sweep, warm hand against "
 f"cold instrument, on a deep ink-blue-black field."),
]

WORLD = (
 "Flat graphic MOTION-DESIGN illustration in the register of a high-end studio explainer: "
 "bold simplified forms, engineered clean line work, generous negative space, 2D planes, NO "
 "photorealism, NO 3D rendering, NO gradients beyond a single soft vignette, NO lens flares. "
 "The palette is FIXED: a deep ink-blue-black field, warm bone-white line work and paper, "
 "steel-grey instrument bodies, one warm muted skin tone for hands, and ONE luminous SIGNAL "
 "ORANGE accent reserved for needles, readings and moving parts. Fine even film grain, flat "
 "matte surfaces, all surfaces clean. There is NO text, NO lettering, NO numerals and NO "
 "writing of any kind anywhere; every dial face carries plain tick marks only, every paper "
 "and plate and strip is completely BLANK. ONE SINGLE COHERENT SCENE, NOT a grid of panels. "
 "16:9, edge to edge, one scene, one locked camera.")

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []

# -- script-level checks (carried) ------------------------------------------
SELFREF = re.compile(r'\b(film|movie|video|episode|documentary)\b', re.I)
hits = [(n, s) for n, s in enumerate(sents, 1) if SELFREF.search(s)]
if hits:
    errs.append('narration names the artefact: ' + '; '.join(f'line {n}' for n, s in hits[:4]))

lines = [s[0] for s in S]
missing = sorted(set(range(1, len(sents) + 1)) - set(lines))
if missing:
    errs.append(f'sentences with no shot: {missing[:12]}')
if lines != sorted(lines):
    errs.append('shots run backwards through the script')

braces = [i for i, s in enumerate(S, 1) if '{' in s[6] or '{' in s[5]]
if braces:
    errs.append('unrendered f-string braces: ' + ' '.join('s%02d' % i for i in braces))

# -- the mover gate (replaces the face gate) --------------------------------
for i, s in enumerate(S, 1):
    mclass, mover, scene = s[3], s[5], s[6]
    if mclass == 'data':
        if mover != 'none':
            errs.append(f's{i:02d}: data rows generate no clip; mover must be "none"')
        continue
    if mover == 'none':
        errs.append(f's{i:02d}: clip row with no mover')
        continue
    # one motion only: reject prompts that yoke two movers together
    if re.search(r'\bwhile\b|\bas\b', mover) and not mclass.startswith('big:'):
        errs.append(f's{i:02d}: ambient mover yokes two motions ("{mover[:50]}")')
    if len(mover.split()) > 18:
        errs.append(f's{i:02d}: mover phrase too long to be one motion ({len(mover.split())}w)')
    # the mover must exist in the keyframe
    key_nouns = [w for w in re.findall(r'[a-z]+', mover.lower())
                 if w in ('needle','hand','hands','receipt','gripper','cuff','bale','keys',
                          'dots','lights','streetlights','invoice','paper','strip','case','arc')]
    if key_nouns and not any(n.rstrip('s') in scene.lower() for n in key_nouns):
        errs.append(f's{i:02d}: mover noun(s) {key_nouns} absent from the keyframe scene')
    # instrument movers are orange (hands are flesh and exempt)
    if any(n in ('needle','gripper','arc') for n in key_nouns) and 'ORANGE' not in scene:
        errs.append(f's{i:02d}: instrument mover but no ORANGE in the keyframe')

# -- negation positivity ----------------------------------------------------
NEG = re.compile(r'\bnothing\b|\bnobody\b|\bwithout\b|\bempty(?!ing)\b', re.I)
for i, s in enumerate(S, 1):
    if NEG.search(s[5]) or (NEG.search(s[6]) and 'BLANK' not in s[6][:400].split('NEG')[0] and
                            not re.search(r'blank|clean|still|alone', s[6], re.I)):
        errs.append(f's{i:02d}: absence phrased as negation — restate as a present state')

# -- motion hierarchy -------------------------------------------------------
bigs = [i for i, s in enumerate(S, 1) if s[3].startswith('big:')]
if not (4 <= len(bigs) <= 6):
    errs.append(f'{len(bigs)} BIG moves; the film needs 4-6')
for a, b in zip(bigs, bigs[1:]):
    if b - a < 2:
        errs.append(f'BIG moves adjacent at s{a:02d}/s{b:02d}')

# -- duration budget --------------------------------------------------------
est = {n: len(sents[n-1].split()) / WPM * 60 for n in range(1, len(sents) + 1)}
total_narr = sum(est.values())
total_clip = sum(s[4] for s in S if s[3] != 'data')
for i, s in enumerate(S, 1):
    if s[3] == 'data':
        continue
    holds = est[s[0]] / lines.count(s[0])
    if s[4] < holds - 1.2:
        errs.append(f's{i:02d}: clip {s[4]}s but its narration hold is ~{holds:.1f}s — '
                    'the freeze-pad would dominate the shot')

setc = Counter(s[2] for s in S)
c = Counter(s[1] for s in S)
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print('classes: ' + '  '.join(f'{k}={v}' for k, v in
      sorted(Counter(s[3].split(":")[0] for s in S).items())))
print('settings: ' + '  '.join(f'{k}={v}' for k, v in setc.most_common()))
print(f'narration ~{total_narr:.0f}s | clip seconds {total_clip} | data stills '
      f'{sum(1 for s in S if s[3]=="data")}')

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs:
        print('  ' + e, file=sys.stderr)
    sys.exit(1)

ids, _seen = [], {}
for row in S:
    n = _seen.get(row[0], 0)
    _seen[row[0]] = n + 1
    ids.append(f'b{row[0]:02d}' + ('' if n == 0 else chr(ord('a') + n)))

(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{CAM[s[1]]} {s[6]} {WORLD}' for i, s in zip(ids, S)}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'setting': s[2], 'motion_class': s[3],
      'clip_seconds': s[4], 'motion_prompt': s[5], 'line': sents[s[0] - 1], 'scene': s[6]}
     for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S) if 'hand' not in s[6].lower()]
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no hands)')
