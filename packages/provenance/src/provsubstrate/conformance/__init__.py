import os

from .runner import ConformanceReport, VectorResult, run_conformance, load_vectors, expect_equal, json_equal, suite_hash_of
from .core_kinds import CORE_HANDLERS

FINANCE_V1_DIR = os.path.join(os.path.dirname(__file__), "vectors_finance_v1")
ACADEMIC_V1_DIR = os.path.join(os.path.dirname(__file__), "vectors_academic_v1")

__all__ = [
    "ConformanceReport", "VectorResult", "run_conformance", "load_vectors", "expect_equal", "json_equal", "suite_hash_of",
    "CORE_HANDLERS", "FINANCE_V1_DIR", "ACADEMIC_V1_DIR",
]
