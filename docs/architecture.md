# 🏗️ Kiến trúc hệ thống GreenEduMap

![Kiến trúc hệ thống](assets/images/Kien_truc_he_thong_GreenEduMap.png)

## Tổng quan

GreenEduMap được xây dựng theo kiến trúc **Microservices** hiện đại, đảm bảo khả năng mở rộng và xử lý dữ liệu lớn.

## Thành phần và công nghệ

| Thành phần         | Công nghệ sử dụng                                       |
| ------------------ | ------------------------------------------------------- |
| **Mobile App**     | React Native (iOS & Android)                            |
| **Web**            | Next.js 15                                              |
| **Backend Core**   | Laravel (PHP), Redis (Cache)                            |
| **AI Services**    | FastAPI (Python) cho NLP, Computer Vision, scikit-learn |
| **API Gateway**    | Traefik, Keycloak (Auth)                                |
| **Message Broker** | Apache Kafka, MQTT (EMQX/Mosquitto)                     |
| **Realtime**       | Reverb (WebSocket)                                      |
| **Database**       | PostgreSQL + PostGIS (GeoData), OpenSearch              |
| **Semantic**       | FiWARE Orion-LD, MongoDB                                |

## Các lớp (Layers) chính

### 📥 Frontend Layer

- **Web Dashboard**: Next.js 15 với TypeScript, TailwindCSS, Chart.js/ECharts
- **Mobile App**: React Native với Expo, API consumption, offline-first
- **Map Visualization**: Mapbox GL JS / Cesium.js cho bản đồ 3D tương tác

### 🔬 Backend Layer

- **API Gateway**: Traefik routing, load balancing
- **Authentication**: Keycloak OpenID Connect, JWT tokens
- **Core Services**: Laravel microservices (User, School, Feedback, Analytics)
- **Cache Layer**: Redis cho session, real-time data
- **Message Queue**: Kafka cho async processing, MQTT cho IoT sensors

### 🧠 AI & Data Layer

- **NLP Service**: FastAPI + spaCy, transformers cho phân tích feedback
- **Computer Vision**: OpenCV + YOLO cho phân tích ảnh vệ tinh
- **ML Pipeline**: scikit-learn, pandas, numpy cho clustering & prediction
- **Time Series**: Prophet, LSTM cho dự báo dữ liệu môi trường

### 💾 Data Layer

- **Relational**: PostgreSQL + PostGIS (spatial queries, geometries)
- **Search**: OpenSearch/Elasticsearch (full-text search, aggregations)
- **Semantic**: MongoDB (JSON-LD storage), FiWARE Orion-LD (NGSI-LD entities)
- **Real-time**: Redis Pub/Sub (WebSocket broadcasts)

## Kiến trúc Microservices

Hệ thống được chia thành các services độc lập:

- **Auth Service**: Xác thực và phân quyền
- **User Service**: Quản lý người dùng
- **Environment Service**: Thu thập dữ liệu môi trường
- **Education Service**: Quản lý trường học và khóa học
- **AI Service**: Phân tích và dự báo
- **Map Service**: Xử lý GIS và bản đồ
- **OpenData Services**: Catalog, Export, LOD

## 🚀 Cách hoạt động (góc nhìn kiến trúc)

1. **Thu thập dữ liệu** 🌐  
   - ETL pipeline lấy dữ liệu từ OpenAQ, OpenWeather, Sentinel, OpenStreetMap và nguồn nội bộ (trường học, feedback công dân) → chuẩn hóa vào PostgreSQL/PostGIS, MongoDB.

2. **Xử lý & phân tích** 🤖  
   - Các dịch vụ AI (FastAPI) phân tích tương quan môi trường ↔ giáo dục, clustering khu vực, dự báo xu hướng và cập nhật entity NGSI-LD trong Orion-LD.

3. **Phục vụ qua API & OpenData** 🔗  
   - API Gateway (Traefik + Keycloak) điều phối request tới các microservice, đồng thời expose OpenData API và NGSI-LD API cho bên thứ ba.

4. **Hiển thị & tương tác** 🗺️  
   - Web Dashboard (Next.js) và Mobile App (React Native) hiển thị bản đồ 3D, dashboard, biểu đồ; người dùng tương tác, gửi feedback và nhận gợi ý hành động xanh theo thời gian thực.

Xem chi tiết trong [PROJECT_WORK.md](../PROJECT_WORK.md).

