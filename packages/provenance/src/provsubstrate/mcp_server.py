"""A dependency-free stdio MCP server.

This is how a model uses the substrate: it can *request* a hash, a verdict,
or a chain check inside an envelope; it cannot mint an approval and it cannot
post. Tools are registered by wedge modules through ``mcp_tools()`` hooks
returning ``[(name, description, input_schema, fn)]``.

Implements the subset of MCP needed for tools over newline-delimited JSON-RPC
2.0 on stdin/stdout: ``initialize``, ``notifications/initialized``,
``tools/list``, ``tools/call``, ``ping``.
"""

from __future__ import annotations

import importlib
import json
import sys
from typing import Any, Callable, Dict, List, Tuple

from .core import canonicalize, content_hash, request_hash, verify_chain, chain_entries

WEDGES = ["finance", "lean", "claims", "repro", "bench", "review"]
PROTOCOL_VERSION = "2025-06-18"

Tool = Tuple[str, str, dict, Callable[[dict], Any]]


def _core_tools() -> List[Tool]:
    return [
        (
            "provsub_canonicalize",
            "Canonical JSON (RFC 8785-style, JS number formatting) and its SHA-256 for any JSON value.",
            {"type": "object", "properties": {"value": {}}, "required": ["value"]},
            lambda a: {"canonical": canonicalize(a["value"]), "sha256": content_hash(a["value"])},
        ),
        (
            "provsub_request_hash",
            "Content-addressed request hash: the replay key for an engine call.",
            {
                "type": "object",
                "properties": {
                    "operation": {"type": "string"}, "engine_version": {"type": "string"}, "schema_hash": {"type": "string"},
                    "inputs": {}, "data_as_of": {"type": "string"}, "deterministic_seed": {"type": "string"},
                },
                "required": ["operation", "engine_version", "schema_hash", "inputs", "data_as_of"],
            },
            lambda a: {"request_hash": request_hash(**{k: a[k] for k in a if k in {"operation", "engine_version", "schema_hash", "inputs", "data_as_of", "deterministic_seed"}})},
        ),
        (
            "provsub_audit_verify",
            "Verify a hash chain of audit entries; reports the first broken seq.",
            {"type": "object", "properties": {"entries": {"type": "array"}}, "required": ["entries"]},
            lambda a: {"ok": verify_chain(a["entries"]).ok, "broken_at_seq": verify_chain(a["entries"]).broken_at_seq},
        ),
        (
            "provsub_audit_chain",
            "Build a hash chain over already-timestamped entries (pure; no clock).",
            {"type": "object", "properties": {"entries": {"type": "array"}}, "required": ["entries"]},
            lambda a: {"entries": chain_entries(a["entries"])},
        ),
    ]


def all_tools() -> Dict[str, Tool]:
    tools: Dict[str, Tool] = {t[0]: t for t in _core_tools()}
    for name in WEDGES:
        try:
            mod = importlib.import_module(f"provsubstrate.{name}")
        except ImportError:
            continue
        hook = getattr(mod, "mcp_tools", None)
        if hook:
            for t in hook():
                tools[t[0]] = t
    return tools


def handle(msg: dict, tools: Dict[str, Tool]) -> dict | None:
    mid = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "provenance-substrate", "version": "0.1.0"},
        }}
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": [
            {"name": n, "description": d, "inputSchema": s} for n, d, s, _ in tools.values()
        ]}}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        t = tools.get(name)
        if not t:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown tool {name}"}}
        try:
            out = t[3](args)
            return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}], "isError": False}}
        except Exception as e:  # noqa: BLE001 — surface as tool error, keep the server alive
            return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True}}
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"unknown method {method}"}}


def serve_stdio() -> int:
    tools = all_tools()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(msg, tools)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(serve_stdio())
