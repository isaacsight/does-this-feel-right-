import { describe, expect, it, beforeEach } from "vitest";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { AppendOnlyAuditLog, type AuditEntry } from "../src/audit-log.js";
import { Approver } from "../src/governance.js";
import { makeLedgerRules } from "../src/verifier/index.js";
import { ledgerPost, approvalSummary, LEDGER_POST_MATERIALITY } from "../src/tools/ledger-post.js";
import { reconcile, ContentAddressedLedger, entryId, type BankLine } from "../src/ledger/index.js";
import { goodClaim } from "./ledger.test.js";

const bank: BankLine[] = [
  { id: "bt-1", date: "2026-08-13", direction: "out", amount: 1240.5, currency: "USD", counterparty: "AG SUPPLY", reference: null, reconciled: false },
];

const secret = Buffer.from("accountant-secret-0001");
const trusted = new Map([["cpa.jane", secret]]);
const approver = new Approver("cpa.jane", secret);
const base = { bank_lines: bank, bank_account_code: "090", data_as_of: "2026-08-15T00:00:00Z" };

async function fixture() {
  const dir = await mkdtemp(join(tmpdir(), "ledger-"));
  const auditPath = join(dir, "audit.jsonl");
  const ledgerPath = join(dir, "ledger.jsonl");
  const auditLog = await AppendOnlyAuditLog.open(auditPath);
  const engine = new ContentAddressedLedger(ledgerPath, bank);
  const deps = {
    auditLog,
    rules: makeLedgerRules(),
    verifierContext: {
      session_id: "sess-1",
      state: { valid_account_codes: ["400", "425"], closed_through: "2026-06-30", posted_doc_hashes: [] } as never,
      jurisdiction: "US" as const,
    },
    trustedApprovers: trusted,
    engine,
  };
  return { auditPath, ledgerPath, deps, engine };
}

async function actions(path: string): Promise<string[]> {
  const raw = await readFile(path, "utf8").catch(() => "");
  return raw.split("\n").filter(Boolean).map((l) => (JSON.parse(l) as AuditEntry).action);
}

async function signedToken(f: Awaited<ReturnType<typeof fixture>>) {
  const first = await ledgerPost({ claim: goodClaim, ...base }, f.deps);
  if (first.ok || !first.request_hash) throw new Error("expected approval stage");
  return approver.approve({
    request_hash: first.request_hash,
    summary: approvalSummary(goodClaim, reconcile(goodClaim, bank)),
    session_id: "sess-1",
    materiality: LEDGER_POST_MATERIALITY,
  });
}

describe("ledger_post end to end", () => {
  let f: Awaited<ReturnType<typeof fixture>>;
  beforeEach(async () => {
    f = await fixture();
  });

  it("stops at the material gate without approval and hands back the hash to sign", async () => {
    const r = await ledgerPost({ claim: goodClaim, ...base }, f.deps);
    expect(r.ok).toBe(false);
    if (r.ok) return;
    expect(r.stage).toBe("approval");
    expect(r.request_hash).toMatch(/^[0-9a-f]{64}$/);
    expect((await ContentAddressedLedger.read(f.ledgerPath))).toEqual({ ok: true, entries: [] });
    expect(await actions(f.auditPath)).toEqual(["extraction_claim", "reconciliation", "verifier_check", "approval_denied"]);
  });

  it("posts when a trusted human signs the exact envelope; both chains verify", async () => {
    const token = await signedToken(f);
    const r = await ledgerPost({ claim: goodClaim, ...base, approval: token }, f.deps);
    expect(r.ok).toBe(true);
    if (!r.ok) return;
    expect(r.request_hash).toBe(token.request_hash);
    expect(r.response.value.total).toBe(1240.5);
    expect(r.response.value.matched_bank_line_id).toBe("bt-1");

    const ledger = await ContentAddressedLedger.read(f.ledgerPath);
    expect(ledger.ok).toBe(true);
    if (!ledger.ok) return;
    expect(ledger.entries.length).toBe(1);
    const e = ledger.entries[0]!;
    expect(e.entry_id).toBe(r.response.value.entry_id);
    expect(e.reference).toContain(`doc:${goodClaim.doc_hash.slice(0, 16)}`);
    expect(e.doc_hash).toBe(goodClaim.doc_hash);
    expect(e.total).toBe(1240.5);
    expect(e.line_items.length).toBe(2);
    // The engine's id is the hash of the entry's own bytes.
    const { entry_id, posted_at: _p, ...body } = e;
    expect(entryId(body)).toBe(entry_id);

    const tail = (await actions(f.auditPath)).slice(-6);
    expect(tail).toEqual(["extraction_claim", "reconciliation", "verifier_check", "approval_granted", "engine_request", "engine_response"]);
    expect(await AppendOnlyAuditLog.verify(f.auditPath)).toEqual({ ok: true });

    // The bank line is now reconciled in the engine's feed.
    const feed = await f.engine.bankLines();
    expect(feed.ok && feed.value[0]?.reconciled).toBe(true);
  });

  it("is idempotent: reposting the same canonical entry does not duplicate", async () => {
    const token = await signedToken(f);
    const a = await ledgerPost({ claim: goodClaim, ...base, approval: token }, f.deps);
    const b = await ledgerPost({ claim: goodClaim, ...base, approval: token }, f.deps);
    expect(a.ok && b.ok).toBe(true);
    if (!a.ok || !b.ok) return;
    expect(b.response.value.entry_id).toBe(a.response.value.entry_id);
    const ledger = await ContentAddressedLedger.read(f.ledgerPath);
    expect(ledger.ok && ledger.entries.length).toBe(1);
  });

  it("rejects an approval signed for a different envelope", async () => {
    const forged = approver.approve({ request_hash: "f".repeat(64), summary: "something else", session_id: "sess-1", materiality: LEDGER_POST_MATERIALITY });
    const r = await ledgerPost({ claim: goodClaim, ...base, approval: forged }, f.deps);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.detail).toEqual({ reason: "request_hash_mismatch" });
    expect((await ContentAddressedLedger.read(f.ledgerPath))).toEqual({ ok: true, entries: [] });
  });

  it("rejects an approver outside the trust set", async () => {
    const first = await ledgerPost({ claim: goodClaim, ...base }, f.deps);
    if (first.ok || !first.request_hash) throw new Error("expected approval stage");
    const stranger = new Approver("intern.bob", Buffer.from("x"));
    const token = stranger.approve({ request_hash: first.request_hash, summary: approvalSummary(goodClaim, reconcile(goodClaim, bank)), session_id: "sess-1", materiality: LEDGER_POST_MATERIALITY });
    const r = await ledgerPost({ claim: goodClaim, ...base, approval: token }, f.deps);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.detail).toEqual({ reason: "unknown_approver" });
  });

  it("never reaches the engine when the model misread the total", async () => {
    const r = await ledgerPost({ claim: { ...goodClaim, total: 1204.5 }, ...base }, f.deps);
    expect(r.ok).toBe(false);
    if (!r.ok) {
      expect(r.stage).toBe("reconciliation");
      expect(r.reconciliation?.status).toBe("arithmetic_mismatch");
    }
    expect((await ContentAddressedLedger.read(f.ledgerPath))).toEqual({ ok: true, entries: [] });
  });

  it("refuses a duplicate source document even with a valid approval", async () => {
    const deps = { ...f.deps, verifierContext: { ...f.deps.verifierContext, state: { valid_account_codes: ["400", "425"], posted_doc_hashes: [goodClaim.doc_hash] } as never } };
    const r = await ledgerPost({ claim: goodClaim, ...base }, deps);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.stage).toBe("verifier");
  });

  it("rejects malformed claims before anything is logged", async () => {
    const r = await ledgerPost({ claim: { ...goodClaim, model_lineage: [] }, ...base }, f.deps);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.stage).toBe("claim_shape");
    expect(await actions(f.auditPath)).toEqual([]);
  });

  it("surfaces engine failures as incidents", async () => {
    const token = await signedToken(f);
    const failing = { engine_version: "broken@0", bankLines: f.engine.bankLines.bind(f.engine), post: async () => ({ ok: false as const, error: { code: "network" as const, message: "down" } }) };
    // Different engine_version changes the request hash, so re-sign.
    const deps = { ...f.deps, engine: failing };
    const first = await ledgerPost({ claim: goodClaim, ...base }, deps);
    if (first.ok || !first.request_hash) throw new Error("expected approval stage");
    const tok2 = approver.approve({ ...token, request_hash: first.request_hash });
    const r = await ledgerPost({ claim: goodClaim, ...base, approval: tok2 }, deps);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.stage).toBe("engine");
    expect((await actions(f.auditPath)).at(-1)).toBe("incident");
  });
});

describe("ContentAddressedLedger integrity", () => {
  it("detects a tampered entry on read", async () => {
    const dir = await mkdtemp(join(tmpdir(), "ledger-"));
    const path = join(dir, "ledger.jsonl");
    const engine = new ContentAddressedLedger(path, bank);
    const r = await engine.post({
      direction: "out", counterparty: "X", date: "2026-08-13", currency: "USD",
      line_items: [{ description: "d", quantity: 1, unit_amount: 1240.5, account_code: "400" }],
      bank_account_code: "090", bank_line_id: "bt-1", reference: "r", doc_hash: goodClaim.doc_hash, total: 1240.5,
    });
    expect(r.ok).toBe(true);
    const { writeFile } = await import("node:fs/promises");
    const raw = await readFile(path, "utf8");
    await writeFile(path, raw.replace('"total":1240.5', '"total":1204.5'));
    const read = await ContentAddressedLedger.read(path);
    expect(read.ok).toBe(false);
  });
});
