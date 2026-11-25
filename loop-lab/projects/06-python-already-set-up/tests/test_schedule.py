from dataclasses import replace
from datetime import datetime
from zoneinfo import ZoneInfo

from nudge.schedule import Appointment, due_now, in_quiet_hours, reminder_times
from nudge.settings import Settings

NO_QUIET_HOURS = Settings(quiet_from=24, quiet_until=0)
VILNIUS = ZoneInfo("Europe/Vilnius")


def appointment_at(starts_at: datetime) -> Appointment:
    return Appointment("Rasa Petrauskaite", "+37060000001", starts_at, "Dr. Jonaitis")


def test_reminders_are_earliest_first():
    appointment = appointment_at(datetime(2026, 11, 2, 14, 0))
    times = reminder_times(appointment, NO_QUIET_HOURS)
    assert times == [datetime(2026, 11, 1, 14, 0), datetime(2026, 11, 2, 12, 0)]


def test_quiet_hours_use_the_clinic_time_zone():
    settings = Settings()
    assert in_quiet_hours(datetime(2026, 11, 2, 22, 30, tzinfo=VILNIUS), settings)
    assert not in_quiet_hours(datetime(2026, 11, 2, 12, 0, tzinfo=VILNIUS), settings)


def test_reminder_in_quiet_hours_is_left_out():
    appointment = appointment_at(datetime(2026, 11, 2, 9, 0, tzinfo=VILNIUS))
    times = reminder_times(appointment, Settings())
    assert times == [datetime(2026, 11, 1, 9, 0, tzinfo=VILNIUS)]


def test_due_inside_the_window_only():
    appointment = appointment_at(datetime(2026, 11, 2, 14, 0))
    settings = replace(NO_QUIET_HOURS, window_seconds=300)
    assert due_now(appointment, settings, now=datetime(2026, 11, 2, 12, 3))
    assert not due_now(appointment, settings, now=datetime(2026, 11, 2, 12, 30))
