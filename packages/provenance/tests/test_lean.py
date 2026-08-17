"""Lean proof ledger: unit tests plus the conformance handlers evaluated
against their own compute_expected (round trip + determinism)."""

import json
import os

import pytest

from provsubstrate.core import AppendOnlyAuditLog, ApprovalRequest, Approver, verify_chain
from provsubstrate.lean import (
    CONFORMANCE_HANDLERS,
    LEAN_RECORD_MATERIALITY,
    KernelVerdict,
    LakeDisposer,
    LeanDeps,
    ProofClaim,
    ProofLedger,
    StubKernel,
    approval_summary,
    check_proof,
    compute_expected,
    conformance_cases,
    parse_lean_output,
    prepare,
    proof_file_hash,
    record_proof,
    render_lean_file,
    run_lean_rules,
    statement_hash,
    static_scan,
    validate_claim_shape,
)
from provsubstrate.lean.conformance import (
    APPROVED_AT,
    CLEAN,
    DATA_AS_OF,
    SESSION_ID,
    SORRY,
    TRUSTED_APPROVER,
)

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples", "lean")


def _canon(x) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


# --- claim + rendering -----------------------------------------------------


def test_claim_shape_clean_and_errors_sorted():
    assert validate_claim_shape(CLEAN).ok
    bad = dict(CLEAN)
    bad["confidence"] = 2
    bad["doc_hash"] = "zz"
    del bad["proof"]
    r = validate_claim_shape(bad)
    assert not r.ok
    assert r.errors == sorted(r.errors)
    assert "confidence must be in [0,1]" in r.errors
    assert "doc_hash must be sha256 hex" in r.errors
    assert "proof must be non-empty string" in r.errors
    assert validate_claim_shape(None).errors == ["claim is not an object"]


def test_render_lean_file_is_deterministic_and_hash_matches_bytes():
    c = ProofClaim.from_json(CLEAN)
    src = render_lean_file(c)
    assert src == "import Mathlib.Tactic\n\ntheorem Nat.add_zero' : ∀ n : Nat, n + 0 = n := by\n  intro n\n  rfl\n"
    assert render_lean_file(c) == src
    from provsubstrate.core import sha256_text

    assert proof_file_hash(c) == sha256_text(src)


def test_render_term_mode_and_indentation_normalised():
    c = ProofClaim.from_json({**CLEAN, "imports": [], "proof": "fun n => rfl"})
    assert render_lean_file(c) == "theorem Nat.add_zero' : ∀ n : Nat, n + 0 = n := fun n => rfl\n"
    # Over-indented tactic body is dedented then re-indented by exactly two spaces.
    c2 = ProofClaim.from_json({**CLEAN, "imports": [], "proof": "by\n        intro n\n        rfl"})
    assert render_lean_file(c2) == "theorem Nat.add_zero' : ∀ n : Nat, n + 0 = n := by\n  intro n\n  rfl\n"


def test_example_claim_renders_the_example_file():
    with open(os.path.join(EXAMPLES, "claim.json"), encoding="utf-8") as f:
        claim = ProofClaim.from_json(json.load(f))
    with open(os.path.join(EXAMPLES, "Basic.lean"), encoding="utf-8") as f:
        body = "".join(ln for ln in f if not ln.startswith("--"))
    assert render_lean_file(claim) == body
    assert claim.doc_hash == statement_hash(claim.statement)


# --- disposer --------------------------------------------------------------


def test_static_scan_finds_sorry_admit_native_decide_and_axioms_but_not_in_comments():
    src = "-- sorry in a comment\n/- admit in a block -/\ntheorem t : True := by\n  sorry\naxiom myAx : False\ntheorem u : 2 + 2 = 4 := by native_decide\n"
    s = static_scan(src)
    assert s.sorries == 1
    assert s.axioms == ["Lean.ofReduceBool", "myAx", "sorryAx"]
    assert static_scan('theorem s : "sorry" = "sorry" := rfl').sorries == 0


def test_check_proof_merges_kernel_and_static_scan():
    src = render_lean_file(ProofClaim.from_json(SORRY))
    kernel = StubKernel({proof_file_hash(ProofClaim.from_json(SORRY)): KernelVerdict(True, [], 0, [])})
    v = check_proof(src, kernel)
    assert v.ok and v.sorries == 1 and v.axioms == ["sorryAx"]


def test_stub_kernel_rejects_unknown_hash():
    v = StubKernel({}).check("theorem t : True := trivial\n")
    assert not v.ok and v.errors and "no verdict" in v.errors[0]


def test_parse_lean_output():
    out = (
        "/tmp/x/ProvCheck.lean:3:2: error: unknown identifier 'foo'\n"
        "/tmp/x/ProvCheck.lean:1:8: warning: declaration uses 'sorry'\n"
        "'t' depends on axioms: [propext, Classical.choice]\n"
        "'u' does not depend on any axioms\n"
    )
    v = parse_lean_output(out, 1)
    assert not v.ok
    assert v.errors == ["3:2: unknown identifier 'foo'"]
    assert v.sorries == 1
    assert v.axioms == ["Classical.choice", "propext"]
    assert parse_lean_output("", 0).ok


@pytest.mark.skipif(not LakeDisposer.available(), reason="lean not on PATH")
def test_real_kernel_accepts_example():
    with open(os.path.join(EXAMPLES, "claim.json"), encoding="utf-8") as f:
        claim = ProofClaim.from_json(json.load(f))
    v = check_proof(render_lean_file(claim), LakeDisposer(timeout=120))
    assert v.ok, v.errors
    assert v.sorries == 0


# --- rules + gate ----------------------------------------------------------


def test_rules_run_every_check_no_short_circuit():
    c = ProofClaim.from_json({**CLEAN, "toolchain": "", "confidence": 0.1, "doc_hash": "0" * 64})
    v = KernelVerdict(False, ["boom"], 2, ["Lean.ofReduceBool"])
    r = run_lean_rules(c, v)
    assert not r.ok
    assert len(r.checks) == 6
    assert r.codes() == [
        "KERNEL_REJECTED",
        "CONTAINS_SORRY",
        "FORBIDDEN_AXIOM",
        "CONFIDENCE_BELOW_FLOOR",
        "STATEMENT_HASH_MISMATCH",
        "TOOLCHAIN_UNPINNED",
    ]
    ok = run_lean_rules(ProofClaim.from_json(CLEAN), KernelVerdict(True, [], 0, ["propext", "Quot.sound"]))
    assert ok.ok and ok.codes() == []


def test_approval_summary_is_fixed_format():
    s = approval_summary(ProofClaim.from_json(CLEAN), KernelVerdict(True, [], 0, ["propext"]))
    assert s.startswith("Record proof of Nat.add_zero' (92 bytes, kernel ok, 0 sorries, axioms: propext) toolchain leanprover/lean4:v4.12.0 mathlib 3f2b9c1d8e7a file ")
    assert s == approval_summary(ProofClaim.from_json(CLEAN), KernelVerdict(True, [], 0, ["propext"]))


def _deps(kernel_table, secret=b"academic-approver-secret-0001"):
    log = AppendOnlyAuditLog(None, clock=lambda: DATA_AS_OF)
    return LeanDeps(StubKernel(kernel_table), log, ProofLedger(), {"pi.ada": secret})


def test_record_proof_end_to_end_with_valid_approval():
    claim = ProofClaim.from_json(CLEAN)
    table = {proof_file_hash(claim): KernelVerdict(True, [], 0, ["propext"])}
    deps = _deps(table)
    p = prepare(claim, deps.kernel, data_as_of=DATA_AS_OF)
    tok = Approver("pi.ada", b"academic-approver-secret-0001").approve(p.approval_request(SESSION_ID), APPROVED_AT)
    r = record_proof(claim, deps, tok, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
    assert r.ok and r.stage is None
    assert r.audit_actions == ["proof_claim", "kernel_verdict", "verifier_check", "approval_granted", "proof_recorded"]
    assert r.entry_id is not None and len(deps.ledger.entries) == 1
    assert deps.ledger.entries[0]["entry_id"] == r.entry_id
    assert deps.ledger.entries[0]["approver"] == "pi.ada"
    assert deps.ledger.entries[0]["recorded_at"] == APPROVED_AT
    assert verify_chain(deps.audit_log.entries).ok
    # The approval bound the exact request hash and materiality.
    assert tok.request_hash == r.request_hash and tok.materiality == LEAN_RECORD_MATERIALITY


def test_record_proof_stops_before_gate_on_sorry_and_records_nothing():
    claim = ProofClaim.from_json(SORRY)
    deps = _deps({proof_file_hash(claim): KernelVerdict(True, [], 1, ["sorryAx"])})
    p = prepare(claim, deps.kernel, data_as_of=DATA_AS_OF)
    tok = Approver("pi.ada", b"academic-approver-secret-0001").approve(p.approval_request(SESSION_ID), APPROVED_AT)
    r = record_proof(claim, deps, tok, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
    assert not r.ok and r.stage == "verifier"
    assert r.audit_actions == ["proof_claim", "kernel_verdict", "verifier_check"]
    assert deps.ledger.entries == []


def test_record_proof_refuses_wrong_hash_unknown_approver_and_missing_token():
    claim = ProofClaim.from_json(CLEAN)
    table = {proof_file_hash(claim): KernelVerdict(True, [], 0, [])}
    for mode in ("wrong_hash", "unknown", "none"):
        deps = _deps(table)
        p = prepare(claim, deps.kernel, data_as_of=DATA_AS_OF)
        areq = p.approval_request(SESSION_ID)
        if mode == "wrong_hash":
            tok = Approver("pi.ada", b"academic-approver-secret-0001").approve(ApprovalRequest("1" * 64, areq.summary, SESSION_ID, LEAN_RECORD_MATERIALITY), APPROVED_AT)
        elif mode == "unknown":
            tok = Approver("student.bob", b"not-in-the-trust-set").approve(areq, APPROVED_AT)
        else:
            tok = None
        r = record_proof(claim, deps, tok, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
        assert not r.ok and r.stage == "approval", mode
        assert r.audit_actions[-1] == "approval_denied"
        assert deps.ledger.entries == []


def test_record_proof_bad_shape_touches_nothing():
    deps = _deps({})
    r = record_proof({"theorem_name": "x"}, deps, None, session_id=SESSION_ID, data_as_of=DATA_AS_OF)
    assert r.stage == "claim_shape" and r.audit_actions == [] and deps.audit_log.entries == []


# --- conformance -----------------------------------------------------------

_KINDS = {"lean_claim_shape", "lean_proof_file_hash", "lean_rules", "lean_approval_summary", "lean_record"}


def test_conformance_catalogue_is_fixed_and_covers_every_kind():
    cases = conformance_cases()
    assert {c["kind"] for c in cases} == _KINDS == set(CONFORMANCE_HANDLERS)
    ids = [(c["kind"], c["id"]) for c in cases]
    assert len(ids) == len(set(ids))
    assert _canon(cases) == _canon(conformance_cases())
    for want in ("clean_valid_approval", "proof_with_sorry", "kernel_rejected", "forbidden_axiom", "unpinned_toolchain", "hash_mismatch", "wrong_hash_approval", "unknown_approver", "no_approval"):
        assert ("lean_record", want) in ids


@pytest.mark.parametrize("case", conformance_cases(), ids=lambda c: f"{c['kind']}/{c['id']}")
def test_conformance_round_trip_and_determinism(case):
    exp1 = compute_expected(case["kind"], case["input"])
    exp2 = compute_expected(case["kind"], case["input"])
    assert _canon(exp1) == _canon(exp2)
    ok, detail = CONFORMANCE_HANDLERS[case["kind"]](case["input"], exp1)
    assert ok, detail
    # JSON round trip: vectors are files.
    reloaded = json.loads(json.dumps({"input": case["input"], "expected": exp1}))
    ok2, detail2 = CONFORMANCE_HANDLERS[case["kind"]](reloaded["input"], reloaded["expected"])
    assert ok2, detail2


def test_negative_control_sloppy_render_fails_every_hash_vector():
    """A port that pastes the proof on its own line without normalising the
    layout fails every lean_proof_file_hash vector, and its stub-kernel
    lookups (keyed by that hash) miss."""
    from provsubstrate.core import sha256_text

    def bad_render(claim: ProofClaim) -> str:
        return "\n".join([f"import {i}" for i in claim.imports] + ["", f"theorem {claim.theorem_name} : {claim.statement} :=", claim.proof, ""])

    total = failed = 0
    for c in conformance_cases():
        if c["kind"] != "lean_proof_file_hash":
            continue
        total += 1
        exp = compute_expected(c["kind"], c["input"])
        if sha256_text(bad_render(ProofClaim.from_json(c["input"]["claim"]))) != exp["proof_file_hash"]:
            failed += 1
    assert total >= 6 and failed == total


def test_pinned_constants():
    assert TRUSTED_APPROVER["approver_id"] == "pi.ada"
    assert SESSION_ID == "academic-conformance-session"
    assert DATA_AS_OF == "2026-08-17T00:00:00.000Z" and APPROVED_AT == "2026-08-17T12:00:00.000Z"
