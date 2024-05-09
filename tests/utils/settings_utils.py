#!/usr/bin/env python3
"""Utility for reading sample settings during tests"""

from pathlib import Path

from settings.settings import read_settings
from settings.types import Settings


def read_test_settings() -> Settings:
    """Read sample settings file and return as Settings"""

    # Sample file
    current_folder: Path = Path(__file__).resolve().parent
    sample_file_name: str = "sample_settings.yml"
    sample_file_path: str = current_folder.joinpath(sample_file_name).__str__()

    # Call function
    settings: Settings = read_settings(sample_file_path)

    return settings
