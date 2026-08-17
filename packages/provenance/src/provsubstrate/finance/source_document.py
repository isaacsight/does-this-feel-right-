"""Content-addressed source documents.

A source document — a supplier invoice, a grain delivery ticket, a fuel
receipt, a bank statement page — is the evidence a ledger entry rests on.
Before any model reads it, we hash the bytes. The hash is carried in every
downstream envelope, so two operators extracting from the same bytes produce
the same replay key, a document altered after extraction is detectable, and
the same document cannot be posted twice without tripping the
duplicate-document rule. The bytes stay with the operator; only the hash
travels.

Port of ``kbot-finance/src/ledger/source-document.ts``. ``captured_at`` is
required here: nothing in this package reads a clock.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..core.envelope import sha256_bytes


@dataclass(frozen=True)
class SourceDocument:
    doc_hash: str
    """SHA-256 hex over the raw bytes."""
    byte_length: int
    mime: str
    """MIME type as supplied by the capture path; not sniffed."""
    label: str
    """Operator-supplied label, e.g. "grain-ticket-2026-08-12.pdf". Not hashed."""
    captured_at: str
    """ISO 8601 UTC time the bytes were sealed."""

    def to_json(self) -> dict:
        return {
            "doc_hash": self.doc_hash,
            "byte_length": self.byte_length,
            "mime": self.mime,
            "label": self.label,
            "captured_at": self.captured_at,
        }


def seal_source_document(data: bytes, *, mime: str, label: str, captured_at: str) -> SourceDocument:
    return SourceDocument(sha256_bytes(data), len(data), mime, label, captured_at)


@dataclass(frozen=True)
class SourceDocumentVerdict:
    ok: bool
    reason: Optional[str] = None  # "hash_mismatch" | "length_mismatch"


def verify_source_document(data: bytes, doc: SourceDocument) -> SourceDocumentVerdict:
    """Recompute the hash of ``data`` and compare to a sealed document."""
    if len(data) != doc.byte_length:
        return SourceDocumentVerdict(False, "length_mismatch")
    if sha256_bytes(data) != doc.doc_hash:
        return SourceDocumentVerdict(False, "hash_mismatch")
    return SourceDocumentVerdict(True)
