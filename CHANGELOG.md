# Changelog
Tất cả những thay đổi đáng chú ý của dự án **GreenEduMap** sẽ được ghi lại tại đây.

Định dạng dựa trên **Keep a Changelog**, và dự án này tuân theo **Semantic Versioning**.

---

## [1.2.3]
### Updated
- Cập nhật Submodule cho hệ thống bản đồ và mô-đun AI
- Cải thiện chính xác hoá dữ liệu môi trường trong ETL pipeline

---

## [1.2.2] – 2025-01-18
### Added
- Thêm CI/CD workflow với GitHub Actions (build – test – deploy tự động)
- Bổ sung hướng dẫn đóng góp chi tiết trong `CONTRIBUTING.md`
- Mở kênh cộng đồng: Discord + Mailing list  
### Changed
- Cập nhật tài liệu cấu trúc thư mục và hướng dẫn test
- Tối ưu hóa script thu thập dữ liệu từ OpenAQ và Sentinel
### Security
- Thêm quy trình báo lỗi bảo mật (Security Disclosure Policy)

---

## [1.2.1] – 2025-01-12
### Added
- Module xuất dữ liệu GeoJSON/CSV từ Dashboard
- Thêm chế độ Dark Mode cho giao diện bản đồ
### Changed
- Cải tiến UI: màu, icon, độ tương phản
- Cải thiện tài liệu `setup.md` và quy trình cấu hình
### Fixed
- Sửa lỗi hiển thị ký tự tiếng Việt trên máy Windows
- Khắc phục lỗi định dạng thời gian trong biểu đồ

---

## [1.2.0] – 2025-01-10
### Added
- Tích hợp **AI Recommender**
  - Gợi ý khu vực trồng cây để giảm nhiệt độ
  - Gợi ý lắp đặt pin mặt trời theo mức bức xạ  
  - Đưa ra mức độ ưu tiên hành động theo dân số – chi phí
- Dashboard phân tích nâng cao: Heatmap, biểu đồ tương quan, xuất báo cáo
### Changed
- Tối ưu hiệu suất hiển thị bản đồ (Tile Cache + GeoJSON phân mảnh)
- Cải thiện hiệu năng API xử lý dữ liệu lớn
### Fixed
- Fix lỗi phân loại vùng Xanh – Vàng – Đỏ trong K-Means
- Khắc phục lỗi trùng tọa độ phường/xã

---

## [1.1.4]
### Updated
- Cập nhật Submodule cho các package xử lý raster, vector tiles
- Bổ sung caching cho request lặp lại

---

## [1.1.3]
### Added
- Tích hợp Submodule cho hệ thống cảm biến môi trường và bản đồ giáo dục

---

## [1.1.2] – 2024-12-07
### Added
- Thêm CI/CD với GitHub Actions
- Tài liệu “Hướng dẫn đóng góp” đầy đủ
- Mailing list và nhóm cộng đồng hỗ trợ người dùng
### Changed
- Cập nhật CONTRIBUTING.md với workflow Git chuẩn
- Bổ sung hướng dẫn chạy test & mock data
### Security
- Thêm quy trình báo cáo lỗ hổng bảo mật

---

## [1.1.1] – 2024-12-06
### Added
- Thêm các file JSON mẫu trong thư mục `datasets/`
- Hỗ trợ import dữ liệu trực tiếp từ JSON
### Changed
- Cập nhật đường dẫn đọc dữ liệu trong `setup.md`
- Cải thiện hướng dẫn import từ file ngoại tuyến
### Fixed
- Sửa lỗi hiển thị tiếng Việt trong README
- Khắc phục lỗi đường dẫn không hợp lệ trên Windows

---

## [1.1.0] – 2024-12-06
### Added
- Thêm hướng dẫn kết nối PostgreSQL + PostGIS
- Bổ sung URL DB mẫu để chạy nhanh cho người mới
- Thêm tài liệu tham khảo về dữ liệu vệ tinh Copernicus/Sentinel
### Changed
- Đơn giản hóa quy trình setup bằng Docker Compose
- Tổ chức lại cấu trúc `setup.md` cho rõ ràng
### Removed
- Gỡ bỏ các hình ảnh cũ không còn sử dụng
- Loại bỏ hướng dẫn cài đặt thủ công không cần thiết

---

## [1.0.1] – 2024-12-03
### Changed
- Cập nhật tên repo từ `greenedumap` sang `GreenEduMap-Platform`
- Chuẩn hóa cấu trúc dự án theo tiêu chuẩn open-source
- Cập nhật toàn bộ đường dẫn trong README và tài liệu
### Added
- Thêm hướng dẫn cài đặt chi tiết
- Thêm tài liệu về quy trình đóng góp
- Bổ sung CHANGELOG để theo dõi lịch sử thay đổi

---

## [1.0.0] – 2024-11-30
### Added
- Portal quản trị (Admin): quản lý dữ liệu, người dùng, thống kê
- Bản đồ môi trường: AQI, PM2.5, PM10, O3, NO2, cây xanh
- Bản đồ giáo dục xanh: trường học, hoạt động, xếp hạng
- Dashboard phân tích & thống kê
### Changed
- Nâng cấp giao diện người dùng (UI/UX)
- Tối ưu hiệu năng hệ thống
### Fixed
- Sửa lỗi xác thực đăng nhập
- Khắc phục lỗi đồng bộ dữ liệu

---

## [0.1.0] – 2024-11-25
### Added
- Khởi tạo dự án GreenEduMap
- Thiết kế kiến trúc hệ thống
- Xây dựng prototype bản đồ đầu tiên
