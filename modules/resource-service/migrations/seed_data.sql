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

