/* ──────────────────────────────────────────────────────────────
   ISSUE 429 — MAR 2027
   THE INK IS THE CELL · インクが本体

   The Oxford Nanopore MinION puts a DNA/RNA sequencing run on a
   kitchen table: USB-C to a laptop, reads filling in as they
   happen. This issue reviews the instrument WITHOUT owning it —
   the specimen register, declared on the cover seal (SPECIMEN 00 ·
   NO RUN YET) and enforced line by line: store prices were read
   from the ONT US store on 2026-08-18; every run figure is
   third-party representative (Menon, 2026-05) and says so where
   it appears. Nothing has been bought. No run has been performed.
   The source of record is the in-repo purchase brief at
   docs/hardware/nanopore-sequencer.md and the Run Folio
   Specimen 00 beside it.

   Identity: ivory (the lab-bench white), classic layout, ivy
   accent (the life-sciences seed's first plate), and the
   warty-spots ornament reused from 369 — the specimen dermis
   re-read as PORES, which is what the instrument is. Fourth
   `plate` instance: apparatus unchanged, the proof renderer gains
   the `squiggle` grammar (a stepped ionic-current trace with one
   seeded window raised into the accent and given its base call).
   Price tag denominated in the run, not the cover: the flow cell
   is the ink.

   The artifact came first at
   artifacts/429-the-ink-is-the-cell.html — a six-stratum descent
   (bench → extraction → library → pore → basecall → folio) with
   the sample choice and basecall model carried down every
   stratum. What the reduction gives up: the descent itself (the
   site plate is one working bench, not six strata), the carried
   sample choice (buccal/coffee/RNA re-inking the floor), and the
   folio receipt as an operable floor — the spread keeps the
   mechanism, the economics, and the discipline in prose.

   Pre-press note: the adversarial fact pass caught the draft
   claiming the MinKNOW→Clair3 stack is “all open source” — false
   (MinKNOW is ONT-proprietary and free; Dorado is
   source-published under ONT’s licence; minimap2 and Clair3 are
   open outright). Corrected here and in the source brief in the
   same change.
   ────────────────────────────────────────────────────────────── */

import type { IssueRecord } from './index'

export const ISSUE_429: IssueRecord = {
  number: '429',
  month: 'MAR',
  year: '2027',
  feature: 'THE INK IS THE CELL',
  featureJp: 'インクが本体',
  price: '$1,100 · THE INK',
  tagline: 'MAGAZINE FOR CITY CODERS · 街のコーダーのために',

  coverStock: 'ivory',
  coverLayout: 'classic',
  coverOrnament: 'warty-spots',
  coverSeal: { label: 'SPECIMEN 00 · NO RUN YET', date: 'III·27' },
  accent: 'ivy',

  headline: {
    prefix: 'THE INK IS THE',
    emphasis: 'CELL',
    suffix: '.',
    swash: 'A $3,150 device sequences nothing out of the box. The flow cell is the ink — it expires, ships on ice, and dies as designed — and the economics of the palm-sized press are written entirely in consumables.',
  },
  coverDeck: 'The device is the cheap part. The ink is the decision.',

  contents: [
    { n: '001', en: 'The press and the ink', jp: '印刷機とインク', tag: 'MATERIALS' },
    { n: '002', en: 'A strand threads a pore', jp: '鎖が孔をくぐる', tag: 'MECHANISM' },
    { n: '003', en: 'Dies as designed', jp: '設計どおりに死ぬ', tag: 'CONSUMABLE' },
    { n: '004', en: 'The folio before the instrument', jp: '装置より先に台帳を', tag: 'DISCIPLINE' },
    { n: '005', en: 'Nothing bought', jp: '何も買っていない', tag: 'STATUS' },
  ],

  spread: {
    type: 'plate',
    proofStyle: 'squiggle',
    kicker: 'MATERIALS REVIEW · OXFORD NANOPORE MINION — FACTS READ 18 AUG 2026',
    title: 'THE INK IS THE CELL.',
    titleLines: ['THE INK', 'IS THE', 'CELL'],
    titleJp: 'インクが本体 — フローセルの経済',
    deck: 'Oxford Nanopore’s MinION puts a sequencing run on a kitchen table — USB-C to a laptop, reads filling in as they happen. The purchase brief says the device is not the decision. The flow cell is: it expires, it ships on ice, and it meters every page the press will ever print. A materials review, written before anything is bought.',
    byline: 'BY THE EDITORS · KERNEL.CHAT',
    stock: 'ivory',

    dossier: {
      kicker: 'THE INSTRUMENT · 器械',
      note: 'Store prices were read from the ONT US store on 2026-08-18. Run figures — pore counts, N50, read quality, POD5 size, and the run-cost dollars — are representative numbers from a third-party home-run ledger — Menon, 2026-05 — not ours: nothing has been bought and no run has been performed. The plate is this magazine’s drawing, not instrument telemetry.',
      items: [
        { label: 'INSTRUMENT', value: 'MINION MK1D · PALM-SIZED · USB-C TO A LAPTOP · DNA OR RNA' },
        { label: 'PRICE', value: 'PACK $5,150 · DEVICE ONLY $3,150 — ONT US STORE, READ 2026-08-18' },
        { label: 'THE INK', value: 'FLOW CELLS · EXPIRE · SHIP ON ICE · ~$1,100 PER LATER RUN' },
        { label: 'YIELD', value: '~30 Gb PER CELL · ~10X HUMAN GENOME · PROMETHION ~100 Gb, ~30X' },
        { label: 'STACK', value: 'MINKNOW FREE · DORADO SOURCE-PUBLISHED · MINIMAP2 + CLAIR3 OPEN SOURCE' },
        { label: 'STATUS', value: 'NOTHING BOUGHT · NO RUN PERFORMED · RUN FIGURES THIRD-PARTY — MENON, 2026-05' },
      ],
    },

    intro: [
      {
        heading: 'The press and the ink',
        headingJp: '印刷機とインク',
        paragraphs: [
          'Oxford Nanopore’s MinION is a sequencer the size of a palm, and the mechanism fits in a sentence: a single strand of DNA or RNA threads a protein pore, the ionic current wiggles as each base passes, and a laptop decodes bases from the squiggle in real time — you watch the run fill in instead of waiting for a lab to mail results back. On the US store, read 2026-08-18, the device alone is $3,150. Out of the box it cannot read a single base — no flow cell, no kit. A press, delivered without ink.',
          'Every publication learns this arithmetic eventually. The press is a one-time line; the paper and the ink are forever, and they — not the machine — set the price of a page. The MinION obeys the same law with the terms renamed. The page is a genome. The ink is the flow cell. The press is the box on the table.',
        ],
      },
      {
        heading: 'Dies as designed',
        headingJp: '設計どおりに死ぬ',
        paragraphs: [
          'The flow cell comes in DNA and RNA editions, ships on ice, and expires whether or not it is used. It also spends itself while it works: in the specimen figures — third-party, after Menon’s 2026-05 home-run ledger — a cell opens at 1,412 active pores and closes 72 hours later at 310. The decay is not a malfunction. It is the unit of account.',
          'This is why the brief’s sternest sentence is about shopping, not science. Menon’s rule: “Don’t buy them until you’re ready to run.” An unopened device on a desk costs nothing further. A flow cell on ice is already spending itself.',
        ],
      },
    ],

    plateKicker: 'PLATE No.4 — SPECIMEN MODEL · 標本模型',
    plateHint: 'DRAG OR ARROW-KEY A BLOCK TO REROUTE THE BENCH · PULL TO THREAD A NEW DETERMINISTIC STRAND',
    plateCaption: 'FIG. 1 — THE RUN, REDUCED TO A LEGIBLE PATH: A SAMPLE ENTERS THE PORE; THE CURRENT WIGGLES; A LAPTOP CALLS THE BASES; THE FOLIO FILES THE HASHES.',
    blocks: [
      { id: 'b1', label: 'BLOCK 01 · SAMPLE', labelJp: '検体', kind: 'text', prompt: '“Whole-genome long-read sequence of one buccal sample — a reading, not a diagnosis.”', x: 3, y: 36 },
      { id: 'b2', label: 'BLOCK 02 · THE PORE', labelJp: '細孔', kind: 'image', models: ['MINION MK1D · R10.4.1', 'DNA OR RNA'], x: 36, y: 4 },
      { id: 'b3', label: 'BLOCK 03 · THE SQUIGGLE', labelJp: '電流', kind: 'image', models: ['DORADO SUP · Q≥20 91% ◇', 'REAL-TIME READS'], x: 36, y: 56 },
      { id: 'b4', label: 'BLOCK 04 · THE FOLIO', labelJp: '台帳', kind: 'video', models: ['PROVENANCE-SUBSTRATE 0.1.1', 'SHA-256 EVERY STEP'], x: 70, y: 28 },
    ],
    wires: [
      { from: 'b1', to: 'b2' },
      { from: 'b2', to: 'b3' },
      { from: 'b3', to: 'b4' },
    ],
    runLabel: '★ THREAD THE STRAND',
    runAgainLabel: '★ THREAD AGAIN — 再読',
    plateNote: 'Plate No.4 is a deterministic editorial simulation drawn by this magazine. No sequencer is owned, no run has been performed, and the traces are not instrument telemetry: the squiggle grammar preserves the shape of a nanopore read — stepped current, one called window — while every line is generated only from the printed seed. The same seed draws the same strand. Store prices were read from the ONT US store on 2026-08-18; run figures marked ◇ are third-party representative — Menon, 2026-05. The ledger counts only your pulls, redraws, and rearrangements in this browser; reloading restores the standing plate. Nothing is sent or graded.',

    /* The ticker renders text-transform: uppercase, which would turn
     * Gb (gigabases) into GB (gigabytes) — units are spelled out here. */
    ticker: ['PACK $5,150', 'DEVICE ONLY $3,150', 'LATER RUN ~$1,100 ◇', 'RUN ONE ~$3,200–4,100 ◇', 'NEBNEXT ~$1,275 ◇ — 24 PREPS, 1 USED', '~30 GIGABASES PER CELL ◇ · ~10X GENOME', 'PROMETHION ~100 GIGABASES ◇ · ~30X', '1,412 → 310 PORES / 72 H ◇', 'N50 11.4 KILOBASES ◇', 'NOTHING BOUGHT'],
    tickerLabel: 'THE CONSUMABLES LEDGER · 消耗品台帳 — STORE PRICES READ 2026-08-18 · ◇ THIRD-PARTY, MENON 2026-05',
    catalogKicker: 'THE MATERIALS FILE, IN FOUR ENTRIES · 消耗品記録',
    catalog: [
      { n: '01', en: 'Expiry', jp: '期限', body: 'The flow cell is the ink, and the ink is perishable. It ships on ice, it expires on the shelf, and it dies while it works — the specimen figures, third-party from Menon, 2026-05, open a run at 1,412 active pores and close it at 310 after 72 hours. That is not a defect. That is the pricing model, and each later run costs about $1,100 — mostly the cell.' },
      { n: '02', en: 'Surplus', jp: '余剰', body: 'Kits are sized for labs, and a solo bench pays the lab price. The hidden line in the brief is the NEBNext Companion Module at about $1,275 — twenty-four preps bought, one used. Menon is blunt twice: “DNA quality matters more than quantity”, and library prep “is where most failures happen”. The surplus is not a discount opportunity. It is the cost of practicing a craft alone.' },
      { n: '03', en: 'Arithmetic', jp: '勘定', body: 'The Mk1D Pack is $5,150 with five cells and a kit; the device alone is $3,150 and prints nothing until a cell arrives. The pack is the right SKU only if five cells actually burn before they expire. Run one lands near $3,200–4,100 in reagents and bench on top of the device. One MinION cell yields ~30 Gb, roughly 10x a human genome; the 30x that clinical-grade variant calling asks for belongs to a PromethION cell at ~100 Gb.' },
      { n: '04', en: 'Provenance', jp: '来歴', body: 'The folio is four pages: claim, ledger, reading, colophon. Every step carries a SHA-256 — POD5, basecall, alignment, calls — and anyone holding the raw data re-derives every number. The stack that produces it runs free on the laptop the sample walks up to: MinKNOW closed but free, Dorado’s source published, minimap2 and Clair3 open outright.' },
    ],

    outro: [
      {
        heading: 'Your sample, your laptop, your ledger',
        headingJp: '自分の検体、自分の端末、自分の台帳',
        paragraphs: [
          'The shape of the machine matches the shape of the house. Local-first: the sample never leaves the kitchen table, and no lab mails results back — you watch the run fill in on your own screen. BYOK, translated into biology: your sample, your laptop, your ledger. And the pipeline from basecall to variant calls is inspectable — Dorado’s source is published, minimap2 and Clair3 are open outright — which means the audit is not a promise. It is a command anyone can re-run.',
          'The laptop is also the honest caveat. Menon recommends 64 GB of RAM or more and clocks basecalling in several hours on his M3 Ultra Studio; the M3 Max this issue was drafted on carries 36 — expect it to work, slower, and to be good for nothing else while it runs. One run writes roughly 98 to 100 GB of POD5, per the same third-party ledger. Local-first does not mean fast. It means the wait happens on your own bench, inside your own ledger, instead of inside someone else’s.',
        ],
      },
      {
        heading: 'The folio before the instrument',
        headingJp: '装置より先に台帳を',
        paragraphs: [
          'This magazine’s discipline is unchanged by the change of substrate: count what gets read, cut what doesn’t, file the audit in public. Pointed at biology, that discipline has a name — the run folio. Specimen 00 already exists, drafted from the purchase brief with every measurement marked as borrowed: an N50 of 11.4 kb, 1,412 pores fading to 310 across 72 hours, 91% of reads at Q≥20 — representative values from published home runs, after Menon, 2026-05. The hashes read computed at run, because there has been no run.',
          'That order is the whole argument. The folio is sellable in that state; the instrument is justified by the first paid folio — never the other way round. Nothing has been bought. No run has been performed. When the first page is ready — a named client, a written experiment, a folio waiting to be filled — then, and only then, buy the ink.',
        ],
      },
    ],
    pullQuote: { text: 'The cell dies as designed. The ledger does not.', attribution: 'THE INK IS THE CELL · ISSUE 429' },
    references: {
      kicker: 'THE SOURCE FILE · 出典',
      note: 'Store pages read 2026-08-18; the run-cost and yield ledger is third-party (Menon, 2026-05) and marked ◇ wherever it appears. The in-house purchase brief and Run Folio Specimen 00 are filed in this repository.',
      items: [
        { authors: 'Oxford Nanopore Technologies', year: '2026', title: 'MinION Mk1D — US store product page', journal: 'store.nanoporetech.com/us/minion.html · read 2026-08-18' },
        { authors: 'Oxford Nanopore Technologies', year: '2026', title: 'PromethION 2 — US store product page', journal: 'store.nanoporetech.com/us/p2.html · read 2026-08-18' },
        { authors: 'Menon', year: '2026', title: 'Home genome sequencing guide', journal: 'themenonlab.blog · 2026-05-26 · third-party cost ledger' },
        { authors: 'kernel.chat', year: '2026', title: 'Nanopore sequencer — purchase brief + Run Folio Specimen 00', journal: 'docs/hardware/nanopore-sequencer.md · filed 2026-08-18' },
      ],
    },
    signoff: '街のコーダーたちへ — price the ink before the press, file the ledger before the run, and never buy a cell without a page waiting for it.',
  },

  audit: {
    drafted: 'artifact-first editorial build · Claude Fable 5 · 19 Aug 2026',
    verified: 'ONT US store prices (read 2026-08-18) + Menon 2026-05 third-party ledger; adversarial fact / Japanese / voice pass pre-press; artifact edition filed at artifacts/429-the-ink-is-the-cell.html',
    adherence: 'fourth `plate` instance — `squiggle` proof grammar added, apparatus unchanged; specimen register disclosed on cover seal, dossier, plate, and ticker',
    readCut: 'the draft’s “all open source” stack claim caught pre-press and corrected here and in the source brief; benchmark talk cut',
    pressed: 'III·27 · specimen register — nothing bought, no run performed',
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
