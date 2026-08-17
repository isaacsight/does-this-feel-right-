# claims — the claim graph

**The model proposes** the numbers in a manuscript. A `provenance-manifest.json`
holds `paper {doc_hash, title}`, `computations` (command, entrypoint and its hash,
`input_hashes` for every file read, a declared `environment`, an
`output_selector`: JSON pointer `/mean`, regex `re:mean=([0-9.]+)`, or `""` for
all of stdout), `claims` (value, unit, tolerance, location, `source_doc_hash`,
`computation_ref`, `model_lineage`, `confidence`) and `edges` linking claims to
computations. Every `claim_id` and `computation_id` is the content hash of its
body, so a manifest that lies about which computation backs a number fails
`validate_manifest` before anything runs.

**Re-execution disposes.** `SubprocessReexecutor` checks the entrypoint and every
input against the pinned hashes first (a changed input is `input_hash_mismatch`,
never a wrong number), runs the command, and pulls one number out of stdout.
`verify_claim` is float arithmetic: `|observed - value| <= tolerance` is
`confirmed`, otherwise `mismatch`; a failed run is `execution_failed`. Rules run
in fixed order: `rule.claims.computation_linked` (DANGLING_COMPUTATION),
`rule.claims.confirmed` (UNCONFIRMED_CLAIM), `rule.claims.tolerance`
(TOLERANCE_EXCEEDED), `rule.claims.environment_pinned` (ENVIRONMENT_UNPINNED),
`rule.claims.confidence_floor` (CONFIDENCE_BELOW_FLOOR, default 0.6).
`StubReexecutor` replays a table keyed by computation id (used by the vectors).

**The corresponding author signs** a multi-line summary listing every claim's
verdict, bound to the `claims.attest` envelope (`claim-graph@0.1.0`, inputs
`{manifest_hash, claims: [{claim_id, computation_id, request_hash, verdict}]}`),
materiality `claims.attest`. Each claim also has its own `claims.verify`
envelope; the badge is computed from the verification report either way.

## Quick start (Python)

```python
import json, sys
from provsubstrate.core import AppendOnlyAuditLog, Approver
from provsubstrate.claims import (AttestationLedger, ClaimsDeps, SubprocessReexecutor, attest_manifest,
                                  badge_json, badge_svg, prepare, validate_manifest)

manifest = json.load(open("examples/claims/provenance-manifest.json"))
assert validate_manifest(manifest).ok
rx = SubprocessReexecutor("examples/claims", executable_map={"python3": sys.executable})

p = prepare(manifest, rx, data_as_of="2026-08-17T00:00:00.000Z")   # re-executes; records nothing
print(p.request_hash); print(p.summary)                               # the author reads exactly this
print(badge_json(p.report()))                                         # {"label": "claims verified", "message": "1/1 ...", ...}

# The human's step (never the agent's).
token = Approver("author.x", b"secret").approve(p.approval_request("session-1"), "2026-08-17T12:00:00.000Z")

log = AppendOnlyAuditLog("audit.jsonl", clock=lambda: "2026-08-17T12:00:01.000Z")
deps = ClaimsDeps(rx, log, AttestationLedger(), {"author.x": b"secret"})
r = attest_manifest(manifest, None, deps, token, session_id="session-1", data_as_of="2026-08-17T00:00:00.000Z")
print(r.ok, r.stage, r.entry_id, r.audit_actions)
open("badge.svg", "w").write(badge_svg(p.report()))
```

## Command line

```bash
provsub claims verify provenance-manifest.json --workdir . [--map python3=/usr/bin/python3] \
        --data-as-of T --session-id S --summary-out summary.txt      # per-claim verdicts, badge, request_hash, summary
provsub claims badge provenance-manifest.json --svg --workdir .       # or --json (shields.io endpoint)
provsub approve --request-hash H --summary-file summary.txt --session-id S --materiality claims.attest \
        --approver-id author.x --secret-file ~/.provsub/secret --approved-at T --out tok.json   # HUMAN
provsub claims attest provenance-manifest.json --workdir . --approval tok.json --trust author.x=~/.provsub/secret \
        --audit audit.jsonl --ledger attestations.json --data-as-of T --session-id S
```

`--results r.json` (a `computation_id -> ExecutionResult` table) replays runs
instead of executing; with neither `--workdir` nor `--results` every claim is
`execution_failed`. `attest` without `--approval` stops at the gate. The summary
is multi-line, so sign it from a file. MCP tools: `claims_verify`, `claims_badge`.

## Conformance kinds (academic v1)

| kind | case ids |
|---|---|
| `claim_manifest_hash` | clean, key_order_irrelevant, empty_manifest, one_byte_changes_hash |
| `claim_manifest_shape` | clean, dangling_edge, duplicate_claim_id, missing_input_hash, edge_contradicts_claim, bad_tolerance, id_mismatch, no_edge_is_ok, not_an_object, wrong_paper_hash |
| `claim_verify` | clean, tolerance_edge_inside, tolerance_edge_float_inside, tolerance_edge_float_over, tolerance_override, mismatch, exec_failed, input_hash_mismatch, no_value_in_output, no_computation |
| `claim_rules` | all_pass, unconfirmed, tolerance_exceeded, dangling, env_unpinned, low_confidence, confidence_at_floor |
| `claim_attest` | clean_valid_approval, mismatch_blocks, exec_failed_blocks, input_hash_mismatch_blocks, dangling_edge_shape, dangling_computation_rule, wrong_hash_approval, unknown_approver, no_approval, missing_result_is_failure |

`claim_verify` pins IEEE-754 deltas (`3.51 - 3.5` is inside `0.01`; `3.6 - 3.5`
is outside `0.1`); a port that rounds first fails those vectors. See
`src/provsubstrate/claims/conformance.py`.

## Audit-action sequence (fixed)

`claim_extraction` -> `reexecution` -> `verifier_check` -> (`approval_granted` |
`approval_denied`) -> `attestation_recorded`. A manifest-shape failure logs
nothing; any failing rule stops after `verifier_check`.

## Approval summary (exact format)

Header, then one line per claim in manifest order, joined by `\n`:

```
Attest {confirmed}/{total} claims confirmed for "{title}" manifest {manifest_hash[:12]}
Claim {claim_id[:12]} = {value} {unit} tol {tolerance} observed {observed|-} delta {delta|-} ({status}) computation {computation_ref[:12]}
```

Numbers are canonical JSON (`3.5`, `0`, `1.8708`). Example (vector
`claim_attest/clean_valid_approval`):

```
Attest 2/2 claims confirmed for "A Small Paper With Two Numbers In It" manifest ad57bbdccafd
Claim 4712b64ae63b = 3.5 kg tol 0.01 observed 3.5 delta 0 (confirmed) computation f3ef341cb0f0
Claim a4c752621a48 = 1.8708 kg tol 0.0001 observed 1.8708 delta 0 (confirmed) computation 20afa256238b
```

Materiality `claims.attest`.
