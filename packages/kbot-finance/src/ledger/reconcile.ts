import type { ExtractionClaim } from "./extraction-claim.js";
import type { BankLine } from "./engine.js";

/**
 * Deterministic reconciliation engine.
 *
 * Takes a model's extraction claim and the bank feed and decides — with
 * arithmetic, not judgement — whether the claim is confirmed. Pure function
 * of its inputs: same claim + same bank lines + same policy = same result,
 * byte for byte. That is what lets the envelope be marked
 * `byte_identical_replayable: true`, and what lets an auditor rerun it.
 *
 * Two independent checks:
 *
 *   1. Arithmetic identity — the document must agree with itself.
 *      sum(line_amount) == subtotal, subtotal + tax == total, and each
 *      line's quantity * unit_amount == line_amount, all within tolerance.
 *      A model that misreads a digit fails here before it touches the bank.
 *
 *   2. Bank-feed match — an unreconciled bank line must exist with the same
 *      direction, an amount within tolerance, and a date within the window.
 *      Exactly one such line = matched. None = unmatched. Several = ambiguous
 *      (the human, not the model, picks).
 */

export const RECONCILE_ENGINE_VERSION = "ledger-reconcile@0.1.0";

export interface ReconcilePolicy {
  /** Absolute tolerance in currency units, e.g. 0.01. */
  readonly amount_tolerance: number;
  /** Days either side of the claimed date a bank line may sit. */
  readonly date_window_days: number;
}

export const DEFAULT_RECONCILE_POLICY: ReconcilePolicy = {
  amount_tolerance: 0.01,
  date_window_days: 5,
};

export interface ArithmeticCheck {
  readonly ok: boolean;
  readonly line_sum: number;
  readonly claimed_subtotal: number;
  readonly claimed_total: number;
  readonly computed_total: number;
  readonly bad_lines: ReadonlyArray<number>;
}

export type ReconcileStatus = "matched" | "unmatched" | "ambiguous" | "arithmetic_mismatch";

export interface ReconcileResult {
  readonly status: ReconcileStatus;
  readonly arithmetic: ArithmeticCheck;
  /** Bank line ids that matched within policy. */
  readonly candidates: ReadonlyArray<string>;
  /** The single confirmed bank line id when status === "matched". */
  readonly matched_bank_line_id: string | null;
  readonly policy: ReconcilePolicy;
}

export function checkArithmetic(claim: ExtractionClaim, tol: number): ArithmeticCheck {
  const bad_lines: number[] = [];
  let line_sum = 0;
  claim.line_items.forEach((li, i) => {
    const expected = li.quantity * li.unit_amount;
    if (Math.abs(expected - li.line_amount) > tol) bad_lines.push(i);
    line_sum += li.line_amount;
  });
  line_sum = round2(line_sum);
  const computed_total = round2(claim.subtotal + claim.tax);
  const ok =
    bad_lines.length === 0 &&
    Math.abs(line_sum - claim.subtotal) <= tol &&
    Math.abs(computed_total - claim.total) <= tol;
  return {
    ok,
    line_sum,
    claimed_subtotal: claim.subtotal,
    claimed_total: claim.total,
    computed_total,
    bad_lines,
  };
}

export function reconcile(
  claim: ExtractionClaim,
  bankLines: ReadonlyArray<BankLine>,
  policy: ReconcilePolicy = DEFAULT_RECONCILE_POLICY,
): ReconcileResult {
  const arithmetic = checkArithmetic(claim, policy.amount_tolerance);
  if (!arithmetic.ok) {
    return { status: "arithmetic_mismatch", arithmetic, candidates: [], matched_bank_line_id: null, policy };
  }

  const claimDay = claim.date ? dayNumber(claim.date) : null;
  const candidates = bankLines
    .filter((l) => !l.reconciled)
    .filter((l) => l.direction === claim.direction)
    .filter((l) => l.currency === null || l.currency === claim.currency)
    .filter((l) => Math.abs(l.amount - claim.total) <= policy.amount_tolerance)
    .filter((l) => {
      if (claimDay === null || l.date === null) return true;
      return Math.abs(dayNumber(l.date) - claimDay) <= policy.date_window_days;
    })
    .map((l) => l.id)
    .sort();

  if (candidates.length === 1) {
    return { status: "matched", arithmetic, candidates, matched_bank_line_id: candidates[0] ?? null, policy };
  }
  if (candidates.length === 0) {
    return { status: "unmatched", arithmetic, candidates, matched_bank_line_id: null, policy };
  }
  return { status: "ambiguous", arithmetic, candidates, matched_bank_line_id: null, policy };
}

/** Whole days since epoch for a YYYY-MM-DD string. Timezone-free by construction. */
export function dayNumber(isoDate: string): number {
  const [y, m, d] = isoDate.split("-").map(Number);
  return Math.floor(Date.UTC(y ?? 1970, (m ?? 1) - 1, d ?? 1) / 86_400_000);
}

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}
