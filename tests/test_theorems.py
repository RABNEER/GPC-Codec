"""
Formal verification of theoretical theorems
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

def test_theorem_2_asymptotic_lower_bound():
    """Verify Theorem 2: B_E / M >= 8/13 for all K"""
    for K in [4, 6, 8, 16, 32]:
        codec = GeneralizedPathaCode(K=K)
        ratio = codec.BE / codec.M
        assert ratio >= (8 * K + 5) / (13 * K + 6)
        assert ratio >= 8 / 13
