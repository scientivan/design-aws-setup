#!/usr/bin/env bash
# Uji pemeriksaan layanan, pencarian acara, dan empat endpoint CRUD Ticket.
set -euo pipefail
E=${EVENT_URL:-http://localhost:8081}
T=${TICKET_URL:-http://localhost:8082}
step() { echo; echo "### $*"; }
step "GET $E/health";  curl -s -w '\nHTTP %{http_code}\n' "$E/health"
step "GET $T/health";  curl -s -w '\nHTTP %{http_code}\n' "$T/health"
step "GET $E/events";  curl -s -w '\nHTTP %{http_code}\n' "$E/events"
step "CREATE  POST $T/tickets"
RESP=$(curl -s -X POST "$T/tickets" -H 'Content-Type: application/json' \
  -d '{"eventId":"evt-001","buyerName":"Test Buyer","buyerEmail":"buyer@example.com","quantity":2}')
echo "$RESP"
ID=$(echo "$RESP" | python3 -c 'import sys,json;print(json.load(sys.stdin)["ticketId"])')
step "READ    GET $T/tickets/$ID";    curl -s -w '\nHTTP %{http_code}\n' "$T/tickets/$ID"
step "UPDATE  PUT $T/tickets/$ID";    curl -s -w '\nHTTP %{http_code}\n' -X PUT "$T/tickets/$ID" -H 'Content-Type: application/json' -d '{"status":"PAID"}'
step "DELETE  DELETE $T/tickets/$ID"; curl -s -w 'HTTP %{http_code}\n' -X DELETE "$T/tickets/$ID"
step "READ after delete (expect 404)"; curl -s -w '\nHTTP %{http_code}\n' "$T/tickets/$ID"
step "CREATE with unknown event (expect 404 from event-service check)"
curl -s -w '\nHTTP %{http_code}\n' -X POST "$T/tickets" -H 'Content-Type: application/json' -d '{"eventId":"evt-999","buyerName":"X"}'
echo; echo "CRUD_TEST_DONE"
