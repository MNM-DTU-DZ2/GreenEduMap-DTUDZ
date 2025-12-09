--
-- GreenEduMap-DTUDZ - User-Specific Seed Data
-- Copyright (C) 2025 DTU-DZ2 Team
--
-- Seed data for user favorites, contributions, activities, settings
-- Each user has sample data based on their role
--

-- Clear existing data
TRUNCATE TABLE user_favorites CASCADE;
TRUNCATE TABLE user_contributions CASCADE;
TRUNCATE TABLE user_activities CASCADE;
TRUNCATE TABLE user_settings CASCADE;

-- ============================================
-- GET USER IDs (for reference)
-- ============================================
-- We'll use subqueries to get user IDs by email

-- ============================================
-- USER SETTINGS (for all users)
-- ============================================
INSERT INTO user_settings (user_id, notification_enabled, email_notifications, push_notifications, language, theme, default_city, privacy_level, data)
SELECT id, true, true, true, 'vi', 'dark', 'TP. Hồ Chí Minh', 'private', '{"dashboard_layout": "admin"}'
FROM users WHERE email = 'admin@greenedumap.vn';

INSERT INTO user_settings (user_id, notification_enabled, email_notifications, push_notifications, language, theme, default_city, privacy_level, data)
SELECT id, true, false, true, 'en', 'dark', 'TP. Hồ Chí Minh', 'public', '{"api_console": true}'
FROM users WHERE email = 'dev@greenedumap.vn';

INSERT INTO user_settings (user_id, notification_enabled, email_notifications, push_notifications, language, theme, default_city, privacy_level, data)
SELECT id, true, true, true, 'vi', 'light', 'Đà Nẵng', 'public', '{"school_dashboard": true}'
FROM users WHERE email = 'school1@dtu.edu.vn';

INSERT INTO user_settings (user_id, notification_enabled, email_notifications, push_notifications, language, theme, default_city, privacy_level, data)
SELECT id, true, true, true, 'vi', 'light', 'TP. Hồ Chí Minh', 'public', '{"volunteer_mode": true}'
FROM users WHERE email = 'volunteer1@gmail.com';

INSERT INTO user_settings (user_id, notification_enabled, email_notifications, push_notifications, language, theme, default_city, privacy_level, data)
SELECT id, true, false, true, 'vi', 'light', 'TP. Hồ Chí Minh', 'friends', '{"first_login": false}'
FROM users WHERE email = 'citizen1@gmail.com';

-- ============================================
-- USER FAVORITES - School User (school1@dtu.edu.vn)
-- ============================================
-- School favorites other schools & parks
INSERT INTO user_favorites (user_id, target_type, target_id, note, is_public)
SELECT u.id, 'school', s.id, 'Trường đối tác - trao đổi sinh viên', true
FROM users u, schools s
WHERE u.email = 'school1@dtu.edu.vn' AND s.name LIKE '%Bách Khoa%'
LIMIT 1;

INSERT INTO user_favorites (user_id, target_type, target_id, note, is_public)
SELECT u.id, 'green_zone', g.id, 'Địa điểm tổ chức hoạt động ngoại khóa', true
FROM users u, green_zones g
WHERE u.email = 'school1@dtu.edu.vn' AND g.zone_type = 'park'
LIMIT 1;

-- ============================================
-- USER FAVORITES - Volunteer (volunteer1@gmail.com)
-- ============================================
INSERT INTO user_favorites (user_id, target_type, target_id, note, is_public)
SELECT u.id, 'green_zone', g.id, 'Khu vực hoạt động tình nguyện', true
FROM users u, green_zones g
WHERE u.email = 'volunteer1@gmail.com' AND g.zone_type = 'park'
LIMIT 2;

INSERT INTO user_favorites (user_id, target_type, target_id, note, is_public)
SELECT u.id, 'recycling_center', r.id, 'Trung tâm tái chế gần nhà', false
FROM users u, recycling_centers r
WHERE u.email = 'volunteer1@gmail.com'
LIMIT 1;

-- ============================================
-- USER FAVORITES - Citizen (citizen1@gmail.com)
-- ============================================
INSERT INTO user_favorites (user_id, target_type, target_id, note, is_public)
SELECT u.id, 'school', s.id, 'Trường con đang học', false
FROM users u, schools s
WHERE u.email = 'citizen1@gmail.com' AND s.type = 'elementary'
LIMIT 1;

INSERT INTO user_favorites (user_id, target_type, target_id, note, is_public)
SELECT u.id, 'green_zone', g.id, 'Công viên gần nhà - hay đi dạo', true
FROM users u, green_zones g
WHERE u.email = 'citizen1@gmail.com' AND g.zone_type = 'park'
LIMIT 2;

-- ============================================
-- USER CONTRIBUTIONS - Volunteer (volunteer1@gmail.com)
-- ============================================
-- AQI Reports from volunteer
INSERT INTO user_contributions (user_id, type, title, description, location, latitude, longitude, address, status, is_public, data)
SELECT u.id, 'aqi_report', 'Báo cáo chất lượng không khí Q3', 
       'Đo lường AQI thực tế tại Công viên Lê Thị Riêng. Không khí trong lành, phù hợp tập thể dục buổi sáng.',
       ST_GeogFromText('SRID=4326;POINT(106.6867 10.7834)'), 10.7834, 106.6867,
       'Công viên Lê Thị Riêng, Quận 3, TP.HCM', 'approved', true,
       '{"aqi_value": 45, "pm25": 15.2, "measurement_method": "portable_sensor", "weather": "sunny"}'
FROM users u WHERE u.email = 'volunteer1@gmail.com';

INSERT INTO user_contributions (user_id, type, title, description, location, latitude, longitude, address, status, is_public, data)
SELECT u.id, 'aqi_report', 'Cảnh báo ô nhiễm khu công nghiệp',
       'Phát hiện khói thải từ nhà máy, mùi khó chịu. Cần kiểm tra.',
       ST_GeogFromText('SRID=4326;POINT(106.6602 10.7722)'), 10.7722, 106.6602,
       'Khu vực Quận 10, gần Đại học Bách Khoa', 'pending', true,
       '{"aqi_value": 120, "pm25": 55.8, "issue_type": "industrial_pollution", "photos": 2}'
FROM users u WHERE u.email = 'volunteer1@gmail.com';

-- Green spot discovery
INSERT INTO user_contributions (user_id, type, title, description, location, latitude, longitude, address, status, is_public, data)
SELECT u.id, 'green_spot', 'Phát hiện vườn cộng đồng mới',
       'Khu dân cư tự tổ chức trồng rau sạch, có khoảng 50 gia đình tham gia. Rất đẹp và xanh.',
       ST_GeogFromText('SRID=4326;POINT(106.7123 10.8089)'), 10.8089, 106.7123,
       'Hẻm 475 Điện Biên Phủ, Bình Thạnh', 'approved', true,
       '{"area_sqm": 200, "plants": ["vegetables", "herbs"], "community_size": 50}'
FROM users u WHERE u.email = 'volunteer1@gmail.com';

-- ============================================
-- USER CONTRIBUTIONS - Citizen (citizen1@gmail.com)
-- ============================================
INSERT INTO user_contributions (user_id, type, title, description, location, latitude, longitude, address, status, is_public, data)
SELECT u.id, 'feedback', 'Góp ý cải thiện công viên',
       'Công viên 30/4 rất đẹp nhưng thiếu thùng rác phân loại. Đề xuất lắp thêm thùng rác tái chế.',
       ST_GeogFromText('SRID=4326;POINT(106.6978 10.7712)'), 10.7712, 106.6978,
       'Công viên 30/4, Quận 1', 'approved', true,
       '{"category": "infrastructure", "priority": "medium"}'
FROM users u WHERE u.email = 'citizen1@gmail.com';

INSERT INTO user_contributions (user_id, type, title, description, location, latitude, longitude, address, status, is_public, data)
SELECT u.id, 'issue', 'Rác thải bừa bãi',
       'Phát hiện điểm đổ rác trái phép ở góc phố. Cần dọn dẹp và lắp camera.',
       ST_GeogFromText('SRID=4326;POINT(106.6934 10.7701)'), 10.7701, 106.6934,
       'Góc đường Nguyễn Huệ - Lê Lợi, Quận 1', 'pending', true,
       '{"category": "waste", "severity": "high", "photos": 3}'
FROM users u WHERE u.email = 'citizen1@gmail.com';

-- ============================================
-- USER CONTRIBUTIONS - Developer (dev@greenedumap.vn)
-- ============================================
INSERT INTO user_contributions (user_id, type, title, description, location, latitude, longitude, address, status, is_public, data)
SELECT u.id, 'feedback', 'API Enhancement Suggestion',
       'Đề xuất thêm endpoint /api/v1/analytics để truy vấn thống kê theo thời gian.',
       NULL, NULL, NULL, NULL, 'approved', true,
       '{"category": "api", "endpoint": "/api/v1/analytics", "priority": "high"}'
FROM users u WHERE u.email = 'dev@greenedumap.vn';

-- ============================================
-- USER ACTIVITIES - Admin
-- ============================================
INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'login', NULL, NULL, 'Đăng nhập hệ thống quản trị', false
FROM users u WHERE u.email = 'admin@greenedumap.vn';

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'approve', 'contribution', c.id, 'Phê duyệt đóng góp từ volunteer', false
FROM users u, user_contributions c
WHERE u.email = 'admin@greenedumap.vn' AND c.status = 'approved'
LIMIT 1;

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'update', 'system', NULL, 'Cập nhật cấu hình hệ thống', false
FROM users u WHERE u.email = 'admin@greenedumap.vn';

-- ============================================
-- USER ACTIVITIES - Developer
-- ============================================
INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'create', 'api_key', NULL, 'Tạo API key mới cho project', false
FROM users u WHERE u.email = 'dev@greenedumap.vn';

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'view', 'documentation', NULL, 'Xem API documentation', true
FROM users u WHERE u.email = 'dev@greenedumap.vn';

-- ============================================
-- USER ACTIVITIES - School
-- ============================================
INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'view', 'school', s.id, 'Xem thông tin trường', true
FROM users u, schools s
WHERE u.email = 'school1@dtu.edu.vn' AND s.code = 'DTU-DN-001'
LIMIT 1;

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'share', 'green_course', NULL, 'Chia sẻ khóa học xanh lên mạng xã hội', true
FROM users u WHERE u.email = 'school1@dtu.edu.vn';

-- ============================================
-- USER ACTIVITIES - Volunteer
-- ============================================
INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'create', 'contribution', c.id, 'Báo cáo chất lượng không khí mới', true
FROM users u, user_contributions c
WHERE u.email = 'volunteer1@gmail.com' AND c.type = 'aqi_report'
LIMIT 1;

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'favorite', 'green_zone', NULL, 'Thêm công viên vào danh sách yêu thích', true
FROM users u WHERE u.email = 'volunteer1@gmail.com';

-- ============================================
-- USER ACTIVITIES - Citizen
-- ============================================
INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'view', 'map', NULL, 'Xem bản đồ chất lượng không khí', false
FROM users u WHERE u.email = 'citizen1@gmail.com';

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'search', 'school', NULL, 'Tìm kiếm trường tiểu học gần nhà', false
FROM users u WHERE u.email = 'citizen1@gmail.com';

INSERT INTO user_activities (user_id, action, target_type, target_id, description, is_public)
SELECT u.id, 'create', 'contribution', c.id, 'Góp ý cải thiện công viên', true
FROM users u, user_contributions c
WHERE u.email = 'citizen1@gmail.com' AND c.type = 'feedback'
LIMIT 1;

-- ============================================
-- SUMMARY
-- ============================================
SELECT 'User-specific data seeded:' as status,
       (SELECT COUNT(*) FROM user_settings) as settings,
       (SELECT COUNT(*) FROM user_favorites) as favorites,
       (SELECT COUNT(*) FROM user_contributions) as contributions,
       (SELECT COUNT(*) FROM user_activities) as activities;
