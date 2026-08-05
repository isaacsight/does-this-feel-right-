#!/usr/bin/env python3
"""Frame book — The Lab and the Jungle. 78 frames, one per sentence.

The house protagonist crosses into the RISO universe. He is spine across films the
way the narrator's voice is; only what the process demands changes.

Two faults from the cast test are fixed here, both in the character/world clause:

  HAIR   two thick vertical strokes on a round head read as RABBIT EARS. Thin was
         antennae, thick was ears. The fix is SHAPE, not weight: the two strokes
         kink, lean off vertical, and are different lengths.
  GREEN  a green leaf appeared in the close-up test. In a locked two-ink world that
         is a third ink, and the gate's hue census cannot catch it here because it
         is effectively disabled for two-ink films. Forbidden by name.

Every frame carries CAMERA, EXPRESSION, MOVE and the picture:

  CAMERA     quota ENFORCED below
  EXPRESSION this film HAS a cast again, so the last film's "behaviour" column goes
             back to being a face. v1 of cognitive-debt had ONE expression for seven
             minutes because no line of the board ever asked for a second.
  MOVE       per-shot camera move — the previous two films used one uniform push,
             alternating direction by index, which is motion by formula rather than
             by meaning. Here the move belongs to the beat.

Run: python3 board.py   (writes production/prompts.json + board.json, refuses on fail)
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

HERO = ("the recurring cartoon character: a small round bald head, EXACTLY TWO hairs "
        "standing up from the crown drawn as THICK solid strokes that KINK and LEAN "
        "at different angles and are different lengths, like a cowlick — never two "
        "straight vertical strokes, never symmetrical, never rabbit ears, never "
        "antennae. A hooded jacket in the PINK ink, trousers in the DEEP BLUE ink, "
        "pale shoes left as bare paper. Big simple shapes, heavy outlines, no fine "
        "detail on him anywhere")

# (camera, expression, move, scene)
# camera ∈ XCU CU MED WIDE XWIDE OVER LOW      move ∈ HOLD PUSH PULL PANL PANR TILTU TILTD
S = [
# ---- ACT 1 — the sentence you repeated ------------------------------------
("MED","mouth open mid-word","PUSH", f"{HERO} standing in a jungle laboratory, mouth open mid-sentence, one hand raised as if quoting somebody. Vines behind him."),
("XCU","smug, eyes shut","HOLD", f"EXTREME CLOSE-UP on a small white mouse sitting upright on a bench, absurdly pleased with itself, eyes shut, chest out. Huge in frame."),
("WIDE","hopeful, watching","PANR", f"A jungle laboratory. {HERO} watches a tall glass tank in which one tiny mouse sits under an enormous leaf. He is hopeful, hands clasped."),
("CU","trusting, wide eyes","HOLD", f"CLOSE on {HERO}, eyes wide and completely trusting, nodding, one thick eyebrow raised."),
("MED","firm, flat mouth","HOLD", f"{HERO} standing straight with a flat firm mouth, both hands out low and open, insisting. Bench and vines behind."),
("WIDE","absorbed, bent over","TILTD", f"{HERO} bent over a bench absorbed in work, surrounded by flasks and coiled tubing, a wall of jungle leaves pressing in from the right."),
("XWIDE","tiny, arms out","PULL", f"A very wide shot: {HERO} stands tiny at the edge of an enormous open jungle clearing, arms out, the neat laboratory bench behind him looking absurdly small against the vegetation."),
("CU","puzzled, head tilted","PUSH", f"CLOSE on {HERO} holding up an empty flask and staring into it, head tilted right over, puzzled."),
("MED","realising, brow up","HOLD", f"{HERO} turning to look at the floor beneath his own feet, both eyebrows shot up, as if noticing the room for the first time."),
("LOW","small, looking up","TILTU", f"Low camera looking steeply up at the enormous walls and ceiling of a laboratory, cabinets towering, vines coming through a vent overhead. {HERO} stands tiny at the bottom of frame looking up."),
("WIDE","determined, striding","PANL", f"{HERO} striding purposefully across a jungle laboratory with a clipboard-sized blank pale board under one arm, determined."),
# ---- ACT 2 — the temperature ----------------------------------------------
("CU","shivering, teeth set","PUSH", f"CLOSE on one small mouse sitting on a bench with its shoulders hunched right up and its teeth set, plainly cold. Two short motion strokes beside it for shivering."),
("MED","officious, pointing","HOLD", f"{HERO} standing beside an ENORMOUS wall thermostat dial, far taller than he is, pointing at it officiously."),
("MED","comfortable, smiling","HOLD", f"{HERO} standing relaxed and comfortable with a small satisfied smile, hands in his jacket pockets, in a plain corner of the lab."),
("CU","indignant, mouth wide","HOLD", "CLOSE on one small mouse standing on its hind legs with its mouth open in indignation, completely bare, no clothing, one arm gesturing at itself."),
("MED","hopeful, reaching","PANR", "A mouse reaching up with both paws toward a small hanging heat lamp that is much too high above it, on tiptoe."),
("XWIDE","-","PULL", "A vast wall of identical small cages in a grid receding into the distance, each with one tiny hunched mouse inside, all shivering, all identical."),
("MED","weary, dragging","PANL", "One mouse dragging an ENORMOUS coin-shaped weight behind it across a bench, exhausted, the weight far bigger than the mouse."),
("CU","sympathetic, wincing","HOLD", f"CLOSE on {HERO} wincing in sympathy, one eye squeezed shut, shoulders up around his ears."),
("MED","earnest, presenting","HOLD", f"{HERO} standing beside a huge blank pale board, presenting it with one open hand, earnest and slightly proud. No writing on the board."),
("WIDE","busy, carrying","PANR", f"{HERO} carrying a mouse cage across the lab toward a bright warm corner where an enormous heat lamp hangs, vines everywhere."),
("MED","astonished, hands on head","PUSH", "One mouse standing upright and thriving beside a shape that has visibly SHRUNK to a fraction of its former size, drawn as a small pale lump with a much larger dotted outline around it showing what it used to be."),
("XCU","fierce, teeth bared","HOLD", "EXTREME CLOSE-UP on one mouse looking fierce and alert, teeth bared, an enormous shield-like shape rising behind it."),
("MED","stern, arms folded","HOLD", f"{HERO} standing with arms folded and a stern flat mouth beside a mouse wrapped in an absurdly large scarf, correcting a misunderstanding."),
("WIDE","strained, splitting","TILTD", "One mouse standing on a bench trying to hold up TWO enormous objects at once, one in each paw, arms shaking, clearly unable to manage both."),
("OVER","-","PUSH", "Straight-down overhead of an open notebook lying on a bench, its pages entirely blank, with a huge thermostat dial lying beside it unrecorded."),
# ---- ACT 3 — the clean mouse ----------------------------------------------
("CU","eyebrows climbing","PUSH", f"CLOSE on {HERO}, both thick eyebrows climbing right up his forehead, mouth pulled sideways."),
("MED","fastidious, scrubbing","HOLD", f"{HERO} scrubbing a bench with an absurdly large brush, foam everywhere, fastidious and intent."),
("WIDE","-","PANR", "A gleaming empty laboratory bench stretching the width of the frame with absolutely nothing on it, while behind the glass wall a dense jungle presses in, full of leaves."),
("MED","approving, thumb up","HOLD", f"{HERO} nodding approvingly at a spotless sealed glass box with one small mouse inside it, one thumb raised."),
("MED","explaining, finger up","PANL", f"{HERO} beside a huge pale document board, one finger raised, explaining. The board is blank."),
("WIDE","-","PUSH", "Two mice side by side on a bench: on the left an enormous adult mouse standing solid and scarred, on the right a tiny smooth newborn mouse in a bonnet, absurdly small beside it."),
("CU","delighted, hand to mouth","HOLD", f"CLOSE on {HERO} laughing with one hand over his mouth, eyes creased, delighted."),
("MED","furtive, carrying","PANR", f"{HERO} sneaking through the lab carrying a small cardboard box with a very scruffy mouse peering out of the top, furtive, glancing sideways."),
("MED","cheerful, filthy","HOLD", "Three extremely scruffy pet-shop mice standing together on a bench, cheerfully filthy, one with a bent ear, one with a patch, one chewing a leaf."),
("WIDE","chaotic, delighted","TILTU", "A clean laboratory cage with the tidy white mouse inside it and three filthy pet-shop mice climbing in over the top, chaos beginning, all of them delighted."),
("MED","transformed, standing tall","PUSH", "The formerly tiny clean mouse now standing tall and broad on the bench, arms crossed, visibly grown up, the bonnet lying discarded at its feet."),
("XWIDE","-","PULL", "A very wide laboratory with a long row of tiny mice in bonnets standing in a line on a bench, absurdly small, facing an enormous closed door."),
# ---- ACT 4 — the trade -----------------------------------------------------
("MED","holding both","HOLD", f"{HERO} standing centre with an arm outstretched on each side, holding a small object in each hand at the same height, comparing them."),
("CU","serious, level","HOLD", f"CLOSE on {HERO} with a level serious face, no comedy, looking straight ahead."),
("MED","gesturing, precise","HOLD", f"{HERO} gesturing at a huge dial and a huge scrubbing brush standing side by side like exhibits, precise and calm."),
("WIDE","reasonable, shrugging","PANR", f"{HERO} shrugging reasonably with both palms up, standing between the neat laboratory on the left and the wall of jungle on the right."),
("MED","adjusting, tongue out","PUSH", f"{HERO} on tiptoe adjusting an enormous dial with both hands, tongue poking out in concentration."),
("MED","sealing, straining","HOLD", f"{HERO} pressing an enormous lid down onto a glass box with all his weight, straining, one foot off the ground."),
("XCU","-","PUSH", "EXTREME CLOSE-UP on the edge of a blade slicing cleanly through a leaf, the cut edge razor sharp."),
("XWIDE","tiny, marooned","PULL", "A vast empty white-tiled room with one tiny mouse alone in the exact centre, absurdly small, nothing else anywhere in the frame."),
("MED","weighing, tilting","TILTD", f"{HERO} standing beside an enormous balance beam tipped hard to one side, watching it tilt, hands behind his back."),
("CU","firm, flat","HOLD", f"CLOSE on {HERO} shaking his head slowly with a firm flat mouth, one finger raised."),
# ---- ACT 5 — two places ----------------------------------------------------
("WIDE","-","PANR", "A wide frame split down the middle by a single vertical glass wall: on the left a spotless empty laboratory, on the right a dense chaotic jungle full of leaves and vines. Same ground line runs through both."),
("MED","confident, arms wide","HOLD", f"{HERO} standing on the laboratory side with both arms spread wide and confident, everything around him neat, empty and labelled with nothing."),
("WIDE","overwhelmed, small","TILTU", f"{HERO} standing on the jungle side, tiny beneath enormous leaves, insects, hanging vines and branches all crowding in from every edge."),
("XWIDE","-","PULL", "An enormous jungle canopy seen wide, everything happening at once: birds, huge leaves, vines, flowers, water, all overlapping, no clear centre."),
("MED","hopeful, carrying","PANR", f"{HERO} carrying a small potted seedling in both hands, walking from the clean side toward the jungle side, hopeful."),
("WIDE","dismayed, empty-handed","HOLD", f"{HERO} standing in the jungle holding an empty pot, the seedling gone, dismayed, leaves towering over him."),
("MED","accusing, pointing","PUSH", "Three tall plain figures in coats standing in a row, all pointing accusingly downward at a small wilted seedling on the ground."),
("CU","sheepish, shrinking","HOLD", f"CLOSE on {HERO} shrinking down into his hood, sheepish, eyes sideways."),
("MED","conceding, nodding","HOLD", f"{HERO} nodding once, conceding the point, mouth flat, hands at his sides."),
("WIDE","puzzled, examining","TILTD", f"{HERO} crouched over a perfectly healthy seedling lying on the jungle floor, examining it, puzzled, nothing visibly wrong with it."),
("XCU","-","PULL", "EXTREME CLOSE-UP on a small pot, and around it a huge ghostly dotted outline of an entire room — walls, bench, ceiling — that plainly did not come with it."),
("MED","struggling, dragging","PANL", f"{HERO} trying to drag an ENORMOUS laboratory room behind him on a rope, the whole room absurdly larger than he is, feet slipping."),
("WIDE","cheerful, oblivious","PANR", "A long line of the same character walking single file into the jungle, each one carrying a small pot and cheerfully leaving a large dotted room-outline behind them on the ground."),
("XCU","mouth moving","PUSH", f"EXTREME CLOSE-UP on {HERO}'s mouth mid-sentence, enormous in frame, one word visibly leaving as a small solid shape."),
# ---- ACT 6 — what to do with it -------------------------------------------
("CU","questioning, brow raised","HOLD", f"CLOSE on {HERO} with one thick eyebrow raised high and his head tipped, asking."),
("MED","refusing, hands up","HOLD", f"{HERO} pushing away an enormous drooping shape with both hands, refusing it, mouth turned down."),
("WIDE","industrious, working","PANR", "A jungle laboratory busy with work: three of the character at benches, one on a ladder in the vines, flasks bubbling, everything in motion and cheerful."),
("MED","self-examining, mirror","PUSH", f"{HERO} holding up a large hand mirror and peering into it closely, examining his own face with one eye squeezed shut."),
("CU","attentive, listening","HOLD", f"CLOSE on {HERO} with his head turned and one hand cupped behind an ear, listening intently."),
("MED","considering, finger up","HOLD", f"{HERO} pausing mid-step with one finger raised, considering, eyes up."),
("OVER","-","TILTD", "Straight-down overhead of a laboratory bench with one small object in the exact centre and, drawn around it, the dotted outline of everything that was removed to leave it there."),
("XCU","-","PUSH", "EXTREME CLOSE-UP on one small clamp holding something absolutely still, gripping hard, enormous in frame."),
("MED","candid, open-handed","HOLD", f"{HERO} turning to face the viewer directly, both hands open, candid, no comedy in the face."),
("XWIDE","tiny, surrounded","PULL", f"{HERO} standing tiny in the exact centre of an enormous plain room whose four walls are visible on all sides, nothing else in it."),
("WIDE","posed, still","HOLD", "A row of identical frames on a wall, each containing the same character in exactly the same pose, absolutely uniform, unmoving."),
("MED","fixed, unblinking","HOLD", f"CLOSE on {HERO} standing perfectly still and unblinking beside a large pink ink drum and a large blue ink drum, and nothing else."),
("XWIDE","-","PANR", "A vast pristine landscape with no weather in it at all: no wind, no rain, no cloud, everything static and perfectly clean, one tiny figure at the edge."),
("MED","offering, gentle","HOLD", f"{HERO} holding out one small white mouse on his open palm toward the viewer, gently, unhurried."),
("CU","calm, honest","HOLD", f"CLOSE on {HERO} with a calm honest face, looking straight at the viewer, no gag."),
("XWIDE","tiny, walking out","PULL", f"An enormous frame: on the left a small spotless white room, and stretching away to the right an immense wild jungle. {HERO} is tiny, walking away from the room into the green."),
]

WORLD = (
 "a RISOGRAPH PRINT: printed in exactly TWO inks on uncoated off-white paper with "
 "visible paper tooth, and the paper is the SAME warm off-white across the whole "
 "frame with no cool grey and no pure white anywhere. The two inks are a bright "
 "FLUORESCENT PINK and a deep BLUE, and NOTHING ELSE — there is NO green, NO yellow, "
 "NO orange and NO brown anywhere in the image, and every plant, leaf and vine is "
 "printed in the pink or the blue like everything else. Every filled area is a "
 "coarse visible halftone of round dots, never a smooth flat fill. The two ink "
 "layers are slightly MISREGISTERED so their edges do not line up and a narrow band "
 "of bare paper shows along one side of every shape. Where the two inks overlap they "
 "multiply into a single darker violet. Semi-transparent ink, uneven roller coverage, "
 "patchy density, occasional streaking. Bold heavy outlines. No gradients, no soft "
 "shading, no glow, no drop shadows, no photographic texture. Edges slightly ragged "
 "from the screen. There is NO text, NO lettering, NO numbers and NO writing of any "
 "kind anywhere. 16:9, edge to edge, one scene, one camera.")

MIN_CAM = {'XCU': 6, 'CU': 6, 'OVER': 2, 'LOW': 1, 'XWIDE': 8}
MIN_MOVE = {'PUSH': 8, 'PULL': 6, 'PANL': 4, 'PANR': 8, 'TILTU': 2, 'TILTD': 4}
MAX_RUN = 3

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []
if len(S) != len(sents):
    errs.append(f'{len(S)} frames for {len(sents)} sentences — must be 1:1')

cams = [s[0] for s in S]; moves = [s[2] for s in S]
c, m = Counter(cams), Counter(moves)
for k, n in MIN_CAM.items():
    if c[k] < n: errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
for k, n in MIN_MOVE.items():
    if m[k] < n: errs.append(f'move quota: {k} has {m[k]}, needs {n}')
if c['XCU'] + c['CU'] < 12: errs.append(f"close-ups {c['XCU']+c['CU']}, needs 12")
for label, seq in (('camera', cams), ('move', moves)):
    run, prev = 1, None
    for i, v in enumerate(seq, 1):
        if v == prev:
            run += 1
            if run > MAX_RUN: errs.append(f'frame {i}: {run} consecutive {label} {v} (max {MAX_RUN})')
        else: run, prev = 1, v
named = sum(1 for s in S if s[1] != '-')
if named < 50: errs.append(f'expressions named on {named}, needs 50')

print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print('moves:   ' + '  '.join(f'{k}={v}' for k, v in sorted(m.items())))
print(f"close-ups {c['XCU']+c['CU']} | expressions named on {named}/{len(S)}")

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs: print('  ' + e, file=sys.stderr)
    sys.exit(1)

ids = [f'b{i:02d}' for i in range(1, len(S) + 1)]
(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{s[3]} {WORLD}' for i, s in zip(ids, S)}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'camera': s[0], 'expression': s[1], 'move': s[2], 'line': ln, 'scene': s[3]}
     for i, s, ln in zip(ids, S, sents)], indent=1))
print(f'\nwrote {len(ids)} prompts + board.json')
