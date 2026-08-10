#!/usr/bin/env python3
"""Frame book — Tipping (episode 4). 129 frames: 119 sentences + 10 second
frames for every sentence over 25 words.

Every law here was paid for on an earlier film:

  THE CAMERA IS A CROP     CAM names where the frame edge cuts; scene text
                           never says "close on".
  COUNTS, NOT NOUNS        THREE buttons, FIVE jurors plus ONE staring child,
                           TWO tailcoat points, ONE white glove, ONE apron
                           pencil, EIGHT diners — stated in EVERY frame that
                           stages the character. A reference sheet is not
                           sufficient.
  A FACE ACTION PER FRAME  declared in the expression field AND present in
                           the scene text the model actually receives.
  EVENTS, NOT STATES       something happens in every frame.
  OMISSION, NOT NEGATION   absences are described as present things. The lint
                           below rejects "no ", "without" and "n't" in scene
                           text.
  SIGN-SHAPED OBJECTS      the tablet shows THREE BLANK ROUNDED RECTANGLES and
                           ONE small blank rectangle; protest signs are BLANK
                           BOARDS; the ledger is RULED LINES; checks are blank
                           slips. No scene may request letters, words, numbers
                           or writing as visible content. The numbers live in
                           narration and in the deterministic DATA frames only.
  TRIBUNAL LIGHT           the flat gouache shaft on judgment frames; THEATRE
                           accent (hard spotlight, black surround) on exactly
                           TWO setpieces: the first screen-turn (line 9) and
                           the public-performance act (line 90). CUSTOMS
                           (dusty side window-light, long soft beams) on the
                           history acts.
  TWO-SIDED FRAMES         judge and judged in ONE picture (the hovering thumb
                           AND the five studying the pastry case).
  THE PULLMAN ACT (51-58)  played entirely straight: customs light, calm
                           composed weary faces, and its rows are gated
                           against "shaft", "jury", "spotlight" and every
                           comic staging word.
  ENVIRONMENT CAP          the cafe is this film's rooftop loft: <=20% of
                           frames, measured rather than hoped for.

Two settings beyond the ten in CAST.md, both demanded by the script:
"manor" (the Tudor great house, lines 22-25 — the vails scene has no home in
the ten) and "stage" (line 90's theatre setpiece); "pullman" carries the act
WORLD.md orders played straight. Flagged for review.

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

MAN = ("THE MAN: a small slight man with a round face and a big confident nose, EXACTLY "
       "TWO kinked hairs leaning at different angles on his crown, a flat VERMILION RED coat "
       "with THREE round buttons, thin stick legs and absurdly oversized shoes")
BARISTA = ("THE BARISTA: a tall young woman in a cream shirt with sleeves rolled to the elbow, "
           "a SAGE GREEN half-apron with ONE front pocket holding TWO pens, a completely blank "
           "name badge, her hair in a high knot with ONE pencil pushed through it")
SCREEN = ("THE SCREEN: an oversized matte near-black tablet slab drawn like a monument on ONE "
          "steel counter-mount arm, showing THREE large blank rounded rectangles stacked and "
          "ONE small blank rectangle below them, cleaner and newer than everything around it")
JURY = ("THE JURY: FIVE people in line, each in a DIFFERENT palette colour coat with different "
        "faces and builds, plus ONE staring child in a striped jumper")
WAITER = ("THE GRAND WAITER: a towering 1890s hotel waiter in a black tailcoat with TWO points, "
          "white waistcoat and white bow tie, ONE white glove on the open palm he holds "
          "discreetly at hip height, his bare hand balancing a tray aloft, a gold watch-chain "
          "in a shallow arc, his eyes at the horizon")
CRUSADER = ("THE CRUSADER: a 1912 reformer in a straw boater, rolled shirtsleeves with sleeve "
            "garters, a completely blank MUSTARD GOLD sash, a waistcoat, pamphlets under ONE arm")
RESEARCHER = ("THE RESEARCHER: a man in a dusty ORANGE cardigan with THREE buttons over a "
              "checked shirt, corduroy trousers, ONE clipboard, his face set in mild permanent "
              "surprise")
PORTER = ("THE PORTER: a Black Pullman porter in a crisp dark uniform coat with TWO neat rows "
          "of polished buttons and ONE soft-brimmed uniform cap, his bearing upright and composed")

# "a darker mix of the scene's colour" let the model pick the colour, and it
# picked noir teal three times (b009, b015, b074). The colours are named now.
SHAFT = ("a single soft-edged column of pale CREAM light falling from directly above, the "
         "surrounding field a flat darker warm DUSTY ORANGE-brown")
THEATRE = "a hard theatrical spotlight with a black surround"
CUSTOMS = "dusty side window-light falling across the scene in long soft beams"

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
# ACT 1 — the counter, the man, the monument ---------------------------------
(1,"WIDE","-","cafe", "A cafe counter standing unattended in flat morning light, a bare cream wall behind it, ONE glass jar and ONE folded cloth waiting on the wood, steam curling up from behind the counter."),
(2,"MED","eyes forward, hopeful","void", f"{MAN} walking briskly across a bare cream field with his eyes forward and hopeful, his absurdly oversized shoes slapping the ground."),
(3,"XCU","-","void", "ONE steaming paper coffee cup on flat cream with FOUR blank coins stacked neatly beside it, the steam rising in a thin confident line."),
(4,"CU","brows soft, eyes wanting","void", f"{MAN} cupping both hands around the shape of a small imagined cup, his brows soft and his eyes wanting exactly one small thing."),
(5,"XWIDE","eyes down, tired","nightstreet", f"{MAN} tiny on a long dark shuttered street, trudging with his eyes down and tired, every window dark, ONE doorway far ahead glowing warm."),
(6,"MED","eyes lifting, relieved","nightstreet", f"{MAN} pushing open a glass cafe door with both hands, warm gold light pouring out over him, his eyes lifting and relieved."),
(7,"MED","mouth open mid-order, chin dipping","cafe", f"{MAN} at the counter with his mouth open mid-order and one finger raised, and {BARISTA} nodding back to him, her chin dipping once."),
(8,"CU","eyes widening, hand freezing","cafe", f"{BARISTA} laying both hands on {SCREEN} and beginning to turn it, while beside the counter {MAN}'s eyes widen and his reaching hand freezes in mid-air."),
(9,"WIDE","eyes wide, mouth a flat line of dread","cafe", f"A single soft-edged column of pale CREAM light falling from directly above, the surrounding cafe a flat darker DUSTY ORANGE-brown, on {SCREEN} swivelling on its mount to face {MAN}, who stares at it with wide eyes and a mouth gone to a flat line of dread."),
(10,"XCU","-","cafe", f"The face of {SCREEN} filling the picture, its THREE large blank rounded rectangles glowing softly and its ONE small blank rectangle sitting quietly beneath them."),
(11,"WIDE","eyes busy elsewhere, child staring","cafe", f"{MAN} small at the counter before {SCREEN}, and behind him {JURY} stretching back toward the door, the child staring straight at the slab while the FIVE grown jurors aim their busy eyes at the ceiling and their own shoes."),
# ACT 2 — the hearing nobody convened ----------------------------------------
(12,"MED","one brow up, long level look","void", f"{MAN} and {SCREEN} facing each other alone on flat cream, the man lifting one brow and giving the slab a long level look, his arms folding."),
(13,"XCU","-","cafe", "ONE clean dry portafilter hanging on its hook and ONE empty cup waiting upside down on a folded towel, the espresso machine's chrome throwing back the room's warm light."),
(14,"MED","eyes lifting politely to the middle distance","cafe", f"{BARISTA} finishing her turn of {SCREEN} with both hands, formal as a bailiff presenting evidence, then lifting her eyes politely into the middle distance, the espresso machine waiting cold behind her."),
(15,"WIDE","chin coming up, throat swallowing","cafe", f"{SHAFT} falling squarely on {MAN} at the counter, his chin coming up and his throat swallowing, {SCREEN} looming at the edge of the light."),
(16,"WIDE","eyes flicking door to door","void", f"THREE tall blank doors standing ajar on a bare cream field, and {MAN} walking slowly toward them casting THREE long shadows, one toward each door, his eyes flicking from door to door."),
(17,"XCU","-","void", "Beneath THREE large blank rounded rectangles, ONE small blank rectangle drawn tiny and apologetic, ringed in a heavy vermilion circle like an exhibit."),
(18,"WIDE","-","capitol", f"An empty judge's bench towering in a vast marble hall, ONE gavel resting on its block, {CUSTOMS} over rows of empty seats."),
(19,"MED","-","void", "A takeaway coffee cup standing on flat cream, and clipped to its lid a tiny toy judge's bench complete with a tiny gavel, dangling like a free prize."),
# ACT 3 — vails: the manor, the liner, the cosplay ---------------------------
(20,"XWIDE","-","void", "A long road unrolling backward across an enormous bare cream plain toward a far stone manor house on the horizon, blank milestones shrinking away along it."),
(21,"MED","mouth a firm line, palms up","void", f"{BARISTA} alone on flat cream holding up both empty palms, her mouth a firm line, an enormous accusing shadow-finger falling across the field beside her and missing her completely."),
(22,"XWIDE","-","manor", "A great timbered Tudor manor house on a hill under a low ink-blue sky, ONE carriage crawling up the long drive toward it, rooks lifting from the bare trees."),
(23,"MED","eyes level and careful, bowing","manor", "A departing guest in a fur-collared cloak pressing coins into the open palms of THREE liveried servants lined up by the great door, the nearest servant bowing with his eyes level and careful."),
(24,"XCU","-","manor", "TWO coins dropping downhill through the picture from a gloved hand above into a bare open palm below, the ribbon of a formal bow curling around their fall."),
(25,"WIDE","chin high, eyes half-closed","manor", "An aristocrat sweeping down a great staircase scattering coins behind him with his chin high and his eyes half-closed, servants stooping to gather them in his wake."),
(26,"XWIDE","-","liner", "An Atlantic liner's deck streaming with steam and salt light, wealthy American travellers small at the rail watching the horizon, ONE souvenir trunk between them plastered with blank labels."),
(27,"MED","one brow cocked, practising","liner", "An American traveller on the liner deck practising a lordly coin-press into his own open palm with one brow cocked, checking his posture in a polished brass porthole."),
(28,"WIDE","-","void", f"On ONE long counter running across flat cream, {SCREEN} mid-swivel at one end and a single WHITE-GLOVED open palm rising at the other, one unbroken line of wood joining them."),
(29,"CU","chin high, eyes sliding sideways","void", f"{MAN} in a paper crown two sizes too big pressing ONE coin into a white-gloved open palm, his chin high and his eyes sliding sideways to check who is watching."),
# ACT 4 — America organizes against the tip ----------------------------------
(30,"MED","brows shooting up, mouth falling open","void", f"A colossal rolled broadsheet, completely blank, thudding down onto the cream field beside {MAN}, whose brows shoot up and whose mouth falls open."),
(31,"XWIDE","jaws set, marching","mainstreet1912", f"A 1912 Main Street under bunting, a crowd in straw boaters and cloth caps marching together with their jaws set, completely BLANK boards held aloft, {CUSTOMS}."),
(32,"MED","chin up, beaming","mainstreet1912", f"{CRUSADER} at a trestle table welcoming new members, pressing a pamphlet into the hands of the nearest man with his chin up and beaming, an open ledger of RULED LINES before a queue that runs off the edge of the picture."),
(33,"WIDE","-","data", DATA),
(34,"MED","mouth firm, pressing","capitol", f"In a vast marble hall, ONE clerk at a tiny desk pressing a heavy seal onto a small blank page with his mouth firm, {CUSTOMS} crossing the floor."),
(35,"MED","eyes narrowed, peering down","capitol", "ONE nickel-sized blank coin lying in the middle of the vast marble floor behind a small velvet rope, TWO guards leaning in over it with their eyes narrowed, peering down."),
(36,"MED","mouths open, recoiling","mainstreet1912", "A newsboy holding a completely BLANK broadsheet high over his head, and around him a ring of townspeople recoiling with their mouths open and hands flying to their hats, in the dusty street light."),
(37,"WIDE","mouth wide, mid-cry","mainstreet1912", f"{CRUSADER} up on his soapbox with his mouth wide mid-cry and one fist raised, {SHAFT}, the crowd's straw boaters tilting up toward him."),
(38,"MED","-","void", "THREE small blank coins huddled together on an enormous bare cream field, one colossal accusing finger thrusting into the picture toward them from the edge."),
(39,"MED","brows down, thundering","mainstreet1912", f"A reformer in a high collar holding a thick book with a completely BLANK cloth cover high over his head with both hands, his brows down and mouth thundering to a street crowd, {CUSTOMS} behind him."),
(40,"MED","-","void", "A row of FIVE coins lying along the bottom of the frame, and above each coin ONE fresh crack splitting the smooth cream plaster: five coins, five cracks."),
# ACT 5 — the bans fail ------------------------------------------------------
(41,"MED","eyes down, folding","capitol", f"A clerk in the marble hall quietly folding a small blank page closed and sliding it into ONE drawer among many, his eyes down, dust hanging in the long soft window beams."),
(42,"WIDE","one brow up, mouth helpless","diner", "EIGHT diners at one round table after dinner all mid-tip at once, coins and blank slips crossing in every direction, and ONE towering police officer looming over them with one brow up and his mouth helpless, ONE blank pad dangling forgotten from his hand."),
(43,"WIDE","-","data", DATA),
(44,"MED","eyes huge, bracing","void", f"An enormous coin dropping from the top of the frame toward {MAN}, who looks up into its widening shadow with his eyes huge, bracing, his knees buckling."),
(45,"WIDE","-","void", f"A seesaw on flat cream tipping hard: on the high rising end ONE small tidy blank pay envelope, and crashing down on the low end {SCREEN}, dust puffing out from under the beam."),
(46,"XCU","eyes at the horizon","hotel1890s", f"{WAITER}, the picture cropping hard to his ONE white-gloved open palm at hip height as a coin arrives in it, the gold watch-chain arcing above, {CUSTOMS} catching the glove's seams."),
(47,"XCU","-","capitol", "A gavel striking its block beside ONE small blank coin on the marble, dust jumping at the impact, long soft window beams behind."),
(48,"MED","-","hotel1890s", f"An open drawer lined with velvet, and ONE white glove laid flat inside it, folded and retired, the drawer sliding gently shut in {CUSTOMS}."),
(49,"MED","chin up, eyes fixed forward","void", f"{MAN} and {SCREEN} posed side by side like a formal wedding portrait on flat cream, the man's chin up and his eyes fixed forward, ONE glass jar of coins held between them like a bouquet."),
(50,"MED","eyes resigned in the mirror","taxi", f"The dark back seat of a taxi, {SCREEN} glowing on the partition, {MAN} feeding coins toward it with resigned eyes, and a second pair of eyes watching him in the rear-view mirror."),
# ACT 6 — the Pullman act. PLAYED STRAIGHT: customs light, calm faces,
# nothing overhead, nothing watching, nothing funny. -------------------------
(51,"WIDE","-","pullman", f"A long dark Pullman sleeping car standing at a platform at dusk, its flanks smooth unbroken panels of deep ink-blue painted metal, its windows glowing warm and even, steam drifting low along the wheels, {CUSTOMS} lying across the platform."),
(52,"MED","faces calm and composed","pullman", "A hiring office window at the end of the platform, a line of Black men in neat coats waiting before it with calm composed faces, hats held in their hands, the window's shutter half-raised."),
(53,"MED","face composed, movements exact","pullman", f"{PORTER} smoothing a berth's blanket flat with both hands inside the sleeping car, his face composed and his movements exact, and on the ledge beside him ONE thin pay envelope lying flat and slack."),
(54,"WIDE","face calm, carrying","pullman", f"{PORTER} carrying TWO heavy cases down the narrow corridor of the sleeping car, passengers' doors ajar along one side, his face calm, the window-light crossing him in long soft beams."),
(55,"XCU","-","pullman", "ONE coin resting in the centre of an open work-worn palm, held perfectly steady, the cuff of a dark uniform sleeve with polished buttons at the wrist."),
(56,"CU","eyes weary and composed","pullman", f"{PORTER} at the end of his shift looking at ONE coin in his open palm with weary composed eyes, and beside him on the ledge the thin envelope lying flat and empty."),
(57,"WIDE","mouths moving; face still and composed","pullman", f"Split by a train window: inside, TWO writers in wing collars arguing across a first-class table with their mouths moving; on the platform beyond the glass, {PORTER} lifting cases, his face still and composed, living the answer."),
(58,"MED","-","pullman", "A payroll window shuttered flat, its ledger of RULED LINES closed on the sill, and through the doorway beyond, the platform where cases move from hand to hand in the dusty beams."),
# ACT 7 — the $2.13 law ------------------------------------------------------
(59,"WIDE","eyes down, passing","capitol", "A small folded page travelling hand to hand up a long flight of marble steps between clerks with their eyes down, each hand passing it higher, long soft window beams overhead."),
(60,"MED","-","capitol", "A colossal law book lying open on a marble plinth, its pages RULED LINES, and ONE small blank receipt slip sliding out from between the pages and drifting to the floor."),
(61,"WIDE","-","data", DATA),
(62,"MED","mouth flat, pressing shut","payroll1991", f"A 1991 payroll office: ONE man in a short-sleeved dress shirt and ONE bad wide tie pressing a huge ledger of RULED LINES closed with both hands, his mouth flat, {SHAFT} falling on the ledger, a tiny stack of THREE coins beside it."),
(63,"WIDE","-","data", DATA),
(64,"MED","eyes apologetic; eyes on the middle distance","diner", "A diner booth where a customer's hand tucks folded blank bills straight into a server's ONE apron pocket, his eyes apologetic, her eyes fixed on the middle distance, sun coming through the glass."),
(65,"WIDE","eyes going startled wide","cafe", f"{SHAFT} on the counter as {SCREEN} swivels and a stream of blank payroll slips pours out of it, sliding across the counter into the raised hands of {MAN}, whose eyes go startled wide."),
(66,"MED","-","taxi", f"{SCREEN} glowing alone on a taxi partition in the dark, square to an empty back seat whose cushion still holds the dent of a passenger, the meter's housing dark and completely blank."),
(67,"WIDE","-","barbershop", f"A barbershop of facing mirrors, and in every reflection {SCREEN} waiting beside the chair, slab after slab receding to infinity, each one facing outward, its THREE large blank rounded rectangles repeating away into the glass."),
# ACT 8 — the folklore -------------------------------------------------------
(68,"CU","eyes a decade older, thumb hovering","cafe", f"{MAN} at the counter with his thumb hovering over {SCREEN} and his eyes gone a decade older, ONE bead of sweat sliding down his round face."),
(69,"MED","eyes searching upward","void", f"{MAN} on tiptoe reaching up toward an enormous high shelf that holds ONE massive rolled scroll, his eyes searching upward, his fingertips just brushing the shelf edge."),
(70,"MED","one brow arched; eyes going doubtful","barbershop", "In a barbershop with flat CREAM walls and DUSTY ORANGE trim, a barber pausing mid-cut to lean down and confide in his customer's ear with one brow arched in total confidence, the customer's eyes going doubtful in the mirror, TWO more waiting customers leaning in to hear."),
(71,"CU","eyes flat, unconvinced","barbershop", "The customer's face in the mirror, his eyes flat and unconvinced under his half-cut hair, the barber's confident smile multiplied behind him in TWO facing mirrors."),
(72,"XWIDE","-","void", "A massive scroll unrolled across the entire cream field from edge to edge, blank down its whole length, ONE magnifying glass resting on it mid-search."),
(73,"MED","tongue out, hammering","void", f"{MAN} nailing a small crooked blank plaque onto the base of a stone monument with his tongue out in concentration, THREE bent nails already scattered at his feet."),
(74,"WIDE","jaw tight, eyes coming up into the light","cafe", f"The full hearing in one picture: a single soft-edged column of pale CREAM light falling from directly above, the surrounding cafe a flat darker DUSTY ORANGE-brown, on {MAN}, whose jaw is tight and whose eyes come up into the light, {SCREEN} looming square before him, and behind him {JURY}, the child staring, the grown jurors studying their own fingernails with busy eyes."),
# ACT 9 — Lynn at the diner --------------------------------------------------
(75,"MED","mild permanent surprise, pressing","diner", f"{RESEARCHER} outside the diner window pressing his clipboard flat to the glass, and a booth of THREE diners inside looking back up at him over their coffee."),
(76,"CU","mild permanent surprise, sliding in","diner", f"{RESEARCHER} sliding into a sunlit window booth with his clipboard, coffee arriving in front of him before he asks, sun laying a warm stripe across the table."),
(77,"MED","mild permanent surprise, measuring","diner", f"{RESEARCHER} at the booth measuring everything at once: ONE light meter aimed at the sun, ONE ruler laid along a blank check slip, ONE thermometer standing in his coffee."),
(78,"MED","-","void", "A coffee cup and a single coin standing far apart on flat cream, joined by ONE thin string sagging almost to the ground between them."),
(79,"XCU","-","void", "The middle of that string filling the picture, frayed down to a single fibre, still holding."),
(80,"MED","sweat beading on his brow; friendly eyes","diner", "A diner shrinking down into his booth as an enormous blank check slip unrolls off the table edge toward his lap, sweat beading on his brow, and the server standing very close with her friendly eyes on him."),
(81,"WIDE","mild permanent surprise, pulling","diner", f"{RESEARCHER} at a bank of FOUR tall brass levers behind the diner counter, pulling the smallest one with both hands, as the room's sunlight brightens a full notch."),
(82,"CU","eyes closing warm","diner", "Sunlight flooding the booth as a server rests ONE hand on a diner's shoulder, the diner's eyes closing warm despite himself, her felt-tip pen hovering over the blank slip."),
(83,"MED","eyes on the sunshine, offering","diner", "A diner at the register holding his coins out toward the bright window and the weather beyond it, his eyes on the sunshine, the cashier's open hand waiting patiently beneath the coins."),
(84,"MED","-","void", f"{SCREEN} with a small hatch standing open at its base, revealing the machinery inside: ONE tiny weathervane spinning, ONE coiled spring quivering, and ONE felt-tip pen resting on a little shelf."),
(85,"MED","-","void", "Laid in a row on flat cream: ONE small rain cloud drifting at ankle height, ONE alarm clock with a blank face rattling on its feet, and ONE felt-tip pen lying still, casting the row's longest shadow."),
# ACT 10 — reading the screen right ------------------------------------------
(86,"CU","one eye narrowed, peering","void", f"{MAN} leaning around the back edge of {SCREEN} to peer at its front with one eye narrowed, his body curving into a hook of suspicion."),
(87,"MED","-","void", f"{SCREEN} looming over a small overturned glass tip jar on flat cream, coins spilled in an arc, the slab's flat shadow lying across them."),
(88,"WIDE","-","void", f"ONE heavy chain running across the whole frame, link by link, from the base of {SCREEN} at one end to a single upturned WHITE GLOVE at the other, the chain pulled taut."),
(89,"WIDE","eyes at the horizon; eyes flicking to the palm","hotel1890s", f"{WAITER} holding his ONE white-gloved palm open at hip height in the centre of a full dining room, TWENTY seated diners' eyes flicking to the palm over their soup, {CUSTOMS} down the length of the room."),
(90,"WIDE","chin lifted for the house; head bowed low","stage", f"Under {THEATRE}, on a bare stage: ONE man in evening dress pressing a coin into the open palm of a bowing waiter whose head stays low, the giver's chin lifted for the house, an audience of dark silhouettes filling the black around the light."),
(91,"MED","-","void", f"{SCREEN} and an old glass tip jar standing side by side on flat cream, both upright and intact, the jar's coins catching the same light as the slab's THREE large blank rounded rectangles."),
(92,"MED","-","void", f"The single WHITE GLOVE and {SCREEN} facing each other on flat cream, the glove dropping empty to the ground between them while the slab's glow carries on flat and even."),
(93,"WIDE","-","void", f"{SCREEN} alone under {SHAFT} on a bare cream field, square to the front, its THREE large blank rounded rectangles glowing evenly, the darker field around the light lying flat and calm."),
# ACT 11 — the mercy ---------------------------------------------------------
(94,"WIDE","every pair of eyes a shade softer","cafe", f"The whole counter again in warmer light: {MAN} before {SCREEN}, {BARISTA} behind the counter, {JURY} behind him, every pair of eyes in the room a shade softer, steam finally rising from the machine."),
(95,"MED","eyes aimed elsewhere; child staring","cafe", f"{JURY} in a row behind {MAN}, the FIVE grown jurors aiming their eyes at the ceiling, the floor, a fingernail, a shoe and a blank-faced wristwatch, and the ONE child staring straight ahead."),
(96,"CU","eyes drifting, lips moving","cafe", "The five jurors' faces in a loose row, every pair of eyes drifting somewhere harmless, ONE juror counting the ceiling tiles with silently moving lips."),
(97,"CU","eyes fixed carefully forward","cafe", "Along the queue, FIVE thumbs down at FIVE coat seams each giving one small secret practice press, the jurors' eyes fixed carefully forward, the child's thumb practising hardest of all."),
(98,"WIDE","thumb frozen; eyes ferociously studying","cafe", f"Both halves in one picture: {MAN}'s thumb frozen over {SCREEN} in the foreground, and behind him {JURY}, all FIVE grown jurors bending to study the pastry case with ferocious eyes, the child staring straight at the slab."),
(99,"WIDE","knuckles tight, eyes ahead","barbershop", f"{JURY} reflected in TWO facing barbershop mirrors, the queue multiplying away to infinity, every reflected juror gripping a hat or a strap with tight knuckles and eyes ahead, every reflected child staring."),
(100,"MED","eyes lifted politely away","cafe", f"{BARISTA} behind the counter with her eyes lifted politely into the middle distance, her hands folding a cloth into smaller and smaller squares, {MAN} at the edge of the picture pressing on alone."),
(101,"MED","eyes neutral, formal","cafe", f"{BARISTA} performing the quarter-turn: both hands on {SCREEN}, rotating it with a bailiff's formality, her eyes neutral, her ONE front pocket holding its TWO pens exactly level."),
(102,"MED","brows lifted, palms open","void", f"{BARISTA} standing beside an unrolled blueprint of RULED LINES with {SCREEN} planted on top of it, holding up both open palms, her brows lifted in plain deniability."),
(103,"CU","mouths pressed into the same flat line","cafe", f"{MAN} and {BARISTA} looking at each other across {SCREEN}, both mouths pressed into the same flat embarrassed line, and between them ONE coin standing on edge in the middle of the counter, mid-roll toward her side."),
(104,"MED","mouths matching flat lines","void", f"{MAN} and {BARISTA} standing on either side of {SCREEN} on bare cream, each raising one hand palm-out in the same disowning gesture, their mouths matching flat lines."),
(105,"CU","blushes rising, eyes down and away","void", f"{MAN} and {BARISTA} cropped to their two faces side by side, each looking down and away from the other, matching blushes rising on both sets of cheeks."),
(106,"MED","eyes lifting past the slab","cafe", f"{MAN} pressing ONE of the THREE large blank rounded rectangles of {SCREEN} with his thumb while his eyes are already lifting past the slab's top edge to {BARISTA} beyond it, her eyes coming up to meet his."),
(107,"WIDE","-","void", "Rising off the top of the frame on FOUR thin strings: ONE blank button, ONE mustard sash, ONE white glove and ONE coin cased in a block of ice, each lifting away and leaving the cream field clearer."),
(108,"XCU","-","void", "At the bottom of the cleared cream field, ONE small plain coin resting alone, warm-toned, casting one soft small shadow."),
(109,"MED","eyes kind, wishing well","void", f"{MAN} and {BARISTA} facing each other on plain cream, each raising a hand in a small wave, the man's kind eyes wishing her well, ONE coin passing between them along the bottom of the picture."),
(110,"XWIDE","-","nightstreet", "ONE lit cafe window glowing alone in a dark street, TWO small figures inside it at the counter mid-hand-over, the warm light spilling out across the wet pavement."),
(111,"MED","-","void", "ONE small folded paper boat riding low in a thin painted stream, loaded far past its gunwales with a towering stack of blank payroll slips, water lapping at its folds."),
(112,"WIDE","-","capitol", f"TWO empty podiums set facing each other in the vast marble hall, waiting, {CUSTOMS} crossing the floor between them, ONE folded blank page lying ready on each podium."),
(113,"MED","eyes on each other","void", f"{MAN} and {BARISTA} standing together at one side of the frame with their eyes on each other, and far away at the frame's other edge TWO tiny podiums facing off by themselves."),
(114,"MED","eyes even and steady","void", f"{MAN} and {BARISTA} each holding one end of a single long blank receipt strip stretched taut between them, holding it level, their eyes even and steady."),
(115,"MED","eyes warm over the steam","cafe", f"{BARISTA} setting ONE paper cup of coffee into {MAN}'s waiting hands across the counter, steam rising between their faces, her eyes warm, {SCREEN} out of the exchange at the far edge of the frame."),
(116,"CU","eyes up and meeting hers, small true smile","cafe", f"{MAN} cropped close with the cup held at his chest, a small true smile arriving, his eyes up and meeting hers as his mouth shapes a thank-you."),
(117,"WIDE","eyes ahead, walking home","nightstreet", f"{MAN} walking home along the dark shuttered street with the cup warm in both hands and his eyes ahead, and in every dark shop window ONE faint glowing slab with THREE large blank rounded rectangles hanging pale in the pane."),
(118,"XWIDE","-","void", "ONE small coffee cup standing far off-centre on an enormous bare cream field, its thin line of steam the only rising thing in the picture."),
(119,"XWIDE","every face turned forward","void", f"ONE long queue running across the whole cream field, everyone in it waiting together: {MAN}, then {BARISTA}, then {JURY}, then {WAITER}, then {CRUSADER}, then {RESEARCHER}, then {PORTER}, every face turned forward, each figure keeping careful faith with the back ahead of them."),
]

# ============================================================================
# SECOND FRAMES — every sentence over 25 words carries two pictures so the
# hold stays under ~9s at 161wpm. map-shots.py splits the sentence's span
# evenly across the frames beneath it.
# ============================================================================
EXTRA = {
 32: [("XWIDE","-","mainstreet1912", "A queue of new members stretching the whole length of Main Street and around the far corner, hats of every class bobbing along it, bunting swinging overhead in the dusty light.")],
 39: [("XCU","-","mainstreet1912", "The thick book filling the picture, held aloft in TWO hands, its cloth cover completely BLANK, its page edges worn soft from many thumbs.")],
 45: [("MED","eyes at the horizon, unbending","hotel1890s", f"{WAITER} walking away down a chandeliered corridor with ONE fat blank pay envelope tucked under his arm and his tray retired flat under the other, {CUSTOMS} behind him.")],
 53: [("CU","eyes down, steady","pullman", "A paymaster's grille at the corridor's end, ONE thin blank envelope sliding under it into a waiting open hand, the man's eyes down and steady, the ledger of RULED LINES open behind the grille in the dusty beams.")],
 62: [("WIDE","mouths satisfied, filing out","payroll1991", "The same huge ledger now wrapped in a heavy chain with ONE fat padlock, and THREE men in good suits filing out of the office door with satisfied mouths, their briefcases swinging.")],
 65: [("XCU","-","cafe", "Blank payroll slips crossing the wooden counter line in a sliding fan, the leading slip tipping over the counter's edge into an open waiting hand.")],
 74: [("XCU","-","cafe", "ONE small thumb hovering a coin's width above THREE large blank rounded rectangles, trembling slightly, lit from below by the slab's pale warm CREAM glow, the field around the slab a deep warm brown.")],
 82: [("XCU","-","diner", "A felt-tip pen touching down on a blank check slip, ONE loose friendly curve already begun, warm sunlight lying across the paper.")],
 111:[("MED","-","payroll1991", f"The huge 1991 ledger of RULED LINES lying open under {SHAFT}, and resting in the crease between its pages, ONE tiny folded paper boat.")],
 119:[("MED","small nods passing down the line","void", "The same queue seen closer at waist height: each person's hand steadying the elbow of the person ahead, a chain of small braced kindnesses running the whole length of the line, small nods passing down it.")],
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
 "own dominant colour from that set. Expressions are BOLD, exaggerated and readable at a "
 "glance. Visible gouache texture, flat matte, NO gradients, NO airbrushed shading, NO "
 "photographic texture, NO three-dimensional rendering. There is NO text, NO lettering, NO "
 "numbers and NO writing of any kind anywhere in the image; any sign, board, placard, label, "
 "badge, sash, page or screen is completely BLANK. Any crowd is individuated: different faces, "
 "different builds, clothes in DIFFERENT colours from the palette, never a row of matching "
 "coats. These are ORIGINAL characters in a general mid-century cartoon idiom: NO existing "
 "cartoon characters, NO studio logos, NO trade dress, and no likeness of any real person. "
 "ONE SINGLE COHERENT SCENE, NOT a grid of panels, NOT a sheet of studies. 16:9, edge to "
 "edge, one scene, one camera.")

WPM = 161
MAX_HOLD = 9.6
MIN_CAM = {'XCU': 10, 'CU': 12, 'XWIDE': 8}
MAX_RUN = 3
MIN_CU_SHARE = 0.20
MIN_EVENT_SHARE = 0.85
CAFE_MAX_SHARE = 0.20
CORE_ENVS = {'cafe','hotel1890s','liner','mainstreet1912','capitol','diner','payroll1991',
             'taxi','barbershop','nightstreet','void','data'}

FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|cheeks|'
                  r'tongue|chin|frown|blank|soft|hard\b|calm|composed|weary|star(e|ing)|blush|'
                  r'surprise|nod|dread|faces?\b', re.I)
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
    r'perform|plant|rise|rising|casc|cascade|flick|aim|stagger|clip|mid-roll|steady|repeat',
    re.I)
CAST = re.compile(r'THE MAN|BARISTA|THE JURY|GRAND WAITER|CRUSADER|RESEARCHER|THE PORTER|'
                  r'man\b|men\b|woman|women|people|crowd|guest|servant|aristocrat|traveller|'
                  r'clerk|guard|newsboy|reformer|officer|diners?\b|server|customer|barber|'
                  r'child|jurors?|figures?|writers?|passenger|cashier|waiter|porter', re.I)

# COUNTS, NOT NOUNS — a scene that stages a character or the slab must carry
# the numeric words. A reference sheet is not sufficient.
REQ = {
 'VERMILION RED coat':  ['TWO kinked hairs', 'THREE round buttons'],
 'THE BARISTA':         ['ONE front pocket', 'TWO pens', 'ONE pencil'],
 'THE JURY':            ['FIVE', 'ONE staring child'],
 'GRAND WAITER':        ['TWO points', 'ONE white glove'],
 'THE CRUSADER':        ['MUSTARD GOLD sash'],
 'THE RESEARCHER':      ['THREE buttons'],
 'Pullman porter':      ['TWO neat rows'],
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
slabless = [i for i, s in enumerate(S, 1) if not isdata[i-1]
            and re.search(r'\bslab\b', s[4], re.I)
            and 'THREE large blank rounded rectangles' not in s[4]]
if slabless:
    errs.append('slab staged with its rectangle counts missing: ' +
                ' '.join('b%03d' % i for i in slabless[:8]))

# OMISSION, NOT NEGATION — reject negation describing visual content.
NEG = re.compile(r"\bno\s|\bwithout\b|n't\b", re.I)
neg = [i for i, s in enumerate(S, 1) if not isdata[i-1] and NEG.search(s[4])]
if neg:
    errs.append('negation in scene text: ' + ' '.join('b%03d' % i for i in neg[:10]))

# SIGN-SHAPED OBJECTS — no scene may request written content.
SIGNS = re.compile(r'\b(letter|letters|lettering|lettered|word|words|writing|written|writes|'
                   r'text|texts|number|numbers|numeral|numerals|digits?|caption|inscrib\w*|'
                   r'font|typeface|says|reading\b|reads\b)\b', re.I)
signy = [i for i, s in enumerate(S, 1) if not isdata[i-1] and SIGNS.search(s[4])]
if signy:
    errs.append('scene requests written content: ' + ' '.join('b%03d' % i for i in signy[:10]))

# ENVIRONMENT CAP — the cafe stays under 20%; every core environment appears.
setc = Counter(s[3] for s in S)
if setc['cafe'] / len(S) > CAFE_MAX_SHARE:
    errs.append(f'cafe is {setc["cafe"]}/{len(S)} ({setc["cafe"]/len(S):.0%}), '
                f'max {CAFE_MAX_SHARE:.0%}')
unused = sorted(CORE_ENVS - set(setc))
if unused:
    errs.append(f'core environments unused: {unused}')

# TRIBUNAL ACCENTS — theatre on at most 2 setpieces.
theatre = [i for i, s in enumerate(S, 1) if re.search(r'spotlight', s[4], re.I)]
if len(theatre) > 2:
    errs.append(f'THEATRE accent on {len(theatre)} frames; max 2: ' +
                ' '.join('b%03d' % i for i in theatre))

# THE PULLMAN ACT (51-58) IS PLAYED STRAIGHT — customs light, calm faces,
# nothing overhead, nothing watching, nothing funny.
STRAIGHT = re.compile(r'shaft|jury|juror|spotlight|column of lighter value|ABSURD|COLOSSAL|'
                      r'ENORMOUS|cartoon|grin|bulging|comically', re.I)
pull = [i for i, s in enumerate(S, 1) if 51 <= s[0] <= 58
        and (STRAIGHT.search(s[4]) or STRAIGHT.search(s[2]))]
if pull:
    errs.append('the Pullman act broke its straightness: ' + ' '.join('b%03d' % i for i in pull))

cast = [s for s in live if CAST.search(s[4])]
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(live)} ({cu/len(live):.0%}) | faces "
      f"{len([s for s in live if s[2]!='-'])}/{len(live)} | events "
      f"{len(live)-len(noev)}/{len(live)} | cast {len(cast)}/{len(live)} "
      f"({len(cast)/len(live):.0%}) | data {ndata} | holds {sum(holds):.0f}s/{budget:.0f}s")
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
# generator: the first batch sent them and the model drew the sentinel text,
# burning retries against the glyph gate. Excluded at the source.
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{CAM[s[1]]} {strip_cam(s[4])} {WORLD}'
     for i, s in zip(ids, S) if s[4] != DATA}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'expression': s[2], 'setting': s[3],
      'line': sents[s[0] - 1], 'scene': s[4],
      'hold_est_s': round((len(sents[s[0]-1].split()) / WPM * 60) / per_line[s[0]], 2)}
     for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S) if s[4] == DATA or not (
    'VERMILION RED coat' in s[4] or 'THE BARISTA' in s[4] or 'THE JURY' in s[4] or
    'GRAND WAITER' in s[4] or 'THE CRUSADER' in s[4] or 'THE RESEARCHER' in s[4] or
    'Pullman porter' in s[4])]
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
