"""
DNA Storage Integration Example
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

codec = GeneralizedPathaCode(K=4)
nibble = [1, 1, 0, 1]
cw = codec.encode(nibble)

# Simple quaternary base mapping
BASES = ["A", "C", "G", "T"]
oligo = "".join(BASES[(cw[i] << 1) | cw[i+1]] for i in range(0, len(cw), 2))
print(f"Protected Oligo ({len(oligo)} nt): {oligo}")
