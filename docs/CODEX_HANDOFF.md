# Handoff for the documentation agent

This file gives you everything needed to write the three remaining Week 12 deliverables. Use only the facts here and in the linked files. Do not invent resources, IDs, or test results.

## What the course asks for

Source is `../Lab_Project_Cloud_Computing_AWS_Lab_Project_Briefing_Updated.pdf` (one folder above this repo).

1. Architecture diagram. Label planned components, data flow, and IAM or security.
2. Design brief of 1 to 2 pages. Cover the use case, the chosen track, the data entity, and the 4 CRUD endpoints.
3. Git repository with README, starter code, deployment plan, and progressive commits. This repo already covers it.
4. AWS evidence. Screenshots and connectivity or test outputs.

Track B minimum is "two planned services" and "build one Docker image". This project has two services built and pushed.

## Facts to use

| Topic | Source file |
|---|---|
| Endpoints, entity fields, status codes | `docs/api-spec.md` |
| What was deployed and what is planned | `docs/deployment-plan.md` |
| Account, VPC, subnets, instances, security group, ECR digests, IAM | `evidence/outputs/07-infrastructure-inventory.txt` |
| Tool versions and identity | `evidence/outputs/01-environment.txt` |
| Build and run log | `evidence/outputs/02-docker-build-run.txt`, `03-docker-ps.txt`, `06-docker-images.txt` |
| CRUD test output | `evidence/outputs/04-crud-test.txt` |
| ECR push output | `evidence/outputs/05-ecr-push.txt` |
| Screenshots | `evidence/screenshots/` (see table below) |

## Architecture diagram content

Draw the current state (Week 12) and mark planned parts with a dashed line and the word "planned".

Current state, inside AWS account 339712824643, region us-east-1.

1. VPC `LabVPC` 10.16.0.0/16 containing `Public Subnet1` 10.16.10.0/24 in us-east-1a.
2. In that subnet, EC2 instance `aws-cloud9-MicroservicesIDE` (t3.small, Amazon Linux 2023, private IP 10.16.10.227) acting as the Docker host.
3. On that host, Docker network `ticketing-net` with two containers. `event-service` on port 8081 and `ticket-service` on port 8082. Arrow from ticket-service to event-service labeled `GET /events/{id}` (validate event on create).
4. Security group `sg-010fc165085e65785` allows only TCP 22 from the AWS Cloud9 service ranges. Ports 8081 and 8082 are not public.
5. Developer (browser) connects to the Cloud9 IDE over the AWS console, and Cloud9 reaches the instance over SSH.
6. Amazon ECR private registry with repos `ticketing/event-service:v1` and `ticketing/ticket-service:v1`. Arrow from the EC2 host to ECR labeled `docker push` (and later `docker pull`).
7. IAM. The EC2 host acts with the lab role `voclabs` through Cloud9 managed temporary credentials. ECR login uses `aws ecr get-login-password`, a short-lived token. No access keys are stored in the repo.

Planned (dashed).

1. Application Load Balancer in Public Subnet1 and Public Subnet2, routing `/events*` to event-service and `/tickets*` to ticket-service. This is the only public entry for users.
2. Persistent storage for tickets (SQLite on a Docker volume first).
3. Amazon ECS services per microservice and a CodePipeline plus CodeDeploy pipeline (lab Phases 5 to 9).

Request flow to show, numbered. User sends `POST /tickets` (1), ticket-service asks event-service for the event (2), event-service returns the event (3), ticket-service stores the Ticket and returns 201 (4). In Week 12 the "user" is `curl` on the same host.

The `MonolithicAppServer` instance (t2.micro, 10.16.10.229) was created by the lab and is not part of this app. Leave it out of the diagram or show it greyed out with that note.

## Design brief content

Use case is event ticketing for campus events. Track B (EC2, Docker, ECR). Reason for the track is that the lab environment supports exactly these services and the briefing allows Track B. The single entity is `Ticket`. The four CRUD endpoints are in `docs/api-spec.md`. Explain why there are two services. event-service owns event data and ticket-service owns bookings, so each can be built, deployed, and later scaled on its own. Mention the Week 12 limits honestly. Storage is in memory, the services are not exposed to the internet yet, and tests ran from inside the instance.

## Screenshot index

| File | Shows |
|---|---|
| `01-cloud9-docker-ps-and-post-ticket.jpg` | Cloud9 terminal with both containers up and a `POST /tickets` returning HTTP 201 |
| `02-ecr-repositories.jpg` | ECR private repositories `ticketing/event-service` and `ticketing/ticket-service` |
| `03-ecr-ticket-service-image-v1.jpg` | Image `v1` in `ticketing/ticket-service`, 18.05 MB, digest `sha256:2cce6dc1...` |
| `04-ec2-instances-running.jpg` | EC2 list with `aws-cloud9-MicroservicesIDE` t3.small running and 3/3 checks passed |
| `05-cloud9-environment.jpg` | Cloud9 environment `MicroservicesIDE`, EC2 instance, SSH connection |

The screenshots show the lab user email in the console header. Crop or blur it before the evidence goes anywhere public.

## Known gaps (do not hide them)

1. No screenshot of the event-service image detail page. The push output in `05-ecr-push.txt` covers it.
2. `01-environment.txt` has an empty instance type because the metadata call returned nothing. Use the EC2 list screenshot for the instance type.
3. The Git repo has no remote yet. Pushing to GitHub is up to the owner.

## Writing rules from the owner

Do not use bullet characters or em dashes in documents. Use paragraphs, numbered lists, or tables. Avoid semicolons, and do not use a colon to explain the previous sentence.
