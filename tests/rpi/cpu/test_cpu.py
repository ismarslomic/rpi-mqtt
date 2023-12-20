#!/usr/bin/env python3
"""Tests to verify the RPI CPU usage readings"""

from unittest.mock import MagicMock

import psutil

from rpi.cpu.cpu import read_cpu_use_percent


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
    psutil.getloadavg = MagicMock(return_value=[])

    # Call function
    cpu_use_percent: float = read_cpu_use_percent()

    # Assert
    assert 0.2 == cpu_use_percent
