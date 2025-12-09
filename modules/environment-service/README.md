# Environment Service

OpenAQ and OpenWeather API integration service for GreenEduMap.

## Features

- ✅ OpenAQ API integration (air quality data)
- ✅ OpenWeather API integration (weather data)
- ✅ NGSI-LD entity creation
- ✅ Scheduled data fetching
- ✅ Spatial queries (PostGIS)
- ✅ Public OpenData endpoints

## Tech Stack

- **Framework**: FastAPI 0.109
- **Database**: PostgreSQL + PostGIS
- **External APIs**: OpenAQ, OpenWeather
- **Scheduler**: APScheduler

## Setup

### 1. Get API Keys

#### OpenAQ API
- Free tier: 10,000 requests/month
- Sign up: https://openaq.org/
- No API key required (public API)

#### OpenWeather API
- Free tier: 60 calls/minute, 1M calls/month
- Sign up: https://openweathermap.org/api
- Get API key from https://home.openweathermap.org/api_keys

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Service

```bash
# Development
uvicorn app.main:app --reload --port 8007

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8007 --workers 4
```

## API Endpoints

### Air Quality

```
GET  /api/v1/air-quality                # Latest measurements
GET  /api/v1/air-quality/location       # By location + radius
GET  /api/v1/air-quality/history        # Historical data
GET  /api/v1/air-quality/{id}           # Specific measurement
```

### Weather

```
GET  /api/v1/weather/current            # Current weather
GET  /api/v1/weather/forecast           # 5-day forecast
GET  /api/v1/weather/location           # Weather by location
```

### NGSI-LD

```
GET  /ngsi-ld/v1/entities?type=AirQuality
POST /ngsi-ld/v1/entities               # Create entity
```

## Examples

```bash
# Get air quality near Da Nang
curl "http://localhost:8007/api/v1/air-quality/location?lat=16.0544&lon=108.2022&radius=50"

# Get current weather
curl "http://localhost:8007/api/v1/weather/current?lat=16.0544&lon=108.2022"

# Get forecast
curl "http://localhost:8007/api/v1/weather/forecast?lat=16.0544&lon=108.2022"
```

## Scheduled Tasks

- **Air Quality**: Fetch every hour
- **Weather**: Fetch every 30 minutes
- **Cleanup**: Remove old data daily

## License

MIT
