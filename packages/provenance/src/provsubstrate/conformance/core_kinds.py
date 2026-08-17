"""Handlers for the substrate-level kinds of the finance v1 suite — the kinds
that do not depend on any accounting logic and that every wedge in this
package (finance, Lean, claims, repro, bench, review) shares:

  canonicalize, source_document, approval_token, approval_verify,
  ledger_entry_id, audit_chain

The finance-specific kinds live in ``provsubstrate.finance.conformance``.
"""

from __future__ import annotations

from typing import Dict

from ..core.canonical import canonicalize
from ..core.envelope import sha256_text, seal_document, content_hash
from ..core.approval import Approver, ApprovalRequest, ApprovalToken, verify_approval
from ..core.audit import chain_entries, verify_chain
from .runner import Handler, expect_equal


def h_canonicalize(inp, exp):
    c = canonicalize(inp["value"])
    if c != exp["canonical"]:
        return False, f"canonical mismatch: {c}"
    h = sha256_text(c)
    return (True, None) if h == exp["sha256"] else (False, f"sha256 mismatch: {h}")


def h_source_document(inp, exp):
    d = seal_document(inp["text_utf8"].encode("utf-8"), mime=inp.get("mime", ""), label=inp.get("label", ""))
    return expect_equal({"doc_hash": d.doc_hash, "byte_length": d.byte_length}, exp)


def _req(d) -> ApprovalRequest:
    return ApprovalRequest(d["request_hash"], d["summary"], d["session_id"], d["materiality"])


def h_approval_token(inp, exp):
    t = Approver(inp["approver_id"], inp["secret_utf8"].encode("utf-8")).approve(_req(inp["request"]), inp["approved_at"])
    return expect_equal(t.to_json(), exp["token"])


def h_approval_verify(inp, exp):
    trusted = {t["approver_id"]: t["secret_utf8"].encode("utf-8") for t in inp["trusted"]}
    v = verify_approval(ApprovalToken.from_json(inp["token"]), trusted, _req(inp["request"]))
    return expect_equal({"ok": v.ok, "reason": v.reason}, exp)


def h_ledger_entry_id(inp, exp):
    entry = inp["entry"]
    eid = content_hash(entry)
    if eid != exp["entry_id"]:
        return False, f"entry_id mismatch: {eid}"
    c = canonicalize(entry)
    return (True, None) if c == exp["canonical"] else (False, "canonical mismatch")


def h_audit_chain(inp, exp):
    chained = chain_entries(inp["entries"])
    hashes = [{"seq": e["seq"], "prev_hash": e["prev_hash"], "self_hash": e["self_hash"]} for e in chained]
    ok, detail = expect_equal(hashes, exp["hashes"])
    if not ok:
        return False, detail
    if chained[0]["prev_hash"] != exp["genesis"]:
        return False, "genesis mismatch"
    intact = verify_chain(chained)
    if not intact.ok:
        return False, f"intact chain reported broken at {intact.broken_at_seq}"
    t = inp["tamper"]
    tampered = [({**e, "payload": t["payload"]} if e["seq"] == t["seq"] else e) for e in chained]
    r = verify_chain(tampered)
    broken = -1 if r.ok else r.broken_at_seq
    return (True, None) if broken == exp["tampered_broken_at_seq"] else (False, f"tamper detected at {broken}")


CORE_HANDLERS: Dict[str, Handler] = {
    "canonicalize": h_canonicalize,
    "source_document": h_source_document,
    "approval_token": h_approval_token,
    "approval_verify": h_approval_verify,
    "ledger_entry_id": h_ledger_entry_id,
    "audit_chain": h_audit_chain,
}
