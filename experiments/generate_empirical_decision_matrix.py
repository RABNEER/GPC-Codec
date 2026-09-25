"""
Consolidates empirical hard test results from all three candidate channels
into a comprehensive Decision Matrix for IRIS 2026.
"""

import json
import os

def load_results():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "uac_hard_test_results.json")) as f:
        uac = json.load(f)
    with open(os.path.join(base, "uav_hard_test_results.json")) as f:
        uav = json.load(f)
    with open(os.path.join(base, "dna_nanopore_hard_test_results.json")) as f:
        dna = json.load(f)
    return uac, uav, dna

def main():
    uac, uav, dna = load_results()
    
    print("=" * 90)
    print("EMPIRICAL CHANNEL DECISION MATRIX - GPC EVALUATION")
    print("=" * 90)
    print(f"{'Channel':<32} | {'b=10 FER':<10} | {'b=20 FER':<10} | {'b=30 FER':<10} | {'Latency':<10} | {'Rate Viability'}")
    print("-" * 90)
    
    # UAC
    uac_10 = uac['burst_sweep']['10']['GPC_FER'] * 100
    uac_20 = uac['burst_sweep']['20']['GPC_FER'] * 100
    uac_30 = uac['burst_sweep']['30']['GPC_FER'] * 100
    uac_lat = uac['burst_sweep']['20']['GPC_Mean_Latency_us']
    print(f"{'1. Underwater Acoustic (UAC)':<32} | {uac_10:5.2f}%     | {uac_20:5.2f}%     | {uac_30:5.2f}%     | {uac_lat:5.1f} us  | High (Tiny beacon)")

    # UAV
    uav_10 = uav['burst_sweep']['10']['GPC_FER'] * 100
    uav_20 = uav['burst_sweep']['20']['GPC_FER'] * 100
    uav_30 = uav['burst_sweep']['30']['GPC_FER'] * 100
    uav_lat = uav['burst_sweep']['20']['GPC_Mean_Latency_us']
    print(f"{'2. UAV C2 Telemetry / RF Jamming':<32} | {uav_10:5.2f}%     | {uav_20:5.2f}%     | {uav_30:5.2f}%     | {uav_lat:5.1f} us  | Exceptional (<0.1ms)")

    # DNA
    dna_10 = dna['burst_sweep']['10']['GPC_Strand_Dropout_Rate'] * 100
    dna_20 = dna['burst_sweep']['20']['GPC_Strand_Dropout_Rate'] * 100
    dna_30 = dna['burst_sweep']['30']['GPC_Strand_Dropout_Rate'] * 100
    dna_lat = dna['burst_sweep']['20']['GPC_Mean_Latency_us']
    print(f"{'3. DNA Storage Strand Address':<32} | {dna_10:5.2f}%     | {dna_20:5.2f}%     | {dna_30:5.2f}%     | {dna_lat:5.1f} us  | Good (29nt header)")
    print("=" * 90)

if __name__ == "__main__":
    main()
