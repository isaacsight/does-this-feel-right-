#!/usr/bin/env python3
"""Frame book — First Come, First Served. v3. LITERAL, EXAGGERATED, POPULATED.

WHY V3. The v2 cut was rejected on four counts, all of them mine, all of them
measurable in the board that produced it:

  repetitive     79 of 102 scenes contained a queue; 55 said "standing"
  no expression  ZERO frames named a face part. Not one, in 102 frames
  no feeling     53 frames named no expression at all, and of the rest 57% were
                 deliberately bland — because the world clause TOLD them to be.
                 I theorised that a blank face would make the scratched marks
                 funnier by contrast, and so engineered blankness into the
                 protagonist for eight minutes
  the squiggles  the second-medium idea communicated nothing to a viewer. It was
                 conceptually neat and it was decoration. It is gone entirely

That is the SECOND board in a row where I reasoned my way out of the thing that
works. On the underdog episode the board carried a regex BANNING the comedian's
vocabulary; here it banned the face. The two episodes Isaac liked are full of
absurdly wide eyes, mouths open mid-protest and brows shot off the head.

THE V3 RULE: paint WHAT IS SAID, as a physical event, pushed past realism, with
a specific face doing a specific thing, somewhere new, with somebody else in it.
Exaggerated AND literal at the same time — that is how a viewer connects the
voice to the picture.

  LITERAL     the sentence's own noun is in the frame. Temperature -> a bursting
              thermometer. Arithmetic -> a chalkboard of sums. Police -> a
              policeman. The thing itself, not a metaphor for it
  EXAGGERATED it is a cartoon EVENT — bursting, popping, streaming, toppling,
              collapsing — never a state, and never "standing"
  FACE        eyes, brows, mouth, jaw or lips, named, in every frame with a person
  POPULATED   other characters, doing something to him or near him
  ELSEWHERE   the environments change constantly and the queue is capped, so the
              episode travels instead of circling one shop

All five are checked below, because a rule I merely intend is a rule I have now
twice drifted out of.

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

HERO = ("the recurring character in mid-century cartoon style: a small slight man with "
        "a round young face and a big confident nose, EXACTLY TWO hairs sticking up from "
        "the crown that KINK and LEAN at different angles and are different lengths, a "
        "flat VERMILION RED coat, thin stick legs and ABSURDLY oversized shoes, drawn "
        "with a strong readable silhouette and a confident tapering ink outline")

CUTTER = ("THE SECOND MAN: a pleasant unremarkable middle-aged man in a sage green "
          "raincoat and a soft hat, completely oblivious, never smug and never a villain")

# (line, camera, face action or '-', scene)
S = [
# ACT 1 — the most powerful law you have ever obeyed -------------------------
(1,"WIDE","eyes wide, jaw dropped", f"On a windswept clifftop {HERO} stares up at an ENORMOUS stone tablet twice his height that has cracked clean down the middle, his eyes ABSURDLY wide and his jaw dropped to his chest, while a goat calmly chews the bottom corner of it."),
(2,"MED","asleep, mouth open, snoring", "Inside a police station a fat policeman sleeps with his hat over his face and his boots up on the desk, mouth hanging open mid-snore, a fly settling on his lip, while through the window behind him TWELVE people wait in a perfect orderly line down the street."),
(3,"XCU","-", "EXTREME CLOSE-UP on a COLOSSAL contract whose signature space is completely empty, and a tiny cartoon pen lying beside it snapped clean in half, ink leaking out."),
(4,"WIDE","-", "An ENORMOUS empty courtroom where a cobweb stretches between the judge's gavel and the bench, a mouse curled asleep in the witness box and dust drifting through a shaft of light."),
(5,"CU","eyes bulging, teeth bared", f"CLOSE on {HERO}'s face erupting — eyes bulging, teeth bared, both hairs shot bolt upright, steam whistling from both ears — as a stranger's elbow slides into the frame in front of him."),
(6,"WIDE","brows up, mouth pursed", f"{HERO} crouching to peer under an ENORMOUS forest of queueing legs with a magnifying glass, brows up and mouth pursed with concentration, while the people above him carry on chatting and one drops a glove on his head."),
# ACT 2 — third, and at peace ------------------------------------------------
(7,"MED","eyes half closed, humming", f"Inside a warm bakery {HERO} waits third in a line of SIX, behind a fat woman in a bonnet and a man with a dachshund, his eyes half closed and lips pursed in a hum, a tray of buns steaming on the counter."),
(8,"WIDE","-", "A cheerful cartoon bakery interior in full detail: the baker sliding a tray out of the oven, a cat asleep on a flour sack, a child pressed flat against the glass counter with both palms and a squashed nose."),
(9,"CU","yawning enormously", f"CLOSE on {HERO} yawning ABSURDLY wide with his eyes squeezed shut and his tongue curled, so relaxed that his hat is sliding off the back of his head."),
(10,"CU","eyebrows raised, shrugging", f"{HERO} shrugging ENORMOUSLY with both palms up and eyebrows raised at the dachshund, which stares back at him, while the fat woman ahead counts out coins."),
(11,"WIDE","eyes closed, blissful", f"{HERO} leaning back against the bakery counter with his eyes closed and a blissful smile, one leg crossed over the other, under a clock whose hands are both drooping like wet string."),
# ACT 3 — THE INTRUSION ------------------------------------------------------
(12,"WIDE","mouth open, eyes popping", f"{CUTTER} striding up the side of a bakery queue of SIX people and inserting himself at the second position with a pleasant nod, while behind him {HERO}'s mouth falls open and his eyes pop clean forward, one enormous shoe lifting off the floor."),
# ACT 4 — the body reacts ----------------------------------------------------
(13,"CU","eyes crossing, hair rising", f"CLOSE on {HERO} as his whole face goes taut — eyes crossing, both hairs rising, collar buttons pinging off across the frame — with one hand clamped hard over his own mouth."),
(14,"XCU","teeth gritted, eyes watering", f"EXTREME CLOSE-UP on {HERO} with a thermometer in his mouth BURSTING, mercury shooting out of the top and splattering the ceiling, his teeth gritted and his eyes watering."),
(15,"CU","eyes bulging in time", f"{HERO} second in a bakery line of SIX as his shirt front thumps out a full inch with every heartbeat, buttons popping off across the counter, his eyes bulging in time, while the baker calmly wraps a loaf and notices nothing."),
(16,"CU","one eye twitching", f"CLOSE on {HERO} with an ENORMOUS chalkboard of frantic arithmetic hovering above his head, chalk dust pouring off it, one eye twitching violently while his mouth holds a polite little smile."),
# ACT 5 — 1837, and Carlyle --------------------------------------------------
(17,"WIDE","-", "A grand Parisian boulevard in the 1790s where an ENORMOUS powdered aristocrat in a wig is carried bodily over the heads of a shouting crowd toward a bakery door, wig flying, nobody polite anywhere in the frame."),
(18,"WIDE","brows knitted, tongue out", "A whole candlelit study seen from across the room: a bearded Scotsman in a nightshirt at a desk under a tall window, his FULL HEAD and shoulders well inside the frame, scribbling furiously in a ledger with brows knitted and tongue between his teeth, ink spraying off the nib, a candle guttering beside him, and through the window TWELVE people queueing in the street below."),
(19,"XWIDE","-", "A VAST cold Paris street at dawn: DOZENS of gaunt people in shawls waiting in a perfect patient line that snakes around three corners, one baker handing out a single loaf, a dog asleep in the gutter."),
# ACT 6 — it arrived because of scale ----------------------------------------
(20,"MED","scowling, teeth bared", "Two ENORMOUS cartoon women in bonnets elbowing each other viciously at a market stall, both scowling with teeth bared, cabbages flying through the air while a stallholder ducks under his own counter."),
(21,"WIDE","-", "A thundering Victorian railway platform where a locomotive erupts steam across the whole frame and DOZENS of top-hatted passengers pour out of every door at once, hats sailing off their heads."),
(22,"WIDE","-", "A gigantic factory gate bursting open at shift change, HUNDREDS of workers streaming out in a single wave, lunch pails swinging, one man carried along entirely off his feet."),
(23,"MED","laughing, mouths open", "A sleepy medieval village square where TEN neighbours amble about a well chatting and laughing with no line at all, two of them laughing with their mouths open, a baby on a hip, a chicken strolling through."),
(24,"WIDE","grinning, smug", "A cramped market where one grinning man shoves three smaller people bodily out of his way, a second man drops a COLOSSAL gold coin into a merchant's raised palm, and a uniformed servant waits patiently in a line of FIVE holding his master's hat."),
(25,"XWIDE","-", "A VAST concourse where TWO HUNDRED tiny figures pour in through six entrances at the same moment and collide in the middle, luggage cartwheeling into the air."),
(26,"MED","grinning, arms folded", "A tiny village bakery where TEN neighbours stand about chatting with no line at all, one leaning on the counter, the baker grinning with his arms folded."),
(27,"XWIDE","-", "A VAST railway platform under a glass roof with TWO HUNDRED commuters arriving in one surge as an ABSURDLY large station clock strikes above them, everyone moving at once and nobody able to sort it out."),
# ACT 7 — infrastructure, not manners ----------------------------------------
(28,"CU","mouth flat, half-lidded", f"CLOSE on {HERO} holding a lace doily up beside his face with a completely flat mouth and half-lidded eyes, entirely unimpressed by it."),
(29,"WIDE","chest out, chin up", f"{HERO} on a girder in a hard hat with his chest out and chin up, directing a crane that is lowering an ENORMOUS steel beam into place across a construction site while workers below crane their necks."),
(30,"MED","-", "A cartoon machine the size of a house, all brass funnels and levers, into which a jostling crowd walks at one end and out of which they emerge in a neat single file of TEN, an operator hauling on a lever with both feet off the ground."),
(31,"CU","wincing, one eye shut", f"CLOSE on {HERO} wincing with one eye shut and teeth bared as an ancient woman with a walking frame is overtaken in the line by a boy on a scooter."),
(32,"WIDE","brows up, mouths moving", f"DOZENS of people in a queue all craning their necks and pointing to count their own positions, mouths moving, {HERO} among them counting on his fingers with his brows shot up."),
# ACT 8 — nobody is in charge ------------------------------------------------
(33,"MED","glaring sideways, jaw set", f"{HERO} third in a bakery queue of SIX people, glaring sideways with his jaw set at {CUTTER}, who is cheerfully turning a bun over and noticing nothing at all."),
(34,"WIDE","-", "An ENORMOUS empty guard's booth in the middle of a busy street with its door swinging open and a whistle hanging unused on a nail, while TEN people file past it in a perfectly orderly line."),
# ACT 9 — Milgram, 1986 ------------------------------------------------------
(35,"CU","peering, brows furrowed", "Two researchers in white coats crouching behind a potted plant in a station, peering through binoculars with their brows furrowed and clipboards clamped under their arms."),
(36,"XWIDE","-", "A VAST 1980s New York ticket hall packed with DOZENS of separate queues, and one researcher on a rope being lowered from the ceiling with a clipboard to count them all."),
(37,"CU","mouth mid-sentence, bland", "CLOSE on a plain-faced man in a jacket saying four words with a completely bland mouth and one hand raised in a small apologetic gesture."),
(38,"WIDE","-", "A cartoon heap of everything the intruder did NOT bring: a crutch, a completely blank sob-story placard, a bunch of flowers and a violin, all lying discarded on the floor beside his feet."),
# ACT 10 — what actually happened --------------------------------------------
(39,"WIDE","straining, teeth bared", "TEN people in a line leaning like a rope in a tug of war, everyone straining backwards with teeth bared and heels dug in to hold their positions, while an intruder steps calmly into the middle of it."),
(40,"MED","fierce eyes, arm out", "One furious woman with fierce eyes throwing an arm out like a level-crossing barrier to block an intruder, while NINE people behind her stare determinedly at the ceiling."),
(41,"XCU","-", "EXTREME CLOSE-UP on a COLOSSAL pie made of actual pastry with one thin slice cut out of it, a fork stabbed upright into the small piece."),
(42,"CU","eye-rolling enormously", "CLOSE on a commuter performing an ABSURDLY large eye-roll, eyes rolling right back into his head, his face snapping instantly afterwards to total neutrality."),
# ACT 11 — the enforcement arm is a noise ------------------------------------
(43,"CU","leaning in, brows up", f"{HERO} leaning ENORMOUSLY far toward the viewer with both brows up and one finger raised, a spotlight snapping onto him in a dark room."),
(44,"WIDE","-", "An ENORMOUS muscular arm reaching down out of the clouds to hold up a VAST stone building — and at the end of the arm, where the fist should be, is a tiny pair of pursed lips."),
(45,"XCU","lips pursed, tiny puff", "EXTREME CLOSE-UP on a pair of lips pursed absurdly tight releasing one tiny puff of air, and twelve feet away a single leaf drops off a plant."),
(46,"WIDE","shrugging, backs turned", "Half a cartoon crowd shrugging ENORMOUSLY with palms up while the other half simply have their backs turned, one man visibly whistling at the sky."),
# ACT 12 — front and back ----------------------------------------------------
(47,"WIDE","-", "A line of TWELVE people sliced down the middle by a wall: on the front side people lounge in deckchairs with sunglasses and cold drinks, on the back side people are scarlet-faced and gripping the barrier with both fists."),
(48,"CU","serene, eyes closed", "CLOSE on the man at the very front of a line of TWELVE serenely sipping tea with his eyes closed and his little finger raised, entirely at peace with the world."),
# ACT 13 — two intruders -----------------------------------------------------
(49,"MED","delighted, brows raised", "A researcher in a white coat grinning with delight and raised brows as he hauls down an ENORMOUS unmarked brass lever with both hands."),
(50,"WIDE","mouths open, arms up", "TWO identical men in jackets stepping side by side into the front of a single-file line of TWELVE people waiting at a shop door, and every one of the TWELVE behind them leaning bodily out of the line to shout forward at them, ANGRY SCOWLING faces with eyebrows slammed down and mouths open mid-protest, one hat flying off. They stay in their line. This is a queue objecting, NOT a protest march: no placards, no raised fists, nobody happy and nobody celebrating."),
(51,"XCU","-", "EXTREME CLOSE-UP on a COLOSSAL brass pressure gauge with its needle slammed hard against the top of the dial and the glass cracking across."),
# ACT 14 — what we are actually defending ------------------------------------
(52,"CU","one brow up, sly", f"CLOSE on {HERO} with one brow up and a sly sideways look, slowly turning an ENORMOUS blank card over in both hands."),
(53,"CU","eyebrows tilted up, apologetic", "A flustered man with his hat crushed in both hands and his eyebrows tilted up in apology, having plainly not seen the line of NINE people he has walked into, while they visibly soften."),
(54,"WIDE","mouths open, scrambling", "A line of TWELVE people disintegrating completely into a scrambling ANGRY free-for-all, people clambering over each other with teeth bared and eyebrows down, hats and shoes in the air, one man riding another's shoulders."),
(55,"WIDE","jaws set, linking arms", "DOZENS of people linking arms with fierce set jaws to form a human chain across a street, one small dog linking in at the end with its paw."),
(56,"CU","mouth set, finger wagging", f"CLOSE on {HERO} shaking his head firmly with his mouth set and one finger wagging, standing in front of an ENORMOUS completely blank sign."),
(57,"WIDE","mouths open, gripping", "A cartoon crowd all grabbing the edges of a VAST tablecloth as it starts to slide off a table, every mouth open in alarm, plates already tipping into the air."),
# ACT 15 — the choice --------------------------------------------------------
(58,"MED","sweating, eyes darting", f"{HERO} at a fork in a road under an ENORMOUS blank signpost, sweat flying off his face in droplets, both eyes darting in opposite directions."),
(59,"CU","mouth opening, resolute", f"CLOSE on {HERO}'s mouth beginning to open and one finger rising, his eyes fixed with sudden resolve."),
(60,"WIDE","eyes wide, knees buckling", f"{HERO} caught mid-sentence with one finger raised on a brightly lit stage while NINE people in the audience stare directly at HIM with folded arms, a spotlight burning down, his eyes wide and his knees buckling."),
(61,"CU","smiling, seething", f"{HERO} smiling with his mouth clamped shut while smoke pours from both ears and his two hairs vibrate, keyed to a warm dusty ORANGE bakery interior, with {CUTTER} just behind his shoulder examining a bun and noticing nothing."),
# ACT 16 — THE TUT -----------------------------------------------------------
(62,"WIDE","-", "DOZENS of ordinary people in a bakery queue all doing precisely nothing with enormous commitment, examining ceilings, shoes and fingernails."),
(63,"XCU","lips pursed, nostril flaring", f"ONLY the lower half of {HERO}'s face — his pursed lips, chin and one flaring nostril FILL THE WHOLE FRAME, his eyes ABOVE the top edge and not visible at all. Keyed to flat sage GREEN. Nothing else is in the picture."),
(64,"CU","one small tut", f"{HERO} completing a single tiny tut, one thin sound-ripple travelling away from his mouth right across a crowded INK BLUE shop interior where SIX other people carry on entirely unmoved, everything about him snapping instantly back to normal."),
(65,"CU","brows tilting, sheepish", f"{HERO} small and alone on a wide mustard GOLD pavement making the noise a moment too late, his brows tilting sheepishly, while {CUTTER} is already half out of the far side of the frame carrying his bun away."),
# ACT 17 — the noise IS the system -------------------------------------------
(66,"CU","brows up, dawning grin", f"{HERO} looking straight at the viewer with both brows up and a dawning delighted grin, a lightbulb popping on above his head and throwing light across a cream and INK BLUE street where TWELVE people queue behind him, all facing the other way."),
(67,"XCU","-", "A tiny pair of pursed red lips resting on a COLOSSAL mustard GOLD velvet cushion beneath a clear glass dome on a cream plinth, in a bright cream museum room, lit like a crown jewel. The painted scene runs right to all four edges of the picture: there is NO border, NO frame and NO black bar down any side."),
(68,"WIDE","-", "A VAST cartoon machine room where DOZENS of small pursed mouths on brass stands tut in sequence, driving an ENORMOUS flywheel that powers a whole city."),
(69,"MED","unimpressed, flat mouths", "A cartoon knight in full armour charging up on a horse with a lance raised, and a line of TEN ordinary people simply looking at him with flat unimpressed mouths."),
(70,"XWIDE","tutting, endless", "DOZENS of ordinary people stretching away to the horizon, every single one of them making the same tiny disapproving mouth, one small puff of air leaving each."),
(71,"MED","brows raised, easy", f"{HERO} stepping easily over a limbo bar set six inches off the ground with his brows raised, while an ENORMOUS high-jump bar towers unused behind him."),
# ACT 18 — what it costs to run ----------------------------------------------
(72,"XCU","-", "EXTREME CLOSE-UP on a COLOSSAL cash register drawer springing open to reveal one single small coin rolling around inside it."),
(73,"WIDE","asleep, snoring", "The same fat policeman asleep at his desk with his hat over his face, snoring so hard the papers lift off the desk, while outside the window TWELVE people wait in a perfect line."),
(74,"MED","-", "A security camera hanging off a wall by its own wires with a bird's nest built inside the housing and three chicks looking out of it."),
(75,"WIDE","-", "An ENORMOUS ticket barrier standing wide open and unattended in the middle of an empty field, while TEN people file politely through it anyway."),
(76,"CU","cheeks pink, sheepish", "CLOSE on an ordinary man going pink in the cheeks with an embarrassed sheepish grimace, one hand rubbing the back of his neck."),
(77,"WIDE","-", "A cartoon set of scales with a COLOSSAL gleaming marble institution on one pan and one tiny pursed mouth on the other, and the tiny mouth is dragging its pan to the floor."),
# ACT 19 — everywhere else ---------------------------------------------------
(78,"MED","brows up, noticing", f"{HERO} walking down a busy street with his brows up and mouth open, suddenly noticing dozens of tiny courtesies happening around him at once."),
(79,"CU","mouth half-smiling, eyes glazing", "A man holding a heavy door open with his foot and elbow while FOUR people file through, his mouth half-smiling and his eyes glazing over as a fifth appears in the distance."),
(80,"XCU","three pairs of eyes watching", "EXTREME CLOSE-UP on a hand hovering over ONE last biscuit on a plate, with three pairs of eyes visible at the edges of the frame all watching it."),
(81,"WIDE","-", "A VAST escalator where every single person stands neatly to one side, and the one man walking up the empty side has an ENORMOUS spotlight following him from nowhere."),
(82,"MED","-", "A TINY brass doorstop no bigger than a thumb sitting alone in the middle of a COLOSSAL cream marble pedestal in a bright grand hall, with TEN ordinary people gathered round it gazing up with their mouths open and their hats held to their chests, exactly as if they were standing at a great monument."),
(83,"WIDE","-", "A cutaway of an ENORMOUS building whose load-bearing columns are built out of stacked tiny pursed mouths, all tutting quietly, holding the whole structure up."),
# ACT 20 — be fair to the man who cut ----------------------------------------
(84,"CU","brows raised, hands up", f"{HERO} holding both hands up in a fair-minded gesture with his brows raised, standing beside {CUTTER}, who is still turning his bun over."),
(85,"CU","sneering, lip curled", "CLOSE on a genuinely awful cartoon man sneering with a curled lip and narrowed eyes as he deliberately treads on somebody's foot."),
(86,"WIDE","exhausted, eyes vacant", f"{CUTTER} trudging through pouring rain with his shoulders down and his eyes vacant, soaked to the skin, having plainly had the worst day of his life, walking straight past a queue of TEN he has not seen."),
(87,"XCU","-", "A man holding up an ENORMOUS brass ruler as long as he is tall and squinting along its edge with one eye shut, his mouth pursed — and the whole face of the ruler is smooth and completely BLANK, with no markings and no engraving of any kind on it."),
(88,"CU","gentle, brows soft", f"CLOSE on {HERO} with a gentle level face and soft brows, shaking his head very slightly."),
# ACT 21 — so what do we do --------------------------------------------------
(89,"CU","brows raised, palms up", f"{HERO} turning to the viewer in an empty windswept plain with both palms up and his brows raised in a question, his coat flapping."),
(90,"WIDE","brows raised, two fingers", f"{HERO} holding up TWO fingers with brisk raised brows beside a comically tiny podium, a tiny medal and a tiny trumpet being blown by a tiny man."),
# ACT 22 — you are allowed to say something ----------------------------------
(91,"CU","chin lifted, mouth open", f"{HERO} speaking up in a line of NINE people with his chin lifted and his mouth open, while the people around him turn with warm approving faces and one gives him a thumbs up."),
(92,"WIDE","nodding, approving", "DOZENS of people in a queue nodding in unison with approving mouths at somebody who has just objected, one reaching over to pat him on the back."),
(93,"CU","recoiling, lip curled", "CLOSE on an ordinary face recoiling with a disgusted curled lip — aimed squarely at the intruder, not at the man who objected."),
(94,"MED","cowering, eyes shut", f"{HERO} cowering under an ENORMOUS thought-bubble full of pointing crowds and falling debris, eyes screwed shut, while the actual room around him is completely calm and empty."),
# ACT 23 — how much you get for free -----------------------------------------
(95,"MED","mouth open in wonder", f"{HERO} in a sunlit open PARK with his arms thrown open and his mouth open in wonder as dozens of small everyday courtesies happen around him at once among the trees — a bench shuffled along, a dropped hat returned, a pram lifted over a step. No shops and no shopfronts anywhere in the frame."),
(96,"XWIDE","-", "A VAST landscape of ordinary life running to the horizon — queues of TEN, held doors, orderly escalators, patient crowds — drawn like a bustling map, and not one official anywhere in it."),
(97,"MED","-", "An ENORMOUS empty awards stage with a spotlight burning down on absolutely nobody, a microphone standing alone and rows of empty seats."),
(98,"XCU","-", "A pair of hands opening a COLOSSAL cream velvet-lined medal case, and a disappointed face with a downturned mouth leaning in over the top edge of it — the case is completely EMPTY, just a small medal-shaped dent in the velvet where nothing has ever sat."),
# ACT 24 — it is your turn ---------------------------------------------------
(99,"CU","eyes narrowing, neck glowing", f"CLOSE on {HERO} with the back of his neck glowing red hot and steam curling off it, his eyes narrowing, as somebody steps into the line ahead of him."),
(100,"WIDE","chin up, brows raised", f"{HERO} in an ENORMOUS empty courtroom wearing a judge's wig ABSURDLY too big for him, chin up and brows raised, banging a gavel."),
(101,"XCU","lips pursed, eyes bright", f"EXTREME CLOSE-UP on {HERO}'s lips pursing deliberately and his eyes bright, making the noise on purpose this time."),
(102,"XWIDE","grinning, pointing", f"{HERO} turning and pointing one finger directly at the viewer with a broad grin and both hairs bouncing, while behind him a VAST sunlit street carries an orderly queue away to the horizon."),
]

# ============================================================================
# SECOND FRAMES. One picture per sentence tied SHOT LENGTH to SENTENCE LENGTH,
# and those measure different things: a sentence is long because it carries
# three clauses, a shot should be long because the picture rewards looking. The
# collision was b18 — the most information-dense line in the script holding one
# still for 19.4 seconds.
#
# So a long sentence now carries several pictures, each painting a clause the
# one before it does not. map-shots.py already splits a sentence's span evenly
# across however many frames sit under it (see its comment at the grouping
# step); it only needed its id check relaxed.
#
# Target: no shot over ~6s. Short sentences keep ONE frame — "He tuts." at 1.2s
# is the snap, and splitting it would kill the joke.
# ============================================================================
EXTRA = {
 5: [("MED","brows up, waving", f"A tiny cartoon BRAIN with little legs sprinting in from the "
      f"side of the frame waving both arms, arriving far too late, while {HERO} is already "
      "rigid with his eyes bulging and his fists clenched.")],
 6: [("CU","one brow up, sly", f"{HERO} holding up a small saucer on which sits one tiny pair "
      "of pursed lips, looking straight at the viewer with one brow raised and his mouth "
      "twisted, as if presenting the least impressive object in the world.")],
 11:[("CU","bland mouth, shrugging", f"A reporter in a mackintosh holding a microphone up to "
      f"{HERO} in the bakery line, and {HERO} shrugging with a completely bland mouth and "
      "half-lidded eyes as if the question bored him.")],
 16:[("CU","brows down, finger up", f"{HERO} leaning right into the camera with one finger "
      "raised, mouth open mid-insistence and brows down, while behind him an ENORMOUS "
      "blank-faced clock has one hand that has barely moved.")],
 18:[("WIDE","-", "A burning Paris street in the 1790s: a mob with pikes surging past a "
      "toppling statue, smoke rolling across the rooftops, shutters banging."),
     ("CU","hollow, mouth tight", "A gaunt woman in a shawl clutching ONE small loaf of bread "
      "to her chest with both arms, her mouth tight and her eyes hollow, two children "
      "gripping her skirt."),
     ("WIDE","-", "A baker at his door handing the first loaf to the very first man in a line "
      "of TWENTY people, and every one of the twenty behind him watching the exchange without "
      "moving an inch.")],
 22:[("XWIDE","-", "A VAST city square seen from high above with HUNDREDS of tiny figures "
      "converging into it from eight streets at once, like water running into a basin.")],
 24:[("CU","long-suffering, mouth flat", "A liveried servant standing in a line of FIVE holding his "
      "master's hat and gloves, his mouth flat and his eyes rolled up to the sky with "
      "centuries of patience.")],
 27:[("WIDE","-", "An ENORMOUS completely BLANK departure board looming over a station hall, "
      "and beneath it TWO HUNDRED people locked in total gridlock, cases jammed together.")],
 30:[("MED","triumphant grin, flexing", "A COLOSSAL strongman in a leopard-skin flexing both arms with "
      "a triumphant grin, being calmly waved to the BACK of a line of TEN by a small clerk."),
     ("WIDE","-", "At the head of a line of TEN: a top-hatted man brandishing a fistful of calling "
      "cards, and beside him a starving man with a hollow face — and in front of them both, "
      "one entirely ordinary person who simply arrived first, examining his fingernails.")],
 34:[("CU","eyes wide, thumbs at himself", f"{HERO} alone in an ENORMOUS empty marble hall "
      "turning to the camera and pointing both thumbs at his own chest, eyes wide and mouth "
      "open in disbelief.")],
 36:[("XWIDE","-", "A whole city seen from above with DOZENS of separate queues threaded "
      "through its streets, and standing beside each one a tiny figure in a white coat."),
     ("CU","brows raised, ticking", "A researcher in a white coat ticking a clipboard with brisk "
      "raised brows while just behind his shoulder a plain man in a jacket steps into a line "
      "of TEN.")],
 42:[("CU","glaring at nothing", "An intruder settled comfortably into a line of TEN with his "
      "hands in his pockets, while the woman directly behind him glares fixedly at nothing at "
      "all, her mouth clamped shut and one eyebrow twitching.")],
 44:[("CU","jaw dropped, tiny", f"{HERO} craning up at something enormous above and out of "
      "frame with his jaw dropped and his hat falling off the back of his head.")],
 47:[("CU","scarlet, teeth bared", "A scarlet-faced man at the BACK of a line of TWELVE gripping a metal "
      "barrier with both fists, teeth bared and eyebrows slammed down, vibrating.")],
 48:[("WIDE","eyes closed, then red-faced", "The man at the head of a line reclining in a deckchair with "
      "sunglasses and a cold drink, his eyes closed and entirely serene — while the TWELVE "
      "people behind him are "
      "packed together red-faced and shouting.")],
 53:[("CU","eyebrows tilted up, apologetic", "A flustered man with a bawling baby under one arm and a "
      "bag splitting open cutting into a line of NINE, his eyebrows tilted up in apology, and "
      "every face in the line visibly softening.")],
 57:[("CU","eyes snapping sideways", "A tight row of TEN faces in which every single pair of "
      "eyes snaps sideways in the same direction at the same instant, mouths flattening.")],
 60:[("MED","staring flatly, mouths flat", f"NINE strangers in a row staring flatly with their mouths flat, directly at the "
      f"camera, memorising it, while at the far edge of the frame {CUTTER} strolls away with "
      "his bun, entirely unremembered.")],
 70:[("MED","the same small mouth", "The same tiny disapproving mouth repeated over and over "
      "into the far distance, smaller and smaller, each one letting out one small puff of "
      "air, going on for ever.")],
 76:[("WIDE","a dozen pink cheeks", "A busy street in which A DOZEN different people are all "
      "going pink in the cheeks at the same moment, each caught in his own tiny social "
      "mishap — a dropped glove, a wrong turn, a bumped elbow.")],
 81:[("XWIDE","-", "A VAST city seen from above moving in perfectly smooth streams — and in "
      "the middle of its main square, an empty writing desk and an empty chair, with nobody "
      "sitting at them and nothing on the desk at all.")],
 86:[("CU","mouth slack, eyes fixed", f"{CUTTER}'s face in the pouring rain, completely hollow, "
      "his mouth slack and his eyes fixed on nothing, water running off the brim of his hat "
      "in a steady stream.")],
 91:[("MED","brows up, lifting", f"{HERO} lifting an ENORMOUS price tag the size of a door "
      "with one finger, his brows up in surprise, because it weighs nothing at all.")],
 95:[("MED","arms full, mouth open", f"{HERO} with his arms completely full as strangers hand "
      "him things from every direction at once — a held door, a returned hat, a given-up "
      "seat — his mouth open and his brows up.")],
 96:[("WIDE","-", "A busy sunlit city square where TWENTY people flow smoothly past a bare wooden "
      "coat stand on its own in the middle of the square, with one dark blue tunic and "
      "a peaked cap hanging on it, the empty sleeves hanging limp and flat."),
     ("MED","bored faces, half-lidded eyes", "THREE ordinary people each performing one tiny courtesy "
      "with completely bored faces and half-lidded eyes — holding a door, moving a bag, "
      "stepping aside — none of them looking pleased with themselves.")],
 99:[("CU","eyes darting sideways", f"{HERO} with the back of his neck glowing red hot and steam "
      "curling off it, and a stranger's hand entering the frame to pat him reassuringly on "
      "the shoulder, his eyes darting sideways at it.")],
}

# Splice the extras in after the frame they belong to, keeping script order.
_S = []
for row in S:
    _S.append(row)
    for cam, expr, scene in EXTRA.get(row[0], []):
        _S.append((row[0], cam, expr, scene))
S = _S


WORLD = (
 "a MID-CENTURY ANIMATION BACKGROUND AND CEL in the American limited-animation idiom "
 "of the late 1950s: flat gouache-painted backgrounds and flat painted cel figures "
 "with confident tapering ink outlines and no interior shading, in a warm graphic "
 "palette of INK BLUE, mustard GOLD, sage GREEN, dusty ORANGE, cream and flat "
 "VERMILION RED, each scene keying its own dominant colour from that set. "
 "Expressions are BOLD, exaggerated and readable at a glance, in the tradition of "
 "classic theatrical cartoon animation. Visible gouache texture, flat matte, NO "
 "gradients, NO airbrushed shading, NO photographic texture, NO three-dimensional "
 "rendering. There is NO text, NO lettering, NO numbers and NO writing of any kind "
 "anywhere in the image; any sign, board, placard or banner is completely BLANK. "
 "This is an ORIGINAL character in a general mid-century cartoon idiom: NO existing "
 "cartoon characters, NO studio logos, NO trade dress. ONLY the people described above "
 "appear in this image — if the description above names nobody, there are NO PEOPLE IN "
 "THE IMAGE AT ALL. Any crowd is individuated: different faces, different builds and "
 "clothes in DIFFERENT colours from the palette, never a row of matching coats. "
 "ONE SINGLE COHERENT SCENE, NOT a grid of panels, NOT a sheet of studies. 16:9, edge "
 "to edge, one scene, one camera.")


# THE CAMERA IS A CROP, NOT A NOUN. The v3 probe declared b13 a close-up and got
# a full-body figure in a street; it declared b12 a wide and got a two-shot. The
# model reads "CLOSE on" as a mood word. It does not ignore an instruction that
# names which part of the body the frame edge cuts through.
CAM = {
 'XCU':   ("EXTREME CLOSE-UP, the camera pushed right in: the subject FILLS THE ENTIRE FRAME "
           "and is CROPPED HARD by all four edges. Almost no background is visible."),
 'CU':    ("CLOSE-UP: his HEAD AND SHOULDERS FILL THE FRAME, cropped at the chest, the top of "
           "his head near the top edge. Only a suggestion of background behind him."),
 'MED':   "MEDIUM SHOT, the figures cut off at the knees and filling most of the frame height.",
 'WIDE':  "WIDE SHOT: the full figures stand well inside the frame with the setting around them.",
 'XWIDE': "VERY WIDE SHOT: the figures are SMALL in a large landscape that fills the frame.",
}
_CAMWORD = re.compile(r'^(EXTREME )?CLOSE(-UP)? on ', re.I)
def strip_cam(scene):
    """Drop the old advisory prefix so CAM is the only camera instruction."""
    s = _CAMWORD.sub('', scene)
    return s[0].upper() + s[1:] if s else s

MIN_CAM = {'XCU': 12, 'CU': 25, 'XWIDE': 4}
MAX_RUN = 3
MIN_CU_SHARE = 0.42        # a face cannot carry a beat at full-body distance
MAX_QUEUE_SHARE = 0.40     # v2 ran 77 percent
MIN_EVENT_SHARE = 0.85     # something must HAPPEN, not merely be
MIN_CAST_SHARE = 0.55      # other people, doing things

# A face ACTION, not a mood. v2 named zero of these in 102 frames.
FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|'
                  r'cheeks|tongue|chin|snor|tut|hum|point|shrug|nod', re.I)
# A physical EVENT, not a state. "standing" is deliberately absent.
EVENT = re.compile(r'burst|pop|fly|flying|flap|shoot|splatt|erupt|stream|pour|collaps|'
                   r'toppl|crack|snap|spring|slam|throw|thrown|swing|scatter|scrambl|'
                   r'clamber|shov|elbow|carr|drop|slid|slide|tipping|vibrat|whistl|'
                   r'lift|roll|cartwheel|buckl|hover|dart|curl|glow|steam|smoke|leak|'
                   r'ping|wag|nod|shak|crouch|lean|reach|step|walk|ride|hold|haul|pull|'
                   r'peer|point|count|charg|chew|trudg|wrap|slice|stab|bang|snak|'
                   r'settl|strid|amble|stroll|duck|dig|turn|rub|sip|sail|thump|spray|strik|rais|'
                   r'crush|link|examin|crane|hang|stretch|tilt|clamp|snak|wav|'
                   r'trudg|file|jostl|squeez|press|balanc|tut', re.I)
CAST = re.compile(r'SECOND MAN|policeman|baker|woman|women|man\b|men\b|people|crowd|'
                  r'researcher|commuter|passenger|worker|child|boy|girl|knight|'
                  r'merchant|servant|neighbour|stranger|dog|cat|goat|chicken|mouse|'
                  r'stallholder|guard|operator|audience|figure|intruder|objector', re.I)
QUEUE = re.compile(r'queue|\bline\b|single file', re.I)

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []
lines = [s[0] for s in S]
missing = sorted(set(range(1, len(sents) + 1)) - set(lines))
if missing:
    errs.append(f'sentences with no frame: {missing[:12]}')
if lines != sorted(lines):
    errs.append('frames run backwards through the script')
if max(lines) > len(sents):
    errs.append(f'frame points at sentence {max(lines)}; script has {len(sents)}')

# An unrendered {HERO} would ship the brace text straight to the model.
braces = [i for i, s in enumerate(S, 1) if '{' in s[3]]
if braces:
    errs.append('unrendered f-string braces in scene: ' +
                ' '.join('b%02d' % i for i in braces[:10]))

cams = [s[1] for s in S]
c = Counter(cams)
for k, n in MIN_CAM.items():
    if c[k] < n:
        errs.append(f'camera quota: {k} has {c[k]}, needs {n}')
cu = c['CU'] + c['XCU']
if cu / len(S) < MIN_CU_SHARE:
    errs.append(f'close-ups {cu}/{len(S)} ({cu/len(S):.0%}), needs {MIN_CU_SHARE:.0%}')
run, prev = 1, None
for i, cam in enumerate(cams, 1):
    if cam == prev:
        run += 1
        if run > MAX_RUN:
            errs.append(f'frame {i}: {run} consecutive {cam}')
    else:
        run, prev = 1, cam

noface = [i for i, s in enumerate(S, 1) if s[2] != '-' and not FACE.search(s[2])]
if noface:
    errs.append('expression declared but names no face action: ' +
                ' '.join('b%02d' % i for i in noface[:10]))
# the expression must also survive into the prompt the model actually reads
lost = [i for i, s in enumerate(S, 1) if s[2] != '-' and not FACE.search(s[3])]
if lost:
    errs.append('expression not present in the SCENE text: ' +
                ' '.join('b%02d' % i for i in lost[:10]))
noev = [i for i, s in enumerate(S, 1) if not EVENT.search(s[3])]
if len(S) - len(noev) < MIN_EVENT_SHARE * len(S):
    errs.append(f'physical event on {len(S)-len(noev)}/{len(S)}, needs {MIN_EVENT_SHARE:.0%}; '
                'flat: ' + ' '.join('b%02d' % i for i in noev[:10]))
standing = [i for i, s in enumerate(S, 1) if re.search(r'\bstand(s|ing)?\b', s[3], re.I)]
if len(standing) > 12:
    errs.append(f'"standing" in {len(standing)} scenes (v2 had 55); max 12')
cast = [s for s in S if CAST.search(s[3])]
if len(cast) / len(S) < MIN_CAST_SHARE:
    errs.append(f'other characters in {len(cast)}/{len(S)} ({len(cast)/len(S):.0%}), '
                f'needs {MIN_CAST_SHARE:.0%}')
q = [s for s in S if QUEUE.search(s[3])]
if len(q) / len(S) > MAX_QUEUE_SHARE:
    errs.append(f'queue scenes {len(q)}/{len(S)} ({len(q)/len(S):.0%}), '
                f'max {MAX_QUEUE_SHARE:.0%}')
for i, s in enumerate(S, 1):
    if re.search(r'charcoal|scratched ink|scribbled hatching|smeared ink', s[3], re.I):
        errs.append(f'b{i:02d}: the second-medium marks are gone; do not reintroduce them')

uncounted = [i for i, s in enumerate(S, 1)
             if QUEUE.search(s[3]) and not re.search(
                 r'\b(TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|TWELVE|TWENTY|DOZENS|HUNDREDS|TWO HUNDRED)\b', s[3])]
if uncounted:
    errs.append('queue named with no COUNT of people (the b12 fault): ' +
                ' '.join('b%02d' % i for i in uncounted[:10]))

print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(S)} ({cu/len(S):.0%}) | "
      f"faces {len([s for s in S if s[2] != '-'])}/{len(S)} | "
      f"events {len(S)-len(noev)}/{len(S)} | "
      f"cast {len(cast)}/{len(S)} ({len(cast)/len(S):.0%}) | "
      f"queue {len(q)}/{len(S)} ({len(q)/len(S):.0%}) | "
      f"standing {len(standing)}")

if errs:
    print('\nBOARD REJECTED:', file=sys.stderr)
    for e in errs:
        print('  ' + e, file=sys.stderr)
    sys.exit(1)

# STABLE IDS. Numbering the 133 frames b01..b133 would have renamed every
# existing picture — b19 would point at a scene b19 was never generated for —
# and turned a 32-frame top-up into a 133-frame reshoot at four times the cost.
# A frame's id is therefore its SENTENCE number, and the extra frames under a
# sentence take a letter suffix: b18, b18b, b18c, b18d.
ids, _seen = [], {}
for row in S:
    n = _seen.get(row[0], 0)
    _seen[row[0]] = n + 1
    ids.append(f'b{row[0]:02d}' + ('' if n == 0 else chr(ord('a') + n)))
assert len(set(ids)) == len(ids), 'duplicate frame id'

(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{CAM[s[1]]} {strip_cam(s[3])} {WORLD}' for i, s in zip(ids, S)}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'expression': s[2],
      'line': sents[s[0] - 1], 'scene': s[3]} for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S)
          if 'VERMILION RED coat' not in s[3] and 'SECOND MAN' not in s[3]]
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
