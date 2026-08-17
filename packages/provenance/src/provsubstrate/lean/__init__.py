"""Proof ledger: the model proposes a proof, the Lean kernel disposes, a
mathematician signs."""

from .claim import ClaimShape, ProofClaim, proof_file_hash, render_lean_file, statement_hash, validate_claim_shape
from .kernel import (
    KernelDisposer,
    KernelUnavailable,
    KernelVerdict,
    LakeDisposer,
    StaticScan,
    StubKernel,
    check_proof,
    merge_verdict,
    parse_lean_output,
    static_scan,
    strip_comments,
)
from .ledger import (
    LEAN_ENGINE_VERSION,
    LEAN_OPERATION,
    LEAN_RECORD_MATERIALITY,
    LEAN_SCHEMA,
    LEAN_SCHEMA_HASH,
    LeanDeps,
    Prepared,
    ProofLedger,
    RecordResult,
    approval_summary,
    check_request,
    prepare,
    record_proof,
)
from .rules import (
    CONFIDENCE_BELOW_FLOOR,
    CONTAINS_SORRY,
    DEFAULT_AXIOM_ALLOWLIST,
    DEFAULT_CONFIDENCE_FLOOR,
    FORBIDDEN_AXIOM,
    KERNEL_REJECTED,
    STATEMENT_HASH_MISMATCH,
    TOOLCHAIN_UNPINNED,
    RuleCheck,
    RuleReport,
    run_lean_rules,
)
from .conformance import CONFORMANCE_HANDLERS, compute_expected, conformance_cases
from .mcp import lean_check, lean_prepare, mcp_tools

__all__ = [
    "lean_check", "lean_prepare", "mcp_tools",
    "ClaimShape", "ProofClaim", "proof_file_hash", "render_lean_file", "statement_hash", "validate_claim_shape",
    "KernelDisposer", "KernelUnavailable", "KernelVerdict", "LakeDisposer", "StaticScan", "StubKernel",
    "check_proof", "merge_verdict", "parse_lean_output", "static_scan", "strip_comments",
    "LEAN_ENGINE_VERSION", "LEAN_OPERATION", "LEAN_RECORD_MATERIALITY", "LEAN_SCHEMA", "LEAN_SCHEMA_HASH",
    "LeanDeps", "Prepared", "ProofLedger", "RecordResult", "approval_summary", "check_request", "prepare", "record_proof",
    "CONFIDENCE_BELOW_FLOOR", "CONTAINS_SORRY", "DEFAULT_AXIOM_ALLOWLIST", "DEFAULT_CONFIDENCE_FLOOR", "FORBIDDEN_AXIOM",
    "KERNEL_REJECTED", "STATEMENT_HASH_MISMATCH", "TOOLCHAIN_UNPINNED", "RuleCheck", "RuleReport", "run_lean_rules",
    "CONFORMANCE_HANDLERS", "compute_expected", "conformance_cases",
]
