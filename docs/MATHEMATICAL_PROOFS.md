# Standalone Mathematical Proofs

## Theorem 1: Support-Cover Characterization of Marked Burst Erasures
A repetition placement code with support sets $S_j$ tolerates any contiguous marked burst erasure of length $L$ if and only if:
$$L \le \min_{j \in \{1, \dots, K\}} 	ext{span}_j, \quad 	ext{where } 	ext{span}_j = \max(S_j) - \min(S_j)$$

## Theorem 2: Non-Vanishing Asymptotic Burst-Erasure Bound
In GPC, every symbol $j$ appears in Stage 1 ($\min(S_j) \le 2K$) and Stage 5 ($\max(S_j) \ge 10K + 5$).
Therefore:
$$	ext{span}_j \ge (10K + 5) - (2K) = 8K + 5$$
$$M = 13K + 6$$
$$\liminf_{K 	o \infty} rac{B_E}{M} \ge \lim_{K 	o \infty} rac{8K + 5}{13K + 6} = rac{8}{13} pprox 61.54\%$$
