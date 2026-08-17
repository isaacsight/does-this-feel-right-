"""The disposer: submission shape, the AI-disclosure check, and the rules
that run against the manuscript's chain before a review is recorded.

``validate_submission`` is structural (sorted error strings, nothing
logged). ``ai_disclosure_check`` is the content rule set over the
submission itself; ``code`` is the first failing code in a fixed order and
``codes`` lists them all. ``run_review_rules`` runs every applicable rule
against the chain (open, intact, same manuscript, not a duplicate) plus the
disclosure verdict, without short-circuit, mirroring the finance verifier.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from .chain import ReviewChain, verify_review_chain
from .model import AI_SCOPES, HEX64, RECOMMENDATIONS, DisclosureVerdict, ReviewSubmission


def validate_submission(sub: ReviewSubmission) -> List[str]:
    errors: List[str] = []
    m = sub.manuscript
    if not isinstance(m.title, str) or not m.title.strip():
        errors.append("manuscript.title: empty")
    if not isinstance(m.doc_hash, str) or not HEX64.match(m.doc_hash):
        errors.append("manuscript.doc_hash: not a sha256 hex")
    if not isinstance(m.venue, str) or not m.venue.strip():
        errors.append("manuscript.venue: empty")
    if not isinstance(m.round, int) or isinstance(m.round, bool) or m.round < 1:
        errors.append("manuscript.round: must be an integer >= 1")
    if not isinstance(sub.reviewer_id, str) or not sub.reviewer_id.strip():
        errors.append("reviewer_id: empty")
    if not isinstance(sub.review_text, str):
        errors.append("review_text: must be a string")
    if not isinstance(sub.recommendation, str):
        errors.append("recommendation: must be a string")
    elif sub.recommendation and sub.recommendation not in RECOMMENDATIONS:
        errors.append(f"recommendation: unknown {sub.recommendation!r}")
    ai = sub.ai_contribution
    if ai.scope not in AI_SCOPES:
        errors.append(f"ai_contribution.scope: unknown {ai.scope!r}")
    if ai.prompt_hash is not None and (not isinstance(ai.prompt_hash, str) or not HEX64.match(ai.prompt_hash)):
        errors.append("ai_contribution.prompt_hash: not a sha256 hex")
    for i, ml in enumerate(ai.model_lineage):
        if not isinstance(ml, dict) or not ml.get("model") or not ml.get("version"):
            errors.append(f"ai_contribution.model_lineage[{i}]: needs model and version")
    if not isinstance(sub.timestamp, str) or not sub.timestamp:
        errors.append("timestamp: empty")
    return sorted(errors)


DISCLOSURE_CODES = ("MANUSCRIPT_HASH_MISMATCH", "EMPTY_REVIEW", "MISSING_RECOMMENDATION", "UNDISCLOSED_AI", "SUBSTANTIVE_AI_NO_LINEAGE")


def ai_disclosure_check(sub: ReviewSubmission, manuscript_hash: Optional[str] = None) -> DisclosureVerdict:
    """Content rules over the submission. ``manuscript_hash`` is the hash of
    the manuscript bytes the venue holds; when given it must equal what the
    reviewer says they reviewed."""
    codes: List[str] = []
    if manuscript_hash is not None and sub.manuscript.doc_hash != manuscript_hash:
        codes.append("MANUSCRIPT_HASH_MISMATCH")
    if not sub.review_text.strip():
        codes.append("EMPTY_REVIEW")
    if sub.recommendation not in RECOMMENDATIONS:
        codes.append("MISSING_RECOMMENDATION")
    ai = sub.ai_contribution
    if ai.used and (ai.scope == "none" or not ai.disclosed_text.strip()):
        codes.append("UNDISCLOSED_AI")
    if ai.used and ai.scope == "substantive" and (not ai.model_lineage or not ai.prompt_hash):
        codes.append("SUBSTANTIVE_AI_NO_LINEAGE")
    ordered = [c for c in DISCLOSURE_CODES if c in codes]
    return DisclosureVerdict(not ordered, ordered[0] if ordered else None, ordered)


def _rule_chain(sub, chain, disclosure):
    if chain is None or not chain.entries:
        return False, "CHAIN_NOT_OPEN"
    v = verify_review_chain(chain.entries)
    if not v.ok:
        return False, "CHAIN_BROKEN" if v.reason == "chain" else "CHAIN_NOT_OPEN"
    return True, None


def _rule_manuscript(sub, chain, disclosure):
    if chain is None or chain.manuscript_doc_hash() is None:
        return False, "MANUSCRIPT_HASH_MISMATCH"
    return chain.manuscript_doc_hash() == sub.manuscript.doc_hash, "MANUSCRIPT_HASH_MISMATCH"


def _rule_duplicate(sub, chain, disclosure):
    if chain is None:
        return True, None
    return not chain.has_review(sub.reviewer_id, sub.manuscript.round), "DUPLICATE_REVIEW"


def _rule_disclosure(sub, chain, disclosure):
    return disclosure.ok, disclosure.code


REVIEW_RULES: Tuple[Tuple[str, object], ...] = (
    ("rule.review.chain", _rule_chain),
    ("rule.review.manuscript", _rule_manuscript),
    ("rule.review.duplicate", _rule_duplicate),
    ("rule.review.disclosure", _rule_disclosure),
)


def run_review_rules(sub: ReviewSubmission, chain: Optional[ReviewChain], disclosure: DisclosureVerdict) -> dict:
    checks = []
    for rule_id, fn in REVIEW_RULES:
        ok, code = fn(sub, chain, disclosure)  # type: ignore[operator]
        checks.append({"rule_id": rule_id, "pass": True} if ok else {"rule_id": rule_id, "pass": False, "code": code})
    return {"ok": all(c["pass"] for c in checks), "checks": checks}
