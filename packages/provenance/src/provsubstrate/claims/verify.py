"""Verdicts and rules-as-code for claims.

``verify_claim`` is deterministic float arithmetic:
``|observed - value| <= tolerance`` confirms, otherwise mismatch; a failed
run or a changed input never becomes a number. Rules run in a fixed order,
all of them, and report ``{rule_id, pass, code|null}``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .model import Claim, Computation
from .reexec import ExecutionResult

DEFAULT_CONFIDENCE_FLOOR = 0.6

CONFIRMED = "confirmed"
MISMATCH = "mismatch"
EXECUTION_FAILED = "execution_failed"
INPUT_HASH_MISMATCH_STATUS = "input_hash_mismatch"

UNCONFIRMED_CLAIM = "UNCONFIRMED_CLAIM"
TOLERANCE_EXCEEDED = "TOLERANCE_EXCEEDED"
DANGLING_COMPUTATION = "DANGLING_COMPUTATION"
ENVIRONMENT_UNPINNED = "ENVIRONMENT_UNPINNED"
CONFIDENCE_BELOW_FLOOR = "CONFIDENCE_BELOW_FLOOR"


@dataclass(frozen=True)
class ClaimVerdict:
    status: str  # confirmed | mismatch | execution_failed | input_hash_mismatch
    observed: Optional[float]
    delta: Optional[float]  # observed - value, signed

    def to_json(self) -> dict:
        return {"status": self.status, "observed": self.observed, "delta": self.delta}

    @staticmethod
    def from_json(d) -> "ClaimVerdict":
        return ClaimVerdict(d["status"], d.get("observed"), d.get("delta"))


def verify_claim(claim: Claim, computation: Optional[Computation], result: Optional[ExecutionResult], tolerance: Optional[float] = None) -> ClaimVerdict:
    """``tolerance`` overrides the claim's own when given. A missing
    computation or result is an execution failure: nothing was observed."""
    if computation is None or result is None:
        return ClaimVerdict(EXECUTION_FAILED, None, None)
    if result.input_mismatches:
        return ClaimVerdict(INPUT_HASH_MISMATCH_STATUS, None, None)
    if not result.ok or result.output_value is None:
        return ClaimVerdict(EXECUTION_FAILED, None, None)
    tol = claim.tolerance if tolerance is None else tolerance
    observed = float(result.output_value)
    delta = observed - float(claim.value)
    status = CONFIRMED if abs(delta) <= tol else MISMATCH
    return ClaimVerdict(status, observed, delta)


@dataclass(frozen=True)
class RuleCheck:
    rule_id: str
    passed: bool
    code: Optional[str]

    def to_json(self) -> dict:
        return {"rule_id": self.rule_id, "pass": self.passed, "code": self.code}


@dataclass(frozen=True)
class RuleReport:
    ok: bool
    checks: List[RuleCheck]

    def to_json(self) -> dict:
        return {"ok": self.ok, "checks": [c.to_json() for c in self.checks]}

    def codes(self) -> List[str]:
        return [c.code for c in self.checks if c.code]


def environment_pinned(computation: Optional[Computation]) -> bool:
    """Pinned means: a non-empty python version and a version string for
    every listed package. Nothing is auto-detected."""
    if computation is None:
        return False
    env = computation.environment or {}
    py = env.get("python")
    if not isinstance(py, str) or not py.strip():
        return False
    pk = env.get("packages", {})
    if not isinstance(pk, dict):
        return False
    return all(isinstance(v, str) and v.strip() for v in pk.values())


def run_claim_rules(
    claim: Claim,
    computation: Optional[Computation],
    verdict: Optional[ClaimVerdict],
    *,
    confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR,
) -> RuleReport:
    """Fixed order; conformance vectors pin it."""
    dangling = computation is None
    status = verdict.status if verdict is not None else None
    unconfirmed = status not in (CONFIRMED, MISMATCH)  # never observed a number
    exceeded = status == MISMATCH
    pinned = environment_pinned(computation)
    conf_ok = claim.confidence >= confidence_floor
    checks = [
        RuleCheck("rule.claims.computation_linked", not dangling, None if not dangling else DANGLING_COMPUTATION),
        RuleCheck("rule.claims.confirmed", not unconfirmed, None if not unconfirmed else UNCONFIRMED_CLAIM),
        RuleCheck("rule.claims.tolerance", not exceeded, None if not exceeded else TOLERANCE_EXCEEDED),
        RuleCheck("rule.claims.environment_pinned", pinned, None if pinned else ENVIRONMENT_UNPINNED),
        RuleCheck("rule.claims.confidence_floor", conf_ok, None if conf_ok else CONFIDENCE_BELOW_FLOOR),
    ]
    return RuleReport(all(c.passed for c in checks), checks)
