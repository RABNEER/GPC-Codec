"""
Comprehensive Unit Tests for gpc_codec and dual-namespace compatibility.
"""

import pytest
import sys
import os

# Ensure local src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

def test_dual_import_equivalence():
    """Verify that both import gpc and import gpc_codec work and expose identical objects."""
    import gpc
    import gpc_codec

    assert gpc.__version__ == gpc_codec.__version__
    assert gpc.GeneralizedPathaCode is gpc_codec.GeneralizedPathaCode
    assert gpc.GPCEncoder is gpc_codec.GPCEncoder
    assert gpc.GPCDecoder is gpc_codec.GPCDecoder
    assert gpc.decode_gpc_burst_deletion is gpc_codec.decode_gpc_burst_deletion
    assert gpc.decode_gpc_erasure is gpc_codec.decode_gpc_erasure
    assert gpc.simulate_burst_deletion is gpc_codec.simulate_burst_deletion
    assert gpc.simulate_burst_erasure is gpc_codec.simulate_burst_erasure
    assert gpc.simulate_transposition is gpc_codec.simulate_transposition
    assert gpc.simulate_mixed_channel is gpc_codec.simulate_mixed_channel

def test_high_level_encoder_decoder_roundtrip():
    """Verify GPCEncoder and GPCDecoder work as drop-in high-level classes."""
    from gpc_codec import GPCEncoder, GPCDecoder

    for K in [4, 6, 8]:
        enc = GPCEncoder(K=K)
        dec = GPCDecoder(K=K)
        
        # Test clean encode/decode
        msg = [1 if i % 2 == 0 else 0 for i in range(K)]
        codeword = enc(msg)
        assert len(codeword) == 13 * K + 6
        
        recovered = dec(codeword)
        assert recovered == tuple(msg)

def test_gpc_decoder_burst_deletion():
    """Verify GPCDecoder recovers messages from unmarked burst deletions."""
    from gpc_codec import GPCEncoder, GPCDecoder, simulate_burst_deletion

    enc = GPCEncoder(K=4)
    dec = GPCDecoder(K=4)
    msg = [1, 0, 1, 1]
    codeword = enc.encode(msg)

    # Test burst deletion b=5 across various start positions
    for start in [0, 5, 12, 20, 35, 45]:
        rx = simulate_burst_deletion(codeword, burst_length=5, start_idx=start)
        assert len(rx) == len(codeword) - 5
        recovered = dec.decode(rx)
        assert recovered == tuple(msg)

def test_gpc_decoder_burst_erasure():
    """Verify GPCDecoder recovers messages from marked burst erasures up to BE."""
    from gpc_codec import GPCEncoder, GPCDecoder, simulate_burst_erasure, GeneralizedPathaCode

    gpc = GeneralizedPathaCode(K=4)
    enc = GPCEncoder(K=4)
    dec = GPCDecoder(K=4)
    msg = [0, 1, 1, 0]
    codeword = enc(msg)

    # Test erasure burst of length BE = 47
    burst_len = gpc.BE
    for start in [0, 5, 10]:
        rx = simulate_burst_erasure(codeword, burst_length=burst_len, start_idx=start)
        assert len(rx) == len(codeword)
        assert rx.count(None) == burst_len
        recovered = dec(rx)
        assert recovered == tuple(msg)

def test_channel_simulators_reproducibility():
    """Verify channel simulation seed determinism."""
    from gpc_codec import (
        simulate_burst_deletion,
        simulate_burst_erasure,
        simulate_transposition,
        simulate_mixed_channel
    )

    data = [1, 0, 1, 0, 1, 1, 0, 0] * 4
    # Burst deletion deterministic
    d1 = simulate_burst_deletion(data, burst_length=4, seed=42)
    d2 = simulate_burst_deletion(data, burst_length=4, seed=42)
    assert d1 == d2

    # Transposition deterministic
    t1 = simulate_transposition(data, num_transpositions=3, seed=123)
    t2 = simulate_transposition(data, num_transpositions=3, seed=123)
    assert t1 == t2

    # Mixed channel deterministic
    m1 = simulate_mixed_channel(data, deletion_rate=0.05, insertion_rate=0.02, substitution_rate=0.03, seed=999)
    m2 = simulate_mixed_channel(data, deletion_rate=0.05, insertion_rate=0.02, substitution_rate=0.03, seed=999)
    assert m1 == m2
