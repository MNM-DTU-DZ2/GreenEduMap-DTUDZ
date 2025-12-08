# GreenEduMap API Documentation

**Version:** 1.0  
**Base URL:** `https://api.greenedumap.io.vn/api/v1`  
**Authentication:** Bearer Token (JWT)

---

## Table of Contents

1. [Authentication](#authentication)
2. [Environment Data](#environment-data)
3. [Education Data](#education-data)
4. [Green Resources](#green-resources)
5. [Public Endpoints](#public-endpoints)
6. [AI Tasks](#ai-tasks)
7. [Error Codes](#error-codes)

---

## Authentication

### POST /auth/register

Register a new user account.

**Request:**
```json
{
  "username": "johndoe",
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe",
  "phone": "+84901234567"
}
```

**Note:** Password must be at least 8 characters.

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2025-12-05T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### POST /auth/login

Login to existing account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Note:** Login uses email, not username.

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### POST /auth/refresh

Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### GET /auth/me

Get current user profile.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+84901234567",
  "created_at": "2025-12-05T12:00:00Z",
  "updated_at": "2025-12-05T12:00:00Z"
}
```

---

### PATCH /auth/profile

Update user profile.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "full_name": "John Smith",
  "phone": "+84901234567"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Smith",
  "phone": "+84901234567",
  "updated_at": "2025-12-05T12:30:00Z"
}
```

---

## Environment Data

### GET /api/v1/air-quality

Get air quality data with pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 10, max: 100)
- `city` (string, optional): Filter by city name

**Response (200 OK):**
```json
{
  "total": 150,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "station_name": "Quận 1 - TPHCM",
      "city": "Ho Chi Minh City",
      "latitude": 10.7769,
      "longitude": 106.7009,
      "aqi": 85,
      "pm25": 35.5,
      "pm10": 55.2,
      "co": 0.8,
      "no2": 25.3,
      "so2": 10.1,
      "o3": 45.6,
      "timestamp": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/v1/air-quality/latest

Get latest air quality data (last 24 hours).

**Query Parameters:**
- `limit` (int, optional): Number of records (default: 10)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "station_name": "Quận 1 - TPHCM",
      "aqi": 85,
      "pm25": 35.5,
      "category": "Moderate",
      "timestamp": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/v1/air-quality/{item_id}

Get specific air quality record by ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "station_name": "Quận 1 - TPHCM",
  "city": "Ho Chi Minh City",
  "latitude": 10.7769,
  "longitude": 106.7009,
  "aqi": 85,
  "pm25": 35.5,
  "pm10": 55.2,
  "co": 0.8,
  "no2": 25.3,
  "so2": 10.1,
  "o3": 45.6,
  "timestamp": "2025-12-05T12:00:00Z"
}
```

---

### GET /api/v1/weather

Get weather data with pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "city_name": "Ho Chi Minh City",
      "latitude": 10.8231,
      "longitude": 106.6297,
      "temperature": 32.5,
      "humidity": 75,
      "pressure": 1012,
      "wind_speed": 15.5,
      "weather_description": "Partly cloudy",
      "timestamp": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/v1/weather/current

Get current weather data.

**Query Parameters:**
- `lat` (float, optional): Latitude
- `lon` (float, optional): Longitude  
- `city` (string, optional): City name (alternative to lat/lon)
- `fetch_new` (boolean, optional): Force fetch new data from OpenWeather API

**Note:** Use either lat/lon OR city. Parameter `fetch_new=true` recommended to get fresh data.

**Response (200 OK):**
```json
{
  "city_name": "Ho Chi Minh City",
  "temperature": 32.5,
  "humidity": 75,
  "weather_description": "Partly cloudy",
  "timestamp": "2025-12-05T12:00:00Z"
}
```

---

## Education Data

### GET /api/v1/schools

Get list of schools with pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return
- `district` (string, optional): Filter by district
- `city` (string, optional): Filter by city

**Response (200 OK):**
```json
{
  "total": 500,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Trường THPT Lê Hồng Phong",
      "address": "240 Nguyễn Thị Minh Khai, Quận 3",
      "district": "Quận 3",
      "city": "Ho Chi Minh City",
      "latitude": 10.7881,
      "longitude": 106.6917,
      "school_type": "High School",
      "green_score": 85.5,
      "total_students": 1200,
      "has_green_program": true
    }
  ]
}
```

---

### GET /api/v1/schools/nearby

Get schools near a location.

**Query Parameters:**
- `latitude` (float, required): Latitude
- `longitude` (float, required): Longitude
- `radius_km` (float, optional): Search radius in km (default: 5)
- `limit` (int, optional): Number of results (default: 10)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Trường THPT Lê Hồng Phong",
      "distance": 1.5,
      "latitude": 10.7881,
      "longitude": 106.6917,
      "green_score": 85.5
    }
  ]
}
```

---

### GET /api/v1/schools/{school_id}

Get detailed information about a specific school.

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Trường THPT Lê Hồng Phong",
  "address": "240 Nguyễn Thị Minh Khai, Quận 3",
  "district": "Quận 3",
  "city": "Ho Chi Minh City",
  "latitude": 10.7881,
  "longitude": 106.6917,
  "school_type": "High School",
  "green_score": 85.5,
  "total_students": 1200,
  "has_green_program": true,
  "green_initiatives": [
    "Solar panels",
    "Recycling program",
    "Green garden"
  ],
  "contact": {
    "phone": "+84283932xxxx",
    "email": "info@lehongphong.edu.vn"
  }
}
```

---

### GET /api/v1/green-courses

Get list of green/environmental courses.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "title": "Environmental Science Basics",
      "description": "Introduction to environmental science",
      "school_id": 1,
      "school_name": "Trường THPT Lê Hồng Phong",
      "duration_hours": 40,
      "level": "Beginner"
    }
  ]
}
```

---

## Green Resources

### GET /api/open-data/green-zones

Get list of green zones (parks, forests, etc.).

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return
- `zone_type` (string, optional): Filter by zone type (park, forest, garden)

**Response (200 OK):**
```json
{
  "total": 100,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Công viên Tao Đàn",
      "zone_type": "park",
      "district": "Quận 1",
      "city": "Ho Chi Minh City",
      "area_sqm": 100000,
      "tree_count": 500,
      "latitude": 10.7789,
      "longitude": 106.6944
    }
  ]
}
```

---

### GET /api/open-data/green-zones/nearby

Get green zones near a location.

**Query Parameters:**
- `latitude` (float, required): Latitude
- `longitude` (float, required): Longitude
- `radius` (float, optional): Search radius in km (default: 5)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Công viên Tao Đàn",
      "distance": 0.8,
      "zone_type": "park",
      "area_sqm": 100000
    }
  ]
}
```

---

### GET /api/open-data/green-resources

Get list of green resources (renewable energy, recycling centers, etc.).

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return
- `type` (string, optional): Filter by resource type

**Response (200 OK):**
```json
{
  "total": 75,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Solar Panel Installation",
      "type": "renewable_energy",
      "location": "Quận 1",
      "capacity": "500 kW",
      "status": "active"
    }
  ]
}
```

---

### GET /api/v1/green-zones

Get list of green zones (authenticated endpoint).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
{
  "total": 100,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Công viên Tao Đàn",
      "zone_type": "park",
      "district": "Quận 1",
      "city": "Ho Chi Minh City",
      "area_sqm": 100000,
      "tree_count": 500,
      "latitude": 10.7789,
      "longitude": 106.6944
    }
  ]
}
```

---

### GET /api/v1/green-zones/{zone_id}

Get specific green zone details (authenticated endpoint).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Công viên Tao Đàn",
  "zone_type": "park",
  "district": "Quận 1",
  "city": "Ho Chi Minh City",
  "area_sqm": 100000,
  "tree_count": 500,
  "latitude": 10.7789,
  "longitude": 106.6944,
  "description": "Historic park in District 1",
  "facilities": ["playground", "walking paths", "benches"]
}
```

---

### GET /api/v1/green-resources

Get list of green resources (authenticated endpoint).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
{
  "total": 75,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Solar Panel Installation",
      "type": "renewable_energy",
      "location": "Quận 1",
      "capacity": "500 kW",
      "status": "active"
    }
  ]
}
```

---

### GET /api/v1/green-resources/{resource_id}

Get specific green resource details (authenticated endpoint).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Solar Panel Installation",
  "type": "renewable_energy",
  "location": "Quận 1",
  "capacity": "500 kW",
  "status": "active",
  "description": "Rooftop solar installation",
  "installation_date": "2024-01-15"
}
```

---

### GET /api/v1/centers

Get list of recycling centers (authenticated endpoint).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Green Recycling Center",
      "type": "recycling",
      "address": "123 Nguyen Hue, District 1",
      "latitude": 10.7769,
      "longitude": 106.7009,
      "accepted_materials": ["plastic", "paper", "glass", "metal"]
    }
  ]
}
```

---

## Public Endpoints

### GET /api/open-data/air-quality

Public air quality data (no authentication required).

**Query Parameters:**
- `city` (string, optional): Filter by city
- `limit` (int, optional): Number of records

**Response (200 OK):**
```json
{
  "data": [
    {
      "station_name": "Quận 1 - TPHCM",
      "aqi": 85,
      "category": "Moderate",
      "timestamp": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/open-data/air-quality/location

Public air quality data near a specific location (no authentication required).

**Query Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude
- `radius` (int, optional): Search radius in km (default: 50, max: 200)

**Response (200 OK):**
```json
{
  "data": [
    {
      "station_name": "Quận 1 - TPHCM",
      "aqi": 85,
      "category": "Moderate",
      "distance": 2.5,
      "timestamp": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/open-data/weather/current

Public current weather data (no authentication required).

**Query Parameters:**
- `lat` (float, optional): Latitude
- `lon` (float, optional): Longitude
- `city` (string, optional): City name (alternative to lat/lon)

**Note:** Use either lat/lon OR city.

**Response (200 OK):**
```json
{
  "city_name": "Ho Chi Minh City",
  "temperature": 32.5,
  "humidity": 75,
  "weather_description": "Partly cloudy"
}
```

---

### GET /api/open-data/weather/forecast

Public weather forecast (7 days, no authentication required).

**Query Parameters:**
- `lat` (float, optional): Latitude
- `lon` (float, optional): Longitude
- `city` (string, optional): City name (alternative to lat/lon)

**Note:** Use either lat/lon OR city.

**Response (200 OK):**
```json
{
  "city_name": "Ho Chi Minh City",
  "forecast": [
    {
      "date": "2025-12-06",
      "temperature_max": 34,
      "temperature_min": 26,
      "humidity": 70,
      "weather_description": "Sunny"
    }
  ]
}
```

---

### GET /api/open-data/catalog

Get open data catalog.

**Response (200 OK):**
```json
{
  "datasets": [
    {
      "name": "Air Quality Data",
      "description": "Real-time air quality monitoring",
      "endpoint": "/api/open-data/air-quality",
      "update_frequency": "hourly"
    },
    {
      "name": "School Directory",
      "description": "List of schools with green programs",
      "endpoint": "/api/v1/schools",
      "update_frequency": "daily"
    }
  ]
}
```

**Note:** This endpoint currently returns sample/placeholder data and is under active development.

---

### GET /api/open-data/centers

Get public recycling centers (no authentication required).

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
{
  "total": 50,
  "skip": 0,
  "limit": 10,
  "data": [
    {
      "id": 1,
      "name": "Green Recycling Center",
      "type": "recycling",
      "address": "123 Nguyen Hue, District 1",
      "latitude": 10.7769,
      "longitude": 106.7009,
      "accepted_materials": ["plastic", "paper", "glass", "metal"]
    }
  ]
}
```

---

### GET /api/open-data/centers/nearby

Get recycling centers near a location (no authentication required).

**Query Parameters:**
- `latitude` (float, required): Latitude
- `longitude` (float, required): Longitude
- `radius_km` (float, optional): Search radius in km (default: 10, max: 100)

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Green Recycling Center",
      "distance": 1.2,
      "address": "123 Nguyen Hue, District 1",
      "accepted_materials": ["plastic", "paper", "glass", "metal"]
    }
  ]
}
```

---

### GET /api/open-data/export/air-quality

Export air quality data in multiple formats (no authentication required).

**Query Parameters:**
- `format` (string, optional): Export format - `json`, `csv`, or `geojson` (default: json)

**Response (200 OK):**
```json
{
  "message": "Export feature coming soon",
  "format": "json",
  "service": "export-service"
}
```

**Note:** This endpoint is currently a placeholder and will be fully implemented in a future release.

---

## AI Tasks

### POST /api/v1/tasks/ai/clustering

Queue AI clustering task for data analysis.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "data_type": "environment",
  "n_clusters": 3,
  "method": "kmeans"
}
```

**Response (200 OK):**
```json
{
  "status": "queued",
  "task_id": "task_uuid_123"
}
```

---

### POST /api/v1/tasks/ai/prediction

Queue AI prediction task (e.g., air quality forecast).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "prediction_type": "air_quality",
  "location_id": "location_uuid"
}
```

**Response (200 OK):**
```json
{
  "status": "queued",
  "task_id": "task_uuid_456"
}
```

---

### POST /api/v1/tasks/ai/correlation

Queue AI correlation analysis task.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "analysis_type": "pearson"
}
```

**Response (200 OK):**
```json
{
  "status": "queued",
  "task_id": "task_uuid_789"
}
```

---

### POST /api/v1/tasks/export

Queue data export task.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "data_type": "schools",
  "format": "csv"
}
```

**Response (200 OK):**
```json
{
  "status": "queued",
  "task_id": "task_uuid_export_123"
}
```

---

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Missing or invalid authentication token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service temporarily unavailable |

---

### Error Response Format

```json
{
  "detail": "Error message description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2025-12-05T12:00:00Z"
}
```

---

### Common Error Codes

| Error Code | Description |
|------------|-------------|
| `INVALID_CREDENTIALS` | Invalid email or password |
| `TOKEN_EXPIRED` | Access token has expired |
| `TOKEN_INVALID` | Invalid or malformed token |
| `USER_NOT_FOUND` | User account not found |
| `EMAIL_ALREADY_EXISTS` | Email already registered |
| `VALIDATION_ERROR` | Request validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource not found |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `SERVICE_UNAVAILABLE` | Backend service unavailable |

---

## Rate Limiting

- **Public endpoints**: 100 requests per minute
- **Authenticated endpoints**: 300 requests per minute
- **AI task endpoints**: 10 requests per minute

Rate limit headers:
```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1733400000
```

---

## Pagination

All list endpoints support pagination with the following parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)

Response includes:
```json
{
  "total": 500,
  "skip": 0,
  "limit": 10,
  "data": []
}
```

---

## Filtering

Many endpoints support filtering via query parameters:

- `city`: Filter by city name
- `district`: Filter by district
- `type`: Filter by resource/zone type
- `latitude` & `longitude`: Geographic filtering

---

## Best Practices

1. **Always use HTTPS** for API requests
2. **Store tokens securely** - Never expose tokens in client-side code
3. **Implement token refresh** - Refresh tokens before they expire
4. **Handle errors gracefully** - Check status codes and error messages
5. **Respect rate limits** - Implement exponential backoff for retries
6. **Use pagination** - Don't request all data at once
7. **Cache responses** - Cache public data to reduce API calls

---

## Support

For API support, please contact:
- **Email**: dev@greenedumap.io.vn
- **GitHub**: https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ
- **Documentation**: https://greenedumap.io.vn/docs

---

**Last Updated**: December 5, 2025  
**API Version**: 1.0
