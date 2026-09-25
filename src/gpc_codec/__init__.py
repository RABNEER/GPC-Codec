"""
Generalized Patha Codes (GPC-Codec)
===================================
A parameterized placement error-correcting inner code engineered for
channels suffering unmarked deletions, transpositions, and coordinate drift.

Primary Exports:
    - GPCEncoder: High-level encoder for GPC codewords
    - GPCDecoder: High-level decoder for erasures and deletions
    - GeneralizedPathaCode: Parameterized core codec
    - simulate_burst_deletion: Channel simulation for unmarked burst deletions
    - simulate_burst_erasure: Channel simulation for marked erasures
    - simulate_transposition: Channel simulation for coordinate jitter / reordering
    - simulate_mixed_channel: Channel simulation for joint ins/del/sub noise
"""

from gpc.core import GeneralizedPathaCode, GPCEncoder, GPCDecoder
from gpc.decoder import decode_gpc_burst_deletion, decode_gpc_erasure
from gpc.channel import (
    simulate_burst_deletion,
    simulate_burst_erasure,
    simulate_transposition,
    simulate_mixed_channel,
)
from gpc.baselines import (
    build_literal_ghana_placement,
    build_reviewer_baseline_placement,
    build_uniform_interleaved_placement,
)

__version__ = "1.0.1"
__author__ = "Ranveer"
__license__ = "MIT"

__all__ = [
    "GeneralizedPathaCode",
    "GPCEncoder",
    "GPCDecoder",
    "decode_gpc_burst_deletion",
    "decode_gpc_erasure",
    "simulate_burst_deletion",
    "simulate_burst_erasure",
    "simulate_transposition",
    "simulate_mixed_channel",
    "build_literal_ghana_placement",
    "build_reviewer_baseline_placement",
    "build_uniform_interleaved_placement",
]
