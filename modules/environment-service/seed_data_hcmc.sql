--
-- GreenEduMap-DTUDZ - Ho Chi Minh City Environment Seed Data
-- Green Zones, Air Quality, Weather, Solar Resources
--
-- NOTE: This file APPENDS to existing data (does not truncate)
--

-- ============================================
-- GREEN ZONES (Parks and Green Spaces)
-- ============================================

-- District 1 Parks
INSERT INTO green_zones (name, code, location, area_sqm, tree_count, zone_type, address, is_public) VALUES
('Công viên 30 Tháng 4', 'CV-Q1-001', ST_GeogFromText('SRID=4326;POINT(106.6978 10.7712)'), 125000, 2500, 'park', 'Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh', true),
('Công viên Tao Đàn', 'CV-Q1-002', ST_GeogFromText('SRID=4326;POINT(106.6923 10.7789)'), 102000, 1800, 'park', 'Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh', true),
('Công viên Lê Văn Tám', 'CV-Q1-003', ST_GeogFromText('SRID=4326;POINT(106.6934 10.7701)'), 38000, 650, 'park', 'Phường Bến Thành, Quận 1, TP. Hồ Chí Minh', true),

-- District 3 Parks
('Công viên Lê Thị Riêng', 'CV-Q3-001', ST_GeogFromText('SRID=4326;POINT(106.6867 10.7834)'), 45000, 850, 'park', 'Phường 8, Quận 3, TP. Hồ Chí Minh', true),
('Công viên Hoàng Văn Thụ', 'CV-Q3-002', ST_GeogFromText('SRID=4326;POINT(106.6889 10.7867)'), 52000, 950, 'park', 'Phường 4, Quận 3, TP. Hồ Chí Minh', true),
('Công viên Văn hóa Quận 3', 'CV-Q3-003', ST_GeogFromText('SRID=4326;POINT(106.6845 10.7801)'), 68000, 1200, 'park', 'Phường 7, Quận 3, TP. Hồ Chí Minh', true),

-- Bình Thạnh District (near HUTECH)
('Công viên Gia Định', 'CV-BT-001', ST_GeogFromText('SRID=4326;POINT(106.7089 10.8156)'), 89000, 1600, 'park', 'Phường 15, Bình Thạnh, TP. Hồ Chí Minh', true),
('Công viên Lê Thị Riêng', 'CV-BT-002', ST_GeogFromText('SRID=4326;POINT(106.7123 10.8089)'), 42000, 780, 'park', 'Phường 17, Bình Thạnh, TP. Hồ Chí Minh', true),

-- District 11 Parks
('Công viên Đầm Sen', 'CV-Q11-001', ST_GeogFromText('SRID=4326;POINT(106.6378 10.7656)'), 500000, 8000, 'park', 'Phường 4, Quận 11, TP. Hồ Chí Minh', true),

-- Green Corridors
('Đại lộ Nguyễn Huệ', 'GC-Q1-001', ST_GeogFromText('SRID=4326;POINT(106.7006 10.7745)'), 25000, 450, 'street', 'Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh', true),
('Đường Lê Duẩn', 'GC-Q1-002', ST_GeogFromText('SRID=4326;POINT(106.6934 10.7823)'), 32000, 580, 'street', 'Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh', true),

-- University Campuses (Green Spaces)
('Khuôn viên HUTECH', 'CAMPUS-001', ST_GeogFromText('SRID=4326;POINT(106.8067 10.8508)'), 150000, 800, 'campus', '475A Điện Biên Phủ, Bình Thạnh, TP. Hồ Chí Minh', true),
('Khuôn viên Đại học Bách Khoa', 'CAMPUS-002', ST_GeogFromText('SRID=4326;POINT(106.6602 10.7722)'), 200000, 1000, 'campus', '268 Lý Thường Kiệt, Quận 10, TP. Hồ Chí Minh', true),

-- Riverside Parks
('Công viên Bạch Đằng', 'CV-RS-001', ST_GeogFromText('SRID=4326;POINT(106.7089 10.7689)'), 75000, 1300, 'riverside', 'Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh', true),
('Công viên Bến Bạch Đằng', 'CV-RS-002', ST_GeogFromText('SRID=4326;POINT(106.7123 10.7712)'), 58000, 980, 'riverside', 'Phường Tân Định, Quận 1, TP. Hồ Chí Minh', true);

-- ============================================
-- AIR QUALITY MONITORING STATIONS
-- ============================================

INSERT INTO air_quality (location, aqi, pm25, pm10, co, no2, o3, so2, source, station_name, measurement_date) VALUES
-- District 1 Stations
(ST_GeogFromText('SRID=4326;POINT(106.7006 10.7745)'), 78.5, 28.3, 52.8, 0.6, 22.5, 38.9, 10.2, 'sensor', 'Quận 1 - Trung tâm', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.6978 10.7712)'), 65.2, 22.1, 45.3, 0.5, 18.7, 32.4, 8.5, 'sensor', 'Công viên 30/4', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.7089 10.7689)'), 58.3, 18.5, 38.9, 0.4, 15.2, 28.6, 6.8, 'sensor', 'Bến Bạch Đằng', NOW() - INTERVAL '30 minutes'),

-- District 3 Stations
(ST_GeogFromText('SRID=4326;POINT(106.6867 10.7834)'), 72.8, 25.6, 48.7, 0.5, 20.3, 35.2, 9.1, 'sensor', 'Quận 3 - Trung tâm', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.6889 10.7867)'), 68.4, 23.8, 46.2, 0.5, 19.1, 33.8, 8.7, 'sensor', 'Công viên Hoàng Văn Thụ', NOW() - INTERVAL '30 minutes'),

-- Bình Thạnh (HUTECH area)
(ST_GeogFromText('SRID=4326;POINT(106.8067 10.8508)'), 82.3, 31.2, 58.5, 0.7, 24.8, 42.1, 11.5, 'sensor', 'HUTECH University', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.7089 10.8156)'), 75.6, 27.4, 51.2, 0.6, 21.9, 37.5, 9.8, 'sensor', 'Công viên Gia Định', NOW() - INTERVAL '30 minutes'),

-- Industrial/Traffic Areas
(ST_GeogFromText('SRID=4326;POINT(106.6602 10.7722)'), 95.8, 42.5, 78.3, 1.2, 32.6, 48.7, 15.2, 'sensor', 'Khu vực Bách Khoa', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.6756 10.7623)'), 88.2, 36.8, 68.9, 0.9, 28.4, 44.2, 13.1, 'sensor', 'Quận 5 - Công nghiệp', NOW() - INTERVAL '30 minutes'),

-- Residential Areas
(ST_GeogFromText('SRID=4326;POINT(106.6934 10.7701)'), 62.5, 20.8, 42.1, 0.4, 16.8, 30.2, 7.3, 'sensor', 'Khu dân cư Quận 1', NOW() - INTERVAL '30 minutes');

-- ============================================
-- WEATHER STATIONS
-- ============================================

INSERT INTO weather (location, city_name, temperature, feels_like, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, source, observation_time) VALUES
-- District 1
(ST_GeogFromText('SRID=4326;POINT(106.7006 10.7745)'), 'TP. Hồ Chí Minh', 32.5, 36.2, 68, 1010, 4.2, 135, 45, 'Clouds', 'Partly cloudy', 'sensor', NOW() - INTERVAL '15 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.6978 10.7712)'), 'TP. Hồ Chí Minh', 31.8, 35.5, 70, 1011, 3.8, 140, 40, 'Clouds', 'Scattered clouds', 'sensor', NOW() - INTERVAL '15 minutes'),

-- District 3
(ST_GeogFromText('SRID=4326;POINT(106.6867 10.7834)'), 'TP. Hồ Chí Minh', 32.2, 35.9, 69, 1010, 4.0, 138, 42, 'Clouds', 'Few clouds', 'sensor', NOW() - INTERVAL '15 minutes'),

-- Bình Thạnh (HUTECH)
(ST_GeogFromText('SRID=4326;POINT(106.8067 10.8508)'), 'TP. Hồ Chí Minh', 33.1, 37.2, 65, 1009, 5.2, 125, 50, 'Clouds', 'Broken clouds', 'sensor', NOW() - INTERVAL '15 minutes'),
(ST_GeogFromText('SRID=4326;POINT(106.7089 10.8156)'), 'TP. Hồ Chí Minh', 32.8, 36.8, 66, 1009, 4.8, 130, 48, 'Clouds', 'Partly cloudy', 'sensor', NOW() - INTERVAL '15 minutes'),

-- Riverside (cooler)
(ST_GeogFromText('SRID=4326;POINT(106.7089 10.7689)'), 'TP. Hồ Chí Minh', 30.5, 33.8, 75, 1012, 6.5, 110, 30, 'Clear', 'Clear sky', 'sensor', NOW() - INTERVAL '15 minutes'),

-- University Areas
(ST_GeogFromText('SRID=4326;POINT(106.6602 10.7722)'), 'TP. Hồ Chí Minh', 32.0, 35.7, 68, 1010, 4.5, 132, 43, 'Clouds', 'Scattered clouds', 'sensor', NOW() - INTERVAL '15 minutes');
