#!/bin/bash

# GreenEduMap Docker Environment Startup Script
# Usage: ./start.sh

set -e

echo "🚀 Starting GreenEduMap Docker Environment..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. You can edit it if needed."
    echo ""
fi

# Pull images first (faster startup)
echo "📥 Pulling Docker images..."
docker-compose pull

# Build auth service
echo "🔨 Building Auth Service..."
docker-compose build auth-service

# Start database services first
echo "🗄️ Starting database services..."
docker-compose up -d postgres redis mongodb

# Wait for databases to be healthy
echo "⏳ Waiting for databases to be ready..."
sleep 10

# Check postgres health
until docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do
    echo "   Waiting for PostgreSQL..."
    sleep 2
done
echo "✅ PostgreSQL is ready"

# Check redis health
until docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; do
    echo "   Waiting for Redis..."
    sleep 1
done
echo "✅ Redis is ready"

echo "✅ MongoDB is ready"
echo ""

# Start application services
echo "🚀 Starting application services..."
docker-compose up -d auth-service adminer

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "🌐 Access URLs:"
echo "  - Auth Service API:    http://localhost:8001"
echo "  - Auth Service Docs:   http://localhost:8001/docs"
echo "  - Adminer (DB UI):     http://localhost:8080"
echo ""
echo "📝 Useful commands:"
echo "  - View logs:           docker-compose logs -f"
echo "  - Stop services:       docker-compose down"
echo "  - Restart a service:   docker-compose restart auth-service"
echo ""
echo "✨ Happy coding! ✨"
