#!/usr/bin/env python3
"""Tests to verify the temperature readings of Rpi hardware components"""

from unittest.mock import MagicMock, patch

import psutil

from rpi.temperature.temperature import read_temperature
from rpi.temperature.types import HwTemperature


# patching vcgencmd command run by the subprocess.run
@patch("rpi.temperature.temperature.subprocess.run")
def test_read_temperature(mock_run):
    # Mock psutil
    psutil_mock = {
        "cpu_thermal": [{"label": "", "current": 46.365, "high": 110.0, "critical": 110.0}],
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

    cpu_temp: HwTemperature = temps[0]
    assert "cpu_thermal" == cpu_temp.name
    assert 46.4 == cpu_temp.current
    assert 110.0 == cpu_temp.high
    assert 110.0 == cpu_temp.critical

    adc_temp: HwTemperature = temps[1]
    assert "rp1_adc" == adc_temp.name
    assert 54.3 == adc_temp.current
    assert None is adc_temp.high
    assert None is adc_temp.critical

    gpu_temp: HwTemperature = temps[2]
    assert "gpu" == gpu_temp.name
    assert 51.0 == gpu_temp.current
    assert None is gpu_temp.high
    assert None is gpu_temp.critical
