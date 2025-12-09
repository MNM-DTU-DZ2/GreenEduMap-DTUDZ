# Auth Service

FastAPI-based authentication and authorization service for GreenEduMap.

## Features

- ✅ User Registration & Login
- ✅ JWT Authentication (Access + Refresh tokens)
- ✅ Password Hashing (bcrypt)
- ✅ Role-Based Access Control (RBAC)
- ✅ API Key Management for Developers
- ✅ OpenAPI Documentation (Swagger)
- ✅ Async PostgreSQL with SQLAlchemy

## Tech Stack

- **Framework**: FastAPI 0.109
- **Database**: PostgreSQL + SQLAlchemy (async)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic v2

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Service

```bash
# Development
python -m app.main 

# Or with uvicorn directly
uvicorn app.main:app --reload --port 8001
```

### 4. Access Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## API Endpoints

### Authentication

```
POST /api/v1/auth/register    - Register new user
POST /api/v1/auth/login       - Login (get tokens)
POST /api/v1/auth/refresh     - Refresh access token
GET  /api/v1/auth/me          - Get current user info
```

### User Management

```
GET    /api/v1/users          - List users (Admin only)
GET    /api/v1/users/{id}     - Get user by ID
DELETE /api/v1/users/{id}     - Delete user (Admin only)
```

### API Keys

```
POST /api/v1/api-keys         - Create API key (Developers)
```

## User Roles

- `admin` - Full access
- `developer` - Can create API keys
- `volunteer` - Rescue operations
- `citizen` - Basic access
- `school` - Education features

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html
```

## Docker

```bash
# Build
docker build -t greenedumap-auth .

# Run
docker run -p 8001:8001 --env-file .env greenedumap-auth
```

## Database Schema

### Users Table
- `id` (UUID) - Primary key
- `email` (String) - Unique
- `username` (String) - Unique  
- `password_hash` (String)
- `role` (String) - admin|volunteer|citizen|developer|school
- `is_active` (Boolean)
- `is_verified` (Boolean)
- `is_public` (Boolean) - OpenData flag
- Timestamps

### API Keys Table
- `id` (UUID)
- `user_id` (UUID)
- `key_hash` (String)
- `scopes` (String)
- `rate_limit` (Integer)

### Refresh Tokens Table
- `id` (UUID)
- `user_id` (UUID)
- `token_hash` (String)
- `expires_at` (DateTime)
- `is_revoked` (Boolean)

## Security

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with expiration
- Refresh token rotation
- API key hashing
- Role-based access control

## License

MIT
