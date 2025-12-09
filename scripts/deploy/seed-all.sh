#!/bin/bash
#
# GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
# Copyright (C) 2025 DTU-DZ2 Team
#
# Master Seeder Script - Seeds ALL demo data (Đà Nẵng + TP.HCM)
# Run this on VPS after pulling latest code
#
# Usage: ./seed-all.sh [--hcmc-only] [--danang-only]
#

set -e

echo "==========================================="
echo " GreenEduMap - Full Demo Data Seeder"
echo " (Đà Nẵng + TP. Hồ Chí Minh)"
echo "==========================================="
echo ""

POSTGRES_CONTAINER="greenedumap-postgres"
POSTGRES_USER="postgres"
POSTGRES_DB="greenedumap"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Parse arguments
SEED_DANANG=true
SEED_HCMC=true

if [ "$1" == "--hcmc-only" ]; then
    SEED_DANANG=false
    echo -e "${YELLOW}Mode: TP.HCM only${NC}"
elif [ "$1" == "--danang-only" ]; then
    SEED_HCMC=false
    echo -e "${YELLOW}Mode: Đà Nẵng only${NC}"
else
    echo -e "${YELLOW}Mode: Full (Đà Nẵng + TP.HCM)${NC}"
fi
echo ""

cd "$ROOT_DIR"

# ============================================
# Step 1: FCM Tokens Migration
# ============================================
echo -e "${CYAN}[1/8] Running FCM tokens migration...${NC}"
docker cp modules/auth-service/migrations/add_fcm_tokens.sql $POSTGRES_CONTAINER:/tmp/fcm.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/fcm.sql 2>/dev/null || true
echo -e "${GREEN}✓ FCM tokens table created${NC}"
echo ""

# ============================================
# Step 2: Auth Service (Users)
# ============================================
echo -e "${CYAN}[2/10] Seeding Auth Service (Users)...${NC}"
docker cp modules/auth-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/auth_seed.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/auth_seed.sql
echo -e "${GREEN}✓ Auth data seeded (10 users)${NC}"
echo ""

# ============================================
# Step 3: User Data Tables (Favorites, Contributions, Activities, Settings)
# ============================================
echo -e "${CYAN}[3/10] Creating User Data tables...${NC}"
docker cp modules/auth-service/migrations/user_data_tables.sql $POSTGRES_CONTAINER:/tmp/user_tables.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/user_tables.sql
echo -e "${GREEN}✓ User data tables created (favorites, contributions, activities, settings)${NC}"
echo ""

# ============================================
# Step 3: Resource Service - Create recycling_centers table
# ============================================
echo -e "${CYAN}[4/10] Setting up Resource Service tables...${NC}"
docker cp modules/resource-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/resource_seed.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/resource_seed.sql
echo -e "${GREEN}✓ Resource data seeded (Đà Nẵng)${NC}"
echo ""

# ============================================
# Step 4: Environment Service - Đà Nẵng
# ============================================
if [ "$SEED_DANANG" = true ]; then
    echo -e "${CYAN}[5/10] Seeding Environment Service (Đà Nẵng)...${NC}"
    docker cp modules/environment-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/environment_seed.sql
    docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/environment_seed.sql
    echo -e "${GREEN}✓ Environment data seeded (Đà Nẵng)${NC}"
else
    echo -e "${YELLOW}[5/10] Skipping Đà Nẵng environment data...${NC}"
fi
echo ""

# ============================================
# Step 5: Environment Service - TP.HCM
# ============================================
if [ "$SEED_HCMC" = true ]; then
    echo -e "${CYAN}[6/10] Seeding Environment Service (TP.HCM)...${NC}"
    if [ -f "modules/environment-service/seed_data_hcmc.sql" ]; then
        docker cp modules/environment-service/seed_data_hcmc.sql $POSTGRES_CONTAINER:/tmp/environment_hcmc.sql
        docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/environment_hcmc.sql
        echo -e "${GREEN}✓ Environment data seeded (TP.HCM - 15 zones, 10 AQI, 7 weather)${NC}"
    else
        echo -e "${YELLOW}⚠ HCMC environment seed file not found, skipping...${NC}"
    fi
else
    echo -e "${YELLOW}[6/10] Skipping TP.HCM environment data...${NC}"
fi
echo ""

# ============================================
# Step 6: Education Service - Đà Nẵng
# ============================================
if [ "$SEED_DANANG" = true ]; then
    echo -e "${CYAN}[7/10] Seeding Education Service (Đà Nẵng)...${NC}"
    docker cp modules/education-service/migrations/seed_data.sql $POSTGRES_CONTAINER:/tmp/education_seed.sql
    docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/education_seed.sql
    echo -e "${GREEN}✓ Education data seeded (Đà Nẵng - 5 schools)${NC}"
else
    echo -e "${YELLOW}[7/10] Skipping Đà Nẵng education data...${NC}"
fi
echo ""

# ============================================
# Step 7: Education Service - TP.HCM
# ============================================
if [ "$SEED_HCMC" = true ]; then
    echo -e "${CYAN}[8/10] Seeding Education Service (TP.HCM)...${NC}"
    if [ -f "modules/education-service/migrations/seed_data_hcmc.sql" ]; then
        docker cp modules/education-service/migrations/seed_data_hcmc.sql $POSTGRES_CONTAINER:/tmp/education_hcmc.sql
        docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/education_hcmc.sql
        echo -e "${GREEN}✓ Education data seeded (TP.HCM - 21 schools, 5 courses)${NC}"
    else
        echo -e "${YELLOW}⚠ HCMC education seed file not found, skipping...${NC}"
    fi
else
    echo -e "${YELLOW}[8/10] Skipping TP.HCM education data...${NC}"
fi
echo ""

# ============================================
# Step 9: Seed User-Specific Data
# ============================================
echo -e "${CYAN}[9/10] Seeding User-Specific Data (favorites, contributions, activities)...${NC}"
docker cp modules/auth-service/migrations/seed_user_data.sql $POSTGRES_CONTAINER:/tmp/user_data.sql
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/user_data.sql
echo -e "${GREEN}✓ User data seeded (favorites, contributions, activities, settings)${NC}"
echo ""

# ============================================
# Step 10: Verify Data
# ============================================
echo -e "${CYAN}[10/10] Verifying data...${NC}"
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
UNION ALL SELECT 'user_favorites', COUNT(*) FROM user_favorites
UNION ALL SELECT 'user_contributions', COUNT(*) FROM user_contributions
UNION ALL SELECT 'user_activities', COUNT(*) FROM user_activities
UNION ALL SELECT 'user_settings', COUNT(*) FROM user_settings
ORDER BY table_name;
"

# Show cities distribution
echo ""
echo -e "${YELLOW}Schools by City:${NC}"
docker exec $POSTGRES_CONTAINER psql -U $POSTGRES_USER -d $POSTGRES_DB -c "
SELECT city, COUNT(*) as count FROM schools GROUP BY city ORDER BY count DESC;
"

echo ""
echo -e "${GREEN}==========================================="
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
echo -e "${YELLOW}Available Seed Options:${NC}"
echo "  ./seed-all.sh              # Seed all data (Đà Nẵng + TP.HCM)"
echo "  ./seed-all.sh --hcmc-only  # Seed TP.HCM data only"
echo "  ./seed-all.sh --danang-only # Seed Đà Nẵng data only"
echo ""
