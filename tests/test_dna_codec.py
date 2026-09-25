"""
Unit tests for BC-DNA Constrained Codec and Goldman baseline.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from dna_codec import ConstrainedDNACodec, Goldman2013Codec, generate_rll2_codebook

def test_codebook_constraints():
    """Verify 256-word codebook satisfies RLL-2 and GC balance (40% - 60%)."""
    byte_to_dna, dna_to_byte = generate_rll2_codebook()
    assert len(byte_to_dna) == 256
    assert len(dna_to_byte) == 256

    for b, word in byte_to_dna.items():
        assert len(word) == 5
        # Check homopolymer run <= 2
        for i in range(len(word) - 2):
            assert not (word[i] == word[i+1] == word[i+2])
        # Check GC count is 2 or 3
        gc = sum(1 for c in word if c in ('G', 'C'))
        assert gc in (2, 3)
        # Check boundary isolation
        assert word[0] != word[1]
        assert word[-1] != word[-2]

def test_dna_codec_roundtrip():
    """Verify clean roundtrip for ConstrainedDNACodec."""
    codec = ConstrainedDNACodec()
    payload = b"Hello, DNA Storage World! 1234567890 GPC Codec Verification."
    encoded = codec.encode(payload)
    
    # Check max homopolymer run across encoded stream is <= 2
    for i in range(len(encoded) - 2):
        assert not (encoded[i] == encoded[i+1] == encoded[i+2])
        
    decoded_bytes, blocks_processed, resync_count = codec.decode(encoded, expected_bytes=len(payload))
    assert decoded_bytes == payload
    assert blocks_processed > 0

def test_goldman_baseline_roundtrip():
    """Verify Goldman (2013) ternary differential baseline roundtrip."""
    codec = Goldman2013Codec()
    payload = b"Goldman 2013 Baseline Test"
    encoded = codec.encode(payload)
    
    # Goldman guarantees no consecutive identical bases (k=1)
    for i in range(len(encoded) - 1):
        assert encoded[i] != encoded[i+1]
        
    decoded = codec.decode(encoded, expected_bytes=len(payload))
    assert decoded == payload
