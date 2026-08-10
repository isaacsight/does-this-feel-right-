#!/usr/bin/env python3
"""Frame book — Selling Immortality (episode 6). 143 frames: 127 sentences +
16 second frames for every sentence over 25 words.

Every law here was paid for on an earlier film:

  THE CAMERA IS A CROP     CAM names where the frame edge cuts; scene text
                           never says "close on".
  COUNTS, NOT NOUNS        THREE coat buttons, the single lonely PAIR of
                           hairs, ONE row of warm round bulbs, ONE amber
                           vial, TWELVE bearded physicians, THREE rich
                           ticket-holding old men, ONE small monkey, FOUR
                           recliners, SIX executives — stated in EVERY frame
                           that stages the character. A reference sheet is
                           not sufficient.
  A FACE ACTION PER FRAME  declared in the expression field AND present in
                           the scene text the model actually receives.
  EVENTS, NOT STATES       something happens in every frame.
  OMISSION, NOT NEGATION   absences described as present things ("the
                           counter shelf bare, the shutter drawn down").
  THE VIAL LAW             the product is "softly glowing warm AMBER", the
                           same phrase every era — vial, tonic, IV bag,
                           ornament, pill. The glow is painted flat.
  MIDWAY LIGHT             every night-street frame states "flat MUSTARD
                           GOLD" booth light and "flat INK BLUE" evening at
                           point of use; never "warm light" alone.
  THE WARM-MAN LAW         the Man keeps "his red coat and warm face
                           unchanged in the blue evening" in every evening
                           frame, stated at point of use, gated below.
  SIGN-SHAPE LAW           labels, posters, tickets, contracts, certificates,
                           ledgers, the FDA page — every one "completely
                           BLANK" in its own row. The apothecary probe leaked
                           lettering; this film is MADE of label shapes.
  LIKENESS LAW             the 1889 lecturer, the 1925 surgeon, the 1930
                           believer, the modern protocol-keeper are period
                           TYPES. The narration names names; the pictures
                           never do — the surnames are gated out of scenes.
  THE STRAIGHT ACT (45-57) the Byers act: pharmacy staging, composed faces,
                           the Pullman gravity. Its rows gated against comic
                           vocabulary AND against booth/barker/bulb words.
  ACCENTS                  PROSPECTUS (elevated camera, blank sealed papers)
                           on the boardroom act and the FDA beat only;
                           APOTHECARY (bottle-wall symmetry, light through
                           the amber) on product/authority frames; capped.
  THE TURN                 the Man facing AWAY from the booth toward the
                           queue drawn as every era at once, ONE blank
                           ticket per hand; the last frames land in order.
  ENVIRONMENT CAP          booth/queue night-street frames <=30% combined,
                           measured rather than hoped for.

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
BARKER = ("THE BARKER: a tall smiling man with a thin mustache in a dusty ORANGE coat and ONE "
          "straw boater, one arm PRESENTING with the palm turned up, warm and delighted and "
          "certain")
# The monument's NAME leaked onto its signboard as lettering (calibration
# 2026-08-10, twice — the second roll passed under the glyph floor). A capital
# name in scene text is a signage invitation: the prompt now carries no name
# and blanks the signboard at point of use.
BOOTH = ("one small wooden market stall with ONE row of warm round bulbs painted as "
         "flat MUSTARD GOLD discs along its top edge, ONE counter shelf, and ONE "
         "completely BLANK wooden signboard above the counter")
VIAL = "ONE small glass vial of softly glowing warm AMBER"
TICKET = "ONE completely BLANK ticket"
NIGHT = "the booth glowing flat MUSTARD GOLD and the street in flat INK BLUE evening"
WARM = "his red coat and warm face unchanged in the blue evening"

PHYSICIANS = ("TWELVE bearded physicians in dark frock coats, individuated faces and builds, "
              "seated in curved rows")
LECTURER = ("ONE bearded lecturer in a dark frock coat at the lectern, a period type with "
            "broad generic features, holding ONE glass syringe")
HOLDERS = ("THREE rich ticket-holding old men in dark suits with canes, each holding ONE "
           "completely BLANK ticket")
SURGEON = "ONE proud surgeon in a white coat, a period type with broad generic features"
MONKEY = "ONE small monkey"
BELIEVER = "one composed period man in a dark suit, his face steady and dignified"
EXECS = "SIX suited executives in ink blue around ONE long table"
ORNAMENT = "ONE molecule-shaped glass ornament holding softly glowing warm AMBER"
KEEPER = "ONE trim man in plain grey, a modern type with calm generic features"
MOUSE = "ONE white mouse in ONE clear cage"

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
# ACT 1 — the booth, the queue, the want --------------------------------------
(1,"WIDE","-","nightstreet", f"{BOOTH} standing at the head of a night street, {NIGHT}, the strung bulbs hanging like a lit window full of company, the queue's long shadows reaching toward the glow."),
(2,"MED","eyes down at the ticket, fingers tight","nightstreet", f"{MAN} near the front of the queue holding {TICKET} with both hands the way a nervous man holds things, his eyes down at it and his fingers tight, {NIGHT}, {WARM}."),
(3,"MED","faces calm, eyes forward","nightstreet", f"The queue at eye level from within it: SIX queueing figures individuated in different palette coats, faces calm and eyes forward toward the glow, {NIGHT}."),
(4,"CU","eyes wanting one small thing","void", f"{MAN} on flat cream curling both hands around one small imagined shape held at his chest, his brows soft, his eyes wanting exactly one small thing."),
(5,"CU","brows soft, chin lifting","void", f"{MAN} cropped close pressing one open hand flat over his chest, his brows soft and his chin lifting, flat cream behind."),
(6,"XWIDE","-","nightstreet", f"A long cold street receding across the whole frame, and the small booth standing bright at the queue's head, {NIGHT}, tiny queueing figures dotted along the block toward it."),
(7,"XCU","-","nightstreet", "The booth's wooden corner post filling the picture, layer upon layer of old paint showing at a chipped edge like tree rings, ONE warm round bulb painted as a flat MUSTARD GOLD disc hanging above, the street behind in flat INK BLUE evening."),
(8,"MED","beaming, arm sweeping the brush","nightstreet", f"{BARKER} sweeping ONE wide brush of fresh paint across the booth's front panel, beaming, ONE paint pot hooked on his free arm, {NIGHT}."),
(9,"MED","eyes narrowing with recognition","nightstreet", f"{MAN} stopped mid-street and turning toward the booth, his eyes narrowing with recognition, {NIGHT}, {WARM}."),
(10,"WIDE","both faces lit warm across the counter","nightstreet", f"The transaction staged square: {MAN} at the counter shelf and {BARKER} behind it leaning toward him, both faces lit warm across the counter, {VIAL} resting between them on the shelf, {NIGHT}, {WARM}."),
(11,"MED","jaw set, eyes up on the salesman","nightstreet", f"{MAN} pushing ONE fat coin purse across the counter shelf with both hands, his jaw set and his eyes up on {BARKER}, whose palm is already turning up, {NIGHT}, {WARM}."),
(12,"MED","beaming; eyes going wide","nightstreet", f"{BARKER} presenting {VIAL} across the counter with his palm up, beaming, and {MAN} receiving it with both hands, his eyes going wide at the warm glow, {NIGHT}, {WARM}."),
(13,"WIDE","-","void", f"FIVE small wooden stalls in a row on flat cream, each dressed differently — bunting, clinic white, pharmacy shelving, glass panels, spa panels — and on each counter shelf {VIAL} resting, the same amber five times."),
(14,"CU","eyes steady, chin lifting","nightstreet", f"{MAN} at the front of the queue turning his head slowly, his eyes steady and his chin lifting, {TICKET} held flat to his chest, {NIGHT}, {WARM}."),
# ACT 2 — Paris, 1889 ---------------------------------------------------------
(15,"XWIDE","-","lecture1889", "A gaslit Paris boulevard in flat evening, ONE grand stone institute with tall lit windows, a row of gas lamps glowing down the block, TWO carriages waiting at the steps."),
(16,"WIDE","every bearded face serious and forward","lecture1889", f"The gaslit lecture hall: {PHYSICIANS}, every bearded face serious and forward, gaslight sconces flickering along the walls."),
(17,"MED","mouth open wide with conviction","lecture1889", f"{LECTURER} mid-declaration, one fist pressed to his own chest and the syringe lifted high in the other hand, his mouth open wide with conviction, gaslight warm on the polished wood."),
(18,"CU","eyes shining with certainty, chest swelling","lecture1889", f"{LECTURER} cropped at the chest, his eyes shining with certainty and his chest swelling, the syringe held up like a torch."),
(19,"XCU","-","lecture1889", "ONE gloved hand holding ONE glass syringe filling the picture, a single bead of liquid at its tip catching the gaslight."),
(20,"CU","mid-flex, beaming","lecture1889", f"{LECTURER} flexing one arm inside his frock-coat sleeve and beaming down at it, the lectern's edge below."),
(21,"XCU","-","void", "ONE hand against flat cream holding up ONE single finger, the cuff buttoned, the finger lit like a small monument."),
(22,"WIDE","-","data", DATA),
(23,"MED","face grave over the bare page","void", "ONE ledger of completely BLANK ruled pages lying open and untouched on a desk seen from slightly ABOVE, ONE capped pen resting beside it, ONE clerk's face grave over the bare page."),
(24,"WIDE","faces eager at the counter","apothecary", "A Paris apothecary in frontal shop-portrait symmetry: a wall of identical small bottles in neat ranks with every label a completely BLANK paper rectangle, polished wood and brass, a press of customers leaning to the counter with individuated eager faces, and ONE small glass vial of softly glowing warm AMBER on the counter, its light passing through onto the nearest faces."),
(25,"WIDE","-","void", "A race staged on flat cream: ONE laden merchant's cart rolling fast in the lead, and far behind it ONE clerk on foot carrying a tall stack of completely BLANK papers, the gap between them widening."),
(26,"CU","eyes warm through the glass","apothecary", f"ONE apothecary in an apron holding {VIAL} up before a lamp, the amber light passing through it onto his lit face, his eyes warm through the glass."),
(27,"XCU","-","apothecary", f"{VIAL} upended over ONE white saucer, a single thin clear drop falling, the saucer bare and clean beneath it."),
(28,"MED","faces hopeful, hands to chests","void", "FOUR patients seated in a parlour row on flat cream, individuated faces hopeful, each pressing one hand to the chest, and on the side table ONE small glass vial of softly glowing warm AMBER, its glow reaching their faces."),
(29,"WIDE","faces reasonable and kind","lecture1889", f"{PHYSICIANS} rising in an orderly line, each receiving ONE small glass vial of softly glowing warm AMBER from a passed tray, faces reasonable and kind, gaslight even across the hall."),
(30,"XCU","-","void", "ONE tiny pebble lodged under the corner of ONE great marble column on flat cream, the column's whole weight leaning on it."),
(31,"WIDE","-","nightstreet", f"{BOOTH} unchanged on the night street, {NIGHT}, the painted discs warm as ever, the queue reformed and patient below."),
# ACT 3 — the 1920s -----------------------------------------------------------
(32,"MED","beaming over the brush","nightstreet", f"{BARKER} rolling clean clinic white over the booth's old panel, beaming over the brush, ONE paint pot at his feet, {NIGHT}."),
(33,"WIDE","faces expecting good service","nightstreet", f"The queue now {HOLDERS}, watch chains and monocles, faces expecting good service, and among them {MAN} holding {TICKET}, {NIGHT}, {WARM}."),
(34,"MED","nose up, mouth prim","void", "ONE rich old man at a white-clothed table pushing ONE soup bowl back to arm's length, his chin up and his mouth prim, ONE waiter's hands already receiving the bowl."),
(35,"WIDE","faces patient","clinic1925", f"A white-tiled clinic hall: {HOLDERS} seated in a patient row beneath ONE window with ONE palm tree outside, faces patient, and {SURGEON} consulting ONE clipboard with a completely BLANK sheet."),
(36,"CU","chin high with pride","clinic1925", f"{SURGEON} snapping ONE rubber glove at the wrist, chin high with pride, white tile gleaming behind him."),
(37,"MED","-","clinic1925", f"The clinic in full swing down its corridor: TWO gowned assistants wheeling ONE gurney past, {SURGEON} striding ahead, steam rising from ONE sterilizer, the palm window bright."),
(38,"XWIDE","-","void", f"A painted savannah on flat cream: ONE fenced preserve running to the horizon, {MONKEY} perched on the nearest fence post with its tail curled, ONE palm tree, and parked at the gate ONE gleaming touring car."),
(39,"MED","face bright with invitation","clinic1925", "ONE clinic attendant holding out ONE completely BLANK appointment card with both hands, her face bright with invitation, the white doorway warm behind her."),
(40,"CU","mouth mid-boast, chest out","clinic1925", "ONE rich old customer mid-boast in a leather chair, chest out, counting his recovered virtues on raised fingers, his cane hooked on the chair arm."),
(41,"MED","faces stern with judgment","void", "TWO rich old men holding ONE hat up between them and gravely agreeing over its brim, faces stern with judgment, ONE hatbox open on the table."),
(42,"WIDE","-","clinic1925", "The clinic still and unattended years on: dust sheets drawn over the chairs, the palm outside grown wild across the window, ONE cane left hooked on a rail, the white tile gone dim."),
(43,"MED","brows lifting, palm out","nightstreet", f"{MAN} at the booth's counter with one open palm held out flat, brows lifting, the counter shelf bare and the shutter drawn down behind it, {NIGHT}, {WARM}."),
(44,"XCU","-","nightstreet", "The booth's counter shelf up close: bare polished wood, ONE small closed cash box, the shutter drawn down to the shelf, ONE warm round bulb painted as a flat MUSTARD GOLD disc above, the street reflected flat INK BLUE in the brass fittings."),
# ACT 4 — the 1930s. PLAYED STRAIGHT: pharmacy staging, composed faces. -------
(45,"WIDE","-","pharmacy1930", "A small American pharmacy at street level in plain flat daylight, ONE composed period man in a dark suit pushing the door open mid-step, the doorway bell arm swinging, long shelves of identical small bottles inside, every label a completely BLANK white rectangle."),
(46,"MED","-","pharmacy1930", "ONE druggist's hand in a white sleeve lifting ONE tonic bottle of softly glowing warm AMBER down from the shelf, the glow lighting the underside of his composed face from below, the neighbouring bottles plain and unlit, every label a completely BLANK white rectangle."),
(47,"XCU","-","pharmacy1930", "The tonic pouring: ONE glass on the counter filling with water as ONE composed hand tips the bottle, the softly glowing warm AMBER swirling into the water and the water taking the glow, ONE completely BLANK paper label squared on the bottle's front."),
(48,"MED","face open and trusting","pharmacy1930", f"At the counter, {BELIEVER}, receiving the softly glowing warm AMBER tonic bottle with both hands, his face open and trusting, the pharmacist's hands passing it across."),
(49,"WIDE","-","pharmacy1930", "A pantry cupboard swung open: rows of identical emptied bottles filling every shelf, dozens deep, and ONE fresh bottle of softly glowing warm AMBER standing apart on the counter beside them."),
(50,"MED","both faces composed, eyes lowered","pharmacy1930", f"A period physician resting one hand on the shoulder of the seated believer — {BELIEVER} — both faces composed and grave, the physician's eyes lowered, the instrument case shut on the desk."),
(51,"MED","mouths open in easy talk","pharmacy1930", "TWO customers at the pharmacy counter mid-conversation over the softly glowing warm AMBER tonic bottle between them, mouths open in easy talk, the pharmacist's face still as he wraps a parcel."),
(52,"CU","face going still","pharmacy1930", "ONE of the two customers cropped close, his mouth closing and his face going still mid-thought, the counter's edge below."),
(53,"MED","face plain and level","pharmacy1930", "The pharmacist in his bow tie facing squarely across the counter, his face plain and level, both hands resting flat on the wood, the shelves ranked behind him."),
(54,"WIDE","-","pharmacy1930", "Seen from slightly ABOVE, the counter laid with ONE completely BLANK report, ONE completely BLANK certificate and ONE gavel in a row, each resting untouched, dust settled evenly over all three."),
(55,"CU","face grave beneath the armband","pharmacy1930", "The pharmacist wearing ONE black armband, his face grave, lifting the softly glowing warm AMBER tonic bottle down from the shelf with both hands, the shelf gap holding a clean ring of dust."),
(56,"MED","face still over the fold","pharmacy1930", "ONE folded newspaper with a completely BLANK front page lying open on the counter seen from slightly ABOVE, the pharmacist bent over it, his face still, one hand flat on the fold."),
(57,"XWIDE","-","void", "A small funeral procession crossing a flat grey-cream field: SIX mourners pacing behind ONE black carriage, hats held to chests, the line moving slow and level."),
# ACT 5 — 2008: the boardroom (PROSPECTUS) ------------------------------------
(58,"WIDE","-","nightstreet", f"{BOOTH} re-dressed in a sleek glass boardroom skin, chrome trim screwed over the old wood, the same cart underneath showing at the wheels, {NIGHT}."),
(59,"CU","-","nightstreet", "The booth's corner up close: ONE crisp glass panel screwed over chipped layers of old painted wood, ONE warm round bulb painted as a flat MUSTARD GOLD disc reflected in the glass, flat INK BLUE evening behind."),
(60,"MED","face absorbed, brows level","refereeroom", f"A warm university laboratory in morning light through tall windows, wooden benches and brass fittings: {MOUSE} plump and quick on ONE running wheel, and ONE modern scientist — a type with calm generic features — watching absorbed, his brows level, ONE clear dish of dark red residue on the bench."),
(61,"CU","face steady, eyes careful","refereeroom", "The modern scientist type cropped at the chest lifting the clear dish toward the warm window light, his face steady and his eyes careful, wooden shelves of glassware ranked behind."),
(62,"MED","eyes lifting to the glow","void", "FIVE onlookers individuated on flat cream, eyes lifting together toward ONE small point of softly glowing warm AMBER held high above them in a raised hand."),
(63,"WIDE","-","data", DATA),
(64,"XCU","-","boardroom2008", "Seen from slightly ABOVE, ONE completely BLANK contract page carrying ONE wax seal and ONE red ribbon, TWO fountain pens laid parallel beside it, the long table's wood cold and polished."),
(65,"MED","faces lit through the amber","boardroom2008", f"{EXECS} leaning in around {ORNAMENT}, the amber light passing through it onto the nearest faces, TWO hands reaching toward it at once, glass walls sheer behind."),
(66,"WIDE","-","paperoffice", "A paper office in dusty pale daylight falling in long beams: ONE clerk's trolley arriving stacked with completely BLANK sealed documents, ribbons trailing, ONE desk lamp burning at the far desk."),
(67,"MED","face grave in the lamp light","paperoffice", "Seen from slightly ABOVE, ONE completely BLANK report laid square on a blotter, ONE wax seal pressed at its corner, and ONE clerk setting his pen down beside it, his face grave in the lamp light."),
(68,"MED","both pairs of eyes narrowing at the glow","refereeroom", "TWO technicians in lab coats bent over ONE clear dish under a bench lamp, the dish glowing on its own, both pairs of eyes narrowing at the glow, steel racks behind."),
(69,"XCU","-","refereeroom", "ONE clear dish filling the picture, its rim glowing a thin chemical green, ONE gloved fingertip lifting its edge toward the light."),
(70,"CU","-","void", "ONE lit bulb glowing inside ONE glass instrument bell on flat cream, its light spreading in painted rings, ONE dial beneath it completely BLANK."),
(71,"XWIDE","-","boardroom2008", "The boardroom floor bare: chairs squared in at the long table, the glass door shut flush, ONE dust sheet drawn over the far credenza, thin daylight lying even across the glass walls."),
(72,"MED","-","boardroom2008", f"Seen from slightly ABOVE, ONE completely BLANK receipt slip lying alone at the centre of the long bare table, {ORNAMENT} standing beside it, its amber the one warmth in the room."),
# ACT 6 — 2019: the lounge ----------------------------------------------------
(73,"MED","beaming behind the counter","nightstreet", f"{BARKER} hanging ONE IV bag of softly glowing warm AMBER liquid from a hook above the booth's counter shelf, beaming, fresh spa panels fitted over the old wood, {NIGHT}."),
(74,"WIDE","faces easy, eyes half-closed","lounge2019", "A glass lounge at dusk over a city: FOUR recliners with FOUR IV stands, ONE bag of softly glowing warm AMBER liquid on each stand, THREE relaxed clients with faces easy and eyes half-closed, ONE white-coated attendant holding ONE completely BLANK tablet moving between them, ONE potted fig at the floor-to-ceiling glass, the city flat INK BLUE beyond."),
(75,"MED","face serene over the paper","lounge2019", "ONE reclined client holding ONE completely BLANK white slip of paper up at arm's length, its face bare and unmarked, his face serene, the attendant's tray passing with ONE capped pen."),
(76,"MED","-","paperoffice", "Seen from slightly ABOVE in dusty pale daylight, ONE single completely BLANK government page lying square on a desk, ONE embossed seal at its foot, ONE desk lamp burning steady over it."),
(77,"MED","faces brisk","lounge2019", "TWO attendants wheeling the FOUR IV stands away at speed, the softly glowing warm AMBER bags boxed on a cart, ONE dust sheet drawn over the nearest of the FOUR recliners, both faces brisk."),
(78,"XCU","-","void", "ONE wall clock with a completely BLANK face filling the frame, hands only, the minute hand sweeping through one visible step."),
(79,"MED","-","paperoffice", "ONE brass balance in the long dusty light: in one pan ONE completely BLANK ribboned sheet of paper, in the other ONE completely BLANK plain sheet of paper, both faces bare and unmarked, the beam tipping slowly from one side to the other."),
(80,"MED","-","paperoffice", "ONE ribboned completely BLANK document unrolling open across the desk like a small carpet, and standing at its far end ONE tiny wooden market stall drawn small as a toy, warm light rising from the tiny stall as the paper reaches it."),
(81,"MED","-","paperoffice", "ONE plain completely BLANK page dropping flat onto the tiny toy market stall like a lid, the small warm light pressed to a thin line at the paper's edge, the desk lamp steady above."),
(82,"WIDE","-","lounge2019", "The lounge unchanged in the same dusk: the FOUR recliners standing exactly where they stood, the potted fig unmoved at the glass, the city beyond holding its same flat INK BLUE."),
(83,"CU","eyes clearing","lounge2019", "ONE client's face cropped close as his eyes clear and refocus, one hand rising slowly to his own chest, the dusk soft behind the glass."),
# ACT 7 — today: the protocol -------------------------------------------------
(84,"WIDE","-","nightstreet", f"{BOOTH} stripped back to bare unpainted wood, and standing behind its own counter shelf {KEEPER}, arranging ONE row of identical small bottles each holding softly glowing warm AMBER, {NIGHT}."),
(85,"WIDE","face calm","protocol", f"A morning kitchen table set end to end: {KEEPER} seated before ONE pill-organizer grid of blank compartments, a wall of identical small bottles of softly glowing warm AMBER ranked behind him, TWO wall clocks with completely BLANK faces showing hands only, morning light flat across it all, his face calm."),
(86,"MED","face earnest, eyes kind","protocol", f"{KEEPER} pausing mid-routine with one hand resting flat on the table, his face earnest and his eyes kind, morning light warm on the plain grey coat."),
(87,"CU","-","protocol", "The wall of identical small bottles of softly glowing warm AMBER cropped tight, rank upon rank receding, ONE hand drawing a single bottle out of line."),
(88,"MED","jaw set with resolve","protocol", f"{KEEPER} tipping a stream of small pills of softly glowing warm AMBER from ONE bottle into an open palm, his jaw set with resolve, the clock hands behind him climbing toward the top."),
(89,"XCU","-","protocol", "ONE clock's minute hand alone against a completely BLANK clock face, ticking one visible step short of the top."),
(90,"WIDE","-","protocol", "The kitchen staged as a freight dock: ONE hand truck stacked with crates of identical small bottles of softly glowing warm AMBER parked at the table, ONE clipboard with a completely BLANK sheet hanging from a crate, morning light through the open door."),
(91,"MED","face resolute","protocol", f"{KEEPER} standing at the table's end facing ONE empty white plate laid like an opponent, his face resolute, the clock hands above just short of noon, both clock faces completely BLANK."),
# ACT 8 — the referee ---------------------------------------------------------
(92,"MED","eyes turning from the glow","nightstreet", f"{MAN} in the queue turning his head away from the booth's glow toward ONE plain grey door across the street, his eyes steady on it, {NIGHT}, {WARM}."),
(93,"MED","-","refereeroom", "ONE plain grey door standing open onto flat fluorescent light, ONE completely BLANK nameplate screwed level at eye height, the corridor beyond ranked with steel."),
(94,"WIDE","-","refereeroom", "The referee's mouse room in flat fluorescent light: rows of clear cages on steel racks, each cage holding ONE white mouse, ONE clipboard with ONE completely BLANK ruled sheet hanging at the rack's end, the room even and cool."),
(95,"MED","-","refereeroom", f"{MOUSE} nosing into ONE small feeding dish set inside the cage, the dish holding a dark red residue, ONE gloved hand withdrawing from the cage door."),
(96,"MED","-","refereeroom", "TWO identical clear cages side by side on brushed steel, TWO identical white mice sitting in identical postures at the centre of identical level bedding, everything about the two cages exactly alike."),
(97,"XCU","-","refereeroom", "FOUR identical clear cages in a TWO-by-TWO grid, FOUR identical white mice in identical postures, the grid perfectly even, the fluorescent light lying flat across all four."),
(98,"CU","-","void", f"ONE hand holding {VIAL} up before ONE bare fluorescent tube, the cold light passing straight through the amber and landing plain on the wall behind."),
(99,"XWIDE","-","void", "FIVE small wooden stalls in a receding row on flat cream, each dressed in a different era's trim and each leaning a little further toward the ground than the one before, every shutter drawn down, and before them ONE small glass vial lying on its side, its warm AMBER glow guttering low."),
(100,"WIDE","-","data", DATA),
(101,"XCU","-","void", "ONE small glass vial lying on its side on flat cream, drained of its warm AMBER, its glass clear and unlit, casting one thin plain shadow."),
# ACT 9 — the unclaimed table -------------------------------------------------
(102,"MED","-","apothecary", f"On the apothecary counter, {VIAL} standing in its lamp circle, and beside it, unclaimed, ONE pair of worn walking shoes with their laces loose, the wall of identical small bottles ranked behind with every label completely BLANK."),
(103,"WIDE","-","data", DATA),
(104,"WIDE","-","apothecary", "The apothecary in frontal shop-portrait symmetry: the wall of identical small bottles of softly glowing warm AMBER in neat ranks, every label a completely BLANK paper rectangle, and squared at the counter's centre ONE pair of worn walking shoes, the light passing through the amber onto them."),
(105,"MED","-","void", f"{VIAL} lying on its side on flat cream with its stopper out, and a small painted country road running past it into the distance, TWO tiny walkers on the road already far beyond the glass."),
(106,"MED","faces mid-talk and warm","void", "TWO figures walking together along a cream road, individuated, faces mid-talk and warm, their strides matched, TWO long shadows overlapping behind them."),
(107,"XCU","-","void", "TWO right hands meeting in one firm shake filling the picture, the grip full and even, TWO cuffs at the frame edges — one vermilion red, one sage green."),
(108,"MED","face lighting at the door","void", "A Tuesday staged as a container: ONE open doorway warm with lamplight, ONE small table set with TWO cups, ONE arriving figure at the threshold, and the host's face lighting at the door."),
(109,"MED","-","void", f"Laid side by side on ONE plain table: {VIAL} at one end, and at the other TWO clasped hands resting easy on the wood, the amber's glow reaching only halfway between them."),
# ACT 10 — back at the booth --------------------------------------------------
(110,"WIDE","eyes down at the glow","nightstreet", f"{MAN} at the front of the queue at last, {VIAL} received in both hands, his eyes down at its glow, {BOOTH} above and ahead of him, {NIGHT}, {WARM}."),
(111,"MED","-","nightstreet", "ONE thick ledger of completely BLANK ruled pages lying open on the booth's counter shelf seen from slightly ABOVE, both pages bare from edge to edge, the flat MUSTARD GOLD bulb light resting on the paper and flat INK BLUE evening beyond."),
(112,"CU","shoulders easing, eyes going soft","nightstreet", f"{MAN}'s face easing as the vial's warm AMBER light reaches it, his shoulders dropping and his eyes going soft, {NIGHT}, {WARM}."),
(113,"XCU","-","nightstreet", f"ONE open palm holding {VIAL} upright, the amber glow pooling in the hand, flat MUSTARD GOLD light above and flat INK BLUE evening beyond the fingers."),
(114,"CU","eyes half-closed and calm","nightstreet", f"{MAN}'s face lit warm from below by the vial's AMBER glow, his eyes half-closed and calm, {NIGHT}, {WARM}."),
(115,"XWIDE","-","nightstreet", f"The whole street: {BOOTH} bright at the head of the long patient queue, {NIGHT}, the painted discs warm over the shuffling line."),
# ACT 11 — THE TURN -----------------------------------------------------------
(116,"MED","jaw setting, eyes leaving the glow","nightstreet", f"THE TURN: {MAN} at the booth's counter turning on his heel to face AWAY from the booth and toward the queue, his jaw setting and his eyes leaving the glow for the faces, {VIAL} still in one hand, {NIGHT}, {WARM}."),
(117,"WIDE","every face carrying the same small want","nightstreet", f"The queue as the true version: every era at once down the row — frock coats, canes and white coats, bow ties, grey suits, athleisure — every figure individuated with dignity, every face carrying the same small want, ONE completely BLANK ticket in every hand, {NIGHT}."),
(118,"MED","faces changing down the row, all wanting","nightstreet", f"The row up close: ONE bearded 1889 physician, ONE 1925 rich man with his cane, ONE 1930 believer, ONE 2008 executive and ONE 2019 client standing shoulder to shoulder, faces changing down the row and all wanting the same thing, the whole row standing well INSIDE the frame with clear open space at both sides, the pavement beneath them lit flat warm cream by the booth's mustard glow, ONE completely BLANK ticket in every hand, {NIGHT}."),
(119,"CU","eyes wet and warm, chin up","nightstreet", f"{MAN} cropped close facing the queue, his eyes wet and warm and his chin up, {NIGHT}, {WARM}."),
(120,"WIDE","-","void", "FIVE small glass vials lying on their sides in a row on flat cream, their softly glowing warm AMBER dimming stage by stage down the line, FIVE stoppers scattered beside them."),
(121,"WIDE","-","nightstreet", f"From behind {MAN}'s shoulder: the whole long queue standing before him where the street runs, every era at once, each figure holding ONE completely BLANK ticket, {NIGHT}, {WARM}."),
(122,"MED","face patient and open","nightstreet", f"ONE unhurried figure standing midway down the queue holding ONE completely BLANK ticket of its own, face patient and open, hats and coats of every era pressing warm around it, {NIGHT}."),
(123,"WIDE","chin up, eyes forward","nightstreet", f"{MAN} stepping sideways out of the queue's line, one oversized shoe planted outside it, his chin up and his eyes forward down the row, the queue holding its shape behind him, {NIGHT}, {WARM}."),
(124,"MED","beaming at the work","nightstreet", f"{BARKER} up ONE ladder against the booth prying open ONE fresh paint pot, beaming at the work, the painted discs warm above him, {NIGHT}."),
(125,"WIDE","faces turning warm as he passes","nightstreet", f"{MAN} walking down the row past the queue's faces, strangers turning warm as he passes, coats of every era catching the booth's far glow, {NIGHT}, {WARM}."),
(126,"MED","eyes up on the faces ahead, easy","nightstreet", f"{MAN} sliding {VIAL} away into his coat pocket mid-stride, his eyes up on the faces ahead, easy, {NIGHT}, {WARM}."),
(127,"MED","both faces opening warm","nightstreet", f"{MAN} stopping before ONE queueing stranger and putting out his hand, the stranger's hand already rising to meet it, both faces opening warm, ONE completely BLANK ticket in the stranger's other hand, {NIGHT}, {WARM}."),
]

# ============================================================================
# SECOND FRAMES — every sentence over 25 words carries two pictures so the
# hold stays under ~9.6s at 158wpm.
# ============================================================================
EXTRA = {
 2:  [("XCU","-","nightstreet", "TWO small hands gripping ONE completely BLANK ticket at its edges, the paper bowing slightly, flat MUSTARD GOLD booth glow catching one edge and flat INK BLUE evening beyond the fingers.")],
 4:  [("MED","faces carrying the same want","void", "A short row of FOUR queueing figures from every walk of life on flat cream, individuated, each holding ONE completely BLANK ticket, each face carrying the same small want.")],
 17: [("CU","brows climbing","lecture1889", "TWO bearded front-row doctors in dark frock coats leaning together, brows climbing, one gripping the other's sleeve, gaslight behind them.")],
 37: [("WIDE","-","clinic1925", f"Through the clinic window, {MONKEY} sitting on a fence rail beside ONE palm tree, its tail curled around the rail, the white tile framing the view.")],
 50: [("WIDE","-","pharmacy1930", "A quiet bedroom in plain daylight: the bed made smooth, the curtains half drawn, ONE stoppered bottle of softly glowing warm AMBER standing on the nightstand, ONE pocket watch resting still beside it.")],
 60: [("CU","-","refereeroom", f"{MOUSE} filling the frame mid-stride on its running wheel, whiskers swept back, the wheel spokes turning, warm morning light on the glass, bedding scattered below.")],
 63: [("WIDE","faces closed and certain","boardroom2008", f"Seen from slightly ABOVE, {EXECS}, ONE completely BLANK contract with ONE red ribbon lying square at the table's centre, {ORNAMENT} beside it, faces closed and certain, glass walls sheer behind.")],
 74: [("CU","-","lounge2019", "ONE bag of softly glowing warm AMBER liquid hanging from ONE IV stand, the line curving down and away, the dusk city soft beyond the glass.")],
 85: [("MED","-","protocol", "The pill-organizer grid seen from slightly ABOVE: ranks of blank compartments, each holding ONE small pill of softly glowing warm AMBER, ONE hand lifting the next pill in sequence, morning light even across the grid.")],
 86: [("MED","-","protocol", "TWO coats hanging on TWO wall hooks side by side: ONE plain grey coat and ONE flat vermilion red coat with THREE round buttons, morning light resting evenly across both.")],
 94: [("MED","face exact and unhurried","refereeroom", "ONE technician in a grey coat lifting ONE clear cage down from the rack with both hands, her face exact and unhurried, the fluorescent light flat on the steel.")],
 103:[("XWIDE","-","void", "A long road across flat cream crowded with walkers: DOZENS of striding figures individuated in different palette coats, arms swinging, the line of them receding to the horizon.")],
 110:[("XCU","-","nightstreet", "ONE small glass vial of softly glowing warm AMBER held in TWO small hands, the amber the same amber as ever, flat MUSTARD GOLD booth glow above and flat INK BLUE evening around the hands.")],
 112:[("MED","face at rest in the glow","void", "ONE buyer from another era seated on a doorstep at evening holding ONE small bottle of softly glowing warm AMBER to his chest, his face at rest in the glow, the street around the doorway flat INK BLUE.")],
 118:[("CU","-","nightstreet", "FIVE hands from five eras side by side — lace cuff, suit cuff, shirtsleeve, grey wool, athleisure — each holding ONE completely BLANK ticket, flat MUSTARD GOLD glow catching the papers' edges, flat INK BLUE evening behind.")],
 120:[("CU","jaw set, eyes level","nightstreet", f"{MAN} holding {VIAL} out at arm's length and looking past it to the queue, his jaw set, his eyes level and unforgiving, {NIGHT}, {WARM}.")],
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
 "own dominant colour from that set. Every glow is painted as a flat matte disc or field of "
 "colour, never a rendered radiance. Expressions are BOLD, exaggerated and readable at a "
 "glance. Visible gouache texture, flat matte, NO gradients, NO airbrushed shading, NO "
 "photographic texture, NO three-dimensional rendering. There is NO text, NO lettering, NO "
 "numbers and NO writing of any kind anywhere in the image; any sign, board, placard, label, "
 "badge, ticket, page, banner, document or screen is completely BLANK. Any crowd is "
 "individuated: different faces, different builds, clothes in DIFFERENT colours from the "
 "palette, never a row of matching coats. These are ORIGINAL characters in a general "
 "mid-century cartoon idiom: NO existing cartoon characters, NO studio logos, NO trade "
 "dress, and no likeness of any real person. ONE SINGLE COHERENT SCENE, NOT a grid of "
 "panels, NOT a sheet of studies. 16:9, edge to edge, one scene, one camera.")

WPM = 158
MAX_HOLD = 9.6
MIN_CAM = {'XCU': 10, 'CU': 12, 'XWIDE': 8}
MAX_RUN = 3
MIN_CU_SHARE = 0.20
MIN_EVENT_SHARE = 0.85
BOOTH_MAX_SHARE = 0.30          # booth/queue night-street frames, combined
BOOTH_ENVS = {'nightstreet'}
EVENING_ENVS = {'nightstreet'}  # THE WARM-MAN LAW bites here
PROSPECTUS_ENVS = {'boardroom2008', 'paperoffice'}
PROSPECTUS_MAX = 14
APOTHECARY_MAX = 8
CORE_ENVS = {'nightstreet','lecture1889','clinic1925','pharmacy1930','boardroom2008',
             'lounge2019','protocol','refereeroom','apothecary','paperoffice','void','data'}
STRAIGHT_LINES = range(45, 58)   # the Byers act, played entirely straight

FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|cheeks|'
                  r'tongue|chin|frown|soft|calm|composed|weary|star(e|ing)|blush|surprise|nod|'
                  r'dread|faces?\b|wanting|patient|measured|settled|kind\b|pleased|sincere|'
                  r'joy\b|counting|grave|serene|earnest|resolut|absorb|trust|eager|certain|'
                  r'conviction|exact|unhurried|dignified|steady|brisk|prim|stern|clear', re.I)
EVENT = re.compile(
    r'burst|pop|fly|flar|blast|shoot|erupt|stream|pour|collaps|toppl|crack|snap|spring|slam|'
    r'throw|thrown|swing|scatter|shov|carr|drop|slid|tipping|vibrat|lift|roll|hover|dart|glow|'
    r'steam|smoke|nod|shak|crouch|lean|reach|step|walk|run|hold|haul|pull|peer|point|count|'
    r'trudg|wrap|bang|settl|duck|turn|rub|sip|thump|spray|strik|rais|crush|crane|hang|stretch|'
    r'tilt|wav|file|squeez|press|balanc|climb|land|swarm|feed|trac|receiv|arriv|load|cross|'
    r'tumbl|pil|recoil|glanc|hurry|bend|bent|crowd|tear|driv|measur|argu|greet|wait|'
    r'watch|look|open|shut|reced|dwarf|clutch|slip|fork|appear|swivel|rotat|freez|curl|march|'
    r'thud|bow|sweep|stoop|practis|welcom|fold|jump|rest|loom|dangl|buckl|puff|retir|pose|'
    r'smooth|travel|drift|tuck|unroll|brush|nail|study|shrink|brighten|flood|offer|spill|'
    r'meet|wish|spread|ring|split|huddl|thrust|catch|pass|grip|perform|plant|rise|rising|'
    r'casc|flick|aim|stagger|clip|steady|repeat|pace|pacing|plump|clink|pin|tap|wheel|light|'
    r'lit\b|beam|trad|dip|recit|square|straighten|leap|rock|spin|pat|draw|heap|tick|sit\b|'
    r'sitting|stand|pry|arrang|withdraw|refocus|swell|flex|declar|consult|boast|agree|'
    r'flutter|park|screw|dress|stride|striding|shuffl|nose|nosing|perch|box', re.I)

# COUNTS, NOT NOUNS — a scene that stages a character must carry the numeric
# words. A reference sheet is not sufficient.
REQ = {
 'VERMILION RED coat':      ['THREE round buttons', 'PAIR of hairs'],
 'THE BARKER':              ['ONE straw boater', 'dusty ORANGE'],
 'THE BULB-BOOTH':          ['ONE row of warm round bulbs', 'ONE counter shelf'],
 'bearded physicians':      ['TWELVE'],
 'ticket-holding old men':  ['THREE'],
 'recliners':               ['FOUR'],
 'executives':              ['SIX'],
 'monkey':                  ['ONE small monkey'],
 'white mouse':             ['ONE white mouse'],
 'pill-organizer':          ['blank compartments'],
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

# SIGN-SHAPE LAW — no scene may request written content, and every row that
# names a label-shaped object states BLANK in that same row. The apothecary
# probe leaked lettering; this film is MADE of label-shaped objects.
SIGNS = re.compile(r'\b(letter|letters|lettering|lettered|word|words|writing|written|writes|'
                   r'text|texts|number|numbers|numeral|numerals|digits?|caption|inscrib\w*|'
                   r'font|typeface|says|reading\b|reads\b)\b', re.I)
signy = [i for i, s in enumerate(S, 1) if not isdata[i-1] and SIGNS.search(s[4])]
if signy:
    errs.append('scene requests written content: ' + ' '.join('b%03d' % i for i in signy[:10]))
LABELISH = re.compile(r'\b(labels?|posters?|tickets?|contracts?|certificat\w*|documents?|'
                      r'pages?|prospectus\w*|ledgers?|invoices?|slips?|tablets?|nameplates?|'
                      r'charts?|clipboards?|cards?|dials?|calendars?|newspapers?|reports?|'
                      r'papers?)\b', re.I)
unblanked = [i for i, s in enumerate(S, 1) if not isdata[i-1]
             and LABELISH.search(s[4]) and 'BLANK' not in s[4]]
if unblanked:
    errs.append('label-shaped object staged with its BLANK missing: ' +
                ' '.join('b%03d' % i for i in unblanked[:10]))

# THE VIAL LAW — the product carries the same amber phrase in every era.
PRODUCT = re.compile(r'\bvials?\b|\btonic\b|\bIV bag\b|\bbags? of\b|molecule-shaped|'
                     r'\belixir\b|\bpills?\b', re.I)
coldvial = [i for i, s in enumerate(S, 1) if not isdata[i-1]
            and PRODUCT.search(s[4]) and 'AMBER' not in s[4].upper()]
if coldvial:
    errs.append('product staged with its amber missing: ' +
                ' '.join('b%03d' % i for i in coldvial[:10]))

# MIDWAY LIGHT — every night-street frame names both colours at point of use.
unlit = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] == 'nightstreet'
         and ('MUSTARD' not in s[4] or 'INK BLUE' not in s[4])]
if unlit:
    errs.append('night-street frame missing MUSTARD GOLD / INK BLUE at point of use: ' +
                ' '.join('b%03d' % i for i in unlit[:10]))

# THE WARM-MAN LAW — every evening frame with the Man carries the warmth clause.
coldman = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] in EVENING_ENVS
           and 'VERMILION RED coat' in s[4] and 'warm face unchanged' not in s[4]]
if coldman:
    errs.append('evening frame stages the Man with the warmth clause missing: ' +
                ' '.join('b%03d' % i for i in coldman[:10]))

# LIKENESS LAW — the narration may say the names; the pictures never do.
NAMES = re.compile(r'Brown-S[ée]quard|Voronoff|Byers|Sinclair|Johnson', re.I)
likeness = [i for i, s in enumerate(S, 1) if NAMES.search(s[4]) or NAMES.search(s[2])]
if likeness:
    errs.append('a real surname reached SCENE text: ' + ' '.join('b%03d' % i for i in likeness))

# ENVIRONMENT CAP — booth/queue night-street frames <=30% combined; every core
# environment appears; accents stay capped.
setc = Counter(s[3] for s in S)
unknown = sorted(set(setc) - CORE_ENVS)
if unknown:
    errs.append(f'unknown environment tags: {unknown}')
booth_n = sum(setc[e] for e in BOOTH_ENVS)
if booth_n / len(S) > BOOTH_MAX_SHARE:
    errs.append(f'booth/queue frames are {booth_n}/{len(S)} ({booth_n/len(S):.0%}), '
                f'max {BOOTH_MAX_SHARE:.0%}')
unused = sorted(CORE_ENVS - set(setc))
if unused:
    errs.append(f'core environments unused: {unused}')
prospectus_n = sum(setc[e] for e in PROSPECTUS_ENVS)
if prospectus_n > PROSPECTUS_MAX:
    errs.append(f'{prospectus_n} PROSPECTUS-accent frames; cap {PROSPECTUS_MAX}')
if setc['apothecary'] > APOTHECARY_MAX:
    errs.append(f'{setc["apothecary"]} APOTHECARY-accent frames; cap {APOTHECARY_MAX}')

# THE STRAIGHT ACT (45-57) — the Byers act rejects comic staging AND the
# booth's whole vocabulary. Pharmacy gravity, the same as the Pullman act.
COMIC = re.compile(r'shaft|spotlight|jury|juror|grin|comic|ABSURD|COLOSSAL|ENORMOUS|'
                   r'cartoon|gag\b|wink|bulging|booth|barker|bulbs?\b|queue', re.I)
bent = [i for i, s in enumerate(S, 1) if s[0] in STRAIGHT_LINES and not isdata[i-1]
        and (COMIC.search(s[4]) or COMIC.search(s[2]))]
if bent:
    errs.append('the straight act broke its straightness: ' + ' '.join('b%03d' % i for i in bent))

# INTERACTION QUOTA — the Barker and the Man share at least THREE frames.
shared = [i for i, s in enumerate(S, 1)
          if 'THE BARKER' in s[4] and 'VERMILION RED coat' in s[4]]
if len(shared) < 3:
    errs.append(f'the Barker and the Man share {len(shared)} frames; the law is at least 3')

# THE TURN — the final frames land in script order and stage what the script
# stages: the turn away, the every-era queue, the step out, the walk, the hello.
def _scene_for(line):
    rows = [s for s in S if s[0] == line]
    return rows[0][4] if rows else ''
turn_checks = [
    (116, 'AWAY from the booth', 'line 116 stages the Man facing AWAY from the booth'),
    (117, 'every era at once',   'line 117 stages the queue as every era at once'),
    (117, 'BLANK ticket in every hand', 'line 117 gives every hand ONE blank ticket'),
    (123, 'out of the queue',    'line 123 stages the step out of the queue'),
    (125, 'walking down the row','line 125 stages the walk down the row'),
    (127, 'putting out his hand','line 127 stages the hello'),
]
for line, need, msg in turn_checks:
    if need not in _scene_for(line):
        errs.append(f'THE TURN out of order: {msg}')

dusk = [s for s in live if s[3] in EVENING_ENVS]
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(live)} ({cu/len(live):.0%}) | faces "
      f"{len([s for s in live if s[2]!='-'])}/{len(live)} | events "
      f"{len(live)-len(noev)}/{len(live)} | data {ndata} | night-street {booth_n} "
      f"({booth_n/len(S):.0%}) | prospectus {prospectus_n} | apothecary "
      f"{setc['apothecary']} | holds {sum(holds):.0f}s/{budget:.0f}s")
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
    'VERMILION RED coat' in s[4] or 'THE BARKER' in s[4] or 'physicians' in s[4] or
    'lecturer' in s[4] or 'old men' in s[4] or 'surgeon' in s[4] or 'pharmacist' in s[4] or
    'believer' in s[4] or 'executives' in s[4] or 'client' in s[4] or 'attendant' in s[4] or
    'plain grey' in s[4] or 'technician' in s[4] or 'scientist' in s[4])]
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
