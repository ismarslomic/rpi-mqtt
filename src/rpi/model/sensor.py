#!/usr/bin/env python3
"""Service for reading the Rpi model"""
from rpi.types import RpiSensor, SensorNotAvailableException


class RpiModelSensor(RpiSensor):
    """Sensor for Rpi model"""

    name: str = "Rpi model"

    def read(self) -> str:
        return read_rpi_model()


def read_rpi_model() -> str:
    """Read Rpi model"""

    model_file_name = "/sys/firmware/devicetree/base/model"

    try:
        with open(model_file_name, "r", encoding="utf-8") as f:
            model = f.readline().strip("\x00")

        return model
    except FileNotFoundError as err:
        raise SensorNotAvailableException("rpi model file not available for this Rpi") from err