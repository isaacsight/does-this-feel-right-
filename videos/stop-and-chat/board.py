#!/usr/bin/env python3
"""Frame book — The Stop-and-Chat (episode 8). 119 frames across 92 sentences:
every sentence carries at least one picture, every sentence over 25 words
carries two or three, and 4 of the 119 are built as deterministic data cards.

Direction: DEADPAN GEOMETRY — the gap between people is the subject of every
frame. Every law below was paid for on an earlier film; the three at the top
are the ones that bite hardest on THIS one.

  FLAT-RUN v1             no run of 3+ consecutive rows that are BOTH castless
                          ('-') AND the same setting.
  FLAT-RUN v2             and no cross-setting castless run either — a symbol
                          in a void followed by a symbol in the snow is the
                          same fault wearing a different coat. Max castless
                          run is 2, measured, everywhere.
  THE GAP IS THE SUBJECT  two-figure frames state "exactly TWO figures" at
                          point of use or the occupants prior grows a crowd;
                          the empty middle is painted as carefully as either
                          figure; composed-amid-avoidance is a face ACTION,
                          never '-'.
  THE PLATFORM MONUMENT   the same FIVE REGULARS in the same five positions
                          (mustard/sage/ink-blue/dusty-orange/cream) expanded
                          in FULL at every point of use — a reference sheet
                          is not sufficient, gated per row.
  COUNTS, NOT NOUNS       the single lonely PAIR of hairs, THREE round
                          buttons, ONE row of round buttons, ONE small
                          ink-blue scarf, ONE completely BLANK folded
                          newspaper — stated in EVERY frame that stages them.
  THE CAMERA IS A CROP    CAM names where the edge cuts; scene text never
                          says "close on" and never names the artefact.
  LABEL-INVITATION        every sign/board/oval/panel/cup/newspaper/card/
                          sheet/page/dial carries "completely BLANK" in its
                          own row; every other document type-noun is banned
                          outright. Delete the labelled object, never argue
                          with it.
  OMISSION, NOT NEGATION  absences described as present things — an empty
                          seat is "one cushion undented".
  EVENTS, NOT STATES      something happens in every frame; these are stills,
                          so every row stages a HELD moment of an action.
  NAMED LIGHTING COLOURS  snow dusk states flat INK BLUE at point of use;
                          lamplight is flat mustard GOLD. Never "a darker mix".
  LIKENESS LAW            no comedian, no researcher, no real person is ever
                          drawn; surnames gated out of scene text entirely.
  NEVER SMUG              the avoider is us. His face does dread, calculation,
                          hope, relief. The grip on silence is priced.
  THE WARM ACT (37-44)    the coffee-shop act is played straight: warm plain
                          daylight, full gravity, no geometry gags at all.
  CLUB ACCENT — ONE       exactly ONE club frame in the whole film, on the
                          twist beat: ONE hard spotlight circle, the surround
                          ALWAYS rows of individuated silhouettes (empty black
                          fails — paid theatre lesson), ONE deep warm
                          brick-red back wall.
  INTERACTION QUOTA       the Man and the Familiar Stranger share >=4 frames
                          without ever facing each other; the avoidance arc
                          appears TWICE as concrete footprint geometry in
                          snow (never a diagram, never a dotted line); the
                          final row stages them two paces apart, both turned,
                          mouths CLOSED.
  ENVIRONMENT CAP         platform frames <=22%, measured not hoped for.
  DATA FRAMES             pure-number beats (the three-way split, the
                          2%/48%/34% exits, 89%, 4.0 vs 1.5) built
                          deterministically, NEVER generated, excluded from
                          prompts.json at the source.

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
FS = ("THE FAMILIAR STRANGER: a tall composed woman in a mustard GOLD coat with ONE row of round "
      "buttons and ONE small ink-blue scarf, carrying ONE completely BLANK folded newspaper")
GREY = "ONE tall man in an ink-blue coat with ONE grey scarf"
REGULARS = ("THE FIVE REGULARS holding the same five positions far apart along the platform's "
            f"yellow line — {FS} standing third from the left, ONE broad man in a sage GREEN "
            f"coat, {GREY}, ONE woman in a dusty-orange coat, ONE woman in a cream coat — all "
            "five faces individuated and composed, all five aimed straight ahead")
ELEVOTHER = "ONE broad man in a sage GREEN coat with ONE flat cap"
BENCHOTHER = ("ONE seated woman in a dusty-orange coat with ONE completely BLANK folded "
              "newspaper closed on her lap")
BARISTA = ("THE BARISTA: a broad warm-faced man with short flat DARK hair, warm peach skin and "
           "a wide easy jaw, drawn flat in one single even paint tone, in a sage GREEN apron "
           "behind ONE counter with ONE brass machine")
ARC = ("ONE curved line of single footprints pressed into level snow, bending wide out toward "
       "the kerb and back again")
OVAL = "ONE completely BLANK white oval board"
INDICATOR = ("ONE long indicator strip above the doors carrying ONE row of small round unlit "
             "lamps, every lamp face completely BLANK")
PHONES = ("ONE pair of round headphones seated over both ears, the cord hanging loose with its "
          "plug end resting free")
PHOTOWALL = ("ONE plain wall carrying NINE small photographic prints hung in THREE even rows of "
             "THREE, each print showing one plain painted commuter face, the wall bare and even "
             "around them")
SILH = ("ROWS of individuated dark silhouettes seated politely around the dark, ONE deep warm "
        "brick-red back wall behind them")
TWO = "exactly TWO figures"
WARM = "warm plain daylight"

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
# ACT 1 — the sidewalk arc ----------------------------------------------------
(1,"XWIDE","both faces composed and level","sidewalk", f"A long empty sidewalk on a Tuesday morning, squared straight down its length in flat even light: {TWO} held far apart at either end of the pavement, {MAN} striding at the near end and {GREY} striding at the far end, the wide bare pavement lying level between them, both faces composed and level."),
(2,"CU","eyes flicking sideways, face composed and innocent","sidewalk", "The Man's round face and big confident nose held level as he paces, the single lonely PAIR of hairs standing up at the very top of his crown — one thin hair kinking left, one leaning right — his eyes flicking sideways along the pavement, his face composed and innocent, the flat morning light even behind him."),
(3,"WIDE","both faces composed and purposeful","sidewalk", f"{TWO} on the long sidewalk, each one veering a small deliberate step outward at the same moment: {MAN} drifting toward ONE row of parked cars at the kerb and {GREY} drifting the other way toward the shopfronts, both faces composed and purposeful, the pavement opening bare between them."),
(3,"XWIDE","-","snowstreet", f"Seen from slightly ABOVE, {ARC}, and beside it ONE second line of footprints bending the opposite way, the pale lane of untouched snow lying wide and smooth between the two curves, one thin band of flat INK BLUE dusk along the far kerb."),
(3,"MED","both faces composed, eyes level","sidewalk", f"{TWO} passing each other at the widest point of the sidewalk, {MAN} walking close to the parked cars and {GREY} walking close to the shopfronts, both aimed straight ahead with their faces composed and their eyes level, the bare lane of pavement holding wide between them."),
(4,"XWIDE","both faces composed and level","sidewalk", f"A shuttered hardware shopfront on the empty morning street, ONE completely BLANK white sign board over its door and ONE stack of tin pails on the pavement outside, {TWO} sliding wide apart as they pass it — {MAN} and {GREY} — both faces composed and level."),
(4,"MED","faces composed and serious","void", "FOUR children about nine years old pacing a bare cream floor in TWO pairs, each pair drifting a small step apart at the same moment exactly as the grown ones do, individuated, their faces composed and serious."),
(5,"MED","faces turned up and attentive","void", "FOUR children seated in ONE row of small chairs on flat cream, all four faces turned up and attentive toward ONE empty chair standing where a teacher would sit, its cushion undented and its seat bare."),
(6,"XCU","-","void", "Seen from directly ABOVE and filling the view, ONE completely BLANK large paper sheet squared alone on plain level wood, ONE uncapped pen resting at its foot, the sheet's face bare and even under flat light."),
(7,"MED","face composed and mild","sidewalk", "ONE warden in a dusty-orange uniform standing at the kerb with both hands resting behind his back, his face composed and mild, watching the wide bare stretch of pavement where the two walkers passed."),
(8,"WIDE","face stiff with dread, the other face composed","sidewalk", f"{TWO} caught at the exact moment of a break: {MAN} halted mid-stride with one hand half-raised and his mouth open on a single sound, his face stiff with dread, and {GREY} three paces further on already turned away along the pavement, his face composed."),
# ACT 2 — the elevator and the headphones -------------------------------------
(9,"WIDE","both faces composed and level","elevator", f"{TWO} inside ONE small steel elevator, squared dead centre: {MAN} pressed into the left corner and {ELEVOTHER} pressed into the right, a bare stretch of floor lying between their shoes, both chins lifted, both faces composed and level, {INDICATOR}."),
(10,"MED","both faces composed and patient","elevator", f"Inside the steel elevator, {TWO} — {MAN} and {ELEVOTHER} — both with their chins tipped up at {INDICATOR}, ONE panel of round unlit buttons completely BLANK beside the doors, both faces composed and patient, the floor lying bare between them."),
(10,"XCU","-","elevator", f"{INDICATOR}, filling the view, ONE single lamp glowing flat mustard GOLD at its middle, the brushed steel around it plain and even."),
(11,"CU","chin lifted, face composed and studious","elevator", "The Man's round face tipped up, his chin lifted, the single lonely PAIR of hairs at his crown catching the light — one thin hair kinking left, one leaning right — his face composed and studious, the plain steel ceiling above him."),
(12,"XCU","eyes tipped up, face composed and studious","elevator", "The broad man's face in the opposite corner, tipped up at exactly the same angle, ONE flat cap pushed back on his head, his eyes tipped up and his face composed and studious, plain steel behind him."),
(13,"WIDE","both faces composed, eyes up","elevator", f"The whole nine-foot steel room seen square: {TWO} standing in opposite corners, {MAN} and {ELEVOTHER}, a wide bare rectangle of floor lying between them, both faces composed and their eyes up at {INDICATOR}."),
(13,"MED","-","elevator", "Seen from directly ABOVE, the two crowns of two heads in opposite corners of a small steel box — one bald and smooth with a single lonely PAIR of hairs standing up at its top, one wearing ONE flat cap — and the bare square of floor lying wide between them."),
(14,"WIDE","faces composed and sealed","traincar", f"A carriage of rows of seats in flat even light: FOUR individuated commuters seated far apart, each one wearing {PHONES}, each face composed and sealed, one empty seat between every pair of them with its cushion undented."),
(15,"XCU","face composed, eyes level","traincar", f"{PHONES}, filling the view over one composed face at the edge of the picture, the cord hanging in one long loose curve, his face composed and his eyes level."),
(15,"WIDE","faces bright and busy","sidewalk", "A shopfront fully lit and fully staffed on the morning street: THREE individuated shop staff at their posts inside, one lifting a crate, one polishing the counter, their faces bright and busy, and ONE completely BLANK closed sign hanging square in the middle of the bright window."),
(16,"MED","faces composed and admiring","void", "ONE pair of round headphones resting alone on ONE small cream plinth, completely BLANK, and TWO onlookers standing well back with their hands behind their backs, their faces composed and admiring."),
(17,"XWIDE","face composed and untroubled","sidewalk", f"{MAN} wearing ONE pair of round headphones with the cord's plug end resting free, shown at THREE points along one long pavement — nearest large, middle smaller, farthest small at the corner — his face composed and untroubled at every one of the three."),
# ACT 3 — the 7:40, and the archive walking in --------------------------------
(18,"XWIDE","all five faces individuated and composed","platform", f"ONE long commuter platform seen square and formally symmetrical in flat morning light, {OVAL} hanging over the middle of it, {REGULARS}, and {MAN} stepping onto his own spot at the near end, wide empty concrete lying between every one of them."),
(19,"WIDE","faces composed and kind","traincar", "A full carriage at capacity: SIX individuated commuters seated far apart down the rows, every face composed and kind, one empty seat standing between each of them with its cushion undented and its armrest bare."),
(19,"MED","face kind and formal","traincar", "ONE seated commuter in a cream coat lifting his bag off the seat beside him and setting it on his knees to leave that seat open, his face kind and formal, the rest of the carriage holding composed and still around him."),
(20,"MED","face polite and exact","traincar", "ONE archivist in a sage GREEN coat stepping in through the carriage doors carrying ONE small wooden bead counter, his face polite and exact, the seated commuters holding composed and still along the rows behind him."),
(21,"WIDE","-","data", DATA),
(21,"MED","three faces composed and distinct","void", "THREE commuters standing far apart on flat cream, individuated and distinct: the first turned toward a stranger with his mouth open mid-sentence, the second seated alone holding ONE completely BLANK folded newspaper, the third standing plainly with both hands in his pockets, all three faces composed."),
(22,"WIDE","faces certain and composed","traincar", "SIX individuated seated commuters down the carriage rows, every one of them with one hand raised in a vote and every raised hand leaning the same way, their faces certain and composed."),
(23,"MED","face braced and hopeful","sidewalk", f"{MAN} halted with one ABSURDLY oversized shoe already up on the step of ONE bus door, his hand gripping the rail, his face braced and hopeful, the bare morning pavement stretching behind him."),
(24,"XWIDE","faces individuated and composed","void", "ONE long commuter train drawn side-on crossing flat cream, its windows a level row of small warm dusty ORANGE rectangles, ONE individuated seated figure at each window, every face composed."),
(25,"MED","both faces open and warm","traincar", f"{TWO} seated commuters turned toward each other across one carriage table mid-conversation, one leaning in with a hand lifted, both faces open and warm, the rest of the rows holding composed and still behind them."),
(26,"CU","brows up, face plainly pleased","traincar", "ONE talker's face filling the picture, her brows up and her mouth open on a laugh she is holding, her face plainly pleased, the blurred flat cream of the carriage wall behind her."),
(27,"CU","face lifted and delighted","traincar", "The same talker's face lifted a degree further, her chin up and her eyes bright, her face delighted and composed, one hand rising into the bottom edge of the picture."),
(28,"CU","face braced and composed","traincar", "The listener on the receiving end, his hands still flat on his knees at the bottom edge, his shoulders squared, his face braced and composed as the talking arrives from the left.")
,
(29,"WIDE","both faces warm and easy","traincar", f"{TWO} seated commuters now both turned in toward each other, both leaning the same small degree, both faces warm and easy, the carriage rows holding composed and still around them."),
# ACT 4 — the liking gap ------------------------------------------------------
(30,"WIDE","faces composed, every one leaning the same way","void", "SEVEN individuated figures standing in ONE wide row on flat cream, spaced far apart, every one of them leaning the same small degree to the same side, their faces composed."),
(31,"XWIDE","faces small and composed","sidewalk", "A tall grey street seen straight down its middle, small individuated figures walking far apart on both pavements, their faces composed, one thin band of flat INK BLUE lying along the rooftops."),
(32,"CU","face grave and exact","void", "ONE careful man in a dusty-orange coat holding ONE brass pocket gauge up into the light with both hands, its dial completely BLANK, his face grave and exact."),
(33,"XCU","-","void", "ONE brass gauge filling the view, its dial completely BLANK, its single needle bent hard over to one side and resting there, the brass rim worn smooth."),
(34,"WIDE","face exact and careful, the other face composed","void", f"{TWO} standing far apart on flat cream, one holding ONE brass rule up level in the wide empty air between them and squinting along it, his face exact and careful, the other standing still with her face composed."),
(35,"MED","both faces composed and polite","void", f"A plain lab room on flat cream: {TWO} strangers seated far apart at either end of ONE long table, both leaning back, both faces composed and polite, and ONE archivist in a sage GREEN coat watching from the far corner."),
(35,"WIDE","faces individuated and composed","void", "ROWS of folding chairs standing open on flat cream, individuated workshop attendees gathered in pairs far apart between them, each pair holding a wide gap, every face composed and pleasant."),
(35,"WIDE","both faces composed and level","stairwell", "A long dormitory corridor with FOUR plain doors down one side, ONE student standing at the first door and ONE student standing at the last, both half-turned back into their own rooms, both faces composed and level, the corridor floor lying bare between them."),
(36,"CU","face wincing slightly, brows drawn","stairwell", "The Man's face in the corridor as he walks out, his brows drawn and one eye narrowed, his face wincing slightly at something already finished, the plain wall running level behind him."),
(36,"WIDE","every face wearing the same faint wince","traincar", "A full carriage of individuated seated commuters, every single one of them wearing the same faint wince at the same moment, hands folded in laps, the rows running level down the picture."),
# ACT 5 — THE WARM ACT. Played straight: warm plain daylight, no gags. --------
(37,"MED","face easy and warm","coffeeshop", f"{BARISTA} drawing one slow cloth along the counter in {WARM}, his sleeves pushed up, his face easy and warm drawn flat with ONE clean tapering ink outline and one single even paint tone across his face, flat matte everywhere, the brass machine standing bright beside him painted as ONE flat gouache shape."),
(38,"MED","face down and hurried","coffeeshop", f"ONE customer in a hurry at the counter, coat still swinging, pushing ONE completely BLANK small card across the wood with one hand and his eyes down, his face hurried, {BARISTA} meeting the card with one broad hand in {WARM}."),
(38,"MED","both faces warm and level","coffeeshop", f"{MAN} standing squarely at the counter with his chin lifted, meeting the barista's eyes, and {BARISTA} leaning in on both forearms, both faces warm and level, {WARM} across the wood between them."),
(39,"XCU","-","coffeeshop", f"ONE completely BLANK cup set down on the counter by ONE broad hand, the steam rising straight, the wood grain running level beneath it in {WARM}."),
(40,"WIDE","faces composed and patient","coffeeshop", f"FIVE individuated customers standing in ONE queue at even spacing across the shop, bags on shoulders, their faces composed and patient, {WARM} lying down the whole length of the counter."),
(41,"CU","face warm and surprised","coffeeshop", "The Man's face lifted from the counter, his chin up and his eyes meeting someone above the bottom edge, his face warm and surprised, warm plain daylight across his cheek."),
(41,"XCU","-","coffeeshop", f"TWO bare hands in the same warm peach skin tone as every face meeting over ONE completely BLANK small card across the counter, one broad hand from a rolled sage GREEN sleeve and one small hand from a VERMILION RED sleeve, the card passing between them, {WARM} on the wood."),
(42,"CU","face warm and content","coffeeshop", f"ONE woman at a small table pressing ONE small ink stamp down onto ONE completely BLANK ruled page, one round mark for each day, her face warm and content in {WARM}."),
(43,"WIDE","one face down, one face turned back and warm","coffeeshop", f"TWO customers leaving by the same door at once, individuated: one walking out with his head down and his face closed, the other turned back over her shoulder mid-thanks with her face warm, {WARM} through the glass."),
(44,"CU","face plainly lighter","coffeeshop", f"The Man on the pavement side of the shop window holding ONE completely BLANK cup, his shoulders down and his face plainly lighter than it was, {WARM} on the glass beside him."),
# ACT 6 — minute nine, and the 2021 exits -------------------------------------
(45,"WIDE","both faces composed and level","bench", f"{TWO} on ONE long park bench, {MAN} at the far left end with one forefinger raised and {BENCHOTHER} at the far right end, the long empty middle of the bench painted as carefully as either of them, both faces composed and level."),
(46,"CU","mouth open on one small sound, face braced","bench", "The Man's face on the bench, his mouth open on one small sound, his chin lifted, his face braced and composed, the sage GREEN park hedge lying flat behind him."),
(47,"XCU","jaw composed and level","bench", "ONE small hand lifted in a half-greeting and held perfectly still at shoulder height, one flat VERMILION RED cuff at its wrist, the Man's jaw composed and level at the top edge of the picture."),
(48,"WIDE","both faces stiff and composed","bench", f"{TWO} at the two far ends of ONE long park bench with the topic finished, {MAN} and {BENCHOTHER}, both aimed straight ahead, both faces stiff and composed, the long empty middle of the bench bare and bright between them."),
(48,"WIDE","both faces composed and trapped","void", f"ONE plain room on flat cream with its walls running unbroken all the way round, TWO chairs standing far apart against opposite walls, {TWO} seated in them, both faces composed and trapped, the bare floor lying wide between."),
(49,"MED","face exact and unhurried","bench", "ONE archivist in a sage GREEN jacket crouched low beside the end of the park bench holding ONE brass stopwatch out flat on his palm, his face exact and unhurried, the bench running away level behind him."),
(50,"XWIDE","faces individuated and composed","void", "ROWS of small benches standing far apart across a wide flat cream field, TWO individuated seated figures at the two ends of every bench, every gap the same width, every face composed."),
(51,"WIDE","-","data", DATA),
(52,"MED","both faces composed and tired","bench", f"{TWO} still sitting at the two ends of the long park bench long after, {MAN} and {BENCHOTHER}, ONE long band of flat mustard GOLD evening light lying across both their knees, both faces composed and tired."),
(53,"MED","one face wanting more, one face composed","bench", f"{TWO} at the bench: {BENCHOTHER} already risen and half-turned back with one hand still out toward the seat, her face wanting more, and {MAN} settling back against the slats with his face composed."),
(54,"MED","both faces exact and careful","bench", "TWO hands, one at each end, holding ONE brass rule laid flat along the empty slats of the long park bench and measuring the gap between them, both faces above it exact and careful."),
(55,"CU","chin level, face firm","bench", "The Man's face on the bench with one flat open palm raised into the bottom edge of the picture, stopping something, his chin level and his face firm."),
(56,"WIDE","both faces composed and level","bench", f"{TWO} at the two far ends of the long park bench, {MAN} and {BENCHOTHER}, ONE brass rule lying along the whole bare middle stretch of slats between them, that stretch running as long again as the two of them together, both faces composed and level."),
# ACT 7 — both chairs ---------------------------------------------------------
(57,"MED","face careful and curious","void", "ONE small brass shape held up and turned slowly in TWO hands on flat cream, the Man's face beyond it careful and curious, the light lying even across the metal."),
(58,"WIDE","both faces composed and polite","bench", f"{TWO} gripping the slats at their own ends of the long park bench, {MAN} and {BENCHOTHER}, each leaning one small degree toward the path out and each holding, both faces composed and polite, the empty middle bright between them."),
(58,"MED","both faces composed and dutiful","void", f"{TWO} standing far apart on flat cream, each feeding ONE brass coin into ONE small slot post standing midway between them, its dial completely BLANK, both faces composed and dutiful."),
(59,"MED","face composed and recognising","void", f"TWO identical plain chairs standing far apart on flat cream, {MAN} seated composed in the left one, and the right one holding one cushion dented in exactly his shape, his face composed and recognising."),
(60,"MED","face dawning and grave","void", f"{MAN} standing between TWO plain wooden chairs holding ONE hammer loose at his side, fresh sawdust lying at his ABSURDLY oversized shoes, his face dawning and grave."),
(61,"WIDE","both faces courteous and composed","void", f"{TWO} standing far apart on flat cream, each politely holding up one end of ONE long plain plank between them, the plank standing as the very wall that keeps them apart, both faces courteous and composed."),
(62,"XWIDE","faces kind and individuated","void", "A wide cream room of individuated figures each performing one small courtesy at once — one holding a door, one offering a chair, one lifting a bag from a lap — every face kind and every gesture aimed away from its own owner."),
(63,"WIDE","faces composed and hopeful","void", "The same wide cream room as everybody rises to leave, individuated, each one still holding out one small object toward somebody else, every hand still full, every face composed and hopeful."),
# ACT 8 — 1972, the photographs, the platform ---------------------------------
(64,"MED","face careful and exact","void", "ONE long plain shelf standing at chest height on flat cream with FIVE small brass objects set along it, ONE archivist reaching for the fifth with both hands, his face careful and exact."),
(65,"XWIDE","all five faces individuated and composed","platform", f"The long commuter platform square and formally symmetrical again in flat morning light, {OVAL} over its middle, {REGULARS}, {MAN} at his own spot at the near end, and ONE archivist at the far end stooping behind ONE boxy black bellows apparatus on ONE wooden tripod."),
(65,"MED","faces composed and attentive","platform", f"ONE archivist standing on the platform a week later holding THREE small photographic prints out at arm's length toward {REGULARS}, each print showing one plain painted commuter face, their faces composed and attentive, wide empty concrete between him and every one of them."),
(66,"WIDE","-","data", DATA),
(67,"WIDE","-","data", DATA),
(67,"MED","face recognising and calm","platform", f"{MAN} standing at his own spot with his eyes travelling along the line of {REGULARS}, FOUR of the five held inside ONE broad band of flat mustard GOLD morning light and the fifth standing just outside it, his face recognising and calm."),
(68,"WIDE","face recognising and grave","void", f"{MAN} standing before {PHOTOWALL} with one hand raised toward THREE of the prints and one hand at his side, his face recognising and grave."),
(68,"XCU","-","platform", "ONE pair of ABSURDLY oversized dark shoes standing exactly on the yellow line at the platform's edge, the painted yellow running level across the picture, the concrete grain even around them."),
(68,"WIDE","all five faces individuated and composed","platform", f"The platform's yellow line running the whole width of the picture with {REGULARS} and {MAN} standing far apart along it, ONE pale worn patch of concrete under each pair of shoes marking the exact spot each of them has kept for years."),
# ACT 9 — the honest weighing -------------------------------------------------
(69,"CU","face exact and careful","void", "ONE bare hand in warm peach skin, its wrist rising from a mustard GOLD sleeve, lowering the fifth small brass weight onto the pan of ONE brass balance, the beam settling, and the archivist's face beyond it exact and careful."),
(70,"WIDE","both faces composed and easy","traincar", f"{TWO} commuters sharing one carriage bench seat with their shoulders almost touching, both faces composed and easy, and through the window behind them ONE dark street corner at night with ONE lone figure standing under ONE lamp of flat mustard GOLD."),
(71,"MED","face fair and exact","void", f"ONE archivist standing at {PHOTOWALL} with one flat hand resting over the middle print, his face fair and exact, the bare cream floor running out wide in front of him."),
(72,"MED","face uncertain and honest","coffeeshop", f"ONE customer at a small table turning ONE small brass dial by hand, its dial completely BLANK, her face uncertain and honest, {WARM} across the table."),
(73,"MED","both faces fair and composed","void", "TWO archivists standing far apart on flat cream, the nearer one holding both open palms up in plain concession and the farther one standing squared with his hands at his sides, both faces fair and composed."),
(74,"XCU","-","void", "ONE bare thumb on a bare hand in warm peach skin, its wrist rising from a mustard GOLD sleeve, sliding THREE small brass weights off the pan of the brass balance, the pan lifting and the beam easing back toward level, the brass worn bright."),
(75,"WIDE","faces composed, every one leaning the same degree","stairwell", "The long dormitory corridor with FOUR students standing at FOUR plain doors, every one of them leaning the same small degree back into their own doorway, every face composed, the corridor floor bare down the middle."),
(75,"MED","one face braced, one face already warm","coffeeshop", f"{BARISTA} leaning in over the counter with his face already warm, and ONE customer standing back a full pace with his shoulders up and his face braced, {WARM} between them."),
(76,"MED","face level and honest","void", "The long plain shelf with FIVE small brass objects standing along it, every one of them tipped the same way, and ONE archivist standing back from it with both arms at his sides, his face level and honest."),
# ACT 10 — the twist: the courtesy is the unkind act. ONE club frame. ---------
(77,"MED","face polite and composed","traincar", "ONE seated commuter's polite half-smile held under ONE hard band of flat mustard GOLD light falling in through the carriage window and lying across his folded hands and the seat back beside him, his face lifted clear of the band in plain even light, polite and composed."),
(78,"WIDE","both faces composed and courteous","traincar", f"{TWO} commuters seated far apart across the carriage aisle, both aimed straight ahead, both faces composed and courteous, the bare aisle floor running wide and clean between them."),
(79,"XWIDE","-","snowstreet", f"Seen from slightly ABOVE, {ARC}, and beside it ONE second line of footprints bending the opposite way, the pale lane of untouched snow lying wide and smooth between the two curves, one thin band of flat INK BLUE dusk along the far kerb."),
(79,"MED","both faces composed, chins up","elevator", f"{TWO} in opposite corners of the small steel elevator, {MAN} wearing ONE pair of round headphones with the cord's plug end resting free and {ELEVOTHER} with his cap pushed back, both chins up at {INDICATOR}, both faces composed."),
(80,"CU","face opening, hands loosening","traincar", "The spoken-to commuter's face filling the picture as it opens, his brows lifting and his mouth starting, his hands loosening off his knees at the bottom edge, the carriage flat and even behind him."),
(81,"MED","face composed and well-meaning, mouth CLOSED","traincar", f"{MAN} seated in the carriage holding both open palms level on his knees, his mouth CLOSED, his face composed and well-meaning, one empty seat beside him with its cushion undented."),
(81,"WIDE","both faces composed and courteous","club", f"ONE hard spotlight circle on a dark stage floor with {TWO} seated far apart at the two ends of ONE long bench inside it, a wide stretch of empty bench between them, BOTH facing straight out toward the dark room, heads level and parallel, eyes forward, each resting ONE open palm flat on the bench in the empty middle, both palms bare, both faces composed and courteous, the floor beyond the circle's edge a step and a half darker, {SILH}."),
(81,"CU","face composed and unaware","traincar", "The receiving commuter's face in the carriage, turned to the window with his chin level, his face composed and unaware, one thin band of flat INK BLUE along the glass beside him."),
(82,"MED","both faces composed and pleasant","traincar", f"{TWO} seated eighteen inches apart on one carriage bench, {MAN} and {FS}, both aimed straight ahead, both faces composed and pleasant, the narrow strip of seat between them empty and undented."),
(82,"XWIDE","every face composed and individuated","traincar", "The whole carriage down its length: TEN individuated commuters seated in pairs, every pair holding exactly the same gap between them, every one of them aimed straight ahead, every face composed."),
(83,"CU","face composed and careful","traincar", "The Man's face at the carriage window, chin level, the single lonely PAIR of hairs at his crown standing up — one thin hair kinking left, one leaning right — his face composed and careful."),
(84,"WIDE","both faces careful and composed","traincar", f"{TWO} seated commuters turning their heads one small degree away from each other at exactly the same moment, both faces careful and composed, the empty strip of seat between them lying bare."),
# ACT 11 — tomorrow at 7:40 ---------------------------------------------------
(85,"XWIDE","all five faces individuated and composed","platform", f"The long commuter platform square and symmetrical in flat morning light with ONE train drawing in along its edge, {OVAL} over the middle, {REGULARS}, and {MAN} standing at his own spot, every one of them holding the same eleven inches of space."),
(86,"MED","face composed and level","platform", f"{REGULARS}, the ink-blue-coated man with ONE grey scarf standing exactly on his own worn patch of concrete, his face composed and level, wide empty platform lying on both sides of him."),
(87,"XCU","-","platform", "TWO carriage doors parting a hand's width, the rubber edges drawing back, ONE small round chime lamp glowing flat mustard GOLD above them, the steel plain and even around it."),
(88,"MED","face turned to the glass, eyes wanting, mouth CLOSED","traincar", f"{TWO} seated across the aisle, {MAN} with his face turned to the glass and his eyes wanting and his mouth CLOSED, and {FS} seated opposite aimed straight ahead, the bare aisle running between them."),
(88,"XWIDE","face individuated and calm","stairwell", "ONE tall apartment front seen across the tracks from the platform's edge, THREE lit third-floor windows in a row, ONE individuated figure standing at the middle window holding ONE completely BLANK cup, her face calm, the brickwork running flat and even around them."),
(89,"XWIDE","faces composed and settled","traincar", "The whole carriage holding still, individuated commuters seated in the same postures down every row, hands in the same places, all faces composed and settled."),
(90,"XCU","-","void", "ONE flat open palm filling the view with ONE small brass coin resting at its centre, the fingers loose and level, the light lying flat across the skin."),
(91,"CU","face hopeful and unsure","void", "The same small brass coin lifted a hand's width above the open palm between TWO fingertips, the Man's face beyond it hopeful and unsure."),
(92,"XWIDE","all five faces individuated and composed","platform", f"The long commuter platform square and symmetrical in flat morning light, {OVAL} over the middle, {REGULARS} standing at their five positions and {MAN} at his own, every one of them waiting, wide empty concrete lying between all of them."),
(92,"MED","both faces composed and hopeful, mouths CLOSED","platform", f"exactly TWO figures filling the near half of the picture, {MAN} and {FS} standing CLOSE, only two paces of bare platform between them — a gap ONE stride wide — at the platform's near end, both turned fully toward each other for the first time, mouths CLOSED, both faces composed and hopeful, the long platform lying bare and bright behind the two of them, every stretch of concrete empty to the far end."),
]

# TWIST — the rationed staging law: a small number of designated frames each
# carrying ONE quietly wrong off-centre detail, tagged here so the cap is
# measured and so none of them lands inside the warm act.
TWIST = {
 15: 'fully staffed',                 # the closed sign on a bright busy shop
 48: 'unbroken all the way round',    # the room with no door in it
 59: 'dented in exactly his shape',   # the other chair
 61: 'the very wall',                 # the plank they politely hold up
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
MIN_CAM = {'XCU': 12, 'CU': 16, 'XWIDE': 16}
MAX_RUN = 3
MIN_CU_SHARE = 0.20
MIN_WIDE_SHARE = 0.38          # the geometry direction wants room for the gap
MAX_CASTLESS_RUN = 2           # flat-run v1 AND v2, measured together
PLATFORM_MAX_SHARE = 0.22
CLUB_MAX = 1
CLUB_LINES = {81}
CORE_ENVS = {'platform','traincar','sidewalk','elevator','coffeeshop','bench','stairwell',
             'snowstreet','void','club','data'}
STRAIGHT_LINES = range(37, 45)          # the coffee-shop act, played entirely straight
DUSK_ENVS = {'snowstreet'}              # named lighting colours bite here
TWOFIG_ENVS = {'elevator', 'bench'}     # the two-figure rooms
REG_REQ = ['REGULARS', 'sage GREEN coat', 'ink-blue coat', 'dusty-orange coat', 'cream coat']

FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|cheeks|'
                  r'tongue|chin|frown|soft|calm|composed|weary|star(e|ing)|blush|surprise|nod|'
                  r'dread|faces?\b|wanting|patient|measured|settled|kind\b|pleased|sincere|'
                  r'grave|serene|earnest|resolut|absorb|trust|eager|certain|attentive|exact|'
                  r'unhurried|dignified|steady|clear|level|warm|bright|hopeful|reasonable|'
                  r'relieved|engaged|intent|distant|gentle|easy|at peace|proud|resolved|'
                  r'serious|careful|alive|sure|still\b|mild|innocent|polite|courteous|braced|'
                  r'stiff|sealed|studious|delighted|content|lighter|trapped|firm|curious|'
                  r'recognising|dawning|honest|unaware|unsure|untroubled|fair\b|open\b|'
                  r'purposeful|individuated|CLOSED|admiring|formal|tired|concern', re.I)
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
    r'\blay\b|stir|gap|burn|water|applaud|toast|cheer|dispute|disput|rake|rakes|'
    r'raking|fan|fanning|coil|veer|pass|kink|polish|stamp|vote|seat|bend|part|widen|'
    r'keep|kept|risen|halt|swing|queue|marking|worn', re.I)

# COUNTS, NOT NOUNS — a scene that stages a character must carry the numeric
# words. A reference sheet is not sufficient (paid lesson, twice).
REQ = {
 'VERMILION RED coat': ['THREE round buttons', 'PAIR of hairs', 'ABSURDLY oversized shoes'],
 'mustard GOLD coat':  ['ONE row of round buttons', 'ONE small ink-blue scarf',
                        'ONE completely BLANK folded newspaper'],
 'grey scarf':         ['ink-blue coat'],
 'silhouettes':        ['brick-red'],
 'headphones':         ['ONE pair of round headphones'],
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
SELFREF_S = re.compile(r'\b(movie|video|episode|documentary|narrat\w+|camera|cameras|viewer|'
                       r'film|films|frame|frames|framed|framing|shot|lens)\b|close on', re.I)
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
if not 3 <= ndata <= 6:
    errs.append(f'{ndata} data frames; this film expects 3-6')

cams = [s[1] for s in live]
c = Counter(cams)
for k, n in MIN_CAM.items():
    if c[k] < n:
        errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
cu = c['CU'] + c['XCU']
if cu / len(live) < MIN_CU_SHARE:
    errs.append(f'close-ups {cu}/{len(live)} ({cu/len(live):.0%}), needs {MIN_CU_SHARE:.0%}')
wide = c['WIDE'] + c['XWIDE']
if wide / len(live) < MIN_WIDE_SHARE:
    errs.append(f'wides {wide}/{len(live)} ({wide/len(live):.0%}), needs {MIN_WIDE_SHARE:.0%} '
                f'— the gap needs room')
run, prev = 1, None
for i, cam in enumerate(cams, 1):
    if cam == prev:
        run += 1
        if run > MAX_RUN:
            errs.append(f'live frame {i}: {run} consecutive {cam}')
    else:
        run, prev = 1, cam

# THE FLAT-RUN GATE v1 — no run of 3+ consecutive rows that are both castless
# (expression '-') AND the same setting.
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
    errs.append('FLAT RUN v1 — 3+ consecutive castless rows in one setting: ' +
                '; '.join(f'row {i} ({env}, run of {r})' for i, env, r in flagged[:6]))

# THE FLAT-RUN GATE v2 — and no cross-setting castless symbol run either. A
# symbol in a void followed by a symbol in the snow is the same fault.
run2, flagged2 = 0, []
for i, s in enumerate(S, 1):
    if s[2] == '-':
        run2 += 1
        if run2 > MAX_CASTLESS_RUN:
            flagged2.append((i, run2))
    else:
        run2 = 0
if flagged2:
    errs.append('FLAT RUN v2 — castless run across settings: ' +
                '; '.join(f'row {i} (run of {r})' for i, r in flagged2[:6]))

# FACE ACTION — declared, and present in the scene text itself. Composed-amid-
# avoidance is an ACTION, never '-'.
noface = [i for i, s in enumerate(S, 1)
          if not isdata[i-1] and s[2] != '-' and not FACE.search(s[2])]
if noface:
    errs.append('expression names no face action: ' + ' '.join('b%03d' % i for i in noface[:10]))
lost = [i for i, s in enumerate(S, 1)
        if not isdata[i-1] and s[2] != '-' and not FACE.search(s[4])]
if lost:
    errs.append('face action absent from the SCENE text: ' + ' '.join('b%03d' % i for i in lost[:10]))

MIN_EVENT_SHARE = 0.85
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

# THE PLATFORM MONUMENT — any platform row staging a coated figure expands the
# FIVE REGULARS in full at point of use. The FINAL row is exempt: the ending
# is the monument breaking — the Stranger leaves her position, and staging the
# other four kept pulling the pair apart in generation (measured, 2 rolls).
badreg = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] == 'platform'
          and 'coat' in s[4] and 'for the first time' not in s[4]
          and any(t not in s[4] for t in REG_REQ)]
if badreg:
    errs.append('platform row staging coats without the FIVE REGULARS expanded: ' +
                ' '.join('b%03d' % i for i in badreg[:8]))

# THE GAP IS THE SUBJECT — the two-figure rooms state their occupants prior.
badtwo = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] in TWOFIG_ENVS
          and 'coat' in s[4] and TWO not in s[4]]
if badtwo:
    errs.append('two-figure room without "exactly TWO figures" at point of use: ' +
                ' '.join('b%03d' % i for i in badtwo[:8]))
ntwo = len([s for s in live if TWO in s[4]])
if ntwo < 14:
    errs.append(f'only {ntwo} frames state "exactly TWO figures"; the gap needs at least 14')

# OMISSION, NOT NEGATION — reject negation describing visual content.
NEG = re.compile(r"\bno\s|\bwithout\b|n't\b|\bnever\b|\bnothing\b", re.I)
neg = [i for i, s in enumerate(S, 1) if not isdata[i-1] and NEG.search(s[4])]
if neg:
    errs.append('negation in scene text: ' + ' '.join('b%03d' % i for i in neg[:10]))

# LABEL-INVITATION — no scene may request written content; every label-shaped
# word from the allowed set states BLANK in its own row; every other document
# type-noun is banned outright (delete the labelled object, never argue).
SIGNS = re.compile(r'\b(letter|letters|lettering|lettered|word|words|writing|written|writes|'
                   r'text|texts|number|numbers|numeral|numerals|digits?|caption|inscrib\w*|'
                   r'font|typeface|says|reading\b|reads\b)\b', re.I)
signy = [i for i, s in enumerate(S, 1) if not isdata[i-1] and SIGNS.search(s[4])]
if signy:
    errs.append('scene requests written content: ' + ' '.join('b%03d' % i for i in signy[:10]))
BLANKREQ = re.compile(r'\b(signs?|signboards?|boards?|ovals?|panels?|cups?|newspapers?|cards?|'
                      r'sheets?|pages?|grids?|plinths?|papers?|dials?|tickets?|banners?|'
                      r'plaques?|screens?)\b', re.I)
unblanked = [i for i, s in enumerate(S, 1) if not isdata[i-1]
             and BLANKREQ.search(s[4]) and 'BLANK' not in s[4]]
if unblanked:
    errs.append('label-shaped object staged with its BLANK missing: ' +
                ' '.join('b%03d' % i for i in unblanked[:10]))
BANNED_NOUNS = re.compile(r'\b(labels?|posters?|contracts?|certificat\w*|documents?|ledgers?|'
                          r'invoices?|nameplates?|charts?|clipboards?|calendars?|timetables?|'
                          r'reports?|receipts?|memos?|folders?|slips?|bills?|lists?|notices?|'
                          r'placards?|leaflets?|magazines?|prospectus\w*)\b', re.I)
typed = [i for i, s in enumerate(S, 1) if not isdata[i-1] and BANNED_NOUNS.search(s[4])]
if typed:
    errs.append('banned document type-noun in scene text: ' +
                ' '.join('b%03d' % i for i in typed[:10]))

# NEVER A DIAGRAM — the avoidance arc is footprints in snow, not drawn lines.
DIAGRAM = re.compile(r'\bdotted\b|\bdiagram\w*|\barrows?\b|\bgraph\b|\bchart\b|dashed line', re.I)
diag = [i for i, s in enumerate(S, 1) if not isdata[i-1] and DIAGRAM.search(s[4])]
if diag:
    errs.append('the geometry became a diagram: ' + ' '.join('b%03d' % i for i in diag[:10]))

# LIKENESS LAW — the narration may carry the study; the pictures never carry a
# person. No comedian, no researcher, no city, ever.
NAMES = re.compile(r'\bLarry\b|\bDavid\b|\bCarr\b|Epley|Schroeder|Milgram|Boothby|Sandstrom|'
                   r'\bDunn\b|Mastroianni|\bGilbert\b|Cooney|\bWilson\b|\bClark\b|Chicago',
                   re.I)
likeness = [i for i, s in enumerate(S, 1) if NAMES.search(s[4]) or NAMES.search(s[2])]
if likeness:
    errs.append('a real surname reached SCENE text: ' + ' '.join('b%03d' % i for i in likeness))

# NEVER SMUG — the avoider is us; his face does dread, calculation, hope.
SMUG = re.compile(r'smug|smirk|\bsly\b|snide|mock\w*|ridicul\w*', re.I)
smug = [i for i, s in enumerate(S, 1) if SMUG.search(s[4]) or SMUG.search(s[2])]
if smug:
    errs.append('smugness reached a row: ' + ' '.join('b%03d' % i for i in smug))

# ENVIRONMENT CAP — platform frames <=22%; every core environment appears.
setc = Counter(s[3] for s in S)
unknown = sorted(set(setc) - CORE_ENVS)
if unknown:
    errs.append(f'unknown environment tags: {unknown}')
plat_n = setc['platform']
if plat_n / len(S) > PLATFORM_MAX_SHARE:
    errs.append(f'platform frames are {plat_n}/{len(S)} ({plat_n/len(S):.0%}), '
                f'max {PLATFORM_MAX_SHARE:.0%}')
unused = sorted(CORE_ENVS - set(setc))
if unused:
    errs.append(f'core environments unused: {unused}')

# NAMED LIGHTING COLOURS — every snow-dusk frame states flat INK BLUE at point
# of use. Never "a darker mix".
unlit = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] in DUSK_ENVS
         and 'INK BLUE' not in s[4]]
if unlit:
    errs.append('dusk frame missing flat INK BLUE at point of use: ' +
                ' '.join('b%03d' % i for i in unlit[:10]))

# THE WARM ACT (37-44) — no geometry gags, no club, no twist; warm plain
# daylight in every coffee-shop row, the one room where the distance closes.
COMIC = re.compile(r'spotlight|silhouett|brick-red|footprints?|empty middle|wide detour|'
                   r'holding perfectly still|the gap between|far apart|exactly TWO figures|'
                   r'undented|step and a half darker', re.I)
bent = [i for i, s in enumerate(S, 1) if s[0] in STRAIGHT_LINES and not isdata[i-1]
        and (COMIC.search(s[4]) or COMIC.search(s[2]))]
if bent:
    errs.append('the warm act broke its straightness: ' + ' '.join('b%03d' % i for i in bent))
unwarm = [i for i, s in enumerate(S, 1) if s[0] in STRAIGHT_LINES and not isdata[i-1]
          and s[3] == 'coffeeshop' and ('warm' not in s[4] or 'daylight' not in s[4])]
if unwarm:
    errs.append('warm-act row missing warm plain daylight: ' +
                ' '.join('b%03d' % i for i in unwarm[:10]))

# CLUB ACCENT — exactly ONE club frame in the whole film, on the twist beat,
# carrying its populated surround (empty black fails — paid theatre lesson)
# and its deep warm brick-red back wall.
club = [i for i, s in enumerate(S, 1) if not isdata[i-1] and 'spotlight' in s[4]]
badclub = [i for i in club if 'silhouettes' not in S[i-1][4] or 'brick-red' not in S[i-1][4]]
if badclub:
    errs.append('club frame with an unpopulated surround or missing brick-red wall: ' +
                ' '.join('b%03d' % i for i in badclub))
if len(club) != CLUB_MAX:
    errs.append(f'{len(club)} club frames; this film rations exactly {CLUB_MAX}')
outside = [i for i in club if S[i-1][0] not in CLUB_LINES]
if outside:
    errs.append('club staging outside the twist beat: ' + ' '.join('b%03d' % i for i in outside))
clubenv = [i for i, s in enumerate(S, 1) if s[3] == 'club']
if len(clubenv) != CLUB_MAX or clubenv != club:
    errs.append(f'club environment tag and club staging disagree: {clubenv} vs {club}')

# TWIST — <=6 tagged lines, each carrying its one quietly wrong detail, and
# every tagged line sitting outside the warm act.
if len(TWIST) > TWIST_MAX:
    errs.append(f'{len(TWIST)} twist lines tagged; cap {TWIST_MAX}')
def _scene_for(line):
    return ' || '.join(s[4] for s in S if s[0] == line)
for line, detail in TWIST.items():
    if detail not in _scene_for(line):
        errs.append(f'twist line {line} missing its wrong detail "{detail}"')
    if line in STRAIGHT_LINES:
        errs.append(f'twist tagged inside the warm act: line {line}')

# INTERACTION QUOTA — the Man and the Familiar Stranger share at least FOUR
# frames, and in every one of them before the last line both are aimed
# elsewhere; the final row stages them two paces apart, both turned, mouths
# CLOSED, the moment before.
AVOID = re.compile(r'straight ahead|turned away|looking away|eyes front', re.I)
shared = [i for i, s in enumerate(S, 1)
          if 'VERMILION RED coat' in s[4] and 'mustard GOLD coat' in s[4]]
if len(shared) < 4:
    errs.append(f'the Man and the Familiar Stranger share {len(shared)} frames; '
                f'the law is at least 4')
unavoided = [i for i in shared if S[i-1][0] != 92 and not AVOID.search(S[i-1][4])]
if unavoided:
    errs.append('a shared frame without the avoidance aim stated: ' +
                ' '.join('b%03d' % i for i in unavoided[:8]))

# THE AVOIDANCE ARC — concrete footprint geometry, at least twice, worded
# identically on every return (a motif described only in words drifts).
prints = [i for i, s in enumerate(S, 1) if 'curved line of single footprints' in s[4]]
if len(prints) < 2:
    errs.append(f'the avoidance arc appears as footprint geometry {len(prints)} times; '
                f'the law is at least 2')
if len({S[i-1][4] for i in prints}) > 1:
    errs.append('the footprint arc is worded differently on its returns: ' +
                ' '.join('b%03d' % i for i in prints))

# THE ENDING — the film stops the moment before, in script order.
ending_checks = [
    (92, 'two paces',    'the final row stages them two paces apart'),
    (92, 'both turned',  'the final row turns them toward each other'),
    (92, 'mouths CLOSED','the final row keeps both mouths CLOSED'),
]
for line, need, msg in ending_checks:
    if need not in _scene_for(line):
        errs.append(f'THE ENDING out of order: {msg}')
mouths = [i for i, s in enumerate(S, 1) if re.search(r'mouths? CLOSED', s[4])]
if len(mouths) < 3:
    errs.append(f'the closed mouth is the film\'s grip and appears in {len(mouths)} rows; '
                f'the law is at least 3')

dead = [s for s in S if s[2] == '-' and s[4] != DATA]
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(live)} ({cu/len(live):.0%}) | wides {wide}/{len(live)} "
      f"({wide/len(live):.0%}) | faces {len([s for s in live if s[2]!='-'])}/{len(live)} | "
      f"events {len(live)-len(noev)}/{len(live)} | data {ndata} | platform {plat_n} "
      f"({plat_n/len(S):.0%}) | club {len(club)} | twist {len(TWIST)} | two-figure {ntwo} | "
      f"shared {len(shared)} | footprints {len(prints)} | castless {len(dead)} | holds "
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
