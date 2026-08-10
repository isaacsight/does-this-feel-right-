#!/usr/bin/env python3
"""Frame book — Canoes Became Boats. 80 frames, one per sentence.

THE COLLAGE WORLD, from Isaac's mood board. Every frame is torn and cut paper
layered on cream stock, taped, with matte gold leaf accents. The medium IS the
argument here and that is why this world was chosen for this film: a memory is
not a recording played back, it is fragments reassembled — and every frame is
visibly fragments reassembled.

Proven by a 5-frame test ($0.20): it composes single coherent SCENES rather than
mood boards (the risk that mattered), the character survives as cut paper, torn
edges carry an expression better than riso did, and gold reads as flat matte leaf
with no gradient.

CLAIM REGISTER. The claims table in videos/memory-reconsolidation/CLAIMS.md is
reused: Bartlett and Loftus are Tier 1-2 Indicative and may be shown flat.
Reconsolidation is CONTESTED and this film does not touch it. Nunn & Reid 2016 is
stated with its hedge intact — the paper says stories "appear to" reach beyond
7,000 years, and the board must not draw a certainty the paper does not claim.

Every frame carries CAMERA, EXPRESSION and the picture. Expression is named on
every frame with a face because cognitive-debt v1 had ONE expression for seven
minutes, and no line of that board ever asked for a second.

FOUR MOTIFS, each the same object recurring:
  THE SCRAP     one torn piece of paper — a fragment of a memory
  THE CANOE     becomes a boat. Planted 28, paid off 34 and 74.
  THE COASTLINE the sea coming in. THE TURN, 55-60.
  THE HAND      someone else's hand, putting it right. 66, 76.

Run: python3 board.py    (writes production/prompts.json + board.json)
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

HERO = ("the recurring character, built from CUT AND TORN PAPER: a small round head "
        "cut from cream paper with deckled torn edges, EXACTLY TWO hairs standing up "
        "as torn paper slivers that KINK and LEAN at different angles and different "
        "lengths (never symmetrical, never vertical, never rabbit ears), a hooded "
        "jacket torn from VERMILION RED paper, trousers torn from deep COBALT BLUE "
        "paper, shoes cut from cream stock. Every part is a separate torn shape "
        "layered over the next, casting a faint hard paper shadow")

# (line, camera, expression, scene)   camera ∈ XCU CU MED WIDE XWIDE OVER LOW
#
# `line` is the 1-based sentence this frame sits under. Two frames may share a
# sentence — the film needs more cuts than it has sentences, and map-shots.py
# splits a shared sentence's span evenly between them. v1 was strictly 1:1 and ran
# a 5.8s mean hold, which is slow.
S = [
# ============ HOME — cream + vermilion, warm, safe ==========================
(1,"CU","warm, inviting", f"CLOSE on {HERO}, looking straight at the viewer with a warm open face, holding out one ABSURDLY small bright paper scrap on his flat palm toward us."),
(2,"XCU","-", "EXTREME CLOSE-UP on one small bright paper scrap, COLOSSAL in frame, built from about nine little torn pieces layered together, every seam visible."),
(3,"WIDE","fond, remembering", f"{HERO} standing in a warm cream room with three ENORMOUS floating paper fragments above him — a kitchen table, a window, a blank oval face — each far bigger than he is."),
(4,"MED","content, cradling", f"{HERO} cradling the nine-piece scrap in both hands, chin down, an ABSURDLY soft smile, the scrap glowing pale against his vermilion coat."),
(5,"XWIDE","tiny, setting out", f"A VAST cream field with a single torn ground line. {HERO} walks in from the left, TINY, the scrap held out ahead of him like a lantern."),
(6,"WIDE","uneasy, glancing back", f"{HERO} mid-stride, glancing back over his shoulder, while behind him a long trail of TINY dropped paper pieces stretches away to the horizon."),
# ============ ACT 2 — the traveller and his want ============================
(7,"MED","proud, presenting", f"{HERO} holding the nine-piece scrap up beside his face, presenting it, ABSURDLY pleased."),
(8,"XCU","-", "EXTREME CLOSE-UP on the scrap alone on cream, COLOSSAL in frame, still all nine pieces, one corner lifting."),
(9,"CU","careful, tongue out", f"CLOSE on {HERO} tucking the scrap into an ABSURDLY deep coat pocket with both hands, tongue poking out with care."),
(10,"WIDE","delighted, performing", f"{HERO} standing on a low table with the scrap held ABSURDLY high above his head, mouth wide, while five plain paper listeners below lean in with ENORMOUS round eyes."),
(11,"MED","determined, gripping", f"{HERO} gripping the scrap to his chest with both fists ABSURDLY tight, jaw set, whole body braced."),
(12,"XWIDE","small, hopeful", f"A VAST cream field. {HERO} TINY at the left edge, scrap in hand, facing a long empty ground line that runs off to the right, with a faint mustard shore in the far distance."),
# ============ ISLAND ONE — MUSTARD. Bartlett. ==============================
(13,"XWIDE","-", "A wide MUSTARD YELLOW island rising from a cream sea, with a TOWERING green paper archway on it, and a TINY figure just stepping ashore at its foot."),
(14,"WIDE","performing, oblivious", f"{HERO} on the mustard shore telling the story with both arms flung ABSURDLY wide, to nobody at all."),
(15,"XCU","-", "EXTREME CLOSE-UP on the scrap, COLOSSAL in frame, and one of its nine pieces is now a DIFFERENT shade and a different shape from the others, sitting proud of the surface."),
(15,"CU","unaware, cheerful", f"CLOSE on {HERO} smiling ABSURDLY wide and tucking the scrap away without once looking at it."),
(16,"WIDE","attentive, rows of them", "A mustard hall packed with DOZENS of identical plain paper students seated in rows, all leaning ABSURDLY far forward at the same angle."),
(17,"MED","-", "A TOWERING plain grey paper figure in a long coat handing down one enormous torn page to a TINY seated student, the page bigger than the student."),
(18,"WIDE","-", "The same torn page shown four times across the frame, each version visibly HALF the size and twice as ragged as the one before, the last barely a shred."),
(19,"XCU","-", "EXTREME CLOSE-UP: a pale paper CANOE, narrow and pointed, COLOSSAL and alone on mustard."),
(19,"XCU","-", "EXTREME CLOSE-UP: a pale paper BOAT, blunt and square, COLOSSAL, in exactly the same place and at exactly the same size as the canoe was."),
(20,"MED","-", "A TOWERING black paper ghost shape drifting off the top edge of the frame, leaving only its torn outline behind on the mustard ground."),
(21,"CU","conspiratorial, leaning in", f"CLOSE on {HERO} leaning ABSURDLY far into the camera with one eyebrow shot up and a small knowing smile, about to explain."),
(22,"MED","emphatic, palms open", f"{HERO} holding out both empty palms beside an ENORMOUS open filing box that is completely empty inside."),
(23,"WIDE","assembling, absorbed", f"{HERO} kneeling on mustard ground fitting torn pieces into a rough shape, and the pile of spare scraps beside him is ABSURDLY bigger than the shape itself."),
(24,"LOW","-", "Low camera looking up a TOWERING shelf that runs off the top of the frame. One lonely canoe shape on the bottom shelf. Every shelf above it crammed with DOZENS of identical boats."),
(25,"MED","matter-of-fact, filing", f"{HERO} on tiptoe posting a canoe shape into a drawer labelled with a boat silhouette, not even looking, an ABSURDLY tall ladder wobbling under him."),
(26,"XCU","-", "EXTREME CLOSE-UP on a seam between two torn pieces, COLOSSAL, the join almost impossible to find."),
# ============ ISLAND TWO — COBALT. Loftus. =================================
(27,"XWIDE","-", "A COBALT BLUE island rising from a cream sea, hard-edged and angular, with a TINY figure stepping ashore and the mustard island now small on the horizon behind him."),
(28,"MED","open, unsuspecting", f"{HERO} turning with an open friendly face toward a TOWERING plain grey paper figure who is simply holding out one blank card."),
(29,"CU","flinching, eyes wide", f"CLOSE on {HERO} flinching, eyes ABSURDLY wide, as an ENORMOUS jagged word-shape, bigger than his head, is pushed toward his ear."),
(29,"XCU","-", "EXTREME CLOSE-UP on the scrap, COLOSSAL in frame, and one more piece has changed — it is now a harsher, louder colour than the rest of it."),
(30,"WIDE","-", "Two blocky cut-paper cars, ABSURDLY toy-like, one vermilion and one cobalt, meeting on a cream ground with a small burst of torn yellow between them."),
(31,"MED","neutral, mild", "A plain grey paper figure standing at an ABSURDLY polite distance, TINY across a wide cream floor, holding a blank card, face completely flat."),
(32,"MED","forceful, looming", "The SAME grey figure now LOOMING ABSURDLY close, filling the frame, arm thrust forward, the card violently jagged."),
(33,"WIDE","-", "The same two paper cars again, but the burst between them is now THREE TIMES larger, exploding off the top of the frame."),
(34,"CU","dawning, mouth opening", f"CLOSE on {HERO} as it dawns on him, mouth beginning to open, both eyebrows climbing."),
(35,"WIDE","unsettled, glancing round", f"{HERO} standing in a cobalt room whose walls are made of ENORMOUS listening ears, glancing round, unsettled, the scrap clutched to his chest."),
(36,"WIDE","performing, uneasy", f"{HERO} back on the low table mid-gesture, and DOZENS of small scraps are drifting in from every edge toward the thing in his hands, unnoticed."),
(37,"MED","hollow, hands out", f"{HERO} holding the scrap out toward five listeners, and DOZENS of pieces are flying out of THEIR hands into it as he speaks, his face hollow."),
# ============ ACT 5 — THE BOX. near-black, cold, the low point =============
(38,"CU","frightened, wide-eyed", f"CLOSE on {HERO} genuinely frightened, eyes ABSURDLY wide, clutching the scrap so hard it crumples."),
(39,"WIDE","sealing, straining", f"{HERO} shoving the scrap into an ENORMOUS near-black box far bigger than he is, straining with both arms, one foot off the ground."),
(40,"LOW","exhausted, standing guard", f"Low camera looking up at a TOWERING glass case on a near-black plinth, with {HERO} TINY at its base, arms folded, eyes heavy, standing guard."),
(41,"XWIDE","tiny, alone", f"A VAST near-black field, empty, with {HERO} and his glass case TINY in the middle of it and absolutely nobody else anywhere."),
(42,"XCU","-", "EXTREME CLOSE-UP inside the glass case, the scrap COLOSSAL in frame, and it is down to SIX pieces now, with clean empty gaps where three used to be."),
(42,"CU","stricken, mouth open", f"CLOSE on {HERO} pressed against the glass, mouth open, seeing what has happened to it anyway."),
# ============ ISLAND THREE — BLUE SEA + GOLD. Nunn & Reid. =================
(43,"XWIDE","tiny, hesitating", f"A VAST cobalt paper sea with a distant shore, and {HERO} TINY in a small paper boat, oars up, hesitating."),
(44,"XWIDE","-", "A COLOSSAL blue coastline filling most of the frame, with a single MATTE GOLD LEAF sun hanging enormous and low above it."),
(45,"CU","awed, looking up", f"CLOSE on {HERO} looking up with an ABSURDLY wide open mouth, gold light on his face."),
(46,"XWIDE","-", "A VAST coast with twenty one small torn paper markers set in a long curving line along it, each with a TINY figure standing beside it."),
(47,"WIDE","-", "A TOWERING flat cobalt sea advancing across the frame, its torn edge ragged and far taller than the tiny hills it is swallowing."),
(48,"XWIDE","-", "A VAST scene of cobalt water with three TINY mustard hilltops still showing, and beneath the surface a faint torn outline showing how far the land once reached."),
(49,"MED","astonished, counting", f"{HERO} standing beside a COLOSSAL stack of torn paper layers running off the top of the frame, counting them on his fingers, astonished."),
(50,"CU","puzzled, head tilted", f"CLOSE on {HERO} with his head tilted ABSURDLY far over, brow furrowed, working something out."),
# ============ ACT 7 — the structure ========================================
(51,"WIDE","expectant, peering", f"{HERO} peering hopefully at four islanders with his eyes ABSURDLY wide, expecting something remarkable, on a gold-lit shore."),
(52,"MED","deflating, shoulders drop", f"{HERO} with his shoulders dropping ABSURDLY low, realising they are perfectly ordinary people."),
(53,"WIDE","-", "Two identical paper shapes on a shore. The left one stands inside a TOWERING lattice of paper strips. The right one stands alone and is buckling over."),
(54,"MED","proud, upright", "A family of five cut-paper figures standing in a line joined by torn paper cords, the eldest holding an ENORMOUS scrap above them all."),
(55,"WIDE","stern, correcting", "One islander reaching in with both hands to straighten a badly crooked ENORMOUS paper shape while another speaks with an ABSURDLY wide open mouth."),
(56,"CU","embarrassed, accepting", "CLOSE on an islander being corrected, cheeks flushed pink, taking it, not arguing."),
(57,"WIDE","industrious, swarming", "SIX cut-paper figures swarming over one COLOSSAL paper shape laid across the whole frame, each holding a piece in place, one taping a seam."),
# ============ ACT 8 — back to island one ===================================
(58,"MED","realising, turning", f"{HERO} turning sharply to look back across a VAST sea toward the TINY distant mustard island, eyes wide."),
(59,"WIDE","-", "A COLOSSAL pair of near-black paper scissors lifting one TINY scene out of a vast paper tapestry, leaving a clean hole."),
(60,"WIDE","-", "A mustard hall where every seat is empty, DOZENS of them, and one lone torn scrap sits on the floor in the middle."),
(61,"XWIDE","-", "A VAST empty field with one TINY figure sitting alone holding a scrap, and absolutely nobody within reach of him."),
(62,"WIDE","-", "One paper shape collapsed into a heap of separate pieces spread ABSURDLY wide across the frame, nothing holding any of it together."),
(63,"CU","fair, plain", f"CLOSE on {HERO} nodding once with a plain fair face, giving Bartlett his due, no gag."),
(64,"WIDE","-", "The same collapsed heap, and standing around it the clear torn OUTLINE of a TOWERING frame that is no longer there."),
(65,"MED","pointed, gesturing", f"{HERO} gesturing at the TOWERING empty outline with both arms flung wide, eyebrows up, making the point."),
(66,"WIDE","identical, blank", "Four identical plain paper figures in a row with COMPLETELY blank flat faces, beneath a TOWERING archway that dwarfs them."),
(67,"CU","direct, asking", f"CLOSE on {HERO} looking straight down the lens, one brow raised, asking it back at us."),
# ============ ACT 9 — HOME, the return =====================================
(68,"XWIDE","tiny, arriving", f"A VAST warm cream field at dusk with {HERO} TINY, walking home along a torn ground line, the gold sun low behind him."),
(69,"MED","nervous, offering", f"{HERO} holding the six-piece scrap out toward three paper figures, hesitant, ABSURDLY small in the gesture."),
(70,"WIDE","interrupted, mouth open", f"{HERO} mid-sentence with three figures all talking at once around him, their mouths ABSURDLY wide, hands reaching in toward the scrap."),
(71,"CU","stung, blinking", f"CLOSE on {HERO} blinking, mouth half open, being contradicted and taking it."),
(72,"XCU","-", "EXTREME CLOSE-UP on the scrap, COLOSSAL in frame and now only FOUR pieces, half the size it was — but each piece pressed flat and solid, edges clean."),
(73,"WIDE","held, steady", f"{HERO} and three figures all holding the small four-piece scrap up together, six hands on it, and it is finally still."),
# ============ ACT 10 — what to do ==========================================
(74,"CU","warm, direct", f"CLOSE on {HERO} looking straight at the viewer with a warm face, holding up the small solid scrap toward us."),
(75,"MED","protective, refusing", f"{HERO} pulling the scrap back from an ABSURDLY large open bin yawning at his feet."),
(76,"XCU","-", "EXTREME CLOSE-UP on a smooth join, COLOSSAL in frame, with a thin line of MATTE GOLD LEAF running along it making the seam suddenly visible."),
(77,"MED","stopping, hand up", f"{HERO} holding up an ABSURDLY large flat hand to stop us, shaking his head, brow raised."),
(78,"WIDE","building, determined", f"{HERO} with sleeves up, hammering together a TOWERING lattice of paper strips around the small scrap."),
(79,"OVER","-", "Straight-down overhead of an ENORMOUS blank cream sheet with one TINY cut-paper pen resting on it. No writing."),
(80,"WIDE","open, mid-sentence", f"{HERO} talking with an ABSURDLY wide open mouth while a friend reaches in with both hands to adjust the shape between them."),
(81,"MED","stubborn, turning away", "A second cut-paper figure clutching its own ABSURDLY warped and buckled shape, turning away, refusing to let anyone near it."),
# ============ ACT 11 — the confession ======================================
(82,"CU","candid, plain", f"CLOSE on {HERO} facing the viewer, both hands open, candid, no comedy at all."),
(83,"XWIDE","-", "A VAST empty cream field with a COLOSSAL machine of torn scraps assembling a shape in mid-air, and absolutely nobody anywhere near it."),
(84,"WIDE","-", "The machine's shape standing alone, and all around it the torn OUTLINE of a family that is not there — TOWERING, empty."),
(85,"MED","urging, leaning in", f"{HERO} leaning ABSURDLY far toward the viewer, one hand out, urging us."),
(86,"XWIDE","tiny, walking away", f"A VAST warm cream field with {HERO} TINY, walking away from us toward three distant paper figures, the small scrap held out ahead of him."),
]

WORLD = (
 "a PAPER COLLAGE: the entire image is built from torn and cut pieces of paper layered "
 "on a warm cream paper ground, and every shape has a visibly TORN OR DECKLED EDGE with "
 "the white core of the paper showing along the tear. Pieces overlap and cast faint "
 "hard-edged paper shadows, and a few are held down with short strips of pale masking "
 "tape. The palette is strictly limited to VERMILION RED, deep COBALT BLUE, soft BLUSH "
 "PINK, MUSTARD YELLOW, dark FOREST GREEN, near-BLACK and the cream paper itself, plus "
 "small accents of flat MATTE GOLD LEAF. Surfaces carry real paper texture: some pieces "
 "show coarse halftone dot printing, some thick dry brushed paint, some plain flat pulp. "
 "Flat matte finish throughout: NO gradients, NO soft airbrushed shading, NO glow, NO "
 "metallic sheen or shine on the gold, NO photographic texture, and no shadows other "
 "than the hard paper offsets. There is NO text, NO lettering, NO numbers and NO writing "
 "of any kind anywhere in the image. This is ONE SINGLE COHERENT SCENE assembled from "
 "paper, NOT a mood board, NOT a grid of samples, NOT a sheet of unrelated swatches. "
 "16:9, edge to edge, one scene, one camera.")

MIN_CAM = {'XCU': 6, 'CU': 6, 'OVER': 1, 'LOW': 2, 'XWIDE': 8}
MAX_RUN = 3

# Enforced after v1 of this board came back flat. Measured: 60% of frames had no
# character in them at all, 52% named no expression, and only 11% named any
# exaggeration. That is the drift that got `who-you-measured` shelved — a film of
# objects reads as a diagram, and the character is what carries these.
#
# EXAGGERATION IS REQUIRED ON EVERY FRAME, including object-only ones. An
# environment can be exaggerated: absurd scale, absurd quantity, a thing far
# larger or far smaller than it should be. "A box on the ground" is a diagram;
# "a box the size of a room, and a tiny door in it" is a picture.
MIN_HERO_SHARE = 0.55      # he must be IN most of the film
MIN_EXAG_SHARE = 0.85      # nearly every frame does something past realism.
# Not 1.0 on purpose: a handful of beats are deliberately plain — the look to
# camera, the confession, the honest nod — and they only land because everything
# around them is pushed. Exaggeration everywhere is exaggeration nowhere.
# Case-INSENSITIVE. The first version listed some words in lower case only and
# under-counted frames that shouted them — HUNDREDS, DOZENS, HALF THE all missed.
# A matcher that disagrees with itself makes you rewrite scenes that were already
# right, which is the same trap as measuring the gate's ground with a different
# mask from the check.
EXAG = re.compile(r'\b(enormous|absurd\w*|vast|towering|tiny|colossal|impossibl\w+|'
                  r'far (?:bigger|larger|smaller|taller)|hundreds|dozens|'
                  r'off the (?:top|edge)|many times|twice (?:the|its)|half (?:the|its)|'
                  r'crumpling|flying out|swarming|teeter\w*|yawning)\b', re.I)

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []
lines = [s[0] for s in S]
if sorted(set(lines)) != list(range(1, len(sents) + 1)):
    missing = set(range(1, len(sents) + 1)) - set(lines)
    errs.append(f'every sentence needs at least one frame; missing {sorted(missing)[:8]}')
if max(lines) > len(sents):
    errs.append(f'frame points at sentence {max(lines)}, script has {len(sents)}')
cams = [s[1] for s in S]
c = Counter(cams)
for k, n in MIN_CAM.items():
    if c[k] < n:
        errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
if c['XCU'] + c['CU'] < 12:
    errs.append(f"close-ups {c['XCU'] + c['CU']}, needs 12")
run, prev = 1, None
for i, cam in enumerate(cams, 1):
    if cam == prev:
        run += 1
        if run > MAX_RUN:
            errs.append(f'frame {i}: {run} consecutive {cam} (max {MAX_RUN})')
    else:
        run, prev = 1, cam
# The world's own failure mode, forbidden at the board as well as in the clause.
for i, (_, _, _, sc) in enumerate(S, 1):
    if re.search(r'\b(mood ?board|swatch|grid of|collage of samples)\b', sc, re.I):
        errs.append(f'frame {i}: describes a board of samples, not a scene')

hero = [s for s in S if 'recurring character' in s[3]]
exag = [s for s in S if EXAG.search(s[3])]
named = sum(1 for s in S if s[2] != '-')
# Every frame he is in must say what his face is doing.
faceless = [i for i, s in enumerate(S, 1)
            if 'recurring character' in s[3] and s[2] == '-']

if len(hero) / len(S) < MIN_HERO_SHARE:
    errs.append(f'character in {len(hero)}/{len(S)} frames '
                f'({len(hero)/len(S):.0%}), needs {MIN_HERO_SHARE:.0%}')
if len(exag) / len(S) < MIN_EXAG_SHARE:
    errs.append(f'exaggeration named on {len(exag)}/{len(S)} '
                f'({len(exag)/len(S):.0%}), needs {MIN_EXAG_SHARE:.0%}')
if faceless:
    errs.append(f'character present but no expression named: '
                f'{" ".join("b%02d" % i for i in faceless[:12])}')

print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {c['XCU'] + c['CU']} | expressions {named}/{len(S)} | "
      f"character {len(hero)}/{len(S)} ({len(hero)/len(S):.0%}) | "
      f"exaggeration {len(exag)}/{len(S)} ({len(exag)/len(S):.0%})")

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs:
        print('  ' + e, file=sys.stderr)
    sys.exit(1)

ids = [f'b{i:02d}' for i in range(1, len(S) + 1)]
(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{s[3]} {WORLD}' for i, s in zip(ids, S)}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'expression': s[2],
      'line': sents[s[0] - 1], 'scene': s[3]} for i, s in zip(ids, S)], indent=1))
print(f'\nwrote {len(ids)} prompts + board.json')
