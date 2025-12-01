# 🔧 Development Workflow

Development guidelines and setup for GreenEduMap.

---

## 🚀 Getting Started

### 1. Prerequisites

- Docker & Docker Compose
- Git
- Node.js 18+ (for web app)
- Python 3.11+ (for AI service)

### 2. Initial Setup

```bash
# Clone repository
git clone https://github.com/MNM-DTU-DZ2/GreenEduMap-DTUDZ.git
cd GreenEduMap-DTUDZ

# Start infrastructure
cd infrastructure/docker
docker-compose up -d

# Verify services
docker-compose ps
```

---

## 📂 Project Structure

```
GreenEduMap-DTUDZ/
├── modules/           # Microservices
│   ├── auth-service/
│   ├── environment-service/
│   ├── resource-service/
│   └── shared/       # Shared utilities
├── infrastructure/   # Docker configs
├── docs/            # Documentation
├── scripts/         # Automation scripts
└── collections/     # API testing
```

---

## 🔄 Git Workflow

### Branch Strategy

```
main (production)
  ↑
develop (staging)
  ↑
feature/* (development)
```

### Commit Convention

Use **Conventional Commits**:

```
type(scope): subject

body (optional)

BREAKING CHANGE: description (optional)
```

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style
- `refactor` - Code refactoring
- `perf` - Performance
- `test` - Tests
- `build` - Build system
- `ci` - CI/CD
- `chore` - Maintenance

### Quick Commit

```powershell
# Use automation script
.\scripts\git\git-push.ps1
```

---

## 🧪 Testing

### Manual Testing

Use Postman collections in `collections/postman/`

### API Testing

```bash
# Auth service
curl http://localhost:8001/health

# Environment service
curl http://localhost:8002/health
```

---

## 🏗️ Adding New Service

1. Create service folder in `modules/`
2. Add Dockerfile
3. Update `docker-compose.yml`
4. Add to API Gateway routes
5. Create Postman collection
6. Document in `docs/PROJECT_CONTEXT.md`

---

## 📝 Code Style

- **Python**: PEP 8, Black formatter
- **JavaScript**: ESLint + Prettier
- **Commits**: Conventional Commits

---

## 🔧 Troubleshooting

### Service won't start

```bash
docker-compose logs [service-name]
docker-compose restart [service-name]
```

### Database issues

```bash
docker-compose down -v
docker-compose up -d
```

---

## 📚 See Also

- [Docker Guide](DOCKER.md)
- [Project Context](PROJECT_CONTEXT.md)
- [Git Scripts](../scripts/git/README.md)
