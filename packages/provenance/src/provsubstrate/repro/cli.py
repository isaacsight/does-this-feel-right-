"""``provsub repro`` — paper + repo in, attempted reproduction out, signed
report, versioned dataset.

    provsub repro judge target.json attempt.json (--workdir . | --run-record rr.json | --stub stub.json) [--data-as-of T]
    provsub repro record target.json attempt.json (same run source) [--approval tok.json] [--audit audit.jsonl]
                                                  [--trusted ... | --trust ID=FILE] [--report-out report.json]
    provsub repro export reports/*.json --version 1.0.0 --jsonl out.jsonl --manifest m.json
                                        [--zenodo z.json --title T --creator "Name" ... --description D] [--croissant c.json]

``judge`` prints the verdict, the rules and the request hash + summary line
to sign; ``record`` without ``--approval`` stops at the gate. ``export``
writes one canonical JSON line per signed report, sorted by report_id, and
the manifest whose hashes Zenodo and Croissant metadata cite.
"""

from __future__ import annotations

import argparse
import glob
import os

from .._cli_common import add_gate_args, dump_json, fail, gate_summary, load_approval, load_json, load_trusted, open_audit, write_json
from .dataset import DATASET_NAME, croissant_metadata, dataset_manifest, export_jsonl, zenodo_metadata
from .ledger import REPRO_MATERIALITY, record_reproduction
from .mcp import repro_judge, runner_of
from .model import ReproductionAttempt, ReproductionTarget


def _run_args(args: argparse.Namespace) -> dict:
    return {
        "workdir": args.workdir,
        "run_record": load_json(args.run_record) if args.run_record else None,
        "stub": load_json(args.stub) if args.stub else None,
        "timeout": args.timeout,
        "confidence_floor": args.confidence_floor,
    }


def _add_run_flags(p: argparse.ArgumentParser) -> None:
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--workdir", default=None, help="really execute the attempt's commands here")
    g.add_argument("--run-record", default=None, help="an observed RunRecord JSON to judge as-is")
    g.add_argument("--stub", default=None, help='replay table JSON {"table": {"cmd words": {"exit_code", "stdout"}}, "wall_seconds"?}')
    p.add_argument("--timeout", type=float, default=600.0)
    p.add_argument("--confidence-floor", type=float, default=0.6)


def cmd_judge(args: argparse.Namespace) -> int:
    try:
        out = repro_judge({"target": load_json(args.target), "attempt": load_json(args.attempt), **_run_args(args), "data_as_of": args.data_as_of, "session_id": args.session_id})
    except ValueError as e:
        return fail(str(e))
    if out["shape"]["ok"]:
        out["gate"] = gate_summary(request_hash=out["request_hash"], summary=out["summary"], materiality=REPRO_MATERIALITY, session_id=args.session_id)
    dump_json(out)
    return 0 if out.get("ok") else 1


def cmd_record(args: argparse.Namespace) -> int:
    target = ReproductionTarget.from_json(load_json(args.target))
    attempt = ReproductionAttempt.from_json(load_json(args.attempt))
    try:
        runner, label = runner_of(_run_args(args))
    except ValueError as e:
        return fail(str(e))
    approval = load_approval(args)
    trusted = load_trusted(args)
    if approval is not None and not trusted:
        return fail("record: an approval was given but no trust set (--trusted / --trust); the token cannot be verified")
    r = record_reproduction(
        target=target, attempt=attempt, runner=runner, audit_log=open_audit(args), session_id=args.session_id, trusted=trusted,
        data_as_of=args.data_as_of, approval=approval, confidence_floor=args.confidence_floor,
    )
    r.update({"runner": label, "materiality": REPRO_MATERIALITY, "session_id": args.session_id, "data_as_of": args.data_as_of})
    if r["stage"] == "approval" and approval is None:
        r["gate"] = gate_summary(request_hash=r["request_hash"], summary=r.get("summary"), materiality=REPRO_MATERIALITY, session_id=args.session_id)
    if r["ok"] and args.report_out:
        write_json(args.report_out, r["report"])
    dump_json(r)
    return 0 if r["ok"] else 1


def _reports(patterns: list[str]) -> list[dict]:
    out: list[dict] = []
    for pat in patterns:
        paths = sorted(glob.glob(pat)) or ([pat] if os.path.exists(pat) else [])
        if not paths:
            raise FileNotFoundError(pat)
        for p in paths:
            doc = load_json(p)
            # accept a bare signed report or a `repro record` output carrying one
            out.append(doc["report"] if isinstance(doc, dict) and "report" in doc and "report_id" not in doc else doc)
    return out


def cmd_export(args: argparse.Namespace) -> int:
    try:
        reports = _reports(args.reports)
    except FileNotFoundError as e:
        return fail(f"export: no such report {e}")
    manifest = dataset_manifest(reports, args.version)
    if args.jsonl:
        with open(args.jsonl, "w", encoding="utf-8") as f:
            f.write(export_jsonl(reports))
    if args.manifest:
        write_json(args.manifest, manifest)
    if args.zenodo:
        if not args.creator:
            return fail("export: --zenodo needs at least one --creator \"Name\" (or \"Name|Affiliation\")")
        creators = []
        for c in args.creator:
            name, _, aff = c.partition("|")
            creators.append({"name": name.strip(), **({"affiliation": aff.strip()} if aff else {})})
        z = zenodo_metadata(
            manifest,
            title=args.title or f"{DATASET_NAME} {args.version}",
            creators=creators,
            description=args.description or "Signed reproduction reports: paper claims, attempted reproduction, deterministic verdict, human approval.",
            license=args.license,
        )
        write_json(args.zenodo, z)
    if args.croissant:
        write_json(args.croissant, croissant_metadata(manifest, license=args.license, url=args.url, cite_as=args.cite_as))
    dump_json({"row_count": manifest["row_count"], "dataset_hash": manifest["dataset_hash"], "distribution": manifest["distribution"], "written": {k: getattr(args, k) for k in ("jsonl", "manifest", "zenodo", "croissant") if getattr(args, k)}})
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("repro", help="reproducibility ledger: run it, judge it, sign it, export it")
    s = p.add_subparsers(dest="repro_cmd")

    j = s.add_parser("judge", help="verdict + rules for an attempt; prints the request hash and summary line to sign")
    j.add_argument("target")
    j.add_argument("attempt")
    _add_run_flags(j)
    j.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    j.add_argument("--session-id", default="provsub-cli")
    j.set_defaults(func=cmd_judge)

    r = s.add_parser("record", help="run the full path; without --approval it stops at the gate")
    r.add_argument("target")
    r.add_argument("attempt")
    _add_run_flags(r)
    r.add_argument("--report-out", default=None, help="on success, write the signed report JSON here")
    add_gate_args(r)
    r.set_defaults(func=cmd_record)

    e = s.add_parser("export", help="dataset export of signed reports: JSONL + manifest (+ Zenodo / Croissant metadata)")
    e.add_argument("reports", nargs="+", help="signed report JSON files or globs")
    e.add_argument("--version", required=True)
    e.add_argument("--jsonl", default=None)
    e.add_argument("--manifest", default=None)
    e.add_argument("--zenodo", default=None)
    e.add_argument("--croissant", default=None)
    e.add_argument("--title", default=None)
    e.add_argument("--creator", action="append", default=None, help='"Name" or "Name|Affiliation"; repeatable')
    e.add_argument("--description", default=None)
    e.add_argument("--license", default="CC-BY-4.0", help="MIT | CC-BY-4.0 | CC0-1.0")
    e.add_argument("--url", default=None)
    e.add_argument("--cite-as", default=None)
    e.set_defaults(func=cmd_export)

    p.set_defaults(func=lambda x: (p.print_help(), 2)[1])
