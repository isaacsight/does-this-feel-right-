#!/usr/bin/env python3
"""Frame book — Who You Measured. 78 frames, one per sentence.

Object-led: there is NO cast anywhere in this film. The world test showed the
character does not survive halftone plus misregistration (WORLD.md), and the
subject — measurement, samples, distributions — has its own object vocabulary.

Boarded against PLAYBOOK 10.38 FROM THE START rather than as a rescue pass, which
is the whole lesson of the previous film. Every frame carries:

  CAMERA       from a quota this file ENFORCES (v1 of the last film had two
               close-ups in 88 frames and nobody noticed until the contact
               sheets were laid side by side)
  BEHAVIOUR    what the object DOES. The cast-free equivalent of naming an
               expression: without it every frame is an object sitting still.
  EXAGGERATION scale, quantity, or distortion, past realism.

FOUR MOTIFS, each one object seen repeatedly, never a description re-invented:
  THE DOT     one measured person. Never a figure, never a face — a plain disc.
  THE ARROW   a cause. Planted at 7, paid off at 72.
  THE ROOMS   two rooms in cross-section. THE TURN at 59-61.
  THE RULER   the instrument. Introduced at 45, turned on itself at 75.

Run: python3 board.py     (writes production/prompts.json, refuses on quota fail)
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

# (camera, behaviour, scene)   camera ∈ XCU CU MED WIDE XWIDE OVER LOW
S = [
# ---- ACT 1 — the causes you were handed -----------------------------------
("CU","pinned",       "One small plain disc alone on a flat ground line, with a single ENORMOUS arrow pointing down at it. The arrow is many times larger than the disc it points at. Nothing else."),
("MED","streaming",   "A plain upright rectangle the size of a paperback, and pouring out of it an ABSURD stream of hundreds of tiny discs that fans out and fills the lower half of the frame. Nothing else."),
("WIDE","descending", "A long chain of identical plain discs joined by short straight strokes, descending diagonally from the top left corner to the bottom right and running off both edges. Every disc identical. Nothing else."),
("OVER","lying",      "Straight-down overhead of one plain rectangular card lying alone on a flat surface, ABSURDLY large, filling almost the whole frame. Blank. Nothing else."),
("XWIDE","scattered", "An enormous empty field with three small plain objects placed very far apart along one ground line, tiny and isolated. Nothing else."),
("LOW","looming",     "Low camera looking steeply up at THREE enormous arrows hanging above, all pointing down at one tiny plain disc on the ground far below. Nothing else."),
("XCU","filling",     "EXTREME CLOSE-UP of one enormous arrow filling the entire frame, its point at the right edge, its tail running off the left. Nothing else."),
("WIDE","aligned",    "A long row of plain shapes on a ground line, all of them arrows, every single one pointing the same direction to the right. Absolutely uniform. Nothing else."),
("WIDE","standing",   "Three tall plain columns standing in a row on a ground line, evenly spaced, each a different height. Nothing else."),
("MED","separated",   "Three clearly different plain objects in a row on a ground line: a round flask, a short chain of discs, and a wide open jar. Nothing else."),
("OVER","shadowing",  "Straight-down overhead of those same three different objects, and beneath each one an IDENTICAL shadow of exactly the same shape and size, revealing they cast the same shape. Nothing else."),
# ---- ACT 2 — the chemical -------------------------------------------------
("CU","opening",      "CLOSE on one round flask standing alone, its neck open, tipped very slightly. Nothing else."),
("XCU","bursting",    "EXTREME CLOSE-UP of a single enormous burst shape, a ragged star of short strokes radiating from one point, filling the whole frame. Nothing else."),
("MED","draining",    "A round flask lying on its side on a ground line with a thin trail of tiny discs running out of it and off the right edge of the frame. Nothing else."),
("WIDE","glowing",    "A single plain disc on a ground line, very large, with a wide flat halo of concentric rings spreading out around it to the frame edges. Nothing else."),
("CU","resting",      "CLOSE on one plain disc sitting still on a flat surface, perfectly centred, nothing happening to it at all. Nothing else."),
("MED","flipping",    "Two identical plain shapes side by side on a ground line, and the RIGHT one is upside down relative to the left one, an exact mirror. Nothing else."),
("OVER","documented", "Straight-down overhead of one plain rectangular card lying flat, blank, with a plain ruled line running under it. Nothing else."),
("WIDE","listening",  "A wide field with one small plain dome shape on a ground line and a single fine line running from it up and off the top edge of the frame. Nothing else."),
("XCU","gapping",     "EXTREME CLOSE-UP of two thick horizontal bars stacked with a clear empty gap between them, the gap the brightest part of the frame. Nothing else."),
("LOW","spiking",     "A flat horizontal baseline running the width of the frame, absolutely level, with ONE enormous vertical spike shooting up from it far higher than the frame can hold. Nothing else."),
("MED","flattening",  "The same flat horizontal baseline running the width of the frame, completely level, with no spike anywhere on it at all. Nothing else."),
("CU","quieting",     "CLOSE on one small plain disc, alone and still, with the surrounding field completely empty. Nothing else."),
("XCU","erupting",    "EXTREME CLOSE-UP of one enormous burst of short strokes radiating outward from a single point, filling the entire frame edge to edge. Nothing else."),
("MED","splitting",   "One plain shape on a ground line that has been split cleanly down the middle into two halves, the halves pulled slightly apart with bare paper between them. Nothing else."),
("WIDE","paired",     "Two plain shapes standing apart on a ground line: on the left a shape leaning hard forward as if straining toward the right; on the right a shape sitting squat and settled. Nothing else."),
("LOW","reaching",    "Low camera looking up at one enormous plain shape leaning far over, stretched and distorted as it reaches toward a tiny plain disc placed just out of its reach. Nothing else."),
("MED","collapsing",  "One tall plain shape on a ground line that has buckled and folded down onto itself into a low heap. Nothing else."),
("MED","standing",    "One plain squat shape sitting upright and completely intact on a ground line, unchanged and solid. Nothing else."),
("WIDE","separating", "A wide field with two plain shapes very far apart on one ground line, a great deal of empty paper between them, one leaning forward and one at rest. Nothing else."),
("XCU","straining",   "EXTREME CLOSE-UP of one plain hook shape stretched and pulled thin, distorted by tension, filling the frame. Nothing else."),
("CU","empty",        "CLOSE on one plain open bowl shape, completely empty inside, filling much of the frame. Nothing else."),
# ---- ACT 3 — the gene -----------------------------------------------------
("MED","touching",    "Two plain chains of discs entering from opposite edges of the frame, their end links just touching in the middle. Nothing else."),
("WIDE","repeating",  "A long row of fifteen identical small plain rectangles on a ground line, evenly spaced, absolutely uniform. Nothing else."),
("OVER","selecting",  "Straight-down overhead of many small plain discs scattered on a surface, with ONE of them circled by a single plain ring. Nothing else."),
("XWIDE","massing",   "A vast field with a few hundred small plain discs gathered in a loose crowd on the ground, all identical, occupying only the lower third. Nothing else."),
("CU","labelled",     "CLOSE on one single link of a chain, enormous at this scale, with a plain ring drawn tightly around it. No writing of any kind. Nothing else."),
("MED","tilting",     "A plain balance beam on a central post, tipped hard over to one side, with a small pile of discs heaped on the low end and nothing on the high end. Nothing else."),
("WIDE","stacking",   "A tall stack of plain rectangular cards on a ground line, leaning, with a scattering of identical cards lying flat and blank on the ground beside it, clearly discarded. Nothing else."),
("MED","shaking",     "A plain shape on a ground line drawn with a doubled wobbling outline, as if unsteady, with short motion strokes on either side of it. Nothing else."),
("OVER","widening",   "Straight-down overhead of a small cluster of discs beside an ENORMOUSLY larger cluster of the same discs, the second so large it runs off three edges of the frame. Nothing else."),
("XWIDE","flooding",  "An enormous field completely packed edge to edge with tiny identical discs, hundreds of thousands of them, so dense they read as a single texture, with no gaps anywhere. Nothing else."),
("WIDE","levelling",  "Eighteen small plain rectangles standing in a row on a ground line, and beside them eighteen more identical rectangles, the two groups indistinguishable from one another. Nothing else."),
("XCU","hollow",      "EXTREME CLOSE-UP of one plain ring drawn on bare paper with absolutely nothing inside it, the empty centre filling most of the frame. Nothing else."),
# ---- ACT 4 — the sample ---------------------------------------------------
("MED","measuring",   "One plain straight ruler bar lying across a ground line, with evenly spaced tick strokes along its edge. No numbers, no letters. Nothing else."),
("OVER","publishing", "Straight-down overhead of one plain rectangular card lying alone, blank, with its corner turned up. Nothing else."),
("XCU","titled",      "EXTREME CLOSE-UP of the turned-up corner of one plain card, enormous, the bare paper showing beneath it. No writing of any kind. Nothing else."),
("WIDE","grouping",   "Five plain rectangles of identical size standing close together in a tight cluster on a ground line, touching one another. Nothing else."),
("XWIDE","dwarfing",  "A vast field. A dense block of small discs occupies almost the entire frame, and a TINY separate cluster of the same discs sits alone at the bottom corner, absurdly small beside it. Nothing else."),
("MED","shrugging",   "A plain balance beam sitting perfectly level on its post, with an equal small pile of discs on each end, entirely unremarkable. Nothing else."),
("WIDE","comparing",  "Two groups of discs on a ground line, drawn to the same size, with a single plain vertical stroke standing between them. Nothing else."),
("XWIDE","outlying",  "A very wide field with a long tight band of identical discs running across the middle, and ONE disc sitting far above the band, isolated, an obvious outlier. Nothing else."),
("MED","repeating",   "The same tight band of discs with THREE separate discs sitting far outside it, each one alone, at different distances above the band. Nothing else."),
("LOW","holding",     "Low camera looking steeply up at one ENORMOUS ruler bar held horizontally overhead, running off both edges of the frame, its tick marks huge. Beneath it, one tiny disc. Nothing else."),
# ---- ACT 5 — THE TURN -----------------------------------------------------
("CU","singular",     "CLOSE on one plain rectangular card standing upright and alone on a ground line, blank. Nothing else."),
("WIDE","pairing",    "Many small pairs of identical discs on a ground line, each pair joined by a short stroke, arranged in an even row. Nothing else."),
("OVER","asking",     "Straight-down overhead of one plain ring drawn on bare paper, empty, with two short strokes leading away from it in different directions. Nothing else."),
("MED","forking",     "A single plain stroke that runs in from the left edge and splits into TWO strokes of equal weight leading to two identical empty rings. Nothing else."),
("WIDE","filling",    "Two plain empty rooms side by side in cross-section, sharing one ground line. The LEFT room is almost entirely filled by one large solid block that reaches the ceiling. The RIGHT room is empty. Nothing else."),
("WIDE","inverting",  "The SAME two rooms side by side in cross-section on the same ground line, at the same size and framing, but now the LEFT room is empty and the RIGHT room is almost entirely filled by the large solid block. Nothing else."),
("WIDE","doubling",   "The same two rooms side by side in cross-section, identical in size and framing, one filled and one empty, seen together in a single wide view. Nothing else."),
("XCU","holding",     "EXTREME CLOSE-UP of the single ground line where the two rooms meet, the corner of each room just visible at the frame edges, the bare paper enormous between them. Nothing else."),
("MED","detaching",   "One plain disc and one plain ruler bar lying separately on a ground line with a clear space between them, obviously not touching. Nothing else."),
("XWIDE","situating", "A vast field with one small plain room drawn in cross-section, tiny and alone, and inside it a single disc. Everything around it is bare paper. Nothing else."),
("WIDE","moving",     "The same small room in cross-section shown twice on one ground line, far apart, and in each one the block inside sits at a visibly different height. Nothing else."),
("LOW","failing",     "Low camera looking up at one enormous arrow standing on its point, unsupported and clearly toppling, casting no shadow. Nothing else."),
# ---- ACT 6 — what survived, and the confession ----------------------------
("MED","discarding",  "A plain open bin shape on a ground line with several plain cards tipped into it, and one card caught on the rim, half in. Nothing else."),
("CU","refusing",     "CLOSE on one plain card standing upright and firmly intact on a ground line, undamaged. Nothing else."),
("WIDE","remaining",  "A wide field with several plain objects still standing upright on a ground line, solid and undisturbed, and a scattering of fallen shapes lying flat around them. Nothing else."),
("XWIDE","persisting","A vast field with a long descending chain of identical discs running from the top of the frame down to the ground line and continuing off the bottom edge. Nothing else."),
("MED","pulling",     "One plain shape leaning hard forward toward a small disc just out of reach, stretched by the effort, with the disc plainly untouched. Nothing else."),
("WIDE","fragmenting","One large plain shape on a ground line broken cleanly into three separate pieces that have fallen apart from one another, with bare paper between them. Nothing else."),
("XCU","reflecting",  "EXTREME CLOSE-UP of one enormous arrow, the same arrow as before, now bent back on itself so its point aims at its own tail. Nothing else."),
("XWIDE","sourcing",  "An enormous field packed edge to edge with tiny identical marks, a single uniform texture with no variation anywhere, running off all four edges. Nothing else."),
("LOW","implicating", "Low camera looking steeply up at one ENORMOUS ruler bar overhead, and a second identical ruler bar laid across it at an angle, measuring the first one. Nothing else."),
("CU","asking",       "CLOSE on one plain empty ring on bare paper, nothing inside it, nothing around it. Nothing else."),
("MED","narrowing",   "A wide plain shape on a ground line that tapers sharply to a single fine point at its right end. Nothing else."),
("XWIDE","closing",   "An enormous empty field of bare paper with one single small plain disc sitting alone on a ground line at the very bottom, and nothing else anywhere in the frame."),
]

WORLD = (
 "a RISOGRAPH PRINT: the whole image is printed in exactly TWO inks on uncoated "
 "off-white paper with visible paper tooth, and the paper is the SAME warm off-white "
 "across the whole frame with no change of paper colour toward the foreground and no "
 "cool grey or pure white anywhere. The two inks are a bright FLUORESCENT PINK and a "
 "deep BLUE, and nothing else. Every filled area is a coarse visible halftone of round "
 "dots, never a smooth flat fill. The two ink layers are slightly MISREGISTERED so "
 "their edges do not line up and a narrow band of bare paper shows along one side of "
 "every shape. Where the two inks overlap they multiply into a single darker violet. "
 "The ink is semi-transparent with uneven roller coverage, patchy density and "
 "occasional light streaking. No gradients, no soft shading, no glow, no drop shadows, "
 "no photographic texture. Edges are slightly ragged from the screen. "
 "There is NO text, NO lettering, NO numbers and NO writing of any kind anywhere. "
 "There are NO people, NO figures, NO faces and NO hands anywhere in the image. "
 "16:9, edge to edge, one scene, one camera.")

MIN = {'XCU': 6, 'CU': 6, 'OVER': 6, 'LOW': 6, 'XWIDE': 8}
MAX_RUN = 3

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []
if len(S) != len(sents):
    errs.append(f'{len(S)} frames for {len(sents)} sentences — must be 1:1')

cams = [s[0] for s in S]
c = Counter(cams)
for k, n in MIN.items():
    if c[k] < n:
        errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
if c['XCU'] + c['CU'] < 11:
    errs.append(f"close-ups {c['XCU'] + c['CU']}, needs 11")
run, prev = 1, None
for i, cam in enumerate(cams, 1):
    if cam == prev:
        run += 1
        if run > MAX_RUN:
            errs.append(f'frame {i}: {run} consecutive {cam} (max {MAX_RUN})')
    else:
        run, prev = 1, cam
for i, (_, _, scene) in enumerate(S, 1):
    for bad in ('figure', 'person', 'people', 'hand', 'face'):
        if re.search(rf'\b{bad}\b', scene, re.I):
            errs.append(f'frame {i}: names "{bad}" — this film has no cast')

print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {c['XCU'] + c['CU']} | behaviours named on {sum(1 for s in S if s[1])}/{len(S)}")

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs:
        print('  ' + e, file=sys.stderr)
    sys.exit(1)

ids = [f'b{i:02d}' for i in range(1, len(S) + 1)]
out = {i: f'{s[2]} {WORLD}' for i, s in zip(ids, S)}
(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(out, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'camera': s[0], 'behaviour': s[1], 'line': ln, 'scene': s[2]}
     for i, s, ln in zip(ids, S, sents)], indent=1))
print(f'\nwrote {len(out)} prompts + board.json')
