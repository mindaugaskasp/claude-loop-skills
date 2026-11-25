"""Command line: `nudge appointments.csv --dry-run`."""

import argparse
import sys
from pathlib import Path

from nudge.importer import ImportProblem, read_appointments
from nudge.schedule import reminder_times
from nudge.settings import load_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nudge", description="Send appointment reminders.")
    parser.add_argument("csv", help="CSV export from the booking system")
    parser.add_argument("--dry-run", action="store_true", help="list reminders, send nothing")
    args = parser.parse_args(argv)

    settings = load_settings()
    try:
        appointments = read_appointments(Path(args.csv))
    except ImportProblem as problem:
        sys.stderr.write(f"{problem}\n")
        return 1

    if args.dry_run:
        for appointment in appointments:
            for moment in reminder_times(appointment, settings):
                sys.stdout.write(
                    f"{moment:%Y-%m-%d %H:%M}  {appointment.phone}  {appointment.patient_name}\n"
                )
        return 0

    sys.stderr.write(
        "No message gateway is configured on this machine. "
        "Run with --dry-run to see what would be sent.\n"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
