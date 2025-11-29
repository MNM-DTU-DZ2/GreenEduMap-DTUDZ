# 📝 Tổng quan về GreenEduMap

![Banner](assets/images/banner_greenedu.png)

## 🎯 Mục tiêu dự án

**GreenEduMap** là một dự án mã nguồn mở do đội **DTU-DZ_2** đến từ **Đại học Duy Tân** phát triển để tham gia cuộc thi **Olympic Tin học Sinh viên – Khối Mã nguồn mở 2025**. Dự án thuộc lĩnh vực đô thị thông minh xanh, với mục tiêu:

🤝 **Kết nối người dân – trường học – chính quyền** bằng bản đồ tri thức.

🔍 **Minh bạch hóa dữ liệu đô thị** theo từng khu vực để cộng đồng dễ tiếp cận.

🤖 **Tối ưu hóa quy trình ra quyết định bằng AI** giúp gợi ý hành động xanh phù hợp từng khu vực.

🎓 **Thúc đẩy giáo dục bền vững** và khuyến khích cộng đồng cùng đóng góp, mở rộng.

Dự án tập trung hình thành một nền tảng toàn diện kết hợp AI, GIS, OpenData và dashboard thời gian thực để tạo nên hệ sinh thái đô thị minh bạch, xanh và có khả năng mở rộng cho nhiều địa phương.

## ✨ Modules chính

### 1. 📱 Module tương tác người dân

🌍 Xem dữ liệu môi trường realtime (chất lượng không khí, nhiệt độ, cảnh báo ô nhiễm)

🏫 Tìm kiếm trường học xanh và khóa học bền vững (Green Skills)

📊 Theo dõi chất lượng sống theo từng khu vực

💡 Nhận gợi ý hành động xanh từ AI GreenBot

### 2. 🤖 Module phân tích AI & Dữ liệu

🧠 **AI GreenBot**: Phân tích tương quan môi trường ↔ giáo dục, phát hiện mẫu bất thường

📈 Clustering khu vực (Xanh – Vàng – Đỏ) dựa trên chỉ số môi trường

🔮 Dự báo xu hướng ô nhiễm và biến động mảng xanh

⭐ Đánh giá và gợi ý hành động xanh tự động cho từng khu vực

### 3. 🗺️ Module quản lý dữ liệu môi trường & giáo dục

🌡️ Thu thập và quản lý dữ liệu môi trường (OpenAQ, OpenWeather, Sentinel)

🏫 Quản lý trường học, khóa học xanh và tính toán Green Score

🗺️ Bản đồ 3D realtime hiển thị dữ liệu môi trường – giáo dục theo từng phường/xã

📊 Dashboard trực quan cho chính quyền và trường học

### 4. 📊 Module quản trị hệ thống & OpenData

📉 Dashboard tổng quan và báo cáo KPI cho cơ quan quản lý

🔗 API mở theo chuẩn NGSI-LD và Linked Open Data

📥 Export dữ liệu đa định dạng (JSON, CSV, GeoJSON, RDF)

⚙️ Phân quyền, quản lý người dùng và giám sát hệ thống

## 🏗️ Kiến trúc hệ thống

Hệ thống được thiết kế theo kiến trúc Microservices, đảm bảo khả năng mở rộng và xử lý dữ liệu lớn:

- **Frontend**: Next.js 15 (Web), React Native (Mobile)
- **Backend**: Laravel (PHP), FastAPI (Python cho AI)
- **Database**: PostgreSQL + PostGIS, MongoDB, Redis
- **Semantic**: FiWARE Orion-LD cho NGSI-LD
- **Infrastructure**: Docker, Kubernetes, Traefik

Xem chi tiết tại [Kiến trúc hệ thống](architecture.md).

## 🔗 Linked Open Data

GreenEduMap tuân thủ chuẩn **NGSI-LD** (ETSI GS CIM 009) để chia sẻ dữ liệu đô thị xanh theo hướng Linked Open Data.

Xem chi tiết tại [NGSI-LD Guide](api/ngsi-ld.md).


