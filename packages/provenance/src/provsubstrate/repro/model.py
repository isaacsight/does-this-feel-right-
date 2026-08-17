"""Reproducibility-ledger data model.

A ``ReproductionTarget`` is what a paper *says* (claims with tolerances, a
pinned repo commit, a pinned environment, the commands it publishes). A
``ReproductionAttempt`` is the model's *proposal* of how to reproduce it —
which commands to run and which output selectors map to which claims. It is
the claim type of this wedge: it carries ``model_lineage`` and the
``doc_hash`` of the paper it read. A ``RunRecord`` is what actually happened
when a ``Runner`` executed the attempt. Everything is a frozen dataclass with
an explicit JSON shape so hashes are stable across ports.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..core.envelope import content_hash

HEX64 = re.compile(r"^[0-9a-f]{64}$")
GIT_COMMIT = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")

OVERALL_STATUSES = ("reproduced", "partially_reproduced", "not_reproduced", "could_not_run")
CLAIM_STATUSES = ("confirmed", "mismatch", "missing")


def _lineage_json(lineage: Sequence[Mapping[str, Any]]) -> List[dict]:
    # None-safe: a malformed lineage must survive the round trip so validation can name it.
    return [{"model": m.get("model"), "version": m.get("version")} for m in lineage]


@dataclass(frozen=True)
class PaperRef:
    title: str
    doc_hash: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None

    def to_json(self) -> dict:
        return {"title": self.title, "doc_hash": self.doc_hash, "doi": self.doi, "arxiv_id": self.arxiv_id}

    @staticmethod
    def from_json(d: Mapping) -> "PaperRef":
        return PaperRef(d["title"], d["doc_hash"], d.get("doi"), d.get("arxiv_id"))


@dataclass(frozen=True)
class RepoRef:
    url: str
    commit: Optional[str] = None

    def to_json(self) -> dict:
        return {"url": self.url, "commit": self.commit}

    @staticmethod
    def from_json(d: Mapping) -> "RepoRef":
        return RepoRef(d["url"], d.get("commit"))


@dataclass(frozen=True)
class ClaimSpec:
    claim_id: str
    description: str
    value: float
    unit: str
    tolerance: float

    def to_json(self) -> dict:
        return {
            "claim_id": self.claim_id, "description": self.description, "value": self.value, "unit": self.unit, "tolerance": self.tolerance,
        }

    @staticmethod
    def from_json(d: Mapping) -> "ClaimSpec":
        return ClaimSpec(d["claim_id"], d["description"], d["value"], d["unit"], d["tolerance"])


@dataclass(frozen=True)
class ReproductionTarget:
    paper: PaperRef
    repo: RepoRef
    claims: Tuple[ClaimSpec, ...]
    environment_spec: Dict[str, str]
    commands: Tuple[Tuple[str, ...], ...]

    def to_json(self) -> dict:
        return {
            "paper": self.paper.to_json(),
            "repo": self.repo.to_json(),
            "claims": [c.to_json() for c in self.claims],
            "environment_spec": dict(self.environment_spec),
            "commands": [list(c) for c in self.commands],
        }

    @staticmethod
    def from_json(d: Mapping) -> "ReproductionTarget":
        return ReproductionTarget(
            PaperRef.from_json(d["paper"]),
            RepoRef.from_json(d["repo"]),
            tuple(ClaimSpec.from_json(c) for c in d["claims"]),
            dict(d.get("environment_spec") or {}),
            tuple(tuple(str(x) for x in c) for c in d.get("commands") or []),
        )

    def target_hash(self) -> str:
        """Content hash of the target: what an attempt binds to."""
        return content_hash(self.to_json())

    def claim(self, claim_id: str) -> Optional[ClaimSpec]:
        for c in self.claims:
            if c.claim_id == claim_id:
                return c
        return None


@dataclass(frozen=True)
class OutputSelector:
    """How to read one claim's value out of one command's stdout: a regex
    with a capture group. Regex because it is deterministic, dependency-free
    and portable across ports."""

    claim_id: str
    command_index: int
    pattern: str
    group: int = 1

    def to_json(self) -> dict:
        return {"claim_id": self.claim_id, "command_index": self.command_index, "pattern": self.pattern, "group": self.group}

    @staticmethod
    def from_json(d: Mapping) -> "OutputSelector":
        return OutputSelector(d["claim_id"], int(d["command_index"]), d["pattern"], int(d.get("group", 1)))


@dataclass(frozen=True)
class ReproductionAttempt:
    """The model's proposal. ``target_hash`` and ``doc_hash`` bind it to the
    exact target and paper it read; ``confidence`` is its own estimate that
    the selectors map outputs to claims correctly."""

    target_hash: str
    doc_hash: str
    commands: Tuple[Tuple[str, ...], ...]
    selectors: Tuple[OutputSelector, ...]
    model_lineage: List[dict]
    prompt_hash: str
    confidence: float = 1.0
    notes: str = ""

    def to_json(self) -> dict:
        return {
            "target_hash": self.target_hash,
            "doc_hash": self.doc_hash,
            "commands": [list(c) for c in self.commands],
            "selectors": [s.to_json() for s in self.selectors],
            "model_lineage": _lineage_json(self.model_lineage),
            "prompt_hash": self.prompt_hash,
            "confidence": self.confidence,
            "notes": self.notes,
        }

    @staticmethod
    def from_json(d: Mapping) -> "ReproductionAttempt":
        return ReproductionAttempt(
            d["target_hash"],
            d["doc_hash"],
            tuple(tuple(str(x) for x in c) for c in d.get("commands") or []),
            tuple(OutputSelector.from_json(s) for s in d.get("selectors") or []),
            [dict(m) for m in d.get("model_lineage") or []],
            d["prompt_hash"],
            d.get("confidence", 1.0),
            d.get("notes", ""),
        )

    def attempt_hash(self) -> str:
        return content_hash(self.to_json())


@dataclass(frozen=True)
class CommandResult:
    index: int
    exit_code: int
    stdout_sha256: str
    stderr_sha256: str

    def to_json(self) -> dict:
        return {"index": self.index, "exit_code": self.exit_code, "stdout_sha256": self.stdout_sha256, "stderr_sha256": self.stderr_sha256}

    @staticmethod
    def from_json(d: Mapping) -> "CommandResult":
        return CommandResult(int(d["index"]), int(d["exit_code"]), d["stdout_sha256"], d["stderr_sha256"])


@dataclass(frozen=True)
class RunRecord:
    """What the runner observed. ``wall_seconds`` is supplied by the runner's
    clock argument (or is 0.0 when no clock was given) — never read from a
    global clock inside this package."""

    commands: Tuple[CommandResult, ...]
    extracted: Dict[str, Optional[float]]
    wall_seconds: float = 0.0
    error: Optional[str] = None

    def to_json(self) -> dict:
        return {
            "commands": [c.to_json() for c in self.commands],
            "extracted": {k: self.extracted[k] for k in sorted(self.extracted)},
            "wall_seconds": self.wall_seconds,
            "error": self.error,
        }

    @staticmethod
    def from_json(d: Mapping) -> "RunRecord":
        return RunRecord(
            tuple(CommandResult.from_json(c) for c in d.get("commands") or []),
            dict(d.get("extracted") or {}),
            d.get("wall_seconds", 0.0),
            d.get("error"),
        )

    @property
    def succeeded(self) -> bool:
        return self.error is None and all(c.exit_code == 0 for c in self.commands)


@dataclass(frozen=True)
class ClaimVerdict:
    claim_id: str
    status: str  # confirmed | mismatch | missing
    observed: Optional[float]
    delta: Optional[float]

    def to_json(self) -> dict:
        return {"claim_id": self.claim_id, "status": self.status, "observed": self.observed, "delta": self.delta}


@dataclass(frozen=True)
class ReproVerdict:
    overall: str
    per_claim: Tuple[ClaimVerdict, ...] = field(default_factory=tuple)

    @property
    def confirmed(self) -> int:
        return sum(1 for c in self.per_claim if c.status == "confirmed")

    @property
    def total(self) -> int:
        return len(self.per_claim)

    def to_json(self) -> dict:
        return {
            "overall": self.overall,
            "per_claim": [c.to_json() for c in self.per_claim],
            "confirmed": self.confirmed,
            "total": self.total,
        }

    @staticmethod
    def from_json(d: Mapping) -> "ReproVerdict":
        return ReproVerdict(
            d["overall"],
            tuple(ClaimVerdict(c["claim_id"], c["status"], c.get("observed"), c.get("delta")) for c in d.get("per_claim") or []),
        )
