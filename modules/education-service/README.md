# Education Service

Green education tracking and school management service for GreenEduMap.

## Features

- **Schools Management**: CRUD operations for schools with PostGIS spatial support
- **Green Courses**: Track environmental education programs
- **Green Score**: Calculate and rank schools by sustainability metrics
- **Spatial Queries**: Find nearby schools using PostGIS
- **OpenData Compliance**: Public API endpoints with proper metadata

## API Endpoints

### Schools
- `POST /api/v1/schools` - Create school
- `GET /api/v1/schools` - List schools (with filters)
- `GET /api/v1/schools/{id}` - Get school details
- `PUT /api/v1/schools/{id}` - Update school
- `DELETE /api/v1/schools/{id}` - Delete school
- `GET /api/v1/schools/nearby` - Find nearby schools
- `GET /api/v1/schools/rankings` - Get schools by green score

### Green Courses
- `POST /api/v1/green-courses` - Create course
- `GET /api/v1/green-courses` - List courses
- `GET /api/v1/green-courses/{id}` - Get course details
- `GET /api/v1/green-courses/by-school/{school_id}` - Get courses by school
- `PUT /api/v1/green-courses/{id}` - Update course
- `DELETE /api/v1/green-courses/{id}` - Delete course

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with PostGIS
- **ORM**: SQLAlchemy (async)
- **Validation**: Pydantic v2

## Setup

1. Copy `.env.example` to `.env`
2. Configure database connection
3. Run with Docker:

```bash
docker-compose up -d education-service
```

4. Access docs at `http://localhost:8008/docs`

## Database Schema

### schools
- Geospatial location (PostGIS POINT)
- Green score (0-100)
- School type classification
- Facilities metadata (JSONB)

### green_courses
- Linked to schools
- Category-based classification
- Syllabus metadata (JSONB)

## Development

Run locally:
```bash
cd modules/education-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8008
```

## Testing

```bash
# Run tests
pytest

# Test API
curl http://localhost:8008/health
```

## Green Score Algorithm

The green score (0-100) is calculated based on:
- Green facilities (solar panels, gardens, recycling)
- Number and quality of green courses
- Environmental correlation (nearby air quality)
- Community engagement activities

*Full algorithm implementation in Day 3*
