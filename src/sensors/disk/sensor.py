#!/usr/bin/env python3
"""Service for reading the Rpi disk usage"""

from collections import namedtuple

import psutil

from sensors.disk.types import DiskUse
from sensors.types import RpiSensor, SensorNotAvailableException
from sensors.utils import bytes_to_gibibytes, round_percent


class DiskUseSensor(RpiSensor):
    """Sensor for disk usage"""

    name: str = "Disk use"

    def read(self) -> DiskUse:
        self.logger.debug("Reading sensor data")
        return self._read_disk_use()

    def _read_disk_use(self) -> DiskUse:
        """Read statistics about disk usage for path '/'"""

        # doc: https://psutil.readthedocs.io/en/latest/
        if not hasattr(psutil, "disk_usage"):
            self.logger.warning("This platform does not support psutil.disk_usage()")
            raise SensorNotAvailableException("disk_usage() not available for this Rpi")

        path = "/"
        disk_usage: namedtuple = psutil.disk_usage(path)

        self.logger.debug("Reading sensor data successfully")
        return DiskUse(
            path=path,
            total_gib=bytes_to_gibibytes(disk_usage.total),
            used_gib=bytes_to_gibibytes(disk_usage.used),
            used_pct=round_percent(disk_usage.percent),
            free_gib=bytes_to_gibibytes(disk_usage.free),
        )
