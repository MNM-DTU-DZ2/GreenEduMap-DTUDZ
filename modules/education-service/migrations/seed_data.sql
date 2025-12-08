--
-- GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
-- Copyright (C) 2025 DTU-DZ2 Team
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program. If not, see <https://www.gnu.org/licenses/>.
--

-- Seed data for Education Service
-- Sample schools in Đà Nẵng

-- Clear existing data
TRUNCATE TABLE green_courses CASCADE;
TRUNCATE TABLE schools CASCADE;

INSERT INTO schools (name, code, location, address, city, district, type, total_students, total_teachers, total_trees, green_area, phone, email, website, is_public, green_score) VALUES
('Đại học Duy Tân', 'DTU-DN-001', ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 'Quang Trung, Hải Châu', 'Đà Nẵng', 'Hải Châu', 'university', 15000, 800, 500, 10000, '0236 3650 403', 'contact@duytan.edu.vn', 'https://duytan.edu.vn', true, 85.5),
('THPT Phan Châu Trinh', 'PCT-DN-001', ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Phan Châu Trinh, Hải Châu', 'Đà Nẵng', 'Hải Châu', 'high', 1200, 65, 150, 2000, '0236 3821 234', 'pct@danang.edu.vn', null, true, 78.0),
('THCS Trần Quốc Toản', 'TQT-DN-001', ST_GeogFromText('SRID=4326;POINT(108.2134 16.0456)'), 'Trần Quốc Toản, Thanh Khê', 'Đà Nẵng', 'Thanh Khê', 'middle', 800, 45, 80, 1200, '0236 3654 789', 'tqt@danang.edu.vn', null, true, 72.5),
('Tiểu học Nguyễn Du', 'ND-DN-001', ST_GeogFromText('SRID=4326;POINT(108.2012 16.0567)'), 'Nguyễn Du, Hải Châu', 'Đà Nẵng', 'Hải Châu', 'elementary', 600, 35, 60, 800, '0236 3789 456', 'nd@danang.edu.vn', null, true, 68.0),
('Đại học Bách Khoa', 'BK-DN-001', ST_GeogFromText('SRID=4326;POINT(108.2145 16.0745)'), '54 Nguyễn Lương Bằng', 'Đà Nẵng', 'Liên Chiểu', 'university', 12000, 650, 400, 8000, '0236 3731 111', 'info@dut.udn.vn', 'https://dut.udn.vn', true, 82.0);

-- Sample green courses
INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public) 
SELECT 
    id,
    'Environmental Science Basics',
    'Introduction to environmental protection and sustainability',
    'environment',
    10,
    30,
    true
FROM schools WHERE code = 'DTU-DN-001';

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public)
SELECT
    id,
    'Renewable Energy Workshop',
    'Hands-on workshop about solar and wind energy',
    'energy',
    8,
    25,
    true
FROM schools WHERE code = 'BK-DN-001';

INSERT INTO green_courses (school_id, title, description, category, duration_weeks, max_students, is_public)
SELECT
    id,
    'Climate Change and Sustainability',
    'Understanding climate change impacts and sustainable solutions',
    'climate',
    12,
    40,
    true
FROM schools WHERE code = 'PCT-DN-001';

-- Sample green activities (table not created yet, skipping for now)
-- TODO: Create green_activities table in migration
