import type { Rule, VerifierAction, VerifierContext, RuleResult } from "./index.js";
import type { ExtractionClaim } from "../ledger/extraction-claim.js";
import type { ReconcileResult } from "../ledger/reconcile.js";
import { dayNumber } from "../ledger/reconcile.js";

/**
 * Ledger rules — rules-as-code for posting to a general ledger.
 *
 * Each is a pure predicate over the `ledger.post` action. Failures carry
 * reason codes an accountant can read without opening the code. All are
 * GLOBAL: they encode bookkeeping discipline, not a jurisdiction's statute
 * (jurisdiction-specific tax rules layer on top the same way EU RTS 6 does
 * for trading).
 *
 * Expected action.inputs shape (see tools/ledger-post.ts):
 *   { claim: ExtractionClaim, reconciliation: ReconcileResult, ... }
 *
 * Expected context.state shape:
 *   {
 *     closed_through?: "YYYY-MM-DD",          // period lock
 *     valid_account_codes?: string[],         // live chart of accounts
 *     posted_doc_hashes?: string[],           // already-posted documents
 *   }
 */

interface LedgerInputs {
  claim?: ExtractionClaim;
  reconciliation?: ReconcileResult;
}

interface LedgerState {
  closed_through?: string;
  valid_account_codes?: ReadonlyArray<string>;
  posted_doc_hashes?: ReadonlyArray<string>;
}

const OPS = ["ledger.post"] as const;

/** A document may not be posted into a closed accounting period. */
export function makePeriodLockRule(): Rule {
  return {
    id: "rule.ledger.period_lock",
    jurisdictions: ["GLOBAL"],
    operations: [...OPS],
    evaluate(action: VerifierAction, context: VerifierContext): RuleResult {
      const claim = (action.inputs as LedgerInputs)?.claim;
      const closed = (context.state as LedgerState)?.closed_through;
      if (!claim?.date || !closed) return { pass: true };
      if (dayNumber(claim.date) <= dayNumber(closed)) {
        return {
          pass: false,
          reason: {
            code: "PERIOD_LOCKED",
            summary: `Document dated ${claim.date} falls in a period closed through ${closed}`,
            details: { claim_date: claim.date, closed_through: closed },
          },
        };
      }
      return { pass: true };
    },
  };
}

/** Every proposed account code must exist in the live chart of accounts. */
export function makeAccountCodeRule(): Rule {
  return {
    id: "rule.ledger.account_code",
    jurisdictions: ["GLOBAL"],
    operations: [...OPS],
    evaluate(action: VerifierAction, context: VerifierContext): RuleResult {
      const claim = (action.inputs as LedgerInputs)?.claim;
      const valid = (context.state as LedgerState)?.valid_account_codes;
      if (!claim || !valid) return { pass: true };
      const set = new Set(valid);
      const unknown = claim.line_items.map((l) => l.account_code).filter((c) => !set.has(c));
      if (unknown.length > 0) {
        return {
          pass: false,
          reason: {
            code: "UNKNOWN_ACCOUNT_CODE",
            summary: `Proposed account code(s) not in chart: ${[...new Set(unknown)].join(", ")}`,
            details: { unknown: [...new Set(unknown)] },
          },
        };
      }
      return { pass: true };
    },
  };
}

/** The same source document (by content hash) may not be posted twice. */
export function makeDuplicateDocumentRule(): Rule {
  return {
    id: "rule.ledger.duplicate_document",
    jurisdictions: ["GLOBAL"],
    operations: [...OPS],
    evaluate(action: VerifierAction, context: VerifierContext): RuleResult {
      const claim = (action.inputs as LedgerInputs)?.claim;
      const posted = (context.state as LedgerState)?.posted_doc_hashes ?? [];
      if (!claim) return { pass: true };
      if (posted.includes(claim.doc_hash)) {
        return {
          pass: false,
          reason: {
            code: "DUPLICATE_SOURCE_DOCUMENT",
            summary: "A document with identical bytes has already been posted",
            details: { doc_hash: claim.doc_hash },
          },
        };
      }
      return { pass: true };
    },
  };
}

/** The reconciliation engine must have confirmed the claim. */
export function makeReconciledRule(): Rule {
  return {
    id: "rule.ledger.reconciled",
    jurisdictions: ["GLOBAL"],
    operations: [...OPS],
    evaluate(action: VerifierAction, _context: VerifierContext): RuleResult {
      const rec = (action.inputs as LedgerInputs)?.reconciliation;
      if (!rec) {
        return {
          pass: false,
          reason: { code: "NOT_RECONCILED", summary: "No reconciliation result attached", details: null },
        };
      }
      if (rec.status !== "matched") {
        return {
          pass: false,
          reason: {
            code: rec.status === "arithmetic_mismatch" ? "ARITHMETIC_MISMATCH" : "NOT_RECONCILED",
            summary: `Reconciliation status is ${rec.status}`,
            details: {
              status: rec.status,
              candidates: [...rec.candidates],
              arithmetic: rec.arithmetic as unknown as null,
            },
          },
        };
      }
      return { pass: true };
    },
  };
}

/** Model confidence below the floor is refused regardless of reconciliation. */
export function makeConfidenceFloorRule(min: number): Rule {
  return {
    id: "rule.ledger.confidence_floor",
    jurisdictions: ["GLOBAL"],
    operations: [...OPS],
    evaluate(action: VerifierAction, _context: VerifierContext): RuleResult {
      const claim = (action.inputs as LedgerInputs)?.claim;
      if (!claim) return { pass: true };
      if (claim.confidence < min) {
        return {
          pass: false,
          reason: {
            code: "CONFIDENCE_BELOW_FLOOR",
            summary: `Model confidence ${claim.confidence} below floor ${min}`,
            details: { confidence: claim.confidence, floor: min },
          },
        };
      }
      return { pass: true };
    },
  };
}

/** The standard ledger ruleset. */
export function makeLedgerRules(options: { confidence_floor?: number } = {}): ReadonlyArray<Rule> {
  return [
    makePeriodLockRule(),
    makeAccountCodeRule(),
    makeDuplicateDocumentRule(),
    makeReconciledRule(),
    makeConfidenceFloorRule(options.confidence_floor ?? 0.6),
  ];
}
