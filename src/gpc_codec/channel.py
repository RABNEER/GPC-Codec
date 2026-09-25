"""
Channel simulation module alias.
"""
from gpc.channel import (
    simulate_burst_deletion,
    simulate_burst_erasure,
    simulate_transposition,
    simulate_mixed_channel,
)

__all__ = [
    "simulate_burst_deletion",
    "simulate_burst_erasure",
    "simulate_transposition",
    "simulate_mixed_channel",
]
