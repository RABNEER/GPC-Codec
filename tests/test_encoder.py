"""
Unit tests for GPC Encoder
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

def test_codeword_length():
    for K in [4, 6, 8]:
        codec = GeneralizedPathaCode(K=K)
        assert codec.M == 13 * K + 6
        msg = [1] * K
        cw = codec.encode(msg)
        assert len(cw) == codec.M

def test_pilot_positions():
    codec = GeneralizedPathaCode(K=4)
    cw = codec.encode([0, 0, 0, 0])
    for p in codec.pilots:
        assert cw[p] == 1
