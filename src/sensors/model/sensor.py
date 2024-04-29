#!/usr/bin/env python3
"""Service for reading the Rpi model"""
from sensors.types import RpiSensor, SensorNotAvailableException


class RpiModelSensor(RpiSensor):
    """Sensor for Rpi model"""

    name: str = "rpi_model"

    def read(self) -> str:
        self.logger.debug("Reading sensor data")

        return self._read_rpi_model()

    def _read_rpi_model(self) -> str:
        """Read Rpi model"""

        model_file_name = "/sys/firmware/devicetree/base/model"

        try:
            with open(model_file_name, "r", encoding="utf-8") as f:
                model = f.readline().strip("\x00")

            self.logger.debug("Reading sensor data successfully")

            return model
        except FileNotFoundError as err:
            self.logger.warning("Rpi model file not available for this Rpi")
            raise SensorNotAvailableException("rpi model file not available for this Rpi") from err
