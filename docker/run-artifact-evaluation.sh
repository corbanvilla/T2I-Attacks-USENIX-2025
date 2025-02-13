#!/bin/bash
set -eu

cd work

ARTIFACTS_PATH="src/artifact_evaluation"

# Define color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if [ ! -d "$ARTIFACTS_PATH" ]; then
    printf "${RED}❌ Error: Directory $ARTIFACTS_PATH does not exist${NC}\n"
    exit 1
fi

printf "${BLUE}🚀 Starting experiments...${NC}\n"
cd "${ARTIFACTS_PATH}"

# List of experiments to run
experiments=(
    "experiments/dalle2_blocklist.py"
    "experiments/dalle3_lrl.py"
    "experiments/get_moderation.py"
)

# Loop through each experiment
for experiment in "${experiments[@]}"; do
    if [ -f "$experiment" ]; then
        printf "${BLUE}📋 Running experiment: ${experiment}...${NC}\n"
        python "$experiment"
        printf "${GREEN}✅ Completed: ${experiment}${NC}\n"
    else
        printf "${RED}❌ Error: ${experiment} not found${NC}\n"
    fi
done

printf "${GREEN}✅ All experiments completed${NC}\n"
