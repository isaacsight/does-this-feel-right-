"""The whole finance v1 suite — 143 vectors across 13 kinds — must pass
byte-for-byte. This is the proof that the Python ledger substrate is the
same substrate as the TypeScript reference, not a rewrite that happens to
look similar. Two negative controls (mirroring the reference's own test)
show the vectors actually bite: an implementation that auto-picks the first
candidate when ambiguous fails exactly the ambiguity vectors, and one that
forgets to sort keys fails every hash-bearing kind it touches."""

import json
import os
from dataclasses import replace

from provsubstrate.conformance.core_kinds import CORE_HANDLERS
from provsubstrate.conformance.runner import run_conformance
from provsubstrate.core.envelope import sha256_text
from provsubstrate.finance import (
    ALL_FINANCE_V1_HANDLERS,
    FINANCE_HANDLERS,
    LEDGER_SCHEMA_HASH,
    make_finance_handlers,
    reconcile,
)

VECTORS = os.path.join(os.path.dirname(__file__), "..", "src", "provsubstrate", "conformance", "vectors_finance_v1")

ALL_KINDS = {
    "canonicalize", "source_document", "approval_token", "approval_verify", "ledger_entry_id", "audit_chain",
    "claim_shape", "arithmetic", "reconcile", "reconcile_envelope", "ledger_rules", "approval_summary", "ledger_post",
}


def test_all_finance_v1_vectors_pass():
    r = run_conformance(VECTORS, ALL_FINANCE_V1_HANDLERS)
    assert r.manifest_ok
    assert r.failed == 0, [(x.path, x.detail) for x in r.results if x.status == "fail"]
    assert r.skipped == 0
    assert r.passed == 143
    assert r.total == 143
    assert set(r.kinds_claimed) == ALL_KINDS
    assert set(FINANCE_HANDLERS) == {"claim_shape", "arithmetic", "reconcile", "reconcile_envelope", "ledger_rules", "approval_summary", "ledger_post"}


def test_ledger_schema_hash_matches_manifest_pin():
    with open(os.path.join(VECTORS, "manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    assert LEDGER_SCHEMA_HASH == manifest["reference_versions"]["ledger_schema_hash"]


def test_negative_control_auto_pick_when_ambiguous_fails_exactly_the_ambiguity_vectors():
    # A tempting shortcut: pick the first candidate when ambiguous.
    def broken_reconcile(claim, bank_lines, policy):
        r = reconcile(claim, bank_lines, policy)
        if r.status == "ambiguous":
            return replace(r, status="matched", matched_bank_line_id=r.candidates[0] if r.candidates else None)
        return r

    handlers = {**CORE_HANDLERS, **make_finance_handlers(reconcile_fn=broken_reconcile)}
    r = run_conformance(VECTORS, handlers)
    failed = sorted(x.path for x in r.results if x.status == "fail")
    assert "reconcile/ambiguous_two.json" in failed
    assert "reconcile/ambiguous_three_sorted_ids.json" in failed
    assert "reconcile_envelope/ambiguous_two.json" in failed
    # Only ambiguity vectors fail; everything else still passes.
    assert all(("ambiguous" in p) for p in failed), failed
    assert r.passed > r.total - 5


def test_negative_control_unsorted_keys_fails_every_hash_bearing_kind():
    def unsorted_canonicalize(v):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))

    def unsorted_request_hash(*, operation, engine_version, schema_hash, inputs, data_as_of, deterministic_seed=None):
        return sha256_text(unsorted_canonicalize({"operation": operation, "engine_version": engine_version, "schema_hash": schema_hash, "inputs": inputs, "data_as_of": data_as_of}))

    def h_canonicalize(inp, exp):
        c = unsorted_canonicalize(inp["value"])
        return (c == exp["canonical"] and sha256_text(c) == exp["sha256"], c)

    def h_ledger_entry_id(inp, exp):
        return (sha256_text(unsorted_canonicalize(inp["entry"])) == exp["entry_id"], None)

    handlers = {
        **CORE_HANDLERS,
        **make_finance_handlers(request_hash_fn=unsorted_request_hash),
        "canonicalize": h_canonicalize,
        "ledger_entry_id": h_ledger_entry_id,
    }
    r = run_conformance(VECTORS, handlers)
    failed_kinds = {x.kind for x in r.results if x.status == "fail"}
    assert "canonicalize" in failed_kinds
    assert "ledger_entry_id" in failed_kinds
    assert "reconcile_envelope" in failed_kinds
