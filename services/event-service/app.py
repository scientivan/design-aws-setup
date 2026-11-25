"""event-service menyediakan katalog baca-saja untuk acara yang dapat dipesan.

Layanan hanya memakai pustaka standar Python.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8081"))

EVENTS = {
    "evt-001": {"eventId": "evt-001", "name": "Campus Music Night", "date": "2026-12-12", "venue": "Grha Sabha Pramana", "capacity": 500, "price": 75000},
    "evt-002": {"eventId": "evt-002", "name": "Cloud Computing Talk", "date": "2026-12-19", "venue": "DTETI Auditorium", "capacity": 150, "price": 0},
    "evt-003": {"eventId": "evt-003", "name": "Startup Demo Day", "date": "2027-01-09", "venue": "UGM Innovation Hub", "capacity": 300, "price": 25000},
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parts = [p for p in self.path.split("?")[0].split("/") if p]
        if parts == ["health"]:
            return self._send(200, {"service": "event-service", "status": "ok"})
        if parts == ["events"]:
            return self._send(200, list(EVENTS.values()))
        if len(parts) == 2 and parts[0] == "events":
            event = EVENTS.get(parts[1])
            if event:
                return self._send(200, event)
            return self._send(404, {"error": "event not found"})
        return self._send(404, {"error": "route not found"})

    def log_message(self, fmt, *args):
        print("[event-service] " + fmt % args, flush=True)


if __name__ == "__main__":
    print(f"event-service listening on :{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
