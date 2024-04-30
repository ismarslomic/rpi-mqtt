#!/usr/bin/env python3
"""Service for reading network data for Rpi"""

import re
import socket
import struct
import subprocess

from sensors.network.types import WiFiConnectionInfo
from sensors.types import RpiSensor, SensorNotAvailableException


class IpAddressSensor(RpiSensor):
    """Sensor for IP address"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "ip_addr"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_ip()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_ip(self) -> str:
        """Read Rpi IP"""

        ip_pipe_file_name = "/proc/net/tcp"

        try:
            with open(ip_pipe_file_name, "r", encoding="utf-8") as f:
                tcp_content = f.read().strip("\x00")
                ip = _parse_ip_from_tcp_content(tcp_content)

                return ip
        except Exception as err:
            self.logger.warning("Ip address file not available for this Rpi")
            raise SensorNotAvailableException("Ip address file not available for this Rpi", err) from err


class HostnameSensor(RpiSensor):
    """Sensor for hostname"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "hostname"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_hostname()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_hostname(self) -> str:
        """Read Rpi hostname"""

        host_name_file_name = "/etc/hostname"

        try:
            with open(host_name_file_name, "r", encoding="utf-8") as f:
                hostname = f.readline().strip()

                return hostname
        except Exception as err:
            self.logger.warning("Hostname file not available for this Rpi")
            raise SensorNotAvailableException("hostname file not available for this Rpi", err) from err


class EthernetMacAddressSensor(RpiSensor):
    """Sensor for Ethernet Mac address"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "eth_mac_addr"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_ethernet_mac_address()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_ethernet_mac_address(self) -> str:
        """Read the RPI mac address of the ethernet (eth0) network interface"""

        try:
            mac_address = _read_mac_address_for_interface("eth0")

            return mac_address
        except SensorNotAvailableException as err:
            self.logger.warning("Ethernet mac address not available for this Rpi")
            raise err


class WifiMacAddressSensor(RpiSensor):
    """Sensor for Wi-Fi Mac address"""

    _state: str | None = None

    @property
    def name(self) -> str:
        return "wifi_mac_addr"

    @property
    def state(self) -> str | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_wifi_mac_address()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_wifi_mac_address(self) -> str:
        """Read the RPI mac address of the Wi-Fi (wlan0) network interface"""
        try:
            mac_address = _read_wifi_mac_address()

            return mac_address
        except SensorNotAvailableException as err:
            self.logger.warning("Wifi mac address not available for this Rpi")
            raise err


class WifiConnectionSensor(RpiSensor):
    """Sensor for Wi-Fi connection"""

    _state: WiFiConnectionInfo | None = None

    @property
    def name(self) -> str:
        return "wifi_connection"

    @property
    def state(self) -> WiFiConnectionInfo | None:
        return self._state

    def refresh_state(self) -> None:
        self.logger.debug("Refreshing sensor state")
        self._state = self._read_wifi_connection()
        self.logger.debug("Refreshing sensor state successfully")

    def _read_wifi_connection(self) -> WiFiConnectionInfo:
        """Read Wi-Fi connection, such as ssid and signal strength"""

        # doc: https://wireless.wiki.kernel.org/en/users/Documentation/iw
        args = ["iw", "wlan0", "link"]

        try:
            result = subprocess.run(args, capture_output=True, text=True, check=False)
        except FileNotFoundError as err:
            self.logger.warning("Command 'iw' not found for this Rpi")
            raise SensorNotAvailableException("Wi-Fi connection info not available for this Rpi") from err

        if result.returncode != 0:
            self.logger.warning("Process 'iw' returned code %s: %s", str(result.returncode), str(result.stderr))
            raise SensorNotAvailableException("Failed to read Wi-Fi connection", result.stderr)

        result_as_list = result.stdout.split("\n")
        ssid: str = ""
        signal: int = 0
        freq: int = 0
        status: str = "on"

        try:
            mac_address: str = _read_wifi_mac_address()
        except SensorNotAvailableException as err:
            self.logger.warning("Failed reading Wi-fi mac address")
            raise err

        for item in result_as_list:
            item_stripped = item.strip()
            if item_stripped.startswith("SSID:"):
                item_split = item_stripped.split("SSID: ")
                ssid = item_split[1].strip()
            elif item_stripped.startswith("signal:"):
                item_split = item_stripped.split("signal: ")
                signal = int(item_split[1].replace("dBm", "").strip())
            elif item_stripped.startswith("freq:"):
                item_split = item_stripped.split("freq: ")
                freq = int(item_split[1].strip())

        if result == "Not connected." or ssid == "":
            self.logger.debug("Wifi not connected, result='%s' ssid='%s'", str(result), str(ssid))
            status = "off"

        return WiFiConnectionInfo(
            status=status, ssid=ssid, signal_strength_dbm=signal, freq_mhz=freq, mac_addr=mac_address
        )


def _read_wifi_mac_address() -> str:
    """Read the RPI mac address of the Wi-Fi (wlan0) network interface"""

    return _read_mac_address_for_interface("wlan0")


def _read_mac_address_for_interface(interface: str) -> str:
    """Read the RPI mac address for specific network interface"""

    mac_address_file_name = f"/sys/class/net/{interface}/address"

    try:
        with open(mac_address_file_name, "r", encoding="utf-8") as f:
            return f.readline().strip()
    except Exception as err:
        raise SensorNotAvailableException(f"Failed to read mac address for interface '{interface}'", err) from err


def _parse_ip_from_tcp_content(content: str) -> str:
    ip: str = ""

    for line in content.split("\n"):
        #
        # Example:
        # 3: 8D01A8C0:0016 B801A8C0:E3A7 01 00000000:00000000 02:00096E3C 00000000
        # |   |                           |--> status: connection state
        # |   |
        # |   |
        # |   |
        # |   |---------------------------> addr: local IPv4 address
        # |----------------------------------> id
        #
        mo = re.match("^.{2}(?P<id>.{2}).{2}(?P<addr>.{8})..{4} .{8}..{4} (?P<status>.{2}).*|", line, re.MULTILINE)
        if mo and mo.group("id") != "sl":
            status = int(mo.group("status"), 16)  # convert from hex to decimal
            if status == 1:  # connection established
                ip = _little_endian_hex_to_ip(mo.group("addr"))
                break
    return ip


def _little_endian_hex_to_ip(little_endian_hex: str) -> str:
    """Converts IP address in little-endian four-byte hexadecimal number to IP string"""

    # https://stackoverflow.com/a/2198052
    return socket.inet_ntoa(struct.pack("<L", int(little_endian_hex, 16)))
