#!/usr/bin/env python3
"""Common types in module Mqtt"""

from dataclasses import dataclass

from mqtt.constants import TOPIC_COMMANDS_LWT_POSTFIX, TOPIC_SENSOR_STATES_LWT_POSTFIX, TOPIC_SENSOR_STATES_POSTFIX
from settings.types import MqttSettings


@dataclass()
class RpiMqttTopics:
    """Type holding all mqtt topics used by this script"""

    _topic_prefix: str
    _discovery_topic_prefix: str
    _sensor_name: str

    sensor_states_base_topic: str
    sensor_states_topic: str
    sensor_states_topic_abbr: str
    sensor_states_lwt_topic: str
    sensor_states_lwt_topic_abbr: str

    command_base_topic: str
    command_topic_names: list[str]
    command_lwt_topic: str

    lwt_topic_names: list[str]
    """List of LWT topic names"""

    def __init__(self, mqtt_settings: MqttSettings, sensor_name: str):
        self._topic_prefix = mqtt_settings.base_topic.lower()
        self._discovery_topic_prefix = mqtt_settings.discovery_topic_prefix.lower()
        self._sensor_name = sensor_name

        # Base topics
        self.sensor_states_base_topic = f"{self._topic_prefix}/sensor/{self._sensor_name}"
        self.command_base_topic = f"{self._topic_prefix}/command/{self._sensor_name}"

        # Command topics
        self.command_topic_names = []

        # LWT topics for sensor states
        self.sensor_states_lwt_topic = f"{self.sensor_states_base_topic}/{TOPIC_SENSOR_STATES_LWT_POSTFIX}"
        self.sensor_states_lwt_topic_abbr = f"~/{TOPIC_SENSOR_STATES_LWT_POSTFIX}"

        # LWT topics for commands
        self.command_lwt_topic = f"{self.command_base_topic}/{TOPIC_COMMANDS_LWT_POSTFIX}"

        # Union of LWT topics
        self.lwt_topic_names = [self.sensor_states_lwt_topic, self.command_lwt_topic]

        # Sensor states topics
        self.sensor_states_topic = f"{self.sensor_states_base_topic}/{TOPIC_SENSOR_STATES_POSTFIX}"
        self.sensor_states_topic_abbr = f"~/{TOPIC_SENSOR_STATES_POSTFIX}"

    def discovery_topic(self, component: str, unique_id: str) -> str:
        """Returns name of the Mqtt discovery topic in format
        <discovery_prefix>/<component>/<node_id>]<unique_id>/config"""

        return f"{self._discovery_topic_prefix}/{component}/{self._sensor_name}/{unique_id}/config"
