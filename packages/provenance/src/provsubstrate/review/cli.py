"""``provsub review`` — signed review chains with disclosed AI contribution.

    provsub review open manuscript.json --actor editor.grace --at T [--session-id S] --out chain.json
    provsub review check submission.json [--chain chain.json] [--manuscript-hash H] [--data-as-of T]
    provsub review record submission.json chain.json [--approval tok.json] [--audit audit.jsonl]
                                                     [--trusted ... | --trust ID=FILE] [--manuscript-hash H] [--receipt-out r.json]
    provsub review verify chain.json
    provsub review receipt chain.json --seq N

``check`` prints the disclosure verdict, the rules and the request hash +
summary line the editor signs; ``record`` without ``--approval`` stops at
the gate, with a valid token it appends a hash-only ``reviewed`` entry to
chain.json and prints the reviewer's receipt.
"""

from __future__ import annotations

import argparse

from .._cli_common import add_gate_args, dump_json, fail, gate_summary, load_approval, load_json, load_trusted, open_audit, write_json
from .chain import ReviewChain
from .ledger import REVIEW_MATERIALITY, record_review, review_receipt
from .mcp import review_chain_verify, review_check
from .model import Manuscript, ReviewSubmission


def cmd_open(args: argparse.Namespace) -> int:
    m = Manuscript.from_json(load_json(args.manuscript))
    chain = ReviewChain.open(args.session_id, m, args.actor, args.at)
    write_json(args.out, chain.to_json())
    dump_json({"written": args.out, "head": chain.head(), "manuscript_doc_hash": chain.manuscript_doc_hash()})
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    out = review_check(
        {
            "submission": load_json(args.submission),
            "chain": load_json(args.chain) if args.chain else None,
            "manuscript_hash": args.manuscript_hash,
            "data_as_of": args.data_as_of,
            "session_id": args.session_id,
        }
    )
    if out["shape"]["ok"]:
        out["gate"] = gate_summary(request_hash=out["request_hash"], summary=out["summary"], materiality=REVIEW_MATERIALITY, session_id=args.session_id)
    dump_json(out)
    return 0 if out.get("ok") else 1


def cmd_record(args: argparse.Namespace) -> int:
    sub = ReviewSubmission.from_json(load_json(args.submission))
    chain = ReviewChain.from_json(load_json(args.chain))
    approval = load_approval(args)
    trusted = load_trusted(args)
    if approval is not None and not trusted:
        return fail("record: an approval was given but no trust set (--trusted / --trust); the token cannot be verified")
    r = record_review(
        submission=sub, chain=chain, audit_log=open_audit(args), session_id=args.session_id, trusted=trusted,
        data_as_of=args.data_as_of, approval=approval, manuscript_hash=args.manuscript_hash,
    )
    r.update({"materiality": REVIEW_MATERIALITY, "session_id": args.session_id, "data_as_of": args.data_as_of})
    if r["stage"] == "approval" and approval is None:
        r["gate"] = gate_summary(request_hash=r["request_hash"], summary=r.get("summary"), materiality=REVIEW_MATERIALITY, session_id=args.session_id)
    if r["ok"]:
        write_json(args.chain, chain.to_json())
        r["chain"] = args.chain
        if args.receipt_out:
            write_json(args.receipt_out, r["receipt"])
    dump_json(r)
    return 0 if r["ok"] else 1


def cmd_verify(args: argparse.Namespace) -> int:
    out = review_chain_verify({"chain": load_json(args.chain)})
    dump_json(out)
    return 0 if out["verdict"]["ok"] else 1


def cmd_receipt(args: argparse.Namespace) -> int:
    chain = ReviewChain.from_json(load_json(args.chain))
    entry = next((e for e in chain.entries if e.get("seq") == args.seq), None)
    if entry is None:
        return fail(f"receipt: no entry with seq {args.seq}")
    try:
        dump_json(review_receipt(entry))
    except ValueError as e:
        return fail(str(e))
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("review", help="peer-review provenance: disclosure rules dispose, the editor signs, the chain carries hashes only")
    s = p.add_subparsers(dest="review_cmd")

    o = s.add_parser("open", help="open a manuscript's review chain with a `submitted` entry")
    o.add_argument("manuscript", help="Manuscript JSON {title, doc_hash, venue, round}")
    o.add_argument("--actor", required=True, help="who opens the chain, e.g. editor.grace")
    o.add_argument("--at", required=True, help="timestamp of the submitted entry (ISO 8601)")
    o.add_argument("--session-id", default="provsub-cli")
    o.add_argument("--out", required=True)
    o.set_defaults(func=cmd_open)

    c = s.add_parser("check", help="disclosure verdict + rules; prints the request hash and summary line the editor signs")
    c.add_argument("submission")
    c.add_argument("--chain", default=None, help="the manuscript's chain JSON; without it only shape + disclosure are checked")
    c.add_argument("--manuscript-hash", default=None, help="hash of the manuscript bytes the venue holds")
    c.add_argument("--data-as-of", default="1970-01-01T00:00:00.000Z")
    c.add_argument("--session-id", default="provsub-cli")
    c.set_defaults(func=cmd_check)

    r = s.add_parser("record", help="run the full path; without --approval it stops at the gate; on success extends chain.json")
    r.add_argument("submission")
    r.add_argument("chain")
    r.add_argument("--manuscript-hash", default=None)
    r.add_argument("--receipt-out", default=None, help="write the reviewer's hash-only receipt here")
    add_gate_args(r)
    r.set_defaults(func=cmd_record)

    v = s.add_parser("verify", help="verify a review chain")
    v.add_argument("chain")
    v.set_defaults(func=cmd_verify)

    rc = s.add_parser("receipt", help="reviewer receipt for a `reviewed` entry")
    rc.add_argument("chain")
    rc.add_argument("--seq", type=int, required=True)
    rc.set_defaults(func=cmd_receipt)

    p.set_defaults(func=lambda x: (p.print_help(), 2)[1])
