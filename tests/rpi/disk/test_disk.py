#!/usr/bin/env python3
"""Tests to verify the RPI disk usage readings"""

from collections import namedtuple
from unittest.mock import MagicMock

import psutil

from rpi.disk.disk import read_disk_use
from rpi.disk.types import DiskUse


def test_read_disk_use():
    # Mock psutil
    disk_tuple = namedtuple("sdiskusage", ["total", "used", "free", "percent"])
    psutil_mock = disk_tuple(total=30809550848, used=11738292224, free=17485807616, percent=40.2)
    psutil.disk_usage = MagicMock(return_value=psutil_mock)

    # Call function
    disk_use: DiskUse = read_disk_use()

    # Assert
    assert "/" == disk_use.path
    assert 28.69 == disk_use.total
    assert 10.93 == disk_use.used
    assert 40.2 == disk_use.used_percent
    assert 16.28 == disk_use.free
