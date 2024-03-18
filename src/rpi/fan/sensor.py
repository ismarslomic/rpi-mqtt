#!/usr/bin/env python3
"""Service for reading the Rpi fans speed"""
import psutil

from rpi.fan.types import FanSpeed
from rpi.types import RpiSensor, SensorNotAvailableException


class FanSpeedSensor(RpiSensor):
    """Sensor for fan speed"""

    name: str = "Fan speed"

    def read(self) -> dict[str, FanSpeed]:
        return read_fans_speed()


def read_fans_speed() -> dict[str, FanSpeed]:
    """Read Rpi hardware fans speed

    As the temperature of the Raspberry Pi increases, the official RPi fans reacts in the following way:

    - below 50°C, the fan does not spin at all (0% speed)
    - at 50°C, the fan turns on at a low speed (30% speed)
    - at 60°C, the fan speed increases to a medium speed (50% speed)
    - at 67.5°C, the fan speed increases to a high speed (70% speed)
    - at 75°C the fan increases to full speed (100% speed)

    The same mapping of temperature ranges to fan speeds applies to temperature decreases as well,
    with a 5°C hysteresis; fan speed decreases when the temperature drops to 5°C below each of the above thresholds.

    """

    # RPi doc: https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html#cooling-raspberry-pi-5
    # psutil doc: https://psutil.readthedocs.io/en/latest/
    fans_speed: dict[str, FanSpeed] = {}

    if not hasattr(psutil, "sensors_fans"):
        raise SensorNotAvailableException("sensors_fans() not available for this Rpi")

    fans: dict[str, list] = psutil.sensors_fans()

    if not fans:
        raise SensorNotAvailableException("none fans detected for this Rpi")

    for fan_name, fan_measurements in fans.items():
        for fan_measurement in fan_measurements:
            name: str = fan_measurement.label or fan_name
            fans_speed[name] = FanSpeed(curr_speed_rpm=fan_measurement.current)

    return fans_speed
