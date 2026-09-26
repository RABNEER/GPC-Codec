"""
Formal verification of theoretical theorems
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

def test_theorem_1_exact_formulas_and_asymptotic_bound():
    """Verify Theorem 1: M = 13K + 6 and B_E = 10K + 7 (for K >= 3), asymptotic ratio 10/13"""
    for K in [3, 4, 6, 8, 16, 32]:
        codec = GeneralizedPathaCode(K=K)
        assert codec.M == 13 * K + 6, f"Block length mismatch for K={K}: {codec.M} != {13*K+6}"
        assert codec.BE == 10 * K + 7, f"BE mismatch for K={K}: {codec.BE} != {10*K+7}"
        ratio = codec.BE / codec.M
        assert ratio >= 10 / 13, f"Asymptotic ratio violation for K={K}: {ratio} < 10/13"
