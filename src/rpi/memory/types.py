#!/usr/bin/env python3
"""Types in module Memory"""

from dataclasses import dataclass


@dataclass
class MemoryUse:
    """Class representing memory usage reading"""

    total: float
    """Total physical memory (exclusive swap), in gibibytes (GiB). Example: '7.86'"""

    available: float
    """The memory available, without the system going into swap, in gibibytes (GiB). Example: '6.43'"""

    used_percent: float
    """The memory used in percentage. Example: '18.2'"""
