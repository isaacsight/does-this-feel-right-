"""JSON-in / JSON-out operations for the finance wedge, shared by the CLI and
the MCP server.

Only verdict-producing operations live here: reconcile a claim against a
bank feed, and prepare a post (run the full ``ledger_post`` path with no
approval, in memory, to obtain the request hash and the exact summary line
a human would sign). Posting with an approval is CLI-only.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import ContentAddressedRequest
from .engine import LEDGER_ENGINE_VERSION, MemoryLedger, entry_id
from .extraction_claim import validate_claim_shape
from .ledger_post import (
    LEDGER_POST_MATERIALITY,
    LEDGER_SCHEMA_HASH,
    LedgerPostDeps,
    LedgerPostInputs,
    LedgerPostResult,
    approval_summary,
    ledger_post,
)
from .reconcile import DEFAULT_RECONCILE_POLICY, RECONCILE_ENGINE_VERSION, policy_json, reconcile
from .verifier import VerifierContext, make_ledger_rules

DEFAULT_DATA_AS_OF = "1970-01-01T00:00:00.000Z"
DEFAULT_SESSION_ID = "provsub-cli"
DEFAULT_BANK_ACCOUNT_CODE = "bank"
DEFAULT_JURISDICTION = "GLOBAL"


def bank_lines_of(doc: Any) -> list:
    """Accept a bare list or ``{"bank_lines": [...]}``."""
    if isinstance(doc, Mapping) and "bank_lines" in doc:
        return list(doc["bank_lines"])
    if isinstance(doc, list):
        return list(doc)
    raise ValueError("bank feed must be a JSON array of bank lines or {\"bank_lines\": [...]}")


def finance_reconcile(a: Mapping[str, Any]) -> dict:
    """Arithmetic + bank-feed match for one claim. Pure. Includes the
    reconcile envelope's request hash and the approval summary line the
    post would carry."""
    shape = validate_claim_shape(a["claim"])
    if not shape.ok:
        return {"shape": {"ok": False, "errors": list(shape.errors)}}
    claim = shape.claim
    assert claim is not None
    bank_lines = bank_lines_of(a["bank_lines"])
    policy = a.get("policy") if a.get("policy") is not None else DEFAULT_RECONCILE_POLICY
    data_as_of = a.get("data_as_of") or DEFAULT_DATA_AS_OF
    rec = reconcile(claim, bank_lines, policy)
    req = ContentAddressedRequest(
        operation="ledger.reconcile",
        engine_version=RECONCILE_ENGINE_VERSION,
        schema_hash=LEDGER_SCHEMA_HASH,
        inputs={"claim": claim, "bank_lines": bank_lines, "policy": policy_json(policy)},
        data_as_of=data_as_of,
    )
    return {
        "shape": {"ok": True, "errors": []},
        "data_as_of": data_as_of,
        "reconcile_request_hash": req.request_hash(),
        "reconciliation": rec.to_json(),
        "approval_summary": approval_summary(claim, rec),
    }


def build_deps(a: Mapping[str, Any], *, audit_log: AppendOnlyAuditLog, trusted: Mapping[str, bytes], bank_lines: Sequence[Mapping], now: str) -> LedgerPostDeps:
    engine = MemoryLedger(a.get("engine_version") or LEDGER_ENGINE_VERSION, bank_lines, id_of=entry_id, posted_at=now)
    return LedgerPostDeps(
        audit_log=audit_log,
        rules=make_ledger_rules(confidence_floor=a.get("confidence_floor")),
        verifier_context=VerifierContext(a.get("session_id") or DEFAULT_SESSION_ID, a.get("state") or {}, a.get("jurisdiction") or DEFAULT_JURISDICTION),
        trusted_approvers=trusted,
        engine=engine,
        clock=lambda: now,
    )


def post_result_json(r: LedgerPostResult, deps: LedgerPostDeps, *, session_id: str, data_as_of: str) -> dict:
    out: dict = {
        "ok": r.ok,
        "stage": r.stage,
        "request_hash": r.request_hash,
        "materiality": LEDGER_POST_MATERIALITY,
        "session_id": session_id,
        "data_as_of": data_as_of,
        "reconciliation": r.reconciliation.to_json() if r.reconciliation is not None else None,
        "audit_actions": deps.audit_log.actions(),
        "detail": r.detail,
    }
    if isinstance(r.detail, Mapping) and "summary" in r.detail:
        out["summary"] = r.detail["summary"]
    if r.response is not None:
        out["response"] = r.response.to_json()
        out["posted"] = list(deps.engine.posted) if hasattr(deps.engine, "posted") else None
    return out


def finance_prepare_post(a: Mapping[str, Any]) -> dict:
    """Run the whole ledger_post path in memory with no approval. If the
    claim survives reconciliation and the verifier, the result stops at
    the gate and carries ``request_hash`` + ``summary``: exactly what a
    human signs with ``provsub approve``. Nothing is written anywhere."""
    bank_lines = bank_lines_of(a["bank_lines"])
    data_as_of = a.get("data_as_of") or DEFAULT_DATA_AS_OF
    session_id = a.get("session_id") or DEFAULT_SESSION_ID
    now = a.get("now") or data_as_of
    deps = build_deps({**a, "session_id": session_id}, audit_log=AppendOnlyAuditLog(None, clock=lambda: now), trusted={}, bank_lines=bank_lines, now=now)
    inputs = LedgerPostInputs(
        claim=a["claim"],
        bank_lines=bank_lines,
        bank_account_code=a.get("bank_account_code") or DEFAULT_BANK_ACCOUNT_CODE,
        data_as_of=data_as_of,
        policy=a.get("policy"),
        approval=None,
    )
    r = ledger_post(inputs, deps)
    return post_result_json(r, deps, session_id=session_id, data_as_of=data_as_of)


_CLAIM_SCHEMA = {"type": "object", "description": "ExtractionClaim as the model produced it (hashed as received)"}
_BANK_SCHEMA = {"type": "array", "items": {"type": "object"}, "description": "bank feed lines {id, date, direction, amount, currency, counterparty, reference, reconciled}"}
_POLICY_SCHEMA = {"type": "object", "properties": {"amount_tolerance": {"type": "number"}, "date_window_days": {"type": "number"}}}


def mcp_tools() -> list:
    return [
        (
            "finance_reconcile",
            ("Deterministic reconciliation of a model's extraction claim against a bank feed: arithmetic identity, then bank match "
            "(matched | unmatched | ambiguous | arithmetic_mismatch). Returns the reconcile envelope hash and the summary line a post would carry."),
            {
                "type": "object",
                "properties": {"claim": _CLAIM_SCHEMA, "bank_lines": _BANK_SCHEMA, "policy": _POLICY_SCHEMA, "data_as_of": {"type": "string"}},
                "required": ["claim", "bank_lines"],
            },
            finance_reconcile,
        ),
        (
            "finance_prepare_post",
            ("Dry-run the ledger post path (claim shape, reconciliation, verifier rules) in memory with no approval. Returns the request_hash "
            "and the exact summary line a human must sign with `provsub approve`; the model cannot post."),
            {
                "type": "object",
                "properties": {
                    "claim": _CLAIM_SCHEMA,
                    "bank_lines": _BANK_SCHEMA,
                    "policy": _POLICY_SCHEMA,
                    "bank_account_code": {"type": "string"},
                    "state": {"type": "object", "description": "{closed_through?, valid_account_codes?, posted_doc_hashes?}"},
                    "confidence_floor": {"type": "number"},
                    "jurisdiction": {"type": "string"},
                    "engine_version": {"type": "string"},
                    "session_id": {"type": "string"},
                    "data_as_of": {"type": "string"},
                    "now": {"type": "string"},
                },
                "required": ["claim", "bank_lines"],
            },
            finance_prepare_post,
        ),
    ]
