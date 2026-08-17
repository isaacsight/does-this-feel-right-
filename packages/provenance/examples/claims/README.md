# Claims example

`data.csv` (six masses), `compute_mean.py` (prints `{"mean": ..., "n": 6}`),
and `provenance-manifest.json` linking the claim "3.5 kg" in section 3.1 to
that computation. `make_manifest.py` regenerates the manifest with the
current file hashes.

```python
import json, sys
from provsubstrate.claims import SubprocessReexecutor, prepare, badge_json
m = json.load(open("examples/claims/provenance-manifest.json"))
rx = SubprocessReexecutor("examples/claims", executable_map={"python3": sys.executable})
p = prepare(m, rx, data_as_of="2026-08-17T00:00:00.000Z")
print(p.summary)
print(badge_json(p.report()))
```

Edit one number in `data.csv` and run again: the re-executor refuses to run
(`INPUT_HASH_MISMATCH`), because the manifest pinned the bytes.
