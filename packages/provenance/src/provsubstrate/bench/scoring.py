"""Scoring (the disposer), the results envelope, and the report.

``score`` is pure: abstained, wrong_unit, then correct/hallucinated by a
decimal delta against the task's tolerance. ``score_with_substrate`` adds
what deterministic recompute would have produced and whether it would have
caught the model's wrong number. ``run_benchmark`` seals the per-task scores
into a content-addressed envelope so a reported hallucination rate has a
replay key.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Callable, Dict, List, Mapping, Optional, Sequence

from ..core.canonical import canonicalize
from ..core.envelope import ContentAddressedRequest, sha256_text
from .generators import default_recompute
from .model import MitigatedScore, ModelAnswer, Score, Task, TaskSet
from .responders import Responder

BENCH_OPERATION = "bench.score"
BENCH_ENGINE_VERSION = "quant-bench@0.1.0"
BENCH_SCHEMA_HASH = sha256_text(
    canonicalize(
        {
            "type": "object",
            "fields": {
                "taskset_hash": {"type": "string"},
                "responder": {"type": "ResponderLineage"},
                "scores": {"type": "array", "items": {"type": "TaskScore"}},
            },
        }
    )
)


def _dec(x) -> Decimal:
    return Decimal(repr(float(x)))


def _norm_unit(u: Optional[str]) -> str:
    return (u or "").strip().lower()


def score(task: Task, answer: ModelAnswer) -> Score:
    """abstained (no value) > wrong_unit > correct within tolerance > hallucinated."""
    if answer.value is None:
        return Score("abstained", None)
    gt = task.ground_truth
    try:
        delta = float(_dec(answer.value) - _dec(gt.value))
        within = abs(_dec(answer.value) - _dec(gt.value)) <= _dec(gt.tolerance)
    except (InvalidOperation, ValueError, TypeError):
        return Score("hallucinated", None)
    if _norm_unit(answer.unit) != _norm_unit(gt.unit):
        return Score("wrong_unit", delta)
    return Score("correct" if within else "hallucinated", delta)


def score_with_substrate(task: Task, answer: ModelAnswer, recompute: Callable[[Task], Optional[float]] = default_recompute) -> MitigatedScore:
    """Raw score plus the substrate's view. ``caught`` is true exactly when
    the model's answer was wrong (hallucinated or wrong_unit) and the
    deterministic recompute is right — the case where the ledger would have
    replaced the model's number with the computed one."""
    raw = score(task, answer)
    try:
        recomputed = recompute(task)
    except Exception:  # noqa: BLE001 — a recompute that throws is an abstaining substrate, not a crash of the bench
        recomputed = None
    ok = False
    if recomputed is not None:
        try:
            ok = abs(_dec(recomputed) - _dec(task.ground_truth.value)) <= _dec(task.ground_truth.tolerance)
        except (InvalidOperation, ValueError, TypeError):
            ok = False
    wrong = raw.status in ("hallucinated", "wrong_unit")
    return MitigatedScore(raw, recomputed, ok, bool(wrong and ok))


@dataclass(frozen=True)
class DomainCounts:
    n: int = 0
    correct: int = 0
    hallucinated: int = 0
    abstained: int = 0
    wrong_unit: int = 0
    caught: int = 0

    def to_json(self) -> dict:
        d = {
            "n": self.n, "correct": self.correct, "hallucinated": self.hallucinated, "abstained": self.abstained,
            "wrong_unit": self.wrong_unit, "caught": self.caught,
        }
        d["hallucination_rate"] = _rate(self.hallucinated, self.n)
        d["caught_rate"] = _rate(self.caught, self.hallucinated + self.wrong_unit)
        return d


def _rate(num: int, den: int) -> Optional[float]:
    return None if den == 0 else num / den


@dataclass(frozen=True)
class Report:
    taskset_name: str
    taskset_version: str
    taskset_hash: str
    responder: dict
    engine_version: str
    data_as_of: str
    request_hash: str
    per_domain: Dict[str, DomainCounts]
    totals: DomainCounts
    results: List[dict] = field(default_factory=list)

    @property
    def hallucination_rate(self) -> Optional[float]:
        return _rate(self.totals.hallucinated, self.totals.n)

    @property
    def caught_rate(self) -> Optional[float]:
        return _rate(self.totals.caught, self.totals.hallucinated + self.totals.wrong_unit)

    def to_json(self) -> dict:
        return {
            "taskset_name": self.taskset_name,
            "taskset_version": self.taskset_version,
            "taskset_hash": self.taskset_hash,
            "responder": self.responder,
            "engine_version": self.engine_version,
            "data_as_of": self.data_as_of,
            "request_hash": self.request_hash,
            "per_domain": {k: self.per_domain[k].to_json() for k in sorted(self.per_domain)},
            "totals": self.totals.to_json(),
            "hallucination_rate": self.hallucination_rate,
            "caught_rate": self.caught_rate,
            "results": list(self.results),
        }


def _bump(c: DomainCounts, status: str, caught: bool) -> DomainCounts:
    return DomainCounts(
        c.n + 1,
        c.correct + (status == "correct"),
        c.hallucinated + (status == "hallucinated"),
        c.abstained + (status == "abstained"),
        c.wrong_unit + (status == "wrong_unit"),
        c.caught + (1 if caught else 0),
    )


def bench_request(taskset_hash: str, responder: Mapping, scores: Sequence[Mapping], data_as_of: str) -> ContentAddressedRequest:
    return ContentAddressedRequest(
        operation=BENCH_OPERATION,
        engine_version=BENCH_ENGINE_VERSION,
        schema_hash=BENCH_SCHEMA_HASH,
        inputs={"taskset_hash": taskset_hash, "responder": dict(responder), "scores": [dict(s) for s in scores]},
        data_as_of=data_as_of,
    )


def run_benchmark(
    taskset: TaskSet,
    responder: Responder,
    *,
    data_as_of: str,
    recompute: Callable[[Task], Optional[float]] = default_recompute,
) -> Report:
    """Score every task, roll up per domain, seal the scores in an envelope.
    Results are sorted by task_id so the request hash does not depend on the
    order tasks were answered."""
    per: Dict[str, DomainCounts] = {}
    totals = DomainCounts()
    results: List[dict] = []
    for task in taskset.tasks:
        ans = responder.answer(task)
        m = score_with_substrate(task, ans, recompute)
        results.append(
            {
                "task_id": task.task_id, "domain": task.domain, "status": m.raw.status, "delta": m.raw.delta,
                "recomputed": m.recomputed, "recompute_correct": m.recompute_correct, "caught": m.caught,
            }
        )
        per[task.domain] = _bump(per.get(task.domain, DomainCounts()), m.raw.status, m.caught)
        totals = _bump(totals, m.raw.status, m.caught)
    results.sort(key=lambda r: r["task_id"])
    resp = {"model_lineage": [dict(x) for x in responder.model_lineage], "prompt_hash": responder.prompt_hash}
    scores = [{"task_id": r["task_id"], "status": r["status"], "delta": r["delta"], "caught": r["caught"]} for r in results]
    req = bench_request(taskset.taskset_hash, resp, scores, data_as_of)
    return Report(
        taskset.name, taskset.version, taskset.taskset_hash, resp, BENCH_ENGINE_VERSION, data_as_of, req.request_hash(), per, totals, results,
    )


def _pct(x: Optional[float]) -> str:
    return "n/a" if x is None else f"{x * 100:.1f}%"


def report_markdown(report: Report) -> str:
    """A table per domain plus totals; header lines carry the hashes an
    auditor needs to replay the run."""
    lineage = ", ".join(f"{m.get('model')}@{m.get('version')}" for m in report.responder.get("model_lineage", []))
    lines = [
        f"# Quantitative hallucination benchmark — {report.taskset_name} {report.taskset_version}",
        "",
        f"- taskset_hash: `{report.taskset_hash}`",
        f"- responder: {lineage or '(none)'} prompt `{report.responder.get('prompt_hash', '')[:12]}`",
        f"- engine: `{report.engine_version}` data_as_of {report.data_as_of}",
        f"- request_hash: `{report.request_hash}`",
        "",
        "| domain | n | correct | hallucinated | abstained | wrong_unit | hallucination_rate | caught | caught_rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for dom in sorted(report.per_domain):
        c = report.per_domain[dom]
        lines.append(
            f"| {dom} | {c.n} | {c.correct} | {c.hallucinated} | {c.abstained} | {c.wrong_unit} | "
            f"{_pct(_rate(c.hallucinated, c.n))} | {c.caught} | {_pct(_rate(c.caught, c.hallucinated + c.wrong_unit))} |"
        )
    t = report.totals
    lines.append(
        f"| **all** | {t.n} | {t.correct} | {t.hallucinated} | {t.abstained} | {t.wrong_unit} | "
        f"{_pct(report.hallucination_rate)} | {t.caught} | {_pct(report.caught_rate)} |"
    )
    lines.append("")
    lines.append("caught = model wrong AND deterministic recompute right: the hallucination the substrate would have stopped.")
    return "\n".join(lines) + "\n"
