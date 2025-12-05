#!/bin/bash
# ============================================
# GreenEduMap Cleanup Script
# Xóa tất cả containers, images, volumes liên quan đến greenedumap
# ============================================

# Don't exit on error - we'll handle errors manually
set +e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🧹 GreenEduMap Cleanup Script${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root: sudo ./cleanup-greenedumap.sh${NC}"
    exit 1
fi

# Confirmation
echo -e "${YELLOW}⚠️  WARNING: This will delete ALL GreenEduMap containers, images, and volumes!${NC}"
echo ""
read -p "Type 'yes' to continue, or anything else to cancel: " CONFIRM

# Trim whitespace and convert to lowercase for comparison
CONFIRM=$(echo "$CONFIRM" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}❌ Cancelled${NC}"
    exit 0
fi

echo -e "${GREEN}✅ Confirmed! Proceeding with cleanup...${NC}"

echo ""
echo -e "${YELLOW}[Step 1/5] Stopping all GreenEduMap containers...${NC}"
CONTAINERS=$(docker ps -a --filter "name=greenedumap" --format "{{.Names}}" 2>/dev/null)
if [ -n "$CONTAINERS" ]; then
    echo "$CONTAINERS" | xargs -r docker stop 2>/dev/null
    echo -e "${GREEN}✅ Containers stopped${NC}"
else
    echo -e "${GREEN}✅ No containers to stop${NC}"
fi

echo ""
echo -e "${YELLOW}[Step 2/5] Removing all GreenEduMap containers...${NC}"
CONTAINERS=$(docker ps -a --filter "name=greenedumap" --format "{{.Names}}" 2>/dev/null)
if [ -n "$CONTAINERS" ]; then
    echo "$CONTAINERS" | xargs -r docker rm -f 2>/dev/null
    echo -e "${GREEN}✅ Containers removed${NC}"
else
    echo -e "${GREEN}✅ No containers to remove${NC}"
fi

echo ""
echo -e "${YELLOW}[Step 3/5] Removing all GreenEduMap images...${NC}"
IMAGES=$(docker images --filter "reference=*greenedumap*" --format "{{.Repository}}:{{.Tag}}" 2>/dev/null)
if [ -n "$IMAGES" ]; then
    echo "$IMAGES" | xargs -r docker rmi -f 2>/dev/null
    echo -e "${GREEN}✅ GreenEduMap images removed${NC}"
else
    echo -e "${GREEN}✅ No GreenEduMap images to remove${NC}"
fi

DOCKER_IMAGES=$(docker images --filter "reference=*docker-*" --format "{{.Repository}}:{{.Tag}}" 2>/dev/null)
if [ -n "$DOCKER_IMAGES" ]; then
    echo "$DOCKER_IMAGES" | xargs -r docker rmi -f 2>/dev/null
    echo -e "${GREEN}✅ Docker build images removed${NC}"
fi

echo ""
echo -e "${YELLOW}[Step 4/5] Removing all GreenEduMap volumes...${NC}"
VOLUMES=$(docker volume ls --filter "name=greenedumap" --format "{{.Name}}" 2>/dev/null)
if [ -n "$VOLUMES" ]; then
    echo "$VOLUMES" | xargs -r docker volume rm -f 2>/dev/null
    echo -e "${GREEN}✅ Volumes removed${NC}"
else
    echo -e "${GREEN}✅ No volumes to remove${NC}"
fi

echo ""
echo -e "${YELLOW}[Step 5/5] Cleaning up unused Docker resources...${NC}"
docker system prune -f > /dev/null 2>&1
echo -e "${GREEN}✅ Cleanup complete${NC}"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✅ CLEANUP COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${CYAN}📋 Summary:${NC}"
echo "   - All GreenEduMap containers: REMOVED"
echo "   - All GreenEduMap images: REMOVED"
echo "   - All GreenEduMap volumes: REMOVED"
echo "   - Unused Docker resources: CLEANED"
echo ""
echo -e "${YELLOW}💡 You can now run deploy.sh for a fresh deployment${NC}"
echo ""

