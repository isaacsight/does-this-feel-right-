"""Peer-review provenance data model.

A ``ReviewSubmission`` is the claim of this wedge: a reviewer's text and
recommendation about a sealed manuscript, with an explicit AI-contribution
disclosure carrying ``model_lineage`` and the ``prompt_hash``. The
manuscript is identified by ``doc_hash`` — the chain never needs the
manuscript bytes, only their hash. Timestamps are passed in.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Mapping, Optional

from ..core.envelope import content_hash, sha256_text

HEX64 = re.compile(r"^[0-9a-f]{64}$")
RECOMMENDATIONS = ("accept", "minor", "major", "reject")
AI_SCOPES = ("none", "language", "summary", "substantive")
ENTRY_KINDS = ("submitted", "reviewed", "editor_decision", "author_response")


@dataclass(frozen=True)
class Manuscript:
    title: str
    doc_hash: str
    venue: str
    round: int

    def to_json(self) -> dict:
        return {"title": self.title, "doc_hash": self.doc_hash, "venue": self.venue, "round": self.round}

    @staticmethod
    def from_json(d: Mapping) -> "Manuscript":
        return Manuscript(d["title"], d["doc_hash"], d["venue"], int(d["round"]))


@dataclass(frozen=True)
class AIContribution:
    used: bool
    model_lineage: List[dict] = field(default_factory=list)
    prompt_hash: Optional[str] = None
    scope: str = "none"
    disclosed_text: str = ""

    def to_json(self) -> dict:
        return {
            "used": self.used,
            "model_lineage": [{"model": m.get("model"), "version": m.get("version")} for m in self.model_lineage],
            "prompt_hash": self.prompt_hash,
            "scope": self.scope,
            "disclosed_text": self.disclosed_text,
        }

    @staticmethod
    def from_json(d: Mapping) -> "AIContribution":
        return AIContribution(
            bool(d.get("used", False)), [dict(m) for m in d.get("model_lineage") or []], d.get("prompt_hash"), d.get("scope", "none"), d.get("disclosed_text", ""),
        )

    @staticmethod
    def none() -> "AIContribution":
        return AIContribution(False, [], None, "none", "")


@dataclass(frozen=True)
class ReviewSubmission:
    manuscript: Manuscript
    reviewer_id: str
    review_text: str
    recommendation: str
    ai_contribution: AIContribution
    timestamp: str

    def to_json(self) -> dict:
        return {
            "manuscript": self.manuscript.to_json(),
            "reviewer_id": self.reviewer_id,
            "review_text": self.review_text,
            "recommendation": self.recommendation,
            "ai_contribution": self.ai_contribution.to_json(),
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_json(d: Mapping) -> "ReviewSubmission":
        return ReviewSubmission(
            Manuscript.from_json(d["manuscript"]), d["reviewer_id"], d.get("review_text", ""), d.get("recommendation", ""),
            AIContribution.from_json(d.get("ai_contribution") or {}), d["timestamp"],
        )

    @property
    def review_hash(self) -> str:
        """SHA-256 of the review text: what the chain and receipts carry
        instead of the text itself."""
        return sha256_text(self.review_text)

    def submission_hash(self) -> str:
        return content_hash(self.to_json())


@dataclass(frozen=True)
class DisclosureVerdict:
    ok: bool
    code: Optional[str] = None
    codes: List[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return {"ok": self.ok, "code": self.code, "codes": list(self.codes)}
