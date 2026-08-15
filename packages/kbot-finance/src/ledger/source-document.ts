import { createHash } from "node:crypto";

/**
 * Content-addressed source documents.
 *
 * A source document — a supplier invoice, a grain delivery ticket, a
 * fuel receipt, a bank statement page — is the evidence a ledger entry
 * rests on. Before any model reads it, we hash the bytes. The hash is
 * carried in every downstream envelope, so:
 *
 *   - two operators extracting from the same bytes produce the same
 *     replay key;
 *   - a document altered after extraction is detectable;
 *   - the same document cannot be posted twice without tripping the
 *     duplicate-document rule.
 *
 * The bytes themselves stay with the operator. Only the hash travels.
 */

export interface SourceDocument {
  /** SHA-256 hex over the raw bytes. */
  readonly doc_hash: string;
  readonly byte_length: number;
  /** MIME type as supplied by the capture path; not sniffed. */
  readonly mime: string;
  /** Operator-supplied label, e.g. "grain-ticket-2026-08-12.pdf". Not hashed. */
  readonly label: string;
  /** ISO 8601 UTC time the bytes were sealed. */
  readonly captured_at: string;
}

export function sealSourceDocument(
  bytes: Uint8Array,
  meta: { readonly mime: string; readonly label: string; readonly captured_at?: string },
): SourceDocument {
  const doc_hash = createHash("sha256").update(bytes).digest("hex");
  return {
    doc_hash,
    byte_length: bytes.byteLength,
    mime: meta.mime,
    label: meta.label,
    captured_at: meta.captured_at ?? new Date().toISOString(),
  };
}

/** Recompute the hash of bytes and compare to a sealed document. */
export function verifySourceDocument(
  bytes: Uint8Array,
  doc: SourceDocument,
): { ok: true } | { ok: false; reason: "hash_mismatch" | "length_mismatch" } {
  if (bytes.byteLength !== doc.byte_length) return { ok: false, reason: "length_mismatch" };
  const h = createHash("sha256").update(bytes).digest("hex");
  if (h !== doc.doc_hash) return { ok: false, reason: "hash_mismatch" };
  return { ok: true };
}
