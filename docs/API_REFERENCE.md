# GPC Codec Python API Reference

### `GeneralizedPathaCode(K=4)`
- `K`: Payload message length.
- `M`: Codeword length ($13K + 6$).
- `rate`: Information rate $K / M$.
- `BE`: Minimum span ($10K + 7$).
- `encode(msg)`: Encodes $K$ binary bits into $M$-bit braided codeword.
- `decode(rx)`: Recovers $K$ bits in $\mathcal{O}(M)$ time under erasures or deletions.
