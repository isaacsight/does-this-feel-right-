"""Per-manuscript review chain.

An append-only hash chain over ``{kind, actor, payload}`` entries using the
core chain primitives (``self_hash = sha256(canonical(entry without
self_hash))``, ``prev_hash`` links, genesis zeros). The chain opens with a
``submitted`` entry that pins the manuscript's ``doc_hash``; every later
entry (``reviewed``, ``editor_decision``, ``author_response``) chains to it.
Review text never enters the chain — only its hash — so the chain can be
shared with authors and editors without leaking a confidential review.
Loaded entries are kept verbatim so ``verify`` sees tampering.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Mapping, Optional, Sequence

from ..core.audit import GENESIS_HASH, AuditEntryInput, ChainVerdict, audit_entry_hash, chain_entries, verify_chain
from .model import ENTRY_KINDS, Manuscript


def _subject(doc_hash: str) -> str:
    return f"manuscript:{doc_hash}"


@dataclass(frozen=True)
class ReviewChainVerdict:
    ok: bool
    broken_at_seq: Optional[int] = None
    reason: Optional[str] = None  # "chain" | "not_open" | "bad_kind"

    def to_json(self) -> dict:
        return {"ok": self.ok, "broken_at_seq": self.broken_at_seq, "reason": self.reason}


def verify_review_chain(entries: Sequence[Mapping]) -> ReviewChainVerdict:
    """Core chain verification plus the review-specific shape: the first
    entry must be ``submitted`` and every kind must be a known kind."""
    v: ChainVerdict = verify_chain(list(entries))
    if not v.ok:
        return ReviewChainVerdict(False, v.broken_at_seq, "chain")
    if not entries or entries[0].get("action") != "submitted":
        return ReviewChainVerdict(False, 0, "not_open")
    for e in entries:
        if e.get("action") not in ENTRY_KINDS:
            return ReviewChainVerdict(False, e.get("seq"), "bad_kind")
    return ReviewChainVerdict(True)


def build_review_chain(session_id: str, items: Sequence[Mapping]) -> List[dict]:
    """Pure: chain ``[{kind, actor, payload, timestamp}]`` from genesis. What
    the ``review_chain`` conformance kind pins."""
    inputs = []
    doc_hash: Optional[str] = None
    for it in items:
        if it["kind"] == "submitted" and doc_hash is None:
            doc_hash = it["payload"]["doc_hash"]
        inputs.append(
            AuditEntryInput(
                it["kind"], _subject(doc_hash or ""), session_id, it["payload"], it["timestamp"], it.get("model_lineage"), it.get("approver"),
                {"actor": it["actor"]},
            )
        )
    return chain_entries(inputs)


class ReviewChain:
    """In-memory chain for one manuscript. ``session_id`` is the venue or
    editorial session the chain belongs to; timestamps are passed to
    ``append``."""

    def __init__(self, session_id: str, entries: Optional[Sequence[Mapping]] = None):
        self.session_id = session_id
        self.entries: List[dict] = [dict(e) for e in (entries or [])]

    @staticmethod
    def open(session_id: str, manuscript: Manuscript, actor: str, timestamp: str) -> "ReviewChain":
        c = ReviewChain(session_id)
        c.append("submitted", actor, manuscript.to_json(), timestamp)
        return c

    def append(self, kind: str, actor: str, payload, timestamp: str, *, model_lineage=None, approver=None) -> dict:
        if kind not in ENTRY_KINDS:
            raise ValueError(f"ReviewChain: unknown entry kind {kind!r}")
        doc_hash = self.manuscript_doc_hash()
        if doc_hash is None:
            if kind != "submitted":
                raise ValueError("ReviewChain: chain must be opened with a 'submitted' entry first")
            doc_hash = payload["doc_hash"]
        inp = AuditEntryInput(kind, _subject(doc_hash), self.session_id, payload, timestamp, model_lineage, approver, {"actor": actor})
        sk = inp.skeleton(len(self.entries), self.head() or GENESIS_HASH)
        entry = {**sk, "self_hash": audit_entry_hash(sk)}
        self.entries.append(entry)
        return entry

    def head(self) -> Optional[str]:
        return self.entries[-1]["self_hash"] if self.entries else None

    def manuscript_doc_hash(self) -> Optional[str]:
        for e in self.entries:
            if e.get("action") == "submitted":
                return e["payload"].get("doc_hash")
        return None

    def manuscript(self) -> Optional[Manuscript]:
        for e in self.entries:
            if e.get("action") == "submitted":
                return Manuscript.from_json(e["payload"])
        return None

    def reviews(self) -> List[dict]:
        return [e for e in self.entries if e.get("action") == "reviewed"]

    def has_review(self, reviewer_id: str, round: int) -> bool:
        for e in self.reviews():
            p = e.get("payload") or {}
            if p.get("reviewer_id") == reviewer_id and (p.get("manuscript") or {}).get("round") == round:
                return True
        return False

    def verify(self) -> ReviewChainVerdict:
        return verify_review_chain(self.entries)

    def to_json(self) -> dict:
        return {"session_id": self.session_id, "entries": list(self.entries)}

    @staticmethod
    def from_json(d: Mapping) -> "ReviewChain":
        return ReviewChain(d["session_id"], d.get("entries") or [])
