#!/usr/bin/env python3
"""Service for reading the Rpi model"""
from sensors.types import RpiSensor, SensorNotAvailableException


class RpiModelSensor(RpiSensor):
    """Sensor for Rpi model"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "rpi_model"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_rpi_model()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_rpi_model(self) -> str:
        """Read Rpi model"""

        model_file_name = "/sys/firmware/devicetree/base/model"

        try:
            with open(model_file_name, "r", encoding="utf-8") as f:
                model = f.readline().strip("\x00")

            return model
        except FileNotFoundError as err:
            self.logger.warning("Rpi model file not available for this Rpi")
            raise SensorNotAvailableException("rpi model file not available for this Rpi") from err
