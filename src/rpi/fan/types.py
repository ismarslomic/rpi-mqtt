#!/usr/bin/env python3
"""Types in module Fan"""

from dataclasses import dataclass


@dataclass
class FanSpeed:
    """Class representing fan speed reading"""

    curr_speed_rpm: int
    """Current fan speed, measured in RPM (revolutions per minute). Example: '2998'"""

    max_speed_rpm: int = 8000
    """Maximum fan speed, measured in RPM (revolutions per minute).
    Hardcoded to 8000 RPM, assuming RPi active cooler is installed (not possible to read this value from RPi)"""

    def __post_init__(self):
        percent = (self.curr_speed_rpm / self.max_speed_rpm) * 100
        self.curr_speed_pct = round(percent, 2)
