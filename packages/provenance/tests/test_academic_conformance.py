"""The academic v1 suite is generated from this implementation and must not
drift: regenerate in memory, diff against disk, and pass every vector."""

import importlib

from provsubstrate.conformance import run_conformance, ACADEMIC_V1_DIR
from provsubstrate.conformance.generate import check, WEDGES

EXPECTED_KINDS = {
    "lean_claim_shape", "lean_proof_file_hash", "lean_rules", "lean_approval_summary", "lean_record",
    "claim_manifest_hash", "claim_manifest_shape", "claim_verify", "claim_rules", "claim_attest",
    "repro_target_hash", "repro_judge", "repro_rules", "repro_approval_summary", "repro_record", "repro_dataset_manifest",
    "bench_taskset_hash", "bench_score", "bench_report_hash",
    "review_shape", "review_disclosure", "review_chain", "review_approval_summary", "review_record",
}


def _handlers():
    h = {}
    for name in WEDGES:
        h.update(importlib.import_module(f"provsubstrate.{name}").CONFORMANCE_HANDLERS)
    return h


def test_academic_v1_no_drift():
    ok, problems = check()
    assert ok, problems


def test_academic_v1_all_pass_and_all_kinds_claimed():
    r = run_conformance(ACADEMIC_V1_DIR, _handlers())
    assert r.manifest_ok
    assert r.failed == 0, [(x.path, x.detail) for x in r.results if x.status == "fail"]
    assert r.skipped == 0
    assert set(r.kinds_claimed) == EXPECTED_KINDS
    assert r.total == 167


def test_suite_hash_is_pinned():
    # Bumping this number is a deliberate act: it means the reference behaviour changed.
    r = run_conformance(ACADEMIC_V1_DIR, _handlers())
    assert r.suite_hash == "880744c3325c92279da369d68ce3bc6dc2deeee917373f59e739db9b6448395f"
