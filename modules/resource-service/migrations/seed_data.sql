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

-- Seed data for Resource Service
-- Sample green zones and recycling centers in Đà Nẵng

-- Create recycling_centers table if not exists
CREATE TABLE IF NOT EXISTS recycling_centers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    center_type VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(255),
    operating_hours JSONB,
    accepted_materials JSONB,
    capacity_tons_per_month NUMERIC(10, 2),
    is_active BOOLEAN DEFAULT true,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address VARCHAR(1000),
    city VARCHAR(255),
    district VARCHAR(255),
    data_uri VARCHAR(500),
    ngsi_ld_uri VARCHAR(500),
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recycling_centers_location ON recycling_centers USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_recycling_centers_code ON recycling_centers(code);

-- Clear existing data
TRUNCATE TABLE green_resources CASCADE;
TRUNCATE TABLE green_zones CASCADE;

-- Green Zones (Parks, Gardens, Forests)
INSERT INTO green_zones (name, code, zone_type, address, area_sqm, tree_count, vegetation_coverage, maintained_by, phone, facilities, is_public, location) VALUES
('Công viên Biển Đông', 'GZ-001', 'park', 'Võ Nguyên Giáp, Phước Mỹ, Sơn Trà, Đà Nẵng', 50000, 250, 85.5, 'UBND Quận Sơn Trà', '0236 3888 000', '["playground", "walking_path", "bike_lane", "wifi"]', true, ST_GeogFromText('SRID=4326;POINT(108.2430 16.0543)')),
('Công viên 29/3', 'GZ-002', 'park', '29 Tháng 3, Hải Châu, Đà Nẵng', 35000, 180, 78.3, 'UBND Quận Hải Châu', '0236 3777 000', '["lake", "fountain", "benches", "lighting"]', true, ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)')),
('Vườn Hoa Châu Á', 'GZ-003', 'garden', 'Bạch Đằng, Hải Châu, Đà Nẵng', 15000, 120, 92.0, 'Sở Xây dựng', '0236 3666 000', '["flower_garden", "photo_spot", "cafe"]', true, ST_GeogFromText('SRID=4326;POINT(108.2235 16.0612)')),
('Rừng Nguyên Sinh Bà Nà', 'GZ-004', 'forest', 'Hòa Vang, Đà Nẵng', 500000, 50000, 95.8, 'Ban Quản lý Bà Nà Hills', '0236 3991 999', '["hiking", "wildlife", "waterfall", "fresh_air"]', true, ST_GeogFromText('SRID=4326;POINT(108.0075 15.9964)')),
('Bán đảo Sơn Trà', 'GZ-005', 'forest', 'Sơn Trà, Đà Nẵng', 4400000, 380000, 96.5, 'Ban Quản lý Khu BTTN', '0236 3836 000', '["wildlife", "beach", "temple", "viewpoint"]', true, ST_GeogFromText('SRID=4326;POINT(108.2717 16.1083)')),
('Công viên APEC', 'GZ-006', 'park', 'Võ Nguyên Giáp, Phước Mỹ, Ngũ Hành Sơn, Đà Nẵng', 28000, 150, 80.2, 'UBND Quận Ngũ Hành Sơn', '0236 3955 000', '["sculpture", "lawn", "events", "parking"]', true, ST_GeogFromText('SRID=4326;POINT(108.2508 16.0311)'));

-- Green Resources (using actual schema: name, type, quantity, available_quantity, unit, zone_id, status, is_public, meta_data)
INSERT INTO green_resources (name, type, quantity, available_quantity, unit, zone_id, status, is_public, meta_data) VALUES
('Cây xanh Công viên Biển Đông', 'trees', 250, 250, 'cây', (SELECT id FROM green_zones WHERE code = 'GZ-001' LIMIT 1), 'available', true, '{"species": ["phượng", "dừa", "xanh"], "planted_year": 2015}'::jsonb),
('Ghế công cộng CV 29/3', 'bench', 50, 48, 'cái', (SELECT id FROM green_zones WHERE code = 'GZ-002' LIMIT 1), 'available', true, '{"material": "gỗ", "condition": "good"}'::jsonb),
('Thùng rác thải phân loại', 'bin', 30, 30, 'cái', (SELECT id FROM green_zones WHERE code = 'GZ-003' LIMIT 1), 'available', true, '{"types": ["recyclable", "organic", "general"], "capacity_liters": 120}'::jsonb),
('Đèn LED chiếu sáng', 'lighting', 80, 75, 'bộ', (SELECT id FROM green_zones WHERE code = 'GZ-006' LIMIT 1), 'available', true, '{"power_watts": 50, "solar_powered": true}'::jsonb),
('Hệ thống tưới tự động', 'irrigation', 5, 5, 'hệ thống', (SELECT id FROM green_zones WHERE code = 'GZ-001' LIMIT 1), 'available', true, '{"coverage_sqm": 10000, "water_source": "recycled"}'::jsonb);

-- Recycling Centers
TRUNCATE TABLE recycling_centers CASCADE;

INSERT INTO recycling_centers (name, code, center_type, phone, email, operating_hours, accepted_materials, capacity_tons_per_month, is_active, is_public, location, address, city, district) VALUES
-- Collection Points
('Điểm Thu Gom Hải Châu', 'RC-DN-001', 'collection_point', '0236 3888 111', 'haichau@greenedumap.vn', '{"monday": "7:00-17:00", "tuesday": "7:00-17:00", "wednesday": "7:00-17:00", "thursday": "7:00-17:00", "friday": "7:00-17:00", "saturday": "7:00-12:00", "sunday": "closed"}'::jsonb, '["plastic", "paper", "metal", "glass"]'::jsonb, 5.0, true, true, ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Phan Châu Trinh, Hải Châu', 'Đà Nẵng', 'Hải Châu'),

('Điểm Thu Gom Sơn Trà', 'RC-DN-002', 'collection_point', '0236 3888 112', 'sontra@greenedumap.vn', '{"monday": "6:00-18:00", "tuesday": "6:00-18:00", "wednesday": "6:00-18:00", "thursday": "6:00-18:00", "friday": "6:00-18:00", "saturday": "6:00-15:00", "sunday": "closed"}'::jsonb, '["plastic", "paper", "cardboard", "electronics"]'::jsonb, 4.5, true, true, ST_GeogFromText('SRID=4326;POINT(108.2430 16.0543)'), 'Võ Nguyên Giáp, Sơn Trà', 'Đà Nẵng', 'Sơn Trà'),

('Điểm Thu Gom Ngũ Hành Sơn', 'RC-DN-003', 'collection_point', '0236 3888 113', 'nguhanh@greenedumap.vn', '{"monday": "7:00-17:00", "tuesday": "7:00-17:00", "wednesday": "7:00-17:00", "thursday": "7:00-17:00", "friday": "7:00-17:00", "saturday": "7:00-14:00", "sunday": "closed"}'::jsonb, '["plastic", "metal", "glass", "textiles"]'::jsonb, 3.8, true, true, ST_GeogFromText('SRID=4326;POINT(108.2508 16.0311)'), 'Võ Nguyên Giáp, Ngũ Hành Sơn', 'Đà Nẵng', 'Ngũ Hành Sơn'),

-- Processing Facilities
('Nhà Máy Tái Chế Đà Nẵng', 'RC-DN-004', 'processing_facility', '0236 3777 200', 'nhamay@greenedumap.vn', '{"monday": "8:00-17:00", "tuesday": "8:00-17:00", "wednesday": "8:00-17:00", "thursday": "8:00-17:00", "friday": "8:00-17:00", "saturday": "closed", "sunday": "closed"}'::jsonb, '["plastic", "paper", "cardboard", "metal", "glass", "organic"]'::jsonb, 150.0, true, false, ST_GeogFromText('SRID=4326;POINT(108.1456 16.0234)'), 'Khu Công Nghiệp Hòa Khánh', 'Đà Nẵng', 'Liên Chiểu'),

('Trung Tâm Xử Lý Rác Thải Khánh Sơn', 'RC-DN-005', 'processing_facility', '0236 3666 300', 'khanhson@greenedumap.vn', '{"monday": "6:00-18:00", "tuesday": "6:00-18:00", "wednesday": "6:00-18:00", "thursday": "6:00-18:00", "friday": "6:00-18:00", "saturday": "6:00-12:00", "sunday": "closed"}'::jsonb, '["organic", "composting", "recycling"]'::jsonb, 200.0, true, false, ST_GeogFromText('SRID=4326;POINT(108.0912 16.1123)'), 'Hòa Ninh, Hòa Vang', 'Đà Nẵng', 'Hòa Vang'),

-- Drop-off Centers
('Trung Tâm Thu Gom Thanh Khê', 'RC-DN-006', 'drop_off_center', '0236 3555 400', 'thanhkhe@greenedumap.vn', '{"monday": "6:00-20:00", "tuesday": "6:00-20:00", "wednesday": "6:00-20:00", "thursday": "6:00-20:00", "friday": "6:00-20:00", "saturday": "6:00-18:00", "sunday": "7:00-17:00"}'::jsonb, '["plastic", "paper", "metal", "glass", "electronics", "batteries", "bulbs"]'::jsonb, 12.0, true, true, ST_GeogFromText('SRID=4326;POINT(108.2134 16.0456)'), 'Điện Biên Phủ, Thanh Khê', 'Đà Nẵng', 'Thanh Khê'),

('Trung Tâm Thu Gom Cẩm Lệ', 'RC-DN-007', 'drop_off_center', '0236 3444 500', 'camle@greenedumap.vn', '{"monday": "6:00-19:00", "tuesday": "6:00-19:00", "wednesday": "6:00-19:00", "thursday": "6:00-19:00", "friday": "6:00-19:00", "saturday": "7:00-17:00", "sunday": "7:00-15:00"}'::jsonb, '["plastic", "paper", "cardboard", "glass", "metal", "clothes"]'::jsonb, 10.0, true, true, ST_GeogFromText('SRID=4326;POINT(108.1923 16.0289)'), 'Nguyễn Lương Bằng, Cẩm Lệ', 'Đà Nẵng', 'Cẩm Lệ'),

('Eco Station Liên Chiểu', 'RC-DN-008', 'drop_off_center', '0236 3333 600', 'lienchia@greenedumap.vn', '{"monday": "6:00-20:00", "tuesday": "6:00-20:00", "wednesday": "6:00-20:00", "thursday": "6:00-20:00", "friday": "6:00-20:00", "saturday": "6:00-19:00", "sunday": "7:00-18:00"}'::jsonb, '["plastic", "paper", "electronics", "batteries", "oil", "chemicals"]'::jsonb, 8.5, true, true, ST_GeogFromText('SRID=4326;POINT(108.1745 16.0745)'), 'Nguyễn Lương Bằng, Liên Chiểu', 'Đà Nẵng', 'Liên Chiểu');

-- Summary
SELECT 'Resource seeder completed: ' ||
       (SELECT COUNT(*) FROM green_zones) || ' green zones, ' ||
       (SELECT COUNT(*) FROM green_resources) || ' resources, ' ||
       (SELECT COUNT(*) FROM recycling_centers) || ' recycling centers' as message;
