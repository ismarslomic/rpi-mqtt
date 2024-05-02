#!/usr/bin/env python3
"""Common date utility functions"""

from datetime import datetime, timezone

tz = timezone.utc


def now() -> datetime:
    """Returns date time now in UTC timezone"""

    return datetime.now(tz)


def now_to_iso_datetime() -> str:
    """Returns date time now in UTC timezone as string"""

    dt_now = now()
    dt_now_iso = datetime_to_iso_datetime(dt_now)

    return dt_now_iso


def datetime_to_iso_datetime(dt: datetime) -> str:
    """Converts datetime to iso datetime string"""

    return dt.isoformat()
