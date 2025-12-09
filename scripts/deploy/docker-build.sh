#!/bin/bash
# GreenEduMap Docker Build Script for macOS/Linux
# Build and start services from scratch

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${CYAN}=====================================${NC}"
echo -e "${CYAN} GreenEduMap - Docker Build & Start${NC}"
echo -e "${CYAN}=====================================${NC}"
echo ""

# Get script directory and navigate
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/infrastructure/docker"
cd "$DOCKER_DIR"

# ================================
# Environment Setup
# ================================
echo -e "${YELLOW}[0/5] Setting up environment...${NC}"

# Check for environment file
ENV_FILE=".env.local"
if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo -e "${RED}WARNING: $ENV_FILE not found!${NC}"
    echo -e "${YELLOW}Creating from .env.example...${NC}"
    cp ".env.example" "$ENV_FILE"
    echo -e "${GREEN}✓ Created $ENV_FILE${NC}"
    echo -e "${GRAY}  Review and adjust settings if needed${NC}"
else
    echo -e "${GREEN}✓ Using existing $ENV_FILE${NC}"
fi

echo ""

# ================================
# 1. Build all services
# ================================
echo -e "${YELLOW}[1/5] Building all services...${NC}"
echo ""

docker-compose --env-file "$ENV_FILE" build --no-cache

echo ""
echo -e "${GREEN}[OK] All services built!${NC}"
echo ""

# ================================
# 2. Start services
# ================================
echo -e "${YELLOW}[2/5] Starting services...${NC}"
docker-compose --env-file "$ENV_FILE" up -d

echo ""
echo -e "${GREEN}[OK] Services started!${NC}"
echo ""

# Wait for services to be ready
echo -e "${CYAN}Waiting 20 seconds for services to initialize...${NC}"
sleep 20

echo ""
echo -e "${CYAN}Service Status:${NC}"
docker-compose --env-file "$ENV_FILE" ps

# Read ports from .env file
API_PORT=$(grep "^API_GATEWAY_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "4500")
RESOURCE_PORT=$(grep "^RESOURCE_SERVICE_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "4304")
EDUCATION_PORT=$(grep "^EDUCATION_SERVICE_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "4302")
OPENDATA_PORT=$(grep "^OPENDATA_SERVICE_PORT=" "$ENV_FILE" | cut -d'=' -f2 || echo "4305")

# Default values if not found
: ${API_PORT:=4500}
: ${RESOURCE_PORT:=4304}
: ${EDUCATION_PORT:=4302}
: ${OPENDATA_PORT:=4305}

echo ""
echo -e "${YELLOW}Quick Health Checks:${NC}"

# API Gateway health check
echo -n "- API Gateway (port $API_PORT): "
if curl -s -f "http://localhost:$API_PORT/health" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# Resource Service health check
echo -n "- Resource Service (port $RESOURCE_PORT): "
if curl -s -f "http://localhost:$RESOURCE_PORT/health" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# Education Service health check
echo -n "- Education Service (port $EDUCATION_PORT): "
if curl -s -f "http://localhost:$EDUCATION_PORT/health" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# OpenData Service health check
echo -n "- OpenData Service (port $OPENDATA_PORT): "
if curl -s -f "http://localhost:$OPENDATA_PORT/health" > /dev/null 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# ================================
# 3. Wait for database to be ready
# ================================
echo ""
echo -e "${YELLOW}[3/5] Preparing database...${NC}"

POSTGRES_CONTAINER="greenedumap-postgres"
POSTGRES_USER="postgres"
POSTGRES_DB="greenedumap"

# Wait for PostgreSQL to be ready
echo -e "${CYAN}Waiting for PostgreSQL to be ready...${NC}"
MAX_ATTEMPTS=30
ATTEMPT=0
PG_READY=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ] && [ $PG_READY -eq 0 ]; do
    if docker exec "$POSTGRES_CONTAINER" pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; then
        PG_READY=1
        echo -e "${GREEN}PostgreSQL is ready!${NC}"
    else
        ATTEMPT=$((ATTEMPT + 1))
        sleep 1
    fi
done

if [ $PG_READY -eq 0 ]; then
    echo -e "${RED}PostgreSQL did not become ready in time${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}INFO: Init scripts (01-04) are auto-executed by PostgreSQL on first startup${NC}"
echo -e "${GRAY}      Location: infrastructure/docker/init-scripts/${NC}"
echo ""
echo -e "${GREEN}[OK] Database initialized!${NC}"

# ================================
# 4. Seed database (optional sample data)
# ================================
echo ""
echo -e "${YELLOW}[4/5] Seeding sample data...${NC}"

# Function to execute SQL file
execute_sql_file() {
    local SERVICE_NAME="$1"
    local FILE_PATH="$2"
    
    echo ""
    echo -e "${CYAN}[$SERVICE_NAME]${NC}"
    
    if [ ! -f "$FILE_PATH" ]; then
        echo -e "${YELLOW}  WARNING: File not found, skipping...${NC}"
        return 1
    fi
    
    FILE_NAME=$(basename "$FILE_PATH")
    echo -e "${GRAY}  Loading: $FILE_NAME${NC}"
    
    # Copy file to container
    TIMESTAMP=$(date +%Y%m%d%H%M%S)
    CONTAINER_PATH="/tmp/seed_${TIMESTAMP}.sql"
    docker cp "$FILE_PATH" "${POSTGRES_CONTAINER}:${CONTAINER_PATH}" > /dev/null
    
    # Execute SQL and filter output
    RESULT=$(docker exec "$POSTGRES_CONTAINER" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$CONTAINER_PATH" 2>&1 | \
             grep -v "^NOTICE:" | grep -v "^WARNING:")
    
    # Check for errors
    if echo "$RESULT" | grep -q "ERROR:"; then
        ERROR_LINE=$(echo "$RESULT" | grep "ERROR:" | head -n 1)
        echo -e "${RED}  ERROR: $ERROR_LINE${NC}"
        return 1
    else
        echo -e "${GREEN}  SUCCESS: Data seeded${NC}"
        return 0
    fi
}

# Seed scripts
declare -a SEED_SCRIPTS=(
    "Education Service:$PROJECT_ROOT/modules/education-service/migrations/seed_data.sql"
    "Resource Service:$PROJECT_ROOT/modules/resource-service/migrations/seed_data.sql"
)

SUCCESS_COUNT=0
TOTAL_SCRIPTS=${#SEED_SCRIPTS[@]}

for script in "${SEED_SCRIPTS[@]}"; do
    IFS=':' read -r SERVICE_NAME FILE_PATH <<< "$script"
    if execute_sql_file "$SERVICE_NAME" "$FILE_PATH"; then
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    fi
done

echo ""
echo -e "${GREEN}[OK] Seeding completed! ($SUCCESS_COUNT/$TOTAL_SCRIPTS successful)${NC}"

# ================================
# 5. Display statistics
# ================================
echo ""
echo -e "${YELLOW}[5/5] Database Statistics...${NC}"

TABLES=("schools" "green_courses" "green_zones" "green_resources" "air_quality" "weather" "green_activities")

for TABLE in "${TABLES[@]}"; do
    COUNT=$(docker exec "$POSTGRES_CONTAINER" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "SELECT COUNT(*) FROM $TABLE;" 2>/dev/null | xargs)
    if [ ! -z "$COUNT" ] && [ "$COUNT" != "0" ]; then
        echo -e "${GREEN}  $TABLE : $COUNT rows${NC}"
    fi
done

echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN} Deployment Complete!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo -e "${YELLOW}View logs with:${NC}"
echo -e "${GRAY}  docker-compose logs -f SERVICE_NAME${NC}"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo -e "${GRAY}  docker-compose ps                  # View running services${NC}"
echo -e "${GRAY}  docker-compose logs -f api-gateway # Follow API gateway logs${NC}"
echo -e "${GRAY}  docker-compose down                # Stop all services${NC}"
echo -e "${GRAY}  docker-compose restart SERVICE     # Restart a service${NC}"
echo ""
