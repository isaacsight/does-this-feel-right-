"""Envelope, gate, audit sequence, attestation, badge.

``attest_manifest`` is the full path from a manifest of claims to a signed
attestation, every step on the audit chain:

  1. manifest shape; the claims are extracted (``claim_extraction``)
  2. every computation is re-executed by the disposer, each claim gets a
     verdict inside its own ``claims.verify`` envelope (``reexecution``)
  3. rules-as-code per claim (``verifier_check``) — any failure stops here
  4. the corresponding author's signed approval, bound to the attestation
     request hash and to the summary that lists every claim's status
     (``approval_granted`` | ``approval_denied``)
  5. the attestation lands (``attestation_recorded``); ``entry_id`` is its
     content hash

The badge is computed from the verification report and can be shown
whether or not an attestation was recorded; the attestation is the thing a
human signed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Mapping, Optional, Union

from ..core.approval import ApprovalRequest, ApprovalToken, verify_approval
from ..core.audit import AppendOnlyAuditLog
from ..core.canonical import canonicalize
from ..core.envelope import ContentAddressedRequest, content_hash
from .model import Claim, Computation, ManifestShape, manifest_hash, validate_manifest
from .reexec import ExecutionResult, Reexecutor
from .verify import CONFIRMED, DEFAULT_CONFIDENCE_FLOOR, ClaimVerdict, RuleReport, run_claim_rules, verify_claim

CLAIMS_ENGINE_VERSION = "claim-graph@0.1.0"
CLAIMS_VERIFY_OPERATION = "claims.verify"
CLAIMS_ATTEST_OPERATION = "claims.attest"
CLAIMS_ATTEST_MATERIALITY = "claims.attest"

CLAIMS_SCHEMA = {
    "type": "object",
    "fields": {
        "manifest_hash": {"type": "sha256"},
        "claim_id": {"type": "sha256"},
        "computation": {"type": "Computation|null"},
    },
}
CLAIMS_SCHEMA_HASH = content_hash(CLAIMS_SCHEMA)


def verify_request(mhash: str, claim: Claim, computation: Optional[Computation], data_as_of: str) -> ContentAddressedRequest:
    """Per-claim envelope: the replay key for one re-execution."""
    return ContentAddressedRequest(
        operation=CLAIMS_VERIFY_OPERATION,
        engine_version=CLAIMS_ENGINE_VERSION,
        schema_hash=CLAIMS_SCHEMA_HASH,
        inputs={"manifest_hash": mhash, "claim_id": claim.claim_id, "computation": computation.to_json() if computation else None},
        data_as_of=data_as_of,
    )


def _fmt(x: Optional[float]) -> str:
    return "-" if x is None else canonicalize(x)


def approval_summary(claim: Claim, verdict: ClaimVerdict) -> str:
    """One line per claim, exactly what the author signs for it."""
    return (
        f"Claim {claim.claim_id[:12]} = {canonicalize(claim.value)} {claim.unit} tol {canonicalize(claim.tolerance)} "
        f"observed {_fmt(verdict.observed)} delta {_fmt(verdict.delta)} ({verdict.status}) computation {claim.computation_ref[:12]}"
    )


@dataclass(frozen=True)
class ClaimOutcome:
    claim: Claim
    computation: Optional[Computation]
    result: Optional[ExecutionResult]
    verdict: ClaimVerdict
    request_hash: str
    report: RuleReport

    def to_json(self) -> dict:
        return {
            "claim_id": self.claim.claim_id,
            "computation_id": self.computation.computation_id if self.computation else None,
            "request_hash": self.request_hash,
            "verdict": self.verdict.to_json(),
        }


def attestation_summary(mhash: str, title: str, outcomes: List[ClaimOutcome]) -> str:
    """Header plus one line per claim. Multi-line on purpose: the human
    signs the whole list, not a digest of it."""
    confirmed = sum(1 for o in outcomes if o.verdict.status == CONFIRMED)
    head = f'Attest {confirmed}/{len(outcomes)} claims confirmed for "{title}" manifest {mhash[:12]}'
    return "\n".join([head] + [approval_summary(o.claim, o.verdict) for o in outcomes])


def attest_request(mhash: str, outcomes: List[ClaimOutcome], data_as_of: str) -> ContentAddressedRequest:
    """The envelope the human signs: manifest hash plus every per-claim
    verdict and its own request hash."""
    return ContentAddressedRequest(
        operation=CLAIMS_ATTEST_OPERATION,
        engine_version=CLAIMS_ENGINE_VERSION,
        schema_hash=CLAIMS_SCHEMA_HASH,
        inputs={"manifest_hash": mhash, "claims": [o.to_json() for o in outcomes]},
        data_as_of=data_as_of,
    )


def verification_report(mhash: str, outcomes: List[ClaimOutcome]) -> dict:
    """What the badge is built from."""
    counts: Dict[str, int] = {}
    for o in outcomes:
        counts[o.verdict.status] = counts.get(o.verdict.status, 0) + 1
    return {
        "manifest_hash": mhash,
        "total": len(outcomes),
        "confirmed": counts.get(CONFIRMED, 0),
        "counts": dict(sorted(counts.items())),
        "statuses": {o.claim.claim_id: o.verdict.status for o in outcomes},
    }


class AttestationLedger:
    """In-memory, append-only; ``entry_id`` is the content hash of the body."""

    def __init__(self) -> None:
        self.entries: List[dict] = []

    def append(self, body: Mapping[str, Any]) -> str:
        entry_id = content_hash(dict(body))
        self.entries.append({"entry_id": entry_id, **body})
        return entry_id

    def to_json(self) -> List[dict]:
        return [dict(e) for e in self.entries]


@dataclass
class ClaimsDeps:
    reexecutor: Reexecutor
    audit_log: AppendOnlyAuditLog
    ledger: AttestationLedger
    trusted_approvers: Mapping[str, bytes]
    confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR


@dataclass(frozen=True)
class Prepared:
    """Everything deterministic that precedes the gate."""

    shape: ManifestShape
    manifest_hash: str
    title: str
    outcomes: List[ClaimOutcome]
    request: ContentAddressedRequest
    request_hash: str
    summary: str

    @property
    def ok(self) -> bool:
        return all(o.report.ok for o in self.outcomes)

    def approval_request(self, session_id: str) -> ApprovalRequest:
        return ApprovalRequest(self.request_hash, self.summary, session_id, CLAIMS_ATTEST_MATERIALITY)

    def report(self) -> dict:
        return verification_report(self.manifest_hash, self.outcomes)


def prepare(
    manifest: Mapping[str, Any],
    reexecutor: Reexecutor,
    *,
    data_as_of: str,
    results: Optional[Mapping[str, Union[ExecutionResult, Mapping[str, Any]]]] = None,
    confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR,
) -> Prepared:
    """Validate, re-execute (once per computation, unless ``results`` are
    supplied), verify each claim, run rules, build the envelope and the
    summary. Raises ``ValueError`` on a malformed manifest; callers that
    want the shape errors call ``validate_manifest`` first."""
    shape = validate_manifest(manifest)
    if not shape.ok:
        raise ValueError("manifest shape: " + "; ".join(shape.errors))
    mhash = manifest_hash(manifest)
    title = str(manifest["paper"].get("title", ""))
    comps = {c.computation_id: c for c in shape.computations}
    got: Dict[str, ExecutionResult] = {
        k: (v if isinstance(v, ExecutionResult) else ExecutionResult.from_json(v)) for k, v in (results or {}).items()
    }
    outcomes: List[ClaimOutcome] = []
    for claim in shape.claims:
        comp = comps.get(shape.edges.get(claim.claim_id, ""))
        res: Optional[ExecutionResult] = None
        if comp is not None:
            if comp.computation_id not in got:
                got[comp.computation_id] = reexecutor.run(comp)
            res = got[comp.computation_id]
        verdict = verify_claim(claim, comp, res)
        rh = verify_request(mhash, claim, comp, data_as_of).request_hash()
        rep = run_claim_rules(claim, comp, verdict, confidence_floor=confidence_floor)
        outcomes.append(ClaimOutcome(claim, comp, res, verdict, rh, rep))
    req = attest_request(mhash, outcomes, data_as_of)
    return Prepared(shape, mhash, title, outcomes, req, req.request_hash(), attestation_summary(mhash, title, outcomes))


@dataclass(frozen=True)
class AttestResult:
    ok: bool
    stage: Optional[str]  # None | manifest_shape | verifier | approval
    request_hash: Optional[str]
    manifest_hash: Optional[str]
    statuses: Dict[str, str]
    audit_actions: List[str]
    entry_id: Optional[str]
    detail: Any = None

    def to_json(self) -> dict:
        return {
            "ok": self.ok,
            "stage": self.stage,
            "request_hash": self.request_hash,
            "manifest_hash": self.manifest_hash,
            "statuses": dict(self.statuses),
            "audit_actions": list(self.audit_actions),
            "entry_id": self.entry_id,
        }


def _lineage(claims: List[Claim]) -> List[dict]:
    seen: List[dict] = []
    for c in claims:
        for m in c.model_lineage:
            if m not in seen:
                seen.append(dict(m))
    return seen


def attest_manifest(
    manifest: Mapping[str, Any],
    results: Optional[Mapping[str, Union[ExecutionResult, Mapping[str, Any]]]],
    deps: ClaimsDeps,
    approval: Optional[ApprovalToken] = None,
    *,
    session_id: str,
    data_as_of: str,
    approved_at_clock: Optional[Callable[[], str]] = None,
) -> AttestResult:
    """End to end. ``results`` may carry re-execution results already
    obtained (keyed by computation id); anything missing is run through
    ``deps.reexecutor``. ``approved_at_clock`` supplies the entry's
    ``recorded_at``; default is the token's ``approved_at`` so a replay
    records the same entry id."""
    log = deps.audit_log
    start = len(log.entries)

    def actions() -> List[str]:
        return [e["action"] for e in log.entries[start:]]

    # 1. Shape + extraction.
    shape = validate_manifest(manifest)
    if not shape.ok:
        return AttestResult(False, "manifest_shape", None, None, {}, [], None, {"errors": shape.errors})
    mhash = manifest_hash(manifest)
    log.append(
        "claim_extraction",
        "claims.extract",
        session_id,
        {"manifest_hash": mhash, "paper": dict(manifest["paper"]), "claims": [c.to_json() for c in shape.claims]},
        model_lineage=_lineage(shape.claims),
    )

    # 2. Re-execution: the disposer.
    p = prepare(manifest, deps.reexecutor, data_as_of=data_as_of, results=results, confidence_floor=deps.confidence_floor)
    log.append(
        "reexecution",
        CLAIMS_VERIFY_OPERATION,
        session_id,
        {
            "manifest_hash": mhash,
            "claims": [
                {
                    **o.to_json(),
                    "result": None
                    if o.result is None
                    else {"ok": o.result.ok, "exit_code": o.result.exit_code, "output_hash": o.result.output_hash, "output_value": o.result.output_value, "input_mismatches": list(o.result.input_mismatches)},
                }
                for o in p.outcomes
            ],
        },
    )
    statuses = {o.claim.claim_id: o.verdict.status for o in p.outcomes}

    # 3. Rules.
    log.append(
        "verifier_check",
        CLAIMS_ATTEST_OPERATION,
        session_id,
        {"request_hash": p.request_hash, "reports": [{"claim_id": o.claim.claim_id, "report": o.report.to_json()} for o in p.outcomes]},
    )
    if not p.ok:
        return AttestResult(False, "verifier", p.request_hash, mhash, statuses, actions(), None, [{"claim_id": o.claim.claim_id, **o.report.to_json()} for o in p.outcomes if not o.report.ok])

    # 4. Gate.
    areq = p.approval_request(session_id)
    if approval is None:
        log.append("approval_denied", CLAIMS_ATTEST_OPERATION, session_id, {"request_hash": p.request_hash, "reason": "no_approval_token", "summary": p.summary})
        return AttestResult(False, "approval", p.request_hash, mhash, statuses, actions(), None, {"reason": "no_approval_token", "summary": p.summary})
    v = verify_approval(approval, deps.trusted_approvers, areq)
    if not v.ok:
        log.append("approval_denied", CLAIMS_ATTEST_OPERATION, session_id, {"request_hash": p.request_hash, "reason": v.reason}, approver=approval.approver_id)
        return AttestResult(False, "approval", p.request_hash, mhash, statuses, actions(), None, {"reason": v.reason})
    log.append(
        "approval_granted", CLAIMS_ATTEST_OPERATION, session_id, {"request_hash": p.request_hash, "approved_at": approval.approved_at}, approver=approval.approver_id
    )

    # 5. Record.
    recorded_at = approved_at_clock() if approved_at_clock else approval.approved_at
    body = {
        "manifest_hash": mhash,
        "request_hash": p.request_hash,
        "paper": dict(manifest["paper"]),
        "claims": [{"claim_id": o.claim.claim_id, "computation_id": o.computation.computation_id if o.computation else None, "status": o.verdict.status, "observed": o.verdict.observed, "delta": o.verdict.delta, "request_hash": o.request_hash} for o in p.outcomes],
        "model_lineage": _lineage(shape.claims),
        "approver": approval.approver_id,
        "approved_at": approval.approved_at,
        "recorded_at": recorded_at,
    }
    entry_id = deps.ledger.append(body)
    log.append("attestation_recorded", CLAIMS_ATTEST_OPERATION, session_id, {"request_hash": p.request_hash, "entry_id": entry_id}, approver=approval.approver_id)
    return AttestResult(True, None, p.request_hash, mhash, statuses, actions(), entry_id)


# --- badge -----------------------------------------------------------------


def _badge_color(confirmed: int, total: int) -> str:
    if total == 0:
        return "lightgrey"
    if confirmed == total:
        return "brightgreen"
    if confirmed * 2 >= total:
        return "orange"
    return "red"


def badge_json(report: Mapping[str, Any]) -> dict:
    """shields.io endpoint format."""
    confirmed, total = int(report["confirmed"]), int(report["total"])
    return {
        "schemaVersion": 1,
        "label": "claims verified",
        "message": f"{confirmed}/{total} · suite {report['manifest_hash'][:8]}",
        "color": _badge_color(confirmed, total),
    }


_COLORS = {"brightgreen": "#4c1", "orange": "#fe7d37", "red": "#e05d44", "lightgrey": "#9f9f9f"}


def badge_svg(report: Mapping[str, Any]) -> str:
    """Small flat badge, self-contained. Widths are 6.5px per character so
    the bytes are deterministic across platforms (no font measurement)."""
    b = badge_json(report)
    label, msg = b["label"], b["message"]
    lw = int(len(label) * 6.5) + 10
    mw = int(len(msg) * 6.5) + 10
    w = lw + mw
    color = _COLORS[b["color"]]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{label}: {msg}">'
        f"<title>{label}: {msg}</title>"
        f'<rect width="{lw}" height="20" fill="#555"/>'
        f'<rect x="{lw}" width="{mw}" height="20" fill="{color}"/>'
        f'<g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">'
        f'<text x="{lw / 2:g}" y="14">{label}</text>'
        f'<text x="{lw + mw / 2:g}" y="14">{msg}</text>'
        f"</g></svg>"
    )
