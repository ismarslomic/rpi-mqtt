#!/usr/bin/env python3
"""Interface for Rpi sensors API"""
import logging
from abc import ABC, abstractmethod
from typing import List


class CommonLogger(ABC):
    """Common logger interface, defining functions for logging info, debug and warning messages."""

    @abstractmethod
    def info(self, msg: str):
        """Log an info message."""

    @abstractmethod
    def debug(self, msg: str):
        """Log a debug message."""

    @abstractmethod
    def warning(self, msg: str):
        """Log a warning message."""


class SensorLogger(CommonLogger):
    """Sensor logger class."""

    def __init__(self, sensor: str):
        self.sensor: str = sensor
        self.warnings: List[str] = []

    def info(self, msg: str):
        logging.info(self._get_logging_message(msg))

    def debug(self, msg: str):
        logging.debug(self._get_logging_message(msg))

    def warning(self, msg: str):
        logging.warning(self._get_logging_message(msg))

    def configure(self, sensor: str):
        """Configure logger with the given <sensor>."""
        self.sensor = sensor

    def _get_logging_message(self, msg: str) -> str:
        _msg = msg if msg else "<no message>"
        _sensor = self.sensor if self.sensor else "<none>"

        columns = [
            "[sensor]",
            f"[{_sensor}]",
            _msg,
        ]
        return " ".join(columns)


class RpiSensor(ABC):
    """Abstract base class for Rpi sensors, defining the common API."""

    name: str
    """Name of this sensor. Must be unique across all sensors."""

    logger: SensorLogger

    def __init__(self, enabled: bool):
        self._enabled = enabled
        self.logger = SensorLogger(self.name)

        try:
            self.read()
            self._available = True
        except SensorNotAvailableException:
            self._available = False

    @abstractmethod
    def read(self) -> object:
        """Returning the latest state of the sensor."""

        raise NotImplementedError("read() must be implemented in sensor sub-class.")

    def available(self) -> bool:
        """Indicate if this sensor is available on running Rpi platform."""

        return self._available

    def enabled(self) -> bool:
        """Indicates if this sensor is enabled by the user."""

        return self._enabled


class SensorNotAvailableException(Exception):
    """Exception class indicating a sensor is not available."""
