"""``provsub claims`` — every number in a paper, hash-linked to the
computation that produced it; re-execution disposes; the author signs.

    provsub claims verify manifest.json [--workdir .] [--results r.json] [--map python3=/usr/bin/python3] [--data-as-of T]
    provsub claims attest manifest.json [--workdir .|--results r.json] [--approval tok.json] [--audit audit.jsonl]
                                        [--trusted ... | --trust ID=FILE] [--ledger attestations.json]
    provsub claims badge manifest.json (--svg | --json) [--workdir .|--results r.json] [--report verify-output.json]

``verify`` prints per-claim verdicts, the badge, and the attestation
request hash + the multi-line summary the corresponding author signs (use
``--summary-out`` to save it for ``provsub approve --summary-file``).
``attest`` without ``--approval`` stops at the gate.
"""

from __future__ import annotations

import argparse
import sys

from .._cli_common import add_gate_args, dump_json, fail, gate_summary, load_approval, load_json, load_trusted, open_audit, write_json
from .attest import CLAIMS_ATTEST_MATERIALITY, AttestationLedger, ClaimsDeps, attest_manifest, badge_json, badge_svg
from .mcp import claims_verify, reexecutor_of
from .verify import DEFAULT_CONFIDENCE_FLOOR


def _reexec_args(args: argparse.Namespace) -> dict:
    emap = {}
    for spec in getattr(args, "map", None) or []:
        k, _, v = spec.partition("=")
        if not k or not v:
            raise ValueError(f"--map expects NAME=PATH, got {spec!r}")
        emap[k] = v
    return {
        "workdir": args.workdir,
        "results": load_json(args.results) if args.results else None,
        "executable_map": emap or None,
        "timeout": args.timeout,
    }


def _add_reexec_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--workdir", default=None, help="run the computations for real in this directory (entrypoint and input hashes are checked first)")
    p.add_argument("--results", default=None, help="JSON table computation_id -> ExecutionResult to replay instead of running")
    p.add_argument("--map", action="append", default=None, metavar="NAME=PATH", help="resolve a recorded interpreter name, e.g. python3=/usr/bin/python3")
    p.add_argument("--timeout", type=float, default=300.0)
    p.add_argument("--confidence-floor", type=float, default=DEFAULT_CONFIDENCE_FLOOR)


def cmd_verify(args: argparse.Namespace) -> int:
    out = claims_verify({"manifest": load_json(args.manifest), **_reexec_args(args), "data_as_of": args.data_as_of, "session_id": args.session_id, "confidence_floor": args.confidence_floor})
    if out["shape"]["ok"]:
        out["gate"] = gate_summary(request_hash=out["request_hash"], summary=out["summary"], materiality=CLAIMS_ATTEST_MATERIALITY, session_id=args.session_id)
        if args.summary_out:
            with open(args.summary_out, "w", encoding="utf-8") as f:
                f.write(out["summary"] + "\n")
    dump_json(out)
    return 0 if out.get("ok") else 1


def cmd_badge(args: argparse.Namespace) -> int:
    if args.report:
        report = load_json(args.report)
        report = report.get("report", report)
    else:
        v = claims_verify({"manifest": load_json(args.manifest), **_reexec_args(args), "data_as_of": args.data_as_of, "confidence_floor": args.confidence_floor})
        if not v["shape"]["ok"]:
            dump_json(v)
            return 1
        report = v["report"]
    if args.svg:
        sys.stdout.write(badge_svg(report) + "\n")
    else:
        dump_json(badge_json(report))
    return 0


def cmd_attest(args: argparse.Namespace) -> int:
    manifest = load_json(args.manifest)
    rx, label = reexecutor_of(_reexec_args(args))
    approval = load_approval(args)
    trusted = load_trusted(args)
    if approval is not None and not trusted:
        return fail("attest: an approval was given but no trust set (--trusted / --trust); the token cannot be verified")
    ledger = AttestationLedger()
    if args.ledger:
        try:
            ledger.entries = list(load_json(args.ledger))
        except FileNotFoundError:
            pass
    deps = ClaimsDeps(rx, open_audit(args), ledger, trusted, args.confidence_floor)
    results = load_json(args.results) if args.results else None
    r = attest_manifest(manifest, results, deps, approval, session_id=args.session_id, data_as_of=args.data_as_of)
    out = r.to_json()
    out.update({"reexecutor": label, "materiality": CLAIMS_ATTEST_MATERIALITY, "session_id": args.session_id, "data_as_of": args.data_as_of, "detail": r.detail})
    if r.stage == "approval" and approval is None and isinstance(r.detail, dict):
        out["summary"] = r.detail.get("summary")
        out["gate"] = gate_summary(request_hash=r.request_hash, summary=out["summary"], materiality=CLAIMS_ATTEST_MATERIALITY, session_id=args.session_id)
        if args.summary_out:
            with open(args.summary_out, "w", encoding="utf-8") as f:
                f.write(out["summary"] + "\n")
    if r.ok and args.ledger:
        write_json(args.ledger, ledger.to_json())
        out["ledger"] = args.ledger
    dump_json(out)
    return 0 if r.ok else 1


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("claims", help="claim graph: numbers in a paper, re-executed; the corresponding author signs")
    s = p.add_subparsers(dest="claims_cmd")

    v = s.add_parser("verify", help="re-execute and verify every claim; prints the attestation request hash and summary to sign")
    v.add_argument("manifest", help="provenance-manifest.json")
    _add_reexec_flags(v)
    v.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    v.add_argument("--session-id", default="provsub-cli")
    v.add_argument("--summary-out", default=None, help="write the exact multi-line summary here for `provsub approve --summary-file`")
    v.set_defaults(func=cmd_verify)

    b = s.add_parser("badge", help="claims-verified badge as shields.io JSON or SVG")
    b.add_argument("manifest")
    g = b.add_mutually_exclusive_group()
    g.add_argument("--svg", action="store_true")
    g.add_argument("--json", action="store_true")
    b.add_argument("--report", default=None, help="reuse a `claims verify` output instead of re-running")
    _add_reexec_flags(b)
    b.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    b.set_defaults(func=cmd_badge)

    a = s.add_parser("attest", help="run the full path; without --approval it stops at the gate")
    a.add_argument("manifest")
    _add_reexec_flags(a)
    a.add_argument("--ledger", default=None, help="attestation ledger JSON (list of entries) to extend on success")
    a.add_argument("--summary-out", default=None)
    add_gate_args(a)
    a.set_defaults(func=cmd_attest)

    p.set_defaults(func=lambda x: (p.print_help(), 2)[1])
