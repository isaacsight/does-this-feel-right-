import { mkdir, writeFile, rm, readFile } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { canonicalize, sha256, type JsonValue } from "../envelope.js";
import { RECONCILE_ENGINE_VERSION } from "../ledger/reconcile.js";
import { LEDGER_ENGINE_VERSION } from "../ledger/engine.js";
import { LEDGER_SCHEMA_HASH, LEDGER_POST_MATERIALITY } from "../tools/ledger-post.js";
import { referenceImplementation as ref } from "./reference.js";
import type { ConformanceVector, ConformanceManifest, VectorKind } from "./types.js";
import {
  FIXED_AS_OF, FIXED_APPROVED_AT, FIXED_SESSION, APPROVER, STRANGER,
  DEFAULT_POLICY, WIDE_POLICY, TIGHT_POLICY,
  DOCS, DOC_HASH, CLAIMS, MALFORMED, FEEDS, ENTRIES, CANON, AUDIT_SEQ,
} from "./cases.js";

/**
 * Generate conformance vectors from the case catalogue using the reference
 * implementation. Writes conformance/vectors/v1/<kind>/<id>.json and a
 * manifest with per-file SHA-256 + a suite hash.
 *
 *   npx tsx src/conformance/generate.ts            # write
 *   npx tsx src/conformance/generate.ts --check    # regenerate in memory, diff against disk
 *
 * Every input is JSON-round-tripped BEFORE expected values are computed so
 * the vector on disk and the value the reference saw are identical.
 */

const here = dirname(fileURLToPath(import.meta.url));
const OUT = join(here, "..", "..", "conformance", "vectors", "v1");

const rt = <T>(v: T): T => JSON.parse(JSON.stringify(v)) as T;
const enc = new TextEncoder();

async function build(): Promise<ConformanceVector[]> {
  const V: ConformanceVector[] = [];
  const push = (v: ConformanceVector) => V.push(rt(v));

  // canonicalize
  for (const [id, value] of Object.entries(CANON)) {
    const value_rt = rt(value);
    const canonical = ref.canonicalize(value_rt);
    push({ format_version: 1, kind: "canonicalize", id, description: `canonical JSON + sha256 for ${id}`, input: { value: value_rt }, expected: { canonical, sha256: ref.sha256(canonical) } });
  }

  // source_document
  for (const [id, d] of Object.entries(DOCS)) {
    const r = ref.sealSourceDocument(enc.encode(d.text_utf8));
    push({ format_version: 1, kind: "source_document", id, description: `sha256 over utf8 bytes of ${d.label}`, input: d, expected: r });
  }

  // claim_shape — well-formed and malformed
  for (const [id, claim] of Object.entries(CLAIMS)) {
    const r = ref.validateClaimShape(rt(claim));
    push({ format_version: 1, kind: "claim_shape", id: `ok_${id}`, description: `well-formed claim ${id}`, input: { claim: rt(claim) as unknown as JsonValue }, expected: r.ok ? { ok: true, errors: [] } : { ok: false, errors: [...r.errors].sort() } });
  }
  for (const [id, claim] of Object.entries(MALFORMED)) {
    const c = rt(claim);
    const r = ref.validateClaimShape(c);
    push({ format_version: 1, kind: "claim_shape", id: `bad_${id}`, description: `malformed claim ${id}`, input: { claim: c }, expected: r.ok ? { ok: true, errors: [] } : { ok: false, errors: [...r.errors].sort() } });
  }

  // arithmetic
  const arithCases: Array<[string, string, number]> = [
    ["clean", "clean", 0.01], ["misread_total", "misread_total", 0.01], ["bad_line", "bad_line", 0.01],
    ["three_lines_rounding", "three_lines_rounding", 0.01], ["cents_edge_tol_1c", "cents_edge", 0.01], ["cents_edge_tol_0", "cents_edge", 0],
    ["eur", "eur", 0.01], ["receive", "receive", 0.01], ["fuel", "fuel", 0.01], ["clean_zero_tol", "clean", 0],
  ];
  for (const [id, key, tol] of arithCases) {
    const claim = rt(CLAIMS[key]!);
    push({ format_version: 1, kind: "arithmetic", id, description: `checkArithmetic(${key}, tol=${tol})`, input: { claim, tolerance: tol }, expected: ref.checkArithmetic(claim, tol) });
  }

  // reconcile
  const recCases: Array<[string, string, string, typeof DEFAULT_POLICY]> = [
    ["matched_standard", "clean", "standard", DEFAULT_POLICY],
    ["unmatched_empty_feed", "clean", "empty", DEFAULT_POLICY],
    ["unmatched_fuel_only", "clean", "fuel_only", DEFAULT_POLICY],
    ["ambiguous_two", "clean", "two_candidates", DEFAULT_POLICY],
    ["ambiguous_three_sorted_ids", "clean", "three_candidates_unsorted", DEFAULT_POLICY],
    ["unmatched_already_reconciled", "clean", "reconciled_only", DEFAULT_POLICY],
    ["unmatched_wrong_direction", "clean", "wrong_direction", DEFAULT_POLICY],
    ["unmatched_far_default_window", "clean", "far_only", DEFAULT_POLICY],
    ["matched_far_wide_window", "clean", "far_only", WIDE_POLICY],
    ["matched_line_without_date", "clean", "no_date_line", DEFAULT_POLICY],
    ["matched_claim_without_date", "no_date", "far_only", DEFAULT_POLICY],
    ["matched_line_without_currency", "clean", "no_currency_line", DEFAULT_POLICY],
    ["unmatched_currency_mismatch", "clean", "eur_line", DEFAULT_POLICY],
    ["matched_eur", "eur", "eur_line", DEFAULT_POLICY],
    ["matched_one_cent_within_tol", "clean", "cents", DEFAULT_POLICY],
    ["unmatched_two_cents", "clean", "two_cents", DEFAULT_POLICY],
    ["unmatched_one_cent_zero_tol", "clean", "cents", TIGHT_POLICY],
    ["matched_window_edge_inclusive", "clean", "window_edge", DEFAULT_POLICY],
    ["unmatched_window_past", "clean", "window_past", DEFAULT_POLICY],
    ["matched_window_before_inclusive", "clean", "window_before", DEFAULT_POLICY],
    ["matched_receive_direction", "receive", "receive", DEFAULT_POLICY],
    ["arith_mismatch_short_circuits", "misread_total", "standard", DEFAULT_POLICY],
    ["arith_bad_line_short_circuits", "bad_line", "standard", DEFAULT_POLICY],
    ["matched_rounding_tiny", "three_lines_rounding", "tiny", DEFAULT_POLICY],
    ["matched_mixed_bag_ignores_noise", "clean", "mixed_bag", DEFAULT_POLICY],
    ["matched_fuel", "fuel", "standard", DEFAULT_POLICY],
    ["matched_tight_policy_exact", "clean", "standard", TIGHT_POLICY],
  ];
  for (const [id, ckey, fkey, policy] of recCases) {
    const claim = rt(CLAIMS[ckey]!); const bank_lines = rt(FEEDS[fkey]!); const p = rt(policy);
    push({ format_version: 1, kind: "reconcile", id, description: `reconcile(${ckey}, ${fkey}, ${JSON.stringify(policy)})`, input: { claim, bank_lines, policy: p }, expected: ref.reconcile(claim, bank_lines, p) });
  }

  // reconcile_envelope — the replay key
  for (const [id, ckey, fkey, policy] of recCases.slice(0, 6)) {
    const claim = rt(CLAIMS[ckey]!); const bank_lines = rt(FEEDS[fkey]!); const p = rt(policy);
    const inputs = { claim, bank_lines, policy: p } as unknown as JsonValue;
    const req = { operation: "ledger.reconcile" as const, engine_version: RECONCILE_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, inputs, data_as_of: FIXED_AS_OF };
    push({ format_version: 1, kind: "reconcile_envelope", id, description: `content-addressed envelope for reconcile ${id}`, input: { operation: "ledger.reconcile", engine_version: RECONCILE_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, claim, bank_lines, policy: p, data_as_of: FIXED_AS_OF }, expected: { request_hash: ref.requestHash(req), result: ref.reconcile(claim, bank_lines, p), byte_identical_replayable: true } });
  }
  // same envelope, keys shuffled in inputs → same hash
  {
    const claim = rt(CLAIMS["clean"]!); const bank_lines = rt(FEEDS["standard"]!);
    const shuffled = JSON.parse(JSON.stringify(Object.fromEntries(Object.entries(claim).reverse())));
    const inputs = { policy: DEFAULT_POLICY, bank_lines, claim: shuffled } as unknown as JsonValue;
    const req = { operation: "ledger.reconcile" as const, engine_version: RECONCILE_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, inputs, data_as_of: FIXED_AS_OF };
    push({ format_version: 1, kind: "reconcile_envelope", id: "matched_standard_keys_shuffled", description: "identical logical inputs with different key order → identical request_hash", input: { operation: "ledger.reconcile", engine_version: RECONCILE_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, claim: shuffled, bank_lines, policy: DEFAULT_POLICY, data_as_of: FIXED_AS_OF }, expected: { request_hash: ref.requestHash(req), result: ref.reconcile(claim, bank_lines, DEFAULT_POLICY), byte_identical_replayable: true } });
  }
  // different as-of → different hash (documented as separate vector)
  {
    const claim = rt(CLAIMS["clean"]!); const bank_lines = rt(FEEDS["standard"]!);
    const inputs = { claim, bank_lines, policy: DEFAULT_POLICY } as unknown as JsonValue;
    const as_of = "2026-08-16T00:00:00.000Z";
    const req = { operation: "ledger.reconcile" as const, engine_version: RECONCILE_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, inputs, data_as_of: as_of };
    push({ format_version: 1, kind: "reconcile_envelope", id: "matched_standard_next_day_as_of", description: "same inputs, different data_as_of → different request_hash", input: { operation: "ledger.reconcile", engine_version: RECONCILE_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, claim, bank_lines, policy: DEFAULT_POLICY, data_as_of: as_of }, expected: { request_hash: ref.requestHash(req), result: ref.reconcile(claim, bank_lines, DEFAULT_POLICY), byte_identical_replayable: true } });
  }

  // ledger_rules
  const okState = { valid_account_codes: ["400", "425", "430", "200"], closed_through: "2026-06-30", posted_doc_hashes: [] as string[] };
  const recClean = ref.reconcile(rt(CLAIMS["clean"]!), rt(FEEDS["standard"]!), DEFAULT_POLICY);
  const rulesCases: Array<[string, string, ReturnType<typeof ref.reconcile>, typeof okState | Record<string, unknown>, number, "US" | "EU" | "GLOBAL"]> = [
    ["all_pass", "clean", recClean, okState, 0.6, "US"],
    ["all_pass_eu", "clean", recClean, okState, 0.6, "EU"],
    ["all_pass_global", "clean", recClean, okState, 0.6, "GLOBAL"],
    ["period_locked", "clean", recClean, { ...okState, closed_through: "2026-08-31" }, 0.6, "US"],
    ["period_locked_same_day", "clean", recClean, { ...okState, closed_through: "2026-08-12" }, 0.6, "US"],
    ["period_open_day_after", "clean", recClean, { ...okState, closed_through: "2026-08-11" }, 0.6, "US"],
    ["period_no_lock_configured", "clean", recClean, { valid_account_codes: okState.valid_account_codes }, 0.6, "US"],
    ["unknown_account_code", "unknown_code", recClean, okState, 0.6, "US"],
    ["no_chart_supplied_passes", "unknown_code", recClean, { closed_through: "2026-06-30" }, 0.6, "US"],
    ["duplicate_document", "clean", recClean, { ...okState, posted_doc_hashes: [DOC_HASH.grain_ticket] }, 0.6, "US"],
    ["not_reconciled_empty", "clean", ref.reconcile(rt(CLAIMS["clean"]!), [], DEFAULT_POLICY), okState, 0.6, "US"],
    ["not_reconciled_ambiguous", "clean", ref.reconcile(rt(CLAIMS["clean"]!), rt(FEEDS["two_candidates"]!), DEFAULT_POLICY), okState, 0.6, "US"],
    ["arithmetic_mismatch", "misread_total", ref.reconcile(rt(CLAIMS["misread_total"]!), rt(FEEDS["standard"]!), DEFAULT_POLICY), okState, 0.6, "US"],
    ["confidence_below_floor", "low_confidence", recClean, okState, 0.6, "US"],
    ["confidence_at_floor_passes", "fuel", ref.reconcile(rt(CLAIMS["fuel"]!), rt(FEEDS["standard"]!), DEFAULT_POLICY), okState, 0.71, "US"],
    ["confidence_floor_zero", "low_confidence", recClean, okState, 0, "US"],
    ["multiple_failures", "unknown_code", ref.reconcile(rt(CLAIMS["unknown_code"]!), [], DEFAULT_POLICY), { ...okState, closed_through: "2026-12-31", posted_doc_hashes: [DOC_HASH.grain_ticket] }, 0.99, "US"],
    ["no_date_claim_period_lock_passes", "no_date", ref.reconcile(rt(CLAIMS["no_date"]!), rt(FEEDS["standard"]!), DEFAULT_POLICY), { ...okState, closed_through: "2026-12-31" }, 0.6, "US"],
  ];
  for (const [id, ckey, reconciliation, state, floor, jurisdiction] of rulesCases) {
    const input = rt({ confidence_floor: floor, claim: CLAIMS[ckey]!, reconciliation, state, jurisdiction });
    push({ format_version: 1, kind: "ledger_rules", id, description: `ledger rules: ${id}`, input: input as never, expected: ref.runLedgerRules(input as never) });
  }

  // approval_summary
  for (const [id, ckey, fkey] of [["clean", "clean", "standard"], ["no_vendor_no_date", "no_vendor", "standard"], ["ambiguous", "clean", "two_candidates"], ["receive", "receive", "receive"], ["eur", "eur", "eur_line"]] as const) {
    const claim = rt(CLAIMS[ckey]!); const rec = ref.reconcile(claim, rt(FEEDS[fkey]!), DEFAULT_POLICY);
    push({ format_version: 1, kind: "approval_summary", id, description: `approval summary string for ${id}`, input: { claim, reconciliation: rec }, expected: { summary: ref.approvalSummary(claim, rec) } });
  }

  // approval_token + approval_verify
  const claim = rt(CLAIMS["clean"]!);
  const rec = ref.reconcile(claim, rt(FEEDS["standard"]!), DEFAULT_POLICY);
  const inputs = { claim, reconciliation: rec, reconciliation_request_hash: "0".repeat(64), bank_account_code: "090" } as unknown as JsonValue;
  const postReq = { operation: "ledger.post", engine_version: LEDGER_ENGINE_VERSION, schema_hash: LEDGER_SCHEMA_HASH, inputs, data_as_of: FIXED_AS_OF };
  const request = { request_hash: ref.requestHash(postReq), summary: ref.approvalSummary(claim, rec), session_id: FIXED_SESSION, materiality: LEDGER_POST_MATERIALITY };
  const token = ref.approve(APPROVER.approver_id, APPROVER.secret_utf8, request, FIXED_APPROVED_AT);
  push({ format_version: 1, kind: "approval_token", id: "clean", description: "HMAC-SHA256 token over canonical signing input, fixed approved_at", input: { ...APPROVER, request, approved_at: FIXED_APPROVED_AT }, expected: { token } });
  const token2 = ref.approve(APPROVER.approver_id, APPROVER.secret_utf8, request, "2026-08-15T12:00:01.000Z");
  push({ format_version: 1, kind: "approval_token", id: "clean_one_second_later", description: "different approved_at → different signature", input: { ...APPROVER, request, approved_at: "2026-08-15T12:00:01.000Z" }, expected: { token: token2 } });
  const trusted = [APPROVER];
  const verifyCases: Array<[string, typeof token, typeof trusted, typeof request]> = [
    ["valid", token, trusted, request],
    ["wrong_request_hash", token, trusted, { ...request, request_hash: "f".repeat(64) }],
    ["wrong_session", token, trusted, { ...request, session_id: "other" }],
    ["wrong_materiality", token, trusted, { ...request, materiality: "trade.execute" }],
    ["wrong_summary", token, trusted, { ...request, summary: request.summary + " " }],
    ["unknown_approver", token, [STRANGER], request],
    ["empty_trust_set", token, [], request],
    ["forged_signature", { ...token, signature: "0".repeat(64) }, trusted, request],
    ["short_signature", { ...token, signature: "abcd" }, trusted, request],
    ["wrong_secret", token, [{ approver_id: APPROVER.approver_id, secret_utf8: "different-secret" }], request],
    ["stranger_signs_valid_request", ref.approve(STRANGER.approver_id, STRANGER.secret_utf8, request, FIXED_APPROVED_AT), trusted, request],
    ["approved_at_altered", { ...token, approved_at: "2026-08-15T12:00:01.000Z" }, trusted, request],
  ];
  for (const [id, tok, tr, req] of verifyCases) {
    push({ format_version: 1, kind: "approval_verify", id, description: `verifyApproval: ${id}`, input: { token: rt(tok), trusted: rt(tr), request: rt(req) }, expected: ref.verifyApproval(rt(tok), rt(tr), rt(req)) });
  }

  // ledger_entry_id
  for (const [id, entry] of Object.entries(ENTRIES)) {
    const e = rt(entry);
    push({ format_version: 1, kind: "ledger_entry_id", id, description: `entry_id = sha256(canonical entry) for ${id}`, input: { entry: e }, expected: { entry_id: ref.entryId(e), canonical: canonicalize(e as unknown as JsonValue) } });
  }

  // audit_chain
  {
    const entries = rt(AUDIT_SEQ) as unknown as Parameters<typeof ref.chainAuditEntries>[0];
    const chained = ref.chainAuditEntries(entries);
    const tamper = { seq: 2, payload: { ok: false } as JsonValue };
    const tampered = chained.map((e) => (e.seq === tamper.seq ? { ...e, payload: tamper.payload } : e));
    const v = ref.verifyAuditChain(tampered);
    push({ format_version: 1, kind: "audit_chain", id: "five_entries_tamper_seq_2", description: "hash chain over 5 fixed entries; tampering seq 2 breaks at seq 2", input: { entries, tamper }, expected: { genesis: "0".repeat(64), hashes: chained.map((e) => ({ seq: e.seq, prev_hash: e.prev_hash, self_hash: e.self_hash })), tampered_broken_at_seq: v.ok ? -1 : v.broken_at_seq } });
    // Tamper the first entry → breaks at 0; tamper the last → breaks at last.
    for (const seq of [0, 4]) {
      const t = { seq, payload: { tampered: true } as JsonValue };
      const tt = chained.map((e) => (e.seq === seq ? { ...e, payload: t.payload } : e));
      const vv = ref.verifyAuditChain(tt);
      push({ format_version: 1, kind: "audit_chain", id: `five_entries_tamper_seq_${seq}`, description: `tampering seq ${seq} breaks at seq ${seq}`, input: { entries, tamper: t }, expected: { genesis: "0".repeat(64), hashes: chained.map((e) => ({ seq: e.seq, prev_hash: e.prev_hash, self_hash: e.self_hash })), tampered_broken_at_seq: vv.ok ? -1 : vv.broken_at_seq } });
    }
    // Single-entry chain.
    const one = entries.slice(0, 1);
    const c1 = ref.chainAuditEntries(one);
    const t1 = { seq: 0, payload: {} as JsonValue };
    const v1 = ref.verifyAuditChain(c1.map((e) => ({ ...e, payload: t1.payload })));
    push({ format_version: 1, kind: "audit_chain", id: "single_entry", description: "one entry chains from genesis", input: { entries: one, tamper: t1 }, expected: { genesis: "0".repeat(64), hashes: c1.map((e) => ({ seq: e.seq, prev_hash: e.prev_hash, self_hash: e.self_hash })), tampered_broken_at_seq: v1.ok ? -1 : v1.broken_at_seq } });
  }

  // ledger_post — end to end
  const stdState = { valid_account_codes: ["400", "425", "430", "200"], closed_through: "2026-06-30", posted_doc_hashes: [] as string[] };
  const postBase = { engine_version: LEDGER_ENGINE_VERSION, bank_account_code: "090", data_as_of: FIXED_AS_OF, policy: DEFAULT_POLICY, confidence_floor: 0.6, state: stdState, jurisdiction: "US" as const, session_id: FIXED_SESSION, trusted: [APPROVER], approved_at: FIXED_APPROVED_AT, engine_fails: false };
  const postCases: Array<[string, Partial<typeof postBase> & { claim: JsonValue; bank_lines: ReturnType<typeof rt<typeof FEEDS[string]>>; approval: "none" | "valid" | "wrong_hash" | "unknown_approver" }]> = [
    ["stops_at_gate_without_approval", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "none" }],
    ["posts_with_valid_approval", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid" }],
    ["rejects_wrong_hash_approval", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "wrong_hash" }],
    ["rejects_unknown_approver", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "unknown_approver" }],
    ["arithmetic_mismatch_never_reaches_gate", { claim: rt(CLAIMS["misread_total"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid" }],
    ["unmatched_never_reaches_gate", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["empty"]!), approval: "valid" }],
    ["ambiguous_never_reaches_gate", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["two_candidates"]!), approval: "valid" }],
    ["duplicate_document_refused", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid", state: { ...stdState, posted_doc_hashes: [DOC_HASH.grain_ticket] } }],
    ["period_locked_refused", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid", state: { ...stdState, closed_through: "2026-12-31" } }],
    ["unknown_account_code_refused", { claim: rt(CLAIMS["unknown_code"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid" }],
    ["low_confidence_refused", { claim: rt(CLAIMS["low_confidence"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid" }],
    ["malformed_claim_logs_nothing", { claim: rt(MALFORMED["no_lineage"]!), bank_lines: rt(FEEDS["standard"]!), approval: "none" }],
    ["engine_failure_is_incident", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "valid", engine_fails: true }],
    ["posts_receive", { claim: rt(CLAIMS["receive"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["receive"]!), approval: "valid" }],
    ["posts_eur", { claim: rt(CLAIMS["eur"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["eur_line"]!), approval: "valid" }],
    ["posts_total_from_bank_not_model", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["cents"]!), approval: "valid" }],
    ["different_engine_version_different_hash", { claim: rt(CLAIMS["clean"]!) as unknown as JsonValue, bank_lines: rt(FEEDS["standard"]!), approval: "none", engine_version: "some-other-ledger@9.9.9" }],
  ];
  for (const [id, over] of postCases) {
    const input = rt({ ...postBase, ...over });
    push({ format_version: 1, kind: "ledger_post", id, description: `ledger_post end to end: ${id}`, input: input as never, expected: await ref.ledgerPost(input as never) });
  }

  return V;
}

function fileFor(v: ConformanceVector): string {
  return `${v.kind}/${v.id}.json`;
}

async function main(): Promise<void> {
  const check = process.argv.includes("--check");
  const vectors = await build();
  const files = new Map<string, string>();
  for (const v of vectors) files.set(fileFor(v), JSON.stringify(v, null, 2) + "\n");

  const pkg = JSON.parse(await readFile(join(here, "..", "..", "package.json"), "utf8")) as { name: string; version: string };
  const entries = [...files.entries()].sort(([a], [b]) => (a < b ? -1 : 1)).map(([path, body]) => {
    const v = vectors.find((x) => fileFor(x) === path)!;
    return { path, kind: v.kind as VectorKind, id: v.id, sha256: sha256(body) };
  });
  const manifest: ConformanceManifest = {
    format_version: 1,
    generated_by: "src/conformance/generate.ts",
    reference_versions: { package: `${pkg.name}@${pkg.version}`, reconcile_engine: RECONCILE_ENGINE_VERSION, ledger_engine: LEDGER_ENGINE_VERSION, ledger_schema_hash: LEDGER_SCHEMA_HASH },
    vectors: entries,
    suite_hash: sha256(canonicalize(entries as unknown as JsonValue)),
  };
  const manifestBody = JSON.stringify(manifest, null, 2) + "\n";

  if (check) {
    const onDisk = await readFile(join(OUT, "manifest.json"), "utf8").catch(() => "");
    if (onDisk !== manifestBody) {
      const prev = onDisk ? (JSON.parse(onDisk) as ConformanceManifest) : null;
      console.error(`conformance: manifest drift. on disk suite_hash=${prev?.suite_hash ?? "(none)"} regenerated=${manifest.suite_hash}`);
      if (prev) {
        const a = new Map(prev.vectors.map((v) => [v.path, v.sha256]));
        for (const v of entries) if (a.get(v.path) !== v.sha256) console.error(`  changed: ${v.path}`);
        for (const v of prev.vectors) if (!files.has(v.path)) console.error(`  removed: ${v.path}`);
      }
      process.exit(1);
    }
    console.log(`conformance: ${entries.length} vectors, suite_hash ${manifest.suite_hash} — matches disk`);
    return;
  }

  await rm(OUT, { recursive: true, force: true });
  for (const [path, body] of files) {
    await mkdir(join(OUT, dirname(path)), { recursive: true });
    await writeFile(join(OUT, path), body, "utf8");
  }
  await writeFile(join(OUT, "manifest.json"), manifestBody, "utf8");
  const byKind = entries.reduce<Record<string, number>>((acc, e) => ((acc[e.kind] = (acc[e.kind] ?? 0) + 1), acc), {});
  console.log(`conformance: wrote ${entries.length} vectors to ${OUT}`);
  for (const [k, n] of Object.entries(byKind)) console.log(`  ${k}: ${n}`);
  console.log(`suite_hash ${manifest.suite_hash}`);
}

const invokedDirectly = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (invokedDirectly) {
  main().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}

export { build as buildVectors };
