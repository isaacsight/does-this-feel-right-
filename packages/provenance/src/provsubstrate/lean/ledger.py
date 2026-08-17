"""The proof ledger: envelope, gate, audit sequence, record.

``record_proof`` is the full path from a model's proposed proof to a ledger
entry, every step on the audit chain:

  1. claim shape (``proof_claim``)
  2. the kernel disposes, in a content-addressed envelope (``kernel_verdict``)
  3. rules-as-code (``verifier_check``) — any failure stops here
  4. a mathematician's signed approval bound to THIS request hash
     (``approval_granted`` | ``approval_denied``)
  5. the entry lands (``proof_recorded``); ``entry_id`` is its content hash

The model is never on the path between "proof" and "recorded". The kernel
verdict is what gets recorded, and the human signed the exact line that
described it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Mapping, Optional, Sequence, Union

from ..core.approval import ApprovalRequest, ApprovalToken, verify_approval
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import ContentAddressedRequest, content_hash
from .claim import ProofClaim, ClaimShape, proof_file_hash, render_lean_file, validate_claim_shape
from .kernel import KernelDisposer, KernelVerdict, check_proof
from .rules import DEFAULT_AXIOM_ALLOWLIST, DEFAULT_CONFIDENCE_FLOOR, RuleReport, run_lean_rules

LEAN_ENGINE_VERSION = "lean-proof-ledger@0.1.0"
LEAN_OPERATION = "lean.check"
LEAN_RECORD_MATERIALITY = "lean.record"

# Fixed schema; its content hash goes in every envelope so a schema change
# is a different request hash.
LEAN_SCHEMA = {
    "type": "object",
    "fields": {
        "claim": {"type": "ProofClaim"},
        "toolchain": {"type": "string"},
        "mathlib_rev": {"type": "string"},
    },
}
LEAN_SCHEMA_HASH = content_hash(LEAN_SCHEMA)


def check_request(claim: ProofClaim, data_as_of: str) -> ContentAddressedRequest:
    """The envelope. Its hash is the replay key and what the human signs."""
    return ContentAddressedRequest(
        operation=LEAN_OPERATION,
        engine_version=LEAN_ENGINE_VERSION,
        schema_hash=LEAN_SCHEMA_HASH,
        inputs={"claim": claim.to_json(), "toolchain": claim.toolchain, "mathlib_rev": claim.mathlib_rev},
        data_as_of=data_as_of,
    )


def approval_summary(claim: ProofClaim, verdict: KernelVerdict) -> str:
    """The exact line the mathematician signs. Deterministic over its
    inputs; the proof-file hash names the bytes the kernel saw."""
    source = render_lean_file(claim)
    nbytes = len(source.encode("utf-8"))
    kernel = "kernel ok" if verdict.ok else "kernel REJECTED"
    axioms = ",".join(verdict.axioms) if verdict.axioms else "none"
    toolchain = claim.toolchain or "(unpinned)"
    mathlib = claim.mathlib_rev[:12] if claim.mathlib_rev else "(none)"
    return (
        f"Record proof of {claim.theorem_name} ({nbytes} bytes, {kernel}, {verdict.sorries} sorries, axioms: {axioms}) "
        f"toolchain {toolchain} mathlib {mathlib} file {proof_file_hash(claim)[:12]}"
    )


class ProofLedger:
    """In-memory, append-only. ``entry_id`` is the content hash of the entry
    body, so two ledgers that recorded the same proof under the same
    approval agree on the id."""

    def __init__(self) -> None:
        self.entries: List[dict] = []

    def append(self, body: Mapping[str, Any]) -> str:
        entry_id = content_hash(dict(body))
        self.entries.append({"entry_id": entry_id, **body})
        return entry_id

    def find(self, theorem_name: str) -> List[dict]:
        return [e for e in self.entries if e.get("theorem_name") == theorem_name]

    def to_json(self) -> List[dict]:
        return [dict(e) for e in self.entries]


@dataclass
class LeanDeps:
    kernel: KernelDisposer
    audit_log: AppendOnlyAuditLog
    ledger: ProofLedger
    trusted_approvers: Mapping[str, bytes]
    confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR
    axiom_allowlist: Sequence[str] = DEFAULT_AXIOM_ALLOWLIST


@dataclass(frozen=True)
class Prepared:
    """Everything deterministic that precedes the gate: the claim, the
    rendered bytes, the kernel verdict, the envelope and the summary line.
    ``prepare`` is what a caller uses to obtain the request hash and
    summary to put in front of a human before calling ``record_proof``."""

    claim: ProofClaim
    source: str
    proof_file_hash: str
    verdict: KernelVerdict
    request: ContentAddressedRequest
    request_hash: str
    report: RuleReport
    summary: str

    def approval_request(self, session_id: str) -> ApprovalRequest:
        return ApprovalRequest(self.request_hash, self.summary, session_id, LEAN_RECORD_MATERIALITY)


def prepare(
    claim: ProofClaim,
    kernel: KernelDisposer,
    *,
    data_as_of: str,
    confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR,
    axiom_allowlist: Sequence[str] = DEFAULT_AXIOM_ALLOWLIST,
) -> Prepared:
    source = render_lean_file(claim)
    verdict = check_proof(source, kernel)
    request = check_request(claim, data_as_of)
    report = run_lean_rules(claim, verdict, confidence_floor=confidence_floor, axiom_allowlist=axiom_allowlist)
    return Prepared(claim, source, proof_file_hash(claim), verdict, request, request.request_hash(), report, approval_summary(claim, verdict))


@dataclass(frozen=True)
class RecordResult:
    ok: bool
    stage: Optional[str]  # None | claim_shape | kernel | verifier | approval
    request_hash: Optional[str]
    kernel_ok: Optional[bool]
    audit_actions: List[str]
    entry_id: Optional[str]
    detail: Any = None

    def to_json(self) -> dict:
        return {
            "ok": self.ok,
            "stage": self.stage,
            "request_hash": self.request_hash,
            "kernel_ok": self.kernel_ok,
            "audit_actions": list(self.audit_actions),
            "entry_id": self.entry_id,
        }


def record_proof(
    claim: Union[ProofClaim, Mapping[str, Any]],
    deps: LeanDeps,
    approval: Optional[ApprovalToken] = None,
    *,
    session_id: str,
    data_as_of: str,
    approved_at_clock: Optional[Callable[[], str]] = None,
) -> RecordResult:
    """End to end. ``approved_at_clock`` supplies the ledger entry's
    ``recorded_at``; when omitted the approval token's ``approved_at`` is
    used, so a replay with the same token records the same entry id."""
    log = deps.audit_log
    start = len(log.entries)

    def actions() -> List[str]:
        return [e["action"] for e in log.entries[start:]]

    # 1. Shape.
    claim_json = claim.to_json() if isinstance(claim, ProofClaim) else dict(claim)
    shape: ClaimShape = validate_claim_shape(claim_json)
    if not shape.ok or shape.claim is None:
        return RecordResult(False, "claim_shape", None, None, [], None, {"errors": shape.errors})
    c = shape.claim
    log.append("proof_claim", "lean.claim", session_id, c.to_json(), model_lineage=c.model_lineage)

    # 2. Kernel disposes inside the envelope.
    p = prepare(c, deps.kernel, data_as_of=data_as_of, confidence_floor=deps.confidence_floor, axiom_allowlist=deps.axiom_allowlist)
    log.append(
        "kernel_verdict",
        LEAN_OPERATION,
        session_id,
        {"request_hash": p.request_hash, "proof_file_hash": p.proof_file_hash, "verdict": p.verdict.to_json()},
    )

    # 3. Rules.
    log.append("verifier_check", LEAN_OPERATION, session_id, {"request_hash": p.request_hash, "report": p.report.to_json()})
    if not p.report.ok:
        stage = "kernel" if not p.verdict.ok else "verifier"
        return RecordResult(False, stage, p.request_hash, p.verdict.ok, actions(), None, p.report.to_json())

    # 4. Gate.
    areq = p.approval_request(session_id)
    if approval is None:
        log.append(
            "approval_denied", LEAN_OPERATION, session_id, {"request_hash": p.request_hash, "reason": "no_approval_token", "summary": p.summary}
        )
        return RecordResult(False, "approval", p.request_hash, p.verdict.ok, actions(), None, {"reason": "no_approval_token", "summary": p.summary})
    verdict = verify_approval(approval, deps.trusted_approvers, areq)
    if not verdict.ok:
        log.append(
            "approval_denied", LEAN_OPERATION, session_id, {"request_hash": p.request_hash, "reason": verdict.reason}, approver=approval.approver_id
        )
        return RecordResult(False, "approval", p.request_hash, p.verdict.ok, actions(), None, {"reason": verdict.reason})
    log.append(
        "approval_granted",
        LEAN_OPERATION,
        session_id,
        {"request_hash": p.request_hash, "approved_at": approval.approved_at},
        approver=approval.approver_id,
    )

    # 5. Record.
    recorded_at = approved_at_clock() if approved_at_clock else approval.approved_at
    body = {
        "theorem_name": c.theorem_name,
        "statement": c.statement,
        "doc_hash": c.doc_hash,
        "proof_file_hash": p.proof_file_hash,
        "request_hash": p.request_hash,
        "toolchain": c.toolchain,
        "mathlib_rev": c.mathlib_rev,
        "kernel": p.verdict.to_json(),
        "model_lineage": c.model_lineage,
        "prompt_hash": c.prompt_hash,
        "approver": approval.approver_id,
        "approved_at": approval.approved_at,
        "recorded_at": recorded_at,
    }
    entry_id = deps.ledger.append(body)
    log.append("proof_recorded", LEAN_OPERATION, session_id, {"request_hash": p.request_hash, "entry_id": entry_id}, approver=approval.approver_id)
    return RecordResult(True, None, p.request_hash, p.verdict.ok, actions(), entry_id)
