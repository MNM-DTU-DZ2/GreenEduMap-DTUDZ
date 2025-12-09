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
# API Gateway

Central API Gateway for GreenEduMap microservices architecture.

## Features

- ✅ Service routing and orchestration
- ✅ Public OpenData API (no authentication)
- ✅ NGSI-LD endpoints
- ✅ Rate limiting
- ✅ CORS handling
- ✅ Health check aggregation

## Architecture

```
Client → API Gateway (Port 8000) → Microservices
                                   ├── Auth Service (8001)
                                   ├── Environment Service (8007)
                                   ├── Resource Service (8004)
                                   ├── Education Service (8008)
                                   └── AI Service (8006)
```

## Public OpenData Endpoints

### Environment Data
```
GET  /api/open-data/air-quality
GET  /api/open-data/air-quality/location?lat={lat}&lon={lon}&radius={km}
GET  /api/open-data/weather/current?lat={lat}&lon={lon}
GET  /api/open-data/weather/forecast?lat={lat}&lon={lon}
```

### Education Data
```
GET  /api/open-data/schools
GET  /api/open-data/schools/location?lat={lat}&lon={lon}&radius={km}
GET  /api/open-data/schools/green-score
```

### Export
```
GET  /api/open-data/export/air-quality?format=csv
GET  /api/open-data/export/schools?format=geojson
```

### NGSI-LD
```
GET    /ngsi-ld/v1/entities
GET    /ngsi-ld/v1/entities?type=AirQuality
POST   /ngsi-ld/v1/entities
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run gateway
uvicorn app.main:app --reload --port 8000
```

## Access

- API Gateway: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## License

MIT
