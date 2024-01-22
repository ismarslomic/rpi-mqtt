#!/usr/bin/env python3
"""Types in module Disk"""

from dataclasses import dataclass


@dataclass
class DiskUse:
    """Class representing disk usage reading"""

    path: str
    """The mount path. Example: '/'"""

    total_gib: float
    """Total disk space, in gibibytes (GiB). Example: '28.69'"""

    used_gib: float
    """Used disk space, in gibibytes (GiB). Example: '10.93'"""

    used_pct: float
    """Used disk space, in percent. Example: '40.2'"""

    free_gib: float
    """Free disk space, in gibibytes (GiB). Example: '16.28'"""
