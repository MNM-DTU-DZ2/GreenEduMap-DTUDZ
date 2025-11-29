# 🔑 API Keys Setup Guide

Đã tạo các file sau để quản lý API keys một cách an toàn:

## 📁 Files Created:

### 1. `scripts/api-keys.env` ✅
```bash
OPENWEATHER_API_KEY=30de77839a05db1dfe983c341a297838
```
**⚠️ File này đã được thêm vào .gitignore - KHÔNG được push lên Git!**

### 2. `.gitignore` ✅
Đã update để ignore:
- `scripts/api-keys.env`
- `.env`
- Tất cả secrets và sensitive files

### 3. Helper Scripts:

**Windows (PowerShell):**
```powershell
.\scripts\load-api-keys.ps1
```

**Linux/Mac (Bash):**
```bash
source ./scripts/load-api-keys.sh
```

## 🚀 Cách Sử Dụng:

### Cách 1: Manually update `.env` file
```bash
cd infrastructure/docker

# Edit .env file
# Find: OPENWEATHER_API_KEY=
# Change to: OPENWEATHER_API_KEY=30de77839a05db1dfe983c341a297838
```

### Cách 2: Copy từ api-keys.env
```powershell
# Get key from api-keys.env
cat scripts/api-keys.env

# Then paste vào infrastructure/docker/.env
```

## ✅ Verify Setup:

```bash
cd infrastructure/docker
docker-compose down
docker-compose up -d

# Test Weather API
curl "http://localhost:8007/api/v1/weather/current?lat=16.0544&lon=108.2022&fetch_new=true"
```

## 🔒 Security Note:

✅ **SAFE TO COMMIT:**
- `.gitignore`
- `scripts/load-api-keys.sh`
- `scripts/load-api-keys.ps1`
- `.env.example`

❌ **NEVER COMMIT:**
- `scripts/api-keys.env` 
- `infrastructure/docker/.env`
- Any file with actual API keys!

---

**API Key đã được lưu an toàn trong `scripts/api-keys.env`! 🎉**
