import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";
import { canonicalize, sha256, type JsonValue } from "../envelope.js";
import type { ConformanceImplementation } from "./implementation.js";
import type { ConformanceManifest, ConformanceVector } from "./types.js";

/**
 * Conformance runner. Point it at a vectors directory and an implementation;
 * it returns one result per vector. The reference passes all of them; a
 * port passes the kinds it claims to support.
 *
 * Comparison rules per kind (see types.ts):
 *   - hashes / signatures / canonical strings: exact string equality
 *   - structured results: JSON-equal after canonicalization (key order ignored)
 */

export interface VectorResult {
  readonly path: string;
  readonly kind: ConformanceVector["kind"];
  readonly id: string;
  readonly pass: boolean;
  readonly detail?: string;
}

export interface ConformanceReport {
  readonly suite_hash: string;
  readonly manifest_ok: boolean;
  readonly total: number;
  readonly passed: number;
  readonly results: ReadonlyArray<VectorResult>;
}

const enc = new TextEncoder();
const eq = (a: unknown, b: unknown): boolean =>
  canonicalize(a as JsonValue) === canonicalize(b as JsonValue);
const fail = (detail: string): { pass: false; detail: string } => ({ pass: false, detail });
const ok = (): { pass: true } => ({ pass: true });

export async function evaluateVector(
  v: ConformanceVector,
  impl: ConformanceImplementation,
): Promise<{ pass: boolean; detail?: string }> {
  try {
    switch (v.kind) {
      case "canonicalize": {
        const c = impl.canonicalize(v.input.value);
        if (c !== v.expected.canonical) return fail(`canonical mismatch: ${c}`);
        const h = impl.sha256(c);
        return h === v.expected.sha256 ? ok() : fail(`sha256 mismatch: ${h}`);
      }
      case "source_document": {
        const r = impl.sealSourceDocument(enc.encode(v.input.text_utf8));
        return eq(r, v.expected) ? ok() : fail(JSON.stringify(r));
      }
      case "claim_shape": {
        const r = impl.validateClaimShape(v.input.claim);
        const got = r.ok ? { ok: true, errors: [] } : { ok: false, errors: [...r.errors].sort() };
        return eq(got, v.expected) ? ok() : fail(JSON.stringify(got));
      }
      case "arithmetic": {
        const r = impl.checkArithmetic(v.input.claim, v.input.tolerance);
        return eq(r, v.expected) ? ok() : fail(JSON.stringify(r));
      }
      case "reconcile": {
        const r = impl.reconcile(v.input.claim, v.input.bank_lines, v.input.policy);
        return eq(r, v.expected) ? ok() : fail(JSON.stringify(r));
      }
      case "reconcile_envelope": {
        const { operation, engine_version, schema_hash, claim, bank_lines, policy, data_as_of } = v.input;
        const h = impl.requestHash({ operation, engine_version, schema_hash, inputs: { claim, bank_lines, policy } as unknown as JsonValue, data_as_of });
        if (h !== v.expected.request_hash) return fail(`request_hash mismatch: ${h}`);
        const r = impl.reconcile(claim, bank_lines, policy);
        return eq(r, v.expected.result) ? ok() : fail(JSON.stringify(r));
      }
      case "ledger_rules": {
        const r = impl.runLedgerRules(v.input);
        return eq(r, v.expected) ? ok() : fail(JSON.stringify(r));
      }
      case "approval_summary": {
        const s = impl.approvalSummary(v.input.claim, v.input.reconciliation);
        return s === v.expected.summary ? ok() : fail(s);
      }
      case "approval_token": {
        const t = impl.approve(v.input.approver_id, v.input.secret_utf8, v.input.request, v.input.approved_at);
        return eq(t, v.expected.token) ? ok() : fail(JSON.stringify(t));
      }
      case "approval_verify": {
        const r = impl.verifyApproval(v.input.token, v.input.trusted, v.input.request);
        return eq(r, v.expected) ? ok() : fail(JSON.stringify(r));
      }
      case "ledger_entry_id": {
        const id = impl.entryId(v.input.entry);
        if (id !== v.expected.entry_id) return fail(`entry_id mismatch: ${id}`);
        const c = impl.canonicalize(v.input.entry as unknown as JsonValue);
        return c === v.expected.canonical ? ok() : fail(`canonical mismatch`);
      }
      case "audit_chain": {
        const chained = impl.chainAuditEntries(v.input.entries as never);
        const hashes = chained.map((e) => ({ seq: e.seq, prev_hash: e.prev_hash, self_hash: e.self_hash }));
        if (!eq(hashes, v.expected.hashes)) return fail(JSON.stringify(hashes));
        if (chained[0]?.prev_hash !== v.expected.genesis) return fail("genesis mismatch");
        const intact = impl.verifyAuditChain(chained);
        if (!intact.ok) return fail(`intact chain reported broken at ${intact.broken_at_seq}`);
        const tampered = chained.map((e) => (e.seq === v.input.tamper.seq ? { ...e, payload: v.input.tamper.payload } : e));
        const r = impl.verifyAuditChain(tampered);
        const broken = r.ok ? -1 : r.broken_at_seq;
        return broken === v.expected.tampered_broken_at_seq ? ok() : fail(`tamper detected at ${broken}`);
      }
      case "ledger_post": {
        const r = await impl.ledgerPost(v.input);
        return eq(r, v.expected) ? ok() : fail(JSON.stringify(r));
      }
      default: {
        const never: never = v;
        return fail(`unknown kind ${(never as { kind: string }).kind}`);
      }
    }
  } catch (e) {
    return fail(`threw: ${(e as Error).message}`);
  }
}

export async function loadVectors(dir: string): Promise<{ manifest: ConformanceManifest; vectors: Array<{ path: string; body: string; vector: ConformanceVector }> }> {
  const manifest = JSON.parse(await readFile(join(dir, "manifest.json"), "utf8")) as ConformanceManifest;
  const out: Array<{ path: string; body: string; vector: ConformanceVector }> = [];
  for (const kind of await readdir(dir, { withFileTypes: true })) {
    if (!kind.isDirectory()) continue;
    for (const f of await readdir(join(dir, kind.name))) {
      if (!f.endsWith(".json")) continue;
      const path = `${kind.name}/${f}`;
      const body = await readFile(join(dir, path), "utf8");
      out.push({ path, body, vector: JSON.parse(body) as ConformanceVector });
    }
  }
  out.sort((a, b) => (a.path < b.path ? -1 : 1));
  return { manifest, vectors: out };
}

export async function runConformance(dir: string, impl: ConformanceImplementation): Promise<ConformanceReport> {
  const { manifest, vectors } = await loadVectors(dir);
  const manifestEntries = new Map(manifest.vectors.map((m) => [m.path, m.sha256]));
  let manifest_ok = manifest.vectors.length === vectors.length;
  const results: VectorResult[] = [];
  for (const { path, body, vector } of vectors) {
    if (manifestEntries.get(path) !== sha256(body)) manifest_ok = false;
    const r = await evaluateVector(vector, impl);
    results.push({ path, kind: vector.kind, id: vector.id, pass: r.pass, ...(r.detail !== undefined ? { detail: r.detail } : {}) });
  }
  return { suite_hash: manifest.suite_hash, manifest_ok, total: results.length, passed: results.filter((r) => r.pass).length, results };
}
