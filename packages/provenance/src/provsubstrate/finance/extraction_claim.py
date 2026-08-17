"""Extraction claims.

When a model reads a source document and returns "vendor X, total 1,240.50,
dated 2026-08-12, looks like fertiliser", that output is a CLAIM. It is not
a ledger entry and it never becomes one directly. It is recorded — with the
model that made it and the document hash it was made from — and then handed
to a deterministic engine that must independently confirm it.

Port of ``kbot-finance/src/ledger/extraction-claim.ts``. Claims are kept as
the plain JSON mappings the model produced: the reference hashes the object
*as received* (extra keys and all) into the request envelope, so wrapping it
in a typed record here would silently change the replay key.

Claim shape (``ExtractionClaim`` in the reference)::

    doc_hash: sha256 hex        direction: "out" | "in"
    vendor: str | None          date: "YYYY-MM-DD" | None
    currency: ISO 4217          subtotal, tax, total: number
    line_items: [{description, quantity, unit_amount, line_amount, account_code, tax_type?}]
    reference: str | None       confidence: number in [0, 1]
    model_lineage: [{model, version}]  (non-empty)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional

from ..core.audit import AppendOnlyAuditLog
from ._js import is_finite_number, is_js_number, js_string, js_string_length

ExtractionClaim = Mapping[str, Any]

_SHA256_HEX = re.compile(r"[0-9a-f]{64}")
_ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


@dataclass(frozen=True)
class ClaimShapeResult:
    ok: bool
    errors: List[str] = field(default_factory=list)
    claim: Optional[ExtractionClaim] = None


def _prop(obj: Any, key: str) -> Any:
    """JavaScript property access on a JSON value: objects yield the member
    or undefined (None here); primitives yield undefined; null throws."""
    if obj is None:
        raise TypeError(f"Cannot read properties of null (reading '{key}')")
    if isinstance(obj, dict):
        return obj.get(key)
    return None


def validate_claim_shape(claim: Any) -> ClaimShapeResult:
    """Structural validation for claims arriving from any model. Pure.

    Error strings are the reference's, verbatim, in the reference's order;
    the conformance runner sorts them before comparing."""
    errors: List[str] = []
    if not isinstance(claim, dict):
        return ClaimShapeResult(False, ["claim is not an object"])
    c = claim
    doc_hash = c.get("doc_hash")
    if not isinstance(doc_hash, str) or not _SHA256_HEX.fullmatch(doc_hash):
        errors.append("doc_hash must be sha256 hex")
    if c.get("direction") != "out" and c.get("direction") != "in":
        errors.append("direction must be out|in")
    currency = c.get("currency")
    if not isinstance(currency, str) or js_string_length(currency) != 3:
        errors.append("currency must be ISO 4217")
    for k in ("subtotal", "tax", "total"):
        if not is_finite_number(c.get(k)):
            errors.append(f"{k} must be finite number")
    line_items = c.get("line_items")
    if not isinstance(line_items, list) or len(line_items) == 0:
        errors.append("line_items must be non-empty")
    else:
        for i, li in enumerate(line_items):
            code = _prop(li, "account_code")
            if not isinstance(code, str) or len(code) == 0:
                errors.append(f"line_items[{i}].account_code missing")
            for k in ("quantity", "unit_amount", "line_amount"):
                if not is_finite_number(_prop(li, k)):
                    errors.append(f"line_items[{i}].{k} must be finite number")
    confidence = c.get("confidence")
    if not is_js_number(confidence) or confidence < 0 or confidence > 1:
        errors.append("confidence must be in [0,1]")
    lineage = c.get("model_lineage")
    if not isinstance(lineage, list) or len(lineage) == 0:
        errors.append("model_lineage required")
    date = c.get("date")
    if date is not None and not _ISO_DATE.fullmatch(js_string(date)):
        errors.append("date must be YYYY-MM-DD or null")
    if errors:
        return ClaimShapeResult(False, errors)
    return ClaimShapeResult(True, [], c)


def record_extraction_claim(audit_log: AppendOnlyAuditLog, session_id: str, claim: ExtractionClaim) -> dict:
    """Record a claim in the audit log. Returns the entry so the caller can
    carry its self_hash forward into the reconciliation envelope."""
    return audit_log.append(
        "extraction_claim",
        "ledger.extract",
        session_id,
        claim,
        model_lineage=claim.get("model_lineage"),
    )
