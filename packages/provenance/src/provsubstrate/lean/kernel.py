"""The disposer: the Lean kernel, never a model.

``KernelDisposer.check(source)`` returns a structured ``KernelVerdict``.
Two implementations ship: ``LakeDisposer`` runs the real ``lean`` (through
``lake env`` when a project directory is given) and parses its diagnostics;
``StubKernel`` answers from a table keyed by the proof-file hash so tests and
conformance vectors need no Lean at all. Whatever the kernel says, a static
scan of the source also counts ``sorry``/``admit`` and spots ``native_decide``
and ``axiom`` declarations — a kernel that accepted a file with a ``sorry`` in
it still leaves the ``sorry`` on the record.

Running the real kernel against ``examples/lean/Basic.lean``::

    from provsubstrate.lean import LakeDisposer, check_proof
    k = LakeDisposer()                       # plain `lean`, no lake project
    # or LakeDisposer(project_dir="/path/to/mathlib-project") for `lake env lean`
    if LakeDisposer.available():
        v = check_proof(open("examples/lean/Basic.lean").read(), k)
        print(v.ok, v.errors, v.sorries, v.axioms)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from typing import Any, List, Mapping, Optional, Protocol

from ..core.envelope import sha256_text

# Axiom that `native_decide` introduces; Lean reports it under this name.
NATIVE_DECIDE_AXIOM = "Lean.ofReduceBool"
# Axiom that any `sorry` elaborates to.
SORRY_AXIOM = "sorryAx"


@dataclass(frozen=True)
class KernelVerdict:
    ok: bool
    errors: List[str] = field(default_factory=list)
    sorries: int = 0
    axioms: List[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return {"ok": self.ok, "errors": list(self.errors), "sorries": self.sorries, "axioms": list(self.axioms)}

    @staticmethod
    def from_json(d: Mapping[str, Any]) -> "KernelVerdict":
        return KernelVerdict(bool(d["ok"]), list(d.get("errors", [])), int(d.get("sorries", 0)), list(d.get("axioms", [])))


class KernelDisposer(Protocol):
    def check(self, source: str) -> KernelVerdict: ...


# --- static scan -----------------------------------------------------------

_BLOCK_COMMENT_RE = re.compile(r"/-.*?-/", re.DOTALL)
_LINE_COMMENT_RE = re.compile(r"--[^\n]*")
_STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
_SORRY_RE = re.compile(r"\b(sorry|admit)\b")
_NATIVE_DECIDE_RE = re.compile(r"\bnative_decide\b")
_AXIOM_DECL_RE = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*axiom\s+([^\s:(]+)", re.MULTILINE)


def strip_comments(source: str) -> str:
    """Comments and string literals cannot hide a ``sorry``, nor fake one."""
    s = _BLOCK_COMMENT_RE.sub(" ", source)
    s = _LINE_COMMENT_RE.sub(" ", s)
    s = _STRING_RE.sub('""', s)
    return s


@dataclass(frozen=True)
class StaticScan:
    sorries: int
    axioms: List[str]

    def to_json(self) -> dict:
        return {"sorries": self.sorries, "axioms": list(self.axioms)}


def static_scan(source: str) -> StaticScan:
    """Count ``sorry``/``admit`` and collect axioms the source itself
    introduces (``axiom`` declarations, ``native_decide``). Pure."""
    s = strip_comments(source)
    sorries = len(_SORRY_RE.findall(s))
    axioms = set(_AXIOM_DECL_RE.findall(s))
    if _NATIVE_DECIDE_RE.search(s):
        axioms.add(NATIVE_DECIDE_AXIOM)
    if sorries:
        axioms.add(SORRY_AXIOM)
    return StaticScan(sorries, sorted(axioms))


def merge_verdict(kernel: KernelVerdict, scan: StaticScan) -> KernelVerdict:
    """The static scan can only add: sorries are the max of both counts,
    axioms the sorted union. The kernel's ok/errors are its own."""
    return KernelVerdict(
        ok=kernel.ok,
        errors=list(kernel.errors),
        sorries=max(kernel.sorries, scan.sorries),
        axioms=sorted(set(kernel.axioms) | set(scan.axioms)),
    )


def check_proof(source: str, kernel: KernelDisposer) -> KernelVerdict:
    """Kernel verdict merged with the static scan — the disposer proper."""
    return merge_verdict(kernel.check(source), static_scan(source))


# --- stub kernel -----------------------------------------------------------


class StubKernel:
    """Deterministic table ``proof_file_hash -> KernelVerdict``. A hash not
    in the table is rejected loudly, so a rendering drift never passes as
    a checked proof."""

    def __init__(self, table: Mapping[str, KernelVerdict | Mapping[str, Any]]):
        self._table = {h: (v if isinstance(v, KernelVerdict) else KernelVerdict.from_json(v)) for h, v in table.items()}

    def check(self, source: str) -> KernelVerdict:
        h = sha256_text(source)
        v = self._table.get(h)
        if v is None:
            return KernelVerdict(False, [f"stub kernel: no verdict for proof file {h[:12]}"], 0, [])
        return v


# --- real kernel -----------------------------------------------------------

_DIAG_RE = re.compile(r"^(?P<file>[^:\n]+):(?P<line>\d+):(?P<col>\d+): (?P<sev>error|warning|info): (?P<msg>.*)$")
_AXIOMS_LINE_RE = re.compile(r"'(?P<name>[^']+)' depends on axioms: \[(?P<list>[^\]]*)\]")
_NO_AXIOMS_LINE_RE = re.compile(r"'(?P<name>[^']+)' does not depend on any axioms")
_DECL_NAME_RE = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma)\s+([^\s:(]+)", re.MULTILINE)


class KernelUnavailable(RuntimeError):
    pass


class LakeDisposer:
    """Runs ``lake env lean <file>`` inside ``project_dir`` (or plain ``lean``
    when no project is given). The bytes checked are exactly ``source``; a
    ``#print axioms`` trailer is appended for each theorem so the axioms
    the kernel reports can be parsed, and the trailer is excluded from what
    the ledger hashes (see ``render_lean_file``). Times out; reports a
    structured verdict rather than raising, except when Lean is absent."""

    def __init__(self, project_dir: Optional[str] = None, timeout: float = 120.0, print_axioms: bool = True):
        self.project_dir = project_dir
        self.timeout = timeout
        self.print_axioms = print_axioms

    @staticmethod
    def available(project_dir: Optional[str] = None) -> bool:
        return shutil.which("lake" if project_dir else "lean") is not None

    def _command(self, path: str) -> List[str]:
        if self.project_dir:
            return ["lake", "env", "lean", path]
        return ["lean", path]

    def check(self, source: str) -> KernelVerdict:
        if not self.available(self.project_dir):
            raise KernelUnavailable("lean is not on PATH" if not self.project_dir else "lake is not on PATH")
        text = source
        if self.print_axioms:
            names = _DECL_NAME_RE.findall(strip_comments(source))
            if names:
                text = source.rstrip("\n") + "\n\n" + "\n".join(f"#print axioms {n}" for n in names) + "\n"
        with tempfile.TemporaryDirectory(prefix="provsub-lean-") as td:
            path = os.path.join(td, "ProvCheck.lean")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            try:
                proc = subprocess.run(
                    self._command(path),
                    cwd=self.project_dir or td,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired:
                return KernelVerdict(False, [f"timeout after {self.timeout:g}s"], 0, [])
        return parse_lean_output(proc.stdout + "\n" + proc.stderr, proc.returncode)


def parse_lean_output(output: str, returncode: int) -> KernelVerdict:
    """Parse ``lean`` diagnostics into a verdict. ``error:`` lines fail the
    check; ``declaration uses 'sorry'`` warnings count sorries; ``#print
    axioms`` output lists axioms. Pure, so it is unit-testable without Lean."""
    errors: List[str] = []
    sorries = 0
    axioms: set = set()
    for raw in output.splitlines():
        line = raw.rstrip()
        m = _DIAG_RE.match(line)
        if m:
            sev, msg = m.group("sev"), m.group("msg")
            if sev == "error":
                errors.append(f"{m.group('line')}:{m.group('col')}: {msg}")
            elif sev == "warning" and "declaration uses 'sorry'" in msg:
                sorries += 1
            continue
        a = _AXIOMS_LINE_RE.search(line)
        if a:
            for name in a.group("list").split(","):
                name = name.strip()
                if name:
                    axioms.add(name)
    ok = returncode == 0 and not errors
    return KernelVerdict(ok, errors, sorries, sorted(axioms))
