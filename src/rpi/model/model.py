#!/usr/bin/env python3
"""Service for reading the Rpi model"""


def read_rpi_model() -> str:
    """Read Rpi model"""

    model_file_name = "/sys/firmware/devicetree/base/model"
    with open(model_file_name, "r") as f:
        model = f.readline().strip("\x00")

    return model
