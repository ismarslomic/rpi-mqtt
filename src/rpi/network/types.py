#!/usr/bin/env python3
"""Types in module Network"""

from dataclasses import dataclass


@dataclass
class WiFiConnectionInfo:
    """Class representing Wi-Fi information"""

    ssid: str
    """The SSID of the Wi-Fi network. Example 'my-network'"""

    signal_strength_dbm: int
    """The signal strength of the Wi-Fi connection, in dBm. Example '-43'"""
