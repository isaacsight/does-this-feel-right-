"""Peer-review provenance: shape, disclosure, chain, record flow, receipt,
and conformance handler round-trips."""

from provsubstrate.core import AppendOnlyAuditLog, ApprovalRequest, Approver, canonicalize, verify_chain
from provsubstrate.review import (
    CONFORMANCE_HANDLERS,
    REVIEW_MATERIALITY,
    AIContribution,
    Manuscript,
    ReviewChain,
    ReviewSubmission,
    ai_disclosure_check,
    approval_summary,
    build_review_chain,
    compute_expected,
    conformance_cases,
    record_review,
    review_receipt,
    run_review_rules,
    validate_submission,
    verify_review_chain,
)
from provsubstrate.review.conformance import (
    AI_NONE,
    AI_SUBSTANTIVE,
    AI_SUBSTANTIVE_NO_LINEAGE,
    AI_UNDISCLOSED_SCOPE,
    APPROVED_AT,
    DATA_AS_OF,
    MANUSCRIPT_DOC_HASH,
    OTHER_DOC_HASH,
    SESSION_ID,
    SUBMITTED_AT,
    TRUSTED_APPROVER,
    base_manuscript,
    base_submission,
)

TRUSTED = {TRUSTED_APPROVER["approver_id"]: TRUSTED_APPROVER["secret_utf8"].encode("utf-8")}


def clock():
    return DATA_AS_OF


def test_validate_submission():
    assert validate_submission(base_submission()) == []
    errs = validate_submission(ReviewSubmission(Manuscript("", "zz", "", 0), "", "", "maybe", AIContribution(True, [{"model": "x"}], "short", "weird", ""), ""))
    assert errs == sorted(errs) and len(errs) >= 9
    assert any("model_lineage[0]" in e for e in errs)


def test_disclosure_rules():
    assert ai_disclosure_check(base_submission()).ok
    assert ai_disclosure_check(base_submission(ai=AI_NONE)).ok
    assert ai_disclosure_check(base_submission(ai=AI_SUBSTANTIVE)).ok
    assert ai_disclosure_check(base_submission(ai=AI_UNDISCLOSED_SCOPE)).code == "UNDISCLOSED_AI"
    assert ai_disclosure_check(base_submission(ai=AIContribution(True, [], None, "summary", ""))).code == "UNDISCLOSED_AI"
    assert ai_disclosure_check(base_submission(ai=AI_SUBSTANTIVE_NO_LINEAGE)).code == "SUBSTANTIVE_AI_NO_LINEAGE"
    assert ai_disclosure_check(base_submission(recommendation="")).code == "MISSING_RECOMMENDATION"
    assert ai_disclosure_check(base_submission(review_text=" ")).code == "EMPTY_REVIEW"
    assert ai_disclosure_check(base_submission(), OTHER_DOC_HASH).code == "MANUSCRIPT_HASH_MISMATCH"
    v = ai_disclosure_check(base_submission(review_text="", ai=AI_UNDISCLOSED_SCOPE), OTHER_DOC_HASH)
    assert v.code == "MANUSCRIPT_HASH_MISMATCH" and v.codes == ["MANUSCRIPT_HASH_MISMATCH", "EMPTY_REVIEW", "UNDISCLOSED_AI"]


def test_chain_build_verify_and_tamper():
    items = [
        {"kind": "submitted", "actor": "editor.grace", "payload": base_manuscript().to_json(), "timestamp": SUBMITTED_AT},
        {"kind": "reviewed", "actor": "r1", "payload": {"reviewer_id": "r1", "review_hash": "a" * 64, "manuscript": base_manuscript().to_json()}, "timestamp": "2026-08-10T00:00:00.000Z"},
        {"kind": "editor_decision", "actor": "editor.grace", "payload": {"decision": "minor"}, "timestamp": "2026-08-11T00:00:00.000Z"},
    ]
    chained = build_review_chain(SESSION_ID, items)
    assert verify_review_chain(chained).ok and verify_chain(chained).ok
    assert chained[0]["prev_hash"] == "0" * 64 and chained[1]["prev_hash"] == chained[0]["self_hash"]
    tampered = [dict(e) for e in chained]
    tampered[1]["payload"] = {"reviewer_id": "r1", "review_hash": "b" * 64}
    v = verify_review_chain(tampered)
    assert not v.ok and v.broken_at_seq == 1 and v.reason == "chain"
    # not opened
    assert verify_review_chain(build_review_chain(SESSION_ID, items[1:])).reason == "not_open"
    # ReviewChain object produces the same hashes as the pure builder
    c = ReviewChain.open(SESSION_ID, base_manuscript(), "editor.grace", SUBMITTED_AT)
    c.append("reviewed", "r1", items[1]["payload"], items[1]["timestamp"])
    c.append("editor_decision", "editor.grace", items[2]["payload"], items[2]["timestamp"])
    assert [e["self_hash"] for e in c.entries] == [e["self_hash"] for e in chained]
    assert c.head() == chained[-1]["self_hash"] and c.manuscript_doc_hash() == MANUSCRIPT_DOC_HASH
    assert c.has_review("r1", 1) and not c.has_review("r2", 1) and not c.has_review("r1", 2)
    # loaded entries are verbatim, so tampering is visible through the object too
    assert not ReviewChain(SESSION_ID, tampered).verify().ok
    assert ReviewChain.from_json(c.to_json()).verify().ok


def _record(sub, chain, approval=None, manuscript_hash=None):
    log = AppendOnlyAuditLog(None, clock)
    res = record_review(
        submission=sub, chain=chain, audit_log=log, session_id=SESSION_ID, trusted=TRUSTED, data_as_of=DATA_AS_OF,
        approval=approval, manuscript_hash=manuscript_hash,
    )
    return res, log


def _sign(res, who="pi.ada", secret=None, request_hash=None):
    secret = secret if secret is not None else TRUSTED["pi.ada"]
    return Approver(who, secret).approve(ApprovalRequest(request_hash or res["request_hash"], res["summary"], SESSION_ID, REVIEW_MATERIALITY), APPROVED_AT)


def test_record_full_path_receipt_and_refusals():
    chain = ReviewChain.open(SESSION_ID, base_manuscript(), "editor.grace", SUBMITTED_AT)
    sub = base_submission()
    dry, _ = _record(sub, chain)
    assert dry["stage"] == "approval" and dry["audit_actions"] == ["review_submitted", "disclosure_check", "verifier_check", "approval_denied"]
    assert dry["summary"] == approval_summary(sub, dry["request_hash"])
    assert dry["summary"].startswith("Record review of On the Provenance of Numbers in Machine- round 1 by reviewer-2f9c rec minor ai:language request ")
    res, log = _record(sub, chain, _sign(dry))
    assert res["ok"] and res["audit_actions"] == ["review_submitted", "disclosure_check", "verifier_check", "approval_granted", "review_recorded"]
    assert verify_chain(log.entries).ok and chain.verify().ok
    assert res["entry_id"] == chain.entries[-1]["self_hash"] and chain.entries[-1]["action"] == "reviewed"
    # the chain and the receipt carry hashes only
    assert sub.review_text not in canonicalize(chain.entries)
    rec = review_receipt(chain.entries[-1])
    assert rec["review_hash"] == sub.review_hash and rec["entry_id"] == res["entry_id"] and rec["approved_by"] == "pi.ada"
    assert "recommendation" not in rec and sub.review_text not in canonicalize(rec)
    assert rec["ai_contribution"] == {"used": True, "scope": "language"}
    # duplicate by the same reviewer in the same round is refused at the verifier
    dup, _ = _record(sub, chain, _sign(dry))
    assert dup["stage"] == "verifier" and any(c.get("code") == "DUPLICATE_REVIEW" for c in dup["verifier"]["checks"])
    # a second reviewer extends the chain; the chain head is part of the envelope
    sub2 = base_submission(reviewer_id="reviewer-7a01", recommendation="major", ai=AI_NONE)
    dry2, _ = _record(sub2, chain)
    assert dry2["request_hash"] != dry["request_hash"]
    res2, _ = _record(sub2, chain, _sign(dry2))
    assert res2["ok"] and len(chain.reviews()) == 2
    # wrong-hash and unknown-approver tokens are refused
    fresh = ReviewChain.open(SESSION_ID, base_manuscript(), "editor.grace", SUBMITTED_AT)
    d3, _ = _record(sub, fresh)
    r_wrong, _ = _record(sub, fresh, _sign(d3, request_hash="f" * 64))
    assert r_wrong["stage"] == "approval" and r_wrong["detail"]["reason"] == "request_hash_mismatch"
    r_unk, _ = _record(sub, fresh, _sign(d3, who="student.bob", secret=b"not-in-the-trust-set"))
    assert r_unk["stage"] == "approval" and r_unk["detail"]["reason"] == "unknown_approver"
    assert fresh.reviews() == []


def test_disclosure_and_hash_mismatch_never_reach_gate_and_malformed_logs_nothing():
    chain = ReviewChain.open(SESSION_ID, base_manuscript(), "editor.grace", SUBMITTED_AT)
    res, log = _record(base_submission(ai=AI_UNDISCLOSED_SCOPE), chain)
    assert res["stage"] == "disclosure" and res["audit_actions"] == ["review_submitted", "disclosure_check", "verifier_check"]
    res, _ = _record(base_submission(), chain, manuscript_hash=OTHER_DOC_HASH)
    assert res["stage"] == "disclosure" and res["disclosure"]["code"] == "MANUSCRIPT_HASH_MISMATCH"
    # chain opened for a different manuscript
    other = ReviewChain.open(SESSION_ID, base_manuscript(doc_hash=OTHER_DOC_HASH), "editor.grace", SUBMITTED_AT)
    res, _ = _record(base_submission(), other)
    assert res["stage"] == "verifier" and any(c.get("code") == "MANUSCRIPT_HASH_MISMATCH" for c in res["verifier"]["checks"])
    # chain not opened
    res, _ = _record(base_submission(), ReviewChain(SESSION_ID))
    assert res["stage"] == "verifier" and any(c.get("code") == "CHAIN_NOT_OPEN" for c in res["verifier"]["checks"])
    res, log = _record(base_submission(manuscript=base_manuscript(doc_hash="nothex")), chain)
    assert res["stage"] == "submission_shape" and log.entries == [] and res["request_hash"] is None
    # rules run without short-circuit
    r = run_review_rules(base_submission(ai=AI_UNDISCLOSED_SCOPE), other, ai_disclosure_check(base_submission(ai=AI_UNDISCLOSED_SCOPE)))
    assert [c["rule_id"] for c in r["checks"]] == ["rule.review.chain", "rule.review.manuscript", "rule.review.duplicate", "rule.review.disclosure"]
    assert [c.get("code") for c in r["checks"]] == [None, "MANUSCRIPT_HASH_MISMATCH", None, "UNDISCLOSED_AI"]


def test_conformance_handlers_round_trip_and_determinism():
    cases = conformance_cases()
    assert {c["kind"] for c in cases} == {"review_shape", "review_disclosure", "review_chain", "review_approval_summary", "review_record"}
    ids = [(c["kind"], c["id"]) for c in cases]
    assert len(ids) == len(set(ids))
    for c in cases:
        e1 = compute_expected(c["kind"], c["input"])
        e2 = compute_expected(c["kind"], c["input"])
        assert canonicalize(e1) == canonicalize(e2), c["id"]
        ok, detail = CONFORMANCE_HANDLERS[c["kind"]](c["input"], e1)
        assert ok, (c["kind"], c["id"], detail)
    c = next(x for x in cases if x["kind"] == "review_chain" and x["id"] == "five_entries_tamper_seq_1")
    exp = compute_expected(c["kind"], c["input"])
    assert exp["tampered"]["broken_at_seq"] == 1
    ok, _ = CONFORMANCE_HANDLERS["review_chain"](c["input"], {**exp, "head": "0" * 64})
    assert not ok
    assert canonicalize(conformance_cases()) == canonicalize(cases)
