"""
Unit tests for GPC Marked Burst-Erasure Decoding
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

def test_erasure_recovery():
    K = 4
    codec = GeneralizedPathaCode(K=K)
    msg = (1, 0, 1, 0)
    cw = codec.encode(msg)
    
    # Inject burst erasure of length L = BE = 47
    L = codec.BE
    for s in [0, 5, 10]:
        rx = list(cw)
        for i in range(s, s + L):
            rx[i] = None
        decoded = codec.decode(rx)
        assert decoded == msg
