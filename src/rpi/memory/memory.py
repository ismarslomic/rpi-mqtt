#!/usr/bin/env python3
"""Service for reading the Rpi memory usage"""
from collections import namedtuple

import psutil

from rpi.memory.types import MemoryUse


def read_memory_use() -> MemoryUse:
    """Read statistics about system memory usage"""

    # doc: https://psutil.readthedocs.io/en/latest/
    memory: namedtuple = psutil.virtual_memory()

    return MemoryUse(
        total_gib=__bytes_to_gibibytes(memory.total),
        available_gib=__bytes_to_gibibytes(memory.available),
        used_pct=__round_percent(memory.percent),
    )


def __round_percent(percent: float) -> float:
    """Round percent value to 1 decimal"""

    return round(percent, 1)


def __bytes_to_gibibytes(value_bytes: int) -> float:
    """Convert bytes (B) to gibibytes (GiB) with 2 decimals"""

    value_gibibytes: float = value_bytes / 1024.0 / 1024.0 / 1024.0

    return round(value_gibibytes, 2)
