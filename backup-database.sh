#!/bin/bash
set -exu

DOCKER_COMPOSE=./docker-compose.yml
BACKUP_DIR=./backups
BACKUP_FILE=$BACKUP_DIR/dump_`date +%Y-%m-%d"_"%H_%M_%S`

POSTGRES_CONTAINER=$(docker ps | grep postgres | cut -d' ' -f1)
POSTGRES_USERNAME=$(cat $DOCKER_COMPOSE | grep POSTGRES_USER | cut -d':' -f2 | tr -d ' ')
POSTGRES_PASSWORD=$(cat $DOCKER_COMPOSE | grep POSTGRES_PASSWORD | cut -d':' -f2 | tr -d ' ')

if [ -z "$POSTGRES_CONTAINER" ]; then
    echo "Postgres container not found."
    exit 1
fi

if [ -z "$POSTGRES_USERNAME" ]; then
    echo "Postgres username not found."
    exit 1
fi

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Postgres password not found."
    exit 1
fi

mkdir -p $BACKUP_DIR

# Dump database
export PGPASSWORD=$POSTGRES_PASSWORD
# docker exec -t $POSTGRES_CONTAINER pg_dump --data-only -d t2i-attacks -U $POSTGRES_USERNAME | gzip > $BACKUP_FILE.sql.gz
docker exec -t $POSTGRES_CONTAINER pg_dump -d t2i-attacks -U $POSTGRES_USERNAME | gzip > $BACKUP_FILE.sql.gz
# docker exec -t $POSTGRES_CONTAINER pg_dumpall -c -U $POSTGRES_USERNAME | gzip > $BACKUP_FILE.sql.gz
unset PGPASSWORD