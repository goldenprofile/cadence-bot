"""
Parse reminder schedule strings and check if they fire at a given minute.

Supported formats (case-insensitive):
  daily HH:MM
  MON HH:MM
  MON,WED,FRI HH:MM

Weekday names: MON TUE WED THU FRI SAT SUN
"""

from datetime import datetime

_WEEKDAYS = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6}


def should_fire(schedule: str, now: datetime) -> bool:
    """Return True if the reminder should fire at `now` (checked at minute precision)."""
    parts = schedule.strip().upper().split()
    if len(parts) != 2:
        return False

    day_part, time_part = parts

    parts = time_part.split(":")
    if len(parts) != 2 or len(parts[0]) != 2 or len(parts[1]) != 2:
        return False
    try:
        h, m = int(parts[0]), int(parts[1])
    except ValueError:
        return False

    if now.hour != h or now.minute != m:
        return False

    if day_part == "DAILY":
        return True

    target_days = {_WEEKDAYS[d] for d in day_part.split(",") if d in _WEEKDAYS}
    return now.weekday() in target_days


def is_valid_schedule(schedule: str) -> bool:
    """Return True if the schedule string is parseable."""
    parts = schedule.strip().upper().split()
    if len(parts) != 2:
        return False

    day_part, time_part = parts

    parts = time_part.split(":")
    if len(parts) != 2 or len(parts[0]) != 2 or len(parts[1]) != 2:
        return False
    try:
        h, m = int(parts[0]), int(parts[1])
    except ValueError:
        return False

    if not (0 <= h <= 23 and 0 <= m <= 59):
        return False

    if day_part == "DAILY":
        return True

    day_names = day_part.split(",")
    return bool(day_names) and all(d in _WEEKDAYS for d in day_names)
