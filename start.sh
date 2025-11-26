#!/bin/bash

# GreenEduMap Quick Start Script
# This script sets up and runs the entire GreenEduMap application

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🌿 GreenEduMap - Smart City Environmental Platform 🌿   ║"
echo "║              Quick Start Setup Script                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker is not installed!${NC}"
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose is not installed!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker & Docker Compose detected${NC}\n"

# Create environment files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo -e "${BLUE}📝 Creating backend .env file...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ backend/.env created${NC}"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo -e "${BLUE}📝 Creating frontend .env.local file...${NC}"
    cat > frontend/.env.local << 'FRONTEND_ENV'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=GreenEduMap
FRONTEND_ENV
    echo -e "${GREEN}✓ frontend/.env.local created${NC}"
fi

# Start Docker Compose
echo -e "\n${BLUE}🐳 Starting Docker containers...${NC}"
echo -e "${YELLOW}This may take a few minutes on first run...${NC}\n"

cd docker
docker-compose up --build -d

# Wait for services to be ready
echo -e "\n${BLUE}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check if services are running
if docker-compose ps | grep -q "greenedumap_postgres"; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL not ready yet${NC}"
fi

if docker-compose ps | grep -q "greenedumap_backend"; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${YELLOW}⚠️  Backend not ready yet${NC}"
fi

if docker-compose ps | grep -q "greenedumap_frontend"; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend not ready yet${NC}"
fi

cd ..

# Print access URLs
echo -e "\n${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ GreenEduMap is starting up!${NC}\n"
echo -e "${YELLOW}📱 Frontend:${NC}        ${BLUE}http://localhost:3000${NC}"
echo -e "${YELLOW}🔌 Backend API:${NC}      ${BLUE}http://localhost:8000${NC}"
echo -e "${YELLOW}📚 API Docs:${NC}         ${BLUE}http://localhost:8000/docs${NC}"
echo -e "${YELLOW}📘 ReDoc:${NC}           ${BLUE}http://localhost:8000/redoc${NC}"
echo -e "${YELLOW}🗄️  Database:${NC}        ${BLUE}postgresql://postgres:password@localhost:5432/greenedumap${NC}"
echo -e "\n${BLUE}════════════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}💡 Tips:${NC}"
echo "   • Check logs: docker-compose logs -f"
echo "   • Restart: docker-compose restart"
echo "   • Stop: docker-compose down"
echo "   • View docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${GREEN}🎉 Happy coding! 🌱${NC}\n"

# Optionally open browser
read -p "Open browser tabs? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v open &> /dev/null; then
        # macOS
        open http://localhost:3000
        open http://localhost:8000/docs
    elif command -v xdg-open &> /dev/null; then
        # Linux
        xdg-open http://localhost:3000
        xdg-open http://localhost:8000/docs
    elif command -v start &> /dev/null; then
        # Windows
        start http://localhost:3000
        start http://localhost:8000/docs
    fi
fi

echo -e "${GREEN}✅ Setup complete!${NC}\n"
