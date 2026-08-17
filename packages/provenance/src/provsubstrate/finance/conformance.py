"""Conformance handlers for the finance-specific kinds of the finance v1 suite:

  claim_shape, arithmetic, reconcile, reconcile_envelope, ledger_rules,
  approval_summary, ledger_post

Each handler mirrors ``evaluateVector`` in the reference runner
(``kbot-finance/src/conformance/run.ts``) — the same inputs are fed to the
same functions and compared the same way (exact for hashes and summary
lines, JSON-equal after canonicalization for structured results). Together
with the substrate kinds in ``conformance.core_kinds`` this is the whole
suite; ``ALL_FINANCE_V1_HANDLERS`` is what a port hands to
``run_conformance``.

``make_finance_handlers`` takes the reconcile and request-hash functions as
parameters so a test can substitute a *wrong* one and confirm the vectors
catch it (the negative controls).
"""

from __future__ import annotations

from typing import Callable, Dict, Optional

from ..conformance.core_kinds import CORE_HANDLERS
from ..conformance.runner import Handler, expect_equal
from ..core.approval import ApprovalRequest, ApprovalToken, Approver
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import request_hash
from .engine import MemoryLedger, entry_id
from .extraction_claim import validate_claim_shape
from .ledger_post import LEDGER_POST_MATERIALITY, LedgerPostDeps, LedgerPostInputs, approval_summary, ledger_post
from .reconcile import check_arithmetic, reconcile
from .verifier import VerifierAction, VerifierContext, make_ledger_rules, run_verifier

ReconcileFn = Callable[..., object]
RequestHashFn = Callable[..., str]

_FIXED_CLOCK = "2026-08-15T00:00:00.000Z"


def run_ledger_rules(inp: dict) -> dict:
    """``runVerifier(makeLedgerRules(opts), action, context)`` flattened to
    per-rule pass + reason code, as the ``ledger_rules`` kind pins it."""
    report = run_verifier(
        make_ledger_rules(confidence_floor=inp["confidence_floor"]),
        VerifierAction("ledger.post", {"claim": inp["claim"], "reconciliation": inp["reconciliation"]}, "material"),
        VerifierContext("conformance", inp["state"], inp["jurisdiction"]),
    )
    return {
        "ok": report.ok,
        "checks": [
            {"rule_id": c.rule_id, "pass": c.result.passed, "code": None if c.result.passed else c.result.reason.code}
            for c in report.checks
        ],
    }


def run_ledger_post_vector(inp: dict) -> dict:
    """The end-to-end flow exactly as the reference conformance adapter
    drives it: an in-memory engine and audit sink; when an approval is
    requested, a dry run yields the request hash to sign, the audit log is
    reset, and the real run's action sequence is what gets reported."""
    engine = MemoryLedger(inp["engine_version"], inp["bank_lines"], fail=inp["engine_fails"], id_of=entry_id)
    trusted = {t["approver_id"]: t["secret_utf8"].encode("utf-8") for t in inp["trusted"]}
    deps = LedgerPostDeps(
        audit_log=AppendOnlyAuditLog(None, lambda: _FIXED_CLOCK),
        rules=make_ledger_rules(confidence_floor=inp["confidence_floor"]),
        verifier_context=VerifierContext(inp["session_id"], inp["state"], inp["jurisdiction"]),
        trusted_approvers=trusted,
        engine=engine,
        clock=lambda: _FIXED_CLOCK,
    )
    base = dict(
        claim=inp["claim"],
        bank_lines=inp["bank_lines"],
        bank_account_code=inp["bank_account_code"],
        data_as_of=inp["data_as_of"],
        policy=inp["policy"],
    )

    approval: Optional[ApprovalToken] = None
    if inp["approval"] != "none":
        dry = ledger_post(LedgerPostInputs(**base), deps)
        if dry.request_hash:
            rec = reconcile(inp["claim"], inp["bank_lines"], inp["policy"])
            req = ApprovalRequest(
                request_hash="f" * 64 if inp["approval"] == "wrong_hash" else dry.request_hash,
                summary=approval_summary(inp["claim"], rec),
                session_id=inp["session_id"],
                materiality=LEDGER_POST_MATERIALITY,
            )
            if inp["approval"] == "unknown_approver":
                signer = {"approver_id": "intern.bob", "secret_utf8": "not-in-the-trust-set"}
            else:
                signer = inp["trusted"][0]
            approval = Approver(signer["approver_id"], signer["secret_utf8"].encode("utf-8")).approve(req, inp["approved_at"])
        # Reset the audit log so the recorded sequence is the real run only.
        deps.audit_log = AppendOnlyAuditLog(None, lambda: _FIXED_CLOCK)

    r = ledger_post(LedgerPostInputs(**base, approval=approval), deps)
    audit_actions = deps.audit_log.actions()
    if r.ok:
        assert r.response is not None
        return {
            "ok": True,
            "stage": None,
            "request_hash": r.request_hash,
            "reconcile_status": "matched",
            "audit_actions": audit_actions,
            "posted_entry_id": r.response.value["entry_id"],
            "posted_total": r.response.value["total"],
        }
    return {
        "ok": False,
        "stage": r.stage,
        "request_hash": r.request_hash,
        "reconcile_status": r.reconciliation.status if r.reconciliation is not None else None,
        "audit_actions": audit_actions,
        "posted_entry_id": None,
        "posted_total": None,
    }


def make_finance_handlers(*, reconcile_fn: ReconcileFn = reconcile, request_hash_fn: RequestHashFn = request_hash) -> Dict[str, Handler]:
    def h_claim_shape(inp, exp):
        r = validate_claim_shape(inp["claim"])
        got = {"ok": True, "errors": []} if r.ok else {"ok": False, "errors": sorted(r.errors)}
        return expect_equal(got, exp)

    def h_arithmetic(inp, exp):
        return expect_equal(check_arithmetic(inp["claim"], inp["tolerance"]).to_json(), exp)

    def h_reconcile(inp, exp):
        return expect_equal(reconcile_fn(inp["claim"], inp["bank_lines"], inp["policy"]).to_json(), exp)

    def h_reconcile_envelope(inp, exp):
        h = request_hash_fn(
            operation=inp["operation"],
            engine_version=inp["engine_version"],
            schema_hash=inp["schema_hash"],
            inputs={"claim": inp["claim"], "bank_lines": inp["bank_lines"], "policy": inp["policy"]},
            data_as_of=inp["data_as_of"],
        )
        if h != exp["request_hash"]:
            return False, f"request_hash mismatch: {h}"
        return expect_equal(reconcile_fn(inp["claim"], inp["bank_lines"], inp["policy"]).to_json(), exp["result"])

    def h_ledger_rules(inp, exp):
        return expect_equal(run_ledger_rules(inp), exp)

    def h_approval_summary(inp, exp):
        s = approval_summary(inp["claim"], inp["reconciliation"])
        return (True, None) if s == exp["summary"] else (False, s)

    def h_ledger_post(inp, exp):
        return expect_equal(run_ledger_post_vector(inp), exp)

    return {
        "claim_shape": h_claim_shape,
        "arithmetic": h_arithmetic,
        "reconcile": h_reconcile,
        "reconcile_envelope": h_reconcile_envelope,
        "ledger_rules": h_ledger_rules,
        "approval_summary": h_approval_summary,
        "ledger_post": h_ledger_post,
    }


FINANCE_HANDLERS: Dict[str, Handler] = make_finance_handlers()

ALL_FINANCE_V1_HANDLERS: Dict[str, Handler] = {**CORE_HANDLERS, **FINANCE_HANDLERS}
