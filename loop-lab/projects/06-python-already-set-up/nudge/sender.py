"""Sends the reminders that are due."""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from nudge.schedule import Appointment, due_now
from nudge.settings import Settings
from nudge.templates import render

log = logging.getLogger(__name__)


class Gateway(Protocol):
    """Whatever delivers a text message. Returns the message's id."""

    def send(self, phone: str, text: str) -> str: ...


@dataclass(frozen=True)
class SendResult:
    appointment: Appointment
    message_id: str | None
    attempted_at: datetime


def _stamp() -> datetime:
    return datetime.utcnow()


def send_due(
    appointments: list[Appointment],
    settings: Settings,
    gateway: Gateway,
    now: datetime | None = None,
) -> list[SendResult]:
    """Send a reminder for every appointment that has one due now."""
    results = []
    for appointment in appointments:
        if not due_now(appointment, settings, now):
            continue
        text = render(appointment, settings)
        try:
            message_id = gateway.send(appointment.phone, text)
        except OSError as error:
            log.warning(f"Could not send to {appointment.phone}: {error}")
            results.append(SendResult(appointment, None, _stamp()))
            continue
        log.info(f"Sent reminder {message_id} to {appointment.phone}")
        results.append(SendResult(appointment, message_id, _stamp()))
    return results
