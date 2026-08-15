import { appendFile, readFile } from "node:fs/promises";
import { canonicalize, sha256, type JsonValue } from "../envelope.js";

/**
 * The ledger engine boundary.
 *
 * The substrate does not care which general ledger sits underneath. Any
 * system that can (a) present a bank feed and (b) accept a posted entry
 * can implement `LedgerEngine`. The audit chain, the reconciliation
 * engine, the rules, and the material gate are all above this line and
 * identical regardless of what is below it.
 *
 * This file also ships a reference engine — `ContentAddressedLedger` — an
 * append-only JSONL ledger of our own in which every posted entry's id IS
 * the SHA-256 of its canonical bytes. It is the smallest thing that is
 * still a real ledger, it makes the package self-contained, and it is the
 * shape we think a ledger should have: no entry can exist without a
 * replay key.
 */

export const LEDGER_ENGINE_VERSION = "content-addressed-ledger@0.1.0";

/** A bank-feed line as the reconciliation engine consumes it. */
export interface BankLine {
  readonly id: string;
  /** YYYY-MM-DD or null if the feed did not supply one. */
  readonly date: string | null;
  readonly direction: "out" | "in";
  /** Absolute amount, currency units, rounded to 2dp. */
  readonly amount: number;
  readonly currency: string | null;
  readonly counterparty: string | null;
  readonly reference: string | null;
  /** True once a ledger entry has already been matched to this line. */
  readonly reconciled: boolean;
}

export interface LedgerLineItem {
  readonly description: string;
  readonly quantity: number;
  readonly unit_amount: number;
  readonly account_code: string;
  readonly tax_type?: string;
}

/** What the substrate hands to an engine to post. Vendor-neutral. */
export interface LedgerEntry {
  readonly direction: "out" | "in";
  readonly counterparty: string | null;
  /** YYYY-MM-DD. */
  readonly date: string | null;
  readonly currency: string;
  readonly line_items: ReadonlyArray<LedgerLineItem>;
  /** Code of the bank/cash account the movement sits in. */
  readonly bank_account_code: string;
  /** Bank-feed line this entry settles. */
  readonly bank_line_id: string;
  /** Free text; the substrate prefixes it with the source-document hash. */
  readonly reference: string;
  /** SHA-256 of the sealed source document. */
  readonly doc_hash: string;
  /** Total as asserted by the bank feed, not the model. */
  readonly total: number;
}

export interface PostedEntry {
  /** Engine-assigned identifier for the posted entry. */
  readonly entry_id: string;
  readonly posted_at: string;
}

export type LedgerOutcome<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly error: LedgerEngineError };

export interface LedgerEngineError {
  readonly code: "network" | "unauthorized" | "validation" | "duplicate" | "io" | "unknown";
  readonly message: string;
}

export interface LedgerEngine {
  /** Pinned engine identity carried into every envelope, e.g. "content-addressed-ledger@0.1.0". */
  readonly engine_version: string;
  /** Present the (unreconciled and reconciled) bank feed. */
  bankLines(): Promise<LedgerOutcome<ReadonlyArray<BankLine>>>;
  /** Post an entry. Must be idempotent on identical canonical entries. */
  post(entry: LedgerEntry): Promise<LedgerOutcome<PostedEntry>>;
}

/** Deterministic id for an entry: SHA-256 over its canonical JSON. */
export function entryId(entry: LedgerEntry): string {
  return sha256(canonicalize(entry as unknown as JsonValue));
}

interface StoredEntry extends LedgerEntry {
  readonly entry_id: string;
  readonly posted_at: string;
}

/**
 * ContentAddressedLedger — reference engine. JSONL on disk, one entry per
 * line, entry_id = sha256(canonical entry). Posting the same canonical
 * entry twice returns the original (idempotent) rather than duplicating.
 * The bank feed is supplied by the operator (their bank's export) and held
 * in memory; `markReconciled` flips a line once it settles.
 */
export class ContentAddressedLedger implements LedgerEngine {
  readonly engine_version = LEDGER_ENGINE_VERSION;
  private feed: BankLine[];
  private posted = new Map<string, StoredEntry>();
  private loaded = false;

  constructor(
    private readonly path: string,
    feed: ReadonlyArray<BankLine> = [],
  ) {
    this.feed = [...feed];
  }

  private async load(): Promise<void> {
    if (this.loaded) return;
    this.loaded = true;
    try {
      const raw = await readFile(this.path, "utf8");
      for (const line of raw.split("\n").filter((l) => l.length > 0)) {
        const e = JSON.parse(line) as StoredEntry;
        this.posted.set(e.entry_id, e);
        this.feed = this.feed.map((b) => (b.id === e.bank_line_id ? { ...b, reconciled: true } : b));
      }
    } catch (err) {
      if ((err as NodeJS.ErrnoException).code !== "ENOENT") throw err;
    }
  }

  async bankLines(): Promise<LedgerOutcome<ReadonlyArray<BankLine>>> {
    await this.load();
    return { ok: true, value: [...this.feed] };
  }

  async post(entry: LedgerEntry): Promise<LedgerOutcome<PostedEntry>> {
    await this.load();
    const id = entryId(entry);
    const existing = this.posted.get(id);
    if (existing) return { ok: true, value: { entry_id: id, posted_at: existing.posted_at } };
    if (!this.feed.some((b) => b.id === entry.bank_line_id)) {
      return { ok: false, error: { code: "validation", message: `unknown bank line ${entry.bank_line_id}` } };
    }
    const stored: StoredEntry = { ...entry, entry_id: id, posted_at: new Date().toISOString() };
    try {
      await appendFile(this.path, JSON.stringify(stored) + "\n", "utf8");
    } catch (e) {
      return { ok: false, error: { code: "io", message: (e as Error).message } };
    }
    this.posted.set(id, stored);
    this.feed = this.feed.map((b) => (b.id === entry.bank_line_id ? { ...b, reconciled: true } : b));
    return { ok: true, value: { entry_id: id, posted_at: stored.posted_at } };
  }

  /** Every entry on disk, oldest first. Verifies each entry_id against its bytes. */
  static async read(path: string): Promise<{ ok: true; entries: ReadonlyArray<StoredEntry> } | { ok: false; bad_entry_id: string }> {
    const raw = await readFile(path, "utf8").catch(() => "");
    const entries: StoredEntry[] = [];
    for (const line of raw.split("\n").filter((l) => l.length > 0)) {
      const e = JSON.parse(line) as StoredEntry;
      const { entry_id, posted_at: _posted_at, ...body } = e;
      if (entryId(body as LedgerEntry) !== entry_id) return { ok: false, bad_entry_id: entry_id };
      entries.push(e);
    }
    return { ok: true, entries };
  }
}
