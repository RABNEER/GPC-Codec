"""
Deterministic Linear-Time Decoder Implementations for GPC
"""

from typing import List, Tuple, Optional
from collections import defaultdict

def decode_gpc_erasure(
    received_with_erasures: List[Optional[int]],
    placement: List[int],
    K: int
) -> Optional[Tuple[int, ...]]:
    """O(M) Linear-time majority voting decoder for marked erasures."""
    votes = defaultdict(list)
    for idx, bit in enumerate(received_with_erasures):
        if bit is not None:
            sym = placement[idx]
            if sym > 0:
                votes[sym].append(bit)
    decoded = []
    for sym in range(1, K + 1):
        v = votes[sym]
        if not v:
            return None
        ones = sum(v)
        zeros = len(v) - ones
        decoded.append(1 if ones >= zeros else 0)
    return tuple(decoded)

def decode_gpc_burst_deletion(
    rx_bits: Tuple[int, ...],
    b_len: int,
    K: int,
    placement: List[int],
    pilots: List[int]
) -> Optional[Tuple[int, ...]]:
    """
    Algorithm 1: Two-Phase Greedy Alignment with Consensus Margin Voting.
    Evaluates candidate burst cut positions s in [0, M - b] and resolves
    hypotheses via consensus confidence margin.
    """
    M = len(placement)
    best_s_candidates = []
    best_score = -1

    for s_cand in range(M - b_len + 1):
        score = 0
        for p in pilots:
            if p < s_cand:
                idx = p
            elif p >= s_cand + b_len:
                idx = p - b_len
            else:
                continue
            if idx < len(rx_bits) and rx_bits[idx] == 1:
                score += 1
        if score > best_score:
            best_score = score
            best_s_candidates = [s_cand]
        elif score == best_score:
            best_s_candidates.append(s_cand)

    best_margin = -1
    best_decoded = None

    for s_hat in best_s_candidates:
        full_aligned = list(rx_bits[:s_hat]) + [None] * b_len + list(rx_bits[s_hat:])
        votes = {sym: [] for sym in range(1, K + 1)}
        for idx, sym in enumerate(placement):
            if sym > 0 and full_aligned[idx] is not None:
                votes[sym].append(full_aligned[idx])

        candidate_msg = []
        margin_sum = 0
        valid = True
        for sym in range(1, K + 1):
            v = votes[sym]
            if not v:
                valid = False
                break
            ones = sum(v)
            zeros = len(v) - ones
            candidate_msg.append(1 if ones >= zeros else 0)
            margin_sum += abs(ones - zeros)

        if valid and margin_sum > best_margin:
            best_margin = margin_sum
            best_decoded = tuple(candidate_msg)

    return best_decoded
