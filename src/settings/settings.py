#!/usr/bin/env python3
"""Service for reading the settings file"""
from pathlib import Path

import yaml

from settings.types import Settings

docs_folder: Path = Path(__file__).resolve().parent.parent.parent.joinpath("docs")


def read_settings(file_path: str | None = None) -> Settings:
    """Reads settings from settings file (YAML) from provided file path or returns default settings if not provided"""

    if file_path:
        yml_content = _parse_settings_file_as_dict(file_path)
        return Settings(**yml_content)

    return Settings()


def _parse_settings_file_as_dict(file_path: str) -> dict[str, dict]:
    """Parse settings yaml file as python dict"""

    file = Path(file_path)
    if not file.is_file():
        raise ValueError(f"{file.name} is not a file")

    with open(file, mode="r", encoding="UTF-8") as f:
        return yaml.full_load(f) or {}
