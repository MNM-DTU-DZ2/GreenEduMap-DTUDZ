-- Add more historical data for ML training

-- Air Quality Data - Generate 30 days of historical data
INSERT INTO air_quality (location, aqi, pm25, pm10, co, no2, o3, so2, source, station_name, measurement_date)
SELECT 
    ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'),
    50 + (RANDOM() * 50)::numeric(10,2),
    12 + (RANDOM() * 25)::numeric(10,2),
    25 + (RANDOM() * 40)::numeric(10,2),
    0.2 + (RANDOM() * 0.8)::numeric(10,2),
    10 + (RANDOM() * 20)::numeric(10,2),
    20 + (RANDOM() * 30)::numeric(10,2),
    5 + (RANDOM() * 10)::numeric(10,2),
    'sensor',
    'Đà Nẵng - Trung tâm',
    NOW() - (s || ' hours')::interval
FROM generate_series(1, 720) AS s;  -- 30 days * 24 hours

-- More locations
INSERT INTO air_quality (location, aqi, pm25, pm10, co, no2, o3, so2, source, station_name, measurement_date)
SELECT 
    ST_GeogFromText('SRID=4326;POINT(108.2435 16.0398)'),
    35 + (RANDOM() * 40)::numeric(10,2),
    8 + (RANDOM() * 20)::numeric(10,2),
    18 + (RANDOM() * 35)::numeric(10,2),
    0.1 + (RANDOM() * 0.6)::numeric(10,2),
    8 + (RANDOM() * 15)::numeric(10,2),
    15 + (RANDOM() * 25)::numeric(10,2),
    3 + (RANDOM() * 8)::numeric(10,2),
    'sensor',
    'Đà Nẵng - Bãi biển Mỹ Khê',
    NOW() - (s || ' hours')::interval
FROM generate_series(1, 720) AS s;

INSERT INTO air_quality (location, aqi, pm25, pm10, co, no2, o3, so2, source, station_name, measurement_date)
SELECT 
    ST_GeogFromText('SRID=4326;POINT(108.1523 16.0756)'),
    80 + (RANDOM() * 60)::numeric(10,2),
    35 + (RANDOM() * 40)::numeric(10,2),
    60 + (RANDOM() * 50)::numeric(10,2),
    0.8 + (RANDOM() * 1.2)::numeric(10,2),
    20 + (RANDOM() * 30)::numeric(10,2),
    35 + (RANDOM() * 35)::numeric(10,2),
    12 + (RANDOM() * 15)::numeric(10,2),
    'sensor',
    'Khu công nghiệp Hòa Khánh',
    NOW() - (s || ' hours')::interval
FROM generate_series(1, 720) AS s;

-- Weather Data - Historical
INSERT INTO weather (location, city_name, temperature, feels_like, humidity, pressure, wind_speed, wind_direction, clouds, weather_main, weather_description, source, observation_time)
SELECT 
    ST_GeogFromText('SRID=4326;POINT(108.2208 16.0678)'),
    'Đà Nẵng',
    24 + (RANDOM() * 8)::numeric(5,2),
    26 + (RANDOM() * 8)::numeric(5,2),
    60 + (RANDOM() * 25)::integer,
    1008 + (RANDOM() * 10)::integer,
    2 + (RANDOM() * 6)::numeric(5,2),
    (RANDOM() * 360)::integer,
    (RANDOM() * 80)::integer,
    CASE WHEN RANDOM() < 0.6 THEN 'Clouds' ELSE 'Clear' END,
    CASE WHEN RANDOM() < 0.6 THEN 'Partly cloudy' ELSE 'Clear sky' END,
    'sensor',
    NOW() - (s || ' hours')::interval
FROM generate_series(1, 720) AS s;

