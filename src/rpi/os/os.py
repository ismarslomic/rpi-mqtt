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


def read_os_release() -> str:
    """Read OS release"""

    release_file_name = "/etc/os-release"
    with open(release_file_name, "r") as f:
        release = f.readline().replace("PRETTY_NAME=", "").replace("\n", "").replace('"', "").strip()

    return release
