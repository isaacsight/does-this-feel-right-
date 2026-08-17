"""Conformance for the claim graph (academic v1 kinds ``claim_*``).

``conformance_cases()`` is the fixed catalogue; ``compute_expected`` derives
``expected`` from the reference behaviour; the handlers check a port. All
re-execution goes through ``StubReexecutor`` so no subprocess runs.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from ..conformance.runner import Handler, expect_equal
from ..core.approval import Approver, ApprovalRequest, ApprovalToken
from ..core.audit import AppendOnlyAuditLog
from ..core.envelope import sha256_text
from .attest import AttestationLedger, ClaimsDeps, attest_manifest, prepare
from .model import Claim, Computation, manifest_hash, validate_manifest
from .reexec import ExecutionResult, StubReexecutor
from .verify import ClaimVerdict, run_claim_rules, verify_claim

# Academic v1 fixed constants (see ARCHITECTURE.md).
DATA_AS_OF = "2026-08-17T00:00:00.000Z"
APPROVED_AT = "2026-08-17T12:00:00.000Z"
SESSION_ID = "academic-conformance-session"
TRUSTED_APPROVER = {"approver_id": "pi.ada", "secret_utf8": "academic-approver-secret-0001"}
UNTRUSTED_SIGNER = {"approver_id": "student.bob", "secret_utf8": "not-in-the-trust-set"}
MODEL_LINEAGE = [{"model": "local-27b", "version": "conformance"}]
CONFIDENCE_FLOOR = 0.6

PAPER_DOC_HASH = sha256_text("A Small Paper With Two Numbers In It, v1 manuscript bytes")
PAPER_TITLE = "A Small Paper With Two Numbers In It"
ENV = {"python": "3.12.4", "packages": {"numpy": "2.0.1"}}
ENV_UNPINNED = {"python": "", "packages": {"numpy": "2.0.1"}}


def _comp(**over: Any) -> dict:
    fields: Dict[str, Any] = {
        "command": ["python3", "compute_mean.py", "data.csv"],
        "entrypoint": "compute_mean.py",
        "entrypoint_hash": sha256_text("import csv,json,sys\n# fixture entrypoint\n"),
        "input_hashes": {"data.csv": sha256_text("x\n1\n2\n3\n4\n5\n6\n")},
        "environment": ENV,
        "output_selector": "/mean",
        "expected_output_hash": None,
    }
    fields.update(over)
    return Computation.build(**fields).to_json()


COMP_MEAN = _comp()
COMP_SD = _comp(command=["python3", "compute_sd.py", "data.csv"], entrypoint="compute_sd.py", entrypoint_hash=sha256_text("import statistics\n"), output_selector="/sd")
COMP_UNPINNED = _comp(environment=ENV_UNPINNED)


def _claim(computation_id: str, **over: Any) -> dict:
    fields: Dict[str, Any] = {
        "value": 3.5,
        "unit": "kg",
        "tolerance": 0.01,
        "location": {"section": "4.2", "sentence_hash": sha256_text("The mean mass was 3.5 kg.")},
        "source_doc_hash": PAPER_DOC_HASH,
        "computation_ref": computation_id,
        "model_lineage": MODEL_LINEAGE,
        "confidence": 0.9,
    }
    fields.update(over)
    return Claim.build(**fields).to_json()


CLAIM_MEAN = _claim(COMP_MEAN["computation_id"])
CLAIM_SD = _claim(COMP_SD["computation_id"], value=1.8708, unit="kg", tolerance=0.0001, location={"table": "T1", "cell": "B3"})
CLAIM_LOW_CONF = _claim(COMP_MEAN["computation_id"], confidence=0.3, location={"section": "5", "sentence_hash": sha256_text("low")})
CLAIM_UNPINNED = _claim(COMP_UNPINNED["computation_id"], location={"section": "6", "sentence_hash": sha256_text("unpinned")})
CLAIM_ORPHAN = _claim("f" * 64, location={"section": "7", "sentence_hash": sha256_text("orphan")})


def _manifest(claims: List[dict], comps: List[dict], edges: Optional[List[dict]] = None, **over: Any) -> dict:
    m: Dict[str, Any] = {
        "format_version": 1,
        "paper": {"doc_hash": PAPER_DOC_HASH, "title": PAPER_TITLE},
        "computations": comps,
        "claims": claims,
        "edges": edges if edges is not None else [{"claim_id": c["claim_id"], "computation_id": c["computation_ref"]} for c in claims],
    }
    m.update(over)
    return m


MANIFEST_CLEAN = _manifest([CLAIM_MEAN, CLAIM_SD], [COMP_MEAN, COMP_SD])


def _res(stdout: str, ok: bool = True, exit_code: int = 0, value: Optional[float] = None, mismatches: Optional[List[str]] = None, stderr: str = "") -> dict:
    return {
        "ok": ok,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "output_value": value,
        "output_hash": sha256_text(stdout),
        "input_mismatches": mismatches or [],
    }


RES_MEAN_OK = _res('{"mean": 3.5, "n": 6}\n', value=3.5)
RES_MEAN_EDGE = _res('{"mean": 3.51, "n": 6}\n', value=3.51)  # 3.51 - 3.5 = 0.009999999999999787 in IEEE-754: inside 0.01
RES_MEAN_EDGE_OVER = _res('{"mean": 3.6, "n": 6}\n', value=3.6)  # 3.6 - 3.5 = 0.10000000000000009: outside a 0.1 tolerance
RES_MEAN_EDGE_EXACT = _res('{"mean": 3.75, "n": 6}\n', value=3.75)  # with tolerance 0.25: delta 0.25 exactly representable
RES_MEAN_OFF = _res('{"mean": 3.7, "n": 6}\n', value=3.7)
RES_SD_OK = _res('{"sd": 1.8708, "n": 6}\n', value=1.8708)
RES_FAIL = _res("", ok=False, exit_code=1, stderr="Traceback: ZeroDivisionError")
RES_INPUT_MISMATCH = _res("", ok=False, exit_code=-1, stderr="INPUT_HASH_MISMATCH: data.csv", mismatches=["data.csv"])
RES_NO_VALUE = _res("done\n", ok=True, exit_code=0, value=None)

RESULTS_CLEAN = {COMP_MEAN["computation_id"]: RES_MEAN_OK, COMP_SD["computation_id"]: RES_SD_OK}


def _attest_input(manifest: dict, results: dict, approval: str, **over: Any) -> dict:
    d = {
        "manifest": manifest,
        "results": results,
        "session_id": SESSION_ID,
        "data_as_of": DATA_AS_OF,
        "approved_at": APPROVED_AT,
        "trusted": [TRUSTED_APPROVER],
        "confidence_floor": CONFIDENCE_FLOOR,
        "approval": approval,  # valid | wrong_hash | unknown_approver | none
    }
    d.update(over)
    return d


def conformance_cases() -> List[dict]:
    cases: List[dict] = []

    def add(kind: str, id_: str, description: str, inp: dict) -> None:
        cases.append({"kind": kind, "id": id_, "description": description, "input": inp})

    # claim_manifest_hash
    add("claim_manifest_hash", "clean", "content hash of the manifest", {"manifest": MANIFEST_CLEAN})
    shuffled = {k: MANIFEST_CLEAN[k] for k in ["edges", "claims", "computations", "paper", "format_version"]}
    add("claim_manifest_hash", "key_order_irrelevant", "same manifest, keys in another order, same hash", {"manifest": shuffled})
    add("claim_manifest_hash", "empty_manifest", "no claims, no computations", {"manifest": _manifest([], [])})
    add("claim_manifest_hash", "one_byte_changes_hash", "a different title is a different manifest", {"manifest": _manifest([CLAIM_MEAN, CLAIM_SD], [COMP_MEAN, COMP_SD], paper={"doc_hash": PAPER_DOC_HASH, "title": PAPER_TITLE + "."})})

    # claim_manifest_shape
    add("claim_manifest_shape", "clean", "well-formed manifest", {"manifest": MANIFEST_CLEAN})
    add("claim_manifest_shape", "dangling_edge", "edge to a computation not in the manifest", {"manifest": _manifest([CLAIM_MEAN, CLAIM_ORPHAN], [COMP_MEAN])})
    add("claim_manifest_shape", "duplicate_claim_id", "same claim twice", {"manifest": _manifest([CLAIM_MEAN, CLAIM_MEAN], [COMP_MEAN], edges=[{"claim_id": CLAIM_MEAN["claim_id"], "computation_id": COMP_MEAN["computation_id"]}])})
    comp_no_hash = _comp(input_hashes={"data.csv": ""})
    add("claim_manifest_shape", "missing_input_hash", "an input whose pinned hash is empty", {"manifest": _manifest([_claim(comp_no_hash["computation_id"])], [comp_no_hash])})
    add("claim_manifest_shape", "edge_contradicts_claim", "an edge that disagrees with the claim's own computation_ref", {"manifest": _manifest([CLAIM_MEAN], [COMP_MEAN, COMP_SD], edges=[{"claim_id": CLAIM_MEAN["claim_id"], "computation_id": COMP_SD["computation_id"]}])})
    add("claim_manifest_shape", "bad_tolerance", "negative tolerance", {"manifest": _manifest([_claim(COMP_MEAN["computation_id"], tolerance=-0.5)], [COMP_MEAN])})
    add("claim_manifest_shape", "id_mismatch", "a claim whose id is not the hash of its body", {"manifest": _manifest([{**CLAIM_MEAN, "value": 9.9}], [COMP_MEAN])})
    add("claim_manifest_shape", "no_edge_is_ok", "a claim without an edge is structurally fine (DANGLING_COMPUTATION is a rule)", {"manifest": _manifest([CLAIM_MEAN], [COMP_MEAN], edges=[])})
    add("claim_manifest_shape", "not_an_object", "a non-object manifest is one error", {"manifest": []})
    add("claim_manifest_shape", "wrong_paper_hash", "claim source_doc_hash must match paper.doc_hash", {"manifest": _manifest([_claim(COMP_MEAN["computation_id"], source_doc_hash="a" * 64)], [COMP_MEAN])})

    # claim_verify
    def verify_input(claim: dict, comp: Optional[dict], result: Optional[dict], tolerance: Optional[float] = None) -> dict:
        return {"claim": claim, "computation": comp, "result": result, "tolerance": tolerance}

    add("claim_verify", "clean", "observed equals value", verify_input(CLAIM_MEAN, COMP_MEAN, RES_MEAN_OK))
    add("claim_verify", "tolerance_edge_inside", "|delta| exactly equal to tolerance confirms (0.25 is exact in binary)", verify_input(_claim(COMP_MEAN["computation_id"], tolerance=0.25), COMP_MEAN, RES_MEAN_EDGE_EXACT))
    add("claim_verify", "tolerance_edge_float_inside", "3.51 - 3.5 in IEEE-754 is 0.009999999999999787 <= 0.01: confirmed; the vector pins the exact float delta", verify_input(CLAIM_MEAN, COMP_MEAN, RES_MEAN_EDGE))
    add("claim_verify", "tolerance_edge_float_over", "3.6 - 3.5 in IEEE-754 is 0.10000000000000009 > 0.1: mismatch; a port that rounds first fails this vector", verify_input(_claim(COMP_MEAN["computation_id"], tolerance=0.1), COMP_MEAN, RES_MEAN_EDGE_OVER))
    add("claim_verify", "tolerance_override", "an explicit tolerance overrides the claim's", verify_input(CLAIM_MEAN, COMP_MEAN, RES_MEAN_EDGE, tolerance=0.02))
    add("claim_verify", "mismatch", "observed 3.7 vs claimed 3.5", verify_input(CLAIM_MEAN, COMP_MEAN, RES_MEAN_OFF))
    add("claim_verify", "exec_failed", "non-zero exit is execution_failed, no observed value", verify_input(CLAIM_MEAN, COMP_MEAN, RES_FAIL))
    add("claim_verify", "input_hash_mismatch", "changed input never becomes a number", verify_input(CLAIM_MEAN, COMP_MEAN, RES_INPUT_MISMATCH))
    add("claim_verify", "no_value_in_output", "exit 0 but nothing numeric under the selector", verify_input(CLAIM_MEAN, COMP_MEAN, RES_NO_VALUE))
    add("claim_verify", "no_computation", "no computation, no result", verify_input(CLAIM_ORPHAN, None, None))

    # claim_rules
    def rules_input(claim: dict, comp: Optional[dict], verdict: Optional[dict], floor: float = CONFIDENCE_FLOOR) -> dict:
        return {"claim": claim, "computation": comp, "verdict": verdict, "confidence_floor": floor}

    v_ok = {"status": "confirmed", "observed": 3.5, "delta": 0}
    v_mis = {"status": "mismatch", "observed": 3.7, "delta": 0.20000000000000018}
    v_fail = {"status": "execution_failed", "observed": None, "delta": None}
    add("claim_rules", "all_pass", "linked, confirmed, pinned, confident", rules_input(CLAIM_MEAN, COMP_MEAN, v_ok))
    add("claim_rules", "unconfirmed", "execution failed: UNCONFIRMED_CLAIM", rules_input(CLAIM_MEAN, COMP_MEAN, v_fail))
    add("claim_rules", "tolerance_exceeded", "mismatch: TOLERANCE_EXCEEDED (a number was observed, so not UNCONFIRMED)", rules_input(CLAIM_MEAN, COMP_MEAN, v_mis))
    add("claim_rules", "dangling", "no computation: DANGLING_COMPUTATION, UNCONFIRMED_CLAIM, ENVIRONMENT_UNPINNED", rules_input(CLAIM_ORPHAN, None, None))
    add("claim_rules", "env_unpinned", "empty python version: ENVIRONMENT_UNPINNED", rules_input(CLAIM_UNPINNED, COMP_UNPINNED, v_ok))
    add("claim_rules", "low_confidence", "CONFIDENCE_BELOW_FLOOR", rules_input(CLAIM_LOW_CONF, COMP_MEAN, v_ok))
    add("claim_rules", "confidence_at_floor", "confidence equal to the floor passes", rules_input(_claim(COMP_MEAN["computation_id"], confidence=CONFIDENCE_FLOOR), COMP_MEAN, v_ok))

    # claim_attest
    add("claim_attest", "clean_valid_approval", "two claims confirmed, attestation recorded, entry id pinned", _attest_input(MANIFEST_CLEAN, RESULTS_CLEAN, "valid"))
    add("claim_attest", "mismatch_blocks", "one claim off by 0.2 stops at verifier", _attest_input(MANIFEST_CLEAN, {**RESULTS_CLEAN, COMP_MEAN["computation_id"]: RES_MEAN_OFF}, "valid"))
    add("claim_attest", "exec_failed_blocks", "a failed re-execution stops at verifier", _attest_input(MANIFEST_CLEAN, {**RESULTS_CLEAN, COMP_SD["computation_id"]: RES_FAIL}, "valid"))
    add("claim_attest", "input_hash_mismatch_blocks", "a changed input stops at verifier", _attest_input(MANIFEST_CLEAN, {**RESULTS_CLEAN, COMP_MEAN["computation_id"]: RES_INPUT_MISMATCH}, "valid"))
    add("claim_attest", "dangling_edge_shape", "manifest with a dangling edge stops at manifest_shape, nothing on the chain", _attest_input(_manifest([CLAIM_MEAN, CLAIM_ORPHAN], [COMP_MEAN]), RESULTS_CLEAN, "valid"))
    add("claim_attest", "dangling_computation_rule", "a claim with no edge reaches the verifier and fails DANGLING_COMPUTATION", _attest_input(_manifest([CLAIM_MEAN, CLAIM_ORPHAN], [COMP_MEAN], edges=[{"claim_id": CLAIM_MEAN["claim_id"], "computation_id": COMP_MEAN["computation_id"]}]), RESULTS_CLEAN, "valid"))
    add("claim_attest", "wrong_hash_approval", "token over another request hash is refused", _attest_input(MANIFEST_CLEAN, RESULTS_CLEAN, "wrong_hash"))
    add("claim_attest", "unknown_approver", "signer outside the trust set is refused", _attest_input(MANIFEST_CLEAN, RESULTS_CLEAN, "unknown_approver"))
    add("claim_attest", "no_approval", "no token: approval_denied, nothing recorded", _attest_input(MANIFEST_CLEAN, RESULTS_CLEAN, "none"))
    add("claim_attest", "missing_result_is_failure", "stub has no result for a computation: execution_failed", _attest_input(MANIFEST_CLEAN, {COMP_MEAN["computation_id"]: RES_MEAN_OK}, "valid"))
    return cases


# --- reference behaviour ---------------------------------------------------


def _token(inp: Mapping[str, Any], areq: ApprovalRequest) -> Optional[ApprovalToken]:
    mode = inp["approval"]
    if mode == "none":
        return None
    trusted = Approver(TRUSTED_APPROVER["approver_id"], TRUSTED_APPROVER["secret_utf8"].encode("utf-8"))
    if mode == "valid":
        return trusted.approve(areq, inp["approved_at"])
    if mode == "unknown_approver":
        return Approver(UNTRUSTED_SIGNER["approver_id"], UNTRUSTED_SIGNER["secret_utf8"].encode("utf-8")).approve(areq, inp["approved_at"])
    if mode == "wrong_hash":
        return trusted.approve(ApprovalRequest("0" * 64, areq.summary, areq.session_id, areq.materiality), inp["approved_at"])
    raise ValueError(f"unknown approval mode {mode!r}")


def _run_attest(inp: Mapping[str, Any]) -> dict:
    trusted = {t["approver_id"]: t["secret_utf8"].encode("utf-8") for t in inp["trusted"]}
    reexec = StubReexecutor(inp["results"])
    log = AppendOnlyAuditLog(None, clock=lambda: inp["data_as_of"])
    deps = ClaimsDeps(reexec, log, AttestationLedger(), trusted, inp["confidence_floor"])
    approval = None
    if inp["approval"] != "none" and validate_manifest(inp["manifest"]).ok:
        p = prepare(inp["manifest"], reexec, data_as_of=inp["data_as_of"], confidence_floor=inp["confidence_floor"])
        approval = _token(inp, p.approval_request(inp["session_id"]))
    r = attest_manifest(inp["manifest"], None, deps, approval, session_id=inp["session_id"], data_as_of=inp["data_as_of"])
    return r.to_json()


def _opt_comp(d: Optional[Mapping[str, Any]]) -> Optional[Computation]:
    return Computation.from_json(d) if d is not None else None


def compute_expected(kind: str, inp: Mapping[str, Any]) -> Any:
    if kind == "claim_manifest_hash":
        return {"manifest_hash": manifest_hash(inp["manifest"])}
    if kind == "claim_manifest_shape":
        return validate_manifest(inp["manifest"]).to_json()
    if kind == "claim_verify":
        res = ExecutionResult.from_json(inp["result"]) if inp.get("result") is not None else None
        return verify_claim(Claim.from_json(inp["claim"]), _opt_comp(inp.get("computation")), res, inp.get("tolerance")).to_json()
    if kind == "claim_rules":
        v = ClaimVerdict.from_json(inp["verdict"]) if inp.get("verdict") is not None else None
        return run_claim_rules(Claim.from_json(inp["claim"]), _opt_comp(inp.get("computation")), v, confidence_floor=inp["confidence_floor"]).to_json()
    if kind == "claim_attest":
        return _run_attest(inp)
    raise KeyError(kind)


# --- handlers ---------------------------------------------------------------


def h_claim_manifest_hash(inp, exp):
    h = manifest_hash(inp["manifest"])
    return (True, None) if h == exp["manifest_hash"] else (False, f"manifest_hash mismatch: {h}")


def h_claim_manifest_shape(inp, exp):
    return expect_equal(validate_manifest(inp["manifest"]).to_json(), exp)


def h_claim_verify(inp, exp):
    return expect_equal(compute_expected("claim_verify", inp), exp)


def h_claim_rules(inp, exp):
    return expect_equal(compute_expected("claim_rules", inp), exp)


def h_claim_attest(inp, exp):
    return expect_equal(_run_attest(inp), exp)


CONFORMANCE_HANDLERS: Dict[str, Handler] = {
    "claim_manifest_hash": h_claim_manifest_hash,
    "claim_manifest_shape": h_claim_manifest_shape,
    "claim_verify": h_claim_verify,
    "claim_rules": h_claim_rules,
    "claim_attest": h_claim_attest,
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
]
