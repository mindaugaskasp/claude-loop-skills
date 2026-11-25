"""Reads the booking system's CSV export."""

import csv
import logging
import re
from datetime import datetime
from pathlib import Path

from nudge.schedule import Appointment

log = logging.getLogger(__name__)

PHONE = re.compile(r"\+[1-9][0-9]{7,14}")
COLUMNS = ("patient_name", "phone", "starts_at", "clinician")


class ImportProblem(Exception):
    """The file cannot be used as it is. The message says what to fix."""


def read_appointments(path: Path) -> list[Appointment]:
    """Read every usable row. Rows with a bad phone number are skipped and reported."""
    appointments = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ImportProblem(
                f"{path.name} has no column named {', '.join(missing)}. "
                "Export the appointments again with all four columns."
            )
        for number, row in enumerate(reader, start=2):
            phone = row["phone"].strip()
            if not PHONE.fullmatch(phone):
                log.warning(f"Row {number}: phone {phone!r} is not in international form, skipped")
                continue
            try:
                starts_at = datetime.strptime(row["starts_at"].strip(), "%Y-%m-%d %H:%M")
            except ValueError as error:
                raise ImportProblem(
                    f"Row {number} of {path.name}: the start time {row['starts_at']!r} is not "
                    "in the form 2026-11-02 09:30. Correct it in the booking system and export again."
                ) from error
            appointments.append(
                Appointment(
                    patient_name=row["patient_name"].strip(),
                    phone=phone,
                    starts_at=starts_at,
                    clinician=row["clinician"].strip(),
                )
            )
    return appointments
