#!/usr/bin/env python3
"""Tests to verify the network readings of Rpi"""
import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from sensors.network.sensor import (
    EthernetMacAddressSensor,
    HostnameSensor,
    IpAddressSensor,
    WifiConnectionSensor,
    WifiMacAddressSensor,
    _parse_ip_from_tcp_content,
)
from sensors.network.types import WiFiConnectionInfo
from sensors.types import SensorNotAvailableException


# patching 'iw' command run by the subprocess.run and reading mac address for Wi-Fi interface
@patch("sensors.network.sensor.subprocess.run")
@patch("builtins.open", new_callable=mock_open, read_data="a9:3a:dd:b1:cc:46")
def test_read_wifi_connection_when_connected(_, mock_run):
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
    wifi_connection_sensor = WifiConnectionSensor(enabled=True)
    wifi_connection_sensor.refresh_state()
    wifi_info: WiFiConnectionInfo = wifi_connection_sensor.state

    # Assert Wi-Fi information returned
    assert "on" == wifi_info.status
    assert "MyNetwork 5G-2" == wifi_info.ssid
    assert -43 == wifi_info.signal_strength_dbm
    assert 5520 == wifi_info.freq_mhz
    assert "a9:3a:dd:b1:cc:46" == wifi_info.mac_addr


# patching 'iw' command run by the subprocess.run and reading mac address for Wi-Fi interface
@patch("sensors.network.sensor.subprocess.run")
@patch("builtins.open", new_callable=mock_open, read_data="a9:3a:dd:b1:cc:46")
def test_read_wifi_connection_when_connected_as_dict(_, mock_run):
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
    wifi_connection_sensor = WifiConnectionSensor(enabled=True)
    wifi_connection_sensor.refresh_state()
    wifi_info: dict = wifi_connection_sensor.state_as_dict

    # Assert Wi-Fi information returned
    assert "on" == wifi_info["status"]
    assert "MyNetwork 5G-2" == wifi_info["ssid"]
    assert -43 == wifi_info["signal_strength_dbm"]
    assert 5520 == wifi_info["freq_mhz"]
    assert "a9:3a:dd:b1:cc:46" == wifi_info["mac_addr"]

    # Assert JSON serialization
    json.dumps(wifi_info)


# patching 'iw' command run by the subprocess.run
@patch("sensors.network.sensor.subprocess.run")
@patch("builtins.open", new_callable=mock_open, read_data="a9:3a:dd:b1:cc:46")
def test_read_wifi_connection_when_disconnected(_, mock_run):
    # Mock subprocess.run running vcgencmd to read GPU temperature
    mock_proc = MagicMock(returncode=0, stdout="Not connected.")
    mock_run.return_value = mock_proc

    # Call function
    wifi_connection_sensor = WifiConnectionSensor(enabled=True)
    wifi_connection_sensor.refresh_state()
    wifi_info: WiFiConnectionInfo = wifi_connection_sensor.state

    # Assert Wi-Fi information returned
    assert "off" == wifi_info.status
    assert "" == wifi_info.ssid
    assert 0 == wifi_info.signal_strength_dbm
    assert 0 == wifi_info.freq_mhz
    assert "a9:3a:dd:b1:cc:46" == wifi_info.mac_addr


@patch("builtins.open", new_callable=mock_open, read_data="a8:3a:dd:b1:cc:45")
def test_read_ethernet_mac_address_when_success(_):
    # Call function
    ethernet_mac_address_sensor = EthernetMacAddressSensor(enabled=True)
    ethernet_mac_address_sensor.refresh_state()
    actual_mac_address = ethernet_mac_address_sensor.state

    # Assert mac address returned
    assert "a8:3a:dd:b1:cc:45" == actual_mac_address


@patch("builtins.open", new_callable=mock_open, read_data="a9:3a:dd:b1:cc:46")
def test_read_wifi_mac_address_when_success(_):
    # Call function
    wifi_mac_address_sensor = EthernetMacAddressSensor(enabled=True)
    wifi_mac_address_sensor.refresh_state()
    actual_mac_address = wifi_mac_address_sensor.state

    # Assert mac address returned
    assert "a9:3a:dd:b1:cc:46" == actual_mac_address


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


@pytest.mark.parametrize(
    "strength, quality",
    [
        (-20, "Excellent"),
        (-30, "Excellent"),
        (-66, "Excellent"),
        (-67, "Very good"),
        (-69, "Very good"),
        (-70, "Ok"),
        (-79, "Ok"),
        (-80, "Not good"),
        (-89, "Not good"),
        (-90, "Unusable"),
        (-130, "Unusable"),
    ],
)
def test_signal_strength_quality_when_connected(strength: int, quality: str):
    wifi_info = WiFiConnectionInfo(
        status="on", ssid="MyWifi", signal_strength_dbm=strength, freq_mhz=5520, mac_addr="a9:3a:dd:b1:cc:46"
    )
    assert wifi_info.signal_strength_quality == quality


def test_signal_strength_quality_when_disconnected():
    wifi_info = WiFiConnectionInfo(
        status="off", ssid="", signal_strength_dbm=0, freq_mhz=0, mac_addr="a9:3a:dd:b1:cc:46"
    )
    assert wifi_info.signal_strength_quality == "N/A"


@patch("builtins.open", side_effect=FileNotFoundError("No such file or directory"))
def test_read_ip_address_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        IpAddressSensor(enabled=True).refresh_state()

    # Assert error message
    assert "Ip address file not available for this Rpi" in str(exec_info)


@patch("builtins.open", side_effect=FileNotFoundError("No such file or directory"))
def test_read_hostname_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        HostnameSensor(enabled=True).refresh_state()

    # Assert error message
    assert "hostname file not available for this Rpi" in str(exec_info)


@patch("builtins.open", side_effect=FileNotFoundError("No such file or directory"))
def test_read_ethernet_mac_address_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        EthernetMacAddressSensor(enabled=True).refresh_state()

    # Assert error message
    assert "Failed to read mac address" in str(exec_info)


@patch("builtins.open", side_effect=FileNotFoundError("No such file or directory"))
def test_read_wifi_mac_address_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        WifiMacAddressSensor(enabled=True).refresh_state()

    # Assert error message
    assert "Failed to read mac address" in str(exec_info)


@patch("sensors.network.sensor.subprocess.run", side_effect=FileNotFoundError("iw not found"))
def test_read_wifi_connection_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        WifiConnectionSensor(enabled=True).refresh_state()

    # Assert error message
    assert "Wi-Fi connection info not available for this Rpi" in str(exec_info)
