"""Generate (or check) the academic v1 conformance suite from the reference
implementation.

Each wedge module exposes ``conformance_cases()`` — a fixed catalogue of
``{kind, id, description, input}`` — and ``compute_expected(kind, input)``.
This script writes one vector per file under ``vectors_academic_v1/<kind>/``
plus a ``manifest.json`` with a per-file SHA-256 and a ``suite_hash`` (SHA-256
over the canonical JSON of the manifest's ``vectors`` array).

``--check`` regenerates in memory and diffs against disk. Drift means either
the reference changed (bump the format version and say why in the commit) or
something is non-deterministic (a bug — fix it).
"""

from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
from typing import Dict, List, Tuple

from ..core.canonical import canonicalize
from ..core.envelope import sha256_text
from .runner import run_conformance, suite_hash_of

FORMAT_VERSION = 1
WEDGES = ["lean", "claims", "repro", "bench", "review"]
HERE = os.path.dirname(__file__)
ACADEMIC_DIR = os.path.join(HERE, "vectors_academic_v1")
FINANCE_DIR = os.path.join(HERE, "vectors_finance_v1")


def _dump(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def collect() -> Tuple[List[Tuple[str, dict]], Dict[str, object]]:
    """Return (files, handlers): files are (relative path, vector body);
    handlers is the union of every wedge's CONFORMANCE_HANDLERS."""
    files: List[Tuple[str, dict]] = []
    handlers: Dict[str, object] = {}
    versions: Dict[str, str] = {}
    for name in WEDGES:
        try:
            mod = importlib.import_module(f"provsubstrate.{name}")
        except ImportError as e:  # a wedge not yet present is skipped loudly
            print(f"[generate] wedge {name} not importable: {e}", file=sys.stderr)
            continue
        cases = getattr(mod, "conformance_cases", None)
        compute = getattr(mod, "compute_expected", None)
        hs = getattr(mod, "CONFORMANCE_HANDLERS", None)
        if not (cases and compute and hs):
            print(f"[generate] wedge {name} lacks conformance surface; skipped", file=sys.stderr)
            continue
        handlers.update(hs)
        versions[name] = getattr(mod, "ENGINE_VERSION", f"{name}@0.1.0")
        for c in cases():
            body = {
                "format_version": FORMAT_VERSION,
                "kind": c["kind"],
                "id": c["id"],
                "description": c["description"],
                "input": c["input"],
                "expected": compute(c["kind"], c["input"]),
            }
            files.append((f"{c['kind']}/{c['id']}.json", body))
    files.sort(key=lambda t: t[0])
    handlers["_versions"] = versions  # type: ignore[assignment]
    return files, handlers


def build_manifest(files: List[Tuple[str, dict]], versions: Dict[str, str]) -> dict:
    vectors = [
        {"path": rel, "kind": body["kind"], "id": body["id"], "sha256": sha256_text(_dump(body))}
        for rel, body in files
    ]
    return {
        "format_version": FORMAT_VERSION,
        "generated_by": "provsubstrate.conformance.generate",
        "reference_versions": {"package": "provenance-substrate@0.1.0", **versions},
        "vectors": vectors,
        "suite_hash": suite_hash_of(vectors),
    }


def write(directory: str = ACADEMIC_DIR) -> dict:
    files, handlers = collect()
    versions = handlers.pop("_versions")  # type: ignore[assignment]
    manifest = build_manifest(files, versions)  # type: ignore[arg-type]
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    for rel, body in files:
        path = os.path.join(directory, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(_dump(body))
    with open(os.path.join(directory, "manifest.json"), "w", encoding="utf-8") as f:
        f.write(_dump(manifest))
    return manifest


def check(directory: str = ACADEMIC_DIR) -> Tuple[bool, List[str]]:
    """Regenerate in memory; compare every file and the manifest to disk.
    Then run the handlers against the on-disk suite as a second guard."""
    files, handlers = collect()
    versions = handlers.pop("_versions")  # type: ignore[assignment]
    manifest = build_manifest(files, versions)  # type: ignore[arg-type]
    problems: List[str] = []
    for rel, body in files:
        path = os.path.join(directory, rel)
        if not os.path.exists(path):
            problems.append(f"missing on disk: {rel}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            if f.read() != _dump(body):
                problems.append(f"drift: {rel}")
    mpath = os.path.join(directory, "manifest.json")
    if not os.path.exists(mpath):
        problems.append("missing manifest.json")
    else:
        with open(mpath, "r", encoding="utf-8") as f:
            on_disk = json.load(f)
        if canonicalize(on_disk) != canonicalize(manifest):
            problems.append(f"manifest drift (disk suite {on_disk.get('suite_hash','?')[:16]} vs generated {manifest['suite_hash'][:16]})")
    if not problems:
        report = run_conformance(directory, handlers)  # type: ignore[arg-type]
        if report.failed:
            problems += [f"handler failed: {r.path}: {r.detail}" for r in report.results if r.status == "fail"]
        if report.skipped:
            problems += [f"kind without handler: {k}" for k in report.kinds_skipped]
    return (not problems), problems


def main(argv: List[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--check" in argv:
        ok, problems = check()
        for p in problems:
            print(p)
        print("academic v1: no drift" if ok else f"academic v1: {len(problems)} problem(s)")
        return 0 if ok else 1
    m = write()
    print(f"academic v1: wrote {len(m['vectors'])} vectors; suite_hash {m['suite_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
