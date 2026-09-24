"""
UAV Swarm Stateless Heartbeat Telemetry Example
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

codec = GeneralizedPathaCode(K=6)
# Velocity vector quantized to 6 bits
v_state = [1, 0, 1, 1, 0, 0]
frame = codec.encode(v_state)
print(f"Broadcast Frame (84 bits): {''.join(map(str, frame))}")
