"""Claim graph: unit tests, a real SubprocessReexecutor run on the example,
and the conformance handlers evaluated against their own compute_expected
(round trip + determinism)."""

import json
import os
import shutil
import sys

import pytest

from provsubstrate.claims import (
    CLAIMS_ATTEST_MATERIALITY,
    CONFORMANCE_HANDLERS,
    AttestationLedger,
    Claim,
    ClaimsDeps,
    ClaimVerdict,
    Computation,
    ExecutionResult,
    StubReexecutor,
    SubprocessReexecutor,
    approval_summary,
    attest_manifest,
    badge_json,
    badge_svg,
    compute_expected,
    conformance_cases,
    extract_value,
    manifest_hash,
    prepare,
    run_claim_rules,
    validate_manifest,
    verify_claim,
)
from provsubstrate.claims.conformance import (
    APPROVED_AT,
    CLAIM_MEAN,
    COMP_MEAN,
    DATA_AS_OF,
    MANIFEST_CLEAN,
    RES_MEAN_OK,
    RESULTS_CLEAN,
    SESSION_ID,
)
from provsubstrate.core import AppendOnlyAuditLog, ApprovalRequest, Approver, verify_chain

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples", "claims")


def _canon(x) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


# --- model -----------------------------------------------------------------


def test_ids_are_content_hashes_and_key_order_irrelevant():
    c = Claim.from_json(CLAIM_MEAN)
    from provsubstrate.core import content_hash

    assert c.claim_id == content_hash(c.body())
    assert Computation.from_json(COMP_MEAN).computation_id == content_hash(Computation.from_json(COMP_MEAN).body())
    shuffled = json.loads(json.dumps(MANIFEST_CLEAN))
    shuffled = {k: shuffled[k] for k in reversed(list(shuffled))}
    assert manifest_hash(shuffled) == manifest_hash(MANIFEST_CLEAN)


def test_validate_manifest_reports_sorted_errors():
    m = json.loads(json.dumps(MANIFEST_CLEAN))
    m["edges"].append({"claim_id": "a" * 64, "computation_id": "b" * 64})
    m["claims"][0]["tolerance"] = -1
    r = validate_manifest(m)
    assert not r.ok
    assert r.errors == sorted(r.errors)
    assert any("dangling edge: claim" in e for e in r.errors)
    assert any("dangling edge: computation" in e for e in r.errors)
    assert any("id does not match body" in e for e in r.errors)  # tolerance change breaks the id too
    assert validate_manifest(MANIFEST_CLEAN).ok


# --- disposer --------------------------------------------------------------


def test_extract_value_selectors():
    assert extract_value('{"mean": 3.5}', "/mean") == 3.5
    assert extract_value('{"a": [1, {"b": "2.5"}]}', "/a/1/b") == 2.5
    assert extract_value("mean=3.25 n=6\n", "re:mean=([0-9.]+)") == 3.25
    assert extract_value("  42\n", "") == 42.0
    assert extract_value("nothing here", "/mean") is None
    assert extract_value('{"mean": true}', "/mean") is None
    assert extract_value("abc", "") is None


def test_verify_claim_float_edges():
    c = Claim.from_json(CLAIM_MEAN)  # 3.5 +/- 0.01
    comp = Computation.from_json(COMP_MEAN)
    ok = ExecutionResult.from_json(RES_MEAN_OK)
    assert verify_claim(c, comp, ok).status == "confirmed"
    v = verify_claim(c, comp, ExecutionResult(True, "", "", 0, 3.6, "x"), tolerance=0.1)
    assert v.status == "mismatch" and v.delta == 0.10000000000000009
    assert verify_claim(c, comp, ExecutionResult(True, "", "", 0, 3.75, "x"), tolerance=0.25).status == "confirmed"
    assert verify_claim(c, comp, ExecutionResult(False, "", "boom", 1, None, "x")).status == "execution_failed"
    assert verify_claim(c, comp, ExecutionResult(False, "", "", -1, None, "x", ["data.csv"])).status == "input_hash_mismatch"
    assert verify_claim(c, None, None).status == "execution_failed"


def test_rules_run_every_check_no_short_circuit():
    c = Claim.from_json({**CLAIM_MEAN, "confidence": 0.1})
    r = run_claim_rules(c, None, None)
    assert not r.ok and len(r.checks) == 5
    assert r.codes() == ["DANGLING_COMPUTATION", "UNCONFIRMED_CLAIM", "ENVIRONMENT_UNPINNED", "CONFIDENCE_BELOW_FLOOR"]
    r2 = run_claim_rules(Claim.from_json(CLAIM_MEAN), Computation.from_json(COMP_MEAN), ClaimVerdict("mismatch", 3.7, 0.2))
    assert r2.codes() == ["TOLERANCE_EXCEEDED"]
    r3 = run_claim_rules(Claim.from_json(CLAIM_MEAN), Computation.from_json(COMP_MEAN), ClaimVerdict("confirmed", 3.5, 0.0))
    assert r3.ok


def test_subprocess_reexecutor_runs_the_example_for_real(tmp_path):
    with open(os.path.join(EXAMPLES, "provenance-manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    assert validate_manifest(manifest).ok
    rx = SubprocessReexecutor(EXAMPLES, timeout=60, executable_map={"python3": sys.executable})
    comp = Computation.from_json(manifest["computations"][0])
    assert rx.check_inputs(comp) == []
    res = rx.run(comp)
    assert res.ok, res.stderr
    assert res.exit_code == 0 and res.output_value == 3.5
    p = prepare(manifest, rx, data_as_of=DATA_AS_OF)
    assert p.ok
    assert [o.verdict.status for o in p.outcomes] == ["confirmed"]
    assert p.summary.startswith('Attest 1/1 claims confirmed for "Example manuscript" manifest ')
    assert badge_json(p.report())["message"].startswith("1/1 · suite ")

    # Tamper with an input in a copy: the re-executor refuses to run.
    work = tmp_path / "claims"
    shutil.copytree(EXAMPLES, work)
    with open(work / "data.csv", "a", encoding="utf-8") as f:
        f.write("g,9.9\n")
    rx2 = SubprocessReexecutor(str(work), timeout=60, executable_map={"python3": sys.executable})
    res2 = rx2.run(comp)
    assert not res2.ok and res2.input_mismatches == ["data.csv"]
    assert verify_claim(Claim.from_json(manifest["claims"][0]), comp, res2).status == "input_hash_mismatch"


def test_subprocess_reexecutor_reports_failed_command(tmp_path):
    (tmp_path / "boom.py").write_text("import sys\nsys.exit(3)\n", encoding="utf-8")
    from provsubstrate.core import sha256_bytes

    comp = Computation.build(
        command=["python3", "boom.py"],
        entrypoint="boom.py",
        entrypoint_hash=sha256_bytes((tmp_path / "boom.py").read_bytes()),
        input_hashes={},
        environment={"python": "3", "packages": {}},
        output_selector="",
    )
    res = SubprocessReexecutor(str(tmp_path), timeout=60, executable_map={"python3": sys.executable}).run(comp)
    assert not res.ok and res.exit_code == 3 and res.output_value is None


# --- gate + attestation ----------------------------------------------------


def _deps(results):
    log = AppendOnlyAuditLog(None, clock=lambda: DATA_AS_OF)
    return ClaimsDeps(StubReexecutor(results), log, AttestationLedger(), {"pi.ada": b"academic-approver-secret-0001"})


def test_approval_summary_fixed_format():
    s = approval_summary(Claim.from_json(CLAIM_MEAN), ClaimVerdict("confirmed", 3.5, 0.0))
    assert s == f"Claim {CLAIM_MEAN['claim_id'][:12]} = 3.5 kg tol 0.01 observed 3.5 delta 0 (confirmed) computation {COMP_MEAN['computation_id'][:12]}"
    s2 = approval_summary(Claim.from_json(CLAIM_MEAN), ClaimVerdict("execution_failed", None, None))
    assert "observed - delta - (execution_failed)" in s2


def test_attest_end_to_end_with_valid_approval():
    deps = _deps(RESULTS_CLEAN)
    p = prepare(MANIFEST_CLEAN, deps.reexecutor, data_as_of=DATA_AS_OF)
    tok = Approver("pi.ada", b"academic-approver-secret-0001").approve(p.approval_request(SESSION_ID), APPROVED_AT)
    r = attest_manifest(MANIFEST_CLEAN, None, deps, tok, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
    assert r.ok and r.stage is None
    assert r.audit_actions == ["claim_extraction", "reexecution", "verifier_check", "approval_granted", "attestation_recorded"]
    assert set(r.statuses.values()) == {"confirmed"}
    assert len(deps.ledger.entries) == 1 and deps.ledger.entries[0]["entry_id"] == r.entry_id
    assert deps.ledger.entries[0]["approver"] == "pi.ada"
    assert verify_chain(deps.audit_log.entries).ok
    assert tok.materiality == CLAIMS_ATTEST_MATERIALITY and tok.request_hash == r.request_hash
    # Passing the results explicitly gives the same request hash and entry id.
    deps2 = _deps({})
    r2 = attest_manifest(MANIFEST_CLEAN, {k: ExecutionResult.from_json(v) for k, v in RESULTS_CLEAN.items()}, deps2, tok, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
    assert r2.ok and r2.entry_id == r.entry_id


def test_attest_refuses_wrong_hash_unknown_approver_and_missing_token():
    for mode in ("wrong_hash", "unknown", "none"):
        deps = _deps(RESULTS_CLEAN)
        p = prepare(MANIFEST_CLEAN, deps.reexecutor, data_as_of=DATA_AS_OF)
        areq = p.approval_request(SESSION_ID)
        if mode == "wrong_hash":
            tok = Approver("pi.ada", b"academic-approver-secret-0001").approve(ApprovalRequest("1" * 64, areq.summary, SESSION_ID, CLAIMS_ATTEST_MATERIALITY), APPROVED_AT)
        elif mode == "unknown":
            tok = Approver("student.bob", b"not-in-the-trust-set").approve(areq, APPROVED_AT)
        else:
            tok = None
        r = attest_manifest(MANIFEST_CLEAN, None, deps, tok, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
        assert not r.ok and r.stage == "approval", mode
        assert r.audit_actions[-1] == "approval_denied" and deps.ledger.entries == []


def test_attest_stops_at_verifier_on_mismatch():
    results = dict(RESULTS_CLEAN)
    results[COMP_MEAN["computation_id"]] = {**RES_MEAN_OK, "stdout": '{"mean": 3.7}', "output_value": 3.7}
    deps = _deps(results)
    r = attest_manifest(MANIFEST_CLEAN, None, deps, None, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
    assert r.stage == "verifier" and r.audit_actions == ["claim_extraction", "reexecution", "verifier_check"]
    assert r.statuses[CLAIM_MEAN["claim_id"]] == "mismatch"


def test_badge_formats():
    rep = {"manifest_hash": "abcdef0123456789" + "0" * 48, "total": 12, "confirmed": 12}
    j = badge_json(rep)
    assert j == {"schemaVersion": 1, "label": "claims verified", "message": "12/12 · suite abcdef01", "color": "brightgreen"}
    assert badge_json({**rep, "confirmed": 7})["color"] == "orange"
    assert badge_json({**rep, "confirmed": 2})["color"] == "red"
    svg = badge_svg(rep)
    assert svg.startswith("<svg ") and "claims verified" in svg and "12/12 · suite abcdef01" in svg
    assert svg == badge_svg(rep)


# --- conformance -----------------------------------------------------------

_KINDS = {"claim_manifest_hash", "claim_manifest_shape", "claim_verify", "claim_rules", "claim_attest"}


def test_conformance_catalogue_is_fixed_and_covers_every_kind():
    cases = conformance_cases()
    assert {c["kind"] for c in cases} == _KINDS == set(CONFORMANCE_HANDLERS)
    ids = [(c["kind"], c["id"]) for c in cases]
    assert len(ids) == len(set(ids))
    assert _canon(cases) == _canon(conformance_cases())
    for want in ("clean_valid_approval", "mismatch_blocks", "exec_failed_blocks", "input_hash_mismatch_blocks", "dangling_edge_shape", "wrong_hash_approval", "unknown_approver", "no_approval"):
        assert ("claim_attest", want) in ids


@pytest.mark.parametrize("case", conformance_cases(), ids=lambda c: f"{c['kind']}/{c['id']}")
def test_conformance_round_trip_and_determinism(case):
    exp1 = compute_expected(case["kind"], case["input"])
    exp2 = compute_expected(case["kind"], case["input"])
    assert _canon(exp1) == _canon(exp2)
    ok, detail = CONFORMANCE_HANDLERS[case["kind"]](case["input"], exp1)
    assert ok, detail
    reloaded = json.loads(json.dumps({"input": case["input"], "expected": exp1}))
    ok2, detail2 = CONFORMANCE_HANDLERS[case["kind"]](reloaded["input"], reloaded["expected"])
    assert ok2, detail2


def test_negative_control_rounding_port_fails_float_edge_vector():
    """A port that rounds |delta| to 2 decimals before comparing confirms
    3.6 within 0.1 and fails the pinned vector."""
    for c in conformance_cases():
        if c["kind"] == "claim_verify" and c["id"] == "tolerance_edge_float_over":
            exp = compute_expected(c["kind"], c["input"])
            claim = Claim.from_json(c["input"]["claim"])
            observed = c["input"]["result"]["output_value"]
            rounded = round(abs(observed - claim.value), 2) <= claim.tolerance
            assert rounded is True and exp["status"] == "mismatch"
            return
    raise AssertionError("vector missing")
