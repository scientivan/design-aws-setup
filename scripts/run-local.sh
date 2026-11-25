#!/usr/bin/env bash
# Bangun dan jalankan kedua container pada satu jaringan di Cloud9 atau host Docker lain.
set -euo pipefail
cd "$(dirname "$0")/.."
docker build -t event-service ./services/event-service
docker build -t ticket-service ./services/ticket-service
docker network inspect ticketing-net >/dev/null 2>&1 || docker network create ticketing-net
docker rm -f event-service ticket-service >/dev/null 2>&1 || true
docker run -d --name event-service --network ticketing-net -p 8081:8081 event-service
docker run -d --name ticket-service --network ticketing-net -p 8082:8082 \
  -e EVENT_SERVICE_URL=http://event-service:8081 ticket-service
sleep 2
docker ps --filter name=-service --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
