"""Regulatory verifier and the ledger rules.

Every action passes through the verifier before reaching the engine. Rules
are pure functions over (action, context); failures emit a reason code
analogous to ECOA adverse-action notices. Short-circuit is intentionally not
used: every applicable rule runs so audit logs record the full evaluation,
not just the first failure.

Port of ``kbot-finance/src/verifier/index.ts`` and ``verifier/ledger-rules.ts``.
The ledger rules encode bookkeeping discipline, not a jurisdiction's statute,
so all are GLOBAL. Reason codes: ``PERIOD_LOCKED``, ``UNKNOWN_ACCOUNT_CODE``,
``DUPLICATE_SOURCE_DOCUMENT``, ``NOT_RECONCILED``, ``ARITHMETIC_MISMATCH``,
``CONFIDENCE_BELOW_FLOOR``.

Expected ``action.inputs`` shape (see ``ledger_post``)::

    {claim: ExtractionClaim, reconciliation: ReconcileResult (JSON), ...}

Expected ``context.state`` shape::

    {closed_through?: "YYYY-MM-DD", valid_account_codes?: [str], posted_doc_hashes?: [str]}
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Mapping, Optional, Sequence

from ._js import js_string
from .reconcile import day_number

Jurisdiction = str  # "US" | "EU" | "UK" | "SG" | "HK" | "UAE" | "GLOBAL"


@dataclass(frozen=True)
class VerifierAction:
    operation: str
    """Operation, e.g. "ledger.post"."""
    inputs: Any
    """The request payload the agent is asking to execute."""
    materiality: str  # "informational" | "operational" | "material"


@dataclass(frozen=True)
class VerifierContext:
    session_id: str
    state: Any
    """Current positions, exposure, or other state rules may need to inspect."""
    jurisdiction: Jurisdiction
    """Selects the active ruleset."""


@dataclass(frozen=True)
class RuleEvidence:
    code: str
    summary: str
    details: Any

    def to_json(self) -> dict:
        return {"code": self.code, "summary": self.summary, "details": self.details}


@dataclass(frozen=True)
class RuleResult:
    passed: bool
    reason: Optional[RuleEvidence] = None

    def to_json(self) -> dict:
        if self.passed:
            return {"pass": True}
        assert self.reason is not None
        return {"pass": False, "reason": self.reason.to_json()}


PASS = RuleResult(True)


def _fail(code: str, summary: str, details: Any) -> RuleResult:
    return RuleResult(False, RuleEvidence(code, summary, details))


@dataclass(frozen=True)
class Rule:
    id: str
    """Stable identifier, e.g. "rule.ledger.period_lock"."""
    jurisdictions: Sequence[Jurisdiction]
    operations: Sequence[str]
    """Operations the rule cares about. Match-all = "*"."""
    evaluate: Callable[[VerifierAction, VerifierContext], RuleResult]
    """Pure evaluator."""


@dataclass(frozen=True)
class VerifierCheck:
    rule_id: str
    result: RuleResult

    def to_json(self) -> dict:
        return {"rule_id": self.rule_id, "result": self.result.to_json()}


@dataclass(frozen=True)
class VerifierReport:
    ok: bool
    checks: List[VerifierCheck] = field(default_factory=list)

    def to_json(self) -> dict:
        return {"ok": self.ok, "checks": [c.to_json() for c in self.checks]}


def run_verifier(rules: Sequence[Rule], action: VerifierAction, context: VerifierContext) -> VerifierReport:
    """Run all applicable rules and return a structured report."""
    applicable = [
        r
        for r in rules
        if (context.jurisdiction in r.jurisdictions or "GLOBAL" in r.jurisdictions)
        and ("*" in r.operations or action.operation in r.operations)
    ]
    checks = [VerifierCheck(r.id, r.evaluate(action, context)) for r in applicable]
    return VerifierReport(all(c.result.passed for c in checks), checks)


# ---------------------------------------------------------------------------
# Ledger rules
# ---------------------------------------------------------------------------

_OPS = ("ledger.post",)


def _input(action: VerifierAction, key: str) -> Optional[Mapping[str, Any]]:
    """``(action.inputs as LedgerInputs)?.claim`` — absent or non-object is
    treated as undefined; ``{}`` stays truthy as it is in JS."""
    inputs = action.inputs
    v = inputs.get(key) if isinstance(inputs, Mapping) else None
    return v if isinstance(v, Mapping) else None


def _claim_of(action: VerifierAction) -> Optional[Mapping[str, Any]]:
    return _input(action, "claim")


def _reconciliation_of(action: VerifierAction) -> Optional[Mapping[str, Any]]:
    return _input(action, "reconciliation")


def _state(context: VerifierContext) -> Mapping[str, Any]:
    return context.state if isinstance(context.state, Mapping) else {}


def make_period_lock_rule() -> Rule:
    """A document may not be posted into a closed accounting period."""

    def evaluate(action: VerifierAction, context: VerifierContext) -> RuleResult:
        claim = _claim_of(action)
        closed = _state(context).get("closed_through")
        # `!claim?.date || !closed` — a missing, null, or empty date/lock passes.
        if claim is None or not claim.get("date") or not closed:
            return PASS
        if day_number(claim["date"]) <= day_number(closed):
            return _fail(
                "PERIOD_LOCKED",
                f"Document dated {claim['date']} falls in a period closed through {closed}",
                {"claim_date": claim["date"], "closed_through": closed},
            )
        return PASS

    return Rule("rule.ledger.period_lock", ("GLOBAL",), _OPS, evaluate)


def make_account_code_rule() -> Rule:
    """Every proposed account code must exist in the live chart of accounts."""

    def evaluate(action: VerifierAction, context: VerifierContext) -> RuleResult:
        claim = _claim_of(action)
        valid = _state(context).get("valid_account_codes")
        # `!claim || !valid` — an empty chart is truthy in JS and still enforced.
        if claim is None or valid is None:
            return PASS
        known = set(valid)
        unknown = [li["account_code"] for li in claim["line_items"] if li["account_code"] not in known]
        if unknown:
            deduped = list(dict.fromkeys(unknown))
            return _fail(
                "UNKNOWN_ACCOUNT_CODE",
                "Proposed account code(s) not in chart: " + ", ".join(deduped),
                {"unknown": deduped},
            )
        return PASS

    return Rule("rule.ledger.account_code", ("GLOBAL",), _OPS, evaluate)


def make_duplicate_document_rule() -> Rule:
    """The same source document (by content hash) may not be posted twice."""

    def evaluate(action: VerifierAction, context: VerifierContext) -> RuleResult:
        claim = _claim_of(action)
        posted = _state(context).get("posted_doc_hashes")
        if posted is None:
            posted = []
        if claim is None:
            return PASS
        if claim["doc_hash"] in posted:
            return _fail(
                "DUPLICATE_SOURCE_DOCUMENT",
                "A document with identical bytes has already been posted",
                {"doc_hash": claim["doc_hash"]},
            )
        return PASS

    return Rule("rule.ledger.duplicate_document", ("GLOBAL",), _OPS, evaluate)


def make_reconciled_rule() -> Rule:
    """The reconciliation engine must have confirmed the claim."""

    def evaluate(action: VerifierAction, _context: VerifierContext) -> RuleResult:
        rec = _reconciliation_of(action)
        if rec is None:
            return _fail("NOT_RECONCILED", "No reconciliation result attached", None)
        status = rec["status"]
        if status != "matched":
            return _fail(
                "ARITHMETIC_MISMATCH" if status == "arithmetic_mismatch" else "NOT_RECONCILED",
                f"Reconciliation status is {status}",
                {"status": status, "candidates": list(rec["candidates"]), "arithmetic": rec["arithmetic"]},
            )
        return PASS

    return Rule("rule.ledger.reconciled", ("GLOBAL",), _OPS, evaluate)


def make_confidence_floor_rule(minimum: float) -> Rule:
    """Model confidence below the floor is refused regardless of reconciliation."""

    def evaluate(action: VerifierAction, _context: VerifierContext) -> RuleResult:
        claim = _claim_of(action)
        if claim is None:
            return PASS
        if claim["confidence"] < minimum:
            return _fail(
                "CONFIDENCE_BELOW_FLOOR",
                f"Model confidence {js_string(claim['confidence'])} below floor {js_string(minimum)}",
                {"confidence": claim["confidence"], "floor": minimum},
            )
        return PASS

    return Rule("rule.ledger.confidence_floor", ("GLOBAL",), _OPS, evaluate)


def make_ledger_rules(*, confidence_floor: Optional[float] = None) -> List[Rule]:
    """The standard ledger ruleset, in the reference's order."""
    return [
        make_period_lock_rule(),
        make_account_code_rule(),
        make_duplicate_document_rule(),
        make_reconciled_rule(),
        make_confidence_floor_rule(0.6 if confidence_floor is None else confidence_floor),
    ]
