#!/usr/bin/env python3
"""Service for reading the Rpi memory usage"""
from collections import namedtuple

import psutil

from sensors.memory.types import MemoryUse
from sensors.types import RpiSensor, SensorNotAvailableException
from sensors.utils import bytes_to_gibibytes, round_percent


class MemoryUseSensor(RpiSensor):
    """Sensor for memory usage"""

    _state: MemoryUse | None = None

    @property
    def name(self) -> str:
        return "memory_use"

    @property
    def state(self) -> MemoryUse | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_memory_use()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_memory_use(self) -> MemoryUse:
        """Read statistics about system memory usage"""

        # doc: https://psutil.readthedocs.io/en/latest/
        if not hasattr(psutil, "virtual_memory"):
            self.logger.warning("This platform does not support psutil.virtual_memory()")
            raise SensorNotAvailableException("virtual_memory() not available for this Rpi")

        memory: namedtuple = psutil.virtual_memory()

        return MemoryUse(
            total_gib=bytes_to_gibibytes(memory.total),
            available_gib=bytes_to_gibibytes(memory.available),
            used_pct=round_percent(memory.percent),
        )
