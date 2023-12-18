#!/usr/bin/env python3
"""Types in module Fan"""

from dataclasses import dataclass


@dataclass
class FanSpeed:
    """Class representing fan speed reading"""

    name: str
    """Name of the fan, representing a certain hardware sensor fan. Example: 'pwmfan'"""

    speed: int
    """Current speed, measured in RPM (revolutions per minute). Example: '2998'"""
