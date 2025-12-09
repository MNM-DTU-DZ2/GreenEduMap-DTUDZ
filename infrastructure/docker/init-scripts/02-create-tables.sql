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

-- Create tables for GreenEduMap
-- This runs after PostGIS is enabled

-- Air Quality table
CREATE TABLE IF NOT EXISTS air_quality (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    aqi NUMERIC(10, 2),
    pm25 NUMERIC(10, 2),
    pm10 NUMERIC(10, 2),
    co NUMERIC(10, 2),
    no2 NUMERIC(10, 2),
    o3 NUMERIC(10, 2),
    so2 NUMERIC(10, 2),
    source VARCHAR(50) NOT NULL,
    station_name VARCHAR(255),
    station_id VARCHAR(100),
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    ngsi_ld_uri VARCHAR(500),
    measurement_date TIMESTAMPTZ NOT NULL,
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create spatial index on location
CREATE INDEX IF NOT EXISTS idx_air_quality_location ON air_quality USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_air_quality_measurement_date ON air_quality(measurement_date DESC);
CREATE INDEX IF NOT EXISTS idx_air_quality_is_public ON air_quality(is_public);

-- Weather table
CREATE TABLE IF NOT EXISTS weather (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    city_name VARCHAR(255),
    temperature NUMERIC(5, 2),
    feels_like NUMERIC(5, 2),
    humidity INTEGER,
    pressure INTEGER,
    wind_speed NUMERIC(5, 2),
    wind_direction INTEGER,
    clouds INTEGER,
    visibility INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(255),
    weather_icon VARCHAR(10),
    rain_1h NUMERIC(10, 2),
    rain_3h NUMERIC(10, 2),
    snow_1h NUMERIC(10, 2),
    snow_3h NUMERIC(10, 2),
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    ngsi_ld_uri VARCHAR(500),
    source VARCHAR(50) NOT NULL DEFAULT 'openweather',
    observation_time TIMESTAMPTZ NOT NULL,
    sunrise TIMESTAMPTZ,
    sunset TIMESTAMPTZ,
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_weather_location ON weather USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_weather_observation_time ON weather(observation_time DESC);

-- Schools table
CREATE TABLE IF NOT EXISTS schools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address VARCHAR(1000),
    city VARCHAR(255),
    district VARCHAR(255),
    type VARCHAR(50) NOT NULL,
    green_score NUMERIC(5, 2),
    total_trees INTEGER,
    green_area NUMERIC(10, 2),
    total_students INTEGER,
    total_teachers INTEGER,
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(500),
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    ngsi_ld_uri VARCHAR(500),
    facilities JSONB,
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_schools_location ON schools USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_schools_code ON schools(code);
CREATE INDEX IF NOT EXISTS idx_schools_green_score ON schools(green_score DESC);

-- Rescue Centers table
CREATE TABLE IF NOT EXISTS rescue_centers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address VARCHAR(1000),
    total_capacity INTEGER,
    current_occupancy INTEGER DEFAULT 0,
    manager_name VARCHAR(255),
    phone VARCHAR(20),
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    ngsi_ld_uri VARCHAR(500),
    facilities JSONB,
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_rescue_centers_location ON rescue_centers USING GIST(location);

-- Resources table
CREATE TABLE IF NOT EXISTS resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(500) NOT NULL,
    type VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    available_quantity INTEGER NOT NULL DEFAULT 0,
    unit VARCHAR(50) NOT NULL,
    center_id UUID REFERENCES rescue_centers(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'available',
    expiry_date TIMESTAMPTZ,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    data_uri VARCHAR(500),
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resources_center_id ON resources(center_id);
CREATE INDEX IF NOT EXISTS idx_resources_type ON resources(type);

-- Data Catalog table
CREATE TABLE IF NOT EXISTS data_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    description VARCHAR(2000),
    category VARCHAR(100) NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    api_endpoint VARCHAR(500) NOT NULL,
    download_url VARCHAR(500),
    download_formats TEXT[],
    license VARCHAR(100) DEFAULT 'MIT',
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    update_frequency VARCHAR(50),
    last_updated TIMESTAMPTZ,
    download_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    schema_fields JSONB,
    spatial_coverage JSONB,
    temporal_coverage JSONB,
    documentation_url VARCHAR(500),
    tags TEXT[],
    meta_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_data_catalog_category ON data_catalog(category);

-- Log success
DO $$
BEGIN
    RAISE NOTICE 'All tables created successfully for GreenEduMap';
END $$;
