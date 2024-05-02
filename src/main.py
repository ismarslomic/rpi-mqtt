#!/usr/bin/env python3
"""Main program that reads sensor data and publish to MQTT broker"""
import json

from cli_utils import cli_create_arg_parser
from log_utils import set_global_log_config
from sensors.main import AllRpiSensors, create_sensors
from settings.settings import read_settings
from settings.types import Settings

if __name__ == "__main__":
    # Read user settings
    parser = cli_create_arg_parser()
    settings_file_path = parser.parse_args().settings_file
    user_settings: Settings = read_settings(file_path=settings_file_path)

    # Configure global log settings
    set_global_log_config(settings=user_settings)

    sensors = create_sensors(settings=user_settings)
    all_sensors = AllRpiSensors(sensors=sensors, script_settings=user_settings.script)
    all_sensors_as_dict = all_sensors.as_dict()

    print(f"Publishing to MQTT data:{json.dumps(all_sensors_as_dict)}")
    # print_sensor_availability(all_sensors)

    # Connect to MQTT and publish & subscribe
    # start_pub_sub(mqtt_settings=user_settings.mqtt, script_settings=user_settings.script)
