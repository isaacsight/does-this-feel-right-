#!/usr/bin/env python3
"""Frame book — The Million-Dollar Pigeon. 115 frames, one per sentence.

Everything the queue episode cost is enforced here from the first batch rather
than after a rejected cut:

  THE CAMERA IS A CROP     "CLOSE on" is advisory and gets ignored; CAM names
                           which part of the body the frame edge cuts through.
  COUNTS, NOT NOUNS        "a queue" can be satisfied by an empty pavement.
                           "a line of SIX people" cannot.
  A FACE ACTION PER FRAME  checked twice — on the declared expression AND on
                           the scene text the model actually receives, because
                           a frame can declare "mortified" and ship a prompt
                           with no face in it.
  EVENTS, NOT STATES       something happens; nobody "stands".
  OMISSION, NOT NEGATION   cast.json withholds the character sheet from the
                           frames that name nobody. Four separate failures
                           across two episodes proved text cannot cancel what
                           a reference asserts in pixels.

And one quota this subject needs that the queue episode did not:

  THE TWO-SIDED FRAME      the comedy is the gap between a human side that
                           means everything and a bird side that means nothing.
                           Where both are present, stage both — never cut away
                           to the reaction.

  ENVIRONMENT CAP          the rooftop loft is this film's bakery queue. It is
                           capped, and the board tags every frame with its
                           setting so the cap is measured rather than hoped for.

THE ONE ACT WITH NO JOKES: act 2 (Cher Ami, lines 14-27) and the two death
lines in act 7 are staged straight. The probe proved the world can carry
gravity; this is where it has to.

Run: python3 board.py
"""
import json, re, sys
from pathlib import Path
from collections import Counter

FILM = Path(__file__).resolve().parent

FANCIER = ("THE FANCIER: a small slight man with a round face and a big confident nose, "
           "EXACTLY TWO hairs sticking up from his crown that kink and lean at different "
           "angles, a flat VERMILION RED coat, thin stick legs and ABSURDLY oversized shoes")
KIM = ("THE HEN: a plump grey racing pigeon with a tiny head, a bright orange eye and ONE "
       "white splash on her left wing")
COCK = ("THE COCK: a grey racing pigeon, scruffier than the hen, his feathers ruffled on "
        "one side")

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
# ACT 1 — the bird does one thing, so we gave it a job ------------------------
(1,"CU","eye bright, head cocked","void", f"{KIM} filling the frame against flat cream, her head cocked and her orange eye bright and fixed on something far outside the picture."),
(2,"MED","brows up, gaping","void", f"{FANCIER} gaping with his brows up and mouth open at {KIM}, who ignores him completely, the two of them alone on flat cream."),
(3,"XWIDE","-","road", "A tiny lorry crossing an ENORMOUS empty plain with one bird bursting out of a hatch at the back and climbing hard, the road running away to a far horizon."),
(4,"MED","-","void", "A bare wooden signpost standing alone in the middle of a deserted flat cream field with a completely BLANK arm pointing one way, and a single pigeon flying past it in the opposite direction. The field is empty and unpeopled to the horizon."),
(5,"WIDE","-","loft", "A small wooden loft by itself on a deserted rooftop at golden hour, its landing board down and warm light pouring out of the open door. The rooftop is bare and unoccupied, with nobody on it and nobody below."),
(6,"XCU","-","loft", "EXTREME CLOSE-UP on THREE things in a row against warm wood: one perch worn smooth, one small round doorway, and one battered latch."),
(7,"MED","brows knitted, arguing","study", "FOUR scientists in white coats crowding round a table, all arguing at once with their brows knitted and mouths open, one holding a compass, one pointing at the sun through a window, one sniffing the air, one tracing a road map — while a pigeon on the table looks away."),
(8,"CU","utterly blank","void", f"{KIM} filling the frame with a completely blank expression, one eye visible, saying nothing at all, while a microphone on a boom pokes into the frame toward her."),
(9,"XWIDE","-","sky", "A VAST pale sky with one small dark bird crossing it in a dead straight line, tiny against the emptiness."),
(10,"MED","-","void", "A cartoon cutaway of a pigeon on flat cream showing THREE simple parts and nothing else: a heart, two wings, and a small luggage label tied to one leg, completely BLANK."),
(11,"CU","brows down, mouth open","loft", f"{FANCIER} leaning right into the camera with one finger raised, his brows down and mouth open mid-insistence, the loft behind him out of focus."),
(12,"WIDE","grinning, grabbing","void", "SIX cheerful men in overalls swarming around one calm pigeon on a plinth, grinning and reaching for it with clipboards, tape measures and a tiny harness."),
(13,"CU","brows raised, brisk","void", f"{FANCIER} briskly handing a tiny BLANK envelope to {KIM} with both brows raised, like a foreman giving out a shift rota."),
# ACT 2 — war. NO COMEDY IN THIS ACT ----------------------------------------
(14,"MED","jaw set, running","argonne", "A signaller in a muddy trench running bent double with a wicker basket clutched to his chest, jaw set, shells bursting behind him."),
(15,"XWIDE","-","argonne", "A VAST shattered forest at dawn under a low ink-blue sky: splintered trees, wire, water in the shell holes, smoke drifting across everything."),
(16,"WIDE","eyes screwed shut","argonne", "TWENTY American soldiers in WIDE FLAT-BRIMMED shallow steel helmets like upturned soup plates, pressed flat into a hillside hollow with their arms over their heads, eyes screwed shut and mouths open, earth erupting in fountains all around them."),
(17,"MED","heads down, eyes hollow","argonne", "A dead radio set with its wires torn out lying in the mud, and beside it TWO exhausted soldiers with their heads down and their eyes hollow, one holding a runner's message pouch that is empty."),
(18,"CU","eyes steady, hands cupped","argonne", "A young AMERICAN doughboy in a WIDE FLAT-BRIMMED shallow steel helmet like an upturned soup plate, his hands caked in grey-brown mud, cupped around one small grey pigeon like a match held out of the wind, his face above just visible, jaw set, eyes exhausted and steady. The mud is grey-brown, not orange."),
(19,"WIDE","-","argonne", "One small bird climbing hard through a sky torn with shellbursts and smoke trails, tiny and alone, wings beating, the shattered forest far below."),
(20,"XWIDE","-","argonne", "The same shattered forest at total rest under a wide pale opening sky: fine dust hanging motionless in still air, water lying flat and mirror-calm in the shell holes, one bird settling onto a broken branch. The whole picture is silent and completely undisturbed."),
(21,"WIDE","eyes down, exhausted","argonne", "A long line of American soldiers in WIDE FLAT-BRIMMED shallow steel helmets walking slowly out of the treeline into open light, filthy, their eyes down, some carrying others."),
(22,"XCU","-","museum", "EXTREME CLOSE-UP on a small bronze military cross on a faded ribbon, pinned to a green velvet backing."),
(23,"MED","mouths closed, hats off","museum", "A glass museum case holding one small mounted pigeon, and THREE visitors standing before it with their hats off and their mouths closed, one child pressed to the glass."),
(24,"MED","-","museum", "A second glass case beside the first, and a third beyond it, each holding one small mounted bird, receding away down a quiet gallery."),
(25,"WIDE","-","museum", "A long wall hung with THIRTY-TWO small identical medals on ribbons in neat rows, filling the frame."),
(26,"MED","-","museum", "Beside that wall, three much smaller groups of medals: a group of EIGHTEEN, a group of THREE, and one single medal on its own with a small cat asleep beneath it."),
(27,"XWIDE","-","museum", "A VAST gallery seen from high above, where the pigeon wall runs the entire length of one side and everything else in the room is dwarfed by it."),
# ACT 3 — so we raced them ---------------------------------------------------
(28,"MED","mouths set, stooped","street", "SIX demobbed soldiers in ill-fitting civilian coats trudging away down a street with kit bags and their mouths set — and every one of them carrying a wicker basket with a pigeon looking out of it."),
(29,"WIDE","grinning, conspiratorial","club", "TEN men crowded round a back-room table grinning at each other, one already unrolling a large BLANK sheet of paper, baskets stacked to the ceiling behind them."),
(30,"CU","brows up, explaining","club", f"{FANCIER} with both brows up and one hand raised mid-explanation, leaning toward the camera in a dim club room."),
(31,"XWIDE","-","field", "Dawn over a VAST empty field: one lorry with all its side hatches dropped open, and HUNDREDS of pigeons BLASTING out of it and sweeping DIAGONALLY across the whole width of the frame from low left to high right and off the top corner, a broad slanting river of birds rather than a column, wings beating hard, the nearest birds LARGE with visible feathers and the furthest tiny specks. TWO tiny men below with their hats blown out of their hands."),
(32,"XWIDE","-","sky", "An ENORMOUS sky in which the birds scatter outward in every direction like a firework going off, each one heading a different way, already far apart."),
(33,"WIDE","-","village", "Two neighbouring rooftops seen together: one bird dropping onto the left loft, one bird dropping onto the right loft, each to its own door."),
(34,"XWIDE","-","sky", "A VAST empty cloudscape with nothing in it at all but weather, filling the entire frame."),
(35,"XWIDE","-","field", "A COLOSSAL empty stadium with grass growing through the terraces and not one person in it, and far above, tiny in the sky, TWELVE birds flying over it without stopping."),
(36,"MED","frowning, calculating","club", "TWO men at a trestle table frowning over a long paper tape, one running a finger down it, the other working a hand-cranked adding machine with his tongue between his teeth."),
(37,"XCU","-","club", "EXTREME CLOSE-UP on a small rubber ring being slipped over a pigeon's leg by two enormous careful fingers, the ring completely BLANK."),
(38,"MED","narrowed eyes, leaning in","club", "A heavy brass clock with a wax seal on it sitting on a trestle table, and FOUR men leaning in around it with narrowed eyes, all watching each other's hands rather than the clock."),
(39,"CU","one brow raised, wry","club", f"{FANCIER} looking directly at the viewer with one brow raised and his mouth twisted wryly, the sealed clock beside him."),
(40,"CU","brows soft, trusting","loft", f"{FANCIER} holding {KIM} up in both open palms with a completely trusting face, brows soft, offering her to the sky."),
(41,"MED","eyes on each other","club", "The same brass clock now wrapped in chains and padlocks on a table, with SIX men sitting round it in a ring, arms folded, their eyes on each other and nobody watching the bird."),
# ACT 4 — Darwin -------------------------------------------------------------
(42,"MED","brows raised, comparing","study", "A bearded Victorian man in a loft coat holding up TWO wildly different pigeons at arm's length and comparing them with his brows raised and his mouth open, one bird fantastically frilled, the other plain."),
(43,"XCU","-","study", "EXTREME CLOSE-UP on a heavy open book on a desk, its pages completely BLANK, a small brown finch perched on the corner being politely ignored."),
(44,"MED","-","study", "The same open book with a pigeon standing squarely in the middle of its BLANK pages, filling the spread, quite at home."),
(45,"WIDE","brows soft, content","study", "A Victorian garden with a large wooden loft at the end of it, and the bearded man pottering toward it in shirtsleeves with a feed scoop, his brows soft and entirely content, house behind."),
(46,"WIDE","grinning, in between","london", "A gaslit London street with TWO doorways side by side: through the left, FIVE men in top hats and frock coats; through the right, FIVE men in flat caps and mufflers — and the bearded man grinning in the middle of the pavement between them holding a pigeon, being greeted by both sides."),
(47,"MED","brows down, absorbed","london", "A cramped workshop where THREE fanciers in aprons bend over their birds with total absorption, one measuring a wing, one holding a bird up to a lamp, one writing in a ledger with BLANK pages."),
(48,"CU","brows down, scribbling","study", "The bearded man scribbling furiously in a notebook with his brows down and tongue between his teeth, ink spraying, a pigeon standing on his shoulder."),
# ACT 5 — the money ----------------------------------------------------------
(49,"MED","-","void", "A cartoon family tree of pigeons on flat cream, and coins tumbling down through it from branch to branch, piling up at the bottom."),
(50,"WIDE","mouths murmuring","auction", "A grand saleroom filling with TWENTY people taking their seats, mouths murmuring, chandeliers above, a bare velvet cushion waiting on a table at the front."),
(51,"MED","preening, calm","auction", f"{KIM} on a bare velvet cushion under a warm spotlight, calmly preening one wing, while behind her TWENTY faces lean forward in the dark."),
(52,"MED","-","auction", "TWO bidding paddles raised high out of the dark, one vast and gold and one small and black, both completely smooth and BARE, their owners hidden below the frame."),
(53,"CU","eyes bulging, sweating","auction", "An auctioneer with his eyes bulging and his mouth open mid-shout, sweat flying off his forehead, gavel raised, an ENORMOUS BLANK gold board glowing behind him."),
(54,"WIDE","mouths open, erupting","auction", f"The gavel coming down hard, TWENTY people erupting out of their seats with mouths open and hands to their heads — and {KIM} on the cushion, mid-preen, not looking up."),
(55,"MED","-","auction", "A second velvet cushion beside the first, empty, with a slightly smaller BLANK gold board above it, dimmed and forgotten."),
(56,"CU","one brow up, confiding","auction", f"{FANCIER} turning to the viewer with one brow up and a confiding half-smile, the saleroom blurred behind him."),
(57,"WIDE","-","field", "A racing basket lying on its side in an empty field with its door tied shut and grass growing through the wicker."),
(58,"MED","tender, nesting","loft", f"{KIM} settled deep in a nest box lined with straw, {COCK} beside her, both of them quiet."),
(59,"WIDE","-","loft", "An ENORMOUS palatial loft, far grander than a shed, with one small hen sitting in the middle of it doing nothing, and the door standing wide open behind her."),
# ACT 6 — cocaine and the horse lab -----------------------------------------
(60,"WIDE","narrowed eyes, sly","village", "A modest brick house with a COLOSSAL gleaming loft on its roof twice the size of the house, and a man on a ladder glancing over his shoulder with narrowed eyes."),
(61,"CU","mouths set, determined","club", "FOUR federation officials in overcoats arriving at a loft door with a clipboard and a case of small jars, their mouths set."),
(62,"XCU","-","club", "TWENTY tiny specimen jars in a warm wooden rack on a mustard GOLD tabletop, each with a completely BLANK label, one gloved hand placing the twentieth. The whole picture is keyed to warm cream, mustard GOLD and dusty ORANGE."),
(63,"MED","shrugging, blank","club", "A Belgian technician in a white coat shrugging enormously with both palms up and his mouth turned down, in front of a machine whose readout panel is completely BLANK."),
(64,"WIDE","-","road", "A small parcel on a conveyor belt travelling past an aeroplane window view of an ENORMOUS ocean, and beyond it a dry sunlit landscape."),
(65,"MED","squinting, disbelieving","lab", "An empty laboratory late at night, hung with ENORMOUS oil paintings of racehorses and crowded with COLOSSAL gold horse trophies, every workbench abandoned and every stool pushed in — and one lone official working after hours in a white coat holding up a TINY specimen jar in tweezers, squinting with one eye shut and his eyebrows climbing in complete disbelief."),
(66,"MED","eyebrows shooting up","lab", "The same official recoiling from a readout with his eyebrows shooting up and his mouth open, holding up SIX small cards, FIVE in one hand and ONE held apart in the other."),
(67,"CU","eyes wide, wired","loft", "A single pigeon filling the frame with its eyes ABSURDLY wide and both wings thrown out, feathers standing on end, vibrating."),
(68,"WIDE","blank, anonymous","club", "SIX identical BLANK jars standing in a row on a bench, and behind them a wall of TWENTY loft doors, every one of them shut."),
(69,"MED","mouth open, brows drawn","club", "An official holding up a sheet of paper that is completely BLANK with both hands, his mouth open and his brows drawn together in frustration, a room of shut doors behind."),
(70,"WIDE","grinning, shrugging","club", "TEN men grinning and filing out of a club room with their baskets, shrugging as they go, leaving SIX jars behind on the table untouched."),
# ACT 7 — Shanghai. The death lines are staged STRAIGHT. ---------------------
(71,"MED","-","void", "A cartoon set of scales with one tiny pill on one pan and a COLOSSAL heap of banknotes on the other, the notes completely BLANK, the pill lifted uselessly into the air."),
(72,"XWIDE","-","shanghai", "A VAST modern city skyline at dusk under an enormous sky, towers receding into haze."),
(73,"WIDE","brows down, conferring","shanghai", "TWO men in windcheaters with their brows down, bent over a large BLANK map spread on a car bonnet, tracing a long line across it with one finger, a city behind them."),
(74,"MED","brows soft, mouths set","henan", "The same TWO men feeding birds in a bare yard, and behind them a wall covered edge to edge with tally scratches, their brows soft and their mouths set."),
(75,"WIDE","-","henan", "A split scene: on the left a country loft in a green field with pigeons landing on it, on the right an identical loft on a city rooftop with the same pigeons landing on it, joined by one long line of flight across the middle."),
(76,"CU","eye fixed, certain","void", f"{KIM} filling the frame in profile against flat cream, entirely certain, one orange eye fixed forward."),
(77,"MED","brows knitted, thinking","void", f"{FANCIER} with his brows knitted and one finger to his temple, staring hard at a single pigeon perched on a bare plinth in front of him."),
(78,"MED","-","void", "A cartoon diagram on flat cream: one bird, and TWO identical small houses instead of one, a line running from the bird to each."),
(79,"WIDE","eyes darting, furtive","shanghai", "TWO men hurrying along a railway platform with FOUR cardboard milk cartons clutched to their chests, eyes darting sideways, an ENORMOUS sleek white train alongside them."),
(80,"MED","mouths open, arms up","shanghai", "The same TWO men on a small stage with their arms up in triumph and their mouths open, receiving FOUR trophies, a crowd of TWENTY applauding below."),
(81,"CU","frowning, suspicious","club", "An official frowning at a paper tape with his eyes narrowed and his mouth pulled tight, holding it up close to his face."),
(82,"WIDE","-","shanghai", "An ENORMOUS white train streaking across the frame at speed — and above it, level with it, FOUR pigeons apparently flying at exactly the same impossible pace."),
(83,"CU","mouths set flat, eyes hard","club", "THREE officials standing shoulder to shoulder looking down at a table of results, all three with their mouths set flat and their eyes hard."),
(84,"WIDE","-","void", "A COLOSSAL heap of BLANK banknotes on flat cream with one small ordinary man standing beside it, dwarfed, looking up at it."),
(85,"WIDE","-","shanghai", "An empty yard at night with a loft door standing open and no birds inside it at all, one feather on the ground, a single bare bulb burning."),
(86,"MED","impassive, judging","court", "A courtroom bench where THREE impassive figures in robes look down at TWO small men standing below them, hands at their sides, heads lowered."),
(87,"XCU","-","club", "EXTREME CLOSE-UP on a heavy brass sealed clock, its wax seal perfectly intact, gleaming and undisturbed."),
(88,"MED","-","void", "A small house on flat cream with a bird flying toward it — and a second identical house appearing beside it, so the bird's line of flight forks in two."),
# ACT 8 — the widowhood reveal ----------------------------------------------
(89,"CU","leaning in, brows up","void", f"{FANCIER} leaning ENORMOUSLY far toward the viewer with both brows up and one finger raised, a spotlight snapping onto him in the dark."),
(90,"MED","-","void", "THREE objects racing along a bare cream field seen from the side, no people anywhere: a tiny white pill, a small sleek white train, and a plain wooden nest box — and the nest box is streaking far ahead of the other two with speed lines behind it."),
(91,"WIDE","brows up, explaining","loft", f"{FANCIER} on the rooftop beside the open loft, one hand raised matter-of-factly mid-explanation, brows up, the painted scene running right to all four edges of the picture with NO border and NO black bar down any side, {KIM} and {COCK} on the perch behind him."),
(92,"CU","tender, leaning together","loft", f"{KIM} and {COCK} on one perch in warm mustard GOLD light, leaning very slightly together, doing nothing at all."),
(93,"MED","eyes following","loft", f"Two enormous careful human hands lifting {COCK} away from the perch, while {KIM} stays behind on the perch, her eyes following him."),
(94,"WIDE","-","road", "One wicker pigeon basket on the tailgate of a plain lorry on a deserted country road, the lorry small against an ENORMOUS empty landscape, its rear hatch dropping open and one grey pigeon leaving it fast with long curved motion lines trailing behind its wings. No people in the picture, and no sound-effect lettering of any kind — speed is shown only with drawn motion lines."),
(95,"WIDE","-","sky", "One bird tearing across a burning ORANGE sky with its wings driving hard, low and fast over a landscape, the horizon streaming past beneath it."),
(96,"MED","-","void", "A COLOSSAL open ledger on flat cream with two BLANK columns, one short and one long, a quill lying across it."),
(97,"XCU","-","void", "EXTREME CLOSE-UP on a tiny pill inside a red circle with a hard diagonal bar struck through it."),
(98,"XCU","-","loft", "EXTREME CLOSE-UP on a plain wooden nest box with a small brass trophy sitting inside it where an egg should be."),
(99,"MED","eyes down, sheepish","club", "TEN fanciers in a club room all with their eyes down on their own shoes at once, hands behind their backs, in front of a completely BLANK noticeboard."),
(100,"WIDE","-","void", "A COLOSSAL machine of brass funnels, gears and flywheels filling the frame — and at the very centre of it, driving the whole thing, one small plain wooden nest box."),
(101,"XWIDE","-","village", "A VAST city of banks, towers and rooftops built in tiers, and holding the whole structure up at its base, one small wooden loft with two birds sitting in the doorway."),
# ACT 9 — Tyson, and the yard ------------------------------------------------
(102,"MED","besotted, gentle","loft", "FOUR very different people side by side on a rooftop — an old woman, a boy, a man in overalls and a man in a good suit — every one of them holding a pigeon and every one of them besotted."),
(103,"WIDE","teeth bared, eyes streaming","brooklyn", "A Brooklyn street corner at dusk where a boy swings at a bigger boy with his teeth bared and his eyes streaming, an empty cage tipped over on the ground between them."),
(104,"CU","face gone soft","gym", "An ENORMOUS heavyweight in a dressing gown and tiny reading glasses, holding one small pigeon in two cupped boxing gloves like a soap bubble, his face gone completely soft."),
(105,"MED","preening, unimpressed","void", "A COLOSSAL heap of BLANK banknotes on flat cream with one small pigeon standing on top of it, preening, entirely unimpressed."),
(106,"WIDE","-","argonne", "One small grey pigeon flying steadily across a torn smoky sky high above a shattered forest of broken trees, tiny against the weather, wings level. No people and no other animals in the picture."),
(107,"WIDE","-","club", "One small grey pigeon flying straight across a deserted club room directly above a long table covered with brass sealed clocks and small rubber rings, not looking down at any of it. The room is empty of people."),
(108,"XWIDE","-","sky", "A VAST dawn sky with one small dark bird crossing it, and far below on the horizon a single small rooftop loft with its door open."),
(109,"MED","-","void", "A plain wooden shelf against flat cream holding THREE elaborate objects in a row — a gavel, a gold trophy and a brass sealed clock — and lying beside them one plain grey pigeon feather. Nothing else is in the picture: no people and no animals."),
(110,"CU","eye level, certain","void", f"{KIM} filling the frame head-on against flat cream, her orange eye level and certain, wings folded."),
(111,"MED","brows up, delighted","loft", f"{FANCIER} looking at the viewer with both brows up and a delighted dawning grin, hands spread, the loft behind him."),
(112,"WIDE","mouth open, eyebrows raised","loft", f"{FANCIER} on a brick rooftop at dusk beside his loft, STANDING UP on an upturned crate, stretched tall on his toes with a stopwatch held high above his head at full arm's length, head tipped right back, mouth open and eyebrows raised in hope. He is SMALL and low in the frame and an ENORMOUS empty sky fills the entire upper two thirds of the picture above him. A thermos and an enamel mug cooling on the parapet."),
(113,"MED","brows soft, chin lifting","loft", f"{FANCIER} settling onto the crate with his mug in both hands and his brows soft, chin lifting, the washing lines and chimney pots running away behind him."),
(114,"XWIDE","-","sky", "An ENORMOUS empty evening sky filling almost the whole frame, with one small rooftop and one tiny figure on it at the very bottom edge, looking up."),
(115,"WIDE","grinning, arms lifting","loft", f"{KIM} dropping onto the landing board with her wings flared wide — and below her {FANCIER} with his arms lifting and an ENORMOUS grin breaking across his face, the stopwatch forgotten in one hand."),
]

# ============================================================================
# SECOND FRAMES. One frame per sentence tied SHOT LENGTH to SENTENCE LENGTH,
# and at 115 sentences over 636 seconds the mean hold was already 5.5s before
# any variance — 47 shots ran past six seconds and the Darwin opener held one
# still for 13.9. Long sentences now carry several pictures, each painting a
# clause the one before it does not. map-shots.py splits a sentence's span
# evenly across however many frames sit under it.
#
# Short sentences keep ONE frame. "It goes home." at 1.6s is the landing.
# ============================================================================
EXTRA = {
 3:  [("MED","-","road", "A wicker basket being lifted into the back of a plain lorry on a deserted road, its lid strapped down, one grey pigeon looking out through the weave.")],
 7:  [("MED","brows down, baffled", "study", "The same FOUR scientists now sitting in silence with their brows down and mouths shut, surrounded by a compass, a sun chart, a jar of air and a road map, none of them looking at each other.")],
 14: [("XCU","-","argonne", "EXTREME CLOSE-UP on a tiny rolled paper message being slipped into a small metal tube on a pigeon's leg by two careful mud-stained fingers, the paper completely BLANK. The whole picture is keyed to warm cream and mud brown.")],
 19: [("XWIDE","-","argonne", "A VAST torn sky seen from very far away with one almost invisible speck of a bird crossing it, the shattered forest a thin dark line at the bottom of the frame.")],
 22: [("MED","chin lifted, mouth firm","museum", "A French officer in a blue greatcoat pinning a small bronze cross onto a green velvet cushion held by an aide, his chin lifted and his mouth firm, a small grey pigeon watching from a perch beside them.")],
 25: [("XCU","-","museum", "EXTREME CLOSE-UP on one small silver medal on a striped ribbon lying on dark velvet, and behind it, out of focus, a long row of identical medals receding away.")],
 26: [("MED","-","museum", "A small tabby cat asleep on a velvet cushion directly beneath one single medal on a wall, entirely untroubled.")],
 31: [("MED","-","field", "A row of TWELVE wicker baskets strapped shut in the back of a lorry, each with grey pigeons looking out through the weave, the tailgate up and the road unrolling behind.")],
 35: [("XWIDE","-","sky", "An ENORMOUS empty blue sky filling the whole frame with FIVE tiny birds scattered across it at great distances from one another, each flying a different way.")],
 36: [("XCU","-","club", "EXTREME CLOSE-UP on a brass slide rule and a stub of pencil lying on a paper tape covered in tally scratches, a thumb pressing the tape flat.")],
 37: [("MED","brows down, concentrating","club", "A fancier bent right over a bird on a table with his brows down and tongue between his teeth, threading a small rubber ring onto its leg with enormous care.")],
 38: [("XCU","-","club", "EXTREME CLOSE-UP on a small dark chip glinting inside a plastic leg band, held up between two fingers against a warm cream background.")],
 42: [("MED","brows raised, sorting","study", "A Victorian workbench covered with SIX wildly different pigeons in a row — one enormously frilled, one with a fan tail, one with a hooded crest — and a bearded man leaning over them with his brows raised, comparing."),
      ("XCU","-","study", "EXTREME CLOSE-UP on a pair of brass callipers measuring the beak of one pigeon, the bird holding perfectly still.")],
 46: [("MED","grinning, welcomed","london", "Inside a panelled gentlemen's club: FIVE men in top hats and frock coats crowding round a table with pigeons on it, all grinning, and the bearded man among them with his sleeves rolled up.")],
 47: [("XCU","-","study", "EXTREME CLOSE-UP on TWO pigeon skulls side by side on a velvet cloth, wildly different in shape, one long and one snub.")],
 49: [("MED","-","void", "A cartoon ledger on flat cream where a line of pigeons walks across the page and turns into a line of coins halfway along.")],
 51: [("XCU","-","auction", "EXTREME CLOSE-UP on one bright orange pigeon eye filling most of the frame, the white splash of a wing just visible below it.")],
 52: [("MED","-","auction", "TWO enormous leather armchairs turned away from the camera in a dark room, one gold paddle resting on the arm of one and one black paddle on the other, their occupants hidden.")],
 54: [("XCU","-","auction", "EXTREME CLOSE-UP on an auctioneer's gavel striking a wooden block, the impact throwing a small burst of splinters and dust.")],
 60: [("WIDE","narrowed eyes, measuring","village", "A man on a rooftop looking across at his neighbour's much larger loft with his eyes narrowed and his mouth pulled tight, a tape measure hanging forgotten from his hand.")],
 64: [("XWIDE","-","road", "A VAST dry sunlit landscape with a single small van crossing it, carrying one parcel, mountains far behind.")],
 65: [("XCU","-","lab", "EXTREME CLOSE-UP on a tiny specimen jar held in tweezers against an ENORMOUS gold trophy behind it, the jar smaller than one of the trophy's handles.")],
 66: [("MED","-","lab", "SIX small cards laid out on a bench in a row, FIVE of them plain and ONE of them pushed slightly apart from the others, a gloved finger resting on the odd one.")],
 68: [("MED","arms folded, mouths closed","club", "TWENTY loft doors in a long row, every one of them shut, and in front of them SIX men with their arms folded and their mouths closed."),],
 72: [("XWIDE","-","shanghai", "A VAST city of towers at night with a river of light running through it, seen from very high above.")],
 73: [("XWIDE","-","henan", "An ENORMOUS green landscape of terraced fields with one small road crossing it, and far away on the horizon the faint towers of a city.")],
 75: [("MED","brows soft, feeding","shanghai", "The same TWO men on a city rooftop scattering grain for the same birds, their brows soft, the city skyline behind them instead of fields.")],
 79: [("XCU","-","shanghai", "EXTREME CLOSE-UP on a cardboard milk carton with its top folded shut and small air holes punched in the side, one grey feather caught in the fold.")],
 80: [("XCU","-","shanghai", "EXTREME CLOSE-UP on FOUR small gold trophies standing in a row on a table, gleaming, one slightly taller than the rest.")],
 82: [("MED","mouths open, astonished","club", "THREE officials round a table with their mouths open and their eyebrows climbing, one holding a paper tape that has run right off the end of the table and onto the floor.")],
 84: [("WIDE","-","void", "A COLOSSAL heap of BLANK banknotes on flat cream, and a small wooden loft sitting on top of it like a crown.")],
 86: [("XCU","-","court", "EXTREME CLOSE-UP on a wooden gavel resting on its block, still, with a pair of empty handcuffs lying open beside it.")],
 89: [("MED","-","void", "A cartoon iceberg on flat cream with the auctions, a milk carton and a tiny jar drawn on the small part above the water, and one enormous plain nest box filling everything below it.")],
 90: [("XCU","-","void", "EXTREME CLOSE-UP on a plain wooden nest box lined with straw, warm and ordinary, filling the whole frame.")],
 92: [("MED","-","loft", "TWO pigeons building a nest together in a wooden box, one passing a straw to the other, straw scattered around them.")],
 94: [("XWIDE","-","road", "A VAST landscape at dawn with one small lorry crossing it on a thin road, tiny against the distance.")],
 95: [("XCU","-","sky", "EXTREME CLOSE-UP on one grey pigeon's wing driving downward at full stretch, every feather taut, the ground streaking past far below.")],
 99: [("MED","eyes down, sheepish","club", "TEN fanciers in a club room with their eyes down and their hands behind their backs, standing in front of a plain wooden nest box set on a table like an exhibit.")],
 100:[("WIDE","-","auction", "A COLOSSAL gold auction board, a horse trophy, TWO bidding paddles and a brass sealed clock all stacked into an unstable tower on flat cream."),
      ("XCU","-","loft", "EXTREME CLOSE-UP on a plain wooden nest box at the very bottom of that stack, taking the entire weight, unbothered.")],
 102:[("CU","brows soft, besotted","loft", "An old woman filling the frame with a pigeon held against her cheek, her brows soft and her eyes closed, entirely besotted. The whole picture is keyed to warm cream, dusty ORANGE and mustard GOLD.")],
 103:[("XCU","-","brooklyn", "EXTREME CLOSE-UP on an empty wire cage tipped on its side on a stone step, its door hanging open, one grey feather on the ground beside it.")],
 104:[("MED","gone soft, remembering","gym", "An ENORMOUS heavyweight sitting alone on a bench in a dressing room with his gloves off and his face gone soft, watching one small pigeon walk along the bench toward him.")],
 105:[("XCU","-","void", "EXTREME CLOSE-UP on one grey pigeon foot standing squarely on a COLOSSAL BLANK banknote, gripping it.")],
 108:[("XWIDE","-","sky", "An ENORMOUS dawn sky with one bird high in it and, far below at the very bottom edge, a single small open loft door with warm light in it.")],
 109:[("MED","-","void", "A single plain grey feather lying alone on flat cream, taking up very little of the frame.")],
 112:[("WIDE","brows up, turning","loft", "The fancier on his rooftop turning to look at the viewer with his brows up and a small hopeful smile, one hand still shading his eyes as he scans the sky.")],
 115:[("CU","eyes shining, grinning","loft", "The fancier filling the frame with his eyes shining and an ENORMOUS grin breaking across his face, both arms coming up, a wingtip just entering the frame beside him.")],
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
 "glance, in the tradition of classic theatrical cartoon animation. Visible gouache texture, "
 "flat matte, NO gradients, NO airbrushed shading, NO photographic texture, NO "
 "three-dimensional rendering. There is NO text, NO lettering, NO numbers and NO writing of "
 "any kind anywhere in the image; any sign, board, placard, label or banner is completely "
 "BLANK. Any crowd is individuated: different faces, different builds, clothes in DIFFERENT "
 "colours from the palette, never a row of matching coats. These are ORIGINAL characters in a "
 "general mid-century cartoon idiom: NO existing cartoon characters, NO studio logos, NO "
 "trade dress, and no likeness of any real person. ONE SINGLE COHERENT SCENE, NOT a grid of "
 "panels, NOT a sheet of studies. Every animal in this world is an ORDINARY REAL ANIMAL "
 "drawn in the cartoon idiom: birds are real birds with real wings and feathers, standing "
 "on bird feet and behaving like birds. Animals wear no clothing and have no human hands "
 "or human faces. 16:9, edge to edge, one scene, one camera.")

MIN_CAM = {'XCU': 8, 'CU': 18, 'XWIDE': 10}
MAX_RUN = 3
MIN_CU_SHARE = 0.24        # lower than the queue film: this episode is about SCALE too
MIN_EVENT_SHARE = 0.80
MIN_CAST_SHARE = 0.55
MAX_SETTING_SHARE = 0.22   # the loft is this film's bakery queue

FACE = re.compile(r'\beyes?\b|brows?|mouth|jaw|teeth|lips?|grin|laugh|glar|winc|flinch|gasp|'
                  r'blink|snarl|twitch|squint|scowl|beam|gape|yawn|sneer|smil|nostril|cheeks|'
                  r'tongue|chin|frown|preen|besotted|tender|impassive|blank|soft|hard\b', re.I)
EVENT = re.compile(
    r'burst|pop|fly|flying|flew|flar|blast|shoot|erupt|stream|pour|collaps|toppl|crack|snap|'
    r'spring|slam|throw|thrown|swing|scatter|scrambl|clamber|shov|elbow|carr|drop|slid|tipping|'
    r'vibrat|whistl|lift|roll|buckl|hover|dart|curl|glow|steam|smoke|leak|ping|wag|nod|shak|'
    r'crouch|lean|reach|step|walk|run|ride|hold|haul|pull|peer|point|count|examin|charg|chew|'
    r'trudg|wrap|slice|stab|bang|snak|settl|strid|amble|stroll|duck|dig|turn|rub|sip|sail|'
    r'thump|spray|strik|rais|crush|link|crane|hang|stretch|tilt|clamp|wav|file|jostl|squeez|'
    r'press|balanc|climb|land|swarm|feed|trac|receiv|applaud|arriv|load|cross|scratch|tumbl|'
    r'pil|recoil|glanc|hurry|bend|bent|crowd|tear|driv|scribbl|measur|writ|sniff|argu|potter|'
    r'greet|wait|watch|look|grow|open|shut|reced|dwarf|strea|clutch|slip|fork|appear',
    re.I)
CAST = re.compile(r'FANCIER|THE HEN|THE COCK|pigeon|bird|man\b|men\b|woman|women|people|crowd|'
                  r'soldier|official|scientist|technician|fancier|visitor|child|boy|girl|'
                  r'auctioneer|heavyweight|figure|neighbour|racer|cat\b|finch', re.I)

sents = [s.strip() for a in re.split(r'\n\s*\n', (FILM / 'script.txt').read_text())
         if a.strip() for s in re.split(r'(?<=[.!?])\s+', a.strip()) if s.strip()]

errs = []

# NEVER NAME THE ARTEFACT. The narration must not refer to itself as a film, an
# episode or a video — it breaks the spell, and it is the same fault as the
# narrator becoming a persona. The queue episode shipped with two of these
# ("the finding of the whole film", "the part that changes the film") and
# nobody caught them until after publication. Checked here because the board is
# the last gate every script passes through before pictures get paid for.
SELFREF = re.compile(r'\b(film|movie|video|episode|documentary|this programme)\b', re.I)
hits = [(n, s) for n, s in enumerate(sents, 1) if SELFREF.search(s)]
if hits:
    errs.append('narration names the artefact (never do this): ' +
                '; '.join(f'line {n}: "{s[:60]}"' for n, s in hits[:4]))

lines = [s[0] for s in S]
missing = sorted(set(range(1, len(sents) + 1)) - set(lines))
if missing:
    errs.append(f'sentences with no frame: {missing[:12]}')
if lines != sorted(lines):
    errs.append('frames run backwards through the script')
if max(lines) > len(sents):
    errs.append(f'frame points at sentence {max(lines)}; script has {len(sents)}')

braces = [i for i, s in enumerate(S, 1) if '{' in s[4]]
if braces:
    errs.append('unrendered f-string braces: ' + ' '.join('b%02d' % i for i in braces[:10]))

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
    errs.append('expression names no face action: ' + ' '.join('b%02d' % i for i in noface[:10]))
lost = [i for i, s in enumerate(S, 1) if s[2] != '-' and not FACE.search(s[4])]
if lost:
    errs.append('expression absent from the SCENE text: ' + ' '.join('b%02d' % i for i in lost[:10]))
noev = [i for i, s in enumerate(S, 1) if not EVENT.search(s[4])]
if len(S) - len(noev) < MIN_EVENT_SHARE * len(S):
    errs.append(f'physical event on {len(S)-len(noev)}/{len(S)}, needs {MIN_EVENT_SHARE:.0%}; '
                'flat: ' + ' '.join('b%02d' % i for i in noev[:10]))
standing = [i for i, s in enumerate(S, 1) if re.search(r'\bstand(s|ing)?\b', s[4], re.I)]
if len(standing) > 18:
    errs.append(f'"standing" in {len(standing)} scenes; max 18')
cast = [s for s in S if CAST.search(s[4])]
if len(cast) / len(S) < MIN_CAST_SHARE:
    errs.append(f'cast in {len(cast)}/{len(S)} ({len(cast)/len(S):.0%}), needs {MIN_CAST_SHARE:.0%}')

setc = Counter(s[3] for s in S)
for k, n in setc.items():
    if n / len(S) > MAX_SETTING_SHARE:
        errs.append(f'setting "{k}" is {n}/{len(S)} ({n/len(S):.0%}), max {MAX_SETTING_SHARE:.0%}')

# Act 2 is the war act and is staged straight. Nothing in it may be funny.
COMIC = re.compile(r'ABSURD|COLOSSAL|ENORMOUS|comically|cartoon|grin|bulging', re.I)
war = [i for i, s in enumerate(S, 1) if 14 <= s[0] <= 27 and COMIC.search(s[4])]
if war:
    errs.append('comic staging inside the war act: ' + ' '.join('b%02d' % i for i in war))

print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(S)} ({cu/len(S):.0%}) | faces {len([s for s in S if s[2]!='-'])}/{len(S)} | "
      f"events {len(S)-len(noev)}/{len(S)} | cast {len(cast)}/{len(S)} ({len(cast)/len(S):.0%})")
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
    ids.append(f'b{row[0]:02d}' + ('' if n == 0 else chr(ord('a') + n)))
assert len(set(ids)) == len(ids), 'duplicate frame id'

(FILM / 'production').mkdir(exist_ok=True)
(FILM / 'production' / 'prompts.json').write_text(json.dumps(
    {i: f'{CAM[s[1]]} {strip_cam(s[4])} {WORLD}' for i, s in zip(ids, S)}, indent=1))
(FILM / 'production' / 'board.json').write_text(json.dumps(
    [{'id': i, 'line_no': s[0], 'camera': s[1], 'expression': s[2], 'setting': s[3],
      'line': sents[s[0] - 1], 'scene': s[4]} for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S)
          if 'VERMILION RED coat' not in s[4] and 'THE HEN' not in s[4] and 'THE COCK' not in s[4]]
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
