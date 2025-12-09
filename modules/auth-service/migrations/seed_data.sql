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

-- Auth Service Demo Data Seeder
-- Creates sample users for testing and demo

-- Clear existing data
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE api_keys CASCADE;
TRUNCATE TABLE refresh_tokens CASCADE;

-- Insert demo users
-- Password for all users: password123 (bcrypt hash)
INSERT INTO users (id, email, username, password_hash, full_name, phone, role, is_active, is_verified, is_public, created_at, updated_at) VALUES
-- Admin user
(gen_random_uuid(), 'admin@greenedumap.vn', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Quản trị viên', '0901234567', 'admin', true, true, false, NOW(), NOW()),

-- Developer users
(gen_random_uuid(), 'dev@greenedumap.vn', 'developer', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Nguyễn Văn Dev', '0901234568', 'developer', true, true, false, NOW(), NOW()),

-- School users
(gen_random_uuid(), 'school1@dtu.edu.vn', 'dtu_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'ĐH Duy Tân', '0236-3650403', 'school', true, true, true, NOW(), NOW()),
(gen_random_uuid(), 'school2@ueh.edu.vn', 'ueh_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'ĐH Kinh Tế TPHCM', '028-73030000', 'school', true, true, true, NOW(), NOW()),

-- Volunteer users
(gen_random_uuid(), 'volunteer1@gmail.com', 'green_warrior', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Trần Thị Xanh', '0907654321', 'volunteer', true, true, true, NOW(), NOW()),
(gen_random_uuid(), 'volunteer2@gmail.com', 'eco_hero', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Lê Văn Tuấn', '0908765432', 'volunteer', true, true, true, NOW(), NOW()),

-- Citizen users
(gen_random_uuid(), 'citizen1@gmail.com', 'nguyen_van_a', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Nguyễn Văn A', '0909876543', 'citizen', true, true, false, NOW(), NOW()),
(gen_random_uuid(), 'citizen2@gmail.com', 'tran_thi_b', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Trần Thị B', '0909876544', 'citizen', true, true, false, NOW(), NOW()),
(gen_random_uuid(), 'citizen3@gmail.com', 'le_van_c', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Lê Văn C', '0909876545', 'citizen', true, false, false, NOW(), NOW()),
(gen_random_uuid(), 'citizen4@gmail.com', 'pham_thi_d', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIq.Nn7IOe', 'Phạm Thị D', '0909876546', 'citizen', true, true, true, NOW(), NOW());

-- Success message
SELECT 'Auth seeder completed: ' || COUNT(*) || ' users created' as message FROM users;
