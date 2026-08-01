/* ──────────────────────────────────────────────────────────────
   ISSUE 428 — MAR 2027
   NOTHING NEW WAS ADDED
   何ひとつ新しくはない — 規則は動かず、審査の列だけが動いた

   The second `compare` instance (406 was the first, and remains the
   only other). Per docs/interaction-language.md rule 7, two
   instances is the threshold at which a pattern MAY be extracted —
   this issue deliberately does not extract one. CompareFeature is
   reused as written; the only change to it is an optional
   `references` block, which every prior compare (406) is unaffected
   by because it is optional.

   The material: YouTube's 15 July 2025 monetization update, which
   renamed the "repetitious content" policy to "inauthentic content"
   and named three categories that make a channel ineligible. The
   platform's own framing, repeated in every clarification since:
   no new policies were added to the Partner Program.

   Why a switch and not an essay: the load-bearing sentence is
   literally true and practically incomplete, and those are not
   points on a spectrum. Read as THE LETTER, the July update moved
   nothing — the eligibility bar is where it always was, generative
   AI is explicitly not the question, reaction videos with original
   commentary are untouched. Read as THE QUEUE, a policy lives where
   it is enforced, and the update handed the review stack three new
   handles, two of which ("generic", "off-putting") are affective
   judgments made at a scale only a classifier can serve. Both
   readings survive the same six facts. There is no blended reading
   that is sixty per cent letter and forty per cent queue.

   Unlike 406, this piece DOES give a verdict. 406 declined because
   both of its readings had equal claim on the same day; here they
   do not — they answer different questions (what you are owed
   versus what you will meet), and saying so is the honest
   resolution rather than a false symmetry.

   Every fact is externally sourced and dated; the six citations are
   filed in the spread's own references block, which is what the
   `references` field was added to CompareSpread for. No fact is
   invented for symmetry, and no reading is written as a strawman —
   THE LETTER is argued as the platform would argue it.

   Identity decisions:
     • coverStock = 'cream' — the anchor stock, unused across the
       419–427 run. The plainest paper in the cabinet for the least
       novel policy update: the material makes the argument before
       the headline does.
     • coverLayout = 'classic' — the switch lives inside the spread;
       the cover has no apparatus to stage.
     • coverSeal = NO NEW POLICIES · III·27 — the signature move.
       The platform's own sentence, stamped as a rubber seal, in the
       corner where a reader expects an embargo notice. The stamp
       is the claim the whole issue is a reading of.
     • accent = 'brick' — deeper, archival, record-of-record. Unused
       in the 419–427 run, and the correct register for a piece
       whose subject is a text rather than an event.
     • spread.type = 'compare', spread.stock = 'cream'.

   Artifact edition: artifacts/428-nothing-new-was-added.html —
   THE REVIEW QUEUE, a six-stratum descent of one upload from the
   file to the rule that judges it. The depth axis (artifact-
   language §III) is the review stack itself, which the spread has
   no room for: the spread argues the text, the artifact lowers a
   probe through the machinery the text runs on. Carried context is
   the upload's character, chosen at the surface, re-inking every
   stratum below it. What the reduction gives up: the descent, the
   gauge, and the three-way carry — the spread keeps the binary
   because the binary is the argument.
   ────────────────────────────────────────────────────────────── */

import type { IssueRecord } from './index'

export const ISSUE_428: IssueRecord = {
  number: '428',
  month: 'MAR',
  year: '2027',
  feature: 'NOTHING NEW WAS ADDED',
  featureJp: '何ひとつ新しくはない',
  price: '¥0 · BYOK',
  tagline: 'MAGAZINE FOR CITY CODERS · 街のコーダーのために',

  coverStock: 'cream',
  coverLayout: 'classic',

  coverSeal: {
    label: 'NO NEW POLICIES',
    date: 'III·27',
  },

  accent: 'brick',

  headline: {
    prefix: 'Nothing',
    emphasis: 'New',
    suffix: ' Was Added.',
    swash: 'A platform renamed one policy and half the internet read a ban. The text moved nothing. The review queue moved anyway. Six facts, read both ways, on a switch.',
  },

  coverDeck:
    'A platform renamed one policy and half the internet read a ban. Six facts, read both ways.',

  contents: [
    { n: '001', en: 'A rename that renamed nothing', jp: '名を変えただけの改訂', tag: 'POLICY' },
    { n: '002', en: 'The sentence nobody finished reading', jp: '誰も読み終えなかった一文', tag: 'FACT' },
    { n: '003', en: 'The three that lose the money', jp: '収益を失う三分類', tag: 'FACT' },
    { n: '004', en: 'The tool was never the question', jp: '道具は問題ではなかった', tag: 'FACT' },
    { n: '005', en: 'Reactions were never the target', jp: 'リアクションは的ではない', tag: 'FACT' },
    { n: '006', en: 'The second look, and the wait', jp: '再審査と、その待ち時間', tag: 'QUEUE' },
  ],

  spread: {
    type: 'compare',
    kicker: 'THE SWITCH · 二読',
    title: 'Nothing New Was Added.',
    titleJp: '何ひとつ新しくはない。',
    deck: 'On 15 July 2025 a platform renamed one policy and published a sentence: no new policies were added to the Partner Program. It is true. It is also the least useful true sentence of that year. Read as THE LETTER, the rules stand exactly where they stood. Read as THE QUEUE, three new words entered the machinery that decides what your upload earns. Same six facts. Flip the switch.',
    byline: 'BY THE EDITORS · KERNEL.CHAT',
    stock: 'cream',

    intro: [
      {
        heading: 'A clarification is not nothing',
        headingJp: '明確化は、無ではない',
        paragraphs: [
          'The update was small enough to be a footnote. A policy called "repetitious content" — in force since long before a model could render a face — became a policy called "inauthentic content", and three categories were spelled out underneath it: content that is generic, templated, or mass-produced; content that is off-putting or distressing; and synthetic personas presenting as authorities on health, finance, law, or politics. The platform said, in as many words, that nothing had been added to the Partner Program. Every clarification since has said it again.',
          'And the creator internet read a ban on AI. Not because anyone lied, but because a rule and its enforcement are two different objects, and only one of them was published. The text is a promise about what you are owed. The queue is a description of what you will meet. This piece holds both, on a switch, because there is no reading that is part-way between a promise and a description — the honest move is to give the reader all six facts under one lens, then all six under the other.',
        ],
      },
    ],

    lenses: [
      {
        id: 'letter',
        label: 'THE LETTER',
        labelJp: '条文',
        stance:
          'Read the text as written and nothing moved: a rename of a guideline already in force, tool-agnostic by design, with the eligibility bar exactly where it has always been.',
      },
      {
        id: 'queue',
        label: 'THE QUEUE',
        labelJp: '審査',
        stance:
          'A policy lives where it is enforced. Three new words entered a review stack that runs at platform scale, and a new word is a new handle — whatever the changelog says.',
      },
    ],

    defaultLens: 'letter',

    facts: [
      {
        fact: 'On 15 July 2025 the "repetitious content" policy was renamed "inauthentic content".',
        factJp:
          '2025年7月15日、「繰り返しの多いコンテンツ」の規定が「本物ではないコンテンツ」に改称された。',
        readingA:
          'A minor update to a longstanding guideline, in the platform\'s own words. Content of this kind has never been eligible for monetization; the rename makes the existing bar easier to describe to the people it applies to.',
        readingB:
          'The old name described a measurable property — a thing repeats or it does not. The new one names a judgment. "Repetitious" is something you can count; "inauthentic" is something somebody has to decide about you.',
      },
      {
        fact: 'The platform stated that no new policies were added to the Partner Program.',
        factJp:
          'YouTubeは、パートナープログラムに新しい規則は一切追加していないと述べた。',
        readingA:
          'Literally true and worth taking at face value. Nobody\'s eligibility changed on 15 July. A channel that was monetizable on the fourteenth was monetizable on the sixteenth, under the same standard, for the same reasons.',
        readingB:
          'That sentence was published because a very large number of creators had already concluded otherwise. A clarification issued into a panic is evidence that the enforcement was being felt before the wording changed — which is the whole disagreement, stated by the platform, in the platform\'s own reassurance.',
      },
      {
        fact: 'Three categories were named as ineligible: generic or repetitive content; off-putting or distressing content; and AI personas presenting as experts on sensitive topics such as health, finance, law, or politics.',
        factJp:
          '収益化の対象外となる三つの分類が名指しされた。定型的・反復的なもの、不快なもの、そして健康・金融・法律・政治といった重要な話題で専門家を装う合成人格である。',
        readingA:
          'Each is a specific, describable failure, and the third is the one that matters most: a synthetic figure claiming medical or financial authority is a harm with a name, not an aesthetic complaint. None of the three is a rule about a tool.',
        readingB:
          'Two of the three are affective judgments. "Generic" and "off-putting" are the kind of call a person makes in a second and a classifier makes a million times a day, and neither of them can show its work. A creator cannot appeal a vibe.',
      },
      {
        fact: 'The policy is tool-agnostic: it applies the same way to generative AI, CGI, stock footage, and a camera.',
        factJp:
          '規定は道具を問わない。生成AIも、CGIも、ストック映像も、カメラも同じ扱いである。',
        readingA:
          'AI was never the question, and the platform ships AI tools of its own. What is asked for is unique human contribution — voice, editing, structure, a point of view — and content that has it stays eligible no matter what rendered the frames.',
        readingB:
          'Tool-agnostic is a claim about the rule, not about the distribution of what arrives. The content most likely to be generic at scale is the content that became cheapest to produce, so a neutral rule lands unevenly on purpose — and the creators it lands on are the ones who were told the tool is fine.',
      },
      {
        fact: 'The reused-content policy did not change. Commentary, clips, compilations, and reaction videos are reviewed as they were before.',
        factJp:
          '再利用コンテンツの規定に変更はない。解説、切り抜き、まとめ、リアクションは従来どおり審査される。',
        readingA:
          'The clearest correction of the July misreading. A reaction video carrying original commentary was monetizable before and is monetizable after; what was disqualified is a bare repost of someone else\'s work, which was already disqualified.',
        readingB:
          '"As before" is both the reassurance and the problem. Reused-content review was already the least predictable surface on the platform, and this update pointed a great deal of new attention at it while changing none of the machinery that made it unpredictable.',
      },
      {
        fact: 'Since 10 March 2025, a video first assigned "Limited" or "No ad earnings" is routed for an additional review that may be completed by a human. Most decisions still land in minutes; some take up to 24 hours.',
        factJp:
          '2025年3月10日以降、当初「制限付き」または「収益化なし」と判定された動画は、人間が担当しうる追加審査へ自動的に回される。大半は数分で決まるが、最大で24時間かかる場合もある。',
        readingA:
          'The platform spending real money to be more right. A person sees the full context of a video and can weigh cultural difference in a way the first-pass classifier cannot, and the stated purpose is to raise monetization potential, not lower it.',
        readingB:
          'It is also the platform conceding, in a product change, that the automated pass is wrong often enough to need a second one. The relief is genuine and it arrives as a wait — and a video earns most of what it will ever earn in the hours that wait is running.',
      },
    ],

    verdict:
      'Both readings are true and they are not symmetrical, because they answer different questions. THE LETTER is what the platform owes you and will defend. THE QUEUE is what your upload will actually meet on a Tuesday. Read the letter so you know what is being promised; build for the queue, because that is the thing that pays.',

    outro: [
      {
        heading: 'Where a rule actually lives',
        headingJp: '規則が実際に住む場所',
        paragraphs: [
          'The practical instruction survives the disagreement intact, which is how you know it is the real one. Put something in the video that could only have come from you — a voice, a cut, an argument, a mistake — and it does not matter what rendered the frames. That was the rule in 2019 and it is the rule now. The July update did not invent it; it wrote it down in a way that finally scared people into reading it.',
          'What the update did change is the vocabulary the machinery has to work with. "Repetitious" was a property of a file. "Inauthentic" is a verdict about a person. Nothing in the changelog moved, and something in the room did — and a magazine that files an audit with every issue is not in a position to pretend those are the same thing.',
        ],
      },
    ],

    references: {
      kicker: 'THE POLICY FILE · 出典',
      note: 'Every fact above, with where it came from. Six claims, six citations, all read before the issue was set.',
      items: [
        {
          authors: 'YouTube Help',
          year: '2025',
          title: 'YouTube channel monetization policies',
          journal: 'support.google.com/youtube/answer/1311392',
        },
        {
          authors: 'YouTube Help',
          year: '2025',
          title: 'Understanding additional reviews for ad monetization',
          journal: 'support.google.com/youtube/answer/16271309',
        },
        {
          authors: 'Social Media Today',
          year: '2025',
          title: 'YouTube Clarifies Changes to Monetization Rules Around Inauthentic Content',
          journal: 'socialmediatoday.com, 8 July 2025',
        },
        {
          authors: 'PPC Land',
          year: '2025',
          title: 'YouTube clarifies "inauthentic content" policy changes',
          journal: 'ppc.land',
        },
        {
          authors: 'Search Engine Journal',
          year: '2025',
          title: 'YouTube Targets Mass-Produced Content In Monetization Update',
          journal: 'searchenginejournal.com',
        },
        {
          authors: 'Tubefilter',
          year: '2025',
          title: 'YouTube thinks a more human touch will cut down on demonetization mistakes',
          journal: 'tubefilter.com, 11 March 2025',
        },
      ],
    },

    pullQuote: {
      text: '"Repetitious" was a property of a file. "Inauthentic" is a verdict about a person.',
      attribution: 'THE SWITCH DESK · 428',
    },

    signoff: '街のコーダーたちへ — read the letter, then build for the queue.',
  },

  audit: {
    drafted: 'magazine-editor session, III·27',
    verified: 'six claims, six citations — all sourced before the issue was set',
    adherence: 'CompareSpread, second instance · no pattern extracted (rule 7)',
    readCut: 'six facts, twelve readings · no fact invented for symmetry',
    pressed: 'III·27 · artifact edition 428-nothing-new-was-added',
  },

  credits: {
    editorInChief: 'Isaac Hernandez',
    creativeDirection: 'kernel.chat group',
    artDirection: 'in-house',
    copy: 'kernel.chat editorial',
    japanese: 'kernel.chat editorial',
    production: 'kernel.chat group',
  },
}
