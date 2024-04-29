#!/usr/bin/env python3
"""Utility functions for logging"""

import logging
from datetime import datetime, timezone

from settings.types import LogLevel, Settings


# noinspection SpellCheckingInspection
def set_global_log_config(settings: Settings):
    """Set global log formatting and log level based on the user settings"""

    log_level: LogLevel = settings.script.log_level
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.Formatter.formatTime = (
        lambda self, record, datefmt=None: datetime.fromtimestamp(record.created, timezone.utc)
        .astimezone()
        .isoformat(sep="T", timespec="milliseconds")
    )

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=numeric_level)
