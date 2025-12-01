-- Education Service Database Schema
-- Run this after PostgreSQL + PostGIS is ready

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable PostGIS if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;

-- ========================================
-- Schools Table
-- ========================================
CREATE TABLE IF NOT EXISTS schools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    code VARCHAR UNIQUE NOT NULL,
    
    -- PostGIS Geography for location
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    address VARCHAR,
    
    -- School classification
    type VARCHAR NOT NULL CHECK (type IN ('elementary', 'middle', 'high', 'university')),
    
    -- Green score (0-100)
    green_score NUMERIC(5, 2) DEFAULT 0.0 NOT NULL CHECK (green_score >= 0 AND green_score <= 100),
    
    -- OpenData fields
    is_public BOOLEAN DEFAULT TRUE NOT NULL,
    data_uri VARCHAR,
    ngsi_ld_uri VARCHAR,
    
    -- Extensibility
    facilities JSONB,
    meta_data JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create spatial index on location
CREATE INDEX IF NOT EXISTS idx_schools_location ON schools USING GIST(location);

-- Create index on green_score for ranking queries
CREATE INDEX IF NOT EXISTS idx_schools_green_score ON schools(green_score DESC);

-- Create index on type for filtering
CREATE INDEX IF NOT EXISTS idx_schools_type ON schools(type);


-- ========================================
-- Green Courses Table
-- ========================================
CREATE TABLE IF NOT EXISTS green_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    
    title VARCHAR NOT NULL,
    description TEXT,
    category VARCHAR NOT NULL CHECK (category IN ('environment', 'energy', 'sustainability', 'recycling', 'climate', 'biodiversity')),
    
    max_students INTEGER,
    duration_weeks INTEGER,
    
    -- OpenData fields
    is_public BOOLEAN DEFAULT TRUE NOT NULL,
    
    -- Course details
    syllabus JSONB,
    meta_data JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create index on school_id for foreign key lookups
CREATE INDEX IF NOT EXISTS idx_green_courses_school_id ON green_courses(school_id);

-- Create index on category for filtering
CREATE INDEX IF NOT EXISTS idx_green_courses_category ON green_courses(category);

-- Comments for documentation
COMMENT ON TABLE schools IS 'Schools participating in green education programs';
COMMENT ON COLUMN schools.location IS 'Geographic location as PostGIS POINT (longitude, latitude)';
COMMENT ON COLUMN schools.green_score IS 'Green/sustainability score from 0 to 100';
COMMENT ON COLUMN schools.facilities IS 'JSON object containing green facilities (solar panels, gardens, etc.)';

COMMENT ON TABLE green_courses IS 'Green/environmental courses offered by schools';
COMMENT ON COLUMN green_courses.category IS 'Course category: environment, energy, sustainability, recycling, climate, biodiversity';
COMMENT ON COLUMN green_courses.syllabus IS 'JSON object containing detailed course structure';
