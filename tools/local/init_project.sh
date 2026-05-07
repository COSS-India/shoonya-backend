#!/bin/bash bash



echo 'Initializing project for local development'

docker compose -f docker-compose.local.yml down
docker compose -f docker-compose.local.yml build
docker compose -f docker-compose.local.yml up -d --remove-orphans

