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
# 🚀 Hướng Dẫn Deploy GreenEduMap trên VPS Ubuntu

## 📋 Mục Lục
1. [Xóa Containers và Images Cũ](#1-xóa-containers-và-images-cũ)
2. [Deploy Mới](#2-deploy-mới)
3. [Kiểm Tra](#3-kiểm-tra)

---

## 1. Xóa Containers và Images Cũ

### Cách 1: Sử dụng Script Tự Động (Khuyến nghị)

```bash
# Di chuyển vào thư mục scripts
cd /opt/greenedumap/scripts/deploy

# Chạy script cleanup
sudo ./cleanup-greenedumap.sh
```

Script sẽ:
- ✅ Dừng tất cả containers greenedumap
- ✅ Xóa tất cả containers greenedumap
- ✅ Xóa tất cả images greenedumap
- ✅ Xóa tất cả volumes greenedumap
- ✅ Dọn dẹp Docker system

### Cách 2: Xóa Thủ Công

```bash
# 1. Dừng và xóa containers
docker ps -a --filter "name=greenedumap" --format "{{.Names}}" | xargs -r docker stop
docker ps -a --filter "name=greenedumap" --format "{{.Names}}" | xargs -r docker rm -f

# 2. Xóa images
docker images --filter "reference=*greenedumap*" --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f
docker images --filter "reference=*docker-*" --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f

# 3. Xóa volumes
docker volume ls --filter "name=greenedumap" --format "{{.Name}}" | xargs -r docker volume rm -f

# 4. Dọn dẹp
docker system prune -f
```

---

## 2. Deploy Mới

### Bước 1: Clone/Pull Repository

```bash
# Nếu chưa có repository
cd /opt
sudo git clone <your-repo-url> greenedumap

# Nếu đã có repository
cd /opt/greenedumap
sudo git pull origin main
```

### Bước 2: Chạy Deploy Script

```bash
cd /opt/greenedumap/scripts/deploy
sudo chmod +x deploy.sh
sudo ./deploy.sh
```

Script sẽ hỏi:
1. **Deployment mode**: Domain-based (1) hoặc IP-only (2)
2. **Domain/Email** (nếu chọn mode 1)
3. **Repository URL** (nếu chưa clone)
4. **Seed database** (y/N) - **Chọn 'y' để có dữ liệu mẫu**

### Bước 3: Đợi Deploy Hoàn Tất

Script sẽ tự động:
- ✅ Cập nhật hệ thống
- ✅ Cài đặt Docker & Docker Compose
- ✅ Cài đặt Nginx & Certbot (nếu dùng domain)
- ✅ Clone/Pull repository
- ✅ Tạo .env file với passwords tự động
- ✅ Build và start services
- ✅ Chạy migrations
- ✅ Seed database (nếu chọn 'y')
- ✅ Cấu hình Nginx & SSL (nếu dùng domain)

---

## 3. Kiểm Tra

### 3.1. Kiểm Tra Services

```bash
cd /opt/greenedumap/infrastructure/docker
docker-compose ps
```

Tất cả services phải có status `Up` và `healthy`.

### 3.2. Kiểm Tra Logs

```bash
# Xem logs tất cả services
docker-compose logs -f

# Xem logs một service cụ thể
docker-compose logs -f api-gateway
docker-compose logs -f web-app
```

### 3.3. Kiểm Tra API

```bash
# Health check
curl http://localhost:10000/health

# Test endpoints
curl http://localhost:10000/api/v1/schools?limit=5
curl http://localhost:10000/api/v1/green-zones?limit=5
curl http://localhost:10000/api/v1/green-resources?limit=5
```

### 3.4. Kiểm Tra Database

```bash
# Vào PostgreSQL container
docker exec -it greenedumap-postgres psql -U greenedumap -d greenedumap_prod

# Kiểm tra số lượng records
SELECT COUNT(*) FROM schools;
SELECT COUNT(*) FROM green_zones;
SELECT COUNT(*) FROM green_resources;
SELECT COUNT(*) FROM air_quality;
```

### 3.5. Seed Database (Nếu Chưa Seed)

Nếu bạn đã skip seed trong quá trình deploy, có thể chạy sau:

```bash
cd /opt/greenedumap/scripts/deploy
sudo chmod +x seed_database.sh
sudo ./seed_database.sh
```

---

## 🔧 Troubleshooting

### Lỗi: Container không start

```bash
# Xem logs chi tiết
docker-compose logs <service-name>

# Restart service
docker-compose restart <service-name>
```

### Lỗi: Database connection failed

```bash
# Kiểm tra PostgreSQL
docker exec greenedumap-postgres pg_isready -U greenedumap

# Kiểm tra .env file
cat /opt/greenedumap/infrastructure/docker/.env
```

### Lỗi: Port đã được sử dụng

```bash
# Tìm process đang dùng port
sudo lsof -i :10000
sudo lsof -i :4000

# Kill process
sudo kill -9 <PID>
```

### Lỗi: SSL certificate failed

```bash
# Kiểm tra DNS đã trỏ về IP chưa
nslookup your-domain.com

# Retry SSL
sudo certbot --nginx -d your-domain.com -d www.your-domain.com -d api.your-domain.com
```

---

## 📝 Lưu Ý Quan Trọng

1. **Credentials**: Được lưu tại `/root/greenedumap-credentials.txt`
2. **Backup**: Nên backup database trước khi xóa containers
3. **Firewall**: Mở ports cần thiết (80, 443, 22)
4. **Updates**: Chạy `git pull` và `docker-compose up -d --build` để update

---

## 🎯 Quick Commands

```bash
# Xem status
docker-compose ps

# Xem logs
docker-compose logs -f

# Restart tất cả
docker-compose restart

# Stop tất cả
docker-compose down

# Update code
cd /opt/greenedumap
git pull
cd infrastructure/docker
docker-compose up -d --build

# Seed data
/opt/greenedumap/scripts/deploy/seed_database.sh
```

---

## ✅ Checklist Sau Khi Deploy

- [ ] Tất cả containers đang chạy (`docker-compose ps`)
- [ ] API Gateway trả về 200 (`curl http://localhost:10000/health`)
- [ ] Web app accessible (http://your-ip:4000 hoặc https://your-domain)
- [ ] Database có dữ liệu (kiểm tra bằng psql)
- [ ] SSL certificate hoạt động (nếu dùng domain)
- [ ] Logs không có lỗi (`docker-compose logs`)

---

**Chúc bạn deploy thành công! 🎉**

