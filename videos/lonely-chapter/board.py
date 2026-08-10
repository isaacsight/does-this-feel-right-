#!/usr/bin/env python3
"""Frame book — The Lonely Chapter (episode 5). 140 frames: 127 sentences +
13 second frames for every sentence over 25 words.

Every law here was paid for on an earlier film:

  THE CAMERA IS A CROP     CAM names where the frame edge cuts; scene text
                           never says "close on".
  COUNTS, NOT NOUNS        THREE coat buttons, the single lonely PAIR of
                           hairs, TWELVE lodge ranks in TWO facing rows, ONE
                           gavel, ONE mustard collar per man, FIVE league
                           bowlers, TWO chairs ONE cooler, THREE silhouetted
                           figures per warm window — stated in EVERY frame
                           that stages the character. A reference sheet is
                           not sufficient.
  A FACE ACTION PER FRAME  declared in the expression field AND present in
                           the scene text the model actually receives.
  EVENTS, NOT STATES       something happens in every frame; the Man's
                           loneliness is GEOMETRY (thresholds, panes, the
                           vacant chair), never a slumped figure in a void.
  OMISSION, NOT NEGATION   absences are described as present things ("the
                           second cushion smooth and empty", "one lane lit,
                           the neighbouring lanes dark still shapes").
  THE WARM-MAN LAW         in every dusk frame the Man keeps "his red coat
                           and warm face unchanged in the blue evening" —
                           stated at point of use, gated below.
  SIGN-SHAPED OBJECTS      the phone screen is dark, or shows ONE glowing
                           blank rounded rectangle; lodge banners are BLANK
                           cloth; bowling shirts have BLANK backs; the studio
                           photographs are BLANK grey plates; the study's
                           files are matching BLANK folders. No text ever.
  THE STRAIGHT ACT (76-87) Holt-Lunstad + Harvard played entirely straight:
                           study/archive staging, customs calm, and its rows
                           gated against every comic staging word.
  PROCESSION               full pageantry on the 1924 lodge; exactly ONE
                           mirrored-empty modern frame (line 122); theatre
                           accents banned outright.
  TWO-SIDED SILENCE        the two living rooms staged as mirrors at least
                           THREE times; the ending lands in order: press ->
                           the other room lights -> the coffee-table scramble.
  ENVIRONMENT CAP          the living rooms combined <=22% of frames,
                           measured rather than hoped for.

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

MAN = ("THE MAN: a small slight man with a round face and a big confident nose, his head bald "
       "and smooth with bare scalp at the sides, bare above the ears, and at the very top of "
       "his crown a single lonely PAIR of hairs — one thin hair kinking left, one thin hair "
       "leaning right — a flat VERMILION RED coat with THREE round buttons, thin stick legs "
       "and absurdly oversized shoes")
FRIEND = ("THE FRIEND: a big warm man a head taller and heavier than the small man, in a SAGE "
          "GREEN jacket over a mustard waistcoat with ONE flat cap, a broad open face built "
          "for beaming")
# "smartphone on a coffee table" reliably drew a LAPTOP (twice, eye-QC 2026-08-10):
# a dark rectangle plus a table summons the open-hinge prior. The cure is the
# tipping shape-anchor move — describe the SHAPE positively, one flat closed tile.
PHONE = ("THE TELEPHONE: a thin flat hand-sized near-black slab of a phone drawn slightly "
         "too large, one single flat closed shape lying completely FLAT like a small dark "
         "tile, thin as a coaster from every angle, its glass face turned up")
GM = ("THE GRAND MASTER: a large beaming man in a dark suit with ONE mustard GOLD ceremonial "
      "collar and ONE gavel, a gold watch-chain in a shallow arc")
RANKS = ("THE LODGE RANKS: TWELVE men in dark suits, ONE mustard collar per man, completely "
         "BLANK sashes, individuated faces and builds, arranged in TWO facing rows, BLANK "
         "cloth banners overhead, candles lit")
SITTERS = ("TWO PORTRAIT SITTERS: two 19th-century men in dark frock coats and beards, their "
           "faces easy and unremarkable")
RESEARCHER = ("THE RESEARCHER: a woman in an ink-blue cardigan with THREE buttons, ONE "
              "clipboard under her arm, her manner exact and unhurried")
LEAGUE = ("FIVE league bowlers in matching sage shirts with completely BLANK backs, "
          "individuated faces and builds")

# THE WARM-MAN LAW, stated at point of use in every dusk frame with the Man.
WARM = "his red coat and warm face unchanged in the blue evening"

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
# ACT 1 — the couch, the phone, the six-hundred-pound want --------------------
(1,"WIDE","eyes locked on the phone","manliving", f"A dusk living room in flat ink blue with sage wallpaper, seen from slightly ABOVE so the full top of ONE low coffee table is visible, {PHONE} lying flat in the middle of the visible tabletop, and {MAN} on the couch leaning toward it, his eyes locked down on its dark glass, {WARM}."),
(2,"CU","eyes fixed, fingers curling back","manliving", f"{MAN}'s hand rising toward the phone and stopping in mid-air, the fingers curling slowly back, his eyes fixed and his jaw working, {WARM}."),
(3,"MED","brows knotting","manliving", f"{PHONE} FACE UP on the coffee table, its dark screen showing nothing, and {MAN} leaning in over his knees studying it the way a climber studies a cliff, his brows knotting, {WARM}."),
(4,"CU","eyes wanting","void", f"{MAN} curling both hands around one small imagined shape held at his chest, his brows soft and his eyes wanting exactly one small thing."),
(5,"MED","beaming, laughing","void", f"A memory on flat cream: {FRIEND} at a wedding table raising ONE glass high in a toast and beaming, and {MAN} beside him laughing with both hands pressed to his chest, confetti hanging in the air."),
(6,"WIDE","teeth gritting","manliving", f"{MAN} gripping {PHONE} with both hands and hauling upward like a man lifting a boulder, his knees buckling and his teeth gritting, the coffee table tilting under the effort, {WARM}."),
(7,"MED","mid-yawn, eyes easy","void", f"A bright morning corner on flat cream: {MAN} pressing ONE dumbbell overhead with one easy arm, mid-yawn, his eyes easy, his other hand resting flat on ONE stack of TWO larger weights."),
(8,"WIDE","eyes down at the phone","manliving", f"The whole room from across it: {MAN} small at one end of the couch, the second cushion smooth and empty beside him, {PHONE} FACE UP on the table with its dark screen showing nothing, the lamp's circle reaching the couch and stopping, his eyes down at the phone, {WARM}."),
(9,"XCU","-","void", "The near-black smartphone huge on flat cream, FACE UP, its dark screen holding one small warm reflection of a leaning man."),
(10,"XWIDE","-","void", "A long road unrolling backward across an enormous cream plain from ONE small coffee table in the foreground toward a far marble temple with SIX columns, a long low hall with ONE wide doorway, and a small shopfront with ONE big window, every signboard on every building a completely BLANK painted board, tiny figures dotted along the road walking away"),
# ACT 2 — the sentence -------------------------------------------------------
(11,"MED","mouths making the same shape","sidewalk", f"{MAN} and {FRIEND} outside a small restaurant in flat midday light, both mid-sentence with their mouths making the same shape, four hands already drifting up into the same goodbye."),
(12,"CU","chins dipping in time","sidewalk", f"TWO right hands meeting between the two men in a half-shake half-wave, {MAN}'s chin dipping and {FRIEND}'s chin dipping back in time with it."),
(13,"XWIDE","-","sidewalk", "The restaurant parking lot: two men far apart between the parked cars, each raising one hand high, each with one car door already open, the goodbye stretching across the whole lot."),
(14,"MED","nodding warmly, eyes following it down","sidewalk", f"{MAN} and {FRIEND} nodding warmly over ONE small blank datebook page drifting down to the pavement between them, both pairs of eyes following it down."),
(15,"MED","brows rising with every panel","void", f"{MAN} unfolding an enormous blank sheet that keeps unfolding past both arms' reach, more blank panels dropping open at each shake, his brows rising higher with every panel."),
(16,"WIDE","chins solemn, eyes kind","sidewalk", f"{MAN} and {FRIEND} bowing to each other on the sidewalk with diplomatic formality, their chins solemn and their eyes kind, hats lifted an exact inch, TWO abandoned coffee cups on the round table through the window behind them."),
(17,"WIDE","mouth still going, waving","sidewalk", f"{FRIEND} walking backward away down the sidewalk waving with one big arm, his mouth still going, each backward step longer than the last, {MAN} waving back from the restaurant door."),
(18,"XWIDE","-","sidewalk", "The whole street: one tiny figure at a far car door and one tiny figure at the restaurant, one last small wave crossing the whole distance between them, the car door swinging."),
(19,"CU","eyes perfectly sincere","sidewalk", f"{MAN} cropped close at the restaurant door, one hand pressed flat over his chest, his eyes perfectly sincere."),
(20,"CU","eyes dropping","sidewalk", f"The same crop one beat later: {MAN}'s hand sliding off his chest and hanging at his coat seam, the fingers curling shut, his eyes dropping to the pavement."),
# ACT 3 — the numbers --------------------------------------------------------
(21,"XWIDE","-","nightstreet", f"{MAN} small on the night street walking home under flat ink blue, THREE lit mustard windows along the street each holding THREE silhouetted figures mid-laugh, {WARM}."),
(22,"XWIDE","-","void", "THREE small men far apart on an enormous bare cream field, each turning slowly on the spot as if listening for something, three long thin shadows wheeling with them."),
(23,"XCU","-","void", "ONE open palm held out flat and steady on flat cream, bare from wrist to fingertip, the lamp light pooling in it."),
(24,"WIDE","-","data", DATA),
(25,"WIDE","-","data", DATA),
(26,"MED","mid-laugh; eyes forward","void", "TWO park benches on flat cream: on one, THREE women leaning together mid-laugh; on the other, ONE man at the very end with his eyes forward, the long bare stretch of bench beside him painted as carefully as he is."),
(27,"MED","mouth set grave","study", "A uniformed official at a desk in the study of files pressing ONE heavy stamp down beside a stack of matching BLANK folders, his mouth set grave, dust hanging in the long window light."),
(28,"WIDE","one brow up, peering","void", f"A colossal cutaway clockwork filling the frame, ONE gear fallen out and lying at its base, {MAN} peering into the gap where it turned, one brow up."),
(29,"WIDE","eyes sliding sideways","manliving", f"A long rigid trend-line cut from grey card propped on the couch beside {MAN} like a guest, its far end sagging to the carpet, his eyes sliding sideways to it, {PHONE} FACE UP on the table with its dark screen showing nothing, {WARM}."),
# ACT 4 — the missing vocabulary ---------------------------------------------
(30,"XCU","eyes narrowed, peering down","void", "The near-black smartphone drawn huge on flat cream, FACE UP, its dark screen showing nothing, and pressing in from the frame's edge one round warm face with a big confident nose peering down into it with narrowed eyes."),
(31,"MED","mouth practising a shape","void", f"{MAN} rehearsing before ONE tall free-legged mirror on flat cream, one hand extended to his own reflection, his mouth practising a shape and losing it halfway."),
(32,"CU","eyes going wide with horror","void", f"{MAN} cropped close mid-sentence with one hand out, his own eyes going wide with horror at the sentence leaving his mouth."),
(33,"MED","beaming; eyes sliding away mortified","void", f"TWO small boys on flat cream trading ONE juice box between them, both beaming, and beside them {MAN} holding out his own ONE juice box, his eyes sliding away mortified."),
(34,"MED","teeth gripping a rose","void", "A suitor down on ONE knee on flat cream holding up ONE small ring, ONE rose gripped in his teeth, and crouched behind him a prompter holding open a scroll of RULED LINES."),
(35,"MED","mouths set in firm lines","void", "TWO men in dark suits shaking hands across ONE long table, ONE blank contract lying square between them, TWO fountain pens capped and ready, both mouths set in firm professional lines."),
(36,"WIDE","every face tilting up, beaming","void", "ONE man rising at a dinner table with ONE glass held high, the seated guests lifting theirs back to him, every face tilting up and beaming."),
(37,"WIDE","brows knotted, peering","void", f"THREE stone pedestals in a row on flat cream: ONE wedding ring on the first, ONE fountain pen on the second, and the third bare and dusted clean, {MAN} up on tiptoe peering over its empty top, his brows knotted."),
(38,"MED","chins dipping in unison","sidewalk", f"{MAN} and {FRIEND} performing the farewell like a rite: matching half-waves raised, chins dipping in unison, ONE small blank datebook lying shut on the pavement between them."),
(39,"CU","mouth open enormous, eyes straining","void", f"{MAN} cropped close with his mouth open enormous and his eyes straining, and above his lips ONE tiny blank speech balloon the size of a postage stamp."),
# ACT 5 — the photographs ----------------------------------------------------
(40,"MED","-","studio", "The photographer's studio door swinging open in the 1870s, the street wall around the doorway flat painted CREAM with sage trim, warm mustard light and slow dust rolling out over the threshold, ONE brass bell above the door mid-swing."),
(41,"WIDE","-","studio", "A studio wall hung edge to edge with framed BLANK grey plates, dozens in ornate frames, ONE ladder leaning at the wall's end, dust drifting through the window light."),
(42,"XCU","-","studio", "TWO clasped hands filling the picture, one from each dark frock-coat sleeve, held perfectly steady for the long exposure."),
(43,"MED","faces easy, holding still","studio", f"{SITTERS} posed before a painted backdrop, one arm wrapped around the other's shoulder, their faces easy, holding still for the count."),
(44,"MED","chins level, faces settled","studio", f"{SITTERS}, one seated square in the other's lap, both matter-of-fact, chins level, faces settled, four hands folded like a Sunday portrait."),
(45,"WIDE","faces easy, holding the pose","studio", f"The whole transaction in one picture: {SITTERS} holding their lap pose with faces easy, the photographer stooped under ONE dark cloth behind ONE wooden bellows box on a tripod with THREE wooden legs, and ONE coin lying ready on the side table."),
(46,"CU","face mild, nodding once","studio", "The photographer emerging from under the dark cloth with his face mild and unbothered, nodding once, business as usual, ONE plate holder tucked under his arm."),
(47,"MED","face calm and pleased","study", "ONE historian in a cardigan at a long table laid with BLANK grey plates in rows, ONE magnifying glass moving from plate to plate, her face calm and pleased, dust in the window light."),
(48,"MED","-","void", "A parlour corner on flat cream: ONE armchair, ONE potted fern, and hanging level on the wallpaper between them ONE framed BLANK grey plate, as ordinary as the furniture around it, dust settling."),
(49,"MED","both beaming","studio", f"{SITTERS} at the studio door paying: one pressing TWO coins into the photographer's open palm, the other straightening his companion's collar, both beaming."),
(50,"WIDE","-","void", "ONE long cream hall, and receding along it FOUR paired poses of the same two men: seated in a lap nearest, then shaking hands, then trading a small nod, then far off walking apart with backward waves, each pair a step further apart."),
# ACT 6 — the lodge ----------------------------------------------------------
(51,"WIDE","-","lodge1924", "A 1900s Main Street mid-construction: men in cloth caps hauling ONE marble column upright with ropes, scaffolding around a half-built temple facade, every rope taut with shared effort."),
(52,"MED","eyes turning back over his shoulder","manliving", f"{MAN} on his couch at dusk with his eyes turning back over his shoulder, and rising close behind the couch his own great-grandfather — the same small man, identical, wearing ONE mustard GOLD ceremonial collar over the same red coat — {WARM}."),
(53,"WIDE","beaming across at each other","lodge1924", f"The lodge hall in 1924 in full pageantry: {RANKS}, the TWO facing rows beaming across at each other, and at the head {GM} lifting the gavel."),
(54,"WIDE","beaming, arms spreading wide","lodge1924", f"The hall packed to the walls: {RANKS}, hats racked in a long row, and {GM} spreading both arms wide to the room, beaming."),
(55,"CU","eyes steady and satisfied","lodge1924", f"{GM} lowering himself into ONE great carved chair, both hands folding over the gavel on its block, his eyes steady and satisfied."),
(56,"MED","faces solemn and delighted at once","lodge1924", "TWO lodge members trading an elaborate secret handshake in candlelight, ONE mustard collar per man, their faces solemn and delighted at once, regalia glinting, ONE gavel resting on its block behind them."),
(57,"WIDE","every face turned warmly opposite","lodge1924", f"The full ceremony in one picture: {RANKS}, {GM} at the head with the gavel raised, and every face along the TWO facing rows turned warmly to the face opposite."),
(58,"XCU","-","lodge1924", "ONE coin dropping into ONE felt-lined collection tray, a mustard-collared cuff steady beneath it, candlelight catching the coin's edge mid-fall."),
(59,"WIDE","-","lodge1924", "The hall drawn like an engine running to time: members filing through the great door in an even stream, ONE wall clock with a completely BLANK face above them, coats swinging onto hooks in rhythm."),
(60,"XCU","-","lodge1924", "ONE wall calendar of completely BLANK ruled squares in candlelight, one square ringed in mustard, the ring's paint still wet."),
(61,"WIDE","every face beaming","lodge1924", f"{RANKS} raising their glasses in unison toward the BLANK calendar and its one mustard-ringed square, every face along the TWO facing rows beaming."),
# ACT 7 — the fact that breaks him -------------------------------------------
(62,"CU","eyes rising, mouth opening a little","manliving", f"{MAN}'s face as the fact lands: his eyes rising from {PHONE} on the table to the empty air over his shoulder where the collar hung, his mouth opening a little, {WARM}."),
(63,"WIDE","eyes travelling from one to the other","void", f"One cream field split by distance: at the far left the marble temple small and complete, at the far right the near-black smartphone drawn huge and FACE UP with its dark screen showing nothing, and {MAN} between them, his eyes travelling from one to the other."),
(64,"CU","jaw tight, thumb curling back","manliving", f"{MAN}'s thumb hovering over {PHONE}'s dark screen and then curling slowly back into his fist, his jaw tight, {WARM}."),
(65,"XCU","-","void", "ONE small brass balance on flat cream: in one pan ONE goose feather, in the other the near-black smartphone FACE UP with its dark screen showing nothing, the beam slammed all the way down on the phone's side."),
(66,"MED","eyes certain, mouth mid-oath","lodge1924", "The great-grandfather — the same small round-faced man in his flat VERMILION RED coat with THREE round buttons, the single lonely PAIR of hairs on his bald crown — reciting an oath among tall columns with one hand raised, his eyes certain and his mouth mid-oath, candles burning."),
(67,"MED","eyes flat and unsurprised","manliving", f"ONE tiny toy crane with a wrecking ball on the coffee table, its little ball resting against {PHONE}'s edge, and {MAN} watching it with flat unsurprised eyes, {WARM}."),
]
S += [
# ACT 8 — bowling alone ------------------------------------------------------
(68,"WIDE","-","bowling", "A modern bowling alley: one lane lit warm, the neighbouring lanes dark still shapes receding, ONE ball waiting on the return rack, the pin deck bright at the lit lane's end."),
(69,"WIDE","-","data", DATA),
(70,"WIDE","-","data", DATA),
(71,"MED","eyes following the ball","bowling", "ONE bowler mid-roll on the lit lane, his form perfect and his eyes following the ball, and behind him the long row of moulded plastic chairs, each seat holding only its own shadow."),
(72,"WIDE","every face mid-laugh","bowling", f"The late-seventies league in full cry: {LEAGUE} around the ball rack, every face mid-laugh, TWO high-fives crossing at once, pitchers sweating on the scorers' table, the whole alley lit warm."),
(73,"XCU","-","bowling", "TEN pins racked bright and tight at the lane's end, ONE full beer glass sweating on the ledge beside the ball return, condensation sliding."),
(74,"MED","all five faces lighting at once","bowling", f"{LEAGUE} turning together toward the alley door as ONE man walks in late, all five faces lighting at once, TWO hands already rising to wave him over."),
(75,"WIDE","-","bowling", "The modern alley again: one lane lit, the neighbouring lanes dark still shapes, and at the counter ONE long wall of rented shoes in pigeonholes, every pair squared and waiting, the attendant's chair pushed in."),
# ACT 9 — the bill. PLAYED STRAIGHT: study staging, customs calm. ------------
(76,"MED","-","study", "A desk lamp clicking on over a blotter in the study of files, ONE blank slip lying square in the light, ONE empty chair pushed neatly in at the desk, the long shelf of matching BLANK folders running into the dark behind it, the room still and unattended, dust hanging in the lamp light."),
(77,"MED","face calm, counting","study", f"{RESEARCHER} at a long table, stacks of matching BLANK folders rising around her, her hand moving folder to folder in an even count, her face calm."),
(78,"MED","eyes level between them","study", f"TWO matching BLANK folders lying squared side by side on the table, and {RESEARCHER} resting one flat hand on each, her eyes level between them."),
(79,"CU","face measured and exact","study", f"{RESEARCHER} cropped close raising ONE finger, her face measured and exact, the window light flat on the table behind her."),
(80,"MED","face patient, steadying","study", f"{RESEARCHER} pressing both palms down over a stack of loose pages as a draft from the window lifts their corners, her face patient, steadying the stack in place."),
(81,"CU","eyes steady on it","study", f"{RESEARCHER}'s two hands lifting ONE thick folder from the table, the weight of it showing in her wrists, her eyes steady on it."),
(82,"MED","-","study", "TWO matching BLANK folders resting in the two pans of ONE brass balance on the table, the beam holding level, dust drifting through the window light."),
(83,"MED","-","study", "ONE drawer sliding open the full length of the table, matching BLANK folders receding inside it file after file, the drawer's brass pull still swinging."),
(84,"WIDE","-","study", f"The longest shelf in the room, matching BLANK folders wall to wall, ONE wooden ladder against it, {RESEARCHER} high on the ladder drawing down the farthest folder, dust turning in the light."),
(85,"CU","face settled and kind","study", "An older man in a soft cardigan at the study window, hands folded behind him, his face settled and kind, the evening light even on the long shelf beside him."),
(86,"MED","-","manliving", f"The living room quiet at dusk: {PHONE} FACE UP on the coffee table with its dark screen showing nothing, the couch cushion holding the shape of a sitter, the lamp burning steady."),
(87,"XCU","-","manliving", "The near-black smartphone FACE UP, its dark screen holding one small warm reflection of the lamp, steady as a held breath."),
# ACT 10 — the posted price --------------------------------------------------
(88,"MED","brows going up","void", f"{RESEARCHER} wheeling ONE shop till on a cart across flat cream toward {MAN}, whose brows go up as he pats his coat for a wallet."),
(89,"WIDE","-","void", "A shop counter on flat cream stacked with small clocks, every clock face completely BLANK, ONE price board hanging above them, completely BLANK, ONE bell waiting by the till."),
(90,"WIDE","-","data", DATA),
(91,"MED","one brow lifting","void", f"{RESEARCHER} turning ONE stern ledger of RULED LINES over to reveal ONE warm-stained BLANK recipe card tucked inside its cover, one brow lifting."),
(92,"XCU","-","void", "TWO hourglasses side by side mid-pour: mustard-gold sand streaming in one, grey sand in the other, the golden pour catching the light."),
(93,"WIDE","mid-laugh","porch", f"{MAN} and {FRIEND} mid-laugh in TWO chairs on a back porch at dusk, ONE cooler between them, TWO sodas raised, the evening flat ink blue beyond the rail, {WARM}."),
(94,"XCU","-","void", "ONE hourglass filling the picture, its mustard-gold sand streaming down and heaping like treasure, grains catching the light as they fall."),
(95,"MED","mid-laugh above the gears","porch", f"A cutaway beneath the porch boards revealing warm clockwork gears turning under TWO chairs and ONE cooler, {MAN} and {FRIEND} above them mid-laugh, sodas tilting, {WARM}."),
(96,"MED","doubled over laughing","lodge1924", "In a corner of the lodge hall, TWO members doubled over laughing at something between them while the ceremony proceeds down the hall, candlelight warm on both, ONE mustard collar per man."),
(97,"CU","grinning past it at each other","lodge1924", "ONE mustard fez upturned on a table like an emptied carton, tissue paper spilling out of it, and TWO members grinning past it at each other, collars askew."),
(98,"MED","squaring the page, eyes pleased","lodge1924", "A year of BLANK calendar pages pinned across the lodge wall, one column of squares ringed in mustard down every page, TWO members squaring the newest page level, their eyes pleased."),
(99,"WIDE","-","void", "The marble temple facade on flat cream with its great door standing wide open, plain daylight reaching all the way through to the back wall, the steps swept clean."),
(100,"MED","-","void", "ONE coupon book of completely BLANK stubs lying open, ONE stub freshly torn and lying beside THREE coins, a mustard-collared cuff resting at the page's edge."),
(101,"XCU","-","void", "TWO valentine hearts drawn identical side by side on flat cream, ONE wooden ruler laid beneath them measuring them level."),
(102,"XCU","-","void", "TWO calendar pages side by side: the left page ringed in mustard again and again, square after square, the right page bare from edge to edge, ONE pencil resting between them."),
# ACT 11 — the mirror --------------------------------------------------------
(103,"WIDE","eyes down at the phone","manliving", f"The man's living room seen from outside through its window pane at dusk, {MAN} small inside at the couch with his eyes down at the phone, the sage wallpaper warm behind him, the ink-blue evening filling the street side of the glass, {WARM}."),
(104,"WIDE","-","friendliving", "Across town, a second living room the twin of the first with dusty orange wallpaper: another couch, another lamp, another near-black smartphone lying FACE UP on another coffee table, its dark screen showing nothing, the second cushion smooth and empty."),
(105,"MED","broad face drawn with wanting","friendliving", f"{FRIEND} leaning low over his coffee table, both big hands planted, his broad face drawn with wanting, the near-black smartphone FACE UP between his hands with its dark screen showing nothing."),
(106,"CU","eyes wanting the same one thing","friendliving", f"{FRIEND}'s big hand hovering over the phone and curling slowly back — the same gesture at the same height as the small man's across town — his eyes wanting the same one thing."),
(107,"MED","eyes circling with him","friendliving", f"{FRIEND} pacing a worn oval into the rug around his coffee table, turning his cap in his hands, his eyes circling with him, the phone FACE UP at the oval's centre with its dark screen showing nothing."),
(108,"WIDE","both leaning, eyes down","mirror", f"TWO living rooms in one picture, wall to wall, mirrored: sage wallpaper left, dusty orange right, {MAN} leaning at his phone in one with his eyes down and {FRIEND} leaning at his in the other with his eyes down, the compositions folded across the centre line, {WARM}."),
(109,"MED","both pairs of eyes returning to the phones","mirror", f"The two rooms again: in one {MAN} plumping the second cushion smooth and empty, in the other {FRIEND} straightening a lampshade that is already straight, both pairs of eyes returning to the phones, {WARM}."),
(110,"XWIDE","-","void", "A long road across flat cream between two small houses at its far ends, ONE moving van midway along it, and on the horizon the temple with ONE chain across its door and a bowling alley with one dark BLANK sign."),
(111,"WIDE","eyes down above the gears","mirror", f"The two living rooms side by side, and beneath both floors one shared cutaway of grey clockwork running under the road between them, gears turning slow, {MAN} and {FRIEND} each leaning at his own phone above with his eyes down, {WARM}."),
# ACT 12 — the call ----------------------------------------------------------
(112,"MED","eyes clearing","manliving", f"{MAN} lifting the phone off the coffee table in ONE hand, light as a playing card now, his eyes clearing, the lamp steady, {WARM}."),
(113,"CU","jaw setting and letting go","manliving", f"{MAN}'s ONE thumb pressing down on the screen, which lights with ONE glowing blank rounded rectangle, the warm glow catching his chin, his jaw setting and then letting go, {WARM}."),
(114,"MED","-","manliving", f"{MAN} from behind, the single lonely PAIR of hairs on his bald crown against the lamplight, the glowing phone at his ear, his face turned away toward the window and the blue evening, {WARM}."),
(115,"WIDE","eyes blazing joy","friendliving", f"The other living room as its dark screen suddenly lights with ONE glowing blank rounded rectangle, and {FRIEND} already mid-leap across the room, his eyes blazing joy, his cap flying off, his shin clipping the coffee table's corner, TWO coasters spinning off the edge."),
(116,"MED","broad face breaking into a beam","friendliving", f"{FRIEND} pressing the lit phone to his ear with both big hands, his broad face breaking open into a beam, the lamp light warm on the dusty orange wallpaper."),
(117,"XWIDE","-","nightstreet", "The whole night street under flat ink blue: window after window down both sides, and in each one ONE small figure leaning at a sill where ONE tiny warm glow waits FACE UP, a street of held breaths."),
(118,"XCU","-","void", "ONE glowing blank rounded rectangle pulsing steady and open on a dark field, its light spreading in soft rings."),
(119,"MED","both mouths mid-sentence","mirror", f"The two living rooms one last time, both phones lit with ONE glowing blank rounded rectangle each, {MAN} at his ear in one room and {FRIEND} at his ear in the other, both mouths mid-sentence, {WARM}."),
(120,"MED","mouth going, finger tapping the air","manliving", f"{MAN} at his window with the lit phone at his ear, his mouth going, one finger tapping three small points in the air as if pinning a day, a place and an hour to it, {WARM}."),
(121,"WIDE","-","porch", "The back porch readied at dusk: TWO lawn chairs squared to each other, TWO sodas sweating on the lid of ONE cooler, and above the garage door ONE round clock with a completely BLANK face, its hands just past the top."),
(122,"WIDE","-","lodgetoday", "The same lodge hall today drawn in the same ceremonial composition: the long floor bare and polished, stacked chairs where the TWO facing rows formed, ONE folding table where the great chair sat, the tall windows lighting an event-venue emptiness."),
(123,"MED","-","void", "Laid along ONE long table: ONE folded robe, ONE rolled scroll of BLANK parchment, and ONE mustard fez set gently at the row's end, a soft dust sheet drawing over all three."),
(124,"WIDE","both faces mid-laugh","porch", f"{MAN} and {FRIEND} arrived in the TWO chairs at dusk, sodas raised toward each other over ONE cooler, both faces mid-laugh, the ink-blue evening deep beyond the porch rail, {WARM}."),
(125,"XCU","-","porch", "ONE soda cap popping off a bottle balanced on ONE cooler's lid, fizz rising in a small bright column, TWO chair legs at the frame's edge."),
(126,"CU","eyes creased mid-laugh","porch", f"{MAN} and {FRIEND} clinking sodas over ONE cooler, both pairs of eyes creased mid-laugh, the TWO chairs pulled close, {WARM}."),
(127,"XCU","-","void", "ONE wall calendar of completely BLANK ruled squares, and ONE small hand drawing a fresh vermilion ring around one square, the pen just lifting."),
]

# ============================================================================
# SECOND FRAMES — every sentence over 25 words carries two pictures so the
# hold stays under ~9.6s at 158wpm. map-shots.py splits the sentence's span
# evenly across the frames beneath it.
# ============================================================================
EXTRA = {
 41: [("MED","face hidden, one hand raised for stillness","studio", "The photographer stooped under ONE dark cloth behind ONE wooden bellows box on a tripod with THREE wooden legs, his face hidden and one hand raised for stillness, dust hanging in the warm light.")],
 50: [("XCU","-","void", "TWO right hands meeting in one brisk dry handshake, both cuffs buttoned to the wrist, daylight flat and correct around them.")],
 51: [("MED","jaws set with the same care","lodge1924", "TWO masons setting ONE keystone together at the top of the temple arch, four hands overlapping on the stone, their jaws set with the same care.")],
 53: [("XWIDE","-","lodge1924", "The marble temple at dusk from the street, every tall window glowing flat mustard with THREE silhouetted figures mid-laugh in each lit window, a queue of members climbing the steps two by two.")],
 54: [("MED","mouth firm, pressing the seal","lodge1924", "ONE membership ledger of RULED LINES lying open on a lectern, ONE clerk pressing a seal down onto the page with his mouth firm, a queue of joining men curling away behind him toward the door.")],
 59: [("MED","mouths mid-greeting","lodge1924", "TWO members meeting on the temple steps and pointing happily up at the BLANK-faced clock over the door, both mouths mid-greeting, neither man slowing his climb.")],
 63: [("MED","-","void", "Laid out on ONE long table: ONE mustard GOLD ceremonial collar, ONE rolled title scroll of BLANK parchment, and ONE calendar page of BLANK squares with one square ringed in mustard — an inheritance in three objects.")],
 77: [("WIDE","face calm, reaching","study", f"The study's long shelf of matching BLANK folders running the room's whole length, dust hanging in the window light, {RESEARCHER} small at the far end reaching up to draw down ONE folder, her face calm.")],
 84: [("MED","-","study", "ONE folder lying open flat on the table, and resting on its pages ONE stethoscope coiled into a neat circle, the window light lying across both.")],
 90: [("MED","eyes checking each against the next","void", f"{RESEARCHER} setting out THREE hourglasses in rising sizes on a shop counter, smallest to largest, her eyes checking each against the next.")],
 111:[("XCU","-","void", "ONE great grey gear filling the picture, turning slow between two painted house foundations, its teeth worn round with years.")],
 115:[("CU","eyes enormous with hurry","friendliving", f"{FRIEND}'s big hand closing around the lit phone as the coffee table rocks, ONE coaster still spinning on its rim beside the glowing blank rounded rectangle, his eyes enormous with hurry.")],
 117:[("MED","eyes down the blue street","nightstreet", "ONE window up close: a man leaning at his sill, his phone FACE UP on the wood with its dark screen showing nothing, his eyes down the blue street toward the corner.")],
}

_S = []
for row in S:
    _S.append(row)
    for cam, expr, setting, scene in EXTRA.get(row[0], []):
        _S.append((row[0], cam, expr, setting, scene))
S = _S

WORLD = (
 "a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom of the "
 "late 1950s: flat gouache-painted backgrounds and flat painted cel figures with confident "
 "tapering ink outlines and no interior shading, in a warm graphic palette of INK BLUE, "
 "mustard GOLD, sage GREEN, dusty ORANGE, cream and flat VERMILION RED, each scene keying its "
 "own dominant colour from that set. Warm fields are flat MUSTARD GOLD and cool fields are "
 "flat INK BLUE, both flat matte gouache. Expressions are BOLD, exaggerated and readable at a "
 "glance. Visible gouache texture, flat matte, NO gradients, NO airbrushed shading, NO "
 "photographic texture, NO three-dimensional rendering. There is NO text, NO lettering, NO "
 "numbers and NO writing of any kind anywhere in the image; any sign, board, placard, label, "
 "badge, sash, page, banner or screen is completely BLANK. Any crowd is individuated: "
 "different faces, different builds, clothes in DIFFERENT colours from the palette, never a "
 "row of matching coats. These are ORIGINAL characters in a general mid-century cartoon "
 "idiom: NO existing cartoon characters, NO studio logos, NO trade dress, and no likeness of "
 "any real person. ONE SINGLE COHERENT SCENE, NOT a grid of panels, NOT a sheet of studies. "
 "16:9, edge to edge, one scene, one camera.")

WPM = 158
MAX_HOLD = 9.6
MIN_CAM = {'XCU': 10, 'CU': 12, 'XWIDE': 8}
MAX_RUN = 3
MIN_CU_SHARE = 0.20
MIN_EVENT_SHARE = 0.85
LIVING_MAX_SHARE = 0.22
LIVING_ENVS = {'manliving', 'friendliving', 'mirror'}
DUSK_ENVS = {'manliving', 'friendliving', 'mirror', 'nightstreet', 'porch'}
CORE_ENVS = {'manliving','friendliving','sidewalk','lodge1924','lodgetoday','studio',
             'bowling','porch','study','nightstreet','void','data'}
STRAIGHT_LINES = range(76, 88)   # Holt-Lunstad + Harvard, played straight

FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|cheeks|'
                  r'tongue|chin|frown|blank|soft|hard\b|calm|composed|weary|star(e|ing)|blush|'
                  r'surprise|nod|dread|faces?\b|wanting|patient|measured|settled|kind\b|'
                  r'pleased|mortified|sincere|joy\b|counting|steadying|grave', re.I)
EVENT = re.compile(
    r'burst|pop|fly|flar|blast|shoot|erupt|stream|pour|collaps|toppl|crack|snap|spring|slam|'
    r'throw|thrown|swing|scatter|shov|carr|drop|slid|tipping|vibrat|lift|roll|hover|dart|glow|'
    r'steam|smoke|nod|shak|crouch|lean|reach|step|walk|run|hold|haul|pull|peer|point|count|'
    r'trudg|wrap|bang|settl|duck|turn|rub|sip|thump|spray|strik|rais|crush|crane|hang|stretch|'
    r'tilt|wav|file|squeez|press|balanc|climb|land|swarm|feed|trac|receiv|arriv|load|cross|'
    r'tumbl|pil|recoil|glanc|hurry|bend|bent|crowd|tear|driv|scribbl|measur|argu|greet|wait|'
    r'watch|look|open|shut|reced|dwarf|clutch|slip|fork|appear|swivel|rotat|freez|curl|march|'
    r'thud|bow|sweep|stoop|practis|welcom|fold|jump|rest|loom|dangl|buckl|puff|retir|pose|'
    r'smooth|shutter|travel|drift|tuck|unroll|brush|confid|nail|study|fray|shrink|brighten|'
    r'flood|offer|spill|meet|wish|spread|ring|split|huddl|thrust|catch|pass|grip|multipl|'
    r'perform|plant|rise|rising|casc|flick|aim|stagger|clip|steady|repeat|pace|pacing|plump|'
    r'clink|pin|tap|wheel|light|lit\b|beam|rehears|unfold|trad|dip|record|recit|square|'
    r'straighten|leap|rock|spin|pat|draw|circling|heap', re.I)
CAST = re.compile(r'THE MAN|THE FRIEND|LODGE RANKS|GRAND MASTER|PORTRAIT SITTERS|RESEARCHER|'
                  r'league bowlers|man\b|men\b|woman|women|people|crowd|guest|servant|'
                  r'clerk|official|historian|photographer|bowler|member|mason|suitor|prompter|'
                  r'child|boys?\b|figures?|sitter|great-grandfather', re.I)

# COUNTS, NOT NOUNS — a scene that stages a character must carry the numeric
# words. A reference sheet is not sufficient.
REQ = {
 'VERMILION RED coat':   ['THREE round buttons', 'PAIR of hairs'],
 'THE FRIEND':           ['ONE flat cap', 'mustard waistcoat'],
 'GRAND MASTER':         ['ONE mustard GOLD ceremonial collar', 'ONE gavel'],
 'LODGE RANKS':          ['TWELVE', 'TWO facing rows'],
 'PORTRAIT SITTERS':     ['faces easy'],
 'THE RESEARCHER':       ['THREE buttons', 'ONE clipboard'],
 'league bowlers':       ['FIVE', 'BLANK backs'],
}

sents = [s.strip() for s in re.split(r'[.!?]+', (FILM / 'script.txt').read_text()) if s.strip()]

errs = []

# NEVER NAME THE ARTEFACT — in narration or in scene text.
SELFREF = re.compile(r'\b(film|movie|video|episode|documentary|this programme|narrat\w+|'
                     r'camera crew|voice-?over)\b', re.I)
hits = [(n, s) for n, s in enumerate(sents, 1) if SELFREF.search(s)]
if hits:
    errs.append('narration names the artefact: ' +
                '; '.join(f'line {n}: "{s[:60]}"' for n, s in hits[:4]))
scam = [i for i, s in enumerate(S, 1)
        if SELFREF.search(s[4]) or re.search(r'\bcamera\b|\bviewer\b|close on', s[4], re.I)]
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
if not 3 <= ndata <= 5:
    errs.append(f'{ndata} data frames; the pipeline expects 3-5')

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

# SIGN-SHAPED OBJECTS — no scene may request written content, and any staged
# screen is either dark or ONE glowing blank rounded rectangle.
SIGNS = re.compile(r'\b(letter|letters|lettering|lettered|word|words|writing|written|writes|'
                   r'text|texts|number|numbers|numeral|numerals|digits?|caption|inscrib\w*|'
                   r'font|typeface|says|reading\b|reads\b)\b', re.I)
signy = [i for i, s in enumerate(S, 1) if not isdata[i-1] and SIGNS.search(s[4])]
if signy:
    errs.append('scene requests written content: ' + ' '.join('b%03d' % i for i in signy[:10]))
badscreen = [i for i, s in enumerate(S, 1) if not isdata[i-1]
             and re.search(r'\bscreen\b', s[4], re.I)
             and 'dark screen' not in s[4] and 'glowing blank rounded rectangle' not in s[4]]
if badscreen:
    errs.append('screen staged neither dark nor as ONE glowing blank rounded rectangle: ' +
                ' '.join('b%03d' % i for i in badscreen[:8]))

# THE WARM-MAN LAW — every dusk frame with the Man carries the warmth clause.
coldman = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] in DUSK_ENVS
           and 'VERMILION RED coat' in s[4] and 'warm face unchanged' not in s[4]]
if coldman:
    errs.append('dusk frame stages the Man with the warmth clause missing: ' +
                ' '.join('b%03d' % i for i in coldman[:10]))

# ENVIRONMENT CAP — the living rooms stay under 22% combined; every core
# environment appears.
setc = Counter(s[3] for s in S)
living = sum(setc[e] for e in LIVING_ENVS)
if living / len(S) > LIVING_MAX_SHARE:
    errs.append(f'living rooms are {living}/{len(S)} ({living/len(S):.0%}), '
                f'max {LIVING_MAX_SHARE:.0%}')
unused = sorted(CORE_ENVS - set(setc))
if unused:
    errs.append(f'core environments unused: {unused}')

# PROCESSION — exactly ONE mirrored-empty modern lodge frame, and theatre
# accents banned outright (spotlights and shafts stopped landing on tipping).
if setc['lodgetoday'] != 1:
    errs.append(f'{setc["lodgetoday"]} mirrored-empty modern lodge frames; the law is exactly 1')
theatre = [i for i, s in enumerate(S, 1)
           if re.search(r'spotlight|black surround|soft-edged column|\bshaft\b', s[4], re.I)]
if theatre:
    errs.append('theatre-style accent staged: ' + ' '.join('b%03d' % i for i in theatre))

# THE STRAIGHT ACT (76-87) — Holt-Lunstad + Harvard reject comic staging.
STRAIGHT = re.compile(r'shaft|spotlight|jury|juror|grin|comic|ABSURD|COLOSSAL|ENORMOUS|'
                      r'cartoon|gag\b|wink|bulging', re.I)
bent = [i for i, s in enumerate(S, 1) if s[0] in STRAIGHT_LINES and not isdata[i-1]
        and (STRAIGHT.search(s[4]) or STRAIGHT.search(s[2]))]
if bent:
    errs.append('the straight act broke its straightness: ' + ' '.join('b%03d' % i for i in bent))

# TWO-SIDED SILENCE — the two rooms staged as mirrors at least THREE times,
# and the ending lands in order: press -> other room lights -> scramble.
nmirror = setc['mirror']
if nmirror < 3:
    errs.append(f'{nmirror} mirror frames; the two living rooms pair up at least 3 times')

# The porch carries its own counts: TWO chairs, ONE cooler.
badporch = [i for i, s in enumerate(S, 1) if s[3] == 'porch'
            and ('ONE cooler' not in s[4] or 'TWO' not in s[4])]
if badporch:
    errs.append('porch staged with TWO chairs / ONE cooler missing: ' +
                ' '.join('b%03d' % i for i in badporch))

# Every warm window is membership: THREE silhouetted figures minimum.
badwin = [i for i, s in enumerate(S, 1) if 'silhouett' in s[4].lower()
          and 'THREE silhouetted figures' not in s[4]]
if badwin:
    errs.append('warm window staged with its THREE-figure count missing: ' +
                ' '.join('b%03d' % i for i in badwin))

dusk = [s for s in live if s[3] in DUSK_ENVS]
cast = [s for s in live if CAST.search(s[4])]
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(live)} ({cu/len(live):.0%}) | faces "
      f"{len([s for s in live if s[2]!='-'])}/{len(live)} | events "
      f"{len(live)-len(noev)}/{len(live)} | cast {len(cast)}/{len(live)} "
      f"({len(cast)/len(live):.0%}) | data {ndata} | dusk {len(dusk)} | "
      f"mirrors {nmirror} | holds {sum(holds):.0f}s/{budget:.0f}s")
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
      'hold_est_s': round((len(sents[s[0]-1].split()) / WPM * 60) / per_line[s[0]], 2)}
     for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S) if s[4] == DATA or not (
    'VERMILION RED coat' in s[4] or 'THE FRIEND' in s[4] or 'LODGE RANKS' in s[4] or
    'GRAND MASTER' in s[4] or 'PORTRAIT SITTERS' in s[4] or 'THE RESEARCHER' in s[4] or
    'league bowlers' in s[4])]
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
