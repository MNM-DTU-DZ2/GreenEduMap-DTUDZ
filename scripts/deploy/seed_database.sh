#!/bin/bash
#!/bin/bash
#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

# ============================================
# GreenEduMap Database Seeder (Linux/Bash)
# Seed sample data after deployment
# ============================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🌱 GreenEduMap Database Seeder${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  Running without root, some commands may need sudo${NC}"
fi

# Configuration
PROJECT_DIR="/opt/greenedumap"
DOCKER_DIR="${PROJECT_DIR}/infrastructure/docker"
POSTGRES_CONTAINER="greenedumap-postgres"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_DB="${POSTGRES_DB:-greenedumap}"

# Check if PostgreSQL container is running
echo -e "${YELLOW}[Step 1/4] Checking PostgreSQL container...${NC}"
if ! docker ps --filter "name=${POSTGRES_CONTAINER}" --format "{{.Names}}" | grep -q "${POSTGRES_CONTAINER}"; then
    echo -e "${RED}❌ PostgreSQL container is not running${NC}"
    echo -e "${YELLOW}   Run: cd ${DOCKER_DIR} && docker-compose up -d postgres${NC}"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL container is running${NC}"

# Wait for PostgreSQL to be ready
echo -e "${YELLOW}[Step 2/4] Waiting for PostgreSQL to be ready...${NC}"
for i in {1..30}; do
    if docker exec ${POSTGRES_CONTAINER} pg_isready -U "${POSTGRES_USER}" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ PostgreSQL did not become ready in time${NC}"
        exit 1
    fi
    sleep 1
done

# Function to execute SQL file
execute_sql_file() {
    local service_name=$1
    local file_path=$2
    
    echo ""
    echo -e "${CYAN}[${service_name}]${NC}"
    
    if [ ! -f "$file_path" ]; then
        echo -e "${YELLOW}⚠️  File not found: ${file_path}${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}   Loading: ${file_path}${NC}"
    
    # Copy file to container and execute
    local container_path="/tmp/seed_$(date +%s).sql"
    docker cp "$file_path" ${POSTGRES_CONTAINER}:${container_path} > /dev/null 2>&1
    
    # Execute SQL (suppress NOTICE messages)
    local result=$(docker exec ${POSTGRES_CONTAINER} psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -f ${container_path} 2>&1 | grep -v "NOTICE:" | grep -v "WARNING:" || true)
    
    # Check for errors
    if echo "$result" | grep -q "ERROR:"; then
        echo -e "${RED}   ❌ Error: $(echo "$result" | grep "ERROR:")${NC}"
        return 1
    else
        echo -e "${GREEN}   ✅ Successfully seeded${NC}"
        return 0
    fi
}

# Seed files
echo -e "${YELLOW}[Step 3/5] Running init scripts (create tables)...${NC}"

# Init scripts (create tables first)
init_files=(
    "${PROJECT_DIR}/infrastructure/docker/init-scripts/01-init-postgis.sql:PostGIS Extension"
    "${PROJECT_DIR}/infrastructure/docker/init-scripts/02-create-tables.sql:Core Tables"
    "${PROJECT_DIR}/infrastructure/docker/init-scripts/03_education_schema.sql:Education Schema"
    "${PROJECT_DIR}/infrastructure/docker/init-scripts/04_green_zones.sql:Green Zones Tables"
)

for init_entry in "${init_files[@]}"; do
    IFS=':' read -r file_path service_name <<< "$init_entry"
    execute_sql_file "$service_name" "$file_path" || true
done

echo -e "${YELLOW}[Step 4/5] Seeding sample data...${NC}"

seed_files=(
    "${PROJECT_DIR}/modules/education-service/migrations/seed_data.sql:Education Service"
    "${PROJECT_DIR}/modules/resource-service/migrations/seed_data.sql:Resource Service"
    "${PROJECT_DIR}/modules/environment-service/seed_data.sql:Environment Service"
    "${PROJECT_DIR}/modules/environment-service/seed_data_historical.sql:Environment Service (Historical)"
)

success_count=0
total_count=${#seed_files[@]}

for seed_entry in "${seed_files[@]}"; do
    IFS=':' read -r file_path service_name <<< "$seed_entry"
    if execute_sql_file "$service_name" "$file_path"; then
        ((success_count++))
    fi
done

# Display statistics
echo ""
echo -e "${YELLOW}[Step 4/4] Data Statistics...${NC}"

tables=("schools" "green_courses" "green_zones" "green_resources" "air_quality" "weather" "green_activities")

for table in "${tables[@]}"; do
    count=$(docker exec ${POSTGRES_CONTAINER} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -t -c "SELECT COUNT(*) FROM ${table};" 2>/dev/null | tr -d ' ' || echo "0")
    if [ "$count" != "0" ] && [ -n "$count" ]; then
        echo -e "${GREEN}   ${table}: ${count} rows${NC}"
    fi
done

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ SEEDING COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo -e "${CYAN}   Services seeded: ${success_count}/${total_count}${NC}"
echo ""
echo -e "${YELLOW}💡 You can now test the API endpoints${NC}"
echo ""

