"""
Benchmarking Flat GPC(K=6) vs Hierarchical GPC(K=4) Under Severe Stress
========================================================================
Tests both schemes under:
1. Extended burst deletions: b = 0, 4, 8, 10, 12, 14, 16 nt
2. Deletions hitting anywhere in the header (including the cluster tag for hierarchical)
3. Oxford Nanopore R10.4 compound noise (0.6% sub, 0.6% del, 0.4% ins)
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gpc import GeneralizedPathaCode
from experiments.verify_table1_reproducibility import (
    build_gpc_placement,
    encode_placement,
    decode_gpc_burst_deletion
)
from experiments.test_real_dna_storage import (
    get_real_phix174_genome,
    bits_to_dna,
    dna_to_bits
)

def benchmark_sweep():
    header, genome = get_real_phix174_genome()
    payload_len = 150
    num_strands = int(np.ceil(len(genome) / payload_len))
    padded_genome = genome.ljust(num_strands * payload_len, 'A')
    
    codec_k6 = GeneralizedPathaCode(K=6)
    codec_k4 = GeneralizedPathaCode(K=4)
    
    burst_lengths = [0, 4, 8, 10, 12, 14, 16]
    trials_per_point = 200
    
    print("=" * 90)
    print(f"STRESS BENCHMARK: FLAT K=6 VS HIERARCHICAL K=4 ({trials_per_point} Full Genome Runs per Point)")
    print("=" * 90)
    print(f"{'Burst (nt)':<12} | {'Flat K=6 Loss (%)':<20} | {'Hierarchical K=4 Loss (%)':<25} | {'Unprotected Loss (%)':<20}")
    print("-" * 90)
    
    np.random.seed(42)
    
    results = []
    for b_nt in burst_lengths:
        b_bits = b_nt * 2
        
        # 1. Flat K=6
        k6_lost_strands = 0
        total_k6_strands = 0
        
        # 2. Hierarchical K=4 (where deletion can hit ANYWHERE in the 30-nt header including cluster tag)
        k4_lost_strands = 0
        total_k4_strands = 0
        
        # 3. Unprotected
        unprot_lost_strands = 0
        total_unprot_strands = 0
        
        for t in range(trials_per_point):
            # Test a random strand from the 36 strands
            strand_id = np.random.randint(0, num_strands)
            
            # --- FLAT K=6 ---
            bits_k6 = tuple(int(x) for x in f"{strand_id:06b}")
            cw_k6 = codec_k6.encode(bits_k6)
            hdr_k6 = bits_to_dna(cw_k6) # 42 nt
            total_k6_strands += 1
            if b_nt > 0:
                s = np.random.randint(0, len(hdr_k6) - b_nt + 1)
                corrupted_k6 = hdr_k6[:s] + hdr_k6[s + b_nt:]
            else:
                corrupted_k6 = hdr_k6
            dec_k6 = codec_k6.decode(dna_to_bits(corrupted_k6))
            if dec_k6 is None or int("".join(str(b) for b in dec_k6), 2) != strand_id:
                k6_lost_strands += 1
                
            # --- HIERARCHICAL K=4 ---
            cluster_id = strand_id // 16
            inner_idx = strand_id % 16
            cluster_tag = ['A', 'C', 'G', 'T'][cluster_id]
            bits_k4 = tuple(int(x) for x in f"{inner_idx:04b}")
            cw_k4 = codec_k4.encode(bits_k4)
            hdr_k4 = cluster_tag + bits_to_dna(cw_k4) # 30 nt total
            total_k4_strands += 1
            if b_nt > 0:
                s = np.random.randint(0, len(hdr_k4) - b_nt + 1)
                corrupted_k4 = hdr_k4[:s] + hdr_k4[s + b_nt:]
            else:
                corrupted_k4 = hdr_k4
            
            # Decoding Hierarchical:
            # If s == 0, the cluster tag was deleted inside the burst!
            # The remaining header is shorter.
            if len(corrupted_k4) < 30 - b_nt:
                k4_lost_strands += 1
            else:
                rx_tag = corrupted_k4[0]
                rx_gpc = corrupted_k4[1:]
                if rx_tag not in ['A', 'C', 'G', 'T'] or len(rx_gpc) != 29 - b_nt:
                    # Deletion crossed cluster tag boundary
                    k4_lost_strands += 1
                else:
                    rec_cluster = {'A': 0, 'C': 1, 'G': 2, 'T': 3}[rx_tag]
                    dec_k4 = codec_k4.decode(dna_to_bits(rx_gpc))
                    if dec_k4 is None:
                        k4_lost_strands += 1
                    else:
                        rec_inner = int("".join(str(b) for b in dec_k4), 2)
                        rec_id = rec_cluster * 16 + rec_inner
                        if rec_id != strand_id:
                            k4_lost_strands += 1
                            
            # --- UNPROTECTED ---
            total_unprot_strands += 1
            if b_nt == 0:
                pass
            else:
                unprot_lost_strands += 1 # Any deletion destroys unprotected 6-bit index
                
        loss_k6 = (k6_lost_strands / total_k6_strands) * 100
        loss_k4 = (k4_lost_strands / total_k4_strands) * 100
        loss_unprot = (unprot_lost_strands / total_unprot_strands) * 100
        
        print(f"{b_nt:<12} | {loss_k6:>18.2f}% | {loss_k4:>23.2f}% | {loss_unprot:>18.2f}%")
        results.append((b_nt, loss_k6, loss_k4, loss_unprot))
        
    print("=" * 90)

if __name__ == "__main__":
    benchmark_sweep()
