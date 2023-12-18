#!/usr/bin/env python3
"""Service for reading the Rpi CPU usage"""

import psutil


def read_cpu_use_percent() -> float:
    """Return a float representing the current system-wide CPU utilization as a percentage"""

    # doc: https://psutil.readthedocs.io/en/latest/
    cpu_use_percent: float = psutil.cpu_percent(interval=0.1)

    return cpu_use_percent
