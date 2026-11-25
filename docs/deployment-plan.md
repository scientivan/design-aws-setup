# Deployment plan

## Phase 1 (Week 12, done)

1. Cloud9 environment `MicroservicesIDE` was created as an EC2 `t3.small` instance with Amazon Linux 2023 in LabVPC, Public Subnet1, using the SSH connection type. The lab only accepts these exact settings.
2. The code was uploaded to Cloud9 and both images were built with `scripts/run-local.sh`. The base image comes from `public.ecr.aws/docker/library/python:3.12-alpine` to avoid Docker Hub pull limits.
3. Both containers run on the Docker bridge network `ticketing-net`. Port 8081 is event-service and port 8082 is ticket-service. The ports are published on the host but are not opened in the security group, so testing was done from inside the instance.
4. `scripts/test-crud.sh` passed. Create returned 201, read 200, update 200, delete 204, and read after delete 404.
5. `scripts/push-ecr.sh` created the private repositories `ticketing/event-service` and `ticketing/ticket-service` with scan on push enabled, then pushed tag `v1` of each image.

## Phase 2 (planned)

1. Replace in-memory storage with a persistent store so tickets survive container restarts. The simplest option inside this lab is a Docker volume with SQLite on the EC2 host. A managed database is a later option if the lab allows it.
2. Run the images pulled from ECR instead of locally built ones, so the EC2 host only needs `docker pull` and `docker run`.
3. Put an Application Load Balancer in front, with path routing `/events*` to event-service and `/tickets*` to ticket-service. Only the load balancer would accept public HTTP traffic.

## Phase 3 (planned, follows the lab's Phase 5 to 9)

1. Move the containers to Amazon ECS with one task definition and one service per microservice, so each can scale on its own.
2. Add a CI/CD pipeline with CodeCommit (or another Git source), CodePipeline, and CodeDeploy so a push to the repository rebuilds the image and deploys it.

## Cost and budget

The lab budget is USD 40 and cannot be reset. The main running cost is the Cloud9 `t3.small` instance, which hibernates after 30 minutes without activity. ECR storage for two images of about 18 MB each is far below USD 0.01 per month. End the lab session after each work session to stop the clock.
