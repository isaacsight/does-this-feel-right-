# repro — the reproducibility ledger

**The model proposes** how to reproduce a paper. A `ReproductionTarget` is what
the paper says: `paper {title, doc_hash, doi?, arxiv_id?}`, `repo {url, commit}`,
`claims [{claim_id, description, value, unit, tolerance}]`, `environment_spec`,
`commands`. A `ReproductionAttempt` is the model's proposal: `commands` to run and
`selectors` (`{claim_id, command_index, pattern, group}`: a regex with a capture
group over one command's stdout), plus `model_lineage`, `prompt_hash`,
`confidence`, and the `target_hash` / `doc_hash` it binds to.

**The judge disposes.** A `Runner` executes the attempt (`SubprocessRunner` in a
working directory, stopping at the first non-zero exit; `StubRunner` replays a
table of `(exit_code, stdout)`) and returns a `RunRecord`: per-command exit codes
and stdout/stderr hashes plus the values the selectors extracted. `judge`
compares extracted values to the paper's claims in decimal over the shortest
float repr (`0.86 - 0.85` is exactly `0.01`), claim by claim: `confirmed`,
`mismatch`, `missing`; overall `reproduced`, `partially_reproduced`,
`not_reproduced` (never vacuously reproduced with zero claims), or
`could_not_run`. Rules, all of them, in fixed order: `rule.repro.commit_pinned`
(NO_COMMIT_PINNED, full 40/64-hex only), `rule.repro.environment_pinned`
(ENVIRONMENT_UNPINNED), `rule.repro.claims_present` (ZERO_CLAIMS),
`rule.repro.run_succeeded` (RUN_FAILED), `rule.repro.claims_agree`
(CLAIM_MISMATCH), `rule.repro.confidence_floor` (CONFIDENCE_BELOW_FLOOR, 0.6).

**The reproducer signs** the summary line, bound to the `repro.judge` envelope
(`repro-ledger@0.1.0`, inputs `{target, attempt, run_record}`), materiality
`repro.report`. The signed report (`report_id` = content hash of envelope +
verdict + token) is a dataset row: `export_jsonl` writes canonical JSON lines
sorted by `report_id`; `dataset_manifest`, `zenodo_metadata` and
`croissant_metadata` cite the same hashes. Partial or negative verdicts stop at
the verifier and stay on the audit chain as attempts; they are never signed.

## Quick start (Python)

```python
from provsubstrate.core import AppendOnlyAuditLog, Approver, ApprovalRequest
from provsubstrate.repro import (REPRO_MATERIALITY, ClaimSpec, OutputSelector, PaperRef, RepoRef, ReproductionAttempt,
                                 ReproductionTarget, StubRunner, dataset_manifest, export_jsonl, record_reproduction)

target = ReproductionTarget(
    PaperRef("A Small Replication Study", "e3b0c442" + "0" * 56), RepoRef("https://github.com/x/y", "3f2a9c1e5b7d4a6f8c0e2b4d6f8a0c2e4b6d8f0a"),
    (ClaimSpec("accuracy", "Table 2", 0.85, "fraction", 0.01),), {"python": "3.11.4"}, (("python3", "evaluate.py"),))
attempt = ReproductionAttempt(target.target_hash(), target.paper.doc_hash, target.commands,
                              (OutputSelector("accuracy", 0, r"accuracy=([0-9.]+)"),),
                              [{"model": "local-27b", "version": "x"}], "a" * 64, confidence=0.9)
runner = StubRunner({"python3 evaluate.py": (0, "accuracy=0.86\n")})   # SubprocessRunner("./repo") to really run it
log = AppendOnlyAuditLog(None, clock=lambda: "2026-08-17T00:00:00.000Z")
common = dict(target=target, attempt=attempt, runner=runner, audit_log=log, session_id="s1",
              trusted={"pi.ada": b"secret"}, data_as_of="2026-08-17T00:00:00.000Z")
dry = record_reproduction(**common)                                   # stops at the gate: request_hash + summary
token = Approver("pi.ada", b"secret").approve(ApprovalRequest(dry["request_hash"], dry["summary"], "s1", REPRO_MATERIALITY),
                                              "2026-08-17T12:00:00.000Z")   # the human's step
r = record_reproduction(**common, approval=token)
print(r["ok"], r["overall"], r["report_id"], r["audit_actions"])
open("reports.jsonl", "w").write(export_jsonl([r["report"]])); print(dataset_manifest([r["report"]], "1.0.0")["dataset_hash"])
```

## Command line

```bash
provsub repro judge target.json attempt.json --workdir ./repo --data-as-of T --session-id S    # or --stub s.json | --run-record rr.json
provsub approve --request-hash H --summary "..." --session-id S --materiality repro.report \
        --approver-id pi.ada --secret-file ~/.provsub/secret --approved-at T --out tok.json      # HUMAN
provsub repro record target.json attempt.json --workdir ./repo --approval tok.json --trust pi.ada=~/.provsub/secret \
        --audit audit.jsonl --report-out report.json --data-as-of T --session-id S
provsub repro export reports/*.json --version 1.0.0 --jsonl out.jsonl --manifest m.json \
        --zenodo z.json --creator "Ada Lovelace|Kernel" --croissant c.json
```

`record` without `--approval` stops at the gate. `--stub` replays
`{"table": {"python3 run.py": {"exit_code": 0, "stdout": "..."}}}`. MCP tools:
`repro_judge`, `repro_dataset_manifest`.

## Conformance kinds (academic v1)

| kind | case ids |
|---|---|
| `repro_target_hash` | pinned, unpinned_commit, keys_shuffled |
| `repro_judge` | full, partial, mismatch, missing_claim, could_not_run, no_selectors, zero_claims, tolerance_edge_decimal |
| `repro_rules` | all_pass, unpinned_commit, short_commit, unpinned_environment, zero_claims, run_failed, claim_mismatch, confidence_below_floor, confidence_at_floor_passes, multiple_failures |
| `repro_approval_summary` | reproduced, partial, unpinned, long_title_truncated |
| `repro_record` | records_with_valid_approval, stops_at_gate_without_approval, rejects_wrong_hash_approval, rejects_unknown_approver, partial_never_reaches_gate, mismatch_never_reaches_gate, could_not_run_never_reaches_gate, unpinned_commit_never_reaches_gate, low_confidence_refused, malformed_attempt_logs_nothing |
| `repro_dataset_manifest` | two_reports, two_reports_reversed, empty |

All cases run through `StubRunner`; see `src/provsubstrate/repro/conformance.py`.

## Audit-action sequence (fixed)

`repro_attempt` -> `run_record` -> `verifier_check` -> (`approval_granted` |
`approval_denied`) -> `report_recorded`. A malformed attempt logs nothing;
`could_not_run` stops with stage `run`, any other failing rule with stage
`verifier`, both after `verifier_check`.

## Approval summary (exact format)

```
Record reproduction of {title[:40]} commit {commit[:12]|(unpinned)} verdict {overall} {confirmed}/{total} claims doc:{doc_hash[:12]}
```

Example (vector `repro_approval_summary/reproduced`):
`Record reproduction of Attention Is Not All You Need: A Small R commit 3f2a9c1e5b7d verdict reproduced 3/3 claims doc:5de4cf692493`.
Materiality `repro.report`.
