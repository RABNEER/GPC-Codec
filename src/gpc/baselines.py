"""
Historical and Matched Classical Baseline Generators
"""

from typing import List

def build_literal_ghana_placement(K: int) -> List[int]:
    """Literal boundary-pinned Vedic Ghana recitation placement."""
    placement = []
    for i in range(1, K):
        p1 = [i, i+1]
        p2 = [i+1, i]
        p3 = [i, i+1]
        if i + 2 <= K:
            p3.append(i+2)
        p4 = list(reversed(p3))
        p5 = list(p3)
        placement.extend(p1 + p2 + p3 + p4 + p5)
    return placement

def build_reviewer_baseline_placement(K: int) -> List[int]:
    """Single-burst optimal repetition baseline: c(x) = x || 111111 || x^12."""
    placement = []
    placement.extend(list(range(1, K + 1)))
    placement.extend([0] * 6)
    for _ in range(12):
        placement.extend(list(range(1, K + 1)))
    return placement

def build_uniform_interleaved_placement(K: int) -> List[int]:
    """Uniform cyclic interleaving baseline: 13 passes of (1..K) + 6 pilots at end."""
    placement = []
    for _ in range(13):
        placement.extend(list(range(1, K + 1)))
    placement.extend([0] * 6)
    return placement
