#!/usr/bin/env python3
"""Types in module Throttle"""

from dataclasses import dataclass


@dataclass
class SystemThrottleStatus:
    """Class representing system throttle status"""

    status: str
    """Throttling status simplified as binary string, 'throttled' or 'not throttled'."""

    status_hex: str
    """Throttling status represented as hexadecimal value. Example: '0x50000'"""

    status_decimal: int
    """Throttling status represented as decimal value. Example: '327680'"""

    status_binary: str
    """Throttling status represented as binary value. Example: '0b1010000000000000000'"""

    reason: str
    """Human readable reason for system throttling, if throttling has occurred.
    Example: 'Under-voltage has occurred. Throttling has occurred'"""
