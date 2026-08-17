"""JSON-in / JSON-out operations for the bench wedge, shared by the CLI and
the MCP server. There is no human gate in this wedge: a benchmark run seals
its scores in a content-addressed envelope and that is the artefact.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .generators import taskset_v1
from .model import ModelAnswer, Task, TaskSet
from .responders import DistractorResponder, NullResponder, OracleResponder, Responder
from .scoring import report_markdown, run_benchmark, score, score_with_substrate

DEFAULT_DATA_AS_OF = "2026-08-17T00:00:00.000Z"
"""The academic v1 constant; a bench run is a replay, so the default is a
fixed date rather than a clock. Pass ``data_as_of`` to bind another one."""


def parse_responder(spec: str, *, seed: int | None = None, rate: float = 0.5) -> Responder:
    """``oracle`` | ``null`` | ``distractor[:SEED]``."""
    if spec == "oracle":
        return OracleResponder()
    if spec == "null":
        return NullResponder()
    if spec == "distractor" or spec.startswith("distractor:"):
        s = seed
        if ":" in spec:
            s = int(spec.split(":", 1)[1])
        return DistractorResponder(0 if s is None else s, rate)
    raise ValueError(f"unknown responder {spec!r}; use oracle | null | distractor:SEED")


def taskset_of(a: Mapping[str, Any]) -> TaskSet:
    ts = a.get("taskset")
    if ts is None or ts == "v1":
        return taskset_v1()
    return TaskSet.from_json(ts)


def bench_taskset(a: Mapping[str, Any]) -> dict:
    ts = taskset_of(a)
    by_domain: dict[str, int] = {}
    for t in ts.tasks:
        by_domain[t.domain] = by_domain.get(t.domain, 0) + 1
    out = {
        "name": ts.name, "version": ts.version, "format_version": ts.format_version, "count": len(ts.tasks), "taskset_hash": ts.taskset_hash,
        "by_domain": {k: by_domain[k] for k in sorted(by_domain)},
        "first_task_id": ts.tasks[0].task_id if ts.tasks else None, "last_task_id": ts.tasks[-1].task_id if ts.tasks else None,
    }
    if a.get("include_tasks"):
        out["tasks"] = [t.to_json() for t in ts.tasks]
    return out


def bench_score(a: Mapping[str, Any]) -> dict:
    """Pure scoring of one answer against one task, plus what deterministic
    recompute would have done."""
    task = Task.from_json(a["task"])
    ans = ModelAnswer.from_json(a["answer"])
    return {"task_id": task.task_id, "score": score(task, ans).to_json(), "mitigated": score_with_substrate(task, ans).to_json()}


def bench_run(a: Mapping[str, Any]) -> dict:
    """Run a reference responder over the task set and seal the scores. Set
    ``include_results`` for per-task rows, ``markdown`` for the report text."""
    responder = parse_responder(str(a.get("responder", "oracle")), seed=a.get("seed"), rate=float(a.get("rate", 0.5)))
    r = run_benchmark(taskset_of(a), responder, data_as_of=a.get("data_as_of") or DEFAULT_DATA_AS_OF)
    j = r.to_json()
    if not a.get("include_results"):
        j.pop("results", None)
    if a.get("markdown"):
        j["markdown"] = report_markdown(r)
    return j


def mcp_tools() -> list:
    return [
        (
            "bench_score",
            ("Score one model answer against one benchmark task (correct | hallucinated | abstained | wrong_unit, decimal delta) and report whether "
            "deterministic recompute would have caught a wrong number. Pure."),
            {"type": "object", "properties": {"task": {"type": "object"}, "answer": {"type": "object"}}, "required": ["task", "answer"]},
            bench_score,
        ),
        (
            "bench_run",
            ("Run a reference responder (oracle | null | distractor with seed/rate) over the shipped quantitative-hallucination task set and seal the "
            "scores in a content-addressed envelope; returns per-domain counts, rates and the request_hash. Deterministic."),
            {
                "type": "object",
                "properties": {
                    "responder": {"type": "string", "description": "oracle | null | distractor | distractor:SEED"},
                    "seed": {"type": "integer"}, "rate": {"type": "number"}, "data_as_of": {"type": "string"},
                    "include_results": {"type": "boolean"}, "markdown": {"type": "boolean"}, "taskset": {"type": "object"},
                },
            },
            bench_run,
        ),
        (
            "bench_taskset",
            "The shipped task set's name, version, count, per-domain counts and taskset_hash (optionally the tasks themselves).",
            {"type": "object", "properties": {"include_tasks": {"type": "boolean"}, "taskset": {"type": "object"}}},
            bench_taskset,
        ),
    ]
