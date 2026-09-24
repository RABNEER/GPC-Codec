"""
Generalized Patha Codes (GPC) Python Codec Library
===================================================
A parameterized placement error-correcting inner code engineered for
channels suffering unmarked deletions and coordinate drift.
"""

from .core import GeneralizedPathaCode
from .decoder import decode_gpc_burst_deletion, decode_gpc_erasure
from .baselines import (
    build_literal_ghana_placement,
    build_reviewer_baseline_placement,
    build_uniform_interleaved_placement
)

__version__ = "1.0.0"
__all__ = [
    "GeneralizedPathaCode",
    "decode_gpc_burst_deletion",
    "decode_gpc_erasure",
    "build_literal_ghana_placement",
    "build_reviewer_baseline_placement",
    "build_uniform_interleaved_placement",
]
