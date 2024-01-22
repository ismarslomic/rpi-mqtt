#!/usr/bin/env python3
"""Tests to verify the Rpi's OS information"""

from unittest.mock import MagicMock, mock_open, patch

import psutil
import pytest

from rpi.os.os import read_os_release, read_rpi_boot_time, read_rpi_os_kernel


@patch("rpi.os.os.subprocess.run")
def test_read_rpi_os_kernel(mock_run):
    # Mock subprocess.run
    uname_mock = "6.1.0-rpi7-rpi-2712 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64\n"
    mock_proc = MagicMock(returncode=0, stdout=uname_mock)
    mock_run.return_value = mock_proc

    # Call function
    kernel_info: str = read_rpi_os_kernel()

    # Assert 1 fan speed reading
    assert "6.1.0-rpi7-rpi-2712 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64" == kernel_info


@patch("rpi.os.os.subprocess.run")
def test_read_rpi_os_kernel_return_code_one(mock_run):
    # Mock subprocess.run
    uname_mock = "6.1.0-rpi7-rpi-2712 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64"
    mock_proc = MagicMock(returncode=1, stdout=uname_mock)
    mock_run.return_value = mock_proc

    # Call function
    with pytest.raises(RuntimeError) as exec_info:
        read_rpi_os_kernel()

    # Assert error message
    assert "Failed to read OS kernel version" in str(exec_info)


os_release_mock = """PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/\""""


@patch("builtins.open", new_callable=mock_open, read_data=os_release_mock)
def test_read_os_release(_):
    # Call function
    os_release: str = read_os_release()

    # Assert
    assert "Debian GNU/Linux 12 (bookworm)" == os_release


def test_read_rpi_boot_time():
    # Mock psutil
    psutil_mock: float = 1705927879.0
    psutil.boot_time = MagicMock(return_value=psutil_mock)

    # Call function
    boot_time: str = read_rpi_boot_time()

    # Assert boot time in ISO format
    assert "2024-01-22T12:51:19+00:00" == boot_time
