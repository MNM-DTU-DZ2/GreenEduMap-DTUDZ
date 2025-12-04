-- Simple seed data for Environment Service (matching actual schema)

-- Clear existing data
TRUNCATE TABLE air_quality CASCADE;
TRUNCATE TABLE weather CASCADE;

-- Air Quality Data (using actual schema)
INSERT INTO air_quality (location, aqi, pm25, pm10, co, no2, o3, so2, source, station_name, measurement_date) VALUES
(ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 68.5, 22.3, 45.8, 0.4, 18.2, 35.6, 8.1, 'sensor', 'Đà Nẵng - Trung tâm', NOW() - INTERVAL '1 hour'),
(ST_GeogFromText('SRID=4326;POINT(108.2435 16.0398)'), 52.0, 15.8, 32.4, 0.3, 12.5, 28.3, 5.2, 'sensor', 'Đà Nẵng - Bãi biển Mỹ Khê', NOW() - INTERVAL '1 hour'),
(ST_GeogFromText('SRID=4326;POINT(108.1523 16.0756)'), 95.2, 42.5, 78.9, 1.2, 28.7, 45.2, 15.8, 'sensor', 'Khu công nghiệp Hòa Khánh', NOW() - INTERVAL '1 hour'),
(ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 58.3, 18.9, 38.5, 0.5, 15.6, 31.2, 6.8, 'sensor', 'Khu đại học', NOW() - INTERVAL '1 hour'),
(ST_GeogFromText('SRID=4326;POINT(108.2717 16.1083)'), 35.8, 8.2, 18.5, 0.2, 8.3, 22.5, 3.1, 'sensor', 'Bán đảo Sơn Trà', NOW() - INTERVAL '1 hour');

-- Weather Data (using actual schema)
INSERT INTO weather (location, city_name, temperature, feels_like, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, source, observation_time) VALUES
(ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'), 'Đà Nẵng', 28.5, 30.2, 75, 1012, 3.2, 120, 40, 'Clouds', 'Partly cloudy', 'sensor', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(108.2435 16.0398)'), 'Đà Nẵng', 27.8, 29.5, 78, 1013, 5.8, 95, 20, 'Clear', 'Clear sky', 'sensor', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(108.2717 16.1083)'), 'Đà Nẵng', 26.5, 28.0, 82, 1014, 4.5, 110, 30, 'Clouds', 'Scattered clouds', 'sensor', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(108.2022 16.0544)'), 'Đà Nẵng', 28.0, 29.8, 76, 1012, 2.8, 130, 35, 'Clouds', 'Few clouds', 'sensor', NOW() - INTERVAL '30 minutes'),
(ST_GeogFromText('SRID=4326;POINT(108.1993 16.0439)'), 'Đà Nẵng', 29.2, 31.5, 70, 1011, 6.2, 85, 15, 'Clear', 'Clear sky', 'sensor', NOW() - INTERVAL '30 minutes');

