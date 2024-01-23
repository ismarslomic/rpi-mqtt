#!/usr/bin/env python3
"""Types in module Network"""

from dataclasses import dataclass


@dataclass
class WiFiConnectionInfo:
    """Class representing Wi-Fi information"""

    ssid: str
    """The SSID of the Wi-Fi network. Example 'my-network'"""

    signal_strength_dbm: int
    """The signal strength of the Wi-Fi connection, in decibel-milliwatts (dBm). Example '-43'"""

    def __post_init__(self):
        self.signal_strength_quality = self.__signal_strength_quality()

    def __signal_strength_quality(self) -> str:
        """Return human-readable quality of the Wi-Fi signal strength, example: Excellent|Very good|Unusable"""

        if self.signal_strength_dbm >= -66:
            return "Excellent"
        if -67 >= self.signal_strength_dbm >= -69:
            return "Very good"
        if -70 >= self.signal_strength_dbm >= -79:
            return "Ok"
        if -80 >= self.signal_strength_dbm >= -89:
            return "Not good"

        return "Unusable"
