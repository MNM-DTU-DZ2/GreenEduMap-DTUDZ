#!/bin/bash
# ==============================================
# GreenEduMap VPS Deployment Script
# ==============================================
# This script deploys GreenEduMap on VPS (Ubuntu)

set -e  # Exit on any error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} GreenEduMap - VPS Deployment${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# Navigate to docker directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCKER_DIR="$PROJECT_ROOT/infrastructure/docker"
cd "$DOCKER_DIR"

# ===========================================
# 0. Environment Setup
# ===========================================
echo -e "${YELLOW}[0/6] Setting up environment...${NC}"

# Check for environment file
ENV_FILE=".env.production"
if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo -e "${RED}ERROR: $ENV_FILE not found!${NC}"
    echo -e "${YELLOW}Creating from .env.example...${NC}"
    cp .env.example "$ENV_FILE"
    echo -e "${GREEN}✓ Created $ENV_FILE${NC}"
    echo ""
    echo -e "${RED}⚠️  IMPORTANT: You MUST edit $ENV_FILE before continuing!${NC}"
    echo -e "${YELLOW}Required changes:${NC}"
    echo "  1. Set POSTGRES_PASSWORD to a strong password"
    echo "  2. Generate JWT_SECRET_KEY: openssl rand -base64 64"
    echo "  3. Update NEXT_PUBLIC_API_URL with your domain"
    echo "  4. Update CORS_ORIGINS with your domains"
    echo "  5. Set DEBUG=false"
    echo "  6. Set NODE_ENV=production"
    echo ""
    echo -e "${CYAN}Press Enter after you've edited $ENV_FILE...${NC}"
    read
fi

echo -e "${GREEN}✓ Using $ENV_FILE${NC}"
echo ""

# ===========================================
# 1. Check Prerequisites
# ===========================================
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}ERROR: Docker Compose is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed${NC}"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  Not running as root. Make sure your user is in the docker group.${NC}"
fi

echo ""

# ===========================================
# 2. Pull Latest Code (optional)
# ===========================================
echo -e "${YELLOW}[2/6] Checking for updates...${NC}"
if [ -d "$PROJECT_ROOT/.git" ]; then
    echo "Git repository detected. Pull latest changes? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        git pull
        echo -e "${GREEN}✓ Code updated${NC}"
    fi
else
    echo -e "${YELLOW}Not a git repository, skipping...${NC}"
fi
echo ""

# ===========================================
# 3. Build Services
# ===========================================
echo -e "${YELLOW}[3/6] Building services...${NC}"
docker-compose --env-file "$ENV_FILE" build --no-cache

echo ""
echo -e "${GREEN}[OK] All services built!${NC}"
echo ""

# ===========================================
# 4. Start Services
# ===========================================
echo -e "${YELLOW}[4/6] Starting services...${NC}"
docker-compose --env-file "$ENV_FILE" up -d

echo ""
echo -e "${GREEN}[OK] Services started!${NC}"
echo ""

# Wait for services
echo "Waiting 30 seconds for services to initialize..."
sleep 30

echo ""
echo -e "${CYAN}Service Status:${NC}"
docker-compose --env-file "$ENV_FILE" ps

# Read ports from env file
API_PORT=$(grep "^API_GATEWAY_PORT=" "$ENV_FILE" | cut -d'=' -f2)
RESOURCE_PORT=$(grep "^RESOURCE_SERVICE_PORT=" "$ENV_FILE" | cut -d'=' -f2)
EDUCATION_PORT=$(grep "^EDUCATION_SERVICE_PORT=" "$ENV_FILE" | cut -d'=' -f2)
OPENDATA_PORT=$(grep "^OPENDATA_SERVICE_PORT=" "$ENV_FILE" | cut -d'=' -f2)
WEB_PORT=$(grep "^WEB_APP_PORT=" "$ENV_FILE" | cut -d'=' -f2)

: ${API_PORT:=4500}
: ${RESOURCE_PORT:=4304}
: ${EDUCATION_PORT:=4302}
: ${OPENDATA_PORT:=4305}
: ${WEB_PORT:=4501}

echo ""
echo -e "${YELLOW}Health Checks:${NC}"

# API Gateway
echo -n "- API Gateway (port $API_PORT): "
if curl -f -s "http://localhost:$API_PORT/health" > /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# Resource Service
echo -n "- Resource Service (port $RESOURCE_PORT): "
if curl -f -s "http://localhost:$RESOURCE_PORT/health" > /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# Education Service
echo -n "- Education Service (port $EDUCATION_PORT): "
if curl -f -s "http://localhost:$EDUCATION_PORT/health" > /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# OpenData Service
echo -n "- OpenData Service (port $OPENDATA_PORT): "
if curl -f -s "http://localhost:$OPENDATA_PORT/health" > /dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
fi

# ===========================================
# 5. Initialize Database
# ===========================================
echo ""
echo -e "${YELLOW}[5/6] Initializing database...${NC}"

POSTGRES_CONTAINER="greenedumap-postgres"
POSTGRES_USER="postgres"
POSTGRES_DB="greenedumap"

# Wait for PostgreSQL
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker exec "$POSTGRES_CONTAINER" pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; then
        echo -e "${GREEN}PostgreSQL is ready!${NC}"
        break
    fi
    sleep 1
done

echo ""
echo -e "${CYAN}INFO: Init scripts (01-04) are auto-executed by PostgreSQL on first startup${NC}"
echo -e "      Location: infrastructure/docker/init-scripts/"
echo ""
echo -e "${GREEN}[OK] Database initialized!${NC}"

# ===========================================
# 6. Seed Database
# ===========================================
echo ""
echo -e "${YELLOW}[6/6] Seeding sample data...${NC}"

# Function to execute SQL file
seed_sql() {
    local service_name="$1"
    local sql_file="$2"
    
    echo ""
    echo -e "${CYAN}[$service_name]${NC}"
    
    if [ ! -f "$sql_file" ]; then
        echo -e "  ${YELLOW}WARNING: File not found, skipping...${NC}"
        return 1
    fi
    
    local filename=$(basename "$sql_file")
    echo "  Loading: $filename"
    
    # Copy file to container
    local timestamp=$(date +%Y%m%d%H%M%S)
    local container_path="/tmp/seed_$timestamp.sql"
    docker cp "$sql_file" "${POSTGRES_CONTAINER}:${container_path}" > /dev/null
    
    # Execute SQL
    if docker exec "$POSTGRES_CONTAINER" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$container_path" 2>&1 | grep -q "ERROR:"; then
        echo -e "  ${RED}ERROR: Failed to seed data${NC}"
        return 1
    else
        echo -e "  ${GREEN}SUCCESS: Data seeded${NC}"
        return 0
    fi
}

# Seed scripts
success_count=0
total_count=0

# Education Service
total_count=$((total_count + 1))
if seed_sql "Education Service" "$PROJECT_ROOT/modules/education-service/migrations/seed_data.sql"; then
    success_count=$((success_count + 1))
fi

# Resource Service
total_count=$((total_count + 1))
if seed_sql "Resource Service" "$PROJECT_ROOT/modules/resource-service/migrations/seed_data.sql"; then
    success_count=$((success_count + 1))
fi

echo ""
echo -e "${GREEN}[OK] Seeding completed! ($success_count/$total_count successful)${NC}"

# ===========================================
# Summary
# ===========================================
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} Deployment Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${CYAN}Access your services:${NC}"
echo "  API Gateway:    http://YOUR_SERVER_IP:$API_PORT"
echo "  Web App:        http://YOUR_SERVER_IP:$WEB_PORT"
echo "  Adminer (DB):   http://YOUR_SERVER_IP:4600"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Configure nginx reverse proxy"
echo "  2. Set up SSL certificates (Let's Encrypt)"
echo "  3. Point your domain to this server"
echo "  4. Update CORS_ORIGINS in $ENV_FILE if needed"
echo ""
echo -e "${CYAN}View logs with:${NC}"
echo "  docker-compose --env-file $ENV_FILE logs -f [SERVICE_NAME]"
echo ""
