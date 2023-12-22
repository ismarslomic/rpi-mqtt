#!/usr/bin/env python3
"""Types in module Bootloader"""

from dataclasses import dataclass


@dataclass
class BootloaderVersion:
    """Class representing bootloader version"""

    status: str
    """Update status of current version, 'up to date' and 'update available'. Example: 'up to date'"""

    current: str
    """The current bootloader version, represented as ISO 8601 date time. Example: '2023-12-06T18:29:25+00:00'"""

    latest: str
    """The latest bootloader version, represented as ISO 8601 date time. Example: '2023-12-06T18:29:25+00:00'"""
