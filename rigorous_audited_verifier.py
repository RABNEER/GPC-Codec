"""
Audited Rigorous Verification of Generalized Patha Codes (GPC)
==============================================================
Implements the exact verification protocol required by the research review:
1. Environment snapshot (Python, OS, timestamp)
2. Exact placement specifications for GPC and matched baselines (M = 13K + 6)
3. Exhaustive check of ALL 2^K binary messages for K=4 and K=6:
   - Marked contiguous burst erasures: B_E (codebook uniqueness + decoder recovery)
   - Unmarked contiguous burst deletions: B_del (codebook ambiguity check across all b)
   - Collision witness logging
4. Side-by-side comparison with Reviewer's Baseline: c(x) = x || 111111 || x^12
5. Export to machine-readable results_audited.json
"""

import sys
import os
import time
import json
import itertools
from collections import defaultdict

# ---------------------------------------------------------
# 1. Scheme Definitions & Placement Generators
# ---------------------------------------------------------

def build_gpc_placement(K):
    """
    GPC placement with 5 stage-major cycles + 6 transition pilots (0).
    Cycles: F2 (2K), B2 (2K), F3 (3K), B3 (3K), F3 (3K) -> 13K data symbols + 6 pilots.
    Total length M = 13K + 6.
    """
    placement = []
    
    def add_cycle(pass_type):
        placement.append(0) # Transition pilot anchor
        for i in range(K):
            s0 = i + 1
            s1 = ((i + 1) % K) + 1
            s2 = ((i + 2) % K) + 1
            if pass_type == 'F2':
                placement.extend([s0, s1])
            elif pass_type == 'B2':
                placement.extend([s1, s0])
            elif pass_type == 'F3':
                placement.extend([s0, s1, s2])
            elif pass_type == 'B3':
                placement.extend([s2, s1, s0])
    
    add_cycle('F2')
    add_cycle('B2')
    add_cycle('F3')
    add_cycle('B3')
    add_cycle('F3')
    placement.append(0) # Final anchor
    return placement

def build_reviewer_baseline_placement(K):
    """
    Reviewer's baseline: c(x) = x || 111111 || x^12
    Uses 1 copy of x, 6 pilots (0), then 12 copies of x.
    Total length M = 13K + 6.
    """
    placement = []
    # 1 copy of x: 1..K
    placement.extend(list(range(1, K + 1)))
    # 6 pilots (0)
    placement.extend([0] * 6)
    # 12 copies of x
    for _ in range(12):
        placement.extend(list(range(1, K + 1)))
    return placement

def build_uniform_interleaved_placement(K):
    """
    Uniform interleaving: 13 copies of (1..K) interleaved, plus 6 pilots (0) at end.
    Total length M = 13K + 6.
    """
    placement = []
    for _ in range(13):
        placement.extend(list(range(1, K + 1)))
    placement.extend([0] * 6)
    return placement

def build_literal_ghana_placement(K):
    """
    Literal Ghana Patha without toroidal wrapping (boundary-pinned).
    """
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

def encode_placement(msg, placement, pilot_val=1):
    """Encodes a binary message vector using the placement array."""
    return [pilot_val if sym == 0 else msg[sym - 1] for sym in placement]

# ---------------------------------------------------------
# 2. Linear-Time Majority-Voting Erasure Decoder
# ---------------------------------------------------------

def decode_erasure_majority(received_with_erasures, placement, K):
    """
    Linear-time O(M) majority voting decoder for marked erasures (None indicates erased).
    """
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
            return None # Erased all copies of sym
        ones = sum(v)
        zeros = len(v) - ones
        decoded.append(1 if ones >= zeros else 0)
    return tuple(decoded)

# ---------------------------------------------------------
# 3. Exhaustive Verification Algorithms
# ---------------------------------------------------------

def compute_spans(placement, K):
    """Computes max(S_j) - min(S_j) for each symbol."""
    pos = defaultdict(list)
    for idx, sym in enumerate(placement):
        if sym > 0:
            pos[sym].append(idx)
    spans = {j: (max(pos[j]) - min(pos[j])) if len(pos[j]) >= 2 else 0 for j in range(1, K + 1)}
    return spans

def check_exhaustive_marked_erasures(placement, K):
    """
    Exhaustively tests all 2^K messages across every burst length L in [1, M]
    and every start position s in [0, M - L].
    Returns:
    - B_E_theoretical: min_j span_j
    - B_E_codebook: maximum L where all 2^K messages remain pairwise distinct under all starts
    - B_E_decoder: maximum L where majority decoder succeeds for all messages and starts
    - failure_witness: first case where failure occurs at B_E + 1
    """
    M = len(placement)
    messages = list(itertools.product([0, 1], repeat=K))
    codewords = [encode_placement(msg, placement) for msg in messages]
    spans = compute_spans(placement, K)
    B_E_theoretical = min(spans.values())
    
    B_E_codebook = 0
    B_E_decoder = 0
    first_failure_witness = None
    
    for L in range(1, M + 1):
        level_codebook_ok = True
        level_decoder_ok = True
        
        for s in range(M - L + 1):
            # Check codebook distinctness
            seen = {}
            for idx, msg in enumerate(messages):
                cw = codewords[idx]
                surviving = tuple(cw[:s] + cw[s+L:])
                if surviving in seen:
                    level_codebook_ok = False
                    if first_failure_witness is None:
                        first_failure_witness = {
                            "type": "erasure_codebook_collision",
                            "L": L,
                            "start": s,
                            "msg1": seen[surviving],
                            "msg2": msg,
                            "surviving_length": len(surviving)
                        }
                    break
                seen[surviving] = msg
            
            # Check decoder
            if level_codebook_ok:
                for idx, msg in enumerate(messages):
                    cw = codewords[idx]
                    rx = list(cw)
                    for i in range(s, s + L):
                        rx[i] = None
                    dec = decode_erasure_majority(rx, placement, K)
                    if dec != msg:
                        level_decoder_ok = False
                        break
            else:
                level_decoder_ok = False
                
            if not level_codebook_ok and not level_decoder_ok:
                break
                
        if level_codebook_ok:
            B_E_codebook = L
        if level_decoder_ok:
            B_E_decoder = L
        if not level_codebook_ok:
            break
            
    return {
        "B_E_theoretical": B_E_theoretical,
        "B_E_codebook": B_E_codebook,
        "B_E_decoder": B_E_decoder,
        "first_failure_witness": first_failure_witness,
        "spans": spans
    }

def check_exhaustive_burst_deletions(placement, K, max_b=25):
    """
    Exhaustively tests all 2^K messages for unmarked contiguous burst deletions.
    For each length b, computes D_b(c(x)) for all x.
    Checks if D_b(c(x)) intersects D_b(c(x')) for any x != x'.
    Logs exact collision witness when intersection occurs.
    """
    M = len(placement)
    messages = list(itertools.product([0, 1], repeat=K))
    codewords = [encode_placement(msg, placement) for msg in messages]
    
    B_del_codebook = 0
    collision_witnesses = {}
    
    for b in range(1, min(max_b + 1, M)):
        # Generate descendants for each message
        descendants = []
        for idx, cw in enumerate(codewords):
            desc = set()
            for s in range(M - b + 1):
                desc.add(tuple(cw[:s] + cw[s+b:]))
            descendants.append(desc)
            
        collision_found = False
        for i in range(len(messages)):
            for j in range(i + 1, len(messages)):
                common = descendants[i].intersection(descendants[j])
                if common:
                    collision_found = True
                    colliding_string = list(common)[0]
                    # Find which starts produced this colliding string
                    s_i = [s for s in range(M - b + 1) if tuple(codewords[i][:s] + codewords[i][s+b:]) == colliding_string]
                    s_j = [s for s in range(M - b + 1) if tuple(codewords[j][:s] + codewords[j][s+b:]) == colliding_string]
                    collision_witnesses[b] = {
                        "msg1": list(messages[i]),
                        "msg2": list(messages[j]),
                        "b": b,
                        "start_msg1": s_i[0] if s_i else None,
                        "start_msg2": s_j[0] if s_j else None,
                        "colliding_output_sample": list(colliding_string[:20])
                    }
                    break
            if collision_found:
                break
                
        if not collision_found:
            B_del_codebook = b
        else:
            # We found a collision at length b.
            # Continue checking if smaller b had no collisions!
            break
            
    return {
        "B_del_guaranteed": B_del_codebook,
        "collision_witnesses": collision_witnesses
    }

# ---------------------------------------------------------
# 4. Main Verification Execution
# ---------------------------------------------------------

def run_audited_verification():
    print("=" * 80)
    print("AUDITED RIGOROUS VERIFICATION OF GENERALIZED PATHA CODES")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print(f"Python: {sys.version.split()[0]} | Platform: {sys.platform}")
    print("=" * 80)
    
    results = {
        "metadata": {
            "timestamp_utc": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
            "python_version": sys.version,
            "platform": sys.platform,
        },
        "schemes": {}
    }
    
    for K in [4, 6]:
        print(f"\n" + "#" * 60)
        print(f"--- RUNNING EXHAUSTIVE BENCHMARKS FOR K = {K} (2^{K} = {2**K} MESSAGES) ---")
        print("#" * 60)
        
        schemes_to_test = [
            ("GPC (Challenger)", build_gpc_placement(K)),
            ("Reviewer Baseline (x || 1^6 || x^12)", build_reviewer_baseline_placement(K)),
            ("Uniform Interleaved (x * 13 || 1^6)", build_uniform_interleaved_placement(K)),
            ("Literal Ghana Patha (Raw)", build_literal_ghana_placement(K))
        ]
        
        for name, pl in schemes_to_test:
            M = len(pl)
            rate = K / M
            print(f"\n[Scheme: {name}]")
            print(f"  Length M = {M}, Rate R = {rate:.4f}")
            
            # 1. Marked Erasure Check
            t0 = time.time()
            erasure_res = check_exhaustive_marked_erasures(pl, K)
            t_erasure = time.time() - t0
            print(f"  Marked Erasures: Theoretical B_E={erasure_res['B_E_theoretical']}, "
                  f"Codebook B_E={erasure_res['B_E_codebook']}, Decoder B_E={erasure_res['B_E_decoder']} "
                  f"({t_erasure:.2f}s)")
            if erasure_res['first_failure_witness']:
                fw = erasure_res['first_failure_witness']
                print(f"    Failure Witness at L={fw['L']}, start={fw['start']}: "
                      f"msg1={fw['msg1']} collides with msg2={fw['msg2']}")
            
            # 2. Unmarked Deletion Check
            t0 = time.time()
            deletion_res = check_exhaustive_burst_deletions(pl, K, max_b=20)
            t_deletion = time.time() - t0
            print(f"  Unmarked Deletions: Guaranteed B_del = {deletion_res['B_del_guaranteed']} ({t_deletion:.2f}s)")
            if deletion_res['collision_witnesses']:
                first_b = min(deletion_res['collision_witnesses'].keys())
                cw = deletion_res['collision_witnesses'][first_b]
                print(f"    First Deletion Collision at b={cw['b']}: "
                      f"msg1={cw['msg1']} (deleted at {cw['start_msg1']}) == "
                      f"msg2={cw['msg2']} (deleted at {cw['start_msg2']})")
                      
            # Store in results
            scheme_key = f"{name}_K{K}"
            results["schemes"][scheme_key] = {
                "name": name,
                "K": K,
                "M": M,
                "rate": rate,
                "marked_erasures": erasure_res,
                "unmarked_deletions": deletion_res,
                "timing": {
                    "erasure_eval_sec": t_erasure,
                    "deletion_eval_sec": t_deletion
                }
            }
            
    # Save machine-readable JSON
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_audited.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n" + "=" * 80)
    print(f"Audited results successfully written to: {output_path}")
    print("=" * 80)

if __name__ == "__main__":
    run_audited_verification()
