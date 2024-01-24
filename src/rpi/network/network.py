#!/usr/bin/env python3
"""Service for reading network data for Rpi"""

import re
import socket
import struct
import subprocess

from rpi.network.types import WiFiConnectionInfo


def read_ip() -> str:
    """Read Rpi IP"""

    ip_pipe_file_name = "/proc/net/tcp"

    try:
        with open(ip_pipe_file_name, "r", encoding="utf-8") as f:
            tcp_content = f.read().strip("\x00")
            return _parse_ip_from_tcp_content(tcp_content)
    except Exception as err:
        raise RuntimeError("Failed to read ip", err) from err


def read_hostname() -> str:
    """Read Rpi hostname"""

    host_name_file_name = "/etc/hostname"

    try:
        with open(host_name_file_name, "r", encoding="utf-8") as f:
            return f.readline().strip()
    except Exception as err:
        raise RuntimeError("Failed to read host name", err) from err


def read_ethernet_mac_address() -> str:
    """Read the RPI mac address of the ethernet (eth0) network interface"""

    return __read_mac_address_for_interface("eth0")


def read_wifi_mac_address() -> str:
    """Read the RPI mac address of the Wi-Fi (wlan0) network interface"""

    return __read_mac_address_for_interface("wlan0")


def read_wifi_connection() -> WiFiConnectionInfo:
    """Read Wi-Fi connection, such as ssid and signal strength"""

    # doc: https://wireless.wiki.kernel.org/en/users/Documentation/iw
    args = ["iw", "wlan0", "link"]
    result = subprocess.run(args, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        raise RuntimeError("Failed to read Wi-Fi connection", result.stderr)

    result_as_list = result.stdout.split("\n")
    ssid: str = ""
    signal: int = 0
    freq: int = 0
    status: str = "on"
    mac_address: str = read_wifi_mac_address()

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
        status = "off"

    return WiFiConnectionInfo(status=status, ssid=ssid, signal_strength_dbm=signal, freq_mhz=freq, mac_addr=mac_address)


def __read_mac_address_for_interface(interface: str) -> str:
    """Read the RPI mac address for specific network interface"""

    mac_address_file_name = f"/sys/class/net/{interface}/address"

    try:
        with open(mac_address_file_name, "r", encoding="utf-8") as f:
            return f.readline().strip()
    except Exception as err:
        raise RuntimeError(f"Failed to read mac address for interface '{interface}'", err) from err


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
