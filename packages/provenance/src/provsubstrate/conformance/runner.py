"""Conformance runner.

Point it at a vectors directory (``manifest.json`` + ``<kind>/<id>.json``)
and a mapping of kind → handler. Each handler receives the vector's
``input`` and ``expected`` and returns ``(pass, detail)``. Hashes and
canonical strings compare exactly; structured results compare JSON-equal
after canonicalization. The report carries the manifest's ``suite_hash`` —
the one number to quote when claiming conformance — and whether every file
on disk still matches its manifest entry.

Kinds present in the suite but absent from ``handlers`` are reported as
``skipped``: a port may claim a subset, and must say which.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Mapping, Optional, Tuple

from ..core.canonical import canonicalize
from ..core.envelope import sha256_text

Handler = Callable[[dict, dict], Tuple[bool, Optional[str]]]


def json_equal(a, b) -> bool:
    return canonicalize(a) == canonicalize(b)


def expect_equal(got, want) -> Tuple[bool, Optional[str]]:
    return (True, None) if json_equal(got, want) else (False, json.dumps(got, ensure_ascii=False, sort_keys=True))


@dataclass
class VectorResult:
    path: str
    kind: str
    id: str
    status: str  # "pass" | "fail" | "skip"
    detail: Optional[str] = None


@dataclass
class ConformanceReport:
    suite_hash: str
    format_version: int
    manifest_ok: bool
    total: int
    passed: int
    failed: int
    skipped: int
    kinds_claimed: List[str]
    kinds_skipped: List[str]
    results: List[VectorResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.manifest_ok

    def to_json(self) -> dict:
        d = asdict(self)
        d["ok"] = self.ok
        return d

    def summary(self) -> str:
        line = f"{self.passed}/{self.total - self.skipped} passed"
        if self.skipped:
            line += f", {self.skipped} skipped ({', '.join(self.kinds_skipped)})"
        line += f"; suite {self.suite_hash[:16]}… manifest {'ok' if self.manifest_ok else 'MISMATCH'}"
        return line


def load_vectors(directory: str) -> Tuple[dict, List[Tuple[str, str, dict]]]:
    with open(os.path.join(directory, "manifest.json"), "r", encoding="utf-8") as f:
        manifest = json.load(f)
    out: List[Tuple[str, str, dict]] = []
    for kind in sorted(os.listdir(directory)):
        kdir = os.path.join(directory, kind)
        if not os.path.isdir(kdir):
            continue
        for fn in sorted(os.listdir(kdir)):
            if not fn.endswith(".json"):
                continue
            rel = f"{kind}/{fn}"
            with open(os.path.join(kdir, fn), "r", encoding="utf-8") as f:
                body = f.read()
            out.append((rel, body, json.loads(body)))
    out.sort(key=lambda t: t[0])
    return manifest, out


def run_conformance(directory: str, handlers: Mapping[str, Handler]) -> ConformanceReport:
    manifest, vectors = load_vectors(directory)
    entries = {m["path"]: m["sha256"] for m in manifest["vectors"]}
    manifest_ok = len(manifest["vectors"]) == len(vectors)
    results: List[VectorResult] = []
    kinds_seen: Dict[str, bool] = {}
    for rel, body, v in vectors:
        if entries.get(rel) != sha256_text(body):
            manifest_ok = False
        kind = v["kind"]
        h = handlers.get(kind)
        if h is None:
            kinds_seen.setdefault(kind, False)
            results.append(VectorResult(rel, kind, v["id"], "skip"))
            continue
        kinds_seen[kind] = True
        try:
            ok, detail = h(v["input"], v["expected"])
        except Exception as e:  # noqa: BLE001 — a throw is a failed vector, reported as such
            ok, detail = False, f"threw: {type(e).__name__}: {e}"
        results.append(VectorResult(rel, kind, v["id"], "pass" if ok else "fail", None if ok else detail))
    passed = sum(1 for r in results if r.status == "pass")
    failed = sum(1 for r in results if r.status == "fail")
    skipped = sum(1 for r in results if r.status == "skip")
    return ConformanceReport(
        suite_hash=manifest["suite_hash"],
        format_version=manifest.get("format_version", 0),
        manifest_ok=manifest_ok,
        total=len(results),
        passed=passed,
        failed=failed,
        skipped=skipped,
        kinds_claimed=sorted(k for k, c in kinds_seen.items() if c),
        kinds_skipped=sorted(k for k, c in kinds_seen.items() if not c),
        results=results,
    )


def suite_hash_of(vectors_meta: List[dict]) -> str:
    """The manifest's ``suite_hash`` is SHA-256 over the canonical JSON of the
    ``vectors`` array (path, kind, id, sha256 per file)."""
    return sha256_text(canonicalize(vectors_meta))
