"""Quantitative-hallucination benchmark: generators, responders, scoring,
the results envelope, and conformance handler round-trips."""

from provsubstrate.bench import (
    CONFORMANCE_HANDLERS,
    CallableResponder,
    DistractorResponder,
    GroundTruth,
    Lcg,
    ModelAnswer,
    NullResponder,
    OracleResponder,
    Task,
    TaskSet,
    compute_expected,
    conformance_cases,
    default_recompute,
    gen_arithmetic_tasks,
    gen_invoice_tasks,
    gen_pdf_text_tasks,
    gen_table_tasks,
    report_markdown,
    run_benchmark,
    score,
    score_with_substrate,
    taskset_v1,
)
from provsubstrate.core import canonicalize

AS_OF = "2026-08-17T00:00:00.000Z"


def test_lcg_is_deterministic_and_seed_sensitive():
    a = [Lcg(5).next() for _ in range(3)]
    b = [Lcg(5).next() for _ in range(3)]
    c = [Lcg(6).next() for _ in range(3)]
    assert a == b and a != c
    r = Lcg(1)
    draws = [r.randint(3, 7) for _ in range(200)]
    assert min(draws) >= 3 and max(draws) <= 7


def test_generators_deterministic_and_seeded():
    for gen in (gen_invoice_tasks, gen_table_tasks, gen_arithmetic_tasks, gen_pdf_text_tasks):
        x = [t.task_id for t in gen(11, 6)]
        y = [t.task_id for t in gen(11, 6)]
        z = [t.task_id for t in gen(12, 6)]
        assert x == y and x != z and len(set(x)) == 6


def test_taskset_v1_fixed():
    ts = taskset_v1()
    assert len(ts.tasks) == 60
    assert ts.taskset_hash == taskset_v1().taskset_hash
    domains = {t.domain for t in ts.tasks}
    assert domains == {"finance", "table", "math", "pdf_text"}
    assert TaskSet.from_json(ts.to_json()).taskset_hash == ts.taskset_hash
    for t in ts.tasks:
        assert t.task_id == Task.from_json(t.to_json()).task_id
        assert t.distractors, t.question


def test_every_task_is_solvable_by_oracle_and_by_recompute_and_every_distractor_is_wrong():
    ts = taskset_v1()
    oracle = OracleResponder()
    for t in ts.tasks:
        assert score(t, oracle.answer(t)).status == "correct"
        r = default_recompute(t)
        assert r is not None
        assert score(t, ModelAnswer(t.task_id, r, t.ground_truth.unit, "", [], "")).status == "correct", (t.domain, t.question, r, t.ground_truth)
        for d in t.distractors:
            assert score(t, ModelAnswer(t.task_id, d, t.ground_truth.unit, "", [], "")).status == "hallucinated"


def test_score_statuses():
    t = Task.create("math", "a = 2\nb = 3\nexpression: a + b\n", "Compute a + b.", GroundTruth(5.0, "integer", 0), [2.0, 3.0, 6.0], {"kind": "arithmetic"})
    assert score(t, ModelAnswer(t.task_id, 5.0, "integer", "", [], "")).status == "correct"
    assert score(t, ModelAnswer(t.task_id, None, "integer", "", [], "")).status == "abstained"
    assert score(t, ModelAnswer(t.task_id, 5.0, "USD", "", [], "")).status == "wrong_unit"
    s = score(t, ModelAnswer(t.task_id, 6.0, "integer", "", [], ""))
    assert s.status == "hallucinated" and s.delta == 1.0
    # tolerance uses decimal delta
    t2 = Task.create("finance", "x", "q", GroundTruth(0.85, "USD", 0.01), [], {})
    assert score(t2, ModelAnswer(t2.task_id, 0.86, "usd", "", [], "")).status == "correct"


def test_score_with_substrate_caught_semantics():
    ts = taskset_v1()
    t = next(x for x in ts.tasks if x.recompute_spec.get("kind") == "invoice_total")
    wrong = ModelAnswer(t.task_id, t.distractors[0], t.ground_truth.unit, "", [], "")
    m = score_with_substrate(t, wrong)
    assert m.raw.status == "hallucinated" and m.recompute_correct and m.caught
    right = ModelAnswer(t.task_id, t.ground_truth.value, t.ground_truth.unit, "", [], "")
    assert not score_with_substrate(t, right).caught
    # substrate that abstains catches nothing
    assert not score_with_substrate(t, wrong, recompute=lambda task: None).caught
    # substrate that is itself wrong catches nothing
    assert not score_with_substrate(t, wrong, recompute=lambda task: 1.0).caught
    # a throwing recompute abstains rather than crashing the bench
    def boom(task):
        raise RuntimeError("no")
    assert score_with_substrate(t, wrong, recompute=boom).recomputed is None


def test_responders():
    ts = taskset_v1()
    assert all(NullResponder().answer(t).value is None for t in ts.tasks)
    d1 = DistractorResponder(7)
    d2 = DistractorResponder(7)
    d3 = DistractorResponder(8)
    a1 = [d1.answer(t).value for t in ts.tasks]
    a2 = [d2.answer(t).value for t in reversed(ts.tasks)][::-1]  # order-independent
    a3 = [d3.answer(t).value for t in ts.tasks]
    assert a1 == a2 and a1 != a3
    wrong = sum(1 for t, v in zip(ts.tasks, a1) if v != t.ground_truth.value)
    assert 0 < wrong < 60
    assert all(DistractorResponder(3, rate=1.0).answer(t).value in t.distractors for t in ts.tasks)
    assert all(DistractorResponder(3, rate=0.0).answer(t).value == t.ground_truth.value for t in ts.tasks)
    # CallableResponder wraps bare numbers, tuples, None and ModelAnswer
    lin = [{"model": "ext", "version": "1"}]
    c = CallableResponder(lambda t: t.ground_truth.value, lin, "p" * 64)
    a = c.answer(ts.tasks[0])
    assert a.value == ts.tasks[0].ground_truth.value and a.model_lineage == lin and a.prompt_hash == "p" * 64
    assert CallableResponder(lambda t: None, lin, "p" * 64).answer(ts.tasks[0]).value is None
    assert CallableResponder(lambda t: (1.5, "EUR", "why"), lin, "p" * 64).answer(ts.tasks[0]).unit == "EUR"


def test_run_benchmark_report_and_envelope():
    ts = taskset_v1()
    r_or = run_benchmark(ts, OracleResponder(), data_as_of=AS_OF)
    assert r_or.totals.n == 60 and r_or.totals.correct == 60 and r_or.hallucination_rate == 0.0 and r_or.caught_rate is None
    r_null = run_benchmark(ts, NullResponder(), data_as_of=AS_OF)
    assert r_null.totals.abstained == 60
    r_d = run_benchmark(ts, DistractorResponder(7), data_as_of=AS_OF)
    assert r_d.totals.hallucinated > 0 and r_d.totals.caught == r_d.totals.hallucinated and r_d.caught_rate == 1.0
    assert r_d.request_hash == run_benchmark(ts, DistractorResponder(7), data_as_of=AS_OF).request_hash
    assert r_d.request_hash != r_or.request_hash
    # order of tasks does not change the envelope
    shuffled = TaskSet(ts.name, ts.version, tuple(reversed(ts.tasks)))
    assert shuffled.taskset_hash != ts.taskset_hash  # the set itself is ordered
    j = r_d.to_json()
    assert set(j["per_domain"]) == {"finance", "table", "math", "pdf_text"}
    assert sum(v["n"] for v in j["per_domain"].values()) == 60
    md = report_markdown(r_d)
    assert "| finance |" in md and "| **all** | 60 |" in md and r_d.request_hash in md and ts.taskset_hash in md


def test_conformance_handlers_round_trip_and_determinism():
    cases = conformance_cases()
    assert {c["kind"] for c in cases} == {"bench_taskset_hash", "bench_score", "bench_report_hash"}
    ids = [(c["kind"], c["id"]) for c in cases]
    assert len(ids) == len(set(ids))
    for c in cases:
        e1 = compute_expected(c["kind"], c["input"])
        e2 = compute_expected(c["kind"], c["input"])
        assert canonicalize(e1) == canonicalize(e2), c["id"]
        ok, detail = CONFORMANCE_HANDLERS[c["kind"]](c["input"], e1)
        assert ok, (c["kind"], c["id"], detail)
    ts_exp = compute_expected("bench_taskset_hash", {"taskset": "v1"})
    assert ts_exp["count"] == 60 and ts_exp["taskset_hash"] == taskset_v1().taskset_hash
    ok, _ = CONFORMANCE_HANDLERS["bench_taskset_hash"]({"taskset": "v1"}, {**ts_exp, "count": 59})
    assert not ok
    assert canonicalize(conformance_cases()) == canonicalize(cases)
