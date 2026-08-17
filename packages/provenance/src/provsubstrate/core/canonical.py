"""Canonical JSON, byte-compatible with the kbot-finance reference (TypeScript).

The reference is RFC 8785 JCS simplified: object keys sorted, numbers in the
shortest round-trip form *as JavaScript prints them*, strings escaped the way
``JSON.stringify`` escapes them. Two implementations that disagree on a single
byte here produce different hashes everywhere above, so this module is the
foundation the conformance vectors pin first.

JavaScript number formatting is reproduced from ECMA-262 Number::toString:
integral values below 1e21 print without a decimal point or exponent;
exponent form is used for magnitudes >= 1e21 or < 1e-6; the exponent has an
explicit sign and no zero padding (``1e-7``, ``1e+21``).
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from typing import Any

JsonValue = Any  # str | int | float | bool | None | list | dict


class CanonicalizeError(ValueError):
    pass


def _js_number(x: int | float) -> str:
    if isinstance(x, bool):  # bool is an int subclass; guard against misuse
        raise CanonicalizeError("bool passed as number")
    if isinstance(x, int):
        return str(x)
    if not math.isfinite(x):
        raise CanonicalizeError(f"canonicalize: non-finite number is not representable: {x}")
    if x == 0:
        return "0"  # covers -0.0: JSON.stringify(-0) === "0"
    # Shortest round-trip digits from repr (Python and V8 both use the
    # shortest-digits algorithm), then re-lay them out per ECMA-262.
    _, dtuple, dexp = Decimal(repr(abs(x))).as_tuple()
    dlist = list(dtuple)
    while len(dlist) > 1 and dlist[-1] == 0:
        dlist.pop()
        dexp += 1
    digits = "".join(str(d) for d in dlist)
    k = len(digits)
    n = k + dexp  # value = 0.d1...dk * 10^n
    sign = "-" if x < 0 else ""
    if k <= n <= 21:
        s = digits + "0" * (n - k)
    elif 0 < n <= 21:
        s = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        s = "0." + "0" * (-n) + digits
    else:
        e = n - 1
        es = ("+" if e >= 0 else "-") + str(abs(e))
        s = digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + es
    return sign + s


def _js_string(s: str) -> str:
    # json.dumps with ensure_ascii=False escapes exactly what JSON.stringify
    # escapes: quote, backslash, and control characters below U+0020.
    return json.dumps(s, ensure_ascii=False)


def _sort_key(k: str) -> tuple:
    # JavaScript sorts keys by UTF-16 code units. Python sorts by code point.
    # They differ only for astral characters vs. U+E000..U+FFFF; encode to
    # UTF-16 to match exactly.
    return tuple(k.encode("utf-16-be"))


def canonicalize(value: JsonValue) -> str:
    """Return the canonical JSON string for ``value``."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return _js_number(value)
    if isinstance(value, str):
        return _js_string(value)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(canonicalize(v) for v in value) + "]"
    if isinstance(value, dict):
        parts = []
        for k in sorted(value.keys(), key=_sort_key):
            if not isinstance(k, str):
                raise CanonicalizeError(f"canonicalize: non-string key {k!r}")
            parts.append(_js_string(k) + ":" + canonicalize(value[k]))
        return "{" + ",".join(parts) + "}"
    raise CanonicalizeError(f"canonicalize: unsupported type {type(value).__name__}")


def canonical_bytes(value: JsonValue) -> bytes:
    return canonicalize(value).encode("utf-8")
