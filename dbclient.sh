#!/bin/bash
set -eu

DOCKER_COMPOSE=./docker-compose.yml

POSTGRES_CONTAINER=$(docker compose ps | grep postgres | cut -d' ' -f1)
POSTGRES_USERNAME=$(cat $DOCKER_COMPOSE | grep POSTGRES_USER | cut -d':' -f2 | tr -d ' ')
POSTGRES_DATABASE=$(cat $DOCKER_COMPOSE | grep POSTGRES_DB | cut -d':' -f2 | tr -d ' ')

if [ -z "$POSTGRES_CONTAINER" ]; then
    echo "Postgres container not running!"
    exit 1
fi

if [ -z "$POSTGRES_USERNAME" ]; then
    echo "Postgres username not found."
    exit 1
fi

if [ -z "$POSTGRES_DATABASE" ]; then
    echo "Postgres database not found."
    exit 1
fi

docker exec -it $POSTGRES_CONTAINER psql -d $POSTGRES_DATABASE -U $POSTGRES_USERNAME
