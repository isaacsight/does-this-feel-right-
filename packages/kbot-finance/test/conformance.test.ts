import { describe, expect, it } from "vitest";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { runConformance, referenceImplementation } from "../src/conformance/index.js";
import { buildVectors } from "../src/conformance/generate.js";

const DIR = join(dirname(fileURLToPath(import.meta.url)), "..", "conformance", "vectors", "v1");

describe("conformance vectors v1", () => {
  it("reference implementation passes every committed vector and the manifest is intact", async () => {
    const report = await runConformance(DIR, referenceImplementation);
    const failed = report.results.filter((r) => !r.pass);
    expect(failed, JSON.stringify(failed, null, 2)).toEqual([]);
    expect(report.manifest_ok).toBe(true);
    expect(report.total).toBeGreaterThan(100);
  });

  it("regeneration is deterministic: rebuilt vectors equal committed vectors byte for byte", async () => {
    const rebuilt = await buildVectors();
    const { loadVectors } = await import("../src/conformance/run.js");
    const { vectors } = await loadVectors(DIR);
    expect(rebuilt.length).toBe(vectors.length);
    const byPath = new Map(vectors.map((v) => [v.path, v.body]));
    for (const v of rebuilt) {
      const body = JSON.stringify(v, null, 2) + "\n";
      expect(byPath.get(`${v.kind}/${v.id}.json`), `${v.kind}/${v.id}`).toBe(body);
    }
  });

  it("a wrong implementation fails the vectors that pin its behaviour", async () => {
    const broken = {
      ...referenceImplementation,
      // A tempting shortcut: pick the first candidate when ambiguous.
      reconcile: (c: Parameters<typeof referenceImplementation.reconcile>[0], b: Parameters<typeof referenceImplementation.reconcile>[1], p: Parameters<typeof referenceImplementation.reconcile>[2]) => {
        const r = referenceImplementation.reconcile(c, b, p);
        return r.status === "ambiguous" ? { ...r, status: "matched" as const, matched_bank_line_id: r.candidates[0] ?? null } : r;
      },
    };
    const report = await runConformance(DIR, broken);
    const failed = report.results.filter((r) => !r.pass).map((r) => r.path);
    expect(failed).toContain("reconcile/ambiguous_two.json");
    expect(failed).toContain("reconcile/ambiguous_three_sorted_ids.json");
    expect(failed).toContain("reconcile_envelope/ambiguous_two.json");
    // Everything that does not involve ambiguity still passes.
    expect(report.results.filter((r) => r.pass).length).toBeGreaterThan(report.total - 5);
  });

  it("an implementation that forgets to sort keys fails every hash-bearing vector", async () => {
    const unsorted = { ...referenceImplementation, canonicalize: (v: unknown) => JSON.stringify(v) };
    const report = await runConformance(DIR, unsorted);
    const failedKinds = new Set(report.results.filter((r) => !r.pass).map((r) => r.kind));
    expect(failedKinds.has("canonicalize")).toBe(true);
    expect(failedKinds.has("ledger_entry_id")).toBe(true);
  });
});
