"""
RLL-2 / GC-Balanced Constrained DNA Codec (BC-DNA)
==================================================
A deterministic, high-density constrained sequence code for synthetic DNA data storage.

Key Mathematical Properties:
1. Strict Homopolymer Constraint: Maximum run length k <= 2 across entire stream (including word boundaries).
2. Strict GC Content Constraint: Every 5-mer has 40% or 60% GC content (mean 50.0%).
3. Code Rate: Exactly 8 bits / 5 nucleotides = 1.600 bits/nt (20.0% higher density than Goldman 2013).
4. Deterministic O(1) byte-to-5mer lookup table.
5. Periodic Bounded-Slip Markers (BSM) for drift confinement on insertion/deletion channels.
"""

import itertools
from typing import List, Tuple, Dict, Optional

# Nucleotide alphabet
BASES = ['A', 'C', 'G', 'T']

def _max_homopolymer_run(seq: str) -> int:
    """Computes the maximum consecutive identical nucleotide run length."""
    if not seq:
        return 0
    m = 1
    c = 1
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            c += 1
            m = max(m, c)
        else:
            c = 1
    return m

def _gc_count(seq: str) -> int:
    """Counts G and C nucleotides in sequence."""
    return sum(1 for b in seq if b in ('G', 'C'))

def generate_rll2_codebook() -> Tuple[Dict[int, str], Dict[str, int]]:
    """
    Generates the bijective 256-word codebook mapping byte [0..255] -> 5-mer.
    Each 5-mer satisfies:
      1. Internal run length <= 2.
      2. GC count in {2, 3} (40% to 60%).
      3. First two bases distinct (s[0] != s[1]).
      4. Last two bases distinct (s[-1] != s[-2]).
    Because s[0] != s[1] and s[-1] != s[-2], concatenation of any two words
    guarantees maximum boundary run <= 2.
    """
    candidates = []
    for p in itertools.product(BASES, repeat=5):
        s = "".join(p)
        if _max_homopolymer_run(s) <= 2 and 2 <= _gc_count(s) <= 3:
            if s[0] != s[1] and s[-1] != s[-2]:
                candidates.append(s)
    
    # Sort deterministically
    candidates.sort()
    
    # Select first 256 words
    byte_to_dna = {i: candidates[i] for i in range(256)}
    dna_to_byte = {candidates[i]: i for i in range(256)}
    return byte_to_dna, dna_to_byte

# Initialize global tables
BYTE_TO_5MER, FIVE_MER_TO_BYTE = generate_rll2_codebook()

# Bounded-Slip Marker (BSM)
# A biologically compliant marker sequence with minimum aperiodic autocorrelation sidelobe (= 1)
# Length = 8 nt, k <= 2, GC = 50%, with single-nucleotide boundaries (s[0] != s[1], s[-1] != s[-2])
# Mathematically guarantees global maximum homopolymer run length <= 2 across entire stream.
SYNC_MARKER = "ACAGTCGA"

class BCDNACodec:
    """
    Bounded-Slip Constrained DNA Codec (BC-DNA).
    Encodes byte streams into DNA with k <= 2, GC in [40%, 60%], and periodic sync markers.
    """
    def __init__(self, block_size_bytes: int = 16):
        """
        Args:
            block_size_bytes: Number of data bytes per synchronization block.
                              Default 16 bytes = 80 nt payload + 8 nt marker.
                              Total rate = (16 * 8) / (80 + 8) = 128 / 88 = 1.454 bits/nt.
        """
        self.block_size = block_size_bytes
        self.marker = SYNC_MARKER
        self.marker_len = len(self.marker)

    @property
    def raw_rate(self) -> float:
        """Raw code rate without markers (bits/nt)."""
        return 8.0 / 5.0  # 1.60 bits/nt

    @property
    def effective_rate(self) -> float:
        """Effective code rate including synchronization markers (bits/nt)."""
        payload_bits = self.block_size * 8
        total_nt = (self.block_size * 5) + self.marker_len
        return payload_bits / total_nt

    def encode(self, data: bytes) -> str:
        """Encodes raw byte stream into DNA string with periodic sync markers."""
        dna_blocks = []
        n = len(data)
        
        for i in range(0, n, self.block_size):
            chunk = data[i:i + self.block_size]
            block_dna = "".join(BYTE_TO_5MER[b] for b in chunk)
            dna_blocks.append(block_dna + self.marker)
            
        return "".join(dna_blocks)

    def decode(self, received_dna: str, expected_bytes: int, search_window: int = 12) -> Tuple[bytes, int, int]:
        """
        Decodes received DNA stream back to bytes, using sync markers to realign against drift.
        
        Args:
            received_dna: Noisy or shifted DNA sequence from sequencing channel.
            expected_bytes: Original payload length in bytes.
            search_window: Maximum drift displacement (+/- nt) searched around expected marker position.
            
        Returns:
            Tuple of (recovered_bytes, num_recovered_blocks, num_drift_resyncs)
        """
        recovered_bytes = bytearray()
        pos = 0
        total_len = len(received_dna)
        bytes_remaining = expected_bytes
        resync_count = 0
        blocks_processed = 0

        while pos < total_len and bytes_remaining > 0:
            current_block_bytes = min(self.block_size, bytes_remaining)
            expected_payload_nt = current_block_bytes * 5
            
            # 1. Check if enough sequence remains
            if pos + expected_payload_nt > total_len:
                break
                
            # 2. Extract local payload nucleotides
            payload_slice = received_dna[pos:pos + expected_payload_nt]
            
            # Decode 5-mers
            block_bytes = bytearray()
            for j in range(0, len(payload_slice) - 4, 5):
                five_mer = payload_slice[j:j+5]
                if five_mer in FIVE_MER_TO_BYTE:
                    block_bytes.append(FIVE_MER_TO_BYTE[five_mer])
                else:
                    # Nearest hamming neighbor fallback
                    best_byte = 0
                    best_dist = 99
                    for candidate, b_val in FIVE_MER_TO_BYTE.items():
                        d = sum(1 for a, b in zip(five_mer, candidate) if a != b)
                        if d < best_dist:
                            best_dist = d
                            best_byte = b_val
                            if d <= 1:
                                break
                    block_bytes.append(best_byte)
                    
            recovered_bytes.extend(block_bytes)
            bytes_remaining -= len(block_bytes)
            blocks_processed += 1
            
            # 3. Locate synchronization marker to realign frame
            nominal_marker_pos = pos + expected_payload_nt
            best_match_pos = nominal_marker_pos
            best_score = -1
            min_drift = 999

            # Windowed correlation search for marker
            w_start = max(0, nominal_marker_pos - search_window)
            w_end = min(total_len - self.marker_len + 1, nominal_marker_pos + search_window + 1)
            
            for candidate_pos in range(w_start, w_end):
                sub = received_dna[candidate_pos:candidate_pos + self.marker_len]
                match_score = sum(1 for a, b in zip(sub, self.marker) if a == b)
                drift_dist = abs(candidate_pos - nominal_marker_pos)
                
                # Prioritize higher score, break ties by proximity to nominal position
                if (match_score > best_score) or (match_score == best_score and drift_dist < min_drift):
                    best_score = match_score
                    best_match_pos = candidate_pos
                    min_drift = drift_dist

            # If marker found with high fidelity (at least 6/8 bases matching), realign
            if best_score >= 6:
                drift = best_match_pos - nominal_marker_pos
                if drift != 0:
                    resync_count += 1
                pos = best_match_pos + self.marker_len
            else:
                # Nominal advance if marker lost
                pos = nominal_marker_pos + self.marker_len

        # Pad or trim to expected size
        if len(recovered_bytes) < expected_bytes:
            recovered_bytes.extend(b'\x00' * (expected_bytes - len(recovered_bytes)))
        else:
            recovered_bytes = recovered_bytes[:expected_bytes]

        return bytes(recovered_bytes), blocks_processed, resync_count


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

class NaiveDirectCodec:
    """
    Baseline 1: Naive 2-bit direct nucleotide mapping.
    00 -> A, 01 -> C, 10 -> G, 11 -> T.
    Rate = 2.0 bits/nt.
    Has unbounded homopolymers and uncontrolled GC content.
    """
    BIT_TO_BASE = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    BASE_TO_BIT = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}

    @property
    def raw_rate(self) -> float:
        return 2.0

    @property
    def effective_rate(self) -> float:
        return 2.0

    def encode(self, data: bytes) -> str:
        dna = []
        for b in data:
            bits = f"{b:08b}"
            for k in range(0, 8, 2):
                dna.append(self.BIT_TO_BASE[bits[k:k+2]])
        return "".join(dna)

    def decode(self, received_dna: str, expected_bytes: int) -> bytes:
        bits = []
        for b in received_dna:
            bits.append(self.BASE_TO_BIT.get(b, '00'))
        bit_str = "".join(bits)
        out = bytearray()
        for i in range(0, len(bit_str) - 7, 8):
            out.append(int(bit_str[i:i+8], 2))
        if len(out) < expected_bytes:
            out.extend(b'\x00' * (expected_bytes - len(out)))
        return bytes(out[:expected_bytes])


class GoldmanNature2013Codec:
    """
    Baseline 2: Goldman et al. (Nature 2013) base-3 ternary differential codec.
    Rate = 8 / 6 = 1.333 bits/nt.
    Guarantees k = 1 (no adjacent duplicate bases).
    """
    BASES = ['A', 'C', 'G', 'T']

    @property
    def raw_rate(self) -> float:
        return 8.0 / 6.0  # 1.333 bits/nt

    @property
    def effective_rate(self) -> float:
        return 8.0 / 6.0

    def encode(self, data: bytes) -> str:
        dna = []
        prev = 'A'
        for b in data:
            val = b
            trits = []
            for _ in range(6):
                trits.append(val % 3)
                val //= 3
            for t in trits:
                avail = [x for x in self.BASES if x != prev]
                chosen = avail[t]
                dna.append(chosen)
                prev = chosen
        return "".join(dna)

    def decode(self, received_dna: str, expected_bytes: int) -> bytes:
        out = bytearray()
        prev = 'A'
        for i in range(0, len(received_dna) - 5, 6):
            trits = []
            for j in range(6):
                curr = received_dna[i + j]
                avail = [x for x in self.BASES if x != prev]
                if curr in avail:
                    trits.append(avail.index(curr))
                else:
                    trits.append(0)
                prev = curr
            val = sum(t * (3 ** k) for k, t in enumerate(trits))
            out.append(val % 256)
        if len(out) < expected_bytes:
            out.extend(b'\x00' * (expected_bytes - len(out)))
        return bytes(out[:expected_bytes])
