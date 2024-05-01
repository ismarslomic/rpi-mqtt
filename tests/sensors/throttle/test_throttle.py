#!/usr/bin/env python3
"""Tests to verify the system throttle readings of Rpi"""
import json
from unittest.mock import MagicMock, patch

import pytest

from sensors.throttle.sensor import ThrottledSensor
from sensors.throttle.types import SystemThrottleStatus
from sensors.types import SensorNotAvailableException


# patching vcgencmd command run by the subprocess.run
@patch("sensors.throttle.sensor.subprocess.run")
def test_read_throttle_status_not_throttled(mock_run):
    # Mock subprocess.run running vcgencmd to read throttle status
    mock_proc = MagicMock(returncode=0, stdout="throttled=0x0")
    mock_run.return_value = mock_proc

    # Call function
    throttled_sensor = ThrottledSensor(enabled=True)
    throttled_sensor.refresh_state()
    throttled_status: SystemThrottleStatus = throttled_sensor.state

    # Assert
    assert "0x0" == throttled_status.status_hex
    assert 0 == throttled_status.status_decimal
    assert "0b0" == throttled_status.status_binary
    assert "Not throttled" == throttled_status.reason


# patching vcgencmd command run by the subprocess.run
@patch("sensors.throttle.sensor.subprocess.run")
def test_read_throttle_status_not_throttled_as_dict(mock_run):
    # Mock subprocess.run running vcgencmd to read throttle status
    mock_proc = MagicMock(returncode=0, stdout="throttled=0x0")
    mock_run.return_value = mock_proc

    # Call function
    throttled_sensor = ThrottledSensor(enabled=True)
    throttled_sensor.refresh_state()
    throttled_status: dict = throttled_sensor.state_as_dict

    # Assert
    assert "0x0" == throttled_status["status_hex"]
    assert 0 == throttled_status["status_decimal"]
    assert "0b0" == throttled_status["status_binary"]
    assert "Not throttled" == throttled_status["reason"]

    # Assert JSON serialization
    json.dumps(throttled_status)


@patch("sensors.throttle.sensor.subprocess.run")
def test_read_throttle_status_throttled_under_voltage(mock_run):
    # Mock subprocess.run running vcgencmd to read throttle status
    mock_proc = MagicMock(returncode=0, stdout="throttled=0x50000")
    mock_run.return_value = mock_proc

    # Call function
    throttled_sensor = ThrottledSensor(enabled=True)
    throttled_sensor.refresh_state()
    throttled_status: SystemThrottleStatus = throttled_sensor.state

    # Assert
    assert "0x50000" == throttled_status.status_hex
    assert 327680 == throttled_status.status_decimal
    assert "0b1010000000000000000" == throttled_status.status_binary
    assert "Under-voltage has occurred. Throttling has occurred" == throttled_status.reason


@patch("sensors.throttle.sensor.subprocess.run", side_effect=FileNotFoundError("vcgencmd not found"))
def test_read_throttle_status_when_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        throttled_sensor = ThrottledSensor(enabled=True)
        throttled_sensor.refresh_state()

    # Assert error message
    assert "vcgencmd not available for this Rpi" in str(exec_info)
