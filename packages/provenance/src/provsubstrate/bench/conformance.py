"""Conformance catalogue for the quantitative-hallucination benchmark
(academic v1). Kinds: ``bench_taskset_hash`` (the shipped set's hash and
count are fixed), ``bench_score`` (pure scoring), ``bench_report_hash`` (a
full run's envelope hash and counts for the reference responders).
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..conformance.runner import Handler, expect_equal
from .generators import taskset_v1
from .model import GroundTruth, ModelAnswer, Task
from .responders import DistractorResponder, NullResponder, OracleResponder
from .scoring import run_benchmark, score, score_with_substrate

DATA_AS_OF = "2026-08-17T00:00:00.000Z"
MODEL_LINEAGE = [{"model": "local-27b", "version": "conformance"}]
PROMPT_HASH = "b1a4c9d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"


def responder_from_input(inp: dict):
    kind = inp["responder"]
    if kind == "oracle":
        return OracleResponder()
    if kind == "null":
        return NullResponder()
    if kind == "distractor":
        return DistractorResponder(inp.get("seed", 0), inp.get("rate", 0.5))
    raise ValueError(f"unknown responder {kind!r}")


def compute_expected(kind: str, inp: dict) -> Any:
    if kind == "bench_taskset_hash":
        ts = taskset_v1()
        by_domain: Dict[str, int] = {}
        for t in ts.tasks:
            by_domain[t.domain] = by_domain.get(t.domain, 0) + 1
        return {
            "name": ts.name, "version": ts.version, "count": len(ts.tasks), "taskset_hash": ts.taskset_hash,
            "by_domain": {k: by_domain[k] for k in sorted(by_domain)},
            "first_task_id": ts.tasks[0].task_id, "last_task_id": ts.tasks[-1].task_id,
        }
    if kind == "bench_score":
        task = Task.from_json(inp["task"])
        ans = ModelAnswer.from_json(inp["answer"])
        m = score_with_substrate(task, ans)
        return {"score": score(task, ans).to_json(), "mitigated": m.to_json()}
    if kind == "bench_report_hash":
        r = run_benchmark(taskset_v1(), responder_from_input(inp), data_as_of=inp["data_as_of"])
        j = r.to_json()
        return {
            "request_hash": j["request_hash"], "taskset_hash": j["taskset_hash"], "totals": j["totals"],
            "hallucination_rate": j["hallucination_rate"], "caught_rate": j["caught_rate"], "per_domain": j["per_domain"],
        }
    raise KeyError(f"bench: unknown conformance kind {kind!r}")


def _case(kind: str, cid: str, description: str, inp: dict) -> dict:
    return {"kind": kind, "id": cid, "description": description, "input": inp}


def _answer(task: Task, value, unit=None, rationale="") -> dict:
    return ModelAnswer(task.task_id, value, task.ground_truth.unit if unit is None else unit, rationale, MODEL_LINEAGE, PROMPT_HASH).to_json()


def conformance_cases() -> List[dict]:
    cases: List[dict] = []
    ts = taskset_v1()
    cases.append(_case("bench_taskset_hash", "v1", "taskset_v1: 60 tasks, fixed hash", {"taskset": "v1"}))

    inv_total = next(t for t in ts.tasks if t.recompute_spec.get("kind") == "invoice_total")
    inv_line = next(t for t in ts.tasks if t.recompute_spec.get("kind") == "invoice_line")
    table_mean = next(t for t in ts.tasks if t.recompute_spec.get("agg") == "mean")
    table_sum = next(t for t in ts.tasks if t.recompute_spec.get("agg") == "sum")
    math_t = next(t for t in ts.tasks if t.domain == "math")
    pdf_t = next(t for t in ts.tasks if t.domain == "pdf_text")

    score_cases = [
        ("correct_exact", inv_total, _answer(inv_total, inv_total.ground_truth.value), "exact ground truth is correct; substrate agrees; nothing to catch"),
        ("hallucinated_previous_total", inv_total, _answer(inv_total, inv_total.distractors[0]), "picks the previous-statement total: hallucinated and caught"),
        ("abstained", inv_total, _answer(inv_total, None), "no value is abstained; not caught (nothing wrong to catch)"),
        ("wrong_unit", inv_total, _answer(inv_total, inv_total.ground_truth.value, unit="EUR"), "right number wrong unit"),
        ("line_amount_off_by_unit_price", inv_line, _answer(inv_line, inv_line.distractors[0]), "line question answered with the unit price"),
        ("mean_within_tolerance", table_mean, _answer(table_mean, table_mean.ground_truth.value + 0.004), "mean off by 0.004 within tol 0.005 is correct"),
        ("mean_just_outside", table_mean, _answer(table_mean, table_mean.ground_truth.value + 0.006), "mean off by 0.006 outside tol is hallucinated"),
        ("sum_off_by_one", table_sum, _answer(table_sum, table_sum.ground_truth.value + 1), "sum off by one with tol 0"),
        ("math_off_by_one", math_t, _answer(math_t, math_t.distractors[-1]), "arithmetic near-miss"),
        ("pdf_half_year_only", pdf_t, _answer(pdf_t, pdf_t.distractors[0]), "reports first-half revenue as the total"),
    ]
    for cid, task, ans, desc in score_cases:
        cases.append(_case("bench_score", cid, desc, {"task": task.to_json(), "answer": ans}))
    unparsable = Task.create("finance", "no numbers here\n", "What is the total?", GroundTruth(10.0, "USD", 0), [9.0], {"kind": "invoice_total"})
    cases.append(_case("bench_score", "substrate_abstains_on_unparsable", "recompute returns None: wrong answer is not caught", {"task": unparsable.to_json(), "answer": _answer(unparsable, 9.0)}))

    cases.append(_case("bench_report_hash", "oracle", "oracle: zero hallucinations, zero caught", {"responder": "oracle", "data_as_of": DATA_AS_OF}))
    cases.append(_case("bench_report_hash", "null", "null: everything abstained", {"responder": "null", "data_as_of": DATA_AS_OF}))
    cases.append(_case("bench_report_hash", "distractor_seed_7", "distractor at seed 7 rate 0.5: fixed hallucination and caught rates", {"responder": "distractor", "seed": 7, "rate": 0.5, "data_as_of": DATA_AS_OF}))
    cases.append(_case("bench_report_hash", "distractor_seed_7_always", "distractor at seed 7 rate 1.0: every task with distractors is wrong", {"responder": "distractor", "seed": 7, "rate": 1.0, "data_as_of": DATA_AS_OF}))
    return cases


def _mk(kind: str) -> Handler:
    def h(inp, exp):
        return expect_equal(compute_expected(kind, inp), exp)
    h.__name__ = f"h_{kind}"
    return h


CONFORMANCE_HANDLERS: Dict[str, Handler] = {k: _mk(k) for k in ("bench_taskset_hash", "bench_score", "bench_report_hash")}
