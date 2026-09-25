"""
Constrained DNA Codec (BC-DNA) Package
======================================
Implements RLL-2 / GC-balanced constrained coding for DNA data storage,
Goldman (2013) ternary differential baselines, and nanopore channel models.
"""

from .codec import (
    BCDNACodec,
    NaiveDirectCodec,
    GoldmanNature2013Codec,
    generate_rll2_codebook,
)
from .channel import (
    NanoporeChannel,
)

# Friendly aliases
ConstrainedDNACodec = BCDNACodec
Goldman2013Codec = GoldmanNature2013Codec

__all__ = [
    "BCDNACodec",
    "ConstrainedDNACodec",
    "NaiveDirectCodec",
    "GoldmanNature2013Codec",
    "Goldman2013Codec",
    "generate_rll2_codebook",
    "NanoporeChannel",
]
