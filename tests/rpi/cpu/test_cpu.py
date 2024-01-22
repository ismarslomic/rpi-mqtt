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
    assert 0.2 == cpu_use_percent


def test_read_load_average():
    # Mock psutil
    psutil.cpu_count = MagicMock(return_value=4)
    psutil.getloadavg = MagicMock(return_value=(0.28125, 0.0771484375, 0.02490234375))

    # Call function
    load_average: LoadAverage = read_load_average()

    # Assert
    assert 4 == load_average.cpu_cores
    assert 7.03 == load_average.load_1min_pct
    assert 1.93 == load_average.load_5min_pct
    assert 0.62 == load_average.load_15min_pct
