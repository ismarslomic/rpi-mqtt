#!/usr/bin/env python3
"""Types in module Cpu"""

from dataclasses import dataclass


@dataclass
class LoadAverage:
    """Class representing system load average over the last 1, 5 and 15 minutes"""

    cpu_cores: int
    """The total number of (logical) CPU cores. Example: '4'"""

    last_minute: float
    """Average system load over the last 1 minute, in percent. Example: '7.21'"""

    last_five_minutes: float
    """Average system load over the last 5 minute, in percent. Example: '1.62'"""

    last_fifteen_minutes: float
    """Average system load over the last 15 minute, in percent. Example: '0.52'"""
