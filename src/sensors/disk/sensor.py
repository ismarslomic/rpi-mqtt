#!/usr/bin/env python3
"""Service for reading the Rpi disk usage"""

from collections import namedtuple

import psutil

from sensors.disk.types import DiskUse
from sensors.types import RpiSensor, SensorNotAvailableException
from sensors.utils import bytes_to_gibibytes, round_percent


class DiskUseSensor(RpiSensor):
    """Sensor for disk usage"""

    _state: DiskUse | None = None

    @property
    def name(self) -> str:
        return "disk_use"

    @property
    def state(self) -> DiskUse | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_disk_use()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_disk_use(self) -> DiskUse:
        """Read statistics about disk usage for path '/'"""

        # doc: https://psutil.readthedocs.io/en/latest/
        if not hasattr(psutil, "disk_usage"):
            self.logger.warning("This platform does not support psutil.disk_usage()")
            raise SensorNotAvailableException("disk_usage() not available for this Rpi")

        path = "/"
        disk_usage: namedtuple = psutil.disk_usage(path)

        return DiskUse(
            path=path,
            total_gib=bytes_to_gibibytes(disk_usage.total),
            used_gib=bytes_to_gibibytes(disk_usage.used),
            used_pct=round_percent(disk_usage.percent),
            free_gib=bytes_to_gibibytes(disk_usage.free),
        )
