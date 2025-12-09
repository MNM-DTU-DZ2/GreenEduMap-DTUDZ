<!--GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
Copyright (C) 2025 DTU-DZ2 Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.-->
# GreenEduMap Docker Environment

Docker Compose stack for GreenEduMap development environment.

## 🎯 Services Included

### Database Layer
- **PostgreSQL 16 + PostGIS** - Main database (port 5432)
- **Redis 7** - Cache & session storage (port 6379)
- **MongoDB 7** - Logs & blockchain data (port 27017)

### Management Tools
- **Adminer** - Database UI (port 8080)

### Application Services
- **Auth Service** - Authentication & authorization (port 8001)

## 🚀 Quick Start

### 1. Copy Environment File

```bash
cd infrastructure/docker
cp .env.example .env
```

Edit `.env` if you want to change default configurations.

### 2. Start All Services

```bash
# Start all services
docker-compose up -d

# Or start specific services
docker-compose up -d postgres redis auth-service
```

### 3. Check Status

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f auth-service

# View all logs
docker-compose logs -f
```

### 4. Access Services

- **Auth Service API**: http://localhost:8001
- **Auth Service Swagger**: http://localhost:8001/docs
- **Adminer (DB UI)**: http://localhost:8080
  - System: `PostgreSQL`
  - Server: `postgres`
  - Username: `postgres`
  - Password: `postgres`
  - Database: `greenedumap`

## 📋 Common Commands

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data!)
docker-compose down -v

# Restart a service
docker-compose restart auth-service

# Rebuild a service
docker-compose up -d --build auth-service
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f auth-service
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 auth-service
```

### Database Operations

```bash
# Access PostgreSQL CLI
docker-compose exec postgres psql -U postgres -d greenedumap

# Create database backup
docker-compose exec postgres pg_dump -U postgres greenedumap > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres greenedumap < backup.sql

# Access Redis CLI
docker-compose exec redis redis-cli

# Access MongoDB CLI
docker-compose exec mongodb mongosh
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes all data!)
docker-compose down -v

# Remove images
docker rmi $(docker images -q greenedumap*)
```

## 🏗️ Adding New Services

To add a new service (e.g., user-service):

1. Create the service directory: `modules/user-service`
2. Add Dockerfile to the service
3. Uncomment or add service in `docker-compose.yml`:

```yaml
user-service:
  build:
    context: ../../modules/user-service
    dockerfile: Dockerfile
  container_name: greenedumap-user-service
  environment:
    DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
  ports:
    - "8002:8002"
  depends_on:
    postgres:
      condition: service_healthy
  networks:
    - greenedumap-network
  restart: unless-stopped
```

4. Rebuild stack:

```bash
docker-compose up -d --build
```

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :5432  # PostgreSQL
lsof -i :8001  # Auth Service

# Kill the process or change port in .env
```

### Service Won't Start

```bash
# Check logs
docker-compose logs auth-service

# Rebuild service
docker-compose up -d --build auth-service

# Remove and recreate
docker-compose rm -f auth-service
docker-compose up -d auth-service
```

### Database Connection Issues

```bash
# Check if postgres is healthy
docker-compose ps postgres

# Wait for postgres to be ready
docker-compose up -d postgres
sleep 10
docker-compose up -d auth-service
```

### Reset Everything

```bash
# Nuclear option - removes everything
docker-compose down -v
docker system prune -a --volumes
docker-compose up -d
```

## 📁 Directory Structure

```
infrastructure/docker/
├── docker-compose.yml        # Main compose file
├── .env.example             # Environment template
├── .env                     # Your local config (gitignored)
├── init-scripts/            # Database init scripts
│   └── 01_create_tables.sql
└── README.md               # This file
```

## 🔐 Security Notes

- **Change default passwords** in production
- **Don't commit `.env`** file (already in .gitignore)
- **Use secrets** for sensitive data in production
- **Limit exposed ports** in production

## 📊 Resource Usage

Approximate memory usage:
- PostgreSQL: ~200MB
- Redis: ~50MB
- MongoDB: ~100MB
- Auth Service: ~50MB
- **Total**: ~400MB

## 🎯 Next Steps

1. ✅ Start Docker environment
2. ✅ Access Auth Service at http://localhost:8001/docs
3. ✅ Test API endpoints with Swagger UI
4. 📝 Add more services (user-service, api-gateway, etc.)
5. 🚀 Build frontend to consume APIs

## 📚 References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [PostGIS Docker Image](https://hub.docker.com/r/postgis/postgis)
- [Redis Docker Image](https://hub.docker.com/_/redis)
