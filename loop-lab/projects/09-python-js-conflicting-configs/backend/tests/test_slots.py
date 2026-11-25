from datetime import UTC, datetime

from repaircafe.slots import Slot, free_slots

SLOT_A = Slot("a", datetime(2026, 12, 5, 10, 0, tzinfo=UTC), "electrics", 2)
SLOT_B = Slot("b", datetime(2026, 12, 5, 11, 0, tzinfo=UTC), "sewing", 1)


def test_full_slot_is_not_free():
    bookings = [{"slot_id": "b", "visitor": "Ona", "item": "clothing", "notes": {}}]
    assert free_slots([SLOT_A, SLOT_B], bookings) == [SLOT_A]


def test_filter_by_skill():
    assert free_slots([SLOT_A, SLOT_B], [], ["sewing"]) == [SLOT_B]
