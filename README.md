# Ticketing on AWS (Track B, Containers)

Week 12 project for the Cloud Computing course. The use case is event ticketing. People browse a small catalog of events and book tickets for one of them. The app is split into two containerized services that run with Docker on an EC2 host and are stored as images in Amazon ECR.

| Item | Choice |
|---|---|
| Use case | Event ticketing |
| Track | B (EC2 + Docker + ECR) |
| Data entity | `Ticket` (one booking) |
| Services | `event-service` (event catalog, read only) and `ticket-service` (Ticket CRUD) |
| AWS environment | AWS Academy Lab Project "Microservices and CI/CD Pipeline Builder" (course 195218), region `us-east-1` |

## Status (Week 12)

Both services build, run, and pass the CRUD test on the Cloud9 EC2 host, and both images are pushed to ECR. Evidence is in `evidence/`. Storage is in memory for now. See `docs/deployment-plan.md` for what comes next.

## Repository layout

| Path | Content |
|---|---|
| `services/event-service/` | `app.py` and `Dockerfile` for the event catalog (port 8081) |
| `services/ticket-service/` | `app.py` and `Dockerfile` for Ticket CRUD (port 8082) |
| `scripts/run-local.sh` | Builds both images and runs them on one Docker network |
| `scripts/test-crud.sh` | Health checks plus the four Ticket CRUD calls |
| `scripts/push-ecr.sh` | Creates the ECR repositories if missing, then tags and pushes both images |
| `docs/api-spec.md` | Endpoints, request and response shapes, status codes |
| `docs/deployment-plan.md` | How it is deployed now and the planned next phases |
| `docs/CODEX_HANDOFF.md` | Facts and instructions for the agent that writes the diagram, design brief, and evidence report |
| `evidence/outputs/` | Raw command outputs captured on AWS |
| `evidence/screenshots/` | AWS console and Cloud9 screenshots |

## Run it

Requirements are Docker, and the AWS CLI for the push step. The services use only the Python standard library, so there is no `pip install`.

```bash
./scripts/run-local.sh        # build and start both containers
./scripts/test-crud.sh        # expect HTTP 201, 200, 200, 204, then 404
./scripts/push-ecr.sh         # push to ECR (needs AWS credentials, e.g. on Cloud9)
```

## Endpoints

| Service | Method and path | Purpose |
|---|---|---|
| event-service | `GET /events`, `GET /events/{eventId}` | Event catalog |
| ticket-service | `POST /tickets` | Create (book) a ticket |
| ticket-service | `GET /tickets/{ticketId}` | Read one ticket |
| ticket-service | `PUT /tickets/{ticketId}` | Update status or buyer data |
| ticket-service | `DELETE /tickets/{ticketId}` | Delete (cancel) a ticket |

Both services also expose `GET /health`. `ticket-service` additionally has `GET /tickets` to list all tickets. Full details are in `docs/api-spec.md`.
