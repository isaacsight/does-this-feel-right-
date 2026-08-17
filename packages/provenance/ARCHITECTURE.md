# provenance-substrate — architecture and conventions

One rule, six wedges, one conformance discipline.

**The rule.** The model proposes; deterministic code disposes; a human signs
the exact bytes; every step is hash-chained. Nothing in this package reads a
clock or a random source on its own — timestamps and seeds are always passed
in — so any run is a replay.

## Layout

```
src/provsubstrate/
  core/          canonical JSON (JS-byte-compatible), envelopes, HMAC approval, hash chain
  conformance/   runner + core-kind handlers + vendored finance v1 vectors + academic v1 vectors
  finance/       port of the kbot-finance ledger substrate (all 13 kinds pass finance v1)
  lean/          proof ledger: model proposes a proof, the Lean kernel disposes, a mathematician signs
  claims/        claim graph: every number in a paper hash-linked to the computation that produced it
  repro/         reproducibility ledger: paper + repo in, attempted reproduction out, signed report, dataset export
  bench/         quantitative-hallucination benchmark: tasks, scoring, results envelopes
  review/        peer-review provenance: signed review chains, AI-contribution disclosure
  cli.py         `provsub` command
  mcp_server.py  stdio MCP server exposing the same operations to agents
```

## Shared shape of every wedge

Each wedge module exposes the same five things:

1. **A claim type** — the model's proposal, always carrying `model_lineage`
   (`[{model, version}]`) and the `doc_hash` of what it read.
2. **A disposer** — a pure or explicitly-stateful function that returns a
   structured verdict. Never a model. (Lean kernel, re-execution, reconciler.)
3. **An envelope** — `ContentAddressedRequest(operation, engine_version,
   schema_hash, inputs, data_as_of)`; `request_hash()` is the replay key.
4. **A gate** — `ApprovalRequest(request_hash, summary, session_id,
   materiality)` where `summary` is the exact human-readable line the human
   signs, and a `verify_approval` call before anything is committed.
5. **An audit sequence** — a fixed, ordered list of `action` names appended to
   an `AppendOnlyAuditLog`. Conformance vectors pin the sequence.

And, for conformance, each wedge exposes:

- `conformance_cases() -> list[{kind, id, description, input}]` — the fixed case catalogue (no clocks, no randomness).
- `compute_expected(kind, input) -> expected` — from the reference behaviour.
- `CONFORMANCE_HANDLERS: dict[kind, handler(input, expected) -> (ok, detail)]`.

`python -m provsubstrate.conformance.generate` regenerates
`conformance/vectors_academic_v1/` and its manifest; `--check` diffs in
memory against disk. Drift means either the reference changed (bump the
format version, say why) or something is non-deterministic (a bug).

## Fixed constants (academic v1)

| Constant | Value |
|---|---|
| `data_as_of` | `2026-08-17T00:00:00.000Z` |
| `approved_at` | `2026-08-17T12:00:00.000Z` |
| `session_id` | `academic-conformance-session` |
| trusted approver | `pi.ada` / secret `academic-approver-secret-0001` (UTF-8) |
| untrusted signer | `student.bob` / secret `not-in-the-trust-set` |
| model lineage | `[{"model": "local-27b", "version": "conformance"}]` |

Secrets are test fixtures. Never real.

## Vocabulary

claim · disposer · verdict · envelope · request hash · gate · summary line ·
approval token · audit chain · suite hash. Never "AI decides", never
"auto-approve".
