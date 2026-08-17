"""Hash-chained append-only audit log.

``self_hash = sha256(canonical(entry without self_hash))``; ``prev_hash``
links; genesis is sixty-four zeros. Tampering with entry *n* breaks
verification at *n*. The pure functions are what conformance vectors pin;
``AppendOnlyAuditLog`` is the JSONL-backed wrapper that supplies ``seq`` and
a caller-provided timestamp.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Sequence

from .canonical import JsonValue, canonicalize
from .envelope import sha256_text

GENESIS_HASH = "0" * 64


def _strip_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


@dataclass(frozen=True)
class AuditEntryInput:
    action: str
    subject: str
    session_id: str
    payload: JsonValue
    timestamp: str
    model_lineage: Optional[list] = None
    approver: Optional[str] = None
    extra: dict = field(default_factory=dict)

    def skeleton(self, seq: int, prev_hash: str) -> dict:
        d = {
            "action": self.action,
            "subject": self.subject,
            "session_id": self.session_id,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "model_lineage": self.model_lineage,
            "approver": self.approver,
            **self.extra,
            "seq": seq,
            "prev_hash": prev_hash,
        }
        return _strip_none(d)

    @staticmethod
    def from_json(d: dict) -> "AuditEntryInput":
        known = {"action", "subject", "session_id", "payload", "timestamp", "model_lineage", "approver", "seq", "prev_hash", "self_hash"}
        return AuditEntryInput(
            d["action"], d["subject"], d["session_id"], d["payload"], d["timestamp"],
            d.get("model_lineage"), d.get("approver"), {k: v for k, v in d.items() if k not in known},
        )


def audit_entry_hash(skeleton: dict) -> str:
    """Hash of an entry excluding ``self_hash``. Pure."""
    return sha256_text(canonicalize(skeleton))


def chain_entries(inputs: Iterable[AuditEntryInput | dict], genesis: str = GENESIS_HASH) -> List[dict]:
    out: List[dict] = []
    prev = genesis
    for seq, inp in enumerate(inputs):
        if isinstance(inp, dict):
            inp = AuditEntryInput.from_json(inp)
        sk = inp.skeleton(seq, prev)
        self_hash = audit_entry_hash(sk)
        out.append({**sk, "self_hash": self_hash})
        prev = self_hash
    return out


@dataclass(frozen=True)
class ChainVerdict:
    ok: bool
    broken_at_seq: Optional[int] = None


def verify_chain(entries: Sequence[dict], genesis: str = GENESIS_HASH) -> ChainVerdict:
    expected_prev = genesis
    expected_seq = 0
    for entry in entries:
        if entry.get("seq") != expected_seq:
            return ChainVerdict(False, expected_seq)
        if entry.get("prev_hash") != expected_prev:
            return ChainVerdict(False, entry["seq"])
        sk = {k: v for k, v in entry.items() if k != "self_hash"}
        if audit_entry_hash(sk) != entry.get("self_hash"):
            return ChainVerdict(False, entry["seq"])
        expected_prev = entry["self_hash"]
        expected_seq += 1
    return ChainVerdict(True)


class AppendOnlyAuditLog:
    """JSONL-backed chain. ``clock`` supplies timestamps so callers control
    determinism (tests pass a fixed sequence)."""

    def __init__(self, path: Optional[str], clock: Callable[[], str]):
        self.path = path
        self._clock = clock
        self._last_hash = GENESIS_HASH
        self._next_seq = 0
        self.entries: List[dict] = []
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lines = [ln for ln in f.read().split("\n") if ln]
            if lines:
                tail = json.loads(lines[-1])
                self._last_hash = tail["self_hash"]
                self._next_seq = tail["seq"] + 1
                self.entries = [json.loads(ln) for ln in lines]

    def append(self, action: str, subject: str, session_id: str, payload: JsonValue, *, model_lineage=None, approver=None, **extra) -> dict:
        inp = AuditEntryInput(action, subject, session_id, payload, self._clock(), model_lineage, approver, extra)
        sk = inp.skeleton(self._next_seq, self._last_hash)
        entry = {**sk, "self_hash": audit_entry_hash(sk)}
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
        self.entries.append(entry)
        self._last_hash = entry["self_hash"]
        self._next_seq += 1
        return entry

    def actions(self) -> List[str]:
        return [e["action"] for e in self.entries]

    def verify(self) -> ChainVerdict:
        return verify_chain(self.entries)


def verify_file(path: str) -> ChainVerdict:
    with open(path, "r", encoding="utf-8") as f:
        entries = [json.loads(ln) for ln in f.read().split("\n") if ln]
    return verify_chain(entries)
