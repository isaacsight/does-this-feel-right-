#!/usr/bin/env python3
"""Frame book — Quitting (episode 7). 124 frames: 111 sentences + 13 second
frames for every sentence over 25 words, 4 of the 111 built as data frames.

Every law here was paid for on an earlier film, plus this film's new one:

  THE FLAT-RUN GATE        Isaac's law, first code enforcement: no run of 3+
                           consecutive rows that are BOTH castless ('-') AND
                           the same setting. Abstract stretches get concrete
                           distinct images with a human where the act allows.
  THE CAMERA IS A CROP     CAM names where the frame edge cuts; scene text
                           never says "close on".
  COUNTS, NOT NOUNS        the single lonely PAIR of hairs, THREE round
                           buttons, ONE whistle on ONE lanyard, FIVE snow
                           queuers, SEVEN robed judges, ONE small potted
                           plant, ONE watering can, TWO floors — stated in
                           EVERY frame that stages the character.
  DEADPAN IS AN ACTION     composed-amid-absurdity is a face ACTION, never
                           '-': "holding perfectly still, face composed,
                           eyes level" — declared AND in the scene text.
  EVENTS, NOT STATES       something happens in every frame.
  OMISSION, NOT NEGATION   absences described as present things.
  SIGN-SHAPE LAW           plaque / ticket / banner / lease / schedule (and
                           sheet/page/grid/dial/sign shapes) carry
                           "completely BLANK" in their own row; every other
                           document type-noun is banned outright.
  LIKENESS LAW             the wall's author and the register's namesake are
                           never drawn; the plaque never letters; surnames
                           gated out of scene text.
  NEVER SMUG               the Man's face does hope, dread, effort, relief.
  CLUB ACCENT              donkey act + verdict beats only: ONE hard
                           spotlight circle, the surround ALWAYS rows of
                           individuated silhouettes (empty black fails, paid
                           lesson), ONE deep warm brick-red back wall, value
                           language ("a step and a half darker"), capped.
  TWIST STAGING LAW        <=6 designated sunk-cost frames, ONE quietly
                           wrong small off-centre detail each, tagged below.
  THE STRAIGHT ACT (82-92) Langer & Rodin: no deadpan gags, no club, no
                           twist — warm plain daylight, composed dignity.
  THE HANDS                the film's subject: closed around objects in >=6
                           frames before the step; the ending lands in
                           script order — lays the ticket down (98), hands
                           open (101), the plant to the sill (104).
  ENVIRONMENT CAP          gym/wall frames <=22%, measured not hoped for.
  DATA FRAMES              pure-number beats (the 2.25:1 tilt, the 30%/15%
                           floors) built deterministically, NEVER generated,
                           excluded from prompts.json at the source.

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

MAN = ("THE MAN: a small slight man with a round face and a big confident nose, his head bald "
       "and smooth except for a single lonely PAIR of hairs at the very top of his crown — one "
       "thin hair kinking left, one leaning right — a flat VERMILION RED coat with THREE round "
       "buttons, thin stick legs and ABSURDLY oversized shoes")
KEEPER = ("THE WALL-KEEPER: a broad gym coach type in a SAGE GREEN tracksuit with ONE whistle "
          "on ONE lanyard, arms folded, monumentally still")
PLAQUE = "ONE huge completely BLANK framed plaque"
TICKET = "ONE completely BLANK ticket"
LEASE = "ONE completely BLANK lease sheet"
SCHED = "ONE completely BLANK schedule grid"
DONKEY = "ONE grey donkey with a composed patient face"
HAY = "ONE neat hay bale"
PAIL = "ONE full pail of water"
SILH = ("ROWS of individuated dark silhouettes seated politely around the dark, ONE deep warm "
        "brick-red back wall behind them")
PLANT = "ONE small potted plant in a mustard pot"
STILL = "holding perfectly still, face composed, eyes level"

DATA = "DATA FRAME — built deterministically, never generated"

CAM = {
 'XCU':   ("EXTREME CLOSE-UP, the camera pushed right in: the subject FILLS THE ENTIRE FRAME "
           "and is CROPPED HARD by all four edges. Almost no background is visible."),
 'CU':    ("CLOSE-UP: the subject FILLS THE FRAME, cropped at the chest, the top of the head "
           "near the top edge. Only a suggestion of background behind."),
 'MED':   "MEDIUM SHOT, the figures cut off at the knees and filling most of the frame height.",
 'WIDE':  "WIDE SHOT: the full figures sit well inside the frame with the setting around them.",
 'XWIDE': "VERY WIDE SHOT: the figures are SMALL in a large landscape that fills the frame.",
}
_CAMWORD = re.compile(r'^(EXTREME )?CLOSE(-UP)? on ', re.I)
def strip_cam(s):
    s = _CAMWORD.sub('', s)
    return s[0].upper() + s[1:] if s else s

# (line, camera, face action or '-', setting tag, scene)
S = [
# ACT 1 — the wall (gym, first light) -----------------------------------------
(1,"WIDE","-","gym", f"A gym interior at first light in formal frontal symmetry: one green-painted wall carrying {PLAQUE} tall as a door, ONE rack of dumbbells squared beneath it, early light lying flat and even across the floorboards."),
(2,"XCU","-","gym", f"One corner of the huge completely BLANK plaque filling the view, its green wall catching the early light, thick old paint standing proud at the frame's chipped edge."),
(3,"MED","holding perfectly still, face composed, eyes level","gym", f"{KEEPER} standing square beneath the huge completely BLANK plaque, {STILL}, the green wall filling the space behind him."),
(4,"MED","face attentive and exact","gym", "ONE inspector in a mustard coat crouched at ONE red wall extinguisher, peering close through ONE raised magnifier, his face attentive and exact, the gym floor stretching level behind him."),
(5,"WIDE","each face turned up mid-nod","gym", f"A file of FOUR gym-goers pacing past beneath the huge completely BLANK plaque, individuated with bags on shoulders, each face turned up toward it mid-nod, morning light flat down the room."),
(6,"MED","-","void", "Seen from slightly ABOVE, ONE completely BLANK sheet squared on a plain table, ONE uncapped pen resting at its foot, the sheet's lower corner bare and untouched, even light on the wood."),
(7,"MED","holding perfectly still, face composed, eyes up","gym", f"{MAN} stopped just inside the gym door beneath the green wall and its huge completely BLANK plaque, holding perfectly still mid-stride, face composed, eyes up at it."),
(8,"MED","both faces composed, eyes level","gym", f"{KEEPER} standing behind {MAN}, one broad hand resting flat on the Man's shoulder, both holding perfectly still, both faces composed, eyes level, the huge completely BLANK plaque squared above them."),
# ACT 2 — the kitchen table, the three papers ---------------------------------
(9,"WIDE","holding perfectly still, face composed, eyes level","kitchen", f"{MAN} seated square at a kitchen table with his coat still on, holding {LEASE}, {TICKET} and {SCHED} pressed together in two closed hands, {STILL}, morning light flat on the wood."),
(10,"XWIDE","-","shop", "The shop small in its empty dusk street, windows dark and sign shape completely BLANK, and before its door ONE small red-coated figure gripping ONE completely BLANK large paper sheet with both hands, tiny against the shopfront."),
(11,"XCU","-","kitchen", f"{TICKET} gripped in ONE closed hand, the paper bowing at its edges, one vermilion red cuff entering at the frame's edge, morning light flat across it."),
(12,"MED","eyes down, jaw set","kitchen", f"{MAN} at the kitchen table gripping ONE completely BLANK ruled grid sheet with both hands, one corner crumpling under his thumb, his eyes down and his jaw set, ONE small dusty trophy at the table's far corner."),
(13,"CU","brows soft, eyes wanting one small thing","kitchen", f"{MAN} looking down at the sheaf of completely BLANK papers in his two closed hands, his brows soft, his eyes wanting exactly one small thing."),
(14,"XCU","-","kitchen", "TWO closed hands resting on the kitchen table around the sheaf of completely BLANK papers, ONE forefinger lifting alone away from the grip."),
(15,"CU","-","kitchen", "TWO closed hands gripping the sheaf of completely BLANK papers, knuckles pale, the grip holding perfectly still on the table's edge."),
(16,"MED","faces composed, eyes level","void", "FOUR figures from different walks of life in different palette coats standing in a calm row on flat cream, individuated, each holding one small gripped object to the chest with closed hands, faces composed, eyes level."),
(17,"MED","holding perfectly still, face composed and hopeful","shop", f"{MAN} standing behind the shop counter at dusk with both closed hands flat on the wood, holding perfectly still, face composed and hopeful, the shelves half bare behind him, ONE wall clock with a single hand hanging off-centre near the door, flat INK BLUE dusk at the window."),
(18,"WIDE","-","shop", "The shop's far corner: ONE armchair parked facing the corner, ONE side table holding ONE cold cup, dust settled evenly over both, the corner lit like a destination by ONE bare bulb of flat mustard GOLD."),
(19,"MED","-","kitchen", "Seen from slightly ABOVE, ONE completely BLANK lease sheet squared alone at the kitchen table's centre, ONE pencil laid parallel beside it, the wood grain running level beneath."),
(20,"MED","both faces composed, eyes level","kitchen", f"{MAN} seated at one end of the kitchen table, and at the other end ONE tall mirror propped upright on a chair returning his face, the mirror's frame cracked at one corner, both faces composed, eyes level, holding perfectly still."),
# ACT 3 — the wall's author ---------------------------------------------------
(21,"MED","-","gym", f"Beside the green wall, ONE bronze statue of a generic leaping figure frozen mid-leap on ONE completely BLANK plinth, the huge completely BLANK plaque squared on the wall behind it."),
(22,"WIDE","-","void", "THREE completely BLANK stone plinths in a row beside the green gym wall, ONE bronze statue of a generic leaping figure standing on the first, the second and third plinths bare with ONE pale dust outline of feet on each."),
(23,"MED","faces settled and reasonable","void", "The bronze statue itself walking calmly away from its plinth carrying ONE bronze sports bag, shown at THREE points along one path — nearest large, middle smaller, farthest small at the door — the completely BLANK stone plinth left bare behind it."),
(24,"WIDE","face settled","void", "The bronze statue seated composed on ONE bench beside its bronze sports bag, legs crossed, one bronze hand resting on the bag's handle, waiting calmly in flat even light."),
(25,"MED","face steady; faces attentive","void", "The bronze statue standing at ONE podium before ROWS of seated individuated onlookers, one bronze arm raised mid-address, the onlookers' faces turned up attentive."),
(26,"CU","-","gym", "ONE telephone sitting on the gym floor directly beneath the huge completely BLANK plaque, its receiver at rest in the cradle, its cord coiled neatly beside it."),
(27,"MED","holding perfectly still, face composed","gym", f"{KEEPER} standing at the green wall beside ONE paint roller and ONE tray parked at the wall's foot, {STILL}, the huge completely BLANK plaque level above."),
# ACT 4 — the banquet ---------------------------------------------------------
(28,"WIDE","-","banquet", "A banquet hall dressed for a start: balloons in palette colours rising to the ceiling, ONE completely BLANK banner hanging over the door, long tables laid, dusty ORANGE lamplight warm across the room."),
(29,"WIDE","faces composed mid-cheer","banquet", "A press of banquet guests raising glasses in unison toward the door, individuated faces composed mid-cheer, holding perfectly still at the top of the toast, the completely BLANK banner above them."),
(30,"MED","face pleased and formal","banquet", "ONE tall white cake carried in high on ONE tray by ONE server, his face pleased and formal, guests turning as it passes, dusty ORANGE lamplight on the icing."),
(31,"MED","-","banquet", "Seen from slightly ABOVE at the banquet door, ONE completely BLANK sheet held open flat by TWO gloved hands, the doorway's warm dusty ORANGE light falling across it."),
(32,"MED","face bright and resolute","void", "ONE small food truck with ONE completely BLANK side panel parked on flat cream, ONE woman in a mustard apron folding out its serving hatch, her face bright and resolute."),
(33,"XWIDE","-","void", "ONE man with ONE suitcase pausing at the open door of ONE bus on flat cream, ONE small hometown drawn tiny at the horizon behind him, the road running long between."),
(34,"MED","face composed and proud","banquet", "The guest of honour standing at the banquet's centre in ONE fine new coat, his face composed and proud, and directly behind him ONE coat rack holding ONE worn old coat, lit exactly the same."),
(35,"WIDE","-","void", "ONE freestanding open doorway on flat cream seen exactly side-on, ONE figure mid-step inside it, the same crossing an entrance from one side and an exit from the other, even light."),
(36,"MED","faces warm; face composed","banquet", "At one door TWO greeters applauding ONE arriving guest, their faces warm; at the other door ONE attendant holding one flat palm turned up, his face composed; the room standing symmetrical between them."),
(37,"WIDE","individuated faces composed","banquet", "ONE long wedding table down the middle of the hall, guests raised mid-toast and holding perfectly still, HALF the glasses tipped toward the couple and HALF toward the open door, individuated faces composed, dusty ORANGE lamplight."),
# ACT 5 — the scale -----------------------------------------------------------
(38,"MED","both faces composed, eyes level","kitchen", f"{MAN} at the kitchen table with the sheaf of completely BLANK papers in two closed hands, and {KEEPER} standing behind him, one broad hand resting on the Man's shoulder, both faces composed, eyes level, holding perfectly still."),
(39,"WIDE","-","scaleroom", "ONE brass grocery scale standing alone at the centre of a flat cream field, squared to view, its pan level and its needle at rest."),
(40,"CU","-","scaleroom", "ONE brass grocery scale with ONE thumb resting quietly on its pan, the needle leaning under the touch, the flat cream field bare around it."),
(41,"WIDE","-","data", DATA),
(42,"WIDE","-","data", DATA),
(43,"MED","faces earnest","scaleroom", "TWO careful men in dark suits disputing across the brass scale, one pointing at the pan and one shaking his head slowly, their faces earnest, the thumb resting on the pan between them."),
(44,"XCU","-","scaleroom", "The scale's needle filling the view, leaning hard to one side and holding there, the dial behind it completely BLANK."),
(45,"MED","holding perfectly still, face composed","scaleroom", "ONE small packed suitcase set on the brass scale's pan, the needle swinging far over, and ONE watching figure standing beside it, holding perfectly still, face composed."),
(46,"WIDE","-","void", "ONE green felt gaming table standing on flat cream, chairs squared around it, ONE wheel already spinning at its centre before anyone sits, ONE chair with three legs standing matter-of-factly at the far corner."),
(47,"MED","face politely composed","void", "ONE croupier figure behind the green felt raking a river of chips toward his own side with ONE long rake, his face politely composed, the players' side of the table bare."),
(48,"CU","holding perfectly still, face composed, eyes level","void", f"{MAN} seated at the green felt with ONE small stack of chips before him, {STILL} on the spinning wheel."),
# ACT 6 — the snowstorm and the theatre ---------------------------------------
(49,"WIDE","-","snowstreet", "From inside a parked car: ONE completely BLANK ticket lying on the dashboard, snow driving sideways beyond the windscreen in flat INK BLUE dusk, ONE hairline crack running across the windscreen's lower corner."),
(50,"WIDE","individuated faces composed","snowstreet", f"FIVE coated figures queueing formally in driving snow before ONE theatre entrance, holding perfectly still, individuated faces composed, each holding ONE completely BLANK ticket, the lobby glowing dusty ORANGE and the street flat INK BLUE."),
(51,"XCU","-","snowstreet", "ONE coin purse lying open on its side on the dashboard, its mouth gaping bare, flat INK BLUE snow light lying across the worn leather."),
(52,"MED","face bright and certain","void", f"In warm October light on flat cream, {MAN} at ONE box-office window sliding coins across the sill with one hand and receiving {TICKET} with the other closed hand, his face bright and certain."),
(53,"MED","holding perfectly still, face composed, eyes on it","snowstreet", f"{TICKET} propped upright on the dashboard facing {MAN} at the wheel like a small speaker, the Man holding perfectly still, face composed, eyes on it, snow driving beyond the glass in flat INK BLUE dusk."),
(54,"WIDE","-","void", "FOUR doorways standing in a row on flat cream — one theatrical, one domestic, one clerical, one military in its trim — and ONE completely BLANK ticket lying squarely at each threshold, even light."),
(55,"MED","faces composed, eyes wide","void", "ONE completely BLANK ticket standing upright in ONE circle of lamplight, casting ONE long tall shadow up the wall behind it, TWO seated listeners leaning in, their faces composed and their eyes wide."),
(56,"XWIDE","-","snowstreet", "ONE small car driving alone into deepening snow down a long straight road, its headlamp beams flat mustard GOLD against the flat INK BLUE storm, one bare wiper arm sweeping the glass."),
(57,"MED","face measured; faces attentive","scaleroom", "ONE careful man in a dark suit presenting the brass scale to ROWS of seated listeners with one open hand, his face measured, their faces attentive, the flat cream field around them."),
(58,"MED","face serene","snowstreet", "Inside the theatre lobby, ONE attendant fanning a thick sheaf of completely BLANK tickets into one wide even fan, his face serene, dusty ORANGE lamplight warm on the carpet and flat INK BLUE dusk at the glass doors."),
# ACT 7 — the donkey (CLUB) ---------------------------------------------------
(59,"WIDE","face composed and patient","field", f"{DONKEY} standing at the centre of ONE hard spotlight circle, exactly midway between {HAY} and {PAIL}, holding perfectly still, the floor beyond the circle's edge a step and a half darker, {SILH}."),
(60,"CU","face composed and patient","field", f"The donkey's composed patient face dead centre, its grey muzzle level, {HAY} edging into view at one side and {PAIL} at the other, the hard light even and the dark beyond a step and a half darker."),
(61,"WIDE","face composed and patient","field", f"THREE stone busts of generic bearded thinkers on THREE completely BLANK plinths ringed just inside the spotlight circle's edge, {DONKEY} holding perfectly still at centre between {HAY} and {PAIL}, {SILH}."),
(62,"MED","face composed and patient","field", f"{DONKEY} caught mid-swivel, its head held at the exact midpoint of the turn from {HAY} to {PAIL}, inside the hard spotlight circle, {SILH}."),
(63,"WIDE","face composed even now","field", f"{DONKEY} lying flat on its side at the spotlight circle's centre, legs straight as a table's, its face composed even now, {HAY} untouched and full at one side and {PAIL} brim-full at the other, {SILH}."),
(64,"XCU","-","field", "FOUR grey donkey hooves planted in FOUR worn hollows in the stage floor, the hard light raking across the boards, the dark beyond the light's edge a step and a half darker."),
(65,"MED","face composed and patient","field", f"{DONKEY} standing at centre with ONE safety rope clipped from its harness to ONE floor ring on EACH side, both ropes pulled taut and even, holding perfectly still inside the spotlight circle, {SILH}."),
(66,"WIDE","faces composed and grave","field", f"SEVEN robed judges seated in ONE raised row at the spotlight circle's edge, their faces composed and grave, ONE gavel held mid-fall, {DONKEY} holding perfectly still below them, {SILH}."),
(67,"MED","faces earnest; the rest composed","field", "TWO of the SEVEN robed judges leaning together mid-dispute with hands raised, their faces earnest, the remaining FIVE holding composed and still, the hard light lying even along the row and the dark beyond a step and a half darker."),
(68,"WIDE","face composed","field", f"{DONKEY} still lying flat on its side at the spotlight circle's centre, legs straight, its face composed, {HAY} and {PAIL} both full and untouched beside it, {SILH}."),
# ACT 8 — tunnels and holes ---------------------------------------------------
(69,"WIDE","holding perfectly still, face composed, eyes down in dread","chemroom", "A chemistry room in flat even light: ONE student seated at a bench before ONE textbook lying open to TWO completely BLANK pages, ONE ashtray beside it holding ONE resting cigarette, the student holding perfectly still, face composed, eyes down in plain dread."),
(70,"XWIDE","-","void", "ONE long dark tunnel drawn straight through a hillside on flat cream, ONE small bright disc of daylight at its far end, ONE tiny walker inside pacing toward it."),
(71,"MED","faces relieved and level","void", "FIVE doctors in white coats stepping out of the tunnel's far mouth into plain daylight one after another, individuated, their faces relieved and level."),
(72,"XWIDE","-","void", "ONE round hole in flat ground wearing ONE arched tunnel entrance as a false front, the facade propped up from behind with TWO wooden braces, the land level and bare around it."),
(73,"MED","-","chemroom", "ONE plain stone stair descending step by step into a dark opening in the floor, ONE resting cigarette smoking on each of FIVE descending steps, the thin smoke rising straight in the still air, the stairwell otherwise bare and unoccupied, the stone plain and clean."),
(74,"MED","both faces composed","void", "TWO identical dark doorway openings side by side on flat cream, seen exactly square, and before each ONE plain man in a plain grey coat standing with hands at his sides, both men identical, both faces composed and level, the two dark openings exactly alike."),
(75,"WIDE","faces composed, eyes up","gym", "Beneath the huge completely BLANK plaque on the green wall, ONE medical student with ONE satchel and ONE smoker with ONE cigarette standing shoulder to shoulder, their faces composed, eyes up at it."),
(76,"MED","holding perfectly still, face composed","gym", f"{KEEPER} standing between the student and the smoker, one broad arm pointing them BOTH the same way down the room, {STILL}."),
(77,"MED","-","void", "ONE wooden post at a fork of two roads on flat cream carrying ONE single arm that points one way for both roads, the two roads bending apart beyond it."),
(78,"XCU","-","gym", "ONE tin of green paint standing open, ONE brush resting across its rim, one wet stripe of fresh green running up the wall behind it."),
(79,"MED","face patient and exact","void", "ONE careful figure standing before the two identical dark openings, lifting ONE lantern of flat mustard GOLD to each in turn, his face patient and exact."),
# ACT 9 — the bridge ----------------------------------------------------------
(80,"CU","holding perfectly still, face composed, eyes level","void", f"{MAN} on flat cream holding perfectly still with one forefinger raised, his face composed, his eyes level and serious."),
(81,"MED","-","void", "Seen from slightly ABOVE, ONE armchair parked at the lip of ONE round open hole in flat cream ground, turned to face away from it, ONE footstool set neatly before the chair."),
# ACT 10 — Langer & Rodin. PLAYED STRAIGHT: warm plain daylight, dignity. -----
(82,"WIDE","-","nursinghome", f"{PLANT} standing on a windowsill in warm plain daylight, ONE lace curtain stirring beside it, the sill's wood worn smooth."),
(83,"XWIDE","faces composed and dignified","nursinghome", "A plain nursing home seen square from across its lawn in warm daylight, TWO floors of lit windows, ONE composed elderly face at a window on each of the TWO floors, dignified and calm."),
(84,"MED","face attentive and dignified","nursinghome", f"ONE elderly resident tilting ONE watering can over {PLANT} on her sill, warm daylight on her hands, her face attentive and dignified."),
(85,"WIDE","face composed and distant","nursinghome", f"ONE staff nurse tilting ONE watering can over {PLANT} while ONE elderly resident sits nearby with hands folded in her lap, her face composed and distant, the room kept perfectly for her, warm daylight down its length."),
(86,"MED","face grave and careful","nursinghome", "ONE researcher at a plain desk in warm daylight moving beads across ONE wooden counting frame one at a time, his face grave and careful."),
(87,"WIDE","-","data", DATA),
(88,"WIDE","-","data", DATA),
(89,"MED","faces careful and grave","nursinghome", "TWO researchers seated at the plain desk with ONE completely BLANK sheet between them, one pointing at it, both faces careful and grave, warm daylight through the window."),
(90,"WIDE","faces alive and dignified","nursinghome", "The deciding floor's corridor in warm daylight: elderly residents at their own doors, one watering ONE window box, one greeting a neighbour across the hall, individuated faces alive and dignified."),
(91,"CU","-","nursinghome", f"{PLANT} held steady in TWO elderly hands, warm daylight through its leaves, the hands sure around the pot."),
(92,"CU","face intent and dignified","nursinghome", "ONE elderly hand hovering over TWO cups set on ONE tray, mid-choice, warm daylight across the tray, her face beyond it intent and dignified."),
(93,"WIDE","-","field", f"{PLANT} standing alone at the centre of the hard spotlight circle, the light holding on its leaves, {SILH}."),
(94,"XCU","-","void", "The elderly resident's armchair with the small plant beside it on the sill, ONE wilted leaf lying dropped on the wood, her hands folded at rest in her lap, her face calm and turned to the middle distance."),
# ACT 11 — the step, the open hands, the plant --------------------------------
(95,"WIDE","holding perfectly still, face composed","frontstep", f"{MAN} standing on ONE snow-dusted front step at dusk, {TICKET} held in one closed hand, snow falling straight in flat INK BLUE dusk, holding perfectly still, face composed, ONE porch lamp of flat mustard GOLD above the door."),
(96,"CU","brows soft, eyes clearing","frontstep", "The Man's face lifting into the falling snow, his brows soft and his eyes clearing, snowflakes resting on the vermilion red shoulders, flat INK BLUE dusk behind."),
(97,"XCU","-","frontstep", f"TWO closed hands held at the chest around {TICKET}, one vermilion red cuff at each side, snow drifting past in flat INK BLUE dusk."),
(98,"MED","face composed and gentle","frontstep", f"{MAN} bending down and laying {TICKET} flat on the snow-dusted step, face up, his face composed and gentle, flat INK BLUE dusk around him and the porch lamp's flat mustard GOLD across the snow."),
(99,"XWIDE","-","frontstep", "The front step and the street holding still, snow falling evenly, the completely BLANK ticket lying face up on the step under the porch lamp's flat mustard GOLD, flat INK BLUE dusk down the whole street."),
(100,"WIDE","-","frontstep", "The doorway seen exactly square: lintel level, floorboards level, snow drifting past the porch, everything holding calmly in its place, flat INK BLUE dusk beyond the lamp's flat mustard GOLD."),
(101,"CU","face soft and calm","frontstep", "The Man's TWO hands OPEN at his sides, palms forward, fingers loose, snow passing behind them, his face above them soft and calm, flat INK BLUE dusk."),
(102,"MED","face calm","frontstep", f"{MAN} holding both open palms up toward the falling snow, his face calm, and far across the street ONE green wall carrying ONE huge completely BLANK plaque standing small in the flat INK BLUE dusk."),
(103,"XCU","-","frontstep", "ONE open palm turned up, ONE snowflake resting whole at its centre, flat INK BLUE dusk beyond the fingers."),
(104,"MED","face at peace","frontstep", f"Indoors in warm lamplight, {MAN} lifting {PLANT} onto the windowsill with TWO open hands, into the light, his face at peace, snow falling soft beyond the glass in flat INK BLUE."),
(105,"MED","face calm","frontstep", f"{MAN} standing at the window beside {PLANT} on its sill, both open hands resting on the sill's wood, his face calm, the flat INK BLUE evening framed warm by the lamplight."),
(106,"WIDE","-","frontstep", "ONE snow-dusted stone step filling the picture, the completely BLANK ticket lying large at its centre, the porch lamp's flat mustard GOLD lying across it, single snowflakes settling on its face, and the rounded toe of ONE ABSURDLY oversized dark shoe just entering the bottom corner beside it, one thin band of flat INK BLUE dusk along the top edge."),
(107,"CU","chin level, eyes calm and certain","frontstep", "The Man's face in the warm window light, chin level, his eyes calm and certain, his face composed, the flat INK BLUE evening soft behind him."),
(108,"XCU","-","frontstep", "TWO open hands at rest on the windowsill's wood — the Man's own small hands in the same warm peach skin tone as his face, flat deep-red sleeve cuffs at both wrists — fingers loose, the small mustard pot standing between them, warm lamplight over all and flat INK BLUE beyond the glass."),
(109,"WIDE","face composed","gym", f"Morning in the gym: the green wall carrying ONE wet sheen of fresh paint, the huge completely BLANK plaque squared upon it, ONE paint tray and ONE roller parked below, and {KEEPER} standing at his post beside it, his face composed."),
(110,"MED","face easy and warm","gym", f"{MAN} passing the green wall at an easy walk, one open hand lifting in a small wave toward the huge completely BLANK plaque, his face easy and warm, {KEEPER} tipping one small nod back, morning light flat across the floor."),
(111,"XWIDE","-","gym", f"{MAN} walking out through the gym's open door into the morning, open hands swinging loose at his sides, small against the light, the green wall and its huge completely BLANK plaque holding still behind him."),
]

# ============================================================================
# SECOND FRAMES — every sentence over 25 words carries two pictures so the
# hold stays under ~9.6s at 157wpm.
# ============================================================================
EXTRA = {
 4:  [("MED","all three faces earnest","gym", "At the gym's front desk, TWO members leaning in toward ONE seated clerk, mouths open mid-argument, hands spread over the counter, all three faces earnest, the morning light flat behind them.")],
 5:  [("CU","eyes already sliding toward the door","gym", "ONE gym-goer's face mid-nod up at the huge completely BLANK plaque, his eyes already sliding toward the door beyond it, his bag strap pulling at his shoulder.")],
 15: [("MED","chin level, face composed and dignified","kitchen", f"{MAN} sitting upright at the kitchen table, chin level, his face composed and dignified, the sheaf of completely BLANK papers held to his chest in two closed hands.")],
 22: [("MED","face exact and unhurried","void", "ONE record keeper in a grey cardigan standing beside the bronze statue holding ONE open book of completely BLANK ruled pages toward it, his brows raised politely, the statue frozen mid-leap above him.")],
 40: [("MED","faces absorbed and exact","scaleroom", "TWO careful men in dark suits bent close over the brass scale, one holding ONE magnifier up to the pan, their faces absorbed and exact, the flat cream field around them.")],
 50: [("CU","-","snowstreet", "ONE gloved hand holding ONE completely BLANK ticket up into the driving snow, the paper catching the dusty ORANGE lobby glow, flat INK BLUE evening beyond it.")],
 61: [("MED","face composed and patient","field", f"ONE silhouetted arm reaching from the dark into the hard light to pass ONE completely BLANK sheet toward {DONKEY}, which holds perfectly still, the light's edge a step and a half darker beyond.")],
 65: [("MED","-","field", f"Seen from slightly ABOVE, the grey donkey's shadow falling exactly midway between {HAY} and {PAIL}, its shape centred to the stride, the circle of hard light holding all three.")],
 66: [("MED","-","field", "Seen from slightly ABOVE, ONE completely BLANK sheet laid square at the centre of the circle of hard light, ONE gavel resting beside it, the boards a step and a half darker beyond the light's edge.")],
 84: [("MED","faces engaged and dignified","nursinghome", "TWO elderly residents carrying TWO chairs to the window themselves, mid-step, their faces engaged and dignified, warm daylight down the room.")],
 89: [("MED","-","nursinghome", "Seen from slightly ABOVE, ONE completely BLANK sheet squared alone on the plain desk in warm daylight, ONE pencil laid level beside it.")],
 93: [("MED","-","void", "Seen from directly ABOVE, filling the frame: ONE completely BLANK large paper sheet, ONE completely BLANK small ticket and ONE completely BLANK ruled grid sheet laid in a calm row on bare level wood, every face bare and unmarked, the table's chairs pushed in and the room still, ONE empty stretch of wood at the row's end.")],
 104:[("XCU","-","frontstep", f"{PLANT} on the sill, lamplight of flat mustard GOLD on its leaves, snow falling soft beyond the glass in flat INK BLUE.")],
}

_S = []
for row in S:
    _S.append(row)
    for cam, expr, setting, scene in EXTRA.get(row[0], []):
        _S.append((row[0], cam, expr, setting, scene))
S = _S

# TWIST — the rationed staging law: designated sunk-cost frames only, ONE
# quietly wrong off-centre detail each, tagged here so the cap is measured.
TWIST = {
 17: 'a single hand',            # the shop clock
 20: 'cracked at one corner',    # the mirror
 46: 'three legs',               # the casino chair
 49: 'hairline crack',           # the windscreen
 56: 'bare wiper arm',           # the wiper
}
TWIST_MAX = 6

WORLD = (
 "a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom of the "
 "late 1950s: flat gouache-painted backgrounds and flat painted cel figures with confident "
 "tapering ink outlines and no interior shading, in a warm graphic palette of INK BLUE, "
 "mustard GOLD, sage GREEN, dusty ORANGE, cream and flat VERMILION RED, each scene keying its "
 "own dominant colour from that set. Expressions are BOLD, exaggerated and readable at a "
 "glance. Visible gouache texture, flat matte, NO gradients, NO airbrushed shading, NO "
 "photographic texture, NO three-dimensional rendering. There is NO text, NO lettering, NO "
 "numbers and NO writing of any kind anywhere in the image; any sign, board, plaque, label, "
 "badge, ticket, page, banner, document or screen is completely BLANK. Any crowd is "
 "individuated: different faces, different builds, clothes in DIFFERENT colours from the "
 "palette, never a row of matching coats. These are ORIGINAL characters in a general "
 "mid-century cartoon idiom: NO existing cartoon characters, NO studio logos, NO trade "
 "dress, and no likeness of any real person. ONE SINGLE COHERENT SCENE, NOT a grid of "
 "panels, NOT a sheet of studies. 16:9, edge to edge, one scene, one camera.")

WPM = 157
MAX_HOLD = 9.6
MIN_CAM = {'XCU': 10, 'CU': 12, 'XWIDE': 8}
MAX_RUN = 3
MIN_CU_SHARE = 0.20
MIN_EVENT_SHARE = 0.85
GYM_MAX_SHARE = 0.22
CLUB_MAX = 10
CORE_ENVS = {'gym','kitchen','shop','banquet','scaleroom','snowstreet','field','chemroom',
             'nursinghome','frontstep','void','data'}
STRAIGHT_LINES = range(82, 93)   # the Langer & Rodin act, played entirely straight
DUSK_ENVS = {'snowstreet','frontstep'}   # named lighting colours bite here

FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|cheeks|'
                  r'tongue|chin|frown|soft|calm|composed|weary|star(e|ing)|blush|surprise|nod|'
                  r'dread|faces?\b|wanting|patient|measured|settled|kind\b|pleased|sincere|'
                  r'grave|serene|earnest|resolut|absorb|trust|eager|certain|attentive|exact|'
                  r'unhurried|dignified|steady|clear|level|warm|bright|hopeful|reasonable|'
                  r'relieved|engaged|intent|distant|gentle|easy|at peace|proud|resolved|'
                  r'serious|careful|alive|sure|still\b', re.I)
EVENT = re.compile(
    r'burst|pop|fly|flar|blast|shoot|erupt|stream|pour|collaps|toppl|crack|snap|spring|slam|'
    r'throw|thrown|swing|scatter|shov|carr|drop|slid|tipping|tilt|vibrat|lift|roll|hover|dart|'
    r'glow|steam|smok|nod|shak|crouch|lean|reach|step|walk|run|hold|haul|pull|peer|point|count|'
    r'trudg|wrap|bang|settl|duck|turn|rub|sip|thump|spray|strik|rais|crush|crane|hang|stretch|'
    r'wav|file|squeez|press|balanc|climb|land|swarm|feed|trac|receiv|arriv|load|cross|'
    r'tumbl|pil|recoil|glanc|hurry|bend|bent|crowd|tear|driv|measur|argu|greet|wait|'
    r'watch|look|open|shut|reced|dwarf|clutch|slip|fork|appear|swivel|rotat|freez|curl|march|'
    r'thud|bow|sweep|stoop|practis|welcom|fold|jump|rest|loom|dangl|buckl|puff|retir|pose|'
    r'smooth|travel|drift|tuck|unroll|brush|nail|study|shrink|brighten|flood|offer|spill|'
    r'meet|wish|spread|ring|split|huddl|thrust|catch|pass|grip|perform|plant|rise|rising|'
    r'casc|flick|aim|stagger|clip|steady|repeat|pace|pacing|plump|clink|pin|tap|wheel|light|'
    r'lit\b|beam|trad|dip|recit|square|straighten|leap|rock|spin|pat|draw|heap|tick|sit\b|'
    r'sitting|stand|pry|arrang|withdraw|refocus|swell|flex|declar|consult|boast|agree|'
    r'flutter|park|screw|dress|stride|striding|shuffl|nose|nosing|perch|box|fall|lying|laid|'
    r'\blay\b|stir|gap|burn|water|applaud|toast|cheer|dispute|disput|grip|griping|rake|rakes|'
    r'raking|fan|fanning|coil', re.I)

# COUNTS, NOT NOUNS — a scene that stages a character must carry the numeric
# words. A reference sheet is not sufficient.
REQ = {
 'VERMILION RED coat':   ['THREE round buttons', 'PAIR of hairs'],
 'SAGE GREEN tracksuit': ['ONE whistle', 'ONE lanyard'],
 'donkey':               ['grey'],
 'hay bale':             ['ONE neat hay bale'],
 'pail':                 ['ONE full pail'],
 'coated figures':       ['FIVE'],
 'potted plant':         ['ONE small potted plant', 'mustard pot'],
 'watering can':         ['ONE watering can'],
 'robed judges':         ['SEVEN'],
}

sents = [s.strip() for s in re.split(r'[.!?]+', (FILM / 'script.txt').read_text()) if s.strip()]

errs = []

# NEVER NAME THE ARTEFACT — in narration or in scene text.
SELFREF_N = re.compile(r'\bthis (film|movie|video|episode)\b|voice-?over|\bnarrat\w+|'
                       r'camera crew|documentary', re.I)
hits = [(n, s) for n, s in enumerate(sents, 1) if SELFREF_N.search(s)]
if hits:
    errs.append('narration names the artefact: ' +
                '; '.join(f'line {n}: "{s[:60]}"' for n, s in hits[:4]))
SELFREF_S = re.compile(r'\b(movie|video|episode|documentary|narrat\w+|camera|viewer)\b|close on',
                       re.I)
scam = [i for i, s in enumerate(S, 1) if s[4] != DATA and SELFREF_S.search(s[4])]
if scam:
    errs.append('scene references the artefact/camera/viewer: ' +
                ' '.join('b%03d' % i for i in scam[:10]))

lines = [s[0] for s in S]
missing = sorted(set(range(1, len(sents) + 1)) - set(lines))
if missing:
    errs.append(f'sentences with no frame: {missing[:12]}')
if lines != sorted(lines):
    errs.append('frames run backwards through the script')
if max(lines) > len(sents):
    errs.append(f'frame points at sentence {max(lines)}; script has {len(sents)}')

# SECOND-FRAME COVERAGE — every sentence over 25 words holds two pictures.
per_line = Counter(lines)
long_uncovered = [n for n, s in enumerate(sents, 1)
                  if len(s.split()) > 25 and per_line[n] < 2]
if long_uncovered:
    errs.append(f'>25-word sentences with a single frame: {long_uncovered}')

# DURATION BUDGET — estimated holds sum to the script's runtime, and no single
# hold runs past MAX_HOLD.
total_words = sum(len(s.split()) for s in sents)
budget = total_words / WPM * 60
holds = [(len(sents[s[0]-1].split()) / WPM * 60) / per_line[s[0]] for s in S]
if abs(sum(holds) - budget) > 0.10 * budget:
    errs.append(f'estimated holds sum to {sum(holds):.0f}s; budget {budget:.0f}s (+/-10%)')
over = [(i, h) for i, h in enumerate(holds, 1) if h > MAX_HOLD]
if over:
    errs.append('holds past %.1fs: ' % MAX_HOLD +
                ' '.join(f'b{S[i-1][0]:03d}({h:.1f}s)' for i, h in over[:8]))

braces = [i for i, s in enumerate(S, 1) if '{' in s[4] or '}' in s[4]]
if braces:
    errs.append('unrendered f-string braces: ' + ' '.join('b%03d' % i for i in braces[:10]))

isdata = [s[4] == DATA for s in S]
live = [s for s, d in zip(S, isdata) if not d]          # generated frames only
ndata = sum(isdata)
if not 2 <= ndata <= 4:
    errs.append(f'{ndata} data frames; this film expects 2-4')

cams = [s[1] for s in live]
c = Counter(cams)
for k, n in MIN_CAM.items():
    if c[k] < n:
        errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
cu = c['CU'] + c['XCU']
if cu / len(live) < MIN_CU_SHARE:
    errs.append(f'close-ups {cu}/{len(live)} ({cu/len(live):.0%}), needs {MIN_CU_SHARE:.0%}')
run, prev = 1, None
for i, cam in enumerate(cams, 1):
    if cam == prev:
        run += 1
        if run > MAX_RUN:
            errs.append(f'live frame {i}: {run} consecutive {cam}')
    else:
        run, prev = 1, cam

# THE FLAT-RUN GATE — Isaac's law: no run of 3+ consecutive rows that are
# both castless (expression '-') AND the same setting.
flat_run, flat_set, flagged = 0, None, []
for i, s in enumerate(S, 1):
    if s[2] == '-':
        if s[3] == flat_set:
            flat_run += 1
        else:
            flat_run, flat_set = 1, s[3]
        if flat_run >= 3:
            flagged.append((i, s[3], flat_run))
    else:
        flat_run, flat_set = 0, None
if flagged:
    errs.append('FLAT RUN — 3+ consecutive castless rows in one setting: ' +
                '; '.join(f'row {i} ({env}, run of {r})' for i, env, r in flagged[:6]))

# FACE ACTION — declared, and present in the scene text itself.
noface = [i for i, s in enumerate(S, 1)
          if not isdata[i-1] and s[2] != '-' and not FACE.search(s[2])]
if noface:
    errs.append('expression names no face action: ' + ' '.join('b%03d' % i for i in noface[:10]))
lost = [i for i, s in enumerate(S, 1)
        if not isdata[i-1] and s[2] != '-' and not FACE.search(s[4])]
if lost:
    errs.append('face action absent from the SCENE text: ' + ' '.join('b%03d' % i for i in lost[:10]))

noev = [i for i, s in enumerate(S, 1) if not isdata[i-1] and not EVENT.search(s[4])]
if (len(live) - len(noev)) < MIN_EVENT_SHARE * len(live):
    errs.append(f'physical event on {len(live)-len(noev)}/{len(live)}, needs '
                f'{MIN_EVENT_SHARE:.0%}; flat: ' + ' '.join('b%03d' % i for i in noev[:10]))

# COUNTS PRESENT wherever the marker appears.
for marker, needs in REQ.items():
    bad = [i for i, s in enumerate(S, 1) if not isdata[i-1] and marker in s[4]
           and any(need not in s[4] for need in needs)]
    if bad:
        errs.append(f'"{marker}" staged with counts missing ({needs}): ' +
                    ' '.join('b%03d' % i for i in bad[:8]))

# OMISSION, NOT NEGATION — reject negation describing visual content.
NEG = re.compile(r"\bno\s|\bwithout\b|n't\b", re.I)
neg = [i for i, s in enumerate(S, 1) if not isdata[i-1] and NEG.search(s[4])]
if neg:
    errs.append('negation in scene text: ' + ' '.join('b%03d' % i for i in neg[:10]))

# SIGN-SHAPE LAW — no scene may request written content; every label-shaped
# word from the allowed set states BLANK in its own row; every other document
# type-noun is banned outright (label-invitation law).
SIGNS = re.compile(r'\b(letter|letters|lettering|lettered|word|words|writing|written|writes|'
                   r'text|texts|number|numbers|numeral|numerals|digits?|caption|inscrib\w*|'
                   r'font|typeface|says|reading\b|reads\b)\b', re.I)
signy = [i for i, s in enumerate(S, 1) if not isdata[i-1] and SIGNS.search(s[4])]
if signy:
    errs.append('scene requests written content: ' + ' '.join('b%03d' % i for i in signy[:10]))
BLANKREQ = re.compile(r'\b(plaques?|tickets?|banners?|leases?|schedules?|sheets?|pages?|'
                      r'grids?|plinths?|signs?|signboards?|papers?|textbooks?|dials?)\b', re.I)
unblanked = [i for i, s in enumerate(S, 1) if not isdata[i-1]
             and BLANKREQ.search(s[4]) and 'BLANK' not in s[4]]
if unblanked:
    errs.append('label-shaped object staged with its BLANK missing: ' +
                ' '.join('b%03d' % i for i in unblanked[:10]))
BANNED_NOUNS = re.compile(r'\b(labels?|posters?|contracts?|certificat\w*|documents?|ledgers?|'
                          r'invoices?|nameplates?|charts?|clipboards?|calendars?|newspapers?|'
                          r'reports?|receipts?|memos?|folders?|slips?|cards?|bills?|lists?|'
                          r'prospectus\w*)\b', re.I)
typed = [i for i, s in enumerate(S, 1) if not isdata[i-1] and BANNED_NOUNS.search(s[4])]
if typed:
    errs.append('banned document type-noun in scene text: ' +
                ' '.join('b%03d' % i for i in typed[:10]))

# LIKENESS LAW — the narration may say the names; the pictures never do.
NAMES = re.compile(r'Jordan|Carr\b|Kahneman|Tversky|Arkes|Blumer|Buridan|Aristotle|Ghazali|'
                   r'Langer|Rodin|Michael|Washington|Connecticut', re.I)
likeness = [i for i, s in enumerate(S, 1) if NAMES.search(s[4]) or NAMES.search(s[2])]
if likeness:
    errs.append('a real surname reached SCENE text: ' + ' '.join('b%03d' % i for i in likeness))

# NEVER SMUG — the Man's face does hope, dread, effort, relief. Gated everywhere.
SMUG = re.compile(r'smug|smirk|\bsly\b|snide', re.I)
smug = [i for i, s in enumerate(S, 1) if SMUG.search(s[4]) or SMUG.search(s[2])]
if smug:
    errs.append('smugness reached a row: ' + ' '.join('b%03d' % i for i in smug))

# ENVIRONMENT CAP — gym/wall frames <=22%; every core environment appears.
setc = Counter(s[3] for s in S)
unknown = sorted(set(setc) - CORE_ENVS)
if unknown:
    errs.append(f'unknown environment tags: {unknown}')
gym_n = setc['gym']
if gym_n / len(S) > GYM_MAX_SHARE:
    errs.append(f'gym frames are {gym_n}/{len(S)} ({gym_n/len(S):.0%}), max {GYM_MAX_SHARE:.0%}')
unused = sorted(CORE_ENVS - set(setc))
if unused:
    errs.append(f'core environments unused: {unused}')

# NAMED LIGHTING COLOURS — every dusk/snow frame states INK BLUE at point of use.
unlit = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] in DUSK_ENVS
         and 'INK BLUE' not in s[4]]
if unlit:
    errs.append('dusk frame missing flat INK BLUE at point of use: ' +
                ' '.join('b%03d' % i for i in unlit[:10]))

# THE STRAIGHT ACT (82-92) — no deadpan gags, no club, no twist; warm plain
# daylight and dignity in every row.
COMIC = re.compile(r'spotlight|silhouett|brick-red|donkey|gag\b|absurd|comic|grin|wink|'
                   r'holding perfectly still|three legs|single hand|cracked|wiper|casino|'
                   r'felt\b|COLOSSAL|ENORMOUS', re.I)
bent = [i for i, s in enumerate(S, 1) if s[0] in STRAIGHT_LINES and not isdata[i-1]
        and (COMIC.search(s[4]) or COMIC.search(s[2]))]
if bent:
    errs.append('the straight act broke its straightness: ' + ' '.join('b%03d' % i for i in bent))
unwarm = [i for i, s in enumerate(S, 1) if s[0] in STRAIGHT_LINES and not isdata[i-1]
          and s[3] == 'nursinghome' and ('warm' not in s[4] or 'daylight' not in s[4])]
if unwarm:
    errs.append('straight-act row missing warm plain daylight: ' +
                ' '.join('b%03d' % i for i in unwarm[:10]))

# CLUB ACCENT — every spotlight row carries its populated surround (the paid
# theatre lesson: empty black fails) and the brick-red wall; capped.
club = [i for i, s in enumerate(S, 1) if not isdata[i-1] and 'spotlight' in s[4]]
badclub = [i for i in club if 'silhouettes' not in S[i-1][4] or 'brick-red' not in S[i-1][4]]
if badclub:
    errs.append('club frame with an unpopulated surround or missing brick-red wall: ' +
                ' '.join('b%03d' % i for i in badclub))
if len(club) > CLUB_MAX:
    errs.append(f'{len(club)} club frames; cap {CLUB_MAX}')
outside = [i for i in club if not (59 <= S[i-1][0] <= 68 or S[i-1][0] == 93)]
if outside:
    errs.append('club staging outside the donkey act / verdict beats: ' +
                ' '.join('b%03d' % i for i in outside))

# TWIST — <=6 tagged frames, each carrying its one quietly wrong detail, and
# every tagged line sitting outside the straight act.
if len(TWIST) > TWIST_MAX:
    errs.append(f'{len(TWIST)} twist frames tagged; cap {TWIST_MAX}')
def _scene_for(line):
    rows = [s for s in S if s[0] == line]
    return rows[0][4] if rows else ''
for line, detail in TWIST.items():
    if detail not in _scene_for(line):
        errs.append(f'twist line {line} missing its wrong detail "{detail}"')
    if line in STRAIGHT_LINES:
        errs.append(f'twist tagged inside the straight act: line {line}')

# THE HANDS — closed around an object in >=6 frames before the step, and the
# ending lands in script order: lays the ticket (98) -> hands open (101) ->
# the plant to the sill (104).
closed = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[0] < 98
          and 'closed hand' in s[4]]
if len(closed) < 6:
    errs.append(f'the Man\'s hands close around an object in {len(closed)} frames '
                f'before the step; the law is at least 6')
ending_checks = [
    (98,  'laying', 'line 98 stages the ticket laid down'),
    (98,  'ticket', 'line 98 stages the ticket laid down'),
    (101, 'OPEN',   'line 101 stages the hands opening'),
    (104, 'plant',  'line 104 stages the plant lifted to the sill'),
    (104, 'sill',   'line 104 stages the plant lifted to the sill'),
]
for line, need, msg in ending_checks:
    if need not in _scene_for(line):
        errs.append(f'THE ENDING out of order: {msg}')

# INTERACTION QUOTA — the wall-keeper and the Man share at least TWO frames.
shared = [i for i, s in enumerate(S, 1)
          if 'SAGE GREEN tracksuit' in s[4] and 'VERMILION RED coat' in s[4]]
if len(shared) < 2:
    errs.append(f'the wall-keeper and the Man share {len(shared)} frames; the law is at least 2')

dead = [s for s in S if s[2] == '-' and s[4] != DATA]
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(live)} ({cu/len(live):.0%}) | faces "
      f"{len([s for s in live if s[2]!='-'])}/{len(live)} | events "
      f"{len(live)-len(noev)}/{len(live)} | data {ndata} | gym {gym_n} "
      f"({gym_n/len(S):.0%}) | club {len(club)} | twist {len(TWIST)} | "
      f"closed-hands {len(closed)} | castless {len(dead)} | holds "
      f"{sum(holds):.0f}s/{budget:.0f}s")
print('settings: ' + '  '.join(f'{k}={v}' for k, v in setc.most_common()))

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs:
        print('  ' + e, file=sys.stderr)
    sys.exit(1)

ids, _seen = [], {}
for row in S:
    n = _seen.get(row[0], 0)
    _seen[row[0]] = n + 1
    ids.append(f'b{row[0]:03d}' + ('' if n == 0 else chr(ord('a') + n)))
assert len(set(ids)) == len(ids), 'duplicate frame id'

(FILM / 'production').mkdir(exist_ok=True)
# Data rows are deterministic ImageMagick builds and must NEVER reach the
# generator: the tipping batch sent them once and the model drew the sentinel
# text, burning retries against the glyph gate. Excluded at the source.
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{CAM[s[1]]} {strip_cam(s[4])} {WORLD}'
     for i, s in zip(ids, S) if s[4] != DATA}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'expression': s[2], 'setting': s[3],
      'line': sents[s[0] - 1], 'scene': s[4],
      'twist': s[0] in TWIST and TWIST[s[0]] in s[4],
      'hold_est_s': round((len(sents[s[0]-1].split()) / WPM * 60) / per_line[s[0]], 2)}
     for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S) if s[4] == DATA or s[2] == '-']
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
