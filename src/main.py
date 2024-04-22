#!/usr/bin/env python3
"""Main program that reads sensor data and publish to MQTT broker"""

from settings.settings import read_settings
from settings.types import Settings

SETTINGS_FILE_PATH = "/Users/ismarslomic/src/smarthytte/rpi-mqtt/src/settings.yml"

settings: Settings = read_settings(file_path=SETTINGS_FILE_PATH)
print(settings)
