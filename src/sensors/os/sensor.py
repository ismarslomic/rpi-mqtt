#!/usr/bin/env python3
"""Service for reading the Rpi OS sensor"""

import subprocess

import psutil

from sensors.types import RpiSensor, SensorNotAvailableException
from sensors.utils import epoch_to_iso_datetime

# Apt is not available on Mac
APT_AVAILABLE = True
try:
    # noinspection PyUnresolvedReferences
    import apt
except ImportError:
    APT_AVAILABLE = False


class OsKernelSensor(RpiSensor):
    """Sensor for OS kernel"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "os_kernel"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_rpi_os_kernel()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_rpi_os_kernel(self) -> str:
        """Read OS kernel version"""

        # doc: https://www.raspberrypi.com/documentation/computers/linux_kernel.html#kernel
        args = ["uname", "-rvm"]

        try:
            result = subprocess.run(args, capture_output=True, text=True, check=False)
        except FileNotFoundError as err:
            self.logger.warning("Command 'uname' not available for this Rpi")
            raise SensorNotAvailableException("os kernel info not available for this Rpi") from err

        if result.returncode != 0:
            self.logger.warning("Process 'uname' returned code %s: %s", str(result.returncode), str(result.stderr))
            raise SensorNotAvailableException("Failed to read OS kernel version", result.stderr)

        os_kernel = result.stdout.replace("\n", "")

        return os_kernel


class OsReleaseSensor(RpiSensor):
    """Sensor for OS release"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "os_release"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_os_release()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_os_release(self) -> str:
        """Read OS release"""

        release_file_name = "/etc/os-release"

        try:
            with open(release_file_name, "r", encoding="utf-8") as f:
                release = f.readline().replace("PRETTY_NAME=", "").replace("\n", "").replace('"', "").strip()

            return release
        except Exception as err:
            self.logger.warning("Ip address file not available for this Rpi")
            raise SensorNotAvailableException("OS release file not available for this Rpi", err) from err


class AvailableUpdatesSensor(RpiSensor):
    """Sensor for available updates"""

    _state: int | None = None

    @property
    def name(self) -> str:
        return "available_updates"

    @property
    def state(self) -> int | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_number_of_available_updates()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_number_of_available_updates(self) -> int:
        """Read number of available package updates (using apt),
        returns SensorNotAvailableException if apt not available"""

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
        self.logger.warning("apt not available for this Rpi")
        raise SensorNotAvailableException("apt not available for this Rpi")


class BootTimeSensor(RpiSensor):
    """Sensor for boot time of Rpi"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "boot_time"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_rpi_boot_time()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_rpi_boot_time(self) -> str:
        """Return the Rpi boot time. Example: '2024-01-22T12:51:19+00:00'"""

        if not hasattr(psutil, "boot_time"):
            self.logger.warning("psutil boot_time() not available for this Rpi")
            raise SensorNotAvailableException("psutil boot_time() not available for this Rpi")

        boot_time_seconds: float = psutil.boot_time()
        boot_time_iso_datetime: str = epoch_to_iso_datetime(timestamp=boot_time_seconds)

        return boot_time_iso_datetime
