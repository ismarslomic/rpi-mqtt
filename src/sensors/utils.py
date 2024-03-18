#!/usr/bin/env python3
"""Common utility functions used across Rpi sensors"""

from datetime import datetime, timezone


def date_and_timestamp_to_iso_datetime(datetime_and_ts: str) -> str:
    """Format datetime and timestamp (seconds since the epoch) as ISO 8601 formatted string, including timezone
    offset. Example input 'Wed Dec  6 18:29:25 UTC 2023 (1701887365)' will return '2023-12-06T18:29:25+00:00'."""

    timestamp: int = int(datetime_and_ts[datetime_and_ts.find("(") + 1 : datetime_and_ts.find(")")])
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def epoch_to_iso_datetime(timestamp: float) -> str:
    """Format timestamp (seconds since the epoch) as ISO 8601 formatted string, including timezone offset.
    Example input '1705927879.0' will return '2024-01-22T12:51:19+00:00'."""

    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def round_percent(percent: float) -> float:
    """Round percent value to 2 decimal"""

    return round(percent, 2)


def round_temp(temp: float) -> float:
    """Round temp value to 1 decimal"""

    return round(temp, 1)


def bytes_to_gibibytes(value_bytes: int) -> float:
    """Convert bytes (B) to gibibytes (GiB) with 2 decimals."""

    value_gibibytes: float = value_bytes / 1024.0 / 1024.0 / 1024.0

    return round(value_gibibytes, 2)
