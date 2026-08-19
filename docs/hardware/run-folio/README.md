<p align="center"><sub>KERNEL PRESS · RUN FOLIO · SPECIMEN 00 · AUGUST 2026</sub></p>

<h1 align="center">A sequencing run,<br>filed in public.</h1>

<p align="center"><em>The Run Folio is the four-page record we hand you after a nanopore sequencing run: what was claimed, what was measured, what it means, and what it cost. Every number on the ledger page can be re-derived by anyone holding the raw data.</em></p>

<p align="center"><sub>公開された配列決定記録 · one run, one folio</sub></p>

---

> **This is Specimen 00.** No run has been performed. Fields marked `◇` show
> the *shape* of a real folio using typical figures from published home
> nanopore runs (Menon, 2026-05); hashes read `computed at run`. A client
> folio replaces every `◇` with a measurement and every `computed at run`
> with a SHA-256.

<br>

## I. The claim

<table>
<tr><td><sub>WHAT WAS ASKED</sub></td><td><strong>Whole-genome long-read sequence of one human buccal sample, sufficient for a targeted-panel reading; not sufficient for clinical-grade variant calling.</strong></td></tr>
<tr><td><sub>FOR</sub></td><td>◇ Client name · engagement reference</td></tr>
<tr><td><sub>SAMPLE</sub></td><td>◇ Buccal swab, collected by the client, extracted same day (Monarch gDNA)</td></tr>
<tr><td><sub>DATELINE</sub></td><td>◇ Los Angeles · YYYY-MM-DD → YYYY-MM-DD (72 h run)</td></tr>
<tr><td><sub>WHAT THIS FOLIO DOES NOT SHOW</sub></td><td>Diagnosis. Ancestry claims. Anything requiring &gt;15x coverage. Anything the ledger below cannot reproduce.</td></tr>
</table>

<br>

## II. The ledger

Everything on this page is machine-checkable. The reproduction bundle
(`ledger.json`, `commands.sh`, checksums) ships with the folio; the raw
reads ship on the client's own drive and never enter this repository.

| # | Step | Tool · version | Input hash | Output hash |
|---|---|---|---|---|
| 01 | Flow-cell check | MinKNOW ◇ 24.x · cell `FAX·····` · ◇ 1,412 active pores at start | — | `computed at run` |
| 02 | Library prep | SQK-LSK114 (ligation) · NEBNext Companion · lot ◇ | — | prep sheet, signed |
| 03 | Sequencing | MinION Mk1D · R10.4.1 · ◇ 72 h · ◇ 30.1 Gb raw | — | POD5 set: `computed at run` (◇ 98 GB) |
| 04 | Basecalling | Dorado ◇ 0.9 · `dna_r10.4.1_e8.2_400bps_sup` · Apple M3 Max | POD5 hash | FASTQ: `computed at run` |
| 05 | Alignment | minimap2 ◇ 2.28 · `-ax map-ont` · GRCh38 | FASTQ hash | BAM: `computed at run` |
| 06 | Variant calls | Clair3 ◇ 1.0 · ONT R10 model | BAM hash | VCF: `computed at run` |
| 07 | Ledger seal | provenance-substrate ◇ 0.1.x | steps 01–06 | `ledger.json`: `computed at run` |

**Yield, as measured**

| Metric | ◇ Specimen | What it tells you |
|---|---|---|
| Raw bases | 30.1 Gb | one MinION cell, typical |
| Read N50 | 11.4 kb | long reads; intact DNA |
| Mean depth (GRCh38) | 9.7x | a *reading*, not a diagnosis |
| Q ≥ 20 reads | 91% | sup basecalling |
| Pores at start → 24 h → end | 1,412 → 880 → 310 | the cell dying, as designed |

<br>

## III. The reading

*Written in plain register. No "may indicate". Where the data is thin, it says so.*

◇ At ~10x depth this run supports confident calls across the targeted
panel regions and a genome-wide sketch; it does not support clinical
interpretation, which begins at ~30x (one PromethION cell, or three
MinION cells pooled). Read length (N50 11.4 kb) shows the extraction
preserved DNA integrity — the step where most first runs fail. The
pore-decay curve is normal for a 72 h run; a wash-and-reload could have
recovered ~5 Gb more and was not attempted.

What we would do next, and what it would cost, is on the last page.

<br>

## IV. The colophon

| | |
|---|---|
| Ran by | ◇ Isaac Hernandez, kernel.chat |
| Hardware | MinION Mk1D · Apple M3 Max, 36 GB · external NVMe |
| Cost of this run | ◇ flow cell $1,050 · kit share $102 · NEBNext share $53 · extraction $150 · time 3 h bench + 72 h run + 6 h basecall |
| Cost of the next run | ◇ ~$1,100 (the flow cell is the ink) |
| Reproduce it | `git clone` the bundle · `sh commands.sh` · compare hashes to `ledger.json` |
| Filed | this folio, this repository, in public |

<p align="center"><sub>★ &nbsp; count what gets read · cut what doesn't · file the audit in public</sub></p>

---

<sub>Specimen 00 was assembled 2026-08-18 without hardware, from the purchase brief in
<a href="../nanopore-sequencer.md">docs/hardware/nanopore-sequencer.md</a>. The designed edition is
<a href="./index.html">index.html</a> in this folder.</sub>
