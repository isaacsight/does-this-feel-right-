"""``provsub bench`` — the quantitative-hallucination benchmark.

    provsub bench run --responder oracle|null|distractor:SEED [--rate R] [--data-as-of T] [--markdown] [--results] [--out report.json]
    provsub bench taskset [--hash] [--dump taskset.json]
    provsub bench score task.json answer.json

No gate here: a run seals its scores in a content-addressed envelope and
prints the request hash. ``--data-as-of`` defaults to the academic v1
constant so a run is a replay, never a clock read.
"""

from __future__ import annotations

import argparse
import sys

from .._cli_common import dump_json, fail, load_json, write_json
from .mcp import DEFAULT_DATA_AS_OF, bench_run, bench_score, bench_taskset


def cmd_run(args: argparse.Namespace) -> int:
    try:
        out = bench_run(
            {
                "responder": args.responder, "seed": args.seed, "rate": args.rate, "data_as_of": args.data_as_of,
                "include_results": args.results or bool(args.out), "markdown": args.markdown,
                "taskset": load_json(args.taskset) if args.taskset else None,
            }
        )
    except ValueError as e:
        return fail(str(e))
    if args.out:
        write_json(args.out, out)
    if args.markdown:
        sys.stdout.write(out["markdown"])
    else:
        dump_json(out)
    return 0


def cmd_taskset(args: argparse.Namespace) -> int:
    out = bench_taskset({"include_tasks": bool(args.dump), "taskset": load_json(args.taskset) if args.taskset else None})
    if args.dump:
        write_json(args.dump, {"format_version": out["format_version"], "name": out["name"], "version": out["version"], "tasks": out["tasks"], "taskset_hash": out["taskset_hash"]})
        out.pop("tasks", None)
    if args.hash:
        print(out["taskset_hash"])
    else:
        dump_json(out)
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    dump_json(bench_score({"task": load_json(args.task), "answer": load_json(args.answer)}))
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("bench", help="quantitative-hallucination benchmark: tasks, scoring, sealed results")
    s = p.add_subparsers(dest="bench_cmd")

    r = s.add_parser("run", help="run a reference responder over the task set and seal the scores")
    r.add_argument("--responder", required=True, help="oracle | null | distractor:SEED")
    r.add_argument("--seed", type=int, default=None, help="distractor seed when not given as distractor:SEED")
    r.add_argument("--rate", type=float, default=0.5, help="distractor rate")
    r.add_argument("--data-as-of", default=DEFAULT_DATA_AS_OF)
    r.add_argument("--taskset", default=None, help="a TaskSet JSON instead of the shipped v1 set")
    r.add_argument("--markdown", action="store_true", help="print the report as markdown")
    r.add_argument("--results", action="store_true", help="include per-task rows in the JSON")
    r.add_argument("--out", default=None, help="write the full report JSON (with per-task rows) here")
    r.set_defaults(func=cmd_run)

    t = s.add_parser("taskset", help="the shipped task set: count, per-domain counts, taskset_hash")
    t.add_argument("--hash", action="store_true", help="print only the taskset_hash")
    t.add_argument("--dump", default=None, help="write the full task set JSON here")
    t.add_argument("--taskset", default=None)
    t.set_defaults(func=cmd_taskset)

    c = s.add_parser("score", help="score one answer against one task (pure)")
    c.add_argument("task")
    c.add_argument("answer")
    c.set_defaults(func=cmd_score)

    p.set_defaults(func=lambda x: (p.print_help(), 2)[1])
