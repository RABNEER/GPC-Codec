"""
Comprehensive Empirical Benchmark Suite for Synthetic DNA Data Storage
======================================================================
Evaluates Bounded-Slip Constrained DNA Codec (BC-DNA) versus
Classical Baselines (Naive Direct Mapping and Goldman Nature 2013).

Benchmarks:
1. Physical Constraint Compliance (Homopolymer run distribution & GC balance).
2. Nanopore Sequencing Noise Sweep (Substitution, Insertion, Homopolymer Deletion).
3. Burst Deletion Stress Test (Measuring Drift Confinement & Resynchronization).
4. Code Rate and Redundancy Overhead Analysis.

Generates:
- `experiments/benchmark_results.json` (Raw empirical data)
- Figures in `figures/` for the publication manuscript.
"""

import os
import sys
import json
import time
import random
import numpy as np

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from dna_codec.codec import (
    BCDNACodec, NaiveDirectCodec, GoldmanNature2013Codec,
    _max_homopolymer_run, _gc_count
)
from dna_codec.channel import NanoporeChannel

def generate_test_payloads():
    """Generates 4 diverse payload types representing real-world digital storage scenarios."""
    payloads = {}
    
    # 1. Structured English Text (5,000 bytes)
    sample_text = (
        "Synthetic DNA data storage encodes digital binary information into nucleotide sequences. "
        "Unlike magnetic tape or optical disks which degrade over decades, DNA possesses immense "
        "information density, theoretical capacity exceeding exabytes per gram, and biological durability "
        "spanning millennia when desiccated at room temperature. However, chemical synthesis via "
        "phosphoramidite methods and sequencing via biological nanopores introduce severe physical constraints. "
        "Specifically, consecutive identical nucleotide runs cause flat-line ionic blockade signals in nanopore "
        "pores, triggering high rates of deletion and insertion errors that destroy coordinate frame synchronization. "
    ) * 12
    payloads['text'] = sample_text[:5000].encode('utf-8')
    
    # 2. High-Entropy Pseudorandom Binary (5,000 bytes)
    rng = random.Random(1337)
    payloads['random_binary'] = bytes([rng.randint(0, 255) for _ in range(5000)])
    
    # 3. 32x32 Binary Scientific Emblem Image (128 bytes = 1024 bits)
    # 13x repeats to reach ~1,664 bytes
    emblem_bytes = bytearray(128)
    for r in range(32):
        for c in range(32):
            dx = c - 15.5
            dy = r - 15.5
            dist = (dx*dx + dy*dy)**0.5
            bit = 1 if (13.0 <= dist <= 15.0 or dist <= 3.5 or abs(dx) < 1.0) else 0
            byte_idx = (r * 32 + c) // 8
            bit_idx = (r * 32 + c) % 8
            if bit:
                emblem_bytes[byte_idx] |= (1 << (7 - bit_idx))
    payloads['image_emblem'] = bytes(emblem_bytes) * 15
    
    # 4. Low-Entropy Structured Telemetry (5,000 bytes with repeated headers)
    telemetry = bytearray()
    for seq in range(250):
        # 20-byte packet: sync, seq, sensor values, checksum
        telemetry.extend(b'\xAA\x55')
        telemetry.extend(seq.to_bytes(2, 'big'))
        telemetry.extend(b'\x00\x00\x12\x34\x00\x00\x56\x78\x00\x00\x9A\xBC\x00\x00\xDE\xF0')
    payloads['telemetry'] = bytes(telemetry)
    
    return payloads

def analyze_homopolymer_distribution(dna_seq):
    """Computes exact histogram of homopolymer run lengths."""
    dist = {}
    n = len(dna_seq)
    if n == 0:
        return dist
    i = 0
    while i < n:
        j = i
        while j < n and dna_seq[j] == dna_seq[i]:
            j += 1
        run_len = j - i
        dist[run_len] = dist.get(run_len, 0) + 1
        i = j
    return dist

def run_experiment_1_physical_compliance(payloads):
    """Evaluates homopolymer runs, GC content, and code rate across codecs."""
    print("\n" + "="*80)
    print("EXPERIMENT 1: Physical Biological Constraint Compliance")
    print("="*80)
    
    codecs = {
        'BC-DNA (Proposed)': BCDNACodec(block_size_bytes=16),
        'Goldman 2013 (Nature)': GoldmanNature2013Codec(),
        'Naive Direct 2-bit': NaiveDirectCodec()
    }
    
    results = {}
    
    for p_name, p_data in payloads.items():
        results[p_name] = {}
        print(f"\n--- Payload: {p_name} ({len(p_data)} bytes) ---")
        for c_name, codec in codecs.items():
            t0 = time.perf_counter()
            dna = codec.encode(p_data)
            enc_time = time.perf_counter() - t0
            
            dna_len = len(dna)
            rate = (len(p_data) * 8.0) / dna_len
            max_run = _max_homopolymer_run(dna)
            gc_pct = (_gc_count(dna) / dna_len) * 100.0
            homo_dist = analyze_homopolymer_distribution(dna)
            
            # Verify clean decode
            t1 = time.perf_counter()
            if isinstance(codec, BCDNACodec):
                rec, _, _ = codec.decode(dna, len(p_data))
            else:
                rec = codec.decode(dna, len(p_data))
            dec_time = time.perf_counter() - t1
            is_lossless = (rec == p_data)
            
            results[p_name][c_name] = {
                'dna_length': dna_len,
                'code_rate_bits_per_nt': round(rate, 4),
                'max_homopolymer': max_run,
                'gc_percentage': round(gc_pct, 2),
                'homopolymer_distribution': {str(k): v for k, v in sorted(homo_dist.items())},
                'is_lossless': is_lossless,
                'encode_time_ms': round(enc_time * 1000, 2),
                'decode_time_ms': round(dec_time * 1000, 2)
            }
            
            runs_gt2 = sum(v for k, v in homo_dist.items() if k > 2)
            print(f"{c_name:22s} | Len: {dna_len:6d} nt | Rate: {rate:.3f} b/nt | MaxRun: {max_run:2d} | Runs>2: {runs_gt2:4d} | GC: {gc_pct:5.1f}% | Lossless: {is_lossless}")

    return results

def run_experiment_2_nanopore_noise_sweep(payloads, num_trials=10):
    """Sweeps sequencing channel noise scaling parameter and measures Byte Error Rate."""
    print("\n" + "="*80)
    print("EXPERIMENT 2: Oxford Nanopore Sequencing Noise Sweep")
    print("="*80)
    
    test_data = payloads['text']  # 5,000 bytes
    codecs = {
        'BC-DNA (Proposed)': BCDNACodec(block_size_bytes=16),
        'Goldman 2013 (Nature)': GoldmanNature2013Codec(),
        'Naive Direct 2-bit': NaiveDirectCodec()
    }
    
    # Pre-encode
    encoded = {c_name: codec.encode(test_data) for c_name, codec in codecs.items()}
    
    noise_levels = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00]
    sweep_results = []
    
    for noise in noise_levels:
        row = {'noise_scaling': noise, 'codecs': {}}
        for c_name, codec in codecs.items():
            ber_trials = []
            del_rates = []
            resyncs_list = []
            
            for trial in range(num_trials):
                # Channel parameters scaled by noise
                ch = NanoporeChannel(
                    base_sub_prob=0.015 * noise,
                    base_ins_prob=0.005 * noise,
                    homopolymer_scaling=noise,
                    seed=1000 * trial + int(noise * 100)
                )
                rx_dna, stats = ch.transmit(encoded[c_name])
                del_rates.append(stats['deletions'] / max(1, len(encoded[c_name])))
                
                if isinstance(codec, BCDNACodec):
                    rec, n_blocks, n_sync = codec.decode(rx_dna, len(test_data))
                    resyncs_list.append(n_sync)
                else:
                    rec = codec.decode(rx_dna, len(test_data))
                    resyncs_list.append(0)
                    
                # Byte Error Rate
                mismatches = sum(1 for a, b in zip(test_data, rec) if a != b)
                ber = mismatches / len(test_data)
                ber_trials.append(ber)
                
            mean_ber = float(np.mean(ber_trials))
            std_ber = float(np.std(ber_trials))
            mean_del = float(np.mean(del_rates))
            mean_resync = float(np.mean(resyncs_list))
            
            row['codecs'][c_name] = {
                'mean_ber': round(mean_ber, 4),
                'std_ber': round(std_ber, 4),
                'mean_del_rate': round(mean_del, 4),
                'mean_resyncs': round(mean_resync, 1)
            }
            
        sweep_results.append(row)
        bc_ber = row['codecs']['BC-DNA (Proposed)']['mean_ber'] * 100
        gold_ber = row['codecs']['Goldman 2013 (Nature)']['mean_ber'] * 100
        naive_ber = row['codecs']['Naive Direct 2-bit']['mean_ber'] * 100
        resyncs = row['codecs']['BC-DNA (Proposed)']['mean_resyncs']
        print(f"Noise {noise:4.2f}x | BC-DNA BER: {bc_ber:5.1f}% ({resyncs:4.0f} resyncs) | Goldman BER: {gold_ber:5.1f}% | Naive BER: {naive_ber:5.1f}%")

    return sweep_results

def run_experiment_3_burst_deletion_stress(payloads, num_trials=10):
    """Stress tests localized burst deletions (e.g. enzymatic synthesis dropout)."""
    print("\n" + "="*80)
    print("EXPERIMENT 3: Localized Burst Deletion Stress Test")
    print("="*80)
    
    test_data = payloads['image_emblem']  # ~1920 bytes
    codecs = {
        'BC-DNA (Proposed)': BCDNACodec(block_size_bytes=16),
        'Goldman 2013 (Nature)': GoldmanNature2013Codec(),
        'Naive Direct 2-bit': NaiveDirectCodec()
    }
    
    encoded = {c_name: codec.encode(test_data) for c_name, codec in codecs.items()}
    burst_lengths = [0, 2, 4, 6, 8, 10, 12, 16, 20, 25, 30]
    burst_results = []
    
    for burst in burst_lengths:
        row = {'burst_nt': burst, 'codecs': {}}
        for c_name, codec in codecs.items():
            ber_trials = []
            dna_orig = encoded[c_name]
            
            for trial in range(num_trials):
                rng = random.Random(trial * 777 + burst)
                # Inject a single burst deletion of length `burst` at a random position in the first 20%
                if burst > 0 and len(dna_orig) > burst + 50:
                    cut_pos = rng.randint(20, min(len(dna_orig) - burst - 10, 300))
                    dna_corrupt = dna_orig[:cut_pos] + dna_orig[cut_pos + burst:]
                else:
                    dna_corrupt = dna_orig
                    
                if isinstance(codec, BCDNACodec):
                    rec, _, _ = codec.decode(dna_corrupt, len(test_data))
                else:
                    rec = codec.decode(dna_corrupt, len(test_data))
                    
                mismatches = sum(1 for a, b in zip(test_data, rec) if a != b)
                ber = mismatches / len(test_data)
                ber_trials.append(ber)
                
            mean_ber = float(np.mean(ber_trials))
            std_ber = float(np.std(ber_trials))
            row['codecs'][c_name] = {
                'mean_ber': round(mean_ber, 4),
                'std_ber': round(std_ber, 4)
            }
            
        burst_results.append(row)
        bc_ber = row['codecs']['BC-DNA (Proposed)']['mean_ber'] * 100
        gold_ber = row['codecs']['Goldman 2013 (Nature)']['mean_ber'] * 100
        naive_ber = row['codecs']['Naive Direct 2-bit']['mean_ber'] * 100
        print(f"Burst {burst:2d} nt | BC-DNA BER: {bc_ber:5.1f}% | Goldman BER: {gold_ber:5.1f}% | Naive BER: {naive_ber:5.1f}%")

    return burst_results

def main():
    print("="*80)
    print("STARTING SCIENTIFIC BENCHMARK SUITE: BC-DNA VS STATE-OF-THE-ART BASELINES")
    print("="*80)
    
    payloads = generate_test_payloads()
    
    exp1 = run_experiment_1_physical_compliance(payloads)
    exp2 = run_experiment_2_nanopore_noise_sweep(payloads, num_trials=8)
    exp3 = run_experiment_3_burst_deletion_stress(payloads, num_trials=8)
    
    full_audit = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'experiment_1_physical_compliance': exp1,
        'experiment_2_nanopore_noise_sweep': exp2,
        'experiment_3_burst_deletion_stress': exp3,
        'theoretical_summary': {
            'naive_rate': 2.000,
            'goldman_rate': 1.333,
            'bc_dna_raw_rate': 1.600,
            'bc_dna_effective_rate_block16': 1.455,
            'bc_dna_effective_rate_block32': 1.524,
            'density_gain_over_goldman_pct': round((1.455 - 1.333) / 1.333 * 100, 1)
        }
    }
    
    out_dir = os.path.join(os.path.dirname(__file__))
    out_file = os.path.join(out_dir, 'benchmark_results.json')
    with open(out_file, 'w') as f:
        json.dump(full_audit, f, indent=2)
        
    print("\n" + "="*80)
    print(f"BENCHMARK COMPLETE. Saved raw audited data to {out_file}")
    print("="*80)

if __name__ == '__main__':
    main()
