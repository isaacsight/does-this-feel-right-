"""The `provsub` CLI and the stdio MCP server, driven as subprocesses.

Every wedge is exercised once through MCP `tools/call` and once through its
CLI; the human gate is exercised end to end (prepare -> `provsub approve`
-> record) against the frozen conformance vectors, so the request hashes
and entry ids the CLI produces are the ones the suites pin. Both
conformance suites are run through the CLI in strict mode.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "src")
EXAMPLES = os.path.join(ROOT, "examples")
FIN_VEC = os.path.join(SRC, "provsubstrate", "conformance", "vectors_finance_v1")
ACA_VEC = os.path.join(SRC, "provsubstrate", "conformance", "vectors_academic_v1")

APPROVED_AT = "2026-08-17T12:00:00.000Z"


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = SRC + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def provsub(*args: str, cwd: str | None = None, check: bool = False) -> subprocess.CompletedProcess:
    p = subprocess.run([sys.executable, "-m", "provsubstrate.cli", *args], capture_output=True, text=True, env=_env(), cwd=cwd or ROOT, check=False)
    if check and p.returncode != 0:
        raise AssertionError(f"provsub {' '.join(args)} failed ({p.returncode}):\n{p.stdout}\n{p.stderr}")
    return p


def provsub_json(*args: str, cwd: str | None = None, expect_rc: int | None = None) -> dict:
    p = provsub(*args, cwd=cwd)
    if expect_rc is not None:
        assert p.returncode == expect_rc, f"rc {p.returncode}: {p.stdout}\n{p.stderr}"
    return json.loads(p.stdout)


def mcp(messages: list[dict]) -> list[dict]:
    lines = "".join(json.dumps(m) + "\n" for m in messages)
    p = subprocess.run([sys.executable, "-m", "provsubstrate.cli", "mcp"], input=lines, capture_output=True, text=True, env=_env(), cwd=ROOT, check=False)
    assert p.returncode == 0, p.stderr
    return [json.loads(line) for line in p.stdout.splitlines() if line.strip()]


def mcp_call(name: str, arguments: dict) -> dict:
    out = mcp(
        [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name, "arguments": arguments}},
        ]
    )
    resp = next(r for r in out if r.get("id") == 2)
    assert "result" in resp, resp
    assert resp["result"]["isError"] is False, resp["result"]
    return json.loads(resp["result"]["content"][0]["text"])


def vector(suite_dir: str, kind: str, cid: str) -> dict:
    with open(os.path.join(suite_dir, kind, cid + ".json"), encoding="utf-8") as f:
        return json.load(f)


def write(path: str, obj) -> str:
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(obj, (bytes, bytearray)):
            f.write(obj.decode("utf-8"))
        elif isinstance(obj, str):
            f.write(obj)
        else:
            json.dump(obj, f, ensure_ascii=False)
    return path


def approve(tmp: str, *, request_hash: str, summary: str, session_id: str, materiality: str, approver_id: str, secret_file: str) -> str:
    """The human's step, as a subprocess."""
    summary_file = write(os.path.join(tmp, "summary.txt"), summary + "\n")
    tok = os.path.join(tmp, "tok.json")
    provsub(
        "approve", "--request-hash", request_hash, "--summary-file", summary_file, "--session-id", session_id, "--materiality", materiality,
        "--approver-id", approver_id, "--secret-file", secret_file, "--approved-at", APPROVED_AT, "--out", tok, check=True,
    )
    return tok


# --- MCP -------------------------------------------------------------------

WEDGE_TOOLS = {
    "finance_reconcile", "finance_prepare_post",
    "lean_check", "lean_prepare",
    "claims_verify", "claims_badge",
    "repro_judge", "repro_dataset_manifest",
    "bench_score", "bench_run", "bench_taskset",
    "review_check", "review_chain_verify",
}
CORE_TOOLS = {"provsub_canonicalize", "provsub_request_hash", "provsub_audit_verify", "provsub_audit_chain"}
NEVER_EXPOSED = {"approve", "provsub_approve", "finance_post", "lean_record", "claims_attest", "repro_record", "review_record"}


def test_mcp_tools_list_has_every_wedge_tool_and_no_minting():
    out = mcp([{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}])
    init = next(r for r in out if r["id"] == 1)
    assert init["result"]["serverInfo"]["name"] == "provenance-substrate"
    tools = next(r for r in out if r["id"] == 2)["result"]["tools"]
    names = {t["name"] for t in tools}
    assert names == CORE_TOOLS | WEDGE_TOOLS
    assert not (names & NEVER_EXPOSED)
    for t in tools:
        assert t["inputSchema"]["type"] == "object"
        assert t["description"]
    # asking for a minting tool by name is refused, not silently ignored
    resp = mcp([{"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"name": "provsub_approve", "arguments": {}}}])[0]
    assert resp["error"]["code"] == -32601


def test_mcp_finance_reconcile_matches_vector():
    v = vector(FIN_VEC, "reconcile", "matched_standard")
    out = mcp_call("finance_reconcile", {"claim": v["input"]["claim"], "bank_lines": v["input"]["bank_lines"], "policy": v["input"]["policy"]})
    assert out["shape"]["ok"]
    assert out["reconciliation"] == v["expected"]
    assert out["approval_summary"].startswith(("SPEND", "RECEIVE"))


def test_mcp_finance_prepare_post_stops_at_gate_with_vector_hash():
    v = vector(FIN_VEC, "ledger_post", "posts_with_valid_approval")
    i = v["input"]
    out = mcp_call(
        "finance_prepare_post",
        {
            "claim": i["claim"], "bank_lines": i["bank_lines"], "policy": i["policy"], "bank_account_code": i["bank_account_code"], "state": i["state"],
            "confidence_floor": i["confidence_floor"], "jurisdiction": i["jurisdiction"], "engine_version": i["engine_version"],
            "session_id": i["session_id"], "data_as_of": i["data_as_of"],
        },
    )
    assert out["ok"] is False and out["stage"] == "approval"
    assert out["request_hash"] == v["expected"]["request_hash"]
    assert out["audit_actions"] == ["extraction_claim", "reconciliation", "verifier_check", "approval_denied"]
    assert out["summary"] and out["materiality"] == "ledger.post"


def test_mcp_lean_prepare_with_stub_table():
    v = vector(ACA_VEC, "lean_record", "clean_valid_approval")
    i = v["input"]
    out = mcp_call("lean_prepare", {"claim": i["claim"], "kernel_table": i["kernel_table"], "data_as_of": i["data_as_of"], "session_id": i["session_id"]})
    assert out["ok"] is True and out["kernel"] == "stub"
    assert out["request_hash"] == v["expected"]["request_hash"]
    assert out["summary"].startswith("Record proof of ")
    assert out["materiality"] == "lean.record"
    # lean_check on raw source with the stub and no table rejects loudly (nothing passes by accident)
    chk = mcp_call("lean_check", {"source": "theorem t : 1 = 1 := by sorry\n", "stub": True})
    assert chk["verdict"]["ok"] is False and chk["static_scan"]["sorries"] == 1


def test_mcp_claims_verify_reexecutes_example_manifest():
    with open(os.path.join(EXAMPLES, "claims", "provenance-manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    out = mcp_call("claims_verify", {"manifest": manifest, "workdir": os.path.join(EXAMPLES, "claims"), "executable_map": {"python3": sys.executable}, "data_as_of": "2026-08-17T00:00:00.000Z"})
    assert out["ok"] is True and out["reexecutor"] == "subprocess"
    assert out["outcomes"][0]["verdict"]["status"] == "confirmed"
    assert out["badge"]["message"].startswith("1/1")
    assert out["summary"].startswith("Attest 1/1 claims confirmed")
    badge = mcp_call("claims_badge", {"report": out["report"]})
    assert badge["svg"].startswith("<svg") and badge["json"]["color"] == "brightgreen"


def test_mcp_repro_judge_matches_vector():
    v = vector(ACA_VEC, "repro_record", "records_with_valid_approval")
    i = v["input"]
    out = mcp_call("repro_judge", {"target": i["target"], "attempt": i["attempt"], "stub": i["stub"], "data_as_of": i["data_as_of"], "session_id": i["session_id"], "confidence_floor": i["confidence_floor"]})
    assert out["ok"] is True and out["verdict"]["overall"] == "reproduced"
    assert out["request_hash"] == v["expected"]["request_hash"]
    assert out["summary"].startswith("Record reproduction of ")


def test_mcp_bench_score_and_run_match_vectors():
    v = vector(ACA_VEC, "bench_score", "hallucinated_previous_total")
    out = mcp_call("bench_score", {"task": v["input"]["task"], "answer": v["input"]["answer"]})
    assert out["score"] == v["expected"]["score"] and out["mitigated"] == v["expected"]["mitigated"]
    r = vector(ACA_VEC, "bench_report_hash", "oracle")
    run = mcp_call("bench_run", {"responder": "oracle", "data_as_of": r["input"]["data_as_of"]})
    assert run["request_hash"] == r["expected"]["request_hash"] and "results" not in run
    ts = mcp_call("bench_taskset", {})
    assert ts["count"] == 60 and ts["taskset_hash"] == run["taskset_hash"]


def test_mcp_review_check_matches_vector_disclosure():
    v = vector(ACA_VEC, "review_disclosure", "undisclosed_scope_none")
    out = mcp_call("review_check", {"submission": v["input"]["submission"]})
    assert out["disclosure"] == v["expected"] and out["ok"] is False
    assert out["report"] is None  # no chain given: rules against the chain are not run
    assert out["summary"].startswith("Record review of ")


# --- CLI: the gate end to end -----------------------------------------------


def test_cli_approve_requires_summary_and_reads_secret_file(tmp_path):
    secret = write(str(tmp_path / "s"), "academic-approver-secret-0001\n")
    p = provsub("approve", "--request-hash", "0" * 64, "--session-id", "s", "--materiality", "m", "--approver-id", "a", "--secret-file", secret, "--approved-at", APPROVED_AT)
    assert p.returncode == 2 and "exactly one of --summary" in p.stderr
    tok = provsub_json("approve", "--request-hash", "0" * 64, "--summary", "line", "--session-id", "s", "--materiality", "m", "--approver-id", "a", "--secret-file", secret, "--approved-at", APPROVED_AT, expect_rc=0)
    from provsubstrate.core import ApprovalRequest, ApprovalToken, verify_approval

    # trailing newline was stripped from the secret file
    assert verify_approval(ApprovalToken.from_json(tok), {"a": b"academic-approver-secret-0001"}, ApprovalRequest("0" * 64, "line", "s", "m")).ok


def test_cli_lean_prepare_approve_record_matches_vector(tmp_path):
    v = vector(ACA_VEC, "lean_record", "clean_valid_approval")
    i = v["input"]
    claim = write(str(tmp_path / "claim.json"), i["claim"])
    table = write(str(tmp_path / "table.json"), i["kernel_table"])
    secret = write(str(tmp_path / "secret"), i["trusted"][0]["secret_utf8"])
    audit = str(tmp_path / "audit.jsonl")
    ledger = str(tmp_path / "ledger.json")
    common = ["--kernel-table", table, "--data-as-of", i["data_as_of"], "--session-id", i["session_id"]]

    prep = provsub_json("lean", "prepare", claim, *common, expect_rc=0)
    assert prep["request_hash"] == v["expected"]["request_hash"] and prep["gate"]["materiality"] == "lean.record"

    # no approval: stops at the gate, audit shows approval_denied, nothing recorded
    denied = provsub_json("lean", "record", claim, *common, "--audit", audit, expect_rc=1)
    assert denied["stage"] == "approval" and denied["audit_actions"][-1] == "approval_denied" and denied["entry_id"] is None

    tok = approve(str(tmp_path), request_hash=prep["request_hash"], summary=prep["summary"], session_id=i["session_id"], materiality="lean.record", approver_id="pi.ada", secret_file=secret)
    # approval without a trust set is refused before anything runs
    p = provsub("lean", "record", claim, *common, "--approval", tok)
    assert p.returncode == 2 and "no trust set" in p.stderr
    rec = provsub_json("lean", "record", claim, *common, "--approval", tok, "--trust", f"pi.ada={secret}", "--audit", audit, "--ledger", ledger, expect_rc=0)
    assert rec["ok"] and rec["entry_id"] == v["expected"]["entry_id"]
    assert rec["audit_actions"] == ["proof_claim", "kernel_verdict", "verifier_check", "approval_granted", "proof_recorded"]
    with open(ledger, encoding="utf-8") as f:
        assert json.load(f)[0]["entry_id"] == v["expected"]["entry_id"]
    # the audit file now holds both runs, chained
    a = provsub("audit", "verify", audit)
    assert a.returncode == 0 and "chain ok" in a.stdout
    with open(audit, encoding="utf-8") as f:
        actions = [json.loads(line)["action"] for line in f if line.strip()]
    assert actions == ["proof_claim", "kernel_verdict", "verifier_check", "approval_denied", "proof_claim", "kernel_verdict", "verifier_check", "approval_granted", "proof_recorded"]


def test_cli_finance_post_matches_vector(tmp_path):
    v = vector(FIN_VEC, "ledger_post", "posts_with_valid_approval")
    i = v["input"]
    claim = write(str(tmp_path / "claim.json"), i["claim"])
    bank = write(str(tmp_path / "bank.json"), i["bank_lines"])
    policy = write(str(tmp_path / "policy.json"), i["policy"])
    state = write(str(tmp_path / "state.json"), i["state"])
    secret = write(str(tmp_path / "secret"), i["trusted"][0]["secret_utf8"])
    common = [
        "--policy", policy, "--state", state, "--bank-account-code", i["bank_account_code"], "--jurisdiction", i["jurisdiction"],
        "--session-id", i["session_id"], "--data-as-of", i["data_as_of"],
    ]
    rec = provsub_json("finance", "reconcile", claim, bank, "--policy", policy, expect_rc=0)
    assert rec["reconciliation"]["status"] == "matched"
    prep = provsub_json("finance", "post", claim, bank, *common, expect_rc=1)
    assert prep["stage"] == "approval" and prep["request_hash"] == v["expected"]["request_hash"]
    tok = approve(str(tmp_path), request_hash=prep["request_hash"], summary=prep["summary"], session_id=i["session_id"], materiality="ledger.post", approver_id=i["trusted"][0]["approver_id"], secret_file=secret)
    posted = str(tmp_path / "posted.json")
    out = provsub_json("finance", "post", claim, bank, *common, "--approval", tok, "--trust", f"{i['trusted'][0]['approver_id']}={secret}", "--posted-out", posted, expect_rc=0)
    assert out["ok"] and out["response"]["value"]["entry_id"] == v["expected"]["posted_entry_id"]
    assert out["response"]["value"]["total"] == v["expected"]["posted_total"]
    assert out["audit_actions"] == v["expected"]["audit_actions"]
    assert os.path.exists(posted)


def test_cli_claims_verify_and_attest_example(tmp_path):
    manifest = os.path.join(EXAMPLES, "claims", "provenance-manifest.json")
    workdir = os.path.join(EXAMPLES, "claims")
    args = ["--workdir", workdir, "--map", f"python3={sys.executable}", "--data-as-of", "2026-08-17T00:00:00.000Z"]
    summary_file = str(tmp_path / "summary.txt")
    v = provsub_json("claims", "verify", manifest, *args, "--summary-out", summary_file, expect_rc=0)
    assert v["ok"] and v["outcomes"][0]["verdict"]["status"] == "confirmed"
    with open(summary_file, encoding="utf-8") as f:
        assert f.read() == v["summary"] + "\n"
    svg = provsub("claims", "badge", manifest, "--svg", *args)
    assert svg.returncode == 0 and svg.stdout.startswith("<svg")
    secret = write(str(tmp_path / "secret"), "s3")
    tok = approve(str(tmp_path), request_hash=v["request_hash"], summary=v["summary"], session_id="provsub-cli", materiality="claims.attest", approver_id="author.x", secret_file=secret)
    ledger = str(tmp_path / "attestations.json")
    out = provsub_json("claims", "attest", manifest, *args, "--approval", tok, "--trust", f"author.x={secret}", "--ledger", ledger, expect_rc=0)
    assert out["ok"] and out["audit_actions"] == ["claim_extraction", "reexecution", "verifier_check", "approval_granted", "attestation_recorded"]
    with open(ledger, encoding="utf-8") as f:
        assert json.load(f)[0]["entry_id"] == out["entry_id"]


def test_cli_repro_judge_record_export(tmp_path):
    v = vector(ACA_VEC, "repro_record", "records_with_valid_approval")
    i = v["input"]
    target = write(str(tmp_path / "target.json"), i["target"])
    attempt = write(str(tmp_path / "attempt.json"), i["attempt"])
    stub = write(str(tmp_path / "stub.json"), i["stub"])
    secret = write(str(tmp_path / "secret"), i["trusted"][0]["secret_utf8"])
    common = ["--stub", stub, "--data-as-of", i["data_as_of"], "--session-id", i["session_id"]]
    j = provsub_json("repro", "judge", target, attempt, *common, expect_rc=0)
    assert j["request_hash"] == v["expected"]["request_hash"] and j["verdict"]["overall"] == "reproduced"
    tok = approve(str(tmp_path), request_hash=j["request_hash"], summary=j["summary"], session_id=i["session_id"], materiality="repro.report", approver_id="pi.ada", secret_file=secret)
    report = str(tmp_path / "report.json")
    r = provsub_json("repro", "record", target, attempt, *common, "--approval", tok, "--trust", f"pi.ada={secret}", "--report-out", report, expect_rc=0)
    assert r["report_id"] == v["expected"]["report_id"]
    jsonl, manifest, zenodo, croissant = (str(tmp_path / n) for n in ("ds.jsonl", "m.json", "z.json", "c.json"))
    e = provsub_json("repro", "export", report, "--version", "1.0.0", "--jsonl", jsonl, "--manifest", manifest, "--zenodo", zenodo, "--croissant", croissant, "--creator", "Ada|Kernel", expect_rc=0)
    assert e["row_count"] == 1
    with open(manifest, encoding="utf-8") as f:
        m = json.load(f)
    assert m["rows"][0]["report_id"] == v["expected"]["report_id"]
    with open(zenodo, encoding="utf-8") as f:
        assert json.load(f)["metadata"]["creators"] == [{"name": "Ada", "affiliation": "Kernel"}]
    with open(croissant, encoding="utf-8") as f:
        assert json.load(f)["distribution"][0]["sha256"] == m["distribution"]["sha256"]


def test_cli_bench_run_and_taskset():
    r = vector(ACA_VEC, "bench_report_hash", "distractor_seed_7")
    out = provsub_json("bench", "run", "--responder", "distractor:7", "--rate", "0.5", expect_rc=0)
    assert out["request_hash"] == r["expected"]["request_hash"] and out["totals"] == r["expected"]["totals"]
    md = provsub("bench", "run", "--responder", "null", "--markdown")
    assert md.returncode == 0 and md.stdout.startswith("# Quantitative hallucination benchmark")
    h = provsub("bench", "taskset", "--hash")
    assert h.stdout.strip() == out["taskset_hash"]


def test_cli_review_open_check_record(tmp_path):
    v = vector(ACA_VEC, "review_record", "records_clean_disclosed")
    i = v["input"]
    manuscript = write(str(tmp_path / "m.json"), i["manuscript"])
    sub = write(str(tmp_path / "sub.json"), i["submission"])
    secret = write(str(tmp_path / "secret"), i["trusted"][0]["secret_utf8"])
    chain = str(tmp_path / "chain.json")
    provsub("review", "open", manuscript, "--actor", i["opened_by"], "--at", i["opened_at"], "--session-id", i["session_id"], "--out", chain, check=True)
    common = ["--data-as-of", i["data_as_of"], "--session-id", i["session_id"]]
    c = provsub_json("review", "check", sub, "--chain", chain, *common, expect_rc=0)
    assert c["ok"] and c["request_hash"] == v["expected"]["request_hash"] and c["report"]["ok"]
    tok = approve(str(tmp_path), request_hash=c["request_hash"], summary=c["summary"], session_id=i["session_id"], materiality="review.record", approver_id="pi.ada", secret_file=secret)
    receipt = str(tmp_path / "receipt.json")
    r = provsub_json("review", "record", sub, chain, *common, "--approval", tok, "--trust", f"pi.ada={secret}", "--receipt-out", receipt, expect_rc=0)
    assert r["entry_id"] == v["expected"]["entry_id"]
    ver = provsub_json("review", "verify", chain, expect_rc=0)
    assert ver["verdict"]["ok"] and ver["length"] == 2 and ver["reviews"][0]["reviewer_id"] == i["submission"]["reviewer_id"]
    with open(receipt, encoding="utf-8") as f:
        assert json.load(f)["entry_id"] == v["expected"]["entry_id"]
    # the same reviewer, same round, again: DUPLICATE_REVIEW at the verifier
    dup = provsub_json("review", "check", sub, "--chain", chain, *common, expect_rc=1)
    assert any(ch.get("code") == "DUPLICATE_REVIEW" for ch in dup["report"]["checks"])


# --- CLI: conformance suites ----------------------------------------------


@pytest.mark.parametrize("suite", ["finance-v1", "academic-v1"])
def test_cli_conformance_strict(suite):
    p = provsub("conformance", suite, "--strict")
    assert p.returncode == 0, p.stdout + p.stderr
    assert "passed" in p.stdout and "manifest ok" in p.stdout


def test_cli_conformance_check_no_drift():
    p = provsub("conformance", "--check")
    assert p.returncode == 0 and "no drift" in p.stdout


def test_cli_help_lists_every_wedge():
    p = provsub("--help")
    for w in ("finance", "lean", "claims", "repro", "bench", "review", "approve", "mcp", "conformance"):
        assert w in p.stdout
