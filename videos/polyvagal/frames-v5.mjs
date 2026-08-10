/**
 * THE THIRD THING — v5 frames. 50 shots.
 *
 * `kind` is tagged on every entry so the mix is auditable, not assumed:
 *   lit   — LITERAL. Draw the sentence. Used wherever a viewer could
 *           misunderstand. This is the majority.
 *   obj   — OBJECTION. The narrator says "you'll tell me X"; the hero visibly
 *           protests and the picture proves him wrong. The film's engine.
 *   phys  — CARTOON PHYSICS. Only where narration has already made the point
 *           and the image cannot be misread.
 *   chair — THE ANCHOR. Same person, same chair, same room. Returns on every
 *           mention of the three settings so a lost viewer can re-enter.
 *   flour — ABSURD FLOURISH. Rationed. Opossum, lizard.
 *
 * DECISION RULE: can the viewer be wrong about what they are seeing? If yes it
 * must be `lit`. v2 applied physics everywhere, so the puns replaced the
 * explanation instead of decorating it.
 *
 * THE CHAIR: one plain wooden chair in one plain room, shot from the same angle
 * every time. It is the spine of the film.
 */

export const V5 = [
  // ── OPEN: the meeting
  { id: 'v01', kind: 'lit', line: "You've felt this. You've probably never had a name for it.",
    scene: 'A plain office meeting room. Six colleagues sit around a table, all turned toward one character who sits frozen with a completely blank face, mouth slightly open, nothing coming out. Everyone else looks expectant. A red folder on the table.' },
  { id: 'v02', kind: 'lit', line: 'Someone asks you a question in a meeting. You know the answer. And nothing comes out.',
    scene: 'Close on the same character at the meeting table. Their mouth is open and completely empty — a small black void where words should be. Eyes wide, sweating. A colleague leans in, waiting patiently. A red folder.' },
  { id: 'v03', kind: 'obj', line: "And you'll tell me that doesn't happen to you. It happened on Tuesday.",
    scene: 'The same character standing in the office, arms folded, chin up, shaking their head firmly in denial with a confident dismissive expression — while directly behind them, in the meeting room through a glass wall, an identical frozen version of themselves still sits blank at the table. They have not noticed it. A red folder.' },

  // ── THE OLD MODEL
  { id: 'v04', kind: 'lit', line: 'For about a hundred years, science had two explanations for stress. Fight, or run.',
    scene: 'A plain wall holding exactly two old framed illustrations, thick with dust: one shows a stick figure with fists raised, the other shows a stick figure running. The character stands looking at them, hands on hips. One frame is red. No writing anywhere.' },
  { id: 'v05', kind: 'obj', line: "You'll say you do neither, because you stay calm. You didn't stay calm.",
    scene: 'The character stands with one hand on their chest, giving a serene reassuring smile directly at the viewer, eyes half closed, radiating calm — while their other hand grips the back of a chair so hard the wood is splintering and cracking. A red chair.' },
  { id: 'v06', kind: 'phys', line: 'You went still.',
    scene: 'The character stands completely rigid in the middle of the office, arms at their sides, eyes flat and open. They have turned entirely to grey stone, cracks running up one leg. A colleague walks past reading a red folder without looking up.' },
  { id: 'v07', kind: 'obj', line: "You'll call that composure. You went grey and stopped blinking.",
    scene: 'Extreme close-up of the stone-grey face, cracked, eyes wide open and unblinking, absolutely no expression at all. A single small red button on the collar below.' },

  // ── THE PROPOSAL
  { id: 'v08', kind: 'lit', line: "Therapists watched people do this for decades and couldn't explain it.",
    scene: 'A therapy room. A clinician sits with a red clipboard and a pen, watching a client who has gone completely blank and slumped sideways in an armchair. The clinician\'s page is entirely empty. They look genuinely stumped.' },
  { id: 'v09', kind: 'lit', line: 'Then in 1994, a neuroscientist called Stephen Porges suggested something simple.',
    scene: 'A plain lecture room. A figure stands at a red podium with one hand raised mid-explanation, addressing a small seated audience who are actually listening. Calm and clear, not chaotic. An opossum sits in the front row.' },
  { id: 'v10', kind: 'lit', line: "There aren't two settings. There are three.",
    scene: 'The same plain wall from before with the two dusty framed illustrations — and now a third, brand new, clean frame has been hung beside them, containing a stick figure sitting perfectly still in a chair. The character stands looking up at the new one. The new frame is red.' },

  // ── SETTING ONE
  { id: 'v11', kind: 'chair', line: "Here's the first. You're with someone you trust.",
    scene: 'A plain room with one plain wooden chair, shot square on. The character sits in it, relaxed and open, leaning slightly forward, smiling at a friend sitting opposite. Warm light. A red mug on a small table between them.' },
  { id: 'v12', kind: 'lit', line: "You're relaxed, you're talking, your face moves easily.",
    scene: 'Close on the character\'s face in warm light, mid-conversation, genuinely animated — eyebrows up, eyes creased, mouth open in an easy laugh. A red collar button.' },
  { id: 'v13', kind: 'flour', line: 'Everyone likes this one.',
    scene: 'Wider on the same warm room: the character and their friend both laughing, and a dog has put its head in the character\'s lap. An opossum is also sitting on the chair arm, entirely relaxed. Nobody reacts to the opossum. A red mug.' },

  // ── SETTING TWO
  { id: 'v14', kind: 'chair', line: "Here's the second. Something goes wrong.",
    scene: 'The identical plain room and the same wooden chair, shot from the same square-on angle — but the light has gone cold and hard. The character sits bolt upright, gripping both armrests, eyes enormous, staring at something offscreen. The red mug has been knocked over.' },
  { id: 'v15', kind: 'lit', line: 'Heart up, muscles tight, ready to argue or ready to leave.',
    scene: 'The same chair. The character is now half out of it, one foot already pointed at the door, one fist clenched, body torn between the two directions. A big red cartoon heart thumps visibly through their shirt.' },
  { id: 'v16', kind: 'lit', line: 'Everyone knows this one too.',
    scene: 'A street. Several ordinary characters caught in the same startled posture at once — shoulders up, eyes wide, all turned toward one offscreen noise. Completely recognisable. One red bag.' },

  // ── SETTING THREE
  { id: 'v17', kind: 'chair', line: "And here's the third. The one you don't want.",
    scene: 'The identical plain room and the same wooden chair from the same square-on angle. The light is flat and grey. The chair is occupied by the character sitting utterly motionless, arms limp at their sides, eyes open and empty. The red mug lies on the floor.' },
  { id: 'v18', kind: 'lit', line: "You can't fight. You can't leave.",
    scene: 'The character in a small plain room with no door and no window at all. They stand in the middle having clearly just tried both — one fist red and sore, one shoe scuffed. They are looking around for an option that does not exist. A red mark on the wall.' },
  { id: 'v19', kind: 'phys', line: 'So your body does the only thing it has left. It shuts down.',
    scene: 'The same sealed room. The character has melted completely off their feet into a soft puddle of limbs on the floor, face still visible and calm on top of the pile. An opossum lies flat beside them. A red mug on its side.' },
  { id: 'v20', kind: 'lit', line: 'Your heart slows.',
    scene: 'Close on the character\'s chest where the big red cartoon heart sits — now barely moving, half-lidded and sleepy, ticking over slowly.' },
  { id: 'v21', kind: 'phys', line: 'You go quiet. You go blank.',
    scene: 'Close on the character\'s face, which has gone completely featureless and smooth — no eyes, no mouth, just a blank oval. Their body posture is entirely normal. A red collar button.' },
  { id: 'v22', kind: 'chair', line: 'Same person. Same chair. Three completely different settings.',
    scene: 'A single wide shot showing the same plain wooden chair three times side by side in the same room. In the first the character sits relaxed and smiling in warm light. In the second they are bolt upright and alarmed in cold light. In the third they sit limp and blank in flat grey light. One red mug appears in each: upright, knocked over, on the floor.' },

  // ── WHY IT LANDED
  { id: 'v23', kind: 'lit', line: 'And here\'s why that landed in therapy rooms.',
    scene: 'The therapy room again. The clinician is now sitting forward with an expression of genuine recognition and relief, pointing gently at the slumped client with a pen, finally understanding something. A red clipboard.' },
  { id: 'v24', kind: 'lit', line: "If shutting down is a setting your body switches into, then going blank isn't weakness.",
    scene: 'A plain room. The character sits in the wooden chair looking blank, and a friend crouches beside the chair with a hand on their arm, calm and unbothered, clearly not judging them at all. A red mug on the floor.' },
  { id: 'v25', kind: 'lit', line: "It isn't you failing to cope.",
    scene: 'Close on the character\'s blank face while a friend\'s hand rests on their shoulder in frame. Nobody is panicking. Quiet and matter-of-fact. A red sleeve.' },
  { id: 'v26', kind: 'lit', line: "It's the oldest survival move there is. Play dead.",
    scene: 'A grass verge. An opossum lies flat on its back with all four paws in the air, tongue out, playing dead with total commitment. Nothing else in frame. One red leaf beside it.' },
  { id: 'v27', kind: 'obj', line: "And you're going to argue with that. From the floor. Where you are currently lying. Thinking.",
    scene: 'The character lies flat on their back on an office floor with one finger raised in the air, mid-objection, mouth open as if making an excellent point. An opossum lies beside them in the same pose, also with one paw raised. A red mug on its side.' },

  // ── NEUROCEPTION
  { id: 'v28', kind: 'obj', line: "So who's doing the switching? You'll say you are.",
    scene: 'The character stands pointing confidently at their own chest with both thumbs, chin up, entirely certain — while behind them a small control panel on the wall is visibly flipping its own switches with nobody touching it. A red switch.' },
  { id: 'v29', kind: 'lit', line: 'Think about walking into a room where two people have just stopped talking.',
    scene: 'A doorway into an office kitchen. The character has one foot through the door. Two colleagues inside have stopped mid-sentence and are looking straight at them in silence. Completely ordinary and immediately recognisable. A red mug on the counter.' },
  { id: 'v30', kind: 'lit', line: 'You knew something was wrong before you could say what.',
    scene: 'Close on the character in that doorway. Their face is still neutral and unsuspecting, but their shoulders have already risen up around their ears and their free hand has gripped the door frame white-knuckled. A red door frame.' },
  { id: 'v31', kind: 'lit', line: 'You didn\'t decide that. Something checked the room and made the call for you.',
    scene: 'The same doorway, seen from behind the character. A small plain lever on their back has already been pulled down into a new position by nothing at all. The character faces forward, unaware. The lever is red.' },
  { id: 'v32', kind: 'lit', line: "Porges called it neuroception. You're not doing it. It's being done to you.",
    scene: 'The character sits calmly reading a book in an armchair, completely at ease — while their whole body from the neck down has quietly stood up and is tiptoeing out of the room without them. A red book.' },
  { id: 'v33', kind: 'lit', line: 'Constantly. Underneath everything.',
    scene: 'A wide, ordinary street scene. Every single character walking along it has a small identical lever on their back, and all of them are in slightly different positions. Nobody is looking at anybody else\'s. One lever is red.' },
  { id: 'v34', kind: 'obj', line: 'Most people hate that.',
    scene: 'Close on the character\'s face wearing an expression of pure sour resentment, arms folded, looking directly at the viewer, entirely unimpressed by what they have just been told. A red collar button.' },

  // ── CO-REGULATION
  { id: 'v35', kind: 'lit', line: 'Watch someone pick up a crying baby. The baby stops.',
    scene: 'A supermarket aisle. A tiny figure is screaming with a mouth wider than its own head, blasting everyone\'s hair backwards down the aisle. An adult is reaching down to pick it up. A red shopping basket.' },
  { id: 'v36', kind: 'lit', line: 'Not because of anything anyone said. Because of a heartbeat, and a voice.',
    scene: 'The same aisle a moment later. The tiny figure is completely calm and held against the adult\'s chest, eyes shut, with a red heart beating gently where its ear is resting. Everyone else\'s hair is still blown backwards.' },
  { id: 'v37', kind: 'lit', line: 'You never grow out of that.',
    scene: 'A sofa. Two grown characters sit in exactly the pose of the adult and the baby, one leaning against the other\'s chest, both looking slightly embarrassed but not moving. A dog is squashed between them. A red mug.' },
  { id: 'v38', kind: 'lit', line: 'Someone walks into a room and it relaxes.',
    scene: 'A tense office meeting of stiff upright figures. A door has opened and every single person has visibly softened and slumped comfortably in their chair at once, faces relieved. A red door.' },
  { id: 'v39', kind: 'lit', line: "Someone else walks in and it doesn't.",
    scene: 'The identical room and the identical people, a different door. Everyone has snapped bolt upright and rigid, several figures lifted clear off their seats, hair standing straight up. A red door.' },
  { id: 'v40', kind: 'lit', line: "Porges called this co-regulation. You're built to be calmed down by other people.",
    scene: 'The plain wooden chair again. The character sits in it looking wrecked, and a friend has simply pulled a second chair alongside and sat down next to them, saying nothing. Both facing forward. A red mug between them.' },
  { id: 'v41', kind: 'obj', line: "You'll want to tell me you're self-sufficient. You're patting your own head.",
    scene: 'The character sits alone in the wooden chair, patting the top of their own head with both hands at once, wearing a determined and entirely unconvincing expression. A dog watches from the doorway with visible pity. A red mug.' },

  // ── TODAY
  { id: 'v42', kind: 'lit', line: 'Every one of those signals is a face, a voice, or a person nearby.',
    scene: 'The character holds three things up in their hands and examines them like tools: a detached cartoon face, a detached mouth, and a detached ear. Plain room, plain light. A red toolbox open at their feet.' },
  { id: 'v43', kind: 'lit', line: 'We text instead of calling.',
    scene: 'Two characters sit at opposite ends of one small sofa, each typing on a phone to the other, neither looking up. Both screens glow red. Utterly ordinary and slightly sad.' },
  { id: 'v44', kind: 'lit', line: 'We take the meeting with the camera off.',
    scene: 'A dim room. The character sits facing a screen full of blank grey rectangles, their own small lit face the only visible one. A red laptop.' },
  { id: 'v45', kind: 'phys', line: 'We lie in bed scrolling, which looks like rest and settles nothing.',
    scene: 'A bedroom at night, almost dark. The character has sunk so deep into the mattress that only their phone-lit face and one thumb remain above the duvet, entirely vacant. An opossum lies flat on the duvet in the same pose. A red phone screen.' },
  { id: 'v46', kind: 'phys', line: "You've been resting for four hours. You feel worse.",
    scene: 'The character stands up off a sofa leaving a deep character-shaped dent in the cushion — and is visibly smaller and more crumpled than before, shoulders sagging. A red mug on the table. A wall clock behind shows it is late.' },

  // ── HONEST BEAT
  { id: 'v47', kind: 'lit', line: 'The biology behind all this is genuinely disputed.',
    scene: 'A laboratory. Two figures in white coats face each other across a bench, both talking at once and pointing at the same wobbling model, neither backing down. A lizard watches from the bench. The model is red.' },
  { id: 'v48', kind: 'lit', line: 'a paper went through the theory\'s five main claims and challenged every one of them.',
    scene: 'The same laboratory. A figure in a white coat calmly lifts one card out of the bottom of a tall house of cards while the character watches in open horror with both hands on their head. One card is red.' },

  // ── THE TURN
  { id: 'v49', kind: 'lit', line: 'People do go still. People do go blank.',
    scene: 'The office meeting room from the opening, exactly the same angle. Once again a character sits frozen and blank while the meeting carries on around them. Quiet, ordinary, no joke. A red folder on the table.' },
  { id: 'v50', kind: 'chair', line: 'That it stops you being embarrassed about the part of you that goes quiet.',
    scene: 'The same plain room and the same wooden chair, square on, warm light. The character sits in it looking blank and quiet — and a friend sits in a second chair beside them, and a dog lies at their feet, and an opossum sits on the chair arm. Nobody is trying to fix anything. A red mug on the table.' },
]

/** Five gate rejects. Two lettering (motion words invite sound effects again),
 *  one duplicate-self the model won't draw, one missed blank face, one wrong scene. */
export const V5_FIX = [
  { id: 'v03', kind: 'obj', line: "And you'll tell me that doesn't happen to you. It happened on Tuesday.",
    scene: 'The character stands in an office with arms folded and chin lifted, shaking their head in confident denial with a smug dismissive smile — while from the neck down their entire body has already turned to cracked grey stone. They have not noticed. A red folder on the floor.' },
  { id: 'v21', kind: 'phys', line: 'You go quiet. You go blank.',
    scene: 'Close on the character. Their head is a completely smooth featureless blank oval — absolutely no eyes, no mouth, no nose, no features of any kind, like an unpainted egg. Their body posture is relaxed and ordinary. A small red button on the collar.' },
  { id: 'v30', kind: 'lit', line: 'You knew something was wrong before you could say what.',
    scene: 'A character standing in an open doorway to an office kitchen, seen from the side. Their face is still calm and unsuspecting, but their shoulders have shot up around their ears and one hand grips the door frame so hard the knuckles are white. Two colleagues inside are silent, watching. A red door frame.' },
  { id: 'v41', kind: 'obj', line: "You'll want to tell me you're self-sufficient. You're patting your own head.",
    scene: 'The character sits alone in a plain wooden chair patting the top of their own head with both hands at once, wearing a determined and entirely unconvincing expression. A dog watches from the doorway with visible pity. A red mug on the floor. Absolutely no letters, words or sound-effect text anywhere in the image.' },
  { id: 'v47', kind: 'lit', line: 'The biology behind all this is genuinely disputed.',
    scene: 'A laboratory. Two figures in white coats stand either side of a bench, both leaning in and talking at once, each pointing at the same wobbling red model between them, neither backing down. A lizard sits on the bench watching. Absolutely no letters, words, numbers or writing anywhere in the image.' },
]

/** Seven fills. Content-locking exposed 7 lines in Acts VI-VII with no frame —
 *  the closing run is short-sentenced and my 50 under-covered it. Worst hold
 *  was 26.1s. These are not decoration; each is an unillustrated line. */
export const V5_FILL = [
  { id: 'w01', kind: 'obj', line: 'And you would love that to mean you can ignore all of it.',
    scene: 'The character stands in a laboratory looking enormously relieved and delighted, already turning to leave with both thumbs up — while behind them the two white-coated figures are still mid-argument, unresolved. A red model on the bench.' },
  { id: 'w02', kind: 'lit', line: "Porges answered, it isn't settled.",
    scene: 'Two figures in white coats sit back to back at two desks, both writing steadily, tall stacks of paper on either side of them. Neither is turning around. Calm, ongoing, unresolved. A red pen on the floor between them.' },
  { id: 'w03', kind: 'lit', line: 'And what it tells you to do, find a face.',
    scene: 'Close on a second character\'s warm open face looking directly at the viewer, present and kind, eyes creased. Plain uncluttered background. A red collar.' },
  { id: 'w04', kind: 'lit', line: 'Hear a voice, breathe out slowly.',
    scene: 'A plain room. The character sits in a wooden chair exhaling so completely that their shoulders have dropped well below where they started, eyes closed, entirely at ease. A friend sits nearby mid-word. A red mug on a table.' },
  { id: 'w05', kind: 'lit', line: 'Be near someone.',
    scene: 'Two characters sit side by side on a step outside a front door in warm evening light, not talking, both looking out at the same thing. A dog lies at their feet. A red mug on the step.' },
  { id: 'w06', kind: 'lit', line: 'You can doubt the theory and still take the advice.',
    scene: 'The character walks along a pavement at dusk holding a small wobbly red model loosely under one arm like a takeaway, entirely relaxed about it, a dog trotting alongside. A lizard sits on a wall watching.' },
  { id: 'w07', kind: 'lit', line: "And maybe that's the useful part. Not that it explains you.",
    scene: 'The character sits alone in the plain wooden chair in soft warm light, looking calm and unhurried, not performing anything. An opossum sits on the chair arm beside them. A red mug on the table.' },
]
