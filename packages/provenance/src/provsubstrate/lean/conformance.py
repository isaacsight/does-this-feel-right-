"""Conformance for the Lean proof ledger (academic v1 kinds ``lean_*``).

``conformance_cases()`` is the fixed catalogue; ``compute_expected`` derives
each vector's ``expected`` from the reference behaviour; the handlers check
a port. Every case runs against ``StubKernel`` so no Lean is required —
the kernel table is keyed by the proof-file hash, which means a port whose
``render_lean_file`` drifts by one byte gets "no verdict" and fails loudly.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping

from ..conformance.runner import Handler, expect_equal
from ..core.approval import Approver, ApprovalRequest, ApprovalToken
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import sha256_text
from .claim import ProofClaim, proof_file_hash, render_lean_file, statement_hash, validate_claim_shape
from .kernel import KernelVerdict, StubKernel, check_proof
from .ledger import LEAN_RECORD_MATERIALITY, LeanDeps, ProofLedger, approval_summary, prepare, record_proof
from .rules import DEFAULT_AXIOM_ALLOWLIST, run_lean_rules

# Academic v1 fixed constants (see ARCHITECTURE.md).
DATA_AS_OF = "2026-08-17T00:00:00.000Z"
APPROVED_AT = "2026-08-17T12:00:00.000Z"
SESSION_ID = "academic-conformance-session"
TRUSTED_APPROVER = {"approver_id": "pi.ada", "secret_utf8": "academic-approver-secret-0001"}
UNTRUSTED_SIGNER = {"approver_id": "student.bob", "secret_utf8": "not-in-the-trust-set"}
MODEL_LINEAGE = [{"model": "local-27b", "version": "conformance"}]
CONFIDENCE_FLOOR = 0.6
TOOLCHAIN = "leanprover/lean4:v4.12.0"
MATHLIB_REV = "3f2b9c1d8e7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c"
PROMPT_HASH = sha256_text("Prove that n + 0 = n for every natural number n.")

STATEMENT = "∀ n : Nat, n + 0 = n"


def _claim(**over: Any) -> dict:
    base = {
        "theorem_name": "Nat.add_zero'",
        "statement": STATEMENT,
        "proof": "by\n  intro n\n  rfl",
        "imports": ["Mathlib.Tactic"],
        "model_lineage": MODEL_LINEAGE,
        "prompt_hash": PROMPT_HASH,
        "toolchain": TOOLCHAIN,
        "mathlib_rev": MATHLIB_REV,
        "confidence": 0.91,
        "doc_hash": statement_hash(STATEMENT),
    }
    base.update(over)
    return base


CLEAN = _claim()
SORRY = _claim(proof="by\n  intro n\n  sorry")
TERM_MODE = _claim(proof="fun n => rfl")
NATIVE_DECIDE = _claim(theorem_name="small_prime", statement="Nat.Prime 97", proof="by native_decide", doc_hash=statement_hash("Nat.Prime 97"))
UNPINNED = _claim(toolchain="")
HASH_MISMATCH = _claim(doc_hash="0" * 64)
LOW_CONFIDENCE = _claim(confidence=0.2)
REJECTED = _claim(proof="by\n  intro n\n  exact rfl'")  # kernel says no (stub); the source is still well-formed
NO_IMPORTS = _claim(imports=[], mathlib_rev="")
MULTILINE_TERM = _claim(proof="fun n =>\n  show n + 0 = n from\n    rfl")

_KV_OK = {"ok": True, "errors": [], "sorries": 0, "axioms": []}
_KV_OK_PROPEXT = {"ok": True, "errors": [], "sorries": 0, "axioms": ["propext"]}
_KV_SORRY = {"ok": True, "errors": [], "sorries": 1, "axioms": ["sorryAx"]}
_KV_REJECT = {"ok": False, "errors": ["3:9: unknown identifier 'rfl''"], "sorries": 0, "axioms": []}
_KV_FORBIDDEN = {"ok": True, "errors": [], "sorries": 0, "axioms": ["propext", "Lean.ofReduceBool"]}
_KV_STRANGE_AXIOM = {"ok": True, "errors": [], "sorries": 0, "axioms": ["propext", "Mathlib.Meta.unsafeAx"]}


def _table(claim_json: dict, verdict: dict) -> dict:
    return {proof_file_hash(ProofClaim.from_json(claim_json)): verdict}


def _record_input(claim_json: dict, verdict: dict, approval: str, **over: Any) -> dict:
    d = {
        "claim": claim_json,
        "kernel_table": _table(claim_json, verdict) if verdict else {},
        "session_id": SESSION_ID,
        "data_as_of": DATA_AS_OF,
        "approved_at": APPROVED_AT,
        "trusted": [TRUSTED_APPROVER],
        "confidence_floor": CONFIDENCE_FLOOR,
        "axiom_allowlist": list(DEFAULT_AXIOM_ALLOWLIST),
        "approval": approval,  # valid | wrong_hash | unknown_approver | none
    }
    d.update(over)
    return d


def conformance_cases() -> List[dict]:
    cases: List[dict] = []

    def add(kind: str, id_: str, description: str, inp: dict) -> None:
        cases.append({"kind": kind, "id": id_, "description": description, "input": inp})

    # lean_claim_shape
    add("lean_claim_shape", "clean", "well-formed claim passes with no errors", {"claim": CLEAN})
    add("lean_claim_shape", "not_an_object", "a non-object claim is one error", {"claim": "theorem foo"})
    add(
        "lean_claim_shape",
        "missing_fields",
        "missing statement, proof, lineage, hashes reported together, sorted",
        {"claim": {"theorem_name": "foo", "toolchain": TOOLCHAIN, "mathlib_rev": "", "confidence": 0.5}},
    )
    add(
        "lean_claim_shape",
        "bad_hashes_and_confidence",
        "non-hex hashes and out-of-range confidence",
        {"claim": _claim(prompt_hash="not-a-hash", doc_hash="ABC", confidence=1.5)},
    )
    add("lean_claim_shape", "bad_theorem_name", "theorem_name must be a Lean identifier", {"claim": _claim(theorem_name="1bad name")})
    add("lean_claim_shape", "unpinned_is_shape_ok", "an empty toolchain is a rule failure, not a shape error", {"claim": UNPINNED})

    # lean_proof_file_hash
    add("lean_proof_file_hash", "tactic_block", "multi-line tactic proof rendered with two-space indent", {"claim": CLEAN})
    add("lean_proof_file_hash", "term_mode", "term-mode proof on the same line", {"claim": TERM_MODE})
    add("lean_proof_file_hash", "one_line_tactic", "single tactic stays on the header line", {"claim": NATIVE_DECIDE})
    add("lean_proof_file_hash", "no_imports", "no import block, no leading blank line", {"claim": NO_IMPORTS})
    add("lean_proof_file_hash", "multiline_term", "multi-line term proof dedented and re-indented", {"claim": MULTILINE_TERM})
    add("lean_proof_file_hash", "sorry", "a sorry is rendered like any other tactic; static scan finds it", {"claim": SORRY})

    # lean_rules
    def rules_input(claim_json: dict, verdict: dict, **over: Any) -> dict:
        d = {"claim": claim_json, "kernel_table": _table(claim_json, verdict), "confidence_floor": CONFIDENCE_FLOOR, "axiom_allowlist": list(DEFAULT_AXIOM_ALLOWLIST)}
        d.update(over)
        return d

    add("lean_rules", "all_pass", "kernel ok, no sorry, allowed axioms, pinned, hash matches", rules_input(CLEAN, _KV_OK_PROPEXT))
    add("lean_rules", "kernel_rejected", "KERNEL_REJECTED; every other rule still runs", rules_input(REJECTED, _KV_REJECT))
    add("lean_rules", "contains_sorry", "CONTAINS_SORRY from the static scan even if the kernel said ok with 0 sorries; sorryAx is also outside the allowlist", rules_input(SORRY, _KV_OK))
    add("lean_rules", "forbidden_axiom_native_decide", "native_decide introduces Lean.ofReduceBool, outside the allowlist", rules_input(NATIVE_DECIDE, _KV_FORBIDDEN))
    add("lean_rules", "forbidden_axiom_from_kernel", "an axiom the kernel reports outside the allowlist", rules_input(CLEAN, _KV_STRANGE_AXIOM))
    add("lean_rules", "allowlist_widened", "the same axiom passes when the allowlist admits it", rules_input(CLEAN, _KV_STRANGE_AXIOM, axiom_allowlist=list(DEFAULT_AXIOM_ALLOWLIST) + ["Mathlib.Meta.unsafeAx"]))
    add("lean_rules", "unpinned_toolchain", "TOOLCHAIN_UNPINNED", rules_input(UNPINNED, _KV_OK))
    add("lean_rules", "hash_mismatch", "STATEMENT_HASH_MISMATCH: doc_hash is not sha256(statement)", rules_input(HASH_MISMATCH, _KV_OK))
    add("lean_rules", "low_confidence", "CONFIDENCE_BELOW_FLOOR", rules_input(LOW_CONFIDENCE, _KV_OK))
    add("lean_rules", "confidence_at_floor", "confidence equal to the floor passes", rules_input(_claim(confidence=CONFIDENCE_FLOOR), _KV_OK))

    # lean_approval_summary
    add("lean_approval_summary", "clean", "kernel ok, propext only", {"claim": CLEAN, "verdict": _KV_OK_PROPEXT})
    add("lean_approval_summary", "no_axioms_no_mathlib", "axioms: none, mathlib (none)", {"claim": NO_IMPORTS, "verdict": _KV_OK})
    add("lean_approval_summary", "rejected_with_sorry", "kernel REJECTED and a sorry count", {"claim": SORRY, "verdict": {"ok": False, "errors": ["x"], "sorries": 1, "axioms": ["sorryAx"]}})
    add("lean_approval_summary", "unpinned", "toolchain (unpinned)", {"claim": UNPINNED, "verdict": _KV_OK})

    # lean_record
    add("lean_record", "clean_valid_approval", "end to end: recorded, entry id pinned", _record_input(CLEAN, _KV_OK_PROPEXT, "valid"))
    add("lean_record", "proof_with_sorry", "stops at verifier: CONTAINS_SORRY", _record_input(SORRY, _KV_SORRY, "valid"))
    add("lean_record", "kernel_rejected", "stops at kernel stage", _record_input(REJECTED, _KV_REJECT, "valid"))
    add("lean_record", "forbidden_axiom", "stops at verifier: FORBIDDEN_AXIOM", _record_input(NATIVE_DECIDE, _KV_FORBIDDEN, "valid"))
    add("lean_record", "unpinned_toolchain", "stops at verifier: TOOLCHAIN_UNPINNED", _record_input(UNPINNED, _KV_OK, "valid"))
    add("lean_record", "hash_mismatch", "stops at verifier: STATEMENT_HASH_MISMATCH", _record_input(HASH_MISMATCH, _KV_OK, "valid"))
    add("lean_record", "wrong_hash_approval", "token signed over a different request hash is refused", _record_input(CLEAN, _KV_OK_PROPEXT, "wrong_hash"))
    add("lean_record", "unknown_approver", "a signer outside the trust set is refused", _record_input(CLEAN, _KV_OK_PROPEXT, "unknown_approver"))
    add("lean_record", "no_approval", "no token: approval_denied, nothing recorded", _record_input(CLEAN, _KV_OK_PROPEXT, "none"))
    add("lean_record", "bad_shape", "shape failure records nothing", _record_input({"theorem_name": "x"}, {}, "valid"))
    return cases


# --- reference behaviour ---------------------------------------------------


def _kernel_from(inp: Mapping[str, Any]) -> StubKernel:
    return StubKernel(inp.get("kernel_table", {}))


def _token(inp: Mapping[str, Any], areq: ApprovalRequest) -> ApprovalToken | None:
    mode = inp["approval"]
    if mode == "none":
        return None
    if mode == "valid":
        return Approver(TRUSTED_APPROVER["approver_id"], TRUSTED_APPROVER["secret_utf8"].encode("utf-8")).approve(areq, inp["approved_at"])
    if mode == "unknown_approver":
        return Approver(UNTRUSTED_SIGNER["approver_id"], UNTRUSTED_SIGNER["secret_utf8"].encode("utf-8")).approve(areq, inp["approved_at"])
    if mode == "wrong_hash":
        other = ApprovalRequest("0" * 64, areq.summary, areq.session_id, areq.materiality)
        return Approver(TRUSTED_APPROVER["approver_id"], TRUSTED_APPROVER["secret_utf8"].encode("utf-8")).approve(other, inp["approved_at"])
    raise ValueError(f"unknown approval mode {mode!r}")


def _run_record(inp: Mapping[str, Any]) -> dict:
    trusted = {t["approver_id"]: t["secret_utf8"].encode("utf-8") for t in inp["trusted"]}
    kernel = _kernel_from(inp)
    log = AppendOnlyAuditLog(None, clock=lambda: inp["data_as_of"])
    deps = LeanDeps(kernel, log, ProofLedger(), trusted, inp["confidence_floor"], tuple(inp["axiom_allowlist"]))
    shape = validate_claim_shape(inp["claim"])
    approval = None
    if shape.ok and shape.claim is not None and inp["approval"] != "none":
        p = prepare(shape.claim, kernel, data_as_of=inp["data_as_of"], confidence_floor=inp["confidence_floor"], axiom_allowlist=tuple(inp["axiom_allowlist"]))
        approval = _token(inp, p.approval_request(inp["session_id"]))
    r = record_proof(inp["claim"], deps, approval, session_id=inp["session_id"], data_as_of=inp["data_as_of"])
    return r.to_json()


def compute_expected(kind: str, inp: Mapping[str, Any]) -> Any:
    if kind == "lean_claim_shape":
        return validate_claim_shape(inp["claim"]).to_json()
    if kind == "lean_proof_file_hash":
        c = ProofClaim.from_json(inp["claim"])
        src = render_lean_file(c)
        return {"source": src, "proof_file_hash": sha256_text(src)}
    if kind == "lean_rules":
        c = ProofClaim.from_json(inp["claim"])
        v = check_proof(render_lean_file(c), _kernel_from(inp))
        return {"verdict": v.to_json(), "report": run_lean_rules(c, v, confidence_floor=inp["confidence_floor"], axiom_allowlist=tuple(inp["axiom_allowlist"])).to_json()}
    if kind == "lean_approval_summary":
        return {"summary": approval_summary(ProofClaim.from_json(inp["claim"]), KernelVerdict.from_json(inp["verdict"]))}
    if kind == "lean_record":
        return _run_record(inp)
    raise KeyError(kind)


# --- handlers ---------------------------------------------------------------


def h_lean_claim_shape(inp, exp):
    return expect_equal(validate_claim_shape(inp["claim"]).to_json(), exp)


def h_lean_proof_file_hash(inp, exp):
    src = render_lean_file(ProofClaim.from_json(inp["claim"]))
    if src != exp["source"]:
        return False, f"source mismatch: {src!r}"
    h = sha256_text(src)
    return (True, None) if h == exp["proof_file_hash"] else (False, f"hash mismatch: {h}")


def h_lean_rules(inp, exp):
    return expect_equal(compute_expected("lean_rules", inp), exp)


def h_lean_approval_summary(inp, exp):
    s = approval_summary(ProofClaim.from_json(inp["claim"]), KernelVerdict.from_json(inp["verdict"]))
    return (True, None) if s == exp["summary"] else (False, f"summary mismatch: {s}")


def h_lean_record(inp, exp):
    return expect_equal(_run_record(inp), exp)


CONFORMANCE_HANDLERS: Dict[str, Handler] = {
    "lean_claim_shape": h_lean_claim_shape,
    "lean_proof_file_hash": h_lean_proof_file_hash,
    "lean_rules": h_lean_rules,
    "lean_approval_summary": h_lean_approval_summary,
    "lean_record": h_lean_record,
}

__all__ = [
    "conformance_cases",
    "compute_expected",
    "CONFORMANCE_HANDLERS",
    "DATA_AS_OF",
    "APPROVED_AT",
    "SESSION_ID",
    "TRUSTED_APPROVER",
    "UNTRUSTED_SIGNER",
    "MODEL_LINEAGE",
    "LEAN_RECORD_MATERIALITY",
]
