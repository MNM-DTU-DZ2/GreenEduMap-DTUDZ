# 🌿 Giới thiệu về dự án GreenEduMap

![Banner](assets/images/greenedumap_banner2.jpg)

**GreenEduMap** là nền tảng bản đồ 3D – dashboard – dữ liệu mở cho đô thị thông minh, kết nối ba lĩnh vực: **môi trường – giáo dục – năng lượng** để phục vụ người dân, chính quyền, trường học, nhà nghiên cứu, doanh nghiệp và tổ chức môi trường.

Nền tảng tích hợp dữ liệu phân tán từ OpenAQ, OpenWeather, Sentinel, OpenStreetMap… sau đó chuẩn hóa bằng NGSI-LD / Linked Open Data và hiển thị trực quan trên bản đồ 3D với phân tích AI và gợi ý hành động xanh.

---

## 💡 Tại sao lại có dự án này?

Chúng ta đều thấy các đô thị đang phát triển nhanh chóng, và các vấn đề như ô nhiễm không khí, hiệu ứng đảo nhiệt đô thị, thiếu cây xanh hay chất lượng giáo dục môi trường đang trở nên nghiêm trọng hơn. Tuy nhiên:

- Dữ liệu môi trường, giáo dục và năng lượng tồn tại rời rạc ở nhiều nguồn khác nhau, khó truy cập và thiếu chuẩn hóa.

- Chính quyền thiếu công cụ phân tích tổng hợp để ra quyết định quy hoạch cây xanh, năng lượng tái tạo hay giáo dục bền vững dựa trên dữ liệu khoa học.

- Người dân và trường học không có nguồn thông tin đáng tin cậy, trực quan về chất lượng môi trường và các hoạt động xanh quanh khu vực mình.

GreenEduMap ra đời để giải quyết những vấn đề đó, hướng tới một đô thị minh bạch hơn, thông minh hơn và bền vững hơn thông qua dữ liệu mở và giáo dục xanh.

---

## 👥 Dự án này dành cho ai?

![Banner](assets/images/Du_an_nay_cho_ai_greenedumap.png)

1. **Người dân** → xem chất lượng sống và nhận gợi ý hành động xanh, cung cấp thông tin môi trường cho lối sống xanh.

2. **Chính quyền** → ra quyết định dựa trên dữ liệu, sử dụng dữ liệu để quản lý đô thị hiệu quả.

3. **Trường học** → triển khai giáo dục xanh (Green Skills), tích hợp dữ liệu vào giáo dục môi trường.

4. **Nhà nghiên cứu** → truy cập dữ liệu mở chuẩn hóa để nghiên cứu và đổi mới, xây dựng mô hình AI/ML.

5. **Doanh nghiệp xanh** → tìm vị trí thích hợp để đầu tư CSR hoặc năng lượng tái tạo, sử dụng dữ liệu cho các sáng kiến bền vững.

6. **Tổ chức môi trường** → sử dụng dữ liệu cho vận động và giám sát, xây dựng chiến dịch truyền thông dựa trên dữ liệu thật.

---

## ✨ Có gì đặc biệt?

![Banner](assets/images/tinh_nang_chinh_greenedumap.png)

- **Bản đồ 3D realtime** — hiển thị dữ liệu môi trường, giáo dục, năng lượng theo thời gian thực với các lớp dữ liệu đa tầng, hỗ trợ tương tác và zoom chi tiết.

- **AI GreenBot + phân tích** — chatbot AI hỗ trợ tư vấn, phân tích tương quan môi trường ↔ giáo dục, clustering khu vực, và gợi ý hành động xanh thông minh.

- **Dashboard đa vai trò** — giao diện tùy biến cho từng đối tượng: chính quyền (KPI, điểm nóng), trường học (khóa học xanh), người dân (chất lượng sống).

- **API mở** — RESTful API theo chuẩn NGSI-LD và Linked Open Data (RDF/JSON-LD), hỗ trợ tích hợp với hệ thống thành phố và bên thứ ba.

- **Thống kê & báo cáo** — biểu đồ xu hướng, so sánh khu vực, export dữ liệu, và báo cáo tự động cho các đối tượng khác nhau.

---

## 🎯  Mục tiêu dự án
![Banner](assets/images/muc_tieu_greenedumap.png)
### 🎯 Mục tiêu tổng thể
Xây dựng bản đồ tri thức đô thị xanh nơi dữ liệu → AI → hành động xanh → cải thiện chất lượng sống.

### 🎯 Mục tiêu cụ thể
- Tăng tính minh bạch dữ liệu đô thị — công khai dữ liệu môi trường, giáo dục, năng lượng theo từng khu vực.
- Xây dựng hệ thống dữ liệu mở theo chuẩn NGSI-LD và Linked Open Data.
- Tối ưu hóa quy trình ra quyết định bằng AI (phân tích tương quan, gợi ý hành động xanh).
- Thúc đẩy giáo dục bền vững (Green Skills) — cung cấp dữ liệu môi trường thật và hệ sinh thái khóa học xanh.
- Khuyến khích cộng đồng đóng góp và mở rộng — mã nguồn mở (GPL v3), API mở, hỗ trợ triển khai đa thành phố.
- Hỗ trợ nghiên cứu và phát triển giải pháp thông minh cho đô thị.
- Xây dựng hệ sinh thái đô thị thông minh, hỗ trợ mô phỏng và dự báo.

---

## 💫  Thách thức mà dự án hướng tới?

- Dữ liệu đô thị hiện tại rời rạc, khó truy cập, thiếu chuẩn hóa.
- Chính quyền thiếu công cụ phân tích nhiệt độ – ô nhiễm – năng lượng – giáo dục theo từng phường/xã.
- Trường học cần dữ liệu thật để dạy kỹ năng xanh.
- Người dân không có nguồn thông tin đáng tin cậy về chất lượng sống quanh mình.
- Cộng đồng thiếu hành vi xanh vì không biết bắt đầu từ đâu.

---

## 🛠️  Giải pháp của dự án
![Banner](assets/images/muc_tieu_greenedumap.png)
- Bản đồ 3D tương tác hiển thị dữ liệu môi trường, giáo dục, năng lượng theo từng phường/xã với các lớp dữ liệu đa tầng.

- ETL Pipeline tích hợp và chuẩn hóa dữ liệu từ nhiều nguồn mở (OpenAQ, OpenWeather, Sentinel, OpenStreetMap).

- AI phân tích tương quan môi trường ↔ giáo dục, clustering khu vực (Xanh – Vàng – Đỏ), và gợi ý hành động xanh dựa trên dữ liệu.

- Dashboard trực quan cho từng đối tượng: chính quyền (phân tích KPI, điểm nóng), trường học (quản lý khóa học xanh), người dân (theo dõi chất lượng sống).

- Hệ thống giáo dục bền vững (Green Skills) — quản lý khóa học, hoạt động xanh, và đánh giá chỉ số "Trường học xanh".

- API mở theo chuẩn NGSI-LD và Linked Open Data (RDF/JSON-LD) để tích hợp với hệ thống thành phố và bên thứ ba.

- Digital Twin đô thị xanh — tạo bản sao số cho từng phường/xã với dữ liệu real-time, hỗ trợ mô phỏng và dự báo xu hướng.

- Mã nguồn mở (GPL v3) với quy trình đóng góp rõ ràng, hỗ trợ triển khai đa thành phố và mở rộng cộng đồng.

---

## 👥 4. Vai trò & phân quyền

| Vai trò | Khả năng | Màn hình |
| --- | --- | --- |
| 👨‍💻 Admin | Quản lý dữ liệu, phân quyền, cấu hình AI | Dashboard, Wards, Users, Logs |
| 🧑‍🏫 School | Khóa học xanh, học viên, báo cáo | Courses, Students, Activities |
| 👩‍💼 Citizen | Bản đồ, phản hồi, nhận gợi ý AI | Map, Feedback, Actions, Stats |

---

## 🧱 5. Kiến trúc hệ thống
![Banner](assets/images/Kien_truc_he_thong_GreenEduMap.png)

### Thành phần và công nghệ sử dụng

| Thành phần | Công nghệ sử dụng |
|-----------|-------------------|
| **Mobile App** | React Native (iOS & Android) |
| **Web Dashboard** | Next.js 15 |
| **Backend Core** | Laravel (PHP), Redis (Cache) |
| **AI Services** | FastAPI (Python) cho NLP, Computer Vision, scikit-learn |
| **API Gateway** | Traefik, Keycloak (Auth) |
| **Message Broker** | Apache Kafka, MQTT (EMQX/Mosquitto) |
| **Realtime** | Reverb (WebSocket) |
| **Database** | PostgreSQL + PostGIS (GeoData), OpenSearch |
| **Semantic** | FiWARE Orion-LD, MongoDB |


---

## 🔄 6. Cách hoạt động

Quy trình đơn giản như sau:

**Người dân/Trường học/Chính quyền truy cập hệ thống** 📱 → Xem bản đồ 3D, dashboard, hoặc gửi phản hồi qua Web/Mobile App.

**Hệ thống thu thập dữ liệu** 🌐 → ETL Pipeline tự động lấy dữ liệu từ OpenAQ, OpenWeather, Sentinel, OpenStreetMap → Làm sạch và chuẩn hóa.

**AI phân tích & xử lý** 🤖 → Phân tích tương quan môi trường ↔ giáo dục, clustering khu vực, gợi ý hành động xanh → Cập nhật NGSI-LD Entities.

**Hiển thị kết quả** 🗺️ → Dữ liệu được hiển thị trên bản đồ 3D realtime, dashboard đa vai trò, và thống kê → Người dùng nhận gợi ý hành động xanh từ AI.

---

## 🧩 7. Thành phần dữ liệu (Data Layers)

### ✔ Environmental Layer
- AQI, PM2.5, PM10, O₃, NO₂
- Nhiệt độ bề mặt (Sentinel)
- Cây xanh, mật độ phủ xanh
- Tiềm năng năng lượng mặt trời

### ✔ Educational Layer
- Trường học
- Hoạt động xanh
- Khóa học Green Skills

### ✔ Energy Layer
- Solar radiation
- Renewable potential heatmap

### ✔ AI Layer
- Clustering: Xanh – Vàng – Đỏ
- Correlation: Môi trường ↔ Giáo dục ↔ Dân cư
- Gợi ý hành động xanh

### ✔ LOD / NGSI-LD Layer
- RDF/JSON-LD
- Turtle
- SOSA/SSN
- Digital Twin cho từng phường/xã
---

## 🌿 8. Lợi ích mang lại

### 🌍 Minh bạch dữ liệu đô thị
Dữ liệu phân tán → chuẩn hóa → hiển thị trực quan.

### 🏛 Hỗ trợ quyết định cho chính quyền
- Xác định điểm nóng đô thị
- Quy hoạch cây xanh / năng lượng tái tạo
- Ưu tiên ngân sách theo mức độ rủi ro

### 🎓 Thúc đẩy giáo dục xanh
- Khóa học Green Skills
- Hoạt động dựa trên dữ liệu thật
- Chỉ số "Trường học xanh"

### 👨‍👩‍👧 Người dân chủ động hành động xanh
- Nhận cảnh báo môi trường
- Gợi ý hành động theo khu vực
- Theo dõi chất lượng sống quanh mình

---

## 📁 9. Cấu trúc thư mục

```
GreenEduMap
├── backend/            # FastAPI, services, AI models
├── frontend/           
├── app/           
├── docker/             # Deployment stack
├── data/               # SQL seeds, GeoJSON, raster
├── docs/               # Documentation, diagrams
├── scripts/            # ETL, LOD exports
└── .github/workflows/  # CI/CD pipelines
```

---

## 🗂 10. Dữ liệu & mô hình

- `users` – Admin, School, Citizen
- `schools`, `courses`, `enrollments`
- `air_quality`, `weather`, `energy_data`
- `citizen_feedback`
- `ai_analysis`, `ai_clusters`

**Bảng GIS:** `geometry(Point, 4326)` + GiST Index  
**LOD Export:** JSON-LD / Turtle / RDF-XML, FiWARE Smart Data Models, W3C SOSA/SSN

---

## 🧪 11. Kiểm thử

```bash
cd backend
pytest -v --cov=app

cd frontend
npm run test
```

---

## 📄 12. Tài liệu liên quan

| File | Mô tả |
| --- | --- |
| `docs/architecture.md` | Kiến trúc chi tiết |
| `docs/api_reference.md` | API đầy đủ |
| `docs/open_data_standards.md` | NGSI-LD, SOSA/SSN, LOD |
| `CONTRIBUTING.md` | Quy tắc đóng góp |

---

## 🤝 13. Đóng góp

1. Fork repo
2. Tạo branch `git checkout -b feature/my-feature`
3. Viết test + cập nhật docs
4. `git commit -m "feat: add xyz"`
5. `git push` & mở Pull Request

Tuân thủ Conventional Commits & Code Style của dự án.

---

## 👥 14. Team Members

| Vai trò | Thành viên | Email |
| --- | --- | --- |
| Leader | Nguyễn Quốc Long | quoclongdng@gmail.com |
| Developer | Trần Xuân Trường | xuantruong081205@gmail.com |
| Developer | Hồ Dương Quốc Huy | huyho2782005@gmail.com |
| Developer | Lê Tuấn Minh | llttminh@gmail.com |

---

## 📜 15. License

MIT License – xem file `LICENSE` để biết chi tiết.

---

🎉 **GreenEduMap – Built for OLP 2025 Smart City Challenge**  
🌿 *Empowering sustainable cities through open data and education.*
