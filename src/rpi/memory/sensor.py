#!/usr/bin/env python3
"""Service for reading the Rpi memory usage"""
from collections import namedtuple

import psutil

from rpi.memory.types import MemoryUse
from rpi.types import RpiSensor, SensorNotAvailableException
from rpi.utils import bytes_to_gibibytes, round_percent


class MemoryUseSensor(RpiSensor):
    """Sensor for memory usage"""

    name: str = "Memory use"

    def read(self) -> MemoryUse:
        return read_memory_use()


def read_memory_use() -> MemoryUse:
    """Read statistics about system memory usage"""

    # doc: https://psutil.readthedocs.io/en/latest/
    if not hasattr(psutil, "virtual_memory"):
        raise SensorNotAvailableException("virtual_memory() not available for this Rpi")

    memory: namedtuple = psutil.virtual_memory()

    return MemoryUse(
        total_gib=bytes_to_gibibytes(memory.total),
        available_gib=bytes_to_gibibytes(memory.available),
        used_pct=round_percent(memory.percent),
    )
