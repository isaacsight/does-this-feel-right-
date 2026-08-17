"""Claim graph: every number in a paper is a claim hash-linked to the
computation that produced it; re-execution disposes; the author signs."""

from .model import (
    MANIFEST_FORMAT_VERSION,
    Claim,
    Computation,
    ManifestShape,
    claim_id_of,
    computation_id_of,
    manifest_hash,
    validate_manifest,
)
from .reexec import INPUT_HASH_MISMATCH, ExecutionResult, Reexecutor, StubReexecutor, SubprocessReexecutor, extract_value
from .verify import (
    CONFIDENCE_BELOW_FLOOR,
    CONFIRMED,
    DANGLING_COMPUTATION,
    DEFAULT_CONFIDENCE_FLOOR,
    ENVIRONMENT_UNPINNED,
    EXECUTION_FAILED,
    INPUT_HASH_MISMATCH_STATUS,
    MISMATCH,
    TOLERANCE_EXCEEDED,
    UNCONFIRMED_CLAIM,
    ClaimVerdict,
    RuleCheck,
    RuleReport,
    environment_pinned,
    run_claim_rules,
    verify_claim,
)
from .attest import (
    CLAIMS_ATTEST_MATERIALITY,
    CLAIMS_ATTEST_OPERATION,
    CLAIMS_ENGINE_VERSION,
    CLAIMS_SCHEMA,
    CLAIMS_SCHEMA_HASH,
    CLAIMS_VERIFY_OPERATION,
    AttestResult,
    AttestationLedger,
    ClaimOutcome,
    ClaimsDeps,
    Prepared,
    approval_summary,
    attest_manifest,
    attest_request,
    attestation_summary,
    badge_json,
    badge_svg,
    prepare,
    verification_report,
    verify_request,
)
from .conformance import CONFORMANCE_HANDLERS, compute_expected, conformance_cases
from .mcp import claims_badge, claims_verify, mcp_tools

__all__ = [
    "claims_badge", "claims_verify", "mcp_tools",
    "MANIFEST_FORMAT_VERSION", "Claim", "Computation", "ManifestShape", "claim_id_of", "computation_id_of", "manifest_hash", "validate_manifest",
    "INPUT_HASH_MISMATCH", "ExecutionResult", "Reexecutor", "StubReexecutor", "SubprocessReexecutor", "extract_value",
    "CONFIDENCE_BELOW_FLOOR", "CONFIRMED", "DANGLING_COMPUTATION", "DEFAULT_CONFIDENCE_FLOOR", "ENVIRONMENT_UNPINNED", "EXECUTION_FAILED",
    "INPUT_HASH_MISMATCH_STATUS", "MISMATCH", "TOLERANCE_EXCEEDED", "UNCONFIRMED_CLAIM", "ClaimVerdict", "RuleCheck", "RuleReport",
    "environment_pinned", "run_claim_rules", "verify_claim",
    "CLAIMS_ATTEST_MATERIALITY", "CLAIMS_ATTEST_OPERATION", "CLAIMS_ENGINE_VERSION", "CLAIMS_SCHEMA", "CLAIMS_SCHEMA_HASH", "CLAIMS_VERIFY_OPERATION",
    "AttestResult", "AttestationLedger", "ClaimOutcome", "ClaimsDeps", "Prepared", "approval_summary", "attest_manifest", "attest_request",
    "attestation_summary", "badge_json", "badge_svg", "prepare", "verification_report", "verify_request",
    "CONFORMANCE_HANDLERS", "compute_expected", "conformance_cases",
]
