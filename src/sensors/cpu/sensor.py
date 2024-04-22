#!/usr/bin/env python3
"""Service for reading the Rpi CPU usage"""

import psutil

from sensors.cpu.types import LoadAverage
from sensors.types import RpiSensor, SensorNotAvailableException
from sensors.utils import round_percent


class CpuUsePctSensor(RpiSensor):
    """Sensor for CPU usage in percent"""

    name: str = "CPU use percent"

    def read(self) -> float:
        self.logger.debug("Reading sensor data")

        return self._read_cpu_use_percent()

    def _read_cpu_use_percent(self) -> float:
        """Return a float representing the current system-wide CPU utilization as a percentage"""

        # doc: https://psutil.readthedocs.io/en/latest/
        if not hasattr(psutil, "cpu_percent"):
            self.logger.warning("This platform does not support psutil.cpu_percent()")
            raise SensorNotAvailableException("cpu_percent() not available for this Rpi")

        cpu_use_percent: float = psutil.cpu_percent(interval=0.1)

        self.logger.debug("Reading sensor data successfully")

        return cpu_use_percent


class CpuLoadAvgSensor(RpiSensor):
    """Sensor for CPU load in average"""

    name: str = "CPU load average"

    def read(self) -> LoadAverage:
        self.logger.debug("Reading sensor data")

        return self._read_load_average()

    def _read_load_average(self) -> LoadAverage:
        """Return the average system load in percent related to number of cpu cores over the last 1, 5 and 15 minutes"""

        # doc: https://psutil.readthedocs.io/en/latest/
        if not hasattr(psutil, "cpu_count"):
            self.logger.warning("This platform does not support psutil.cpu_count()")
            raise SensorNotAvailableException("cpu_count() not available for this Rpi")

        if not hasattr(psutil, "getloadavg"):
            self.logger.warning("This platform does not support psutil.getloadavg()")
            raise SensorNotAvailableException("getloadavg() not available for this Rpi")

        cpu_cores: int = psutil.cpu_count()
        load_avg: tuple[float, float, float] = psutil.getloadavg()
        load_avg_percent: list[float] = [x / cpu_cores * 100 for x in load_avg]

        self.logger.debug("Reading sensor data successfully")

        return LoadAverage(
            cpu_cores=cpu_cores,
            load_1min_pct=round_percent(load_avg_percent[0]),
            load_5min_pct=round_percent(load_avg_percent[1]),
            load_15min_pct=round_percent(load_avg_percent[2]),
        )
