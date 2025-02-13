#!/bin/bash
set -eu

source scripts/config.sh


# Ensure we're in the project root
cd "$(dirname "$0")/.."

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
    printf "${RED}❌ Error: docker is not installed.${NC}\n"
    exit 1
fi

# OpenAI Credentials
if [ ! -f .env ]; then
    read -p "Enter your OpenAI API Key: " openai_api_key
    read -p "Enter your OpenAI Organization Key: " openai_org_key

    echo "OPENAI_API_KEY=$openai_api_key" >> .env
    echo "OPENAI_ORG_KEY=$openai_org_key" >> .env
    printf "${GREEN}✅ Info: .env file created with credentials.${NC}\n"
else
    printf "${GREEN}✅ Info: .env file exists. Not creating.${NC}\n"
    source .env
fi

# Ensure docker compose down (and no existing data in `db_data_postgres`)
printf "${BLUE}🔍 Checking for running containers...${NC}\n"
if docker compose ps --quiet | grep -q .; then
    printf "${BLUE}Found running containers, stopping them...${NC}\n"
    docker compose down
    printf "${GREEN}✅ Stopped running containers${NC}\n"
else
    printf "${GREEN}✅ No running containers found${NC}\n"
fi

# Check for existing SQL files that are not artifact-evaluation.sql
if ls datasets/postgres/*.sql 2>/dev/null | grep -v "artifact-evaluation.sql" >/dev/null; then
    printf "${RED}❌ Error: Found unexpected SQL files in datasets/postgres/${NC}\n"
    printf "${RED}❌ Error: Please run ./scripts/clean-data.sh${NC}\n"
    exit 1
fi

if [ ! -f "datasets/postgres/artifact-evaluation.sql" ]; then
    printf "${BLUE}🔑 Enter artifact evaluation decryption key: ${NC}"
    read -r decrypt_key

    # Decrypt artifact evaluation SQL
    printf "${BLUE}📦 Decrypting artifact evaluation data...${NC}\n"
    if ! unzip -P "$decrypt_key" datasets/postgres/artifact-evaluation.sql.zip -d datasets/postgres/; then
        printf "${RED}❌ Error: Failed to decrypt artifact evaluation data${NC}\n"
        exit 1
    fi
    printf "${GREEN}✅ Artifact evaluation data decrypted${NC}\n"
fi

printf "${BLUE}🐳 Bringing up containers...${NC}\n"
docker compose up -d

printf "${BLUE}⏳ Waiting for services to be ready...${NC}\n"
until docker compose logs notebook 2>&1 | grep -q "Jupyter Server .* is running at:"; do
    sleep 1
done
until docker compose logs postgres 2>&1 | grep -q "database system is ready to accept connections"; do
    sleep 1
done
printf "${GREEN}✅ Services are ready${NC}\n"

# Run artifact evaluation in container
printf "${BLUE}🚀 Starting artifact evaluation...${NC}\n"

docker compose exec -it notebook /bin/bash /run-artifact-evaluation.sh

printf "${GREEN}✅ Artifact evaluation completed${NC}\n"
