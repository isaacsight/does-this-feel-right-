"""JSON-in / JSON-out operations for the Lean wedge, shared by the CLI and
the MCP server: check a proof (kernel + static scan) and prepare the gate
(request hash + the exact summary line a mathematician signs). Recording
with an approval is CLI-only.

The kernel is either the real ``lean`` / ``lake env lean`` (``LakeDisposer``)
or a ``StubKernel`` whose table is keyed by proof-file hash. A stub with no
table rejects every file, so nothing passes by accident on a dry run.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..core.envelope import sha256_text
from .claim import ProofClaim, proof_file_hash, render_lean_file, validate_claim_shape
from .kernel import KernelDisposer, KernelUnavailable, LakeDisposer, StubKernel, check_proof, static_scan
from .ledger import LEAN_RECORD_MATERIALITY, prepare
from .rules import DEFAULT_AXIOM_ALLOWLIST, DEFAULT_CONFIDENCE_FLOOR

DEFAULT_DATA_AS_OF = "1970-01-01T00:00:00.000Z"
DEFAULT_SESSION_ID = "provsub-cli"


def kernel_of(a: Mapping[str, Any]) -> tuple[KernelDisposer, str]:
    """``(kernel, label)``. ``stub`` (or a ``kernel_table``) selects the stub;
    otherwise the real toolchain, which must be on PATH."""
    if a.get("stub") or a.get("kernel_table") is not None:
        return StubKernel(a.get("kernel_table") or {}), "stub"
    project_dir = a.get("project_dir")
    if not LakeDisposer.available(project_dir):
        which = "lake" if project_dir else "lean"
        raise KernelUnavailable(f"{which} is not on PATH; install a Lean toolchain (elan) or pass stub=true / --stub for a dry run")
    return LakeDisposer(project_dir=project_dir, timeout=float(a.get("timeout") or 120.0)), "lake" if project_dir else "lean"


def claim_with_overrides(claim: Mapping[str, Any], a: Mapping[str, Any]) -> dict:
    c = dict(claim)
    if a.get("toolchain") is not None:
        c["toolchain"] = a["toolchain"]
    if a.get("mathlib_rev") is not None:
        c["mathlib_rev"] = a["mathlib_rev"]
    return c


def lean_check(a: Mapping[str, Any]) -> dict:
    """Kernel verdict merged with the static scan for either a raw Lean
    ``source`` or a proof ``claim`` (rendered to bytes first). With a claim
    the rules and the envelope are included too."""
    if a.get("claim") is not None:
        return lean_prepare(a)
    source = a.get("source")
    if not isinstance(source, str):
        raise TypeError("lean_check needs `claim` (proof claim JSON) or `source` (Lean file text)")
    kernel, label = kernel_of(a)
    v = check_proof(source, kernel)
    return {
        "kernel": label,
        "toolchain": a.get("toolchain"),
        "mathlib_rev": a.get("mathlib_rev"),
        "proof_file_hash": sha256_text(source),
        "verdict": v.to_json(),
        "static_scan": static_scan(source).to_json(),
    }


def lean_prepare(a: Mapping[str, Any]) -> dict:
    """Everything deterministic before the gate: shape, rendered bytes,
    kernel verdict, rules, envelope, and the summary line to sign."""
    claim_json = claim_with_overrides(a["claim"], a)
    shape = validate_claim_shape(claim_json)
    if not shape.ok or shape.claim is None:
        return {"shape": {"ok": False, "errors": list(shape.errors)}}
    claim: ProofClaim = shape.claim
    kernel, label = kernel_of(a)
    data_as_of = a.get("data_as_of") or DEFAULT_DATA_AS_OF
    session_id = a.get("session_id") or DEFAULT_SESSION_ID
    p = prepare(
        claim,
        kernel,
        data_as_of=data_as_of,
        confidence_floor=float(a.get("confidence_floor", DEFAULT_CONFIDENCE_FLOOR)),
        axiom_allowlist=tuple(a.get("axiom_allowlist") or DEFAULT_AXIOM_ALLOWLIST),
    )
    return {
        "shape": {"ok": True, "errors": []},
        "kernel": label,
        "toolchain": claim.toolchain,
        "mathlib_rev": claim.mathlib_rev,
        "source": p.source,
        "proof_file_hash": proof_file_hash(claim),
        "verdict": p.verdict.to_json(),
        "static_scan": static_scan(p.source).to_json(),
        "report": p.report.to_json(),
        "ok": p.report.ok,
        "data_as_of": data_as_of,
        "session_id": session_id,
        "materiality": LEAN_RECORD_MATERIALITY,
        "request_hash": p.request_hash,
        "summary": p.summary,
    }


def render(a: Mapping[str, Any]) -> dict:
    c = ProofClaim.from_json(claim_with_overrides(a["claim"], a))
    return {"source": render_lean_file(c), "proof_file_hash": proof_file_hash(c)}


_CLAIM = {"type": "object", "description": "ProofClaim: theorem_name, statement, proof, imports, model_lineage, prompt_hash, toolchain, mathlib_rev, confidence, doc_hash"}
_KERNEL = {
    "stub": {"type": "boolean", "description": "use the stub kernel (dry run; rejects unless kernel_table has the proof-file hash)"},
    "kernel_table": {"type": "object", "description": "proof_file_hash -> {ok, errors, sorries, axioms} for the stub kernel"},
    "project_dir": {"type": "string", "description": "Lake project for `lake env lean` (Mathlib imports)"},
    "toolchain": {"type": "string"},
    "mathlib_rev": {"type": "string"},
}


def mcp_tools() -> list:
    return [
        (
            "lean_check",
            ("The Lean kernel disposes: check a proof claim (rendered to exact bytes) or raw Lean source with the real toolchain or a stub, "
            "merged with a static scan for sorry/admit/native_decide/axiom. Returns the verdict; with a claim also rules, request_hash and summary."),
            {
                "type": "object",
                "properties": {"claim": _CLAIM, "source": {"type": "string"}, **_KERNEL, "data_as_of": {"type": "string"}, "session_id": {"type": "string"}},
            },
            lean_check,
        ),
        (
            "lean_prepare",
            ("Everything before the gate for a proof claim: shape, rendered file + proof_file_hash, kernel verdict, rules-as-code, and the "
            "request_hash + exact summary line a mathematician must sign with `provsub approve`. Records nothing."),
            {
                "type": "object",
                "properties": {
                    "claim": _CLAIM, **_KERNEL, "data_as_of": {"type": "string"}, "session_id": {"type": "string"},
                    "confidence_floor": {"type": "number"}, "axiom_allowlist": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["claim"],
            },
            lean_prepare,
        ),
    ]
