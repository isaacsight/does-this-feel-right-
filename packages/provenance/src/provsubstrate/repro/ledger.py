"""Envelope, gate and audit sequence for recording a reproduction.

    1. attempt shape         -> malformed: stop, log nothing
    2. repro_attempt         (the model's proposal, with lineage)
    3. run_record            (what the runner observed)
    4. verifier_check        (judge verdict + rules; failure stops here)
    5. approval_granted | approval_denied
    6. report_recorded

The verdict is deterministic code over the run record; the model is never
on the path between "attempt" and "verdict". A signed report attests the
exact envelope the human read. Negative or partial verdicts stop at the
verifier and stay on the audit chain as attempts — they are never signed
as reports.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from ..core.approval import ApprovalRequest, ApprovalToken, verify_approval
from ..core.audit import AppendOnlyAuditLog
from ..core.canonical import canonicalize
from ..core.envelope import ContentAddressedRequest, content_hash, sha256_text
from .judge import judge, run_repro_rules, validate_attempt
from .model import ReproductionAttempt, ReproductionTarget, ReproVerdict, RunRecord
from .runner import Runner

REPRO_OPERATION = "repro.judge"
REPRO_ENGINE_VERSION = "repro-ledger@0.1.0"
REPRO_MATERIALITY = "repro.report"
REPRO_SUBJECT = "repro.report"
REPORT_FORMAT_VERSION = 1

REPRO_SCHEMA_HASH = sha256_text(
    canonicalize(
        {
            "type": "object",
            "fields": {
                "target": {"type": "ReproductionTarget"},
                "attempt": {"type": "ReproductionAttempt"},
                "run_record": {"type": "RunRecord"},
            },
        }
    )
)


def repro_request(target: ReproductionTarget, attempt: ReproductionAttempt, run_record: RunRecord, data_as_of: str) -> ContentAddressedRequest:
    return ContentAddressedRequest(
        operation=REPRO_OPERATION,
        engine_version=REPRO_ENGINE_VERSION,
        schema_hash=REPRO_SCHEMA_HASH,
        inputs={"target": target.to_json(), "attempt": attempt.to_json(), "run_record": run_record.to_json()},
        data_as_of=data_as_of,
    )


def approval_summary(target: ReproductionTarget, verdict: ReproVerdict) -> str:
    """The exact line the human signs. Deterministic over its inputs."""
    commit = target.repo.commit[:12] if target.repo.commit else "(unpinned)"
    return (
        f"Record reproduction of {target.paper.title[:40]} commit {commit} verdict {verdict.overall} "
        f"{verdict.confirmed}/{verdict.total} claims doc:{target.paper.doc_hash[:12]}"
    )


def build_report(
    *,
    request: ContentAddressedRequest,
    target: ReproductionTarget,
    attempt: ReproductionAttempt,
    run_record: RunRecord,
    verdict: ReproVerdict,
    approval: ApprovalToken,
    session_id: str,
) -> dict:
    """A signed report row: envelope + verdict + the approval token that
    binds a human to it. ``report_id`` is the content hash of the body."""
    body = {
        "format_version": REPORT_FORMAT_VERSION,
        "operation": request.operation,
        "engine_version": request.engine_version,
        "schema_hash": request.schema_hash,
        "data_as_of": request.data_as_of,
        "request_hash": request.request_hash(),
        "session_id": session_id,
        "target_hash": target.target_hash(),
        "target": target.to_json(),
        "attempt_hash": attempt.attempt_hash(),
        "attempt": attempt.to_json(),
        "run_record": run_record.to_json(),
        "verdict": verdict.to_json(),
        "approval": approval.to_json(),
    }
    return {"report_id": content_hash(body), **body}


def record_reproduction(
    *,
    target: ReproductionTarget,
    attempt: ReproductionAttempt,
    runner: Runner,
    audit_log: AppendOnlyAuditLog,
    session_id: str,
    trusted: Mapping[str, bytes],
    data_as_of: str,
    approval: Optional[ApprovalToken] = None,
    confidence_floor: float = 0.6,
) -> Dict[str, Any]:
    """End to end. Returns ``{ok, stage, request_hash, overall, audit_actions,
    report_id, ...}``; ``stage`` is ``None`` on success, otherwise one of
    ``attempt_shape | run | verifier | approval``. Extra keys (``summary``,
    ``verdict``, ``verifier``, ``report``, ``detail``) carry what a caller
    needs to sign or to explain a refusal."""
    errors = validate_attempt(target, attempt)
    if errors:
        return {
            "ok": False, "stage": "attempt_shape", "request_hash": None, "overall": None,
            "audit_actions": audit_log.actions(), "report_id": None, "detail": {"errors": errors},
        }
    target_hash = target.target_hash()
    audit_log.append(
        "repro_attempt", REPRO_SUBJECT, session_id,
        {"target_hash": target_hash, "attempt_hash": attempt.attempt_hash(), "attempt": attempt.to_json()},
        model_lineage=attempt.model_lineage,
    )

    run_record = runner.run(target, attempt)
    audit_log.append("run_record", REPRO_SUBJECT, session_id, {"target_hash": target_hash, "run_record": run_record.to_json()})

    verdict = judge(target, attempt, run_record)
    request = repro_request(target, attempt, run_record, data_as_of)
    request_hash = request.request_hash()
    report = run_repro_rules(target, attempt, verdict, confidence_floor)
    audit_log.append(
        "verifier_check", REPRO_SUBJECT, session_id,
        {"request_hash": request_hash, "verdict": verdict.to_json(), "report": report},
    )
    base = {"request_hash": request_hash, "overall": verdict.overall, "verdict": verdict.to_json(), "verifier": report}
    if not report["ok"]:
        stage = "run" if verdict.overall == "could_not_run" else "verifier"
        return {"ok": False, "stage": stage, **base, "audit_actions": audit_log.actions(), "report_id": None, "detail": report}

    summary = approval_summary(target, verdict)
    approval_request = ApprovalRequest(request_hash, summary, session_id, REPRO_MATERIALITY)
    if approval is None:
        audit_log.append(
            "approval_denied", REPRO_SUBJECT, session_id,
            {"request_hash": request_hash, "reason": "no_approval_token", "summary": summary},
        )
        return {
            "ok": False, "stage": "approval", **base, "summary": summary, "audit_actions": audit_log.actions(),
            "report_id": None, "detail": {"reason": "no_approval_token", "summary": summary},
        }
    v = verify_approval(approval, trusted, approval_request)
    if not v.ok:
        audit_log.append(
            "approval_denied", REPRO_SUBJECT, session_id, {"request_hash": request_hash, "reason": v.reason}, approver=approval.approver_id,
        )
        return {
            "ok": False, "stage": "approval", **base, "summary": summary, "audit_actions": audit_log.actions(),
            "report_id": None, "detail": {"reason": v.reason},
        }
    audit_log.append(
        "approval_granted", REPRO_SUBJECT, session_id,
        {"request_hash": request_hash, "approved_at": approval.approved_at}, approver=approval.approver_id,
    )

    signed = build_report(
        request=request, target=target, attempt=attempt, run_record=run_record, verdict=verdict, approval=approval, session_id=session_id,
    )
    audit_log.append(
        "report_recorded", REPRO_SUBJECT, session_id,
        {"request_hash": request_hash, "report_id": signed["report_id"], "overall": verdict.overall},
        approver=approval.approver_id,
    )
    return {
        "ok": True, "stage": None, **base, "summary": summary, "audit_actions": audit_log.actions(),
        "report_id": signed["report_id"], "report": signed,
    }
