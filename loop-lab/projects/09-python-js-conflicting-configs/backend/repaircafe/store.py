import json
from pathlib import Path

from repaircafe.slots import Slot, parse_slot

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "bookings.json"


def load(path: Path = DATA_FILE) -> tuple[list[Slot], list[dict]]:
    if not path.exists():
        return [], []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [parse_slot(s) for s in raw["slots"]], raw["bookings"]


def save(slots: list[Slot], bookings: list[dict], path: Path = DATA_FILE) -> None:
    raw = {
        "slots": [
            {"id": s.slot_id, "starts_at": s.starts_at.isoformat(), "skill": s.skill, "capacity": s.capacity}
            for s in slots
        ],
        "bookings": bookings,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
