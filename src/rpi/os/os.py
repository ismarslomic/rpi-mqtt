#!/usr/bin/env python3
"""Service for reading the Rpi OS info"""

import subprocess

# Apt is not available on Mac
APT_AVAILABLE = True
try:
    # noinspection PyUnresolvedReferences
    import apt
except ImportError:
    APT_AVAILABLE = False


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
    with open(release_file_name, "r", encoding="utf-8") as f:
        release = f.readline().replace("PRETTY_NAME=", "").replace("\n", "").replace('"', "").strip()

    return release


def read_number_of_available_updates() -> int:
    """Read number of available package updates (using apt), returns -1 if apt not available"""

    if APT_AVAILABLE:
        cache = apt.Cache()
        cache.open(None)
        # apt update will be run automatically every day by the OS, so at some point of time the upgrade will report
        # available updates. We could run cache.update(), but this command requires sudo
        cache.upgrade()
        # Get marked changes
        changes = cache.get_changes()

        # Return number of changes
        return len(changes)

    # apt not available
    return -1
