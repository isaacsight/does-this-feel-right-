import type { ExtractionClaim } from "../ledger/extraction-claim.js";
import type { BankLine, LedgerEntry } from "../ledger/engine.js";
import type { ReconcilePolicy } from "../ledger/reconcile.js";
import { sealSourceDocument } from "../ledger/source-document.js";
import type { JsonValue } from "../envelope.js";

/**
 * The case catalogue. Inputs only — expected values are computed by
 * generate.ts from the reference implementation. Every fixture here is
 * fixed: no clocks, no randomness. Change a case → regenerate → the
 * manifest's suite_hash changes, and that is the signal.
 */

export const FIXED_AS_OF = "2026-08-15T00:00:00.000Z";
export const FIXED_APPROVED_AT = "2026-08-15T12:00:00.000Z";
export const FIXED_SESSION = "conformance-session";
export const APPROVER = { approver_id: "cpa.jane", secret_utf8: "conformance-approver-secret-0001" };
export const STRANGER = { approver_id: "intern.bob", secret_utf8: "not-in-the-trust-set" };

export const DEFAULT_POLICY: ReconcilePolicy = { amount_tolerance: 0.01, date_window_days: 5 };
export const WIDE_POLICY: ReconcilePolicy = { amount_tolerance: 0.5, date_window_days: 60 };
export const TIGHT_POLICY: ReconcilePolicy = { amount_tolerance: 0, date_window_days: 0 };

// ---------------------------------------------------------------- documents

export const DOCS = {
  grain_ticket: { text_utf8: "GRAIN DELIVERY TICKET #4471 — 32.5 t wheat — Ag Supply Co — 2026-08-12", mime: "application/pdf", label: "ticket-4471.pdf" },
  fuel_receipt: { text_utf8: "FUEL 88.00 USD 2026-08-13 pump 3", mime: "image/jpeg", label: "fuel-0813.jpg" },
  empty: { text_utf8: "", mime: "application/octet-stream", label: "empty.bin" },
  unicode: { text_utf8: "Facture n° 12 — café ☕ — 1 240,50 €", mime: "text/plain", label: "facture-12.txt" },
  grain_ticket_tampered: { text_utf8: "GRAIN DELIVERY TICKET #4471 — 33.5 t wheat — Ag Supply Co — 2026-08-12", mime: "application/pdf", label: "ticket-4471.pdf" },
} as const;

const enc = new TextEncoder();
export const DOC_HASH = Object.fromEntries(
  Object.entries(DOCS).map(([k, d]) => [k, sealSourceDocument(enc.encode(d.text_utf8), { mime: d.mime, label: d.label, captured_at: FIXED_AS_OF }).doc_hash]),
) as Record<keyof typeof DOCS, string>;

// ------------------------------------------------------------------- claims

export const CLAIMS: Record<string, ExtractionClaim> = {
  clean: {
    doc_hash: DOC_HASH.grain_ticket,
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
    model_lineage: [{ model: "local-27b", version: "conformance" }],
  },
  misread_total: {} as ExtractionClaim, // filled below
  bad_line: {} as ExtractionClaim,
  no_date: {} as ExtractionClaim,
  no_vendor: {} as ExtractionClaim,
  low_confidence: {} as ExtractionClaim,
  receive: {} as ExtractionClaim,
  eur: {} as ExtractionClaim,
  cents_edge: {} as ExtractionClaim,
  fuel: {} as ExtractionClaim,
  three_lines_rounding: {} as ExtractionClaim,
  tax_type: {} as ExtractionClaim,
  unknown_code: {} as ExtractionClaim,
};

const clean = CLAIMS["clean"]!;
CLAIMS["misread_total"] = { ...clean, total: 1204.5 };
CLAIMS["bad_line"] = { ...clean, line_items: [{ ...clean.line_items[0]!, line_amount: 950 }, clean.line_items[1]!] };
CLAIMS["no_date"] = { ...clean, date: null };
CLAIMS["no_vendor"] = { ...clean, vendor: null, reference: null };
CLAIMS["low_confidence"] = { ...clean, confidence: 0.3 };
CLAIMS["receive"] = {
  ...clean,
  direction: "in",
  vendor: "Grain Buyer Ltd",
  subtotal: 9750,
  tax: 0,
  total: 9750,
  line_items: [{ description: "Wheat 32.5t @ 300", quantity: 32.5, unit_amount: 300, line_amount: 9750, account_code: "200" }],
  reference: "RCT-2201",
};
CLAIMS["eur"] = {
  ...clean,
  doc_hash: DOC_HASH.unicode,
  vendor: "Café Fournisseur",
  currency: "EUR",
  subtotal: 1033.75,
  tax: 206.75,
  total: 1240.5,
  line_items: [{ description: "Café — 25 kg", quantity: 25, unit_amount: 41.35, line_amount: 1033.75, account_code: "400" }],
  reference: "F-12",
};
// 0.1 + 0.2 territory: three lines that only sum correctly with rounding.
CLAIMS["three_lines_rounding"] = {
  ...clean,
  subtotal: 0.3,
  tax: 0,
  total: 0.3,
  line_items: [
    { description: "a", quantity: 1, unit_amount: 0.1, line_amount: 0.1, account_code: "400" },
    { description: "b", quantity: 1, unit_amount: 0.1, line_amount: 0.1, account_code: "400" },
    { description: "c", quantity: 1, unit_amount: 0.1, line_amount: 0.1, account_code: "400" },
  ],
  reference: null,
};
// Exactly at tolerance boundary: line 3 * 33.33 = 99.99, claimed 100.00 → off by 0.01.
CLAIMS["cents_edge"] = {
  ...clean,
  subtotal: 100,
  tax: 0,
  total: 100,
  line_items: [{ description: "edge", quantity: 3, unit_amount: 33.33, line_amount: 100, account_code: "400" }],
  reference: null,
};
CLAIMS["fuel"] = {
  ...clean,
  doc_hash: DOC_HASH.fuel_receipt,
  vendor: "Pump 3",
  date: "2026-08-13",
  subtotal: 80,
  tax: 8,
  total: 88,
  line_items: [{ description: "Diesel", quantity: 40, unit_amount: 2, line_amount: 80, account_code: "430" }],
  reference: null,
  confidence: 0.71,
};
CLAIMS["tax_type"] = {
  ...clean,
  line_items: clean.line_items.map((l) => ({ ...l, tax_type: "INPUT" })),
};
CLAIMS["unknown_code"] = { ...clean, line_items: [{ ...clean.line_items[0]!, account_code: "999" }, clean.line_items[1]!] };

// -------------------------------------------------------- malformed claims

export const MALFORMED: Record<string, JsonValue> = {
  not_object: "nope",
  null_claim: null,
  bad_hash: { ...(clean as unknown as Record<string, JsonValue>), doc_hash: "nope" },
  bad_direction: { ...(clean as unknown as Record<string, JsonValue>), direction: "sideways" },
  bad_currency: { ...(clean as unknown as Record<string, JsonValue>), currency: "US" },
  nan_total: { ...(clean as unknown as Record<string, JsonValue>), total: "1240.50" },
  empty_lines: { ...(clean as unknown as Record<string, JsonValue>), line_items: [] },
  line_missing_code: { ...(clean as unknown as Record<string, JsonValue>), line_items: [{ description: "x", quantity: 1, unit_amount: 1, line_amount: 1 }] },
  confidence_over: { ...(clean as unknown as Record<string, JsonValue>), confidence: 1.5 },
  no_lineage: { ...(clean as unknown as Record<string, JsonValue>), model_lineage: [] },
  bad_date: { ...(clean as unknown as Record<string, JsonValue>), date: "12/08/2026" },
  everything_wrong: { doc_hash: 1, direction: "x", currency: "", subtotal: "a", tax: null, total: NaN as unknown as number, line_items: "no", confidence: -1, model_lineage: "none", date: 20260812 } as unknown as JsonValue,
};

// --------------------------------------------------------------- bank feeds

export const BANK: Record<string, BankLine> = {
  match_out: { id: "bt-1", date: "2026-08-13", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  fuel_out: { id: "bt-2", date: "2026-08-13", direction: "out", amount: 88.0, currency: "USD", counterparty: "FUEL", reference: null, reconciled: false },
  match_out_dup: { id: "bt-9", date: "2026-08-14", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  match_out_reconciled: { id: "bt-1r", date: "2026-08-13", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: true },
  match_in: { id: "bt-3", date: "2026-08-12", direction: "in", amount: 1240.5, currency: "USD", counterparty: "SOMEONE", reference: null, reconciled: false },
  match_out_far: { id: "bt-4", date: "2026-09-30", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  match_out_no_date: { id: "bt-5", date: null, direction: "out", amount: 1240.5, currency: "USD", counterparty: null, reference: null, reconciled: false },
  match_out_no_currency: { id: "bt-6", date: "2026-08-13", direction: "out", amount: 1240.5, currency: null, counterparty: null, reference: null, reconciled: false },
  match_out_eur: { id: "bt-7", date: "2026-08-13", direction: "out", amount: 1240.5, currency: "EUR", counterparty: "CAFE", reference: null, reconciled: false },
  off_by_one_cent: { id: "bt-8", date: "2026-08-13", direction: "out", amount: 1240.51, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  off_by_two_cents: { id: "bt-10", date: "2026-08-13", direction: "out", amount: 1240.52, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  edge_of_window: { id: "bt-11", date: "2026-08-17", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  past_window: { id: "bt-12", date: "2026-08-18", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  before_window: { id: "bt-13", date: "2026-08-07", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
  receive_in: { id: "bt-14", date: "2026-08-12", direction: "in", amount: 9750, currency: "USD", counterparty: "GRAIN BUYER", reference: "RCT-2201", reconciled: false },
  tiny: { id: "bt-15", date: "2026-08-12", direction: "out", amount: 0.3, currency: "USD", counterparty: null, reference: null, reconciled: false },
};

const B = BANK;
export const FEEDS: Record<string, ReadonlyArray<BankLine>> = {
  standard: [B["match_out"]!, B["fuel_out"]!],
  empty: [],
  fuel_only: [B["fuel_out"]!],
  two_candidates: [B["match_out"]!, B["fuel_out"]!, B["match_out_dup"]!],
  three_candidates_unsorted: [B["match_out_dup"]!, B["match_out"]!, { ...B["match_out"]!, id: "bt-0" }],
  reconciled_only: [B["match_out_reconciled"]!],
  wrong_direction: [B["match_in"]!],
  far_only: [B["match_out_far"]!],
  no_date_line: [B["match_out_no_date"]!],
  no_currency_line: [B["match_out_no_currency"]!],
  eur_line: [B["match_out_eur"]!],
  cents: [B["off_by_one_cent"]!],
  two_cents: [B["off_by_two_cents"]!],
  window_edge: [B["edge_of_window"]!],
  window_past: [B["past_window"]!],
  window_before: [B["before_window"]!],
  receive: [B["receive_in"]!, B["match_out"]!],
  tiny: [B["tiny"]!],
  mixed_bag: [B["match_out"]!, B["match_out_reconciled"]!, B["match_in"]!, B["match_out_far"]!, B["fuel_out"]!],
};

// ------------------------------------------------------------ ledger entry

export const ENTRIES: Record<string, LedgerEntry> = {
  clean: {
    direction: "out",
    counterparty: "Ag Supply Co",
    date: "2026-08-13",
    currency: "USD",
    line_items: [
      { description: "Urea 46-0-0", quantity: 2, unit_amount: 450, account_code: "400" },
      { description: "Delivery", quantity: 1, unit_amount: 300, account_code: "425" },
    ],
    bank_account_code: "090",
    bank_line_id: "bt-1",
    reference: `doc:${DOC_HASH.grain_ticket.slice(0, 16)} INV-88213`,
    doc_hash: DOC_HASH.grain_ticket,
    total: 1240.5,
  },
};
ENTRIES["clean_keys_shuffled"] = JSON.parse(
  JSON.stringify(Object.fromEntries(Object.entries(ENTRIES["clean"]!).reverse())),
) as LedgerEntry;
ENTRIES["clean_with_tax_type"] = {
  ...ENTRIES["clean"]!,
  line_items: ENTRIES["clean"]!.line_items.map((l) => ({ ...l, tax_type: "INPUT" })),
};
ENTRIES["clean_total_off"] = { ...ENTRIES["clean"]!, total: 1204.5 };

// ---------------------------------------------------------- canonicalize

export const CANON: Record<string, JsonValue> = {
  key_order: { b: 1, a: 2 },
  nested: { z: { c: 1, a: [3, 1, { y: null, x: true }] }, a: "s" },
  numbers: { i: 1, f: 1.5, neg: -0.25, big: 1e21, small: 1e-7, zero: 0, negzero: -0 },
  strings: { q: 'he said "hi"', nl: "a\nb", uni: "café ☕", esc: "\\" },
  empty: { arr: [], obj: {}, str: "" },
  claim: clean as unknown as JsonValue,
};

// ------------------------------------------------------------ audit chain

export const AUDIT_SEQ = [
  { action: "extraction_claim", subject: "ledger.extract", session_id: FIXED_SESSION, timestamp: "2026-08-15T00:00:01.000Z", model_lineage: [{ model: "local-27b", version: "conformance" }], payload: clean as unknown as JsonValue },
  { action: "reconciliation", subject: "ledger.reconcile", session_id: FIXED_SESSION, timestamp: "2026-08-15T00:00:02.000Z", payload: { status: "matched" } },
  { action: "verifier_check", subject: "ledger.post", session_id: FIXED_SESSION, timestamp: "2026-08-15T00:00:03.000Z", payload: { ok: true } },
  { action: "approval_granted", subject: "ledger.post", session_id: FIXED_SESSION, timestamp: "2026-08-15T00:00:04.000Z", approver: APPROVER.approver_id, payload: { request_hash: "0".repeat(64) } },
  { action: "engine_response", subject: "ledger.post", session_id: FIXED_SESSION, timestamp: "2026-08-15T00:00:05.000Z", payload: { entry_id: "abc" } },
] as const;
