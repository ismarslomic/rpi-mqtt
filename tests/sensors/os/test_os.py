#!/usr/bin/env python3
"""Tests to verify the Rpi OS sensor data"""
import importlib
from unittest.mock import MagicMock, mock_open, patch

import psutil
import pytest

from sensors.os.sensor import AvailableUpdatesSensor, BootTimeSensor, OsKernelSensor, OsReleaseSensor
from sensors.types import SensorNotAvailableException


# Tests for OS Kernel sensor
@patch("sensors.os.sensor.subprocess.run")
def test_read_rpi_os_kernel(mock_run):
    # Mock subprocess.run
    uname_mock = "6.1.0-rpi7-rpi-2712 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64\n"
    mock_proc = MagicMock(returncode=0, stdout=uname_mock)
    mock_run.return_value = mock_proc

    # Call function
    kernel_info: str = OsKernelSensor().read()

    # Assert 1 fan speed reading
    assert "6.1.0-rpi7-rpi-2712 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64" == kernel_info


@patch("sensors.os.sensor.subprocess.run", side_effect=FileNotFoundError("uname not found"))
def test_read_rpi_os_kernel_when_uname_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        OsKernelSensor().read()

    # Assert error message
    assert "os kernel info not available for this Rpi" in str(exec_info)


@patch("sensors.os.sensor.subprocess.run")
def test_read_rpi_os_kernel_when_code_one_is_returned(mock_run):
    # Mock subprocess.run
    uname_mock = "6.1.0-rpi7-rpi-2712 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64"
    mock_proc = MagicMock(returncode=1, stdout=uname_mock)
    mock_run.return_value = mock_proc

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        OsKernelSensor().read()

    # Assert error message
    assert "Failed to read OS kernel version" in str(exec_info)


# Tests for OS Release sensor
os_release_mock = """PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/\""""


@patch("builtins.open", new_callable=mock_open, read_data=os_release_mock)
def test_read_os_release(_):
    # Call function
    os_release: str = OsReleaseSensor().read()

    # Assert
    assert "Debian GNU/Linux 12 (bookworm)" == os_release


@patch("builtins.open", side_effect=FileNotFoundError("No such file or directory"))
def test_read_os_release_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        OsReleaseSensor().read()

    # Assert
    assert "os release file not available for this Rpi" in str(exec_info)


# Tests for Available updates sensor
@patch("sensors.os.sensor.APT_AVAILABLE", False)
def test_read_available_updates_when_not_available_for_platform():
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        AvailableUpdatesSensor().read()

    # Assert
    assert "apt not available for this Rpi" in str(exec_info)


# Tests for Boot time sensor
def test_read_rpi_boot_time():
    # Mock psutil
    psutil_mock: float = 1705927879.0
    psutil.boot_time = MagicMock(return_value=psutil_mock)

    # Call function
    boot_time: str = BootTimeSensor().read()

    # Assert boot time in ISO format
    assert "2024-01-22T12:51:19+00:00" == boot_time


def test_read_rpi_boot_time_when_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    importlib.reload(psutil)
    if hasattr(psutil, "boot_time"):
        del psutil.boot_time

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        BootTimeSensor().read()

    # Assert error message
    assert "boot_time() not available for this Rpi" in str(exec_info)
