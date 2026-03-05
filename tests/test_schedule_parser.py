from datetime import datetime

import pytest

from bot.services.schedule_parser import is_valid_schedule, should_fire


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def dt(weekday: int, hour: int, minute: int) -> datetime:
    """Build a datetime with the given weekday (0=Mon) and time."""
    # 2024-01-01 is a Monday (weekday=0)
    base = datetime(2024, 1, 1)
    days_offset = (weekday - base.weekday()) % 7
    return base.replace(day=1 + days_offset, hour=hour, minute=minute, second=0)


MON = dt(0, 9, 0)
TUE = dt(1, 9, 0)
WED = dt(2, 9, 0)
FRI = dt(4, 18, 0)
SUN = dt(6, 9, 0)


# ---------------------------------------------------------------------------
# should_fire
# ---------------------------------------------------------------------------

class TestShouldFireDaily:
    def test_fires_on_matching_time(self):
        assert should_fire("daily 09:00", MON) is True

    def test_fires_every_day_same_time(self):
        for weekday in range(7):
            assert should_fire("daily 09:00", dt(weekday, 9, 0)) is True

    def test_does_not_fire_wrong_hour(self):
        assert should_fire("daily 09:00", dt(0, 10, 0)) is False

    def test_does_not_fire_wrong_minute(self):
        assert should_fire("daily 09:00", dt(0, 9, 1)) is False

    def test_case_insensitive(self):
        assert should_fire("DAILY 09:00", MON) is True
        assert should_fire("daily 09:00", MON) is True


class TestShouldFireSingleDay:
    def test_fires_on_correct_day_and_time(self):
        assert should_fire("FRI 18:00", FRI) is True

    def test_does_not_fire_on_wrong_day(self):
        assert should_fire("FRI 18:00", MON) is False

    def test_does_not_fire_on_adjacent_day(self):
        assert should_fire("MON 09:00", TUE) is False

    def test_fires_monday(self):
        assert should_fire("MON 09:00", MON) is True

    def test_fires_sunday(self):
        assert should_fire("SUN 09:00", SUN) is True

    def test_case_insensitive(self):
        assert should_fire("fri 18:00", FRI) is True


class TestShouldFireMultipleDays:
    def test_fires_on_first_day(self):
        assert should_fire("MON,WED,FRI 09:00", MON) is True

    def test_fires_on_middle_day(self):
        assert should_fire("MON,WED,FRI 09:00", WED) is True

    def test_fires_on_last_day(self):
        assert should_fire("MON,WED,FRI 09:00", FRI.replace(hour=9)) is True

    def test_does_not_fire_on_excluded_day(self):
        assert should_fire("MON,WED,FRI 09:00", TUE) is False


class TestShouldFireEdgeCases:
    def test_midnight(self):
        assert should_fire("daily 00:00", dt(0, 0, 0)) is True
        assert should_fire("daily 00:00", dt(0, 0, 1)) is False

    def test_end_of_day(self):
        assert should_fire("daily 23:59", dt(0, 23, 59)) is True
        assert should_fire("daily 23:59", dt(0, 23, 58)) is False

    def test_invalid_schedule_returns_false(self):
        assert should_fire("", dt(0, 9, 0)) is False
        assert should_fire("bad input", dt(0, 9, 0)) is False
        assert should_fire("BLAH 09:00", dt(0, 9, 0)) is False
        assert should_fire("daily 9:0", dt(0, 9, 0)) is False


# ---------------------------------------------------------------------------
# is_valid_schedule
# ---------------------------------------------------------------------------

class TestIsValidSchedule:
    @pytest.mark.parametrize("schedule", [
        "daily 09:00",
        "DAILY 09:00",
        "MON 09:00",
        "FRI 18:00",
        "SUN 00:00",
        "MON,WED,FRI 09:00",
        "SAT,SUN 10:30",
        "daily 23:59",
        "daily 00:00",
    ])
    def test_valid(self, schedule: str):
        assert is_valid_schedule(schedule) is True

    @pytest.mark.parametrize("schedule", [
        "",
        "09:00",
        "daily",
        "daily 9:00",       # single-digit hour
        "daily 09:0",       # single-digit minute
        "daily 24:00",      # hour out of range
        "daily 09:60",      # minute out of range
        "XYZ 09:00",        # unknown day
        "MON,XYZ 09:00",    # one unknown day
        "daily 09:00 extra",# too many parts
        "MON WED 09:00",    # days separated by space instead of comma
    ])
    def test_invalid(self, schedule: str):
        assert is_valid_schedule(schedule) is False
