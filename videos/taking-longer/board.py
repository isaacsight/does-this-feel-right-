#!/usr/bin/env python3
"""Frame book — Why Everything Takes Longer Than You Think (episode 9).
120 frames across 95 sentences: every sentence carries at least one picture,
every sentence over 25 words carries two (three where the hold would otherwise
run past the ceiling), and 6 of the 120 are built as deterministic data cards.

Direction: DEADPAN SCALE — the gap between the plan and the thing is staged as
SIZE. Every law below was paid for on an earlier film; the ones at the top are
the ones that bite hardest on THIS one.

  DEADPAN SCALE          every act pairs ONE small confident object against ONE
                         enormous patient one, BOTH stated at point of use.
                         Gated per act, minimum two rows each.
  THE MONUMENT           the plank mountain returns with the IDENTICAL string
                         every time — ceiling-high flat planks and plain closed
                         boxes, ONE completely BLANK white instruction sheet on
                         the floor, ONE small brass screw beside it. It shrinks
                         ONLY in the final act, where the marker is absent.
  THE SEASONS WINDOW     the garage recurrence is the film's clock. The staging
                         sentence is worded IDENTICALLY on every return; only
                         the season beyond the window (falling SNOW / pink
                         BLOSSOM / amber LEAVES) and the plant's stage (tiny
                         sprout / leggy and tall / spilling over the bench
                         edge) change. Gated on both sets.
  THE MAN AT POINT OF USE  the single lonely PAIR of hairs, THREE round
                         buttons, ABSURDLY oversized dark ink-blue shoes —
                         expanded in FULL wherever the coat is staged. A
                         reference sheet is NOT sufficient (paid twice).
                         His recurring face is bright morning confidence,
                         never smug: the planner is us.
  FLAT-RUN v1 and v2     no run of 3+ castless rows in one setting, and no
                         cross-setting castless run either. Max castless run
                         is 2, measured, everywhere.
  FREE-LANE GEOMETRY     no layout plate exists in this pipeline, so every
                         castless row carries its own geometry sentence; void
                         castless rows carry the exact cream-field clause.
  LABEL-INVITATION       every sign/sheet/page/plan/drawing/folder/book/cup/
                         plaque/dial carries "completely BLANK" in its own row;
                         every other document type-noun is banned outright.
                         "instruction sheet" is legal ONLY beside its BLANK.
  OMISSION, NOT NEGATION absences described as present things — the missing
                         shelf is "ONE pale rectangle of primer".
  EVENTS, NOT STATES     something happens in every row; these are stills, so
                         each row stages a HELD moment of an action.
  NAMED LIGHTING COLOURS winter window is flat INK BLUE, lamplight and autumn
                         are flat mustard GOLD, harbour dusk is flat dusty
                         ORANGE. Never "a darker mix".
  LIKENESS LAW           no frame resembles any real person. The committee is
                         SEVEN invented faces plus THE SILENT EXPERT; the
                         harbour stages a BUILDING and never an architect;
                         surnames are gated out of scene text entirely.
  THE SILENT EXPERT      sage GREEN cardigan, ONE closed plain completely BLANK
                         folder, face composed and level — at least TWO
                         committee rows and ONE archive-corridor row.
  THE SUFFICIENT ANSWER  the Man holds ONE tiny silver screwdriver UP in at
                         least TWO rows; in the final act it lies flat on the
                         finished shelf, exactly once.
  ENVIRONMENT CAP        garage frames <=22%, measured not hoped for.
  DATA FRAMES            pure-number beats (33.9 / 55.5 / 48.6, the 7-million
                         against 102-million card, eighteen-to-thirty months
                         against eight years, nine of ten) built
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
       "buttons, thin stick legs and ABSURDLY oversized dark ink-blue shoes")
CROWN = ("the single lonely PAIR of hairs at the very top of his crown standing up — one thin "
         "hair kinking left, one leaning right")
MOUNT = ("THE PLANK MOUNTAIN: a ceiling-high stack of flat planks in warm wood tones and plain "
         "closed boxes filling the whole back wall, ONE completely BLANK white instruction sheet "
         "lying flat on the cream floor at its foot, ONE small brass screw beside the sheet")
SD = "ONE tiny silver screwdriver"
UP = f"holding {SD} up at shoulder height"

SNOW = "falling SNOW in flat INK BLUE"
BLOSSOM = "pink BLOSSOM in flat dusty ORANGE"
AMBER = "amber LEAVES in flat mustard GOLD"
P1 = "standing as one tiny sprout"
P2 = "grown leggy and tall"
P3 = "spilling over the bench edge"
GAR_A = f"the same cream garage staging squared straight at the back wall — {MOUNT}, ONE square window in the left wall with "
GAR_B = ", ONE workbench under the window carrying ONE small potted plant "
def GAR(season, plant):
    return GAR_A + season + " beyond it" + GAR_B + plant

GEOM = "a single flat cream field, one low horizon line"
SHELVES = "shelf after shelf of plain closed boxes"
ARCHIVE = f"{SHELVES} running away down ONE long archive corridor"
STUDENT = ("THE STUDENT: ONE young woman at ONE plain desk with her sleeves pushed up, ONE lamp "
           "of flat mustard GOLD beside her and ONE tall stack of completely BLANK pages at her "
           "elbow")
EXPERT_BODY = "ONE older woman in a sage GREEN cardigan, her face composed and level"
EXPERT = (f"THE SILENT EXPERT: {EXPERT_BODY}, seated at the end seat of the long folding table "
          "with her hands folded on ONE closed plain completely BLANK folder")
EXPERT_ARCH = (f"THE SILENT EXPERT: {EXPERT_BODY}, ONE closed plain completely BLANK folder held "
               "flat against her chest")
COMMITTEE = ("exactly SEVEN figures at the table, every face individuated and bright with the "
             "fresh-start look, each with ONE small plain cup completely BLANK")
SHELL = ("ONE half-built white-ribbed shell rising out of the harbour water, bare concrete ribs "
         "with ONE lattice of scaffolds strapped around them and ant-small builders scattered "
         "along the scaffold planks")
BORE = "ONE vast dark tunnel bore opening in a hillside, its mouth taller than the trees"
TWO = "exactly TWO figures"

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
# ACT 1 — the promise, the garage, the mountain -------------------------------
(1,"XWIDE","face bright with morning confidence","garage", f"{GAR(SNOW,P1)}, and {MAN} standing small at the near side {UP}, his face bright with morning confidence, the ceiling-high stack of planks standing patient behind him."),
(2,"CU","chin lifted, face bright with morning confidence","garage", f"The Man's round face and big confident nose held level, {CROWN}, his chin lifted and his face bright with morning confidence, ONE plain closed box of the stacked planks rising past the top edge behind him."),
(3,"WIDE","face bright and busy","garage", f"{MAN} crouched at the workbench laying out FOUR small brass brackets in one even row with ONE long length of pine beside them and ONE dusty electric drill resting where it has sat since the move, his face bright and busy, {MOUNT}."),
(4,"MED","face open and certain","kitchen", f"{MAN} seated at ONE plain kitchen table on a Thursday evening with one hand flat on the wood and his mouth open on one easy sentence, his face open and certain, ONE small cup completely BLANK steaming at his elbow."),
(4,"WIDE","face serene and absorbed","void", f"ONE perfect finished version of the job standing alone on {GEOM}: ONE straight length of pine mounted level on ONE bare clean wall, and {MAN} standing back from it with his arms loose, his face serene and absorbed."),
(4,"XWIDE","face patient and set","void", f"{MAN} walking one long empty road across {GEOM} on a hot afternoon holding ONE small brass bolt up between two fingers, ONE enormous flat-roofed hardware warehouse standing far off at the horizon, his face patient and set."),
(5,"XWIDE","face level and waiting","garage", f"{GAR(SNOW,P1)}, and {MAN} standing in exactly the same place on a Sunday, once more {UP}, his face level and waiting."),
(6,"WIDE","face composed and level","garage", f"ONE bare garage wall running level and unbroken from corner to corner with ONE pale rectangle of primer painted on it where a shelf was meant to go, {MAN} standing beside it with both hands at his sides, his face composed and level, {MOUNT}."),
(7,"MED","faces composed and honest","void", f"THREE small unfinished jobs standing far apart on {GEOM}: ONE shed with its door propped open, ONE spare room holding ONE bare mattress on its side, ONE plain desk carrying ONE completely BLANK page — and THREE individuated people standing beside them, every face composed and honest."),
(8,"CU","brows drawn, face thoughtful and level","garage", f"The Man's face turned three-quarters in the garage, {CROWN}, his brows drawn and his eyes travelling sideways, his face thoughtful and level, the warm wood tones of the stacked planks lying flat behind him."),
(9,"WIDE","face bright with morning confidence","kitchen", f"{MAN} seated at the same plain kitchen table the following Thursday with one hand flat on the wood in exactly the same place and his mouth open on exactly the same sentence, his face bright with morning confidence, ONE small cup completely BLANK steaming at his elbow."),
# ACT 2 — the loan and the future self ----------------------------------------
(10,"MED","face sincere and open","kitchen", f"{MAN} seated at the plain kitchen table with one forefinger raised, saying one date out loud, his face sincere and open, ONE small cup completely BLANK standing untouched beside his hand."),
(11,"XCU","-","void", f"ONE small brass coin resting at the centre of ONE flat open palm and filling the view, the fingers loose and level, {GEOM} running level far behind the wrist, the metal worn bright."),
(12,"WIDE","one face bright and certain, one face composed and unaware","void", f"{TWO} far apart on {GEOM}: {MAN} at the near side holding one hand out, his face bright and certain, and ONE second identical small man in the same flat VERMILION RED coat with THREE round buttons, the same single lonely PAIR of hairs and the same ABSURDLY oversized dark ink-blue shoes standing tiny at the far horizon half-turned away, his face composed and unaware, the ground running enormous and empty between them."),
(12,"MED","face easy and generous","void", f"{MAN} spending ONE fistful of small brass coins at once and letting them fall in one bright stream onto {GEOM}, his face easy and generous, ONE enormous plain strongbox standing shut far behind him."),
(13,"WIDE","face level and arriving","void", f"ONE plain doorway standing alone on {GEOM} with {MAN} stepping through it, his face level and arriving, one long band of flat mustard GOLD light lying across the ground in front of him."),
(14,"XCU","face worn and patient","void", f"The Man's face arriving close and filling the view, {CROWN}, ONE small brass coin held up between two fingertips at the bottom edge, his face worn and patient."),
# ACT 3 — 1994, the honors students -------------------------------------------
(15,"XWIDE","face exact and unhurried","archive", f"{ARCHIVE}, ONE archivist standing tiny at the near end with one hand resting on ONE plain closed box, his face exact and unhurried, the shelves running away far past him."),
(16,"XWIDE","every face resolute and individuated","thesisdesk", "ONE long hall of plain desks in flat even light with NINE individuated students seated far apart at them, sleeves pushed up, ONE tall stack of completely BLANK pages standing at every elbow, every face resolute."),
(16,"MED","face resolute and steady","thesisdesk", f"{STUDENT}, her hands flat on the desk and her shoulders squared, her face resolute and steady, the hall running away level behind her."),
(17,"MED","face polite and exact","thesisdesk", f"ONE researcher in a sage GREEN coat standing at the end of the desk with both hands behind his back asking one question, his face polite and exact, {STUDENT} looking up toward him."),
(18,"CU","face certain and honest","thesisdesk", "The student's face lifted from the desk, her chin up and her mouth open on one short answer, her face certain and honest, ONE lamp of flat mustard GOLD glowing at the edge of the picture."),
(19,"WIDE","-","data", DATA),
(20,"WIDE","face tired and steady","thesisdesk", f"{STUDENT} still at the same desk much later, the stack at her elbow grown enormous and leaning, ONE tiny brass token standing on the wood beside it, her face tired and steady."),
(21,"WIDE","-","data", DATA),
(22,"XWIDE","every face composed and individuated","thesisdesk", "TEN individuated students standing in ONE wide row across the hall, THREE of them holding their stacks of completely BLANK pages closed and level at chest height and the other SEVEN holding theirs open and half-done, every face composed."),
(22,"MED","face patient and level","thesisdesk", "ONE young woman seated at ONE plain desk with one small brass token set down on the wood for every month gone by since September, ONE long row of them running off the desk edge, her face patient and level."),
(23,"XCU","face sincere and level","thesisdesk", "The student's face close and filling the view, her eyes level and her mouth composed, her face sincere and level, ONE lamp of flat mustard GOLD lying warm along her cheek."),
(24,"MED","face absorbed and hopeful","void", f"ONE young woman standing on {GEOM} with her eyes half-closed, and standing beside her ONE second identical version of herself already seated and working at ONE plain desk, her face absorbed and hopeful."),
(25,"MED","face bright with morning confidence","kitchen", f"{MAN} at the plain kitchen table this morning with one finger resting on ONE completely BLANK page of small ruled boxes, his face bright with morning confidence, ONE small cup completely BLANK steaming beside his wrist."),
(26,"WIDE","every face bright and individuated","void", f"SEVEN individuated people standing far apart across {GEOM}, every one of them holding one hand out flat at the same height in the same easy gesture, every face bright and certain."),
# ACT 4 — the worst case ------------------------------------------------------
(27,"CU","face exact and curious","thesisdesk", f"ONE researcher in a sage GREEN coat leaning in over the desk to ask a second question, his face exact and curious, {STUDENT} turning toward him."),
(28,"WIDE","face braced and imaginative","void", f"{MAN} standing small on {GEOM} under ONE enormous dark storm cloud painted as one flat INK BLUE shape filling the whole upper half, his face braced and imaginative, one thin band of pale light lying along the horizon."),
(29,"CU","face composed and unwell","thesisdesk", "ONE young woman seated sideways on the edge of her bed with ONE blanket around her shoulders and ONE plain cup completely BLANK held in both hands, her face composed and unwell, ONE lamp of flat mustard GOLD burning behind her."),
(29,"WIDE","face composed and patient","thesisdesk", "ONE tall stack of completely BLANK pages slid off a plain desk and lying in one loose fan across the hall floor, ONE young woman with her sleeves pushed up standing over it with both arms at her sides, her face composed and patient, ONE plain closed door standing shut at the far end."),
(30,"WIDE","-","data", DATA),
(31,"WIDE","face level and tired","thesisdesk", f"{STUDENT} at the desk one week further on with ONE second row of small brass tokens added beyond the first and running past the desk edge onto the floor, her face level and tired."),
(32,"XCU","-","thesisdesk", "ONE long row of small brass tokens running the whole width of the picture across plain level wood, the last two tokens lying beyond the wood on the bare level floor, the light flat and even across them."),
(33,"XWIDE","face composed and unbothered","void", f"ONE small cushioned marker post standing on {GEOM} and ONE tall walker striding straight past it and onward toward the far edge, his stride long and even, his face composed and unbothered."),
(34,"MED","face grave and exact","void", f"ONE careful man in a dusty-orange coat holding ONE small brass gauge up into the light with both hands, its dial completely BLANK, his face grave and exact, {GEOM} lying wide behind him."),
(35,"WIDE","face composed and certain","void", f"{MAN} standing squarely inside ONE low rectangular border of pine laid flat on the ground on {GEOM} with both feet well inside its edges and ONE small brass screw lying at his toe, his face composed and certain, ONE ceiling-high stack of planks standing far outside the border behind him."),
(36,"XCU","-","void", "ONE small plump cushion set down alone on plain level ground and filling the lower half of the picture, its seams even and its face bare, the light lying flat across it."),
(37,"WIDE","face level and honest","void", f"ONE small plump cushion standing alone at the foot of ONE ceiling-high stack of flat planks and plain closed boxes on {GEOM}, {MAN} standing beside the cushion with one hand held out toward it, his face level and honest."),
# ACT 5 — the observers -------------------------------------------------------
(38,"MED","face fair and pleased","archive", f"{ARCHIVE}, ONE archivist reaching up to lift ONE plain closed box down from a middle shelf with both hands, ONE small brass token resting on its lid, his face fair and pleased."),
(39,"WIDE","THREE faces kind and unsurprised","observers", f"THREE individuated observers standing at ONE enormous wide glass pane and looking through it at ONE plain desk beyond, their faces kind and unsurprised, {STUDENT} small beyond the pane with her back to them."),
(39,"MED","faces exact and level","observers", "THREE individuated observers standing at ONE wide glass pane, the nearest holding up ONE short row of FOUR small brass tokens on one flat palm, their faces exact and level, the room around them plain and even."),
(40,"CU","brows up, face open and asking","observers", "ONE observer's face close at the wide glass pane, her brows up and her mouth open on one question, her face open and asking, the pale reflection of a desk lamp lying flat on the glass beside her."),
(41,"MED","face absorbed and expert","thesisdesk", f"{STUDENT} at the desk with ONE small brass token set out for every part of the job — the easy ones near her hands, the dreaded one pushed far into the corner — her face absorbed and expert."),
(42,"WIDE","face careful and exact","thesisdesk", "ONE young woman standing over ONE plain desk carrying THIRTY small brass tokens spread across its whole surface, her hands hovering above them, her face careful and exact, ONE plain closed door standing shut behind her."),
(42,"CU","face level and unsurprised","observers", "ONE observer seated at ONE plain table on the far side of the wide glass pane with exactly FOUR small brass tokens laid in one short row in front of her and her hands folded beyond them, her face level and unsurprised."),
(43,"WIDE","every face composed and kind","void", f"SEVEN individuated people standing far apart on {GEOM}, every one of them holding ONE small brass gauge up toward somebody else with its dial completely BLANK, every face composed and kind."),
(44,"MED","faces kind and knowing","observers", "THREE individuated observers at the wide glass pane with one of them pointing one flat hand toward the desk beyond it, their faces kind and knowing, the plain wall running level on both sides of them."),
(45,"CU","face hopeful and unsure","thesisdesk", "The student's face close at the desk, her chin level and her eyes wide, her face hopeful and unsure, ONE lamp of flat mustard GOLD lying warm along the side of her face."),
(46,"XWIDE","every face composed and kind","void", f"ROWS of individuated people standing far apart across {GEOM}, every single one of them turned toward a different neighbour and holding ONE small brass gauge up with its dial completely BLANK, every face composed and kind."),
# ACT 6 — the inside view and the outside view --------------------------------
(47,"WIDE","face bright with morning confidence","garage", f"{GAR(BLOSSOM,P2)}, and {MAN} standing between TWO plain open doorways in the near wall with one hand raised toward each, his face bright with morning confidence."),
(48,"MED","face exact and busy","garage", f"{MAN} crouched on the cream garage floor laying out SIX small brass parts in one careful row, {SD} resting beside his knee, his face exact and busy, {MOUNT}."),
(48,"CU","brows up, lips moving, face pleased and adding","garage", f"The Man's round face and big confident nose close, {CROWN}, his brows up and his lips moving as he counts, his face pleased and adding."),
(49,"WIDE","face exact and unhurried","archive", f"{ARCHIVE}, ONE archivist standing at ONE low table pulling TEN plain closed boxes out into one even row along the floor, his face exact and unhurried."),
(50,"MED","both faces level and fair","archive", f"{TWO} far apart in the archive corridor: ONE researcher in a sage GREEN coat at the near end holding ONE completely BLANK plan sheet flat in both hands, and ONE archivist standing tiny at the far end among {SHELVES}, both faces level and fair."),
(51,"CU","chin lifted, face warm and certain","garage", "The Man's face in the garage tipped up toward the bare wall, his chin lifted and his eyes bright, his face warm and certain, ONE completely BLANK white instruction sheet held open in both hands at the bottom edge."),
(52,"MED","face hopeful and light","void", f"{MAN} standing on {GEOM} holding ONE small folded bird up on one flat palm, his face hopeful and light, ONE enormous pale sky lying flat and empty above him."),
(53,"WIDE","face reluctant and honest","garage", f"{MAN} standing in front of {MOUNT}, holding ONE completely BLANK white instruction sheet out at arm's length to one side while he looks the other way toward ONE plain open doorway, his face reluctant and honest."),
(53,"XCU","-","garage", "ONE completely BLANK white instruction sheet held open in TWO bare hands and filling the view, seen from directly ABOVE, the cream floor running level far below it."),
(54,"WIDE","face composed and holding","garage", f"{MAN} with ONE completely BLANK white instruction sheet folded shut in one hand and {UP} in the other, his face composed and holding, {MOUNT}."),
# ACT 7 — the harbour ---------------------------------------------------------
(55,"XWIDE","face level and attentive","harbour", f"{MAN} standing tiny at the edge of ONE enormous harbour in flat dusty ORANGE light, holding ONE short length of pine up level in both hands, his face level and attentive, the water running out enormous and flat behind him."),
(56,"XWIDE","faces composed and certain","harbour", "ONE bare rocky spit of land reaching out into enormous harbour water in flat dusty ORANGE light, THREE individuated tiny figures standing far apart along it with their arms folded, their faces composed and certain, the water running level to the far shore."),
(56,"MED","faces composed and certain","kitchen", "ONE plain wooden table carrying ONE completely BLANK large drawing sheet unrolled flat across it and ONE small neat stack of brass coins set at its corner, TWO individuated builders leaning over it with their sleeves rolled, their faces composed and certain."),
(57,"WIDE","every face exact and practical","kitchen", "SEVEN individuated builders standing close around the same plain wooden table with the completely BLANK large drawing sheet unrolled flat between them, four of them resting rough working hands on its edges, every face exact and practical, ONE plain window behind them."),
(58,"XWIDE","faces bright and expectant","harbour", "ONE finished white-ribbed shell standing complete on its spit of land in flat dusty ORANGE dusk, its pale ribs rising enormous over the harbour, ONE tiny queue of individuated figures waiting at its foot with their faces bright and expectant, the water lying flat and level around it."),
(59,"WIDE","face small and patient","harbour", f"{SHELL} in flat dusty ORANGE light, ONE tiny builder standing high on the topmost scaffold plank with one arm raised, his face small and plain at that distance and his stance patient."),
(60,"MED","faces composed and patient","harbour", "ONE section of the same white shell close in at the waterline in flat dusty ORANGE light, ONE lattice of scaffolds strapped against bare concrete ribs, THREE individuated builders standing on the planks with their hands on the rails, their faces composed and patient, the enormous harbour water lying flat behind them."),
(61,"WIDE","-","data", DATA),
(62,"XWIDE","one face bright and young, one face grown and calm","harbour", "exactly TWO figures on the harbour path in flat dusty ORANGE light: ONE small child in a mustard GOLD coat standing at the near side with her face bright and young, and beyond her the same person grown tall in the same mustard GOLD coat walking toward the finished white shell, her face grown and calm, the pale ribs rising enormous above them both."),
# ACT 8 — the committee, the expert, the archive ------------------------------
(63,"WIDE","every face composed and bright","committee", f"ONE plain committee room in flat even light: {COMMITTEE} seated around ONE long folding table with ONE wide empty stretch of table running down its middle, and {EXPERT}."),
(64,"XWIDE","every face bright with the fresh-start look","committee", f"The same plain committee room seen square — {COMMITTEE} at ONE long folding table with ONE completely BLANK large plan sheet unrolled down its whole length, {EXPERT}, and ONE ceiling-high stack of plain closed boxes standing against the back wall."),
(64,"MED","faces pleasant and administrative","committee", f"FOUR of the committee leaning in over the middle of ONE long folding table with their hands spread on ONE completely BLANK large plan sheet, {COMMITTEE}, their faces pleasant and administrative, {EXPERT}."),
(65,"XCU","chin lifted, face bright and certain","committee", "ONE committee member's face close and filling the view, her chin lifted and her mouth open on one easy answer, her face bright and certain, the sage GREEN wall running flat behind her."),
(66,"WIDE","faces turned and attentive","committee", f"{COMMITTEE} in the plain committee room, six of them turned in their chairs toward the end seat where {EXPERT} sits, their faces attentive and open, ONE long folding table running level between them."),
(66,"XCU","face composed and level","committee", "ONE older woman's face close and filling the view, her hands folded on ONE closed plain completely BLANK folder at the bottom edge, her mouth beginning one slow sentence, her face composed and level, the sage GREEN wall flat behind her."),
(66,"XWIDE","face composed and level","archive", f"{EXPERT_ARCH}, standing alone and small among {ARCHIVE}, the shelves rising ceiling-high on both sides of her and running away far past her."),
(67,"MED","face composed and level","committee", f"ONE older woman in a sage GREEN cardigan seated still at the end seat of ONE long folding table while the six others lean over the completely BLANK large plan sheet, {COMMITTEE}, her hands folded on ONE closed plain completely BLANK folder, her face composed and level."),
(68,"MED","every face bright and busy","committee", f"{COMMITTEE} with the completely BLANK large plan sheet unrolled along ONE long folding table exactly as before, every hand back on the sheet and every face bright and busy, {EXPERT} unmoved at the end seat."),
(69,"WIDE","-","data", DATA),
(70,"XWIDE","face composed and level","archive", f"{ARCHIVE}, ONE plain closed box on a middle shelf with dust lying even across its lid, ONE older woman in a sage GREEN cardigan standing tiny at the far end of the corridor, her face composed and level."),
# ACT 9 — the objection, and the iron law -------------------------------------
(71,"CU","face resolute and tired","thesisdesk", f"{STUDENT}, ONE plain closed door standing shut behind her and ONE window beyond the desk holding a whole street of small lit rooms, her face resolute and tired."),
(71,"WIDE","every face busy and composed","void", f"ONE young woman seated small at ONE plain desk on {GEOM} with SIX individuated people crossing the ground around her in six directions, each carrying one different thing, every face busy and composed, her own face level and resolute."),
(72,"XCU","brows up, face fair and conceding","void", "ONE archivist's face close and filling the view with both open palms lifted into the bottom edge in plain concession, his brows up, his face fair and conceding, flat cream lying even behind him."),
(73,"XWIDE","face small and level","tunnel", f"{BORE}, ONE tiny figure standing at its foot holding ONE small lantern up at shoulder height, his face small and level, the hillside rising enormous above the mouth."),
(74,"XWIDE","every face turned into the dark","tunnel", "ONE vast dark tunnel bore opening in a hillside with its mouth taller than the trees, TEN individuated tiny workers standing in one row across its foot, ONE small lantern glowing flat mustard GOLD among them, every face turned into the dark and composed."),
(74,"WIDE","-","data", DATA),
(74,"WIDE","face level and unsurprised","tunnel", "ONE enormous flat airfield running out to the horizon under flat INK BLUE evening, ONE half-built terminal shell standing far off with ONE lattice of scaffolds around it, ONE tiny surveyor standing in the foreground behind ONE brass instrument on ONE wooden tripod, his face level and unsurprised."),
(75,"WIDE","every face exact and careful","archive", f"{ARCHIVE}, FIVE individuated auditors standing far apart along it with ONE plain closed box open in front of each of them, every face exact and careful."),
(75,"MED","one face exact and grave, one face resolute and tired","tunnel", f"{TWO} far apart in flat even light: ONE auditor in a sage GREEN coat standing tiny at the mouth of the vast dark tunnel bore with ONE plain closed box under his arm, his face exact and grave, and ONE young woman seated at ONE plain desk at the other side with ONE last stack of completely BLANK pages, her face resolute and tired, both of them leaning the same small degree."),
(76,"MED","every face level and plain","void", f"SEVEN individuated people standing in ONE wide row on {GEOM}, every single one of them leaning the same small degree to the same side, every face level and plain."),
(77,"WIDE","every face composed and individuated","void", f"ONE long straight line of pine laid flat across {GEOM} with individuated small figures standing scattered on ONE side of it only, the ground on the other side lying bare and even, every face composed."),
(77,"XWIDE","face bright and astonished","tunnel", "ONE vast dark tunnel bore standing open and finished with ONE small brass ribbon lying cut on the ground at its foot, ONE tiny figure standing beside it with both arms raised, his face bright and astonished, the hillside rising enormous above the mouth."),
(77,"MED","every face delighted and attentive","void", f"NINE individuated people seated close around ONE long dinner table on {GEOM}, one of them standing with ONE plain glass raised and telling something, every other face turned toward him and delighted and attentive."),
(78,"XCU","chin level, face plain and level","void", "ONE listener's face close at the dinner table and filling the view, his chin level and his brows flat, his face plain and level, ONE plain glass standing untouched at the bottom edge."),
(79,"WIDE","face exact and level","archive", f"{ARCHIVE}, ONE entire shelf standing empty with its boxes gone and only ONE pale rectangle of dust marking where each had sat, ONE archivist standing beside it with both hands at his sides, his face exact and level."),
(80,"XWIDE","every face composed and individuated","void", f"ROWS of individuated people standing far apart across {GEOM}, every single one of them leaning the same small degree to the same side, ONE long straight line of pine laid flat on the ground beyond them all with the whole ground on its far side lying bare and even, every face composed."),
# ACT 10 — the law that eats its own correction --------------------------------
(81,"WIDE","face wry and level","void", f"{MAN} standing on {GEOM} beside ONE small brass plaque completely BLANK mounted on ONE short post, one hand resting on the post, his face wry and level, ONE enormous flat pale sky above him."),
(82,"MED","face bright and amused","garage", f"{GAR(AMBER,P3)}, and {MAN} standing at the workbench with one hand flat on the bench and his mouth open on one easy joke, his face bright and amused."),
(83,"XCU","-","void", "ONE small brass ring lying flat on plain level ground and filling the view, one end of it bent round and resting inside its own opposite end, the metal worn bright and the light lying flat across it."),
(84,"MED","face careful and adding","garage", f"{MAN} laying ONE extra length of pine down flat on the cream floor beside the others, his face careful and adding, {MOUNT}."),
(84,"WIDE","face confident and level","garage", f"{MAN} standing between TWO identical stacks of flat planks each as tall as the other with one hand resting on each, his face confident and level, {MOUNT}."),
(85,"CU","eyes crinkled, face knowing and warm","garage", f"The Man's round face and big confident nose close in the garage, {CROWN}, his eyes crinkled and his mouth open on one easy laugh, his face knowing and warm."),
(86,"MED","one face asking, one face cheerful and frank","kitchen", f"{TWO} at ONE plain kitchen table: {MAN} at the near side with one hand open in a question, his face asking, and ONE neighbour in a mustard GOLD coat opposite him with both palms up and his mouth open on one cheerful admission, his face cheerful and frank."),
(86,"CU","face bright with morning confidence","kitchen", "The Man's face close at the kitchen table a moment later, his chin lifted and his mouth open on exactly the same easy sentence as before, his face bright with morning confidence, ONE small cup completely BLANK steaming at the bottom edge."),
(87,"WIDE","face certain and open","void", f"{MAN} pressing one flat palm down onto ONE completely BLANK page laid on ONE low plain table on {GEOM}, his head turned back over his shoulder toward ONE small brass coin lying far behind him on the ground, his face certain and open."),
(87,"MED","face certain and open","void", f"ONE plain chair standing across the low plain table from {MAN}, its cushion undented and its seat bare, the Man seated opposite it with one hand still flat on the completely BLANK page, his face certain and open."),
# ACT 11 — March, the shelf, and the bookcase ---------------------------------
(88,"XWIDE","face worn and warm","dusk", f"The same cream garage in flat dusty ORANGE dusk with {AMBER} beyond the square window in the left wall and ONE small potted plant spilling over the bench edge below it, ONE straight length of pine mounted level on the far wall on FOUR brass brackets, the plank mountain shrunk to ONE short offcut of pine leaning in the corner, the bare garage wall running enormous and even above the shelf, {MAN} standing back with his arms loose, his face worn and warm."),
(89,"MED","faces fond and level","dusk", "ONE straight pine shelf mounted level on the wall carrying TWENTY plain closed books packed tight along it with every spine completely BLANK, the left-hand end dipping one small degree lower than the right, THREE individuated household people standing below it, their faces fond and level."),
(90,"WIDE","every face easy and unbothered","dusk", "The finished pine shelf on the far wall of the garage in flat dusty ORANGE dusk with THREE individuated people standing far apart below it, every one of them turned toward something else entirely, every face easy and unbothered, ONE small potted plant spilling over the bench edge below the square window."),
(91,"CU","eyes on the shelf, face warm and settled","dusk", f"The Man's round face and big confident nose close in flat dusty ORANGE dusk, {CROWN}, his eyes on the shelf above the bottom edge, his face warm and settled."),
(91,"XCU","-","dusk", "ONE tiny silver screwdriver lying flat on the finished pine shelf, seen from directly ABOVE and filling the view, the grain of the pine running level beneath it and one warm band of flat dusty ORANGE light lying across the metal."),
(92,"WIDE","face bright with morning confidence","dusk", f"{MAN} standing in the same garage on a Thursday with one hand raised toward ONE bare wall, {AMBER} beyond the square window in the left wall and ONE small potted plant spilling over the bench edge, his face bright with morning confidence."),
(92,"MED","both faces bright and certain","dusk", "exactly TWO figures standing side by side in the garage, TWO individuated household members with their hands in their pockets, both faces bright and certain, and in front of them ONE enormous pale rectangle of primer painted on the bare wall and rising ceiling-high where a whole bookcase is meant to go, ONE small potted plant spilling over the bench edge beside them."),
(93,"CU","both faces open and believing","dusk", "TWO individuated household faces close together in flat dusty ORANGE dusk, both chins lifted and both mouths open on the same easy agreement, both faces open and believing."),
(94,"MED","both faces bright and certain","dusk", "TWO individuated household members standing in front of the bare garage wall with their arms folded exactly alike, both faces bright and certain, ONE small potted plant spilling over the bench edge behind them and ONE completely BLANK white instruction sheet lying flat on the cream floor at their feet."),
(95,"XWIDE","face warm and proud","dusk", f"ONE tall finished pine bookcase standing against the garage wall in flat mustard GOLD autumn light with amber LEAVES beyond the square window in the left wall, FIVE shelves packed with plain closed books and every spine completely BLANK, the bookcase rising enormous beside {MAN} who stands small with one hand resting on its edge, his face warm and proud, ONE small potted plant spilling over the bench edge."),
]

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
MIN_CAM = {'XCU': 10, 'CU': 15, 'XWIDE': 20}
MAX_RUN = 3
MIN_CU_SHARE = 0.20
MIN_WIDE_SHARE = 0.42          # deadpan scale needs room; wides carry the joke
MAX_CASTLESS_RUN = 2           # flat-run v1 AND v2, measured together
GARAGE_MAX_SHARE = 0.22
CORE_ENVS = {'garage','kitchen','thesisdesk','observers','harbour','committee','archive',
             'tunnel','void','dusk','data'}
DUSK_ENVS = {'harbour'}                 # named lighting colours bite here
ACTS = {'A1': range(1, 10), 'A2': range(10, 15), 'A3': range(15, 27), 'A4': range(27, 38),
        'A5': range(38, 47), 'A6': range(47, 55), 'A7': range(55, 63), 'A8': range(63, 71),
        'A9': range(71, 81), 'A10': range(81, 88), 'A11': range(88, 96)}
FINAL_ACT = ACTS['A11']

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
                  r'purposeful|individuated|CLOSED|admiring|formal|tired|concern|amused|'
                  r'astonished|expectant|believing|conceding|adding|holding|arriving|waiting|'
                  r'generous|imaginative|unwell|unbothered|expert|thoughtful|practical|'
                  r'administrative|wry|frank|asking|knowing|busy|plain\b|young|grown', re.I)
EVENT = re.compile(
    r'burst|pop|fly|flar|blast|shoot|erupt|stream|pour|collaps|toppl|crack|snap|spring|slam|'
    r'throw|thrown|swing|scatter|shov|carr|drop|slid|tipping|tilt|vibrat|lift|roll|hover|dart|'
    r'glow|steam|smok|nod|shak|crouch|lean|reach|step|walk|run|hold|haul|pull|peer|point|count|'
    r'trudg|wrap|bang|settl|duck|turn|rub|sip|thump|spray|strik|rais|crush|crane|hang|stretch|'
    r'wav|file|squeez|press|balanc|climb|land|swarm|feed|trac|receiv|arriv|load|cross|'
    r'tumbl|pil|recoil|glanc|hurry|bend|bent|crowd|tear|driv|measur|argu|greet|wait|'
    r'watch|look|open|shut|reced|dwarf|clutch|slip|fork|appear|swivel|rotat|freez|curl|march|'
    r'thud|bow|sweep|stoop|practis|welcom|fold|jump|rest|loom|dangl|buckl|puff|retir|pose|'
    r'smooth|travel|drift|tuck|unroll|brush|nail|study|shrink|shrunk|brighten|flood|offer|spill|'
    r'meet|wish|spread|ring|split|huddl|thrust|catch|pass|grip|perform|plant|rise|rising|'
    r'casc|flick|aim|stagger|clip|steady|repeat|pace|pacing|plump|clink|pin|tap|wheel|light|'
    r'lit\b|beam|trad|dip|recit|square|straighten|leap|rock|spin|pat|draw|heap|tick|sit\b|'
    r'sitting|stand|pry|arrang|withdraw|refocus|swell|flex|declar|consult|boast|agree|'
    r'flutter|park|screw|dress|stride|striding|shuffl|nose|nosing|perch|box|fall|lying|laid|'
    r'\blay\b|stir|gap|burn|water|applaud|toast|cheer|dispute|disput|rake|rakes|'
    r'raking|fan|fanning|coil|veer|pass|kink|polish|stamp|vote|seat|bend|part|widen|'
    r'keep|kept|risen|halt|swing|queue|marking|worn|mount|pack|prop|say|saying|tell|telling|'
    r'crouch|hover|pushed|packed|strapped', re.I)

# COUNTS, NOT NOUNS — a scene that stages a character must carry the numeric
# words. A reference sheet is not sufficient (paid lesson, twice).
REQ = {
 'VERMILION RED coat': ['THREE round buttons', 'PAIR of hairs',
                        'ABSURDLY oversized dark ink-blue shoes'],
 'THE SILENT EXPERT':  ['sage GREEN cardigan', 'completely BLANK folder',
                        'composed and level'],
 'THE STUDENT':        ['ONE plain desk', 'ONE lamp of flat mustard GOLD',
                        'ONE tall stack of completely BLANK pages'],
 'folding table':      ['exactly SEVEN figures at the table'],
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
if not 4 <= ndata <= 7:
    errs.append(f'{ndata} data frames; this film expects 4-7')

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
                f'— the scale needs room')
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

# THE FLAT-RUN GATE v2 — and no cross-setting castless symbol run either.
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

# FREE-LANE GEOMETRY — no layout plate can be attached in this pipeline, so
# every castless row states its own ground. Void castless rows carry the exact
# cream-field clause; the rest name a level surface at point of use.
GEOMPAT = re.compile(r'running level|lying level|plain level ground|plain level wood|'
                     r'level floor|level beneath|flat cream field', re.I)
nogeom = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[2] == '-'
          and not GEOMPAT.search(s[4])]
if nogeom:
    errs.append('castless row with no geometry sentence of its own: ' +
                ' '.join('b%03d' % i for i in nogeom[:10]))
voidflat = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[2] == '-'
            and s[3] == 'void' and GEOM not in s[4] and 'plain level ground' not in s[4]]
if voidflat:
    errs.append('castless void row without the cream-field clause: ' +
                ' '.join('b%03d' % i for i in voidflat[:10]))

# FACE ACTION — declared, and present in the scene text itself.
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

# THE MONUMENT — the plank mountain is worded IDENTICALLY on every return, and
# it is absent from the final act, where it has shrunk to one offcut.
mon = [i for i, s in enumerate(S, 1) if 'THE PLANK MOUNTAIN' in s[4]]
if len(mon) < 6:
    errs.append(f'the monument returns {len(mon)} times; the law is at least 6')
badmon = [i for i in mon if MOUNT not in S[i-1][4]]
if badmon:
    errs.append('the monument is worded differently on a return: ' +
                ' '.join('b%03d' % i for i in badmon[:8]))
latemon = [i for i in mon if S[i-1][0] in FINAL_ACT]
if latemon:
    errs.append('the monument survives into the final act: ' +
                ' '.join('b%03d' % i for i in latemon))
if not any('shrunk to ONE short offcut' in s[4] for s in S if s[0] in FINAL_ACT):
    errs.append('the final act never shrinks the monument')

# THE SEASONS WINDOW — the garage recurrence is the clock: identical staging,
# three seasons, three plant stages, worded the same on every return.
rec = [i for i, s in enumerate(S, 1) if GAR_A in s[4]]
if len(rec) < 3:
    errs.append(f'the garage recurrence appears {len(rec)} times; the law is at least 3')
badrec = [i for i in rec if GAR_B not in S[i-1][4]]
if badrec:
    errs.append('a garage recurrence dropped the window/bench clause: ' +
                ' '.join('b%03d' % i for i in badrec))
seasons = {s for s in (SNOW, BLOSSOM, AMBER)
           if any(s in S[i-1][4] for i in rec)}
plants = {p for p in (P1, P2, P3) if any(p in S[i-1][4] for i in rec)}
if seasons != {SNOW, BLOSSOM, AMBER}:
    errs.append(f'the seasons window shows only {len(seasons)} of THREE seasons')
if plants != {P1, P2, P3}:
    errs.append(f'the plant shows only {len(plants)} of THREE growth stages')

# THE SUFFICIENT ANSWER — the screwdriver is held UP at least twice, and lies
# flat on the finished shelf exactly once, in the final act.
ups = [i for i, s in enumerate(S, 1) if UP in s[4]]
if len(ups) < 2:
    errs.append(f'the screwdriver is held up in {len(ups)} rows; the law is at least 2')
flatsd = [i for i, s in enumerate(S, 1) if f'{SD} lying flat' in s[4]]
if len(flatsd) != 1 or S[flatsd[0]-1][0] not in FINAL_ACT:
    errs.append(f'the screwdriver lies flat in {len(flatsd)} rows, and must do so exactly '
                f'once, in the final act')

# THE SILENT EXPERT — at least TWO committee rows and ONE archive-corridor row.
exp_comm = [i for i, s in enumerate(S, 1) if 'THE SILENT EXPERT' in s[4] and s[3] == 'committee']
exp_arch = [i for i, s in enumerate(S, 1) if 'THE SILENT EXPERT' in s[4] and s[3] == 'archive']
if len(exp_comm) < 2:
    errs.append(f'the silent expert holds {len(exp_comm)} committee rows; the law is at least 2')
if len(exp_arch) < 1:
    errs.append('the silent expert never reaches the archive corridor')

# DEADPAN SCALE — every act pairs ONE small confident object against ONE
# enormous patient one, both stated at point of use, at least twice per act.
SMALL = re.compile(r'\bONE tiny\b|\bONE small\b|standing tiny|standing small|ant-small|'
                   r'\btiny\b|\bsmall\b', re.I)
BIG = re.compile(r'ceiling-high|enormous|\bvast\b|shelf after shelf|taller than the trees|'
                 r'rising enormous|running away far|whole back wall', re.I)
for act, rng in ACTS.items():
    paired = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[0] in rng
              and SMALL.search(s[4]) and BIG.search(s[4])]
    if len(paired) < 2:
        errs.append(f'{act} stages the scale pairing in {len(paired)} rows; the law is 2 per act')

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
                      r'plaques?|screens?|folders?|plans?|drawings?|books?|spines?)\b', re.I)
unblanked = [i for i, s in enumerate(S, 1) if not isdata[i-1]
             and BLANKREQ.search(s[4]) and 'BLANK' not in s[4]]
if unblanked:
    errs.append('label-shaped object staged with its BLANK missing: ' +
                ' '.join('b%03d' % i for i in unblanked[:10]))
BANNED_NOUNS = re.compile(r'\b(labels?|posters?|contracts?|certificat\w*|documents?|ledgers?|'
                          r'invoices?|nameplates?|charts?|clipboards?|calendars?|timetables?|'
                          r'reports?|receipts?|memos?|slips?|bills?|lists?|notices?|'
                          r'placards?|leaflets?|magazines?|prospectus\w*|blueprints?)\b', re.I)
typed = [i for i, s in enumerate(S, 1) if not isdata[i-1] and BANNED_NOUNS.search(s[4])]
if typed:
    errs.append('banned document type-noun in scene text: ' +
                ' '.join('b%03d' % i for i in typed[:10]))
# the instruction sheet is legal ONLY beside its BLANK, in the same row.
inst = [i for i, s in enumerate(S, 1) if not isdata[i-1] and 'instruction sheet' in s[4]
        and 'completely BLANK white instruction sheet' not in s[4]]
if inst:
    errs.append('an instruction sheet staged without its BLANK: ' +
                ' '.join('b%03d' % i for i in inst[:10]))

# NEVER A DIAGRAM — the argument is objects at scale, not drawn lines.
DIAGRAM = re.compile(r'\bdotted\b|\bdiagram\w*|\barrows?\b|\bgraph\b|\bchart\b|dashed line|'
                     r'\bcurve\b|\btimeline\b', re.I)
diag = [i for i, s in enumerate(S, 1) if not isdata[i-1] and DIAGRAM.search(s[4])]
if diag:
    errs.append('the scale became a diagram: ' + ' '.join('b%03d' % i for i in diag[:10]))

# LIKENESS LAW — the narration may carry the names; the pictures never carry a
# person. No researcher, no author, no architect, no city, ever.
NAMES = re.compile(r'Kahneman|Hofstadter|Flyvbjerg|Buehler|\bGriffin\b|\bRoss\b|\bDaniel\b|'
                   r'Utzon|Sydney|Denver|New South Wales|Channel Tunnel', re.I)
likeness = [i for i, s in enumerate(S, 1) if NAMES.search(s[4]) or NAMES.search(s[2])]
if likeness:
    errs.append('a real name reached SCENE text: ' + ' '.join('b%03d' % i for i in likeness))
ARCH = re.compile(r'\barchitect\w*|\bdesigner\b|\bcomposer\b', re.I)
arch = [i for i, s in enumerate(S, 1) if not isdata[i-1] and ARCH.search(s[4])]
if arch:
    errs.append('the harbour act drew a person it may only draw a building for: ' +
                ' '.join('b%03d' % i for i in arch))

# NEVER SMUG — the planner is us. His face does confidence, hope, patience.
SMUG = re.compile(r'smug|smirk|\bsly\b|snide|mock\w*|ridicul\w*|foolish|silly', re.I)
smug = [i for i, s in enumerate(S, 1) if SMUG.search(s[4]) or SMUG.search(s[2])]
if smug:
    errs.append('smugness reached a row: ' + ' '.join('b%03d' % i for i in smug))
bright = [i for i, s in enumerate(S, 1) if 'bright with morning confidence' in s[4]]
if len(bright) < 5:
    errs.append(f'the bright morning face appears {len(bright)} times; the law is at least 5')

# ENVIRONMENT CAP — garage frames <=22%; every core environment appears.
setc = Counter(s[3] for s in S)
unknown = sorted(set(setc) - CORE_ENVS)
if unknown:
    errs.append(f'unknown environment tags: {unknown}')
gar_n = setc['garage']
if gar_n / len(S) > GARAGE_MAX_SHARE:
    errs.append(f'garage frames are {gar_n}/{len(S)} ({gar_n/len(S):.0%}), '
                f'max {GARAGE_MAX_SHARE:.0%}')
unused = sorted(CORE_ENVS - set(setc))
if unused:
    errs.append(f'core environments unused: {unused}')

# NAMED LIGHTING COLOURS — every harbour frame states its flat dusty ORANGE.
unlit = [i for i, s in enumerate(S, 1) if not isdata[i-1] and s[3] in DUSK_ENVS
         and 'dusty ORANGE' not in s[4]]
if unlit:
    errs.append('harbour frame missing flat dusty ORANGE at point of use: ' +
                ' '.join('b%03d' % i for i in unlit[:10]))

# TWO-FIGURE STAGING — any row staging a pair states its occupants prior, or the
# model grows a crowd (paid lesson).
ntwo = len([s for s in live if TWO in s[4]])
if ntwo < 5:
    errs.append(f'only {ntwo} rows state "exactly TWO figures"; the law is at least 5')

# THE ENDING — the shelf is up, the screwdriver is down, the mountain is gone,
# and the last picture is the bookcase that has yet to be built.
def _scene_for(line):
    return ' || '.join(s[4] for s in S if s[0] == line)
ending_checks = [
    (88, 'mounted level on the far wall',  'the shelf goes up on line 88'),
    (88, 'shrunk to ONE short offcut',     'the mountain is gone by line 88'),
    (91, f'{SD} lying flat',               'the screwdriver lies flat on line 91'),
    (95, 'bookcase',                       'the last picture is the bookcase'),
]
for line, need, msg in ending_checks:
    if need not in _scene_for(line):
        errs.append(f'THE ENDING out of order: {msg}')
if S[-1][0] != len(sents):
    errs.append('the last row does not sit on the last sentence')

dead = [s for s in S if s[2] == '-' and s[4] != DATA]
print('cameras: ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
print(f"close-ups {cu}/{len(live)} ({cu/len(live):.0%}) | wides {wide}/{len(live)} "
      f"({wide/len(live):.0%}) | faces {len([s for s in live if s[2]!='-'])}/{len(live)} | "
      f"events {len(live)-len(noev)}/{len(live)} | data {ndata} | garage {gar_n} "
      f"({gar_n/len(S):.0%}) | monument {len(mon)} | recurrences {len(rec)} | "
      f"screwdriver up {len(ups)} | expert {len(exp_comm)}+{len(exp_arch)} | "
      f"two-figure {ntwo} | bright face {len(bright)} | castless {len(dead)} | holds "
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
      'hold_est_s': round((len(sents[s[0]-1].split()) / WPM * 60) / per_line[s[0]], 2)}
     for i, s in zip(ids, S)], indent=1))
nocast = [i for i, s in zip(ids, S) if s[4] == DATA or s[2] == '-']
(FILM / 'production' / 'cast.json').write_text(json.dumps({'nocast': nocast}, indent=1))
print(f'\nwrote {len(ids)} prompts + board.json + cast.json ({len(nocast)} frames with no cast)')
