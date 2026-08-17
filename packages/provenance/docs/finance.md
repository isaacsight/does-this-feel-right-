# finance — the ledger substrate

Port of `@kernel.chat/kbot-finance` 0.3.0; passes all 143 finance v1 vectors
byte for byte.

**The model proposes** a reading of a source document: an `ExtractionClaim`
`{doc_hash, direction (out|in), vendor, date, currency, subtotal, tax, total,
line_items [{description, quantity, unit_amount, line_amount, account_code,
tax_type?}], reference, confidence, model_lineage}`. The document's bytes were
sealed first (`seal_source_document`); only the hash travels. The claim is
hashed as received, extra keys and all.

**Arithmetic and the bank feed dispose.** `reconcile` is a pure function: the
document must agree with itself (line sums, subtotal + tax = total, quantity x
unit within tolerance; `arithmetic_mismatch` otherwise), then exactly one
unreconciled bank line with the same direction, currency, amount within
`amount_tolerance` and date within `date_window_days` must exist: `matched`;
none is `unmatched`; several is `ambiguous` (a human picks, never the model).
The ledger rules then run, all of them: `rule.ledger.period_lock`
(PERIOD_LOCKED), `rule.ledger.account_code` (UNKNOWN_ACCOUNT_CODE),
`rule.ledger.duplicate_document` (DUPLICATE_SOURCE_DOCUMENT),
`rule.ledger.reconciled` (NOT_RECONCILED | ARITHMETIC_MISMATCH),
`rule.ledger.confidence_floor` (CONFIDENCE_BELOW_FLOOR, default 0.6).

**An accountant signs** the summary line, bound to the `ledger.post` envelope
(engine version of the ledger underneath, inputs `{claim, reconciliation,
reconciliation_request_hash, bank_account_code}`), materiality `ledger.post`.
Only then does the `LedgerEngine` post, and the total that lands is the bank
line's amount, not the model's. Any throw on the engine path is an `incident`.

## Quick start (Python)

```python
import dataclasses, json
from provsubstrate.core import AppendOnlyAuditLog, Approver, ApprovalRequest
from provsubstrate.finance import (LEDGER_ENGINE_VERSION, LEDGER_POST_MATERIALITY, LedgerPostDeps, LedgerPostInputs,
                                   MemoryLedger, VerifierContext, ledger_post, make_ledger_rules, reconcile)

claim = json.load(open("claim.json")); bank_lines = json.load(open("bank.json"))
print(reconcile(claim, bank_lines).to_json()["status"])              # matched | unmatched | ambiguous | arithmetic_mismatch

engine = MemoryLedger(LEDGER_ENGINE_VERSION, bank_lines, posted_at="2026-08-15T00:00:00.000Z")   # or your own LedgerEngine
deps = LedgerPostDeps(
    audit_log=AppendOnlyAuditLog("audit.jsonl", clock=lambda: "2026-08-15T00:00:00.000Z"),
    rules=make_ledger_rules(), verifier_context=VerifierContext("session-1", {"valid_account_codes": ["400", "425"]}, "US"),
    trusted_approvers={"cpa.jane": b"secret"}, engine=engine, clock=lambda: "2026-08-15T00:00:00.000Z")
inputs = LedgerPostInputs(claim=claim, bank_lines=bank_lines, bank_account_code="090", data_as_of="2026-08-15T00:00:00.000Z")

dry = ledger_post(inputs, deps)                                        # stops at the gate: stage "approval"
print(dry.request_hash, dry.detail["summary"])                         # the accountant reads exactly this
token = Approver("cpa.jane", b"secret").approve(
    ApprovalRequest(dry.request_hash, dry.detail["summary"], "session-1", LEDGER_POST_MATERIALITY), "2026-08-15T12:00:00.000Z")   # HUMAN
r = ledger_post(dataclasses.replace(inputs, approval=token), deps)
print(r.ok, r.stage, r.response.value if r.ok else r.detail)          # value.total is the bank line's amount
```

## Command line

```bash
provsub finance reconcile claim.json bank.json [--policy p.json]              # pure; also prints the summary line a post would carry
provsub finance post claim.json bank.json --state state.json --bank-account-code 090 --jurisdiction US \
        --data-as-of T --session-id S                                          # no --approval: stops at the gate, prints what to sign
provsub approve --request-hash H --summary "SPEND USD 1240.50 ..." --session-id S --materiality ledger.post \
        --approver-id cpa.jane --secret-file ~/.provsub/secret --approved-at T --out tok.json      # HUMAN
provsub finance post claim.json bank.json --state state.json --bank-account-code 090 --jurisdiction US \
        --data-as-of T --session-id S --approval tok.json --trust cpa.jane=~/.provsub/secret \
        --audit audit.jsonl --posted-out posted.json
provsub audit verify audit.jsonl
```

The CLI posts to an in-memory `MemoryLedger` built from `bank.json`; a real
ledger implements `LedgerEngine` (`bank_lines()`, `post(entry)`) and is wired in
Python. `--engine-version` must match between the dry run and the post: it is
part of the request hash. `state.json` holds `{closed_through?,
valid_account_codes?, posted_doc_hashes?}`. MCP tools: `finance_reconcile`,
`finance_prepare_post` (verdicts and the line to sign; posting is CLI-only).

## Conformance kinds (finance v1, vendored from the TypeScript reference)

| kind | case ids |
|---|---|
| `claim_shape` | 25 cases: ok_clean, ok_eur, ok_fuel, ok_receive, ok_no_date, ok_no_vendor, ok_tax_type, ok_low_confidence, ok_unknown_code, ok_bad_line, ok_misread_total, ok_cents_edge, ok_three_lines_rounding, bad_not_object, bad_null_claim, bad_bad_hash, bad_bad_direction, bad_bad_currency, bad_bad_date, bad_nan_total, bad_empty_lines, bad_line_missing_code, bad_confidence_over, bad_no_lineage, bad_everything_wrong |
| `arithmetic` | clean, clean_zero_tol, eur, fuel, receive, bad_line, misread_total, cents_edge_tol_0, cents_edge_tol_1c, three_lines_rounding |
| `reconcile` | 27 cases: matched_standard, matched_eur, matched_fuel, matched_receive_direction, matched_one_cent_within_tol, matched_tight_policy_exact, matched_window_edge_inclusive, matched_window_before_inclusive, matched_far_wide_window, matched_claim_without_date, matched_line_without_date, matched_line_without_currency, matched_mixed_bag_ignores_noise, matched_rounding_tiny, unmatched_empty_feed, unmatched_two_cents, unmatched_one_cent_zero_tol, unmatched_wrong_direction, unmatched_currency_mismatch, unmatched_already_reconciled, unmatched_window_past, unmatched_far_default_window, unmatched_fuel_only, ambiguous_two, ambiguous_three_sorted_ids, arith_mismatch_short_circuits, arith_bad_line_short_circuits |
| `reconcile_envelope` | matched_standard, matched_standard_keys_shuffled, matched_standard_next_day_as_of, unmatched_empty_feed, unmatched_already_reconciled, unmatched_fuel_only, ambiguous_two, ambiguous_three_sorted_ids |
| `ledger_rules` | all_pass, all_pass_eu, all_pass_global, period_locked, period_locked_same_day, period_open_day_after, period_no_lock_configured, no_date_claim_period_lock_passes, unknown_account_code, no_chart_supplied_passes, duplicate_document, not_reconciled_empty, not_reconciled_ambiguous, arithmetic_mismatch, confidence_below_floor, confidence_at_floor_passes, confidence_floor_zero, multiple_failures |
| `approval_summary` | clean, eur, receive, no_vendor_no_date, ambiguous |
| `ledger_post` | posts_with_valid_approval, posts_eur, posts_receive, posts_total_from_bank_not_model, stops_at_gate_without_approval, rejects_wrong_hash_approval, rejects_unknown_approver, unmatched_never_reaches_gate, ambiguous_never_reaches_gate, arithmetic_mismatch_never_reaches_gate, period_locked_refused, unknown_account_code_refused, duplicate_document_refused, low_confidence_refused, engine_failure_is_incident, malformed_claim_logs_nothing, different_engine_version_different_hash |

The substrate kinds of the same suite (`canonicalize`, `source_document`,
`approval_token`, `approval_verify`, `ledger_entry_id`, `audit_chain`) are
handled by `provsubstrate.conformance.core_kinds`. See
`src/provsubstrate/finance/conformance.py`.

## Audit-action sequence (fixed)

`extraction_claim` -> `reconciliation` -> `verifier_check` -> (`approval_granted`
| `approval_denied`) -> `engine_request` -> (`engine_response` | `incident`). A
malformed claim logs nothing; a reconciliation or rule failure stops after
`verifier_check`; a missing or invalid token stops at `approval_denied`.

## Approval summary (exact format)

```
{SPEND|RECEIVE} {currency} {total to 2 dp} {vendor|(no vendor)} {date|(no date)} doc:{doc_hash[:12]} bank:{matched_bank_line_id|-}
```

Example (vector `approval_summary/clean`):
`SPEND USD 1240.50 Ag Supply Co 2026-08-12 doc:8e394c0ee918 bank:bt-1`.
Materiality `ledger.post`.
