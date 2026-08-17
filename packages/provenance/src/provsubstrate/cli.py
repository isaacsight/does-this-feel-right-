"""``provsub`` — the command line.

Subcommands are registered by wedge modules through ``register(sub)`` hooks so
the CLI stays thin and each wedge owns its own arguments. Core subcommands:
``conformance``, ``audit``, ``hash``, ``approve``, ``mcp``.

``provsub approve`` is the human's step. It mints the signed approval token
that a wedge's ``record`` / ``post`` / ``attest`` command requires. It is
never called by an agent and is deliberately absent from the MCP server: a
model can request a verdict, it cannot mint one.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys

from ._cli_common import dump_json, fail, read_secret_file, write_json
from .conformance import ACADEMIC_V1_DIR, CORE_HANDLERS, FINANCE_V1_DIR, run_conformance
from .core import ApprovalRequest, Approver, canonicalize, content_hash, verify_file

WEDGES = ["finance", "lean", "claims", "repro", "bench", "review"]


def _load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_conformance(args) -> int:
    from .conformance.generate import check as check_academic

    if args.check:
        ok, problems = check_academic()
        for p in problems:
            print(p)
        print("academic v1: no drift" if ok else f"academic v1: {len(problems)} problem(s)")
        return 0 if ok else 1
    suite = args.suite or "finance-v1"
    if suite == "finance-v1":
        try:
            from .finance.conformance import ALL_FINANCE_V1_HANDLERS as handlers
        except ImportError:
            handlers = CORE_HANDLERS
        report = run_conformance(FINANCE_V1_DIR, handlers)
    elif suite == "academic-v1":
        handlers = {}
        for name in WEDGES[1:]:
            try:
                mod = importlib.import_module(f"provsubstrate.{name}")
                handlers.update(getattr(mod, "CONFORMANCE_HANDLERS", {}))
            except ImportError:
                pass
        report = run_conformance(ACADEMIC_V1_DIR, handlers)
    else:
        print(f"unknown suite {suite}; use finance-v1 | academic-v1", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report.to_json(), indent=2))
    else:
        print(report.summary())
        for r in report.results:
            if r.status == "fail":
                print(f"  FAIL {r.path}: {r.detail}")
    if args.strict and (report.failed or report.skipped or not report.manifest_ok):
        return 1
    return 0 if report.ok else 1


def cmd_audit(args) -> int:
    paths = list(args.path)
    if paths and paths[0] == "verify":  # `provsub audit verify FILE` reads naturally; the verb is optional
        paths = paths[1:]
    if not paths:
        return fail("audit: give a JSONL chain path")
    rc = 0
    for path in paths:
        v = verify_file(path)
        if v.ok:
            print(f"chain ok: {path}")
        else:
            print(f"chain BROKEN at seq {v.broken_at_seq}: {path}")
            rc = 1
    return rc


def cmd_hash(args) -> int:
    obj = _load_json(args.path) if args.path != "-" else json.load(sys.stdin)
    if args.canonical:
        print(canonicalize(obj))
    print(content_hash(obj))
    return 0


def cmd_approve(args) -> int:
    """The human's step: sign the exact summary line bound to a request
    hash. ``--approved-at`` is required because nothing here reads a clock;
    the secret comes from a file (trailing newlines stripped), never from
    the command line."""
    if (args.summary is None) == (args.summary_file is None):
        return fail("approve: give exactly one of --summary or --summary-file")
    if args.summary_file is not None:
        with open(args.summary_file, encoding="utf-8") as f:
            summary = f.read()
        # A summary file usually ends in a newline the human did not sign.
        summary = summary.removesuffix("\n")
    else:
        summary = args.summary
    secret = read_secret_file(args.secret_file)
    if not secret:
        return fail("approve: secret file is empty")
    req = ApprovalRequest(args.request_hash, summary, args.session_id, args.materiality)
    token = Approver(args.approver_id, secret).approve(req, args.approved_at).to_json()
    if args.out:
        write_json(args.out, token)
        print(f"approval token written: {args.out}", file=sys.stderr)
    else:
        dump_json(token)
    return 0


def cmd_mcp(args) -> int:
    from .mcp_server import serve_stdio

    return serve_stdio()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="provsub", description="The model proposes, deterministic code disposes, a human signs.")
    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("conformance", help="run a conformance suite or check the academic suite for drift")
    c.add_argument("suite", nargs="?", choices=["finance-v1", "academic-v1"])
    c.add_argument("--check", action="store_true", help="regenerate academic v1 in memory and diff against disk")
    c.add_argument("--json", action="store_true")
    c.add_argument("--strict", action="store_true", help="fail if any kind is skipped or the manifest mismatches")
    c.set_defaults(func=cmd_conformance)

    a = sub.add_parser("audit", help="verify a JSONL hash chain (`provsub audit [verify] audit.jsonl ...`)")
    a.add_argument("path", nargs="+")
    a.set_defaults(func=cmd_audit)

    h = sub.add_parser("hash", help="content hash of a JSON document (canonical JSON, sha256)")
    h.add_argument("path", help="file or - for stdin")
    h.add_argument("--canonical", action="store_true", help="also print the canonical JSON")
    h.set_defaults(func=cmd_hash)

    ap = sub.add_parser(
        "approve",
        help="HUMAN STEP: mint a signed approval token for a request hash + summary line (never run by an agent)",
        description=(
            "Mint the approval token a wedge's record/post/attest command requires. You are signing the exact summary "
            "line a prepare/check command printed, bound to its request hash. Nothing here reads a clock: pass --approved-at."
        ),
    )
    ap.add_argument("--request-hash", required=True)
    ap.add_argument("--summary", default=None, help="the exact summary line to sign")
    ap.add_argument("--summary-file", default=None, help="file holding the exact summary (multi-line summaries); one trailing newline is dropped")
    ap.add_argument("--session-id", required=True)
    ap.add_argument("--materiality", required=True, help="e.g. ledger.post | lean.record | claims.attest | repro.report | review.record")
    ap.add_argument("--approver-id", required=True)
    ap.add_argument("--secret-file", required=True, help="file whose bytes are your HMAC secret (trailing newlines stripped)")
    ap.add_argument("--approved-at", required=True, help="ISO 8601 UTC time of signing, e.g. 2026-08-17T12:00:00.000Z")
    ap.add_argument("--out", default=None, help="write the token JSON here instead of stdout")
    ap.set_defaults(func=cmd_approve)

    m = sub.add_parser("mcp", help="serve the substrate as a stdio MCP server")
    m.set_defaults(func=cmd_mcp)

    for name in WEDGES:
        try:
            mod = importlib.import_module(f"provsubstrate.{name}.cli")
        except ImportError:
            continue
        reg = getattr(mod, "register", None)
        if reg:
            reg(sub)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
