#!/usr/bin/env python3
"""Service for reading the Rpi fans speed"""
import psutil

from rpi.fan.types import FanSpeed


def read_fans_speed() -> list[FanSpeed]:
    """Read Rpi hardware fans speed"""

    # doc: https://psutil.readthedocs.io/en/latest/
    fans_speed: list[FanSpeed] = []

    fans: dict[str, list] = psutil.sensors_fans()
    if not fans:
        return []

    for fan_name, fan_measurements in fans.items():
        for fan_measurement in fan_measurements:
            fans_speed.append(FanSpeed(name=fan_measurement.label or fan_name, speed_rpm=fan_measurement.current))

    return fans_speed
