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
# 🐳 Docker Setup Guide

Quick guide to run GreenEduMap with Docker.

---

## 📋 Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+
- Git

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ.git
cd GreenEduMap-DTUDZ
```

### 2. Configure Environment

```bash
cd infrastructure/docker
cp .env.example .env
# Edit .env with your configurations
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Verify

```bash
docker-compose ps
```

All services should be `healthy`.

---

## 🔧 Available Services

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL (PostGIS) | 5432 | Main database |
| Redis | 6379 | Cache |
| MongoDB | 27017 | Document store |
| Adminer | 8080 | DB admin UI |
| API Gateway | 8000 | Main API |
| Auth Service | 8001 | Authentication |
| Environment Service | 8002 | Weather/Air Quality |

---

## 📝 Common Commands

### Start all services
```bash
docker-compose up -d
```

### Stop all services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f [service-name]
```

### Rebuild service
```bash
docker-compose up -d --build [service-name]
```

### Reset all data
```bash
docker-compose down -v
docker-compose up -d
```

---

## 🐛 Troubleshooting

### Service won't start

```bash
docker-compose logs [service-name]
```

### Database connection issues

Check `.env` file configuration:
```
DB_HOST=postgres
DB_PORT=5432
DB_USER=greenedumap
DB_PASSWORD=your_password
```

### Port conflicts

Edit `docker-compose.yml` to change port mappings.

---

## 📚 See Also

- [Development Workflow](DEVELOPMENT_WORKFLOW.md)
- [Project Context](PROJECT_CONTEXT.md)
