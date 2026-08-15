import { describe, expect, it } from "vitest";
import {
  sealSourceDocument,
  verifySourceDocument,
  validateClaimShape,
  reconcile,
  checkArithmetic,
  dayNumber,
  type ExtractionClaim,
  type BankLine,
} from "../src/ledger/index.js";
import { runVerifier, makeLedgerRules } from "../src/verifier/index.js";

const bytes = new TextEncoder().encode("GRAIN DELIVERY TICKET #4471 — 32.5 t wheat");
const doc = sealSourceDocument(bytes, { mime: "application/pdf", label: "ticket-4471.pdf", captured_at: "2026-08-12T10:00:00.000Z" });

export const goodClaim: ExtractionClaim = {
  doc_hash: doc.doc_hash,
  direction: "out",
  vendor: "Ag Supply Co",
  date: "2026-08-12",
  currency: "USD",
  subtotal: 1200,
  tax: 40.5,
  total: 1240.5,
  line_items: [
    { description: "Urea 46-0-0", quantity: 2, unit_amount: 450, line_amount: 900, account_code: "400" },
    { description: "Delivery", quantity: 1, unit_amount: 300, line_amount: 300, account_code: "425" },
  ],
  reference: "INV-88213",
  confidence: 0.92,
  model_lineage: [{ model: "qwen3.8:27b", version: "ollama-local" }],
};

const bank: BankLine[] = [
  { id: "bt-1", date: "2026-08-13", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  { id: "bt-2", date: "2026-08-13", direction: "out", amount: 88.0, currency: "USD", counterparty: "FUEL", reference: null, reconciled: false },
];

describe("source documents", () => {
  it("hashes deterministically and detects tampering", () => {
    const again = sealSourceDocument(bytes, { mime: "application/pdf", label: "renamed.pdf" });
    expect(again.doc_hash).toBe(doc.doc_hash);
    expect(verifySourceDocument(bytes, doc)).toEqual({ ok: true });
    const tampered = new TextEncoder().encode("GRAIN DELIVERY TICKET #4471 — 33.5 t wheat");
    expect(verifySourceDocument(tampered, doc)).toEqual({ ok: false, reason: "hash_mismatch" });
  });
});

describe("extraction claims", () => {
  it("accepts a well-formed claim and rejects a malformed one", () => {
    expect(validateClaimShape(goodClaim).ok).toBe(true);
    const bad = validateClaimShape({ ...goodClaim, doc_hash: "nope", confidence: 2, model_lineage: [] });
    expect(bad.ok).toBe(false);
    if (!bad.ok) {
      expect(bad.errors).toContain("doc_hash must be sha256 hex");
      expect(bad.errors).toContain("confidence must be in [0,1]");
      expect(bad.errors).toContain("model_lineage required");
    }
  });
});

describe("reconciliation engine", () => {
  it("is deterministic", () => {
    const a = reconcile(goodClaim, bank);
    const b = reconcile(goodClaim, bank);
    expect(JSON.stringify(a)).toBe(JSON.stringify(b));
  });

  it("matches exactly one bank line within tolerance and window", () => {
    const r = reconcile(goodClaim, bank);
    expect(r.status).toBe("matched");
    expect(r.matched_bank_line_id).toBe("bt-1");
  });

  it("fails arithmetic when the model misreads a digit", () => {
    const misread = { ...goodClaim, total: 1204.5 };
    const r = reconcile(misread, bank);
    expect(r.status).toBe("arithmetic_mismatch");
    expect(r.candidates).toEqual([]);
    const arith = checkArithmetic(misread, 0.01);
    expect(arith.computed_total).toBe(1240.5);
    expect(arith.claimed_total).toBe(1204.5);
  });

  it("flags bad line arithmetic", () => {
    const badLine = {
      ...goodClaim,
      line_items: [{ ...goodClaim.line_items[0]!, line_amount: 950 }, goodClaim.line_items[1]!],
    };
    const arith = checkArithmetic(badLine, 0.01);
    expect(arith.ok).toBe(false);
    expect(arith.bad_lines).toEqual([0]);
  });

  it("returns unmatched when the bank has no such line", () => {
    const r = reconcile(goodClaim, [bank[1]!]);
    expect(r.status).toBe("unmatched");
  });

  it("returns ambiguous when two lines fit and never picks one", () => {
    const dup = { ...bank[0]!, id: "bt-9" };
    const r = reconcile(goodClaim, [...bank, dup]);
    expect(r.status).toBe("ambiguous");
    expect(r.candidates).toEqual(["bt-1", "bt-9"]);
    expect(r.matched_bank_line_id).toBeNull();
  });

  it("respects the date window", () => {
    const far = { ...bank[0]!, date: "2026-09-30" };
    expect(reconcile(goodClaim, [far]).status).toBe("unmatched");
    expect(reconcile(goodClaim, [far], { amount_tolerance: 0.01, date_window_days: 60 }).status).toBe("matched");
  });

  it("ignores already-reconciled lines and wrong direction", () => {
    expect(reconcile(goodClaim, [{ ...bank[0]!, reconciled: true }]).status).toBe("unmatched");
    expect(reconcile(goodClaim, [{ ...bank[0]!, direction: "in" }]).status).toBe("unmatched");
  });

  it("dayNumber is timezone-free", () => {
    expect(dayNumber("2026-08-13") - dayNumber("2026-08-12")).toBe(1);
  });
});

describe("ledger verifier rules", () => {
  const rules = makeLedgerRules({ confidence_floor: 0.6 });
  const rec = reconcile(goodClaim, bank);
  const action = (claim: ExtractionClaim, reconciliation = rec) => ({
    operation: "ledger.post",
    inputs: { claim, reconciliation } as never,
    materiality: "material" as const,
  });
  const ctx = (state: Record<string, unknown>) => ({
    session_id: "s",
    state: state as never,
    jurisdiction: "US" as const,
  });

  it("passes a clean, reconciled claim", () => {
    const report = runVerifier(rules, action(goodClaim), ctx({ valid_account_codes: ["400", "425"], closed_through: "2026-06-30", posted_doc_hashes: [] }));
    expect(report.ok).toBe(true);
    expect(report.checks.length).toBe(5);
  });

  const codeOf = (report: ReturnType<typeof runVerifier>, id: string) => {
    const c = report.checks.find((x) => x.rule_id === id)?.result;
    return c && !c.pass ? c.reason.code : null;
  };

  it("PERIOD_LOCKED", () => {
    const r = runVerifier(rules, action(goodClaim), ctx({ closed_through: "2026-08-31" }));
    expect(codeOf(r, "rule.ledger.period_lock")).toBe("PERIOD_LOCKED");
  });
  it("UNKNOWN_ACCOUNT_CODE", () => {
    const r = runVerifier(rules, action(goodClaim), ctx({ valid_account_codes: ["400"] }));
    expect(codeOf(r, "rule.ledger.account_code")).toBe("UNKNOWN_ACCOUNT_CODE");
  });
  it("DUPLICATE_SOURCE_DOCUMENT", () => {
    const r = runVerifier(rules, action(goodClaim), ctx({ posted_doc_hashes: [goodClaim.doc_hash] }));
    expect(codeOf(r, "rule.ledger.duplicate_document")).toBe("DUPLICATE_SOURCE_DOCUMENT");
  });
  it("NOT_RECONCILED / ARITHMETIC_MISMATCH", () => {
    const un = reconcile(goodClaim, []);
    expect(codeOf(runVerifier(rules, action(goodClaim, un), ctx({})), "rule.ledger.reconciled")).toBe("NOT_RECONCILED");
    const bad = reconcile({ ...goodClaim, total: 1 }, bank);
    expect(codeOf(runVerifier(rules, action(goodClaim, bad), ctx({})), "rule.ledger.reconciled")).toBe("ARITHMETIC_MISMATCH");
  });
  it("CONFIDENCE_BELOW_FLOOR", () => {
    const r = runVerifier(rules, action({ ...goodClaim, confidence: 0.3 }), ctx({}));
    expect(codeOf(r, "rule.ledger.confidence_floor")).toBe("CONFIDENCE_BELOW_FLOOR");
  });
});
