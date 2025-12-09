# GreenEduMap - Project Documentation

> **Tài liệu dự án đầy đủ cho Cursor AI và Developer**
> 
> Cập nhật lần cuối: 2025-12-05

---

## 📋 Mục Lục

1. [Tổng Quan Dự Án](#1-tổng-quan-dự-án)
2. [Kiến Trúc Hệ Thống](#2-kiến-trúc-hệ-thống)
3. [Chi Tiết Các Services](#3-chi-tiết-các-services)
4. [Database Schema](#4-database-schema)
5. [Message Brokers](#5-message-brokers)
6. [Tiến Độ Hoàn Thành](#6-tiến-độ-hoàn-thành)
7. [Công Việc Còn Lại](#7-công-việc-còn-lại)
8. [Hướng Dẫn Phát Triển](#8-hướng-dẫn-phát-triển)
9. [API Endpoints](#9-api-endpoints)
10. [Cấu Hình & Biến Môi Trường](#10-cấu-hình--biến-môi-trường)

---

## 1. Tổng Quan Dự Án

### 1.1 Giới Thiệu

**GreenEduMap** là nền tảng Open Data tích hợp dữ liệu **môi trường** và **giáo dục xanh** tại Việt Nam, phục vụ cuộc thi **OLP 2025 (Olympic Tin học Sinh viên)**.

### 1.2 Mục Tiêu Chính

1. **Thu thập dữ liệu môi trường** từ OpenAQ, OpenWeather và cảm biến IoT
2. **Quản lý thông tin trường học** với chỉ số Green Score
3. **Phân tích tương quan** giữa chất lượng môi trường và giáo dục xanh
4. **Cung cấp Open Data** theo chuẩn NGSI-LD/JSON-LD
5. **Trực quan hóa** trên bản đồ 2D/3D

### 1.3 Công Nghệ Sử Dụng

| Layer | Công nghệ |
|-------|-----------|
| **Frontend** | Next.js 14, React, TypeScript, Mapbox GL, TailwindCSS |
| **Backend** | FastAPI (Python 3.11), Uvicorn |
| **Database** | PostgreSQL 16 + PostGIS, Redis, MongoDB |
| **Message Broker** | RabbitMQ 3.13, EMQX 5.5 (MQTT) |
| **Container** | Docker, Docker Compose |
| **AI/ML** | Scikit-learn, NumPy, Pandas (planned) |

### 1.4 Cấu Trúc Thư Mục

```
GreenEduMap-DTUDZ/
├── infrastructure/
│   └── docker/
│       ├── docker-compose.yml      # Main compose file
│       ├── docker-compose.prod.yml # Production config
│       └── init-scripts/           # SQL initialization
│           ├── 01-init-postgis.sql
│           ├── 02-create-tables.sql
│           └── 03_education_schema.sql
│
├── modules/
│   ├── api-gateway/               # Central API Gateway
│   ├── auth-service/              # Authentication & Authorization
│   ├── education-service/         # Schools & Green Education
│   ├── environment-service/       # Air Quality & Weather
│   ├── resource-service/          # Green Zones & Resources
│   ├── shared/                    # Shared utilities
│   └── web-app/                   # Next.js Frontend
│
├── docs/                          # Documentation
├── scripts/                       # Utility scripts
└── PROJECT.md                     # This file
```

---

## 2. Kiến Trúc Hệ Thống

### 2.1 Sơ Đồ Tổng Quan

```
                                    ┌─────────────────────────────────────┐
                                    │           EXTERNAL APIs             │
                                    │  ┌─────────┐  ┌──────────────────┐  │
                                    │  │ OpenAQ  │  │ OpenWeatherMap   │  │
                                    │  └────┬────┘  └────────┬─────────┘  │
                                    └───────┼────────────────┼────────────┘
                                            │                │
                                            ▼                ▼
┌──────────────┐                  ┌─────────────────────────────────────────┐
│  IoT Sensors │──────MQTT───────►│         ENVIRONMENT-SERVICE             │
│  (AQI, Temp) │      1883        │  • Fetch external API data              │
└──────────────┘                  │  • MQTT Subscriber (sensors/#)          │
                                  │  • RabbitMQ Publisher (events)          │
                                  │  • Process & store environment data     │
                                  └───────────────────┬─────────────────────┘
                                                      │
                                                      │ RabbitMQ
                                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              MESSAGE BROKERS                                  │
│  ┌─────────────────────────────┐    ┌─────────────────────────────┐          │
│  │         RabbitMQ            │    │           EMQX              │          │
│  │  • environment.events       │    │  • sensors/air-quality/#    │          │
│  │  • ai.tasks                 │    │  • sensors/weather/#        │          │
│  │  • export.tasks             │    │  • realtime/aqi/#           │          │
│  │  • notifications            │    │  • realtime/map/update      │          │
│  └─────────────────────────────┘    └─────────────────────────────┘          │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
          ┌─────────────────────────────────┼─────────────────────────────────┐
          │                                 │                                 │
          ▼                                 ▼                                 ▼
┌─────────────────┐            ┌─────────────────────┐            ┌─────────────────┐
│   AI-SERVICE    │            │   EXPORT-SERVICE    │            │ NOTIFY-SERVICE  │
│   (Planned)     │            │     (Planned)       │            │   (Planned)     │
│  • Clustering   │            │  • CSV export       │            │  • Email        │
│  • Predictions  │            │  • GeoJSON export   │            │  • Push notif   │
│  • Correlation  │            │  • RDF/LOD export   │            │  • Webhooks     │
└─────────────────┘            └─────────────────────┘            └─────────────────┘

                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY (:8000)                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  • Rate Limiting (Redis)                                               │  │
│  │  • Request Routing                                                     │  │
│  │  • Authentication Verification                                         │  │
│  │  • Task Queue Publisher (RabbitMQ)                                     │  │
│  │  • OpenData endpoints (/api/open-data/*)                               │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└────────────────────┬─────────────────────────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┬───────────────┬───────────────┐
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
┌─────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│  AUTH   │   │ EDUCATION │   │ENVIRONMENT│   │ RESOURCE  │   │ OPENDATA  │
│ SERVICE │   │  SERVICE  │   │  SERVICE  │   │  SERVICE  │   │ SERVICE   │
│ (:8001) │   │  (:8008)  │   │  (:8007)  │   │  (:8002)  │   │ (Planned) │
└────┬────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └───────────┘
     │              │               │               │
     └──────────────┴───────────────┴───────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐               │
│  │   PostgreSQL    │  │     Redis       │  │    MongoDB      │               │
│  │   + PostGIS     │  │   (Cache)       │  │   (Logs/IoT)    │               │
│  │   (:5432)       │  │   (:6379)       │  │   (:27017)      │               │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘               │
└──────────────────────────────────────────────────────────────────────────────┘

                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                              WEB APPLICATION                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Next.js 14 + React + TypeScript + Mapbox GL                           │  │
│  │  • Interactive Map (2D/3D)                                             │  │
│  │  • School Dashboard                                                    │  │
│  │  • Environment Monitoring                                              │  │
│  │  • Admin Panel                                                         │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
1. DATA INGESTION:
   OpenAQ/OpenWeather ──► environment-service ──► PostgreSQL
   IoT Sensors ──MQTT──► environment-service ──► PostgreSQL + MongoDB

2. EVENT PROCESSING:
   environment-service ──RabbitMQ──► ai-service (clustering, prediction)
   api-gateway ──RabbitMQ──► export-service (CSV, GeoJSON)

3. REAL-TIME UPDATES:
   environment-service ──MQTT──► web-app (via WebSocket bridge)
   
4. API REQUESTS:
   web-app ──REST──► api-gateway ──► microservices ──► PostgreSQL
```

---

## 3. Chi Tiết Các Services

### 3.1 API Gateway (`modules/api-gateway/`)

**Chức năng:** Central routing, rate limiting, task publishing

**Files quan trọng:**
```
api-gateway/
├── app/
│   ├── main.py           # FastAPI app với lifespan management
│   ├── config.py         # Settings (service URLs, RabbitMQ)
│   ├── messaging.py      # RabbitMQ TaskPublisher
│   └── routes/
│       ├── auth.py       # Proxy to auth-service
│       ├── education.py  # Proxy to education-service
│       ├── resources.py  # Proxy to resource-service
│       └── public.py     # Public/OpenData endpoints
├── Dockerfile
└── requirements.txt
```

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (all services) |
| GET | `/api/open-data/*` | OpenData proxy |
| POST | `/api/v1/tasks/ai/clustering` | Queue AI clustering |
| POST | `/api/v1/tasks/ai/prediction` | Queue AI prediction |
| POST | `/api/v1/tasks/export` | Queue data export |

**RabbitMQ Exchanges:**
- `ai.tasks` (DIRECT) - AI processing tasks
- `export.tasks` (DIRECT) - Export tasks
- `notifications` (TOPIC) - Alert notifications

---

### 3.2 Auth Service (`modules/auth-service/`)

**Chức năng:** JWT authentication, user management

**Files quan trọng:**
```
auth-service/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py    # JWT, password hashing
│   ├── models.py          # User model
│   ├── schemas.py         # Pydantic schemas
│   └── services/
│       ├── auth.py        # Login, register, refresh
│       └── user.py        # User CRUD
└── requirements.txt
```

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login, get JWT |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/users/me` | Get current user |

---

### 3.3 Education Service (`modules/education-service/`)

**Chức năng:** School management, Green Score, courses

**Files quan trọng:**
```
education-service/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── api/
│   │   └── schools.py     # School CRUD, nearby search
│   ├── models/
│   │   ├── school.py      # School model (PostGIS geometry)
│   │   ├── green_course.py
│   │   ├── green_activity.py
│   │   └── enrollment.py
│   ├── schemas/
│   │   └── school.py      # Pydantic schemas
│   └── services/
│       └── green_score.py # Green score calculation
├── migrations/
│   ├── create_tables.sql
│   └── seed_data.sql
└── requirements.txt
```

**Database Tables:**
- `schools` - School information with PostGIS location
- `green_courses` - Environmental education courses
- `green_activities` - School green activities
- `enrollments` - Student course enrollments

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/schools` | List schools (filter by type) |
| POST | `/api/v1/schools` | Create school |
| GET | `/api/v1/schools/nearby` | Find nearby schools |
| GET | `/api/v1/schools/ranking` | Green score ranking |
| GET | `/api/v1/schools/{id}` | Get school details |

---

### 3.4 Environment Service (`modules/environment-service/`)

**Chức năng:** Air quality, weather data, IoT integration

**Files quan trọng:**
```
environment-service/
├── app/
│   ├── main.py            # FastAPI với MQTT/RabbitMQ lifespan
│   ├── config.py          # Settings (API keys, broker URLs)
│   ├── messaging.py       # RabbitMQ publisher + MQTT subscriber
│   ├── clients/
│   │   ├── openaq.py      # OpenAQ API client
│   │   └── openweather.py # OpenWeather API client
│   └── routes/
│       ├── air_quality.py # AQI endpoints
│       └── weather.py     # Weather endpoints
└── requirements.txt
```

**MQTT Topics (Subscribed):**
- `sensors/air-quality/#` - AQI sensor data
- `sensors/weather/#` - Weather sensor data
- `sensors/energy/#` - Energy consumption data

**RabbitMQ Events (Published):**
- `environment.events` (FANOUT) - All environment updates
- `notifications` (TOPIC) - AQI alerts

**Key Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/air-quality` | Get AQI data |
| GET | `/api/v1/air-quality/locations` | Available monitoring locations |
| GET | `/api/v1/weather` | Get weather data |
| POST | `/api/v1/trigger-analysis` | Trigger AI analysis |

---

### 3.5 Resource Service (`modules/resource-service/`)

**Chức năng:** Green zones, recycling centers, resources

**Files quan trọng:**
```
resource-service/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── api/
│   │   ├── centers.py      # Recycling centers
│   │   ├── green_zones.py  # Green zones (parks, forests)
│   │   └── green_resources.py
│   ├── models/
│   │   ├── green_zone.py
│   │   └── green_resource.py
│   └── schemas/
└── requirements.txt
```

---

### 3.6 Shared Module (`modules/shared/`)

**Chức năng:** Shared utilities, database models, messaging

**Files quan trọng:**
```
shared/
├── __init__.py
├── database/
│   ├── base.py           # SQLAlchemy base
│   └── models/           # Shared models
├── messaging/
│   ├── __init__.py
│   ├── rabbitmq.py       # RabbitMQ client utilities
│   ├── mqtt.py           # MQTT client utilities
│   └── events.py         # Event definitions
└── requirements.txt
```

---

### 3.7 Web App (`modules/web-app/`)

**Chức năng:** Frontend application

**Tech Stack:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Mapbox GL JS
- TailwindCSS
- Prisma (optional)

**Key Directories:**
```
web-app/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # React components (~100 files)
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities
│   └── context/          # React contexts
├── public/
│   └── images/
├── prisma/
│   └── schema.prisma
└── package.json
```

---

## 4. Database Schema

### 4.1 PostgreSQL Tables

```sql
-- Schools table (education-service)
CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    school_type VARCHAR(50),  -- 'primary', 'secondary', 'high', 'university'
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    location GEOMETRY(Point, 4326),  -- PostGIS
    green_score DECIMAL(5,2) DEFAULT 0,
    student_count INTEGER,
    has_garden BOOLEAN DEFAULT false,
    solar_panels BOOLEAN DEFAULT false,
    recycling_program BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Green Courses
CREATE TABLE green_courses (
    id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES schools(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    duration_hours INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Green Activities
CREATE TABLE green_activities (
    id SERIAL PRIMARY KEY,
    school_id INTEGER REFERENCES schools(id),
    name VARCHAR(255) NOT NULL,
    activity_type VARCHAR(50),
    participants INTEGER,
    activity_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Air Quality Data (environment-service)
CREATE TABLE air_quality_data (
    id SERIAL PRIMARY KEY,
    location_id VARCHAR(100),
    location_name VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    aqi DECIMAL(6,2),
    pm25 DECIMAL(6,2),
    pm10 DECIMAL(6,2),
    co DECIMAL(6,2),
    no2 DECIMAL(6,2),
    o3 DECIMAL(6,2),
    so2 DECIMAL(6,2),
    measured_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather Data
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    location_id VARCHAR(100),
    location_name VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    pressure DECIMAL(7,2),
    wind_speed DECIMAL(5,2),
    clouds INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(255),
    measured_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Green Zones (resource-service)
CREATE TABLE green_zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    zone_type VARCHAR(50),  -- 'park', 'forest', 'garden'
    area_sqm DECIMAL(12,2),
    location GEOMETRY(Polygon, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users (auth-service)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 Spatial Indexes

```sql
CREATE INDEX idx_schools_location ON schools USING GIST(location);
CREATE INDEX idx_green_zones_location ON green_zones USING GIST(location);
CREATE INDEX idx_air_quality_location ON air_quality_data(latitude, longitude);
```

---

## 5. Message Brokers

### 5.1 RabbitMQ Configuration

**Connection:** `amqp://admin:admin123@rabbitmq:5672/greenedumap`

**Exchanges:**

| Exchange | Type | Purpose |
|----------|------|---------|
| `environment.events` | FANOUT | Broadcast environment updates |
| `ai.tasks` | DIRECT | AI processing task queue |
| `export.tasks` | DIRECT | Data export task queue |
| `notifications` | TOPIC | Alert notifications |

**Queues:**

| Queue | Exchange | Routing Key |
|-------|----------|-------------|
| `ai.clustering.queue` | ai.tasks | ai.clustering |
| `ai.prediction.queue` | ai.tasks | ai.prediction |
| `ai.correlation.queue` | ai.tasks | ai.correlation |
| `export.csv.queue` | export.tasks | export.csv |
| `export.geojson.queue` | export.tasks | export.geojson |

**Message Format:**
```json
{
  "task_id": "uuid",
  "event_type": "ai.clustering.requested",
  "timestamp": "2025-12-04T10:00:00Z",
  "source": "api-gateway",
  "data": {
    "task_type": "clustering",
    "parameters": {}
  }
}
```

### 5.2 EMQX (MQTT) Configuration

**Connection:** `mqtt://emqx:1883`

**Topics:**

| Topic Pattern | Publisher | Subscriber | Purpose |
|---------------|-----------|------------|---------|
| `sensors/air-quality/{location_id}` | IoT | environment-service | AQI sensor data |
| `sensors/weather/{location_id}` | IoT | environment-service | Weather sensor data |
| `sensors/energy/{school_id}` | IoT | environment-service | Energy data |
| `realtime/aqi/{location_id}` | environment-service | web-app | Real-time AQI |
| `realtime/weather/{location_id}` | environment-service | web-app | Real-time weather |
| `realtime/map/update` | environment-service | web-app | Map updates |
| `alerts/environment/{severity}` | environment-service | - | Environment alerts |

**Message Format (Sensor):**
```json
{
  "location_id": "danang_01",
  "latitude": 16.0544,
  "longitude": 108.2022,
  "aqi": 75.5,
  "pm25": 25.3,
  "pm10": 45.2,
  "temperature": 28.5,
  "humidity": 75,
  "timestamp": "2025-12-04T10:00:00Z"
}
```

---

## 6. Tiến Độ Hoàn Thành

### 6.1 Đã Hoàn Thành ✅

| Component | Status | Notes |
|-----------|--------|-------|
| **Infrastructure** | | |
| Docker Compose setup | ✅ | PostgreSQL, Redis, MongoDB |
| RabbitMQ integration | ✅ | Exchanges, queues configured |
| EMQX (MQTT) integration | ✅ | Topics configured |
| PostGIS spatial database | ✅ | Indexes created |
| **API Gateway** | | |
| Service routing | ✅ | All services proxied |
| Health aggregation | ✅ | Checks all services |
| RabbitMQ publisher | ✅ | Task queuing |
| Rate limiting | ⚠️ | Redis configured, logic basic |
| Route ordering fixes | ✅ | Air quality & weather routes |
| API Documentation | ✅ | 50+ endpoints documented |
| Postman Collection | ✅ | 30+ requests with auto-token |
| API Test Suite | ✅ | 60% pass rate (15/25 tests) |
| **Auth Service** | | |
| JWT authentication | ✅ | Access + refresh tokens |
| User registration | ✅ | |
| Login/logout | ✅ | |
| **Education Service** | | |
| School CRUD | ✅ | Full CRUD operations |
| Nearby search (PostGIS) | ✅ | ST_DWithin queries |
| Green score ranking | ✅ | |
| Green courses model | ✅ | Schema ready |
| Green activities model | ✅ | Schema ready |
| **Environment Service** | | |
| OpenAQ integration | ✅ | Air quality data |
| OpenWeather integration | ✅ | Weather data |
| MQTT subscriber | ✅ | Listening to sensor topics |
| RabbitMQ publisher | ✅ | Publishing events |
| Alert thresholds | ✅ | AQI warning/critical |
| **Resource Service** | | |
| Green zones CRUD | ✅ | |
| Recycling centers | ✅ | |
| **Web App** | | |
| Next.js setup | ✅ | App Router |
| Map component | ✅ | Mapbox GL |
| Basic UI | ✅ | TailwindCSS |
| **Shared Module** | | |
| Messaging utilities | ✅ | RabbitMQ + MQTT clients |
| Event definitions | ✅ | EventTypes enum |
| **AI Service** | | |
| Clustering (K-Means) | ✅ | Green/Yellow/Red zones |
| Prediction (ARIMA) | ✅ | 7-day AQI forecast |
| Correlation Analysis | ✅ | Environment ↔ Education |
| RabbitMQ consumers | ✅ | 3 task queues |
| **OpenData Service** | | |
| NGSI-LD entities | ✅ | 4 entity types (School, AQI, Zone, Course) |
| DCAT-AP catalog | ✅ | 4 datasets, 13 distributions |
| JSON-LD context | ✅ | 41 vocabulary mappings |
| CSV Export | ✅ | All datasets |
| GeoJSON Export | ✅ | Geographic data |
| RDF Export | ✅ | Turtle, N-Triples, JSON-LD, RDF/XML |
| **Deployment** | | |
| VPS Deployment | ✅ | greenedumap.io.vn + api.greenedumap.io.vn |
| SSL/TLS Certificates | ✅ | Certbot auto-renewal |
| Nginx Reverse Proxy | ✅ | API Gateway & Web App |
| Docker Production | ✅ | All services running |

### 6.2 Đang Phát Triển 🚧

| Component | Status | Notes |
|-----------|--------|-------|
| Green score calculation | 🚧 | Formula cần tinh chỉnh |
| Web app features | 🚧 | Dashboard, filters |

### 6.3 Chưa Bắt Đầu ❌

| Component | Priority | Notes |
|-----------|----------|-------|
| Notification Service | LOW | Email, push notifications |
| Mobile App | LOW | Viết riêng, chưa push |

---

## 7. Công Việc Còn Lại

### 7.1 Priority HIGH - Cần Làm Trước

#### 7.1.1 OpenData Service

**Chức năng:**

1. **NGSI-LD Entities** - Chuẩn hóa dữ liệu
   ```json
   {
     "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
     "id": "urn:ngsi-ld:School:001",
     "type": "School",
     "name": {"type": "Property", "value": "THPT Phan Châu Trinh"},
     "location": {"type": "GeoProperty", "value": {...}}
   }
   ```

2. **JSON-LD Context** - Schema definitions
3. **Data Catalog** - DCAT-AP metadata
4. **SPARQL Endpoint** (optional)

### 7.2 Priority MEDIUM

#### 7.2.1 Export Service

```
export-service/
├── app/
│   ├── consumers/
│   │   ├── csv_export.py
│   │   ├── geojson_export.py
│   │   └── rdf_export.py
│   └── storage/         # File storage
```

#### 7.2.2 Web App Features

- [ ] Dashboard với charts (Chart.js/Recharts)
- [ ] Advanced map filters
- [ ] School comparison tool
- [ ] Real-time MQTT WebSocket bridge
- [ ] Admin panel

### 7.3 Priority LOW

- Notification Service (email, push)
- Mobile App integration
- API documentation (OpenAPI/Swagger)
- Unit tests
- CI/CD pipeline

---

## 8. Hướng Dẫn Phát Triển

### 8.1 Setup Local Environment

```bash
# 1. Clone repository
git clone <repo-url>
cd GreenEduMap-DTUDZ

# 2. Start infrastructure
cd infrastructure/docker
docker-compose up -d postgres redis mongodb rabbitmq emqx

# 3. Wait for services to be healthy
docker-compose ps

# 4. Start backend services
docker-compose up -d api-gateway auth-service education-service environment-service resource-service

# 5. Start frontend
cd ../../modules/web-app
npm install
npm run dev
```

### 8.2 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| API Gateway | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Web App | http://localhost:3000 | - |
| Adminer (DB UI) | http://localhost:8080 | postgres/postgres |
| RabbitMQ Management | http://localhost:15672 | admin/admin123 |
| EMQX Dashboard | http://localhost:18083 | admin/admin123 |

### 8.3 Creating New Service

```bash
# 1. Create service directory
mkdir -p modules/new-service/app

# 2. Create files
touch modules/new-service/app/__init__.py
touch modules/new-service/app/main.py
touch modules/new-service/app/config.py
touch modules/new-service/Dockerfile
touch modules/new-service/requirements.txt

# 3. Add to docker-compose.yml
# 4. Add routing to api-gateway
```

### 8.4 Database Migrations

```bash
# Connect to PostgreSQL
docker exec -it greenedumap-postgres psql -U postgres -d greenedumap

# Run migration
\i /path/to/migration.sql
```

### 8.5 Testing RabbitMQ

```python
# Publish test message
import aio_pika
import asyncio

async def test():
    conn = await aio_pika.connect_robust("amqp://admin:admin123@localhost:5672/greenedumap")
    channel = await conn.channel()
    exchange = await channel.declare_exchange("ai.tasks", aio_pika.ExchangeType.DIRECT)
    await exchange.publish(
        aio_pika.Message(b'{"test": "message"}'),
        routing_key="ai.clustering"
    )
    await conn.close()

asyncio.run(test())
```

### 8.6 Testing MQTT

```python
# Publish sensor data
import aiomqtt
import asyncio

async def test():
    async with aiomqtt.Client("localhost", 1883) as client:
        await client.publish(
            "sensors/air-quality/test",
            '{"aqi": 75, "pm25": 25}'
        )

asyncio.run(test())
```

---

## 9. API Endpoints

### 9.1 API Gateway (`/api/v1/`)

```
# Health & Info
GET  /                          # Gateway info
GET  /health                    # Aggregated health

# Task Queue
POST /api/v1/tasks/ai/clustering    # Queue clustering task
POST /api/v1/tasks/ai/prediction    # Queue prediction task
POST /api/v1/tasks/ai/correlation   # Queue correlation task
POST /api/v1/tasks/export           # Queue export task

# OpenData (proxy)
GET  /api/open-data/schools         # Schools list
GET  /api/open-data/environment     # Environment data
```

### 9.2 Auth Service (`/api/v1/auth/`)

```
POST /api/v1/auth/register      # Register user
POST /api/v1/auth/login         # Login
POST /api/v1/auth/refresh       # Refresh token
GET  /api/v1/users/me           # Current user
```

### 9.3 Education Service (`/api/v1/`)

```
GET    /api/v1/schools              # List schools
POST   /api/v1/schools              # Create school
GET    /api/v1/schools/{id}         # Get school
PUT    /api/v1/schools/{id}         # Update school
DELETE /api/v1/schools/{id}         # Delete school
GET    /api/v1/schools/nearby       # Find nearby (lat, lon, radius)
GET    /api/v1/schools/ranking      # Green score ranking
```

### 9.4 Environment Service (`/api/v1/`)

```
GET  /api/v1/air-quality            # Get AQI data
GET  /api/v1/air-quality/locations  # Available locations
GET  /api/v1/weather                # Get weather data
POST /api/v1/trigger-analysis       # Trigger AI analysis
```

### 9.5 Resource Service (`/api/v1/`)

```
GET    /api/v1/green-zones          # List green zones
POST   /api/v1/green-zones          # Create green zone
GET    /api/v1/green-zones/{id}     # Get green zone
GET    /api/v1/centers              # List recycling centers
```

---

## 10. Cấu Hình & Biến Môi Trường

### 10.1 Docker Compose Environment

```env
# Database
POSTGRES_DB=greenedumap
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

# Redis
REDIS_PORT=6379

# MongoDB
MONGO_PORT=27017

# RabbitMQ
RABBITMQ_USER=admin
RABBITMQ_PASS=admin123
RABBITMQ_PORT=5672
RABBITMQ_MGMT_PORT=15672

# EMQX
MQTT_PORT=1883
EMQX_DASHBOARD_PORT=18083
EMQX_DASHBOARD_USER=admin
EMQX_DASHBOARD_PASS=admin123

# Services
API_GATEWAY_PORT=8000
DEBUG=true

# External APIs
OPENWEATHER_API_KEY=your_api_key
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 10.2 Service-Specific Configs

**API Gateway:**
```python
AUTH_SERVICE_URL = "http://auth-service:8001"
EDUCATION_SERVICE_URL = "http://education-service:8008"
ENVIRONMENT_SERVICE_URL = "http://environment-service:8007"
RESOURCE_SERVICE_URL = "http://resource-service:8002"
RABBITMQ_URL = "amqp://admin:admin123@rabbitmq:5672/greenedumap"
```

**Environment Service:**
```python
OPENAQ_API_URL = "https://api.openaq.org/v2"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5"
MQTT_BROKER_HOST = "emqx"
MQTT_BROKER_PORT = 1883
AQI_WARNING_THRESHOLD = 100
AQI_CRITICAL_THRESHOLD = 150
```

---

## 📌 Quick Reference

### Start All Services
```bash
cd infrastructure/docker
docker-compose up -d
```

### View Logs
```bash
docker logs greenedumap-api-gateway --tail 50 -f
docker logs greenedumap-environment-service --tail 50 -f
```

### Rebuild Service
```bash
docker-compose build <service-name>
docker-compose up -d <service-name>
```

### Database Access
```bash
docker exec -it greenedumap-postgres psql -U postgres -d greenedumap
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Queue AI task
curl -X POST "http://localhost:8000/api/v1/tasks/ai/clustering?data_type=environment"
```

---

## 📝 Notes for Cursor AI

1. **Khi implement AI Service:**
   - Sử dụng aio-pika để consume từ RabbitMQ
   - Kết quả lưu vào PostgreSQL
   - Publish completion event về `environment.events`

2. **Khi implement Export Service:**
   - Hỗ trợ: CSV, GeoJSON, RDF (Turtle/N-Triples)
   - Async processing với progress tracking
   - File storage trong container volume

3. **Khi implement OpenData Service:**
   - Follow NGSI-LD specification
   - Provide JSON-LD context
   - DCAT-AP metadata

4. **Database:**
   - Sử dụng SQLAlchemy async (asyncpg driver)
   - PostGIS cho spatial queries
   - Indexes đã được tạo sẵn

5. **Coding Style:**
   - Python: FastAPI + Pydantic
   - TypeScript: Next.js conventions
   - Follow existing patterns in codebase

---

*Tài liệu này được tạo tự động và cập nhật thủ công. Vui lòng cập nhật khi có thay đổi lớn.*

