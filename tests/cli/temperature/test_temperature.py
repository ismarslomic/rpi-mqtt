#!/usr/bin/env python3
"""Tests to verify the temperature readings of Rpi hardware components"""

from unittest.mock import MagicMock, patch

import psutil

from cli.temperature.temperature import read_temperature
from cli.temperature.types import HwTemperature


# patching platform since sensors_temperatures is not available for all platforms
@patch("sys.platform", "linux")
# patching vcgencmd command run by the subprocess.run
@patch("cli.temperature.temperature.subprocess.run")
def test_read_temperature(mock_run):
    # Mock psutil
    psutil_mock = {
        "cpu_thermal": [{"label": "", "current": 46.3, "high": 110.0, "critical": 110.0}],
        "rp1_adc": [
            {
                "label": "",
                "current": 54.31,
                "high": None,
                "critical": None,
            }
        ],
    }
    psutil.sensors_temperatures = MagicMock(return_value=psutil_mock)

    # Mock subprocess.run running vcgencmd to read GPU temperature
    mock_proc = MagicMock(returncode=0, stdout="temp=51.0'C")
    mock_run.return_value = mock_proc

    # Call function
    temps: list[HwTemperature] = read_temperature()

    # Assert 3 temperature readings
    assert 3 == len(temps)
