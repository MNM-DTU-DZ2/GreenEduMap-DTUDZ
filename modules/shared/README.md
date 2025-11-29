# Shared Module - GreenEduMap

Shared database models and utilities for GreenEduMap microservices.

## Features

- ✅ SQLAlchemy ORM models with async support
- ✅ PostGIS geography columns for spatial data
- ✅ OpenData-compliant (UUID, is_public, data_uri, ngsi_ld_uri)
- ✅ NGSI-LD conversion methods
- ✅ JSONB metadata fields for extensibility

## Models

### AirQuality
Air quality measurements from OpenAQ and sensors.

**Fields:**
- location (PostGIS Point)
- aqi, pm25, pm10, co, no2, o3, so2
- source, station_name
- measurement_date
- OpenData fields (is_public, data_uri, ngsi_ld_uri)

**Methods:**
- `to_dict()` - JSON serialization
- `to_ngsi_ld()` - NGSI-LD entity format

### Weather
Weather data from OpenWeather API.

**Fields:**
- location (PostGIS Point)
- temperature, humidity, pressure
- wind_speed, wind_direction
- weather_main, weather_description
- observation_time

### School
Educational institutions with green metrics.

**Fields:**
- name, code, location
- green_score (0-100)
- facilities (JSONB)
- type (elementary|middle|high|university)

### Resource & RescueCenter
Resource management for rescue operations.

### DataCatalog
OpenData catalog with dataset metadata.

## Installation

### As a Package

```bash
cd modules/shared
pip install -e .
```

### In Dockerfile

```dockerfile
COPY ../shared /tmp/shared
RUN pip install --no-cache-dir /tmp/shared && rm -rf /tmp/shared
```

## Usage

```python
from shared.database.base import get_session
from shared.database.models import AirQuality, Weather, School

# In FastAPI route
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

@router.get("/data")
async def get_data(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(AirQuality))
    return result.scalars().all()
```

## Database Configuration

Set `DATABASE_URL` environment variable:

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
```

## Development

```bash
# Install in editable mode
pip install -e .

# Run tests
pytest
```

## License

MIT
