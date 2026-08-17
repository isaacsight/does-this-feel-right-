"""Reproducibility ledger: unit tests, one real SubprocessRunner run, and
conformance handler round-trips (determinism + a negative control)."""

import json
import sys

import pytest

from provsubstrate.core import AppendOnlyAuditLog, ApprovalRequest, Approver, canonicalize, verify_chain
from provsubstrate.repro import (
    CONFORMANCE_HANDLERS,
    REPRO_MATERIALITY,
    ClaimSpec,
    OutputSelector,
    PaperRef,
    RepoRef,
    ReproductionAttempt,
    ReproductionTarget,
    RunRecord,
    StubRunner,
    SubprocessRunner,
    approval_summary,
    compute_expected,
    conformance_cases,
    croissant_metadata,
    dataset_manifest,
    export_jsonl,
    judge,
    record_reproduction,
    run_repro_rules,
    validate_attempt,
    zenodo_metadata,
)
from provsubstrate.repro.conformance import (
    APPROVED_AT,
    DATA_AS_OF,
    SESSION_ID,
    STDOUT_CRASH,
    STDOUT_FULL,
    STDOUT_PARTIAL,
    TRUSTED_APPROVER,
    base_attempt,
    base_target,
)

TRUSTED = {TRUSTED_APPROVER["approver_id"]: TRUSTED_APPROVER["secret_utf8"].encode("utf-8")}


def clock():
    return DATA_AS_OF


def test_target_hash_is_key_order_independent():
    t = base_target()
    j = t.to_json()
    shuffled = dict(reversed(list(j.items())))
    assert ReproductionTarget.from_json(shuffled).target_hash() == t.target_hash()
    assert base_target(commit=None).target_hash() != t.target_hash()


def test_judge_outcomes():
    t = base_target()
    a = base_attempt(t)
    assert judge(t, a, StubRunner(STDOUT_FULL).run(t, a)).overall == "reproduced"
    assert judge(t, a, StubRunner(STDOUT_PARTIAL).run(t, a)).overall == "partially_reproduced"
    v = judge(t, a, StubRunner(STDOUT_CRASH).run(t, a))
    assert v.overall == "could_not_run"
    assert [c.status for c in v.per_claim] == ["missing", "missing", "missing"]
    # zero claims is never vacuously reproduced
    t0 = base_target(claims=[])
    a0 = base_attempt(t0, selectors=[])
    assert judge(t0, a0, StubRunner(STDOUT_FULL).run(t0, a0)).overall == "not_reproduced"


def test_judge_uses_decimal_delta_not_float_error():
    t = base_target(claims=[ClaimSpec("accuracy", "x", 0.85, "fraction", 0.01)])
    a = base_attempt(t, selectors=[OutputSelector("accuracy", 1, r"accuracy=([0-9.]+)")])
    rr = RunRecord((), {"accuracy": 0.86}, 1.0, None)
    v = judge(t, a, rr)
    assert v.per_claim[0].status == "confirmed"
    assert v.per_claim[0].delta == 0.01
    assert 0.86 - 0.85 > 0.01  # the float trap this guards against


def test_rules_all_run_no_short_circuit():
    t = base_target(commit=None, env={})
    a = base_attempt(t, confidence=0.1)
    v = judge(t, a, StubRunner(STDOUT_CRASH).run(t, a))
    r = run_repro_rules(t, a, v, 0.6)
    assert not r["ok"]
    codes = [c.get("code") for c in r["checks"]]
    assert codes == ["NO_COMMIT_PINNED", "ENVIRONMENT_UNPINNED", None, "RUN_FAILED", None, "CONFIDENCE_BELOW_FLOOR"]
    ok = run_repro_rules(base_target(), base_attempt(base_target()), judge(base_target(), base_attempt(base_target()), StubRunner(STDOUT_FULL).run(base_target(), base_attempt(base_target()))))
    assert ok["ok"] and all(c["pass"] for c in ok["checks"])


def test_validate_attempt_names_every_problem():
    t = base_target()
    a = base_attempt(t, target_hash="0" * 64, prompt_hash="zz", model_lineage=[], selectors=[OutputSelector("nope", 9, "(", 1)], confidence=1.5)
    errs = validate_attempt(t, a)
    assert errs == sorted(errs)
    joined = "\n".join(errs)
    for needle in ("target_hash", "prompt_hash", "model_lineage: empty", "unknown claim", "command_index", "invalid regex", "confidence"):
        assert needle in joined
    assert validate_attempt(t, base_attempt(t)) == []


def _record(t, a, table, approval=None, floor=0.6):
    log = AppendOnlyAuditLog(None, clock)
    res = record_reproduction(
        target=t, attempt=a, runner=StubRunner(table, 12.5), audit_log=log, session_id=SESSION_ID, trusted=TRUSTED,
        data_as_of=DATA_AS_OF, approval=approval, confidence_floor=floor,
    )
    return res, log


def test_record_full_path_and_audit_chain():
    t = base_target()
    a = base_attempt(t)
    dry, _ = _record(t, a, STDOUT_FULL)
    assert dry["stage"] == "approval" and dry["audit_actions"][-1] == "approval_denied"
    tok = Approver("pi.ada", TRUSTED["pi.ada"]).approve(ApprovalRequest(dry["request_hash"], dry["summary"], SESSION_ID, REPRO_MATERIALITY), APPROVED_AT)
    res, log = _record(t, a, STDOUT_FULL, tok)
    assert res["ok"] and res["stage"] is None
    assert res["audit_actions"] == ["repro_attempt", "run_record", "verifier_check", "approval_granted", "report_recorded"]
    assert verify_chain(log.entries).ok
    assert res["report"]["report_id"] == res["report_id"]
    assert res["report"]["verdict"]["overall"] == "reproduced"
    assert res["summary"] == approval_summary(t, judge(t, a, StubRunner(STDOUT_FULL).run(t, a)))
    # same token cannot approve a different run (different request hash)
    res2, _ = _record(t, a, STDOUT_PARTIAL, tok)
    assert not res2["ok"] and res2["stage"] == "verifier"  # never reaches the gate
    # a stranger's token is refused
    bad = Approver("student.bob", b"not-in-the-trust-set").approve(ApprovalRequest(dry["request_hash"], dry["summary"], SESSION_ID, REPRO_MATERIALITY), APPROVED_AT)
    res3, _ = _record(t, a, STDOUT_FULL, bad)
    assert res3["stage"] == "approval" and res3["detail"]["reason"] == "unknown_approver"


def test_malformed_attempt_logs_nothing():
    t = base_target()
    res, log = _record(t, base_attempt(t, target_hash="0" * 64), STDOUT_FULL)
    assert res["stage"] == "attempt_shape" and log.entries == [] and res["request_hash"] is None


def test_subprocess_runner_real_python_script(tmp_path):
    (tmp_path / "metric.py").write_text("print('epoch 3 done')\nprint('accuracy=0.86')\nprint('params=1250000')\n")
    (tmp_path / "boom.py").write_text("import sys\nprint('starting')\nsys.exit(3)\n")
    t = ReproductionTarget(
        PaperRef("Tiny", "a" * 64), RepoRef("https://example.invalid/r", "b" * 40),
        (ClaimSpec("accuracy", "acc", 0.85, "fraction", 0.01), ClaimSpec("params", "n", 1250000, "count", 0)),
        {"python": "any"}, ((sys.executable, "metric.py"),),
    )
    a = ReproductionAttempt(
        t.target_hash(), t.paper.doc_hash, t.commands,
        (OutputSelector("accuracy", 0, r"accuracy=([0-9.]+)"), OutputSelector("params", 0, r"params=(\d+)")),
        [{"model": "local", "version": "test"}], "c" * 64, 0.9,
    )
    ticks = iter([10.0, 12.5])
    rr = SubprocessRunner(str(tmp_path), timeout=60, clock=lambda: next(ticks)).run(t, a)
    assert rr.succeeded and rr.commands[0].exit_code == 0
    assert rr.extracted == {"accuracy": 0.86, "params": 1250000.0}
    assert rr.wall_seconds == 2.5
    assert judge(t, a, rr).overall == "reproduced"
    # a failing script -> could_not_run, second command never runs
    a2 = ReproductionAttempt(t.target_hash(), t.paper.doc_hash, ((sys.executable, "boom.py"), (sys.executable, "metric.py")), a.selectors, a.model_lineage, a.prompt_hash, 0.9)
    rr2 = SubprocessRunner(str(tmp_path), timeout=60).run(t, a2)
    assert not rr2.succeeded and rr2.commands[0].exit_code == 3 and len(rr2.commands) == 1
    assert rr2.wall_seconds == 0.0
    assert judge(t, a2, rr2).overall == "could_not_run"
    # unknown executable -> spawn failure, no exception
    a3 = ReproductionAttempt(t.target_hash(), t.paper.doc_hash, (("definitely-not-a-binary-xyz",),), (), a.model_lineage, a.prompt_hash, 0.9)
    rr3 = SubprocessRunner(str(tmp_path), timeout=5).run(t, a3)
    assert rr3.error is not None and rr3.error.startswith("spawn_failed")


def test_dataset_export_manifest_and_metadata():
    t = base_target()
    a = base_attempt(t)
    dry, _ = _record(t, a, STDOUT_FULL)
    tok = Approver("pi.ada", TRUSTED["pi.ada"]).approve(ApprovalRequest(dry["request_hash"], dry["summary"], SESSION_ID, REPRO_MATERIALITY), APPROVED_AT)
    r1 = _record(t, a, STDOUT_FULL, tok)[0]["report"]
    t2 = base_target(claims=[ClaimSpec("accuracy", "edge", 0.85, "fraction", 0.01)])
    a2 = base_attempt(t2, selectors=[OutputSelector("accuracy", 1, r"accuracy=([0-9.]+)")])
    dry2, _ = _record(t2, a2, STDOUT_FULL)
    tok2 = Approver("pi.ada", TRUSTED["pi.ada"]).approve(ApprovalRequest(dry2["request_hash"], dry2["summary"], SESSION_ID, REPRO_MATERIALITY), APPROVED_AT)
    r2 = _record(t2, a2, STDOUT_FULL, tok2)[0]["report"]

    jsonl = export_jsonl([r1, r2])
    assert jsonl == export_jsonl([r2, r1])  # order-independent
    lines = jsonl.strip().split("\n")
    assert len(lines) == 2 and all(json.loads(ln)["report_id"] for ln in lines)
    assert all(canonicalize(json.loads(ln)) == ln for ln in lines)
    m = dataset_manifest([r1, r2], "1.0.0")
    assert m == dataset_manifest([r2, r1], "1.0.0")
    assert m["row_count"] == 2 and len(m["dataset_hash"]) == 64
    assert m["distribution"]["content_size"] == len(jsonl.encode("utf-8"))
    assert export_jsonl([]) == "" and dataset_manifest([], "1.0.0")["row_count"] == 0

    z = zenodo_metadata(m, title="Repro reports", creators=[{"name": "Hernandez, Isaac"}], description="d", license="CC-BY-4.0")
    assert z["metadata"]["upload_type"] == "dataset" and z["metadata"]["license"] == "cc-by-4.0" and z["metadata"]["version"] == "1.0.0"
    assert m["dataset_hash"] in z["metadata"]["notes"]
    with pytest.raises(ValueError):
        zenodo_metadata(m, title="x", creators=[], description="d", license="Proprietary")
    c = croissant_metadata(m, license="MIT")
    assert c["@type"] == "sc:Dataset" and c["conformsTo"].endswith("croissant/1.0")
    assert c["distribution"][0]["sha256"] == m["distribution"]["sha256"]
    names = [f["name"] for f in c["recordSet"][0]["field"]]
    assert "report_id" in names and "overall" in names
    json.dumps(c)  # serialisable JSON-LD


def test_conformance_handlers_round_trip_and_determinism():
    cases = conformance_cases()
    kinds = {c["kind"] for c in cases}
    assert kinds == {"repro_target_hash", "repro_judge", "repro_rules", "repro_approval_summary", "repro_record", "repro_dataset_manifest"}
    ids = [(c["kind"], c["id"]) for c in cases]
    assert len(ids) == len(set(ids))
    for c in cases:
        e1 = compute_expected(c["kind"], c["input"])
        e2 = compute_expected(c["kind"], c["input"])
        assert canonicalize(e1) == canonicalize(e2), c["id"]
        ok, detail = CONFORMANCE_HANDLERS[c["kind"]](c["input"], e1)
        assert ok, (c["kind"], c["id"], detail)
    # negative control: a wrong expectation fails
    c = next(x for x in cases if x["kind"] == "repro_record" and x["id"] == "records_with_valid_approval")
    exp = compute_expected(c["kind"], c["input"])
    assert exp["ok"] and exp["audit_actions"][-1] == "report_recorded"
    ok, _ = CONFORMANCE_HANDLERS["repro_record"](c["input"], {**exp, "request_hash": "0" * 64})
    assert not ok


def test_conformance_cases_are_json_and_stable():
    a = canonicalize(conformance_cases())
    b = canonicalize(conformance_cases())
    assert a == b
