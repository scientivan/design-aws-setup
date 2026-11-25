# API specification

All bodies are JSON. Timestamps are ISO 8601 in UTC.

## Data entity `Ticket`

One `Ticket` record is one booking for one event.

| Field | Type | Notes |
|---|---|---|
| `ticketId` | string | Generated, format `tkt-` plus 8 hex characters. Primary key |
| `eventId` | string | Must exist in event-service, checked on create |
| `eventName` | string | Copied from event-service at booking time |
| `buyerName` | string | Required on create |
| `buyerEmail` | string | Optional |
| `quantity` | integer | Default 1, must be at least 1 |
| `totalPrice` | integer | Event price in IDR times quantity |
| `status` | string | `BOOKED` on create, can change to `PAID` or `CANCELLED` |
| `createdAt` | string | Set on create |
| `updatedAt` | string | Set on create and on every update |

Events are reference data owned by event-service (`eventId`, `name`, `date`, `venue`, `capacity`, `price`). They are not a second CRUD entity.

## Four CRUD endpoints (ticket-service, port 8082)

| Operation | Request | Success | Errors |
|---|---|---|---|
| Create | `POST /tickets` with `{"eventId","buyerName","buyerEmail"?,"quantity"?}` | 201 and the new Ticket | 400 missing field or bad quantity, 404 unknown event, 503 event-service unreachable |
| Read | `GET /tickets/{ticketId}` | 200 and the Ticket | 404 |
| Update | `PUT /tickets/{ticketId}` with any of `status`, `buyerName`, `buyerEmail` | 200 and the updated Ticket | 400 bad status or JSON, 404 |
| Delete | `DELETE /tickets/{ticketId}` | 204 with no body | 404 |

Extra routes are `GET /tickets` (list) and `GET /health`.

## event-service (port 8081)

| Request | Response |
|---|---|
| `GET /events` | 200 and the list of events |
| `GET /events/{eventId}` | 200 and one event, or 404 |
| `GET /health` | 200 `{"service":"event-service","status":"ok"}` |

## Service to service call

On `POST /tickets`, ticket-service calls `GET {EVENT_SERVICE_URL}/events/{eventId}` with a 3 second timeout. In Docker the URL is `http://event-service:8081`, resolved by the user-defined bridge network `ticketing-net`.
