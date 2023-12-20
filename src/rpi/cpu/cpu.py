#!/usr/bin/env python3
"""Service for reading the Rpi CPU usage"""

import psutil

from rpi.cpu.types import LoadAverage


def read_cpu_use_percent() -> float:
    """Return a float representing the current system-wide CPU utilization as a percentage"""

    # doc: https://psutil.readthedocs.io/en/latest/
    cpu_use_percent: float = psutil.cpu_percent(interval=0.1)

    return cpu_use_percent


def read_load_average() -> LoadAverage:
    """Return the average system load in percent related to number of cpu cores over the last 1, 5 and 15 minutes"""

    # doc: https://psutil.readthedocs.io/en/latest/
    cpu_cores: int = psutil.cpu_count()
    load_avg: tuple[float, float, float] = psutil.getloadavg()
    load_avg_percent: list[float] = [x / cpu_cores * 100 for x in load_avg]

    return LoadAverage(
        cpu_cores=cpu_cores,
        last_minute=__round_percent(load_avg_percent[0]),
        last_five_minutes=__round_percent(load_avg_percent[1]),
        last_fifteen_minutes=__round_percent(load_avg_percent[2]),
    )


def __round_percent(percent: float) -> float:
    """Round percent value to 2 decimal"""

    return round(percent, 2)
