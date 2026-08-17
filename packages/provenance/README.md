# provenance-substrate

**The model proposes. Deterministic code disposes. A human signs the exact bytes. Every step is hash-chained.**

A small, dependency-free Python library — with a language-neutral conformance
suite — for making AI-assisted work *checkable* rather than merely plausible.
It began as the ledger substrate in
[`@kernel.chat/kbot-finance`](../kbot-finance) (where the AI reads an invoice
but may never post the number) and is here generalized to the places academia
is currently forced to trust a model's word:

| Wedge | The model proposes… | …the disposer is… | …and the human who signs is |
|---|---|---|---|
| `finance` | a reading of a source document | arithmetic + the bank feed | an accountant |
| `lean` | a proof | the Lean kernel | a mathematician |
| `claims` | a number in a manuscript | re-execution of the computation that produced it | the corresponding author |
| `repro` | how to reproduce a paper | actually running it, judged against tolerances | the reproducer |
| `bench` | an answer to a quantitative question | a deterministic recompute — the substrate itself, measured | — (a benchmark) |
| `review` | a peer review, with AI contribution disclosed | disclosure rules + a signed review chain | the editor |

Same primitives everywhere: canonical JSON (byte-compatible with the
TypeScript reference, including JavaScript number formatting), SHA-256
content-addressed request envelopes, HMAC-signed approval tokens bound to the
exact summary line the human read, and an append-only hash chain. Nothing in
the package reads a clock or a random source on its own; every run is a replay.

## Install

```bash
pip install provenance-substrate
```

Python ≥ 3.10, no runtime dependencies. Works offline (HPC-friendly).

## Prove it is the same substrate

The finance v1 conformance vectors are vendored. Running them is the claim:

```bash
provsub conformance finance-v1
# 143/143 passed; suite be4cdbe3e0a53bbd… manifest ok
```

The academic v1 suite (Lean, claims, repro, bench, review kinds) is generated
from this reference implementation and checked in CI:

```bash
provsub conformance academic-v1
provsub conformance --check     # regenerate in memory, diff against disk
```

Quote the `suite_hash` when you claim conformance. A port in any language that
reproduces `expected` from `input` for every vector of a kind conforms to that
kind. See [`ARCHITECTURE.md`](./ARCHITECTURE.md) and
[`docs/conformance.md`](./docs/conformance.md).

## Sixty-second tour

```python
from provsubstrate.core import ContentAddressedRequest, Approver, ApprovalRequest, verify_approval, AppendOnlyAuditLog

# 1. The model's reading is a claim; the envelope is the replay key.
req = ContentAddressedRequest(
    operation="claims.verify", engine_version="claim-graph@0.1.0", schema_hash="…",
    inputs={"claim": {"value": 3.7, "unit": "s"}, "computation": {"command": ["python", "mean.py"]}},
    data_as_of="2026-08-17T00:00:00.000Z",
)
h = req.request_hash()

# 2. A deterministic disposer re-runs the computation (see provsubstrate.claims).
# 3. The human signs the exact line they read, bound to h.
summary = "Attest 1 claim: mean = 3.7 s (observed 3.7, confirmed) request " + h[:12]
tok = Approver("pi.ada", b"secret").approve(ApprovalRequest(h, summary, "session-1", "claims.attest"), "2026-08-17T12:00:00.000Z")
assert verify_approval(tok, {"pi.ada": b"secret"}, ApprovalRequest(h, summary, "session-1", "claims.attest")).ok

# 4. Everything lands in a hash chain an auditor can replay.
log = AppendOnlyAuditLog("audit.jsonl", clock=lambda: "2026-08-17T12:00:01.000Z")
log.append("approval_granted", "claims.attest", "session-1", {"request_hash": h}, approver="pi.ada")
assert log.verify().ok
```

Wedge-specific quick starts: [`docs/finance.md`](./docs/finance.md),
[`docs/lean.md`](./docs/lean.md), [`docs/claims.md`](./docs/claims.md),
[`docs/repro.md`](./docs/repro.md), [`docs/bench.md`](./docs/bench.md),
[`docs/review.md`](./docs/review.md).

## Command line and agents

```bash
provsub finance post claim.json bank.json          # stops at the gate: prints the request hash + summary line to sign
provsub lean check Basic.lean --toolchain leanprover/lean4:v4.12.0
provsub claims verify provenance-manifest.json --workdir .
provsub repro judge target.json attempt.json --workdir .
provsub bench run --responder oracle
provsub review check submission.json --chain chain.json
provsub approve --request-hash H --summary "..." --session-id S --materiality lean.record \
                --approver-id you --secret-file ~/.provsub/secret --approved-at T   # the HUMAN step; never an agent's
provsub audit verify audit.jsonl
provsub mcp                      # stdio MCP server exposing the verdict-producing operations to agents
```

Every wedge has `check`/`verify`/`judge` (verdict + the line to sign) and
`record`/`post`/`attest` (needs `--approval tok.json` from `provsub approve`
and a trust set via `--trust ID=SECRET_FILE`). Nothing reads a clock: pass
`--data-as-of`, `--now`, `--approved-at`.

The MCP server is how a model uses this: it can *request* a verdict inside an
envelope (`finance_reconcile`, `finance_prepare_post`, `lean_check`,
`lean_prepare`, `claims_verify`, `claims_badge`, `repro_judge`,
`repro_dataset_manifest`, `bench_score`, `bench_run`, `bench_taskset`,
`review_check`, `review_chain_verify`, plus the core hash and chain tools); it
cannot mint an approval, and nothing records or posts through MCP.

## What this is not

It does not make a model's claim true. It makes the claim checkable,
replayable, and signed — and it puts the model's mistakes on the record
instead of in the paper, the ledger, or the proof.

## Related work

CODECHECK (independent re-execution with a signed certificate), in-toto and
SLSA (signed supply-chain attestations), W3C PROV, RO-Crate and
nanopublications (provenance description), C2PA (content credentials), RFC 8785
JCS (canonical JSON), Lean 4 / mathlib (the kernel as disposer). Each supplies
one piece; this package composes them into a single, conformance-tested
discipline in which a model's proposal is a first-class, hash-addressed object
that a deterministic engine must confirm and a human must sign. See
[`paper/paper.md`](./paper/paper.md).

## Citing

See [`CITATION.cff`](./CITATION.cff). A Zenodo DOI is minted per release from
[`.zenodo.json`](./.zenodo.json).

## License

MIT.
