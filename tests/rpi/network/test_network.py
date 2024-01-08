#!/usr/bin/env python3
"""Tests to verify the network readings of Rpi"""

from unittest.mock import MagicMock, patch

from rpi.network.network import read_wifi_connection
from rpi.network.types import WiFiConnectionInfo


# patching 'iw' command run by the subprocess.run
@patch("rpi.network.network.subprocess.run")
def test_read_wifi_connection_when_connected(mock_run):
    # Mock subprocess.run running iw to read Wi-Fi connection
    iw_mock = (
        "Connected to 04:42:1a:cf:15:c8 (on wlan0)\n"
        "SSID: MyNetwork 5G-2\n"
        "freq: 5520\n"
        "RX: 12225826 bytes (52643 packets)\n"
        "TX: 1402618 bytes (13162 packets)\n"
        "signal: -43 dBm\n"
        "rx bitrate: 433.3 MBit/s\n"
        "tx bitrate: 433.3 MBit/s\n"
        "\n"
        "bss flags:      \n"
        "dtim period:    1\n"
        "beacon int:     100\n"
    )
    mock_proc = MagicMock(returncode=0, stdout=iw_mock)
    mock_run.return_value = mock_proc

    # Call function
    wifi_info: WiFiConnectionInfo = read_wifi_connection()

    # Assert Wi-Fi information returned
    assert "MyNetwork 5G-2" == wifi_info.ssid
    assert -43 == wifi_info.signal_strength_dbm


# patching 'iw' command run by the subprocess.run
@patch("rpi.network.network.subprocess.run")
def test_read_wifi_connection_when_disconnected(mock_run):
    # Mock subprocess.run running vcgencmd to read GPU temperature
    mock_proc = MagicMock(returncode=0, stdout="Not connected.")
    mock_run.return_value = mock_proc

    # Call function
    wifi_info: WiFiConnectionInfo = read_wifi_connection()

    # Assert Wi-Fi information returned
    assert "" == wifi_info.ssid
    assert 0 == wifi_info.signal_strength_dbm
