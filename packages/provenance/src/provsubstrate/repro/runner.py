"""Runners: the part of the disposer that executes an attempt.

The judge never runs anything; it reads a ``RunRecord``. Two runners
produce those records: ``SubprocessRunner`` really executes the attempt's
commands in a working directory, and ``StubRunner`` replays a table of
canned ``(exit_code, stdout)`` per command so conformance vectors exercise
the same extraction path without a process. Both apply the attempt's
selectors identically through ``extract_values``.
"""

from __future__ import annotations

import re
import subprocess
from typing import Callable, Dict, List, Mapping, Optional, Protocol, Sequence, Tuple

from ..core.envelope import sha256_bytes, sha256_text
from .model import CommandResult, ReproductionAttempt, ReproductionTarget, RunRecord


class Runner(Protocol):
    def run(self, target: ReproductionTarget, attempt: ReproductionAttempt) -> RunRecord: ...


def _parse_number(text: str) -> Optional[float]:
    t = text.strip().replace(",", "")
    if t.endswith("%"):
        t = t[:-1]
    try:
        v = float(t)
    except ValueError:
        return None
    if v != v or v in (float("inf"), float("-inf")):
        return None
    return v


def extract_values(attempt: ReproductionAttempt, stdouts: Sequence[str]) -> Dict[str, Optional[float]]:
    """Apply every selector to the stdout of its command. A selector whose
    command did not run, whose regex does not match, or whose capture is not
    a number yields ``None`` — the judge reports that claim as missing."""
    out: Dict[str, Optional[float]] = {}
    for sel in attempt.selectors:
        value: Optional[float] = None
        if 0 <= sel.command_index < len(stdouts):
            try:
                rx = re.compile(sel.pattern, re.MULTILINE)
            except re.error:
                rx = None
            if rx is not None:
                m = rx.search(stdouts[sel.command_index])
                if m is not None:
                    try:
                        captured = m.group(sel.group)
                    except IndexError:
                        captured = None
                    if captured is not None:
                        value = _parse_number(captured)
        out[sel.claim_id] = value
    return {k: out[k] for k in sorted(out)}


def command_key(cmd: Sequence[str]) -> str:
    return " ".join(cmd)


class StubRunner:
    """Replay canned outputs. ``table`` maps ``command_key(cmd)`` to
    ``(exit_code, stdout_text)``; a command absent from the table behaves like
    a shell that cannot find it (exit 127, empty stdout). ``wall_seconds`` is
    passed in, never measured."""

    def __init__(self, table: Mapping[str, Tuple[int, str]], wall_seconds: float = 0.0, stop_on_error: bool = True):
        self.table = dict(table)
        self.wall_seconds = wall_seconds
        self.stop_on_error = stop_on_error

    def run(self, target: ReproductionTarget, attempt: ReproductionAttempt) -> RunRecord:
        results: List[CommandResult] = []
        stdouts: List[str] = []
        error: Optional[str] = None
        for i, cmd in enumerate(attempt.commands):
            code, out = self.table.get(command_key(cmd), (127, ""))
            results.append(CommandResult(i, code, sha256_text(out), sha256_text("")))
            stdouts.append(out)
            if code != 0:
                error = f"exit_{code}: {command_key(cmd)}"
                if self.stop_on_error:
                    break
        return RunRecord(tuple(results), extract_values(attempt, stdouts), self.wall_seconds, error)


class SubprocessRunner:
    """Execute the attempt's commands in ``workdir``. Stops at the first
    non-zero exit (later commands usually depend on earlier ones). ``clock``
    is optional and explicit: pass ``time.monotonic`` to measure wall time;
    without it ``wall_seconds`` is 0.0. Nothing here reads a clock on its own."""

    def __init__(
        self,
        workdir: str,
        timeout: float = 600.0,
        clock: Optional[Callable[[], float]] = None,
        env: Optional[Mapping[str, str]] = None,
        stop_on_error: bool = True,
    ):
        self.workdir = workdir
        self.timeout = timeout
        self.clock = clock
        self.env = dict(env) if env is not None else None
        self.stop_on_error = stop_on_error

    def run(self, target: ReproductionTarget, attempt: ReproductionAttempt) -> RunRecord:
        start = self.clock() if self.clock else None
        results: List[CommandResult] = []
        stdouts: List[str] = []
        error: Optional[str] = None
        for i, cmd in enumerate(attempt.commands):
            argv = list(cmd)
            try:
                p = subprocess.run(argv, cwd=self.workdir, capture_output=True, timeout=self.timeout, env=self.env, check=False)
                code, out, err = p.returncode, p.stdout, p.stderr
            except subprocess.TimeoutExpired as e:
                code, out, err = 124, e.stdout or b"", e.stderr or b""
                error = f"timeout: {command_key(cmd)}"
            except OSError as e:
                code, out, err = 127, b"", str(e).encode("utf-8")
                error = f"spawn_failed: {command_key(cmd)}"
            results.append(CommandResult(i, code, sha256_bytes(out), sha256_bytes(err)))
            stdouts.append(out.decode("utf-8", "replace"))
            if code != 0:
                error = error or f"exit_{code}: {command_key(cmd)}"
                if self.stop_on_error:
                    break
        wall = (self.clock() - start) if (self.clock and start is not None) else 0.0
        return RunRecord(tuple(results), extract_values(attempt, stdouts), wall, error)
