#!/usr/bin/env python3
"""Common types in module Sensors"""

import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, List

from date_utils import now_to_iso_datetime
from settings.types import ScriptSettings


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


class AllRpiSensors:
    """Class representing all sensors"""

    sensors: List[RpiSensor] = []
    available_sensors: List[RpiSensor] = []
    update_interval: int
    sensors_total: int = 0
    sensors_available: int = 0

    def __init__(self, sensors: List[RpiSensor], script_settings: ScriptSettings):
        self.sensors = sensors

        for sensor in self.sensors:
            if sensor.available():
                self.available_sensors.append(sensor)

        self.update_interval = script_settings.update_interval
        self.sensors_total = len(self.sensors)
        self.sensors_available = len(self.available_sensors)

    def _metadata_properties(self) -> dict[str, str | int]:
        """Returns dictionary with metadata properties"""
        return {
            "states_refresh_ts": now_to_iso_datetime(),
            "update_interval": self.update_interval,
            "sensors_total": self.sensors_total,
            "sensors_available": self.sensors_available,
        }

    def refresh_available_sensors(self):
        """Refreshes state of all sensors that are available for this Rpi."""

        for sensor in self.available_sensors:
            sensor.refresh_state()

    def as_dict(self) -> OrderedDict:
        """Sensor states as ordered dict"""

        sensors_as_dict: OrderedDict = OrderedDict()

        # Loop all sensors and add to ordered dictionary
        for sensor in self.available_sensors:
            sensors_as_dict[sensor.name] = sensor.state_as_dict

        # Add metadata properties
        sensors_as_dict["metadata"] = self._metadata_properties()

        return sensors_as_dict


class SensorNotAvailableException(Exception):
    """Exception class indicating a sensor is not available."""
