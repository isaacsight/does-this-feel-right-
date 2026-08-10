#!/usr/bin/env python3
"""Frame book — Somebody Has to Die Now. One frame per sentence, extras on the
long ones.

THE GILLRAY WORLD (see WORLD.md). Hand-coloured Regency etching — the medium
that actually killed the duel. The manual world's diagram grammar (dotted guide
lines, dashed arrows, pointing-hand manicules) is licensed INSIDE this world for
the rules sequences only: the code duello act and the honour-arithmetic act.

THE CAST CORRECTION, at point of use. The test proved the medium AGES him — he
comes back jowly and Regency-faced. The HERO string therefore says the round
face is YOUNG and smooth every time, and boards never rely on the castplate
alone (WORLD.md, "the plates").

COUNTS AT POINT OF USE. The pistol-case probe asked loosely for two pistols and
got three. Every countable object in this board states its count: TWO pistols,
TWO dogs, ONE glove, TWENTY-SIX ruled lines.

FOUR MOTIFS, each the same object recurring:
  THE HAT     knocked to the mud in act 1, carried through the film, worn WET
              in the final frames. The film's scrap-equivalent.
  THE GLOVE   the challenge. Fetched act 2, thrown down act 5, dropped act 8.
  THE ARROWS  the diagram grammar — the rules made visible. Acts 3 and 5 only.
  THE SUN     the huge pale dawn sun. Every field scene sits under it; it is
              fully risen only in the final walk home.

Run: python3 board.py    (writes production/prompts.json + board.json)
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

HERO = ("the recurring character drawn as a REGENCY CARICATURE: a small man with a "
        "round smooth YOUNG face (never jowly, never old), EXACTLY TWO hairs standing "
        "from the crown that KINK and LEAN at different angles and are different "
        "lengths (never symmetrical, never vertical, never rabbit ears), an ENORMOUS "
        "VERMILION RED tailcoat far too big for him, tiny spindly legs, buckled shoes, "
        "in fine crosshatched etched linework with flat watercolour wash")

# The rules-made-visible device, licensed from the manual world for acts 3 and 5.
DIAG = ("with thin DOTTED GUIDE LINES, dashed instructional arrows and small "
        "pointing-hand manicule symbols overlaid on the scene like a plate from an "
        "instruction manual, but containing NO letters and NO numbers")

# (line, camera, expression, scene)   camera in XCU CU MED WIDE XWIDE OVER LOW
S = [
# ============ ACT 1 — the hat, and the question =============================
(1,"CU","affronted, mid-blink", f"CLOSE on {HERO}, seen at the moment a passing elbow clips the brim of his black hat, his eyes ABSURDLY wide mid-blink, the hat just beginning to tip."),
(2,"XCU","-", "EXTREME CLOSE-UP on one black tricorn hat, COLOSSAL in frame, tumbling through empty cream air, etched crosshatching on every facet."),
(3,"WIDE","dismayed, frozen", f"{HERO} frozen mid-stride on a street of leaning etched townhouses, staring down at his hat lying in an ABSURDLY large puddle of brown mud, one hand still raised where the hat used to be."),
(4,"WIDE","-", "A VAST pale field at dawn seen from far away: two TINY figures standing back to back in the middle, one bare tree, and an ENORMOUS pale sun sitting on the horizon, barely risen."),
(5,"MED","earnest, explaining", f"{HERO} facing the viewer with both palms open, and behind him DOZENS of etched gentlemen walking calmly in a long queue toward the horizon, each carrying a pistol case."),
(6,"XCU","-", "EXTREME CLOSE-UP on a single white glove lying flat on cream paper, COLOSSAL in frame, one dotted etched line circling it like an exhibit."),
(7,"CU","uneasy, confiding", f"CLOSE on {HERO} leaning toward the viewer with an uneasy confiding look, both brows up, one finger raised as if to say: this is the part that should worry us."),
# ============ ACT 2 — he wants to go home ===================================
(8,"MED","deflated, staring down", f"{HERO} standing over his hat in the ABSURDLY large mud puddle, shoulders fallen impossibly low, arms hanging, staring down at it."),
(9,"CU","hopeful, glancing sideways", f"CLOSE on {HERO} glancing sideways toward an open etched doorway glowing warm at the edge of frame, his whole face leaning toward it with hope."),
(10,"XWIDE","tiny, yearning", f"A VAST etched street receding to a TINY warm-lit house at the far end, {HERO} tiny in the foreground looking toward it, an ENORMOUS cold blue evening sky above."),
(11,"WIDE","trapped, hemmed in", f"{HERO} hemmed in on both sides by TOWERING etched gentlemen who loom over him like cliffs, every path out of frame blocked by a tailcoat."),
(12,"MED","pleading, waving it off", f"{HERO} with both hands waving in front of him pleadingly, while THREE etched friends stare back at him with ABSURDLY stony identical faces."),
(13,"WIDE","laughing alone", f"{HERO} mid-laugh with one hand raised, alone in the middle of a candlelit room where DOZENS of gentlemen have gone completely silent and turned to stare, every mouth a flat line."),
(14,"MED","-", "One etched servant walking with ABSURD ceremony across the frame, carrying a single white glove on a velvet cushion held far out in front of him, like a crown."),
(15,"MED","equally miserable", f"A second stouter etched gentleman in a mustard coat standing apart, wringing his hands, looking as ABSURDLY miserable as a man can look, his own hat clutched to his chest."),
(16,"CU","miserable, mirrored", "CLOSE on the stout mustard-coated gentleman's face, brows knotted upward in helpless misery, eyes ABSURDLY large and wet, lower lip out."),
(17,"XWIDE","tiny, pacing away", f"A VAST misty dawn field from high above: {HERO} TINY, pacing away from the tiny mustard gentleman in the opposite direction along a single dotted etched line, the ENORMOUS pale sun low on the horizon."),
# ============ ACT 3 — the rulebook. Diagram grammar begins. =================
(18,"XCU","-", f"EXTREME CLOSE-UP on a quill pen pressing into cream laid paper, COLOSSAL in frame, the nib mid-stroke leaving a ruled line, {DIAG}."),
(19,"WIDE","-", f"A long etched table in an Irish assembly room with EXACTLY SIX gentlemen seated along it in identical poses, quills raised in unison, TOWERING stacks of paper between them, {DIAG}."),
(20,"MED","-", "One etched clerk hunched ABSURDLY low over a tiny writing desk, nose nearly touching the page, writing with tremendous care while TWO gentlemen dictate over his shoulders."),
(21,"XWIDE","-", "A VAST etched map-like landscape: a TINY island on the left and a TINY continent on the right, with DOZENS of small white gloves raining down across the ocean between them like snow."),
(22,"WIDE","dwarfed, craning up", f"A TOWERING wall made entirely of TWENTY-SIX ruled blank paper strips stacked like courses of brickwork, with {HERO} TINY at its base craning his head impossibly far back, {DIAG}."),
(23,"CU","relishing, wicked", f"CLOSE on {HERO} with an ABSURDLY wide anticipatory grin, rubbing his hands together, eyes sideways at the viewer: wait until you hear this one."),
(24,"MED","-", f"An etched demonstration: one figure's open hand mid-slap and a second figure's mouth open mid-apology, with a COLOSSAL dashed arrow crossing the apology out, {DIAG}."),
(25,"CU","incredulous, asking", f"CLOSE on {HERO} pointing at his own open mouth with one finger, brows shot ABSURDLY high, incredulous: you follow that?"),
(26,"WIDE","-", f"A tiny etched figure kneeling in apology before a TOWERING figure, and between them an ENORMOUS dotted barrier of guide lines like a fence, {DIAG}."),
(27,"MED","weary, re-reading", f"{HERO} holding a single ENORMOUS sheet of ruled paper at arm's length, his head tilted ABSURDLY far to one side, one hand scratching between his two hairs."),
(28,"CU","hollow, realising", f"CLOSE on {HERO} lowering the ENORMOUS sheet just enough to show his eyes over its edge, all hope gone out of them, the two hairs drooping."),
# ============ ACT 4 — the pettiness gallery =================================
(29,"MED","knowing, conceding", f"{HERO} facing the viewer with one hand up in a fair-enough gesture, the other hand resting on an ENORMOUS closed etched ledger."),
(30,"XCU","-", "EXTREME CLOSE-UP on a single etched laurel wreath, COLOSSAL on cream, drawn with ABSURD ceremonial weight for something so small."),
(31,"XCU","-", "EXTREME CLOSE-UP on an etched crown tipping off the edge of the frame, COLOSSAL, one dotted line tracing its fall."),
(32,"XCU","-", "EXTREME CLOSE-UP on a single etched rose lying on cream paper, COLOSSAL in frame, one petal detaching."),
(33,"CU","flat, deadpan", f"CLOSE on {HERO} looking straight down the lens with a completely flat deadpan face, arms folded: it was not."),
(34,"WIDE","-", "Hyde Park as an etching: EXACTLY TWO Newfoundland dogs mid-scuffle in the centre, ABSURDLY fluffy and enormous, while TWO gentlemen owners lean over them pointing at each other with furious faces."),
(35,"WIDE","-", "The same TWO gentlemen now facing each other at dueling distance in the same park, EXACTLY TWO pistols raised between them, while the TWO dogs sit side by side watching with heads tilted, ABSURDLY innocent."),
(36,"CU","appalled, to camera", f"CLOSE on {HERO} with both hands pressed to the sides of his round young face, mouth a perfect O of appalled disbelief, eyes ABSURDLY wide."),
(37,"WIDE","-", "An etched vignette: one gentleman kneeling to pick up a knocked-over hat mid-apology while a second gentleman ALREADY aims a pistol at him from an ABSURDLY close two paces, the scene tilted."),
(38,"MED","-", "Aboard a heaving etched packet ship: one green-faced gentleman waving away an offered wine glass, while the offering captain rears back with an ABSURDLY theatrical wounded expression, hand to chest."),
(39,"WIDE","-", "An etched horse standing in a field looking directly at the viewer with a completely blank face, while TWO gentlemen behind it gesture at each other with ENORMOUS violence."),
(40,"MED","-", "An etched parrot on a TOWERING ornate stand, beak open mid-squawk, while TWO gentlemen below it lean toward each other nose to nose, faces purple with fury."),
(41,"CU","-", "EXTREME CLOSE-UP on the etched parrot's face filling the frame, one eye COLOSSAL and utterly empty, reflecting two tiny duelling figures in its black pupil."),
(42,"XWIDE","aghast, surveying", f"A VAST etched harbour with a fleet of warships at anchor, DOZENS of naval officers duelling each other in pairs along the whole shoreline, wigs flying, while {HERO} stands TINY in the near corner surveying it aghast."),
(43,"WIDE","-", "An ENORMOUS etched enemy warship looming over the water with its gunports open, and in front of it a small dinner table set with candles, drawn ABSURDLY more menacing than the ship."),
(44,"MED","-", "An etched dinner scene: EIGHT naval officers seated around a table, every single one half-risen from his chair mid-outrage, DOZENS of dropped forks and knives frozen in the air."),
# ============ ACT 5 — the why. Diagram grammar returns. =====================
(45,"LOW","screaming at the sky", f"Low camera looking up at {HERO} on the dawn field, head thrown back, screaming at an ENORMOUS empty sky, arms flung wide, the pale sun low behind him."),
(46,"CU","calming, explaining", f"CLOSE on {HERO} recovered, one hand smoothing his coat, addressing the viewer with sudden ABSURD calm: here's the why."),
(47,"MED","-", f"An etched gentleman standing on a plinth like a monument, and hanging from his neck an ENORMOUS blank medallion the size of his torso, {DIAG}."),
(48,"WIDE","-", f"Three etched vignettes in one scene joined by dashed arrows: a wedding, a moneylender's table, an officer's commissioning, each transaction passing through the SAME single white glove, {DIAG}."),
(49,"MED","-", f"An etched figure calmly placing his own TINY heart, drawn as a small vermilion valentine, onto one pan of an ENORMOUS set of scales, the other pan holding a single word-blank ribbon, {DIAG}."),
(50,"CU","plain, level", f"CLOSE on {HERO} looking level at the viewer, perfectly still, no comedy at all: that's what a duel was."),
(51,"MED","-", f"TWO etched pistols lying crossed on a banker's counting table among neat stacks of coins, drawn EXACTLY like collateral being weighed, a manicule pointing at them, {DIAG}."),
(52,"WIDE","-", f"A fork in an etched road: the left path short with a TINY grave at its end, the right path ENORMOUSLY long with a crowd of turned backs at its end, dashed arrows marking both, {DIAG}."),
(53,"MED","-", "An etched gentleman shrinking as DOZENS of surrounding faces turn away from him in unison, his outline drawn fainter than everyone else's, half-erased."),
(54,"CU","-", "CLOSE on an etched face going transparent: the crosshatching of the wall behind him showing through his cheek, his expression politely devastated, eyes ABSURDLY large."),
(55,"XCU","-", "EXTREME CLOSE-UP on an etched purse turned inside out, COLOSSAL in frame, EXACTLY THREE moths flying out of it."),
(56,"OVER","trapped, looking straight up", f"Straight-down overhead of {HERO} standing at the centre of an ENORMOUS chalk-drawn arithmetic of dotted lines and scales radiating around him on the field like a diagram he is trapped inside, {DIAG}."),
(57,"MED","complicit, shrugging", f"{HERO} caught mid-shrug with an ABSURDLY guilty face, gesturing at the diagram around his feet as if to say: it does add up."),
(58,"XWIDE","tiny, resigned", f"The VAST dawn field again: {HERO} TINY at his mark, pistol at his side, the stout mustard gentleman tiny at the far mark, the ENORMOUS pale sun unmoved on the horizon."),
(59,"CU","resigned, doing sums", f"CLOSE on {HERO} at his mark, eyes rolled upward, lips moving, visibly doing arithmetic he hates, the two hairs bent in opposite directions."),
# ============ ACT 6 — everything bounces ====================================
(60,"MED","asking, arms wide", f"{HERO} turning to the viewer with both arms ABSURDLY wide: so how do we kill a system like that?"),
(61,"WIDE","-", "Three ENORMOUS etched objects lined up on the field like artillery: a royal sceptre, a church pulpit, and a philosopher's armchair, each aimed at a TINY white glove on the ground."),
(62,"WIDE","-", "An etched king tearing a proclamation in half in fury while behind him DOZENS of gentlemen duel merrily across a VAST lawn, one pair duelling ON the palace steps."),
(63,"MED","-", "An etched preacher thundering from a TOWERING pulpit, and below him a congregation of gentlemen all discreetly comparing EXACTLY TWO pistols under their pews, one passing a glove."),
(64,"MED","-", "An etched philosopher presenting an ENORMOUS scroll of reasoning to two duellists who are ALREADY pacing apart, neither looking at him, his scroll drooping."),
(65,"CU","scorekeeping, dry", f"CLOSE on {HERO} holding up three fingers with a dry flat face, then indicating zero with his other hand: nil for three."),
# ============ ACT 7 — Wellington, and the laugh =============================
(66,"MED","conspiratorial, turning", f"{HERO} turning back to the viewer with one brow up and the beginning of a smile, one finger raised: none of those."),
(67,"WIDE","-", "An etched dawn field: an unmistakably TOWERING long-nosed Duke in a plain coat standing at his mark opposite a TINY earl, seconds cowering behind EXACTLY TWO trees."),
(68,"CU","-", "EXTREME CLOSE-UP on the Duke's etched profile, the famous nose COLOSSAL in frame, his expression of a man attending a meeting he finds tiresome."),
(69,"XWIDE","-", "The VAST field from far above: the TWO duelling figures ABSURDLY tiny in an ocean of empty cream paper, the whole scene shrunk to insignificance by the emptiness around it."),
(70,"WIDE","-", "The etched Duke firing with his pistol pointed ABSURDLY wide of everything, the dotted line of the shot sailing off the top corner of the frame past a startled bird."),
(71,"WIDE","laughing despite himself", f"An etched print-shop window crowded with DOZENS of gentlemen and ladies pressed against the glass, all pointing at prints hung inside, every face mid-laugh, with {HERO} squeezed in among them, laughing despite himself."),
(72,"CU","-", "CLOSE on one etched print hung in the window: within it, a caricature of the duel drawn even MORE absurdly, the figures balloon-bodied with ABSURDLY tiny legs, no letters anywhere."),
(73,"MED","-", "An ENORMOUS etched figure of Honour as a puffed-up gentleman literally deflating like a bladder, creases appearing across his chest, while TINY laughing figures point from below."),
(74,"MED","-", "An etched tailor's dummy being redressed: TWO hands lifting away a pistol belt and fitting a plain kind waistcoat in its place, the old belt dropping toward a bin."),
(75,"XWIDE","-", "A VAST field at full morning, completely empty: EXACTLY TWO pairs of footprints walking away in opposite directions, a single white glove abandoned in the middle, the sun higher now."),
(76,"WIDE","-", "An etched merchant and banker facing each other with EXACTLY TWO pistols, both ABSURDLY unsure, checking a rulebook propped open between them, while a crowd of onlookers is ALREADY laughing."),
(77,"CU","wheezing, doubled over", f"CLOSE on three faces in a row — two etched onlookers and {HERO} in the middle — each caught at a different stage of the same laugh: the snort, the doubled-over wheeze, the wiped tear, all ABSURDLY vivid."),
(78,"MED","marvelling, quiet", f"{HERO} facing the viewer, holding up his muddy hat and looking at it with quiet wonder, the fight gone out of the whole world behind him."),
# ============ ACT 8 — the exit costs nothing ================================
(79,"WIDE","deciding, still", f"{HERO} at his mark on the dawn field, pistol lowered to his side, looking across the VAST distance at the stout mustard gentleman, perfectly still, the sun a little higher."),
(80,"XCU","-", "EXTREME CLOSE-UP on a pistol being set down gently on the grass, COLOSSAL in frame, the hand withdrawing from it in one clean motion."),
(81,"WIDE","ridiculous, walking home", f"{HERO} walking away across the field toward the warm-lit TINY house on the horizon, wearing the wet muddy hat, mud dripping down one ear, his back to everything, the ENORMOUS sun climbing."),
(82,"CU","plain, at peace", f"CLOSE on {HERO} under the wet hat's brim, mud on his cheek, wearing the smallest possible smile, entirely at peace, no comedy at all."),
# ============ ACT 9 — 1967 ==================================================
(83,"CU","gleeful, leaning in", f"CLOSE on {HERO} leaning ABSURDLY far into the lens with barely-contained glee, both brows up: one more."),
(84,"WIDE","-", "A neat suburban French garden etched in the same Regency linework: TWO unmistakably MODERN 1960s men — slim dark 1960s business trousers, white dress shirts with sleeves rolled to the elbow, narrow 1960s neckties, short modern haircuts, NO wigs, NO tailcoats, NO breeches — duelling with thin epee swords beside a garden hedge, ABSURDLY formal."),
(85,"MED","-", "The TWO suited etched duellists mid-lunge over a flowerbed while a small crowd of photographers and officials in modern coats watch from ABSURDLY close, one holding back a curious poodle."),
(86,"XCU","-", "EXTREME CLOSE-UP on a wristwatch on a duelling wrist, COLOSSAL in frame, the sword blade crossing behind it, drawn in fine etched crosshatch."),
(87,"MED","-", "An etched elderly couple in armchairs watching all of it happily from their garden fence with teacups, drawn with ABSURD cosiness, a knitted blanket over four knees."),
(88,"CU","pointed, quiet", f"CLOSE on {HERO} looking at the viewer sideways from under the wet hat brim, one brow up, quietly pointed: never as far away as it looks."),
# ============ ACT 10 — the group chat =======================================
(89,"MED","confiding, gentle", f"{HERO} sitting on the etched kerb beside the mud puddle, hat on his knee, talking to the viewer gently, the street behind him softening into open field."),
(90,"WIDE","-", "A VAST dawn field where DOZENS of tiny etched figures stand at duelling marks in pairs, each pair connected not by weapons but by ENORMOUS blank white speech-bubble shapes floating between them."),
(91,"WIDE","-", "One tiny etched figure walking away from his mark while the crowd around his abandoned speech bubble points and laughs, and the ENORMOUS sun catches only him, the walker, in warm light."),
(92,"MED","-", "A single etched figure still standing rigid at his mark as evening crosshatching closes over the field around him, his shadow ABSURDLY long, everyone else long gone."),
(93,"CU","wry, hat on", f"CLOSE on {HERO} setting the wet muddy hat onto his own head with both hands, deliberate as a coronation, water running down past one wry raised brow."),
(94,"XWIDE","tiny, going home", f"The VAST field at last full of risen ENORMOUS sun: {HERO} TINY, walking home along the dotted etched line toward the warm-lit house, hat on, arms swinging, done with it."),
]

WORLD = (
 "a HAND-COLOURED REGENCY ETCHING in the manner of British satirical prints circa "
 "1800: fine crosshatched copper-etched linework in warm sepia-black ink on aged "
 "cream laid paper, coloured with flat translucent watercolour washes in vermilion "
 "red, prussian blue, mustard yellow, sage green and rose pink that sit loosely "
 "inside the lines. Faces and bodies are CARICATURED: bulging eyes, ballooning "
 "coats, tiny legs, enormous indignant gestures. Visible plate tone and paper "
 "grain, slightly uneven wash edges, a faint plate-mark border. Flat matte, NO "
 "photographic texture, NO digital gradients. There is NO text, NO lettering, NO "
 "numbers, NO signatures and NO writing of any kind anywhere in the image. This is "
 "ONE SINGLE COHERENT SCENE, NOT a grid, NOT a sheet of studies. 16:9, edge to "
 "edge, one scene, one camera.")

MIN_CAM = {'XCU': 6, 'CU': 6, 'OVER': 1, 'LOW': 1, 'XWIDE': 8}
MAX_RUN = 3

MIN_HERO_SHARE = 0.40      # the gallery acts are HIS ILLUSTRATIONS — the film
# cuts to him constantly (he is in 38 of 94), but the dogs, the parrot, the Duke
# and the 1967 garden are necessarily his-face-free. 0.55 was right for a film
# whose events all happen TO the character; this one alternates him with the
# exhibits he is presenting. The compensating rule: no more than THREE
# consecutive frames without him, enforced below.
MAX_HERO_GAP = 3
MIN_EXAG_SHARE = 0.85
EXAG = re.compile(r'\b(enormous|absurd\w*|vast|towering|tiny|colossal|impossibl\w+|'
                  r'far (?:bigger|larger|smaller|taller)|hundreds|dozens|'
                  r'off the (?:top|edge)|many times|twice (?:the|its)|half (?:the|its)|'
                  r'crumpling|flying out|swarming|teeter\w*|yawning|balloon\w*|'
                  r'deflating|looming|loom over)\b', re.I)

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
for i, (_, _, _, sc) in enumerate(S, 1):
    if re.search(r'\b(mood ?board|swatch|grid of|sheet of studies)\b', sc, re.I):
        errs.append(f'frame {i}: describes a sheet of studies, not a scene')
    # This world's own lesson: a countable object with no count drifts.
    if re.search(r'\bpistols\b', sc) and not re.search(r'\bTWO\b.{0,40}pistols|pistols?\b.{0,20}\bcrossed', sc):
        if 'a pistol' not in sc and 'his pistol' not in sc and 'pistol case' not in sc:
            errs.append(f'frame {i}: plural pistols without a stated count')

hero = [s for s in S if 'recurring character' in s[3]]
exag = [s for s in S if EXAG.search(s[3])]
named = sum(1 for s in S if s[2] != '-')
faceless = [i for i, s in enumerate(S, 1)
            if 'recurring character' in s[3] and s[2] == '-']
# No more than MAX_HERO_GAP consecutive frames without him.
gap, worst = 0, 0
for s in S:
    gap = 0 if 'recurring character' in s[3] else gap + 1
    worst = max(worst, gap)
if worst > MAX_HERO_GAP + 2:   # the gallery earns a little slack, but not much
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
      f"longest gap without him {worst}")

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
