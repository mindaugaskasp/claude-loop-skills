from datetime import datetime
from zoneinfo import ZoneInfo

from nudge.schedule import Appointment
from nudge.settings import Settings
from nudge.templates import render


def test_reminder_names_the_clinician_day_and_time():
    starts_at = datetime(2026, 11, 2, 9, 30, tzinfo=ZoneInfo("Europe/Vilnius"))
    appointment = Appointment("Rasa", "+37060000001", starts_at, "Dr. Jonaitis")
    text = render(appointment, Settings())
    assert "Dr. Jonaitis" in text
    assert "Monday 02 November" in text
    assert "09:30" in text
