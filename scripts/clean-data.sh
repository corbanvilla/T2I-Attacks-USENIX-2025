#!/bin/bash
set -eu

source scripts/config.sh

# Ensure we're in the project root
cd "$(dirname "$0")/.."

confirm() {
    read -r -p "${1:-Are you sure? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            true
            ;;
        *)
            false
            ;;
    esac
}

# Ensure docker compose down (and no existing data in `db_data_postgres`)
printf "${BLUE}🔍 Checking for running containers...${NC}\n"
if docker compose ps --quiet | grep -q .; then
    printf "${BLUE}Found running containers, stopping them...${NC}\n"
    docker compose down
    printf "${GREEN}✅ Stopped running containers${NC}\n"
else
    printf "${GREEN}✅ No running containers found${NC}\n"
fi

print_info "Starting cleanup process..."

# Clean PostgreSQL SQL files
if [ -d "datasets/postgres" ] && confirm "Delete PostgreSQL SQL files in datasets/postgres/? [y/N] "; then
    rm -f datasets/postgres/*.sql
    print_success "PostgreSQL SQL files deleted"
fi

# Clean PostgreSQL data directory
if [ -d "./db_data_postgres" ] && confirm "Delete PostgreSQL data directory? [y/N] "; then
    sudo rm -rf ./db_data_postgres
    print_success "PostgreSQL data directory deleted"
fi

print_success "Cleanup completed!"

