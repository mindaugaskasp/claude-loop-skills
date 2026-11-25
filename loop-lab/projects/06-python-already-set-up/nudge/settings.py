"""Settings of one clinic, read from the environment."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    clinic_name: str = "Harbour Street Clinic"
    time_zone: str = "Europe/Vilnius"
    hours_before: tuple[int, ...] = (24, 2)
    quiet_from: int = 21
    quiet_until: int = 8
    window_seconds: int = 300


def load_settings() -> Settings:
    """Build the settings, taking anything set in the environment over the defaults."""
    defaults = Settings()
    hours = os.environ.get("NUDGE_HOURS_BEFORE")
    try:
        hours_before = (
            tuple(int(part) for part in hours.split(",")) if hours else defaults.hours_before
        )
    except ValueError as error:
        raise SystemExit(
            f"NUDGE_HOURS_BEFORE is {hours!r}. Set it to whole numbers separated by commas, "
            "for example 24,2."
        ) from error
    return Settings(
        clinic_name=os.environ.get("NUDGE_CLINIC_NAME", defaults.clinic_name),
        time_zone=os.environ.get("NUDGE_TIME_ZONE", defaults.time_zone),
        hours_before=hours_before,
        quiet_from=int(os.environ.get("NUDGE_QUIET_FROM", defaults.quiet_from)),
        quiet_until=int(os.environ.get("NUDGE_QUIET_UNTIL", defaults.quiet_until)),
        window_seconds=defaults.window_seconds,
    )
