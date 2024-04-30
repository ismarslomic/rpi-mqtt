#!/usr/bin/env python3
"""Interface for Rpi sensors API"""
import logging
from abc import ABC, abstractmethod


class RpiSensor(ABC):
    """Abstract base class for Rpi sensors, defining the common API."""

    logger: logging.Logger

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of this sensor. Must be unique across all sensors."""
        raise NotImplementedError("Property name must be implemented in sensor sub-class.")

    @property
    @abstractmethod
    def state(self) -> object | None:
        """Get the current state for this sensor."""
        raise NotImplementedError("Property get state must be implemented in sensor sub-class.")

    def __init__(self, enabled: bool):
        self._enabled = enabled
        logger_name: str = f"{__name__}.{self.name}"
        self.logger = logging.getLogger(logger_name)

        try:
            self.refresh_state()
            self._available = True
        except SensorNotAvailableException:
            self._available = False

    @abstractmethod
    def refresh_state(self) -> None:
        """Refresh current state of this sensor and update the state property."""

        raise NotImplementedError("read() must be implemented in sensor sub-class.")

    def available(self) -> bool:
        """Indicate if this sensor is available on running Rpi platform."""

        return self._available

    def enabled(self) -> bool:
        """Indicates if this sensor is enabled by the user."""

        return self._enabled


class SensorNotAvailableException(Exception):
    """Exception class indicating a sensor is not available."""
