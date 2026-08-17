"""Peer-review provenance: signed review chains with disclosed AI
contribution.

A reviewer submits text + recommendation + an explicit AI-contribution
disclosure about a sealed manuscript; deterministic checks dispose; the
editor signs the exact summary line; a hash-only entry is appended to the
manuscript's chain; the reviewer gets a receipt with hashes and no text.
"""

from .model import AI_SCOPES, ENTRY_KINDS, RECOMMENDATIONS, AIContribution, DisclosureVerdict, Manuscript, ReviewSubmission
from .chain import ReviewChain, ReviewChainVerdict, build_review_chain, verify_review_chain
from .checks import DISCLOSURE_CODES, REVIEW_RULES, ai_disclosure_check, run_review_rules, validate_submission
from .ledger import (
    REVIEW_ENGINE_VERSION,
    REVIEW_MATERIALITY,
    REVIEW_OPERATION,
    REVIEW_SCHEMA_HASH,
    approval_summary,
    record_review,
    review_receipt,
    review_request,
    reviewed_payload,
)
from .conformance import CONFORMANCE_HANDLERS, compute_expected, conformance_cases
from .mcp import mcp_tools, review_chain_verify, review_check

__all__ = [
    "mcp_tools", "review_chain_verify", "review_check",
    "AI_SCOPES", "ENTRY_KINDS", "RECOMMENDATIONS", "AIContribution", "DisclosureVerdict", "Manuscript", "ReviewSubmission",
    "ReviewChain", "ReviewChainVerdict", "build_review_chain", "verify_review_chain",
    "DISCLOSURE_CODES", "REVIEW_RULES", "ai_disclosure_check", "run_review_rules", "validate_submission",
    "REVIEW_ENGINE_VERSION", "REVIEW_MATERIALITY", "REVIEW_OPERATION", "REVIEW_SCHEMA_HASH",
    "approval_summary", "record_review", "review_receipt", "review_request", "reviewed_payload",
    "CONFORMANCE_HANDLERS", "compute_expected", "conformance_cases",
]
