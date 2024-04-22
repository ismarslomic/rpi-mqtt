#!/usr/bin/env python3
"""Service for reading the Rpi temperatures (i.e. for CPU and GPU) by running linux commands"""

import subprocess
from collections import defaultdict

import psutil

from sensors.temperature.types import HwTemperature
from sensors.types import RpiSensor, SensorNotAvailableException
from sensors.utils import round_temp


class TemperatureSensor(RpiSensor):
    """Sensor for temperature"""

    name: str = "Temperature"

    def read(self) -> dict[str, HwTemperature]:
        self.logger.debug("Reading sensor data")
        return self._read_temperature()

    def _read_temperature(self) -> dict[str, HwTemperature]:
        """Read available temperatures for hardware components, such as for CPU and GPU"""

        temps: dict[str, HwTemperature] = self._read_temperatures()
        gpu_temp = self._read_gpu_temperature()
        temps["gpu"] = gpu_temp

        self.logger.debug("Reading sensor data successfully")
        return temps

    def _read_temperatures(self) -> dict[str, HwTemperature]:
        """Read available temperatures, such as for CPU and ADC using the psutil module"""
        hw_temperatures: dict[str, HwTemperature] = {}

        # doc: https://psutil.readthedocs.io/en/latest/
        if not hasattr(psutil, "sensors_temperatures"):
            self.logger.warning("psutil sensors_temperatures() not available for this Rpi")
            raise SensorNotAvailableException("sensors_temperatures() not available for this Rpi")

        temps: defaultdict[str, list] = psutil.sensors_temperatures()

        if not temps:
            self.logger.warning("none temperatures detected for this Rpi")
            raise SensorNotAvailableException("none temperatures detected for this Rpi")

        for temp_name, temp_measurements in temps.items():
            for temp_measurement in temp_measurements:
                name: str = temp_measurement.label or temp_name
                hw_temperatures[name] = HwTemperature(
                    current_c=round_temp(temp_measurement.current),
                    high_c=temp_measurement.high,
                    critical_c=temp_measurement.critical,
                )

        self.logger.debug("Reading hw temperatures successfully")
        return hw_temperatures

    def _read_gpu_temperature(self) -> HwTemperature:
        """Read GPU temperature of the RPI using the RPI vcgencmd cli"""

        # doc: https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd
        args = ["vcgencmd", "measure_temp"]
        try:
            result = subprocess.run(args, capture_output=True, text=True, check=False)
        except FileNotFoundError as err:
            self.logger.warning("vcgencmd not available for this Rpi")
            raise SensorNotAvailableException("vcgencmd not available for this Rpi") from err

        if result.returncode != 0:
            self.logger.warning(
                f"Process 'vcgencmd measure_temp' returned code: {str(result.returncode)}, err: {str(result.stderr)}"
            )
            raise SensorNotAvailableException("Failed to read GPU temperature", result.stderr)

        # result.stdout: temp=51.0'C
        temp_str: str = result.stdout.replace("\n", "").replace("temp=", "").replace("'C", "")
        temp_rounded_c: float = round_temp(temp=float(temp_str))

        self.logger.debug("Reading gpu temperature successfully")
        return HwTemperature(current_c=temp_rounded_c, high_c=None, critical_c=None)
