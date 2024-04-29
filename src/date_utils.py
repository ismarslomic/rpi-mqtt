#!/usr/bin/env python3
"""Common date utility functions"""

from datetime import datetime, timezone

tz = timezone.utc


def now() -> datetime:
    """Returns date time now in UTC timezone"""

    return datetime.now(tz)


def datetime_to_iso_datetime(dt: datetime) -> str:
    """Converts datetime to iso datetime string"""

    return dt.isoformat()
