#!/usr/bin/env python3
"""Tests to verify the RPI CPU usage readings"""
import importlib
from unittest.mock import MagicMock

import psutil
import pytest

from sensors.cpu.sensor import CpuLoadAvgSensor, CpuUsePctSensor
from sensors.cpu.types import LoadAverage
from sensors.types import SensorNotAvailableException


def test_read_cpu_use_percent():
    # Mock psutil
    psutil.cpu_percent = MagicMock(return_value=0.2)

    # Call function
    cpu_use_percent: float = CpuUsePctSensor(enabled=True).read()

    # Assert
    assert 0.2 == cpu_use_percent


def test_read_cpu_use_percent_not_available_for_platform():
    # Mock psutil
    # Make sure that sensors_fans attribute is deleted if it exists (depending on the platform tests are run)
    if hasattr(psutil, "cpu_percent"):
        del psutil.cpu_percent

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        CpuUsePctSensor(enabled=True).read()

    # Assert error message
    assert "cpu_percent() not available for this Rpi" in str(exec_info)


def test_read_load_average():
    # Mock psutil
    psutil.cpu_count = MagicMock(return_value=4)
    psutil.getloadavg = MagicMock(return_value=(0.28125, 0.0771484375, 0.02490234375))

    # Call function
    load_average: LoadAverage = CpuLoadAvgSensor(enabled=True).read()

    # Assert
    assert 4 == load_average.cpu_cores
    assert 7.03 == load_average.load_1min_pct
    assert 1.93 == load_average.load_5min_pct
    assert 0.62 == load_average.load_15min_pct


def test_read_load_average_cpu_count_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    importlib.reload(psutil)
    if hasattr(psutil, "cpu_count"):
        del psutil.cpu_count

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        CpuLoadAvgSensor(enabled=True).read()

    # Assert error message
    assert "cpu_count() not available for this Rpi" in str(exec_info)


def test_read_load_average_getloadavg_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    importlib.reload(psutil)
    if hasattr(psutil, "getloadavg"):
        del psutil.getloadavg

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        CpuLoadAvgSensor(enabled=True).read()

    # Assert error message
    assert "getloadavg() not available for this Rpi" in str(exec_info)
