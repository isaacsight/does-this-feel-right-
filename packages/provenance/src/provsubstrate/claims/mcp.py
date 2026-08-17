"""JSON-in / JSON-out operations for the claims wedge, shared by the CLI and
the MCP server: verify a manifest (re-execute, per-claim verdicts, rules,
the attestation envelope and the exact summary the author signs) and build
the badge. Attesting with an approval is CLI-only.

Re-execution is chosen by the arguments: ``results`` (a table keyed by
computation id) replays canned runs; ``workdir`` runs the computations for
real with ``SubprocessReexecutor``; neither means every claim is
``execution_failed`` (nothing was observed).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .attest import CLAIMS_ATTEST_MATERIALITY, Prepared, badge_json, badge_svg, prepare
from .model import validate_manifest
from .reexec import Reexecutor, StubReexecutor, SubprocessReexecutor
from .verify import DEFAULT_CONFIDENCE_FLOOR

DEFAULT_DATA_AS_OF = "1970-01-01T00:00:00.000Z"
DEFAULT_SESSION_ID = "provsub-cli"


def reexecutor_of(a: Mapping[str, Any]) -> tuple[Reexecutor, str]:
    if a.get("workdir"):
        return (
            SubprocessReexecutor(
                a["workdir"],
                timeout=float(a.get("timeout") or 300.0),
                executable_map=a.get("executable_map") or None,
            ),
            "subprocess",
        )
    return StubReexecutor(a.get("results") or {}), "stub"


def prepared_json(p: Prepared, *, session_id: str, data_as_of: str, reexecutor: str) -> dict:
    return {
        "shape": {"ok": True, "errors": []},
        "reexecutor": reexecutor,
        "manifest_hash": p.manifest_hash,
        "title": p.title,
        "ok": p.ok,
        "outcomes": [
            {
                **o.to_json(),
                "value": o.claim.value,
                "unit": o.claim.unit,
                "tolerance": o.claim.tolerance,
                "report": o.report.to_json(),
                "result": None
                if o.result is None
                else {"ok": o.result.ok, "exit_code": o.result.exit_code, "output_value": o.result.output_value, "output_hash": o.result.output_hash, "input_mismatches": list(o.result.input_mismatches), "stderr": o.result.stderr[-2000:]},
            }
            for o in p.outcomes
        ],
        "report": p.report(),
        "badge": badge_json(p.report()),
        "data_as_of": data_as_of,
        "session_id": session_id,
        "materiality": CLAIMS_ATTEST_MATERIALITY,
        "request_hash": p.request_hash,
        "summary": p.summary,
    }


def claims_verify(a: Mapping[str, Any]) -> dict:
    """Validate the manifest, re-execute (or replay), verify every claim,
    run the rules, and return the attestation envelope hash and the
    multi-line summary the corresponding author would sign."""
    manifest = a["manifest"]
    shape = validate_manifest(manifest)
    if not shape.ok:
        return {"shape": {"ok": False, "errors": list(shape.errors)}}
    rx, label = reexecutor_of(a)
    data_as_of = a.get("data_as_of") or DEFAULT_DATA_AS_OF
    session_id = a.get("session_id") or DEFAULT_SESSION_ID
    p = prepare(manifest, rx, data_as_of=data_as_of, results=a.get("results"), confidence_floor=float(a.get("confidence_floor", DEFAULT_CONFIDENCE_FLOOR)))
    return prepared_json(p, session_id=session_id, data_as_of=data_as_of, reexecutor=label)


def claims_badge(a: Mapping[str, Any]) -> dict:
    """shields.io JSON and a self-contained SVG. Pass a ``report`` (from
    claims_verify) or a ``manifest`` plus the same re-execution arguments."""
    report = a.get("report")
    if report is None:
        v = claims_verify(a)
        if not v["shape"]["ok"]:
            return v
        report = v["report"]
    return {"report": report, "json": badge_json(report), "svg": badge_svg(report)}


_MANIFEST = {"type": "object", "description": "provenance-manifest.json: {format_version, paper, computations, claims, edges}"}
_REEXEC = {
    "workdir": {"type": "string", "description": "run the computations for real inside this directory"},
    "results": {"type": "object", "description": "computation_id -> ExecutionResult to replay instead of running"},
    "executable_map": {"type": "object", "description": "e.g. {\"python3\": \"/usr/bin/python3\"} to resolve the recorded interpreter"},
    "confidence_floor": {"type": "number"},
    "data_as_of": {"type": "string"},
    "session_id": {"type": "string"},
}


def mcp_tools() -> list:
    return [
        (
            "claims_verify",
            ("Re-execution disposes: validate a provenance manifest, re-run (or replay) each computation, verify every claim within its tolerance, "
            "run the rules, and return per-claim verdicts, the badge, and the attestation request_hash + exact summary the author must sign. Records nothing."),
            {"type": "object", "properties": {"manifest": _MANIFEST, **_REEXEC}, "required": ["manifest"]},
            claims_verify,
        ),
        (
            "claims_badge",
            "Badge (shields.io JSON + SVG) for a verification report, or for a manifest after verifying it.",
            {"type": "object", "properties": {"report": {"type": "object"}, "manifest": _MANIFEST, **_REEXEC}},
            claims_badge,
        ),
    ]
