"""Deterministic reconciliation engine.

Takes a model's extraction claim and the bank feed and decides — with
arithmetic, not judgement — whether the claim is confirmed. Pure function of
its inputs: same claim + same bank lines + same policy = same result, byte
for byte. That is what lets the envelope be marked
``byte_identical_replayable`` and what lets an auditor rerun it.

Two independent checks:

1. Arithmetic identity — the document must agree with itself.
   sum(line_amount) == subtotal, subtotal + tax == total, and each line's
   quantity * unit_amount == line_amount, all within tolerance. A model that
   misreads a digit fails here before it touches the bank.

2. Bank-feed match — an unreconciled bank line must exist with the same
   direction, an amount within tolerance, and a date within the window.
   Exactly one such line = matched. None = unmatched. Several = ambiguous
   (the human, not the model, picks).

Port of ``kbot-finance/src/ledger/reconcile.ts``. Float arithmetic follows
the reference operation for operation (JS doubles are Python floats); the
rounding helper is ``Math.round``, not Python's banker's ``round``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional, Sequence, Union

from ._js import js_number_of, js_round, js_sort_key

RECONCILE_ENGINE_VERSION = "ledger-reconcile@0.1.0"

BankLine = Mapping[str, Any]
"""``{id, date: "YYYY-MM-DD"|None, direction: "out"|"in", amount, currency: str|None,
counterparty: str|None, reference: str|None, reconciled: bool}`` — kept as the
plain mapping the feed supplied so it hashes into envelopes unchanged."""


@dataclass(frozen=True)
class ReconcilePolicy:
    amount_tolerance: float
    """Absolute tolerance in currency units, e.g. 0.01."""
    date_window_days: float
    """Days either side of the claimed date a bank line may sit."""

    def to_json(self) -> dict:
        return {"amount_tolerance": self.amount_tolerance, "date_window_days": self.date_window_days}


DEFAULT_RECONCILE_POLICY = ReconcilePolicy(amount_tolerance=0.01, date_window_days=5)

PolicyLike = Union[ReconcilePolicy, Mapping[str, Any]]


def policy_json(policy: PolicyLike) -> Mapping[str, Any]:
    """The reference passes the policy object straight through into the
    result, so a mapping is echoed as-is (extra keys included)."""
    return policy.to_json() if isinstance(policy, ReconcilePolicy) else policy


@dataclass(frozen=True)
class ArithmeticCheck:
    ok: bool
    line_sum: float
    claimed_subtotal: float
    claimed_total: float
    computed_total: float
    bad_lines: List[int] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "ok": self.ok,
            "line_sum": self.line_sum,
            "claimed_subtotal": self.claimed_subtotal,
            "claimed_total": self.claimed_total,
            "computed_total": self.computed_total,
            "bad_lines": list(self.bad_lines),
        }


ReconcileStatus = str  # "matched" | "unmatched" | "ambiguous" | "arithmetic_mismatch"


@dataclass(frozen=True)
class ReconcileResult:
    status: ReconcileStatus
    arithmetic: ArithmeticCheck
    candidates: List[str]
    """Bank line ids that matched within policy, sorted."""
    matched_bank_line_id: Optional[str]
    """The single confirmed bank line id when status == "matched"."""
    policy: Mapping[str, Any]

    def to_json(self) -> dict:
        return {
            "status": self.status,
            "arithmetic": self.arithmetic.to_json(),
            "candidates": list(self.candidates),
            "matched_bank_line_id": self.matched_bank_line_id,
            "policy": dict(self.policy),
        }


def _round2(n: float) -> float:
    return js_round(n * 100) / 100


def check_arithmetic(claim: Mapping[str, Any], tol: float) -> ArithmeticCheck:
    bad_lines: List[int] = []
    line_sum = 0.0
    for i, li in enumerate(claim["line_items"]):
        expected = float(li["quantity"]) * float(li["unit_amount"])
        if abs(expected - float(li["line_amount"])) > tol:
            bad_lines.append(i)
        line_sum += float(li["line_amount"])
    line_sum = _round2(line_sum)
    computed_total = _round2(float(claim["subtotal"]) + float(claim["tax"]))
    ok = len(bad_lines) == 0 and abs(line_sum - float(claim["subtotal"])) <= tol and abs(computed_total - float(claim["total"])) <= tol
    return ArithmeticCheck(
        ok=ok,
        line_sum=line_sum,
        claimed_subtotal=claim["subtotal"],
        claimed_total=claim["total"],
        computed_total=computed_total,
        bad_lines=bad_lines,
    )


def _days_from_civil(y: int, m: int, d: int) -> int:
    """Days since 1970-01-01 for a proleptic Gregorian date; month may be
    any integer (JS ``Date.UTC`` normalises overflow the same way)."""
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    y -= m <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def day_number(iso_date: str) -> float:
    """Whole days since epoch for a YYYY-MM-DD string. Timezone-free by
    construction. Mirrors ``Math.floor(Date.UTC(y, m - 1, d) / 86_400_000)``,
    including its tolerance of missing parts and day overflow."""
    parts = iso_date.split("-")
    y = js_number_of(parts[0]) if len(parts) > 0 else 1970.0
    m = js_number_of(parts[1]) if len(parts) > 1 else 1.0
    d = js_number_of(parts[2]) if len(parts) > 2 else 1.0
    if not (math.isfinite(y) and math.isfinite(m) and math.isfinite(d)):
        return math.nan
    yi, mi, di = int(y), int(m), int(d)
    if 0 <= yi <= 99:
        yi += 1900  # Date.UTC two-digit-year rule
    return float(_days_from_civil(yi, mi, 1) + di - 1)


def reconcile(claim: Mapping[str, Any], bank_lines: Sequence[BankLine], policy: PolicyLike = DEFAULT_RECONCILE_POLICY) -> ReconcileResult:
    pol = policy_json(policy)
    tol = pol["amount_tolerance"]
    window = pol["date_window_days"]
    arithmetic = check_arithmetic(claim, tol)
    if not arithmetic.ok:
        return ReconcileResult("arithmetic_mismatch", arithmetic, [], None, pol)

    claim_day = day_number(claim["date"]) if claim.get("date") else None
    total = float(claim["total"])
    candidates: List[str] = []
    for line in bank_lines:
        if line["reconciled"]:
            continue
        if line["direction"] != claim["direction"]:
            continue
        # `l.currency === null || l.currency === claim.currency`: a feed line
        # with no currency key at all is undefined in JS and never matches.
        if "currency" not in line or not (line["currency"] is None or line["currency"] == claim["currency"]):
            continue
        if not (abs(float(line["amount"]) - total) <= tol):
            continue
        if claim_day is not None and line["date"] is not None:
            if not (abs(day_number(line["date"]) - claim_day) <= window):
                continue
        candidates.append(line["id"])
    candidates.sort(key=js_sort_key)

    if len(candidates) == 1:
        return ReconcileResult("matched", arithmetic, candidates, candidates[0], pol)
    if len(candidates) == 0:
        return ReconcileResult("unmatched", arithmetic, candidates, None, pol)
    return ReconcileResult("ambiguous", arithmetic, candidates, None, pol)
