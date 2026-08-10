#!/usr/bin/env python3
"""Frame book — The Pettiest Wars (working title). One frame per sentence,
extras on the long ones.

THE BAYEUX WORLD (see WORLD.md). Stitched wool on linen — the medium wars get
mythologized in, telling the story of how trophies replace causes.

THE COMEDY-WRITER'S BOARD. The frame never illustrates the joke; it is a
second joke. Five tools, used throughout and enforced where a machine can:

  REACTION    cut to the witness, not the event (the cook, not the kettle)
  DISAGREE    background contradicts foreground (the pig never reacts, ever)
  LADDER      same composition repeated with ONE variable worse each time
              (b13-b15 the bucket's promotion; b58/60/62 the three trophies)
  RUNNER      the fortress on the horizon UNRAVELS a little more each time it
              appears (b16, b28, b44, b67, b80) and is never once mentioned
  INVERT      deadpan the enormous, gild the trivial (Zappolino: dead men
              stitched tiny and plain, the bucket stitched huge in gold)

THE BORDER REACTS. The beast border is the tapestry's laugh track: beasts flee
the battle frames, kneel to the enthroned bucket, and in the final frame one
carries off a tiny bucket of its own. Named at point of use only where it
matters — every frame gets the border from the world clause regardless.

THE PIG'S CHARACTER: indifferent. In every pig frame she is eating one potato,
regardless of what surrounds her. COUNTS AT POINT OF USE: ONE bucket, ONE
cannonball, ONE kettle, ONE pig, ONE potato, TWO armies.

Run: python3 board.py    (writes production/prompts.json + board.json)
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

HERO = ("the recurring character as an EMBROIDERED FIGURE: a small man with a round "
        "smooth YOUNG face stitched in outline, EXACTLY TWO couched-thread hairs "
        "standing from the crown that KINK and LEAN at different angles and are "
        "different lengths (never symmetrical, never vertical), a tunic stitched in "
        "VERMILION RED wool, thin stitched legs, every part of him visible "
        "laid-and-couched wool thread on the linen")

BUCKET = ("one ordinary wooden BUCKET stitched in walnut-brown wool with a simple "
          "rope handle")

# (line, camera, expression, scene)   camera in XCU CU MED WIDE XWIDE OVER LOW
S = [
# ============ ACT 1 — the stupidest wars ====================================
(1,"MED","relishing, presenting", f"{HERO} facing the viewer with both arms spread in a showman's welcome, and behind him a VAST stitched battlefield where two tiny armies charge toward each other, the border beasts already fleeing toward the frame edges."),
(2,"WIDE","-", "A stitched parade of ABSURD military pomp: rows of embroidered soldiers marching with banners, and carried at the front on velvet cushions, three objects with ONE bucket, ONE dead pig and ONE soup kettle, each stitched more richly than any soldier."),
(3,"XCU","-", f"EXTREME CLOSE-UP on {BUCKET}, COLOSSAL in frame, stitched with reverent gold-thread rays radiating from it, one border beast at the frame's bottom edge peering up at it."),
(4,"CU","conspiratorial, leaning in", f"CLOSE on {HERO} leaning ABSURDLY far toward the viewer with one brow up and a small knowing smile, one finger raised: once you've seen it, you'll see it everywhere."),
# ============ ACT 2 — his bucket ============================================
(5,"MED","content, unbothered", f"{HERO} walking with {BUCKET} swinging cheerfully from one hand along a stitched path, humming, under an ABSURDLY blue morning sky, the border beasts strolling along the bottom border in step with him."),
(6,"XCU","-", f"EXTREME CLOSE-UP on {BUCKET} sitting by a stitched well, COLOSSAL and completely ordinary, plain brown thread, no ceremony whatsoever."),
(7,"CU","blank, mid-sip", f"CLOSE on {HERO} drinking from a stitched cup with half-lidded uninterested eyes, the bucket visible behind him on its hook where it belongs, everything ABSURDLY calm."),
(8,"WIDE","stunned, staring", f"{HERO} standing at the well staring at an empty hook on the wall, his whole body a stitched exclamation, arms straight down, DOZENS of tiny stitched question-shapes of loose thread floating above his head."),
(9,"CU","determined, modest", f"CLOSE on {HERO} facing the viewer with a plain reasonable face, holding up one finger: one bucket. That is all he is asking of the world."),
(10,"MED","reasonable, open hands", f"{HERO} with both hands open at waist height in the world's most reasonable gesture, while behind him THREE stitched neighbours are ALREADY reaching for an ABSURDLY well-stocked wall rack of pitchforks."),
(11,"WIDE","alarmed, waving no", f"{HERO} waving both arms in alarm at a crowd of DOZENS of stitched neighbours marching past him with torches and banners, every one of them ignoring him completely, the border beasts marching too."),
(12,"XWIDE","tiny, left behind", f"A VAST stitched field with a crowd streaming toward the horizon under banners, and {HERO} TINY and alone in the foreground, still pointing back at the empty hook on the well."),
# ============ ACT 3 — the escalation ladder =================================
(13,"MED","-", f"{BUCKET} stitched small and plain on a plain stitched table in an empty room. Nothing else. The border beasts at the bottom edge glance at it sideways."),
(14,"MED","-", f"The SAME room and camera: {BUCKET} now on a raised stitched plinth draped in indigo cloth, TWICE its former size, with two stitched candles beside it. The border beasts have turned to face it."),
(15,"MED","-", f"The SAME room and camera: {BUCKET} now ENORMOUS on a stitched altar with gold-thread rays, DOZENS of candles, and two kneeling stitched figures, the border beasts at the bottom edge now kneeling too."),
(16,"WIDE","protesting, unheard", f"{HERO} standing in front of the altar with both arms out in protest at the worshippers, completely ignored, while TINY on the far stitched horizon a small fortress sits with its first few threads coming loose."),
(17,"CU","-", "CLOSE on one stitched neighbour's face mid-shout, mouth ABSURDLY wide, veins stitched on his neck in vermilion, eyes closed with conviction."),
(18,"XWIDE","-", "A VAST stitched landscape at dusk with TWO armies assembling on opposite hills, banners up, and between them an empty valley with one TINY plain hook stitched in the middle where nothing hangs."),
# ============ ACT 4 — Zappolino, and the trophy =============================
(19,"CU","narrating, grave", f"CLOSE on {HERO} looking straight down the lens with a grave face, holding up an ENORMOUS stitched scroll that unrolls past his feet: now the history, because this really is in the books."),
(20,"WIDE","-", "Two stitched city gates facing each other across a valley: one flying vermilion banners, one flying indigo banners, each with DOZENS of citizens shaking fists from the walls at the other."),
(21,"XWIDE","-", "A VAST battle scene: THIRTY-TWO thousand suggested by an ocean of tiny stitched spears on the left, seven thousand by a modest cluster on the right, the border beasts fleeing the bottom border entirely — it stands empty."),
(22,"XWIDE","-", f"The same VAST field after: fallen stitched soldiers rendered TINY and plain like border decorations across the whole cloth, and in the exact centre {BUCKET} stitched LARGER than any man in the richest gold thread on the linen."),
(23,"CU","quiet, to camera", f"CLOSE on {HERO} looking at the viewer in silence, no gag, both hairs still, the battlefield out of focus in stitches behind him."),
(24,"MED","confiding, delighted", f"{HERO} leaning ABSURDLY far toward the viewer with a returning grin, one hand cupped beside his mouth: and this is the part we love — it was NOT over the bucket."),
(25,"WIDE","-", "Two ENORMOUS stitched figures in papal robes and imperial armour arm-wrestling over a table shaped like Italy, while TINY citizens of both cities cheer from the border edges."),
(26,"WIDE","-", "A stitched fortress on a hill being captured: soldiers on ladders, one banner coming down and another going up, stitched in COMPLETELY plain undramatic brown thread, the most boring frame in the film, deliberately."),
(27,"MED","-", "A stitched army marching home victorious through a gate, and one soldier at the rear carrying ONE bucket on a stick over his shoulder, casually, like luggage, while ahead of him DOZENS carry actual banners."),
(28,"WIDE","-", f"A stitched town square where a crowd gathers around {BUCKET} raised on a pole, pointing and marvelling, while TINY on the horizon behind them the fortress has visibly begun UNRAVELLING, threads trailing loose across the linen."),
(29,"MED","-", f"{BUCKET} being installed inside a TOWERING stitched tower, hoisted on ropes past astonished stitched onlookers leaning from every window, gold rays already stitched around it."),
(30,"WIDE","queueing, patient", f"{HERO} standing at the very end of an ABSURDLY long stitched queue that switchbacks up the whole height of the tower, holding a small blank ticket, his two hairs drooping."),
(31,"CU","warning, wry", f"CLOSE on {HERO} looking sideways at the viewer from the ABSURDLY long queue with a wry flat face: they are not going to give it to him either."),
# ============ ACT 5 — the gallery: kettle, pig, pastry ======================
(32,"MED","spotting, pointing", f"{HERO} pointing off-frame with narrowed detective eyes, the other hand shading his brow, a stitched magnifying glass ABSURDLY large in his belt."),
(33,"WIDE","-", "A stitched river scene: ONE ENORMOUS proud imperial ship in full sail flying elaborate banners, sailing directly toward a modest line of Dutch ships stitched flat and unimpressed."),
(34,"XCU","-", "EXTREME CLOSE-UP on ONE stitched cannonball in mid-flight, COLOSSAL in frame, stitched with a long dotted thread line tracing its arc across bare linen."),
(35,"CU","-", "CLOSE on the ship's stitched COOK, ladle still raised mid-stir, staring with ABSURDLY wide eyes at the empty space where his kettle was, stitched soup droplets raining from the top border, his hat askew, one border beast catching drips in its mouth."),
(36,"WIDE","-", "The ENORMOUS imperial flagship lowering its flag in surrender, while on the deck the crew gathers in a mournful stitched circle around ONE dented kettle lying on its side like a fallen comrade."),
(37,"MED","-", "A stitched funeral procession carrying ONE dented kettle on a bier under a small banner, faces ABSURDLY solemn, while the border beasts at the bottom edge hold tiny stitched spoons upright in salute."),
(38,"CU","deadpan, shrugging", f"CLOSE on {HERO} mid-shrug with a flat mouth and raised brows: one shot, one kettle, no dead."),
(39,"WIDE","-", "A stitched island scene: ONE pig stitched perfectly calm in the centre of a potato field, eating ONE potato, while an American farmer gestures at her with ABSURD fury from one side, veins in vermilion."),
(40,"WIDE","-", "The SAME field and camera: the pig unmoved on her potato, but now DOZENS of stitched soldiers have arrived behind the farmer with rifles and a cannon, all aimed in the pig's general direction."),
(41,"XWIDE","-", "The SAME field again from further back: the pig TINY and still eating, and now TWO full stitched warships bristling with cannons crowd the bay behind the field, banners flying, the border beasts hiding behind each other."),
(42,"XCU","-", "EXTREME CLOSE-UP on the stitched PIG's face, COLOSSAL, utterly serene, mid-chew, ONE potato crumb on her snout, her eye a single perfect uninterested stitch."),
(43,"MED","-", "A stitched pastry shop with its awning torn and trays scattered, and a stitched French chef in an ENORMOUS toque pointing at the damage with operatic anguish while two embarrassed officers examine a crumb."),
(44,"WIDE","-", f"Behind the wailing chef, an ENORMOUS stitched fleet fills the harbour, sacks of coins already being carried up gangplanks, while TINY on the far horizon the fortress unravels further, its outline now half loose thread."),
(45,"CU","counting, dry", f"CLOSE on {HERO} counting on three fingers with a dry face: the kettle, the pig, the pastry — none of them started anything. They got promoted."),
# ============ ACT 6 — the why: a gentleman with a flag ======================
(46,"MED","explaining, warm", f"{HERO} facing the viewer with open palms and a warm reasonable face, and stitched above him a small thought-shape of loose thread containing ONE tiny glove."),
(47,"WIDE","-", "An ENORMOUS stitched gentleman whose tailcoat is made entirely of a national flag, TOWERING over a landscape, adjusting his cravat, with tiny stitched citizens standing on his shoulders and hat."),
(48,"MED","-", "The flag-coated giant bending down ABSURDLY low to inspect ONE tiny pig held up to him on a velvet cushion by a kneeling minister, his stitched monocle falling from his eye."),
(49,"WIDE","-", "TWO flag-coated stitched giants standing back to back in duelling pose across a whole valley, pistols the size of church towers, while between their feet the TINY pig eats her potato in the exact centre of the duelling ground."),
(50,"CU","-", "CLOSE on one giant's stitched face, sweating ABSURDLY large single stitched drops, eyes sideways at his rival, mouth a thin line: he cannot laugh and he cannot leave."),
(51,"WIDE","-", "A stitched war council of generals around a map table, every general leaning ABSURDLY far in, and standing ON the map at the centre, ONE pig, calmly eating ONE potato that is stitched exactly where the disputed island should be."),
(52,"MED","recognising, tapping nose", f"{HERO} tapping the side of his nose at the viewer with an ABSURDLY knowing look, while behind him a stitched glove and a stitched pig sit side by side on two small matching plinths."),
(53,"XWIDE","-", "A VAST stitched field at dawn, and facing each other at duelling distance: ONE gentleman on the left, and on the right an entire TINY nation of forty million suggested by a crowd stitched into the shape of one man, the border beasts pacing out the distance."),
# ============ ACT 7 — why we remember the bucket ============================
(54,"CU","turning, sly", f"CLOSE on {HERO} holding up one finger with a sly sideways look, one hair curling into an ABSURD question-mark shape: but that only explains why they fight."),
(55,"MED","-", "A stitched scholar at a desk buried under TOWERING stacks of documents, quill in hand, visibly bored, a single stitched tear of tedium on his cheek, while dust-thread gathers on the papers."),
(56,"MED","-", f"The SAME desk and camera: the scholar GONE, chair flung ABSURDLY far across the room, and on the cleared desk just {BUCKET}, small and perfect, lit by a stitched sunbeam, the border beasts leaning in from the bottom edge to look."),
(57,"WIDE","-", "A stitched grandmother by a fire telling a story to SIX stitched children, and above them her story appears as a thought-shape of thread containing an ENORMOUS glowing bucket and two tiny armies."),
(58,"CU","caught, sheepish", f"CLOSE on {HERO} looking directly at the viewer with a caught, sheepish half-smile, both hands slowly presenting the stitched frame around himself: this film is stitching a bucket right now."),
(59,"OVER","-", f"Straight-down overhead of ENORMOUS stitched hands at work with needle and thread on THIS very tapestry, mid-stitch on a TINY golden bucket, spools of vermilion and indigo wool beside the linen."),
(60,"WIDE","browsing, unsettled", f"{HERO} walking slowly along a stitched museum wall of framed war scenes, and in every single frame the same composition: one TINY object — a bucket, a pig, a kettle, a pastry — stitched in gold at the centre of an ENORMOUS plain battle."),
(61,"MED","-", "A stitched herald on a platform proudly unrolling an ENORMOUS blank banner toward a cheering crowd, and the banner contains only ONE stitched bucket, nothing else, stitched huge and gold."),
(62,"WIDE","-", f"The fortress itself, now in the foreground for the first time: HALF-UNRAVELLED, its walls trailing into loose walnut threads across the bare linen, while every stitched passer-by walks past it without a glance."),
(63,"CU","testing, eyebrow up", f"CLOSE on {HERO} with one eyebrow ABSURDLY high, arms folded, asking the viewer directly: the fortress that actually started it — what was its name?"),
(64,"XCU","-", "EXTREME CLOSE-UP on a patch of bare linen where stitches USED to be: needle holes and a few loose walnut threads in the shape of a fortress outline, COLOSSAL in frame, nothing else."),
(65,"MED","shrugging, complicit", f"{HERO} shrugging ABSURDLY hugely at the viewer with a guilty grin, holding a stitched needle and thread behind his back, one border beast at the frame edge shaking its head at him."),
# ============ ACT 8 — Modena, today =========================================
(66,"XWIDE","tiny, arriving", f"A VAST stitched view of Modena today: the TOWERING tower dominating the cloth, modern stitched tourists with cameras dotted around its base, and {HERO} TINY at the end of the queue at its foot."),
(67,"WIDE","climbing, weary", f"{HERO} climbing an ABSURDLY tight stitched spiral staircase, wedged between a tourist ahead and a tourist behind, his two hairs flattened against the ceiling, while through a tiny window the unravelled fortress threads are just visible on the horizon."),
(68,"WIDE","-", f"The chamber at the top: {BUCKET} inside an ABSURDLY ornate stitched glass case on a TOWERING pedestal, lit with gold-thread rays, velvet ropes around it, TWO stitched guards in ceremonial dress flanking it with halberds."),
(69,"CU","polite, asking", f"CLOSE on {HERO} leaning toward the case with his ABSURDLY politest face, both hands clasped, eyebrows up in the world's most reasonable request: can I have it back?"),
(70,"CU","-", "CLOSE on a stitched guard's face smiling CHEERFULLY while shaking his head no, eyes closed with municipal warmth, completely immovable."),
(71,"MED","-", "A stitched museum placard scene: the guard gesturing at the case with ABSURD ceremonial pride, white glove presenting it, while a stitched velvet curtain behind reveals a SECOND identical bucket in a plainer box marked only with a stitched keyhole."),
(72,"CU","processing, blinking", f"CLOSE on {HERO} blinking slowly at the viewer, mouth slightly open, one hair bending as he processes: a copy of a souvenir of a war that was not about it."),
(73,"MED","long look, quiet", f"{HERO} standing alone before the glowing case, seen from behind at three-quarter, perfectly still, his reflection stitched faintly in the glass beside the bucket, no gag at all."),
(74,"WIDE","deciding, turning", f"{HERO} turning away from the case and walking toward the stitched stairway door with an ABSURD new lightness in his stitched stride, while the guards and tourists keep gazing at the case behind him."),
(75,"MED","-", "A small stitched market stall with DOZENS of ordinary new buckets hanging in rows, plain walnut thread, a bored stitched shopkeeper leaning on the counter."),
(76,"XCU","-", "EXTREME CLOSE-UP on ONE coin passing between two stitched hands over the counter, COLOSSAL in frame, the smallest transaction in the film stitched with gold-thread rays as if it were the treasure."),
(77,"MED","satisfied, swinging", f"{HERO} walking away from the stall with a brand-new bucket swinging from one hand, ABSURDLY pleased with himself, the border beasts skipping along the bottom border in step."),
(78,"CU","settled, wry", f"CLOSE on {HERO} looking at the viewer with a settled wry face, patting the ABSURDLY ordinary new bucket under his arm once: the whole war, refunded, in a minute and a half."),
# ============ ACT 9 — your buckets ==========================================
(79,"MED","gentle, to camera", f"{HERO} sitting on a stitched bench beside the well, new bucket hanging where the old one hung, the evening sky stitched ABSURDLY warm, talking gently to the viewer with both elbows on his knees."),
(80,"WIDE","-", f"A stitched garden fence between two houses with TWO neighbours glaring at each other over it, and the fence itself stitched in ABSURD gold thread with rays, like a relic, while on the horizon the last fortress threads finally lie flat and still."),
(81,"WIDE","-", "A stitched long table of colleagues all pointing at ONE empty stitched chair at its head, every face outraged, the chair stitched with gold rays and a tiny crown hovering above it."),
(82,"CU","asking, steady", f"CLOSE on {HERO} looking level at the viewer, calm and steady, one hand flat on his chest: what is this actually about?"),
(83,"MED","-", f"A stitched pair of scales: on one pan {BUCKET} small and plain, on the other pan an ENORMOUS gold-stitched trophy version of the same bucket with rays and ribbons, the plain one sitting HEAVIER."),
(84,"WIDE","cheerful, arms full", f"{HERO} at a market stall cheerfully buying a new fence post, a new chair, a new kettle and a second bucket all at once, arms ABSURDLY full, while behind him a TOWERING abandoned battlefield stands empty and quiet."),
(85,"MED","warning, one brow", f"{HERO} holding up ONE white stitched glove toward the viewer at ABSURD arm's length, one brow raised in warning, the glove stitched with faint gold rays it has not earned yet."),
(86,"XCU","-", "EXTREME CLOSE-UP on the white glove lying flat on bare linen, COLOSSAL, and a stitched hand calmly folding it closed and putting it away into a small plain pocket."),
(87,"WIDE","not looking, light", f"A stitched tower under construction with scaffolding, masons hoisting an ABSURDLY ornate empty display case toward the top, while in the foreground {HERO} walks past it the other way with his plain new bucket, not looking."),
(88,"CU","plain, kind", f"CLOSE on {HERO} facing the viewer with a plain kind face, no comedy: you get to decide that it won't say anything at all."),
# ============ ACT 10 — go home ==============================================
(89,"MED","urging, leaning in", f"{HERO} leaning ABSURDLY far toward the viewer with both hands out, urging, the new bucket standing faithfully at his feet like a dog."),
(90,"WIDE","-", "A stitched village at evening where DOZENS of tiny figures peacefully carry ordinary buckets from a well, windows glowing, no banners anywhere, the border beasts asleep in a row along the bottom border."),
(91,"MED","-", f"The tower interior one last time: {BUCKET} glowing in its case for nobody — the chamber empty, the guards gone home, one stitched candle guttering."),
(92,"XWIDE","tiny, going home", f"A VAST stitched landscape at dusk, {HERO} TINY on the path home with his new bucket, the tower far behind him still glowing, and the unravelled fortress threads lying quiet across the horizon linen."),
(93,"WIDE","content, almost home", f"{HERO} at his own stitched door in warm window light, hanging the new bucket on the hook where it belongs, and at the bottom edge ONE border beast trots out of the border carrying a TINY bucket of its own."),
]

WORLD = (
 "a MEDIEVAL EMBROIDERED TAPESTRY in the manner of the Bayeux Tapestry: figures "
 "and objects stitched in coloured wool thread on coarse natural LINEN cloth, with "
 "visible individual stitches, laid-and-couched work in the solid areas and "
 "stem-stitch outlines. The palette is wool colours only: VERMILION RED, deep "
 "INDIGO BLUE, MUSTARD OCHRE, sage GREEN, walnut BROWN and the bare linen ground, "
 "with small accents of couched GOLD THREAD. Figures are stylised and slightly "
 "stiff like Romanesque embroidery, with expressive oversized hands and faces. A "
 "narrow decorative embroidered border of small beasts runs along the top and "
 "bottom edges. The linen weave is visible everywhere. Flat matte, NO photographic "
 "depth, NO gradients, NO digital smoothness. There is NO text, NO lettering, NO "
 "numbers and NO writing of any kind anywhere in the image. This is ONE SINGLE "
 "COHERENT SCENE, NOT a grid, NOT a sheet of studies. 16:9, edge to edge, one "
 "scene, one camera.")

MIN_CAM = {'XCU': 6, 'CU': 6, 'OVER': 1, 'XWIDE': 6}
MAX_RUN = 3

MIN_HERO_SHARE = 0.45      # he presents the gallery but OWNS this story (his
# bucket), so he carries more of it than the duel film's 0.40.
MAX_HERO_GAP = 5
MIN_EXAG_SHARE = 0.85
EXAG = re.compile(r'\b(enormous|absurd\w*|vast|towering|tiny|colossal|impossibl\w+|'
                  r'far (?:bigger|larger|smaller|taller)|hundreds|dozens|'
                  r'off the (?:top|edge)|many times|twice (?:the|its)|half (?:the|its)|'
                  r'crumpling|flying out|swarming|teeter\w*|yawning|unravel\w*|'
                  r'operatic|looming|loom over)\b', re.I)

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []
lines = [s[0] for s in S]
if sorted(set(lines)) != list(range(1, len(sents) + 1)):
    missing = set(range(1, len(sents) + 1)) - set(lines)
    errs.append(f'every sentence needs at least one frame; missing {sorted(missing)[:10]}')
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
for i, (_, _, _, sc) in enumerate(S, 1):
    if re.search(r'\b(mood ?board|swatch|grid of|sheet of studies)\b', sc, re.I):
        errs.append(f'frame {i}: describes a sheet of studies, not a scene')

# THE RUNNER IS LOAD-BEARING: the fortress must appear, and must only decay.
runner = [i for i, s in enumerate(S, 1) if 'fortress' in s[3]]
if len(runner) < 5:
    errs.append(f'the fortress runner appears {len(runner)} times, needs 5+ (b16 b28 b44 b62/64 b67 b80 b92)')
# THE PIG NEVER REACTS: every pig frame must contain her indifference.
for i, s in enumerate(S, 1):
    if re.search(r'\bpig\b', s[3], re.I) and not re.search(r'cushion|plinth|museum|counting', s[3]):
        if not re.search(r'eat|serene|calm|unmoved|indifferen|mid-chew', s[3], re.I):
            errs.append(f'frame {i}: the pig is present but not visibly indifferent')

hero = [s for s in S if 'recurring character' in s[3]]
exag = [s for s in S if EXAG.search(s[3])]
named = sum(1 for s in S if s[2] != '-')
faceless = [i for i, s in enumerate(S, 1)
            if 'recurring character' in s[3] and s[2] == '-']
gap, worst = 0, 0
for s in S:
    gap = 0 if 'recurring character' in s[3] else gap + 1
    worst = max(worst, gap)
if worst > MAX_HERO_GAP + 2:
    errs.append(f'longest stretch without the character is {worst} frames (max {MAX_HERO_GAP + 2})')

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
      f"exaggeration {len(exag)}/{len(S)} ({len(exag)/len(S):.0%}) | "
      f"runner x{len(runner)} | longest gap {worst}")

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
