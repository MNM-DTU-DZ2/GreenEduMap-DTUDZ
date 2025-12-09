--
-- GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
-- Copyright (C) 2025 DTU-DZ2 Team
--
-- Full Demo Data Seeder - All Services
-- Run this after all migrations to populate database with demo data
--

-- ============================================
-- ENVIRONMENT SERVICE DATA
-- ============================================

-- Air Quality Sample Data
TRUNCATE TABLE air_quality CASCADE;
INSERT INTO air_quality (id, station_name, latitude, longitude, aqi, pm25, pm10, co, no2, o3, so2, measurement_time, data_source, created_at) VALUES
(gen_random_uuid(), 'Quận 1 - TPHCM', 10.7769, 106.7009, 85, 35.5, 50.2, 0.8, 25.3, 45.1, 8.2, NOW() - INTERVAL '1 hour', 'OpenAQ', NOW()),
(gen_random_uuid(), 'Quận 3 - TPHCM', 10.7863, 106.6867, 72, 28.4, 42.1, 0.6, 21.5, 38.2, 6.5, NOW() - INTERVAL '1 hour', 'OpenAQ', NOW()),
(gen_random_uuid(), 'Đà Nẵng - Hải Châu', 16.0544, 108.2022, 65, 25.1, 38.5, 0.5, 19.2, 35.4, 5.8, NOW() - INTERVAL '1 hour', 'OpenAQ', NOW()),
(gen_random_uuid(), 'Hà Nội - Hoàn Kiếm', 21.0285, 105.8542, 95, 42.3, 58.7, 1.2, 32.1, 52.3, 10.5, NOW() - INTERVAL '1 hour', 'OpenAQ', NOW()),
(gen_random_uuid(), 'Cần Thơ - Ninh Kiều', 10.0452, 105.7469, 68, 26.8, 40.2, 0.7, 20.5, 36.8, 6.2, NOW() - INTERVAL '1 hour', 'OpenAQ', NOW());

-- Weather Sample Data
TRUNCATE TABLE weather CASCADE;
INSERT INTO weather (id, city_name, latitude, longitude, temperature, feels_like, humidity, pressure, wind_speed, weather_main, weather_description, observation_time, data_source, created_at) VALUES
(gen_random_uuid(), 'Ho Chi Minh City', 10.7769, 106.7009, 32.5, 35.2, 75, 1012, 15.5, 'Clouds', 'Partly cloudy', NOW() - INTERVAL '30 minutes', 'OpenWeather', NOW()),
(gen_random_uuid(), 'Da Nang', 16.0544, 108.2022, 28.3, 30.1, 82, 1010, 12.3, 'Clear', 'Clear sky', NOW() - INTERVAL '30 minutes', 'OpenWeather', NOW()),
(gen_random_uuid(), 'Hanoi', 21.0285, 105.8542, 25.1, 26.5, 68, 1015, 8.2, 'Rain', 'Light rain', NOW() - INTERVAL '30 minutes', 'OpenWeather', NOW()),
(gen_random_uuid(), 'Can Tho', 10.0452, 105.7469, 31.2, 33.8, 78, 1011, 10.5, 'Clouds', 'Scattered clouds', NOW() - INTERVAL '30 minutes', 'OpenWeather', NOW());

SELECT 'Environment seeder completed: ' || 
       (SELECT COUNT(*) FROM air_quality) || ' AQI records, ' ||
       (SELECT COUNT(*) FROM weather) || ' weather records' as message;

-- Note: Run education and resource seeders after this
