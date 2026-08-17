"""Responders: anything that turns a ``Task`` into a ``ModelAnswer``.

Three reference responders bracket the space — always right, sometimes
picks a distractor, always abstains — and ``CallableResponder`` adapts any
external function so a real model can be measured without this package
depending on a provider. ``DistractorResponder`` decides per task from a
hash of ``(seed, task_id)``, so its behaviour is order-independent and
replayable.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Protocol, Sequence, Union

from ..core.envelope import sha256_text
from .model import ModelAnswer, Task

REFERENCE_LINEAGE = [{"model": "reference-responder", "version": "0.1.0"}]
REFERENCE_PROMPT_HASH = sha256_text("prompt:bench:reference")


class Responder(Protocol):
    model_lineage: List[dict]
    prompt_hash: str

    def answer(self, task: Task) -> ModelAnswer: ...


class OracleResponder:
    """Always returns the ground truth. The ceiling."""

    def __init__(self, model_lineage: Optional[Sequence[dict]] = None, prompt_hash: str = REFERENCE_PROMPT_HASH):
        self.model_lineage = [dict(m) for m in (model_lineage or [{"model": "oracle", "version": "0.1.0"}])]
        self.prompt_hash = prompt_hash

    def answer(self, task: Task) -> ModelAnswer:
        return ModelAnswer(task.task_id, task.ground_truth.value, task.ground_truth.unit, "ground truth", self.model_lineage, self.prompt_hash)


class NullResponder:
    """Always abstains. The floor for hallucination, the ceiling for abstention."""

    def __init__(self, model_lineage: Optional[Sequence[dict]] = None, prompt_hash: str = REFERENCE_PROMPT_HASH):
        self.model_lineage = [dict(m) for m in (model_lineage or [{"model": "null", "version": "0.1.0"}])]
        self.prompt_hash = prompt_hash

    def answer(self, task: Task) -> ModelAnswer:
        return ModelAnswer(task.task_id, None, task.ground_truth.unit, "abstain", self.model_lineage, self.prompt_hash)


class DistractorResponder:
    """With probability ``rate`` (per task, decided by hash of seed and
    task_id) answers with one of the task's distractors; otherwise answers
    correctly. A task with no distractors is answered correctly."""

    def __init__(self, seed: int, rate: float = 0.5, model_lineage: Optional[Sequence[dict]] = None, prompt_hash: str = REFERENCE_PROMPT_HASH):
        self.seed = int(seed)
        self.rate = float(rate)
        self.model_lineage = [dict(m) for m in (model_lineage or [{"model": "distractor", "version": f"seed-{int(seed)}"}])]
        self.prompt_hash = prompt_hash

    def _draw(self, task: Task) -> int:
        return int(sha256_text(f"{self.seed}:{task.task_id}")[:16], 16)

    def answer(self, task: Task) -> ModelAnswer:
        d = self._draw(task)
        gt = task.ground_truth
        if task.distractors and (d % 10000) / 10000.0 < self.rate:
            pick = task.distractors[(d >> 20) % len(task.distractors)]
            return ModelAnswer(task.task_id, pick, gt.unit, "picked a number from the text", self.model_lineage, self.prompt_hash)
        return ModelAnswer(task.task_id, gt.value, gt.unit, "ground truth", self.model_lineage, self.prompt_hash)


AnswerLike = Union[ModelAnswer, float, int, None, tuple]


class CallableResponder:
    """Adapt ``fn(task)`` from outside. ``fn`` may return a ``ModelAnswer``,
    a bare number (or ``None`` to abstain), or ``(value, unit, rationale)``;
    bare returns are wrapped with this responder's lineage and prompt hash."""

    def __init__(self, fn: Callable[[Task], AnswerLike], model_lineage: Sequence[dict], prompt_hash: str):
        self.fn = fn
        self.model_lineage = [dict(m) for m in model_lineage]
        self.prompt_hash = prompt_hash

    def answer(self, task: Task) -> ModelAnswer:
        r = self.fn(task)
        if isinstance(r, ModelAnswer):
            return r
        if isinstance(r, tuple):
            value = r[0] if len(r) > 0 else None
            unit = r[1] if len(r) > 1 else task.ground_truth.unit
            rationale = r[2] if len(r) > 2 else ""
            return ModelAnswer(task.task_id, None if value is None else float(value), str(unit), str(rationale), self.model_lineage, self.prompt_hash)
        if r is None:
            return ModelAnswer(task.task_id, None, task.ground_truth.unit, "", self.model_lineage, self.prompt_hash)
        return ModelAnswer(task.task_id, float(r), task.ground_truth.unit, "", self.model_lineage, self.prompt_hash)
