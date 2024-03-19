#!/usr/bin/env python3
"""Tests to verify the RPI disk usage readings"""

from collections import namedtuple
from unittest.mock import MagicMock

import psutil
import pytest

from sensors.disk.sensor import DiskUseSensor
from sensors.disk.types import DiskUse
from sensors.types import SensorNotAvailableException


def test_read_disk_use():
    # Mock psutil
    disk_tuple = namedtuple("sdiskusage", ["total", "used", "free", "percent"])
    psutil_mock = disk_tuple(total=30809550848, used=11738292224, free=17485807616, percent=40.23)
    psutil.disk_usage = MagicMock(return_value=psutil_mock)

    # Call function
    disk_use: DiskUse = DiskUseSensor(enabled=True).read()

    # Assert
    assert "/" == disk_use.path
    assert 28.69 == disk_use.total_gib
    assert 10.93 == disk_use.used_gib
    assert 40.23 == disk_use.used_pct
    assert 16.28 == disk_use.free_gib


def test_read_disk_not_available_for_platform():
    # Mock psutil
    # Make sure that attribute is deleted if it exists (depending on the platform tests are run)
    if hasattr(psutil, "disk_usage"):
        del psutil.disk_usage

    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        DiskUseSensor(enabled=True).read()

    # Assert error message
    assert "disk_usage() not available for this Rpi" in str(exec_info)
