#!/usr/bin/env python3
"""Tests to verify the temperature readings of Rpi hardware components"""

import collections
from collections import defaultdict, namedtuple
from unittest.mock import MagicMock, patch

import psutil

from rpi.temperature.temperature import read_temperature
from rpi.temperature.types import HwTemperature


# patching vcgencmd command run by the subprocess.run
@patch("rpi.temperature.temperature.subprocess.run")
def test_read_temperature(mock_run):
    # Mock psutil
    ret: defaultdict[str, list] = collections.defaultdict(list)
    shwtemp = namedtuple("shwtemp", ["label", "current", "high", "critical"])
    ret["cpu_thermal"].append(shwtemp("", 46.365, 110.0, 110.0))
    ret["rp1_adc"].append(shwtemp("", 54.31, None, None))

    psutil.sensors_temperatures = MagicMock(return_value=ret)

    # Mock subprocess.run running vcgencmd to read GPU temperature
    mock_proc = MagicMock(returncode=0, stdout="temp=51.0'C")
    mock_run.return_value = mock_proc

    # Call function
    temps: dict[str, HwTemperature] = read_temperature()

    # Assert 3 temperature readings
    assert 3 == len(temps)

    assert "cpu_thermal" in temps
    cpu_temp: HwTemperature = temps["cpu_thermal"]
    assert 46.4 == cpu_temp.current_c
    assert 110.0 == cpu_temp.high_c
    assert 110.0 == cpu_temp.critical_c

    assert "rp1_adc" in temps
    adc_temp: HwTemperature = temps["rp1_adc"]
    assert 54.3 == adc_temp.current_c
    assert None is adc_temp.high_c
    assert None is adc_temp.critical_c

    assert "gpu" in temps
    gpu_temp: HwTemperature = temps["gpu"]
    assert 51.0 == gpu_temp.current_c
    assert None is gpu_temp.high_c
    assert None is gpu_temp.critical_c
