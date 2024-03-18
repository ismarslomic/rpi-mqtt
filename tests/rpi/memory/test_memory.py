#!/usr/bin/env python3
"""Tests to verify the RPI memory usage readings"""

from collections import namedtuple
from unittest.mock import MagicMock

import psutil
import pytest

from rpi.memory.sensor import MemoryUseSensor
from rpi.memory.types import MemoryUse
from rpi.types import SensorNotAvailableException


def test_read_memory_use():
    # Mock psutil
    memory_tuple = namedtuple("svmem", ["total", "available", "percent"])
    psutil_mock = memory_tuple(total=8443887616, available=6906609664, percent=18.23)
    psutil.virtual_memory = MagicMock(return_value=psutil_mock)

    # Call function
    memory_use: MemoryUse = MemoryUseSensor().read()

    # Assert
    assert 7.86 == memory_use.total_gib
    assert 6.43 == memory_use.available_gib
    assert 18.23 == memory_use.used_pct


def test_read_fans_fan_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    if hasattr(psutil, "virtual_memory"):
        del psutil.virtual_memory

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        MemoryUseSensor().read()

    # Assert error message
    assert "virtual_memory() not available for this Rpi" in str(exec_info)
