# Nanopore sequencer — purchase brief (MinION Mk1D vs PromethION 2)

**Status:** OPEN. Nothing bought. This is the file to read before spending.
**Filed:** 2026-08-18
**Sources:** https://store.nanoporetech.com/us/minion.html and
https://store.nanoporetech.com/us/p2.html (US store, both checked 2026-08-18);
third-party cost ledger: Menon, "Home genome sequencing guide",
https://themenonlab.blog/blog/home-genome-sequencing-guide (2026-05-26)

## What it is

Oxford Nanopore's palm-sized DNA/RNA sequencer. USB-C to a laptop; the
laptop runs MinKNOW (device control) and Dorado (basecalling). Real-time
reads: you watch the run fill in as it happens rather than waiting for a
lab to mail results back. Takes MinION flow cells and, with the Flongle
adapter, cheaper low-throughput Flongle cells.

## Price (US store, 2026-08-18)

| SKU | USD | Included |
|---|---|---|
| MinION Mk1D Pack | **$5,150** | device, Control Expansion Kit, Flow Cell Wash Kit, 12 mo standard support, **5x** MinION/GridION flow cells (DNA or RNA), 1x sequencing kit (configurable) |
| MinION Mk1D device only | **$3,150** | device, 1 yr warranty, 1 yr support. No flow cells, no kit — cannot sequence anything out of the box |

Flow-cell and kit prices are not shown on the product page; they appear at
configuration. Do not budget from memory — capture the configured cart
total here before deciding.

**What a run actually costs (Menon, 2026-05, MinION whole-genome from a
cheek swab; his numbers, not ONT list):**

| Line | USD | Note |
|---|---|---|
| R10.4.1 flow cell | 900–1,200 | the ink; expires; ships on ice |
| Ligation kit SQK-LSK114 | ~610 | 6 preps' worth of enzymes for one run |
| NEBNext Companion Module | ~1,275 | **the hidden line** — 24 preps bought, 1 used |
| Monarch gDNA extraction kit | ~150 | |
| Wash kit | ~17 / wash | reload a part-spent cell |
| Bench kit (pipettes, heat block, mini centrifuge, vortex, mag rack) | 200–800 | one-time |
| Consumables (LoBind tubes, tips, ethanol, PBS) | ~50 | |
| **Reagents + bench for run one** | **~$3,200–4,100** | sum of the lines above; his headline is "$2,000–12,000 including sequencer" |
| **Each later run** | **~$1,100** | mostly the flow cell |

So the $5,150 Pack's 5 cells + 1 kit are worth roughly $5–7k of that
table at his prices; the pack is the right SKU if you will actually run
five cells before they expire, and a trap if you won't. The
device-only $3,150 SKU plus one cell, one kit, and the NEBNext module
lands near $6.2k for run one — same money, one cell instead of five.

Yield: MinION ~30 Gb/cell (~10x human genome; enough for targeted panels
via adaptive sampling, thin for clinical-grade variant calling);
PromethION ~100 Gb/cell (~30x, the variant-calling standard).

## Step-up option: PromethION 2 (P2)

Isaac sent the P2 store page the same day. Facts as of 2026-08-18:

| Model | Public US price | What it is |
|---|---|---|
| **P2 Integrated (P2i)** — the page at `/us/p2.html` | **Not listed.** Store says "Talk to a specialist"; 1 yr support, 1 yr warranty, remote install call included; status "Released" (out of Early Access), lead times "subject to availability" | Two PromethION flow-cell positions, onboard GPU compute, touchscreen. Self-contained; no host computer needed |
| **P2 Solo** | **No direct store page** (`/us/p2-solo.html` and `/us/promethion-2-solo.html` both 404). Menon (2026-05) quotes **~$10,455** | Same two positions, no compute — needs a GPU host you supply |

**Prices not confirmed with ONT:** P2 Solo ~$10.5k (Menon, 2026-05, third
party); P2i has historically been quoted in the $40–50k range
(unverified). Get a written quote before any of this moves.

Why it matters here:

- **Throughput class.** A PromethION flow cell yields roughly 4–7x a
  MinION cell (tens to 100+ Gb vs ~10–30 Gb). That is human-genome
  territory per cell. MinION is bacterial/amplicon/small-genome
  territory. Which class you need is decided by the *first experiment*,
  not by the toy.
- **P2 Solo couples directly to the inference-box plan.** The RTX 5090
  headless Ubuntu build (ceiling $2,500, nothing bought) is close to
  what P2 Solo wants as a host: an NVIDIA GPU with lots of VRAM, 64 GB+
  RAM, and fast NVMe for the POD5 stream. That turns the inference box
  from "a nice-to-have for local models" into "the required half of a
  sequencing rig" — but it also means the *combined* bet is roughly
  $2.5k (box) + P2 Solo quote + PromethION flow cells, which are several
  hundred dollars each and, like MinION cells, expire.
- **The M3 Max cannot host P2 Solo.** MinKNOW's PromethION path needs
  CUDA. So MinION = laptop; P2 = box first, sequencer second.

**Recommendation as of this filing:** if a sequencer is bought at all
this year, it is the **MinION Mk1D Pack ($5,150)**, because it needs no
second machine, no quote cycle, and its cells are cheap enough to burn
while learning. Log the P2 quote when it arrives; revisit only if the
first three MinION runs are yield-limited rather than skill-limited.

## What gets built to share with a client

The box is not the product. The product is the **run folio**: a
client-facing, provenance-verified sequencing report that kernel.chat
already knows how to make — a KERNEL PRESS artifact, not a lab PDF.

**Deliverable: `Run Folio` (one per sequencing run)**

1. **The claim page.** One sentence of what was measured, for whom, on
   what date, and what it does *not* show. Magazine vocabulary: issue,
   dateline, colophon.
2. **The ledger.** provenance-substrate output: SHA-256 of every POD5,
   Dorado/minimap2/Clair3 versions and command lines, flow-cell ID and
   pore-count at start, yield curve, N50, coverage histogram, VCF hash.
   Machine-checkable; anyone with the raw data can re-run and get the
   same hashes.
3. **The reading.** The human layer — what the coverage supports, which
   calls are confident, what would need a PromethION cell to settle.
   Written in the house register: no hedging theatre, no "may indicate".
4. **The colophon.** Who ran it, on what hardware, what it cost, how long
   it took. The audit filed in public, per the discipline.

Rendered two ways: a signed PDF/HTML folio in the e-ink editorial system
(same pipeline as the client quoting engine and Kéan collateral) and a
zip of the ledger + scripts so the client's own bioinformatician can
reproduce it. Never the raw reads in the repo — hashes only.

**Who the client is** (this decides MinION vs P2):

| Client | What they buy | Which sequencer |
|---|---|---|
| Small biotech / academic lab with no bioinformatics staff | reproducible-pipeline setup + folio template they run themselves | MinION or their own box; we sell the substrate, not the sequencing |
| Provenance-conscious buyers (regulated, IP-sensitive) | the ledger format itself: "prove this run happened as stated" | hardware-agnostic — the pitch is the substrate |
| Individual / founder wanting their own genome as an artifact | a one-off 10x MinION run + folio, or 30x via a PromethION service | MinION for the artifact; P2 only if the coverage is the point |
| Coffee / food clients (Kéan, Stereoscope) | origin or contamination fingerprinting as a marketing-grade folio | MinION; amplicon runs, cheap Flongle cells |

**Build order (all $0 until the last step):**

- [ ] `provenance-substrate` recipe: public POD5 -> Dorado -> minimap2 ->
      Clair3 -> ledger JSON. Runs on the M3 Max today.
- [ ] Folio template in the design system: claim / ledger / reading /
      colophon spreads. Render once from the public-data run.
- [x] Specimen folio built 2026-08-18: `docs/hardware/run-folio/`
      (README.md renders on GitHub; index.html is the designed edition).
      Send that, not a deck. Publish as a kernel.chat issue once a real
      run replaces the ◇ specimen values.
- [ ] Only then price a real run for a named client, and only then buy
      the box.

The last row is the whole argument for the MinION over the P2: the
folio is sellable before the sequencer exists, and the sequencer is
justified by the first paid folio, not the other way round.

## Why it belongs in this repo at all

kernel.chat's thesis is *count what gets read; file the audit in public;
keep the manuscripts in the drawer.* A sequencer is the same discipline
pointed at biology: an instrument that produces a public, reproducible
ledger of what was actually measured.

Concrete lanes, ranked by how well they pay for the box:

1. **provenance-substrate, real instrument data.** The substrate
   (github.com/isaacsight/provenance-substrate, v0.1.1 on PyPI, Zenodo DOI
   10.5281/zenodo.21984095) currently proves claims/repro/bench on
   synthetic and software artifacts. A MinION run is a perfect real-world
   test object: raw POD5 -> Dorado basecall -> FASTQ -> claim, every step
   hashable, every step re-runnable on the M3 Max. That is the JOSS
   reviewer's "does this work on real data" question answered with a
   $5,150 instrument instead of a collaborator's goodwill.
2. **Editorial.** An issue on the instrument itself (the flow cell as a
   consumable that dies; the ledger of a run; what "real-time" means when
   the reads arrive faster than you can read them). Fits the magazine's
   grammar; the audit trail (run reports, yield curves) ships as the
   monument.
3. **Bio-research tooling for kbot.** kbot already has the bio-research
   plugin (bioRxiv, PubMed, ChEMBL, ClinicalTrials). Local sequence data
   gives it something to *act on* rather than only read about — a
   local-first, BYOK, $0-inference bio pipeline is on-thesis.
4. **Channel.** The instrument on the desk is a film subject in its own
   right; the archive-footage lane already covers the history of
   sequencing.

## Why not (state the case against before buying)

- **Consumables, not capex, are the cost.** Flow cells ship on ice and
  expire; Menon's rule: "Don't buy them until you're ready to run." An
  idle box burns money. If there is no run scheduled for the first 30
  days after delivery, the purchase is early — and the 5-cell Pack is
  the wrong SKU.
- **Wet lab.** Sequencing needs extracted, *intact* DNA. Bench kit
  $200–800 one-time plus ~$2k of reagents for run one (table above),
  and a place to keep it. Menon: "DNA quality matters more than
  quantity" — rough handling fragments it and shortens reads — and the
  ~3 h library prep "is where most failures happen." Expect the first
  run to be a practice run.
- **Reagent waste is structural.** Kits are sized for labs: 6–24 preps
  bought, 1 used, then they expire. Solo operation pays the lab price
  per run.
- **Same wallet as the inference box.** The RTX 5090 headless build has a
  $2,500 ceiling and nothing bought either. Both are hardware bets during
  a job-search month; only one should move first, and it should be the
  one with a scheduled first job.
- **Runs need attention.** A 24–72 h run is not fire-and-forget; the first
  few will eat evenings.

## Compute check (this machine)

- MinKNOW runs on macOS Apple Silicon; Dorado has a Metal build. Menon
  recommends M3+ with **64 GB+ RAM**; his M3 Ultra Studio basecalls a
  MinION run in "several hours", an NVIDIA GPU ~5x faster. This M3 Max
  has 36 GB — expect it to work but slower, and to be unusable for
  anything else while it runs. Verify against Dorado's current minimum
  before buying.
- Storage: ~100 GB per run of POD5. External SSD for raw data; the repo
  gets hashes and reports, never the reads.
- Downstream stack runs free end to end: MinKNOW (ONT proprietary, free
  with the device) -> Dorado (source-published under ONT's licence) ->
  minimap2 -> Clair3 or PEPPER-Margin-DeepVariant -> VCF (those last
  open source outright). Every step is a provenance-substrate step.
  (Corrected 2026-08-19 — an earlier line here called the whole stack
  "all open source"; MinKNOW is not, and Dorado's licence is ONT's own.)
- The inference box (if built) would basecall faster with `dorado` on
  CUDA, but it is not required. Do not couple the two purchases.

## Decision gates (all must be true before checkout)

- [ ] A first experiment is written down: sample, extraction method,
      kit, expected yield, what claim it tests. Filed next to this doc.
- [ ] Configured cart total captured here (pack + kit + flow cells).
- [ ] Wet-lab kit list priced (start from Menon's table above) and a
      bench identified.
- [ ] provenance-substrate has a stub pipeline for POD5 -> FASTQ -> claim
      that runs on a public nanopore dataset first ($0, no hardware).
- [ ] Explicit OK from Isaac on the spend (never buy on an agent's say-so).
- [ ] (P2 only) written quote captured; inference box actually built and
      basecalling a public POD5 set before the P2 order is placed.

## Alternatives to try first ($0)

- Public nanopore data (ENA/SRA POD5 sets, ONT's own sample data) exercises
  the entire software pipeline and the substrate without a box.
- Flongle-only pricing: if a Flongle adapter + Flongle cells cover the
  first experiments, the device-only SKU plus adapter may beat the pack.
  Price it at configuration.

## Log

- 2026-08-18 — Filed. MinION prices captured from the US store. P2 page
  checked: no public price, P2 Solo has no store page. Nothing bought.
- 2026-08-18 — Folded in Menon's home-WGS cost ledger (2026-05): first
  run ~$3–4k in reagents and bench kit on top of the device, ~$1.1k per later run, NEBNext
  module is the hidden $1,275 line, 64 GB+ RAM recommended for basecalling.
