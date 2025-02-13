#!/bin/bash
set -u

# Check for datasets/postgres/redacted.sql or datasets/postgres/unredacted.sql
if [ -f datasets/postgres/redacted.sql ]; then
    echo "Error: datasets/postgres/redacted.sql already exists. Please remove it before proceeding."
    exit 1
fi
if [ -f datasets/postgres/unredacted.sql ]; then
    echo "Error: datasets/postgres/unredacted.sql already exists. Please remove it before proceeding."
    exit 1
fi

# Ask for decryption key
read -p "Have you been provided a decryption key? (y/N): " has_decryption_key

if [ "$has_decryption_key" == "y" ]; then
    read -p "Enter your decryption key: " decryption_key

    # Decrypt database
    unzip -P "$decryption_key" datasets/postgres/unredacted.sql.zip -d datasets/postgres/
    if [ $? -ne 0 ]; then
        echo "Error: Failed to unzip the file. Please check your decryption key."
        exit 1
    fi

    # Decrypt redacted prompts
    unzip -P "$decryption_key" datasets/prompts/toxic.zip -d datasets/prompts/

else
    echo "Error: Decryption key is required to proceed."
    exit 1
fi

echo "Info: Artifact decryption complete."
