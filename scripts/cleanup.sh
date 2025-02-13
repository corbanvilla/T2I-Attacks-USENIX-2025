#!/bin/bash
set -eu

# Source the config file for message functions
source "$(dirname "$0")/config.sh"

print_info "Starting cleanup process..."

# Stop and remove containers
print_info "Stopping and removing containers..."
if docker compose down; then
    print_success "Successfully stopped and removed containers"
else
    print_error "Failed to stop and remove containers"
    exit 1
fi

# Remove Docker images
print_info "Removing Docker images..."
IMAGES=$(docker compose images -q)
if [ -n "$IMAGES" ]; then
    if docker rmi $IMAGES; then
        print_success "Successfully removed Docker images"
    else
        print_error "Failed to remove Docker images"
        exit 1
    fi
else
    print_info "No Docker images found to remove"
fi

print_success "Cleanup completed successfully!"
