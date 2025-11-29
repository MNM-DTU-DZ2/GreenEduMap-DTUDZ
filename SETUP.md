# GreenEduMap - Setup and Run Instructions

## 🚀 Quick Start

### Step 1: Get OpenWeather API Key

1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Navigate to https://home.openweathermap.org/api_keys
4. Copy your API key

### Step 2: Configure Environment

```bash
cd infrastructure/docker

# Edit .env file
# Find line: OPENWEATHER_API_KEY=
# Add your key: OPENWEATHER_API_KEY=your_actual_key_here
```

### Step 3: Start Services

```bash
# Make sure you're in infrastructure/docker directory
docker-compose up -d
```

This will:
- Create PostgreSQL database with PostGIS
- Create all tables automatically
- Start all services (Auth, Environment, API Gateway)

### Step 4: Verify

```bash
# Check services are running
docker-compose ps

# Check API Gateway
curl http://localhost:8000/health

# Should return:
# {
#   "status": "healthy",
#   "gateway": "healthy",
#   "services": {
#     "environment": "healthy",
#     "auth": "healthy"
#   }
# }
```

## 🧪 Test the APIs

### Get Current Weather

```bash
curl "http://localhost:8000/api/open-data/weather/current?lat=16.0544&lon=108.2022"
```

### Get Air Quality

```bash
# Manually fetch from OpenAQ first
curl -X POST "http://localhost:8007/api/v1/air-quality/fetch?lat=16.0544&lon=108.2022&radius=100"

# Then query
curl "http://localhost:8000/api/open-data/air-quality"
```

## 🗄️ Database Access

### Via Adminer (Web UI)

1. Open http://localhost:8080
2. Login with:
   - System: PostgreSQL
   - Server: postgres
   - Username: postgres
   - Password: postgres
   - Database: greenedumap

### Via CLI

```bash
docker exec -it greenedumap-postgres psql -U postgres -d greenedumap

# Check tables
\dt

# Query air quality
SELECT * FROM air_quality LIMIT 5;

# Query weather
SELECT * FROM weather LIMIT 5;
```

## 🐛 Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs -f environment-service

# Rebuild
docker-compose up -d --build
```

### PostGIS not enabled

```bash
# Check PostGIS
docker exec -it greenedumap-postgres psql -U postgres -d greenedumap -c "SELECT PostGIS_Version();"
```

### Empty data

Make sure to:
1. Add OPENWEATHER_API_KEY to .env
2. Manually fetch data first using the fetch endpoints

## 📚 API Documentation

- API Gateway: http://localhost:8000/docs
- Environment Service: http://localhost:8007/docs

## 🔄 Rebuild After Code Changes

```bash
cd infrastructure/docker
docker-compose down
docker-compose up -d --build
```

---

**Everything should work now! 🎉**
