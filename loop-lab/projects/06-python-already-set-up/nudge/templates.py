"""The texts sent to patients. All wording lives here."""

from nudge.schedule import Appointment
from nudge.settings import Settings

REMINDER = (
    "Hello {name}, this is a reminder of your appointment with {clinician} at {clinic} "
    "on {day} at {time}. Reply C to cancel."
)


def render(appointment: Appointment, settings: Settings) -> str:
    """Fill in the reminder text for one appointment."""
    return REMINDER.format(
        name=appointment.patient_name,
        clinician=appointment.clinician,
        clinic=settings.clinic_name,
        day=f"{appointment.starts_at:%A %d %B}",
        time=f"{appointment.starts_at:%H:%M}",
    )
