"""
GPC Channel Simulation Models
=============================
Provides deterministic and stochastic channel simulation models for evaluating
error-correcting codes under marked erasures, unmarked burst deletions,
transpositions (packet reordering), and mixed insertion/deletion/substitution noise.
"""

import random
from typing import Sequence, List, Optional, Tuple, Union

def simulate_burst_deletion(
    codeword: Sequence[int],
    burst_length: int,
    start_idx: Optional[int] = None,
    seed: Optional[int] = None
) -> List[int]:
    """
    Simulates an unmarked contiguous burst deletion of length `burst_length`.
    
    Args:
        codeword: Input transmitted sequence.
        burst_length: Number of consecutive symbols to delete (b).
        start_idx: Starting index for the deletion cut. If None, chosen uniformly at random.
        seed: Optional RNG seed for deterministic replication.
        
    Returns:
        Shortened sequence with length len(codeword) - burst_length.
    """
    n = len(codeword)
    if burst_length <= 0:
        return list(codeword)
    if burst_length > n:
        raise ValueError(f"Burst length {burst_length} exceeds sequence length {n}")
        
    rng = random.Random(seed)
    max_start = n - burst_length
    if start_idx is None:
        start_idx = rng.randint(0, max_start)
    else:
        if not (0 <= start_idx <= max_start):
            raise ValueError(f"Invalid start_idx {start_idx} for sequence length {n} and burst {burst_length}")
            
    return list(codeword[:start_idx]) + list(codeword[start_idx + burst_length:])

def simulate_burst_erasure(
    codeword: Sequence[int],
    burst_length: int,
    start_idx: Optional[int] = None,
    seed: Optional[int] = None
) -> List[Optional[int]]:
    """
    Simulates a marked contiguous burst erasure of length `burst_length`.
    
    Args:
        codeword: Input transmitted sequence.
        burst_length: Number of consecutive symbols to erase (marked with None).
        start_idx: Starting index for the erasure burst. If None, chosen uniformly.
        seed: Optional RNG seed for deterministic replication.
        
    Returns:
        Sequence of same length with erased positions replaced by None.
    """
    n = len(codeword)
    if burst_length <= 0:
        return list(codeword)
    if burst_length > n:
        raise ValueError(f"Burst length {burst_length} exceeds sequence length {n}")
        
    rng = random.Random(seed)
    max_start = n - burst_length
    if start_idx is None:
        start_idx = rng.randint(0, max_start)
    else:
        if not (0 <= start_idx <= max_start):
            raise ValueError(f"Invalid start_idx {start_idx} for sequence length {n} and burst {burst_length}")
            
    result: List[Optional[int]] = list(codeword)
    for i in range(start_idx, start_idx + burst_length):
        result[i] = None
    return result

def simulate_transposition(
    codeword: Sequence[int],
    num_transpositions: int = 1,
    seed: Optional[int] = None
) -> List[int]:
    """
    Simulates random symbol transpositions (swaps) representing packet reordering or coordinate drift.
    
    Args:
        codeword: Input transmitted sequence.
        num_transpositions: Number of random adjacent or near swaps to execute.
        seed: Optional RNG seed for deterministic replication.
        
    Returns:
        Permuted sequence with identical symbol histogram but altered order.
    """
    res = list(codeword)
    n = len(res)
    if n < 2 or num_transpositions <= 0:
        return res
        
    rng = random.Random(seed)
    for _ in range(num_transpositions):
        idx = rng.randint(0, n - 2)
        res[idx], res[idx + 1] = res[idx + 1], res[idx]
    return res

def simulate_mixed_channel(
    codeword: Sequence[int],
    deletion_rate: float = 0.0,
    insertion_rate: float = 0.0,
    substitution_rate: float = 0.0,
    alphabet: Optional[Sequence[int]] = None,
    seed: Optional[int] = None
) -> List[int]:
    """
    Simulates an uncoordinated mixed memoryless channel with deletions, insertions, and substitutions.
    
    Args:
        codeword: Input transmitted sequence.
        deletion_rate: Independent deletion probability p_del per symbol.
        insertion_rate: Independent insertion probability p_ins before each symbol.
        substitution_rate: Independent substitution probability p_sub per symbol.
        alphabet: Candidate symbols for insertions and substitutions. Default: (0, 1).
        seed: Optional RNG seed.
        
    Returns:
        Corrupted sequence.
    """
    rng = random.Random(seed)
    if alphabet is None:
        alphabet = (0, 1)
        
    out = []
    for sym in codeword:
        # Check insertion before symbol
        if insertion_rate > 0.0 and rng.random() < insertion_rate:
            out.append(rng.choice(alphabet))
            
        # Check deletion of symbol
        if deletion_rate > 0.0 and rng.random() < deletion_rate:
            continue
            
        # Check substitution
        if substitution_rate > 0.0 and rng.random() < substitution_rate:
            sub_choices = [x for x in alphabet if x != sym]
            if sub_choices:
                out.append(rng.choice(sub_choices))
            else:
                out.append(sym)
        else:
            out.append(sym)
            
    # Trailing insertion opportunity
    if insertion_rate > 0.0 and rng.random() < insertion_rate:
        out.append(rng.choice(alphabet))
        
    return out
