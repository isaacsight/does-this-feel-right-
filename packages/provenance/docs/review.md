# review — peer-review provenance

**The model proposes** nothing here directly; the reviewer does, and must say
how much a model helped. A `ReviewSubmission` is `manuscript {title, doc_hash,
venue, round}`, `reviewer_id`, `review_text`, `recommendation` (accept | minor |
major | reject), an `ai_contribution {used, model_lineage, prompt_hash, scope
(none | language | summary | substantive), disclosed_text}`, and a `timestamp`.
The manuscript is identified only by the sha256 of its bytes.

**Deterministic checks dispose.** `validate_submission` is structural.
`ai_disclosure_check` applies the content rules in fixed order and reports the
first failing code plus all of them: MANUSCRIPT_HASH_MISMATCH (when the venue's
hash is given), EMPTY_REVIEW, MISSING_RECOMMENDATION, UNDISCLOSED_AI (used but
scope `none` or no disclosed text), SUBSTANTIVE_AI_NO_LINEAGE. `run_review_rules`
then runs against the manuscript's `ReviewChain`: `rule.review.chain`
(CHAIN_NOT_OPEN | CHAIN_BROKEN), `rule.review.manuscript`
(MANUSCRIPT_HASH_MISMATCH), `rule.review.duplicate` (DUPLICATE_REVIEW: same
reviewer, same round), `rule.review.disclosure` (the disclosure code).

**The editor signs** one line naming manuscript, round, reviewer, recommendation
and disclosed AI scope, bound to the `review.record` envelope
(`review-provenance@0.1.0`, inputs `{submission, chain_head}`), materiality
`review.record`. `record_review` then appends a `reviewed` entry to the chain
carrying hashes only (`review_hash`, never the text) and returns a receipt the
reviewer can hand to a credit system. The chain opens with a `submitted` entry
that pins `doc_hash`; `editor_decision` and `author_response` entries follow.

## Quick start (Python)

```python
from provsubstrate.core import AppendOnlyAuditLog, Approver, ApprovalRequest
from provsubstrate.review import (REVIEW_MATERIALITY, AIContribution, Manuscript, ReviewChain, ReviewSubmission,
                                  ai_disclosure_check, record_review, review_receipt)

m = Manuscript("On the Provenance of Numbers", "41ba8063" + "0" * 56, "KERNEL Workshop 2026", 1)
chain = ReviewChain.open("venue-session", m, "editor.grace", "2026-08-01T09:00:00.000Z")
sub = ReviewSubmission(m, "reviewer-2f9c", "Careful paper; Table 2 needs variance.", "minor",
                       AIContribution(True, [{"model": "local-27b", "version": "x"}], "b" * 64, "language", "Grammar only."),
                       "2026-08-10T15:30:00.000Z")
print(ai_disclosure_check(sub, m.doc_hash).to_json())               # {"ok": true, "code": null, "codes": []}

log = AppendOnlyAuditLog(None, clock=lambda: "2026-08-17T00:00:00.000Z")
common = dict(submission=sub, chain=chain, audit_log=log, session_id="venue-session", trusted={"editor.grace": b"secret"},
              data_as_of="2026-08-17T00:00:00.000Z", manuscript_hash=m.doc_hash)
dry = record_review(**common)                                       # stops at the gate: request_hash + summary
token = Approver("editor.grace", b"secret").approve(ApprovalRequest(dry["request_hash"], dry["summary"], "venue-session", REVIEW_MATERIALITY),
                                                    "2026-08-17T12:00:00.000Z")   # the editor's step
r = record_review(**common, approval=token)
print(r["ok"], r["entry_id"], r["audit_actions"], chain.verify().ok)
print(review_receipt(r["entry"]))                                   # hashes only; no text, no recommendation
```

## Command line

```bash
provsub review open manuscript.json --actor editor.grace --at 2026-08-01T09:00:00.000Z --session-id S --out chain.json
provsub review check submission.json --chain chain.json [--manuscript-hash H] --data-as-of T --session-id S
provsub approve --request-hash H --summary "..." --session-id S --materiality review.record \
        --approver-id editor.grace --secret-file ~/.provsub/secret --approved-at T --out tok.json   # HUMAN
provsub review record submission.json chain.json --approval tok.json --trust editor.grace=~/.provsub/secret \
        --audit audit.jsonl --receipt-out receipt.json --data-as-of T --session-id S
provsub review verify chain.json
provsub review receipt chain.json --seq 1
```

`check` without `--chain` runs shape and disclosure only (`report: null`); with
it, the chain rules too. `record` without `--approval` stops at the gate; on
success it rewrites `chain.json` with the new entry. MCP tools: `review_check`,
`review_chain_verify`.

## Conformance kinds (academic v1)

| kind | case ids |
|---|---|
| `review_shape` | ok_clean, ok_no_ai, ok_substantive, bad_hash, bad_round, bad_recommendation, bad_scope, bad_everything |
| `review_disclosure` | clean_disclosed, clean_no_ai, substantive_with_lineage, undisclosed_scope_none, undisclosed_empty_text, substantive_no_lineage, missing_recommendation, empty_review, manuscript_hash_mismatch, multiple_codes_first_wins |
| `review_chain` | five_entries_tamper_seq_1, five_entries_tamper_seq_3, single_submitted, not_opened |
| `review_approval_summary` | clean, no_ai, long_title_round_2 |
| `review_record` | records_clean_disclosed, records_no_ai, stops_at_gate_without_approval, rejects_wrong_hash_approval, rejects_unknown_approver, undisclosed_ai_never_reaches_gate, substantive_no_lineage_never_reaches_gate, manuscript_hash_mismatch_refused, duplicate_review_refused, second_reviewer_records, malformed_logs_nothing |

See `src/provsubstrate/review/conformance.py`.

## Audit-action sequence (fixed)

`review_submitted` -> `disclosure_check` -> `verifier_check` ->
(`approval_granted` | `approval_denied`) -> `review_recorded`. A structural
failure logs nothing; a disclosure failure stops with stage `disclosure`, a
chain-rule failure with stage `verifier`, both after `verifier_check`. The
chain entry (`reviewed`) is appended only after `approval_granted`.

## Approval summary (exact format)

```
Record review of {title[:40]} round {round} by {reviewer_id} rec {recommendation} ai:{scope} request {request_hash[:12]}
```

Example (vector `review_approval_summary/clean`):
`Record review of On the Provenance of Numbers in Machine- round 1 by reviewer-2f9c rec minor ai:language request 280bff032ca6`.
Materiality `review.record`.
