"""Port of the kbot-finance ledger substrate.

The AI proposes (an extraction claim), arithmetic disposes (a deterministic
reconciliation engine plus rules-as-code), a human signs (an HMAC approval
bound to the exact request hash), and every step is hash-chained. Passes all
143 vectors of the finance v1 conformance suite byte-for-byte; see
``provsubstrate.finance.conformance``.
"""

from .source_document import SourceDocument, SourceDocumentVerdict, seal_source_document, verify_source_document
from .extraction_claim import ClaimShapeResult, ExtractionClaim, record_extraction_claim, validate_claim_shape
from .reconcile import (
    DEFAULT_RECONCILE_POLICY,
    RECONCILE_ENGINE_VERSION,
    ArithmeticCheck,
    BankLine,
    ReconcilePolicy,
    ReconcileResult,
    ReconcileStatus,
    check_arithmetic,
    day_number,
    reconcile,
)
from .engine import (
    LEDGER_ENGINE_VERSION,
    LedgerEngine,
    LedgerEngineError,
    LedgerEntry,
    LedgerOutcome,
    MemoryLedger,
    PostedEntry,
    entry_id,
)
from .verifier import (
    Rule,
    RuleEvidence,
    RuleResult,
    VerifierAction,
    VerifierCheck,
    VerifierContext,
    VerifierReport,
    make_account_code_rule,
    make_confidence_floor_rule,
    make_duplicate_document_rule,
    make_ledger_rules,
    make_period_lock_rule,
    make_reconciled_rule,
    run_verifier,
)
from .ledger_post import (
    LEDGER_POST_MATERIALITY,
    LEDGER_SCHEMA_HASH,
    LedgerPostDeps,
    LedgerPostInputs,
    LedgerPostResult,
    LedgerPostValue,
    approval_summary,
    claim_to_entry,
    ledger_post,
)
from .conformance import ALL_FINANCE_V1_HANDLERS, FINANCE_HANDLERS, make_finance_handlers
from .mcp import finance_prepare_post, finance_reconcile, mcp_tools

__all__ = [
    "finance_prepare_post", "finance_reconcile", "mcp_tools",
    "SourceDocument", "SourceDocumentVerdict", "seal_source_document", "verify_source_document",
    "ClaimShapeResult", "ExtractionClaim", "record_extraction_claim", "validate_claim_shape",
    "DEFAULT_RECONCILE_POLICY", "RECONCILE_ENGINE_VERSION", "ArithmeticCheck", "BankLine", "ReconcilePolicy",
    "ReconcileResult", "ReconcileStatus", "check_arithmetic", "day_number", "reconcile",
    "LEDGER_ENGINE_VERSION", "LedgerEngine", "LedgerEngineError", "LedgerEntry", "LedgerOutcome", "MemoryLedger",
    "PostedEntry", "entry_id",
    "Rule", "RuleEvidence", "RuleResult", "VerifierAction", "VerifierCheck", "VerifierContext", "VerifierReport",
    "make_account_code_rule", "make_confidence_floor_rule", "make_duplicate_document_rule", "make_ledger_rules",
    "make_period_lock_rule", "make_reconciled_rule", "run_verifier",
    "LEDGER_POST_MATERIALITY", "LEDGER_SCHEMA_HASH", "LedgerPostDeps", "LedgerPostInputs", "LedgerPostResult",
    "LedgerPostValue", "approval_summary", "claim_to_entry", "ledger_post",
    "ALL_FINANCE_V1_HANDLERS", "FINANCE_HANDLERS", "make_finance_handlers",
]
