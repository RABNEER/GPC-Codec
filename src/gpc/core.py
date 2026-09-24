"""
Core Generalized Patha Code (GPC) Codec Implementation
"""

from collections import defaultdict
from typing import List, Tuple, Dict, Optional, Union
from .decoder import decode_gpc_burst_deletion, decode_gpc_erasure

class GeneralizedPathaCode:
    """
    Generalized Patha Code (GPC) Parameterized Codec.
    
    Attributes:
        K (int): Number of information/payload symbols.
        M (int): Total block length (M = 13K + 6).
        rate (float): Code rate R = K / M.
        pilots (List[int]): Deterministic pilot anchor coordinates.
        spans (Dict[int, int]): Coordinate span for each symbol 1..K.
        BE (int): Minimum span, equal to exact marked burst-erasure capability.
    """
    def __init__(self, K: int = 4):
        if K < 2:
            raise ValueError("Message dimension K must be >= 2")
        self.K = K
        self.placement = self._build_placement()
        self.M = len(self.placement)
        self.rate = self.K / self.M
        self.pilots = [0, 2*K + 1, 4*K + 2, 7*K + 3, 10*K + 4, 13*K + 5]
        self.spans = self._compute_spans()
        self.BE = min(self.spans.values())

    def _build_placement(self) -> List[int]:
        K = self.K
        placement = []
        def add_cycle(pass_type: str):
            placement.append(0)  # Pilot anchor
            for i in range(K):
                s0 = i + 1
                s1 = ((i + 1) % K) + 1
                s2 = ((i + 2) % K) + 1
                if pass_type == 'F2':
                    placement.extend([s0, s1])
                elif pass_type == 'B2':
                    placement.extend([s1, s0])
                elif pass_type == 'F3':
                    placement.extend([s0, s1, s2])
                elif pass_type == 'B3':
                    placement.extend([s2, s1, s0])
        add_cycle('F2')
        add_cycle('B2')
        add_cycle('F3')
        add_cycle('B3')
        add_cycle('F3')
        placement.append(0)  # Final pilot anchor
        return placement

    def _compute_spans(self) -> Dict[int, int]:
        pos = defaultdict(list)
        for idx, sym in enumerate(self.placement):
            if sym > 0:
                pos[sym].append(idx)
        return {j: (max(pos[j]) - min(pos[j])) if len(pos[j]) >= 2 else 0 for j in range(1, self.K + 1)}

    def encode(self, message: Union[List[int], Tuple[int, ...]]) -> List[int]:
        if len(message) != self.K:
            raise ValueError(f"Message length must be {self.K}, got {len(message)}")
        return [1 if sym == 0 else message[sym - 1] for sym in self.placement]

    def decode(self, received: List[Optional[int]]) -> Optional[Tuple[int, ...]]:
        N = len(received)
        if N == self.M:
            if any(bit is None for bit in received):
                return decode_gpc_erasure(received, self.placement, self.K)
            return decode_gpc_erasure(received, self.placement, self.K)
        elif N < self.M:
            b = self.M - N
            return decode_gpc_burst_deletion(tuple(received), b, self.K, self.placement, self.pilots)
        else:
            raise ValueError(f"Received length {N} exceeds block length {self.M}")
