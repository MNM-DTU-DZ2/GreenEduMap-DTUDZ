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
TRUNCATE TABLE air_quality CASCADE;
TRUNCATE TABLE weather CASCADE;

-- Air Quality Data (recent measurements)
INSERT INTO air_quality (location, station_name, station_id, aqi, pm25, pm10, co, no2, o3, so2, source, measurement_date, is_public) VALUES
(ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Đà Nẵng - Trung tâm', 'danang_center', 68.5, 22.3, 45.8, 0.4, 18.2, 35.6, 8.1, 'sensor', NOW() - INTERVAL '1 hour', true),
(ST_GeogFromText('SRID=4326;POINT(108.2435 16.0398)'), 'Đà Nẵng - Bãi biển Mỹ Khê', 'danang_beach', 52.0, 15.8, 32.4, 0.3, 12.5, 28.3, 5.2, 'sensor', NOW() - INTERVAL '1 hour', true),
(ST_GeogFromText('SRID=4326;POINT(108.1523 16.0756)'), 'Đà Nẵng - KCN Hòa Khánh', 'danang_industrial', 95.2, 42.5, 78.9, 1.2, 28.7, 45.2, 15.8, 'sensor', NOW() - INTERVAL '1 hour', true),
(ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 'Đà Nẵng - Khu đại học', 'danang_university', 58.3, 18.9, 38.5, 0.5, 15.6, 31.2, 6.8, 'sensor', NOW() - INTERVAL '1 hour', true),
(ST_GeogFromText('SRID=4326;POINT(108.2717 16.1083)'), 'Đà Nẵng - Bán đảo Sơn Trà', 'danang_sontra', 35.8, 8.2, 18.5, 0.2, 8.3, 22.5, 3.1, 'sensor', NOW() - INTERVAL '1 hour', true);

-- Historical air quality data (last 24 hours) - simplified
INSERT INTO air_quality (location, station_name, station_id, aqi, pm25, pm10, co, no2, o3, so2, source, measurement_date, is_public) 
SELECT 
    ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'),
    'Đà Nẵng - Trung tâm',
    'danang_center',
    (60 + (RANDOM() * 40))::numeric(10,2),
    (15 + (RANDOM() * 20))::numeric(10,2),
    (30 + (RANDOM() * 40))::numeric(10,2),
    (0.2 + (RANDOM() * 0.8))::numeric(10,2),
    (10 + (RANDOM() * 20))::numeric(10,2),
    (20 + (RANDOM() * 30))::numeric(10,2),
    (5 + (RANDOM() * 10))::numeric(10,2),
    'sensor',
    NOW() - (s || ' hours')::interval,
    true
FROM generate_series(2, 12) AS s;

-- Weather Data (recent measurements)
INSERT INTO weather (location, city_name, temperature, feels_like, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, source, observation_time, is_public) VALUES
(ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Đà Nẵng', 28.5, 30.2, 75, 1012, 3.2, 120, 40, 'Clouds', 'Partly cloudy', 'sensor', NOW() - INTERVAL '30 minutes', true),
(ST_GeogFromText('SRID=4326;POINT(108.2435 16.0398)'), 'Đà Nẵng', 27.8, 29.5, 78, 1013, 5.8, 95, 20, 'Clear', 'Clear sky', 'sensor', NOW() - INTERVAL '30 minutes', true),
(ST_GeogFromText('SRID=4326;POINT(108.2717 16.1083)'), 'Đà Nẵng', 26.5, 28.0, 82, 1014, 4.5, 110, 30, 'Clouds', 'Scattered clouds', 'sensor', NOW() - INTERVAL '30 minutes', true),
(ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 'Đà Nẵng', 28.0, 29.8, 76, 1012, 2.8, 130, 35, 'Clouds', 'Few clouds', 'sensor', NOW() - INTERVAL '30 minutes', true),
(ST_GeogFromText('SRID=4326;POINT(108.1993 16.0439)'), 'Đà Nẵng', 29.2, 31.5, 70, 1011, 6.2, 85, 15, 'Clear', 'Clear sky', 'sensor', NOW() - INTERVAL '30 minutes', true);

-- Historical weather data (last 12 hours) - simplified
INSERT INTO weather (location, city_name, temperature, feels_like, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, source, observation_time, is_public)
SELECT 
    ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'),
    'Đà Nẵng',
    (24 + (RANDOM() * 8))::numeric(5,2),
    (26 + (RANDOM() * 8))::numeric(5,2),
    (65 + (RANDOM() * 20))::integer,
    (1008 + (RANDOM() * 8))::integer,
    (2 + (RANDOM() * 5))::numeric(5,2),
    (RANDOM() * 360)::integer,
    (RANDOM() * 80)::integer,
    CASE WHEN RANDOM() < 0.7 THEN 'Clouds' ELSE 'Clear' END,
    CASE WHEN RANDOM() < 0.7 THEN 'Partly cloudy' ELSE 'Clear sky' END,
    'sensor',
    NOW() - (s || ' hours')::interval,
    true
FROM generate_series(1, 12) AS s;
