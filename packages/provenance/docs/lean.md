# lean — the proof ledger

**The model proposes** a proof: a `ProofClaim` with `theorem_name`, `statement`,
`proof`, `imports`, `model_lineage`, `prompt_hash`, `toolchain`, `mathlib_rev`,
`confidence`, and `doc_hash` (the sha256 of the statement it was asked to prove).

**The Lean kernel disposes.** `render_lean_file` turns the claim into one
deterministic `.lean` file (imports, blank line, `theorem name : statement := ...`,
two-space indent, LF, trailing newline); its sha256 is the `proof_file_hash`.
`check_proof` runs a `KernelDisposer` on those exact bytes and merges the verdict
with a static scan for `sorry`/`admit`, `native_decide` and `axiom` declarations.
`LakeDisposer` runs `lean` (or `lake env lean` inside a project); `StubKernel`
answers from a table keyed by proof-file hash, so a rendering drift is a loud
"no verdict", never a pass. Rules-as-code then run, all of them, in fixed order:
`rule.lean.kernel` (KERNEL_REJECTED), `rule.lean.no_sorry` (CONTAINS_SORRY),
`rule.lean.axiom_allowlist` (FORBIDDEN_AXIOM; default allowlist `propext`,
`Classical.choice`, `Quot.sound`), `rule.lean.confidence_floor`
(CONFIDENCE_BELOW_FLOOR, default 0.6), `rule.lean.statement_hash`
(STATEMENT_HASH_MISMATCH), `rule.lean.toolchain_pinned` (TOOLCHAIN_UNPINNED).

**A mathematician signs** the exact summary line, bound to the request hash of the
`lean.check` envelope (`lean-proof-ledger@0.1.0`, inputs `{claim, toolchain,
mathlib_rev}`, `data_as_of`), materiality `lean.record`. Only then does
`record_proof` append an entry to the `ProofLedger`; `entry_id` is the content
hash of the entry body.

## Quick start (Python)

```python
import json
from provsubstrate.core import AppendOnlyAuditLog, Approver
from provsubstrate.lean import LeanDeps, ProofClaim, ProofLedger, StubKernel, prepare, record_proof, validate_claim_shape

claim_json = json.load(open("examples/lean/claim.json"))
claim = validate_claim_shape(claim_json).claim
# The disposer. Use LakeDisposer() when `lean` is on PATH; the stub needs a verdict per proof-file hash.
from provsubstrate.lean import proof_file_hash
kernel = StubKernel({proof_file_hash(claim): {"ok": True, "errors": [], "sorries": 0, "axioms": []}})

p = prepare(claim, kernel, data_as_of="2026-08-17T00:00:00.000Z")   # kernel + rules + envelope, records nothing
print(p.request_hash, p.summary)                                       # what the human sees

# The human's step (never the agent's): sign the exact line, bound to the hash.
areq = p.approval_request("session-1")
token = Approver("pi.ada", b"academic-approver-secret-0001").approve(areq, "2026-08-17T12:00:00.000Z")

log = AppendOnlyAuditLog("audit.jsonl", clock=lambda: "2026-08-17T12:00:01.000Z")
deps = LeanDeps(kernel, log, ProofLedger(), {"pi.ada": b"academic-approver-secret-0001"})
r = record_proof(claim, deps, token, session_id="session-1", data_as_of="2026-08-17T00:00:00.000Z")
print(r.ok, r.stage, r.entry_id, r.audit_actions)
```

## Command line

```bash
provsub lean render claim.json --raw                       # the exact bytes the kernel checks
provsub lean check Basic.lean --toolchain leanprover/lean4:v4.12.0        # kernel verdict + static scan
provsub lean check claim.json [--project-dir mathlib-proj] [--stub --kernel-table t.json]
provsub lean prepare claim.json --data-as-of T --session-id S           # request_hash + summary to sign
provsub approve --request-hash H --summary "..." --session-id S --materiality lean.record \
                --approver-id pi.ada --secret-file ~/.provsub/secret --approved-at T --out tok.json   # HUMAN
provsub lean record claim.json --approval tok.json --trust pi.ada=~/.provsub/secret \
                --audit audit.jsonl --ledger ledger.json --data-as-of T --session-id S
```

`check` and `prepare` on a claim are the same computation; `record` without
`--approval` stops at the gate. `--stub` needs no Lean installed; without a
`--kernel-table` the stub rejects everything. MCP tools: `lean_check`,
`lean_prepare` (verdicts only; nothing records or mints through MCP).

## Conformance kinds (academic v1)

| kind | case ids |
|---|---|
| `lean_claim_shape` | clean, not_an_object, missing_fields, bad_hashes_and_confidence, bad_theorem_name, unpinned_is_shape_ok |
| `lean_proof_file_hash` | tactic_block, term_mode, one_line_tactic, no_imports, multiline_term, sorry |
| `lean_rules` | all_pass, kernel_rejected, contains_sorry, forbidden_axiom_native_decide, forbidden_axiom_from_kernel, allowlist_widened, unpinned_toolchain, hash_mismatch, low_confidence, confidence_at_floor |
| `lean_approval_summary` | clean, no_axioms_no_mathlib, rejected_with_sorry, unpinned |
| `lean_record` | clean_valid_approval, proof_with_sorry, kernel_rejected, forbidden_axiom, unpinned_toolchain, hash_mismatch, wrong_hash_approval, unknown_approver, no_approval, bad_shape |

Every case runs against `StubKernel`; see `src/provsubstrate/lean/conformance.py`.

## Audit-action sequence (fixed)

`proof_claim` -> `kernel_verdict` -> `verifier_check` -> (`approval_granted` |
`approval_denied`) -> `proof_recorded`. A shape failure logs nothing; a kernel or
rule failure stops after `verifier_check`; a missing or invalid token stops at
`approval_denied` and records nothing.

## Approval summary (exact format)

```
Record proof of {theorem_name} ({nbytes} bytes, {kernel ok|kernel REJECTED}, {sorries} sorries, axioms: {a,b|none}) toolchain {toolchain|(unpinned)} mathlib {mathlib_rev[:12]|(none)} file {proof_file_hash[:12]}
```

Example (vector `lean_approval_summary/clean`):
`Record proof of Nat.add_zero' (92 bytes, kernel ok, 0 sorries, axioms: propext) toolchain leanprover/lean4:v4.12.0 mathlib 3f2b9c1d8e7a file 34d77a06ae18`.
Materiality `lean.record`. The token also binds `session_id` and `request_hash`.
