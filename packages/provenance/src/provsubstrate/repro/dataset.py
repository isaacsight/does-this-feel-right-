"""Versioned dataset export of signed reproduction reports.

One canonical JSON line per report, rows ordered by ``report_id`` so the
same set of reports always yields the same bytes regardless of collection
order. The manifest carries a per-row sha256 and a ``dataset_hash`` over the
row table; Zenodo and Croissant metadata are thin wrappers that cite the
same hashes so a downloader can verify what a DOI points at.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..core.canonical import canonicalize
from ..core.envelope import content_hash, sha256_text

DATASET_FORMAT_VERSION = 1
DATASET_NAME = "reproducibility-ledger-reports"
DATASET_ENCODING = "application/jsonl"

ZENODO_LICENSE_IDS = {"MIT": "mit", "CC-BY-4.0": "cc-by-4.0", "CC0-1.0": "cc-zero"}
SPDX_LICENSE_URLS = {
    "MIT": "https://spdx.org/licenses/MIT.html",
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
}


def _row_key(report: Mapping) -> str:
    rid = report.get("report_id")
    return rid if isinstance(rid, str) and rid else content_hash(report)


def _ordered(reports: Sequence[Mapping]) -> List[Mapping]:
    return sorted(reports, key=_row_key)


def dataset_filename(version: str) -> str:
    return f"{DATASET_NAME}-{version}.jsonl"


def export_jsonl(reports: Sequence[Mapping]) -> str:
    """One canonical JSON line per signed report, sorted by report_id, with a
    trailing newline; empty input yields the empty string."""
    rows = _ordered(reports)
    if not rows:
        return ""
    return "\n".join(canonicalize(r) for r in rows) + "\n"


def dataset_manifest(reports: Sequence[Mapping], version: str) -> dict:
    rows = _ordered(reports)
    table = [{"report_id": _row_key(r), "sha256": sha256_text(canonicalize(r))} for r in rows]
    jsonl = export_jsonl(rows)
    return {
        "format_version": DATASET_FORMAT_VERSION,
        "name": DATASET_NAME,
        "version": version,
        "row_count": len(rows),
        "rows": table,
        "dataset_hash": content_hash(table),
        "distribution": {
            "filename": dataset_filename(version),
            "encoding_format": DATASET_ENCODING,
            "sha256": sha256_text(jsonl),
            "content_size": len(jsonl.encode("utf-8")),
        },
    }


def zenodo_metadata(
    manifest: Mapping,
    *,
    title: str,
    creators: Sequence[Mapping[str, str]],
    description: str,
    license: str = "CC-BY-4.0",
    keywords: Optional[Sequence[str]] = None,
    related_identifiers: Optional[Sequence[Mapping[str, str]]] = None,
) -> dict:
    """Zenodo deposition metadata (``PUT /api/deposit/depositions/:id``
    body). ``license`` is an SPDX-ish id from ``ZENODO_LICENSE_IDS``."""
    if license not in ZENODO_LICENSE_IDS:
        raise ValueError(f"zenodo_metadata: unsupported license {license!r}; one of {sorted(ZENODO_LICENSE_IDS)}")
    kws = list(keywords) if keywords is not None else ["reproducibility", "provenance", "audit", "conformance"]
    notes = (
        f"dataset_hash: {manifest['dataset_hash']}; rows: {manifest['row_count']}; "
        f"file: {manifest['distribution']['filename']} sha256 {manifest['distribution']['sha256']}"
    )
    md: Dict[str, Any] = {
        "title": title,
        "upload_type": "dataset",
        "description": description,
        "creators": [dict(c) for c in creators],
        "access_right": "open",
        "license": ZENODO_LICENSE_IDS[license],
        "keywords": kws,
        "version": manifest["version"],
        "notes": notes,
    }
    if related_identifiers:
        md["related_identifiers"] = [dict(r) for r in related_identifiers]
    return {"metadata": md}


_CROISSANT_CONTEXT = {
    "@language": "en",
    "@vocab": "https://schema.org/",
    "citeAs": "cr:citeAs",
    "column": "cr:column",
    "conformsTo": "dct:conformsTo",
    "cr": "http://mlcommons.org/croissant/",
    "data": {"@id": "cr:data", "@type": "@json"},
    "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
    "dct": "http://purl.org/dc/terms/",
    "extract": "cr:extract",
    "field": "cr:field",
    "fileObject": "cr:fileObject",
    "fileProperty": "cr:fileProperty",
    "fileSet": "cr:fileSet",
    "format": "cr:format",
    "includes": "cr:includes",
    "isLiveDataset": "cr:isLiveDataset",
    "jsonPath": "cr:jsonPath",
    "key": "cr:key",
    "md5": "cr:md5",
    "parentField": "cr:parentField",
    "path": "cr:path",
    "recordSet": "cr:recordSet",
    "references": "cr:references",
    "regex": "cr:regex",
    "repeated": "cr:repeated",
    "replace": "cr:replace",
    "sc": "https://schema.org/",
    "separator": "cr:separator",
    "source": "cr:source",
    "subField": "cr:subField",
    "transform": "cr:transform",
}

_CROISSANT_FIELDS = (
    ("report_id", "sc:Text", "$.report_id"),
    ("request_hash", "sc:Text", "$.request_hash"),
    ("target_hash", "sc:Text", "$.target_hash"),
    ("paper_title", "sc:Text", "$.target.paper.title"),
    ("paper_doc_hash", "sc:Text", "$.target.paper.doc_hash"),
    ("repo_url", "sc:Text", "$.target.repo.url"),
    ("repo_commit", "sc:Text", "$.target.repo.commit"),
    ("overall", "sc:Text", "$.verdict.overall"),
    ("confirmed", "sc:Integer", "$.verdict.confirmed"),
    ("total", "sc:Integer", "$.verdict.total"),
    ("approver_id", "sc:Text", "$.approval.approver_id"),
    ("approved_at", "sc:Text", "$.approval.approved_at"),
)


def croissant_metadata(
    manifest: Mapping,
    *,
    name: str = DATASET_NAME,
    description: str = "Signed reproduction reports: paper claims, attempted reproduction, deterministic verdict, human approval.",
    license: str = "CC-BY-4.0",
    url: Optional[str] = None,
    cite_as: Optional[str] = None,
) -> dict:
    """Minimal MLCommons Croissant 1.0 JSON-LD: one FileObject (the JSONL,
    with its sha256) and one RecordSet whose fields are read by JSON path."""
    fn = manifest["distribution"]["filename"]
    ds: Dict[str, Any] = {
        "@context": _CROISSANT_CONTEXT,
        "@type": "sc:Dataset",
        "name": name,
        "description": description,
        "conformsTo": "http://mlcommons.org/croissant/1.0",
        "license": SPDX_LICENSE_URLS.get(license, license),
        "version": manifest["version"],
        "distribution": [
            {
                "@type": "cr:FileObject",
                "@id": fn,
                "name": fn,
                "contentUrl": fn,
                "encodingFormat": manifest["distribution"]["encoding_format"],
                "sha256": manifest["distribution"]["sha256"],
                "contentSize": f"{manifest['distribution']['content_size']} B",
            }
        ],
        "recordSet": [
            {
                "@type": "cr:RecordSet",
                "@id": "reports",
                "name": "reports",
                "description": f"{manifest['row_count']} signed reproduction reports; dataset_hash {manifest['dataset_hash']}",
                "key": {"@id": "reports/report_id"},
                "field": [
                    {
                        "@type": "cr:Field",
                        "@id": f"reports/{fname}",
                        "name": fname,
                        "dataType": dtype,
                        "source": {"fileObject": {"@id": fn}, "extract": {"jsonPath": jpath}},
                    }
                    for fname, dtype, jpath in _CROISSANT_FIELDS
                ],
            }
        ],
    }
    if url:
        ds["url"] = url
    if cite_as:
        ds["citeAs"] = cite_as
    return ds
