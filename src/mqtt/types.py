#!/usr/bin/env python3
"""Common types in module Mqtt"""
from dataclasses import dataclass

from settings.types import MqttSettings


@dataclass()
class RpiMqttTopics:
    """Type holding all mqtt topics used by this script"""

    base_topic: str
    command_base_topic: str
    command_topic_names: list[str]
    lwt_topic_names: list[str]
    sensor_states_topic: str

    def __init__(self, mqtt_settings: MqttSettings, sensor_name: str):
        self.base_topic = mqtt_settings.base_topic.lower()

        self.command_base_topic = f"{self.base_topic}/command/{sensor_name}"
        self.command_topic_names = []

        self.lwt_topic_names = [
            f"{self.base_topic}/sensor/{sensor_name}/status",
            f"{self.base_topic}/command/{sensor_name}/status",
        ]

        self.sensor_states_topic = f"{self.base_topic}/monitor"
