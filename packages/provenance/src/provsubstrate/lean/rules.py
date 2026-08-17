"""Rules-as-code for recording a proof.

Every applicable rule runs — no short-circuit — so the audit chain carries
the whole evaluation, not the first failure. Each check reports
``{rule_id, pass, code|null}``; the codes are the reason strings a
mathematician or a referee reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence

from .claim import ProofClaim, statement_hash
from .kernel import KernelVerdict

DEFAULT_AXIOM_ALLOWLIST: Sequence[str] = ("propext", "Classical.choice", "Quot.sound")
DEFAULT_CONFIDENCE_FLOOR = 0.6

KERNEL_REJECTED = "KERNEL_REJECTED"
CONTAINS_SORRY = "CONTAINS_SORRY"
FORBIDDEN_AXIOM = "FORBIDDEN_AXIOM"
CONFIDENCE_BELOW_FLOOR = "CONFIDENCE_BELOW_FLOOR"
STATEMENT_HASH_MISMATCH = "STATEMENT_HASH_MISMATCH"
TOOLCHAIN_UNPINNED = "TOOLCHAIN_UNPINNED"


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


def run_lean_rules(
    claim: ProofClaim,
    verdict: KernelVerdict,
    *,
    confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR,
    axiom_allowlist: Sequence[str] = DEFAULT_AXIOM_ALLOWLIST,
) -> RuleReport:
    """Fixed order; conformance vectors pin it."""
    allow = set(axiom_allowlist)
    forbidden = sorted(a for a in verdict.axioms if a not in allow)
    checks = [
        RuleCheck("rule.lean.kernel", verdict.ok, None if verdict.ok else KERNEL_REJECTED),
        RuleCheck("rule.lean.no_sorry", verdict.sorries == 0, None if verdict.sorries == 0 else CONTAINS_SORRY),
        RuleCheck("rule.lean.axiom_allowlist", not forbidden, None if not forbidden else FORBIDDEN_AXIOM),
        RuleCheck(
            "rule.lean.confidence_floor",
            claim.confidence >= confidence_floor,
            None if claim.confidence >= confidence_floor else CONFIDENCE_BELOW_FLOOR,
        ),
        RuleCheck(
            "rule.lean.statement_hash",
            claim.doc_hash == statement_hash(claim.statement),
            None if claim.doc_hash == statement_hash(claim.statement) else STATEMENT_HASH_MISMATCH,
        ),
        RuleCheck("rule.lean.toolchain_pinned", bool(claim.toolchain), None if claim.toolchain else TOOLCHAIN_UNPINNED),
    ]
    return RuleReport(all(c.passed for c in checks), checks)
