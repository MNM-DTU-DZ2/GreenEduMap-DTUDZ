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

-- Seed data for Environment Service
-- Sample air quality and weather data for Đà Nẵng

-- Clear existing data
TRUNCATE TABLE air_quality_data CASCADE;
TRUNCATE TABLE weather_data CASCADE;

-- Air Quality Data (recent measurements)
INSERT INTO air_quality_data (location_id, location_name, latitude, longitude, aqi, pm25, pm10, co, no2, o3, so2, measured_at, data_source) VALUES
('danang_center', 'Đà Nẵng - Trung tâm', 16.0678, 108.2208, 68.5, 22.3, 45.8, 0.4, 18.2, 35.6, 8.1, NOW() - INTERVAL '1 hour', 'sensor'),
('danang_beach', 'Đà Nẵng - Bãi biển Mỹ Khê', 16.0398, 108.2435, 52.0, 15.8, 32.4, 0.3, 12.5, 28.3, 5.2, NOW() - INTERVAL '1 hour', 'sensor'),
('danang_industrial', 'Đà Nẵng - Khu công nghiệp Hòa Khánh', 16.0756, 108.1523, 95.2, 42.5, 78.9, 1.2, 28.7, 45.2, 15.8, NOW() - INTERVAL '1 hour', 'sensor'),
('danang_university', 'Đà Nẵng - Khu đại học', 16.0544, 108.2022, 58.3, 18.9, 38.5, 0.5, 15.6, 31.2, 6.8, NOW() - INTERVAL '1 hour', 'sensor'),
('danang_sontra', 'Đà Nẵng - Bán đảo Sơn Trà', 16.1083, 108.2717, 35.8, 8.2, 18.5, 0.2, 8.3, 22.5, 3.1, NOW() - INTERVAL '1 hour', 'sensor');

-- Historical data (last 24 hours)
INSERT INTO air_quality_data (location_id, location_name, latitude, longitude, aqi, pm25, pm10, co, no2, o3, so2, measured_at, data_source) 
SELECT 
    'danang_center',
    'Đà Nẵng - Trung tâm',
    16.0678,
    108.2208,
    60 + (RANDOM() * 40)::numeric(6,2),
    15 + (RANDOM() * 20)::numeric(6,2),
    30 + (RANDOM() * 40)::numeric(6,2),
    0.2 + (RANDOM() * 0.8)::numeric(6,2),
    10 + (RANDOM() * 20)::numeric(6,2),
    20 + (RANDOM() * 30)::numeric(6,2),
    5 + (RANDOM() * 10)::numeric(6,2),
    NOW() - (s || ' hours')::interval,
    'sensor'
FROM generate_series(2, 24) AS s;

INSERT INTO air_quality_data (location_id, location_name, latitude, longitude, aqi, pm25, pm10, co, no2, o3, so2, measured_at, data_source) 
SELECT 
    'danang_beach',
    'Đà Nẵng - Bãi biển Mỹ Khê',
    16.0398,
    108.2435,
    40 + (RANDOM() * 30)::numeric(6,2),
    10 + (RANDOM() * 15)::numeric(6,2),
    20 + (RANDOM() * 30)::numeric(6,2),
    0.1 + (RANDOM() * 0.5)::numeric(6,2),
    8 + (RANDOM() * 15)::numeric(6,2),
    15 + (RANDOM() * 25)::numeric(6,2),
    3 + (RANDOM() * 8)::numeric(6,2),
    NOW() - (s || ' hours')::interval,
    'sensor'
FROM generate_series(2, 24) AS s;

-- Weather Data (recent measurements)
INSERT INTO weather_data (location_id, location_name, latitude, longitude, temperature, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, measured_at, data_source) VALUES
('danang_center', 'Đà Nẵng - Trung tâm', 16.0678, 108.2208, 28.5, 75.2, 1012.5, 3.2, 120, 40, 'Clouds', 'Partly cloudy', NOW() - INTERVAL '30 minutes', 'sensor'),
('danang_beach', 'Đà Nẵng - Bãi biển Mỹ Khê', 16.0398, 108.2435, 27.8, 78.5, 1013.2, 5.8, 95, 20, 'Clear', 'Clear sky', NOW() - INTERVAL '30 minutes', 'sensor'),
('danang_sontra', 'Đà Nẵng - Bán đảo Sơn Trà', 16.1083, 108.2717, 26.5, 82.0, 1014.0, 4.5, 110, 30, 'Clouds', 'Scattered clouds', NOW() - INTERVAL '30 minutes', 'sensor'),
('danang_university', 'Đà Nẵng - Khu đại học', 16.0544, 108.2022, 28.0, 76.8, 1012.8, 2.8, 130, 35, 'Clouds', 'Few clouds', NOW() - INTERVAL '30 minutes', 'sensor'),
('danang_airport', 'Đà Nẵng - Sân bay', 16.0439, 108.1993, 29.2, 70.5, 1011.5, 6.2, 85, 15, 'Clear', 'Clear sky', NOW() - INTERVAL '30 minutes', 'sensor');

-- Historical weather data (last 24 hours)
INSERT INTO weather_data (location_id, location_name, latitude, longitude, temperature, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, measured_at, data_source)
SELECT 
    'danang_center',
    'Đà Nẵng - Trung tâm',
    16.0678,
    108.2208,
    24 + (RANDOM() * 8)::numeric(5,2),
    65 + (RANDOM() * 20)::numeric(5,2),
    1008 + (RANDOM() * 8)::numeric(7,2),
    2 + (RANDOM() * 5)::numeric(5,2),
    (RANDOM() * 360)::integer,
    (RANDOM() * 80)::integer,
    CASE WHEN RANDOM() < 0.7 THEN 'Clouds' ELSE 'Clear' END,
    CASE WHEN RANDOM() < 0.7 THEN 'Partly cloudy' ELSE 'Clear sky' END,
    NOW() - (s || ' hours')::interval,
    'sensor'
FROM generate_series(1, 24) AS s;

-- Environmental alerts (for testing alert system)
CREATE TABLE IF NOT EXISTS environmental_alerts (
    id SERIAL PRIMARY KEY,
    location_id VARCHAR(100) NOT NULL,
    location_name VARCHAR(255) NOT NULL,
    alert_type VARCHAR(50) NOT NULL, -- 'aqi_high', 'aqi_critical', 'weather_warning'
    severity VARCHAR(20) NOT NULL, -- 'warning', 'critical', 'emergency'
    message TEXT NOT NULL,
    value DECIMAL(10,2),
    threshold DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Sample alerts
INSERT INTO environmental_alerts (location_id, location_name, alert_type, severity, message, value, threshold, is_active) VALUES
('danang_industrial', 'Đà Nẵng - Khu công nghiệp Hòa Khánh', 'aqi_high', 'warning', 'Chỉ số AQI vượt ngưỡng 90, khuyến cáo hạn chế hoạt động ngoài trời', 95.2, 90.0, true),
('danang_center', 'Đà Nẵng - Trung tâm', 'pm25_moderate', 'info', 'Nồng độ PM2.5 ở mức trung bình', 22.3, 25.0, false);

-- Location metadata for mapping
CREATE TABLE IF NOT EXISTS monitoring_locations (
    id SERIAL PRIMARY KEY,
    location_id VARCHAR(100) UNIQUE NOT NULL,
    location_name VARCHAR(255) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    location GEOGRAPHY(Point, 4326),
    city VARCHAR(100) DEFAULT 'Đà Nẵng',
    district VARCHAR(100),
    location_type VARCHAR(50), -- 'urban', 'industrial', 'rural', 'coastal', 'forest'
    has_aqi_sensor BOOLEAN DEFAULT true,
    has_weather_sensor BOOLEAN DEFAULT true,
    sensor_status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'maintenance'
    installation_date DATE,
    last_maintenance DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO monitoring_locations (location_id, location_name, latitude, longitude, location, district, location_type, installation_date) VALUES
('danang_center', 'Đà Nẵng - Trung tâm', 16.0678, 108.2208, ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Hải Châu', 'urban', '2023-01-15'),
('danang_beach', 'Đà Nẵng - Bãi biển Mỹ Khê', 16.0398, 108.2435, ST_GeogFromText('SRID=4326;POINT(108.2435 16.0398)'), 'Ngũ Hành Sơn', 'coastal', '2023-02-20'),
('danang_industrial', 'Đà Nẵng - Khu công nghiệp Hòa Khánh', 16.0756, 108.1523, ST_GeogFromText('SRID=4326;POINT(108.1523 16.0756)'), 'Liên Chiểu', 'industrial', '2023-03-10'),
('danang_university', 'Đà Nẵng - Khu đại học', 16.0544, 108.2022, ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 'Hải Châu', 'urban', '2023-04-05'),
('danang_sontra', 'Đà Nẵng - Bán đảo Sơn Trà', 16.1083, 108.2717, ST_GeogFromText('SRID=4326;POINT(108.2717 16.1083)'), 'Sơn Trà', 'forest', '2023-05-12'),
('danang_airport', 'Đà Nẵng - Sân bay', 16.0439, 108.1993, ST_GeogFromText('SRID=4326;POINT(108.1993 16.0439)'), 'Hải Châu', 'urban', '2023-06-01');

