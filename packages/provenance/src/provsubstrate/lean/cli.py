"""``provsub lean`` — the model proposes a proof, the Lean kernel disposes,
a mathematician signs.

    provsub lean check FILE.lean|claim.json [--toolchain X --mathlib-rev R] [--project-dir D] [--stub] [--kernel-table t.json]
    provsub lean prepare claim.json [same kernel flags] [--data-as-of T --session-id S] [--confidence-floor F] [--allow AXIOM ...]
    provsub lean record claim.json [same] [--approval tok.json] [--audit audit.jsonl] [--trusted ... | --trust ID=FILE] [--ledger ledger.json]
    provsub lean render claim.json     # the exact bytes the kernel checks, and their hash

``check`` on a ``.lean`` file gives the kernel verdict + static scan; on a
claim it also renders, runs the rules and prints the request hash and the
summary line to sign (same as ``prepare``). ``record`` without
``--approval`` stops at the gate. ``--stub`` needs no Lean installed.
"""

from __future__ import annotations

import argparse
import sys

from .._cli_common import add_gate_args, dump_json, fail, gate_summary, load_approval, load_json, load_trusted, open_audit, write_json
from .kernel import KernelUnavailable
from .ledger import LEAN_RECORD_MATERIALITY, LeanDeps, ProofLedger, record_proof
from .mcp import claim_with_overrides, kernel_of, lean_check, lean_prepare, render
from .rules import DEFAULT_AXIOM_ALLOWLIST, DEFAULT_CONFIDENCE_FLOOR


def _kernel_args(args: argparse.Namespace) -> dict:
    return {
        "stub": args.stub,
        "kernel_table": load_json(args.kernel_table) if args.kernel_table else None,
        "project_dir": args.project_dir,
        "toolchain": args.toolchain,
        "mathlib_rev": args.mathlib_rev,
        "timeout": args.timeout,
    }


def _prepare_args(args: argparse.Namespace) -> dict:
    d = _kernel_args(args)
    d.update(
        {
            "data_as_of": args.data_as_of,
            "session_id": args.session_id,
            "confidence_floor": args.confidence_floor,
            "axiom_allowlist": args.allow if args.allow else None,
        }
    )
    return d


def cmd_check(args: argparse.Namespace) -> int:
    try:
        if args.target.endswith(".lean"):
            with open(args.target, encoding="utf-8") as f:
                out = lean_check({"source": f.read(), **_kernel_args(args)})
            dump_json(out)
            return 0 if out["verdict"]["ok"] else 1
        out = lean_prepare({"claim": load_json(args.target), **_prepare_args(args)})
    except KernelUnavailable as e:
        return fail(str(e))
    dump_json(out)
    return 0 if out.get("ok") else 1


def cmd_prepare(args: argparse.Namespace) -> int:
    try:
        out = lean_prepare({"claim": load_json(args.claim), **_prepare_args(args)})
    except KernelUnavailable as e:
        return fail(str(e))
    if out.get("request_hash"):
        out["gate"] = gate_summary(request_hash=out["request_hash"], summary=out["summary"], materiality=LEAN_RECORD_MATERIALITY, session_id=args.session_id)
    dump_json(out)
    return 0 if out.get("ok") else 1


def cmd_render(args: argparse.Namespace) -> int:
    out = render({"claim": load_json(args.claim), "toolchain": args.toolchain, "mathlib_rev": args.mathlib_rev})
    if args.raw:
        sys.stdout.write(out["source"])
    else:
        dump_json(out)
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    claim = claim_with_overrides(load_json(args.claim), {"toolchain": args.toolchain, "mathlib_rev": args.mathlib_rev})
    try:
        kernel, label = kernel_of(_kernel_args(args))
    except KernelUnavailable as e:
        return fail(str(e))
    approval = load_approval(args)
    trusted = load_trusted(args)
    if approval is not None and not trusted:
        return fail("record: an approval was given but no trust set (--trusted / --trust); the token cannot be verified")
    ledger = ProofLedger()
    if args.ledger:
        try:
            ledger.entries = list(load_json(args.ledger))
        except FileNotFoundError:
            pass
    deps = LeanDeps(
        kernel, open_audit(args), ledger, trusted,
        confidence_floor=args.confidence_floor,
        axiom_allowlist=tuple(args.allow) if args.allow else DEFAULT_AXIOM_ALLOWLIST,
    )
    r = record_proof(claim, deps, approval, session_id=args.session_id, data_as_of=args.data_as_of)
    out = r.to_json()
    out.update({"kernel": label, "materiality": LEAN_RECORD_MATERIALITY, "session_id": args.session_id, "data_as_of": args.data_as_of, "detail": r.detail})
    if r.stage == "approval" and approval is None and isinstance(r.detail, dict):
        out["summary"] = r.detail.get("summary")
        out["gate"] = gate_summary(request_hash=r.request_hash, summary=out["summary"], materiality=LEAN_RECORD_MATERIALITY, session_id=args.session_id)
    if r.ok and args.ledger:
        write_json(args.ledger, ledger.to_json())
        out["ledger"] = args.ledger
    dump_json(out)
    return 0 if r.ok else 1


def _add_kernel_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--toolchain", default=None, help="override/record the toolchain, e.g. leanprover/lean4:v4.12.0")
    p.add_argument("--mathlib-rev", default=None, help="override/record the Mathlib revision")
    p.add_argument("--project-dir", default=None, help="Lake project directory; runs `lake env lean` so Mathlib imports resolve")
    p.add_argument("--stub", action="store_true", help="dry run with the stub kernel (no Lean needed; rejects unless --kernel-table names the file)")
    p.add_argument("--kernel-table", default=None, help="stub table JSON: proof_file_hash -> {ok, errors, sorries, axioms}")
    p.add_argument("--timeout", type=float, default=120.0)


def _add_rule_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--confidence-floor", type=float, default=DEFAULT_CONFIDENCE_FLOOR)
    p.add_argument("--allow", action="append", default=None, metavar="AXIOM", help="axiom allowlist entry; repeatable (default propext, Classical.choice, Quot.sound)")


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("lean", help="proof ledger: the model proposes, the Lean kernel disposes, a mathematician signs")
    s = p.add_subparsers(dest="lean_cmd")

    c = s.add_parser("check", help="kernel verdict + static scan for a .lean file or a proof claim")
    c.add_argument("target", help="FILE.lean or claim.json")
    _add_kernel_flags(c)
    _add_rule_flags(c)
    c.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    c.add_argument("--session-id", default="provsub-cli")
    c.set_defaults(func=cmd_check)

    q = s.add_parser("prepare", help="request hash + the exact summary line a mathematician signs (records nothing)")
    q.add_argument("claim")
    _add_kernel_flags(q)
    _add_rule_flags(q)
    q.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    q.add_argument("--session-id", default="provsub-cli")
    q.set_defaults(func=cmd_prepare)

    r = s.add_parser("render", help="the exact Lean bytes the kernel checks, and their sha256")
    r.add_argument("claim")
    r.add_argument("--toolchain", default=None)
    r.add_argument("--mathlib-rev", default=None)
    r.add_argument("--raw", action="store_true", help="print the .lean source instead of JSON")
    r.set_defaults(func=cmd_render)

    w = s.add_parser("record", help="run the full path; without --approval it stops at the gate")
    w.add_argument("claim")
    _add_kernel_flags(w)
    _add_rule_flags(w)
    w.add_argument("--ledger", default=None, help="proof ledger JSON (list of entries) to extend on success")
    add_gate_args(w)
    w.set_defaults(func=cmd_record)

    p.set_defaults(func=lambda a: (p.print_help(), 2)[1])
