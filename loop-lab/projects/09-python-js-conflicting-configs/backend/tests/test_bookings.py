from datetime import UTC, datetime

import pytest

from repaircafe import BookingError
from repaircafe.bookings import add_booking, cancel_booking
from repaircafe.slots import Slot

SLOT = Slot("a", datetime(2026, 12, 5, 10, 0, tzinfo=UTC), "electrics", 1)


def test_booking_is_added():
    bookings = []
    add_booking(SLOT, bookings, "Jonas", "lamp")
    assert bookings[0]["visitor"] == "Jonas"


def test_full_slot_is_refused():
    bookings = [{"slot_id": "a", "visitor": "Ona", "item": "radio", "notes": {}}]
    with pytest.raises(BookingError):
        add_booking(SLOT, bookings, "Jonas", "lamp")


def test_unknown_item_is_refused():
    with pytest.raises(BookingError):
        add_booking(SLOT, [], "Jonas", "car")


def test_cancel():
    bookings = [{"slot_id": "a", "visitor": "Ona", "item": "radio", "notes": {}}]
    assert cancel_booking(bookings, "a", "Ona") is True
    assert bookings == []
