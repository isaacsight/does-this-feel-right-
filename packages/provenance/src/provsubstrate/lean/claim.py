"""Proof claims and the exact bytes the kernel checks.

A model that says "here is a proof of `foo`" has made a *claim*. The claim
carries the model's lineage, the hash of the prompt it answered, the
toolchain and Mathlib revision it targeted, and the hash of the statement
it believes it proved. None of that is trusted: ``render_lean_file`` turns
the claim into one deterministic Lean source file, and the SHA-256 of those
bytes (``proof_file_hash``) is what the kernel verdict, the summary line the
mathematician signs, and the ledger entry all refer to. Same claim, same
bytes, same hash — on any machine.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional

from ..core.envelope import sha256_text

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
# Lean identifiers: a letter or underscore, then word characters, primes and
# dots (namespaces). Unicode letters are allowed; ``\w`` is unicode-aware.
_LEAN_NAME_RE = re.compile(r"^[^\W\d][\w'.]*$")


@dataclass(frozen=True)
class ProofClaim:
    """The model's proposal. ``doc_hash`` is sha256 of ``statement`` — the
    document the model "read" is the statement it was asked to prove."""

    theorem_name: str
    statement: str
    proof: str
    imports: List[str]
    model_lineage: List[dict]
    prompt_hash: str
    toolchain: str
    mathlib_rev: str
    confidence: float
    doc_hash: str

    def to_json(self) -> dict:
        return {
            "theorem_name": self.theorem_name,
            "statement": self.statement,
            "proof": self.proof,
            "imports": list(self.imports),
            "model_lineage": [dict(m) for m in self.model_lineage],
            "prompt_hash": self.prompt_hash,
            "toolchain": self.toolchain,
            "mathlib_rev": self.mathlib_rev,
            "confidence": self.confidence,
            "doc_hash": self.doc_hash,
        }

    @staticmethod
    def from_json(d: Mapping[str, Any]) -> "ProofClaim":
        return ProofClaim(
            theorem_name=d["theorem_name"],
            statement=d["statement"],
            proof=d["proof"],
            imports=list(d.get("imports", [])),
            model_lineage=[dict(m) for m in d["model_lineage"]],
            prompt_hash=d["prompt_hash"],
            toolchain=d.get("toolchain", ""),
            mathlib_rev=d.get("mathlib_rev", ""),
            confidence=d["confidence"],
            doc_hash=d["doc_hash"],
        )


def statement_hash(statement: str) -> str:
    """The claim's ``doc_hash`` must equal this; the rule
    ``STATEMENT_HASH_MISMATCH`` says so."""
    return sha256_text(statement)


@dataclass(frozen=True)
class ClaimShape:
    ok: bool
    errors: List[str] = field(default_factory=list)
    claim: Optional[ProofClaim] = None

    def to_json(self) -> dict:
        return {"ok": self.ok, "errors": list(self.errors)}


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and x not in (float("inf"), float("-inf"))


def validate_claim_shape(claim: Any) -> ClaimShape:
    """Structural validation for a proof claim arriving from any model.
    Errors are sorted so two implementations report the same list. Pure."""
    if not isinstance(claim, Mapping):
        return ClaimShape(False, ["claim is not an object"])
    errors: List[str] = []
    name = claim.get("theorem_name")
    if not isinstance(name, str) or not _LEAN_NAME_RE.match(name):
        errors.append("theorem_name must be a Lean identifier")
    if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
        errors.append("statement must be non-empty string")
    if not isinstance(claim.get("proof"), str) or not claim["proof"].strip():
        errors.append("proof must be non-empty string")
    imports = claim.get("imports", [])
    if not isinstance(imports, list) or any(not isinstance(i, str) or not i for i in imports):
        errors.append("imports must be a list of module names")
    lineage = claim.get("model_lineage")
    if not isinstance(lineage, list) or len(lineage) == 0:
        errors.append("model_lineage required")
    else:
        for i, m in enumerate(lineage):
            if not isinstance(m, Mapping) or not isinstance(m.get("model"), str) or not isinstance(m.get("version"), str):
                errors.append(f"model_lineage[{i}] must have model and version")
    if not isinstance(claim.get("prompt_hash"), str) or not _SHA256_RE.match(claim["prompt_hash"]):
        errors.append("prompt_hash must be sha256 hex")
    if not isinstance(claim.get("toolchain"), str):
        errors.append("toolchain must be a string")
    if not isinstance(claim.get("mathlib_rev"), str):
        errors.append("mathlib_rev must be a string")
    conf = claim.get("confidence")
    if not _is_number(conf) or conf < 0 or conf > 1:
        errors.append("confidence must be in [0,1]")
    if not isinstance(claim.get("doc_hash"), str) or not _SHA256_RE.match(claim["doc_hash"]):
        errors.append("doc_hash must be sha256 hex")
    errors.sort()
    if errors:
        return ClaimShape(False, errors)
    return ClaimShape(True, [], ProofClaim.from_json(claim))


def _is_tactic_block(proof: str) -> bool:
    return proof == "by" or (proof.startswith("by") and proof[2:3].isspace())


def render_lean_file(claim: ProofClaim) -> str:
    """The exact bytes the kernel checks. Imports first, a blank line, then
    the theorem. A proof beginning with ``by`` is a tactic block; anything
    else is a term. One-line bodies stay on the header line
    (``:= by simp``, ``:= fun n => rfl``); multi-line bodies are dedented
    and re-indented by exactly two spaces on the following lines. Trailing
    newline, LF only, no tabs introduced."""
    lines: List[str] = [f"import {imp}" for imp in claim.imports]
    if lines:
        lines.append("")
    proof = claim.proof.strip("\n").strip()
    header = f"theorem {claim.theorem_name} : {claim.statement.strip()}"
    if _is_tactic_block(proof):
        body = textwrap.dedent(proof[2:].strip("\n")).strip("\n")
        if body.strip() == "":
            lines.append(header + " := by")
        elif "\n" not in body:
            # A one-liner keeps its shape: `... := by simp`.
            lines.append(header + " := by " + body.strip())
        else:
            lines.append(header + " := by")
            for ln in body.splitlines():
                lines.append(("  " + ln) if ln.strip() else "")
    else:
        body = textwrap.dedent(proof).strip("\n")
        if "\n" not in body:
            lines.append(header + " := " + body.strip())
        else:
            lines.append(header + " :=")
            for ln in body.splitlines():
                lines.append(("  " + ln) if ln.strip() else "")
    return "\n".join(lines) + "\n"


def proof_file_hash(claim: ProofClaim) -> str:
    return sha256_text(render_lean_file(claim))
