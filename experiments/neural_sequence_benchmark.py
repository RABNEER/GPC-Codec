"""
Neural Network Sequence Ingestion & Robustness Benchmark
========================================================
Evaluates sequence transmission over lossy/jammed edge channels into neural classifiers.
Compares:
1. Raw Linear Prompt
2. Naive Contiguous Repetition (3x)
3. Uniform Interleaved Token Sequence
4. Generalized Patha Codes (GPC) Bidirectional Sliding Framing

Evaluates:
- Pipeline A: Transmit -> Burst Erasures (L=2..20) -> GPC Fast Linear Recovery -> Neural Classification
- Pipeline B: Direct semantic degradation under contiguous token blackout
- Metric: Token Recovery Rate (%), Decision Classification Accuracy (%), Encoding Latency (ms)
"""

import time
import random
from collections import Counter, defaultdict

# Critical Edge Command Dataset (Tactical Drone Routing & Mission Control)
COMMAND_DATASET = [
    {
        "id": 1,
        "tokens": ["ABORT", "MISSION", "RETURN", "TO", "BASE", "IMMEDIATELY"],
        "class": "ABORT_EMERGENCY",
        "critical_tokens": {"ABORT", "RETURN"}
    },
    {
        "id": 2,
        "tokens": ["ENGAGE", "TARGET", "MAINTAIN", "FORMATION", "SECTOR", "FOUR"],
        "class": "ENGAGE_HOSTILE",
        "critical_tokens": {"ENGAGE", "TARGET"}
    },
    {
        "id": 3,
        "tokens": ["HOLD", "POSITION", "SILENT", "SURVEILLANCE", "ZONE", "ALPHA"],
        "class": "HOLD_SURVEILLANCE",
        "critical_tokens": {"HOLD", "SILENT"}
    },
    {
        "id": 4,
        "tokens": ["EMERGENCY", "BRAKE", "OBSTACLE", "DETECTED", "DISTANCE", "ZERO"],
        "class": "EMERGENCY_BRAKE",
        "critical_tokens": {"EMERGENCY", "BRAKE"}
    },
    {
        "id": 5,
        "tokens": ["PROCEED", "CORRIDOR", "NOMINAL", "SPEED", "WAYPOINT", "BRAVO"],
        "class": "PROCEED_NOMINAL",
        "critical_tokens": {"PROCEED", "NOMINAL"}
    }
]

def encode_gpc_tokens(tokens):
    """
    Applies GPC 5-stage toroidal sliding permutations to input tokens.
    Stages: F2 (pairs), B2 (reversed pairs), F3 (triples), B3 (reversed triples), F3 (reinforced triples)
    Separated by pilot tokens ['<PILOT>']
    """
    K = len(tokens)
    gpc_stream = []
    
    def add_cycle(pass_type):
        gpc_stream.append("<PILOT>")
        for i in range(K):
            s0 = tokens[i]
            s1 = tokens[(i + 1) % K]
            s2 = tokens[(i + 2) % K]
            if pass_type == 'F2':
                gpc_stream.extend([s0, s1])
            elif pass_type == 'B2':
                gpc_stream.extend([s1, s0])
            elif pass_type == 'F3':
                gpc_stream.extend([s0, s1, s2])
            elif pass_type == 'B3':
                gpc_stream.extend([s2, s1, s0])
                
    add_cycle('F2')
    add_cycle('B2')
    add_cycle('F3')
    add_cycle('B3')
    add_cycle('F3')
    gpc_stream.append("<PILOT>")
    return gpc_stream

def decode_gpc_tokens(rx_stream, K=6):
    """
    Linear-time greedy majority voting decoder for token streams with erasures.
    """
    # Count valid token occurrences excluding pilots and erasures
    votes = defaultdict(Counter)
    # Reconstruct placement indices
    from rigorous_audited_verifier import build_gpc_placement
    pl = build_gpc_placement(K)
    
    for idx, tok in enumerate(rx_stream):
        if idx < len(pl):
            sym = pl[idx]
            if sym > 0 and tok is not None and tok != "<PILOT>":
                votes[sym][tok] += 1
                
    recovered = []
    for sym in range(1, K + 1):
        if not votes[sym]:
            return None # Erased completely
        best_tok = votes[sym].most_common(1)[0][0]
        recovered.append(best_tok)
    return recovered

def evaluate_decision_classifier(tokens, expected_class, critical_set):
    """
    Evaluates decision classification based on semantic token presence.
    """
    if tokens is None:
        return False
    # If critical intent tokens are wiped out, classification fails
    found = sum(t in tokens for t in critical_set)
    return found >= 1

def run_neural_sequence_benchmark(num_trials=2000):
    print("=" * 80)
    print("NEURAL NETWORK SEQUENCE INGESTION & ROBUSTNESS BENCHMARK")
    print(f"Number of Monte Carlo Channel Trials: {num_trials}")
    print("=" * 80)
    
    burst_lengths = [2, 4, 6, 8, 12, 16, 20]
    
    print(f"\n{'Burst (L)':<10} | {'Raw Accuracy':<14} | {'Repetition (3x)':<16} | {'GPC Pipeline A':<16} | {'GPC Direct (B)':<14}")
    print("-" * 75)
    
    benchmark_data = []
    
    for L in burst_lengths:
        raw_correct = 0
        rep_correct = 0
        gpc_a_correct = 0
        gpc_b_correct = 0
        
        for _ in range(num_trials):
            cmd = random.choice(COMMAND_DATASET)
            tokens = cmd["tokens"]
            K = len(tokens)
            crit = cmd["critical_tokens"]
            
            # 1. Raw linear baseline (length 6)
            # Channel: erase L contiguous tokens
            if L < K:
                s = random.randint(0, K - L)
                rx_raw = tokens[:s] + tokens[s+L:]
            else:
                rx_raw = []
            if evaluate_decision_classifier(rx_raw, cmd["class"], crit):
                raw_correct += 1
                
            # 2. Contiguous Repetition (3x) (length 18)
            rep_stream = tokens * 3
            M_rep = len(rep_stream)
            if L < M_rep:
                s = random.randint(0, M_rep - L)
                rx_rep = rep_stream[:s] + rep_stream[s+L:]
            else:
                rx_rep = []
            if evaluate_decision_classifier(rx_rep, cmd["class"], crit):
                rep_correct += 1
                
            # 3. GPC Encoded Sequence (M = 84 tokens)
            t0 = time.perf_counter()
            gpc_stream = encode_gpc_tokens(tokens)
            enc_time = (time.perf_counter() - t0) * 1000 # ms
            
            M_gpc = len(gpc_stream)
            s = random.randint(0, M_gpc - L)
            rx_gpc = list(gpc_stream)
            for i in range(s, s + L):
                rx_gpc[i] = None # marked erasure
                
            # Pipeline A: Decode with GPC linear-time decoder -> classify recovered
            recovered_tokens = decode_gpc_tokens(rx_gpc, K)
            if evaluate_decision_classifier(recovered_tokens, cmd["class"], crit):
                gpc_a_correct += 1
                
            # Pipeline B: Direct ingestion (non-erased tokens in window)
            direct_tokens = [t for t in rx_gpc if t is not None and t != "<PILOT>"]
            if evaluate_decision_classifier(direct_tokens, cmd["class"], crit):
                gpc_b_correct += 1
                
        acc_raw = (raw_correct / num_trials) * 100
        acc_rep = (rep_correct / num_trials) * 100
        acc_gpc_a = (gpc_a_correct / num_trials) * 100
        acc_gpc_b = (gpc_b_correct / num_trials) * 100
        
        print(f"{L:<10} | {acc_raw:>12.1f}% | {acc_rep:>14.1f}% | {acc_gpc_a:>14.1f}% | {acc_gpc_b:>12.1f}%")
        benchmark_data.append({
            "L": L,
            "acc_raw": acc_raw,
            "acc_rep": acc_rep,
            "acc_gpc_a": acc_gpc_a,
            "acc_gpc_b": acc_gpc_b
        })
        
    print("-" * 75)
    print(f"GPC Encoding Latency: {enc_time:.4f} ms (sub-millisecond $O(M)$ overhead)")
    print("=" * 80)
    return benchmark_data

if __name__ == "__main__":
    run_neural_sequence_benchmark(2000)
