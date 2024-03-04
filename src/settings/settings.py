#!/usr/bin/env python3
"""Service for reading the settings file"""
import json
from pathlib import Path
from textwrap import dedent

import jsonschema_markdown
import yaml

from settings.types import Settings

docs_folder: Path = Path(__file__).resolve().parent.parent.parent.joinpath("docs")


def read_settings(file_path: str | None = None) -> Settings:
    """Reads settings from settings file (YAML) from provided file path or returns default settings if not provided"""

    if file_path:
        yml_content = _parse_settings_file_as_dict(file_path)
        return Settings(**yml_content)

    return Settings()


def write_model_to_json():
    """Write Settings model as json file"""

    model_as_json: str = json.dumps(Settings.model_json_schema(), ensure_ascii=False, indent=2)
    model_as_json += "\n"
    filepath: str = str(docs_folder.joinpath("settings.json"))

    # Writing to json representation of the settings model to file
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(model_as_json)


def write_model_to_mkd():
    """Write Settings model as markdown file"""

    model_as_json: dict = Settings.model_json_schema()
    mkd_filepath: str = str(docs_folder.joinpath("settings.md"))

    settings_mkd_schema: str = dedent(
        """\
    > [!NOTE]
    > This is markdown documentation of the schema for Settings file. You can find corresponding description as
    > JSON schema in [settings.json](settings.json).

    """
    )
    settings_mkd_schema += jsonschema_markdown.generate(schema=model_as_json, footer=False)

    # Writing to markdown representation of the settings model to file
    with open(mkd_filepath, "w", encoding="utf-8") as outfile:
        outfile.write(settings_mkd_schema)


def _parse_settings_file_as_dict(file_path: str) -> dict[str, dict]:
    """Parse settings yaml file as python dict"""

    file = Path(file_path)
    if not file.is_file():
        raise ValueError(f"{file.name} is not a file")

    with open(file, mode="r", encoding="UTF-8") as f:
        return yaml.full_load(f) or {}
