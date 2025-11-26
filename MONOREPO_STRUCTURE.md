
# 🌱 GreenEduMap Monorepo Structure

## 📦 Cấu Trúc Thư Mục

```
GreenEduMap/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD pipeline
│
├── .husky/                           # Git hooks
│
├── docker/
│   ├── docker-compose.yml            # Multi-service orchestration
│   ├── frontend.Dockerfile
│   └── backend.Dockerfile
│
├── docs/                             # Documentation
│   ├── architecture.md
│   ├── api_reference.md
│   ├── open_data_standards.md
│   └── README.md
│
├── scripts/                          # Utility scripts
│   ├── init_db.sh
│   ├── seed_air_quality.py
│   ├── convert_to_jsonld.py
│   └── publish_to_orionld.py
│
├── data/                             # Sample open data
│   ├── openaq_sample.json
│   ├── openweather_sample.json
│   ├── school_dataset.csv
│   └── energy_dataset.csv
│
├── frontend/                         # Next.js Application
│   ├── src/
│   │   ├── app/                      # Routes (app router)
│   │   │   ├── (auth)/              # Auth pages
│   │   │   ├── page.tsx             # Home page
│   │   │   ├── map/                 # Map route
│   │   │   ├── actions/             # Green actions
│   │   │   ├── feedback/            # Feedback form
│   │   │   ├── stats/               # Statistics
│   │   │   ├── chat/                # AI Chat
│   │   │   ├── recommendations/     # AI Recommendations
│   │   │   ├── school/              # School dashboard
│   │   │   └── admin/               # Admin panel
│   │   ├── components/              # React components
│   │   ├── lib/                     # Utilities
│   │   ├── hooks/                   # Custom hooks
│   │   ├── context/                 # React contexts
│   │   ├── layout/                  # Layout components
│   │   └── providers/               # Context providers
│   ├── public/
│   │   └── images/
│   ├── package.json
│   ├── next.config.ts
│   └── Dockerfile
│
├── backend/                          # FastAPI Application
│   ├── app/
│   │   ├── core/                    # Config, security, constants
│   │   ├── db/                      # Database setup
│   │   ├── models/                  # SQLAlchemy models
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── services/                # Business logic
│   │   │   ├── fiware_service.py    # Orion-LD integration
│   │   │   ├── lod_converter.py     # JSON-LD/RDF conversion
│   │   │   ├── ai_service.py        # AI analysis
│   │   │   └── open_data_service.py # OpenAQ/OpenWeather
│   │   ├── api/
│   │   │   └── endpoints/           # API routes
│   │   └── utils/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── fiware-service/                   # FiWARE Integration (optional)
│   ├── adapter.py
│   ├── entity_models/
│   └── requirements.txt
│
├── release/
│   ├── CHANGELOG.md                  # Version history
│   └── version.json                  # Version info
│
├── .editorconfig                     # Editor config
├── .gitignore                        # Git ignore
├── .prettierrc                       # Prettier config
├── CODE_OF_CONDUCT.md               # Community guidelines
├── CONTRIBUTING.md                   # Contribution guide
├── LICENSE                          # MIT License
├── README.md                        # Main documentation
├── package.json                     # Monorepo root scripts
└── MONOREPO_STRUCTURE.md            # This file

```

---

## 🚀 Quick Start Commands

### Development (Both Frontend & Backend)
```bash
yarn dev
```

### Build
```bash
yarn build
```

### Testing
```bash
yarn test           # Run all tests
yarn test:backend   # Backend only
yarn test:frontend  # Frontend only
```

### Linting & Formatting
```bash
yarn lint          # Lint code
yarn format        # Format code
```

### Docker
```bash
yarn docker:up     # Start services
yarn docker:down   # Stop services
yarn docker:logs   # View logs
```

### Database
```bash
yarn init:db       # Initialize database
yarn seed:data     # Seed sample data
yarn publish:lod   # Publish LOD to Orion-LD
```

---

## 📊 Services Architecture

```
┌─────────────────────────────────────────────────────┐
│              Frontend (Next.js) :3000                │
│  Routes: /, /map, /actions, /school/*, /admin/*    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           Backend (FastAPI) :8000                    │
│  /auth, /api/air-quality, /api/ai, /api/ngsi-ld   │
└────┬──────────┬──────────┬──────────┬───────────────┘
     │          │          │          │
     ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────────┐
│Postgres│ │MongoDB │ │Orion-LD  │ │Open APIs     │
│PostGIS │ │ :27017 │ │ :1026    │ │(OpenAQ, etc) │
└────────┘ └────────┘ └──────────┘ └──────────────┘

PostgreSQL:5432  │  MongoDB:27017  │  Orion-LD:1026
```

---

## 🔧 Environment Setup

### Backend (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/greenedumap
ORION_URL=http://localhost:1026
OPENAQ_API_KEY=your_api_key
OPENWEATHER_API_KEY=your_api_key
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `docker/docker-compose.yml` | Multi-service orchestration |
| `.github/workflows/ci.yml` | GitHub Actions CI/CD |
| `package.json` | Monorepo root scripts |
| `CONTRIBUTING.md` | Development guidelines |
| `CODE_OF_CONDUCT.md` | Community standards |
| `release/CHANGELOG.md` | Version history |
| `release/version.json` | Current version info |

---

## 🎯 Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Install Dependencies**
   ```bash
   # Frontend
   cd frontend && yarn install
   
   # Backend
   cd backend && pip install -r requirements.txt
   ```

3. **Start Development**
   ```bash
   yarn dev
   ```

4. **Commit with Conventional Commits**
   ```bash
   git commit -m "feat(auth): add JWT refresh token"
   ```

5. **Push & Create PR**
   ```bash
   git push origin feature/your-feature
   ```

---

## 🐳 Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Next.js web UI |
| Backend | 8000 | FastAPI server |
| PostgreSQL | 5432 | Relational DB |
| MongoDB | 27017 | Document DB (Orion-LD) |
| Orion-LD | 1026 | Semantic broker |

---

## 📚 Documentation Files

- **README.md** - Main project overview
- **CONTRIBUTING.md** - How to contribute
- **CODE_OF_CONDUCT.md** - Community guidelines
- **docs/architecture.md** - System design
- **docs/api_reference.md** - API endpoints
- **docs/open_data_standards.md** - NGSI-LD, LOD info
- **release/CHANGELOG.md** - Version history

---

## ✅ Checklist for New Contributors

- [ ] Read CONTRIBUTING.md
- [ ] Read CODE_OF_CONDUCT.md
- [ ] Fork repository
- [ ] Set up development environment
- [ ] Create feature branch
- [ ] Install dependencies
- [ ] Run `yarn dev`
- [ ] Make changes
- [ ] Run tests: `yarn test`
- [ ] Run linter: `yarn lint`
- [ ] Commit with conventional commits
- [ ] Push to branch
- [ ] Create Pull Request

---

**Built for OLP 2025 Smart City Challenge** 🌍🌱

