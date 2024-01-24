#!/usr/bin/env python3
"""Tests to verify the system throttle readings of Rpi"""

from unittest.mock import MagicMock, patch

from rpi.throttle.throttle import read_throttle_status
from rpi.throttle.types import SystemThrottleStatus


# patching vcgencmd command run by the subprocess.run
@patch("rpi.throttle.throttle.subprocess.run")
def test_read_throttle_status_not_throttled(mock_run):
    # Mock subprocess.run running vcgencmd to read throttle status
    mock_proc = MagicMock(returncode=0, stdout="throttled=0x0")
    mock_run.return_value = mock_proc

    # Call function
    throttled_status: SystemThrottleStatus = read_throttle_status()

    # Assert
    assert "0x0" == throttled_status.status_hex
    assert 0 == throttled_status.status_decimal
    assert "0b0" == throttled_status.status_binary
    assert "Not throttled" == throttled_status.reason


@patch("rpi.throttle.throttle.subprocess.run")
def test_read_throttle_status_throttled_under_voltage(mock_run):
    # Mock subprocess.run running vcgencmd to read throttle status
    mock_proc = MagicMock(returncode=0, stdout="throttled=0x50000")
    mock_run.return_value = mock_proc

    # Call function
    throttled_status: SystemThrottleStatus = read_throttle_status()

    # Assert
    assert "0x50000" == throttled_status.status_hex
    assert 327680 == throttled_status.status_decimal
    assert "0b1010000000000000000" == throttled_status.status_binary
    assert "Under-voltage has occurred. Throttling has occurred" == throttled_status.reason
