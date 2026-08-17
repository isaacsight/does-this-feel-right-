"""Envelope, gate, audit sequence and receipt for recording a review.

    1. submission shape       -> malformed: stop, log nothing
    2. review_submitted       (hashes, recommendation, AI scope, lineage)
    3. disclosure_check       (the AI-disclosure verdict)
    4. verifier_check         (rules against the chain + disclosure; failure stops)
    5. approval_granted | approval_denied   (the editor signs the summary line)
    6. review_recorded        (a 'reviewed' entry appended to the manuscript's chain)

The envelope binds the full submission and the chain head it extends; the
editor signs a line that names the manuscript, round, reviewer,
recommendation and disclosed AI scope. The chain entry and the receipt
carry hashes only.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from ..core.approval import ApprovalRequest, ApprovalToken, verify_approval
from ..core.audit import AppendOnlyAuditLog
from ..core.canonical import canonicalize
from ..core.envelope import ContentAddressedRequest, sha256_text
from .chain import ReviewChain
from .checks import ai_disclosure_check, run_review_rules, validate_submission
from .model import ReviewSubmission

REVIEW_OPERATION = "review.record"
REVIEW_ENGINE_VERSION = "review-provenance@0.1.0"
REVIEW_MATERIALITY = "review.record"
REVIEW_SUBJECT = "review.record"
RECEIPT_FORMAT_VERSION = 1

REVIEW_SCHEMA_HASH = sha256_text(
    canonicalize(
        {
            "type": "object",
            "fields": {
                "submission": {"type": "ReviewSubmission"},
                "chain_head": {"type": "string|null"},
            },
        }
    )
)


def review_request(sub: ReviewSubmission, chain_head: Optional[str], data_as_of: str) -> ContentAddressedRequest:
    return ContentAddressedRequest(
        operation=REVIEW_OPERATION,
        engine_version=REVIEW_ENGINE_VERSION,
        schema_hash=REVIEW_SCHEMA_HASH,
        inputs={"submission": sub.to_json(), "chain_head": chain_head},
        data_as_of=data_as_of,
    )


def approval_summary(sub: ReviewSubmission, request_hash: str) -> str:
    """The exact line the editor signs."""
    m = sub.manuscript
    return (
        f"Record review of {m.title[:40]} round {m.round} by {sub.reviewer_id} rec {sub.recommendation} "
        f"ai:{sub.ai_contribution.scope} request {request_hash[:12]}"
    )


def reviewed_payload(sub: ReviewSubmission, request_hash: str, approval: ApprovalToken) -> dict:
    """What goes on the chain: hashes, recommendation, disclosure — no text."""
    ai = sub.ai_contribution.to_json()
    return {
        "manuscript": sub.manuscript.to_json(),
        "reviewer_id": sub.reviewer_id,
        "review_hash": sub.review_hash,
        "recommendation": sub.recommendation,
        "ai_contribution": {"used": ai["used"], "scope": ai["scope"], "model_lineage": ai["model_lineage"], "prompt_hash": ai["prompt_hash"]},
        "request_hash": request_hash,
        "approval": {"approver_id": approval.approver_id, "approved_at": approval.approved_at, "signature": approval.signature},
    }


def record_review(
    *,
    submission: ReviewSubmission,
    chain: ReviewChain,
    audit_log: AppendOnlyAuditLog,
    session_id: str,
    trusted: Mapping[str, bytes],
    data_as_of: str,
    approval: Optional[ApprovalToken] = None,
    manuscript_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """End to end. Returns ``{ok, stage, request_hash, audit_actions,
    entry_id, ...}``; ``stage`` is ``None`` on success or one of
    ``submission_shape | disclosure | verifier | approval``. ``entry_id`` is
    the ``self_hash`` of the appended chain entry."""
    errors = validate_submission(submission)
    if errors:
        return {"ok": False, "stage": "submission_shape", "request_hash": None, "audit_actions": audit_log.actions(), "entry_id": None, "detail": {"errors": errors}}
    ai = submission.ai_contribution
    audit_log.append(
        "review_submitted", REVIEW_SUBJECT, session_id,
        {
            "manuscript": submission.manuscript.to_json(), "reviewer_id": submission.reviewer_id, "review_hash": submission.review_hash,
            "recommendation": submission.recommendation, "ai_scope": ai.scope, "ai_used": ai.used, "timestamp": submission.timestamp,
        },
        model_lineage=ai.model_lineage if ai.used and ai.model_lineage else None,
    )

    disclosure = ai_disclosure_check(submission, manuscript_hash)
    audit_log.append("disclosure_check", REVIEW_SUBJECT, session_id, {"reviewer_id": submission.reviewer_id, "verdict": disclosure.to_json()})

    request = review_request(submission, chain.head(), data_as_of)
    request_hash = request.request_hash()
    report = run_review_rules(submission, chain, disclosure)
    audit_log.append("verifier_check", REVIEW_SUBJECT, session_id, {"request_hash": request_hash, "report": report})
    base = {"request_hash": request_hash, "disclosure": disclosure.to_json(), "verifier": report}
    if not report["ok"]:
        stage = "disclosure" if not disclosure.ok else "verifier"
        return {"ok": False, "stage": stage, **base, "audit_actions": audit_log.actions(), "entry_id": None, "detail": report}

    summary = approval_summary(submission, request_hash)
    approval_request = ApprovalRequest(request_hash, summary, session_id, REVIEW_MATERIALITY)
    if approval is None:
        audit_log.append("approval_denied", REVIEW_SUBJECT, session_id, {"request_hash": request_hash, "reason": "no_approval_token", "summary": summary})
        return {
            "ok": False, "stage": "approval", **base, "summary": summary, "audit_actions": audit_log.actions(), "entry_id": None,
            "detail": {"reason": "no_approval_token", "summary": summary},
        }
    v = verify_approval(approval, trusted, approval_request)
    if not v.ok:
        audit_log.append("approval_denied", REVIEW_SUBJECT, session_id, {"request_hash": request_hash, "reason": v.reason}, approver=approval.approver_id)
        return {"ok": False, "stage": "approval", **base, "summary": summary, "audit_actions": audit_log.actions(), "entry_id": None, "detail": {"reason": v.reason}}
    audit_log.append(
        "approval_granted", REVIEW_SUBJECT, session_id, {"request_hash": request_hash, "approved_at": approval.approved_at}, approver=approval.approver_id,
    )

    entry = chain.append(
        "reviewed", submission.reviewer_id, reviewed_payload(submission, request_hash, approval), submission.timestamp,
        model_lineage=ai.model_lineage if ai.used and ai.model_lineage else None, approver=approval.approver_id,
    )
    audit_log.append(
        "review_recorded", REVIEW_SUBJECT, session_id,
        {"request_hash": request_hash, "entry_id": entry["self_hash"], "chain_seq": entry["seq"], "reviewer_id": submission.reviewer_id},
        approver=approval.approver_id,
    )
    return {
        "ok": True, "stage": None, **base, "summary": summary, "audit_actions": audit_log.actions(),
        "entry_id": entry["self_hash"], "entry": entry, "receipt": review_receipt(entry),
    }


def review_receipt(entry: Mapping) -> dict:
    """Reviewer-facing receipt for a ``reviewed`` chain entry: what an
    ORCID/Publons-style credit record could consume. Hashes only — no review
    text, and no recommendation (which is confidential)."""
    if entry.get("action") != "reviewed":
        raise ValueError("review_receipt: entry is not a 'reviewed' chain entry")
    p = entry["payload"]
    m = p.get("manuscript") or {}
    ai = p.get("ai_contribution") or {}
    ap = p.get("approval") or {}
    return {
        "format_version": RECEIPT_FORMAT_VERSION,
        "kind": "review_receipt",
        "entry_id": entry["self_hash"],
        "seq": entry["seq"],
        "prev_hash": entry["prev_hash"],
        "session_id": entry.get("session_id"),
        "manuscript_doc_hash": m.get("doc_hash"),
        "venue": m.get("venue"),
        "round": m.get("round"),
        "reviewer_id": p.get("reviewer_id"),
        "review_hash": p.get("review_hash"),
        "ai_contribution": {"used": ai.get("used", False), "scope": ai.get("scope", "none")},
        "request_hash": p.get("request_hash"),
        "approved_by": ap.get("approver_id"),
        "approved_at": ap.get("approved_at"),
        "timestamp": entry.get("timestamp"),
    }
