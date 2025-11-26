# GreenEduMap

Nền tảng giáo dục môi trường tích hợp bản đồ 3D hiển thị AQI, năng lượng xanh, và các hành động xanh được đề xuất bởi AI.

## 🌱 Giới thiệu

GreenEduMap là nền tảng toàn diện kết hợp giữa giáo dục môi trường và công nghệ bản đồ 3D, giúp người dùng:
- Theo dõi chất lượng không khí (AQI) theo thời gian thực
- Khám phá các trường học và khu vực xanh
- Nhận gợi ý hành động xanh từ AI
- Tham gia các khóa học về môi trường
- Đóng góp ý tưởng cho cộng đồng xanh

## 🎯 Tác nhân & Màn hình

### 🏠 1. Trang công cộng (Citizen)

| Screen | Mô tả | Thành phần chính |
|--------|-------|------------------|
| **/ – Trang chủ** | Giới thiệu dự án, link đến bản đồ | HeroSection, About, CTA |
| **/map – Bản đồ sống xanh** | Bản đồ 3D hiển thị AQI, nhiệt độ, năng lượng, trường học | CesiumJS/MapboxGL, LayerToggle |
| **/actions – Gợi ý hành động xanh** | Hiển thị các đề xuất AI | ActionCard, FilterBar |
| **/feedback – Gửi ý tưởng xanh** | Form upload text + ảnh | Formik, Upload component |
| **/stats – Tổng quan khu vực** | Biểu đồ so sánh khu vực (Recharts) | BarChart, RadarChart |

### 🧑‍🏫 2. Trang của Đơn vị giáo dục (School)

| Screen | Mô tả | Thành phần chính |
|--------|-------|------------------|
| **/school/dashboard** | Thống kê học viên, lớp học xanh | Table + Recharts |
| **/school/courses** | Danh sách khóa học xanh | CourseCard, CRUD modals |
| **/school/new** | Tạo khóa học xanh mới | Form component |
| **/school/profile** | Hồ sơ trường | Profile card + edit form |

### 🏛️ 3. Trang quản lý (Admin)

| Screen | Mô tả | Thành phần chính |
|--------|-------|------------------|
| **/admin/dashboard** | Tổng quan thành phố (chỉ số AQI, năng lượng, học tập) | Multi-card dashboard, Recharts, Map overview |
| **/admin/wards** | Quản lý dữ liệu từng phường | Table, map bounding boxes |
| **/admin/ai** | Xem kết quả AI tương quan | Correlation heatmap, AIInsightCard |
| **/admin/users** | Quản lý người dùng / quyền hạn | CRUD table |
| **/admin/logs** | Nhật ký hệ thống | Timeline / AuditLog |

### 🤖 4. Trang AI GreenBot (Chat & Recommendation)

| Screen | Mô tả | Thành phần chính |
|--------|-------|------------------|
| **/chat** | Chat với AI GreenBot (API Coze hoặc Gemini) | ChatUI + backend proxy |
| **/recommendations** | Danh sách hành động xanh AI đề xuất | List + impact chart |

## 🛠️ Tech Stack

- **Framework**: Next.js 15.2.3
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.0
- **UI Components**: Custom components với shadcn/ui patterns
- **Charts**: ApexCharts & Recharts
- **Maps**: Mapbox GL & CesiumJS (tùy chọn)
- **Forms**: React Dropzone, Flatpickr
- **State Management**: Zustand
- **API**: React Query (TanStack Query)

## 📦 Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd GreenEduMap_fe
```

2. Cài đặt dependencies:
```bash
yarn install
```

3. Thiết lập environment variables (tạo file `.env.local`):
```env
# Database
DATABASE_URL="postgresql://..."

# API Keys
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
NEXT_PUBLIC_AI_API_KEY=your_ai_api_key

# App
NEXT_PUBLIC_API_URL=http://localhost:3000
JWT_SECRET=your_jwt_secret
```

4. Chạy migrations:
```bash
yarn prisma:migrate
```

5. Chạy development server:
```bash
yarn dev
```

6. Mở [http://localhost:3000](http://localhost:3000) trong trình duyệt.

## 🌐 Routes Structure

```
/                           # Trang chủ công cộng
/map                        # Bản đồ sống xanh
/actions                    # Gợi ý hành động xanh
/feedback                   # Gửi ý tưởng
/stats                      # Thống kê khu vực

/school/*                   # Routes của đơn vị giáo dục
  ├── /dashboard            # Dashboard trường học
  ├── /courses              # Danh sách khóa học
  ├── /new                  # Tạo khóa học mới
  └── /profile              # Hồ sơ trường

/admin/*                    # Routes của quản trị viên
  ├── /dashboard            # Tổng quan hệ thống
  ├── /wards                # Quản lý phường
  ├── /ai                   # AI insights
  ├── /users                # Quản lý người dùng
  └── /logs                 # Nhật ký hệ thống

/chat                       # Chat với AI GreenBot
/recommendations            # Đề xuất từ AI
```

## 🎨 Theme Support

GreenEduMap hỗ trợ light và dark theme:
- Toggle theme trong header
- Theme preference được lưu tự động
- Dark mode được tối ưu cho trải nghiệm tốt nhất

## 📱 Responsive Design

Platform hoạt động mượt mà trên:
- Desktop (1920px+)
- Laptop (1024px - 1919px)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🚦 Available Scripts

- `yarn dev` - Chạy development server
- `yarn build` - Build cho production
- `yarn start` - Chạy production server
- `yarn lint` - Chạy ESLint
- `yarn prisma:generate` - Generate Prisma client
- `yarn prisma:migrate` - Chạy database migrations
- `yarn prisma:seed` - Seed database với dữ liệu mẫu

## 🔐 Authentication & Authorization

Hệ thống phân quyền dựa trên vai trò:
- **Citizen** - Người dùng công cộng (xem bản đồ, gửi feedback)
- **School** - Đơn vị giáo dục (quản lý khóa học, học viên)
- **Admin** - Quản trị viên (quản lý toàn bộ hệ thống)

## 🗄️ Database Schema

Dự án sử dụng Prisma ORM với PostgreSQL:
- Users & Authentication
- Schools & Courses
- Environmental Data (AQI, Energy, etc.)
- AI Recommendations
- User Feedback

## 📊 Features

### Bản đồ 3D
- Hiển thị AQI theo thời gian thực
- Nhiệt độ và độ ẩm
- Trường học và khu vực xanh
- Năng lượng tái tạo

### AI GreenBot
- Chat thông minh về môi trường
- Đề xuất hành động xanh cá nhân hóa
- Phân tích dữ liệu môi trường

### Giáo dục
- Khóa học trực tuyến
- Tài liệu học tập
- Gamification & thành tích

### Quản lý
- Dashboard tổng quan
- Phân tích dữ liệu
- Quản lý người dùng

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

Dự án được phát hành dưới giấy phép MIT.

## 👥 Support

Để được hỗ trợ và đặt câu hỏi:
- Tạo issue trong repository
- Liên hệ development team

## 🙏 Acknowledgments

- Next.js team
- Mapbox & CesiumJS
- Tailwind CSS
- Các thư viện open-source đã sử dụng

---

**GreenEduMap** - Kết nối giáo dục và môi trường xanh cho tương lai bền vững 🌱
