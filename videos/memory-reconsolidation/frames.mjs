/**
 * Frame definitions — Acts I–V (m01–m38, 39 frames incl. m22b).
 *
 *   env    'workshop' passes the environment plate as a reference.
 *          'plain' and 'kitchen' do NOT — the plate would drag charcoal
 *          shelving and film canisters into rooms that should be bare.
 *   group  frames in the same group are generated IN ORDER, each receiving the
 *          previous approved frame as reference #1. That ordering is what held
 *          the m25/m26 pair together: the seated figure stayed the same drawing,
 *          not merely a similar one.
 *   people false selects STYLE_ENV, which drops the character clause. The style
 *          block's own "thin stick-figure character…" sentence is a standing
 *          instruction to draw a person and will populate an empty room.
 */

// ── Shared clauses, appended per frame ───────────────────────────────────────

/** Fix 2. m25's questioner came back with a malformed dangling hook for a hand. */
export const HANDS = `Hands are relaxed and naturally shaped. When a hand is open and visible, \
draw exactly five clearly separated fingers. Never draw a hand as a dangling hook, a curl, a \
stump or an unresolved squiggle; if a hand would be small or awkward in frame, rest it flat \
against the body, in a pocket, or out of view instead.`

/** Fix 3. The seated figure drifted lower and larger between m25 and m26. */
export const LOCKED_CAMERA = `LOCKED CAMERA: this frame uses the exact same camera position, \
height, distance and lens as the reference image. The room geometry, wall corners, floor line, \
furniture positions and the size and eyeline of any returning figure are all IDENTICAL to the \
reference. Nothing is re-staged, re-scaled or re-framed. Only the specific change described \
above differs.`

/** Fix 1. Emphasis lives in the body. Anger misrepresents a one-word manipulation. */
export const EMPHATIC_NOT_ANGRY = `The gesture is large but the mood is pleasant and \
procedural. Keep the face calm and neutral-friendly: eyebrows level, no frown, no bared teeth, \
no shouting, no sweat drops, no intimidation. This person is being emphatic, not aggressive.`

const K = 'A warm beige kitchen with pale yellow walls, a sink under a window on the back wall, \
a plain counter, and a red mug standing beside the sink.'
const W = 'The cluttered charcoal-grey restoration workshop from the reference image — same \
shelving of cream folders and boxes, same workbench, same warm pool of beige light on the floor, \
same half-built theatrical set of a domestic room braced with visible timber.'
const P = 'A plain sparse room with warm beige walls and a beige floor, seen straight on, wide. \
Completely empty of furniture except where stated. Flat even lighting.'

export const ACTS_I_V = [
  // ── ACT I — THE KITCHEN ────────────────────────────────────────────────────
  { id: 'm01', act: 1, env: 'kitchen', group: 'kitchen', people: true,
    scene: `${K} The stick-figure protagonist stands in the middle of the room facing the viewer, arms folded, chin slightly up, calm and completely certain. Blue curtains hang at the window.` },
  { id: 'm02', act: 1, env: 'kitchen', group: 'kitchen', people: false,
    scene: `${K} Closer view of the sink, the counter and the red mug. Blue curtains at the window. The room is empty.` },
  { id: 'm03', act: 1, env: 'kitchen', group: 'kitchen', people: true,
    scene: `${K} The protagonist stands facing the viewer, arms folded, unaware. Behind them at the window, a second smaller stick-figure archivist stands on a wooden stepladder, calmly painting the curtains blue with a brush — one curtain is finished, the other is still bare fabric.` },
  { id: 'm04', act: 1, env: 'kitchen', group: 'kitchen', people: true,
    scene: `${K} Identical framing and identical protagonist pose. The window now has NO curtains at all — bare glass and a plain frame. The stepladder and the archivist are gone. Everything else in the room is unchanged.` },
  { id: 'm05', act: 1, env: 'kitchen', group: 'kitchen', people: true,
    scene: `${K} The protagonist is turning their head sharply to look back over one shoulder, eyes wide, mouth open, having just noticed something. A folded wooden stepladder leans against the wall behind them.` },
  { id: 'm06', act: 1, env: 'kitchen', group: 'kitchen', people: true,
    scene: `${K} The protagonist faces the viewer, one index finger raised, mid-objection, dignified and insistent. Behind them the archivist quietly carries the folded stepladder toward a doorway, not looking back.` },

  // ── ACT II — NOT PLAYBACK ──────────────────────────────────────────────────
  { id: 'm07', act: 2, env: 'plain', group: 'vault', people: true,
    scene: `A vast immaculate archive: long rows of identical pale shelving in perfect order, cool even light, no dust, nothing out of place. The protagonist stands small in the centre aisle, hands at their sides, looking pleased.` },
  { id: 'm08', act: 2, env: 'plain', group: 'vault', people: true,
    scene: `The same immaculate archive. The protagonist stands at a shelf, drawing out a single plain cream folder with one hand, looking satisfied.` },
  { id: 'm09', act: 2, env: 'plain', group: 'vault', people: true,
    scene: `The same immaculate archive. The protagonist holds the cream folder open in both hands. It is completely empty — nothing inside at all. Their face has fallen: eyes wide, mouth a small flat line of dismay.` },
  { id: 'm10', act: 2, env: 'plain', group: null, people: true,
    scene: `${P} The protagonist kneels on the floor surrounded by a scatter of loose mismatched flat pieces of different sizes and beige tones, holding two of them up and trying to fit them together. Mild concentration.` },
  { id: 'm11', act: 2, env: 'plain', group: 'bartlett', people: true,
    scene: `${P} Two stick-figure people. On the left one sits on a simple wooden chair, telling a story with an open hand raised. On the right a second sits on an identical chair holding a small blank cream notebook, listening. Deliberately undramatic and still.` },
  { id: 'm12', act: 2, env: 'plain', group: 'bartlett', people: true,
    scene: `${P} The same two people, same chairs, same positions. The teller on the left is now gesturing wildly with both arms, body leaning, animated. The listener on the right sits perfectly still, and the blank page of their notebook is now filled with a neat, orderly, symmetrical pattern of tidy horizontal marks — no letters, just even ruled lines.` },
  { id: 'm13', act: 2, env: 'plain', group: null, people: true,
    scene: `${P} The protagonist stands holding two objects, one in each hand: in the right hand a plain ordinary cup, in the left hand a strange lumpy unidentifiable object. They are calmly dropping the strange one behind their back while looking at the ordinary one. Completely untroubled.` },

  // ── ACT III — THE ARCHIVE ──────────────────────────────────────────────────
  { id: 'm14', act: 3, env: 'plain', group: 'vault', people: false,
    scene: `A vast immaculate archive: long rows of identical pale shelving in perfect order, cool even light, nothing out of place. The room is completely deserted.` },
  { id: 'm15', act: 3, env: 'plain', group: null, people: true,
    scene: `${P} The protagonist stands with their back mostly to us, pulling open a plain grey door in the far wall. Warm light spills out through the widening gap onto the floor. Their face is turned just enough to show curiosity.` },
  { id: 'm16', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The protagonist stands at the left edge of the room, stopped dead, staring at the room with a huge shocked open-mouthed expression, arms hanging limp. Two archivist figures in the middle distance continue working on the set and do not look up.` },
  { id: 'm17', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} An archivist stands at the workbench holding up one small blank cream index card between two fingers, presenting it. A fat open folder lies on the bench beside them, obviously otherwise empty. The protagonist looks at the card, unimpressed.` },
  { id: 'm18', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The camera has moved round to see the theatrical set FROM BEHIND: raw unpainted backs of the flats, a lattice of timber braces, cables on the floor. One archivist steadies a brace with both hands.` },
  { id: 'm19', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} An archivist lifts a flat painted wall panel out of a large cardboard document box on the floor, carrying it toward the set with both hands.` },
  { id: 'm20', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} A second archivist stands on a low step adjusting a work lamp on a stand, aiming its beam at the set. Casual, routine, one hand on the lamp housing.` },
  { id: 'm21', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} A corner of the set is missing. An archivist is patching the gap with a panel that plainly does not match — noticeably different colour and clearly the wrong size, overlapping the edges. A second archivist walks past behind without reacting.` },
  { id: 'm22', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} Two archivists push the finished set into position on castors, seen from three-quarters: the front face reads as a convincing warm kitchen, while bare timber bracing is still clearly visible around the side and back edge.` },
  { id: 'm22b', act: 3, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} Seen straight on from the protagonist's eye line, the set now reads as a real warm beige kitchen with no bracing visible. The protagonist stands in the foreground looking at it, satisfied and nodding. One cupboard door on the set is a slightly different shade of beige from the others.` },

  // ── ACT IV — LATER INFORMATION ─────────────────────────────────────────────
  { id: 'm23', act: 4, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} An archivist walks across the floor carrying a single small flat RED strip of card in one hand, heading toward the beige set. Purposeful and ordinary.` },
  { id: 'm24', act: 4, env: 'plain', group: 'l1974', people: true,
    scene: `${P} Two stick-figure people sit on simple wooden chairs side by side with their backs three-quarters to us, watching a small screen on a stand showing two simple cartoon cars. Still and attentive.` },
  { id: 'm25', act: 4, env: 'plain', group: 'l1974', people: true,
    scene: `${P} On the LEFT a stick-figure person sits on a simple wooden chair angled slightly toward the centre, feet on the floor, hands resting in their lap, completely neutral flat expression. On the RIGHT a second stick-figure person stands facing them holding a small blank cream notepad, UPRIGHT and still, weight even on both feet, free hand resting flat against their side, mouth a small neutral oval as they ask a short quiet question. Calm and procedural.` },
  { id: 'm26', act: 4, env: 'plain', group: 'l1974', people: true, emphatic: true,
    scene: `The SAME two people, SAME room, SAME chair. The seated figure on the left has not moved and keeps the exact same neutral flat expression. The ONLY change is the standing questioner on the right, who now leans forward from the waist and raises their free hand high in a large open emphatic gesture, asking the same question with much more emphasis.` },
  { id: 'm27', act: 4, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} On the theatrical set, a crash scene is being assembled — two simple cartoon cars nose to nose. An archivist leans in and scatters a small handful of flat RED fragments across the floor of the set, placing them deliberately.` },
  { id: 'm28', act: 4, env: 'plain', group: null, people: true,
    scene: `${P} Two figures in one frame, connected by a single continuous motion: on the left a questioner with a blank notepad extends one open hand forward in a speaking gesture; that gesture flows directly into the hand of an archivist on the right, who is scattering flat RED fragments onto a small model floor. One movement, two people.` },
  { id: 'm29', act: 4, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The protagonist stands in the foreground facing the viewer, tapping one index finger against their own temple, extremely pleased with themselves. Directly behind them an archivist quietly slips a small blank card into a pocket.` },
  { id: 'm30', act: 4, env: 'plain', group: null, people: true,
    scene: `${P} Five stick-figure people stand in a loose row facing the viewer, obviously different from each other in height and build — tall, short, stout, thin. Every one of them holds an identical small flat RED strip of card in one hand. All calm and neutral.` },
  { id: 'm31', act: 4, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} On the theatrical set, a child's birthday scene has been assembled — a small table, a simple cake, paper hats. An archivist is carefully placing a large friendly dog into the middle of the scene with both hands. The dog looks entirely comfortable. Nobody else in the room reacts.` },

  // ── ACT V — RECONSOLIDATION ────────────────────────────────────────────────
  { id: 'm32', act: 5, env: 'plain', group: 'lists', people: true,
    scene: `${P} The protagonist sits at a plain wooden table seen straight on, with a neat row of five simple distinct objects laid out in front of them. They study the row, concentrating.` },
  { id: 'm33', act: 5, env: 'plain', group: 'lists', people: true,
    scene: `The SAME table and SAME protagonist in the SAME position. The objects are gone. An archivist stands beside the table holding up one small blank cream index card at eye level. Nothing else is happening. The protagonist glances at it.` },
  { id: 'm34', act: 5, env: 'plain', group: 'lists', people: true,
    scene: `The SAME table and SAME protagonist. A new row of five different simple objects is laid out in front of them. The archivist has gone. The protagonist studies the new row.` },
  { id: 'm35', act: 5, env: 'plain', group: 'lists', people: true,
    scene: `The SAME table and SAME protagonist, who is now confidently laying out a row of five objects from memory, one hand placing the last one. Three of the objects are from the first row and two are unmistakably from the second row. The protagonist looks completely certain and has not noticed.` },
  { id: 'm36', act: 5, env: 'plain', group: 'lists', people: true,
    scene: `The SAME table and SAME protagonist, attempting the reverse: they push objects toward the far edge of the table but the objects slide straight off and tumble to the floor, refusing to stay. The protagonist watches them fall, puzzled.` },
  { id: 'm37', act: 5, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} An archivist holds a cream folder open in both hands at chest height. Its loose contents have lifted slightly and hang unsettled in the air just above the folder, as though weightless for a moment. The archivist watches them, waiting.` },
  { id: 'm38', act: 5, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The same archivist has closed the folder and is setting it down flat on the workbench with one hand. Completely ordinary and undramatic. Nothing is floating.` },
]

/**
 * Acts VI–IX (m39–m61, 23 frames).
 *
 * Act VII is the honest-evidence section: no workshop, no archivists, no
 * cartoon physics, plain rooms only. The comedy stops at m47 and does not
 * return until the m61 callback. That silence is what earns the concession —
 * it is the single most transferable thing the last film did.
 *
 * Every frame in Act VI sits under the narration's conditional "if it's right".
 * None of them may be read as asserting reconsolidation is established.
 */
export const ACTS_VI_IX = [
  // ── ACT VI — THE COPY BECOMES THE MASTER ───────────────────────────────────
  { id: 'm39', act: 6, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} An archivist carries a stack of freshly built set pieces away from the stage toward the tall shelving, holding them flat against their chest.` },
  { id: 'm40', act: 6, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} Close on a section of shelving. An archivist slides a cream folder into a narrow gap between other identical cream folders. Once in, it is indistinguishable from its neighbours.` },
  { id: 'm41', act: 6, env: 'workshop', group: 'workshop', people: false,
    scene: `${W} A still, straight-on view of one shelf packed with identical plain cream folders, edge to edge. Nothing distinguishes any of them. The room is deserted.` },
  { id: 'm42', act: 6, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} Two archivists of identical build stand facing each other, each holding up an identical cream folder and pointing at the other's folder with the free hand, mid-disagreement. Both look equally certain.` },
  { id: 'm43', act: 6, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} Wide view of the workshop in disarray: the set is half dismantled, a dropped stack of blank cream paper hangs scattered in mid-air, one archivist is slumped asleep across the workbench, and another is painting a wall panel that is lying face down on the floor.` },
  { id: 'm44', act: 6, env: 'kitchen', group: 'kitchen', people: true,
    scene: `${K} The SAME kitchen and SAME camera as the reference image. The protagonist stands in the identical spot, arms folded. The impossible detail: the window somehow has BOTH blue curtains hanging at it AND a completely bare rail with plain glass, occupying the same window at once. Nobody reacts.` },
  { id: 'm45', act: 6, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The protagonist stands in the centre of the workshop, one hand held out flat and open, palm up, asking for something. Three archivists are visible around the room and every single one of them is looking somewhere else — one at the ceiling, one down into a box, one at their own feet.` },
  { id: 'm46', act: 6, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The identical shot one moment later. Nobody has moved. The protagonist's hand is still out. Not one archivist is looking at them.` },

  // ── ACT VII — THE HONEST PART (comedy stops) ───────────────────────────────
  { id: 'm47', act: 7, env: 'workshop', group: 'workshop', people: false,
    scene: `${W} The workshop at the end of the day: dark, still and completely deserted. One small work lamp is left on over the bench, throwing a narrow pool of light. Every chair is empty. Nobody is in the room.` },
  { id: 'm48', act: 7, env: 'plain', group: 'evidence', people: true,
    scene: `${P} A single plain stick-figure person sits at a simple desk seen straight on, one hand resting on a blank sheet of paper, calm and businesslike. Nothing else in the room.` },
  { id: 'm49', act: 7, env: 'plain', group: 'evidence', people: true,
    scene: `The SAME plain room and SAME camera. Now four plain stick-figure people sit at four identical simple desks in a row, each with a blank sheet, each working separately. None of them look at each other.` },
  { id: 'm50', act: 7, env: 'plain', group: 'evidence', people: false,
    scene: `The SAME plain room and SAME camera. One simple empty chair stands alone in the middle of the room. Nobody is present. Nothing is happening.` },
  { id: 'm51', act: 7, env: 'plain', group: 'evidence', people: true,
    scene: `The SAME plain room. Seven plain stick-figure people stand in a single evenly spaced row facing the viewer, each holding one blank sheet of paper down at their side. All calm, all neutral.` },
  { id: 'm52', act: 7, env: 'plain', group: 'evidence', people: true,
    scene: `The SAME row of seven plain people in the SAME positions. Every one of them now holds their blank sheet up at chest height, facing the viewer. Every sheet is completely empty. No reaction on any face.` },
  { id: 'm53', act: 7, env: 'plain', group: 'evidence', people: true,
    scene: `The SAME plain room. Two plain stick-figure people sit facing each other across a simple table, both mid-speech with one open hand raised, both calm and reasonable. Neither is angry.` },
  { id: 'm54', act: 7, env: 'plain', group: null, people: true,
    scene: `${P} The protagonist stands holding a single small blank cream card, looking at it, genuinely uncertain. Two identical plain cardboard boxes sit on the floor on either side of them. Not comic — simply unsure which box it came from.` },

  // ── ACT VIII — ORDINARY LIFE ───────────────────────────────────────────────
  { id: 'm55', act: 8, env: 'plain', group: null, people: true,
    scene: `${P} The protagonist stands in an ordinary bare room facing the viewer, arms relaxed at their sides, calm and untroubled. Not distressed, not comic. Just standing.` },
  { id: 'm56', act: 8, env: 'plain', group: null, people: true,
    scene: `The protagonist stands facing the viewer, entirely confident and pleasant. The room behind them is split down the middle without comment: the left half is a solid, real beige wall with a skirting board; the right half is a propped-up theatrical flat braced from behind with timber. Neither half is emphasised.` },
  { id: 'm57', act: 8, env: 'plain', group: null, people: true,
    scene: `${P} Two stick-figure people stand a little apart, each turned toward the viewer and each gesturing back over their own shoulder at a different version of the same simple room behind them — the two versions differ in one small detail. Both people look relaxed and sincere. Neither is angry.` },
  { id: 'm58', act: 8, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The protagonist stands close to the camera in the foreground, calm and unbothered, looking slightly off to one side. Behind them, deeper in the room, two archivists carry on working on the set exactly as normal, paying no attention.` },

  // ── ACT IX — CURRENT VERSION ───────────────────────────────────────────────
  { id: 'm59', act: 9, env: 'kitchen', group: 'kitchen', people: false,
    scene: `${K} The SAME kitchen and SAME camera as the reference image, completely empty of people. The window has no curtains, only the bare rail. The red mug stands beside the sink. Still and quiet.` },
  { id: 'm60', act: 9, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} Close on the workbench. A cream folder lies flat. An archivist's hand is peeling a small BLANK rectangular label strip off the folder's edge, and the other hand holds a fresh BLANK label strip ready to press on in its place. Both strips are completely blank with no marks of any kind.` },
  { id: 'm61', act: 9, env: 'workshop', group: 'workshop', people: true,
    scene: `${W} The protagonist stands mid-objection, one index finger raised and mouth open to speak. Beside them an archivist, not looking up, calmly drops a single small blank cream card into a separate open folder and closes it.` },
]
