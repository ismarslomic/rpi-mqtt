#!/usr/bin/env python3
"""Service for reading the Rpi bootloader version"""

import subprocess

from rpi.bootloader.types import BootloaderVersion
from rpi.types import RpiSensor, SensorNotAvailableException
from rpi.utils import date_and_timestamp_to_iso_datetime


class BootloaderSensor(RpiSensor):
    """Sensor for bootloader version"""

    name: str = "Bootloader version"

    def read(self) -> BootloaderVersion:
        return read_rpi_bootloader_version()


def read_rpi_bootloader_version() -> BootloaderVersion:
    """Read current Rpi bootloader version and check for updates"""

    # doc: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#updating-the-eeprom-configuration
    args = ["rpi-eeprom-update"]

    try:
        result = subprocess.run(args, capture_output=True, text=True, check=False)
    except FileNotFoundError as err:
        raise SensorNotAvailableException("rpi-eeprom-update not available for this Rpi") from err

    if result.returncode != 0:
        raise SensorNotAvailableException("Failed to read Rpi bootloader version", result.stderr)

    result_as_list = result.stdout.split("\n")

    update_status = ""
    current_version = ""
    latest_version = ""

    for item in result_as_list:
        item_stripped = item.strip()
        if update_status == "" and item_stripped.startswith("BOOTLOADER:"):
            item_split = item_stripped.split("BOOTLOADER: ")
            update_status = item_split[1].strip()
        elif current_version == "" and item_stripped.startswith("CURRENT:"):
            item_split = item_stripped.split("CURRENT: ")
            current_version = date_and_timestamp_to_iso_datetime(item_split[1].strip())
        elif latest_version == "" and item_stripped.startswith("LATEST:"):
            item_split = item_stripped.split("LATEST: ")
            latest_version = date_and_timestamp_to_iso_datetime(item_split[1].strip())

    return BootloaderVersion(status=update_status, current=current_version, latest=latest_version)