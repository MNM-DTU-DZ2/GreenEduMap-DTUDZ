# 📚 GreenEduMap API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.greenedumap.com`

## Authentication

Currently using Bearer Token (JWT will be implemented).

```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Response Format

All responses are in JSON format:

```json
{
  "data": {},
  "error": null,
  "status": 200
}
```

---

## 🌍 Air Quality Endpoints

### Get Air Quality List

**Endpoint**: `GET /api/air-quality/`

**Parameters**:
- `skip` (int): Offset for pagination (default: 0)
- `limit` (int): Number of records (default: 10, max: 100)
- `city` (string): City name (default: "Hanoi")

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/air-quality/?city=Hanoi&skip=0&limit=10"
```

**Example Response**:
```json
{
  "total": 50,
  "items": [
    {
      "id": 1,
      "ward_name": "Hoàn Kiếm",
      "district": "Hoàn Kiếm",
      "city": "Hanoi",
      "latitude": 21.0285,
      "longitude": 105.8505,
      "aqi": 65.5,
      "pm25": 22.3,
      "pm10": 45.2,
      "no2": 15.8,
      "measurement_date": "2024-11-04T10:30:00",
      "created_at": "2024-11-04T10:30:00",
      "updated_at": "2024-11-04T10:30:00"
    }
  ]
}
```

---

### Get Specific Air Quality Record

**Endpoint**: `GET /api/air-quality/{id}`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/air-quality/1"
```

**Example Response**:
```json
{
  "id": 1,
  "ward_name": "Hoàn Kiếm",
  "aqi": 65.5,
  "pm25": 22.3,
  ...
}
```

**Error Response** (404):
```json
{
  "detail": "Air quality record not found"
}
```

---

### Create Air Quality Record

**Endpoint**: `POST /api/air-quality/`

**Request Body**:
```json
{
  "ward_name": "Đống Đa",
  "district": "Đống Đa",
  "city": "Hanoi",
  "latitude": 21.0245,
  "longitude": 105.8345,
  "aqi": 78.5,
  "pm25": 28.9,
  "pm10": 52.1,
  "no2": 18.5,
  "o3": 12.3,
  "so2": 5.6,
  "co": 0.8,
  "data_source": "OpenAQ"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/air-quality/" \
  -H "Content-Type: application/json" \
  -d '{
    "ward_name": "Đống Đa",
    "city": "Hanoi",
    "aqi": 78.5,
    "pm25": 28.9
  }'
```

**Success Response** (201):
```json
{
  "id": 51,
  "ward_name": "Đống Đa",
  "aqi": 78.5,
  ...
}
```

---

### Get High AQI Alerts

**Endpoint**: `GET /api/air-quality/alerts/high`

**Parameters**:
- `threshold` (float): AQI threshold (default: 150)

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/air-quality/alerts/high?threshold=150"
```

**Example Response**:
```json
[
  {
    "location": "Hoàn Kiếm",
    "aqi_level": "Unhealthy",
    "aqi_value": 175.5,
    "main_pollutant": "PM2.5",
    "recommendation": "Hạn chế hoạt động ngoài trời, sử dụng khẩu trang N95"
  }
]
```

---

### Fetch from OpenAQ

**Endpoint**: `GET /api/air-quality/fetch/openaq`

**Parameters**:
- `city` (string): City name (default: "Hanoi")

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/air-quality/fetch/openaq?city=Hanoi"
```

**Response**:
```json
{
  "success": true,
  "source": "OpenAQ",
  "city": "Hanoi",
  "locations": [...]
}
```

---

## 🤖 AI Analysis Endpoints

### Analyze Correlation

**Endpoint**: `POST /api/ai/analyze/correlation`

**Request Body**:
```json
{
  "analysis_type": "correlation",
  "title": "Environment vs Education Analysis",
  "description": "Analyze correlation between air quality and education scores",
  "env_values": [50, 60, 70, 80, 90],
  "edu_scores": [75, 78, 72, 68, 65]
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/analyze/correlation" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "correlation",
    "env_values": [50, 60, 70, 80, 90],
    "edu_scores": [75, 78, 72, 68, 65]
  }'
```

**Response**:
```json
{
  "correlation_coefficient": -0.854,
  "p_value": 0.0512,
  "slope": -0.35,
  "intercept": 94.5,
  "r_squared": 0.729,
  "interpretation": "Mối tương quan mạnh",
  "recommendation": "Môi trường tốt nhưng giáo dục yếu - cần tăng cường giáo dục"
}
```

---

### Analyze Ward

**Endpoint**: `POST /api/ai/analyze/ward`

**Parameters**:
- `ward_name` (string, query): Name of the ward
- `air_quality_data` (array, body): Air quality measurements
- `school_data` (array, body): School performance data
- `energy_data` (array, body): Energy data

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ai/analyze/ward?ward_name=Hoàn%20Kiếm" \
  -H "Content-Type: application/json" \
  -d '{
    "air_quality_data": [{"aqi": 65.5}],
    "school_data": [{"avg_score": 0.75}],
    "energy_data": [{"renewable_percentage": 30}]
  }'
```

**Response**:
```json
{
  "success": true,
  "data": {
    "ward": "Hoàn Kiếm",
    "correlations": {
      "environment_education": 0.45,
      "energy_environment": 0.32
    },
    "recommendations": [...],
    "confidence": 0.38
  }
}
```

---

### Cluster Wards

**Endpoint**: `POST /api/ai/cluster/wards`

**Request Body**:
```json
[
  {
    "name": "Hoàn Kiếm",
    "aqi": 65.5,
    "avg_school_score": 0.75,
    "renewable_energy": 30,
    "num_schools": 15
  },
  ...
]
```

**Response**:
```json
{
  "success": true,
  "clusters": {
    "0": ["Hoàn Kiếm", "Ba Đình"],
    "1": ["Đống Đa", "Hai Bà Trưng"]
  },
  "n_clusters": 2
}
```

---

### Predict Impact

**Endpoint**: `GET /api/ai/predict/impact`

**Parameters**:
- `action` (string): Action type (tree_planting, solar_installation, green_education)
- `current_aqi` (int): Current AQI level (default: 100)
- `current_energy` (float): Current energy percentage (default: 50.0)

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/ai/predict/impact?action=tree_planting&current_aqi=100"
```

**Response**:
```json
{
  "action": "tree_planting",
  "current_metrics": {
    "aqi": 100,
    "energy_percentage": 50.0
  },
  "predicted_impact": {
    "aqi_reduction": 5.0,
    "co2_reduction": 50,
    "timeline": "1-2 years"
  }
}
```

---

### List Analysis Results

**Endpoint**: `GET /api/ai/results`

**Parameters**:
- `skip` (int): Offset (default: 0)
- `limit` (int): Limit (default: 10)
- `analysis_type` (string): Filter by type (optional)

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/ai/results?skip=0&limit=10&analysis_type=correlation"
```

---

### Get Specific Result

**Endpoint**: `GET /api/ai/results/{id}`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/ai/results/1"
```

---

## ⚡ System Endpoints

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok"
}
```

---

### API Info

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "GreenEduMap API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 📊 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request |
| 404  | Not Found |
| 500  | Server Error |

---

## 🔧 Error Handling

### Common Error Responses

**Validation Error** (400):
```json
{
  "detail": [
    {
      "loc": ["body", "env_values"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Not Found** (404):
```json
{
  "detail": "Air quality record not found"
}
```

**Server Error** (500):
```json
{
  "detail": "Internal server error"
}
```

---

## 📖 Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🚀 Usage Examples

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

# Get air quality
response = requests.get(f"{BASE_URL}/api/air-quality/")
data = response.json()

# Create analysis
payload = {
    "analysis_type": "correlation",
    "env_values": [50, 60, 70],
    "edu_scores": [75, 78, 72]
}
response = requests.post(
    f"{BASE_URL}/api/ai/analyze/correlation",
    json=payload
)
result = response.json()
```

### JavaScript/TypeScript

```typescript
// Using fetch API
const response = await fetch(
  'http://localhost:8000/api/air-quality/'
);
const data = await response.json();

// Using custom API client
import { api } from '@/lib/api';

const airQuality = await api.get('/api/air-quality/');
const analysis = await api.post('/api/ai/analyze/correlation', {
  env_values: [50, 60, 70],
  edu_scores: [75, 78, 72]
});
```

---

## 📝 Rate Limiting (Future)

Will be implemented with following limits:
- 100 requests/minute for public endpoints
- 500 requests/minute for authenticated users

---

**API Version**: 1.0.0  
**Last Updated**: November 2024
