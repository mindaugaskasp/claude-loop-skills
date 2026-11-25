from datetime import UTC, datetime

from repaircafe import BookingError
from repaircafe.slots import Slot, booked_count

ALLOWED_ITEMS = {"lamp", "toaster", "radio", "bicycle", "clothing", "kettle", "laptop"}


def add_booking(slot: Slot, bookings: list[dict], visitor: str, item: str, notes={}) -> dict:
    if item not in ALLOWED_ITEMS:
        raise BookingError(f"We cannot repair a {item} yet. Ask at the desk which items we take.")
    if booked_count(slot, bookings) >= slot.capacity:
        raise BookingError("This slot is full. Please choose another time.")
    notes["booked_at"] = datetime.now(UTC).isoformat()
    booking = {"slot_id": slot.slot_id, "visitor": visitor, "item": item, "notes": notes}
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[dict], slot_id: str, visitor: str) -> bool:
    for index, booking in enumerate(bookings):
        if booking["slot_id"] == slot_id and booking["visitor"] == visitor:
            del bookings[index]
            return True
    return False
