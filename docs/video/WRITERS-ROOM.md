# The writers' and directors' room

A house reference, added 2026-08-07 after four builds of *Nobody Roots for
Goliath* proved that ONE register applied to a whole film flattens it. A room
is not a list of people to admire — each seat is an instrument with a job, and
the Director decides which seats are staffed for a given subject.

The rule that produced this document: **the register theory kept losing to the
thing that works.** Two films written in the comedian's register are the
channel's best-performing and Isaac's favourite. One film written as a
reveal-essay was rebuilt three times. Staff the room from evidence.

## The seats

**Larry David — the grievance engine.** An unwritten social rule, litigated by
somebody with a tiny want and no exit. His signature move is the TRAP: the
complaint is the evidence, so the character cannot defend himself without
proving the accusation. Use for: etiquette, honour, manners, status rules.
Shipped in *Somebody Has to Die Now* and *The Pettiest Wars*.

**Armando Iannucci — institutional absurdity.** Machinery that reliably
produces terrible outcomes with nobody responsible, described in precise,
vicious language. Nobody in an Iannucci scene is evil; the SYSTEM is the
antagonist. Use for: algorithms, policy, bureaucracy, incentives, platforms.

**Michael Schur — the warm structure.** Moral philosophy made load-bearing,
with characters genuinely trying to be good. He is the antidote to a bleak
turn: our films land on "what do we do about it", and Schur is the seat that
makes the answer feel earned rather than tacked on.

**Jesse Armstrong — status.** Every line is a status move; nobody says what
they mean because saying it would cost position. Use for: hierarchy, class,
credit, promotion, reputation. He would have been the right first call on the
underdog film, which is a status story we wrote three times as a mechanism.

**Alec Berg — the compounding consequence.** One small evasion escalating until
it is a catastrophe, each step individually reasonable. Use for: anything with
a slippery slope that is actually real.

**Aniello / Downs / Statsky — generational friction.** The old pro and the
young one, mutual contempt built on mutual need. Use for: craft, obsolescence,
taste, the thing that used to work.

**Quinta Brunson — affection inside constraint.** A film that loves the people
stuck in a broken system without pretending the system works. Use when the
subject could easily curdle into contempt for its own characters.

**Trey Parker — the beat rule.** See below; this seat is structural, not tonal,
and it is staffed on EVERY film.

**Charlie Kaufman — the formal conceit.** The film is about its own form. Use
sparingly and only when the medium is already the argument (the collage world's
memory film was the closest we have come).

## The two seats that became code

**Trey Parker's BUT / THEREFORE rule.** Parker's stated rule: beats should
connect with "but" or "therefore", never "and then". A script whose beats are
joined by "and then" is a list, which is exactly the essay-drift fault that got
two films shelved and one rebuilt three times. This is testable: take each act
transition and ask which conjunction fits. `tools/video/register-profile.py`
gates VOICE; a companion structure gate should reject a script whose acts chain
with "and then".

**Jesse Armstrong's status as a board quota.** The underdog board already
enforces a POWER relation on frames (who is bigger, who is looking at whom, who
is alone) — that check came from the Williamson build and survived because it
is really a status check. Generalise it: on any status subject, every frame
states a status relation.

## How the Director staffs a film

1. Name the subject in one line.
2. Ask what KIND of problem it is: an unwritten rule (David), a system
   (Iannucci), a hierarchy (Armstrong), a slippery slope (Berg), a moral
   question (Schur).
3. Staff one primary seat and at most one secondary. Two voices is a room;
   four is mush.
4. Parker sits on every film, because structure is not a flavour.
5. Write the CLAIMS file first, so whoever holds the pen is making jokes out of
   sourced facts rather than inventing material.

## What a room does NOT change

The house voice band (`register-profile.py`), the story law (a character who
wants something), the no-generated-text law, and the frame gate. A seat changes
the JOKES and the STRUCTURE, never the discipline.

## The directors' chairs

Writers decide what happens; directors decide what the camera does about it.
These are separate instruments and the Director staffs them separately.

**Phoebe Waller-Bridge — the look to camera.** She owns TOCAM, and her rule is
that it is a RELATIONSHIP, not a gag: it starts as a shared glance, deepens
into confession, and the most devastating beat is when the character will no
longer look at us. That is an ARC, and it is machine-checkable exactly like the
spectator runner. Our films have used TOCAM as a flat device; hers escalates.

**Donald Glover — unremarked surrealism.** Something impossible sits in the
background and nobody comments on it, ever. This is our RUNNER doctrine
generalised, and it is the strongest single tool we have for rewatch value: the
fortress unravelling, the unshaken hand, the border beast stealing a bucket.
Glover's rule sharpens it — the strange thing must never be acknowledged by
anybody in the frame OR by the narration.

**Rogen and Goldberg — the oner.** A continuous unbroken take. In a STILLS film
this is a device we have never tried: four to six consecutive frames staged as
one continuous camera move through a space, so the cut disappears and the
sequence reads as motion without any motion. It would break the every-five-
seconds cut rhythm that all four films so far share.

**James Burrows — the master shot.** Let the ensemble play in one wide frame
and cut sparingly. For us that means blocking over coverage: fewer, longer,
better-staged frames rather than more of them. A corrective if a board starts
bloating.

**Jonathan Krisel — deadpan symmetry.** Centred, still, uncomfortable, held a
beat too long. The right chair for absurd worlds where the comedy comes from
composure rather than motion.

**Amy Sherman-Palladino — the walk-and-talk.** Momentum through space while the
words carry the load. In stills: consecutive frames that track a character
moving through a place, the background changing while he does not.

**Dan Harmon — the story circle.** Structural, like Parker. Eight beats:
comfort, want, unfamiliar situation, adapt, get it, pay a price, return,
changed. Our story law says a character must want something; Harmon's circle is
the shape that want has to travel, and it is a better checklist than "acts".

**Dan Levy — the sincere landing.** Cruelty resolved into genuine warmth
without irony. The seat that keeps a bleak turn from curdling — the handshake
taken by a child at the end of the Goliath film is a Levy beat.

**Tina Fey — density.** Joke count per minute, cutaways, no line that is only
doing plot work. A corrective when a script goes explanatory.

## The three that become new craft

1. **The escalating TOCAM** (Waller-Bridge) — declare the arc in the board and
   check it: glance, then confession, then refusal to look.
2. **The oner** (Rogen/Goldberg) — a declared run of consecutive frames staged
   as one camera move. New device; try it on the next film.
3. **The story circle** (Harmon) — sits beside Parker's but/therefore as the
   second structural gate on any script.
