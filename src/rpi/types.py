#!/usr/bin/env python3
"""Interface for Rpi sensors"""
from abc import ABC, abstractmethod


class RpiSensor(ABC):
    """Abstract base class for all Rpi sensors, defining the common API."""

    name: str
    """Name of the sensor. Must be unique across all sensors."""

    @abstractmethod
    def read(self):
        """Read sensor data."""

        raise NotImplementedError("read() must be implemented in sensor sub-class.")

    def available(self) -> bool:
        """Indicate if a sensor is available in Rpi environment it is running."""

        try:
            self.read()
            return True
        except SensorNotAvailableException:
            return False


class SensorNotAvailableException(Exception):
    """Exception class indicating a sensor is not available."""
