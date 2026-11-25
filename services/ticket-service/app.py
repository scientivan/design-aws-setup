"""ticket-service menyediakan CRUD untuk entitas Ticket. Satu Ticket mewakili satu pemesanan.

Layanan memeriksa keberadaan acara melalui event-service sebelum membuat tiket.
Implementasi Minggu 12 menyimpan tiket di memori. Rencana penyimpanan
persisten tersedia di docs/deployment-plan.md.
Layanan hanya memakai pustaka standar Python.
"""
import json
import os
import threading
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8082"))
EVENT_SERVICE_URL = os.environ.get("EVENT_SERVICE_URL", "http://localhost:8081")
VALID_STATUS = {"BOOKED", "PAID", "CANCELLED"}

TICKETS = {}
LOCK = threading.Lock()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_event(event_id):
    try:
        with urllib.request.urlopen(f"{EVENT_SERVICE_URL}/events/{event_id}", timeout=3) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body=None):
        data = b"" if body is None else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return None

    def _parts(self):
        return [p for p in self.path.split("?")[0].split("/") if p]

    def do_GET(self):
        parts = self._parts()
        if parts == ["health"]:
            return self._send(200, {"service": "ticket-service", "status": "ok", "eventServiceUrl": EVENT_SERVICE_URL})
        if parts == ["tickets"]:
            with LOCK:
                return self._send(200, list(TICKETS.values()))
        if len(parts) == 2 and parts[0] == "tickets":
            with LOCK:
                t = TICKETS.get(parts[1])
            return self._send(200, t) if t else self._send(404, {"error": "ticket not found"})
        return self._send(404, {"error": "route not found"})

    def do_POST(self):
        if self._parts() != ["tickets"]:
            return self._send(404, {"error": "route not found"})
        body = self._json()
        if not body or not body.get("eventId") or not body.get("buyerName"):
            return self._send(400, {"error": "eventId and buyerName are required"})
        qty = body.get("quantity", 1)
        if not isinstance(qty, int) or qty < 1:
            return self._send(400, {"error": "quantity must be a positive integer"})
        try:
            event = fetch_event(body["eventId"])
        except Exception as e:  # event-service tidak tersedia
            return self._send(503, {"error": f"event-service unavailable: {e}"})
        if event is None:
            return self._send(404, {"error": "event not found"})
        ticket = {
            "ticketId": "tkt-" + uuid.uuid4().hex[:8],
            "eventId": event["eventId"],
            "eventName": event["name"],
            "buyerName": body["buyerName"],
            "buyerEmail": body.get("buyerEmail", ""),
            "quantity": qty,
            "totalPrice": event["price"] * qty,
            "status": "BOOKED",
            "createdAt": now(),
            "updatedAt": now(),
        }
        with LOCK:
            TICKETS[ticket["ticketId"]] = ticket
        return self._send(201, ticket)

    def do_PUT(self):
        parts = self._parts()
        if not (len(parts) == 2 and parts[0] == "tickets"):
            return self._send(404, {"error": "route not found"})
        body = self._json()
        if body is None:
            return self._send(400, {"error": "invalid JSON"})
        with LOCK:
            t = TICKETS.get(parts[1])
            if not t:
                return self._send(404, {"error": "ticket not found"})
            if "status" in body:
                if body["status"] not in VALID_STATUS:
                    return self._send(400, {"error": f"status must be one of {sorted(VALID_STATUS)}"})
                t["status"] = body["status"]
            for field in ("buyerName", "buyerEmail"):
                if field in body:
                    t[field] = body[field]
            t["updatedAt"] = now()
            return self._send(200, t)

    def do_DELETE(self):
        parts = self._parts()
        if not (len(parts) == 2 and parts[0] == "tickets"):
            return self._send(404, {"error": "route not found"})
        with LOCK:
            if TICKETS.pop(parts[1], None) is None:
                return self._send(404, {"error": "ticket not found"})
        return self._send(204)

    def log_message(self, fmt, *args):
        print("[ticket-service] " + fmt % args, flush=True)


if __name__ == "__main__":
    print(f"ticket-service listening on :{PORT}, event-service at {EVENT_SERVICE_URL}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
