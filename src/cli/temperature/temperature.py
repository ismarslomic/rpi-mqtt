#!/usr/bin/env python3
"""Service for reading the Rpi temperatures (i.e for CPU and GPU) by running linux commands"""

import subprocess

import psutil

from cli.temperature.types import HwTemperature


def read_temperature() -> list[HwTemperature]:
    """Read available temperatures for hardware components, such as for CPU and GPU"""

    temps: list[HwTemperature] = __read_temperatures()
    temps.append(__read_gpu_temperature())

    return temps


def __read_temperatures() -> list[HwTemperature]:
    """Read available temperatures, such as for CPU and ADC"""
    hw_temperatures: list[HwTemperature] = []

    # doc: https://psutil.readthedocs.io/en/latest/
    temps: dict = psutil.sensors_temperatures()
    if not temps:
        return hw_temperatures

    for temp_name, temp_measurements in temps.items():
        for temp_measurement in temp_measurements:
            hw_temperatures.append(
                HwTemperature(
                    name=temp_measurement["label"] or temp_name,
                    current=temp_measurement["current"],
                    high=temp_measurement["high"],
                    critical=temp_measurement["critical"],
                )
            )

    return hw_temperatures


def __read_gpu_temperature() -> HwTemperature:
    """Read GPU temperature of the RPI"""

    # doc: https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd
    args = ["vcgencmd", "measure_temp"]
    result = subprocess.run(args, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        raise RuntimeError("Failed to read GPU temperature", result.stderr)

    # result.stdout: temp=51.0'C
    temp: float = result.stdout.replace("\n", "").replace("temp=", "").replace("'C", "")

    return HwTemperature(name="gpu", current=temp, high=None, critical=None)
