-- Seed data for Education Service
-- Sample schools in Đà Nẵng

INSERT INTO schools (name, code, latitude, longitude, location, address, city, district, type, total_students, total_teachers, total_trees, green_area, principal_name, phone, email, website, is_public, green_score) VALUES
('Đại học Duy Tân', 'DTU-DN-001', 16.0544, 108.2022, ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 'Quang Trung, Hải Châu', 'Đà Nẵng', 'Hải Châu', 'university', 15000, 800, 500, 10000, 'GS. TS. Lê Công Cơ', '0236 3650 403', 'contact@duytan.edu.vn', 'https://duytan.edu.vn', true, 85.5),
('THPT Phan Châu Trinh', 'PCT-DN-001', 16.0678, 108.2208, ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Phan Châu Trinh, Hải Châu', 'Đà Nẵng', 'Hải Châu', 'high', 1200, 65, 150, 2000, 'Nguyễn Văn A', '0236 3821 234', 'pct@danang.edu.vn', null, true, 78.0),
('THCS Trần Quốc Toản', 'TQT-DN-001', 16.0456, 108.2134, ST_GeogFromText('SRID=4326;POINT(108.2134 16.0456)'), 'Trần Quốc Toản, Thanh Khê', 'Đà Nẵng', 'Thanh Khê', 'middle', 800, 45, 80, 1200, 'Trần Thị B', '0236 3654 789', 'tqt@danang.edu.vn', null, true, 72.5),
('Tiểu học Nguyễn Du', 'ND-DN-001', 16.0567, 108.2012, ST_GeogFromText('SRID=4326;POINT(108.2012 16.0567)'), 'Nguyễn Du, Hải Châu', 'Đà Nẵng', 'Hải Châu', 'elementary', 600, 35, 60, 800, 'Lê Văn C', '0236 3789 456', 'nd@danang.edu.vn', null, true, 68.0),
('Đại học Bách Khoa', 'BK-DN-001', 16.0745, 108.2145, ST_GeogFromText('SRID=4326;POINT(108.2145 16.0745)'), '54 Nguyễn Lương Bằng', 'Đà Nẵng', 'Liên Chiểu', 'university', 12000, 650, 400, 8000, 'PGS. TS. Nguyễn Văn D', '0236 3731 111', 'info@dut.udn.vn', 'https://dut.udn.vn', true, 82.0);

-- Sample green courses
INSERT INTO green_courses (school_id, title, description, category, duration_hours, max_students, enrolled_students, instructor_name, start_date, status, is_public) 
SELECT 
    id,
    'Environmental Science Basics',
    'Introduction to environmental protection and sustainability',
    'environment',
    40,
    30,
    25,
    'Dr. Nguyen Thi Lan',
    NOW() + INTERVAL '7 days',
    'active',
    true
FROM schools WHERE code = 'DTU-DN-001';

INSERT INTO green_courses (school_id, title, description, category, duration_hours, max_students, enrolled_students, instructor_name, start_date, status, is_public)
SELECT
    id,
    'Renewable Energy Workshop',
    'Hands-on workshop about solar and wind energy',
    'energy',
    20,
    25,
    18,
    'Ing. Tran Van Minh',
    NOW() + INTERVAL '14 days',
    'active',
    true
FROM schools WHERE code = 'BK-DN-001';

-- Sample green activities
INSERT INTO green_activities (school_id, name, description, activity_type, activity_date, duration_hours, participants_count, trees_planted, waste_collected_kg, impact_points, status, is_public)
SELECT
    id,
    'Campus Tree Planting Day',
    'Annual tree planting event with students and faculty',
    'planting',
    NOW() - INTERVAL '30 days',
    4,
    250,
    100,
    0,
    500,
    'completed',
    true
FROM schools WHERE code = 'DTU-DN-001';

INSERT INTO green_activities (school_id, name, description, activity_type, activity_date, duration_hours, participants_count, trees_planted, waste_collected_kg, impact_points, status, is_public)
SELECT
    id,
    'Beach Cleanup Campaign',
    'Monthly beach cleanup at My Khe Beach',
    'cleanup',
    NOW() - INTERVAL '15 days',
    3,
    120,
    0,
    85.5,
    300,
    'completed',
    true
FROM schools WHERE code = 'PCT-DN-001';
