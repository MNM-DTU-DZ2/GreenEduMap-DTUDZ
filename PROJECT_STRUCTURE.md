# 📋 GreenEduMap - Project Structure Overview

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│          Frontend (Next.js 15 + React)              │
│  ┌──────────────────────────────────────────────┐   │
│  │  Pages: Map, AI Analysis, Stats, Chat, Admin │   │
│  │  Components: UI, Forms, Charts, Relief Map   │   │
│  │  Hooks: useAirQuality, useAIAnalysis, etc.   │   │
│  └──────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────────┘
               │ HTTP/REST
┌──────────────┴──────────────────────────────────────┐
│          Backend (FastAPI + PostgreSQL)             │
│  ┌──────────────────────────────────────────────┐   │
│  │  API Routes: /api/air-quality, /api/ai       │   │
│  │  Services: OpenData, AI, LOD Converter       │   │
│  │  Models: AirQuality, School, User, Analysis  │   │
│  │  Database: PostgreSQL + GeoAlchemy2          │   │
│  └──────────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────────┘
               │
       ┌───────┴──────────┬──────────────┐
       │                  │              │
   ┌───┴────┐      ┌─────┴────┐    ┌────┴────┐
   │Database │      │FiWARE    │    │External │
   │PostgreSQL   │Orion-LD  │    │APIs     │
   │          │      │          │    │         │
   └──────────┘      └──────────┘    └─────────┘
```

## 📁 Backend Structure

```
backend/app/
├── __init__.py
├── main.py                           # FastAPI app entry
│
├── core/                             # Configuration
│   ├── __init__.py
│   ├── config.py                     # Settings & environment
│   ├── security.py                   # Auth utilities
│   ├── constants.py                  # Constants
│   └── utils.py                      # Helpers
│
├── db/                               # Database layer
│   ├── __init__.py
│   ├── base.py                       # SQLAlchemy setup
│   └── init_db.py                    # Database initialization
│
├── models/                           # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── air_quality.py                # AirQuality model
│   ├── education.py                  # School, EducationQuality models
│   ├── user.py                       # User model
│   └── ai_result.py                  # AIAnalysis model
│
├── schemas/                          # Pydantic request/response schemas
│   ├── __init__.py
│   ├── air_quality.py                # AQ schemas
│   ├── user.py                       # User schemas
│   └── ai_result.py                  # AI schemas
│
├── services/                         # Business logic
│   ├── __init__.py
│   ├── open_data_service.py          # Fetch OpenAQ, OpenWeather, OSM
│   ├── ai_service.py                 # AI correlation & clustering
│   ├── fiware_service.py             # FiWARE integration
│   └── lod_converter.py              # RDF/JSON-LD conversion
│
└── api/                              # API routes
    ├── __init__.py
    ├── router.py                     # Main router
    └── endpoints/
        ├── __init__.py
        ├── air_quality.py            # AQ endpoints
        ├── ai_analysis.py            # AI endpoints
        ├── ngsi_ld.py                # FiWARE endpoints (optional)
        └── auth.py                   # Auth endpoints (future)
```

## 📁 Frontend Structure

```
frontend/src/
├── app/                              # Next.js 15 app directory
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Home page
│   ├── map/page.tsx                  # Air quality map
│   ├── ai-analysis/page.tsx          # AI analysis dashboard
│   ├── stats/page.tsx                # Statistics
│   ├── chat/page.tsx                 # AI chat
│   ├── feedback/page.tsx             # Feedback form
│   ├── admin/                        # Admin pages
│   │   └── dashboard.tsx
│   ├── api/                          # API routes (if needed)
│   └── actions/page.tsx              # Green actions
│
├── components/                       # Reusable React components
│   ├── common/                       # Common components
│   ├── forms/                        # Form components
│   ├── charts/                       # Chart components
│   ├── relief/                       # Relief map components
│   ├── ui/                           # UI components (ShadCN)
│   └── header/
│
├── hooks/                            # Custom React hooks
│   ├── useAirQuality.ts              # Air quality data fetching
│   ├── useAIAnalysis.ts              # AI analysis logic
│   ├── useApi.ts                     # Generic API hook
│   ├── useModal.ts                   # Modal state
│   └── [other hooks].ts
│
├── lib/                              # Utilities & helpers
│   ├── api.ts                        # API client
│   ├── auth.ts                       # Auth utilities
│   ├── jwt.ts                        # JWT handling
│   ├── prisma.ts                     # Database client
│   ├── translations.ts               # i18n
│   └── redirect.ts                   # Navigation helpers
│
├── context/                          # React Context
│   ├── ThemeContext.tsx              # Theme provider
│   ├── ToastContext.tsx              # Toast notifications
│   ├── AuthContext.tsx               # Auth state (future)
│   └── SidebarContext.tsx
│
├── store/                            # State management
│   ├── authStore.ts                  # Auth state (Zustand)
│   └── [other stores].ts
│
├── middleware.ts                     # Next.js middleware
├── icons/                            # SVG icons
├── svg.d.ts                          # Icon types
└── globals.css                       # Global styles
```

## 🔌 API Endpoints

### Air Quality APIs
```
GET    /api/air-quality/               # List air quality
GET    /api/air-quality/{id}           # Get by ID
POST   /api/air-quality/               # Create new
GET    /api/air-quality/alerts/high    # Get high AQI alerts
GET    /api/air-quality/fetch/openaq   # Fetch from OpenAQ
```

### AI Analysis APIs
```
POST   /api/ai/analyze/correlation     # Analyze correlation
POST   /api/ai/analyze/ward            # Analyze ward
POST   /api/ai/cluster/wards           # Cluster wards
GET    /api/ai/predict/impact          # Predict impact
GET    /api/ai/results                 # List results
GET    /api/ai/results/{id}            # Get result
```

### Health & Status
```
GET    /                               # Root
GET    /health                         # Health check
GET    /docs                           # Swagger UI
GET    /redoc                          # ReDoc
```

## 📊 Data Models

### AirQuality
```python
- id: int
- ward_name: string
- district: string
- city: string (default: "Hanoi")
- latitude/longitude: float
- aqi: float (required)
- pm25, pm10, no2, o3, so2, co: float
- measurement_date: datetime
- created_at/updated_at: datetime
```

### School
```python
- id: int
- name: string (required)
- code: string (unique)
- district, ward, city: string
- latitude/longitude: float
- school_type: string (Elementary, Middle, High, University)
- total_students: int
- phone, email, website: string
```

### User
```python
- id: int
- email/username: string (unique, required)
- hashed_password: string
- full_name, phone: string
- is_active, is_verified, is_admin: boolean
- role: string (user, educator, admin)
- last_login: datetime
```

### AIAnalysis
```python
- id: int
- analysis_type: string (correlation, prediction, clustering)
- input_parameters: JSON
- correlation_coefficient, model_accuracy: float
- predictions, insights: JSON
- recommendation: text
- recommendation_priority: string
- status: string (processing, completed, failed)
```

## 🔄 Data Flow

### 1️⃣ Fetching Air Quality Data
```
User → Frontend (useAirQuality) → API Client → Backend
    ↓
Backend Routes → Air Quality Endpoint → OpenDataService
    ↓
External APIs (OpenAQ) → Database (PostgreSQL)
    ↓
Response → Frontend → Component Display
```

### 2️⃣ AI Analysis Flow
```
User Input (env values, education scores) → Frontend
    ↓
useAIAnalysis Hook → API Client → Backend
    ↓
AI Endpoint → AIService (correlation analysis)
    ↓
Calculate correlation → Generate recommendations
    ↓
Save to Database → Return response → Frontend Display
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL 16 + PostGIS
- **ORM**: SQLAlchemy 2.0
- **Async**: Uvicorn + httpx
- **AI/ML**: scikit-learn, numpy, pandas, scipy
- **Semantic Web**: rdflib, json-ld
- **Integration**: paho-mqtt (for FiWARE)

### Frontend
- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS + PostCSS
- **UI Library**: ShadCN/UI
- **State**: React Query + Zustand
- **Charts**: Recharts
- **Maps**: Mapbox GL (optional)
- **Auth**: NextAuth.js (future)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 16 + PostGIS
- **Cache**: MongoDB (for FiWARE)
- **FiWARE**: Orion-LD Context Broker

## 📦 Dependencies Management

### Backend (requirements.txt)
- FastAPI & Uvicorn: Web framework
- SQLAlchemy: ORM
- Psycopg2: PostgreSQL driver
- Pydantic: Data validation
- scikit-learn: ML algorithms
- pandas/numpy: Data processing
- requests/httpx: HTTP client

### Frontend (package.json)
- next: React framework
- react-query: Data fetching
- tailwindcss: CSS framework
- lucide-react: Icon library
- zod: Schema validation (optional)

## 🚀 Deployment

### Production Checklist
- [ ] Set SECRET_KEY in environment
- [ ] Configure CORS origins
- [ ] Set DEBUG=False
- [ ] Use production database
- [ ] Configure external API keys
- [ ] Set up SSL/HTTPS
- [ ] Enable logging & monitoring
- [ ] Configure backup strategy

### Docker Deployment
```bash
docker-compose -f docker/docker-compose.yml up -d
```

## 📚 Additional Resources

- [Setup Guide](./SETUP.md)
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Contributing Guidelines](./CONTRIBUTING.md)

---

**Last Updated**: November 2024
**Version**: 1.0.0
