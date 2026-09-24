"""
Monograph Sections Data Aggregator
Exposes get_section_1 through get_section_14 and get_references
"""

try:
    from docs.monograph_part1 import (
        get_section_1, get_section_2, get_section_3,
        get_section_4, get_section_5
    )
    from docs.monograph_part2 import (
        get_section_6, get_section_7, get_section_8,
        get_section_9, get_section_10, get_section_11,
        get_section_12, get_section_13, get_section_14,
        get_references, get_appendix
    )
except ImportError:
    from monograph_part1 import (
        get_section_1, get_section_2, get_section_3,
        get_section_4, get_section_5
    )
    from monograph_part2 import (
        get_section_6, get_section_7, get_section_8,
        get_section_9, get_section_10, get_section_11,
        get_section_12, get_section_13, get_section_14,
        get_references, get_appendix
    )
