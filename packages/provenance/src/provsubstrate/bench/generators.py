"""Deterministic task generators and the fixed ``taskset_v1``.

Randomness comes only from a tiny internal LCG seeded by an explicit
argument — never from ``random``'s global state — so the same seed yields
the same tasks on any host, and the shipped task set has one hash. Money is
generated in integer cents and rendered with two decimals so no float noise
leaks into ground truth. ``default_recompute`` is the deterministic code the
substrate would run instead of trusting the model's number: it re-derives
the answer from the source text alone.
"""

from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional, Sequence, Tuple

from .model import GroundTruth, Task, TaskSet


class Lcg:
    """Numerical Recipes LCG, 32-bit. Small, portable, explicit."""

    A = 1664525
    C = 1013904223
    M = 1 << 32

    def __init__(self, seed: int):
        self.state = int(seed) % Lcg.M

    def next(self) -> int:
        self.state = (Lcg.A * self.state + Lcg.C) % Lcg.M
        return self.state

    def randint(self, lo: int, hi: int) -> int:
        """Inclusive both ends."""
        return lo + (self.next() >> 8) % (hi - lo + 1)

    def choice(self, seq: Sequence):
        return seq[self.randint(0, len(seq) - 1)]


def cents_to_float(c: int) -> float:
    return float(Decimal(c) / Decimal(100))


def fmt_cents(c: int) -> str:
    sign = "-" if c < 0 else ""
    c = abs(c)
    return f"{sign}{c // 100}.{c % 100:02d}"


def _dedupe(values: Sequence[float], exclude: float) -> List[float]:
    out: List[float] = []
    for v in values:
        if v != exclude and v not in out:
            out.append(v)
    return out


VENDORS = ("Northwind Supply", "Ag Supply Co", "Harbor Print Works", "Meridian Labs", "Copperline Tools")
ITEMS = ("Widget A", "Bracket set", "Toner cartridge", "Cable 3m", "Field notebook", "Calibration kit", "Filter pack", "Label roll")
TAX_RATES = (5, 8, 10)


def gen_invoice_tasks(seed: int, n: int) -> List[Task]:
    """Invoices with 2-4 line items, subtotal, tax, total, and a 'previous
    statement total' that is off by a dollar or a dime — the classic misread.
    Half the tasks ask for the total, half for one line's amount."""
    rng = Lcg(seed)
    tasks: List[Task] = []
    for i in range(n):
        vendor = rng.choice(VENDORS)
        n_lines = rng.randint(2, 4)
        lines: List[Tuple[str, int, int, int]] = []
        used = set()
        for _ in range(n_lines):
            item = rng.choice(ITEMS)
            while item in used:
                item = rng.choice(ITEMS)
            used.add(item)
            qty = rng.randint(1, 9)
            unit = rng.randint(150, 9999)
            lines.append((item, qty, unit, qty * unit))
        subtotal = sum(ln[3] for ln in lines)
        rate = rng.choice(TAX_RATES)
        tax = (subtotal * rate + 50) // 100
        total = subtotal + tax
        prev = total + rng.choice((100, -100, 10, -10, 1))
        inv_no = 1000 + rng.randint(0, 8999)
        day = rng.randint(1, 28)
        month = rng.randint(1, 12)
        text_lines = [f"INVOICE INV-{inv_no}", f"Vendor: {vendor}", f"Date: 2026-{month:02d}-{day:02d}"]
        for k, (item, qty, unit, amt) in enumerate(lines, start=1):
            text_lines.append(f"Line {k}: {item} x {qty} @ {fmt_cents(unit)} = {fmt_cents(amt)}")
        text_lines += [
            f"Subtotal: {fmt_cents(subtotal)}",
            f"Tax ({rate}%): {fmt_cents(tax)}",
            f"Total due: {fmt_cents(total)}",
            f"Previous statement total: {fmt_cents(prev)}",
        ]
        text = "\n".join(text_lines) + "\n"
        if i % 2 == 0:
            gt = GroundTruth(cents_to_float(total), "USD", 0.005)
            distractors = _dedupe(
                [cents_to_float(prev), cents_to_float(subtotal), cents_to_float(tax)] + [cents_to_float(ln[3]) for ln in lines], gt.value
            )
            tasks.append(Task.create("finance", text, "What is the total due on this invoice, in USD?", gt, distractors, {"kind": "invoice_total"}))
        else:
            k = rng.randint(1, n_lines)
            item, qty, unit, amt = lines[k - 1]
            gt = GroundTruth(cents_to_float(amt), "USD", 0.005)
            distractors = _dedupe(
                [cents_to_float(unit), cents_to_float(total), cents_to_float(subtotal)] + [cents_to_float(ln[3]) for ln in lines], gt.value
            )
            tasks.append(
                Task.create("finance", text, f"What is the line amount for line {k} ({item}), in USD?", gt, distractors, {"kind": "invoice_line", "line": k})
            )
    return tasks


REGIONS = ("North", "South", "East", "West", "Central", "Coastal", "Highland", "Metro")
COLUMNS = (("units", 20, 400), ("revenue", 900, 9900), ("returns", 0, 60), ("visits", 100, 5000))
AGGS = ("sum", "mean", "max")


def _mean2(values: Sequence[int]) -> float:
    return float((Decimal(sum(values)) / Decimal(len(values))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _agg(values: Sequence[int], agg: str) -> float:
    if agg == "sum":
        return float(sum(values))
    if agg == "max":
        return float(max(values))
    if agg == "mean":
        return _mean2(values)
    raise ValueError(agg)


def gen_table_tasks(seed: int, n: int) -> List[Task]:
    """Small CSV tables with two numeric columns; ask sum, mean or max of
    one. Distractors: the same aggregate over the other column, the other
    aggregates over the asked column, and a cell value."""
    rng = Lcg(seed)
    tasks: List[Task] = []
    for _ in range(n):
        rows = rng.randint(4, 6)
        c1 = rng.choice(COLUMNS)
        c2 = rng.choice(COLUMNS)
        while c2[0] == c1[0]:
            c2 = rng.choice(COLUMNS)
        regs: List[str] = []
        while len(regs) < rows:
            r = rng.choice(REGIONS)
            if r not in regs:
                regs.append(r)
        v1 = [rng.randint(c1[1], c1[2]) for _ in range(rows)]
        v2 = [rng.randint(c2[1], c2[2]) for _ in range(rows)]
        text = f"region,{c1[0]},{c2[0]}\n" + "\n".join(f"{regs[i]},{v1[i]},{v2[i]}" for i in range(rows)) + "\n"
        ask_first = rng.randint(0, 1) == 0
        col, vals, other_vals = (c1[0], v1, v2) if ask_first else (c2[0], v2, v1)
        agg = rng.choice(AGGS)
        gt_value = _agg(vals, agg)
        gt = GroundTruth(gt_value, "count" if col != "revenue" else "USD", 0.005 if agg == "mean" else 0)
        distractors = _dedupe(
            [_agg(other_vals, agg)] + [_agg(vals, a) for a in AGGS if a != agg] + [float(vals[0])], gt_value
        )
        q = {"sum": f"What is the sum of the {col} column?", "mean": f"What is the mean of the {col} column, to two decimals?", "max": f"What is the maximum value in the {col} column?"}[agg]
        tasks.append(Task.create("table", text, q, gt, distractors, {"kind": "table_agg", "column": col, "agg": agg}))
    return tasks


OPS = ("+", "-", "*")


def gen_arithmetic_tasks(seed: int, n: int) -> List[Task]:
    """Integer arithmetic. Distractors are the operands and the off-by-one
    neighbours of the result — the near-misses a model produces."""
    rng = Lcg(seed)
    tasks: List[Task] = []
    for _ in range(n):
        op = rng.choice(OPS)
        if op == "*":
            a, b = rng.randint(12, 99), rng.randint(12, 99)
        else:
            a, b = rng.randint(100, 9999), rng.randint(100, 9999)
        if op == "-" and b > a:
            a, b = b, a
        result = {"+": a + b, "-": a - b, "*": a * b}[op]
        text = f"a = {a}\nb = {b}\nexpression: a {op} b\n"
        gt = GroundTruth(float(result), "integer", 0)
        distractors = _dedupe([float(a), float(b), float(result + 1), float(result - 1)], gt.value)
        tasks.append(Task.create("math", text, f"Compute a {op} b.", gt, distractors, {"kind": "arithmetic"}))
    return tasks


COMPANIES = ("Acme Holdings", "Bramble Foods", "Cobalt Systems", "Delta Marine", "Everly Health")


def gen_pdf_text_tasks(seed: int, n: int) -> List[Task]:
    """A prose paragraph (as extracted from a PDF) with several figures in
    it; ask for the sum of two of them. Distractors are the other figures."""
    rng = Lcg(seed)
    tasks: List[Task] = []
    for _ in range(n):
        co = rng.choice(COMPANIES)
        h1 = rng.randint(50, 400)  # tenths of a million
        h2 = rng.randint(50, 400)
        opex = rng.randint(30, 300)
        head = rng.randint(80, 900)
        year = rng.randint(2022, 2026)

        def m(t: int) -> str:
            return f"{t // 10}.{t % 10}"

        text = (
            f"In fiscal {year}, {co} reported revenue of {m(h1)} million in the first half and {m(h2)} million in the second half. "
            f"Operating expenses were {m(opex)} million for the year. Headcount grew to {head} by year end.\n"
        )
        total = h1 + h2
        gt = GroundTruth(float(Decimal(total) / Decimal(10)), "million USD", 0.05)
        distractors = _dedupe([float(Decimal(h1) / 10), float(Decimal(h2) / 10), float(Decimal(opex) / 10), float(head)], gt.value)
        tasks.append(
            Task.create(
                "pdf_text", text, f"What was {co}'s total revenue for fiscal {year}, in millions of USD?", gt, distractors,
                {"kind": "regex_sum", "pattern": r"revenue of ([0-9.]+) million|and ([0-9.]+) million in the second half"},
            )
        )
    return tasks


TASKSET_V1_NAME = "quant-hallucination"
TASKSET_V1_VERSION = "1.0.0"
TASKSET_V1_PLAN = (("invoice", 101, 20), ("table", 202, 15), ("arithmetic", 303, 15), ("pdf_text", 404, 10))


def taskset_v1() -> TaskSet:
    """The fixed shipped set: 60 tasks across four domains, one hash."""
    gens = {"invoice": gen_invoice_tasks, "table": gen_table_tasks, "arithmetic": gen_arithmetic_tasks, "pdf_text": gen_pdf_text_tasks}
    tasks: List[Task] = []
    for name, seed, n in TASKSET_V1_PLAN:
        tasks.extend(gens[name](seed, n))
    return TaskSet(TASKSET_V1_NAME, TASKSET_V1_VERSION, tuple(tasks))


# ---- the substrate's recompute ------------------------------------------

_LINE_RX = re.compile(r"^Line (\d+): .* x (\d+) @ ([0-9]+\.[0-9]{2}) = ([0-9]+\.[0-9]{2})$", re.MULTILINE)
_TAX_RX = re.compile(r"^Tax \((\d+)%\): ([0-9]+\.[0-9]{2})$", re.MULTILINE)


def _cents(s: str) -> int:
    whole, frac = s.split(".")
    return int(whole) * 100 + int(frac)


def default_recompute(task: Task) -> Optional[float]:
    """Deterministic re-derivation of the answer from ``source_text`` alone,
    driven by ``recompute_spec``. Returns ``None`` when the spec is unknown
    or the text does not parse — the substrate abstains rather than guesses."""
    spec = task.recompute_spec
    kind = spec.get("kind")
    text = task.source_text
    if kind == "invoice_total":
        lines = _LINE_RX.findall(text)
        tax = _TAX_RX.search(text)
        if not lines or not tax:
            return None
        subtotal = sum(int(q) * _cents(u) for _, q, u, _ in lines)
        return cents_to_float(subtotal + _cents(tax.group(2)))
    if kind == "invoice_line":
        for num, q, u, _ in _LINE_RX.findall(text):
            if int(num) == int(spec.get("line", -1)):
                return cents_to_float(int(q) * _cents(u))
        return None
    if kind == "table_agg":
        rows = [r.split(",") for r in text.strip().split("\n")]
        if len(rows) < 2:
            return None
        header = rows[0]
        col = spec.get("column")
        if col not in header:
            return None
        idx = header.index(col)
        try:
            vals = [int(r[idx]) for r in rows[1:]]
        except (ValueError, IndexError):
            return None
        try:
            return _agg(vals, spec.get("agg", ""))
        except ValueError:
            return None
    if kind == "arithmetic":
        m = re.search(r"a = (-?\d+)\nb = (-?\d+)\nexpression: a ([+\-*]) b", text)
        if not m:
            return None
        a, b, op = int(m.group(1)), int(m.group(2)), m.group(3)
        return float({"+": a + b, "-": a - b, "*": a * b}[op])
    if kind == "regex_sum":
        try:
            rx = re.compile(spec.get("pattern", ""))
        except re.error:
            return None
        total = Decimal(0)
        found = False
        for m in rx.finditer(text):
            for g in m.groups():
                if g is not None:
                    total += Decimal(g)
                    found = True
        return float(total) if found else None
    return None
