# GreenEduMap - Danh sách API Endpoints

## 📋 Tổng quan
**Tổng số endpoints:** 21  
**API Gateway:** `http://localhost:8000`  
**API Version:** v1

---

## 🏥 Health & System

### GET /
- **Mô tả:** Root endpoint - API Gateway info
- **Response:** Service name, version, status

### GET /health
- **Mô tả:** Health check cho tất cả microservices
- **Response:** Status của gateway và các services (auth, education, resource, environment)

---

## 🔐 Authentication (Day 8)

### POST /api/v1/auth/register
- **Mô tả:** Đăng ký user mới
- **Body:** `{ username, email, password, role, full_name? }`
- **Response:** `201 Created` - User object
- **Frontend:** `AuthContext.tsx`, `/auth/register`

### POST /api/v1/auth/login
- **Mô tả:** Đăng nhập  
- **Body:** `{ email, password }`
- **Response:** `200 OK` - `{ access_token, refresh_token, token_type, expires_in }`
- **Frontend:** `AuthContext.tsx`, `/auth/login`

### POST /api/v1/auth/refresh
- **Mô tả:** Refresh access token
- **Body:** `{ refresh_token }`
- **Response:** `200 OK` - New tokens

### GET /api/v1/auth/me
- **Mô tả:** Lấy thông tin user hiện tại
- **Headers:** `Authorization: Bearer {token}`
- **Response:** `200 OK` - User object
- **Frontend:** `AuthContext.tsx`, `/profile`

### PUT /api/v1/auth/profile
- **Mô tả:** Cập nhật profile user
- **Headers:** `Authorization: Bearer {token}`
- **Body:** `{ full_name?, phone?, is_public? }`
- **Response:** `200 OK` - Updated user

---

## 🏫 Schools (Education Service)

### GET /api/v1/schools
- **Mô tả:** Danh sách schools
- **Query params:** `limit?, skip?, search?`
- **Response:** Array of schools
- **Frontend:** `SchoolMap.tsx`, `SchoolSearch.tsx`, `test/page.tsx`

### GET /api/v1/schools/{school_id}
- **Mô tả:** Chi tiết 1 trường học
- **Response:** School object với reviews, courses, green_score
- **Frontend:** `schools/[id]/page.tsx`

### GET /api/v1/schools/nearby
- **Mô tả:** Tìm schools gần vị trí
- **Query params:** `latitude, longitude, radius?`
- **Response:** Array of nearby schools

### GET /api/v1/schools/{school_id}/reviews
- **Mô tả:** Lấy reviews của 1 trường
- **Response:** Array of reviews
- **Frontend:** `SchoolReviews.tsx`, `schools/[id]/page.tsx`

### POST /api/v1/schools/{school_id}/reviews
- **Mô tả:** Tạo review mới
- **Headers:** `Authorization: Bearer {token}` (optional)
- **Body:** `{ rating, comment, user_name }`
- **Response:** `201 Created` - Review object
- **Frontend:** `ReviewForm.tsx`

### GET /api/v1/schools/{school_id}/courses
- **Mô tả:** Lấy green courses của trường
- **Response:** Array of courses

### GET /api/v1/schools/{school_id}/green-score
- **Mô tả:** Tính green score
- **Response:** `{ green_score, breakdown }`

---

## 📚 Green Courses

### GET /api/v1/green-courses
- **Mô tả:** Danh sách tất cả green courses
- **Query params:** `school_id?, category?`
- **Response:** Array of courses

---

## 🌍 OpenData Endpoints

### GET /api/open-data/catalog
- **Mô tả:** OpenData catalog theo DCAT-AP format
- **Response:** RDF catalog

### GET /api/open-data/schools
- **Mô tả:** Schools GeoJSON
- **Response:** `{ type: "FeatureCollection", features: [...] }`
- **Frontend:** `SchoolMap.tsx`, `SchoolSearch.tsx`

### GET /api/open-data/centers
- **Mô tả:** Green centers GeoJSON
- **Response:** FeatureCollection

### GET /api/open-data/centers/nearby
- **Mô tả:** Tìm centers gần vị trí
- **Query params:** `latitude, longitude, radius?`
- **Response:** FeatureCollection

### GET /api/open-data/resources
- **Mô tả:** Green resources GeoJSON
- **Response:** FeatureCollection

### GET /api/open-data/air-quality
- **Mô tả:** Air quality data
- **Query params:** `start_date?, end_date?`
- **Response:** Array of AQI readings

### GET /api/open-data/air-quality/location
- **Mô tả:** AQI theo location
- **Query params:** `latitude, longitude`
- **Response:** AQI data

### GET /api/open-data/weather/current
- **Mô tả:** Current weather
- **Query params:** `latitude, longitude`
- **Response:** Weather data

### GET /api/open-data/weather/forecast
- **Mô tả:** Weather forecast
- **Query params:** `latitude, longitude, days?`
- **Response:** Forecast array

### GET /api/open-data/export/air-quality
- **Mô tả:** Export AQI data (CSV/JSON)
- **Query params:** `format=csv|json, start_date?, end_date?`
- **Response:** File download

---

## 📊 Frontend API Usage Summary

### Currently Used APIs:
1. **Auth APIs** (3/5): register, login, me ✅
2. **Schools APIs** (3/7): list, detail, reviews ✅  
3. **OpenData APIs** (1/10): schools GeoJSON ✅

### Not Yet Used in Frontend:
- Green courses
- Nearby schools/centers
- Air quality & weather
- Resources
- Auth profile update
- Auth refresh token

---

## 🔧 API Testing

**Test script:** `scripts/test/test-api.ps1`

**Test coverage:**
- ✅ Health check
- ✅ List schools
- ✅ Auth register
- ✅ Auth login
- ✅ Get current user

---

## 📝 Notes

- All endpoints support CORS
- JWT tokens expire in 30 minutes (1800s)
- Refresh tokens for long-lived sessions
- OpenData endpoints follow W3C standards (DCAT-AP, GeoJSON)
- Rate limiting: TBD
- API versioning: `/api/v1/...`

**Last updated:** 2025-12-02
