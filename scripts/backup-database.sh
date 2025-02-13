#!/bin/bash
set -eu

DOCKER_COMPOSE=./docker-compose.yml
BACKUP_DIR=./backups
BACKUP_FILE=$BACKUP_DIR/dump_`date +%Y-%m-%d"_"%H_%M_%S`

POSTGRES_CONTAINER=$(docker compose ps | grep postgres | cut -d' ' -f1)
POSTGRES_USERNAME=$(cat $DOCKER_COMPOSE | grep POSTGRES_USER | tail -n1 | cut -d':' -f2 | tr -d ' ')
POSTGRES_DATABASE=$(cat $DOCKER_COMPOSE | grep POSTGRES_DB | tail -n1 | cut -d':' -f2 | tr -d ' ')

if [ -z "$POSTGRES_CONTAINER" ]; then
    echo "Postgres container not running!"
    exit 1
fi

if [ -z "$POSTGRES_USERNAME" ]; then
    echo "Postgres username not found."
    exit 1
fi

mkdir -p $BACKUP_DIR

docker exec -t $POSTGRES_CONTAINER pg_dump -d $POSTGRES_DATABASE -U $POSTGRES_USERNAME | gzip > $BACKUP_FILE.sql.gz
