# GreenEduMap API Documentation

**Version:** 1.0  
**Base URL:** `https://api.greenedumap.io.vn/api/v1`  
**Authentication:** Bearer Token (JWT)

---

## Table of Contents

1. [Authentication](#authentication)
2. [User Data](#user-data)
3. [Environment Data](#environment-data)
4. [Education Data](#education-data)
5. [Green Resources](#green-resources)
6. [Public Endpoints](#public-endpoints)
7. [AI Tasks](#ai-tasks)
8. [Error Codes](#error-codes)

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

### GET /auth/validate-token

Validate if the current access token is still valid.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user_id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "role": "citizen",
  "is_active": true,
  "checked_at": "2025-12-05T12:00:00Z"
}
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Could not validate credentials"
}
```

---

### GET /users

List all users (Admin only).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)
- `role` (string, optional): Filter by user role (citizen, volunteer, developer, school, admin)

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "citizen",
    "is_active": true,
    "created_at": "2025-12-05T12:00:00Z"
  }
]
```

---

### GET /users/{user_id}

Get user by ID.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Note:** Users can only view their own profile unless they are admin.

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "phone": "+84901234567",
  "role": "citizen",
  "is_active": true,
  "created_at": "2025-12-05T12:00:00Z",
  "updated_at": "2025-12-05T12:30:00Z"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Not authorized to view this user"
}
```

---

### DELETE /users/{user_id}

Delete user (Admin only). Performs soft delete by setting `is_active = false`.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

---

### POST /api-keys

Create new API key for developers.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Note:** Only users with role `developer` or `admin` can create API keys.

**Request:**
```json
{
  "name": "Production API Key",
  "scopes": "read",
  "rate_limit": 1000
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "name": "Production API Key",
  "api_key": "geem_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "key_prefix": "geem_a1b",
  "scopes": "read",
  "rate_limit": 1000,
  "created_at": "2025-12-05T12:00:00Z"
}
```

**Warning:** The `api_key` field contains the plain API key which is only shown once. Store it securely!

---

### POST /api/v1/fcm-tokens

Register or update FCM token for push notifications.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "token": "fcm_registration_token_from_device",
  "device_type": "ios",
  "device_name": "iPhone 14 Pro",
  "device_id": "unique-device-identifier"
}
```

**Parameters:**
- `token` (string, required): FCM registration token from iOS/Android device
- `device_type` (string, required): Device platform - `ios`, `android`, or `web`
- `device_name` (string, optional): Human-readable device name
- `device_id` (string, optional): Unique device identifier

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "token": "fcm_registration_token...",
  "device_type": "ios",
  "device_name": "iPhone 14 Pro",
  "is_active": true,
  "notification_count": 0,
  "last_used": null,
  "created_at": "2025-12-09T10:00:00Z",
  "updated_at": "2025-12-09T10:00:00Z"
}
```

---

### GET /api/v1/fcm-tokens

List all FCM tokens for current user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "total": 2,
  "tokens": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "token": "fcm_token...",
      "device_type": "ios",
      "device_name": "iPhone 14 Pro",
      "is_active": true,
      "notification_count": 15,
      "last_used": "2025-12-09T09:30:00Z",
      "created_at": "2025-12-05T10:00:00Z",
      "updated_at": "2025-12-09T09:30:00Z"
    }
  ]
}
```

---

### DELETE /api/v1/fcm-tokens/{token_id}

Deactivate an FCM token.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "FCM token deactivated successfully"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "FCM token not found"
}
```

---

### POST /api/v1/notifications/send

Send push notification to user's devices.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "user_id": "uuid",
  "title": "New Update Available",
  "body": "Check out the new air quality data for your area",
  "data": {
    "type": "air_quality_update",
    "resource_id": "zone_123",
    "action": "open_map"
  },
  "image_url": "https://example.com/notification-image.jpg",
  "sound": "default"
}
```

**Parameters:**
- `user_id` (uuid, optional): Target user ID. If not provided, sends to current user. Only admins can specify other users.
- `title` (string, required): Notification title (max 100 chars)
- `body` (string, required): Notification body (max 500 chars)
- `data` (object, optional): Custom data payload for app handling
- `image_url` (string, optional): URL of notification image
- `sound` (string, optional): Notification sound (default: "default")

**Response (200 OK):**
```json
{
  "success": true,
  "sent_count": 2,
  "failed_count": 0,
  "message": "Sent to 2 device(s), 0 failed",
  "details": null
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Only admins can send notifications to other users"
}
```

**Note:** Regular users can only send notifications to themselves. Admins can send to any user by specifying `user_id`.

---

## User Data

API endpoints for managing user-specific data including favorites, contributions, activities, and settings.

### GET /api/v1/user-data/favorites

Get user's favorite locations (green zones, schools, etc.).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `item_type` (string, optional): Filter by type - `green_zone`, `school`, `center`, `air_quality_station`
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "item_type": "green_zone",
    "item_id": "uuid",
    "item_name": "Công viên 29/3",
    "notes": "Khu vực yêu thích để chạy bộ buổi sáng",
    "created_at": "2025-12-05T12:00:00Z"
  }
]
```

---

### POST /api/v1/user-data/favorites

Add a new favorite location.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "item_type": "green_zone",
  "item_id": "uuid-of-the-item",
  "item_name": "Công viên 29/3",
  "notes": "Khu vực yêu thích"
}
```

**Parameters:**
- `item_type` (string, required): Type of item - `green_zone`, `school`, `center`, `air_quality_station`
- `item_id` (uuid, required): ID of the item to favorite
- `item_name` (string, required): Name of the item for display
- `notes` (string, optional): Personal notes about this favorite

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "item_type": "green_zone",
  "item_id": "uuid",
  "item_name": "Công viên 29/3",
  "notes": "Khu vực yêu thích",
  "created_at": "2025-12-05T12:00:00Z"
}
```

---

### DELETE /api/v1/user-data/favorites/{favorite_id}

Remove a favorite.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (204 No Content)**

---

### GET /api/v1/user-data/contributions

Get user's contributions (reports, suggestions, data submissions).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `contribution_type` (string, optional): Filter by type - `report`, `suggestion`, `data_submission`, `review`
- `status` (string, optional): Filter by status - `pending`, `approved`, `rejected`
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "contribution_type": "report",
    "title": "Báo cáo chất lượng không khí",
    "description": "Phát hiện khói bụi nhiều tại khu vực...",
    "location_name": "Quận 1, TP.HCM",
    "latitude": 10.7769,
    "longitude": 106.7009,
    "status": "approved",
    "admin_notes": "Đã xác minh và cập nhật dữ liệu",
    "points_earned": 50,
    "created_at": "2025-12-05T12:00:00Z",
    "reviewed_at": "2025-12-06T10:00:00Z"
  }
]
```

---

### POST /api/v1/user-data/contributions

Submit a new contribution.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "contribution_type": "report",
  "title": "Báo cáo ô nhiễm",
  "description": "Phát hiện khói bụi nhiều tại...",
  "location_name": "Quận 1, TP.HCM",
  "latitude": 10.7769,
  "longitude": 106.7009,
  "extra_data": {
    "severity": "high",
    "photo_urls": ["https://example.com/photo1.jpg"]
  }
}
```

**Parameters:**
- `contribution_type` (string, required): Type - `report`, `suggestion`, `data_submission`, `review`
- `title` (string, required): Title of contribution
- `description` (string, optional): Detailed description
- `location_name` (string, optional): Name of location
- `latitude` (float, optional): Latitude coordinate
- `longitude` (float, optional): Longitude coordinate
- `extra_data` (object, optional): Additional data as JSON

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "contribution_type": "report",
  "title": "Báo cáo ô nhiễm",
  "status": "pending",
  "created_at": "2025-12-05T12:00:00Z"
}
```

---

### GET /api/v1/user-data/contributions/public

Get all approved public contributions (no authentication required for viewing).

**Query Parameters:**
- `contribution_type` (string, optional): Filter by type
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "contribution_type": "report",
    "title": "Báo cáo chất lượng không khí",
    "description": "Phát hiện khói bụi nhiều...",
    "location_name": "Quận 1, TP.HCM",
    "status": "approved",
    "created_at": "2025-12-05T12:00:00Z"
  }
]
```

---

### PATCH /api/v1/user-data/contributions/{contribution_id}/review

Review and approve/reject a contribution (Admin only).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "status": "approved",
  "admin_notes": "Đã xác minh thông tin",
  "points_earned": 50
}
```

**Parameters:**
- `status` (string, required): New status - `approved` or `rejected`
- `admin_notes` (string, optional): Admin notes for the contributor
- `points_earned` (int, optional): Reward points for approved contributions

**Response (200 OK):**
```json
{
  "id": "uuid",
  "status": "approved",
  "admin_notes": "Đã xác minh thông tin",
  "points_earned": 50,
  "reviewed_at": "2025-12-06T10:00:00Z"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Only admins can review contributions"
}
```

---

### GET /api/v1/user-data/activities

Get user's activity history.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `activity_type` (string, optional): Filter by type - `login`, `view`, `favorite`, `contribute`, `share`
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Number of records to return

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "activity_type": "view",
    "description": "Xem thông tin Công viên 29/3",
    "resource_type": "green_zone",
    "resource_id": "uuid",
    "ip_address": "x.x.x.x",
    "user_agent": "Mozilla/5.0...",
    "created_at": "2025-12-05T12:00:00Z"
  }
]
```

---

### POST /api/v1/user-data/activities

Log a new user activity.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "activity_type": "view",
  "description": "Xem thông tin công viên",
  "resource_type": "green_zone",
  "resource_id": "uuid-of-resource"
}
```

**Parameters:**
- `activity_type` (string, required): Type - `login`, `view`, `favorite`, `contribute`, `share`
- `description` (string, optional): Description of activity
- `resource_type` (string, optional): Type of resource accessed
- `resource_id` (uuid, optional): ID of resource accessed

**Response (201 Created):**
```json
{
  "id": "uuid",
  "activity_type": "view",
  "description": "Xem thông tin công viên",
  "created_at": "2025-12-05T12:00:00Z"
}
```

---

### GET /api/v1/user-data/settings

Get user's personal settings.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "user_id": "uuid",
  "theme": "dark",
  "language": "vi",
  "notifications_enabled": true,
  "email_notifications": true,
  "push_notifications": true,
  "default_city": "TP. Hồ Chí Minh",
  "default_latitude": 10.7769,
  "default_longitude": 106.7009,
  "aqi_alert_threshold": 100,
  "weather_units": "metric",
  "map_style": "satellite",
  "privacy_mode": false,
  "data_sharing": true,
  "updated_at": "2025-12-05T12:00:00Z"
}
```

---

### PUT /api/v1/user-data/settings

Update user's personal settings.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "theme": "dark",
  "language": "vi",
  "notifications_enabled": true,
  "email_notifications": true,
  "push_notifications": true,
  "default_city": "Đà Nẵng",
  "default_latitude": 16.0678,
  "default_longitude": 108.2208,
  "aqi_alert_threshold": 150,
  "weather_units": "metric",
  "map_style": "satellite",
  "privacy_mode": false,
  "data_sharing": true
}
```

**Parameters:**
- `theme` (string, optional): UI theme - `light`, `dark`, `system`
- `language` (string, optional): UI language - `vi`, `en`
- `notifications_enabled` (bool, optional): Enable all notifications
- `email_notifications` (bool, optional): Enable email notifications
- `push_notifications` (bool, optional): Enable push notifications
- `default_city` (string, optional): Default city for data display
- `default_latitude` (float, optional): Default latitude
- `default_longitude` (float, optional): Default longitude
- `aqi_alert_threshold` (int, optional): AQI value to trigger alerts (50-500)
- `weather_units` (string, optional): Temperature units - `metric`, `imperial`
- `map_style` (string, optional): Map style - `default`, `satellite`, `terrain`
- `privacy_mode` (bool, optional): Hide activity from public
- `data_sharing` (bool, optional): Allow anonymous data sharing for research

**Response (200 OK):**
```json
{
  "user_id": "uuid",
  "theme": "dark",
  "language": "vi",
  "notifications_enabled": true,
  "default_city": "Đà Nẵng",
  "updated_at": "2025-12-05T14:00:00Z"
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

### GET /api/v1/air-quality/location

Get air quality measurements near a specific location.

**Query Parameters:**
- `lat` (float, required): Latitude (-90 to 90)
- `lon` (float, required): Longitude (-180 to 180)
- `radius` (int, optional): Search radius in kilometers (default: 50, max: 200)
- `limit` (int, optional): Maximum number of results (default: 10, max: 100)

**Response (200 OK):**
```json
{
  "location": {
    "lat": 10.7769,
    "lon": 106.7009
  },
  "radius_km": 50,
  "total": 5,
  "data": [
    {
      "id": "uuid",
      "latitude": 10.7769,
      "longitude": 106.7009,
      "station_name": "Quận 1 - TPHCM",
      "aqi": 85,
      "pm25": 35.5,
      "pm10": 55.2,
      "co": 0.8,
      "no2": 25.3,
      "so2": 10.1,
      "o3": 45.6,
      "measurement_date": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/v1/air-quality/history

Get historical air quality data for a location.

**Query Parameters:**
- `lat` (float, required): Latitude (-90 to 90)
- `lon` (float, required): Longitude (-180 to 180)
- `days` (int, optional): Number of days of history (default: 7, max: 90)
- `radius` (int, optional): Search radius in kilometers (default: 10, max: 50)

**Response (200 OK):**
```json
{
  "location": {
    "lat": 10.7769,
    "lon": 106.7009
  },
  "period": {
    "start": "2025-11-28T12:00:00Z",
    "end": "2025-12-05T12:00:00Z"
  },
  "total": 42,
  "data": [
    {
      "id": "uuid",
      "latitude": 10.7769,
      "longitude": 106.7009,
      "aqi": 85,
      "pm25": 35.5,
      "measurement_date": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### POST /api/v1/air-quality/fetch

Manually trigger fetching air quality data from OpenAQ API (Admin endpoint).

**Query Parameters:**
- `lat` (float, required): Latitude (-90 to 90)
- `lon` (float, required): Longitude (-180 to 180)
- `radius` (int, optional): Search radius in kilometers (default: 50, max: 100)

**Response (200 OK):**
```json
{
  "status": "success",
  "fetched": 10,
  "saved": 10
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Error message from OpenAQ API"
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

### GET /api/v1/weather/location

Get weather observations near a specific location.

**Query Parameters:**
- `lat` (float, required): Latitude (-90 to 90)
- `lon` (float, required): Longitude (-180 to 180)
- `radius` (int, optional): Search radius in kilometers (default: 50, max: 200)
- `hours` (int, optional): Hours of history to retrieve (default: 24, max: 168)

**Response (200 OK):**
```json
{
  "location": {
    "lat": 10.7769,
    "lon": 106.7009
  },
  "radius_km": 50,
  "total": 15,
  "data": [
    {
      "id": "uuid",
      "latitude": 10.7769,
      "longitude": 106.7009,
      "city_name": "Ho Chi Minh City",
      "temperature": 32.5,
      "feels_like": 35.2,
      "humidity": 75,
      "pressure": 1012,
      "wind_speed": 15.5,
      "weather_description": "Partly cloudy",
      "observation_time": "2025-12-05T12:00:00Z"
    }
  ]
}
```

---

### GET /api/v1/weather/forecast

Get 5-day weather forecast with 3-hour intervals.

**Query Parameters:**
- `lat` (float, required): Latitude
- `lon` (float, required): Longitude

**Response (200 OK):**
```json
{
  "city": {
    "name": "Ho Chi Minh City",
    "country": "VN"
  },
  "forecast": [
    {
      "datetime": "2025-12-06T00:00:00Z",
      "temperature": 28.5,
      "feels_like": 31.2,
      "humidity": 80,
      "weather_main": "Rain",
      "weather_description": "light rain",
      "rain_3h": 2.5
    }
  ]
}
```

---

### WebSocket Endpoints

#### WS /ws/air-quality

Real-time air quality updates via WebSocket.

**Connection:**
```javascript
const ws = new WebSocket('wss://api.greenedumap.io.vn/ws/air-quality');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('AQI Update:', data);
};
```

**Message Format:**
```json
{
  "type": "aqi_update",
  "station_name": "Quận 1 - TPHCM",
  "aqi": 85,
  "pm25": 35.5,
  "timestamp": "2025-12-05T12:00:00Z"
}
```

---

#### WS /ws/weather

Real-time weather updates via WebSocket.

**Connection:**
```javascript
const ws = new WebSocket('wss://api.greenedumap.io.vn/ws/weather');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Weather Update:', data);
};
```

**Message Format:**
```json
{
  "type": "weather_update",
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
