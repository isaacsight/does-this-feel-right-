"""Quantitative-hallucination benchmark data model.

A ``Task`` is a source text plus a question whose answer is a number the
text determines exactly; ``distractors`` are the plausible wrong numbers a
model might pick instead. ``task_id`` is the content hash of the task, so a
task set is a content-addressed artefact and any two ports agree on which
task is which. ``recompute_spec`` says how deterministic code would derive
the answer from the source — the substrate the benchmark measures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..core.envelope import content_hash, sha256_text

DOMAINS = ("finance", "table", "pdf_text", "math")
SCORE_STATUSES = ("correct", "hallucinated", "abstained", "wrong_unit")
TASKSET_FORMAT_VERSION = 1


@dataclass(frozen=True)
class GroundTruth:
    value: float
    unit: str
    tolerance: float

    def to_json(self) -> dict:
        return {"value": self.value, "unit": self.unit, "tolerance": self.tolerance}

    @staticmethod
    def from_json(d: Mapping) -> "GroundTruth":
        return GroundTruth(d["value"], d["unit"], d["tolerance"])


@dataclass(frozen=True)
class Task:
    task_id: str
    domain: str
    source_text: str
    question: str
    ground_truth: GroundTruth
    distractors: Tuple[float, ...]
    source_doc_hash: str
    recompute_spec: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def body(domain: str, source_text: str, question: str, ground_truth: GroundTruth, distractors: Sequence[float], recompute_spec: Mapping) -> dict:
        return {
            "domain": domain,
            "source_text": source_text,
            "question": question,
            "ground_truth": ground_truth.to_json(),
            "distractors": list(distractors),
            "source_doc_hash": sha256_text(source_text),
            "recompute_spec": dict(recompute_spec),
        }

    @staticmethod
    def create(domain: str, source_text: str, question: str, ground_truth: GroundTruth, distractors: Sequence[float], recompute_spec: Optional[Mapping] = None) -> "Task":
        if domain not in DOMAINS:
            raise ValueError(f"Task: unknown domain {domain!r}")
        b = Task.body(domain, source_text, question, ground_truth, distractors, recompute_spec or {})
        return Task(content_hash(b), domain, source_text, question, ground_truth, tuple(distractors), b["source_doc_hash"], dict(recompute_spec or {}))

    def to_json(self) -> dict:
        return {"task_id": self.task_id, **Task.body(self.domain, self.source_text, self.question, self.ground_truth, self.distractors, self.recompute_spec)}

    @staticmethod
    def from_json(d: Mapping) -> "Task":
        return Task(
            d["task_id"], d["domain"], d["source_text"], d["question"], GroundTruth.from_json(d["ground_truth"]),
            tuple(d.get("distractors") or []), d["source_doc_hash"], dict(d.get("recompute_spec") or {}),
        )


@dataclass(frozen=True)
class TaskSet:
    name: str
    version: str
    tasks: Tuple[Task, ...]
    format_version: int = TASKSET_FORMAT_VERSION

    @staticmethod
    def hash_of(name: str, version: str, tasks: Sequence[Task], format_version: int = TASKSET_FORMAT_VERSION) -> str:
        return content_hash({"format_version": format_version, "name": name, "version": version, "tasks": [t.to_json() for t in tasks]})

    @property
    def taskset_hash(self) -> str:
        return TaskSet.hash_of(self.name, self.version, self.tasks, self.format_version)

    def to_json(self) -> dict:
        return {
            "format_version": self.format_version, "name": self.name, "version": self.version,
            "tasks": [t.to_json() for t in self.tasks], "taskset_hash": self.taskset_hash,
        }

    @staticmethod
    def from_json(d: Mapping) -> "TaskSet":
        return TaskSet(d["name"], d["version"], tuple(Task.from_json(t) for t in d["tasks"]), d.get("format_version", TASKSET_FORMAT_VERSION))

    def by_id(self, task_id: str) -> Optional[Task]:
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        return None


@dataclass(frozen=True)
class ModelAnswer:
    task_id: str
    value: Optional[float]
    unit: str
    rationale: str
    model_lineage: List[dict]
    prompt_hash: str

    def to_json(self) -> dict:
        return {
            "task_id": self.task_id, "value": self.value, "unit": self.unit, "rationale": self.rationale,
            "model_lineage": [{"model": m.get("model"), "version": m.get("version")} for m in self.model_lineage],
            "prompt_hash": self.prompt_hash,
        }

    @staticmethod
    def from_json(d: Mapping) -> "ModelAnswer":
        return ModelAnswer(d["task_id"], d.get("value"), d.get("unit", ""), d.get("rationale", ""), [dict(m) for m in d.get("model_lineage") or []], d.get("prompt_hash", ""))


@dataclass(frozen=True)
class Score:
    status: str  # correct | hallucinated | abstained | wrong_unit
    delta: Optional[float]

    def to_json(self) -> dict:
        return {"status": self.status, "delta": self.delta}


@dataclass(frozen=True)
class MitigatedScore:
    """The raw score plus what the substrate would have done: ``recomputed``
    is deterministic code's answer, ``caught`` is true when the model was
    wrong and the recompute was right — the hallucination the substrate
    would have stopped."""

    raw: Score
    recomputed: Optional[float]
    recompute_correct: bool
    caught: bool

    def to_json(self) -> dict:
        return {"raw": self.raw.to_json(), "recomputed": self.recomputed, "recompute_correct": self.recompute_correct, "caught": self.caught}
