# Contributing to GPC Codec

Thank you for your interest in contributing to Generalized Patha Codes!

## Verification Guidelines
All algorithmic changes must preserve:
1. Deterministic $\mathcal{O}(M)$ linear-time greedy decoding.
2. 100% bit-exact recovery under marked burst erasures up to $B_E = \min_j \text{span}_j$.
3. Zero codebook deletion collisions up to $B_{\text{del}}^{\text{codebook}}$.

Run verification:
```bash
python experiments/verify_table1_reproducibility.py
python -m pytest tests/
```
