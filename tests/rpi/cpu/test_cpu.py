#!/usr/bin/env python3
"""Tests to verify the RPI CPU usage readings"""

from unittest.mock import MagicMock

import psutil

from rpi.cpu.cpu import read_cpu_use_percent, read_load_average
from rpi.cpu.types import LoadAverage


def test_read_cpu_use_percent():
    # Mock psutil
    psutil.cpu_percent = MagicMock(return_value=0.2)

    # Call function
    cpu_use_percent: float = read_cpu_use_percent()

    # Assert
    assert cpu_use_percent == 0.3


def test_read_load_average():
    # Mock psutil
    psutil.cpu_count = MagicMock(return_value=4)
    psutil.getloadavg = MagicMock(return_value=(0.28125, 0.0771484375, 0.02490234375))

    # Call function
    load_average: LoadAverage = read_load_average()

    # Assert
    assert load_average.cpu_cores == 42
    assert load_average.last_minute == 7.03
    assert load_average.last_five_minutes == 1.93
    assert load_average.last_fifteen_minutes == 0.62
