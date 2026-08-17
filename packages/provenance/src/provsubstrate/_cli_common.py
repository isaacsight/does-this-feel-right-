"""Small helpers shared by the wedge CLIs.

JSON in, JSON out. Nothing here reads a clock: every timestamp comes from a
flag (``--data-as-of``, ``--now``, ``--approved-at``). Secrets are read
from files, never from arguments.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .core.approval import ApprovalToken
from .core.audit import AppendOnlyAuditLog

DEFAULT_DATA_AS_OF = "1970-01-01T00:00:00.000Z"
"""Used when ``--data-as-of`` is omitted; echoed in every output so the
replay key is never hidden. Pass a real snapshot date for real work."""

DEFAULT_SESSION_ID = "provsub-cli"


def load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj: Any, *, compact: bool = False) -> None:
    if compact:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
    else:
        sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_secret_file(path: str) -> bytes:
    """Raw bytes of the file with trailing newlines removed (so an ``echo``
    into a file does not silently change the key)."""
    with open(path, "rb") as f:
        data = f.read()
    return data.rstrip(b"\r\n")


def fail(msg: str, code: int = 2) -> int:
    print(f"provsub: {msg}", file=sys.stderr)
    return code


# --- gate plumbing ----------------------------------------------------------


def add_envelope_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--data-as-of", default=DEFAULT_DATA_AS_OF, help=f"snapshot timestamp bound into the request hash (default {DEFAULT_DATA_AS_OF})")
    p.add_argument("--session-id", default=DEFAULT_SESSION_ID, help=f"session the approval must name (default {DEFAULT_SESSION_ID})")


def add_gate_args(p: argparse.ArgumentParser) -> None:
    add_envelope_args(p)
    p.add_argument("--now", default=None, help="timestamp written on audit entries and sealed envelopes (default: --data-as-of); never the system clock")
    p.add_argument("--approval", default=None, help="signed approval token JSON minted by a human with `provsub approve`")
    p.add_argument("--audit", default=None, help="append-only JSONL audit chain to extend (created if missing)")
    p.add_argument("--trusted", action="append", default=[], help="JSON trust set: {approver_id: secret} or [{approver_id, secret_utf8}]; repeatable")
    p.add_argument("--trust", action="append", default=[], metavar="ID=SECRET_FILE", help="trust one approver whose secret is in a file; repeatable")


def now_of(args: argparse.Namespace) -> str:
    return getattr(args, "now", None) or args.data_as_of


def open_audit(args: argparse.Namespace) -> AppendOnlyAuditLog:
    now = now_of(args)
    return AppendOnlyAuditLog(getattr(args, "audit", None), clock=lambda: now)


def load_trusted(args: argparse.Namespace) -> dict[str, bytes]:
    trusted: dict[str, bytes] = {}
    for path in getattr(args, "trusted", []) or []:
        doc = load_json(path)
        if isinstance(doc, dict):
            for k, v in doc.items():
                trusted[str(k)] = str(v).encode("utf-8")
        elif isinstance(doc, list):
            for t in doc:
                trusted[str(t["approver_id"])] = str(t["secret_utf8"]).encode("utf-8")
        else:
            raise TypeError(f"trust set {path}: expected object or array")
    for spec in getattr(args, "trust", []) or []:
        approver_id, _, path = spec.partition("=")
        if not approver_id or not path:
            raise ValueError(f"--trust expects ID=SECRET_FILE, got {spec!r}")
        trusted[approver_id] = read_secret_file(path)
    return trusted


def load_approval(args: argparse.Namespace) -> ApprovalToken | None:
    path = getattr(args, "approval", None)
    if not path:
        return None
    return ApprovalToken.from_json(load_json(path))


def gate_summary(*, request_hash: str | None, summary: str | None, materiality: str, session_id: str) -> dict:
    """What a human needs to see before running `provsub approve`."""
    return {
        "request_hash": request_hash,
        "summary": summary,
        "materiality": materiality,
        "session_id": session_id,
        "next": None
        if request_hash is None or summary is None
        else (
            "provsub approve --request-hash <request_hash> --summary-file <file containing summary> "
            f"--session-id {session_id} --materiality {materiality} --approver-id <you> --secret-file <your secret> --approved-at <ISO time>"
        ),
    }
