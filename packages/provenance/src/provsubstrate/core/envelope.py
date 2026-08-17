"""Content-addressed request envelopes.

The single load-bearing primitive. Every deterministic-engine call resolves
to a SHA-256 over its canonicalized inputs; identical hash, identical result.
The model layer cannot produce a number, a proof, or a claim verdict — it can
only *request* one inside an envelope, and the envelope is what an auditor,
a referee, or a reviewer replays.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Optional

from .canonical import JsonValue, canonicalize


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def content_hash(value: JsonValue) -> str:
    """SHA-256 of the canonical JSON of ``value``."""
    return sha256_text(canonicalize(value))


@dataclass(frozen=True)
class ContentAddressedRequest:
    operation: str
    engine_version: str
    schema_hash: str
    inputs: JsonValue
    data_as_of: str
    deterministic_seed: Optional[str] = None

    def hashable(self) -> dict:
        h: dict[str, Any] = {
            "operation": self.operation,
            "engine_version": self.engine_version,
            "schema_hash": self.schema_hash,
            "inputs": self.inputs,
            "data_as_of": self.data_as_of,
        }
        if self.deterministic_seed is not None:
            h["deterministic_seed"] = self.deterministic_seed
        return h

    def request_hash(self) -> str:
        return content_hash(self.hashable())


def request_hash(
    *, operation: str, engine_version: str, schema_hash: str, inputs: JsonValue, data_as_of: str, deterministic_seed: Optional[str] = None
) -> str:
    return ContentAddressedRequest(operation, engine_version, schema_hash, inputs, data_as_of, deterministic_seed).request_hash()


@dataclass(frozen=True)
class ContentAddressedResponse:
    request_hash: str
    engine_version: str
    produced_at: str
    byte_identical_replayable: bool
    value: JsonValue

    def to_json(self) -> dict:
        return {
            "request_hash": self.request_hash,
            "engine_version": self.engine_version,
            "produced_at": self.produced_at,
            "byte_identical_replayable": self.byte_identical_replayable,
            "value": self.value,
        }


def seal_envelope(request: ContentAddressedRequest, engine, *, produced_at: str, byte_identical_replayable: bool = False) -> ContentAddressedResponse:
    """Run ``engine(request)`` and wrap the result. ``produced_at`` is passed
    explicitly: nothing in this package reads a clock, so replays and
    conformance vectors stay deterministic."""
    value = engine(request)
    return ContentAddressedResponse(request.request_hash(), request.engine_version, produced_at, byte_identical_replayable, value)


def derive_seed(source: str) -> str:
    return sha256_text(f"seed:{source}")[:32]


@dataclass(frozen=True)
class SealedDocument:
    doc_hash: str
    byte_length: int
    mime: str = "application/octet-stream"
    label: str = ""
    captured_at: str = ""
    extra: dict = field(default_factory=dict)


def seal_document(data: bytes, *, mime: str = "application/octet-stream", label: str = "", captured_at: str = "") -> SealedDocument:
    """A source document (PDF, CSV, .lean file, notebook) is sealed by the
    SHA-256 of its raw bytes. Every claim about it cites ``doc_hash``."""
    return SealedDocument(sha256_bytes(data), len(data), mime, label, captured_at)
