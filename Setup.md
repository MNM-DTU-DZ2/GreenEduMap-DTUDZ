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
# 🗂️ Hướng dẫn cài đặt GreenEduMap

> Hướng dẫn chi tiết cài đặt và chạy hệ thống GreenEduMap từ GitHub về máy local

---

## 🖥️ Yêu cầu hệ thống
- **CPU**: 4 cores trở lên
- **RAM**: 8 GB tối thiểu, 16 GB khuyến nghị
- **Ổ cứng**: 50 GB trống
- **Mạng**: Kết nối internet ổn định

## ⚠️ Nếu không sử dụng Docker
- Nếu bạn không dùng Docker thì xem file [docs/BUILD_WITHOUT_DOCKER.md](docs/BUILD_WITHOUT_DOCKER.md)

---

## 🛠️ Phần mềm cần cài đặt

### Nếu sử dụng Docker (Khuyến nghị)
| Phần mềm | Phiên bản | Mục đích | Link tải |
|----------|-----------|----------|----------|
| **Docker** | 20.10+ | Container runtime | [docker.com](https://www.docker.com/products/docker-desktop) |
| **Docker Compose** | 2.0+ | Orchestration tool | Đã bao gồm trong Docker Desktop |
| **Git** | 2.30+ | Version control | [git-scm.com](https://git-scm.com/downloads) |

### Nếu KHÔNG sử dụng Docker
| Phần mềm | Phiên bản | Mục đích | Link tải |
|----------|-----------|----------|----------|
| **Node.js** | 20+ | Frontend (Next.js) và Mobile (React Native) | [nodejs.org](https://nodejs.org/) |
| **Python** | 3.11+ | Backend (FastAPI) và AI Services | [python.org](https://www.python.org/) |
| **PostgreSQL** | 16+ | Database chính | [postgresql.org](https://www.postgresql.org/) |
| **PostGIS** | 3.4+ | Extension cho PostgreSQL (GIS) | [postgis.net](https://postgis.net/) |
| **MongoDB** | 7+ | NoSQL Database | [mongodb.com](https://www.mongodb.com/) |
| **Redis** | 7+ | Cache và Message Queue | [redis.io](https://redis.io/) |
| **RabbitMQ** | 3.13+ | Message Broker | [rabbitmq.com](https://www.rabbitmq.com/) |
| **EMQX** | 5.5+ | MQTT Broker | [emqx.io](https://www.emqx.io/) |
| **Git** | 2.30+ | Version control | [git-scm.com](https://git-scm.com/downloads) |

---

## 🐳 Cài đặt Docker

### Windows
1. Tải Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Chạy file cài đặt và làm theo hướng dẫn
3. Khởi động lại máy tính
4. Mở Docker Desktop và đợi khởi động hoàn tất
5. Kiểm tra cài đặt:
   ```powershell
   docker --version
   docker compose version
   ```

### macOS
1. Tải Docker Desktop cho Mac: https://www.docker.com/products/docker-desktop/
2. Kéo Docker.app vào thư mục Applications
3. Khởi động Docker từ Applications
4. Kiểm tra cài đặt:
   ```bash
   docker --version
   docker compose version
   ```

### Linux (Ubuntu/Debian)
```bash
# Cài đặt Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Thêm user vào docker group (để không cần sudo)
sudo usermod -aG docker $USER
newgrp docker

# Cài đặt Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Kiểm tra cài đặt
docker --version
docker compose version
```

---

## 📥 Cài đặt hệ thống

### Bước 1: Clone repository từ GitHub

```bash
# Clone project về máy
git clone https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ.git

# Di chuyển vào thư mục project
cd GreenEduMap-DTUDZ
```

### Bước 2: Cấu hình Environment Variables

#### Tạo file .env cho Docker

```bash
# Copy file .env.example
cp infrastructure/docker/.env.example infrastructure/docker/.env
```

Mở file `infrastructure/docker/.env` và cập nhật các thông tin sau (nếu cần):

```env
# =================================
# PORTS (4100-4699 range)
# =================================
POSTGRES_PORT=4100
REDIS_PORT=4101
MONGO_PORT=4102
RABBITMQ_PORT=4200
RABBITMQ_MGMT_PORT=4201
MQTT_PORT=4202
MQTT_WS_PORT=4203
MQTT_WSS_PORT=4204
EMQX_DASHBOARD_PORT=4205
ADMINER_PORT=4600
API_GATEWAY_PORT=4500
WEB_APP_PORT=4501

# =================================
# DATABASE
# =================================
POSTGRES_DB=greenedumap
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
MONGO_DB=greenedumap

# =================================
# MESSAGE BROKERS
# =================================
RABBITMQ_USER=admin
RABBITMQ_PASS=admin123
EMQX_DASHBOARD_USER=admin
EMQX_DASHBOARD_PASS=admin123

# =================================
# SECURITY (Thay đổi trong production!)
# =================================
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars-recommended-64
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# =================================
# API KEYS (Bổ sung key của bạn)
# =================================
OPENWEATHER_API_KEY=your_openweather_api_key
NEXT_PUBLIC_MAPTILER_API_KEY=your_maptiler_api_key

# =================================
# APPLICATION
# =================================
DEBUG=true
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:4500
```

### Bước 3: Cấu hình Services (Optional)

#### Tạo thư mục logs (nếu chưa có)

```bash
# Windows (PowerShell)
New-Item -Path infrastructure/docker/logs -ItemType Directory -Force

# Linux/macOS
mkdir -p infrastructure/docker/logs
```

---

## 🚀 Khởi động services

### Phương pháp 1: Khởi động toàn bộ hệ thống (Đơn giản nhất)

```bash
# Di chuyển vào thư mục docker
cd infrastructure/docker

# Khởi động tất cả services
docker compose up -d

# Xem logs để theo dõi quá trình khởi động
docker compose logs -f
```

> **Lưu ý**: Lần đầu tiên chạy sẽ mất 10-20 phút để tải images và build containers.

### Phương pháp 2: Khởi động từng nhóm services (Khuyến nghị)

Cách này giúp bạn kiểm soát tốt hơn quá trình khởi động:

**Bước 1: Khởi động Databases & Infrastructure**

```bash
cd infrastructure/docker

docker compose up -d postgres redis mongodb rabbitmq emqx adminer
```

Đợi khoảng **30-60 giây** để các database khởi động hoàn tất.

**Bước 2: Kiểm tra databases đã sẵn sàng**

```bash
docker compose ps
```

Tất cả containers phải có trạng thái `Up (healthy)` hoặc `Up`.

**Bước 3: Khởi động Backend Services**

```bash
docker compose up -d auth-service api-gateway resource-service environment-service education-service opendata-service
```

**Bước 4: Khởi động AI Service (Background Worker)**

```bash
docker compose up -d ai-service
```

**Bước 5: Khởi động Web App (Frontend)**

```bash
docker compose up -d web-app
```

### Phương pháp 3: Sử dụng Script quản lý

Dự án có sẵn script để quản lý services dễ dàng hơn:

**Khởi động tất cả services:**
```bash
cd infrastructure/docker
bash start.sh
```

**Dừng tất cả services:**
```bash
cd infrastructure/docker
bash stop.sh
```

Script `start.sh` sẽ tự động:
1. Kiểm tra file `.env` tồn tại
2. Khởi động databases và message brokers trước
3. Đợi databases sẵn sàng
4. Khởi động các backend services
5. Khởi động web application
6. Hiển thị status và logs

---

## 🔧 Cài đặt sau khi khởi động

### 1. Khởi tạo extensions cho PostgreSQL

Sau khi PostgreSQL đã khởi động, cần cài đặt PostGIS extension:

```bash
# Vào container PostgreSQL
docker exec -it greenedumap-postgres bash

# Kết nối vào database
psql -U postgres -d greenedumap

# Tạo extension PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

# Kiểm tra version
SELECT PostGIS_version();

# Thoát
\q
exit
```

### 2. Chạy migrations cho Database

Sau khi extensions đã được tạo, chạy migrations để khởi tạo database schema:

```bash
# Auth Service
docker exec -it greenedumap-auth-service alembic upgrade head

# Resource Service
docker exec -it greenedumap-resource-service alembic upgrade head

# Education Service
docker exec -it greenedumap-education-service alembic upgrade head

# Environment Service
docker exec -it greenedumap-environment-service alembic upgrade head

# OpenData Service
docker exec -it greenedumap-opendata-service alembic upgrade head
```

**Verify migrations:**
```bash
# Check tables created
docker exec -it greenedumap-postgres psql -U postgres -d greenedumap -c "\dt"
```

### 3. Seed dữ liệu khởi tạo

Tạo dữ liệu mẫu và admin user:

```bash
# Seed data cho Auth Service (tạo admin user)
docker exec -it greenedumap-auth-service python -m app.db.init_db

# Import dữ liệu mẫu từ init-scripts (nếu có)
docker exec -i greenedumap-postgres psql -U postgres -d greenedumap < infrastructure/docker/init-scripts/sample_data.sql
```

**Default admin user (nếu được tạo):**
- Email: `admin@greenedumap.vn`
- Password: `admin123` (Thay đổi ngay sau khi đăng nhập đầu tiên!)

---

## ✅ Kiểm tra hệ thống

### 1. Kiểm tra containers đang chạy

```bash
cd infrastructure/docker
docker compose ps
```

Kết quả mong đợi: Tất cả services có trạng thái `Up` hoặc `Up (healthy)`.

```
NAME                              STATUS
greenedumap-adminer               Up
greenedumap-ai-service            Up
greenedumap-api-gateway           Up (healthy)
greenedumap-auth-service          Up (healthy)
greenedumap-education-service     Up (healthy)
greenedumap-emqx                  Up (healthy)
greenedumap-environment-service   Up (healthy)
greenedumap-mongodb               Up (healthy)
greenedumap-opendata-service      Up (healthy)
greenedumap-postgres              Up (healthy)
greenedumap-rabbitmq              Up (healthy)
greenedumap-redis                 Up (healthy)
greenedumap-resource-service      Up (healthy)
greenedumap-web-app               Up
```

### 2. Kiểm tra logs

```bash
# Xem logs tất cả services
docker compose logs

# Xem logs của service cụ thể
docker compose logs api-gateway
docker compose logs auth-service
docker compose logs web-app

# Follow logs realtime
docker compose logs -f environment-service
```

### 3. Truy cập các services

| Service                    | URL                          | Credentials           |
| -------------------------- | ---------------------------- | --------------------- |
| **Web Application**        | http://localhost:4501        | -                     |
| **API Gateway**            | http://localhost:4500        | -                     |
| **API Documentation**      | http://localhost:4500/docs   | -                     |
| **Adminer (DB UI)**        | http://localhost:4600        | postgres / postgres   |
| **RabbitMQ Management**    | http://localhost:4201        | admin / admin123      |
| **EMQX Dashboard**         | http://localhost:4205        | admin / admin123      |

### 4. Test API endpoints

```bash
# Health check API Gateway
curl http://localhost:4500/health

# Health check Auth Service (qua gateway)
curl http://localhost:4500/api/v1/auth/health

# Health check Resource Service
curl http://localhost:4304/health

# Health check Education Service
curl http://localhost:8003/health

# Health check Environment Service (internal)
curl http://localhost:4303/health

# Health check OpenData Service
curl http://localhost:8009/health

# List NGSI-LD entities (OpenData)
curl http://localhost:8009/api/v1/ngsi-ld/entities
```

Nếu các API trả về response (không lỗi connection), nghĩa là hệ thống đã chạy thành công!

### 5. Kiểm tra kết nối database

**PostgreSQL**

```bash
docker exec -it greenedumap-postgres psql -U postgres -d greenedumap -c "\dt"
```

**MongoDB**

```bash
docker exec -it greenedumap-mongodb mongosh --eval "show dbs"
```

**Redis**

```bash
docker exec -it greenedumap-redis redis-cli ping
```

Kết quả mong đợi: `PONG`

---

## 🛑 Dừng và xóa hệ thống

### Dừng tất cả services

```bash
cd infrastructure/docker
docker compose stop
```

### Dừng và xóa containers (giữ lại data)

```bash
docker compose down
```

### Xóa hoàn toàn (bao gồm volumes/data)

```bash
docker compose down -v
```

### Clean rebuild toàn bộ hệ thống

```bash
# Dừng và xóa tất cả
docker compose down -v

# Xóa images
docker compose rm -f
docker images | grep greenedumap | awk '{print $3}' | xargs docker rmi -f

# Build lại từ đầu
docker compose build --no-cache
docker compose up -d
```

---

## 🆘 Troubleshooting

### Lỗi: Port already in use

**Nguyên nhân**: Port đã được sử dụng bởi ứng dụng khác

**Giải pháp**:

1. **Kiểm tra port nào đang bị chiếm**:

   ```bash
   # Windows
   netstat -ano | findstr :4500
   netstat -ano | findstr :4100

   # Linux/macOS
   lsof -i :4500
   lsof -i :4100
   ```

2. **Dừng ứng dụng đang chiếm port** hoặc thay đổi port trong file `.env`

3. **Thay đổi port trong .env**:

   ```env
   POSTGRES_PORT=5100
   API_GATEWAY_PORT=5500
   WEB_APP_PORT=5501
   ```

### Lỗi: Container unhealthy hoặc không khởi động

**Nguyên nhân**: Service không khởi động đúng cách

**Giải pháp**:

```bash
# Xem logs của container
docker compose logs [service-name]

# Ví dụ
docker compose logs postgres
docker compose logs api-gateway

# Restart container
docker compose restart [service-name]

# Rebuild container
docker compose up -d --build [service-name]
```

### Lỗi: Permission denied (Linux)

**Nguyên nhân**: User chưa có quyền chạy Docker

**Giải pháp**:

```bash
# Thêm user vào docker group
sudo usermod -aG docker $USER

# Logout và login lại
# Hoặc chạy lệnh này để áp dụng ngay
newgrp docker
```

### Lỗi: Out of memory

**Nguyên nhân**: Docker không đủ RAM

**Giải pháp**:

1. **Tăng memory limit cho Docker Desktop**:

   - Mở Docker Desktop
   - Settings → Resources → Memory
   - Tăng lên ít nhất 6-8 GB

2. **Hoặc giảm số services chạy đồng thời**:
   ```bash
   # Chỉ chạy services cần thiết
   docker compose up -d postgres redis api-gateway web-app
   ```

### Lỗi: Database connection refused

**Nguyên nhân**: Database chưa khởi động xong

**Giải pháp**:

```bash
# Đợi database khởi động (30-60 giây)
docker compose logs postgres
docker compose logs mongodb

# Kiểm tra health status
docker compose ps

# Nếu vẫn lỗi, restart database
docker compose restart postgres
```

### Lỗi: Cannot connect to Docker daemon

**Nguyên nhân**: Docker Desktop chưa khởi động

**Giải pháp**:

1. Khởi động Docker Desktop
2. Đợi Docker khởi động hoàn tất (icon Docker trên taskbar/menu bar phải màu xanh)
3. Thử lại lệnh

### Lỗi: Build failed hoặc image pull failed

**Nguyên nhân**: Kết nối internet không ổn định hoặc Docker Hub bị chặn

**Giải pháp**:

```bash
# Thử lại build
docker compose build --no-cache

# Hoặc pull image trước
docker compose pull

# Nếu Docker Hub bị chặn, cấu hình Docker mirror
# Thêm vào Docker Desktop Settings → Docker Engine:
{
  "registry-mirrors": ["https://mirror.gcr.io"]
}
```

### Lỗi: Python module not found trong backend services

**Nguyên nhân**: Dependencies chưa được cài đặt trong container

**Giải pháp**:

```bash
# Rebuild service với --no-cache
docker compose build --no-cache [service-name]

# Ví dụ
docker compose build --no-cache ai-service
docker compose up -d ai-service
```

### Xóa và rebuild hoàn toàn

Nếu gặp lỗi không giải quyết được, thử clean rebuild:

```bash
# Dừng tất cả containers
cd infrastructure/docker
docker compose down -v

# Xóa tất cả images của GreenEduMap
docker images | grep greenedumap | awk '{print $3}' | xargs docker rmi -f

# Xóa tất cả volumes
docker volume ls | grep greenedumap | awk '{print $2}' | xargs docker volume rm

# Clean Docker system
docker system prune -a --volumes

# Rebuild lại từ đầu
docker compose up -d --build
```

---

## 📚 Các lệnh Docker hữu ích

```bash
# Xem tất cả containers (kể cả stopped)
docker compose ps -a

# Xem logs realtime
docker compose logs -f

# Xem logs của 1 service
docker compose logs -f api-gateway

# Truy cập shell của container
docker exec -it greenedumap-api-gateway bash

# Xem resource usage
docker stats

# Xóa containers stopped
docker compose rm -f

# Rebuild 1 service cụ thể
docker compose up -d --build auth-service

# Xem networks
docker network ls

# Xem volumes
docker volume ls

# Backup volume (PostgreSQL)
docker run --rm -v greenedumap-postgres-data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres-backup.tar.gz -C /data .

# Restore volume
docker run --rm -v greenedumap-postgres-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/postgres-backup.tar.gz -C /data
```

---

## 📞 Hỗ trợ

Nếu gặp vấn đề trong quá trình cài đặt:

1. **Kiểm tra lại file .env**: Đảm bảo các biến môi trường đã được cấu hình đúng
2. **Kiểm tra logs**: `docker compose logs -f` để xem lỗi chi tiết
3. **Kiểm tra ports**: Đảm bảo không có ứng dụng khác đang chiếm ports
4. **Kiểm tra Docker**: Đảm bảo Docker Desktop đang chạy và có đủ resources (CPU, RAM, Disk)
5. **Tạo issue**: Nếu vẫn gặp lỗi, tạo issue tại [GitHub Issues](https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ/issues)

---

## �‍💻 Dành cho Developer (Development không dùng Docker)

Nếu bạn muốn phát triển local mà không dùng Docker, hãy tham khảo hướng dẫn chi tiết tại [docs/BUILD_WITHOUT_DOCKER.md](docs/BUILD_WITHOUT_DOCKER.md).

### Quick Start cho Development

#### 1. Backend Development (FastAPI)

```bash
# Cài đặt PostgreSQL, Redis local
# Ubuntu/Debian
sudo apt install postgresql redis-server

# Start services
sudo systemctl start postgresql redis

# Chọn service bạn muốn phát triển (ví dụ: Auth Service)
cd modules/auth-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env
cp .env.example .env

# Run with hot-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### 2. Frontend Development (Next.js)

```bash
cd modules/web-app

# Install dependencies
npm install

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
NODE_ENV=development
```

```bash
# Run development server
npm run dev

# Open http://localhost:3000
```

#### 3. 📱 React Native Development (Mobile App)

**Yêu cầu bổ sung:**
- **Android Studio** (cho Android development)
- **Xcode** (cho iOS development - chỉ macOS)
- **Java JDK** 17+
- **Android SDK** API Level 33+
- **CocoaPods** (cho iOS - macOS only)

**Cài đặt:**

```bash
cd modules/appmobile

# Install dependencies
npm install
# hoặc
yarn install

# iOS only (macOS)
cd ios
pod install
cd ..
```

**Cấu hình Environment:**

Tạo file `modules/appmobile/src/config/env.ts`:

```typescript
export const ENV_CONFIG = {
  // API Configuration
  API_URL: 'http://localhost:8000',  // Development: localhost
  // API_URL: 'https://api.greenedumap.vn',  // Production

  // EKYC Configuration (Real-time WebSocket với Laravel Reverb)
  REVERB_APP_ID: 'YOUR_REVERB_APP_ID',
  REVERB_APP_KEY: 'YOUR_REVERB_APP_KEY',
  REVERB_APP_SECRET: 'YOUR_REVERB_APP_SECRET',
  REVERB_HOST: 'YOUR_REVERB_HOST',           // e.g., 'reverb.greenedumap.vn' or 'localhost'
  REVERB_PORT: '443',                         // Port HTTPS (443) hoặc 6001 cho development
  REVERB_SCHEME: 'https',                     // 'https' cho production, 'http' cho local

  // MapTiler Configuration (Open Source Map Provider)
  MAPTILER_API_KEY: 'YOUR_MAPTILER_API_KEY', // Lấy tại https://cloud.maptiler.com/

  // App Configuration
  APP_NAME: 'GreenEduMap',
  APP_VERSION: '1.0.0',
  ENABLE_AI: true,
};
```

**Hoặc sử dụng file .env:**

Tạo file `modules/appmobile/.env`:

```env
# API Configuration
API_URL=http://localhost:8000

# EKYC/Reverb Configuration (Real-time WebSocket)
REVERB_APP_ID=your_reverb_app_id
REVERB_APP_KEY=your_reverb_app_key
REVERB_APP_SECRET=your_reverb_app_secret
REVERB_HOST=localhost
REVERB_PORT=6001
REVERB_SCHEME=http

# MapTiler Configuration
MAPTILER_API_KEY=your_maptiler_api_key

# App Configuration
APP_NAME=GreenEduMap
ENABLE_AI=true
```

**Lưu ý quan trọng:**

> **MapTiler API Key**: Đăng ký miễn phí tại https://cloud.maptiler.com/
> - Free tier: 100,000 map loads/tháng
> - Cần thiết để hiển thị bản đồ trong app

> **Reverb Configuration**: Nếu sử dụng real-time features (WebSocket)
> - Development: Có thể bỏ qua hoặc dùng mock data
> - Production: Cần cấu hình Laravel Reverb server

**Chạy app:**

```bash
# Android
npm run android
# hoặc
npx react-native run-android

# iOS (macOS only)
npm run ios
# hoặc
npx react-native run-ios

# Start Metro bundler riêng biệt
npm start
```

**Debug trên thiết bị thật:**

**Android:**
```bash
# Enable USB debugging trên điện thoại
# Kết nối USB và chạy:
adb devices  # Kiểm tra device được nhận diện

# Nếu dùng API local (localhost), cần port forwarding:
adb reverse tcp:8000 tcp:8000  # Forward API port
adb reverse tcp:6001 tcp:6001  # Forward Reverb port (nếu có)

npm run android
```

**iOS:**
```bash
# Mở Xcode
open ios/GreenEduMapApp.xcworkspace

# Chọn device/simulator và Run
# hoặc dùng CLI:
npm run ios -- --device "Your iPhone Name"
```

**Troubleshooting Mobile:**

1. **Metro bundler cache issues:**
   ```bash
   npx react-native start --reset-cache
   ```

2. **Android build fails:**
   ```bash
   cd android
   ./gradlew clean
   cd ..
   npm run android
   ```

3. **iOS build fails:**
   ```bash
   cd ios
   pod deintegrate
   pod install
   cd ..
   npm run ios
   ```

4. **Map không hiển thị:**
   - Kiểm tra `MAPTILER_API_KEY` đã đúng
   - Kiểm tra internet connection
   - Xem logs: `npx react-native log-android` hoặc `npx react-native log-ios`

5. **Không kết nối được API:**
   - Android emulator: Dùng `http://10.0.2.2:8000` thay vì `localhost:8000`
   - iOS simulator: Dùng `http://localhost:8000` bình thường
   - Real device: Phải dùng IP máy tính (VD: `http://192.168.1.100:8000`)

**Lấy MapTiler API Key:**

1. Truy cập https://cloud.maptiler.com/
2. Đăng ký tài khoản miễn phí
3. Tạo API key mới tại Dashboard
4. Copy key và paste vào file config

**Development Tips:**

- **Hot Reload**: Shake device và chọn "Enable Fast Refresh"
- **Debug Menu**: Shake device hoặc Cmd+D (iOS) / Cmd+M (Android)
- **React DevTools**: `npm install -g react-devtools` và chạy `react-devtools`
- **Network Inspect**: Enable "Debug JS Remotely" để dùng Chrome DevTools

---

## �📚 Tài liệu bổ sung

- [Architecture](docs/ARCHITECTURE.md) - Kiến trúc hệ thống chi tiết
- [API Documentation](docs/API_DOCUMENTATION.md) - Tài liệu API đầy đủ
- [Deployment Guide](docs/DEPLOYMENT.md) - Hướng dẫn deploy lên server
- [Development Workflow](docs/DEVELOPMENT_WORKFLOW.md) - Quy trình phát triển
- [Contributing](CONTRIBUTING.md) - Hướng dẫn đóng góp cho dự án

---

## 🎯 Tóm tắt các bước cài đặt

1. ✅ Cài đặt Docker Desktop
2. ✅ Clone repository về máy
3. ✅ Copy và cấu hình file `.env`
4. ✅ Chạy `docker compose up -d`
5. ✅ Đợi 10-20 phút để build và khởi động
6. ✅ Kiểm tra containers: `docker compose ps`
7. ✅ Tạo PostGIS extension trong PostgreSQL
8. ✅ Truy cập Web App: http://localhost:4501
9. ✅ Truy cập API Docs: http://localhost:4500/docs

**Chúc bạn cài đặt thành công! 🚀**

---

© 2025 **GreenEduMap** - Dữ liệu mở dẫn lối đô thị xanh 🌱
