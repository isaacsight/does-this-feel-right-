"""Reproducibility ledger: paper + repo in, attempted reproduction out,
signed report, exportable as a versioned dataset.

The model proposes an attempt (commands + output selectors); a runner
executes it; ``judge`` disposes claim by claim within the paper's own
tolerances; rules-as-code gate; a human signs the exact summary line; the
signed report is a dataset row with Zenodo and Croissant metadata.
"""

from .model import (
    CLAIM_STATUSES,
    OVERALL_STATUSES,
    ClaimSpec,
    ClaimVerdict,
    CommandResult,
    OutputSelector,
    PaperRef,
    RepoRef,
    ReproductionAttempt,
    ReproductionTarget,
    ReproVerdict,
    RunRecord,
)
from .runner import Runner, StubRunner, SubprocessRunner, command_key, extract_values
from .judge import REPRO_RULES, decimal_delta, judge, run_repro_rules, validate_attempt, within_tolerance
from .ledger import (
    REPRO_ENGINE_VERSION,
    REPRO_MATERIALITY,
    REPRO_OPERATION,
    REPRO_SCHEMA_HASH,
    approval_summary,
    build_report,
    record_reproduction,
    repro_request,
)
from .dataset import (
    DATASET_NAME,
    croissant_metadata,
    dataset_filename,
    dataset_manifest,
    export_jsonl,
    zenodo_metadata,
)
from .conformance import CONFORMANCE_HANDLERS, compute_expected, conformance_cases
from .mcp import FixedRunner, mcp_tools, repro_dataset_manifest, repro_judge

__all__ = [
    "FixedRunner", "mcp_tools", "repro_dataset_manifest", "repro_judge",
    "CLAIM_STATUSES", "OVERALL_STATUSES", "ClaimSpec", "ClaimVerdict", "CommandResult", "OutputSelector", "PaperRef", "RepoRef",
    "ReproductionAttempt", "ReproductionTarget", "ReproVerdict", "RunRecord",
    "Runner", "StubRunner", "SubprocessRunner", "command_key", "extract_values",
    "REPRO_RULES", "decimal_delta", "judge", "run_repro_rules", "validate_attempt", "within_tolerance",
    "REPRO_ENGINE_VERSION", "REPRO_MATERIALITY", "REPRO_OPERATION", "REPRO_SCHEMA_HASH",
    "approval_summary", "build_report", "record_reproduction", "repro_request",
    "DATASET_NAME", "croissant_metadata", "dataset_filename", "dataset_manifest", "export_jsonl", "zenodo_metadata",
    "CONFORMANCE_HANDLERS", "compute_expected", "conformance_cases",
]
