#!/usr/bin/env python3
"""Tests to verify the fans speed of Rpi hardware components"""

from collections import namedtuple
from unittest.mock import MagicMock, patch

import psutil
import pytest

from sensors.fan.sensor import FanSpeedSensor, read_fans_speed
from sensors.fan.types import FanSpeed
from sensors.types import SensorNotAvailableException


def test_read_fans_speed():
    # Mock psutil
    fans_tuple = namedtuple("sfan", ["label", "current"])
    psutil_mock: dict[str, list[fans_tuple]] = {"pwmfan": [fans_tuple(label="", current=2998)]}
    psutil.sensors_fans = MagicMock(return_value=psutil_mock)

    # Call function
    fans_speed: dict[str, FanSpeed] = FanSpeedSensor().read()

    # Assert 1 fan speed reading
    assert 1 == len(fans_speed)

    assert "pwmfan" in fans_speed
    assert 2998 == fans_speed["pwmfan"].curr_speed_rpm
    assert 8000 == fans_speed["pwmfan"].max_speed_rpm
    assert 37.48 == fans_speed["pwmfan"].curr_speed_pct


def test_read_fans_when_no_fans():
    # Mock psutil
    psutil.sensors_fans = MagicMock(return_value=None)

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        FanSpeedSensor().read()

    # Assert error message
    assert "none fans detected for this Rpi" in str(exec_info)


def test_read_fans_fan_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    if hasattr(psutil, "sensors_fans"):
        del psutil.sensors_fans

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        FanSpeedSensor().read()

    # Assert error message
    assert "sensors_fans() not available for this Rpi" in str(exec_info)
