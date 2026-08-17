"""The disposer: re-execution, never a model.

``Reexecutor.run(computation)`` returns a structured ``ExecutionResult``.
``SubprocessReexecutor`` verifies the entrypoint and every input file
against the pinned hashes *before* running anything — a changed input is
``INPUT_HASH_MISMATCH``, not a mysterious wrong number — then runs the
command and pulls the value out of stdout with the computation's
``output_selector``. ``StubReexecutor`` answers from a table keyed by
computation id so vectors need no subprocess.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional, Protocol

from ..core.envelope import sha256_bytes
from .model import Computation

INPUT_HASH_MISMATCH = "INPUT_HASH_MISMATCH"


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    stdout: str
    stderr: str
    exit_code: int
    output_value: Optional[float]
    output_hash: str
    input_mismatches: List[str] = field(default_factory=list)  # names whose bytes did not match

    def to_json(self) -> dict:
        return {
            "ok": self.ok,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "output_value": self.output_value,
            "output_hash": self.output_hash,
            "input_mismatches": list(self.input_mismatches),
        }

    @staticmethod
    def from_json(d: Mapping[str, Any]) -> "ExecutionResult":
        return ExecutionResult(
            bool(d["ok"]),
            d.get("stdout", ""),
            d.get("stderr", ""),
            int(d.get("exit_code", 0)),
            d.get("output_value"),
            d.get("output_hash", sha256_bytes(d.get("stdout", "").encode("utf-8"))),
            list(d.get("input_mismatches", [])),
        )


class Reexecutor(Protocol):
    def run(self, computation: Computation) -> ExecutionResult: ...


# --- value extraction ------------------------------------------------------

_NUMBER_RE = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def _json_pointer(doc: Any, pointer: str) -> Any:
    if pointer == "":
        return doc
    if not pointer.startswith("/"):
        raise KeyError(pointer)
    cur = doc
    for raw in pointer[1:].split("/"):
        tok = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(tok)]
        elif isinstance(cur, Mapping):
            cur = cur[tok]
        else:
            raise KeyError(pointer)
    return cur


def extract_value(stdout: str, selector: str) -> Optional[float]:
    """Pull one number out of stdout. ``/ptr`` = JSON pointer into parsed
    stdout; ``re:<pattern>`` = first group (or whole match) of a regex;
    ``""`` = the whole of stdout, stripped. None when nothing numeric is
    there. Never raises: an unreadable output is an execution failure."""
    try:
        if selector.startswith("/"):
            v = _json_pointer(json.loads(stdout), selector)
        elif selector.startswith("re:"):
            m = re.search(selector[3:], stdout, re.MULTILINE)
            if not m:
                return None
            v = m.group(1) if m.groups() else m.group(0)
        else:
            v = stdout.strip()
        if isinstance(v, bool):
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            s = v.strip()
            m = _NUMBER_RE.fullmatch(s)
            return float(s) if m else None
        return None
    except (ValueError, KeyError, IndexError, TypeError, re.error):
        return None


# --- implementations -------------------------------------------------------


class StubReexecutor:
    """Deterministic table ``computation_id -> ExecutionResult``. Missing
    id = a failed execution, reported as such."""

    def __init__(self, table: Mapping[str, ExecutionResult | Mapping[str, Any]]):
        self._table = {k: (v if isinstance(v, ExecutionResult) else ExecutionResult.from_json(v)) for k, v in table.items()}

    def run(self, computation: Computation) -> ExecutionResult:
        r = self._table.get(computation.computation_id)
        if r is None:
            return ExecutionResult(False, "", f"stub reexecutor: no result for {computation.computation_id[:12]}", -1, None, sha256_bytes(b""))
        return r


class SubprocessReexecutor:
    """Runs ``computation.command`` in ``workdir``. Hash checks first;
    ``executable_map`` lets a caller resolve the recorded interpreter name
    (``python3``) to a concrete binary without changing what the manifest
    says was run."""

    def __init__(self, workdir: str, timeout: float = 300.0, executable_map: Optional[Mapping[str, str]] = None, env: Optional[Mapping[str, str]] = None):
        self.workdir = workdir
        self.timeout = timeout
        self.executable_map = dict(executable_map or {})
        self.env = dict(env) if env is not None else None

    def _file_hash(self, rel: str) -> Optional[str]:
        path = os.path.join(self.workdir, rel)
        if not os.path.isfile(path):
            return None
        with open(path, "rb") as f:
            return sha256_bytes(f.read())

    def check_inputs(self, computation: Computation) -> List[str]:
        """Names (entrypoint first, then inputs sorted) whose on-disk bytes
        do not hash to the pinned value. Empty means run."""
        bad: List[str] = []
        if self._file_hash(computation.entrypoint) != computation.entrypoint_hash:
            bad.append(computation.entrypoint)
        for name, h in sorted(computation.input_hashes.items()):
            if self._file_hash(name) != h:
                bad.append(name)
        return bad

    def run(self, computation: Computation) -> ExecutionResult:
        mismatches = self.check_inputs(computation)
        if mismatches:
            return ExecutionResult(False, "", f"{INPUT_HASH_MISMATCH}: {', '.join(mismatches)}", -1, None, sha256_bytes(b""), mismatches)
        cmd = list(computation.command)
        if cmd and cmd[0] in self.executable_map:
            cmd[0] = self.executable_map[cmd[0]]
        try:
            proc = subprocess.run(cmd, cwd=self.workdir, capture_output=True, text=True, timeout=self.timeout, env=self.env)
        except subprocess.TimeoutExpired:
            return ExecutionResult(False, "", f"timeout after {self.timeout:g}s", -1, None, sha256_bytes(b""))
        except (OSError, ValueError) as e:  # command not found and friends
            return ExecutionResult(False, "", f"spawn failed: {e}", -1, None, sha256_bytes(b""))
        out_hash = sha256_bytes(proc.stdout.encode("utf-8"))
        value = extract_value(proc.stdout, computation.output_selector) if proc.returncode == 0 else None
        return ExecutionResult(proc.returncode == 0, proc.stdout, proc.stderr, proc.returncode, value, out_hash)
