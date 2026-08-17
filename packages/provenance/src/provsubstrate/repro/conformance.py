"""Conformance catalogue for the reproducibility ledger (academic v1).

Kinds: ``repro_target_hash``, ``repro_judge``, ``repro_rules``,
``repro_approval_summary``, ``repro_record``, ``repro_dataset_manifest``.
Every case is built from fixed constants; ``compute_expected`` runs the
reference behaviour; the handlers replay a vector's input through the same
functions and compare JSON-equal.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..conformance.runner import Handler, expect_equal
from ..core.approval import ApprovalRequest, ApprovalToken, Approver
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import sha256_text
from .dataset import dataset_manifest, export_jsonl
from .judge import judge, run_repro_rules
from .ledger import REPRO_MATERIALITY, approval_summary, record_reproduction
from .model import (
    ClaimSpec,
    OutputSelector,
    PaperRef,
    RepoRef,
    ReproductionAttempt,
    ReproductionTarget,
    ReproVerdict,
    RunRecord,
)
from .runner import StubRunner, command_key

# ---- academic v1 fixed constants -------------------------------------------

DATA_AS_OF = "2026-08-17T00:00:00.000Z"
APPROVED_AT = "2026-08-17T12:00:00.000Z"
SESSION_ID = "academic-conformance-session"
TRUSTED_APPROVER = {"approver_id": "pi.ada", "secret_utf8": "academic-approver-secret-0001"}
UNTRUSTED_SIGNER = {"approver_id": "student.bob", "secret_utf8": "not-in-the-trust-set"}
MODEL_LINEAGE = [{"model": "local-27b", "version": "conformance"}]

PAPER_DOC_HASH = sha256_text("Attention Is Not All You Need: A Small Replication Study (v2 preprint)")
PROMPT_HASH = sha256_text("prompt:repro:academic-v1")
COMMIT = "3f2a9c1e5b7d4a6f8c0e2b4d6f8a0c2e4b6d8f0a"
RUN_CMD = ["python3", "run.py"]
EVAL_CMD = ["python3", "evaluate.py"]


def _fixed_clock() -> str:
    return DATA_AS_OF


def base_target(*, commit: Optional[str] = COMMIT, env: Optional[dict] = None, claims: Optional[list] = None) -> ReproductionTarget:
    if env is None:
        env = {"python": "3.11.4", "os": "ubuntu-22.04", "cuda": "none"}
    if claims is None:
        claims = [
            ClaimSpec("accuracy", "Test accuracy (Table 2)", 0.85, "fraction", 0.01),
            ClaimSpec("f1", "Macro F1 (Table 2)", 0.8, "fraction", 0.01),
            ClaimSpec("params", "Parameter count", 1250000, "count", 0),
        ]
    return ReproductionTarget(
        PaperRef("Attention Is Not All You Need: A Small Replication Study", PAPER_DOC_HASH, doi="10.5555/example.1234", arxiv_id="2608.01234"),
        RepoRef("https://github.com/example/small-replication", commit),
        tuple(claims),
        env,
        (tuple(RUN_CMD), tuple(EVAL_CMD)),
    )


def base_attempt(target: ReproductionTarget, *, confidence: float = 0.9, selectors: Optional[list] = None, **overrides) -> ReproductionAttempt:
    if selectors is None:
        selectors = [
            OutputSelector("accuracy", 1, r"accuracy=([0-9.]+)"),
            OutputSelector("f1", 1, r"f1=([0-9.]+)"),
            OutputSelector("params", 0, r"params=([0-9]+)"),
        ]
    kwargs = dict(
        target_hash=target.target_hash(),
        doc_hash=target.paper.doc_hash,
        commands=target.commands,
        selectors=tuple(selectors),
        model_lineage=list(MODEL_LINEAGE),
        prompt_hash=PROMPT_HASH,
        confidence=confidence,
        notes="Run training then evaluation; read metrics from evaluate.py stdout.",
    )
    kwargs.update(overrides)
    return ReproductionAttempt(**kwargs)


STDOUT_FULL = {command_key(RUN_CMD): (0, "training...\nparams=1250000\n"), command_key(EVAL_CMD): (0, "accuracy=0.86\nf1=0.795\n")}
STDOUT_PARTIAL = {command_key(RUN_CMD): (0, "training...\nparams=1250000\n"), command_key(EVAL_CMD): (0, "accuracy=0.86\nf1=0.71\n")}
STDOUT_MISMATCH = {command_key(RUN_CMD): (0, "training...\nparams=1310000\n"), command_key(EVAL_CMD): (0, "accuracy=0.71\nf1=0.62\n")}
STDOUT_MISSING_F1 = {command_key(RUN_CMD): (0, "training...\nparams=1250000\n"), command_key(EVAL_CMD): (0, "accuracy=0.86\n")}
STDOUT_CRASH = {command_key(RUN_CMD): (1, "Traceback (most recent call last):\nModuleNotFoundError: torch\n")}


def stub_from_input(stub: dict) -> StubRunner:
    table = {k: (int(v["exit_code"]), v["stdout"]) for k, v in stub["table"].items()}
    return StubRunner(table, wall_seconds=stub.get("wall_seconds", 0.0))


def _stub_json(table: dict, wall_seconds: float) -> dict:
    return {"table": {k: {"exit_code": v[0], "stdout": v[1]} for k, v in table.items()}, "wall_seconds": wall_seconds}


def _run(target: ReproductionTarget, attempt: ReproductionAttempt, table: dict, wall: float = 12.5) -> RunRecord:
    return StubRunner(table, wall).run(target, attempt)


# ---- record end to end (shared by cases and handler) -----------------------

def record_from_input(inp: dict) -> dict:
    """Replay a ``repro_record`` input: build the token as directed
    (``valid`` / ``wrong_hash`` / ``unknown_approver`` / ``none``) by first
    dry-running without approval to learn the request hash and summary, then
    run once more on a fresh audit log."""
    target = ReproductionTarget.from_json(inp["target"])
    attempt = ReproductionAttempt.from_json(inp["attempt"])
    trusted = {t["approver_id"]: t["secret_utf8"].encode("utf-8") for t in inp["trusted"]}
    session_id = inp["session_id"]
    floor = inp.get("confidence_floor", 0.6)
    mode = inp.get("approval", "none")

    def go(token: Optional[ApprovalToken]) -> dict:
        log = AppendOnlyAuditLog(None, _fixed_clock)
        return record_reproduction(
            target=target, attempt=attempt, runner=stub_from_input(inp["stub"]), audit_log=log, session_id=session_id,
            trusted=trusted, data_as_of=inp["data_as_of"], approval=token, confidence_floor=floor,
        )

    token: Optional[ApprovalToken] = None
    if mode != "none":
        dry = go(None)
        summary = dry.get("summary")
        rh = dry.get("request_hash")
        if summary is not None and rh is not None:
            first = inp["trusted"][0]
            signer = Approver(first["approver_id"], first["secret_utf8"].encode("utf-8"))
            stranger_d = inp.get("untrusted", UNTRUSTED_SIGNER)
            stranger = Approver(stranger_d["approver_id"], stranger_d["secret_utf8"].encode("utf-8"))
            if mode == "valid":
                token = signer.approve(ApprovalRequest(rh, summary, session_id, REPRO_MATERIALITY), inp["approved_at"])
            elif mode == "wrong_hash":
                token = signer.approve(ApprovalRequest("f" * 64, summary, session_id, REPRO_MATERIALITY), inp["approved_at"])
            elif mode == "unknown_approver":
                token = stranger.approve(ApprovalRequest(rh, summary, session_id, REPRO_MATERIALITY), inp["approved_at"])
            else:
                raise ValueError(f"unknown approval mode {mode!r}")
    return go(token)


def _record_expected(res: dict) -> dict:
    return {
        "ok": res["ok"], "stage": res["stage"], "request_hash": res["request_hash"], "overall": res["overall"],
        "audit_actions": res["audit_actions"], "report_id": res["report_id"],
    }


def _record_input(target, attempt, table, *, approval="none", floor=0.6, wall=12.5) -> dict:
    return {
        "target": target.to_json(), "attempt": attempt.to_json(), "stub": _stub_json(table, wall), "confidence_floor": floor,
        "session_id": SESSION_ID, "trusted": [TRUSTED_APPROVER], "untrusted": UNTRUSTED_SIGNER, "approved_at": APPROVED_AT,
        "data_as_of": DATA_AS_OF, "approval": approval,
    }


# ---- compute_expected -----------------------------------------------------

def compute_expected(kind: str, inp: dict) -> Any:
    if kind == "repro_target_hash":
        t = ReproductionTarget.from_json(inp["target"])
        return {"target_hash": t.target_hash()}
    if kind == "repro_judge":
        t = ReproductionTarget.from_json(inp["target"])
        a = ReproductionAttempt.from_json(inp["attempt"])
        r = RunRecord.from_json(inp["run_record"])
        return {"verdict": judge(t, a, r).to_json()}
    if kind == "repro_rules":
        t = ReproductionTarget.from_json(inp["target"])
        a = ReproductionAttempt.from_json(inp["attempt"])
        v = ReproVerdict.from_json(inp["verdict"])
        return run_repro_rules(t, a, v, inp.get("confidence_floor", 0.6))
    if kind == "repro_approval_summary":
        t = ReproductionTarget.from_json(inp["target"])
        v = ReproVerdict.from_json(inp["verdict"])
        return {"summary": approval_summary(t, v)}
    if kind == "repro_record":
        return _record_expected(record_from_input(inp))
    if kind == "repro_dataset_manifest":
        m = dataset_manifest(inp["reports"], inp["version"])
        return {
            "row_count": m["row_count"], "rows": m["rows"], "dataset_hash": m["dataset_hash"],
            "jsonl_sha256": sha256_text(export_jsonl(inp["reports"])), "filename": m["distribution"]["filename"],
        }
    raise KeyError(f"repro: unknown conformance kind {kind!r}")


# ---- case catalogue -------------------------------------------------------

def _case(kind: str, cid: str, description: str, inp: dict) -> dict:
    return {"kind": kind, "id": cid, "description": description, "input": inp}


def conformance_cases() -> List[dict]:
    cases: List[dict] = []
    t = base_target()
    t_unpinned = base_target(commit=None)
    t_short = base_target(commit="3f2a9c1")
    t_noenv = base_target(env={})
    t_noclaims = base_target(claims=[])
    a = base_attempt(t)
    a_low = base_attempt(t, confidence=0.3)

    # repro_target_hash
    cases.append(_case("repro_target_hash", "pinned", "content hash of a fully pinned target", {"target": t.to_json()}))
    cases.append(_case("repro_target_hash", "unpinned_commit", "commit null changes the hash", {"target": t_unpinned.to_json()}))
    shuffled = dict(reversed(list(t.to_json().items())))
    cases.append(_case("repro_target_hash", "keys_shuffled", "key order must not matter", {"target": shuffled}))

    # repro_judge
    runs = {
        "full": (t, a, STDOUT_FULL, "every claim within tolerance -> reproduced"),
        "partial": (t, a, STDOUT_PARTIAL, "one claim off -> partially_reproduced"),
        "mismatch": (t, a, STDOUT_MISMATCH, "no claim within tolerance -> not_reproduced"),
        "missing_claim": (t, a, STDOUT_MISSING_F1, "selector matched nothing -> missing; overall partial"),
        "could_not_run": (t, a, STDOUT_CRASH, "first command fails -> could_not_run, later claims missing"),
    }
    for cid, (tt, aa, table, desc) in runs.items():
        rr = _run(tt, aa, table)
        cases.append(_case("repro_judge", cid, desc, {"target": tt.to_json(), "attempt": aa.to_json(), "run_record": rr.to_json()}))
    a_nosel = base_attempt(t, selectors=[])
    rr = _run(t, a_nosel, STDOUT_FULL)
    cases.append(_case("repro_judge", "no_selectors", "no selectors -> all missing -> not_reproduced", {"target": t.to_json(), "attempt": a_nosel.to_json(), "run_record": rr.to_json()}))
    t_zero = t_noclaims
    a_zero = base_attempt(t_zero, selectors=[])
    rr = _run(t_zero, a_zero, STDOUT_FULL)
    cases.append(_case("repro_judge", "zero_claims", "no claims -> not_reproduced, never vacuously reproduced", {"target": t_zero.to_json(), "attempt": a_zero.to_json(), "run_record": rr.to_json()}))
    t_edge = base_target(claims=[ClaimSpec("accuracy", "edge", 0.85, "fraction", 0.01)])
    a_edge = base_attempt(t_edge, selectors=[OutputSelector("accuracy", 1, r"accuracy=([0-9.]+)")])
    rr = _run(t_edge, a_edge, STDOUT_FULL)
    cases.append(_case("repro_judge", "tolerance_edge_decimal", "0.86 vs 0.85 with tol 0.01 is confirmed (decimal delta, not float error)", {"target": t_edge.to_json(), "attempt": a_edge.to_json(), "run_record": rr.to_json()}))

    # repro_rules
    v_full = judge(t, a, _run(t, a, STDOUT_FULL))
    v_partial = judge(t, a, _run(t, a, STDOUT_PARTIAL))
    v_crash = judge(t, a, _run(t, a, STDOUT_CRASH))
    rules_cases = [
        ("all_pass", t, a, v_full, 0.6, "pinned, env, claims, run ok, agree, confidence -> ok"),
        ("unpinned_commit", t_unpinned, base_attempt(t_unpinned), v_full, 0.6, "NO_COMMIT_PINNED"),
        ("short_commit", t_short, base_attempt(t_short), v_full, 0.6, "abbreviated commit is not pinned"),
        ("unpinned_environment", t_noenv, base_attempt(t_noenv), v_full, 0.6, "ENVIRONMENT_UNPINNED"),
        ("zero_claims", t_noclaims, base_attempt(t_noclaims, selectors=[]), judge(t_noclaims, base_attempt(t_noclaims, selectors=[]), _run(t_noclaims, base_attempt(t_noclaims, selectors=[]), STDOUT_FULL)), 0.6, "ZERO_CLAIMS"),
        ("run_failed", t, a, v_crash, 0.6, "RUN_FAILED"),
        ("claim_mismatch", t, a, v_partial, 0.6, "CLAIM_MISMATCH on a partial verdict"),
        ("confidence_below_floor", t, a_low, v_full, 0.6, "CONFIDENCE_BELOW_FLOOR"),
        ("confidence_at_floor_passes", t, base_attempt(t, confidence=0.6), v_full, 0.6, "confidence == floor passes"),
        ("multiple_failures", t_unpinned, base_attempt(t_unpinned, confidence=0.1), v_crash, 0.6, "every applicable rule reports; no short-circuit"),
    ]
    for cid, tt, aa, vv, floor, desc in rules_cases:
        cases.append(_case("repro_rules", cid, desc, {"target": tt.to_json(), "attempt": aa.to_json(), "verdict": vv.to_json(), "confidence_floor": floor}))

    # repro_approval_summary
    cases.append(_case("repro_approval_summary", "reproduced", "summary line for a full reproduction", {"target": t.to_json(), "verdict": v_full.to_json()}))
    cases.append(_case("repro_approval_summary", "partial", "summary line carries the verdict and count", {"target": t.to_json(), "verdict": v_partial.to_json()}))
    cases.append(_case("repro_approval_summary", "unpinned", "unpinned commit prints (unpinned)", {"target": t_unpinned.to_json(), "verdict": v_full.to_json()}))
    t_long = base_target()
    t_long = ReproductionTarget(PaperRef("A" * 80, t.paper.doc_hash), t_long.repo, t_long.claims, t_long.environment_spec, t_long.commands)
    cases.append(_case("repro_approval_summary", "long_title_truncated", "title is cut at 40 characters", {"target": t_long.to_json(), "verdict": v_full.to_json()}))

    # repro_record
    rec = [
        ("records_with_valid_approval", t, a, STDOUT_FULL, "valid", 0.6, "full path: attempt -> run -> verifier -> signed -> report_recorded"),
        ("stops_at_gate_without_approval", t, a, STDOUT_FULL, "none", 0.6, "verifier ok, no token -> approval_denied"),
        ("rejects_wrong_hash_approval", t, a, STDOUT_FULL, "wrong_hash", 0.6, "token bound to another request hash is refused"),
        ("rejects_unknown_approver", t, a, STDOUT_FULL, "unknown_approver", 0.6, "signer outside the trust set is refused"),
        ("partial_never_reaches_gate", t, a, STDOUT_PARTIAL, "valid", 0.6, "CLAIM_MISMATCH stops at verifier even with a valid token"),
        ("mismatch_never_reaches_gate", t, a, STDOUT_MISMATCH, "valid", 0.6, "not_reproduced stops at verifier"),
        ("could_not_run_never_reaches_gate", t, a, STDOUT_CRASH, "valid", 0.6, "RUN_FAILED stops at stage run"),
        ("unpinned_commit_never_reaches_gate", t_unpinned, base_attempt(t_unpinned), STDOUT_FULL, "valid", 0.6, "NO_COMMIT_PINNED stops at verifier"),
        ("low_confidence_refused", t, a_low, STDOUT_FULL, "valid", 0.6, "CONFIDENCE_BELOW_FLOOR stops at verifier"),
    ]
    for cid, tt, aa, table, mode, floor, desc in rec:
        cases.append(_case("repro_record", cid, desc, _record_input(tt, aa, table, approval=mode, floor=floor)))
    a_bad = base_attempt(t, target_hash="0" * 64, prompt_hash="nothex")
    cases.append(_case("repro_record", "malformed_attempt_logs_nothing", "attempt bound to the wrong target: refused before anything is logged", _record_input(t, a_bad, STDOUT_FULL, approval="valid")))

    # repro_dataset_manifest
    r1 = record_from_input(_record_input(t, a, STDOUT_FULL, approval="valid"))["report"]
    t2 = base_target(claims=[ClaimSpec("accuracy", "edge", 0.85, "fraction", 0.01)])
    a2 = base_attempt(t2, selectors=[OutputSelector("accuracy", 1, r"accuracy=([0-9.]+)")])
    r2 = record_from_input(_record_input(t2, a2, STDOUT_FULL, approval="valid"))["report"]
    cases.append(_case("repro_dataset_manifest", "two_reports", "two signed reports; rows sorted by report_id; per-row sha256 + dataset_hash", {"reports": [r1, r2], "version": "1.0.0"}))
    cases.append(_case("repro_dataset_manifest", "two_reports_reversed", "input order must not change the manifest", {"reports": [r2, r1], "version": "1.0.0"}))
    cases.append(_case("repro_dataset_manifest", "empty", "empty dataset still has a hash", {"reports": [], "version": "1.0.0"}))
    return cases


# ---- handlers -------------------------------------------------------------

def _mk(kind: str) -> Handler:
    def h(inp, exp):
        return expect_equal(compute_expected(kind, inp), exp)
    h.__name__ = f"h_{kind}"
    return h


CONFORMANCE_HANDLERS: Dict[str, Handler] = {
    k: _mk(k) for k in ("repro_target_hash", "repro_judge", "repro_rules", "repro_approval_summary", "repro_record", "repro_dataset_manifest")
}
