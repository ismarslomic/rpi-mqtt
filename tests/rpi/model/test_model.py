#!/usr/bin/env python3
"""Tests to verify the RPI model readings"""

from unittest.mock import mock_open, patch

from rpi.model.model import read_rpi_model


# noinspection PyUnusedLocal
@patch("builtins.open", new_callable=mock_open, read_data="\x00Raspberry Pi 5 Model B Rev 1.0\x00")
def test_read_rpi_model_and_strip_specific_characters(mock_file):
    # Call function
    model: str = read_rpi_model()

    # Assert
    assert "Raspberry Pi 5 Model B Rev 1.0" == model
