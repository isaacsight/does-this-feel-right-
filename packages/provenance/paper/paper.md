---
title: 'provenance-substrate: a conformance-tested discipline for AI-assisted work in which the model proposes, deterministic code disposes, and a human signs'
tags:
  - Python
  - provenance
  - reproducibility
  - formal verification
  - Lean 4
  - peer review
  - AI safety
authors:
  - name: Isaac Hernandez
    orcid: 0000-0000-0000-0000
    affiliation: 1
affiliations:
  - name: kernel.chat, United States
    index: 1
date: 17 August 2026
bibliography: paper.bib
---

# Summary

Large language models now read the receipts, draft the proofs, extract the
numbers, and write the reviews. What they produce is fluent and frequently
correct, and there is no general mechanism by which a reader can tell which
outputs were checked and which were merely asserted. `provenance-substrate`
is a dependency-free Python library, and a language-neutral conformance
suite, that imposes one rule wherever a model touches a result: **the model's
output is a claim; a deterministic engine must confirm it; a human signs the
exact bytes; and every step is hash-chained.** The same four primitives —
canonical JSON, content-addressed request envelopes, HMAC-signed approval
tokens bound to the summary line the human read, and an append-only hash
chain — are instantiated as six *wedges*: double-entry ledgers (the reference
domain), Lean 4 proofs [@moura2021lean], numeric claims in manuscripts,
whole-paper reproductions, a quantitative-hallucination benchmark, and
peer-review provenance with disclosed AI contribution.

Conformance is proved by vectors, not prose. The finance v1 suite (143
vectors) is vendored from the TypeScript reference implementation
[@kbotfinance] and passes byte-for-byte; the academic v1 suite is generated
from this implementation and regenerated in CI. An implementation in any
language that reproduces `expected` from `input` for every vector of a kind
conforms to that kind and quotes the suite hash.

# Statement of need

Reproducibility infrastructure describes provenance (W3C PROV [@prov],
RO-Crate [@rocrate], nanopublications [@nanopub]) or certifies re-execution by
a human (CODECHECK [@codecheck]); software supply chains sign build steps
(in-toto [@intoto], SLSA); media carries content credentials (C2PA); and the
Lean kernel decides proofs [@mathlib]. Closest in spirit, deterministic integrity gates for LLM-assisted
clinical manuscripts [@nam2026gates] exact-match extracted claims against a
manifest-locked analysis table in one domain. Each supplies one piece. None treats a
*model's proposal* as a first-class, hash-addressed object that a
deterministic engine must confirm and a human must sign before it enters the
record, and none ships a conformance suite so that a second implementation can
demonstrate identical behaviour. As AI-assisted analysis becomes routine in
laboratories, in formalization efforts, and in editorial workflows, the
question a referee or auditor needs answered is not "was a model used?" but
"which of these results were confirmed by something that cannot be
sweet-talked, and who signed?" `provenance-substrate` makes that question
answerable by construction, offline, on a laptop or a cluster, without a
service to trust.

# Design

*Canonical JSON.* RFC 8785 [@jcs] simplified: sorted keys, JavaScript number
formatting reproduced from ECMA-262 (fuzzed against V8 on 10^3 doubles with
zero mismatches), `JSON.stringify` string escaping. This is the foundation of
byte-identical hashing across languages.

*Envelopes.* `request_hash = sha256(canonical({operation, engine_version,
schema_hash, inputs, data_as_of}))` is the replay key. Identical hash,
identical result.

*Gates.* An approval token is HMAC-SHA256 over the canonical
`{approved_at, approver_id, materiality, request_hash, session_id, summary}`;
verification refuses on any field mismatch, unknown approver, wrong secret, or
altered timestamp, and says which.

*Chains.* `self_hash = sha256(canonical(entry without self_hash))`, `prev_hash`
links, sixty-four-zero genesis; tampering with entry *n* breaks verification
at *n*.

*Wedges.* Each exposes a claim type carrying model lineage and the hash of
what was read; a disposer (kernel, re-executor, reconciler) that is never a
model; rules-as-code that all run with reason codes; a fixed human-readable
summary line; and a fixed, ordered audit-action sequence pinned by vectors.
Nothing reads a clock or a random source on its own.

*Agents.* The library ships a stdio MCP server so an agent can *request* a
verdict inside an envelope; it cannot mint one.

# Acknowledgements

The ledger substrate and finance v1 conformance vectors originate in
`@kernel.chat/kbot-finance`.

# References
