-- A trivial theorem the core Lean kernel checks without Mathlib.
-- Rendered by `provsubstrate.lean.render_lean_file` from the claim in
-- examples/lean/claim.json; the SHA-256 of this file's bytes is what the
-- proof ledger records.
theorem add_zero_nat : ∀ n : Nat, n + 0 = n := by
  intro n
  rfl
