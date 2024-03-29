#!/usr/bin/env python3
"""Tests to verify reading settings file"""
from pathlib import Path

from settings.settings import read_settings
from settings.types import MqttSettings, ScriptSettings, SensorsMonitoringSettings, Settings


def test_default_settings():
    # Call function
    settings: Settings = read_settings()
    mqtt_settings: MqttSettings = settings.mqtt
    script_settings: ScriptSettings = settings.script
    sensors_settings: SensorsMonitoringSettings = settings.sensors

    # Assert Mqtt Settings
    assert "127.0.0.1" == mqtt_settings.hostname
    assert 1883 == mqtt_settings.port
    assert "rpi-mqtt" == mqtt_settings.client_id
    assert None is mqtt_settings.authentication
    assert None is mqtt_settings.tls

    # Assert Script Settings
    assert 60 == script_settings.update_interval

    # Assert Sensors Monitoring Settings
    for field_name in sensors_settings.__dict__:
        assert True is sensors_settings.__dict__[field_name]


def test_settings_from_file():
    # Sample file
    current_folder: Path = Path(__file__).resolve().parent
    sample_file_name: str = "sample_settings.yml"
    sample_file_path: str = current_folder.joinpath(sample_file_name).__str__()

    # Call function
    settings: Settings = read_settings(sample_file_path)
    mqtt_settings: MqttSettings = settings.mqtt
    script_settings: ScriptSettings = settings.script
    sensors_settings: SensorsMonitoringSettings = settings.sensors

    # Assert Mqtt Settings
    assert "192.168.0.1" == mqtt_settings.hostname
    assert 1337 == mqtt_settings.port
    assert "foo-bar-client-id" == mqtt_settings.client_id
    assert "foo_username" == mqtt_settings.authentication.username
    assert "bar_password" == mqtt_settings.authentication.password
    assert "/my/path/to/ca_certs" == mqtt_settings.tls.ca_certs
    assert "/my/path/to/certfile" == mqtt_settings.tls.certfile
    assert "/my/path/to/keyfile" == mqtt_settings.tls.keyfile

    # Assert Script Settings
    assert 120 == script_settings.update_interval

    # Assert Sensors Monitoring Settings
    assert False is sensors_settings.boot_loader
    assert False is sensors_settings.cpu
    assert False is sensors_settings.disk
    assert True is sensors_settings.fan
    assert False is sensors_settings.memory
    assert True is sensors_settings.network
    assert True is sensors_settings.os
    assert True is sensors_settings.temperature
    assert True is sensors_settings.throttle
