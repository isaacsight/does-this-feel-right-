"""The ledger engine boundary.

The substrate does not care which general ledger sits underneath. Any
system that can (a) present a bank feed and (b) accept a posted entry can
implement ``LedgerEngine``. The audit chain, the reconciliation engine, the
rules, and the material gate are all above this line and identical
regardless of what is below it.

Port of ``kbot-finance/src/ledger/engine.ts``. The reference ships a
JSONL-backed ``ContentAddressedLedger``; here the shipped engine is
``MemoryLedger`` — the same shape held in memory, with ``posted_at`` passed
in rather than read from a clock — which is what the conformance ``ledger_post``
kind runs against. A ledger entry's id IS the SHA-256 of its canonical JSON,
so no entry can exist without a replay key.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Mapping, Optional, Protocol, Sequence

from ..core.envelope import content_hash

LEDGER_ENGINE_VERSION = "content-addressed-ledger@0.1.0"

BankLine = Mapping[str, Any]

LedgerEntry = Mapping[str, Any]
"""What the substrate hands to an engine to post. Vendor-neutral::

    direction, counterparty, date, currency,
    line_items: [{description, quantity, unit_amount, account_code, tax_type?}],
    bank_account_code, bank_line_id, reference, doc_hash,
    total  (as asserted by the bank feed, not the model)

Built by ``ledger_post.claim_to_entry``; kept as a mapping because its
canonical bytes are its identity."""


@dataclass(frozen=True)
class PostedEntry:
    entry_id: str
    """Engine-assigned identifier for the posted entry."""
    posted_at: str


@dataclass(frozen=True)
class LedgerEngineError:
    code: str  # "network" | "unauthorized" | "validation" | "duplicate" | "io" | "unknown"
    message: str


@dataclass(frozen=True)
class LedgerOutcome:
    ok: bool
    value: Any = None
    error: Optional[LedgerEngineError] = None

    @staticmethod
    def success(value: Any) -> "LedgerOutcome":
        return LedgerOutcome(True, value, None)

    @staticmethod
    def failure(code: str, message: str) -> "LedgerOutcome":
        return LedgerOutcome(False, None, LedgerEngineError(code, message))


class LedgerEngine(Protocol):
    engine_version: str
    """Pinned engine identity carried into every envelope."""

    def bank_lines(self) -> LedgerOutcome:
        """Present the (unreconciled and reconciled) bank feed."""
        ...

    def post(self, entry: LedgerEntry) -> LedgerOutcome:
        """Post an entry. Must be idempotent on identical canonical entries."""
        ...


def entry_id(entry: LedgerEntry) -> str:
    """Deterministic id for an entry: SHA-256 over its canonical JSON."""
    return content_hash(entry)


class MemoryLedger:
    """Minimal in-memory engine. Deterministic: ``posted_at`` is fixed at
    construction, and ``fail=True`` makes every post a network error, which
    is how the conformance suite exercises the incident path."""

    def __init__(
        self,
        engine_version: str,
        feed: Sequence[BankLine],
        *,
        fail: bool = False,
        id_of: Callable[[LedgerEntry], str] = entry_id,
        posted_at: str = "2026-08-15T00:00:00.000Z",
    ):
        self.engine_version = engine_version
        self._feed: List[BankLine] = list(feed)
        self._fail = fail
        self._id_of = id_of
        self._posted_at = posted_at
        self.posted: List[dict] = []

    def bank_lines(self) -> LedgerOutcome:
        return LedgerOutcome.success(list(self._feed))

    def post(self, entry: LedgerEntry) -> LedgerOutcome:
        if self._fail:
            return LedgerOutcome.failure("network", "conformance: engine down")
        eid = self._id_of(entry)
        self.posted.append({"entry": entry, "entry_id": eid})
        self._feed = [({**b, "reconciled": True} if b["id"] == entry["bank_line_id"] else b) for b in self._feed]
        return LedgerOutcome.success(PostedEntry(eid, self._posted_at))
