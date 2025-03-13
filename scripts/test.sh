#!/bin/bash

set -e
set -x

docker compose build
docker compose down -v --remove-orphans
docker compose up -d
docker compose exec -T backend bash scripts/test.sh "$@"
docker compose down -v --remove-orphans
