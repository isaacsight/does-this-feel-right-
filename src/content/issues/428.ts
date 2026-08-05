/* ──────────────────────────────────────────────────────────────
   ISSUE 428 — MAR 2027
   THE ONE PERCENT
   一パーセント — 検出器の誠実さは控訴窓口で測る

   The wire story from the platform desk. A Google research paper
   ("scalable detection of adversarial synthetic slop and
   coordinated media abuse") describes a cluster-termination
   system — SCCTS — deployed to a major online video platform:
   channels judged by neighbourhood (shared behaviour, upload
   rhythm, infrastructure), roughly 50,000 coordinated clusters
   identified, on the order of 130,000 channels terminated, an
   appeal-overturn rate under one percent. In the same season,
   Kurzgesagt — 25 million subscribers, human-made for over a
   decade — publicly reported that the platform’s automatic AI
   detectors wrongly classified its videos as synthetic and
   throttled the channel; its contacts at the platform confirmed
   and repaired it within days. A five-million-subscriber
   creator without those contacts reported months of decaying
   reach with no way to learn the cause.

   Filed as a dispatch because it happened on the record and
   left a doctrine: a detector’s honesty is measured at its
   appeal desk, not at its precision figure. Under one percent
   of an industrial sweep is still a street of real people.

   Identity decisions (differentiated from 401, the previous
   dispatch — ivory / asymmetric-left / pool):
     • coverStock = 'ledger' — the sweep IS an accounting
       register; pale graph-ruled paper for a purge counted in
       clusters and percentages.
     • coverLayout = 'ledger-rule' — rules and numbered totals
       across the cover; the cover is the audit (pairs with
       ledger stock, per 372's precedent).
     • coverSeal = TERMINATED · OVERTURNED — the whole story
       in one rubber circle.
     • accent = 'graphite' — pencil-lead grey for audits and
       ledgers (introduced 372, paired with ledger stock). The
       dispatch default (brick) belongs to news with blood in
       it; this is news conducted in tabular numerals.
     • spread.type = 'dispatch', spread.stock = 'ledger'.

   Artifact edition drafted FIRST per artifact-language:
   artifacts/428-the-one-percent.html — an operable sweep field
   (400 seeded channels, farm clusters vs humans), a threshold
   radiogroup carried into every sweep, honest authored hit
   rates disclosed in the colophon, a claims register citing
   public reporting at the floor, seed 428-0805 printed at the
   masthead. The reduction to this spread gives up the operable
   trade (threshold → false positives) and keeps its verdict as
   prose in propositions 03 and 05.

   Provenance: a reader-supplied transcript of a published
   video commentary reporting the Google paper (credited there
   to Jim Louderback’s newsletter), Kurzgesagt’s public
   statement on its throttling, and the platform’s own 2025
   statement of 20 million uploads per day. Claims are printed
   as reported, with hedges kept.
   ────────────────────────────────────────────────────────────── */

import type { IssueRecord } from './index'

export const ISSUE_428: IssueRecord = {
  number: '428',
  month: 'MAR',
  year: '2027',
  feature: 'THE ONE PERCENT',
  featureJp: '一パーセント',
  price: '¥0 · BYOK',
  tagline: 'MAGAZINE FOR CITY CODERS · 街のコーダーのために',

  coverStock: 'ledger',
  coverLayout: 'ledger-rule',

  coverSeal: {
    label: 'TERMINATED · OVERTURNED',
    date: 'III·27',
  },

  accent: 'graphite',

  headline: {
    prefix: 'The',
    emphasis: 'One',
    suffix: 'Percent.',
    swash: 'A classifier learned to terminate channels by the neighbourhood and swept a hundred and thirty thousand of them. Its error bar is under one percent — and one percent of an industrial sweep is still a street of real people. A dispatch on the purge, the false positive with twenty-five million subscribers, and the appeal that turned out to be a phone number.',
  },

  contents: [
    { n: '001', en: 'The sweep is real', jp: '一斉削除は本物である', tag: 'FIELD' },
    { n: '002', en: 'Judgement moved to the neighbourhood', jp: '判定は近傍へ移った', tag: 'METHOD' },
    { n: '003', en: 'The false positive wore a decade of humanity', jp: '誤検出は十年の人間性をまとう', tag: 'CAUTION' },
    { n: '004', en: 'The appeal was a phone number', jp: '控訴は電話番号だった', tag: 'ACCESS' },
    { n: '005', en: 'Measure the detector at its appeal desk', jp: '検出器は控訴窓口で測れ', tag: 'DOCTRINE' },
  ],

  spread: {
    type: 'dispatch',
    kicker: 'DISPATCH · 速報',
    title: 'The One Percent.',
    titleJp: '一パーセント。',
    deck: 'The video platform’s war on synthetic slop found its weapon: terminate the cluster, not the video. Fifty thousand coordinated networks identified, a hundred and thirty thousand channels gone, and an appeal-overturn rate the research paper can print with pride — under one percent. Then the same family of detectors misread one of the most trusted human-made channels on the platform, throttled it quietly, and was corrected only because that channel had people to call. A dispatch on what the error bar hides.',
    byline: 'BY THE EDITORS · KERNEL.CHAT',
    stock: 'ledger',

    slug: 'KERNEL.CHAT WIRE · 428 · III·27 · 50,000 CLUSTERS · 130,000 CHANNELS · OVERTURN UNDER 1% · INK STILL WET',

    dateline: 'THE PLATFORM DESK — FILED WHILE THE SWEEP WAS STILL RUNNING.',

    filedAt: '5 AUG 2026 · COVERING ONE SEASON',
    status: 'FILED',

    bridge: {
      issue: '417',
      text: '417 put a machine’s draft under a reader’s three fates — keep, take the hand, strike — one line at a time. 428 is the same adjudication running in reverse at industrial scale: a machine assigning fates to human work, with no radiogroup offered to the judged.',
    },

    intro: 'The research paper reads like plumbing and describes a purge. A cluster-termination system, deployed by its authors to "a major online video platform," stops asking whether a video broke a rule and starts asking who the channel resembles — who it shares a template with, an upload cadence with, a server with. When the resemblance crosses a threshold, the whole block goes at once. The numbers are the story: fifty thousand clusters, a hundred and thirty thousand channels, millions of videos, an overturn rate under one percent. This dispatch is filed for the remainder — the channels inside that one percent, and the difference between the two kinds of appeal available to them.',

    propositions: [
      {
        n: '01',
        overline: 'FIELD',
        filedAt: '09:12',
        title: 'The sweep is real.',
        titleJp: '一斉削除は本物である',
        body: [
          'Over a hundred thousand channels removed inside six months, by public reporting — and the Google paper behind it claims roughly fifty thousand coordinated clusters identified and on the order of a hundred and thirty thousand channels terminated. The paper never names the platform; its authorship does that for it. These are not first-strike warnings. They are terminations, executed in groups.',
          'The desk notes what the sweep is aimed at, because it matters for everything that follows: not the individual creator experimenting with a first faceless channel, but content farms filing synthetic video at industrial scale — connected operations sharing behaviour, upload patterns, and infrastructure. Against that adversary, the sweep is the right tool. The platform said in 2025 that at least twenty million videos arrive per day. Nothing adjudicated one screen at a time survives that arithmetic.',
        ],
      },
      {
        n: '02',
        overline: 'METHOD',
        filedAt: '10:04',
        title: 'Judgement moved to the neighbourhood.',
        titleJp: '判定は近傍へ移った',
        body: [
          'The quiet doctrine inside the paper is a change of unit. Moderation used to judge the video; then the channel; the cluster system judges the neighbourhood. A channel’s fate is decided partly by what it resembles — and resemblance is a statistic, computed over signals no creator can see, against a threshold no creator can read.',
          'This is how every detection system scales, and the desk does not file it as scandal. It files it as a property with consequences: when the unit of judgement is the neighbourhood, the false positive is no longer a mislabelled video that can be re-reviewed. It is a livelihood, assigned to the wrong block by machinery that was never asked to explain itself.',
        ],
      },
      {
        n: '03',
        overline: 'CAUTION',
        filedAt: '11:40',
        title: 'The false positive wore a decade of humanity.',
        titleJp: '誤検出は十年の人間性をまとう',
        body: [
          'Kurzgesagt has spent over a decade making animation by hand — twenty-five million subscribers, more than three and a half billion views, and a body of work so canonical that it plausibly sits inside the training data of the very generators the platform is sweeping for. This year its views fell to levels it last saw in 2013, while click-through rate and watch time rose. The audience was leaning in; the distribution was gone.',
          'The channel’s own account, published after it got answers: the platform’s automatic AI-detection tools wrongly classified its very much human-made videos as synthetic slop, and started to choke the channel. Not delete — choke. The misread was not a termination with a notice and an appeal link. It was a quiet starvation, invisible from the outside and nearly invisible from the inside, distinguishable from a change in taste only by a creator with the analytics fluency to prove the audience still wanted the work.',
        ],
      },
      {
        n: '04',
        overline: 'ACCESS',
        filedAt: '13:22',
        title: 'The appeal was a phone number.',
        titleJp: '控訴は電話番号だった',
        body: [
          'What repaired the misread was not the appeal process. It was contacts — the channel "quickly got in touch," the platform confirmed something was wrong, and the bug was, in the channel’s careful phrasing, hopefully fixed for now. The desk begrudges nobody here: the channel used the door it had, and the platform’s people were by all accounts helpful and transparent. That is the system working, for the channels it can see.',
          'The filing is for the channels it cannot. A creator with five million subscribers reported the same shape of decay — months of worsening performance, no way to learn whether a classifier was the cause — and no phone to pick up. The overturn rate stays under one percent partly because overturning requires knowing you were misjudged, and the throttled are told nothing. An appeal that depends on a relationship is not a process. It is patronage with a ticketing system.',
        ],
      },
      {
        n: '05',
        overline: 'DOCTRINE',
        filedAt: '15:05',
        title: 'Measure the detector at its appeal desk.',
        titleJp: '検出器は控訴窓口で測れ',
        body: [
          'The doctrine that survives this filing is one sentence: a detection system’s honesty is measured at its appeal desk, not at its precision figure. Under one percent is a genuinely good number, and at twenty million uploads a day it is also thousands of misjudged people — a population, not a rounding error. The precision figure describes the sweep. Only the appeal desk describes what it is like to be swept.',
          'The desk’s tests for any classifier holding livelihoods, filed for reuse: the misjudged must be told they were judged; the appeal must be a process that works without a relationship; and the throttle must be as visible as the termination — a channel choked in silence has been punished without ever being charged. The sweep against the farms can be a flower for the platform. The desk keeps one flower back until the one percent can find the door.',
        ],
      },
    ],

    bulletin: {
      text: 'The classifier moved the unit of judgement from the video to the neighbourhood. The appeal never moved at all.',
      attribution: 'KERNEL.CHAT · DISPATCH · 428',
    },

    outro: 'The farms will rebuild and the sweep will run again; that contest is permanent and the desk is glad the platform is finally winning rounds of it. The remainder is what this dispatch files for the record: a decade-old human channel misread by the machine, repaired through a door most creators will never have, and a percentage that reads as triumph in a research paper and as a season of silent starvation from inside the wrong block. File it beside 401’s doctrine — verify by event, not handshake. A platform that terminates by neighbourhood owes each neighbour, at minimum, the event: you were judged, here is the desk, the desk answers.',

    signoff: '街のコーダーたちへ — count the swept, then count the misjudged; only one of those numbers is in the paper.',

    terminator: 'END OF DISPATCH · KERNEL.CHAT/428 · FILED 5 AUG · ONE SEASON · INK STILL WET',
  },

  audit: {
    drafted: 'artifact first · kernel.chat editorial · Claude Fable 5 · 5 August 2026',
    verified:
      'seven load-bearing claims — cluster count, channel count, overturn rate, upload volume, subscriber and view figures, the throttling account — each printed as reported with its source named in the register; hedges kept ("roughly", "on the order of", "hopefully fixed for now")',
    adherence:
      'ledger stock + ledger-rule + graphite per 372\'s audit-register precedent; sweep field deterministic from printed seed 428-0805; threshold radiogroup roving-tabindex; authored hit rates disclosed in the colophon; session ledger unrecorded and says so; reduced motion resolves sweeps instantly; print keeps the field and register, hides the controls',
    readCut:
      'source transcript ~1,900 words; kept the numbers, the Kurzgesagt account, and the access asymmetry; cut the presenter\'s stagecraft, the 3D-printed prop, and the self-referential shadowban test',
    pressed: 'artifacts/428-the-one-percent.html · III·27',
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
