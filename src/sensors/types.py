#!/usr/bin/env python3
"""Interface for Rpi sensors API"""

import logging
from abc import ABC, abstractmethod
from typing import Any


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
    def state(self) -> dict | object | None:
        """Get the current state for this sensor."""
        raise NotImplementedError("Property get state must be implemented in sensor sub-class.")

    @property
    def state_as_dict(self) -> dict | float | int | str | None:
        """Get the current state for this sensor as dictionary or plain value. Useful for JSON serializing."""
        if hasattr(self.state, "__dict__"):
            return vars(self.state)

        return self.state

    @property
    def _nested_state_as_dict(self) -> dict[str, dict[str, Any]] | None:
        """Get the current state for this sensor as dictionary or plain value. Useful for JSON serializing."""

        if not self.available():
            return None

        state_dict: dict[str, dict[str, Any]] = {}

        for key, value in self.state.items():
            state_dict[key] = vars(value)

        return state_dict

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
