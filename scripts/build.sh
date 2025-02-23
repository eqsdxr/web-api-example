#!/bin/bash

# Exit if there's an error
set -e

docker compose build
docker compose up
