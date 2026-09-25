"""
Generalized Patha Codes (GPC) Python Codec Library
===================================================
A parameterized placement error-correcting inner code engineered for
channels suffering unmarked deletions and coordinate drift.
"""

from .core import GeneralizedPathaCode, GPCEncoder, GPCDecoder
from .decoder import decode_gpc_burst_deletion, decode_gpc_erasure
from .channel import (
    simulate_burst_deletion,
    simulate_burst_erasure,
    simulate_transposition,
    simulate_mixed_channel,
)
from .baselines import (
    build_literal_ghana_placement,
    build_reviewer_baseline_placement,
    build_uniform_interleaved_placement,
)

__version__ = "1.0.1"
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
