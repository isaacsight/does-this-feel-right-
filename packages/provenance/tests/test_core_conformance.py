"""The core kinds of the finance v1 suite must pass byte-for-byte. This is the
proof that the Python substrate is the same substrate as the TypeScript
reference, not a rewrite that happens to look similar."""

import os

from provsubstrate.conformance.runner import run_conformance
from provsubstrate.conformance.core_kinds import CORE_HANDLERS
from provsubstrate.core import canonicalize, Approver, ApprovalRequest, verify_approval, chain_entries, verify_chain

VECTORS = os.path.join(os.path.dirname(__file__), "..", "src", "provsubstrate", "conformance", "vectors_finance_v1")


def test_core_kinds_pass_finance_v1():
    r = run_conformance(VECTORS, CORE_HANDLERS)
    assert r.manifest_ok
    assert r.failed == 0, [(x.path, x.detail) for x in r.results if x.status == "fail"]
    assert r.passed == 33
    assert set(r.kinds_claimed) == {"canonicalize", "source_document", "approval_token", "approval_verify", "ledger_entry_id", "audit_chain"}


def test_js_number_formatting():
    assert canonicalize({"a": 1e21, "b": 1e-7, "c": 1.0, "d": -0.0, "e": 0.000001, "f": 123456789012345680000.0}) == \
        '{"a":1e+21,"b":1e-7,"c":1,"d":0,"e":0.000001,"f":123456789012345680000}'
    assert canonicalize(1e-6) == "0.000001"
    assert canonicalize(1.5e300) == "1.5e+300"
    assert canonicalize(2.5e-8) == "2.5e-8"


def test_negative_controls_unsorted_keys_would_fail():
    # An implementation that forgets to sort keys produces a different hash.
    a = canonicalize({"b": 1, "a": 2})
    assert a == '{"a":2,"b":1}'


def test_approval_binds_every_field():
    req = ApprovalRequest("f" * 64, "post 1 entry", "s", "ledger.post")
    tok = Approver("pi.ada", b"secret").approve(req, "2026-08-17T12:00:00.000Z")
    assert verify_approval(tok, {"pi.ada": b"secret"}, req).ok
    assert verify_approval(tok, {"pi.ada": b"other"}, req).reason == "bad_signature"
    assert verify_approval(tok, {}, req).reason == "unknown_approver"
    other = ApprovalRequest("e" * 64, "post 1 entry", "s", "ledger.post")
    assert verify_approval(tok, {"pi.ada": b"secret"}, other).reason == "request_hash_mismatch"


def test_chain_tamper_detected():
    entries = chain_entries([
        {"action": "a", "subject": "s", "session_id": "x", "timestamp": "2026-08-17T00:00:01.000Z", "payload": {"n": 1}},
        {"action": "b", "subject": "s", "session_id": "x", "timestamp": "2026-08-17T00:00:02.000Z", "payload": {"n": 2}},
        {"action": "c", "subject": "s", "session_id": "x", "timestamp": "2026-08-17T00:00:03.000Z", "payload": {"n": 3}},
    ])
    assert verify_chain(entries).ok
    tampered = [dict(e) for e in entries]
    tampered[1]["payload"] = {"n": 99}
    assert verify_chain(tampered).broken_at_seq == 1
