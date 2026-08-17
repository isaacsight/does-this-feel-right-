"""JSON-in / JSON-out operations for the repro wedge, shared by the CLI and
the MCP server: judge an attempt (validate, run or replay, verdict, rules,
envelope, summary) and build a dataset manifest. Recording with an approval
and exporting files are CLI-only.

The run comes from one of: ``run_record`` (already observed), ``stub`` (a
table ``"cmd words" -> {exit_code, stdout}`` replayed by ``StubRunner``),
or ``workdir`` (``SubprocessRunner`` really executes the attempt).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .dataset import dataset_manifest, export_jsonl
from .judge import judge, run_repro_rules, validate_attempt
from .ledger import REPRO_MATERIALITY, approval_summary, repro_request
from .model import ReproductionAttempt, ReproductionTarget, RunRecord
from .runner import Runner, StubRunner, SubprocessRunner

DEFAULT_DATA_AS_OF = "1970-01-01T00:00:00.000Z"
DEFAULT_SESSION_ID = "provsub-cli"


class FixedRunner:
    """A runner that replays one already-observed ``RunRecord``."""

    def __init__(self, record: RunRecord):
        self.record = record

    def run(self, target: ReproductionTarget, attempt: ReproductionAttempt) -> RunRecord:
        return self.record


def runner_of(a: Mapping[str, Any]) -> tuple[Runner, str]:
    if a.get("run_record") is not None:
        return FixedRunner(RunRecord.from_json(a["run_record"])), "run_record"
    if a.get("stub") is not None:
        stub = a["stub"]
        table = {k: (int(v["exit_code"]), v.get("stdout", "")) for k, v in stub["table"].items()}
        return StubRunner(table, wall_seconds=float(stub.get("wall_seconds", 0.0))), "stub"
    if a.get("workdir"):
        return SubprocessRunner(a["workdir"], timeout=float(a.get("timeout") or 600.0)), "subprocess"
    raise ValueError("repro needs one of run_record, stub, or workdir to obtain a run")


def repro_judge(a: Mapping[str, Any]) -> dict:
    """Validate the attempt against the target, obtain the run, judge claim
    by claim in decimal, run the rules, and return the envelope hash and
    the exact summary line the reproducer would sign."""
    target = ReproductionTarget.from_json(a["target"])
    attempt = ReproductionAttempt.from_json(a["attempt"])
    errors = validate_attempt(target, attempt)
    if errors:
        return {"shape": {"ok": False, "errors": errors}, "target_hash": target.target_hash()}
    runner, label = runner_of(a)
    record = runner.run(target, attempt)
    verdict = judge(target, attempt, record)
    data_as_of = a.get("data_as_of") or DEFAULT_DATA_AS_OF
    session_id = a.get("session_id") or DEFAULT_SESSION_ID
    req = repro_request(target, attempt, record, data_as_of)
    report = run_repro_rules(target, attempt, verdict, float(a.get("confidence_floor", 0.6)))
    return {
        "shape": {"ok": True, "errors": []},
        "runner": label,
        "target_hash": target.target_hash(),
        "attempt_hash": attempt.attempt_hash(),
        "run_record": record.to_json(),
        "verdict": verdict.to_json(),
        "report": report,
        "ok": report["ok"],
        "data_as_of": data_as_of,
        "session_id": session_id,
        "materiality": REPRO_MATERIALITY,
        "request_hash": req.request_hash(),
        "summary": approval_summary(target, verdict),
    }


def repro_dataset_manifest(a: Mapping[str, Any]) -> dict:
    """Manifest (per-row sha256, dataset_hash, distribution) for a set of
    signed reports, plus the JSONL bytes' sha256. Pure."""
    reports = list(a["reports"])
    m = dataset_manifest(reports, a["version"])
    return {"manifest": m, "jsonl_sha256": m["distribution"]["sha256"], "jsonl_bytes": len(export_jsonl(reports).encode("utf-8"))}


_TARGET = {"type": "object", "description": "ReproductionTarget: paper, repo, claims[{claim_id, description, value, unit, tolerance}], environment_spec, commands"}
_ATTEMPT = {"type": "object", "description": "ReproductionAttempt: target_hash, doc_hash, commands, selectors, model_lineage, prompt_hash, confidence, notes"}
_RUN = {
    "run_record": {"type": "object", "description": "an observed RunRecord to judge as-is"},
    "stub": {"type": "object", "description": "{table: {\"cmd words\": {exit_code, stdout}}, wall_seconds?} replayed by StubRunner"},
    "workdir": {"type": "string", "description": "really execute the attempt's commands here"},
    "confidence_floor": {"type": "number"},
    "data_as_of": {"type": "string"},
    "session_id": {"type": "string"},
}


def mcp_tools() -> list:
    return [
        (
            "repro_judge",
            ("The judge disposes: validate a reproduction attempt against its target, obtain the run (replay a run_record or stub table, or execute in a "
            "workdir), verdict per claim within the paper's tolerance (decimal arithmetic), rules-as-code, and the request_hash + exact summary line the "
            "reproducer must sign with `provsub approve`. Records nothing."),
            {"type": "object", "properties": {"target": _TARGET, "attempt": _ATTEMPT, **_RUN}, "required": ["target", "attempt"]},
            repro_judge,
        ),
        (
            "repro_dataset_manifest",
            "Versioned dataset manifest for signed reproduction reports (rows sorted by report_id, per-row sha256, dataset_hash, JSONL sha256). Pure.",
            {"type": "object", "properties": {"reports": {"type": "array", "items": {"type": "object"}}, "version": {"type": "string"}}, "required": ["reports", "version"]},
            repro_dataset_manifest,
        ),
    ]
