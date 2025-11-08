# 🌿 Giới thiệu về dự án GreenEduMap

![Banner](assets/images/greenedumap_bannerchinh.png)

> *"Xanh hơn mỗi ngày – Dữ liệu vì cộng đồng xanh 🌍"*

**GreenEduMap** là hệ thống bản đồ học tập – môi trường – năng lượng mở của đô thị thông minh.  
Dự án xây dựng **hệ sinh thái dữ liệu mở phục vụ đô thị học tập xanh**, kết nối ba lĩnh vực: **môi trường – năng lượng – giáo dục cộng đồng** để giúp người dân, trường học và chính quyền ra quyết định dựa trên dữ liệu thật.

✅ Trực quan hóa dữ liệu theo phường/xã  
✅ Cảnh báo và phân tích xu hướng môi trường  
✅ Đánh giá chỉ số giáo dục xanh (Green Skills)  
✅ Gợi ý hành động xanh theo từng khu vực  
✅ Tích hợp Linked Open Data (RDF/JSON-LD)

Tác giả: **DTU_GreenCity Team**

---

# 💫 Tại sao GreenEduMap quan trọng?

Mỗi đô thị đang phát triển phải đối mặt với ô nhiễm, nhiệt độ tăng, đô thị hóa nhanh và thiếu dữ liệu minh bạch.  
GreenEduMap ra đời để:

- 🌍 **Minh bạch hóa dữ liệu đô thị**  
  Gộp các dữ liệu rời rạc về môi trường, giáo dục, năng lượng thành một hệ thống duy nhất.

- 📊 **Phân tích thông minh bằng AI**  
  Xác định khu vực "báo động môi trường" hoặc “giảm chất lượng học tập” do ô nhiễm, thiếu cây xanh.

- 🧠 **Hỗ trợ chính quyền và trường học**  
  Quy hoạch cây xanh – lớp học xanh – năng lượng mặt trời dựa trên dữ liệu thật.

- 🔥 **Theo dõi dữ liệu thời gian thực**  
  AQI, PM2.5, nhiệt độ bề mặt, năng lượng mặt trời, thống kê giáo dục.

- 🤝 **Kết nối cộng đồng – hành động xanh**  
  Doanh nghiệp, người dân, trường học có thể đề xuất sáng kiến xanh, thực hiện chiến dịch cộng đồng.

---

# ✅ Mục tiêu dự án
## 🎯 Mục tiêu tổng thể

Xây dựng **bản đồ tri thức đô thị xanh**, nơi dữ liệu môi trường – giáo dục – năng lượng được kết nối, phân tích và phục vụ cộng đồng.

## 🎯 Mục tiêu theo đối tượng

✔ **Người dân**  
- Xem bản đồ chất lượng sống  
- Hiểu tác động của môi trường lên sức khỏe và học tập  
- Nhận gợi ý hành động xanh (trồng cây, tiết kiệm năng lượng, tái chế)

✔ **Trường học & giáo viên**  
- Tích hợp dữ liệu môi trường thật vào bài giảng  
- Tổ chức khóa học “Green Skills”  
- Đánh giá mức độ xanh của trường

✔ **Chính quyền đô thị**  
- Ra quyết định quy hoạch cây xanh, năng lượng, cơ sở giáo dục  
- Theo dõi khu vực ô nhiễm và xu hướng thay đổi  
- Ưu tiên ngân sách cho địa bàn cần cải thiện

✔ **Doanh nghiệp xã hội – CSR**  
- Xác định khu vực nên tài trợ hoặc phát triển năng lượng tái tạo  
- Công khai hiệu quả các chiến dịch bảo vệ môi trường

---

# 🔍 Các tính năng chính
![Banner](assets/images/tinhnangchinh.png)
## 🗺 1. Bản đồ môi trường
- AQI, PM2.5, PM10, O3, NO2 theo từng phường/xã
- Nhiệt độ bề mặt từ vệ tinh Sentinel/Copernicus
- Lớp phủ cây xanh → phát hiện vùng “nóng đô thị”
- Chỉ số tiềm năng năng lượng mặt trời

## 📚 2. Bản đồ giáo dục xanh
- Trường học, hoạt động xanh, số khóa học “Green Skills”
- Xếp hạng trường theo chỉ số xanh
- Phân bố chương trình giáo dục bền vững

## 🧠 3. AI phân tích & dự báo
- Phân tích tương quan: **Môi trường ↔ Giáo dục**
- Clustering (K-Means) phân loại: **Xanh – Vàng – Đỏ**
- Dự báo xu hướng môi trường

## 🚀 4. AI Recommender
- Trồng bao nhiêu cây để giảm nhiệt độ & ô nhiễm?
- Khu vực nào cần mở khóa học xanh ngay?
- Nơi nào phù hợp để lắp pin mặt trời?
- Ưu tiên hành động theo tác động – chi phí – dân số

---

# 🧱 Kiến trúc hệ thống

```text
[OpenAQ / OpenWeather / Sentinel / Open Data Giáo dục]
│
▼
ETL Pipeline (Airflow)
- Collector API
- Làm sạch dữ liệu
- Chuyển đổi GeoJSON/CSV/Raster
│
▼
PostgreSQL + PostGIS + Tileserver
+ RDF/JSON-LD + DCAT
│
▼
FastAPI Backend
/env /edu /ml /recommend /lod
│
▼
Vue3 + MapboxGL/CesiumJS

Bản đồ 3D

Dashboard

Time series chart
```

---

# 🧩 Thành phần dữ liệu (Layers)
![Banner](assets/images/thanhphandulieu1.png)

### ✅ Environmental Layer
- AQI, PM2.5, PM10, tiếng ồn, cây xanh
- Nguồn: OpenAQ, OpenWeather, Copernicus, Sentinel

### ✅ Educational Layer
- Trường học, kỹ năng xanh, hoạt động cộng đồng
- Nguồn: data.moet.gov.vn, open data CSV

### ✅ Energy Layer
- Năng lượng mặt trời / gió
- Hiển thị heatmap vùng tiềm năng

### ✅ AI Behavior Layer
- Tương quan dữ liệu
- Gợi ý hành động xanh

### ✅ LOD Layer
- RDF + JSON-LD
- SPARQL endpoint
- Kết nối ChatGov AI / City Open Data

---

## 📌 Lợi ích mang lại

✅ Minh bạch dữ liệu môi trường – giáo dục  
✅ Công cụ ra quyết định cho chính quyền  
✅ Tăng nhận thức cộng đồng  
✅ Thúc đẩy giáo dục môi trường  
✅ Hỗ trợ nghiên cứu học thuật  
✅ Khuyến khích doanh nghiệp xanh đầu tư đúng điểm

---

## 🌏 Đối tượng hướng đến

- Người dân
- Chính quyền đô thị
- Trường học – giáo viên
- Nhà nghiên cứu & chuyên gia
- Doanh nghiệp năng lượng & CSR
- Tổ chức môi trường

---

## ✅ Một vài use-case thực tế

| Tình huống | GreenEduMap hỗ trợ |
|------------|--------------------|
| Khu vực đông dân, nóng đô thị | Gợi ý trồng cây bóng mát → giảm 2–4°C |
| Trường học thiếu chương trình xanh | Đề xuất mở lớp Green Skills |
| Doanh nghiệp CSR tìm nơi tài trợ | Chỉ ra phường nguy cơ cao, ít cây xanh |
| Chính quyền muốn đo hiệu quả trồng cây | Dashboard so sánh trước & sau 6 tháng |

---

## 🏗 Cấu trúc dự án

```text
greenedumap/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ ml/
│  │  ├─ models/
│  │  └─ services/
│  └─ requirements.txt
├─ frontend/
│  ├─ src/
│  └─ public/
├─ data/
│  ├─ geojson/
│  ├─ sentinel/
│  └─ openaq/
├─ docs/
│  ├─ api.md
│  └─ setup.md
└─ assets/
   └─ images/
```
---
## 📚 Hướng dẫn cài đặt
### ✅ Yêu cầu hệ thống

Node.js ≥ 16

Python ≥ 3.9

PostgreSQL + PostGIS

Docker & Docker Compose
---
### ✅ Chạy Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
---
### ✅ Chạy Frontend

```bash
cd frontend
npm install
npm run dev

```
---
### ✅ Docker
```bash
docker-compose up -d
```
---
### 🔌 API Endpoints
```http
GET /env/summary
GET /edu/schools
GET /ml/cluster
GET /ml/corr
POST /recommend
```
---
### 📑 Tài liệu chi tiết

API Docs: docs/api.md

Setup Guide: docs/setup.md

Data Dictionary: docs/data.md (dự kiến)
---
### 🤝 Đóng góp

Fork dự án

Tạo branch mới (feature/my-feature)

Commit (git commit -m "add feature")

Tạo Pull Request
---
### 🐛 Báo lỗi

Mô tả lỗi, bước tái hiện, ảnh chụp màn hình

Gửi vào mục Issues khi public repo
---
### 📝 License

(Thêm khi mở source)
---
## "Xanh hơn – Thông minh hơn – Dữ liệu mở vì cộng đồng 🌱"