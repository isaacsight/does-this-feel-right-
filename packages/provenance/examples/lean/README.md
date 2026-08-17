# Lean example

`Basic.lean` is a trivial theorem the core kernel accepts with no Mathlib.
`claim.json` is the model's claim of that proof; `render_lean_file` produces
`Basic.lean` byte-for-byte from it (the leading comment aside — the ledger
hashes the rendered file, not this one).

Run the real kernel, if `lean` is on PATH:

```python
from provsubstrate.lean import LakeDisposer, check_proof, ProofClaim, render_lean_file
import json
claim = ProofClaim.from_json(json.load(open("examples/lean/claim.json")))
if LakeDisposer.available():
    v = check_proof(render_lean_file(claim), LakeDisposer())
    print(v.ok, v.errors, v.sorries, v.axioms)
```

Inside a Mathlib project use `LakeDisposer(project_dir="/path/to/project")`,
which runs `lake env lean` so imports resolve. Without Lean, `StubKernel`
answers from a table keyed by the proof-file hash; the conformance vectors
use it.
