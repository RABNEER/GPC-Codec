# Generalized Patha Codes (GPC)

[![PyPI version](https://img.shields.io/pypi/v/gpc-codec.svg)](https://pypi.org/project/gpc-codec/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gpc-codec.svg)](https://pypi.org/project/gpc-codec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests Passing](https://img.shields.io/badge/tests-13%20passed-brightgreen.svg)](#running-automated-tests)
[![Research Monograph](https://img.shields.io/badge/Paper-12--Page%20Monograph-blue.svg)](papers/GPC_Full_Research_Paper_12_Pages.pdf)

> **A Parameterized Cyclic Permutation Inner Code Family for Order-Sensitive and Synchronization-Drift Channels.**  
> *Targeted at High-Integrity Systems: Silicon Edge AI Telemetry, Carbon Synthetic DNA Molecular Data Storage, and Autonomous UAV Swarm Coordination.*

---

## 🏛️ Executive Summary

**Generalized Patha Codes (GPC)** modernize ancient Indian Vedic oral recitation mnemonics (*Veda Patha*, specifically *Ghana-Patha*) into an algebraic placement error-correcting inner code family engineered specifically for **order-sensitive channels**.

Standard outer codes—such as Reed-Solomon (RS), BCH, Polar, and Low-Density Parity-Check (LDPC) codes—presuppose an absolute, rigid coordinate grid. When subjected to unmarked deletions, insertions, or timing slips, the symbol indexing frame collapses: a single unmarked deletion ($b=1$) causes a 1-symbol coordinate shift, precipitating **catastrophic frame collapse (0.0% packet recovery)** in downstream decoders.

GPC solves this fundamental vulnerability by interweaving payload symbols across multi-stage toroidal permutation cycles ($\mathcal{S}_K$) anchored by deterministic pilot delimiters. Under sustained burst deletions and coordinate jitter, GPC provides:
- **$\mathcal{O}(M)$ Average-Case Decoding:** Greedy two-phase alignment with consensus confidence margin voting that resolves deletion cuts in sub-millisecond time (worst-case $\mathcal{O}(M^2)$ on degenerate periodic payloads).
- **Asymptotic Recovery Fraction $\ge 76.92\%$:** Guaranteed recovery from contiguous marked burst erasures spanning $B_E = 10K + 7$ symbols on a block of length $M = 13K + 6$ ($\lim_{K \to \infty} B_E / M = 10/13 \approx 76.92\%$).
- **Downstream Resynchronization:** Restores coordinate alignment in sub-millisecond execution time ($81.6\,\mu\text{s}$ per strand), allowing standard outer algebraic decoders to operate at full theoretical efficiency without suffering Strand Address Dropout.

---

## 📦 Installation

Install the official package directly from PyPI:

```bash
pip install gpc-codec
```

Or install the latest development version directly from GitHub:

```bash
git clone https://github.com/RABNEER/GPC-Codec.git
cd GPC-Codec
pip install -e .
```

---

## 🚀 Quickstart Guide

The package provides dual namespace compatibility (`import gpc_codec` or `import gpc`) and includes both high-level interfaces and lower-level channel models.

### 1. Basic Encoding & Decoding

```python
from gpc_codec import GPCEncoder, GPCDecoder

# Initialize GPC codec with payload dimension K = 4
encoder = GPCEncoder(K=4)
decoder = GPCDecoder(K=4)

# Information payload: K binary symbols
message = [1, 0, 1, 1]

# Codeword length M = 13*K + 6 = 58 symbols (including 6 pilot anchors)
codeword = encoder.encode(message)
print("Codeword (length", len(codeword), "):", codeword)

# Clean decode roundtrip
recovered = decoder.decode(codeword)
assert recovered == tuple(message)
print("Decoded message:", recovered)
```

### 2. Recovering from an Unmarked Burst Deletion

When an unmarked burst deletion occurs, symbols are physically excised from the stream, shortening the sequence and destroying rigid coordinate alignments:

```python
from gpc_codec import GPCEncoder, GPCDecoder, simulate_burst_deletion

encoder = GPCEncoder(K=4)
decoder = GPCDecoder(K=4)
message = [1, 0, 1, 1]
codeword = encoder.encode(message)

# Simulate an unmarked burst deletion of length b = 5 symbols at offset 12
corrupted = simulate_burst_deletion(codeword, burst_length=5, start_idx=12)
print(f"Original length: {len(codeword)} -> Corrupted length: {len(corrupted)}")

# GPC Two-Phase Greedy Alignment dynamically reconstructs the deletion cut
recovered = decoder.decode(corrupted)
assert recovered == tuple(message)
print("Successfully recovered original message:", recovered)
```

### 3. Recovering from a Marked Burst Erasure

```python
from gpc_codec import GPCEncoder, GPCDecoder, simulate_burst_erasure, GeneralizedPathaCode

gpc = GeneralizedPathaCode(K=4)
encoder = GPCEncoder(K=4)
decoder = GPCDecoder(K=4)
message = [0, 1, 1, 0]
codeword = encoder.encode(message)

# GPC guarantees recovery up to BE = 10*K + 7 = 47 erased symbols (81.03% of block)
erased_seq = simulate_burst_erasure(codeword, burst_length=gpc.BE, start_idx=5)
print(f"Number of erased positions: {erased_seq.count(None)}")

recovered = decoder.decode(erased_seq)
assert recovered == tuple(message)
print("Successfully recovered message from 47-symbol burst erasure:", recovered)
```

### 4. Synthetic DNA Molecular Storage Codec (BC-DNA)

The library also packages the RLL-2 / GC-balanced constrained sequence codec for synthetic DNA synthesis and Oxford Nanopore sequencing:

```python
from dna_codec import ConstrainedDNACodec

codec = ConstrainedDNACodec()
payload = b"Silicon-to-Carbon Molecular Storage Telemetry"

# Encodes raw bytes into DNA nucleotides (A, C, G, T)
dna_strand = codec.encode(payload)
print(f"Encoded {len(payload)} bytes into {len(dna_strand)} nucleotides")
print(f"Sample DNA: {dna_strand[:30]}...")

# Properties verified: Run-length <= 2, GC content 40%-60%, rate 1.60 bits/nt
decoded_bytes, blocks, resyncs = codec.decode(dna_strand, expected_bytes=len(payload))
assert decoded_bytes == payload
print("Verified bit-exact molecular roundtrip!")
```

---

## 📐 Mathematical Foundations

### 1. Codeword Parameters & Permutation Architecture
For an information block of length $K \ge 2$, a Generalized Patha Code $\text{GPC}(M, K)$ constructs a codeword of block length:
$$M = 13K + 6$$
The structure interleaves six deterministic pilot symbols $\mathcal{P} = 1$ with five distinct permutation cycles over the symmetric group $\mathcal{S}_K$:
$$\mathbf{c} = \big[ \pi_0, \mathbf{F}_2, \pi_1, \mathbf{B}_2, \pi_2, \mathbf{F}_3^{(1)}, \pi_3, \mathbf{B}_3, \pi_4, \mathbf{F}_3^{(2)}, \pi_5 \big]$$

Where:
- $\mathbf{F}_2$: Forward 2-window pass $(s_i, s_{i+1 \pmod K})$ across all $i \in [0, K-1]$.
- $\mathbf{B}_2$: Backward 2-window pass $(s_{i+1 \pmod K}, s_i)$.
- $\mathbf{F}_3^{(1)}, \mathbf{F}_3^{(2)}$: Forward 3-window passes $(s_i, s_{i+1 \pmod K}, s_{i+2 \pmod K})$.
- $\mathbf{B}_3$: Backward 3-window pass $(s_{i+2 \pmod K}, s_{i+1 \pmod K}, s_i)$.
- $\pi_0, \dots, \pi_5$: Deterministic pilot anchors inserted at coordinates $p \in \{0, 2K+1, 4K+2, 7K+3, 10K+4, 13K+5\}$.

### 2. Combinatorial Burst-Erasure Recovery Bound
**Theorem 2 (Combinatorial Erasure Recovery Lower Bound):**  
For any message dimension $K \ge 3$, the minimum coordinate span between identical symbol occurrences across all passes is:
$$B_E(K) = 10K + 7$$
*(Achieved by symbol index 3, which appears at index 4 and index $10K+11$, defining a span of $10K+7$).*  
Consequently, the asymptotic recovery fraction $\eta_{\text{burst}}$ is strictly lower-bounded by:
$$\lim_{K \to \infty} \frac{B_E(K)}{M(K)} = \lim_{K \to \infty} \frac{10K + 7}{13K + 6} = \frac{10}{13} \approx 76.92\%$$
*(For finite $K=4$, $B_E = 47$ over $M=58$, achieving an instantaneous marked erasure tolerance of $81.03\%$.)*

### 3. Algorithm 1: Two-Phase Greedy Alignment Decoder
The decoding process executes in average-case $\mathcal{O}(M)$ time (worst-case $\mathcal{O}(M^2)$ on degenerate periodic payloads):
1. **Phase 1 (Pilot Candidate Filtering):** Evaluates all candidate burst cut offsets $\hat{s} \in [0, M - b]$ against expected pilot coordinates. The candidate set is pruned to:
   $$\mathcal{S}^* = \arg\max_{\hat{s}} \sum_{p \in \mathcal{P}} \mathbf{1}\left( \mathbf{y}[\text{shift}(p, \hat{s}, b)] == 1 \right)$$
2. **Phase 2 (Consensus Confidence Margin Voting):** For each surviving hypothesis $\hat{s} \in \mathcal{S}^*$, symbols are gathered across all non-deleted occurrences. Ties are broken by maximizing the total decision margin:
   $$\mathcal{M}(\hat{s}) = \sum_{j=1}^K \left| \sum_{t} \mathbf{y}^{(j)}_t - \sum_{t} (1 - \mathbf{y}^{(j)}_t) \right|$$

---

## 🔬 Empirical Validation Across 3 Domains (84,732 Machine Trials)

| Metric / Channel Condition | Reviewer Baseline ($x \parallel \mathbf{1}^6 \parallel x^{12}$) | Uniform Interleaving | Schoeny et al. (2017) [42] | Generalized Patha Code (GPC) | Evidence Source (Code / Log) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Marked Burst Erasures ($B_E$, $K=4$)** | **$54$** | $48$ | $26$ | **$47$** ($81.03\%$ block) | `tests/test_erasure_decoder.py` |
| **Unmarked Burst Deletions ($B_{\text{del}}$)** | **$0$** (Collapses on $b=1$) | **$0$** (Collapses on $b=1$) | $7$ | **$20$ nt ($40$ bits)** | `experiments/equal_overhead_dna_audit.json` |
| **DNA Nanopore ($b=22\text{ nt}$ stall)** | $100.0\%$ (Desync) | $100.0\%$ (Desync) | $100.0\%$ (Fatal) | **$1.90\%$ Loss** | `experiments/equal_overhead_dna_audit.json` |
| **Bacteriophage $\Phi$X174 ($b=12\text{ nt}$)** | $100.0\%$ (Desync) | $100.0\%$ (Desync) | $100.0\%$ (Fatal) | **$2.60\%$ Loss** | `experiments/phix174_nanopore_benchmark_audit.json` |
| **Brutal R10.4 Mixed Noise ($b=16\text{ nt}$)** | $100.0\%$ (Desync) | $100.0\%$ (Desync) | $100.0\%$ (Fatal) | **$7.20\%$ Loss** (Bounded) | `experiments/brutal_dna_r10_4_stress_audit.json` |
| **UAV C2 Telemetry ($b=15\text{ bits}$ Jamming)** | $100.0\%$ (Crash) | $100.0\%$ (Crash) | $100.0\%$ (Crash) | **$0.00\%$ FER** ($100\%$ retention) | `experiments/uav_hard_test_results.json` |
| **UAV C2 Telemetry ($b=25\text{ bits}$ Jamming)** | $100.0\%$ (Crash) | $100.0\%$ (Crash) | $100.0\%$ (Crash) | **$0.95\%$ FER** ($99.05\%$ retention) | `experiments/uav_hard_test_results.json` |
| **BCI Neural Telemetry ($b=10\text{ bits}$ Slip)** | $100.0\%$ (Paralysis) | $100.0\%$ (Paralysis) | $100.0\%$ (Paralysis) | **$0.05\%$ FER** ($99.95\%$ retention) | `experiments/neural_bci_hard_test_results.json` |
| **BCI Neural Telemetry ($b=25\text{ bits}$ Slip)** | $100.0\%$ (Paralysis) | $100.0\%$ (Paralysis) | $100.0\%$ (Paralysis) | **$1.45\%$ FER** ($98.55\%$ retention) | `experiments/neural_bci_hard_test_results.json` |
| **Mean Decoding Latency ($K=4$)** | $12.4\,\mu\text{s}$ | $14.1\,\mu\text{s}$ | $184.2\,\mu\text{s}$ | **$106.9\,\mu\text{s}$** (Deterministic) | `experiments/dna_nanopore_hard_test_results.json` |
| **Dynamic Memory Allocation** | Variable | Variable | Dynamic graph | **$0\text{ bytes}$ heap / $128\text{ B}$ bounded stack** | RTL Architecture Specification |

### Domain Highlights:
1. **Carbon Synthetic DNA Storage:** Enforces homopolymer constraints ($L_{\max} \le 2$) and strict GC balance ($40\%\text{--}60\%$) via optimal 5-mer partitioning (400 valid codewords), achieving $1.60\text{ bits/nt}$. Evaluated across 25,500 physical and simulated nanopore trials on the authentic 5,386-base genome of **Bacteriophage $\Phi$X174** (NCBI `NC_001422.1`).
2. **Silicon Mission-Critical UAV C2 Flight Telemetry:** Prevents command desynchronization under severe RF jamming bursts up to 25 bits, maintaining $99.05\%$ packet reception where conventional packet structures fail completely (12,000 trials).
3. **High-Throughput Intracortical BCI Neural Streaming:** Prevents neural spike coordinate loss under wireless timing slips and bit dropouts, maintaining $98.55\%$ valid spike packet recovery at $b=25\text{ bits}$ (12,000 trials).

---

## 📂 Repository Directory Structure

```
GPC-Codec/
├── src/
│   ├── gpc/                         # Core GPC implementation
│   │   ├── __init__.py              # Package exports (v1.0.1)
│   │   ├── core.py                  # GeneralizedPathaCode, GPCEncoder, GPCDecoder
│   │   ├── decoder.py               # Algorithm 1: O(M) greedy alignment decoder
│   │   ├── channel.py               # Burst deletion/erasure/transposition simulators
│   │   ├── baselines.py             # SOTA comparative baseline placements
│   │   └── cli.py                   # Command-line interface
│   ├── gpc_codec/                   # Canonical namespace alias (import gpc_codec)
│   │   ├── __init__.py              # Re-exports all core classes & utilities
│   │   ├── core.py                  # Core alias
│   │   ├── decoder.py               # Decoder alias
│   │   ├── channel.py               # Channel alias
│   │   └── baselines.py             # Baselines alias
│   └── dna_codec/                   # BC-DNA Constrained DNA storage package
│       ├── __init__.py              # DNA codec exports
│       ├── codec.py                 # BCDNACodec & Goldman 2013 baseline
│       └── channel.py               # Oxford Nanopore translocation channel model
│
├── tests/                           # Automated pytest verification suite
│   ├── test_gpc_codec_api.py        # Dual import & high-level API tests
│   ├── test_dna_codec.py            # DNA constraints (RLL-2, GC balance) tests
│   ├── test_encoder.py              # Codeword length & pilot position tests
│   ├── test_deletion_decoder.py     # Unmarked burst deletion recovery tests
│   ├── test_erasure_decoder.py      # Marked burst erasure recovery tests
│   └── test_theorems.py             # Formal verification of Theorems 1-5
│
├── papers/                          # Research manuscripts & publication PDFs
│   ├── GPC_Full_Research_Paper_12_Pages.pdf # 12-Page Master Research Monograph
│   ├── GPC_Comprehensive_Research_Paper.pdf # 4-Page Conference Submission Paper
│   ├── BC_DNA_Research_Paper.pdf            # Constrained DNA Data Storage Paper
│   ├── DNA_Storage_Experimental_Report.pdf  # DNA In-Silico Experimental Report
│   └── Swarm_Telemetry_Experimental_Report.pdf # Swarm Telemetry Report
│
├── experiments/                     # Empirical benchmark & reproducibility scripts
│   ├── equal_overhead_dna_benchmark.py   # Fair equal-overhead DNA benchmark (14,000 trials, Table II)
│   ├── equal_overhead_dna_audit.json     # Machine audit ledger with Clopper-Pearson 95% CIs
│   ├── patha_mechanism_ablation.py      # Pāṭha coding mechanism ablation study (6,000 trials, Table VIII)
│   ├── patha_mechanism_ablation_audit.json # Ablation study audit ledger
│   ├── verify_table1_reproducibility.py  # 60s reproduction of Table I parameter ledger
│   ├── test_algorithm1_edge_cases.py     # Algorithm 1 stress testing
│   ├── modern_sota_baselines_benchmark.py # SOTA comparison against Schoeny et al.
│   └── table1_exact_reproducibility.json # Machine-verifiable audit ledger
│
├── docs/                            # HTML/MathJax publication source templates & assembly scripts
├── pyproject.toml                   # Modern PEP 517/518 build configuration
├── setup.py                         # Backwards-compatible setup script
└── LICENSE                          # MIT Open Source License
```

---

## 🧪 Running Automated Tests

Run the complete test suite using `pytest`:

```bash
# Run all 13 unit tests across gpc, gpc_codec, and dna_codec:
pytest

# Run with verbose output:
pytest -v
```

All 13 tests execute deterministically in **under 0.1 seconds**.

### Reproducing Experimental Table I (Parameter Ledger):
```bash
python experiments/verify_table1_reproducibility.py
```
*Evaluates all 4 placement architectures for $K=4$ and $K=6$ from first principles, matching Table I down to the exact integer.*

### Reproducing Experimental Table II (Equal-Overhead DNA Indexing Benchmark):
```bash
python experiments/equal_overhead_dna_benchmark.py
```
*Runs 14,000 empirical trials across burst lengths $b \in [1..24]$ comparing GPC against Schoeny et al., Marker Codes, and Uniform Interleaving at equal 29-nt overhead with 95% Clopper-Pearson confidence intervals.*

### Reproducing Experimental Table VIII (Pāṭha Mechanism Ablation Study):
```bash
python experiments/patha_mechanism_ablation.py
```
*Executes 6,000 trials isolating the exact quantitative contribution of each Pāṭha component across 6 systematic structural variants.*

---

## 📚 Publications & Manuscripts

The repository includes complete, publication-ready manuscripts in the [`papers/`](papers/) directory:

1. **[12-Page Master Monograph](papers/GPC_Full_Research_Paper_12_Pages.pdf)**:  
   *Generalized Patha Codes: Cyclic Permutation Placement Inner Codes for Synchronization-Drift and Order-Sensitive Channels.* (Complete proofs, parameter ledgers, Oxford Nanopore HMM models, ARM Cortex-M4 cycle profiles, and Clopper-Pearson confidence bounds).
2. **[4-Page Conference Paper](papers/GPC_Comprehensive_Research_Paper.pdf)**:  
   *Dual-column IEEE archival format conference paper summarizing mathematical lineage, core theorems, and 3-domain empirical results.*
3. **[Constrained DNA Storage Paper](papers/BC_DNA_Research_Paper.pdf)**:  
   *Bi-Constrained DNA (BC-DNA): 1.60 bits/nt RLL-2 and GC-balanced constrained sequence coding for synthetic molecular data archives.*

---

## 📜 Academic Citation

If you use Generalized Patha Codes or this codebase in your research, please cite:

```bibtex
@article{ranveer2026gpc,
  title={Generalized Patha Codes: Cyclic Permutation Placement Inner Codes for Synchronization-Drift and Order-Sensitive Channels},
  author={Ranveer},
  journal={arXiv preprint},
  year={2026},
  url={https://github.com/RABNEER/GPC-Codec}
}
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
