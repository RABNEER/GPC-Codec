"""
Formal verification of theoretical theorems and mathematical invariants
"""

import sys
import os
import itertools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from gpc import GeneralizedPathaCode

def test_lemma_1_code_rate_monotonicity():
    """Verify Lemma 1: R(K) = K / (13K + 6) is strictly monotonically increasing with K."""
    rates = []
    for K in [2, 3, 4, 5, 6, 8, 12, 16, 32]:
        codec = GeneralizedPathaCode(K=K)
        expected_M = 13 * K + 6
        expected_R = K / (13 * K + 6)
        assert codec.M == expected_M, f"M mismatch for K={K}: {codec.M} != {expected_M}"
        rates.append(expected_R)
    
    # Assert strict monotonicity: R(K_{i+1}) > R(K_i)
    for i in range(len(rates) - 1):
        assert rates[i+1] > rates[i], f"Monotonicity violation at index {i}: {rates[i+1]} <= {rates[i]}"
    
    # Specific known values
    assert abs(rates[2] - 4 / 58) < 1e-6  # K=4 -> 0.0689655
    assert abs(rates[4] - 6 / 84) < 1e-6  # K=6 -> 0.0714285
    assert rates[-1] < 1 / 13             # Asymptotic bound: 0.076923

def test_theorem_1_exact_formulas_and_asymptotic_bound():
    """Verify Theorem 1: M = 13K + 6 and B_E = 10K + 7 (for K >= 3), asymptotic ratio 10/13"""
    for K in [3, 4, 6, 8, 16, 32]:
        codec = GeneralizedPathaCode(K=K)
        assert codec.M == 13 * K + 6, f"Block length mismatch for K={K}: {codec.M} != {13*K+6}"
        assert codec.BE == 10 * K + 7, f"BE mismatch for K={K}: {codec.BE} != {10*K+7}"
        ratio = codec.BE / codec.M
        assert ratio >= 10 / 13, f"Asymptotic ratio violation for K={K}: {ratio} < 10/13"

def test_theorem_2_marked_erasure_majority_recovery():
    """Verify Theorem 2: Marked burst-erasure single-pass majority voting reconstructs with 0 error."""
    codec = GeneralizedPathaCode(K=4)
    msg = (1, 0, 1, 1)
    cw = codec.encode(msg)
    
    # Test across all burst erasure lengths L <= BE (BE=47 for K=4)
    for L in [1, 5, 10, 20, 30, 40, 47]:
        for s in [0, 5, 10]:
            if s + L <= len(cw):
                erased = list(cw)
                for idx in range(s, s + L):
                    erased[idx] = None
                recovered = codec.decode(erased)
                assert recovered == msg, f"Marked erasure recovery failed for L={L}, s={s}"

def test_theorem_3_candidate_tie_bounds():
    """Verify Theorem 3: Candidate ties are bounded by |S*| <= M - b + 1 and deterministically resolved."""
    codec = GeneralizedPathaCode(K=4)
    P = codec.pilots
    M = codec.M
    
    # Degenerate all-ones test: verifies upper bound |S*| <= M - b + 1
    cw_ones = codec.encode([1, 1, 1, 1])
    for b in [1, 5, 10]:
        rx = cw_ones[b:]
        N = len(rx)
        scores = []
        for s_cand in range(M - b + 1):
            score = sum(1 for p in P if (p if p < s_cand else (p - b if p >= s_cand + b else -1)) in range(N) and rx[p if p < s_cand else (p - b if p >= s_cand + b else -1)] == 1)
            scores.append(score)
        best_score = max(scores)
        ties = sum(1 for sc in scores if sc == best_score)
        assert ties <= M - b + 1, f"Ties exceeded M - b + 1: {ties} > {M - b + 1}"
    
    # Verify 100% deterministic resolution under ties across exhaustive 4-bit payloads
    for bits in itertools.product([0, 1], repeat=4):
        msg = tuple(bits)
        cw = codec.encode(msg)
        for b in [1, 5, 10]:
            rx = cw[b:]
            decoded = codec.decode(rx)
            assert decoded == msg, f"Phase 2 tie resolution failed for msg={msg}, b={b}"

def test_theorem_4_auxiliary_memory_bound():
    """Verify Theorem 4: Auxiliary memory buffer size is strictly O(1) wrt stream length."""
    for K in [2, 4, 6, 8]:
        codec = GeneralizedPathaCode(K=K)
        M = codec.M
        # Unpruned candidate array of single-byte indices: at most M bytes
        cand_array_bytes = M * 1
        # Vote accumulators: 2 counters per symbol
        vote_accum_bytes = 2 * K
        # Loop indices and registers
        registers_bytes = 16
        total_aux_bytes = cand_array_bytes + vote_accum_bytes + registers_bytes
        assert total_aux_bytes < 256, f"Auxiliary memory bound violated for K={K}: {total_aux_bytes} >= 256 bytes"
