"""ledger_post — the full path from a model's reading of a document to a
posted general-ledger entry, with every step on the audit chain.

1. The claim is recorded (``extraction_claim``) with model lineage.
2. The deterministic reconciliation engine runs inside its own
   content-addressed envelope (``byte_identical_replayable: true``) and is
   recorded (``reconciliation``).
3. The ledger verifier runs (``verifier_check``). Any failure stops here
   with a reason code.
4. Posting is material: a signed approval token from a trusted human must
   be present and must bind to THIS request hash. Missing or invalid →
   ``approval_denied``, stop.
5. Only then does the ledger engine post (``engine_request`` /
   ``engine_response``; a throw is an ``incident``).

The model is never on the path between "claim" and "number". The number
that reaches the ledger is the reconciled bank-feed amount, and the human
signed the exact envelope that carried it.

Port of ``kbot-finance/src/tools/ledger-post.ts``. Every dependency is
explicit — audit log, rules, verifier context, trusted approvers, engine,
and a ``clock`` for the envelope's ``produced_at`` — so a run is a replay.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Optional, Sequence

from ..core.approval import ApprovalRequest, ApprovalToken, verify_approval
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import ContentAddressedRequest, ContentAddressedResponse, content_hash, seal_envelope
from ._js import js_to_fixed
from .engine import BankLine, LedgerEngine, LedgerEntry
from .extraction_claim import ExtractionClaim, record_extraction_claim, validate_claim_shape
from .reconcile import DEFAULT_RECONCILE_POLICY, RECONCILE_ENGINE_VERSION, PolicyLike, ReconcileResult, policy_json, reconcile
from .verifier import Rule, VerifierAction, VerifierContext, run_verifier

LEDGER_SCHEMA_HASH = content_hash(
    {
        "type": "object",
        "fields": {
            "claim": {"type": "ExtractionClaim"},
            "reconciliation": {"type": "ReconcileResult"},
            "bank_account_code": {"type": "string"},
        },
    }
)

LEDGER_POST_MATERIALITY = "ledger.post"


@dataclass(frozen=True)
class LedgerPostInputs:
    claim: Any
    """The model's claim, as received. Validated first; hashed as-is."""
    bank_lines: Sequence[BankLine]
    """Bank feed lines the reconciliation engine considers. Usually from ``engine.bank_lines()``."""
    bank_account_code: str
    """Code of the bank/cash account the movement sits in."""
    data_as_of: str
    policy: Optional[PolicyLike] = None
    approval: Optional[ApprovalToken] = None
    """Signed approval. May be omitted on a first call to obtain the request_hash to sign."""


@dataclass
class LedgerPostDeps:
    audit_log: AppendOnlyAuditLog
    rules: Sequence[Rule]
    verifier_context: VerifierContext
    trusted_approvers: Mapping[str, bytes]
    """Trusted approver secrets, keyed by approver_id."""
    engine: LedgerEngine
    """The general ledger underneath. Required — there is no default vendor."""
    clock: Callable[[], str] = field(default=lambda: "1970-01-01T00:00:00.000Z")
    """Supplies ``produced_at`` for sealed envelopes. Passed in, never read."""


@dataclass(frozen=True)
class LedgerPostValue:
    entry_id: str
    matched_bank_line_id: str
    total: float
    currency: str

    def to_json(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "matched_bank_line_id": self.matched_bank_line_id,
            "total": self.total,
            "currency": self.currency,
        }


@dataclass(frozen=True)
class LedgerPostResult:
    ok: bool
    stage: Optional[str] = None
    """On failure: "claim_shape" | "reconciliation" | "verifier" | "approval" | "engine"."""
    request_hash: Optional[str] = None
    """Present from the reconciliation stage on, so an approver can sign it."""
    reconciliation: Optional[ReconcileResult] = None
    detail: Any = None
    response: Optional[ContentAddressedResponse] = None
    """On success: the sealed envelope whose ``value`` is a ``LedgerPostValue`` (as JSON)."""


def approval_summary(claim: ExtractionClaim, rec: ReconcileResult | Mapping[str, Any]) -> str:
    """Human-readable line the approver signs. Deterministic over its inputs."""
    matched = rec.matched_bank_line_id if isinstance(rec, ReconcileResult) else rec.get("matched_bank_line_id")
    direction = "SPEND" if claim["direction"] == "out" else "RECEIVE"
    vendor = claim.get("vendor")
    date = claim.get("date")
    return (
        f"{direction} {claim['currency']} {js_to_fixed(claim['total'], 2)} "
        f"{'(no vendor)' if vendor is None else vendor} {'(no date)' if date is None else date} "
        f"doc:{claim['doc_hash'][:12]} bank:{'-' if matched is None else matched}"
    )


def claim_to_entry(claim: ExtractionClaim, bank_line: BankLine, bank_account_code: str) -> LedgerEntry:
    """Map a confirmed claim onto a vendor-neutral ledger entry. Line detail
    comes from the claim; the total and settlement date come from the bank
    line; the reference carries the source-document hash."""
    line_items = []
    for li in claim["line_items"]:
        item = {
            "description": li["description"],
            "quantity": li["quantity"],
            "unit_amount": li["unit_amount"],
            "account_code": li["account_code"],
        }
        if li.get("tax_type"):
            item["tax_type"] = li["tax_type"]
        line_items.append(item)
    reference = claim.get("reference")
    return {
        "direction": claim["direction"],
        "counterparty": claim.get("vendor"),
        "date": bank_line["date"] if bank_line.get("date") is not None else claim.get("date"),
        "currency": claim["currency"],
        "line_items": line_items,
        "bank_account_code": bank_account_code,
        "bank_line_id": bank_line["id"],
        "reference": f"doc:{claim['doc_hash'][:16]}" + (" " + reference if reference else ""),
        "doc_hash": claim["doc_hash"],
        "total": bank_line["amount"],
    }


def ledger_post(inputs: LedgerPostInputs, deps: LedgerPostDeps) -> LedgerPostResult:
    session_id = deps.verifier_context.session_id
    log = deps.audit_log

    # 1. Claim shape + record.
    shape = validate_claim_shape(inputs.claim)
    if not shape.ok:
        return LedgerPostResult(False, stage="claim_shape", detail={"errors": list(shape.errors)})
    claim = shape.claim
    assert claim is not None
    record_extraction_claim(log, session_id, claim)

    # 2. Deterministic reconciliation in its own envelope.
    policy = inputs.policy if inputs.policy is not None else DEFAULT_RECONCILE_POLICY
    recon_request = ContentAddressedRequest(
        operation="ledger.reconcile",
        engine_version=RECONCILE_ENGINE_VERSION,
        schema_hash=LEDGER_SCHEMA_HASH,
        inputs={"claim": claim, "bank_lines": list(inputs.bank_lines), "policy": policy_json(policy)},
        data_as_of=inputs.data_as_of,
    )
    recon_sealed = seal_envelope(
        recon_request,
        lambda _req: reconcile(claim, inputs.bank_lines, policy),
        produced_at=deps.clock(),
        byte_identical_replayable=True,
    )
    recon: ReconcileResult = recon_sealed.value
    log.append(
        "reconciliation",
        "ledger.reconcile",
        session_id,
        {"request_hash": recon_sealed.request_hash, "result": recon.to_json()},
    )

    # 3. The post request. Its hash is what the human signs.
    request = ContentAddressedRequest(
        operation="ledger.post",
        engine_version=deps.engine.engine_version,
        schema_hash=LEDGER_SCHEMA_HASH,
        inputs={
            "claim": claim,
            "reconciliation": recon.to_json(),
            "reconciliation_request_hash": recon_sealed.request_hash,
            "bank_account_code": inputs.bank_account_code,
        },
        data_as_of=inputs.data_as_of,
    )
    request_hash = request.request_hash()

    verifier_report = run_verifier(
        deps.rules,
        VerifierAction(operation="ledger.post", inputs=request.inputs, materiality="material"),
        deps.verifier_context,
    )
    log.append("verifier_check", "ledger.post", session_id, {"request_hash": request_hash, "report": verifier_report.to_json()})
    if not verifier_report.ok:
        return LedgerPostResult(
            False,
            stage="verifier" if recon.status == "matched" else "reconciliation",
            request_hash=request_hash,
            reconciliation=recon,
            detail=verifier_report.to_json(),
        )

    # 4. Material gate.
    approval_request = ApprovalRequest(
        request_hash=request_hash,
        summary=approval_summary(claim, recon),
        session_id=session_id,
        materiality=LEDGER_POST_MATERIALITY,
    )
    if inputs.approval is None:
        log.append(
            "approval_denied",
            "ledger.post",
            session_id,
            {"request_hash": request_hash, "reason": "no_approval_token", "summary": approval_request.summary},
        )
        return LedgerPostResult(
            False,
            stage="approval",
            request_hash=request_hash,
            reconciliation=recon,
            detail={"reason": "no_approval_token", "summary": approval_request.summary},
        )
    verdict = verify_approval(inputs.approval, deps.trusted_approvers, approval_request)
    if not verdict.ok:
        log.append(
            "approval_denied",
            "ledger.post",
            session_id,
            {"request_hash": request_hash, "reason": verdict.reason},
            approver=inputs.approval.approver_id,
        )
        return LedgerPostResult(False, stage="approval", request_hash=request_hash, reconciliation=recon, detail={"reason": verdict.reason})
    log.append(
        "approval_granted",
        "ledger.post",
        session_id,
        {"request_hash": request_hash, "approved_at": inputs.approval.approved_at},
        approver=inputs.approval.approver_id,
    )

    # 5. Engine.
    log.append("engine_request", "ledger.post", session_id, request.hashable())

    matched = recon.matched_bank_line_id
    bank_line = next((ln for ln in inputs.bank_lines if ln["id"] == matched), None)

    def engine(_req: ContentAddressedRequest) -> dict:
        if bank_line is None:
            raise RuntimeError("ledger.post: matched bank line disappeared")
        entry = claim_to_entry(claim, bank_line, inputs.bank_account_code)
        r = deps.engine.post(entry)
        if not r.ok:
            assert r.error is not None
            raise RuntimeError(f"ledger engine post failed: {r.error.code}: {r.error.message}")
        # The number that lands is the bank feed's, not the model's.
        return LedgerPostValue(r.value.entry_id, bank_line["id"], bank_line["amount"], claim["currency"]).to_json()

    try:
        sealed = seal_envelope(request, engine, produced_at=deps.clock(), byte_identical_replayable=False)
    except Exception as e:  # noqa: BLE001 — any throw on the engine path is an incident, recorded as such
        log.append("incident", "ledger.post", session_id, {"request_hash": request_hash, "error": str(e)})
        return LedgerPostResult(False, stage="engine", request_hash=request_hash, reconciliation=recon, detail={"error": str(e)})

    log.append(
        "engine_response",
        "ledger.post",
        session_id,
        {
            "request_hash": sealed.request_hash,
            "produced_at": sealed.produced_at,
            "entry_id": sealed.value["entry_id"],
            "matched_bank_line_id": sealed.value["matched_bank_line_id"],
            "total": sealed.value["total"],
        },
    )
    return LedgerPostResult(True, request_hash=request_hash, reconciliation=recon, response=sealed)
