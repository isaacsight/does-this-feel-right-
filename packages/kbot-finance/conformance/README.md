# Ledger substrate conformance vectors — format v1

> **Suite hash:** see [`vectors/v1/manifest.json`](./vectors/v1/manifest.json) → `suite_hash`.
> That one number identifies this exact suite. Quote it when you claim conformance.

This directory is the standard. Not the prose in the package README — the
vectors. An implementation of the ledger substrate, in any language, on any
ledger, conforms to a *kind* if it reproduces `expected` from `input` for
every vector of that kind. Hashes and signatures must match byte-for-byte;
structured results must be JSON-equal after canonicalization.

The vectors are **generated from the reference implementation** by
[`src/conformance/generate.ts`](../src/conformance/generate.ts) from a fixed
case catalogue ([`src/conformance/cases.ts`](../src/conformance/cases.ts)).
No clocks, no randomness, no host dependence: `npm run conformance:check`
regenerates in memory and diffs against disk. If it drifts, either the
reference behaviour changed (bump the format version and say why in the
commit) or something is non-deterministic (a bug — fix it).

## Layout

```
conformance/
  README.md                 this file
  vectors/v1/
    manifest.json           per-file sha256 + suite_hash + pinned reference versions
    <kind>/<id>.json        one vector per file
```

Every vector:

```json
{
  "format_version": 1,
  "kind": "reconcile",
  "id": "ambiguous_two",
  "description": "…",
  "input": { … },
  "expected": { … }
}
```

## Kinds

| Kind | Pins | Comparison |
|---|---|---|
| `canonicalize` | Canonical JSON (sorted keys, shortest round-trip numbers, JSON string escaping) and its SHA-256 | exact string |
| `source_document` | SHA-256 over raw source-document bytes; byte length | exact |
| `claim_shape` | Structural validation of an extraction claim; sorted error strings | JSON-equal |
| `arithmetic` | The document must agree with itself: Σ line_amount = subtotal, subtotal + tax = total, qty × unit = line, within tolerance | JSON-equal |
| `reconcile` | Deterministic bank-feed match → `matched` / `unmatched` / `ambiguous` / `arithmetic_mismatch`; candidates sorted by id; ambiguous never auto-picks | JSON-equal |
| `reconcile_envelope` | The content-addressed request hash for a reconcile call (operation + engine_version + schema_hash + canonical inputs + data_as_of) — the replay key an auditor uses | exact hash + JSON-equal result |
| `ledger_rules` | Rules-as-code verdicts and reason codes: `PERIOD_LOCKED`, `UNKNOWN_ACCOUNT_CODE`, `DUPLICATE_SOURCE_DOCUMENT`, `NOT_RECONCILED`, `ARITHMETIC_MISMATCH`, `CONFIDENCE_BELOW_FLOOR`; every applicable rule runs, no short-circuit | JSON-equal |
| `approval_summary` | The exact human-readable line the approver signs | exact string |
| `approval_token` | HMAC-SHA256 over the canonical signing input `{approved_at, approver_id, materiality, request_hash, session_id, summary}` with a fixed `approved_at` | JSON-equal (hex signature exact) |
| `approval_verify` | Token binding: any field mismatch, unknown approver, wrong secret, forged/short signature, altered timestamp → refused with reason | JSON-equal |
| `ledger_entry_id` | A ledger entry's id **is** SHA-256 of its canonical JSON; key order must not matter | exact |
| `audit_chain` | Hash chain over fixed, timestamped entries: `self_hash = sha256(canonical(entry without self_hash))`, `prev_hash` links, genesis `0×64`; tampering entry *n* breaks verification at *n* | exact hashes + broken-at seq |
| `ledger_post` | End to end: claim → reconcile → rules → signed approval bound to the request hash → engine post. Pins the stop stage, the request hash, the reconcile status, the **exact ordered audit-action sequence**, and that the posted total is the bank feed's, not the model's | JSON-equal |

## Running the runner against your implementation

```ts
import { runConformance, type ConformanceImplementation } from "@kernel.chat/kbot-finance/conformance";

const mine: ConformanceImplementation = { /* your port */ };
const report = await runConformance("node_modules/@kernel.chat/kbot-finance/conformance/vectors/v1", mine);
console.log(report.passed, "/", report.total, "suite", report.suite_hash);
```

`ConformanceImplementation` is the surface a port exposes
([`src/conformance/implementation.ts`](../src/conformance/implementation.ts)).
Everything is pure or takes explicit state; `ledgerPost` receives an
in-memory engine and an in-memory audit sink so no disk is involved. A port
that only implements some kinds should say which, and quote the suite hash.

Two negative controls ship in `test/conformance.test.ts`: an implementation
that auto-picks the first candidate when ambiguous fails exactly the
ambiguity vectors; an implementation that forgets to sort keys fails every
hash-bearing kind. If your port fails a vector, the vector's `description`
says what it pins.

## Fixed constants

| Constant | Value |
|---|---|
| `data_as_of` | `2026-08-15T00:00:00.000Z` |
| `approved_at` | `2026-08-15T12:00:00.000Z` |
| `session_id` | `conformance-session` |
| trusted approver | `cpa.jane` / secret `conformance-approver-secret-0001` (UTF-8) |
| untrusted signer | `intern.bob` / secret `not-in-the-trust-set` |
| default policy | `amount_tolerance 0.01`, `date_window_days 5` |
| chart of accounts | `400 425 430 200` |
| period closed through | `2026-06-30` |

Secrets here are test fixtures. They are not, and must never be, real.

## Versioning

`format_version` is the vector schema. `manifest.reference_versions` pins the
reference package, the reconcile engine, the ledger engine, and the ledger
schema hash the vectors were generated against. A change to any pinned
behaviour is a new suite hash and, if the change is semantic, a new
`format_version` directory (`v2/`). Old suites are never edited in place.
