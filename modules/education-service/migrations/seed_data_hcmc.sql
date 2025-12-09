--
-- GreenEduMap-DTUDZ - Ho Chi Minh City Seed Data
-- Copyright (C) 2025 DTU-DZ2 Team
--
-- Seed data for Education Service - HCMC Focus
-- HUTECH University, District 1, and District 3
--
-- NOTE: This file APPENDS to existing data (does not truncate)
--

-- ============================================
-- SCHOOLS IN HO CHI MINH CITY
-- ============================================

-- HUTECH University and surrounding (Quận 9)
INSERT INTO schools (name, code, location, address, city, district, type, total_students, total_teachers, total_trees, green_area, phone, email, website, is_public, green_score) VALUES
('Trường Đại học Công Nghệ TP.HCM (HUTECH)', 'HUTECH-001', ST_GeogFromText('SRID=4326;POINT(106.8067 10.8508)'), '475A Điện Biên Phủ, Phường 25', 'TP. Hồ Chí Minh', 'Bình Thạnh', 'university', 25000, 1200, 800, 15000, '028 5445 7777', 'info@hutech.edu.vn', 'https://hutech.edu.vn', true, 92.5),

-- District 1 - Universities and High Schools
('Trường Đại học Khoa học Tự nhiên', 'KHTN-001', ST_GeogFromText('SRID=4326;POINT(106.7017 10.7626)'), '227 Nguyễn Văn Cừ, Phường 4', 'TP. Hồ Chí Minh', 'Quận 5', 'university', 18000, 950, 600, 12000, '028 3835 1271', 'khtn@hcmus.edu.vn', 'https://hcmus.edu.vn', true, 88.0),

('Trường Đại học Bách Khoa', 'BK-HCM-001', ST_GeogFromText('SRID=4326;POINT(106.6602 10.7722)'), '268 Lý Thường Kiệt, Phường 14', 'TP. Hồ Chí Minh', 'Quận 10', 'university', 30000, 1500, 1000, 20000, '028 3865 4433', 'dhbk@hcmut.edu.vn', 'https://hcmut.edu.vn', true, 90.0),

('THPT Lê Hồng Phong', 'LHP-001', ST_GeogFromText('SRID=4326;POINT(106.6978 10.7769)'), '240 Nguyễn Thị Minh Khai, Phường 6', 'TP. Hồ Chí Minh', 'Quận 3', 'high', 1500, 85, 200, 3000, '028 3930 3611', 'lhp@q3.edu.vn', null, true, 85.5),

('THPT Trần Đại Nghĩa', 'TDN-001', ST_GeogFromText('SRID=4326;POINT(106.6924 10.7828)'), '20 Lý Tự Trọng, Phường Bến Nghé', 'TP. Hồ Chí Minh', 'Quận 1', 'high', 1800, 95, 250, 3500, '028 3822 5124', 'tdn@q1.edu.vn', null, true, 87.0),

('THPT Nguyễn Thị Minh Khai', 'NTMK-001', ST_GeogFromText('SRID=4326;POINT(106.6889 10.7756)'), '2 Nguyễn Thị Minh Khai, Phường Bến Nghé', 'TP. Hồ Chí Minh', 'Quận 1', 'high', 1400, 78, 180, 2800, '028 3829 7271', 'ntmk@q1.edu.vn', null, true, 83.0),

-- District 3 - High Schools and Middle Schools
('THPT Gia Định', 'GD-001', ST_GeogFromText('SRID=4326;POINT(106.6845 10.7889)'), '42 Trần Hưng Đạo, Phường 2', 'TP. Hồ Chí Minh', 'Quận 3', 'high', 1600, 88, 220, 3200, '028 3930 4521', 'gd@q3.edu.vn', null, true, 84.5),

('THPT Nguyễn Thượng Hiền', 'NTH-001', ST_GeogFromText('SRID=4326;POINT(106.6912 10.7845)'), '18 Võ Văn Tần, Phường 6', 'TP. Hồ Chí Minh', 'Quận 3', 'high', 1350, 75, 170, 2600, '028 3930 2145', 'nth@q3.edu.vn', null, true, 82.0),

('THCS Lê Quý Đôn', 'LQD-001', ST_GeogFromText('SRID=4326;POINT(106.6867 10.7801)'), '12 Lê Quý Đôn, Phường 7', 'TP. Hồ Chí Minh', 'Quận 3', 'middle', 1100, 62, 140, 2000, '028 3930 5678', 'lqd@q3.edu.vn', null, true, 79.5),

('THCS Trần Hưng Đạo', 'THD-001', ST_GeogFromText('SRID=4326;POINT(106.6923 10.7867)'), '28 Trần Hưng Đạo, Phường 1', 'TP. Hồ Chí Minh', 'Quận 3', 'middle', 950, 58, 120, 1800, '028 3930 6789', 'thd@q3.edu.vn', null, true, 77.0),

-- District 1 - Middle and Elementary Schools
('THCS Nguyễn Du', 'ND-HCM-001', ST_GeogFromText('SRID=4326;POINT(106.6956 10.7734)'), '15 Nguyễn Du, Phường Bến Nghé', 'TP. Hồ Chí Minh', 'Quận 1', 'middle', 1050, 60, 135, 1900, '028 3822 4567', 'nd@q1.edu.vn', null, true, 78.5),

('Tiểu học Lê Văn Tám', 'LVT-001', ST_GeogFromText('SRID=4326;POINT(106.6934 10.7712)'), '8 Lê Văn Tám, Phường Bến Thành', 'TP. Hồ Chí Minh', 'Quận 1', 'elementary', 800, 45, 100, 1400, '028 3822 3456', 'lvt@q1.edu.vn', null, true, 75.0),

('Tiểu học Trần Hưng Đạo', 'THD-TH-001', ST_GeogFromText('SRID=4326;POINT(106.6901 10.7689)'), '22 Trần Hưng Đạo, Phường Cầu Ông Lãnh', 'TP. Hồ Chí Minh', 'Quận 1', 'elementary', 750, 42, 95, 1300, '028 3836 2345', 'thd-th@q1.edu.vn', null, true, 74.0),

-- District 3 - Elementary Schools
('Tiểu học Võ Thị Sáu', 'VTS-001', ST_GeogFromText('SRID=4326;POINT(106.6878 10.7823)'), '35 Võ Thị Sáu, Phường 8', 'TP. Hồ Chí Minh', 'Quận 3', 'elementary', 820, 46, 105, 1450, '028 3930 1234', 'vts@q3.edu.vn', null, true, 76.0),

('Tiểu học Lý Thường Kiệt', 'LTK-001', ST_GeogFromText('SRID=4326;POINT(106.6845 10.7856)'), '42 Lý Thường Kiệt, Phường 9', 'TP. Hồ Chí Minh', 'Quận 3', 'elementary', 780, 44, 98, 1380, '028 3930 2345', 'ltk@q3.edu.vn', null, true, 75.5),

-- Bình Thạnh District (near HUTECH)
('THPT Bình Thạnh', 'BT-001', ST_GeogFromText('SRID=4326;POINT(106.7123 10.8123)'), '123 Điện Biên Phủ, Phường 15', 'TP. Hồ Chí Minh', 'Bình Thạnh', 'high', 1450, 80, 190, 2900, '028 3899 1234', 'bt@binhth anh.edu.vn', null, true, 81.0),

('THCS Bình Thạnh', 'BT-TH-001', ST_GeogFromText('SRID=4326;POINT(106.7089 10.8089)'), '89 Xô Viết Nghệ Tĩnh, Phường 17', 'TP. Hồ Chí Minh', 'Bình Thạnh', 'middle', 980, 56, 125, 1750, '028 3899 2345', 'bt-th@binhth anh.edu.vn', null, true, 77.5),

-- Additional Universities
('Trường Đại học Kinh tế TP.HCM', 'UEH-001', ST_GeogFromText('SRID=4326;POINT(106.6889 10.7623)'), '59C Nguyễn Đình Chiểu, Phường 6', 'TP. Hồ Chí Minh', 'Quận 3', 'university', 22000, 1100, 700, 14000, '028 3930 5588', 'info@ueh.edu.vn', 'https://ueh.edu.vn', true, 89.5),

('Trường Đại học Sư phạm TP.HCM', 'HCMUE-001', ST_GeogFromText('SRID=4326;POINT(106.6756 10.7623)'), '280 An Dương Vương, Phường 4', 'TP. Hồ Chí Minh', 'Quận 5', 'university', 20000, 1050, 650, 13000, '028 3835 5271', 'dhsp@hcmue.edu.vn', 'https://hcmue.edu.vn', true, 87.5),

('Trường Đại học Y Dược TP.HCM', 'UMP-001', ST_GeogFromText('SRID=4326;POINT(106.6845 10.7556)'), '217 Hồng Bàng, Phường 11', 'TP. Hồ Chí Minh', 'Quận 5', 'university', 15000, 850, 500, 10000, '028 3855 4269', 'dhyd@ump.edu.vn', 'https://ump.edu.vn', true, 86.0),

-- International Schools
('Trường Quốc tế Anh Việt (BVIS)', 'BVIS-001', ST_GeogFromText('SRID=4326;POINT(106.7234 10.8234)'), '225 Nguyễn Văn Hưởng, Thảo Điền', 'TP. Hồ Chí Minh', 'Quận 2', 'international', 1200, 120, 300, 5000, '028 3744 2335', 'info@bvis.edu.vn', 'https://bvis.edu.vn', true, 93.0);

-- ============================================
-- GREEN COURSES
-- ============================================

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public) 
SELECT 
    id,
    'Công nghệ Xanh và Phát triển Bền vững',
    'Khóa học về công nghệ xanh, năng lượng tái tạo và phát triển bền vững tại đô thị',
    'environment',
    12,
    50,
    true
FROM schools WHERE code = 'HUTECH-001';

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public)
SELECT
    id,
    'Năng lượng Tái tạo và Ứng dụng',
    'Workshop thực hành về năng lượng mặt trời, gió và các nguồn năng lượng sạch',
    'energy',
    10,
    40,
    true
FROM schools WHERE code = 'BK-HCM-001';

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public)
SELECT
    id,
    'Biến đổi Khí hậu và Giải pháp Xanh',
    'Nghiên cứu về biến đổi khí hậu và các giải pháp xanh cho thành phố',
    'climate',
    14,
    45,
    true
FROM schools WHERE code = 'KHTN-001';

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public)
SELECT
    id,
    'Kinh tế Xanh và Phát triển Bền vững',
    'Khóa học về kinh tế xanh, doanh nghiệp bền vững và trách nhiệm xã hội',
    'sustainability',
    12,
    60,
    true
FROM schools WHERE code = 'UEH-001';

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public)
SELECT
    id,
    'Giáo dục Môi trường cho Học sinh',
    'Chương trình giáo dục môi trường và ý thức bảo vệ thiên nhiên',
    'environment',
    8,
    35,
    true
FROM schools WHERE code = 'LHP-001';
