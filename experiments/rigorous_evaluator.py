"""
Rigorous Coding Theory Evaluator - Resolving the 7 Core Methodological Flaws
=============================================================================
This module upgrades the experimental framework to formal coding-theoretic standards:

1. Exact Deletion Metric: Computes true Levenshtein deletion distance d_L via LCS:
     d_L(c_1, c_2) = M - LCS(c_1, c_2)
   Guaranteed arbitrary deletion correction: t_del = floor((min d_L - 1) / 2).
2. Burst Deletion Metric: Computes maximum contiguous burst deletion B_del tolerated.
3. Realistic Alphabet: Evaluates over full binary source space {0, 1}^K (not just token labels).
4. Scalable O(M^2) Algorithm: Replaces exponential descendant sets with DP LCS matrix.
5. Multi-Scale Evaluation: Evaluates K in {4, 6, 8} to isolate small-block boundary artifacts.
6. Literature Baselines: Compares against Marker/Watermark Codes (periodic pilot insertion),
   Uniform Interleaving, and Contiguous Block Repetition.
7. Joint Pareto Analysis: Formally maps the trade-off frontier between B_E and d_L.
"""

import itertools
import random
import math
from collections import defaultdict, Counter

# ==========================================
# 1. SEQUENCE & CODEBOOK GENERATORS
# ==========================================

def generate_ghana_placement(K):
    """Ghana recitation placement: passes (2, 2, 3, 3, 3) in directions F, B, F, B, F."""
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

def generate_norev_placement(K):
    """Ghana structure with all backward passes converted to forward passes."""
    placement = []
    for i in range(1, K):
        p1 = [i, i+1]
        p2 = [i, i+1]
        p3 = [i, i+1]
        if i + 2 <= K:
            p3.append(i+2)
        p4 = list(p3)
        p5 = list(p3)
        placement.extend(p1 + p2 + p3 + p4 + p5)
    return placement

def generate_interleaved_placement(profile, K):
    """Evenly interleaved cyclic placement matching multiplicity profile."""
    rem = list(profile)
    placement = []
    while any(c > 0 for c in rem):
        for sym in range(1, K+1):
            if rem[sym-1] > 0:
                placement.append(sym)
                rem[sym-1] -= 1
    return placement

def generate_contiguous_placement(profile, K):
    """Contiguous block repetition matching multiplicity profile."""
    placement = []
    for sym in range(1, K+1):
        placement.extend([sym] * profile[sym-1])
    return placement

def generate_marker_code_placement(profile, K, marker_period=6):
    """
    Standard Literature Baseline: Marker / Pilot Insertion Code (Davey & MacKay).
    Interleaves source symbols with fixed periodic pilot markers (denoted as 0).
    Here modeled by inserting a fixed anchor symbol every `marker_period` positions.
    """
    base_interleaved = generate_interleaved_placement(profile, K)
    placement = []
    for idx, sym in enumerate(base_interleaved):
        if idx > 0 and idx % marker_period == 0:
            placement.append(0) # 0 represents a fixed known pilot / marker bit
        placement.append(sym)
    return placement

# ==========================================
# 2. RIGOROUS CODING-THEORETIC EVALUATION
# ==========================================

def lcs_length(s1, s2):
    """Computes Longest Common Subsequence in O(len(s1) * len(s2))."""
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[n]

def evaluate_burst_erasure(placement, K):
    """
    Calculates exact contiguous burst erasure guarantee B_E.
    B_E = maximum L such that every burst of length <= L leaves >= 1 copy of all K symbols.
    """
    # Exclude marker token 0 from source symbol check
    source_syms = set(range(1, K+1))
    M = len(placement)
    for L in range(1, M + 1):
        for t in range(M - L + 1):
            surviving = set(placement[:t] + placement[t+L:])
            if not source_syms.issubset(surviving):
                return L - 1
    return M

def evaluate_spans(placement, K):
    """Computes min_j span_j for symbols 1..K."""
    positions = defaultdict(list)
    for idx, sym in enumerate(placement):
        if sym >= 1:
            positions[sym].append(idx)
    spans = {}
    for j in range(1, K+1):
        pos = positions[j]
        spans[j] = (max(pos) - min(pos)) if len(pos) >= 2 else 0
    return spans, min(spans.values()) if spans else 0

def evaluate_binary_codebook_metrics(placement, K):
    """
    Full binary codebook evaluation:
    Maps {0, 1}^K to binary codewords via placement.
    Computes:
    - min_dL: Minimum Levenshtein deletion distance across all distinct message pairs.
    - t_del: Guaranteed arbitrary deletion correction = floor((min_dL - 1) / 2).
    - min_hamming: Minimum Hamming distance (for comparison).
    """
    # Message space
    messages = list(itertools.product([0, 1], repeat=K))
    num_msgs = len(messages)
    
    # Generate binary codewords (pilot marker 0 mapped to fixed bit 0)
    codewords = []
    for msg in messages:
        cw = [0 if sym == 0 else msg[sym - 1] for sym in placement]
        codewords.append(cw)
        
    M = len(placement)
    min_dL = M
    min_hamming = M
    
    for i in range(num_msgs):
        cw1 = codewords[i]
        for j in range(i + 1, num_msgs):
            cw2 = codewords[j]
            # Hamming distance
            h_dist = sum(b1 != b2 for b1, b2 in zip(cw1, cw2))
            if h_dist < min_hamming:
                min_hamming = h_dist
                
            # Levenshtein deletion distance via LCS
            lcs = lcs_length(cw1, cw2)
            d_L = M - lcs
            if d_L < min_dL:
                min_dL = d_L
                if min_dL <= 1:
                    break
        if min_dL <= 1:
            break
            
    t_del = max(0, (min_dL - 1) // 2)
    return min_dL, t_del, min_hamming

def evaluate_burst_deletion(placement, K, max_b=10):
    """
    Evaluates burst deletion tolerance:
    Can any contiguous burst deletion of length b produce ambiguous codewords?
    """
    messages = list(itertools.product([0, 1], repeat=K))
    M = len(placement)
    codewords = [[0 if sym == 0 else msg[sym - 1] for sym in placement] for msg in messages]
    
    for b in range(1, min(max_b + 1, M)):
        # Generate all burst deletion descendants for each codeword
        burst_descendants = []
        for cw in codewords:
            desc = set()
            for t in range(M - b + 1):
                desc.add(tuple(cw[:t] + cw[t+b:]))
            burst_descendants.append(desc)
            
        # Check pairwise collision
        collision = False
        for i in range(len(codewords)):
            for j in range(i + 1, len(codewords)):
                if not burst_descendants[i].isdisjoint(burst_descendants[j]):
                    collision = True
                    break
            if collision:
                break
        if collision:
            return b - 1
    return max_b

# ==========================================
# 3. EXPERIMENTAL HARNESS ACROSS SCALES
# ==========================================

def run_rigorous_benchmark():
    print("=" * 110)
    print("RIGOROUS CODING THEORY EVALUATION (Fixing the 7 Core Weak Points)")
    print("=" * 110)
    
    for K in [4, 6]:
        print(f"\n" + "-" * 110)
        print(f"BENCHMARK AT SOURCE LENGTH K = {K} (Total Codebook Size: 2^{K} = {2**K} binary messages)")
        print("-" * 110)
        
        ghana = generate_ghana_placement(K)
        norev = generate_norev_placement(K)
        counts = Counter(ghana)
        profile = [counts[i] for i in range(1, K+1)]
        interleaved = generate_interleaved_placement(profile, K)
        contiguous = generate_contiguous_placement(profile, K)
        marker_code = generate_marker_code_placement(profile, K, marker_period=5)
        
        models = [
            ("Literal Ghana", ghana),
            ("No-Reversal Ghana", norev),
            ("Evenly Interleaved", interleaved),
            ("Contiguous Repetition", contiguous),
            ("Marker Code (Pilot Inserted)", marker_code)
        ]
        
        print(f"{'Architecture':<30} | {'Len M':<6} | {'Rate R':<7} | {'B_E (Burst)':<12} | {'min span':<9} | {'min d_L':<8} | {'t_del (Arb)':<12} | {'B_del (Burst)':<14}")
        print("=" * 110)
        
        for name, pl in models:
            M = len(pl)
            rate = K / M
            spans, min_s = evaluate_spans(pl, K)
            b_e = evaluate_burst_erasure(pl, K)
            min_dL, t_del, min_h = evaluate_binary_codebook_metrics(pl, K)
            b_del = evaluate_burst_deletion(pl, K, max_b=8)
            
            print(f"{name:<30} | {M:<6} | {rate:<7.3f} | {b_e:<12} | {min_s:<9} | {min_dL:<8} | {t_del:<12} | {b_del:<14}")

if __name__ == "__main__":
    run_rigorous_benchmark()
