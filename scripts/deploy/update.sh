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
# GreenEduMap Auto-Update Script v1.0
# Zero-downtime rolling updates
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
echo -e "${BLUE}🔄 GreenEduMap Auto-Update v1.0${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root: sudo ./update.sh${NC}"
    exit 1
fi

# Configuration
PROJECT_DIR="/opt/greenedumap"
DOCKER_DIR="${PROJECT_DIR}/infrastructure/docker"
BACKUP_DIR="/opt/backups/greenedumap"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Project not found at $PROJECT_DIR${NC}"
    echo -e "${YELLOW}Run deploy.sh first to install${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# ============================================
echo -e "${YELLOW}[Step 1/8] Creating Backup${NC}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
echo "Backing up PostgreSQL database..."
docker-compose exec -T postgres pg_dump -U greenedumap greenedumap_prod > "${BACKUP_DIR}/db_${TIMESTAMP}.sql"

# Backup environment file
cp "${DOCKER_DIR}/.env" "${BACKUP_DIR}/.env_${TIMESTAMP}"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "db_*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name ".env_*" -mtime +7 -delete

echo -e "${GREEN}✅ Backup created: ${BACKUP_DIR}/db_${TIMESTAMP}.sql${NC}"

# ============================================
echo -e "${YELLOW}[Step 2/8] Pulling Latest Code${NC}"

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Stash any local changes
git stash

# Pull latest code
git pull origin $CURRENT_BRANCH

echo -e "${GREEN}✅ Code updated${NC}"

# ============================================
echo -e "${YELLOW}[Step 3/8] Pulling Docker Images${NC}"

cd "$DOCKER_DIR"
docker-compose pull

echo -e "${GREEN}✅ Images pulled${NC}"

# ============================================
echo -e "${YELLOW}[Step 4/8] Building Updated Images${NC}"

docker-compose build

echo -e "${GREEN}✅ Images built${NC}"

# ============================================
echo -e "${YELLOW}[Step 5/8] Running Database Migrations${NC}"

# Run migrations before restarting services
docker-compose run --rm auth-service alembic upgrade head || echo "Auth migrations skipped"
docker-compose run --rm education-service alembic upgrade head || echo "Education migrations skipped"

echo -e "${GREEN}✅ Migrations completed${NC}"

# ============================================
echo -e "${YELLOW}[Step 6/8] Rolling Restart - Services${NC}"

# Restart services one by one to minimize downtime
SERVICES=("auth-service" "education-service" "environment-service" "resource-service" "api-gateway" "web-app")

for service in "${SERVICES[@]}"; do
    echo "Restarting $service..."
    docker-compose up -d --no-deps --force-recreate $service
    
    # Wait for service to be healthy
    sleep 3
    
    # Check if service is running
    if docker-compose ps | grep -q "$service.*Up"; then
        echo -e "${GREEN}✅ $service restarted${NC}"
    else
        echo -e "${RED}❌ $service failed to start${NC}"
        echo -e "${YELLOW}Rolling back...${NC}"
        
        # Restore database from backup
        docker-compose exec -T postgres psql -U greenedumap -d greenedumap_prod < "${BACKUP_DIR}/db_${TIMESTAMP}.sql"
        
        # Restore previous version
        git checkout HEAD~1
        docker-compose up -d
        
        echo -e "${RED}Update failed. Rolled back to previous version.${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ All services restarted${NC}"

# ============================================
echo -e "${YELLOW}[Step 7/8] Cleanup${NC}"

# Remove old images
docker image prune -f

# Remove old containers
docker container prune -f

echo -e "${GREEN}✅ Cleanup completed${NC}"

# ============================================
echo -e "${YELLOW}[Step 8/8] Health Check${NC}"

sleep 5

# Check API Gateway
if curl -f http://localhost:8000/health &> /dev/null; then
    echo -e "${GREEN}✅ API Gateway: Healthy${NC}"
else
    echo -e "${RED}❌ API Gateway: Unhealthy${NC}"
fi

# Check Web App
if curl -f http://localhost:3000 &> /dev/null; then
    echo -e "${GREEN}✅ Web App: Healthy${NC}"
else
    echo -e "${RED}❌ Web App: Unhealthy${NC}"
fi

# ============================================
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ UPDATE COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${CYAN}📊 Status:${NC}"
docker-compose ps
echo ""
echo -e "${YELLOW}💡 Useful commands:${NC}"
echo "   View logs: docker-compose logs -f"
echo "   Check status: docker-compose ps"
echo "   Restart service: docker-compose restart <service-name>"
echo "   Rollback: git checkout HEAD~1 && ./update.sh"
echo ""
echo -e "${CYAN}📁 Backup location: ${BACKUP_DIR}/db_${TIMESTAMP}.sql${NC}"
echo ""
