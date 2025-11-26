# 🌍 GreenEduMap - Setup Guide

## 📋 Yêu cầu

- Docker & Docker Compose
- Git
- Node.js 20+ (nếu chạy local không dùng Docker)
- Python 3.11+ (nếu chạy local không dùng Docker)

## 🚀 Quick Start với Docker

### 1️⃣ Clone dự án
```bash
git clone <repository-url>
cd GreenEduMap
```

### 2️⃣ Chạy Docker Compose
```bash
cd docker
docker-compose up --build
```

Services sẽ khởi động:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **MongoDB**: localhost:27017
- **FiWARE Orion-LD**: http://localhost:1026

## 🔧 Local Development (không dùng Docker)

### Backend Setup

```bash
cd backend

# 1. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc: venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy .env file
cp .env.example .env

# 4. Khởi tạo database (PostgreSQL phải chạy trước)
python -m app.db.init_db

# 5. Chạy server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# 1. Install dependencies
yarn install
# hoặc: npm install

# 2. Copy .env file
cp .env.example .env.local

# 3. Chạy dev server
yarn dev
# hoặc: npm run dev
```

## 📝 Cấu trúc Thư mục

```
GreenEduMap/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # Endpoints
│   │   ├── db/                # Database config
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── core/              # Config & utils
│   ├── main.py                # App entry point
│   ├── requirements.txt        # Dependencies
│   └── Dockerfile
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Pages & routes
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom hooks
│   │   ├── lib/               # Utilities
│   │   └── context/           # Context providers
│   ├── package.json
│   └── Dockerfile
│
├── docker/
│   └── docker-compose.yml      # Container orchestration
│
└── docs/                       # Documentation
```

## 🔌 API Endpoints

### Air Quality (Chất Lượng Không Khí)
```bash
GET  /api/air-quality/               # List air quality records
GET  /api/air-quality/{id}           # Get specific record
POST /api/air-quality/               # Create record
GET  /api/air-quality/alerts/high    # Get high AQI alerts
GET  /api/air-quality/fetch/openaq   # Fetch from OpenAQ
```

### AI Analysis (Phân Tích AI)
```bash
POST /api/ai/analyze/correlation     # Analyze correlation
POST /api/ai/analyze/ward            # Analyze ward
POST /api/ai/cluster/wards           # Cluster wards
GET  /api/ai/predict/impact          # Predict action impact
GET  /api/ai/results                 # List results
GET  /api/ai/results/{id}            # Get result
```

## 🎯 Frontend Pages

- 🏠 `/` - Trang chủ
- 🗺️ `/map` - Bản đồ chất lượng không khí
- 🤖 `/ai-analysis` - Phân tích AI
- 📊 `/stats` - Thống kê
- 💬 `/chat` - Chat AI
- ⚙️ `/admin` - Dashboard quản lý

## 🗄️ Database

### Models
- **AirQuality** - Dữ liệu chất lượng không khí
- **School** - Thông tin trường học
- **EducationQuality** - Chỉ số chất lượng giáo dục
- **User** - Người dùng & authentication
- **AIAnalysis** - Kết quả phân tích AI

### Connection Info (Docker)
```
Host: postgres
Port: 5432
User: postgres
Password: password
Database: greenedumap
```

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/db
OPENAQ_API_KEY=your_key
OPENWEATHER_API_KEY=your_key
ORION_URL=http://localhost:1026
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=GreenEduMap
```

## 📚 API Testing

### Using FastAPI Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Using cURL
```bash
# Get air quality data
curl http://localhost:8000/api/air-quality/

# Analyze correlation
curl -X POST http://localhost:8000/api/ai/analyze/correlation \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "correlation",
    "env_values": [50, 60, 70, 80, 90],
    "edu_scores": [75, 78, 72, 68, 65]
  }'
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Building for Production

### Backend
```bash
docker build -t greenedumap-backend:latest -f backend/Dockerfile ./backend
```

### Frontend
```bash
docker build -t greenedumap-frontend:latest -f frontend/Dockerfile ./frontend
```

## 🐛 Troubleshooting

### Port đã được sử dụng
```bash
# Linux/macOS
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database connection error
- Đảm bảo PostgreSQL đang chạy
- Check DATABASE_URL environment variable
- Verify username/password

### API không kết nối
- Check NEXT_PUBLIC_API_URL trong frontend .env
- Ensure backend server đang chạy
- Check CORS settings

## 📖 Documentation

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [API Documentation](./docs/API.md)

## 🤝 Contribution

1. Fork dự án
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file

## 📞 Support

Nếu có vấn đề, vui lòng:
1. Check [Issues](https://github.com/GreenEduMap/issues)
2. Tạo Issue mới với chi tiết lỗi
3. Contact: support@greenedumap.dev

---

**🌱 GreenEduMap - Building a Sustainable Future Together!**
