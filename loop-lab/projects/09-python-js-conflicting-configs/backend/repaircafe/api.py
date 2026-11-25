import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from repaircafe import BookingError, store
from repaircafe.bookings import add_booking
from repaircafe.slots import free_slots


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict) -> None:
        data = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path != "/slots":
            self._send(404, {"error": "Not found"})
            return
        slots, bookings = store.load()
        free = free_slots(slots, bookings)
        listed = [{"id": s.slot_id, "starts_at": s.starts_at.isoformat(), "skill": s.skill} for s in free]
        self._send(200, {"slots": listed})

    def do_POST(self) -> None:
        if self.path != "/bookings":
            self._send(404, {"error": "Not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        slots, bookings = store.load()
        slot = next((s for s in slots if s.slot_id == payload.get("slot_id")), None)
        if slot is None:
            self._send(400, {"error": "That time slot does not exist any more. Please reload the page."})
            return
        # The widget already checks that the name and phone number are filled in.
        try:
            booking = add_booking(slot, bookings, payload["visitor"], payload["item"])
        except BookingError as error:
            self._send(409, {"error": str(error)})
            return
        store.save(slots, bookings)
        self._send(201, booking)


def main() -> None:
    HTTPServer(("127.0.0.1", 8040), Handler).serve_forever()


if __name__ == "__main__":
    main()
