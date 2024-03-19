#!/usr/bin/env python3
"""Interface for Rpi sensors API"""
from abc import ABC, abstractmethod


class RpiSensor(ABC):
    """Abstract base class for Rpi sensors, defining the common API."""

    name: str
    """Name of this sensor. Must be unique across all sensors."""

    def __init__(self, enabled: bool):
        self._enabled = enabled

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
