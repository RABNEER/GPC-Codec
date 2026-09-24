# Generalized Patha Codes (GPC) & Patha-Laya Defense Framework

[![CI Test Suite](https://github.com/RABNEER/GPC-Codec/actions/workflows/ci.yml/badge.svg)](https://github.com/RABNEER/GPC-Codec/actions)
[![Reproducibility Audit](https://github.com/RABNEER/GPC-Codec/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/RABNEER/GPC-Codec/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IRIS 2026 Candidate](https://img.shields.io/badge/IRIS-2026%20Candidate-green.svg)](#)

> **National Science Fair Research Dossier**  
> *Target Competitions:* **IRIS National Science Fair (India)** & **Regeneron ISEF (Team India)**  
> *Subject Categories:* **Systems Software (SOFT)** | **Computational Biology & Bioinformatics (CBIO)** | **Robotics & Intelligent Machines (ROBO)**

## 🏛️ Project Overview
**Generalized Patha Codes (GPC)** modernizes ancient Indian Vedic oral recitation mnemonics (*Veda Patha*) into an algebraic placement error-correcting code family designed for **order-sensitive channels**. 

Traditional codes (Reed-Solomon, LDPC, Polar) presuppose rigid coordinate grids and suffer **catastrophic frame collapse ($B_{\text{del}} = 0$)** under unmarked deletions and synchronization slips. GPC introduces stage-major toroidal permutation windows and deterministic pilot anchors, establishing a resilient joint Pareto operating point ($B_E = 47, B_{\text{del}} = 21$ on $M=58$) with a deterministic $\mathcal{O}(M)$ greedy decoder.

---

## 📂 Repository Directory Structure

```
proud-lavoisier/
│
├── 📜 README.md                                             # Master project navigation guide
├── 📊 results_audited.json                                  # Machine-verifiable audit ledger (110,880 trials)
├── 🔬 rigorous_audited_verifier.py                          # Exhaustive combinatorial proof engine
├── 🧬 generalized_patha_code.py                             # GPC reference implementation
├── 💻 laya_end_to_end_verified.py                           # Domain 1: Silicon Edge AI live jamming testbed
├── 🧠 laya_live_evaluator.py                                # CPU ModernBERT 421M evaluator
├── 🧪 dna_storage_simulation.py                             # Domain 2: Carbon Synthetic DNA storage testbed
├── 🖼️ dna_image_storage_testbed.py                         # Domain 2: Brutal 32x32 Image Recovery testbed (Goldman 2013)
├── 🛸 swarm_telemetry_simulation.py                         # Domain 3: 8-UAV Swarm 3D Telemetry & Collision Avoidance testbed
├── 🌐 simulation.html                                       # Interactive browser GUI & live demo station
│
├── 📄 docs/                                                 # Research Publications & Technical Blueprints
│   ├── GPC_Comprehensive_Research_Paper.pdf                # Submission-Ready Archival Journal Paper (4 pages)
│   ├── GPC_Comprehensive_Research_Paper.md                 # Full Markdown Research Manuscript (Complete)
│   ├── GPC_Comprehensive_Research_Paper.html               # IEEE Master Two-Column HTML Template
│   ├── paper_publication.pdf                               # 3-Page IEEE preliminary publication paper
│   ├── GPC_Mathematical_Formulas_and_Execution_Blueprint.pdf # 4-Page Technical Monograph (with vector SVG math)
│   ├── DNA_Storage_Experimental_Report.pdf                 # 4-Page Audited DNA Testbed Report (with figures & math)
│   ├── Swarm_Telemetry_Experimental_Report.pdf             # 4-Page Audited Drone Swarm Report (with figures & math)
│   ├── paper_ieee.html                                     # IEEE master HTML template
│   ├── formulas_and_solutions_blueprint.html               # Technical blueprint HTML template
│   ├── dna_storage_experimental_report.html                # DNA testbed report HTML template
│   ├── dna_storage_experimental_report.md                  # Markdown source report
│   ├── swarm_telemetry_experimental_report.html            # Swarm testbed report HTML template
│   ├── swarm_telemetry_experimental_report.md              # Markdown source report
│   ├── compile_comprehensive_paper_pdf.py                  # Headless browser compiler for Journal Paper
│   ├── compile_pdf.py                                      # Headless browser compiler for IEEE paper
│   ├── compile_blueprint_pdf.py                            # Headless browser compiler for Blueprint
│   ├── compile_dna_report_pdf.py                           # Headless browser compiler for DNA report
│   ├── compile_swarm_report_pdf.py                         # Headless browser compiler for Swarm report
│   ├── paper_draft.md                                      # Markdown source draft
│   └── latex_table.tex                                     # LaTeX tabular code
│
├── 📈 figures/                                              # Vector Diagrams & Asset Generators
│   ├── figure1_asymptotic_scaling.svg                      # Asymptotic scaling curve (lim inf >= 61.54%)
│   ├── figure2_fer_waterfall.svg                           # Frame Error Rate (FER) waterfall comparison
│   ├── figure3_architecture.svg                            # GPC codec block diagram
│   ├── dna_image_recovery_comparison.png                   # High-res 4-panel DNA recovery figure (300 DPI)
│   ├── swarm_telemetry_recovery_comparison.png             # High-res 4-panel 3D Swarm collision figure (300 DPI)
│   └── generate_figures.py                                 # SVG generator script
│
├── 🧪 experiments/                                          # Historical Benchmarks & Simulation Scripts
│   ├── verify_table1_reproducibility.py                    # Standalone 60s reproduction of Table I
│   ├── test_algorithm1_edge_cases.py                       # Stress test of Algorithm 1 across all edge cases
│   ├── table1_exact_reproducibility.json                   # Machine ledger verifying all Table I metrics
│   ├── modern_sota_baselines_benchmark.py                  # Modern SOTA comparative benchmark
│   ├── modern_sota_baselines_audit.json                    # SOTA comparative audit ledger
│   ├── dna_storage_brutal_audit.json                       # 10 trial audit ledger for DNA image testbed
│   ├── swarm_telemetry_audit.json                          # 12 trial audit ledger for Drone Swarm testbed
│   ├── benchmark_results.csv                               # Historical benchmark logs
│   ├── benchmark_suite.py                                  # General benchmark runner
│   ├── channel_simulation.py                               # Erasure channel simulator
│   ├── neural_sequence_benchmark.py                        # Sequence-length ablation script
│   ├── reproduce_experiments.py                            # Full reproduction suite
│   ├── rigorous_evaluator.py                               # Earlier evaluator
│   └── generate_research_report.py                         # Summary report generator
│
└── 🗄️ archive/                                              # Scratch files, test scripts, and debug renders
```

---

## 🚀 Key Quickstart Commands

### 1. Reproduce Table I in 60 Seconds (1.10 Lakh Combinatorial Proofs)
```bash
python experiments/verify_table1_reproducibility.py
```
*Re-evaluates all 4 architectures for K=4 and K=6 from first principles; reproduces Table I down to the exact integer and verifies against `experiments/table1_exact_reproducibility.json`.*

### 2. Stress-Test Algorithm 1 Edge Cases
```bash
python experiments/test_algorithm1_edge_cases.py
```
*Evaluates pilot obliteration (up to 3 pilots destroyed), stage boundary crossing cuts, extreme payloads (`0000`, `1111`), and displacement tie-breaking (100% exact recovery).*

### 3. Run the Live Silicon Edge AI Jamming Defense
```bash
python laya_end_to_end_verified.py
```
*Loads the 421M-parameter ModernBERT model on CPU, injects a 16-token jamming burst dropping "DO NOT", and verifies bit-exact reconstruction in $552\text{ }\mu\text{s}$ restoring safe HOLD ($P=0.3510$) from fatal ATTACK ($P=0.8127$).*

### 4. Run the Synthetic DNA Molecular Storage Testbed
```bash
# Run 1,000 statistical oligo trials:
python dna_storage_simulation.py

# Run brutal 32x32 image recovery testbed & generate figure:
python dna_image_storage_testbed.py
```
*Outputs side-by-side image comparison figure to `figures/dna_image_recovery_comparison.png` and audit data to `experiments/dna_storage_brutal_audit.json`.*

### 5. Run the Autonomous Drone Swarm Telemetry Testbed
```bash
# Run 8-quadcopter 3D simulation with 12 jamming burst trials & generate figure:
python swarm_telemetry_simulation.py
```
*Outputs 4-panel 3D flight trajectory and waterfall figure to `figures/swarm_telemetry_recovery_comparison.png` and full audit log to `experiments/swarm_telemetry_audit.json`.*

### 6. Recompile the Master Publication PDFs
```bash
# Recompile the 5-Page Comprehensive Journal Paper:
python docs/compile_comprehensive_paper_pdf.py

# Recompile the 3-Page IEEE Conference Paper:
python docs/compile_pdf.py

# Recompile the 4-Page Mathematical Blueprint:
python docs/compile_blueprint_pdf.py

# Recompile the 4-Page Audited DNA Testbed Report:
python docs/compile_dna_report_pdf.py

# Recompile the 4-Page Audited Drone Swarm Report:
python docs/compile_swarm_report_pdf.py
```

---

## 🏆 Key Scientific Metrics Verified

| Metric | Reviewer Baseline ($x \parallel \mathbf{1}^6 \parallel x^{12}$) | Uniform Interleaving | Generalized Patha Code (GPC) |
| :--- | :---: | :---: | :---: |
| **Marked Burst Erasures ($B_E$)** | **$54$** (Theoretical Max) | $48$ | **$47$** ($13\%$ trade-off) |
| **Unmarked Burst Deletions ($B_{\text{del}}$)** | **$0$** (Collapses on $b=1$) | **$0$** (Collapses on $b=1$) | **$21$ practical / $46$ codebook** |
| **Decoding Time Complexity** | $\mathcal{O}(M)$ | $\mathcal{O}(M)$ | **$\mathcal{O}(M)$ deterministic greedy ($552\,\mu\text{s}$)** |
| **ModernBERT Decision Flip Rate** | $100\%$ fatal flip | $100\%$ fatal flip | **$0.0\%$ flip ($100\%$ preserved)** |
| **DNA Nanopore Indel Recovery** | $0.0\%$ (Scrambled noise) | $0.0\%$ (Scrambled noise) | **$100.0\%$ bit-exact recovery ($b \le 20\text{ nt}$)** |
| **Drone Swarm Zero-Collision Window** | $0\text{ ms}$ (Crashes at $30\text{ ms}$) | $20\text{ ms}$ (RS FEC limit) | **$80\text{ ms}$ ($4\times$ wider safety margin)** |

