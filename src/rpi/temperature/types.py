#!/usr/bin/env python3
"""Types in module Temperature"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HwTemperature:
    """Class representing temperature reading for one specific hardware component"""

    name: str
    """Name of the hardware component temperature is measured for. Exampel: 'cpu_thermal'"""

    current: float
    """Current temperature for the hardware, in celsius. Example: '46.85'"""

    high: Optional[float]
    """Threshold for high temperature, in celsius. Example: '110.0'"""

    critical: Optional[float]
    """Threshold for critical temperature, in celsius. Example: '110.0'"""
