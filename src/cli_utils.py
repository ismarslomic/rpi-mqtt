#!/usr/bin/env python3
"""Utility functions for command-line interface"""
from argparse import ArgumentParser


def cli_create_arg_parser() -> ArgumentParser:
    """Create an argparse.ArgumentParser instance for a simple command-line utility.
    The returned parser is pre-configured with one required `-i <settings-file>` argument.
    """
    settings_file: str = "--settings-file"
    parser = ArgumentParser(description="rpi-mqtt command line arguments")
    parser.add_argument(
        "-s",
        settings_file,
        help="path to the settings file, example: -s /Users/john/rpi-mqtt/settings.yml",
        metavar="<settings-file>",
        required=True,
    )

    return parser
