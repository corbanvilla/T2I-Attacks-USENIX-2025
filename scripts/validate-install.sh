#!/bin/bash

# Source the config file for colored output
source "$(dirname "$0")/config.sh"

# Check if unzip is installed
if ! command -v unzip &> /dev/null; then
    print_error "unzip is not installed"
    read -p "Would you like to install unzip? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installing unzip..."
        sudo apt update
        sudo apt install -y unzip
        if [ $? -ne 0 ]; then
            print_error "Failed to install unzip"
            exit 1
        fi
        print_success "unzip installed successfully"
    else
        print_error "unzip is required but installation was declined"
        exit 1
    fi
fi
print_success "unzip is installed"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi
print_success "Docker is installed"

# Check if docker can be run without sudo
if ! docker ps &> /dev/null; then
    print_error "Cannot run 'docker ps'. Please ensure:"
    print_error "1. Docker daemon is running"
    print_error "2. Your user is in the docker group (run 'sudo usermod -aG docker \$USER' and log out/in)"
    exit 1
fi
print_success "Docker permissions are properly configured"

# Check if we're in the project root (look for docker-compose.yml)
if [ ! -f "./docker-compose.yml" ]; then
    print_error "docker-compose.yml not found. Please run this script from the project root directory."
    exit 1
fi
print_success "Project root directory verified"

# Run docker compose build
print_info "Running docker compose build..."
if ! docker compose build; then
    print_error "Docker compose build failed"
    exit 1
fi
print_success "Docker compose build completed successfully"

print_success "All validation checks passed!"
