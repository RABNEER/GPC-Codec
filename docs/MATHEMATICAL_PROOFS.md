# Standalone Mathematical Proofs

## Theorem 1: Support-Cover Characterization of Marked Burst Erasures
A repetition placement code with coordinate support sets $S_j = \{ i : \pi(i) = j \}$ tolerates any contiguous marked burst erasure of length $L$ if and only if:
$$L \le B_E = \min_{j \in \{1, \dots, K\}} \text{span}_j, \quad \text{where } \text{span}_j = \max(S_j) - \min(S_j)$$

## Theorem 2: Exact Combinatorial Burst-Erasure Bound and Non-Vanishing Asymptotic Limit
In GPC with block length $M = 13K + 6$ ($K \ge 3$), the 5 permutation passes are:
$$\mathbf{F}_2, \mathbf{B}_2, \mathbf{F}_3^{(1)}, \mathbf{B}_3, \mathbf{F}_3^{(2)}$$
interleaved by 6 deterministic pilot delimiters at coordinates $\{0, 2K+1, 4K+2, 7K+3, 10K+4, 13K+5\}$.

The minimum coordinate span across all $K$ source symbols is attained by symbol index 3:
- First appearance: inside $\mathbf{F}_2$ at coordinate index 4 (0-indexed).
- Final appearance: inside $\mathbf{F}_3^{(2)}$ at coordinate index $10K + 11$.

Therefore, the exact minimum coordinate span for any message dimension $K \ge 3$ is:
$$B_E(K) = \min_{j \in \{1, \dots, K\}} \text{span}_j = (10K + 11) - 4 = 10K + 7$$

For the primary baseline configuration $K=4$:
$$M(4) = 13(4) + 6 = 58$$
$$B_E(4) = 10(4) + 7 = 47\text{ symbols}$$
$$\text{Recovery Fraction: } \frac{B_E(4)}{M(4)} = \frac{47}{58} \approx 81.03\%$$

In the asymptotic limit as block length $K \to \infty$:
$$\lim_{K \to \infty} \frac{B_E(K)}{M(K)} = \lim_{K \to \infty} \frac{10K + 7}{13K + 6} = \frac{10}{13} \approx 76.92\%$$
