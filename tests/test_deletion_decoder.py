"""
Unit tests for GPC Unmarked Burst-Deletion Decoding
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

def test_burst_deletion_recovery():
    codec = GeneralizedPathaCode(K=4)
    msg = (1, 0, 1, 1)
    cw = codec.encode(msg)
    
    # Test b = 5 burst deletion across various cut positions
    b = 5
    for s in [0, 12, 25, 40]:
        shortened = cw[:s] + cw[s+b:]
        recovered = codec.decode(shortened)
        assert recovered == msg
