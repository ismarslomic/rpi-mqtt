#!/usr/bin/env python3
"""Types in module Disk"""

from dataclasses import dataclass


@dataclass
class DiskUse:
    """Class representing disk usage reading"""

    path: str
    """The mount path. Example: '/'"""

    total: float
    """Total disk space, in gibibytes (GiB). Example: '28.69'"""

    used: float
    """Used disk space, in gibibytes (GiB). Example: '10.93'"""

    used_percent: float
    """Used disk space, in percent. Example: '40.2'"""

    free: float
    """Free disk space, in gibibytes (GiB). Example: '16.28'"""
