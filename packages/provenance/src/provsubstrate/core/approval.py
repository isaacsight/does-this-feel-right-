"""Signed human approval at material gates.

A token binds an approver identity to the *exact* envelope they saw (its
request hash, the summary line they read, the session, the materiality
class) and a timestamp. HMAC-SHA256 over the canonical signing input,
byte-compatible with the kbot-finance reference. Verification refuses on any
field mismatch, an unknown approver, a wrong secret, a forged or short
signature, or an altered timestamp — and says which.
"""

from __future__ import annotations

import hmac
import hashlib
from dataclasses import dataclass, asdict
from typing import Mapping, Optional

from .canonical import canonicalize


@dataclass(frozen=True)
class ApprovalRequest:
    request_hash: str
    summary: str
    session_id: str
    materiality: str


@dataclass(frozen=True)
class ApprovalToken:
    request_hash: str
    summary: str
    session_id: str
    materiality: str
    approver_id: str
    approved_at: str
    signature: str

    def to_json(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_json(d: Mapping) -> "ApprovalToken":
        return ApprovalToken(
            d["request_hash"], d["summary"], d["session_id"], d["materiality"], d["approver_id"], d["approved_at"], d["signature"]
        )


def signing_input(req: ApprovalRequest, approver_id: str, approved_at: str) -> str:
    return canonicalize(
        {
            "approved_at": approved_at,
            "approver_id": approver_id,
            "materiality": req.materiality,
            "request_hash": req.request_hash,
            "session_id": req.session_id,
            "summary": req.summary,
        }
    )


class Approver:
    def __init__(self, approver_id: str, secret: bytes):
        self.approver_id = approver_id
        self._secret = secret

    def approve(self, request: ApprovalRequest, approved_at: str) -> ApprovalToken:
        """``approved_at`` is required: no clock is read in this package."""
        sig = hmac.new(self._secret, signing_input(request, self.approver_id, approved_at).encode("utf-8"), hashlib.sha256).hexdigest()
        return ApprovalToken(
            request.request_hash, request.summary, request.session_id, request.materiality, self.approver_id, approved_at, sig
        )


@dataclass(frozen=True)
class Verdict:
    ok: bool
    reason: Optional[str] = None


def verify_approval(token: ApprovalToken, trusted: Mapping[str, bytes], request: ApprovalRequest) -> Verdict:
    if token.request_hash != request.request_hash:
        return Verdict(False, "request_hash_mismatch")
    if token.session_id != request.session_id:
        return Verdict(False, "session_id_mismatch")
    if token.materiality != request.materiality:
        return Verdict(False, "materiality_mismatch")
    if token.summary != request.summary:
        return Verdict(False, "summary_mismatch")
    secret = trusted.get(token.approver_id)
    if secret is None:
        return Verdict(False, "unknown_approver")
    expected = hmac.new(secret, signing_input(request, token.approver_id, token.approved_at).encode("utf-8"), hashlib.sha256).hexdigest()
    try:
        a = bytes.fromhex(token.signature)
    except ValueError:
        return Verdict(False, "bad_signature")
    b = bytes.fromhex(expected)
    if len(a) != len(b) or not hmac.compare_digest(a, b):
        return Verdict(False, "bad_signature")
    return Verdict(True, None)
