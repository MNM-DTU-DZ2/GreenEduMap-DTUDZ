# 📋 Tóm Tắt: Hướng Dẫn Deploy trên VPS Ubuntu

## 🧹 Bước 1: Xóa Containers và Images Cũ

### Trên VPS Ubuntu, chạy:

```bash
cd /opt/greenedumap/scripts/deploy
sudo chmod +x cleanup-greenedumap.sh
sudo ./cleanup-greenedumap.sh
```

**Hoặc xóa thủ công:**
```bash
# Dừng và xóa containers
docker ps -a --filter "name=greenedumap" --format "{{.Names}}" | xargs -r docker stop
docker ps -a --filter "name=greenedumap" --format "{{.Names}}" | xargs -r docker rm -f

# Xóa images
docker images --filter "reference=*greenedumap*" --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f
docker images --filter "reference=*docker-*" --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f

# Xóa volumes
docker volume ls --filter "name=greenedumap" --format "{{.Name}}" | xargs -r docker volume rm -f

# Dọn dẹp
docker system prune -f
```

---

## 🚀 Bước 2: Deploy Mới

```bash
cd /opt/greenedumap/scripts/deploy
sudo chmod +x deploy.sh seed_database.sh
sudo ./deploy.sh
```

**Script sẽ hỏi:**
1. Deployment mode: Domain (1) hoặc IP-only (2)
2. Domain & Email (nếu chọn domain)
3. Repository URL (nếu chưa clone)
4. **Seed database? (y/N)** ← **Chọn 'y' để có dữ liệu mẫu**

---

## ✅ Bước 3: Kiểm Tra

```bash
# Kiểm tra services
cd /opt/greenedumap/infrastructure/docker
docker-compose ps

# Kiểm tra API
curl http://localhost:10000/health
curl http://localhost:10000/api/v1/schools?limit=5

# Kiểm tra database
docker exec greenedumap-postgres psql -U greenedumap -d greenedumap_prod -c "SELECT COUNT(*) FROM schools;"
```

---

## 📝 Files Đã Tạo/Cập Nhật

1. ✅ `scripts/deploy/cleanup-greenedumap.sh` - Script xóa containers/images
2. ✅ `scripts/deploy/seed_database.sh` - Script seed data cho Linux
3. ✅ `scripts/deploy/deploy.sh` - Đã thêm step seed data (Step 10/11)
4. ✅ `scripts/deploy/VPS_DEPLOYMENT_GUIDE.md` - Hướng dẫn chi tiết

---

## 🔍 Kiểm Tra Deploy Script

**Đã có:**
- ✅ System update
- ✅ Docker installation
- ✅ Nginx & Certbot (domain mode)
- ✅ Git clone/pull
- ✅ Environment configuration
- ✅ Build & start services
- ✅ Database migrations
- ✅ **Database seeding (MỚI THÊM)**
- ✅ Nginx & SSL configuration

**Seed Data Files:**
- ✅ `modules/education-service/migrations/seed_data.sql`
- ✅ `modules/resource-service/migrations/seed_data.sql`
- ✅ `modules/environment-service/seed_data.sql`
- ✅ `modules/environment-service/seed_data_historical.sql`

---

## 💡 Lưu Ý

1. **Seed Data**: Script sẽ hỏi bạn có muốn seed không. Chọn 'y' để có dữ liệu mẫu.
2. **Nếu skip seed**: Có thể chạy sau bằng `sudo ./seed_database.sh`
3. **Credentials**: Được lưu tại `/root/greenedumap-credentials.txt`

---

## 🎯 Quick Test

Sau khi deploy xong, test nhanh:

```bash
# 1. Health check
curl http://localhost:10000/health

# 2. Test APIs
curl http://localhost:10000/api/v1/schools?limit=3
curl http://localhost:10000/api/v1/green-zones?limit=3
curl http://localhost:10000/api/v1/green-resources?limit=3

# 3. Kiểm tra web app
curl http://localhost:4000
```

Tất cả phải trả về 200 OK và có dữ liệu!

