"""Conformance catalogue for peer-review provenance (academic v1).

Kinds: ``review_shape``, ``review_disclosure``, ``review_chain``,
``review_approval_summary``, ``review_record``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..conformance.runner import Handler, expect_equal
from ..core.approval import ApprovalRequest, ApprovalToken, Approver
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import sha256_text
from .chain import ReviewChain, build_review_chain, verify_review_chain
from .checks import ai_disclosure_check, validate_submission
from .ledger import REVIEW_MATERIALITY, approval_summary, record_review
from .model import AIContribution, Manuscript, ReviewSubmission

DATA_AS_OF = "2026-08-17T00:00:00.000Z"
APPROVED_AT = "2026-08-17T12:00:00.000Z"
SESSION_ID = "academic-conformance-session"
TRUSTED_APPROVER = {"approver_id": "pi.ada", "secret_utf8": "academic-approver-secret-0001"}
UNTRUSTED_SIGNER = {"approver_id": "student.bob", "secret_utf8": "not-in-the-trust-set"}
MODEL_LINEAGE = [{"model": "local-27b", "version": "conformance"}]

MANUSCRIPT_DOC_HASH = sha256_text("manuscript: On the Provenance of Numbers in Machine-Assisted Science (submission v1)")
OTHER_DOC_HASH = sha256_text("manuscript: a different file")
PROMPT_HASH = sha256_text("prompt:review:academic-v1")
SUBMITTED_AT = "2026-08-01T09:00:00.000Z"
REVIEWED_AT = "2026-08-10T15:30:00.000Z"
REVIEW_TEXT = (
    "The paper is careful and the substrate is well motivated. Section 4's tolerance argument needs a worked example; "
    "Table 2 should report variance. Minor: typos in the appendix."
)


def _fixed_clock() -> str:
    return DATA_AS_OF


def base_manuscript(**over) -> Manuscript:
    d = {"title": "On the Provenance of Numbers in Machine-Assisted Science", "doc_hash": MANUSCRIPT_DOC_HASH, "venue": "KERNEL Workshop 2026", "round": 1}
    d.update(over)
    return Manuscript(d["title"], d["doc_hash"], d["venue"], d["round"])


AI_NONE = AIContribution.none()
AI_LANGUAGE = AIContribution(True, list(MODEL_LINEAGE), PROMPT_HASH, "language", "Used a local model to polish grammar; all judgements are my own.")
AI_SUBSTANTIVE = AIContribution(True, list(MODEL_LINEAGE), PROMPT_HASH, "substantive", "A local model drafted the summary of related work; I verified every citation.")
AI_UNDISCLOSED_SCOPE = AIContribution(True, list(MODEL_LINEAGE), PROMPT_HASH, "none", "")
AI_UNDISCLOSED_TEXT = AIContribution(True, list(MODEL_LINEAGE), PROMPT_HASH, "summary", "")
AI_SUBSTANTIVE_NO_LINEAGE = AIContribution(True, [], None, "substantive", "A model helped substantially.")


def base_submission(*, manuscript: Optional[Manuscript] = None, reviewer_id: str = "reviewer-2f9c", review_text: str = REVIEW_TEXT, recommendation: str = "minor", ai: AIContribution = AI_LANGUAGE, timestamp: str = REVIEWED_AT) -> ReviewSubmission:
    return ReviewSubmission(manuscript or base_manuscript(), reviewer_id, review_text, recommendation, ai, timestamp)


def record_from_input(inp: dict) -> dict:
    """Replay a ``review_record`` input: open the chain, replay any prior
    reviews (each with a valid signature), then record the submission with
    the directed approval mode."""
    manuscript = Manuscript.from_json(inp["manuscript"])
    sub = ReviewSubmission.from_json(inp["submission"])
    trusted = {t["approver_id"]: t["secret_utf8"].encode("utf-8") for t in inp["trusted"]}
    session_id = inp["session_id"]
    mode = inp.get("approval", "none")
    manuscript_hash = inp.get("manuscript_hash")
    first = inp["trusted"][0]
    signer = Approver(first["approver_id"], first["secret_utf8"].encode("utf-8"))
    stranger_d = inp.get("untrusted", UNTRUSTED_SIGNER)
    stranger = Approver(stranger_d["approver_id"], stranger_d["secret_utf8"].encode("utf-8"))

    def fresh_chain() -> ReviewChain:
        chain = ReviewChain.open(session_id, manuscript, inp.get("opened_by", "editor.grace"), inp.get("opened_at", SUBMITTED_AT))
        for prior in inp.get("prior_reviews") or []:
            ps = ReviewSubmission.from_json(prior)
            dry = record_review(submission=ps, chain=chain, audit_log=AppendOnlyAuditLog(None, _fixed_clock), session_id=session_id, trusted=trusted, data_as_of=inp["data_as_of"])
            tok = signer.approve(ApprovalRequest(dry["request_hash"], dry["summary"], session_id, REVIEW_MATERIALITY), inp["approved_at"])
            r = record_review(submission=ps, chain=chain, audit_log=AppendOnlyAuditLog(None, _fixed_clock), session_id=session_id, trusted=trusted, data_as_of=inp["data_as_of"], approval=tok)
            if not r["ok"]:
                raise RuntimeError(f"prior review did not record: {r}")
        return chain

    def go(token: Optional[ApprovalToken]) -> dict:
        return record_review(
            submission=sub, chain=fresh_chain(), audit_log=AppendOnlyAuditLog(None, _fixed_clock), session_id=session_id, trusted=trusted,
            data_as_of=inp["data_as_of"], approval=token, manuscript_hash=manuscript_hash,
        )

    token: Optional[ApprovalToken] = None
    if mode != "none":
        dry = go(None)
        summary, rh = dry.get("summary"), dry.get("request_hash")
        if summary is not None and rh is not None:
            if mode == "valid":
                token = signer.approve(ApprovalRequest(rh, summary, session_id, REVIEW_MATERIALITY), inp["approved_at"])
            elif mode == "wrong_hash":
                token = signer.approve(ApprovalRequest("f" * 64, summary, session_id, REVIEW_MATERIALITY), inp["approved_at"])
            elif mode == "unknown_approver":
                token = stranger.approve(ApprovalRequest(rh, summary, session_id, REVIEW_MATERIALITY), inp["approved_at"])
            else:
                raise ValueError(f"unknown approval mode {mode!r}")
    return go(token)


def _record_expected(res: dict) -> dict:
    return {"ok": res["ok"], "stage": res["stage"], "request_hash": res["request_hash"], "audit_actions": res["audit_actions"], "entry_id": res["entry_id"]}


def _record_input(sub: ReviewSubmission, *, manuscript: Optional[Manuscript] = None, approval: str = "none", manuscript_hash: Optional[str] = None, prior: Optional[list] = None) -> dict:
    d = {
        "manuscript": (manuscript or base_manuscript()).to_json(), "opened_by": "editor.grace", "opened_at": SUBMITTED_AT,
        "submission": sub.to_json(), "session_id": SESSION_ID, "trusted": [TRUSTED_APPROVER], "untrusted": UNTRUSTED_SIGNER, "approved_at": APPROVED_AT,
        "data_as_of": DATA_AS_OF, "approval": approval, "manuscript_hash": manuscript_hash,
    }
    if prior:
        d["prior_reviews"] = [p.to_json() for p in prior]
    return d


def compute_expected(kind: str, inp: dict) -> Any:
    if kind == "review_shape":
        return {"errors": validate_submission(ReviewSubmission.from_json(inp["submission"]))}
    if kind == "review_disclosure":
        v = ai_disclosure_check(ReviewSubmission.from_json(inp["submission"]), inp.get("manuscript_hash"))
        return {"ok": v.ok, "code": v.code, "codes": v.codes}
    if kind == "review_chain":
        chained = build_review_chain(inp["session_id"], inp["items"])
        hashes = [{"seq": e["seq"], "prev_hash": e["prev_hash"], "self_hash": e["self_hash"]} for e in chained]
        intact = verify_review_chain(chained).to_json()
        t = inp["tamper"]
        tampered = [({**e, "payload": t["payload"]} if e["seq"] == t["seq"] else e) for e in chained]
        tv = verify_review_chain(tampered)
        return {"hashes": hashes, "intact": intact, "tampered": tv.to_json(), "head": chained[-1]["self_hash"] if chained else None}
    if kind == "review_approval_summary":
        return {"summary": approval_summary(ReviewSubmission.from_json(inp["submission"]), inp["request_hash"])}
    if kind == "review_record":
        return _record_expected(record_from_input(inp))
    raise KeyError(f"review: unknown conformance kind {kind!r}")


def _case(kind: str, cid: str, description: str, inp: dict) -> dict:
    return {"kind": kind, "id": cid, "description": description, "input": inp}


def conformance_cases() -> List[dict]:
    cases: List[dict] = []
    clean = base_submission()
    no_ai = base_submission(ai=AI_NONE)
    substantive = base_submission(ai=AI_SUBSTANTIVE)

    # review_shape
    shape = [
        ("ok_clean", clean, "well-formed, AI language use disclosed"),
        ("ok_no_ai", no_ai, "well-formed, no AI"),
        ("ok_substantive", substantive, "well-formed, substantive AI with lineage"),
        ("bad_hash", base_submission(manuscript=base_manuscript(doc_hash="nothex")), "doc_hash not sha256"),
        ("bad_round", base_submission(manuscript=base_manuscript(round=0)), "round below 1"),
        ("bad_recommendation", base_submission(recommendation="strong-accept"), "unknown recommendation"),
        ("bad_scope", base_submission(ai=AIContribution(True, list(MODEL_LINEAGE), PROMPT_HASH, "everything", "x")), "unknown AI scope"),
        ("bad_everything", ReviewSubmission(Manuscript("", "zz", "", 0), "", "", "maybe", AIContribution(True, [{"model": "x"}], "short", "weird", ""), ""), "every structural error, sorted"),
    ]
    for cid, s, desc in shape:
        cases.append(_case("review_shape", cid, desc, {"submission": s.to_json()}))

    # review_disclosure
    disc = [
        ("clean_disclosed", clean, MANUSCRIPT_DOC_HASH, "AI used, scope language, disclosed -> ok"),
        ("clean_no_ai", no_ai, None, "no AI, no manuscript hash given -> ok"),
        ("substantive_with_lineage", substantive, MANUSCRIPT_DOC_HASH, "substantive with lineage and prompt hash -> ok"),
        ("undisclosed_scope_none", base_submission(ai=AI_UNDISCLOSED_SCOPE), None, "used but scope none -> UNDISCLOSED_AI"),
        ("undisclosed_empty_text", base_submission(ai=AI_UNDISCLOSED_TEXT), None, "used, scope summary, no disclosed text -> UNDISCLOSED_AI"),
        ("substantive_no_lineage", base_submission(ai=AI_SUBSTANTIVE_NO_LINEAGE), None, "substantive without lineage -> SUBSTANTIVE_AI_NO_LINEAGE"),
        ("missing_recommendation", base_submission(recommendation=""), None, "MISSING_RECOMMENDATION"),
        ("empty_review", base_submission(review_text="   \n"), None, "EMPTY_REVIEW"),
        ("manuscript_hash_mismatch", clean, OTHER_DOC_HASH, "reviewed a different file than the venue holds"),
        ("multiple_codes_first_wins", base_submission(review_text="", recommendation="", ai=AI_UNDISCLOSED_SCOPE), OTHER_DOC_HASH, "code is the first in fixed order; codes lists all"),
    ]
    for cid, s, mh, desc in disc:
        cases.append(_case("review_disclosure", cid, desc, {"submission": s.to_json(), "manuscript_hash": mh}))

    # review_chain
    items = [
        {"kind": "submitted", "actor": "editor.grace", "payload": base_manuscript().to_json(), "timestamp": SUBMITTED_AT},
        {"kind": "reviewed", "actor": "reviewer-2f9c", "payload": {"manuscript": base_manuscript().to_json(), "reviewer_id": "reviewer-2f9c", "review_hash": clean.review_hash, "recommendation": "minor", "ai_contribution": {"used": True, "scope": "language"}}, "timestamp": REVIEWED_AT},
        {"kind": "reviewed", "actor": "reviewer-7a01", "payload": {"manuscript": base_manuscript().to_json(), "reviewer_id": "reviewer-7a01", "review_hash": sha256_text("second review"), "recommendation": "major", "ai_contribution": {"used": False, "scope": "none"}}, "timestamp": "2026-08-11T10:00:00.000Z"},
        {"kind": "editor_decision", "actor": "editor.grace", "payload": {"decision": "major", "round": 1}, "timestamp": "2026-08-12T08:00:00.000Z"},
        {"kind": "author_response", "actor": "author-11", "payload": {"response_hash": sha256_text("we thank the reviewers"), "round": 2}, "timestamp": "2026-08-20T08:00:00.000Z"},
    ]
    cases.append(_case("review_chain", "five_entries_tamper_seq_1", "tampering the first review breaks verification at 1", {"session_id": SESSION_ID, "items": items, "tamper": {"seq": 1, "payload": {"recommendation": "accept"}}}))
    cases.append(_case("review_chain", "five_entries_tamper_seq_3", "tampering the editor decision breaks at 3", {"session_id": SESSION_ID, "items": items, "tamper": {"seq": 3, "payload": {"decision": "accept", "round": 1}}}))
    cases.append(_case("review_chain", "single_submitted", "a chain of one submitted entry; tamper it", {"session_id": SESSION_ID, "items": items[:1], "tamper": {"seq": 0, "payload": base_manuscript(doc_hash=OTHER_DOC_HASH).to_json()}}))
    cases.append(_case("review_chain", "not_opened", "a chain that does not start with submitted is intact as a hash chain but invalid as a review chain", {"session_id": SESSION_ID, "items": items[1:3], "tamper": {"seq": 1, "payload": {}}}))

    # review_approval_summary
    rh = sha256_text("request:example")
    cases.append(_case("review_approval_summary", "clean", "editor's line for a disclosed-language review", {"submission": clean.to_json(), "request_hash": rh}))
    cases.append(_case("review_approval_summary", "no_ai", "ai:none", {"submission": no_ai.to_json(), "request_hash": rh}))
    long_title = base_submission(manuscript=base_manuscript(title="B" * 90, round=2), recommendation="reject", ai=AI_SUBSTANTIVE)
    cases.append(_case("review_approval_summary", "long_title_round_2", "title cut at 40; round and recommendation carried", {"submission": long_title.to_json(), "request_hash": rh}))

    # review_record
    rec = [
        ("records_clean_disclosed", clean, "valid", None, None, "full path with a valid editor signature"),
        ("records_no_ai", no_ai, "valid", None, None, "no AI use records cleanly"),
        ("stops_at_gate_without_approval", clean, "none", None, None, "verifier ok, no token -> approval_denied"),
        ("rejects_wrong_hash_approval", clean, "wrong_hash", None, None, "token bound to another request hash is refused"),
        ("rejects_unknown_approver", clean, "unknown_approver", None, None, "signer outside the trust set is refused"),
        ("undisclosed_ai_never_reaches_gate", base_submission(ai=AI_UNDISCLOSED_SCOPE), "valid", None, None, "UNDISCLOSED_AI stops at disclosure"),
        ("substantive_no_lineage_never_reaches_gate", base_submission(ai=AI_SUBSTANTIVE_NO_LINEAGE), "valid", None, None, "SUBSTANTIVE_AI_NO_LINEAGE stops at disclosure"),
        ("manuscript_hash_mismatch_refused", clean, "valid", OTHER_DOC_HASH, None, "venue's manuscript hash differs from what was reviewed"),
        ("duplicate_review_refused", clean, "valid", None, [clean], "same reviewer, same round already on the chain -> DUPLICATE_REVIEW at verifier"),
        ("second_reviewer_records", base_submission(reviewer_id="reviewer-7a01", recommendation="major", ai=AI_NONE), "valid", None, [clean], "a different reviewer extends the chain"),
    ]
    for cid, s, mode, mh, prior, desc in rec:
        cases.append(_case("review_record", cid, desc, _record_input(s, approval=mode, manuscript_hash=mh, prior=prior)))
    bad = base_submission(manuscript=base_manuscript(doc_hash="nothex"), recommendation="strong-accept")
    cases.append(_case("review_record", "malformed_logs_nothing", "structural errors: refused before anything is logged", _record_input(bad, approval="valid")))
    return cases


def _mk(kind: str) -> Handler:
    def h(inp, exp):
        return expect_equal(compute_expected(kind, inp), exp)
    h.__name__ = f"h_{kind}"
    return h


CONFORMANCE_HANDLERS: Dict[str, Handler] = {k: _mk(k) for k in ("review_shape", "review_disclosure", "review_chain", "review_approval_summary", "review_record")}
