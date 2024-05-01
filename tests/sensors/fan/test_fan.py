#!/usr/bin/env python3
"""Tests to verify the fans speed of Rpi hardware components"""
import json
from collections import namedtuple
from typing import Any
from unittest.mock import MagicMock

import psutil
import pytest

from sensors.fan.sensor import FanSpeedSensor
from sensors.fan.types import FanSpeed
from sensors.types import SensorNotAvailableException


def test_read_fans_speed():
    # Mock psutil
    fans_tuple = namedtuple("sfan", ["label", "current"])
    psutil_mock: dict[str, list[fans_tuple]] = {"pwmfan": [fans_tuple(label="", current=2998)]}
    psutil.sensors_fans = MagicMock(return_value=psutil_mock)

    # Call function
    fan_speed_sensor = FanSpeedSensor(enabled=True)
    fan_speed_sensor.refresh_state()
    fans_speed: dict[str, FanSpeed] = fan_speed_sensor.state

    # Assert 1 fan speed reading
    assert 1 == len(fans_speed)

    assert "pwmfan" in fans_speed
    assert 2998 == fans_speed["pwmfan"].curr_speed_rpm
    assert 8000 == fans_speed["pwmfan"].max_speed_rpm
    assert 37.48 == fans_speed["pwmfan"].curr_speed_pct


def test_read_fans_speed_as_dict():
    # Mock psutil
    fans_tuple = namedtuple("sfan", ["label", "current"])
    psutil_mock: dict[str, list[fans_tuple]] = {"pwmfan": [fans_tuple(label="", current=2998)]}
    psutil.sensors_fans = MagicMock(return_value=psutil_mock)

    # Call function
    fan_speed_sensor = FanSpeedSensor(enabled=True)
    fan_speed_sensor.refresh_state()
    fans_speed: dict[str, dict[str, Any]] = fan_speed_sensor.state_as_dict

    # Assert 1 fan speed reading
    assert 1 == len(fans_speed)

    assert "pwmfan" in fans_speed
    pwmfan = fans_speed["pwmfan"]
    assert 2998 == pwmfan["curr_speed_rpm"]
    assert 8000 == pwmfan["max_speed_rpm"]
    assert 37.48 == pwmfan["curr_speed_pct"]

    # Assert converting to JSON
    json.dumps(fans_speed)


def test_read_fans_when_no_fans():
    # Mock psutil
    psutil.sensors_fans = MagicMock(return_value=None)

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        fan_speed_sensor = FanSpeedSensor(enabled=True)
        fan_speed_sensor.refresh_state()
        FanSpeedSensor(enabled=True).refresh_state()

    # Assert error message
    assert "none fans detected for this Rpi" in str(exec_info)


def test_read_fans_fan_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    if hasattr(psutil, "sensors_fans"):
        del psutil.sensors_fans

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        fan_speed_sensor = FanSpeedSensor(enabled=True)
        fan_speed_sensor.refresh_state()
        FanSpeedSensor(enabled=True).refresh_state()

    # Assert error message
    assert "sensors_fans() not available for this Rpi" in str(exec_info)
