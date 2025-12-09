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
# Build Without Docker

Hướng dẫn cài đặt và chạy GreenEduMap **KHÔNG sử dụng Docker** (bare metal).

---

## Yêu Cầu Hệ Thống

### Phần Mềm Bắt Buộc
- **Node.js** >= 20.x
- **npm** hoặc **yarn** >= 1.22
- **Python** >= 3.11
- **pip** >= 23.0
- **PostgreSQL** >= 16
- **PostGIS** >= 3.4
- **Redis** >= 7.0
- **MongoDB** >= 7.0

### Optional Services
- **RabbitMQ** >= 3.13 (cho message broker)
- **EMQX** >= 5.5 (MQTT broker)

---

## 1. Cài Đặt Dependencies

### Ubuntu/Debian

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Python 3.11+
sudo apt install python3.11 python3-pip python3-venv python3.11-dev

# PostgreSQL 16 + PostGIS
sudo apt install postgresql-16 postgresql-16-postgis-3 postgresql-contrib

# Redis
sudo apt install redis-server

# MongoDB 7
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org

# RabbitMQ (Optional)
sudo apt install rabbitmq-server

# Build essentials for Python packages
sudo apt install build-essential libpq-dev python3-dev
```

### macOS

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install all services
brew install node@20 python@3.11 postgresql@16 postgis redis mongodb-community rabbitmq

# Start services
brew services start postgresql@16
brew services start redis
brew services start mongodb-community
brew services start rabbitmq
```

### Windows

**Sử dụng Chocolatey:**

```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install packages
choco install nodejs-lts python311 postgresql16 redis-64 mongodb rabbitmq -y
```

**Hoặc tải trực tiếp:**
- Node.js: https://nodejs.org/
- Python: https://www.python.org/downloads/
- PostgreSQL: https://www.postgresql.org/download/windows/
- Redis: https://github.com/microsoftarchive/redis/releases
- MongoDB: https://www.mongodb.com/try/download/community
- RabbitMQ: https://www.rabbitmq.com/download.html

---

## 2. Cấu Hình Database

### PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Create database và user
sudo -u postgres psql <<EOF
CREATE DATABASE greenedumap;
CREATE USER greenedumap_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE greenedumap TO greenedumap_user;

-- Enable PostGIS và UUID
\c greenedumap
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO greenedumap_user;
EOF
```

**Verify PostGIS:**
```bash
psql -U greenedumap_user -d greenedumap -c "SELECT PostGIS_version();"
```

### Redis

```bash
# Start Redis
sudo systemctl start redis

# Test connection
redis-cli ping
# Expected: PONG
```

### MongoDB

```bash
# Start MongoDB
sudo systemctl start mongod

# Create database (tự động tạo khi insert data đầu tiên)
mongosh <<EOF
use greenedumap
db.createCollection("test")
EOF
```

---

## 3. Backend Services (FastAPI)

Tất cả backend services đều sử dụng FastAPI và Python 3.11+

### 3.1. Auth Service

```bash
cd modules/auth-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env
```

**Cấu hình .env:**
```env
# Database
DATABASE_URL=postgresql+asyncpg://greenedumap_user:your_secure_password@localhost:5432/greenedumap

# JWT
SECRET_KEY=your-super-secret-jwt-key-min-32-chars-recommended-64-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
DEBUG=false
HOST=0.0.0.0
PORT=8001

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**Run migrations:**
```bash
# Migrate database
alembic upgrade head

# Create default admin user (if seed script exists)
python -m app.db.init_db
```

**Start service:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

### 3.2. API Gateway

```bash
cd modules/api-gateway

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env
```

**.env:**
```env
# Service URLs
AUTH_SERVICE_URL=http://localhost:8001
RESOURCE_SERVICE_URL=http://localhost:8002
ENVIRONMENT_SERVICE_URL=http://localhost:8007
EDUCATION_SERVICE_URL=http://localhost:8003
OPENDATA_SERVICE_URL=http://localhost:8009

# Redis
REDIS_URL=redis://localhost:6379/0

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# App
HOST=0.0.0.0
PORT=8000
DEBUG=false
CORS_ORIGINS=["http://localhost:3000","*"]
```

**Run:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### 3.3. Resource Service

```bash
cd modules/resource-service

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

**.env:**
```env
DATABASE_URL=postgresql+asyncpg://greenedumap_user:your_secure_password@localhost:5432/greenedumap
HOST=0.0.0.0
PORT=8002
DEBUG=false
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**Migrate & Run:**
```bash
# Migrate
alembic upgrade head

# Start
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

---

### 3.4. Education Service

```bash
cd modules/education-service

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

**.env:**
```env
DATABASE_URL=postgresql+asyncpg://greenedumap_user:your_secure_password@localhost:5432/greenedumap
HOST=0.0.0.0
PORT=8003
DEBUG=false
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**Run:**
```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

---

### 3.5. Environment Service

```bash
cd modules/environment-service

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

**.env:**
```env
DATABASE_URL=postgresql+asyncpg://greenedumap_user:your_secure_password@localhost:5432/greenedumap

# External APIs
OPENAQ_API_URL=https://api.openaq.org/v2
OPENWEATHER_API_KEY=your_openweather_api_key
OPENWEATHER_API_URL=https://api.openweathermap.org/data/2.5

# Scheduler intervals (seconds)
FETCH_AIR_QUALITY_INTERVAL=3600
FETCH_WEATHER_INTERVAL=1800

# Message Brokers
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_CLIENT_ID=environment-service

# App
HOST=0.0.0.0
PORT=8007
DEBUG=false
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**Run:**
```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8007 --reload
```

---

### 3.6. OpenData Service (NGSI-LD)

```bash
cd modules/opendata-service

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

**.env:**
```env
DATABASE_URL=postgresql+asyncpg://greenedumap_user:your_secure_password@localhost:5432/greenedumap
BASE_URL=http://localhost:8009
DATA_BASE_URI=http://greenedumap.vn/data
DEBUG=false
API_V1_STR=/api/v1
MAX_PAGE_SIZE=1000
DEFAULT_PAGE_SIZE=100
```

**Run:**
```bash
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8009 --reload
```

---

### 3.7. AI Service (Background Worker)

```bash
cd modules/ai-service

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

**.env:**
```env
DATABASE_URL=postgresql+asyncpg://greenedumap_user:your_secure_password@localhost:5432/greenedumap
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
DEBUG=false

# ML Settings
CLUSTERING_N_CLUSTERS=3
PREDICTION_FORECAST_DAYS=7
CORRELATION_MIN_SAMPLES=10
```

**Run:**
```bash
# AI Service runs as RabbitMQ consumer
python -m app.main
```

---

## 4. Frontend (Next.js Web App)

```bash
cd modules/web-app

# Install dependencies
npm install
# Or using yarn
yarn install

# Configure environment
cp .env.example .env.local
nano .env.local
```

**.env.local:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MAPTILER_API_KEY=your_maptiler_api_key
NEXT_PUBLIC_APP_NAME=GreenEduMap
NEXT_PUBLIC_ENABLE_AI=true
NODE_ENV=production
```

**Build & Run:**
```bash
# Development mode
npm run dev

# Production build
npm run build
npm run start
```

Truy cập: http://localhost:3000

---

## 5. Mobile App (React Native)

```bash
cd modules/appmobile

# Install dependencies
npm install
# Or
yarn install

# iOS (macOS only)
cd ios
pod install
cd ..

# Configure environment
cp .env.example .env
```

**.env:**
```env
API_URL=http://localhost:8000
MAPTILER_API_KEY=your_maptiler_api_key
```

**Run:**
```bash
# Android
npm run android

# iOS (macOS only)
npm run ios
```

---

## 6. Message Brokers (Optional)

### RabbitMQ

```bash
# Start RabbitMQ
sudo systemctl start rabbitmq-server

# Enable management plugin
sudo rabbitmq-plugins enable rabbitmq_management

# Create user and vhost
sudo rabbitmqctl add_user greenedumap greenedumap_password
sudo rabbitmqctl add_vhost greenedumap
sudo rabbitmqctl set_permissions -p greenedumap greenedumap ".*" ".*" ".*"
```

**Management UI:** http://localhost:15672 (guest/guest)

### EMQX (MQTT)

**Install:**
```bash
# Download and install EMQX
wget https://www.emqx.io/downloads/broker/v5.5.0/emqx-5.5.0-ubuntu22.04-amd64.deb
sudo dpkg -i emqx-5.5.0-ubuntu22.04-amd64.deb

# Start EMQX
sudo systemctl start emqx
```

**Dashboard:** http://localhost:18083 (admin/public)

---

## 7. Verify Services

Check all services running:

```bash
# Auth Service
curl http://localhost:8001/health

# API Gateway
curl http://localhost:8000/health

# Resource Service
curl http://localhost:8002/health

# Education Service
curl http://localhost:8003/health

# Environment Service
curl http://localhost:8007/health

# OpenData Service
curl http://localhost:8009/health

# Web App
curl http://localhost:3000

# PostgreSQL
psql -U greenedumap_user -d greenedumap -c "SELECT version();"

# Redis
redis-cli ping

# MongoDB
mongosh --eval "db.version()"
```

---

## 8. Production Deployment

### Using systemd

Tạo systemd service cho mỗi backend service:

**Auth Service:**
```bash
sudo nano /etc/systemd/system/greenedumap-auth.service
```

```ini
[Unit]
Description=GreenEduMap Auth Service
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/GreenEduMap-DTUDZ/modules/auth-service
Environment="PATH=/path/to/GreenEduMap-DTUDZ/modules/auth-service/venv/bin"
ExecStart=/path/to/GreenEduMap-DTUDZ/modules/auth-service/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable và start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable greenedumap-auth
sudo systemctl start greenedumap-auth
```

Repeat tương tự cho các services khác.

### Using PM2 (for easier management)

```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
cd /path/to/GreenEduMap-DTUDZ
nano ecosystem.config.js
```

**ecosystem.config.js:**
```javascript
module.exports = {
  apps: [
    {
      name: 'auth-service',
      cwd: './modules/auth-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8001',
      interpreter: 'none',
    },
    {
      name: 'api-gateway',
      cwd: './modules/api-gateway',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8000',
      interpreter: 'none',
    },
    {
      name: 'resource-service',
      cwd: './modules/resource-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8002',
      interpreter: 'none',
    },
    {
      name: 'education-service',
      cwd: './modules/education-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8003',
      interpreter: 'none',
    },
    {
      name: 'environment-service',
      cwd: './modules/environment-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8007',
      interpreter: 'none',
    },
    {
      name: 'opendata-service',
      cwd: './modules/opendata-service',
      script: 'venv/bin/uvicorn',
      args: 'app.main:app --host 0.0.0.0 --port 8009',
      interpreter: 'none',
    },
    {
      name: 'ai-service',
      cwd: './modules/ai-service',
      script: 'venv/bin/python',
      args: '-m app.main',
      interpreter: 'none',
    },
    {
      name: 'web-app',
      cwd: './modules/web-app',
      script: 'npm',
      args: 'start',
    },
  ],
};
```

**Start all services:**
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

**Management:**
```bash
pm2 list          # List all processes
pm2 logs          # View logs
pm2 restart all   # Restart all
pm2 stop all      # Stop all
pm2 delete all    # Delete all
```

---

## 9. Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/greenedumap
```

```nginx
upstream api_gateway {
    server localhost:8000;
}

upstream web_app {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Web App
    location / {
        proxy_pass http://web_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API Gateway
    location /api/ {
        proxy_pass http://api_gateway/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Docs
    location /docs {
        proxy_pass http://api_gateway/docs;
    }

    location /redoc {
        proxy_pass http://api_gateway/redoc;
    }
}
```

**Enable và reload:**
```bash
sudo ln -s /etc/nginx/sites-available/greenedumap /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Troubleshooting

### Python Packages Installation Error

```bash
# Install build dependencies
sudo apt install build-essential python3-dev libpq-dev

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Reinstall packages
pip install -r requirements.txt
```

### PostgreSQL Connection Error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check user and permissions
sudo -u postgres psql
\du  # List users
\l   # List databases

# Reset password
ALTER USER greenedumap_user WITH PASSWORD 'new_password';
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
kill -9 <PID>

# Or kill all Python processes
pkill -f uvicorn
```

### Redis Connection Error

```bash
# Check Redis is running
sudo systemctl status redis

# Test connection
redis-cli ping

# Check Redis config
sudo nano /etc/redis/redis.conf
# Make sure: bind 127.0.0.1 ::1
```

### MongoDB Connection Error

```bash
# Check MongoDB status
sudo systemctl status mongod

# Check logs
sudo tail -f /var/log/mongodb/mongod.log

# Restart MongoDB
sudo systemctl restart mongod
```

### RabbitMQ Connection Error

```bash
# Check RabbitMQ status
sudo systemctl status rabbitmq-server

# Check logs
sudo journalctl -u rabbitmq-server -f

# Reset user
sudo rabbitmqctl delete_user greenedumap
sudo rabbitmqctl add_user greenedumap your_password
```

---

## Performance Tuning

### PostgreSQL

```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```

```conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 128MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
max_connections = 200
```

```bash
sudo systemctl restart postgresql
```

### Redis

```bash
sudo nano /etc/redis/redis.conf
```

```conf
maxmemory 256mb
maxmemory-policy allkeys-lru
```

```bash
sudo systemctl restart redis
```

---

## Môi Trường Development

Để phát triển local, chỉ cần chạy services cần thiết:

```bash
# Minimum setup
# 1. Databases
sudo systemctl start postgresql redis

# 2. API Gateway + Auth
cd modules/api-gateway && source venv/bin/activate && uvicorn app.main:app --reload &
cd modules/auth-service && source venv/bin/activate && uvicorn app.main:app --port 8001 --reload &

# 3. Web App
cd modules/web-app && npm run dev
```

---

**Note:** Document này giả định bạn đã có kinh nghiệm quản lý Linux/Unix systems. Nếu cần hỗ trợ, tạo issue tại [GitHub Issues](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/issues).

---

© 2025 **GreenEduMap** - Dữ liệu mở dẫn lối đô thị xanh 🌱
