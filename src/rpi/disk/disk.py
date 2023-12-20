#!/usr/bin/env python3
"""Service for reading the Rpi disk usage"""

from collections import namedtuple

import psutil

from rpi.disk.types import DiskUse


def read_disk_use() -> DiskUse:
    """Read statistics about disk usage for path '/'"""

    # doc: https://psutil.readthedocs.io/en/latest/
    path = "/"
    disk_usage: namedtuple = psutil.disk_usage(path)

    return DiskUse(
        path=path,
        total=__bytes_to_gibibytes(disk_usage.total),
        used=__bytes_to_gibibytes(disk_usage.used),
        used_percent=__round_percent(disk_usage.percent),
        free=__bytes_to_gibibytes(disk_usage.free),
    )


def __round_percent(percent: float) -> float:
    """Round percent value to 1 decimal"""

    return round(percent, 1)


def __bytes_to_gibibytes(value_bytes: int) -> float:
    """Convert bytes (B) to gibibytes (GiB) with 2 decimals"""

    value_gibibytes: float = value_bytes / 1024.0 / 1024.0 / 1024.0

    return round(value_gibibytes, 2)
