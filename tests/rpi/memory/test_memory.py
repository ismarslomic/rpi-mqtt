#!/usr/bin/env python3
"""Tests to verify the RPI memory usage readings"""

from collections import namedtuple
from unittest.mock import MagicMock

import psutil

from rpi.memory.memory import read_memory_use
from rpi.memory.types import MemoryUse


def test_read_memory_use():
    # Mock psutil
    memory_tuple = namedtuple("svmem", ["total", "available", "percent"])
    psutil_mock = memory_tuple(total=8443887616, available=6906609664, percent=18.2)
    psutil.virtual_memory = MagicMock(return_value=psutil_mock)

    # Call function
    memory_use: MemoryUse = read_memory_use()

    # Assert
    assert 7.86 == memory_use.total_gib
    assert 6.43 == memory_use.available_gib
    assert 18.2 == memory_use.used_pct
