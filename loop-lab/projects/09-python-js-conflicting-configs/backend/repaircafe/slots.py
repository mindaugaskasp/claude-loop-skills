from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Slot:
    slot_id: str
    starts_at: datetime
    skill: str
    capacity: int


def parse_slot(raw: dict) -> Slot:
    return Slot(
        slot_id=raw["id"],
        starts_at=datetime.fromisoformat(raw["starts_at"]),
        skill=raw["skill"],
        capacity=int(raw["capacity"]),
    )


def booked_count(slot: Slot, bookings: list[dict]) -> int:
    return sum(1 for b in bookings if b["slot_id"] == slot.slot_id)


def free_slots(slots: list[Slot], bookings: list[dict], skills=[]) -> list[Slot]:
    """Slots that still have room, optionally only for the given repair skills."""
    result = []
    for slot in slots:
        if skills and slot.skill not in skills:
            continue
        if booked_count(slot, bookings) < slot.capacity:
            result.append(slot)
    return result
