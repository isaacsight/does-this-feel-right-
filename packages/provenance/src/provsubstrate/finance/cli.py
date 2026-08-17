"""``provsub finance`` — reconcile a claim; post it through the ledger gate.

    provsub finance reconcile claim.json bank.json [--policy p.json] [--data-as-of T]
    provsub finance post claim.json bank.json [--policy p.json] [--approval tok.json] [--audit audit.jsonl]
                                              [--trusted trusted.json | --trust ID=SECRET_FILE] [--state state.json]
                                              [--bank-account-code CODE] [--confidence-floor F] [--jurisdiction J]
                                              [--session-id S] [--data-as-of T] [--now T] [--posted-out posted.json]

``post`` without ``--approval`` stops at the gate and prints the request
hash and the exact summary line to sign; with a valid token it posts to an
in-memory ledger (``--posted-out`` keeps the entry). Nothing reads a clock.
"""

from __future__ import annotations

import argparse

from .._cli_common import (
    add_gate_args,
    dump_json,
    fail,
    gate_summary,
    load_approval,
    load_json,
    load_trusted,
    now_of,
    open_audit,
    write_json,
)
from .ledger_post import LEDGER_POST_MATERIALITY, LedgerPostInputs, ledger_post
from .mcp import DEFAULT_BANK_ACCOUNT_CODE, DEFAULT_JURISDICTION, bank_lines_of, build_deps, finance_reconcile, post_result_json


def cmd_reconcile(args: argparse.Namespace) -> int:
    out = finance_reconcile(
        {
            "claim": load_json(args.claim),
            "bank_lines": load_json(args.bank),
            "policy": load_json(args.policy) if args.policy else None,
            "data_as_of": args.data_as_of,
        }
    )
    dump_json(out)
    return 0 if out["shape"]["ok"] else 1


def cmd_post(args: argparse.Namespace) -> int:
    claim = load_json(args.claim)
    bank_lines = bank_lines_of(load_json(args.bank))
    approval = load_approval(args)
    trusted = load_trusted(args)
    if approval is not None and not trusted:
        return fail("post: an approval was given but no trust set (--trusted / --trust); the token cannot be verified")
    now = now_of(args)
    deps = build_deps(
        {
            "engine_version": args.engine_version,
            "confidence_floor": args.confidence_floor,
            "session_id": args.session_id,
            "state": load_json(args.state) if args.state else {},
            "jurisdiction": args.jurisdiction,
        },
        audit_log=open_audit(args),
        trusted=trusted,
        bank_lines=bank_lines,
        now=now,
    )
    inputs = LedgerPostInputs(
        claim=claim,
        bank_lines=bank_lines,
        bank_account_code=args.bank_account_code,
        data_as_of=args.data_as_of,
        policy=load_json(args.policy) if args.policy else None,
        approval=approval,
    )
    r = ledger_post(inputs, deps)
    out = post_result_json(r, deps, session_id=args.session_id, data_as_of=args.data_as_of)
    if r.stage == "approval" and approval is None:
        out["gate"] = gate_summary(request_hash=r.request_hash, summary=out.get("summary"), materiality=LEDGER_POST_MATERIALITY, session_id=args.session_id)
    if r.ok and args.posted_out:
        write_json(args.posted_out, out.get("posted"))
    dump_json(out)
    return 0 if r.ok else 1


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("finance", help="ledger substrate: the AI proposes, arithmetic disposes, an accountant signs")
    s = p.add_subparsers(dest="finance_cmd")

    r = s.add_parser("reconcile", help="arithmetic identity + bank-feed match for one claim (pure)")
    r.add_argument("claim", help="ExtractionClaim JSON")
    r.add_argument("bank", help="bank feed JSON (array of lines or {bank_lines: [...]})")
    r.add_argument("--policy", default=None, help="{amount_tolerance, date_window_days}")
    r.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    r.set_defaults(func=cmd_reconcile)

    q = s.add_parser("post", help="run the ledger post path; without --approval it stops at the gate and prints what to sign")
    q.add_argument("claim")
    q.add_argument("bank")
    q.add_argument("--policy", default=None)
    q.add_argument("--state", default=None, help="verifier state JSON {closed_through?, valid_account_codes?, posted_doc_hashes?}")
    q.add_argument("--bank-account-code", default=DEFAULT_BANK_ACCOUNT_CODE)
    q.add_argument("--confidence-floor", type=float, default=None)
    q.add_argument("--jurisdiction", default=DEFAULT_JURISDICTION)
    q.add_argument("--engine-version", default=None, help="pinned engine identity carried into the envelope (default content-addressed-ledger@0.1.0)")
    q.add_argument("--posted-out", default=None, help="on success, write the posted entry JSON here")
    add_gate_args(q)
    q.set_defaults(func=cmd_post)

    p.set_defaults(func=lambda a: (p.print_help(), 2)[1])
