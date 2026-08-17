"""The disposer: attempt shape, the deterministic judge, and rules-as-code.

``judge`` compares what the runner extracted against what the paper claims,
claim by claim, with the paper's own tolerance. Differences are taken in
decimal over the shortest round-trip repr of each float, so ``0.86 - 0.85``
is exactly ``0.01`` and a tolerance of ``0.01`` admits it — the same trap
the finance wedge guards against with cents. Rules run every applicable
check without short-circuit so the audit entry records the full evaluation.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import List, Tuple

from .model import (
    GIT_COMMIT,
    HEX64,
    ClaimVerdict,
    ReproductionAttempt,
    ReproductionTarget,
    ReproVerdict,
    RunRecord,
)


def _dec(x) -> Decimal:
    return Decimal(repr(float(x)))


def decimal_delta(observed: float, expected: float) -> float:
    return float(_dec(observed) - _dec(expected))


def within_tolerance(observed: float, expected: float, tolerance: float) -> bool:
    return abs(_dec(observed) - _dec(expected)) <= _dec(tolerance)


def validate_attempt(target: ReproductionTarget, attempt: ReproductionAttempt) -> List[str]:
    """Structural checks on the model's proposal. Sorted error strings; empty
    means well-formed. Nothing is logged for a malformed attempt."""
    errors: List[str] = []
    if attempt.target_hash != target.target_hash():
        errors.append("target_hash: does not match target")
    if attempt.doc_hash != target.paper.doc_hash:
        errors.append("doc_hash: does not match paper")
    if not attempt.model_lineage:
        errors.append("model_lineage: empty")
    else:
        for i, m in enumerate(attempt.model_lineage):
            if not isinstance(m, dict) or not m.get("model") or not m.get("version"):
                errors.append(f"model_lineage[{i}]: needs model and version")
    if not isinstance(attempt.prompt_hash, str) or not HEX64.match(attempt.prompt_hash):
        errors.append("prompt_hash: not a sha256 hex")
    if not attempt.commands:
        errors.append("commands: empty")
    for i, cmd in enumerate(attempt.commands):
        if not cmd or not all(isinstance(x, str) and x for x in cmd):
            errors.append(f"commands[{i}]: must be a non-empty list of non-empty strings")
    seen = set()
    for i, sel in enumerate(attempt.selectors):
        if target.claim(sel.claim_id) is None:
            errors.append(f"selectors[{i}].claim_id: unknown claim {sel.claim_id!r}")
        if sel.claim_id in seen:
            errors.append(f"selectors[{i}].claim_id: duplicate {sel.claim_id!r}")
        seen.add(sel.claim_id)
        if not (0 <= sel.command_index < len(attempt.commands)):
            errors.append(f"selectors[{i}].command_index: out of range")
        try:
            rx = re.compile(sel.pattern, re.MULTILINE)
            if sel.group < 0 or sel.group > rx.groups:
                errors.append(f"selectors[{i}].group: out of range")
        except re.error:
            errors.append(f"selectors[{i}].pattern: invalid regex")
    try:
        conf = float(attempt.confidence)
        if not (0.0 <= conf <= 1.0):
            errors.append("confidence: must be within [0, 1]")
    except (TypeError, ValueError):
        errors.append("confidence: must be a number")
    return sorted(errors)


def judge(target: ReproductionTarget, attempt: ReproductionAttempt, run_record: RunRecord) -> ReproVerdict:
    """Deterministic verdict. Per claim: ``confirmed`` when
    ``|observed - value| <= tolerance``, ``mismatch`` otherwise, ``missing``
    when nothing was extracted. Overall: ``could_not_run`` if the run failed;
    else ``reproduced`` when every claim is confirmed, ``not_reproduced`` when
    none is (or there are no claims), ``partially_reproduced`` between."""
    per: List[ClaimVerdict] = []
    for c in target.claims:
        observed = run_record.extracted.get(c.claim_id)
        if observed is None:
            per.append(ClaimVerdict(c.claim_id, "missing", None, None))
            continue
        try:
            delta = decimal_delta(observed, c.value)
            ok = within_tolerance(observed, c.value, c.tolerance)
        except (InvalidOperation, ValueError, TypeError):
            per.append(ClaimVerdict(c.claim_id, "missing", None, None))
            continue
        per.append(ClaimVerdict(c.claim_id, "confirmed" if ok else "mismatch", observed, delta))
    if not run_record.succeeded:
        overall = "could_not_run"
    else:
        confirmed = sum(1 for p in per if p.status == "confirmed")
        if not per or confirmed == 0:
            overall = "not_reproduced"
        elif confirmed == len(per):
            overall = "reproduced"
        else:
            overall = "partially_reproduced"
    return ReproVerdict(overall, tuple(per))


# ---- rules -----------------------------------------------------------------

def _rule_commit_pinned(target, attempt, verdict, floor):
    ok = isinstance(target.repo.commit, str) and bool(GIT_COMMIT.match(target.repo.commit))
    return ok, "NO_COMMIT_PINNED"


def _rule_environment_pinned(target, attempt, verdict, floor):
    env = target.environment_spec
    ok = bool(env) and all(isinstance(k, str) and k and isinstance(v, str) and v for k, v in env.items())
    return ok, "ENVIRONMENT_UNPINNED"


def _rule_claims_present(target, attempt, verdict, floor):
    return len(target.claims) > 0, "ZERO_CLAIMS"


def _rule_run_succeeded(target, attempt, verdict, floor):
    return verdict.overall != "could_not_run", "RUN_FAILED"


def _rule_claims_agree(target, attempt, verdict, floor):
    return all(p.status != "mismatch" for p in verdict.per_claim), "CLAIM_MISMATCH"


def _rule_confidence_floor(target, attempt, verdict, floor):
    return float(attempt.confidence) >= float(floor), "CONFIDENCE_BELOW_FLOOR"


REPRO_RULES: Tuple[Tuple[str, object], ...] = (
    ("rule.repro.commit_pinned", _rule_commit_pinned),
    ("rule.repro.environment_pinned", _rule_environment_pinned),
    ("rule.repro.claims_present", _rule_claims_present),
    ("rule.repro.run_succeeded", _rule_run_succeeded),
    ("rule.repro.claims_agree", _rule_claims_agree),
    ("rule.repro.confidence_floor", _rule_confidence_floor),
)


def run_repro_rules(target: ReproductionTarget, attempt: ReproductionAttempt, verdict: ReproVerdict, confidence_floor: float = 0.6) -> dict:
    """Every rule runs; the report lists ``{rule_id, pass, code}`` in fixed
    order (``code`` only when failing), mirroring the finance verifier."""
    checks = []
    for rule_id, fn in REPRO_RULES:
        ok, code = fn(target, attempt, verdict, confidence_floor)  # type: ignore[operator]
        checks.append({"rule_id": rule_id, "pass": bool(ok)} if ok else {"rule_id": rule_id, "pass": False, "code": code})
    return {"ok": all(c["pass"] for c in checks), "checks": checks}
