# AI Service - Machine Learning for GreenEduMap

## 🤖 Chức Năng

AI Service cung cấp 3 tính năng ML chính:

### 1. 🎯 Clustering (Phân vùng)
- **Mục đích**: Phân vùng xanh/vàng/đỏ dựa trên AQI và Green Score
- **Algorithm**: K-Means clustering
- **Input**: Environment data + Education data
- **Output**: Zone assignments (green/yellow/red)

### 2. 📈 Prediction (Dự báo)
- **Mục đích**: Dự báo AQI cho 7 ngày tới
- **Algorithm**: Linear Regression + Moving Average
- **Input**: Historical AQI data
- **Output**: Daily AQI predictions with confidence levels

### 3. 🔗 Correlation (Tương quan)
- **Mục đích**: Phân tích mối liên hệ giữa môi trường và giáo dục
- **Algorithm**: Pearson/Spearman correlation
- **Input**: AQI data + School Green Score data
- **Output**: Correlation coefficients + Insights

## 🏗️ Kiến Trúc

```
ai-service/
├── app/
│   ├── models/              # ML models
│   │   ├── clustering.py
│   │   ├── prediction.py
│   │   └── correlation.py
│   ├── consumers/           # RabbitMQ consumers
│   │   ├── clustering_consumer.py
│   │   ├── prediction_consumer.py
│   │   └── correlation_consumer.py
│   ├── utils/               # Utilities
│   │   └── data_loader.py
│   ├── core/                # Core components
│   │   ├── config.py
│   │   └── database.py
│   └── main.py              # Entry point
├── requirements.txt
└── Dockerfile
```

## 📦 Dependencies

- **ML**: scikit-learn, numpy, pandas, scipy, statsmodels
- **Database**: SQLAlchemy, asyncpg
- **Message Queue**: aio-pika (RabbitMQ)

## 🚀 Usage

### Via RabbitMQ (Recommended)

Queue tasks through API Gateway:

```bash
# Clustering
POST /api/v1/tasks/ai/clustering?n_clusters=3

# Prediction
POST /api/v1/tasks/ai/prediction?location_id=danang_center

# Correlation
POST /api/v1/tasks/ai/correlation?analysis_type=pearson
```

### Direct Usage (Development)

```python
from app.models.clustering import EnvironmentClustering

# Load your data
data = [...]

# Run clustering
clustering = EnvironmentClustering(n_clusters=3)
results = clustering.fit_predict(data)
```

## 🔧 Configuration

Set in `.env` or environment variables:

```env
DATABASE_URL=postgresql+asyncpg://...
RABBITMQ_URL=amqp://admin:admin123@rabbitmq:5672/greenedumap
CLUSTERING_N_CLUSTERS=3
PREDICTION_FORECAST_DAYS=7
```

## 📊 Output Format

### Clustering Result
```json
{
  "zone": "green",
  "cluster_id": 0,
  "zone_avg_aqi": 45.2,
  "green_score": 85.5
}
```

### Prediction Result
```json
{
  "date": "2025-12-05",
  "predicted_aqi": 68.5,
  "confidence": "high",
  "category": "Moderate"
}
```

### Correlation Result
```json
{
  "correlations": {
    "aqi_vs_green_score": {
      "correlation": -0.65,
      "p_value": 0.002,
      "significant": true,
      "interpretation": "Tương quan nghịch mạnh"
    }
  },
  "insights": [...]
}
```

## 🧪 Testing

Tasks được queue từ API Gateway và xử lý async bởi consumers.

## 📝 Notes

- Service chạy liên tục, lắng nghe RabbitMQ queues
- Kết quả được log và có thể lưu vào database
- Phù hợp cho OLP 2025 demo

