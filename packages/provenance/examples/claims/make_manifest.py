"""Regenerate provenance-manifest.json from the files beside it. Run from
this directory: ``python make_manifest.py``. Ids are content hashes, so
editing data.csv or compute_mean.py and re-running changes the manifest;
not re-running makes SubprocessReexecutor report INPUT_HASH_MISMATCH."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))

from provsubstrate.claims import Claim, Computation  # noqa: E402
from provsubstrate.core import sha256_bytes, sha256_text  # noqa: E402


def fhash(name: str) -> str:
    with open(os.path.join(HERE, name), "rb") as f:
        return sha256_bytes(f.read())


def main() -> None:
    paper_hash = sha256_text("Example manuscript: the mean mass of six samples was 3.5 kg.")
    comp = Computation.build(
        command=["python3", "compute_mean.py", "data.csv"],
        entrypoint="compute_mean.py",
        entrypoint_hash=fhash("compute_mean.py"),
        input_hashes={"data.csv": fhash("data.csv")},
        environment={"python": "3.10+", "packages": {}},
        output_selector="/mean",
        expected_output_hash=None,
    )
    claim = Claim.build(
        value=3.5,
        unit="kg",
        tolerance=0.001,
        location={"section": "3.1", "sentence_hash": sha256_text("The mean mass of the six samples was 3.5 kg.")},
        source_doc_hash=paper_hash,
        computation_ref=comp.computation_id,
        model_lineage=[{"model": "local-27b", "version": "example"}],
        confidence=0.95,
    )
    manifest = {
        "format_version": 1,
        "paper": {"doc_hash": paper_hash, "title": "Example manuscript"},
        "computations": [comp.to_json()],
        "claims": [claim.to_json()],
        "edges": [{"claim_id": claim.claim_id, "computation_id": comp.computation_id}],
    }
    with open(os.path.join(HERE, "provenance-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote provenance-manifest.json")


if __name__ == "__main__":
    main()
