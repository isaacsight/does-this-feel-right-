#!/usr/bin/env python3
"""Board v2 — the exaggeration pass.

The v1 board produced 88 frames that were, in Isaac's words, boring and
unexaggerated. Reviewing all four contact sheets: roughly 70 of 88 were the same
shot (full-body figure, side-on, on a ground line at a fixed height), the
protagonist wore one expression throughout, and whole runs were near-duplicates -
six consecutive "figure at a desk in the cap" frames in Act 2 alone.

A $0.31 six-frame pilot established what fixes it, and every scene below carries
all three of those moves:

  SCALE       something is absurdly large or absurdly small, or there are
              absurdly many of it
  POSTURE     the body does what the sentence says, past the point of realism
  CAMERA      a quota, enforced at the bottom of this file: no more than three
              consecutive frames may share a camera distance, and the film must
              carry at least 12 close-ups, 6 overheads, 6 low angles and 8
              extreme wides. v1 had two close-ups and no overheads at all.

Every frame also names an EXPRESSION, because v1's protagonist had one face for
seven and a half minutes.

Run: python3 board-v2.py          (writes production/prompts.json, checks quota)
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

HERO = ("the protagonist - small round head, EXACTLY TWO fine hairs standing up, "
        "tomato-red hooded jacket, black trousers, cream shoes")

# The stair is the film's principal motif and appears in six frames. Boarded ONCE
# here so all six agree: v1's version was a modest six-step flight, which is why the
# central image of the film had no weight.
STAIR = ("an ENORMOUS pale sage staircase of flat rectangular treads climbing from "
         "the bottom-left to off the TOP-RIGHT corner of the frame, each tread far "
         "taller than the protagonist")

# (camera, expression, scene)  — camera is one of
# XCU CU MED WIDE XWIDE OVER LOW
S = {
"b01": ("XWIDE","-", f"A vast empty field of ruled paper. Far away at the bottom left, absurdly tiny, a plain rectangular table with {HERO} seated at it, seen from behind and above. The figure is no taller than the gap between two ruled lines. Nothing else in the entire frame."),
"b02": ("LOW","squinting", f"Low camera looking up. A single bare bulb on a long cord hangs ABSURDLY low beside the head of {HERO}, who is hunched under it, squinting with eyes narrowed to two lines. Beneath the bulb a wide hard-edged cone shape spreads down and outward across the ground, drawn as a SLIGHTLY PALER TINT OF THE SAME SAGE PAPER with a thin near-black outline. Nothing else."),
"b03": ("OVER","-", f"Straight-down overhead. One enormous blank pale sheet fills almost the whole frame. At the very bottom edge, two TINY cream hands rest on the paper's edge, comically small against it. Nothing else."),
"b04": ("OVER","-", "Straight-down overhead. Three blank pale sheets fanned out. The third sheet is ABSURDLY long and unspools off the right edge of the frame like a ribbon, far longer than the other two. Nothing else."),
"b05": ("MED","hugely smug, eyes closed, chin up", f"{HERO} leaning back at an IMPOSSIBLE backward angle in a plain chair, balanced on one chair leg, both hands behind the head, feet up on a table edge. Enormously pleased with themselves. Nothing else."),
"b06": ("WIDE","-", f"{STAIR}. One tread near the middle is MISSING, leaving a clean rectangular gap of blank ruled paper. No figure at all. Nothing else."),
"b07": ("XWIDE","tiny, head tipped back", f"{STAIR}, with one tread near the middle missing. At the very bottom left, {HERO} stands TINY at the foot of it, head tipped right back to look up, one arm pointing up at the gap. Nothing else."),
"b08": ("WIDE","mouth open", f"{STAIR} with one tread missing. A single solid TOMATO-RED tread, identical in shape to the others, HOVERS in the air directly above the gap, unsupported. {HERO} stands tiny at the foot, mouth open. Nothing else."),
"b09": ("MED","blank, eyes wide open", f"{HERO} seated bolt upright gripping a plain flat steering wheel, drawn as a simple near-black circle. Behind them the ruled paper streaks past as long horizontal motion lines. Their eyes are wide and completely blank. NO car body, no windows, no wheels - only the figure, the wheel, and the streaking lines."),
"b10": ("XWIDE","-", f"A wide field of ruled paper with a long row of ELEVEN identical figures, each {HERO}, all standing in exactly the same pose facing the camera with hands in pockets, evenly spaced across the whole width. Every one of them looks away from the viewer at the same angle. Nothing else."),
"b11": ("CU","-", "CLOSE on a plain flat pale machine on a desk, seen from the side. From it extends an ABSURDLY long single line of near-black that runs off the right edge of the frame, like a sentence continuing forever. Two tiny cream hands rest on the machine. No face in frame."),
"b12": ("LOW","-", "Low camera looking steeply up at one colossal blank pale sheet standing upright like a monolith, running off the top edge of the frame. Its shadow falls across the ruled ground toward the camera. Nothing else."),
"b13": ("XWIDE","-", "A vast ruled field packed with FIFTY-FOUR identical small figures, each seated at an identical tiny desk in even rows receding to a high horizon, all wearing a close-fitting pale cap studded with small round near-black discs. All identical, all still. Nothing else."),
"b14": ("CU","gritted, sweating brow lines", f"CLOSE on a huge hourglass standing on the ruled ground, taller than {HERO} who stands beside it at half its height, staring at it. The sand column inside is thick and clearly falling. The figure's brow carries two short tension lines. Nothing else."),
"b15": ("MED","delighted, wide grin", f"{HERO} seated at a desk, arms flung wide in delight, while an ABSURD tower of finished pale sheets stacks itself up from the desk and runs off the top of the frame. Nothing else."),
"b16": ("MED","tired, heavy-lidded", f"{HERO} seated at a desk surrounded by a dense fan of MANY small pale rectangles floating in the air around their head, each a plain blank card. The figure's eyes are heavy-lidded. Nothing else."),
"b17": ("CU","furrowed, mouth a flat line", f"CLOSE on the head and shoulders of {HERO}, three-quarter view, no cap, brow deeply furrowed, mouth a hard flat line, staring down at a single blank pale sheet held up close to the face. Nothing else."),
# A "web of lines" asks for verticals and reads as lettering: this frame failed the
# gate three times, twice on the forbidden margin rule and once on a drawn "WES".
# Every connector is now explicitly DIAGONAL and short.
"b18": ("XCU","-", "EXTREME CLOSE-UP filling the whole frame: many small solid near-black dots scattered evenly across the field, joined to their neighbours by short DIAGONAL near-black strokes, like a constellation. Every connecting stroke runs at a slant - there are NO vertical strokes and NO long straight lines of any kind, and nothing forms a letter, a word or a number. The ruled paper shows behind, its horizontal lines enormous and far apart at this scale. No figure."),
"b19": ("MED","calm, eyes closed, serene", f"{HERO} seated, wearing a close-fitting pale cap studded with small round near-black discs. From the cap erupt FAR TOO MANY fine near-black cords - dozens - spraying outward and upward to fill the whole frame like a fountain and trailing off all four edges. The figure sits perfectly still, hands folded, eyes closed, serene. Nothing else."),
"b20": ("WIDE","chest out, proud", f"Three figures side by side, each {HERO}. Above the FIRST one's head floats a huge dense web of fine near-black lines and dots. Above the second, a much smaller web. Above the third, a single lonely dot. The first figure stands chest out and proud. Nothing else."),
"b21": ("MED","sheepish, shoulders raised", f"CLOSE on the THIRD figure only - {HERO} - shoulders raised to the ears, sheepish, with one single small near-black dot floating above the head where a web should be. Nothing else."),
"b22": ("LOW","-", f"Low camera looking up at a tall plain figure in a plain grey coat, ENORMOUS in the frame, leaning down from above with one hand extended toward the camera. Far below at the bottom of the frame, the top of the head of {HERO}, tiny. Nothing else."),
"b23": ("XCU","mouth open, eyes wide, panicked", f"EXTREME CLOSE-UP on the face of {HERO} filling the frame: mouth open in a wide O, eyes wide, two short lines beside the head for panic. Nothing else."),
"b24": ("WIDE","five blank, one straining", f"SIX identical figures, each {HERO}, standing in a row. FIVE of them have completely blank white speech-less expressions and empty open hands. The SIXTH, at the far right, strains with one finger raised. Nothing else."),
"b25": ("OVER","-", "Straight-down overhead of a plain flat pale machine, closed, with one blank pale sheet beside it and a single tiny cream hand withdrawing off the frame edge. Nothing else."),
"b26": ("CU","-", "CLOSE on a heavy pale ledger book lying shut on the ruled ground, ENORMOUS, filling most of the frame, with one thin tomato-red band across its cover. No writing of any kind on it. No figure."),
"b27": ("XWIDE","chin up, not looking", f"A single towering stack of loose pale sheets so tall it runs off the TOP EDGE of the frame and leans visibly. At its base {HERO}, drawn TINY, no taller than four sheets, strides past left to right with chin lifted, pointedly not looking at it. Low camera. Nothing else."),
"b28": ("WIDE","mouths open, arms flung", f"A ring of SEVEN identical figures, each {HERO}, all facing inward with mouths open and both arms flung wide, all talking at once. In the centre of the ring, one small blank pale card lies on the ground, ignored. Nothing else."),
"b29": ("LOW","-", "Low camera looking up at a single thin blank pale sheet standing upright on its edge, absurdly tall and thin, running off the top of the frame, wobbling. Nothing else."),
"b30": ("XCU","-", "EXTREME CLOSE-UP on the corner of one blank pale sheet, filling the frame, its edge frayed and curling. The ruled paper enormous behind it. No writing anywhere. No figure."),
"b31": ("XWIDE","-", "A vast ruled field with FIFTY-FOUR identical tiny figures standing in even ranks, receding to a high horizon. All are pale grey and featureless except the front rank. Nothing else."),
"b32": ("MED","confused, one eyebrow up", f"{HERO} standing between TWO plain flat pale machines, holding one in each hand at arm's length and looking from one to the other, one eyebrow raised high in confusion. Nothing else."),
"b33": ("XWIDE","-", "An ENORMOUS empty ruled field. In it, EIGHTEEN tiny figures stand in a loose scatter, absurdly small and far apart, occupying only the bottom fifth of the frame. Everything above them is blank ruled paper. Nothing else."),
"b34": ("WIDE","-", "Two solid tomato-red rectangular blocks side by side on the ruled ground. The LEFT block is ENORMOUS, three times the height of the right. The right block is small. Identical shape, wildly different size. No figure."),
"b35": ("CU","caught out, eyes darting sideways", f"CLOSE on the head and shoulders of {HERO}, eyes swivelled hard to one side, caught out, one hand half-raised as if to speak. Nothing else."),
"b36": ("MED","deflating, shoulders sagging", f"{HERO} standing, body DEFLATED and sagging like an emptying balloon, shoulders melted downward, arms hanging far too long, almost to the ground. Nothing else."),
"b37": ("WIDE","-", f"One ENORMOUS tomato-red block, and beside it a block exactly one third its height, both on the ground line. {HERO} stands between them, tiny, looking up at the big one. Nothing else."),
"b38": ("WIDE","stern, arms crossed", "FOUR identical plain grey figures in plain grey coats standing shoulder to shoulder in a row, arms crossed, all facing the camera, stern. They are much taller than the frame's ground line suggests. Nothing else."),
"b39": ("OVER","-", "Straight-down overhead of a blank pale sheet with FOUR large near-black tick-marks scored across it in a column, each a simple flat stroke. No writing, no numbers, no letters. Nothing else."),
"b40": ("XCU","-", "EXTREME CLOSE-UP of one huge open eye drawn in flat near-black linework on cream, pupil wide, filling the frame. Reflected in the pupil, one small flat tomato-red rectangle. Nothing else."),
"b41": ("MED","baffled, both palms up", f"{HERO} standing with both palms turned up and shoulders raised in a huge exaggerated shrug, arms absurdly wide apart, head tilted. Nothing else."),
"b42": ("WIDE","-", "A long horizontal near-black line running the full width of the frame with TWO plain pale markers standing on it, one far to the left and one far to the right, an absurd distance apart. Nothing else."),
"b43": ("LOW","-", "Low camera looking up at one ENORMOUS blank pale magazine page standing upright, running off the top of the frame, curling at its top corner. Nothing else."),
"b44": ("MED","deadpan, staring straight at the viewer", f"{HERO} standing dead centre, staring directly at the viewer with a completely deadpan face, holding up one enormous blank pale sheet beside their head. Nothing else."),
"b45": ("CU","absorbed, eyes down", f"CLOSE on {HERO} seated side-on, holding an open pale book close to the face, absorbed, eyes cast down. Nothing else."),
"b46": ("MED","drooping, eyes closed", f"{HERO} seated holding an open pale book. Their head and neck have drooped ABSURDLY far forward and down, stretching like warm rubber, the head hanging below the level of the seat, eyes closed. From the book one pale ribbon of page unspools off the right edge of the frame. Nothing else."),
"b47": ("WIDE","-", f"{HERO} standing beside an identical-sized plain grey figure, the two of them holding up matching blank pale sheets side by side, comparing them. Nothing else."),
# "question-hook shape" invited a literal drawn "?" — which turned up, huge and red,
# in b72 of all places. Never name a glyph, even to forbid it: the model draws the
# label. Same trap as the hex code that came back as the string D9EE13D.
"b48": ("OVER","-", "Straight-down overhead of one blank pale sheet lying alone on the ruled ground. Across it lies a single plain near-black curved stroke, like a length of cord dropped on the paper, with both ends free. It forms no letter, no number and no symbol of any kind. Nothing else."),
"b49": ("WIDE","-", "A plain grey figure in a long robe standing at the left, and at the right a plain flat pale machine on a stand. Between them on the ruled ground lies one blank pale scroll, half unrolled, ABSURDLY long, running off both edges of the frame. Nothing else."),
"b50": ("CU","one eyebrow raised, wry", f"CLOSE on the head of {HERO} turned to the camera, one eyebrow raised high, mouth slightly crooked, wry, one finger raised beside the face. Nothing else."),
"b51": ("WIDE","-", "Two blank pale sheets standing upright on the ruled ground, far apart. The LEFT one is heavily creased and yellowed at the edges and much larger; the RIGHT one is small and crisp. No figure at all."),
"b52": ("WIDE","-", "THREE blank pale sheets standing upright on the ruled ground in a row, decreasing in size sharply from left to right, the leftmost enormous and the rightmost tiny. No figure at all."),
"b53": ("CU","-", "CLOSE on the bottom corner of one blank pale sheet, lifted and curling, with ONE small solid tomato-red dot sitting alone at its very bottom edge. One cream hand holds the corner. Nothing else."),
"b54": ("OVER","-", "Straight-down overhead of one blank pale sheet at the very bottom of a stack of many, with a single small tomato-red dot at its lowest edge. The stack above is enormous. Nothing else."),
"b55": ("WIDE","-", "Two blank pale sheets on the ruled ground with a clear gap between them. The LEFT sheet is much larger and sits forward; the RIGHT is small and set back. No figure at all."),
"b56": ("XCU","eyes narrowed to slits", f"EXTREME CLOSE-UP on the eyes only of {HERO}, filling the frame, narrowed hard to two flat slits. Nothing else."),
"b57": ("LOW","tiny, looking up", f"An ENORMOUS solid tomato-red rectangular block occupying most of the frame, resting on the ground line and running off the top edge. {HERO} stands beneath its overhang, drawn TINY, arms hanging, looking up. Their whole body is shorter than the block's thickness. Nothing else."),
"b58": ("XWIDE","-", "A vast ruled field with a long line of many identical small figures walking left to right in single file toward the horizon, each identical, stretching off both edges of the frame. Nothing else."),
"b59": ("WIDE","-", "FOUR plain grey figures standing in a row, each holding up one blank pale sheet at exactly the same height and angle. Absolutely identical postures. Nothing else."),
"b60": ("CU","-", "CLOSE on one enormous pale ledger book lying open on the ruled ground, both pages completely blank, filling the frame. No writing of any kind. No figure."),
"b61": ("MED","alarmed, eyebrows shot up", f"{HERO} standing bolt upright, both hands flying up beside the head, eyebrows shot high, hair standing straight, as a huge blank pale card drops in from the top of the frame toward them. Nothing else."),
"b62": ("XCU","pupils sliding hard to one side", f"EXTREME CLOSE-UP on one enormous eye of {HERO}, the pupil slid hard to one side, straining. Nothing else."),
"b63": ("MED","vacant, mouth slightly open", f"{HERO} standing with a completely vacant face, mouth slightly open, while a single long fine near-black line runs from the back of their head off the right edge of the frame. Nothing else."),
"b64": ("LOW","-", "Low camera looking up at ONE enormous pale block standing on a plain plinth, monumental, running off the top of the frame. No figure at all. Nothing else."),
"b65": ("XWIDE","-", "A vast ruled field with TEN identical pale plinths in a long row receding to the horizon, each carrying an identical pale block, absolutely uniform. No figure at all."),
"b66": ("WIDE","-", "TWENTY-ONE small identical pale blocks standing in a long row on the ruled ground. THIRTEEN of them stand upright; the other eight have FALLEN FLAT on their faces. No figure at all."),
"b67": ("CU","-", "CLOSE on ONE pale block lying flat on its face on the ruled ground, alone, filling much of the frame, with an empty plinth behind it. No figure."),
"b68": ("WIDE","-", "TWO empty plain pale plinths side by side on the ruled ground, both completely bare, one twice the width of the other. No figure at all. Nothing else."),
"b69": ("XWIDE","-", "One small bare pale plinth alone in an ENORMOUS empty ruled field, tiny and off centre, everything else blank ruled paper to all four edges. Absolutely no figure and no person of any kind anywhere in the frame. Nothing else."),
"b70": ("XWIDE","-", "A vast ruled field with many identical small figures walking left to right in a long stream, and among them one empty gap where a figure should be. Nothing else."),
"b71": ("WIDE","all nodding, eyes closed", f"FIVE identical figures, each {HERO}, standing in a row all nodding with eyes closed and chins down in perfect agreement, while behind them one blank pale sheet blows away off the frame edge unnoticed. Nothing else."),
"b72": ("CU","-", "CLOSE on the bottom corner of one blank pale sheet, lifted and curling, held by one cream hand. The bottom edge of the sheet is COMPLETELY BARE - no dot, no mark of any kind on it. Nothing else."),
"b73": ("MED","relieved, then faltering", f"{HERO} standing mid-stride with both arms raised in relief, but the face has already fallen - mouth turned down, eyes wide. Caught between two feelings. Nothing else."),
"b74": ("WIDE","-", "Two solid tomato-red blocks on the ruled ground. The LEFT one has toppled and lies flat. The RIGHT one, much smaller and duller, still stands upright. No figure."),
"b75": ("MED","carefully pleased", f"{HERO} placing one small pale box onto a plain bracketed shelf board mounted high on the ruled ground, up on tiptoe, tongue out in concentration, a second identical box under one arm. Nothing else."),
"b76": ("MED","strained, both arms shaking", f"{HERO} reaching far up to place a SECOND identical pale box beside the first on the same plain bracketed shelf board at the same height, stretched to full extent, both arms shaking with two short motion lines. Two boxes on the shelf. Nothing else."),
"b77": ("LOW","stretching, fingertips short", f"Low camera looking steeply up. The same plain bracketed shelf board is now ABSURDLY high overhead with both pale boxes on it, tiny with distance. {HERO} stands far below reaching up with one arm at full stretch, fingertips nowhere near it, mouth open. Nothing else."),
"b78": ("XWIDE","arms down, dwarfed", f"An enormous empty ruled field. {HERO} stands TINY in the middle of a vast clear floor, arms down, with the plain bracketed shelf board far above and the two boxes on it reduced to specks. Nothing else."),
"b79": ("OVER","-", "Straight-down overhead of one plain flat pale machine lying open, one blank pale sheet beside it, and one plain drawing pen lying down, in a neat row on the ruled ground. Absolutely no figure and no hands anywhere in the frame. Nothing else."),
"b80": ("CU","-", "CLOSE on one plain flat pale machine, closed shut, with a fine near-black seam all the way round it and NO way in - no handle, no catch, no opening. Filling the frame. No figure."),
"b81": ("XWIDE","-", f"A vast ruled field. {HERO} walks right to left at the right third of the frame, and the long near-black ground line is drawn only AHEAD of them, to the left edge. Behind them, blank paper with no line at all. Nothing else."),
"b82": ("OVER","-", "Straight-down overhead of one blank pale sheet lying alone on the ruled ground with ONE cream hand flat beside it, fingers spread. No marks of any kind on the paper. Nothing else."),
"b83": ("WIDE","-", f"{STAIR}, with one tread near the middle MISSING, leaving a clean rectangular gap of blank ruled paper. No figure at all. Nothing else."),
"b84": ("MED","mouth wide open, shouting", f"{HERO} standing alone, head tipped back, mouth open ABSURDLY wide in a shout, both fists clenched at the sides. The vast ruled field around them is completely empty - nobody is there. Nothing else."),
"b85": ("XCU","-", f"EXTREME CLOSE-UP on three enormous stair treads. The MIDDLE tread is solid tomato-red; the ones above and below are pale sage. One small cream hand with a slim near-black cuff reaches in from the left edge and touches the red tread with the fingertips. The hand and cuff are SMALL against the treads. No red anywhere except the single middle tread. Nothing else."),
"b86": ("WIDE","-", "TWO identical blank pale cards standing side by side on the ruled ground, exactly the same size and shape, indistinguishable. No figure."),
"b87": ("XCU","-", "EXTREME CLOSE-UP filling the frame on the flat outline of a shape - a plain near-black outlined rectangle - which is completely EMPTY inside, showing the ruled paper through it. Nothing else."),
"b88": ("XWIDE","-", f"An ENORMOUS empty ruled field seen from high and far. At the very bottom, absurdly tiny, {HERO} stands alone facing away from the camera, no taller than the gap between two ruled lines, with a vast blank page above and around them. Nothing else."),
}

# --------------------------------------------------------------------------
# Quota check. v1 failed exactly here, and it failed silently because nobody was
# counting. This refuses to write the prompt set rather than reporting afterwards.
MIN = {'XCU': 6, 'CU': 6, 'OVER': 6, 'LOW': 6, 'XWIDE': 8}
MAX_RUN = 3

def check():
    ids = [f'b{i:02d}' for i in range(1, 89)]
    missing = [i for i in ids if i not in S]
    if missing:
        return [f'missing scenes: {" ".join(missing)}']
    errs = []
    cams = [S[i][0] for i in ids]
    c = Counter(cams)
    for k, n in MIN.items():
        if c[k] < n:
            errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
    run, prev = 1, None
    for i, cam in zip(ids, cams):
        if cam == prev:
            run += 1
            if run > MAX_RUN:
                errs.append(f'{i}: {run} consecutive {cam} shots (max {MAX_RUN})')
        else:
            run, prev = 1, cam
    close = c['XCU'] + c['CU']
    if close < 12:
        errs.append(f'close-ups {close}, needs 12')
    print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
    print(f'close-ups {close} | expressions named on {sum(1 for i in ids if S[i][1] != "-")} frames')
    return errs

errs = check()
if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs:
        print('  ' + e, file=sys.stderr)
    sys.exit(1)

old = json.loads((FILM / 'production' / 'prompt-archive' / 'prompts-v1.json').read_text()) \
    if (FILM / 'production' / 'prompt-archive' / 'prompts-v1.json').exists() \
    else json.loads((FILM / 'production' / 'prompts.json').read_text())
tail = old['b27'][old['b27'].find('a LEDGER world'):]

# The v2 board pushes scale and lighting, and the first smoke frame came back with a
# huge PURE WHITE light cone — a value that does not exist in this world and that the
# gate cannot see, because white is unsaturated and the ground check reads the median.
# Cheaper to forbid it in every prompt than to detect it in every frame.
NO_WHITE = (" There is NO pure white anywhere in the image: the palest tone in the "
            "frame is the pale sage paper itself, and every object is either that "
            "sage, a slightly paler or darker tint of it, the near-black linework, "
            "or the single tomato-red accent.")
out = {i: S[i][2] + ' ' + tail + NO_WHITE for i in (f'b{n:02d}' for n in range(1, 89))}
(FILM / 'production' / 'prompts.json').write_text(json.dumps(out, indent=1))
print(f'\nwrote {len(out)} prompts')
