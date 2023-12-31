#!/usr/bin/env python3
"""Service for reading network data for Rpi"""

import re
import socket
import struct


def read_container_host_ip() -> str:
    """Read Rpi IP (the host IP when running in Docker)"""

    ip_pipe_file_name = "/app/host/host_ip_pipe"
    with open(ip_pipe_file_name, "r", encoding="utf-8") as f:
        data = f.readline().strip("\x00")
        ip = ""
        for line in data.split("\n"):
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
            mo = re.match("^.{2}(?P<id>.{2}).{2}(?P<addr>.{8})..{4} .{8}..{4} (?P<status>.{2}).*|", line)
            if mo and mo.group("id") != "sl":
                status = int(mo.group("status"), 16)  # convert from hex to decimal
                if status == 1:  # connection established
                    ip = _little_endian_hex_to_ip(mo.group("addr"))
                    break
        return ip


def read_container_host_hostname() -> str:
    """Read Rpi hostname (the host hostname when running in Docker)"""

    host_name_file_name = "/app/host/hostname"
    with open(host_name_file_name, "r", encoding="utf-8") as f:
        host_name = f.readline().strip()

    return host_name


def _little_endian_hex_to_ip(little_endian_hex) -> str:
    """Converts IP address in little-endian four-byte hexadecimal number to IP string"""

    # https://stackoverflow.com/a/2198052
    return socket.inet_ntoa(struct.pack("<L", little_endian_hex))
