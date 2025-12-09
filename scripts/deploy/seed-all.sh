#!/bin/bash
#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# Master Seeder Script - Seeds ALL demo data for production demo
# Run this on VPS after pulling latest code
#

set -e

echo "=========================================="
echo " GreenEduMap - Full Demo Data Seeder"
echo "=========================================="
echo ""

POSTGRES_CONTAINER="greenedumap-postgres"
POSTGRES_USER="postgres"
POSTGRES_DB="greenedumap"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}[1/6] Running FCM tokens migration...${NC}"
docker cp modules/auth-service/migrations/add_fcm_tokens.sql $POSTGRES_CONTAINER:/tmp/fcm.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/fcm.sql
echo -e "${GREEN}✓ FCM tokens table created${NC}"
echo ""

echo -e "${CYAN}[2/6] Seeding Auth Service (Users)...${NC}"
docker cp modules/auth-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/auth_seed.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/auth_seed.sql
echo -e "${GREEN}✓ Auth data seeded${NC}"
echo ""

echo -e "${CYAN}[3/6] Seeding Environment Service (AQI + Weather)...${NC}"
docker cp modules/environment-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/environment_seed.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/environment_seed.sql
echo -e "${GREEN}✓ Environment data seeded${NC}"
echo ""

echo -e "${CYAN}[4/6] Seeding Education Service (Schools + Courses)...${NC}"
docker cp modules/education-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/education_seed.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/education_seed.sql
echo -e "${GREEN}✓ Education data seeded${NC}"
echo ""

echo -e "${CYAN}[5/6] Seeding Resource Service (Zones + Resources)...${NC}"
docker cp modules/resource-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/resource_seed.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/resource_seed.sql
echo -e "${GREEN}✓ Resource data seeded${NC}"
echo ""

echo -e "${CYAN}[6/6] Verifying data...${NC}"
echo ""
echo -e "${YELLOW}Database Statistics:${NC}"

# Count records in each table
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
SELECT 
    'users' as table_name, COUNT(*) as records FROM users
UNION ALL SELECT 'schools', COUNT(*) FROM schools
UNION ALL SELECT 'green_courses', COUNT(*) FROM green_courses
UNION ALL SELECT 'green_zones', COUNT(*) FROM green_zones
UNION ALL SELECT 'green_resources', COUNT(*) FROM green_resources
UNION ALL SELECT 'recycling_centers', COUNT(*) FROM recycling_centers
UNION ALL SELECT 'air_quality', COUNT(*) FROM air_quality
UNION ALL SELECT 'weather', COUNT(*) FROM weather
UNION ALL SELECT 'fcm_tokens', COUNT(*) FROM fcm_tokens
ORDER BY table_name;
"

echo ""
echo -e "${GREEN}=========================================="
echo " Demo Data Seeding Complete!"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}Demo Login Credentials:${NC}"
echo "  Admin:     admin@greenedumap.vn / password123"
echo "  Developer: dev@greenedumap.vn / password123"
echo "  School:    school1@dtu.edu.vn / password123"
echo "  Volunteer: volunteer1@gmail.com / password123"
echo "  Citizen:   citizen1@gmail.com / password123"
echo ""
