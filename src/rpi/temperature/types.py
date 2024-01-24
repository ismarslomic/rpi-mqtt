#!/usr/bin/env python3
"""Types in module Temperature"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class HwTemperature:
    """Class representing temperature reading for one specific hardware component"""

    current_c: float
    """Current temperature for the hardware, in celsius. Example: '46.85'"""

    high_c: Optional[float]
    """Threshold for high temperature, in celsius. Example: '110.0'"""

    critical_c: Optional[float]
    """Threshold for critical temperature, in celsius. Example: '110.0'"""
