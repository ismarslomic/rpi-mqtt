#!/usr/bin/env python3
"""Service for reading the Rpi OS info"""
import subprocess


def read_rpi_os_kernel() -> str:
    """Read OS kernel version"""

    # doc: https://www.raspberrypi.com/documentation/computers/linux_kernel.html#kernel
    args = ["uname", "-rvm"]
    result = subprocess.run(args, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        raise RuntimeError("Failed to read OS kernel version", result.stderr)

    return result.stdout
