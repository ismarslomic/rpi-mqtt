#!/usr/bin/env python3
"""Tests to verify the temperature readings of Rpi hardware components"""

import collections
import importlib
import json
from collections import defaultdict, namedtuple
from typing import Any
from unittest.mock import MagicMock, patch

import psutil
import pytest

from sensors.temperature.sensor import TemperatureSensor
from sensors.temperature.types import HwTemperature
from sensors.types import SensorNotAvailableException

# noinspection DuplicatedCode


# patching vcgencmd command run by the subprocess.run
@patch("sensors.temperature.sensor.subprocess.run")
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
    temperature_sensor = TemperatureSensor(enabled=True)
    temperature_sensor.refresh_state()
    temps: dict[str, HwTemperature] = temperature_sensor.state

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


# patching vcgencmd command run by the subprocess.run
@patch("sensors.temperature.sensor.subprocess.run")
def test_read_temperature_as_dict(mock_run):
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
    temperature_sensor = TemperatureSensor(enabled=True)
    temperature_sensor.refresh_state()
    temps: dict[str, dict[str, Any]] = temperature_sensor.state_as_dict

    # Assert 3 temperature readings
    assert 3 == len(temps)

    assert "cpu_thermal" in temps
    cpu_temp: dict[str, float] = temps["cpu_thermal"]
    assert 46.4 == cpu_temp["current_c"]
    assert 110.0 == cpu_temp["high_c"]
    assert 110.0 == cpu_temp["critical_c"]

    assert "rp1_adc" in temps
    adc_temp: dict[str, float] = temps["rp1_adc"]
    assert 54.3 == adc_temp["current_c"]
    assert None is adc_temp["high_c"]
    assert None is adc_temp["critical_c"]

    assert "gpu" in temps
    gpu_temp: dict[str, float] = temps["gpu"]
    assert 51.0 == gpu_temp["current_c"]
    assert None is gpu_temp["high_c"]
    assert None is gpu_temp["critical_c"]

    # Assert converting to JSON
    json.dumps(temps)


def test_read_temperature_when_sensors_temperatures_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    importlib.reload(psutil)
    if hasattr(psutil, "sensors_temperatures"):
        del psutil.sensors_temperatures

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        temperature_sensor = TemperatureSensor(enabled=True)
        temperature_sensor.refresh_state()

    # Assert error message
    assert "sensors_temperatures() not available for this Rpi" in str(exec_info)


def test_read_temperature_when_none_temperatures_detected():
    # Mock psutil
    psutil.sensors_temperatures = MagicMock(return_value=None)

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        temperature_sensor = TemperatureSensor(enabled=True)
        temperature_sensor.refresh_state()

    # Assert error message
    assert "none temperatures detected for this Rpi" in str(exec_info)


# noinspection DuplicatedCode
@patch("sensors.temperature.sensor.subprocess.run", side_effect=FileNotFoundError("vcgencmd not found"))
def test_read_temperature_when_vcgencmd_not_available_for_platform(_):
    # Mock psutil
    ret: defaultdict[str, list] = collections.defaultdict(list)
    shwtemp = namedtuple("shwtemp", ["label", "current", "high", "critical"])
    ret["cpu_thermal"].append(shwtemp("", 46.365, 110.0, 110.0))
    ret["rp1_adc"].append(shwtemp("", 54.31, None, None))

    psutil.sensors_temperatures = MagicMock(return_value=ret)

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        temperature_sensor = TemperatureSensor(enabled=True)
        temperature_sensor.refresh_state()

    # Assert error message
    assert "vcgencmd not available for this Rpi" in str(exec_info)
