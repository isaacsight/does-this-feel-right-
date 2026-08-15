import {
  sealEnvelope,
  sha256,
  canonicalize,
  requestHash,
  type ContentAddressedRequest,
  type ContentAddressedResponse,
  type JsonValue,
} from "../envelope.js";
import { AppendOnlyAuditLog } from "../audit-log.js";
import { runVerifier, type Rule, type VerifierContext } from "../verifier/index.js";
import { verifyApproval, type ApprovalToken, type ApprovalRequest } from "../governance.js";
import { recordExtractionClaim, validateClaimShape, type ExtractionClaim } from "../ledger/extraction-claim.js";
import {
  reconcile,
  DEFAULT_RECONCILE_POLICY,
  RECONCILE_ENGINE_VERSION,
  type ReconcilePolicy,
  type ReconcileResult,
} from "../ledger/reconcile.js";
import type { BankLine, LedgerEngine, LedgerEntry } from "../ledger/engine.js";

/**
 * ledger_post — the full path from a model's reading of a document to a
 * posted general-ledger entry, with every step on the audit chain.
 *
 *   1. The claim is recorded (extraction_claim) with model lineage.
 *   2. The deterministic reconciliation engine runs inside its own
 *      content-addressed envelope (byte_identical_replayable: true) and is
 *      recorded (reconciliation).
 *   3. The ledger verifier runs (verifier_check). Any failure stops here
 *      with a reason code.
 *   4. Posting is material: a signed approval token from a trusted human
 *      must be present and must bind to THIS request hash. Missing or
 *      invalid → approval_denied, stop.
 *   5. Only then does the ledger engine post (engine_request/engine_response).
 *
 * The model is never on the path between "claim" and "number". The number
 * that reaches the ledger is the reconciled bank-feed amount, and the human
 * signed the exact envelope that carried it. Which ledger sits underneath
 * is the engine's business — see ledger/engine.ts.
 */

const SCHEMA_HASH = sha256(
  canonicalize({
    type: "object",
    fields: {
      claim: { type: "ExtractionClaim" },
      reconciliation: { type: "ReconcileResult" },
      bank_account_code: { type: "string" },
    },
  } as JsonValue),
);

export const LEDGER_POST_MATERIALITY = "ledger.post";

export interface LedgerPostInputs {
  readonly claim: ExtractionClaim;
  /** Bank feed lines the reconciliation engine considers. Usually from engine.bankLines(). */
  readonly bank_lines: ReadonlyArray<BankLine>;
  /** Code of the bank/cash account the movement sits in. */
  readonly bank_account_code: string;
  readonly data_as_of: string;
  readonly policy?: ReconcilePolicy;
  /** Signed approval. May be omitted on a first call to obtain the request_hash to sign. */
  readonly approval?: ApprovalToken;
}

export interface LedgerPostDeps {
  readonly auditLog: AppendOnlyAuditLog;
  readonly rules: ReadonlyArray<Rule>;
  readonly verifierContext: VerifierContext;
  /** Trusted approver secrets, keyed by approver_id. */
  readonly trustedApprovers: ReadonlyMap<string, Buffer>;
  /** The general ledger underneath. Required — there is no default vendor. */
  readonly engine: LedgerEngine;
}

export interface LedgerPostValue {
  readonly entry_id: string;
  readonly matched_bank_line_id: string;
  readonly total: number;
  readonly currency: string;
}

export type LedgerPostResult =
  | { readonly ok: true; readonly request_hash: string; readonly response: ContentAddressedResponse<LedgerPostValue> }
  | {
      readonly ok: false;
      readonly stage: "claim_shape" | "reconciliation" | "verifier" | "approval" | "engine";
      /** Present from the reconciliation stage on, so an approver can sign it. */
      readonly request_hash?: string;
      readonly reconciliation?: ReconcileResult;
      readonly detail: JsonValue;
    };

export async function ledgerPost(inputs: LedgerPostInputs, deps: LedgerPostDeps): Promise<LedgerPostResult> {
  const session_id = deps.verifierContext.session_id;

  // 1. Claim shape + record.
  const shape = validateClaimShape(inputs.claim);
  if (!shape.ok) {
    return { ok: false, stage: "claim_shape", detail: { errors: [...shape.errors] } };
  }
  await recordExtractionClaim(deps.auditLog, session_id, shape.claim);

  // 2. Deterministic reconciliation in its own envelope.
  const policy = inputs.policy ?? DEFAULT_RECONCILE_POLICY;
  const reconRequest: ContentAddressedRequest = {
    operation: "ledger.reconcile",
    engine_version: RECONCILE_ENGINE_VERSION,
    schema_hash: SCHEMA_HASH,
    inputs: { claim: shape.claim, bank_lines: inputs.bank_lines, policy } as unknown as JsonValue,
    data_as_of: inputs.data_as_of,
  };
  const reconSealed = await sealEnvelope<ReconcileResult>(
    reconRequest,
    async () => reconcile(shape.claim, inputs.bank_lines, policy),
    { byte_identical_replayable: true },
  );
  await deps.auditLog.append({
    action: "reconciliation",
    subject: "ledger.reconcile",
    session_id,
    payload: { request_hash: reconSealed.request_hash, result: reconSealed.value } as unknown as JsonValue,
  });

  // 3. The post request. Its hash is what the human signs.
  const request: ContentAddressedRequest = {
    operation: "ledger.post",
    engine_version: deps.engine.engine_version,
    schema_hash: SCHEMA_HASH,
    inputs: {
      claim: shape.claim,
      reconciliation: reconSealed.value,
      reconciliation_request_hash: reconSealed.request_hash,
      bank_account_code: inputs.bank_account_code,
    } as unknown as JsonValue,
    data_as_of: inputs.data_as_of,
  };
  const request_hash = requestHash(request);

  const verifier_report = runVerifier(
    deps.rules,
    { operation: "ledger.post", inputs: request.inputs, materiality: "material" },
    deps.verifierContext,
  );
  await deps.auditLog.append({
    action: "verifier_check",
    subject: "ledger.post",
    session_id,
    payload: { request_hash, report: verifier_report } as unknown as JsonValue,
  });
  if (!verifier_report.ok) {
    return {
      ok: false,
      stage: reconSealed.value.status === "matched" ? "verifier" : "reconciliation",
      request_hash,
      reconciliation: reconSealed.value,
      detail: verifier_report as unknown as JsonValue,
    };
  }

  // 4. Material gate.
  const approvalRequest: ApprovalRequest = {
    request_hash,
    summary: approvalSummary(shape.claim, reconSealed.value),
    session_id,
    materiality: LEDGER_POST_MATERIALITY,
  };
  if (!inputs.approval) {
    await deps.auditLog.append({
      action: "approval_denied",
      subject: "ledger.post",
      session_id,
      payload: { request_hash, reason: "no_approval_token", summary: approvalRequest.summary },
    });
    return {
      ok: false,
      stage: "approval",
      request_hash,
      reconciliation: reconSealed.value,
      detail: { reason: "no_approval_token", summary: approvalRequest.summary },
    };
  }
  const verdict = verifyApproval(inputs.approval, deps.trustedApprovers, approvalRequest);
  if (!verdict.ok) {
    await deps.auditLog.append({
      action: "approval_denied",
      subject: "ledger.post",
      session_id,
      approver: inputs.approval.approver_id,
      payload: { request_hash, reason: verdict.reason },
    });
    return {
      ok: false,
      stage: "approval",
      request_hash,
      reconciliation: reconSealed.value,
      detail: { reason: verdict.reason },
    };
  }
  await deps.auditLog.append({
    action: "approval_granted",
    subject: "ledger.post",
    session_id,
    approver: inputs.approval.approver_id,
    payload: { request_hash, approved_at: inputs.approval.approved_at },
  });

  // 5. Engine.
  await deps.auditLog.append({
    action: "engine_request",
    subject: "ledger.post",
    session_id,
    payload: request as unknown as JsonValue,
  });

  const matched = reconSealed.value.matched_bank_line_id;
  const bankLine = inputs.bank_lines.find((l) => l.id === matched);
  const sealed = await sealEnvelope<LedgerPostValue>(
    request,
    async () => {
      if (!bankLine) throw new Error("ledger.post: matched bank line disappeared");
      const entry = claimToEntry(shape.claim, bankLine, inputs.bank_account_code);
      const r = await deps.engine.post(entry);
      if (!r.ok) throw new Error(`ledger engine post failed: ${r.error.code}: ${r.error.message}`);
      return {
        entry_id: r.value.entry_id,
        matched_bank_line_id: bankLine.id,
        // The number that lands is the bank feed's, not the model's.
        total: bankLine.amount,
        currency: shape.claim.currency,
      };
    },
    { byte_identical_replayable: false },
  ).catch((e: Error) => ({ error: e.message }) as const);

  if ("error" in sealed) {
    await deps.auditLog.append({
      action: "incident",
      subject: "ledger.post",
      session_id,
      payload: { request_hash, error: sealed.error },
    });
    return { ok: false, stage: "engine", request_hash, reconciliation: reconSealed.value, detail: { error: sealed.error } };
  }

  await deps.auditLog.append({
    action: "engine_response",
    subject: "ledger.post",
    session_id,
    payload: {
      request_hash: sealed.request_hash,
      produced_at: sealed.produced_at,
      entry_id: sealed.value.entry_id,
      matched_bank_line_id: sealed.value.matched_bank_line_id,
      total: sealed.value.total,
    },
  });

  return { ok: true, request_hash, response: sealed };
}

/** Human-readable line the approver signs. Deterministic over its inputs. */
export function approvalSummary(claim: ExtractionClaim, rec: ReconcileResult): string {
  const dir = claim.direction === "out" ? "SPEND" : "RECEIVE";
  return `${dir} ${claim.currency} ${claim.total.toFixed(2)} ${claim.vendor ?? "(no vendor)"} ${claim.date ?? "(no date)"} doc:${claim.doc_hash.slice(0, 12)} bank:${rec.matched_bank_line_id ?? "-"}`;
}

/**
 * Map a confirmed claim onto a vendor-neutral ledger entry. Line detail
 * comes from the claim; the total and settlement date come from the bank
 * line; the reference carries the source-document hash.
 */
export function claimToEntry(claim: ExtractionClaim, bankLine: BankLine, bank_account_code: string): LedgerEntry {
  return {
    direction: claim.direction,
    counterparty: claim.vendor,
    date: bankLine.date ?? claim.date,
    currency: claim.currency,
    line_items: claim.line_items.map((li) => ({
      description: li.description,
      quantity: li.quantity,
      unit_amount: li.unit_amount,
      account_code: li.account_code,
      ...(li.tax_type ? { tax_type: li.tax_type } : {}),
    })),
    bank_account_code,
    bank_line_id: bankLine.id,
    reference: `doc:${claim.doc_hash.slice(0, 16)}${claim.reference ? " " + claim.reference : ""}`,
    doc_hash: claim.doc_hash,
    total: bankLine.amount,
  };
}
