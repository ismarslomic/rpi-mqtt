#!/usr/bin/env python3
"""Tests to verify the RPI Mqtt topic configuration"""

from mqtt.types import RpiMqttTopics
from settings.types import MqttSettings, Settings
from tests.utils.settings_utils import read_test_settings

# Sample settings file
user_settings: Settings = read_test_settings()
mqtt_settings: MqttSettings = user_settings.mqtt


def test_mqtt_topics_config():
    """Test Mqtt topics based on user settings"""

    # Create instance
    topics: RpiMqttTopics = RpiMqttTopics(mqtt_settings=mqtt_settings, sensor_name="my_sensor")

    # Assert topic names for sensor states
    assert topics.sensor_states_base_topic == "foo/bar/sensor/my_sensor"
    assert topics.sensor_states_topic == "foo/bar/sensor/my_sensor/monitor"
    assert topics.sensor_states_topic_abbr == "~/monitor"

    # Assert topic names for command states
    assert topics.command_base_topic == "foo/bar/command/my_sensor"
    assert topics.command_topic_names == []

    # Assert topic names for LWT
    assert topics.sensor_states_lwt_topic == "foo/bar/sensor/my_sensor/status"
    assert topics.sensor_states_lwt_topic_abbr == "~/status"

    assert topics.command_lwt_topic == "foo/bar/command/my_sensor/status"

    assert topics.lwt_topic_names == ["foo/bar/sensor/my_sensor/status", "foo/bar/command/my_sensor/status"]


def test_mqtt_discovery_topic():
    """Test Mqtt discovery topic name based on user settings"""

    # Create instance
    topics: RpiMqttTopics = RpiMqttTopics(mqtt_settings=mqtt_settings, sensor_name="my_sensor")
    discovery_topic = topics.discovery_topic(component="binary_sensor", unique_id="update_available")

    assert discovery_topic == "homeassistant/binary_sensor/my_sensor/update_available/config"
