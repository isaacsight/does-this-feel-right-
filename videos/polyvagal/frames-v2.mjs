/**
 * THE THIRD THING — v2 frames. 54 scenes. ONE ORDINARY DAY, IN ORDER.
 *
 * v1 was a lecture with 86 illustrations and the viewer got lost. This is the
 * same narration told as one continuous day in one person's life:
 *
 *   09:00 the meeting (the freeze)  ->  REWIND to 07:00  ->  back to the meeting
 *   ->  lunch  ->  afternoon  ->  supermarket at dusk  ->  evening sofa
 *   ->  01:00 bed  ->  [one step outside the day: the lab]  ->  late night floor
 *
 * WHY A DAY: light tells the viewer where they are without a word — warm
 * morning, flat office fluorescent, blue dusk, dark bedroom. Locations repeat
 * instead of multiplying. And the film opens on the hero frozen and alone in a
 * meeting and closes on them flat on the floor with a dog beside them: same
 * posture, opposite meaning.
 *
 * THE FORMULA, every frame: a situation an ordinary person has lived through,
 * resolved by an IMPOSSIBLE cartoon-physics consequence, which NOBODY in frame
 * acknowledges. Never draw the concept — draw the person it happens to.
 *
 * CAST: opossum = the shutdown state · lizard = the "ancient" system, pays off
 * in the honest beat · dog = co-regulation · the colleague = the world not
 * noticing · the clinician = described, never explained.
 *
 * `line` is the sentence each frame must land on. No even distribution.
 */

export const V2 = [
  // ══════════════ 09:00 — THE MEETING. Flat office fluorescent, grey-blue.
  { id: 'g01', line: "There's a third thing your body does when it's frightened.",
    scene: 'A drab open-plan office under flat fluorescent light, mid-morning. In a glass meeting room every colleague has turned expectantly toward the character, who has gone completely rigid and turned to grey stone mid-gesture, hairline cracks running up one arm. Nobody reacts. A red folder on the table.' },
  { id: 'g02', line: 'Not fight.',
    scene: 'Same office meeting room, flat fluorescent light. For one absurd instant the character is in an enormous boxing stance on the table, fists raised, eyes manic, squaring up to a swivel chair. The colleagues carry on talking. One red boxing glove.' },
  { id: 'g03', line: 'Not flight.',
    scene: 'Same meeting room. A perfect character-shaped hole is smashed clean through the glass wall, dust still hanging in the air, a chair spinning. Two red shoes remain neatly on the carpet where they were standing. The meeting continues.' },
  { id: 'g04', line: 'It just stops.',
    scene: 'Same meeting room, flat fluorescent light. The character simply sits there, arms limp, eyes completely flat and empty. Nothing is happening at all. An opossum lies flat on the table in front of them. Nobody looks at it. A red folder.' },

  // ══════════════ REWIND — 07:00. Warm low morning sun through a window.
  { id: 'g05', line: 'Heart going, hands cold,',
    scene: 'A small kitchen at seven in the morning, warm low sun through the window. The character stands over a kettle as an enormous red cartoon heart punches repeatedly out through the front of their shirt, denting it outward each time. A dog watches, unbothered.' },
  { id: 'g06', line: 'ready to swing or ready to leave.',
    scene: 'The same warm morning kitchen. Both of the character\'s hands have snapped clean off at the wrists and lie on the counter as two blue-white blocks of ice, still gripping a mug. Their expression is only mildly inconvenienced. A red kettle.' },
  { id: 'g07', line: "That's been the whole story of stress for a hundred years. It was never the whole story.",
    scene: 'The same kitchen. On the wall hang two framed diagrams thick with cobwebs and hanging crooked, and between them a third empty hook with nothing on it. The character squints at the empty hook while eating toast. A red frame on one diagram.' },
  { id: 'g08', line: 'The meeting where you should speak, and don\'t.',
    scene: 'Back in the office meeting room under flat fluorescent light. Every colleague has turned to the character, whose lower jaw has detached completely and clattered onto the table in front of them. They stare back. Nobody looks at the jaw. A red folder.' },
  { id: 'g09', line: 'The argument where you go completely blank.',
    scene: 'The kitchen that evening, dim warm lamp light. One figure is mid-rant, arms flying. Opposite them the character has gone entirely transparent from the neck up, the cupboards visible straight through their head. A red kettle on the counter.' },
  { id: 'g10', line: 'The bad news that lands, and you feel nothing.',
    scene: 'A hallway by a front door, grey daylight. The character holds an opened letter, face completely neutral — while their whole body has deflated like a balloon into a flat empty skin puddled around their feet, one hand still holding the letter up. A red envelope on the mat.' },
  { id: 'g11', line: 'Not calm. Empty.',
    scene: 'A living room, flat grey afternoon light. The character sits bolt upright on a grey sofa, hands on knees, eyes open and nobody home. A houseplant has grown up through their legs and out of one sleeve. A red mug beside them wears a thick cobweb.' },
  { id: 'g12', line: 'Therapists watched people do this for decades.',
    scene: 'A therapy room, soft daylight. A clinician sits holding a red clipboard, nodding with deep professional recognition, opposite a client who has melted completely off the couch into a puddle on the rug. An opossum lies flat in the puddle. The clinician keeps nodding.' },
  { id: 'g13', line: 'Described it perfectly. Couldn\'t explain it.',
    scene: 'The same therapy room. The clinician alone, pen hovering over a completely blank page, mouth open — while behind them the entire wall of framed certificates silently falls off its hooks and smashes on the floor. They do not turn around. Red clipboard.' },

  // ══════════════ II — THE PROPOSAL. Lecture hall, then the day resumes.
  { id: 'g14', line: 'Then in 1994, a neuroscientist called Stephen Porges said the map was wrong.',
    scene: 'A drab lecture hall. The character stands at a red podium, one finger raised in triumph. Every person in the audience is fast asleep, heads back, mouths open — except one figure standing on a chair applauding wildly. An opossum sleeps in the front row.' },
  { id: 'g15', line: 'Not two settings. Three.',
    scene: 'An office lift. The control panel has two worn buttons and a third that is brand new and glowing red. The character presses the new one. A lizard stands beside them facing the doors, deadpan. Flat fluorescent light.' },
  { id: 'g16', line: "One for when you're safe — and it doesn't just calm you down, it turns your face on.",
    scene: 'A cafe at eight in the morning, warm sun through the window. The character\'s round face has visibly lit up like a lamp, glowing warm gold and casting light across the table onto a delighted friend. A red mug between them. A dog under the table.' },
  { id: 'g17', line: 'Your voice warms. You can be with people.',
    scene: 'The same sunny cafe. The character is talking animatedly and their words come out as small visible curls of warm steam, which the friend is cheerfully warming their hands on. A red mug on the table.' },
  { id: 'g18', line: 'One for threat. Heart up, muscles loaded, fight or run.',
    scene: 'The same cafe one instant later. Every head has snapped toward an offscreen noise. The character has gone rigid with hair vertical and their feet are already spinning in mid-air like a cartoon about to launch. A mug knocked over, red liquid mid-spill.' },
  { id: 'g19', line: 'And one for when you can\'t do either. When you can\'t fight it and you can\'t leave.',
    scene: 'The office meeting room with the door shut, flat fluorescent light, no way out. The character stands in the middle. Their fist has clearly just bounced off the glass wall and is still vibrating. A red mark where it hit.' },
  { id: 'g20', line: "That one doesn't ease off. It stands on the brake. Everything down. Still.",
    scene: 'The same meeting room. The character has fallen straight through the floor leaving a perfect character-shaped hole in the carpet, only their startled face visible at the bottom. An opossum peers into the hole. The meeting continues above. A red folder.' },
  { id: 'g21', line: "And here's what made this land in therapy rooms. Shutting down isn't weakness.",
    scene: 'The therapy room, soft daylight. The clinician points at the puddled client with an expression of genuine delighted recognition, as though something has finally made sense. The client remains a puddle. A red cushion.' },
  { id: 'g22', line: "It's the oldest trick there is. Play dead.",
    scene: 'The office carpet. The character lies rigid on their back with all four limbs straight up in the air. An opossum lies beside them in the identical pose. A lizard lies on the other side, also identical. All three completely serious. A red folder on the floor.' },

  // ══════════════ III — NEUROCEPTION. Lunchtime, brighter, out of the office.
  { id: 'g23', line: "So who's choosing?",
    scene: 'A car at midday moving fast, landscape a horizontal blur through every window. The driver seat is completely empty. The character leans in from the passenger side with both hands raised in an enormous shrug. A lizard sits calmly in the back. A red steering wheel.' },
  { id: 'g24', line: "Because you don't sit down and pick one.",
    scene: 'A staff room armchair. The character jabs at a television remote that has no buttons on it whatsoever, turning it over and over. A red remote. A dog watches from the doorway.' },
  { id: 'g25', line: 'Porges gave it a name. Neuroception.',
    scene: 'A doorway into a busy staff kitchen at lunchtime. The character has one foot through it and every person inside has frozen mid-sentence and turned to look — while the character\'s own hair has already stood bolt upright before their face has caught up. A red door.' },
  { id: 'g26', line: 'Not perception — perception is something you do. This is done to you.',
    scene: 'A lunch table. The character sits calmly reading, entirely relaxed — while their own body from the neck down has silently stood up and is tiptoeing away toward the exit without them. A red book in their hands.' },
  { id: 'g27', line: 'Underneath awareness, constantly, reading the room. A face. A tone. Something behind you.',
    scene: 'An office kitchen. The character makes tea, perfectly serene — while both of their eyes have detached and float on long stalks around the room, one peering at a frowning colleague, one aimed backwards at the door. A red mug.' },
  { id: 'g28', line: "Picking a setting before you've had an opinion.",
    scene: 'The same office kitchen. The character is calmly mid-sip while their hair, their shirt, the steam from the mug and a passing sheet of paper are all already blown completely flat backwards by something offscreen. A red mug.' },
  { id: 'g29', line: 'Hear four words and go on guard.',
    scene: 'An office corridor. A colleague has said something perfectly ordinary — and the character has instantly grown a full suit of plate armour, visor down, standing rigid in the corridor. The colleague keeps talking, entirely unbothered. A red plume on the helmet.' },
  { id: 'g30', line: "You weren't being paranoid. You were being informed. Late.",
    scene: 'An office stairwell. The character stands with hair vertical and eyes enormous, having clearly just understood something — while a single sheet of paper drifts gently down from above and lands on their head. An opossum sits on the stairs. A red handrail.' },

  // ══════════════ IV — CO-REGULATION. Afternoon into dusk.
  { id: 'g31', line: "And you don't do it alone.",
    scene: 'A bus stop bench in the late afternoon, long low light. The character vibrates violently with squiggle lines, physically blurred at the edges. A stranger sits down beside them. A dog sits between them. A red bench slat.' },
  { id: 'g32', line: 'Nervous systems settle each other.',
    scene: 'The same bench a moment later, same low light. The squiggle lines have visibly slid across into the stranger, who is now the one juddering, while the character sits perfectly still, slightly surprised. The dog has not moved. A red bench slat.' },
  { id: 'g33', line: 'Someone picks up a screaming child and the child stops.',
    scene: 'A supermarket queue at dusk. A tiny figure screams with a mouth wider than its own head, sound lines blasting everyone\'s hair straight back down the aisle. An adult reaches down for it. A red shopping basket.' },
  { id: 'g34', line: 'Not because of an argument. Because of a heartbeat.',
    scene: 'The same queue. The tiny figure is now completely serene, held against the adult, eyes closed, a visible red heart beating gently in the adult\'s chest. Everyone else\'s hair is still blown backwards. Nobody comments.' },
  { id: 'g35', line: 'That never stops being true. It just gets less obvious.',
    scene: 'A sofa at dusk. Two adult characters in exactly the pose of the parent and child, one leaning on the other, both looking mildly embarrassed about it. A dog is squeezed between them. A red mug on the table.' },
  { id: 'g36', line: 'Someone walks in and the room loosens.',
    scene: 'A tense meeting room of rigid figures under fluorescent light. A door opens — and every single skeleton has dropped straight out of every body, leaving them all puddled happily in their chairs. Nobody remarks on the skeletons. A red door.' },
  { id: 'g37', line: "Someone else walks in and it doesn't.",
    scene: 'The same room, a different door. Everyone has snapped bolt upright with hair standing vertically, several inches of clear air under everyone in their seats. One figure has turned entirely to grey stone. A red door.' },
  { id: 'g38', line: "You're built to be calmed down by somebody.",
    scene: 'A living room in the evening, one lamp on. The character sits alone trying to pat their own head soothingly with both hands at once, wearing a determined and unsuccessful expression. A dog watches from the doorway with obvious pity. A red mug.' },
  { id: 'g39', line: 'Which is a humiliating thing to find out about yourself in your thirties.',
    scene: 'The same lamplit living room. The dog has put its chin on the character\'s knee and the character\'s steam is visibly retracting back into their ears, shoulders dropping. Their expression is deeply undignified relief. A red collar on the dog.' },

  // ══════════════ V — TODAY. Evening into 01:00.
  { id: 'g40', line: 'Every signal this thing runs on is analogue. A face. A voice with warmth in it.',
    scene: 'The living room, evening lamp light. The character holds up a detached cartoon face, a detached mouth and a detached ear like three old hand tools, inspecting them seriously. A red toolbox open at their feet.' },
  { id: 'g41', line: "So we've spent twenty years trying to warm up by describing a fire.",
    scene: 'The same living room, now freezing — the character\'s breath visible, frost forming on their shoulders and on the sofa — while they hold a glowing phone up toward themselves as though warming their hands on it. A red phone case. A dog shivers beside them.' },
  { id: 'g42', line: 'You text instead of calling.',
    scene: 'Two figures at opposite ends of one grey sofa in the evening, each texting the other, neither looking up. Between them sits a third character hopefully holding out two tin cans joined by string. Both ignore it. Both screens red.' },
  { id: 'g43', line: 'Camera off.',
    scene: 'A dark room lit only by a laptop. The character faces a wall of blank grey rectangles, their own tiny lit face the only one on screen — and they have physically begun to fade out at the edges, one hand already gone. A red laptop.' },
  { id: 'g44', line: "And then there's the scroll — which is strange, because it looks like rest.",
    scene: 'A bedroom at one in the morning, almost black except for the phone. The character has sunk so deeply into the mattress that only their phone-lit face and one thumb remain above the duvet. Utterly vacant. A red phone screen.' },
  { id: 'g45', line: "You're lying down. You're not moving. So does a possum.",
    scene: 'The same dark bedroom. An opossum lies flat on the duvet beside the sunken character in the exact same vacant pose, tongue out. Neither moves. A lizard is asleep on the pillow. The phone screen is red.' },
  { id: 'g46', line: 'No face. No voice. Nobody regulating anybody.',
    scene: 'Close on a phone in the dark, held in a thin hand, showing a completely featureless blank oval where a face should be. The hand has gone grey and slightly stony. A red phone case.' },
  { id: 'g47', line: 'You can rest all evening and stand up emptier than you sat down.',
    scene: 'The living room, late. The character stands up off the grey sofa leaving a deep character-shaped dent behind — and is now visibly two thirds of their former height, shrunken. An opossum has instantly taken the dent. A red mug.' },
  { id: 'g48', line: 'Fine, but flat. Not upset. Just not quite here.',
    scene: 'The cafe again, but now in flat grey light. The character gives a small polite thumbs-up to a friend while being completely two-dimensional, like a paper cutout, edges fluttering in a draught. The friend chats on happily. A red mug.' },

  // ══════════════ VI — THE HONEST BEAT. The one step outside the day.
  { id: 'g49', line: 'The biology here is contested.',
    scene: 'A brightly lit laboratory — the only place in the film that is not part of the day. Two figures in white coats arm-wrestle furiously across a bench over a wobbling model, both deadly serious, beakers rattling. A lizard watches from the bench. The model is red.' },
  { id: 'g50', line: "The evolutionary story doesn't survive comparison with other animals.",
    scene: 'The same laboratory. The character holds a small mammal figurine proudly aloft — while behind them an orderly queue of a crocodile, an owl, an octopus, a lizard and an opossum waits patiently for a turn to speak, stretching out of frame. The character has not noticed. A red base on the figurine.' },
  { id: 'g51', line: 'a paper took its five founding premises and challenged every one. Like a man losing an argument in front of his own family.',
    scene: 'A dining room. The character holds a stack of five plates and four have already exploded across the floor. Their expression has not changed at all. Seated family members continue eating calmly. One remaining plate is red.' },
  { id: 'g52', line: "Porges answered. It isn't settled.",
    scene: 'The laboratory. Two figures in white coats sit back to back at desks writing furiously, stacks of paper piled to the ceiling on either side, neither ever turning around. A red pen lies on the floor between them.' },

  // ══════════════ VII — THE TURN. Late night. Same posture, opposite meaning.
  { id: 'g53', line: 'It spread because it put a word to something real. Going still. Going blank.',
    scene: 'The office meeting room from the opening, flat fluorescent light. Once again a figure has melted into a puddle on the floor beneath the table. A colleague steps carefully over them carrying a coffee, without looking down, and says nothing. A red folder.' },
  { id: 'g54', line: 'And what it points at? A face. A voice.',
    scene: 'Close on a second character\'s warm open face in soft lamp light, looking directly at the viewer, eyes creased, completely present. Uncluttered composition. A red collar.' },
  { id: 'g55', line: 'A slow breath. Someone in the room.',
    scene: 'A kitchen late at night, one warm lamp. The character exhales so thoroughly that their shoulders have dropped a full head\'s height and they are noticeably shorter, entirely at peace. A dog leans against their leg. A red mug on the counter.' },
  { id: 'g56', line: 'Like directions from someone clearly drunk who does genuinely live here.',
    scene: 'A street corner at night under one streetlamp. A cheerfully unsteady figure points confidently down a road while the character listens politely, taking the direction completely seriously. A red door on the house behind. A lizard sits on the wall.' },
  { id: 'g57', line: 'That it stops you being embarrassed about the part of you that goes quiet.',
    scene: 'The office floor at night, lights off, one window glowing. The character lies flat on their back staring at the ceiling — and a dog has simply lain down flat beside them in the same position, also staring at the ceiling. An opossum lies on the other side. Nobody says anything. A red mug on its side.' },
]

/**
 * Two reshoots. Both rendered sound-effect text ("crash", "WOBBLE") — and both
 * because I described MOTION. A wall of certificates falling invites "crash";
 * a door swinging invites "WOBBLE". Same lesson as the v1 lettering failures in
 * a new costume: the model draws what the described action implies, and comic
 * motion implies a sound effect. Restaged as aftermath, not action.
 */
export const V2_FIX = [
  { id: 'g13', line: "Described it perfectly. Couldn't explain it.",
    scene: 'A therapy room in soft daylight. A clinician sits alone in an armchair, pen hovering over a completely blank page, mouth open. Behind them the wall is bare except for empty hooks, and every framed certificate lies already smashed and still on the floor. Nothing is moving. They have not turned around. A red clipboard.' },
  { id: 'g25', line: 'Porges gave it a name. Neuroception.',
    scene: 'A staff kitchen at lunchtime seen from inside. The character stands still in an open doorway with one foot forward. Every person in the room has stopped mid-sentence and is staring silently at them. The character\'s hair is standing bolt upright while their face is still calm and has not caught up. Everything is completely still. A red door frame.' },
]

/**
 * Four fills. Content-locking exposed four narration beats with no frame, so
 * the preceding image stretched across them — worst was 15.8s on a still.
 * These are not decoration; each one is a line that was going unillustrated.
 */
export const V2_FILL = [
  { id: 'h01', line: "Because there's a third one nobody gave you a word for.",
    scene: 'A kitchen table in warm morning light. The character gestures helplessly at their own chest trying to explain something to a friend — and their words are coming out as small blank grey blobs that drop onto the table and sit there. The friend waits patiently. A red mug.' },
  { id: 'h02', line: 'Look at what the last 20 years quietly removed.',
    scene: 'A living room in the evening. Everything is in place except there is a clear person-shaped clean patch in the dust on one end of the sofa, and a clean rectangle on the sideboard where a telephone used to sit. The character stands looking at the empty sofa cushion. A red mug on the table.' },
  { id: 'h03', line: 'And in 2023 a paper took its five founding premises and challenged every one.',
    scene: 'A laboratory. A figure in a white coat calmly removes one single card from the bottom of a tall house of cards, entirely deadpan, while the character watches in open horror with both hands on their head. A lizard sits on the bench. One card is red.' },
  { id: 'h04', line: 'Which might be the most useful thing about it.',
    scene: 'A street at night under a streetlamp. The character walks home carrying a small wobbly red model tucked casually under one arm like a takeaway, completely at ease, a dog trotting alongside. An opossum walks the other way on the opposite pavement.' },
]

/**
 * Continuity reshoot. g31 rendered as a DAYLIGHT bus stop with a red bus; g32
 * — which is meant to be the same bench one moment later, as the squiggles
 * transfer — came back as night on a different bench. The gag depends entirely
 * on it being the same shot, so g32 is redone to match g31's late-afternoon
 * light and setting. Act IV is afternoon, so daylight is the correct one.
 */
export const V2_CONT = [
  { id: 'g32', line: 'Nervous systems settle each other.',
    scene: 'The exact same city bus stop in warm late-afternoon daylight, a red bus at the kerb behind, the same wooden bench. Two characters sit side by side. The squiggle lines have visibly slid across from the first into the second, who is now the one juddering and blurred, while the first sits perfectly still looking mildly surprised. A dog sits between them, unmoved.' },
]
