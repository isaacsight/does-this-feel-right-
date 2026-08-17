import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { canonicalize, sha256, requestHash, type JsonValue } from "../envelope.js";
import { AppendOnlyAuditLog, chainAuditEntries, verifyAuditChain, type AuditEntry } from "../audit-log.js";
import { Approver, verifyApproval } from "../governance.js";
import { runVerifier, makeLedgerRules } from "../verifier/index.js";
import { sealSourceDocument } from "../ledger/source-document.js";
import { validateClaimShape } from "../ledger/extraction-claim.js";
import { checkArithmetic, reconcile } from "../ledger/reconcile.js";
import { entryId } from "../ledger/engine.js";
import { ledgerPost, approvalSummary, LEDGER_POST_MATERIALITY } from "../tools/ledger-post.js";
import { MemoryLedger, type ConformanceImplementation } from "./implementation.js";
import type { LedgerPostVector, LedgerRulesVector } from "./types.js";
import { readFile } from "node:fs/promises";

/** The reference implementation, adapted to the conformance surface. */
export const referenceImplementation: ConformanceImplementation = {
  canonicalize,
  sha256,
  sealSourceDocument(bytes) {
    const d = sealSourceDocument(bytes, { mime: "application/octet-stream", label: "x", captured_at: "2026-01-01T00:00:00.000Z" });
    return { doc_hash: d.doc_hash, byte_length: d.byte_length };
  },
  validateClaimShape(claim) {
    const r = validateClaimShape(claim);
    return r.ok ? { ok: true } : { ok: false, errors: r.errors };
  },
  checkArithmetic,
  reconcile,
  requestHash,
  runLedgerRules(input: LedgerRulesVector["input"]) {
    const report = runVerifier(
      makeLedgerRules({ confidence_floor: input.confidence_floor }),
      { operation: "ledger.post", inputs: { claim: input.claim, reconciliation: input.reconciliation } as unknown as JsonValue, materiality: "material" },
      { session_id: "conformance", state: input.state as unknown as JsonValue, jurisdiction: input.jurisdiction },
    );
    return {
      ok: report.ok,
      checks: report.checks.map((c) => ({ rule_id: c.rule_id, pass: c.result.pass, code: c.result.pass ? null : c.result.reason.code })),
    };
  },
  approvalSummary,
  approve(approver_id, secret_utf8, request, approved_at) {
    return new Approver(approver_id, Buffer.from(secret_utf8, "utf8")).approve(request, approved_at);
  },
  verifyApproval(token, trusted, request) {
    const map = new Map(trusted.map((t) => [t.approver_id, Buffer.from(t.secret_utf8, "utf8")]));
    const r = verifyApproval(token, map, request);
    return r.ok ? { ok: true, reason: null } : { ok: false, reason: r.reason };
  },
  entryId,
  chainAuditEntries: (inputs) => chainAuditEntries(inputs),
  verifyAuditChain: (entries) => verifyAuditChain(entries),
  async ledgerPost(input: LedgerPostVector["input"]) {
    const dir = await mkdtemp(join(tmpdir(), "conformance-"));
    const auditPath = join(dir, "audit.jsonl");
    try {
      const auditLog = await AppendOnlyAuditLog.open(auditPath);
      const engine = new MemoryLedger(input.engine_version, input.bank_lines, input.engine_fails, entryId);
      const trusted = new Map(input.trusted.map((t) => [t.approver_id, Buffer.from(t.secret_utf8, "utf8")]));
      const deps = {
        auditLog,
        rules: makeLedgerRules({ confidence_floor: input.confidence_floor }),
        verifierContext: { session_id: input.session_id, state: input.state as unknown as JsonValue, jurisdiction: input.jurisdiction },
        trustedApprovers: trusted,
        engine,
      };
      const base = {
        claim: input.claim as unknown as LedgerPostVector["input"]["claim"] as never,
        bank_lines: input.bank_lines,
        bank_account_code: input.bank_account_code,
        data_as_of: input.data_as_of,
        policy: input.policy,
      };

      // Build the approval, if any, from a dry run that yields the request_hash.
      let approval: import("../governance.js").ApprovalToken | undefined;
      if (input.approval !== "none") {
        const dry = await ledgerPost(base, deps);
        const hash = dry.ok ? dry.request_hash : dry.request_hash;
        if (hash) {
          const claim = input.claim as never;
          const rec = reconcile(claim, input.bank_lines, input.policy);
          const req = { request_hash: input.approval === "wrong_hash" ? "f".repeat(64) : hash, summary: approvalSummary(claim, rec), session_id: input.session_id, materiality: LEDGER_POST_MATERIALITY };
          const signer = input.approval === "unknown_approver" ? { approver_id: "intern.bob", secret_utf8: "not-in-the-trust-set" } : input.trusted[0]!;
          approval = new Approver(signer.approver_id, Buffer.from(signer.secret_utf8, "utf8")).approve(req, input.approved_at);
        }
        // Reset the audit log so the recorded sequence is the real run only.
        await rm(auditPath, { force: true });
        deps.auditLog = await AppendOnlyAuditLog.open(auditPath);
      }

      const r = await ledgerPost(approval ? { ...base, approval } : base, deps);
      const raw = await readFile(auditPath, "utf8").catch(() => "");
      const audit_actions = raw.split("\n").filter(Boolean).map((l) => (JSON.parse(l) as AuditEntry).action);
      if (r.ok) {
        return {
          ok: true,
          stage: null,
          request_hash: r.request_hash,
          reconcile_status: "matched",
          audit_actions,
          posted_entry_id: r.response.value.entry_id,
          posted_total: r.response.value.total,
        };
      }
      return {
        ok: false,
        stage: r.stage,
        request_hash: r.request_hash ?? null,
        reconcile_status: r.reconciliation?.status ?? null,
        audit_actions,
        posted_entry_id: null,
        posted_total: null,
      };
    } finally {
      await rm(dir, { recursive: true, force: true });
    }
  },
};
