#!/usr/bin/env python3
"""Frame book — Nobody Roots for Goliath. v3, the COMEDIAN's board.

THREE BUILDS TO GET HERE, and the lesson is one sentence: the register theory
kept losing to the thing that actually works.

  v1  Masereel woodcut, Williamson register.  Rejected: creepy, humourless,
      lost continuity. Character in 26% of frames, 13% abstract metaphors, no
      colour anchor. Kept at production/board-v1-woodcut.py.
  v2  Jones world, same Williamson board.  Rejected: repetitive. 61% of frames
      in one arena, 42% "a figure standing", because the CLAUSE hardcoded one
      ground and one geometry into every frame. Kept at board-v2-jones.py.
  v3  Jones world, comedian writes AND directs. The script is rewritten with
      the CHAMPION as protagonist (production/script-v1-williamson.txt keeps
      the essay version), and the doctrine below is the one that made the duel
      and the wars films work.

THE FRAME IS A SECOND JOKE, never an illustration:

  REACTION   cut to the witness, not the event
  DISAGREE   background contradicts foreground
  LADDER     one composition repeated, one variable worse each time
  RUNNER     THE UNSHAKEN HAND. He offers a handshake across the film and
             nobody takes it. Never mentioned in narration. It is his want made
             physical - he only wants somebody to say well done - and it pays
             off in the last act, taken by a child.
  INVERT     deadpan the enormous, exaggerate the trivial

KEPT FROM THE WILLIAMSON WORK, because it was right: TOCAM, the deadpan look
at the viewer; and declared PAIRS, machine-checked for a matching camera.

ALIGNMENT IS NOW CHECKED. v2 shipped ~20 frames playing under the wrong
sentence because the board was written against my memory of the script's shape
rather than the sentences. check_alignment below flags any frame whose LINE is
about people while the SCENE has nobody in it.

TYPOGRAPHY: title card b01, source card b19, four-rung scoreboard ladder.
Composited AFTER the gate by tools/video/typeset-cards.py.

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

CHAMP = ("the CHAMPION in mid-century cartoon style: a large barrel-chested athlete with "
         "a heavy brow and a long dignified face, meticulous and faintly vain, impeccably "
         "turned out in a flat INK BLUE jersey with everything perfectly squared away, "
         "dignified through PRECISION rather than heroic build, wry and intelligent, "
         "never grotesque and never pitiable")

SMALL = ("the SMALL ONE in the same style: a slight scruffy athlete with a round young "
         "face and a big confident nose, EXACTLY TWO hairs standing from the crown that "
         "KINK and LEAN at different angles and different lengths, a flat VERMILION RED "
         "sleeveless jersey, thin stick legs and ABSURDLY oversized shoes")

SPEC = ("ONE PARTICULAR SPECTATOR in the front row: a round middle-aged man in a mustard "
        "flat cap with an ABSURDLY large moustache, always in the same seat, always "
        "recognisably the same man")

HAND = "holding out one hand for a handshake that nobody is taking"

BOARD = ("a large scoreboard above the arena with its face COMPLETELY BLANK and empty, "
         "no numbers and no writing on it at all")

S = [
# ===== ACT 1 (1-6) — the man who did everything right =====================
(1,"XWIDE","immaculate, alone", f"A VAST stylised arena at dusk with ranked rows of TINY spectator shapes all around, and {CHAMP} standing ABSURDLY alone at the exact centre of the cream floor. A calm title-card composition with clear empty sky above."),
(2,"MED","composed, certain", f"{CHAMP} standing with a towel folded over one arm at a perfect right angle, everything about him squared away, looking off toward a crowd we cannot see."),
(3,"WIDE","crowded out", f"A trophy shelf running the entire width of the frame, ABSURDLY crowded with identical trophies, and {CHAMP} at the end of it holding one more with nowhere to put it."),
(4,"LOW","triumphant, unloved", f"Low camera from the floorboards looking steeply UP at {CHAMP} mid-dunk against a ceiling of mustard lights, the rim ENORMOUS in the foreground, and far below a packed band of individually drawn spectators sitting with folded arms, each one a distinct little person with a face."),
(5,"CU","booed, blinking", f"CLOSE on {CHAMP} being booed, taking it on the chin with one slow blink, while DOZENS of individually drawn shouting faces with open mouths and raised fists crowd the frame behind him, every one of them a distinct little person."),
(6,"TOCAM","deadpan, holding it", f"CLOSE on {CHAMP} looking DIRECTLY out of the frame at the viewer with a flat deadpan expression and one eyebrow raised a fraction, holding the look a beat too long."),
# ===== ACT 2 (7-12) — what he wants ======================================
(7,"MED","proud, prepared", f"{CHAMP} in a cramped ink-blue locker room with his kit laid out in a perfect grid on the bench, every item squared, a spirit level resting beside his boots."),
(8,"WIDE","folded up, patient", f"{CHAMP} ABSURDLY oversized in a small physio room, ducking to fit under the ceiling, while a tiny physio taps his knee with a hammer."),
(9,"XCU","reflected, buffing", f"EXTREME CLOSE-UP on a single boot polished to a COLOSSAL shine, with {CHAMP} reflected small and upright in the leather, still buffing it."),
(10,"MED","hopeful, waiting", f"{CHAMP} {HAND} toward a teammate who is walking past looking at a clipboard, entirely unaware."),
(11,"CU","small want, plain", f"CLOSE on {CHAMP} with a plain hopeful face, no comedy in it at all, waiting for something that is not going to arrive."),
(12,"WIDE","oblivious, cheerful", f"A tunnel where {CHAMP} stands to one side {HAND} while DOZENS of people stream past him toward something more interesting off-frame."),
# ===== ACT 3 (13-16) — the small one arrives ============================
(13,"WIDE","scruffy, arriving", f"{SMALL} stepping out onto a stylised arena floor with one sole flapping loose, laces trailing, ABSURDLY unprepared."),
(14,"WIDE","surging, delighted", f"DOZENS of flat spectators surging over a rail toward {SMALL} far below, hats flying off, the rail bending ABSURDLY under them."),
(15,"CU","overjoyed, weeping", f"CLOSE on {SPEC} with his cap pushed back and both hands raised, mouth ENORMOUS in a roar, one comic tear flying off his cheek - the warmest face in the film."),
(16,"MED","watching, keeping score", f"{CHAMP} in the background {HAND} toward {SMALL} as the crowd swarms past him to reach the smaller man, his face perfectly composed."),
# ===== ACT 4 (17-23) — the finding. SOURCE CARD on b19. =================
(17,"CU","level, unbothered", f"CLOSE on {CHAMP} looking at the viewer, level and matter-of-fact, no self-pity anywhere in his face."),
(18,"MED","brisk, unaware", f"A cream university corridor where THREE tidy cartoon researchers walk abreast with clipboards, passing an open doorway through which a distant crowd is visible, all leaning the same way."),
(19,"WIDE","noting it down", f"A lecture room with tiered wooden seating and a COMPLETELY BLANK board behind: two researchers at the front with clipboards while the rows in front of them all lean the same way. Clear empty space along the bottom edge of the frame."),
(20,"WIDE","identical, leaning", "A mustard office where DOZENS of identical workers at identical desks have all swivelled their chairs the same few degrees toward one small figure at the far end."),
(21,"MED","competing, absurd", f"A grand concert stage seen from the wings with heavy curtain filling the foreground: {CHAMP} and {SMALL} at two music stands with violins, the audience beyond leaning ABSURDLY toward the smaller one."),
(22,"WIDE","same lean everywhere", "One wide frame in three flat colour bands stacked vertically - a running track, an office floor, a concert hall - and in every band the watching crowd leans exactly the same way."),
(23,"CU","resigned, informed", f"CLOSE on {CHAMP} taking this in with a slow nod, as a man receiving confirmation of something he already suspected."),
# ===== ACT 5 (24-29) — not spite, worse ================================
(24,"MED","choosing, cheerful", f"TWO researchers holding out TWO identical blank cards toward {SPEC}, who is pointing decisively at one of them."),
(25,"WIDE","split, chatting", f"A cartoon crowd split down the middle: one half cheering ENORMOUSLY at {SMALL}, the other half not booing {CHAMP} but simply facing the wrong way, chatting."),
(26,"MED","queued, lopsided", "A cartoon railway station buffet with two counters: an ENORMOUS queue at one and nobody at all at the other, one bored attendant waiting."),
(27,"CU","delighted, guiltless", f"CLOSE on {SPEC} looking sincerely delighted, entirely without malice, which is somehow worse."),
(28,"WIDE","forgotten, present", f"{CHAMP} standing in the middle of a busy crowd scene while every single person in it faces away from him, none of them hostile, all of them elsewhere."),
(29,"CU","forgotten, blinking", f"CLOSE on {CHAMP} realising he has been forgotten rather than hated, one slow blink, no expression change at all."),
# ===== ACT 6 (30-35) — the mechanism ==================================
(30,"MED","weighed, unequal", f"{SMALL} and {CHAMP} standing side by side facing the viewer while a TOWERING arrow of crowd bodies leans toward the smaller one."),
(31,"CU","borrowing his face", f"CLOSE on {SPEC} wearing EXACTLY the expression of {SMALL} below him - same jaw, same lifted brow, the moustache at the same angle - mirroring without knowing it."),
(32,"XCU","-", f"EXTREME CLOSE-UP on {SPEC}'s eye, COLOSSAL in frame, with TWO tiny figures reflected in the pupil, one ENORMOUS and one small."),
(33,"MED","painted on", f"TWO thought-shapes drawn above the crowd like weather: over {CHAMP} a hard flat cloud, over {SMALL} a soft round one, the crowd painting them on with brushes."),
(34,"CU","assigned contempt", f"CLOSE on {CHAMP} with his chin up and mouth set, drawn so we can see this is how the crowd READS him rather than what he is."),
(35,"CU","assigned gratitude", f"CLOSE on {SMALL} with eyes up and shoulders drawn in, the ABSURDLY apologetic face of somebody who knows he is not supposed to be here."),
# ===== ACT 7 (36-38) — he is worried about his knee ==================
(36,"MED","ordinary, aching", f"{CHAMP} sitting alone on a folding chair with a bag of ice ABSURDLY balanced on one knee, entirely ordinary, thinking about nothing but the knee."),
(37,"XCU","his own hands, serious", f"EXTREME CLOSE-UP on one swollen cartoon knee with a bag of ice on it, COLOSSAL in frame, with {CHAMP}'s own hands resting either side of it, drawn with complete seriousness and no joke at all."),
(38,"WIDE","unnoticed, half-raised", f"A press pack of DOZENS of reporters crowded around {SMALL} on one side of the frame, and {CHAMP} on the other side with his hand half-raised to speak, unnoticed."),
# ===== ACT 8 (39-44) — THE TRAP =====================================
(39,"MED","reasonable, careful", f"{CHAMP} at a small table in a cramped press room, saying something extremely mild with both hands flat and open, the picture of reasonableness."),
(40,"WIDE","recoiling as one", "A wall of DOZENS of reporters all recoiling backwards in unison as though something appalling has been said, notebooks flying up."),
(41,"CU","aghast, delighted", f"CLOSE on {SPEC} looking scandalised and thoroughly enjoying being scandalised, moustache bristling."),
(42,"MED","trapped, mouth open", f"{CHAMP} standing with his mouth open mid-sentence and an ENORMOUS crowd of pointing hands crowding in from every edge of the frame toward his face."),
(43,"XCU","closing, unsaid", f"EXTREME CLOSE-UP on {CHAMP}'s mouth closing, COLOSSAL in frame, the words visibly not coming out, one reporter's pen frozen at the edge of frame."),
(44,"WIDE","excruciating, familiar", f"A cartoon dinner table of eight people at which one man is explaining himself with a raised finger while every other guest is looking at the tablecloth. {CHAMP} is one of the guests, watching it happen to somebody else."),
# ===== ACT 9 (45-47) — he tries harder. LADDER 1-2. ==================
(45,"MED","straining, alone", f"{CHAMP} in a mustard-lit training gym at night surrounded by ropes and medicine balls, working ABSURDLY hard entirely alone, one lamp swinging."),
(46,"WIDE","packed, on their feet", f"{CHAMP} on the arena floor beneath {BOARD}, with the crowd behind the board packed shoulder to shoulder and all of them on their feet."),
(47,"WIDE","thinning, seated", f"The SAME arena and the SAME camera beneath the SAME {BOARD}, {CHAMP} standing exactly as before, and a whole row of the crowd behind it now seated."),
# ===== ACT 10 (48-53) — the abandonment. LADDER 3-4. =================
(48,"LOW","half empty", f"The SAME arena and SAME staging beneath the SAME {BOARD}, seen from a low camera at floor level, {CHAMP} unchanged, and now half the stand behind it is empty."),
(49,"WIDE","one man left", f"The SAME arena and SAME camera beneath the SAME {BOARD} one last time, {CHAMP} unchanged, and only {SPEC} left seated in an otherwise empty stand."),
(50,"MED","cheering the box", "A cartoon crowd cheering ENORMOUSLY at a small figure standing on a low box, drawn so it is obviously the BOX they are looking at and not the person on it."),
(51,"MED","cheering it still", "The SAME crowd and the SAME camera, the box now empty and a different small figure standing on it, and the crowd cheering exactly as hard."),
(52,"MED","falling, quiet", f"{CHAMP} stepping down off the box and watching the cheer follow the box instead of him, his face slowly falling."),
(53,"CU","holding it, lost", f"CLOSE on {CHAMP} holding an ENORMOUS trophy and looking at it with genuine bewilderment, wondering what he did."),
# ===== ACT 11 (54-58) — the arrangement =============================
(54,"MED","reasonable, itemised", f"{CHAMP} at a kitchen table at home holding up a COMPLETELY BLANK check-list scroll and gesturing at it, entirely reasonable, a cold dinner in front of him."),
(55,"WIDE","blank promise", "A cartoon town square where a crowd stands in a neat row holding up an ENORMOUS blank banner with absolutely nothing written on it."),
(56,"MED","completed, voided", f"{CHAMP} in a municipal office handing a folded blank contract back across a counter to a clerk who is already turning away."),
(57,"CU","conditional, sour", f"CLOSE on {SPEC} with arms folded and cap low, looking at somebody who has succeeded and visibly disliking it."),
(58,"XCU","-", "EXTREME CLOSE-UP on a small padlock closing, COLOSSAL in frame, with a tiny cartoon figure visible through the loop of it."),
# ===== ACT 12 (59) — the second turn ================================
(59,"TOCAM","turning it on us", f"CLOSE on {SMALL} looking DIRECTLY out at the viewer with a small knowing look, one brow up, turning the film around."),
# ===== ACT 13 (60-66) — what it cost us =============================
(60,"CU","comfortable, spent nothing", f"CLOSE on {SPEC} sitting well back in his seat with his hands folded on his belly, utterly at ease, having spent nothing at all."),
(61,"XWIDE","relaxed, empty-handed", "A stylised arena from high above, everybody in it empty-handed and leaning the same way, ABSURDLY relaxed."),
(62,"WIDE","switched, urgent", f"A crowded ink-blue betting hall with a low ceiling and a rail of standing men including {SPEC}, every hand gripping a small slip of paper, every body leaned hard the same way."),
(63,"XCU","-", "EXTREME CLOSE-UP on TWO cartoon hands passing a small folded slip of paper between them, COLOSSAL in frame, while far above a crowd cheers on unaware."),
(64,"WIDE","flipped, hard", f"DOZENS of spectators in the SAME ranked rows as before, every hand now gripping a slip and every body leaned hard toward {CHAMP} instead."),
(65,"CU","calculating, cold", f"CLOSE on {SPEC} with a slip crushed in one fist, moustache bristling, watching the favourite with no warmth anywhere."),
(66,"MED","luxury, absurd", f"A smart cream shop interior seen through the window from the pavement, our reflection faint in the glass: {SPEC} inside looking at one small object on a velvet stand lit ABSURDLY grandly, an ENORMOUS blank price tag beside it."),
# ===== ACT 14 (67-70) — the honest version ==========================
(67,"TOCAM","caught, plain", f"CLOSE on {SPEC} facing the viewer directly with no expression to hide behind, simply caught."),
(68,"MED","holding it away", f"{SPEC} holding a smiling cartoon mask slightly away from his own face, not hiding behind it and not putting it down."),
(69,"WIDE","lit, enjoying it", "A cartoon crowd all looking up at something bright off-frame with every face lit and open, thoroughly enjoying the feeling of looking."),
(70,"WIDE","dimmed, folding", "The SAME crowd and the SAME camera as the light goes out, every face lowering at once and the raised arms folding down."),
# ===== ACT 15 (71-76) — where else it lives ========================
(71,"MED","hoisted, half-watched", "A cartoon office where one worker is being hoisted onto shoulders while the colleagues underneath are already glancing away."),
(72,"WIDE","adored then folded", "One frame split by a flat colour band: a tiny packed music venue with an adoring crowd on one side, the SAME band on an ENORMOUS stage with an arms-folded crowd on the other."),
(73,"MED","queued, delighted", f"A cheerful little restaurant with a queue out the door and {SPEC} in it, delighted."),
(74,"MED","passed over", f"The SAME restaurant and the SAME camera with a second identical restaurant now beside it, and {SPEC} walking past both without looking."),
(75,"CU","reasonable, sincere", f"CLOSE on {SPEC} shrugging with a perfectly reasonable expression to the people around him, explaining a change of heart he genuinely believes."),
(76,"MED","raised, unchanged", f"{CHAMP} standing perfectly still while the platform beneath him is quietly cranked upward by two officials, so that only his POSITION has changed."),
# ===== ACT 16 (77) ================================================
(77,"CU","asking, level", f"CLOSE on {SMALL} looking at the viewer and asking without any appeal at all, entirely level."),
# ===== ACT 17 (78-79) — notice the flip ===========================
(78,"CU","catching himself", f"CLOSE on {SPEC} on a night bus lit ink-blue by the window, in the act of noticing his own feeling change, moustache lifting."),
(79,"MED","new hand, old man", f"{SPEC} looking at his own open hand as if he has never seen it before, alone on an empty street."),
# ===== ACT 18 (80-81) — person versus position ====================
(80,"MED","identical, unequal", f"{CHAMP} and {SMALL} standing on TWO plinths of ABSURDLY different heights, the two figures otherwise identical in posture and expression."),
(81,"MED","identical, level", f"The SAME two figures and the SAME camera, both now standing on the flat ground with no plinths at all, still identical."),
# ===== ACT 19 (82-84) — the test ==================================
(82,"OVER","offering it", f"Straight-down overhead of {SPEC}'s two hands on a plain cream surface, holding one small folded slip of paper out toward the viewer."),
(83,"WIDE","ordinary, watching", f"DOZENS of individually drawn spectators with distinct faces watching {CHAMP} and {SMALL} in an ordinary contest in an ordinary way, nothing dramatic happening at all."),
(84,"WIDE","flipped", "The SAME crowd from the SAME camera, every body now leaning the opposite direction, the composition otherwise completely identical."),
# ===== ACT 20 (85-86) — the crowd tells you the price =============
(85,"CU","level, unsurprised", f"CLOSE on {CHAMP} watching the crowd with no bitterness at all, simply reading them."),
(86,"MED","patient, tagged", f"A shop counter where a cheerful assistant is tying an ENORMOUS blank price tag onto {CHAMP}'s wrist while he stands there patiently letting it happen, a small queue of customers watching with interest."),
# ===== ACT 21 (87-93) — still out there, and the payoff ==========
(87,"LOW","still the best", f"Low camera looking up at {CHAMP} mid-play again, immaculate, the crowd above him jeering exactly as in the opening."),
(88,"CU","tired, dignified", f"CLOSE on {CHAMP} with the SAME framing and the SAME camera as the film's opening close-up, the same level eyes, nothing about him changed."),
(89,"WIDE","content, ordinary", f"A cartoon crowd streaming out into a flat evening sky, ordinary faces and ordinary coats, {SPEC} among them entirely content with himself."),
(90,"MED","warm, sincere", f"{SPEC} at a kitchen table with his family, warm and close and completely sincere, feeling like a good man and meaning it."),
(91,"CU","no villain here", f"CLOSE on {SPEC}'s face lit warm at the table, kind and ordinary, the least villainous face imaginable."),
(92,"MED","the payoff", f"{CHAMP} alone in the tunnel {HAND}, and a very small child reaching up and taking it, the only handshake in the entire film."),
(93,"XWIDE","tiny, still there", f"A VAST arena, empty and flat and quiet, with {CHAMP} still standing ABSURDLY alone at the centre long after everybody has gone home."),
]

WORLD = (
 "a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom "
 "of the late 1950s: flat gouache-painted backgrounds, characters painted as flat cels "
 "with confident tapering ink outlines and no interior shading. The palette is warm and "
 "graphic and drawn from INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, cream and "
 "flat VERMILION RED, and EACH SCENE KEYS ITS OWN DOMINANT COLOUR and its own "
 "architecture from that set rather than repeating one ground everywhere. Crowds are "
 "painted as ranked rows of simplified flat graphic shapes rather than rendered faces. "
 "Visible painted gouache texture and slight brush grain in the background washes. "
 "Expressions are BOLD and readable at a glance. Flat matte throughout: NO gradients, "
 "NO airbrushed shading, NO photographic texture, NO three-dimensional rendering, NO "
 "modern digital gloss. This is an ORIGINAL character and an original scene in a "
 "general mid-century cartoon idiom: NO existing cartoon characters, NO studio logos, "
 "NO trade dress, NO recognisable franchise designs of any kind. There is NO text, NO "
 "lettering, NO numbers, NO signage copy and NO writing of any kind anywhere in the "
 "image; any sign, board or banner that appears is completely BLANK. This is ONE SINGLE "
 "COHERENT SCENE, NOT a grid, NOT a model sheet, NOT a sheet of studies. 16:9, edge to "
 "edge, one scene, one camera.")

MIN_CAM = {'XCU': 6, 'CU': 20, 'TOCAM': 3, 'XWIDE': 3, 'LOW': 2, 'OVER': 1}
MAX_RUN = 3
MIN_HERO_SHARE = 0.50
MIN_EXAG_SHARE = 0.55
MAX_SETTING_SHARE = 0.40
EXAG = re.compile(r'\b(enormous|absurd\w*|vast|towering|tiny|colossal|dozens|hundreds|'
                  r'off the (?:top|edge)|comic|bristl\w*|flying|swinging|crowding)\b', re.I)
METAPHOR = re.compile(r'\b(scales?|coins?|masks?|mirror|price tag|plinth|padlock|box)\b', re.I)
PERSON = re.compile(r'CHAMPION|SMALL ONE|PARTICULAR SPECTATOR|spectators?|crowd|figures?|'
                    r'researchers|worker|family|officials?|reporters|child|clerk|physio|'
                    r'attendant|teammate|guests?|people|men\b|band', re.I)

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []
if sorted(s[0] for s in S) != list(range(1, len(sents) + 1)):
    errs.append(f'frames must map 1:1 to {len(sents)} sentences; board has {len(S)}')

cams = [s[1] for s in S]
c = Counter(cams)
for k, n in MIN_CAM.items():
    if c[k] < n: errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
run, prev = 1, None
for i, cam in enumerate(cams, 1):
    if cam == prev:
        run += 1
        if run > MAX_RUN: errs.append(f'frame {i}: {run} consecutive {cam}')
    else: run, prev = 1, cam

# ALIGNMENT. v2 shipped ~20 frames under the wrong sentence.
for i, s in enumerate(S, 1):
    line = sents[s[0] - 1]
    if re.search(r'\bhe\b|\bhim\b|\bhis\b|our man|the crowd|\bthey\b', line, re.I) \
       and not PERSON.search(s[3]):
        errs.append(f'b{i:02d}: line is about people, scene has nobody in it')
    if METAPHOR.search(s[3]) and not PERSON.search(s[3]):
        errs.append(f'b{i:02d}: metaphor object with nobody in the frame')

def setting(sc):
    for name, pat in [('arena', 'arena|court|floor|stand|rail|tiers'), ('locker', 'locker|physio'),
                      ('office', 'office|desks'), ('press', 'press room|reporters'),
                      ('street', 'street|bus|pavement|shop|restaurant'),
                      ('home', 'kitchen|family|dinner'), ('academic', 'lecture|corridor|researchers'),
                      ('gym', 'gym|training'), ('concert', 'concert|venue|band|violin'),
                      ('betting', 'betting'), ('tunnel', 'tunnel')]:
        if re.search(pat, sc, re.I): return name
    return 'other'
setc = Counter(setting(s[3]) for s in S)
top, n = setc.most_common(1)[0]
if n / len(S) > MAX_SETTING_SHARE:
    errs.append(f'setting "{top}" is {n}/{len(S)} ({n/len(S):.0%}), max {MAX_SETTING_SHARE:.0%}')

hero = [s for s in S if 'CHAMPION' in s[3] or 'SMALL ONE' in s[3]]
exag = [s for s in S if EXAG.search(s[3])]
named = sum(1 for s in S if s[2] != '-')
faceless = [i for i, s in enumerate(S, 1)
            if ('CHAMPION' in s[3] or 'SMALL ONE' in s[3]) and s[2] == '-']
if len(hero) / len(S) < MIN_HERO_SHARE:
    errs.append(f'character in {len(hero)}/{len(S)} ({len(hero)/len(S):.0%}), needs {MIN_HERO_SHARE:.0%}')
if len(exag) / len(S) < MIN_EXAG_SHARE:
    errs.append(f'comedy on {len(exag)}/{len(S)} ({len(exag)/len(S):.0%}), needs {MIN_EXAG_SHARE:.0%}')
if faceless:
    errs.append(f'figure present, no expression: {" ".join("b%02d" % i for i in faceless[:10])}')

runner = [i for i, s in enumerate(S, 1) if 'handshake' in s[3]]
if len(runner) < 4: errs.append(f'the unshaken hand appears {len(runner)}x, needs 4+')
if not any('taking it' in S[i - 1][3] for i in runner):
    errs.append('the runner never pays off - somebody must take the hand')

ladder = [i for i, s in enumerate(S, 1) if 'scoreboard' in s[3]]
if len(ladder) != 4: errs.append(f'scoreboard ladder has {len(ladder)} rungs, needs 4')
for i in ladder:
    if 'BLANK' not in S[i - 1][3]:
        errs.append(f'b{i:02d}: scoreboard not declared blank')

print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {c['XCU']+c['CU']} | expressions {named}/{len(S)} | "
      f"character {len(hero)}/{len(S)} ({len(hero)/len(S):.0%}) | comedy {len(exag)}/{len(S)} "
      f"({len(exag)/len(S):.0%}) | hand x{len(runner)} | ladder x{len(ladder)} | "
      f"top setting {top} {n}/{len(S)} ({n/len(S):.0%}) | settings {len(setc)}")

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs: print('  ' + e, file=sys.stderr)
    sys.exit(1)

ids = [f'b{i:02d}' for i in range(1, len(S) + 1)]
(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{s[3]} {WORLD}' for i, s in zip(ids, S)}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'expression': s[2],
      'line': sents[s[0] - 1], 'scene': s[3]} for i, s in zip(ids, S)], indent=1))
print(f'\nwrote {len(ids)} prompts + board.json')
