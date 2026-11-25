"""Works out when each reminder should go out."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from nudge.settings import Settings


@dataclass(frozen=True)
class Appointment:
    patient_name: str
    phone: str
    starts_at: datetime
    clinician: str


def reminder_times(appointment: Appointment, settings: Settings) -> list[datetime]:
    """Return the moments a reminder is due, earliest first, leaving out the quiet hours."""
    hours = sorted(settings.hours_before, reverse=True)
    times = [appointment.starts_at - timedelta(hours=hour) for hour in hours]
    return [moment for moment in times if not in_quiet_hours(moment, settings)]


def in_quiet_hours(moment: datetime, settings: Settings) -> bool:
    """True when the clinic does not want messages sent at this moment."""
    local = moment.astimezone(ZoneInfo(settings.time_zone))
    return local.hour >= settings.quiet_from or local.hour < settings.quiet_until


def due_now(appointment: Appointment, settings: Settings, now: datetime | None = None) -> bool:
    """True when one of the appointment's reminders falls inside the sending window."""
    now = now or datetime.now()
    return any(
        abs((moment - now).total_seconds()) <= settings.window_seconds
        for moment in reminder_times(appointment, settings)
    )
