#!/usr/bin/env python3
"""Tests to verify the fans speed of Rpi hardware components"""

from collections import namedtuple
from unittest.mock import MagicMock

import psutil

from rpi.fan.fan import read_fans_speed
from rpi.fan.types import FanSpeed


def test_read_fans_speed():
    # Mock psutil
    fans_tuple = namedtuple("sfan", ["label", "current"])
    psutil_mock: dict[str, list[fans_tuple]] = {"pwmfan": [fans_tuple(label="", current=2998)]}
    psutil.sensors_fans = MagicMock(return_value=psutil_mock)

    # Call function
    fans_speed: dict[str, FanSpeed] = read_fans_speed()

    # Assert 1 fan speed reading
    assert 1 == len(fans_speed)

    assert "pwmfan" in fans_speed
    assert 2998 == fans_speed["pwmfan"].curr_speed_rpm
    assert 8000 == fans_speed["pwmfan"].max_speed_rpm
    assert 37.48 == fans_speed["pwmfan"].curr_speed_pct


def test_read_fans_when_no_fans():
    # Mock psutil
    psutil_mock: dict[str, list] = {}
    psutil.sensors_fans = MagicMock(return_value=psutil_mock)

    # Call function
    fans_speed: dict[str, FanSpeed] = read_fans_speed()

    # Assert 0 fan speed reading
    assert 0 == len(fans_speed)
