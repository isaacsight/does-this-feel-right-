"""Quantitative-hallucination benchmark: how often does a model invent a
number that is not in the source? The substrate — deterministic recompute
plus a gate — is the mitigation being measured.

Tasks are content-addressed; generators are seeded by explicit argument;
scoring is pure; a run seals its scores in a content-addressed envelope.
"""

from .model import DOMAINS, SCORE_STATUSES, GroundTruth, MitigatedScore, ModelAnswer, Score, Task, TaskSet
from .generators import (
    TASKSET_V1_NAME,
    TASKSET_V1_VERSION,
    Lcg,
    default_recompute,
    gen_arithmetic_tasks,
    gen_invoice_tasks,
    gen_pdf_text_tasks,
    gen_table_tasks,
    taskset_v1,
)
from .responders import CallableResponder, DistractorResponder, NullResponder, OracleResponder, Responder
from .scoring import (
    BENCH_ENGINE_VERSION,
    BENCH_OPERATION,
    BENCH_SCHEMA_HASH,
    DomainCounts,
    Report,
    bench_request,
    report_markdown,
    run_benchmark,
    score,
    score_with_substrate,
)
from .conformance import CONFORMANCE_HANDLERS, compute_expected, conformance_cases
from .mcp import bench_run, bench_score, bench_taskset, mcp_tools, parse_responder

__all__ = [
    "bench_run", "bench_score", "bench_taskset", "mcp_tools", "parse_responder",
    "DOMAINS", "SCORE_STATUSES", "GroundTruth", "MitigatedScore", "ModelAnswer", "Score", "Task", "TaskSet",
    "TASKSET_V1_NAME", "TASKSET_V1_VERSION", "Lcg", "default_recompute",
    "gen_arithmetic_tasks", "gen_invoice_tasks", "gen_pdf_text_tasks", "gen_table_tasks", "taskset_v1",
    "CallableResponder", "DistractorResponder", "NullResponder", "OracleResponder", "Responder",
    "BENCH_ENGINE_VERSION", "BENCH_OPERATION", "BENCH_SCHEMA_HASH", "DomainCounts", "Report",
    "bench_request", "report_markdown", "run_benchmark", "score", "score_with_substrate",
    "CONFORMANCE_HANDLERS", "compute_expected", "conformance_cases",
]
