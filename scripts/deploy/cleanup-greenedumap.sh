#!/bin/bash
# ============================================
# GreenEduMap Cleanup Script
# Xóa tất cả containers, images, volumes liên quan đến greenedumap
# ============================================

set -e

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
read -p "Are you sure? Type 'yes' to continue: " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}❌ Cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}[Step 1/5] Stopping all GreenEduMap containers...${NC}"
docker ps -a --filter "name=greenedumap" --format "{{.Names}}" | xargs -r docker stop
echo -e "${GREEN}✅ Containers stopped${NC}"

echo ""
echo -e "${YELLOW}[Step 2/5] Removing all GreenEduMap containers...${NC}"
docker ps -a --filter "name=greenedumap" --format "{{.Names}}" | xargs -r docker rm -f
echo -e "${GREEN}✅ Containers removed${NC}"

echo ""
echo -e "${YELLOW}[Step 3/5] Removing all GreenEduMap images...${NC}"
docker images --filter "reference=*greenedumap*" --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f
docker images --filter "reference=*docker-*" --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f
echo -e "${GREEN}✅ Images removed${NC}"

echo ""
echo -e "${YELLOW}[Step 4/5] Removing all GreenEduMap volumes...${NC}"
docker volume ls --filter "name=greenedumap" --format "{{.Name}}" | xargs -r docker volume rm -f
echo -e "${GREEN}✅ Volumes removed${NC}"

echo ""
echo -e "${YELLOW}[Step 5/5] Cleaning up unused Docker resources...${NC}"
docker system prune -f
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

