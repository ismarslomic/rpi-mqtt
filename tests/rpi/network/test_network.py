#!/usr/bin/env python3
"""Tests to verify the network readings of Rpi"""

from unittest.mock import MagicMock, patch

from rpi.network.network import _parse_ip_from_tcp_content, read_wifi_connection
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


def test_parse_ip_from_tcp_content():
    tcp_content: str = (
        "  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode\n"
        "   0: 0100007F:0277 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 40517 1 00000000409e6c91 100 0 0 10 0\n"
        "   1: 00000000:170C 00000000:0000 0A 00000000:00000000 00:00000000 00000000  1000        0 17867 1 000000001cdccca5 100 0 0 10 0\n"
        "   2: 00000000:075B 00000000:0000 0A 00000000:00000000 00:00000000 00000000  1883        0 19887 1 000000003d97a760 100 0 0 10 0\n"
        "   3: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 17591 1 000000007982095d 100 0 0 10 0\n"
        "   4: 8D01A8C0:0016 B801A8C0:ECA4 01 00000000:00000000 02:0001C222 00000000     0        0 46224 2 0000000066945424 20 4 19 10 -1\n"
        "   5: 8D01A8C0:0016 B801A8C0:EC6A 01 0000004C:00000000 01:00000014 00000000     0        0 46152 4 0000000080fea0a4 20 4 29 10 19\n"
        "   6: 8D01A8C0:0016 B801A8C0:ED34 01 00000000:00000000 02:000291B8 00000000     0        0 51427 2 00000000b4290d70 20 7 31 10 -1\n"
    )

    ip = _parse_ip_from_tcp_content(tcp_content)

    assert "192.168.1.141" == ip
