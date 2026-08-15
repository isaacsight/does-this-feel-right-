import type { JsonValue } from "../envelope.js";
import type { AppendOnlyAuditLog, AuditEntry } from "../audit-log.js";

/**
 * Extraction claims.
 *
 * When a model reads a source document and returns "vendor X, total 1,240.50,
 * dated 2026-08-12, looks like fertiliser", that output is a CLAIM. It is not
 * a ledger entry and it never becomes one directly. It is recorded — with the
 * model that made it and the document hash it was made from — and then handed
 * to a deterministic engine that must independently confirm it.
 *
 * This is the doctrine of the whole package applied to bookkeeping: the AI
 * layer never produces the number. It proposes; arithmetic and the bank feed
 * dispose; a human signs.
 */

export interface ClaimedLineItem {
  readonly description: string;
  readonly quantity: number;
  readonly unit_amount: number;
  /** quantity * unit_amount as the model read it — checked, not trusted. */
  readonly line_amount: number;
  /** Chart-of-accounts code the model proposes. Verified against the live chart. */
  readonly account_code: string;
  readonly tax_type?: string;
}

export interface ExtractionClaim {
  /** Hash of the sealed source document the claim was extracted from. */
  readonly doc_hash: string;
  readonly direction: "out" | "in";
  readonly vendor: string | null;
  /** ISO date YYYY-MM-DD as read from the document. */
  readonly date: string | null;
  readonly currency: string;
  readonly subtotal: number;
  readonly tax: number;
  readonly total: number;
  readonly line_items: ReadonlyArray<ClaimedLineItem>;
  readonly reference: string | null;
  /** Model self-reported confidence in [0,1]. Advisory; the verifier sets a floor. */
  readonly confidence: number;
  /** Which model + prompt produced this claim. Required. */
  readonly model_lineage: ReadonlyArray<{ readonly model: string; readonly version: string }>;
}

/**
 * Record a claim in the audit log. Returns the entry so the caller can
 * carry its self_hash forward into the reconciliation envelope.
 */
export async function recordExtractionClaim(
  auditLog: AppendOnlyAuditLog,
  session_id: string,
  claim: ExtractionClaim,
): Promise<AuditEntry> {
  return auditLog.append({
    action: "extraction_claim",
    subject: "ledger.extract",
    session_id,
    model_lineage: claim.model_lineage,
    payload: claim as unknown as JsonValue,
  });
}

/** Structural validation for claims arriving from any model. Pure. */
export function validateClaimShape(
  claim: unknown,
): { ok: true; claim: ExtractionClaim } | { ok: false; errors: ReadonlyArray<string> } {
  const errors: string[] = [];
  const c = claim as Partial<ExtractionClaim> | null;
  if (!c || typeof c !== "object") return { ok: false, errors: ["claim is not an object"] };
  if (typeof c.doc_hash !== "string" || !/^[0-9a-f]{64}$/.test(c.doc_hash)) errors.push("doc_hash must be sha256 hex");
  if (c.direction !== "out" && c.direction !== "in") errors.push("direction must be out|in");
  if (typeof c.currency !== "string" || c.currency.length !== 3) errors.push("currency must be ISO 4217");
  for (const k of ["subtotal", "tax", "total"] as const) {
    if (typeof c[k] !== "number" || !Number.isFinite(c[k])) errors.push(`${k} must be finite number`);
  }
  if (!Array.isArray(c.line_items) || c.line_items.length === 0) errors.push("line_items must be non-empty");
  else {
    c.line_items.forEach((li, i) => {
      if (typeof li.account_code !== "string" || li.account_code.length === 0) errors.push(`line_items[${i}].account_code missing`);
      for (const k of ["quantity", "unit_amount", "line_amount"] as const) {
        if (typeof li[k] !== "number" || !Number.isFinite(li[k])) errors.push(`line_items[${i}].${k} must be finite number`);
      }
    });
  }
  if (typeof c.confidence !== "number" || c.confidence < 0 || c.confidence > 1) errors.push("confidence must be in [0,1]");
  if (!Array.isArray(c.model_lineage) || c.model_lineage.length === 0) errors.push("model_lineage required");
  if (c.date !== null && c.date !== undefined && !/^\d{4}-\d{2}-\d{2}$/.test(String(c.date))) errors.push("date must be YYYY-MM-DD or null");
  if (errors.length > 0) return { ok: false, errors };
  return { ok: true, claim: c as ExtractionClaim };
}
