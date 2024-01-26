#!/usr/bin/env python3
"""Service for reading the Rpi bootloader version"""

import subprocess
from datetime import datetime, timezone

from rpi.bootloader.types import BootloaderVersion


def read_rpi_bootloader_version() -> BootloaderVersion:
    """Read current Rpi bootloader version and check for updates"""

    # doc: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#updating-the-eeprom-configuration
    args = ["rpi-eeprom-update"]
    result = subprocess.run(args, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        raise RuntimeError("Failed to read Rpi bootloader version", result.stderr)

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
            current_version = __timestamp_to_iso_format(item_split[1].strip())
        elif latest_version == "" and item_stripped.startswith("LATEST:"):
            item_split = item_stripped.split("LATEST: ")
            latest_version = __timestamp_to_iso_format(item_split[1].strip())

    return BootloaderVersion(status=update_status, current=current_version, latest=latest_version)


def __timestamp_to_iso_format(datetime_and_ts: str) -> str:
    """Format datetime and timestamp (seconds since the epoch) as ISO 8601 formatted string, including timezone
    offset"""

    timestamp: int = int(datetime_and_ts[datetime_and_ts.find("(") + 1 : datetime_and_ts.find(")")])
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
