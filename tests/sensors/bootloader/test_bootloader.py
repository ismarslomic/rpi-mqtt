#!/usr/bin/env python3
"""Tests to verify the RPI bootloader version readings"""

from unittest.mock import MagicMock, patch

import pytest

from sensors.bootloader.sensor import BootloaderSensor
from sensors.bootloader.types import BootloaderVersion
from sensors.types import SensorNotAvailableException


@patch("sensors.bootloader.sensor.subprocess.run")
def test_read_bootloader_version_up_to_date(mock_run):
    """Test reading bootloader version when the current version is up-to-date"""

    # Mock subprocess.run running rpi-eeprom-update to read bootloader version
    bootloader_mock = (
        "BOOTLOADER: up to date\n   "
        "CURRENT: Wed Dec  6 18:29:25 UTC 2023 (1701887365)\n    "
        "LATEST: Wed Dec  6 18:29:25 UTC 2023 (1701887365)\n   "
        "RELEASE: default (/lib/firmware/raspberrypi/bootloader-2712/default)\n            "
        "Use raspi-config to change the release.\n"
    )
    mock_proc = MagicMock(returncode=0, stdout=bootloader_mock)
    mock_run.return_value = mock_proc

    # Call function
    bootloader_version: BootloaderVersion = BootloaderSensor().read()

    # Assert
    assert "up to date" == bootloader_version.status
    assert "2023-12-06T18:29:25+00:00" == bootloader_version.current
    assert "2023-12-06T18:29:25+00:00" == bootloader_version.latest


@patch("sensors.bootloader.sensor.subprocess.run")
def test_read_bootloader_version_update_available(mock_run):
    """Test reading bootloader version when there is an update available"""

    # Mock subprocess.run running rpi-eeprom-update to read bootloader version
    bootloader_mock = (
        "*** UPDATE AVAILABLE ***\n"
        "BOOTLOADER: update available\n   "
        "CURRENT: Mon Nov 20 19:40:17 UTC 2023 (1700509217)\n    "
        "LATEST: Wed Dec  6 18:29:25 UTC 2023 (1701887365)\n   "
        "RELEASE: default (/lib/firmware/raspberrypi/bootloader-2712/default)\n            "
        "Use raspi-config to change the release.\n"
    )
    mock_proc = MagicMock(returncode=0, stdout=bootloader_mock)
    mock_run.return_value = mock_proc

    # Call function
    bootloader_version: BootloaderVersion = BootloaderSensor().read()

    # Assert
    assert "update available" == bootloader_version.status
    assert "2023-11-20T19:40:17+00:00" == bootloader_version.current
    assert "2023-12-06T18:29:25+00:00" == bootloader_version.latest


@patch("sensors.bootloader.sensor.subprocess.run", side_effect=FileNotFoundError("rpi-eeprom-update not found"))
def test_read_bootloader_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        BootloaderSensor().read()

    # Assert error message
    assert "rpi-eeprom-update not available for this Rpi" in str(exec_info)
