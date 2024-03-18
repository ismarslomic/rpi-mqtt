#!/usr/bin/env python3
"""Tests to verify the RPI model readings"""

from unittest.mock import mock_open, patch

import pytest

from sensors.model.sensor import RpiModelSensor
from sensors.types import SensorNotAvailableException


# noinspection PyUnusedLocal
@patch("builtins.open", new_callable=mock_open, read_data="\x00Raspberry Pi 5 Model B Rev 1.0\x00")
def test_read_rpi_model_and_strip_specific_characters(mock_file):
    # Call function
    model: str = RpiModelSensor().read()

    # Assert
    assert "Raspberry Pi 5 Model B Rev 1.0" == model


@patch("builtins.open", side_effect=FileNotFoundError("No such file or directory"))
def test_read_model_not_available_for_platform(_):
    # Call function
    with pytest.raises(SensorNotAvailableException) as exec_info:
        RpiModelSensor().read()

    # Assert error message
    assert "rpi model file not available for this Rpi" in str(exec_info)
