import type { JsonValue } from "../envelope.js";
import type { ExtractionClaim } from "../ledger/extraction-claim.js";
import type { BankLine, LedgerEntry } from "../ledger/engine.js";
import type { ReconcilePolicy, ReconcileResult, ArithmeticCheck } from "../ledger/reconcile.js";
import type { ApprovalRequest, ApprovalToken } from "../governance.js";

/**
 * Ledger-substrate conformance vectors, format v1.
 *
 * A vector is a JSON document with a `kind` discriminator, an `input`, and
 * an `expected`. An implementation conforms to a kind if, for every vector
 * of that kind, it produces `expected` from `input` byte-for-byte (hashes,
 * hex signatures) or structurally (JSON-equal) as the kind specifies.
 *
 * Vectors are generated FROM the reference implementation by
 * src/conformance/generate.ts and committed under conformance/vectors/v1/.
 * The manifest carries a SHA-256 per file. Regenerating must reproduce the
 * manifest exactly; if it does not, either the reference changed (bump the
 * format version) or something is non-deterministic (a bug).
 *
 * Every timestamp in a vector is fixed. Nothing in a vector depends on the
 * wall clock, the host, or the order of object keys.
 */

export const CONFORMANCE_FORMAT_VERSION = 1;

export type VectorKind =
  | "canonicalize"
  | "source_document"
  | "claim_shape"
  | "arithmetic"
  | "reconcile"
  | "reconcile_envelope"
  | "ledger_rules"
  | "approval_summary"
  | "approval_token"
  | "approval_verify"
  | "ledger_entry_id"
  | "audit_chain"
  | "ledger_post";

interface VectorBase<K extends VectorKind, I, E> {
  readonly format_version: 1;
  readonly kind: K;
  readonly id: string;
  readonly description: string;
  readonly input: I;
  readonly expected: E;
}

/** canonicalize(input.value) === expected.canonical; sha256(canonical) === expected.sha256 */
export type CanonicalizeVector = VectorBase<
  "canonicalize",
  { readonly value: JsonValue },
  { readonly canonical: string; readonly sha256: string }
>;

/** sealSourceDocument(utf8(input.text)).doc_hash === expected.doc_hash; byte_length matches. */
export type SourceDocumentVector = VectorBase<
  "source_document",
  { readonly text_utf8: string; readonly mime: string; readonly label: string },
  { readonly doc_hash: string; readonly byte_length: number }
>;

/** validateClaimShape(input.claim) → ok / sorted error strings. */
export type ClaimShapeVector = VectorBase<
  "claim_shape",
  { readonly claim: JsonValue },
  { readonly ok: boolean; readonly errors: ReadonlyArray<string> }
>;

/** checkArithmetic(claim, tolerance) → ArithmeticCheck (JSON-equal). */
export type ArithmeticVector = VectorBase<
  "arithmetic",
  { readonly claim: ExtractionClaim; readonly tolerance: number },
  ArithmeticCheck
>;

/** reconcile(claim, bank_lines, policy) → ReconcileResult (JSON-equal). */
export type ReconcileVector = VectorBase<
  "reconcile",
  { readonly claim: ExtractionClaim; readonly bank_lines: ReadonlyArray<BankLine>; readonly policy: ReconcilePolicy },
  ReconcileResult
>;

/**
 * The content-addressed request envelope for a reconcile call. Given the
 * pinned engine version, schema hash, inputs, and data_as_of, request_hash
 * must match. This is the replay key an auditor uses.
 */
export type ReconcileEnvelopeVector = VectorBase<
  "reconcile_envelope",
  {
    readonly operation: "ledger.reconcile";
    readonly engine_version: string;
    readonly schema_hash: string;
    readonly claim: ExtractionClaim;
    readonly bank_lines: ReadonlyArray<BankLine>;
    readonly policy: ReconcilePolicy;
    readonly data_as_of: string;
  },
  { readonly request_hash: string; readonly result: ReconcileResult; readonly byte_identical_replayable: true }
>;

/** runVerifier(makeLedgerRules(opts), action, context) → per-rule pass + reason code. */
export type LedgerRulesVector = VectorBase<
  "ledger_rules",
  {
    readonly confidence_floor: number;
    readonly claim: ExtractionClaim;
    readonly reconciliation: ReconcileResult;
    readonly state: {
      readonly closed_through?: string;
      readonly valid_account_codes?: ReadonlyArray<string>;
      readonly posted_doc_hashes?: ReadonlyArray<string>;
    };
    readonly jurisdiction: "US" | "EU" | "UK" | "SG" | "HK" | "UAE" | "GLOBAL";
  },
  {
    readonly ok: boolean;
    readonly checks: ReadonlyArray<{ readonly rule_id: string; readonly pass: boolean; readonly code: string | null }>;
  }
>;

/** approvalSummary(claim, reconciliation) === expected.summary (exact string). */
export type ApprovalSummaryVector = VectorBase<
  "approval_summary",
  { readonly claim: ExtractionClaim; readonly reconciliation: ReconcileResult },
  { readonly summary: string }
>;

/**
 * HMAC-SHA256 approval token. Secret is given as UTF-8 text. approved_at is
 * fixed. signature must match hex-for-hex.
 */
export type ApprovalTokenVector = VectorBase<
  "approval_token",
  { readonly approver_id: string; readonly secret_utf8: string; readonly request: ApprovalRequest; readonly approved_at: string },
  { readonly token: ApprovalToken }
>;

/** verifyApproval(token, trusted, request) → ok / reason. */
export type ApprovalVerifyVector = VectorBase<
  "approval_verify",
  {
    readonly token: ApprovalToken;
    readonly trusted: ReadonlyArray<{ readonly approver_id: string; readonly secret_utf8: string }>;
    readonly request: ApprovalRequest;
  },
  { readonly ok: boolean; readonly reason: string | null }
>;

/** entryId(entry) === expected.entry_id */
export type LedgerEntryIdVector = VectorBase<
  "ledger_entry_id",
  { readonly entry: LedgerEntry },
  { readonly entry_id: string; readonly canonical: string }
>;

/**
 * Hash chain over a fixed sequence of audit entries. Timestamps are given,
 * so self_hash values are deterministic. Implementations must reproduce
 * every self_hash and prev_hash, and detect the listed tamper.
 */
export type AuditChainVector = VectorBase<
  "audit_chain",
  {
    readonly entries: ReadonlyArray<{
      readonly action: string;
      readonly subject: string;
      readonly session_id: string;
      readonly timestamp: string;
      readonly model_lineage?: ReadonlyArray<{ model: string; version: string }>;
      readonly approver?: string;
      readonly payload: JsonValue;
    }>;
    /** After hashing, mutate entries[tamper.seq].payload to tamper.payload and re-verify. */
    readonly tamper: { readonly seq: number; readonly payload: JsonValue };
  },
  {
    readonly genesis: string;
    readonly hashes: ReadonlyArray<{ readonly seq: number; readonly prev_hash: string; readonly self_hash: string }>;
    readonly tampered_broken_at_seq: number;
  }
>;

/**
 * End-to-end: given a claim, bank feed, verifier state, and an optional
 * approval, ledgerPost must stop at the given stage (or succeed) and emit
 * exactly the listed audit actions in order. request_hash is deterministic
 * given the fixed engine_version.
 */
export type LedgerPostVector = VectorBase<
  "ledger_post",
  {
    readonly engine_version: string;
    readonly claim: JsonValue;
    readonly bank_lines: ReadonlyArray<BankLine>;
    readonly bank_account_code: string;
    readonly data_as_of: string;
    readonly policy: ReconcilePolicy;
    readonly confidence_floor: number;
    readonly state: LedgerRulesVector["input"]["state"];
    readonly jurisdiction: LedgerRulesVector["input"]["jurisdiction"];
    readonly session_id: string;
    readonly trusted: ReadonlyArray<{ readonly approver_id: string; readonly secret_utf8: string }>;
    /** "none" | "valid" | "wrong_hash" | "unknown_approver" — how the approval is constructed. */
    readonly approval: "none" | "valid" | "wrong_hash" | "unknown_approver";
    readonly approved_at: string;
    /** If true, the engine returns a network error on post. */
    readonly engine_fails: boolean;
  },
  {
    readonly ok: boolean;
    readonly stage: "claim_shape" | "reconciliation" | "verifier" | "approval" | "engine" | null;
    readonly request_hash: string | null;
    readonly reconcile_status: ReconcileResult["status"] | null;
    readonly audit_actions: ReadonlyArray<string>;
    readonly posted_entry_id: string | null;
    readonly posted_total: number | null;
  }
>;

export type ConformanceVector =
  | CanonicalizeVector
  | SourceDocumentVector
  | ClaimShapeVector
  | ArithmeticVector
  | ReconcileVector
  | ReconcileEnvelopeVector
  | LedgerRulesVector
  | ApprovalSummaryVector
  | ApprovalTokenVector
  | ApprovalVerifyVector
  | LedgerEntryIdVector
  | AuditChainVector
  | LedgerPostVector;

export interface ConformanceManifest {
  readonly format_version: 1;
  readonly generated_by: string;
  readonly reference_versions: {
    readonly package: string;
    readonly reconcile_engine: string;
    readonly ledger_engine: string;
    readonly ledger_schema_hash: string;
  };
  readonly vectors: ReadonlyArray<{ readonly path: string; readonly kind: VectorKind; readonly id: string; readonly sha256: string }>;
  /** SHA-256 over the canonical JSON of `vectors`. The one number that identifies this suite. */
  readonly suite_hash: string;
}
