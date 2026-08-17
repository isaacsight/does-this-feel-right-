"""Claims, computations, and the manifest that links them.

Every number in a paper is a ``Claim``: a value with a unit and a tolerance,
located in the manuscript, hash-linked to the ``Computation`` that produced
it. Both ids are content hashes of their bodies, so a claim that changes its
value changes its id, and a manifest that lies about which computation
backs which claim fails validation rather than verification.

``provenance-manifest.json``::

    {"format_version": 1,
     "paper": {"doc_hash": "...", "title": "..."},
     "computations": [...], "claims": [...],
     "edges": [{"claim_id": "...", "computation_id": "..."}]}
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from ..core.envelope import content_hash

MANIFEST_FORMAT_VERSION = 1
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _num(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


@dataclass(frozen=True)
class Claim:
    value: float
    unit: str
    location: Dict[str, Any]
    source_doc_hash: str
    computation_ref: str
    model_lineage: List[dict]
    confidence: float
    tolerance: float = 0.0
    claim_id: str = ""

    def body(self) -> dict:
        return {
            "value": self.value,
            "unit": self.unit,
            "tolerance": self.tolerance,
            "location": dict(self.location),
            "source_doc_hash": self.source_doc_hash,
            "computation_ref": self.computation_ref,
            "model_lineage": [dict(m) for m in self.model_lineage],
            "confidence": self.confidence,
        }

    def to_json(self) -> dict:
        return {"claim_id": self.claim_id, **self.body()}

    @staticmethod
    def build(**fields: Any) -> "Claim":
        """Construct with ``claim_id`` = content hash of the body."""
        c = Claim(claim_id="", **fields)
        return Claim(claim_id=content_hash(c.body()), **fields)

    @staticmethod
    def from_json(d: Mapping[str, Any]) -> "Claim":
        return Claim(
            value=d["value"],
            unit=d["unit"],
            location=dict(d.get("location", {})),
            source_doc_hash=d["source_doc_hash"],
            computation_ref=d["computation_ref"],
            model_lineage=[dict(m) for m in d.get("model_lineage", [])],
            confidence=d["confidence"],
            tolerance=d.get("tolerance", 0.0),
            claim_id=d.get("claim_id", ""),
        )


def claim_id_of(claim: Claim) -> str:
    return content_hash(claim.body())


@dataclass(frozen=True)
class Computation:
    """How a number was made. ``entrypoint`` is the script (relative to the
    workdir) whose bytes hash to ``entrypoint_hash``; ``input_hashes`` pin
    every file it reads; ``environment`` is declared, never auto-detected;
    ``output_selector`` says where in stdout the number is: a JSON pointer
    (``/mean``), a regex with one group (``re:mean=([0-9.]+)``), or ``""``
    for the whole of stdout."""

    command: List[str]
    entrypoint: str
    entrypoint_hash: str
    input_hashes: Dict[str, str]
    environment: Dict[str, Any]
    output_selector: str
    expected_output_hash: Optional[str] = None
    computation_id: str = ""

    def body(self) -> dict:
        d: Dict[str, Any] = {
            "command": list(self.command),
            "entrypoint": self.entrypoint,
            "entrypoint_hash": self.entrypoint_hash,
            "input_hashes": dict(self.input_hashes),
            "environment": dict(self.environment),
            "output_selector": self.output_selector,
        }
        if self.expected_output_hash is not None:
            d["expected_output_hash"] = self.expected_output_hash
        return d

    def to_json(self) -> dict:
        return {"computation_id": self.computation_id, **self.body()}

    @staticmethod
    def build(**fields: Any) -> "Computation":
        c = Computation(computation_id="", **fields)
        return Computation(computation_id=content_hash(c.body()), **fields)

    @staticmethod
    def from_json(d: Mapping[str, Any]) -> "Computation":
        return Computation(
            command=list(d["command"]),
            entrypoint=d["entrypoint"],
            entrypoint_hash=d["entrypoint_hash"],
            input_hashes=dict(d.get("input_hashes", {})),
            environment=dict(d.get("environment", {})),
            output_selector=d.get("output_selector", ""),
            expected_output_hash=d.get("expected_output_hash"),
            computation_id=d.get("computation_id", ""),
        )


def computation_id_of(c: Computation) -> str:
    return content_hash(c.body())


def manifest_hash(manifest: Mapping[str, Any]) -> str:
    """Content hash of the whole manifest; key order does not matter."""
    return content_hash(dict(manifest))


@dataclass(frozen=True)
class ManifestShape:
    ok: bool
    errors: List[str] = field(default_factory=list)
    claims: List[Claim] = field(default_factory=list)
    computations: List[Computation] = field(default_factory=list)
    edges: Dict[str, str] = field(default_factory=dict)  # claim_id -> computation_id

    def to_json(self) -> dict:
        return {"ok": self.ok, "errors": list(self.errors)}


def validate_manifest(manifest: Any) -> ManifestShape:
    """Structural validation. Errors sorted. Checks: format version, paper
    doc hash, ids are content hashes of their bodies, duplicate ids,
    dangling edges (either end), missing or malformed input hashes, bad
    tolerance, claim/paper doc-hash agreement."""
    if not isinstance(manifest, Mapping):
        return ManifestShape(False, ["manifest is not an object"])
    errors: List[str] = []
    if manifest.get("format_version") != MANIFEST_FORMAT_VERSION:
        errors.append(f"format_version must be {MANIFEST_FORMAT_VERSION}")
    paper = manifest.get("paper")
    paper_hash = None
    if not isinstance(paper, Mapping):
        errors.append("paper must be an object")
    else:
        paper_hash = paper.get("doc_hash")
        if not isinstance(paper_hash, str) or not _SHA256_RE.match(paper_hash):
            errors.append("paper.doc_hash must be sha256 hex")
            paper_hash = None
        if not isinstance(paper.get("title"), str):
            errors.append("paper.title must be a string")

    computations: List[Computation] = []
    comp_ids: Dict[str, int] = {}
    raw_comps = manifest.get("computations")
    if not isinstance(raw_comps, list):
        errors.append("computations must be a list")
        raw_comps = []
    for i, rc in enumerate(raw_comps):
        if not isinstance(rc, Mapping):
            errors.append(f"computations[{i}] is not an object")
            continue
        try:
            c = Computation.from_json(rc)
        except (KeyError, TypeError):
            errors.append(f"computations[{i}] missing required fields")
            continue
        cid = c.computation_id
        if not isinstance(cid, str) or not _SHA256_RE.match(cid):
            errors.append(f"computations[{i}].computation_id must be sha256 hex")
        elif cid != computation_id_of(c):
            errors.append(f"computation {cid[:12]} id does not match body")
        if cid in comp_ids:
            errors.append(f"duplicate computation id {cid[:12]}")
        comp_ids[cid] = i
        if not c.command or not all(isinstance(a, str) for a in c.command):
            errors.append(f"computation {cid[:12]} command must be a non-empty list of strings")
        if not isinstance(c.entrypoint, str) or not c.entrypoint:
            errors.append(f"computation {cid[:12]} entrypoint required")
        if not isinstance(c.entrypoint_hash, str) or not _SHA256_RE.match(c.entrypoint_hash):
            errors.append(f"computation {cid[:12]} entrypoint_hash must be sha256 hex")
        for name, h in sorted(c.input_hashes.items()):
            if not isinstance(h, str) or not _SHA256_RE.match(h):
                errors.append(f"computation {cid[:12]} input {name} hash missing")
        if not isinstance(c.environment, Mapping) or not isinstance(c.environment.get("packages", {}), Mapping):
            errors.append(f"computation {cid[:12]} environment must be {{python, packages}}")
        computations.append(c)

    claims: List[Claim] = []
    claim_ids: Dict[str, int] = {}
    raw_claims = manifest.get("claims")
    if not isinstance(raw_claims, list):
        errors.append("claims must be a list")
        raw_claims = []
    for i, rc in enumerate(raw_claims):
        if not isinstance(rc, Mapping):
            errors.append(f"claims[{i}] is not an object")
            continue
        try:
            c = Claim.from_json(rc)
        except (KeyError, TypeError):
            errors.append(f"claims[{i}] missing required fields")
            continue
        cid = c.claim_id
        if not isinstance(cid, str) or not _SHA256_RE.match(cid):
            errors.append(f"claims[{i}].claim_id must be sha256 hex")
        elif cid != claim_id_of(c):
            errors.append(f"claim {cid[:12]} id does not match body")
        if cid in claim_ids:
            errors.append(f"duplicate claim id {cid[:12]}")
        claim_ids[cid] = i
        if not _num(c.value):
            errors.append(f"claim {cid[:12]} value must be finite number")
        if not _num(c.tolerance) or c.tolerance < 0:
            errors.append(f"claim {cid[:12]} tolerance must be a non-negative number")
        if not isinstance(c.unit, str):
            errors.append(f"claim {cid[:12]} unit must be a string")
        if not _num(c.confidence) or c.confidence < 0 or c.confidence > 1:
            errors.append(f"claim {cid[:12]} confidence must be in [0,1]")
        if not c.model_lineage:
            errors.append(f"claim {cid[:12]} model_lineage required")
        if not isinstance(c.source_doc_hash, str) or not _SHA256_RE.match(c.source_doc_hash):
            errors.append(f"claim {cid[:12]} source_doc_hash must be sha256 hex")
        elif paper_hash is not None and c.source_doc_hash != paper_hash:
            errors.append(f"claim {cid[:12]} source_doc_hash does not match paper.doc_hash")
        if not isinstance(c.location, Mapping) or not c.location:
            errors.append(f"claim {cid[:12]} location required")
        claims.append(c)

    edges: Dict[str, str] = {}
    raw_edges = manifest.get("edges")
    if not isinstance(raw_edges, list):
        errors.append("edges must be a list")
        raw_edges = []
    for i, e in enumerate(raw_edges):
        if not isinstance(e, Mapping) or not isinstance(e.get("claim_id"), str) or not isinstance(e.get("computation_id"), str):
            errors.append(f"edges[{i}] must have claim_id and computation_id")
            continue
        cl, co = e["claim_id"], e["computation_id"]
        if cl not in claim_ids:
            errors.append(f"dangling edge: claim {cl[:12]} not in manifest")
        if co not in comp_ids:
            errors.append(f"dangling edge: computation {co[:12]} not in manifest")
        if cl in edges:
            errors.append(f"claim {cl[:12]} has more than one edge")
        edges[cl] = co
    # A claim with no edge is structurally fine; the DANGLING_COMPUTATION
    # rule catches it. An edge that contradicts the claim's own pointer is
    # a lie in the manifest.
    for c in claims:
        if c.claim_id in edges and c.computation_ref != edges[c.claim_id]:
            errors.append(f"claim {c.claim_id[:12]} computation_ref disagrees with its edge")

    errors = sorted(set(errors))
    if errors:
        return ManifestShape(False, errors)
    return ManifestShape(True, [], claims, computations, edges)
