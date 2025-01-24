#!/bin/bash
set -u

# Get UID/GID of the owner of the script
file_path=$(realpath "$0")
file_uid=$(stat -c "%u" "$file_path")
file_gid=$(stat -c "%g" "$file_path")

# Update docker-compose.yml with the UID and GID
sed -i "s/\${NB_UID}/$file_uid/" docker-compose.yml
sed -i "s/\${NB_GID}/$file_gid/" docker-compose.yml

# Docker dependencies
if ! command -v docker &> /dev/null
then
    echo "Error: docker is not installed."
    exit 1
fi

# OpenAI creds
if [ ! -f .env ]; then
    read -p "Enter your OpenAI API Key: " openai_api_key
    read -p "Enter your OpenAI Organization Key: " openai_org_key

    echo "OPENAI_API_KEY=$openai_api_key" >> .env
    echo "OPENAI_ORG_KEY=$openai_org_key" >> .env
    echo "Info: .env file created with OpenAI credentials."
else
    echo "Info: .env file exists. Not creating."
fi

# Check for datasets/postgres/redacted.sql, if not found, unzip
if [ ! -f datasets/postgres/redacted.sql ]; then

    # Check to make sure datasets/postgres/unredacted.sql does not exist
    if [ -f datasets/postgres/unredacted.sql ]; then
        echo "Info: datasets/postgres/unredacted.sql exists. Not unzipping datasets/postgres/redacted.sql"
        exit 1
    else
        echo "Info: Unzipping datasets/postgres/redacted.sql"
        unzip datasets/postgres/redacted.sql.zip -d datasets/postgres
    fi
else
    echo "Info: datasets/postgres/redacted.sql exists. Not unzipping."
fi

echo "Info: Setup complete."
echo "Info: Run 'docker compose up' to launch the artifact."
