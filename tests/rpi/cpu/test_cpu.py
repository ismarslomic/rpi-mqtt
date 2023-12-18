#!/usr/bin/env python3
"""Tests to verify the RPI CPU usage readings"""

from unittest.mock import MagicMock, patch

import psutil

from rpi.cpu.cpu import read_cpu_percent


# patching platform since psutil.cpu_percent is not available for all platforms
@patch("sys.platform", "linux")
def test_read_temperature():
    # Mock psutil
    psutil.cpu_percent = MagicMock(return_value=0.2)

    # Call function
    cpu_percent: float = read_cpu_percent()

    # Assert
    assert 0.2 == cpu_percent
