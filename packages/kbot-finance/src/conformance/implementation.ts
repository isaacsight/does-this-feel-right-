import type { JsonValue } from "../envelope.js";
import type { ExtractionClaim } from "../ledger/extraction-claim.js";
import type { BankLine, LedgerEntry, LedgerEngine, LedgerOutcome, PostedEntry } from "../ledger/engine.js";
import type { ReconcilePolicy, ReconcileResult, ArithmeticCheck } from "../ledger/reconcile.js";
import type { ApprovalRequest, ApprovalToken } from "../governance.js";
import type { AuditEntry, AuditEntryInput } from "../audit-log.js";
import type { LedgerPostVector, LedgerRulesVector } from "./types.js";

/**
 * The surface an implementation exposes to the conformance runner.
 *
 * A third party porting the substrate (another language, another ledger)
 * implements this interface and calls `runConformance(dir, impl)`. Every
 * function is pure or takes its state explicitly. `ledgerPost` is the one
 * stateful flow; it receives an in-memory engine and an in-memory audit
 * sink so no disk is involved.
 */
export interface ConformanceImplementation {
  canonicalize(value: JsonValue): string;
  sha256(text: string): string;
  sealSourceDocument(bytes: Uint8Array): { doc_hash: string; byte_length: number };
  validateClaimShape(claim: unknown): { ok: true } | { ok: false; errors: ReadonlyArray<string> };
  checkArithmetic(claim: ExtractionClaim, tolerance: number): ArithmeticCheck;
  reconcile(claim: ExtractionClaim, bank_lines: ReadonlyArray<BankLine>, policy: ReconcilePolicy): ReconcileResult;
  requestHash(req: { operation: string; engine_version: string; schema_hash: string; inputs: JsonValue; data_as_of: string }): string;
  runLedgerRules(input: LedgerRulesVector["input"]): LedgerRulesVector["expected"];
  approvalSummary(claim: ExtractionClaim, rec: ReconcileResult): string;
  approve(approver_id: string, secret_utf8: string, request: ApprovalRequest, approved_at: string): ApprovalToken;
  verifyApproval(token: ApprovalToken, trusted: ReadonlyArray<{ approver_id: string; secret_utf8: string }>, request: ApprovalRequest): { ok: boolean; reason: string | null };
  entryId(entry: LedgerEntry): string;
  chainAuditEntries(inputs: ReadonlyArray<AuditEntryInput & { timestamp: string }>): AuditEntry[];
  verifyAuditChain(entries: ReadonlyArray<AuditEntry>): { ok: true } | { ok: false; broken_at_seq: number };
  ledgerPost(input: LedgerPostVector["input"]): Promise<LedgerPostVector["expected"]>;
}

/** Minimal in-memory engine for the ledger_post kind. Deterministic. */
export class MemoryLedger implements LedgerEngine {
  readonly posted: Array<{ entry: LedgerEntry; entry_id: string }> = [];
  constructor(
    readonly engine_version: string,
    private feed: ReadonlyArray<BankLine>,
    private readonly fail: boolean,
    private readonly idOf: (e: LedgerEntry) => string,
  ) {}
  async bankLines(): Promise<LedgerOutcome<ReadonlyArray<BankLine>>> {
    return { ok: true, value: this.feed };
  }
  async post(entry: LedgerEntry): Promise<LedgerOutcome<PostedEntry>> {
    if (this.fail) return { ok: false, error: { code: "network", message: "conformance: engine down" } };
    const entry_id = this.idOf(entry);
    this.posted.push({ entry, entry_id });
    this.feed = this.feed.map((b) => (b.id === entry.bank_line_id ? { ...b, reconciled: true } : b));
    return { ok: true, value: { entry_id, posted_at: "2026-08-15T00:00:00.000Z" } };
  }
}
