"""
GPC Quickstart Example
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

# 1. Initialize codec for 4-bit message
codec = GeneralizedPathaCode(K=4)
print(f"Initialized GPC Codec: K={codec.K}, Block Length M={codec.M}, Rate R={codec.rate:.4f}")

# 2. Encode binary payload
message = [1, 0, 1, 1]
codeword = codec.encode(message)
print(f"Original Message: {message}")
print(f"Encoded Codeword (58 bits): {''.join(map(str, codeword))}")

# 3. Simulate severe 10-bit burst deletion
b = 10
cut_start = 18
received = codeword[:cut_start] + codeword[cut_start + b:]
print(f"Received Vector ({len(received)} bits, cut at {cut_start}): {''.join(map(str, received))}")

# 4. Decode in linear time O(M)
decoded = codec.decode(received)
print(f"Decoded Output:   {list(decoded)}")
assert list(decoded) == message
print(">> 100% BIT-EXACT RECONSTRUCTION SUCCESSFUL!")
