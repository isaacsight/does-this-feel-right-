"""JSON-in / JSON-out operations for the review wedge, shared by the CLI and
the MCP server: check a submission (shape, AI-disclosure verdict, rules
against the manuscript's chain when given, envelope, the editor's summary
line) and verify a chain. Recording with an approval is CLI-only.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .chain import ReviewChain, verify_review_chain
from .checks import ai_disclosure_check, run_review_rules, validate_submission
from .ledger import REVIEW_MATERIALITY, approval_summary, review_request
from .model import ReviewSubmission

DEFAULT_DATA_AS_OF = "1970-01-01T00:00:00.000Z"
DEFAULT_SESSION_ID = "provsub-cli"


def chain_of(a: Mapping[str, Any], session_id: str) -> ReviewChain | None:
    c = a.get("chain")
    if c is None:
        return None
    if isinstance(c, Mapping) and "entries" in c:
        return ReviewChain.from_json(c)
    if isinstance(c, list):
        return ReviewChain(session_id, c)
    raise ValueError("chain must be {session_id, entries} or a list of chain entries")


def review_check(a: Mapping[str, Any]) -> dict:
    """Shape, disclosure, rules (when a chain is given), envelope hash and
    the exact line the editor signs. Records nothing."""
    sub = ReviewSubmission.from_json(a["submission"])
    errors = validate_submission(sub)
    if errors:
        return {"shape": {"ok": False, "errors": errors}}
    session_id = a.get("session_id") or DEFAULT_SESSION_ID
    data_as_of = a.get("data_as_of") or DEFAULT_DATA_AS_OF
    chain = chain_of(a, session_id)
    disclosure = ai_disclosure_check(sub, a.get("manuscript_hash"))
    head = chain.head() if chain is not None else None
    request_hash = review_request(sub, head, data_as_of).request_hash()
    report = run_review_rules(sub, chain, disclosure) if chain is not None else None
    ok = disclosure.ok and (report is None or report["ok"])
    return {
        "shape": {"ok": True, "errors": []},
        "submission_hash": sub.submission_hash(),
        "review_hash": sub.review_hash,
        "disclosure": disclosure.to_json(),
        "chain_head": head,
        "chain_verdict": chain.verify().to_json() if chain is not None else None,
        "report": report,
        "ok": ok,
        "data_as_of": data_as_of,
        "session_id": session_id,
        "materiality": REVIEW_MATERIALITY,
        "request_hash": request_hash,
        "summary": approval_summary(sub, request_hash),
    }


def review_chain_verify(a: Mapping[str, Any]) -> dict:
    """Core hash-chain check plus the review shape (opens with submitted,
    known kinds). Reports the manuscript hash and the reviews on it."""
    entries = a["chain"]["entries"] if isinstance(a.get("chain"), Mapping) and "entries" in a["chain"] else a["chain"]
    v = verify_review_chain(list(entries))
    chain = ReviewChain("", entries)
    return {
        "verdict": v.to_json(),
        "length": len(entries),
        "head": chain.head(),
        "manuscript_doc_hash": chain.manuscript_doc_hash(),
        "reviews": [{"seq": e["seq"], "reviewer_id": (e.get("payload") or {}).get("reviewer_id"), "round": ((e.get("payload") or {}).get("manuscript") or {}).get("round")} for e in chain.reviews()],
    }


_SUB = {"type": "object", "description": "ReviewSubmission: manuscript{title, doc_hash, venue, round}, reviewer_id, review_text, recommendation, ai_contribution, timestamp"}
_CHAIN = {"description": "the manuscript's review chain: {session_id, entries} or a list of entries"}


def mcp_tools() -> list:
    return [
        (
            "review_check",
            ("Deterministic checks dispose: submission shape, the AI-contribution disclosure verdict, rules against the manuscript's chain when given "
            "(open, intact, same manuscript, not a duplicate), and the request_hash + exact summary line the editor must sign with `provsub approve`. Records nothing."),
            {
                "type": "object",
                "properties": {"submission": _SUB, "chain": _CHAIN, "manuscript_hash": {"type": "string"}, "data_as_of": {"type": "string"}, "session_id": {"type": "string"}},
                "required": ["submission"],
            },
            review_check,
        ),
        (
            "review_chain_verify",
            "Verify a per-manuscript review chain (hash chain intact, opened with submitted, known kinds) and list the reviews on it. Pure.",
            {"type": "object", "properties": {"chain": _CHAIN}, "required": ["chain"]},
            review_chain_verify,
        ),
    ]
