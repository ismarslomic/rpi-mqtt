#!/usr/bin/env python3
"""Service for reading the Rpi OS sensor"""

import subprocess

import psutil

from rpi.types import RpiSensor, SensorNotAvailableException
from rpi.utils import epoch_to_iso_datetime

# Apt is not available on Mac
APT_AVAILABLE = True
try:
    # noinspection PyUnresolvedReferences
    import apt
except ImportError:
    APT_AVAILABLE = False


class OsKernelSensor(RpiSensor):
    """Sensor for OS kernel"""

    name: str = "Os kernel"

    def read(self) -> str:
        return read_rpi_os_kernel()


class OsReleaseSensor(RpiSensor):
    """Sensor for OS release"""

    name: str = "Os release"

    def read(self) -> str:
        return read_os_release()


class AvailableUpdatesSensor(RpiSensor):
    """Sensor for available updates"""

    name: str = "Available updates"

    def read(self) -> int:
        return read_number_of_available_updates()


class BootTimeSensor(RpiSensor):
    """Sensor for boot time of Rpi"""

    name: str = "Boot time"

    def read(self) -> str:
        return read_rpi_boot_time()


def read_rpi_os_kernel() -> str:
    """Read OS kernel version"""

    # doc: https://www.raspberrypi.com/documentation/computers/linux_kernel.html#kernel
    args = ["uname", "-rvm"]

    try:
        result = subprocess.run(args, capture_output=True, text=True, check=False)
    except FileNotFoundError as err:
        raise SensorNotAvailableException("os kernel info not available for this Rpi") from err

    if result.returncode != 0:
        raise SensorNotAvailableException("Failed to read OS kernel version", result.stderr)

    return result.stdout.replace("\n", "")


def read_os_release() -> str:
    """Read OS release"""

    release_file_name = "/etc/os-release"

    try:
        with open(release_file_name, "r", encoding="utf-8") as f:
            release = f.readline().replace("PRETTY_NAME=", "").replace("\n", "").replace('"', "").strip()

        return release
    except Exception as err:
        raise SensorNotAvailableException("os release file not available for this Rpi", err) from err


def read_number_of_available_updates() -> int:
    """Read number of available package updates (using apt), returns SensorNotAvailableException if apt not available"""

    if APT_AVAILABLE:
        cache = apt.Cache()
        cache.open(None)
        # apt update will be run automatically every day by the OS, so at some point of time the upgrade will report
        # available updates. We could run cache.update(), but this command requires sudo
        cache.upgrade()
        # Get marked changes
        changes = cache.get_changes()

        # Return number of changes
        return len(changes)

    # apt not available
    raise SensorNotAvailableException("apt not available for this Rpi")


def read_rpi_boot_time() -> str:
    """Return the Rpi boot time. Example: '2024-01-22T12:51:19+00:00'"""

    if not hasattr(psutil, "boot_time"):
        raise SensorNotAvailableException("boot_time() not available for this Rpi")

    boot_time_seconds: float = psutil.boot_time()

    return epoch_to_iso_datetime(timestamp=boot_time_seconds)
