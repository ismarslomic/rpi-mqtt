#!/usr/bin/env python3
"""Common types in module Sensors"""

import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, List

from date_utils import now_to_iso_datetime
from mqtt.types import RpiMqttTopics
from settings.types import ScriptSettings


@dataclass
class MqttDiscoveryMessage:
    """The Mqtt Discovery message containing the discovery payload and topic"""

    payload: dict
    """JSON serializable discovery payload as dictionary."""
    topic: str
    """Discovery topic to publish the payload."""


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

    def mqtt_discovery_messages(self, topics: RpiMqttTopics) -> List[MqttDiscoveryMessage]:
        """Returns list of mqtt discovery messages"""

        raise NotImplementedError("Function mqtt_discovery_messages() must be implemented in sensor sub-class.")

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


@dataclass
class MqttDiscoveryDevice:
    """Mqtt device used for discovery"""

    identifiers: list[str] | None
    """A list of IDs that uniquely identify the device. For example a serial number."""
    name: str | None
    """The name of the device."""
    manufacturer: str | None
    """The manufacturer of the device."""
    model: str | None
    """The model of the device."""
    sw_version: str | None
    """The firmware version of the device."""
    serial_number: str | None = None
    """The serial number of the device."""
    hw_version: str | None = None
    """The hardware version of the device."""
    configuration_url: str | None = None
    """A link to the webpage that can manage the configuration of this device."""


@dataclass
class MqttDiscoveryEntity:
    """Mqtt entity used for discovery"""

    name: str | None = None
    """Name of the entity"""
    unique_id: str | None = None
    """A unique identifier for this entity. It must be unique within a platform (like light.hue).
    It should not be configurable or changeable by the user"""
    component: str | None = None
    """One of the supported MQTT integrations, eg. binary_sensor.
    See https://www.home-assistant.io/integrations/mqtt/#configuration-via-mqtt-discovery"""
    device_class: str | None = None
    """Extra classification of what the device is. Each domain specifies their own.
    Device classes can come with extra requirements for unit of measurement and supported features.
    Setting device class automatically sets the entity icon."""
    device: MqttDiscoveryDevice | None = None
    unit_of_measurement: str | None = None
    """The unit of measurement that the entity's state is expressed in. In most cases, for example for the number
    and sensor domains, this is implemented by the domain base entity and should not be implemented by integrations."""
    icon: str | None = None
    """Icon to use in the frontend. Using this property is not recommended.
    See https://developers.home-assistant.io/docs/core/entity/#icons"""
    value_template: str | None = None
    """Defines a template to extract device’s availability from the topic. To determine the devices’s availability
    result of this template will be compared to payload_available and payload_not_available."""
    state_topic: str | None = None
    """The MQTT topic subscribed to receive sensor values. If device_class, state_class, unit_of_measurement or
    suggested_display_precision is set, and a numeric value is expected, an empty value '' will be ignored and will
    not update the state, a 'null' value will set the sensor to an unknown state. The device_class can be null."""
    base_topic: str | None = None
    """A base topic '~' may be defined in the payload to conserve memory when the same topic base is used multiple
    times. In the value of configuration variables ending with _topic, ~ will be replaced with the base topic,
    if the ~ occurs at the beginning or end of the value."""
    availability_topic: str | None = None
    """The MQTT topic subscribed to receive availability (online/offline) updates."""
    payload_available: str | None = None
    """The payload that represents the available state."""
    payload_not_available: str | None = None
    """The payload that represents the unavailable state."""
    json_attributes_topic: str | None = None
    """The MQTT topic subscribed to receive a JSON dictionary payload and then set as sensor attributes.
    Implies force_update of the current sensor state when a message is received on this topic."""
    json_attributes_template: str | None = None
    """Defines a template to extract the JSON dictionary from messages received on the json_attributes_topic"""
    payload_on: str | None = None
    """The string that represents the on state. It will be compared to the message in the state_topic
    (see value_template for details)"""
    payload_off: str | None = None
    """The string that represents the off state. It will be compared to the message in the state_topic
    (see value_template for details)"""


class SensorNotAvailableException(Exception):
    """Exception class indicating a sensor is not available."""
